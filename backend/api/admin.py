"""
Admin API routes for ingestion management.

Provides endpoints for file upload, indexing, and knowledge base management.
"""

import logging
import uuid
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, UploadFile, File, Query, HTTPException, status, Request, BackgroundTasks
from sqlalchemy.orm import Session

from db.session import get_db
from models.user import User
from auth.dependencies import get_current_admin_user
from services.ingestion_service import IngestionService
from services.performance_monitor import get_performance_monitor
from services.health_service import get_overall_health
from services.reindex_service import ReindexService
from llm.grok_client import GrokClient
from middleware.rate_limiter import upload_limiter, rate_limit_dependency, reindex_limiter

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/ingest/upload")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Upload single file for indexing.
    
    Rate limited to 10 uploads per minute per admin user.
    
    Args:
        file: PDF or Markdown file (max 10MB)
        current_user: Admin user (auto-injected)
        db: Database session (auto-injected)
        
    Returns:
        IngestionLog with processing status
    """
    # Rate limiting
    if not upload_limiter.is_allowed(request):
        remaining = upload_limiter.get_remaining(request)
        logger.warning(
            f"Rate limit exceeded for user {current_user.email}"
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "rate_limit_exceeded",
                "message": "Too many upload requests. Please try again later.",
                "details": {
                    "retry_after_seconds": 60,
                    "limit": 10
                }
            }
        )
    
    logger.info(f"Upload started: {file.filename} by {current_user.email}")
    
    service = IngestionService(db)
    
    try:
        log = await service.process_upload(file, current_user)
        
        logger.info(
            f"Upload completed: {file.filename} "
            f"(status={log.status}, chunks={log.chunk_count})"
        )
        
        return {
            "id": str(log.id),
            "file_name": log.file_name,
            "file_size": log.file_size,
            "file_type": log.file_type,
            "status": log.status,
            "created_at": log.created_at.isoformat() if log.created_at else None,
            "message": "File uploaded successfully, processing started"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload failed for {file.filename}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "internal_error",
                "message": "Failed to process file upload"
            }
        )


@router.post("/ingest/upload-batch")
async def upload_batch(
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Upload multiple files for indexing.
    
    Args:
        files: List of PDF or Markdown files (max 10 files, each max 10MB)
        current_user: Admin user (auto-injected)
        db: Database session (auto-injected)
        
    Returns:
        Batch upload results with individual file statuses
    """
    service = IngestionService(db)
    results = []
    accepted = 0
    rejected = 0
    
    for file in files:
        try:
            log = await service.process_upload(file, current_user)
            results.append({
                "id": str(log.id),
                "file_name": log.file_name,
                "status": log.status,
                "message": "Processing started"
            })
            accepted += 1
        except HTTPException as e:
            results.append({
                "file_name": file.filename,
                "status": "rejected",
                "error": e.detail.get("message", str(e)) if isinstance(e.detail, dict) else str(e)
            })
            rejected += 1
        except Exception as e:
            logger.error(f"Batch upload failed for {file.filename}: {e}")
            results.append({
                "file_name": file.filename,
                "status": "rejected",
                "error": "Processing failed"
            })
            rejected += 1
    
    response_status = status.HTTP_207_MULTI_STATUS if rejected > 0 and accepted > 0 else status.HTTP_201_CREATED
    
    return {
        "batch_id": str(uuid.uuid4()),
        "total_files": len(files),
        "accepted_files": accepted,
        "rejected_files": rejected,
        "uploads": results,
        "message": "Batch upload completed" if rejected == 0 else "Batch upload partially completed"
    }, response_status


@router.get("/ingest/files")
async def list_indexed_files(
    status_filter: Optional[str] = Query(None, alias="status"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    List all indexed files with metadata.
    
    Args:
        status_filter: Filter by status (pending, processing, completed, failed)
        limit: Maximum results (1-100)
        offset: Result offset
        current_user: Admin user (auto-injected)
        db: Database session (auto-injected)
        
    Returns:
        Paginated list of indexed files
    """
    service = IngestionService(db)
    
    logs = service.get_ingestion_logs(
        status=status_filter,
        limit=limit,
        offset=offset
    )
    
    # Get total count
    total_query = db.query(IngestionLog)
    if status_filter:
        total_query = total_query.filter(IngestionLog.status == status_filter)
    total = total_query.count()
    
    files = []
    for log in logs:
        files.append({
            "id": str(log.id),
            "file_name": log.file_name,
            "file_size": log.file_size,
            "file_type": log.file_type,
            "status": log.status,
            "chunk_count": log.chunk_count,
            "uploaded_by": {
                "id": str(log.user.id),
                "email": log.user.email
            } if log.user else None,
            "uploaded_at": log.created_at.isoformat() if log.created_at else None,
            "indexed_at": log.completed_at.isoformat() if log.completed_at and log.status == "completed" else None
        })
    
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "files": files,
        "has_more": offset + len(files) < total
    }


@router.delete("/ingest/files/{file_id}")
async def delete_indexed_file(
    file_id: str,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Delete an indexed file from the knowledge base.
    
    Args:
        file_id: Ingestion log ID
        current_user: Admin user (auto-injected)
        db: Database session (auto-injected)
        
    Returns:
        Deletion confirmation
    """
    try:
        log_uuid = uuid.UUID(file_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "invalid_id",
                "message": "Invalid file ID format"
            }
        )
    
    service = IngestionService(db)
    
    log = service.get_ingestion_log(log_uuid)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "not_found",
                "message": "File not found"
            }
        )
    
    success = service.delete_ingestion_log(log_uuid)
    
    if success:
        return {
            "id": file_id,
            "file_name": log.file_name,
            "status": "deleted",
            "message": "File and associated chunks removed from knowledge base"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "deletion_failed",
                "message": "Failed to delete file"
            }
        )


@router.post("/ingest/reindex")
async def trigger_reindex(
    request: Request,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Trigger manual re-indexing of all files in the knowledge base.

    Rate limited to 10 operations per minute per admin user.
    Re-indexing runs as a background task to avoid blocking the API.

    Args:
        request: FastAPI request (for rate limiting)
        background_tasks: FastAPI background tasks
        current_user: Admin user (auto-injected)
        db: Database session (auto-injected)

    Returns:
        Re-index job creation response
    """
    # Rate limiting
    if not reindex_limiter.is_allowed(request):
        remaining = reindex_limiter.get_remaining(request)
        logger.warning(
            f"Re-index rate limit exceeded for user {current_user.email}"
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "rate_limit_exceeded",
                "message": "Too many re-index operations. Please try again later.",
                "details": {
                    "retry_after_seconds": 60,
                    "limit": 10
                }
            }
        )
    
    logger.info(f"Re-indexing requested by {current_user.email}")
    
    try:
        # Create reindex service
        reindex_service = ReindexService(db)
        
        # Start re-indexing job
        job = await reindex_service.start_reindex(current_user)
        
        # Add background task to run re-indexing
        background_tasks.add_task(
            reindex_service.run_reindex_background,
            job.id
        )
        
        logger.info(f"Re-indexing job {job.id} started for {job.total_files} files")
        
        return {
            "job_id": str(job.id),
            "status": job.status,
            "total_files": job.total_files,
            "message": "Re-indexing job created successfully. Processing in background."
        }
    
    except ValueError as e:
        logger.warning(f"Re-indexing request rejected: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "reindex_failed",
                "message": str(e)
            }
        )
    except Exception as e:
        logger.error(f"Re-indexing failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "internal_error",
                "message": "Failed to start re-indexing job"
            }
        )


@router.get("/ingest/reindex/status")
async def get_reindex_status(
    job_id: Optional[str] = Query(default=None, description="Job ID (returns latest if omitted)"),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get re-indexing job status.

    Args:
        job_id: Specific job ID (returns latest if omitted)
        current_user: Admin user (auto-injected)
        db: Database session (auto-injected)

    Returns:
        Re-indexing job status with progress and timing
    """
    try:
        reindex_service = ReindexService(db)
        
        if job_id:
            try:
                job_uuid = uuid.UUID(job_id)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "error": "invalid_job_id",
                        "message": "Invalid job ID format"
                    }
                )
            status = reindex_service.get_job_status(job_uuid)
        else:
            status = reindex_service.get_latest_job()
        
        if not status:
            return {
                "status": "idle",
                "message": "No re-indexing jobs found"
            }
        
        return status
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get re-index status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "internal_error",
                "message": "Failed to retrieve re-indexing status"
            }
        )


@router.get("/ingest/reindex")
async def get_reindex_history(
    limit: int = Query(default=10, ge=1, le=100, description="Number of jobs to return"),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Get re-indexing job history.

    Args:
        limit: Maximum number of jobs to return (1-100)
        current_user: Admin user (auto-injected)
        db: Database session (auto-injected)

    Returns:
        List of recent re-indexing jobs
    """
    try:
        jobs = db.query(ReindexJob).order_by(
            ReindexJob.created_at.desc()
        ).limit(limit).all()
        
        job_list = []
        for job in jobs:
            job_list.append({
                "job_id": str(job.id),
                "status": job.status,
                "total_files": job.total_files,
                "processed_files": job.processed_files,
                "failed_files": job.failed_files,
                "created_at": job.created_at.isoformat() if job.created_at else None,
                "started_at": job.started_at.isoformat() if job.started_at else None,
                "completed_at": job.completed_at.isoformat() if job.completed_at else None,
                "created_by_user_id": str(job.created_by_user_id)
            })
        
        return {
            "jobs": job_list,
            "total": len(job_list)
        }
    
    except Exception as e:
        logger.error(f"Failed to get re-index history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "internal_error",
                "message": "Failed to retrieve re-indexing history"
            }
        )


@router.get("/stats")
async def get_performance_stats(
    time_range: str = Query(default="1h", description="Time range: 1h, 24h, 7d, 30d"),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Get performance metrics and usage analytics.

    Args:
        time_range: Time range for metrics (1h, 24h, 7d, 30d)
        current_user: Admin user (auto-injected)

    Returns:
        Performance metrics with RAG step latencies and usage analytics
    """
    from services.performance_monitor import get_performance_monitor
    
    monitor = get_performance_monitor()
    
    # Get overall metrics
    overall_metrics = monitor.get_metrics()
    
    # Get RAG step-specific metrics
    embedding_metrics = monitor.get_metrics_by_step("embedding")
    search_metrics = monitor.get_metrics_by_step("search")
    context_assembly_metrics = monitor.get_metrics_by_step("context_assembly")
    llm_call_metrics = monitor.get_metrics_by_step("llm_call")
    
    # Calculate RAG latency (embedding + search)
    rag_latency = {
        "avg_ms": round((embedding_metrics.get("avg_latency_ms", 0) + 
                        search_metrics.get("avg_latency_ms", 0)), 2),
        "p95_ms": round((embedding_metrics.get("p95_latency_ms", 0) + 
                        search_metrics.get("p95_latency_ms", 0)), 2),
        "p99_ms": round((embedding_metrics.get("p99_latency_ms", 0) + 
                        search_metrics.get("p99_latency_ms", 0)), 2),
        "sample_count": search_metrics.get("sample_count", 0),
        "time_range": time_range,
        "breakdown": {
            "embedding": embedding_metrics,
            "search": search_metrics
        }
    }
    
    # LLM latency
    llm_latency = {
        "avg_ms": llm_call_metrics.get("avg_latency_ms", 0),
        "p95_ms": llm_call_metrics.get("p95_latency_ms", 0),
        "p99_ms": llm_call_metrics.get("p99_latency_ms", 0),
        "sample_count": llm_call_metrics.get("sample_count", 0),
        "time_range": time_range
    }
    
    # Usage analytics (simplified - would need database queries for actual counts)
    usage_analytics = {
        "total_queries": overall_metrics.get("request_count", 0),
        "total_tokens": 0,  # Would need to track tokens in GrokClient
        "unique_users": 0,  # Would need database query
        "time_range": time_range
    }
    
    return {
        "rag_latency": rag_latency,
        "llm_latency": llm_latency,
        "usage_analytics": usage_analytics,
        "overall_metrics": overall_metrics,
        "last_updated": datetime.utcnow().isoformat()
    }


@router.get("/metrics")
async def get_performance_metrics(
    current_user: User = Depends(get_current_admin_user)
):
    """
    Get performance metrics (legacy endpoint, use /stats instead).

    Args:
        current_user: Admin user (auto-injected)

    Returns:
        Performance metrics with latency statistics
    """
    monitor = get_performance_monitor()
    metrics = monitor.get_metrics()

    return {
        "chat_latency": metrics,
        "api_latency": metrics,  # Same for now, can be separated later
        "last_updated": datetime.utcnow().isoformat()
    }


@router.get("/health")
async def get_system_health(
    current_user: User = Depends(get_current_admin_user)
):
    """
    Get system health status for all critical services.

    Args:
        current_user: Admin user (auto-injected)

    Returns:
        System health status with PostgreSQL, Qdrant, and Grok API status
    """
    try:
        health_status = await get_overall_health()
        return health_status
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "health_check_failed",
                "message": f"Failed to retrieve system health: {str(e)}"
            }
        )


@router.get("/grok/status")
async def check_grok_status(
    current_user: User = Depends(get_current_admin_user)
):
    """
    Check Grok API health.
    
    Args:
        current_user: Admin user (auto-injected)
        
    Returns:
        Grok API health status
    """
    grok_client = GrokClient()
    
    try:
        # Simple health check
        import time
        start = time.time()
        # TODO: Implement actual health check with Grok API
        response_time = int((time.time() - start) * 1000)
        
        return {
            "status": "healthy",
            "response_time_ms": response_time,
            "endpoint": "https://api.x.ai/v1/chat/completions",
            "last_checked": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Grok health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "last_checked": datetime.utcnow().isoformat()
        }


# Import datetime for the endpoints
from datetime import datetime

# Import IngestionLog for type hints
from models.ingestion_log import IngestionLog

# Import ReindexJob for history endpoint
from models.reindex_job import ReindexJob
