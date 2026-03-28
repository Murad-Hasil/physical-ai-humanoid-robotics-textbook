"""
Reindex service for managing knowledge base re-indexing operations.

Handles background re-indexing of all files from IngestionLog entries.
"""

import logging
import asyncio
from datetime import datetime
from typing import Optional
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
import uuid

from models.reindex_job import ReindexJob
from models.ingestion_log import IngestionLog
from services.ingestion_service import IngestionService
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class ReindexService:
    """
    Service for managing re-indexing operations.
    
    Iterates through all IngestionLog entries and re-runs the
    IngestionService pipeline to repopulate Qdrant collection.
    """
    
    def __init__(self, db: Session):
        """
        Initialize reindex service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.ingestion_service = IngestionService(db)
    
    async def count_files(self) -> int:
        """
        Count total files to re-index.
        
        Returns:
            int: Number of completed ingestion logs
        """
        count = self.db.query(IngestionLog).filter(
            IngestionLog.status == "completed"
        ).count()
        logger.info(f"Found {count} files to re-index")
        return count
    
    async def start_reindex(self, user) -> ReindexJob:
        """
        Start a new re-indexing job.
        
        Args:
            user: Admin user triggering the re-index
            
        Returns:
            ReindexJob: Created job record
        """
        # Check for existing running jobs
        running_jobs = self.db.query(ReindexJob).filter(
            ReindexJob.status == "running"
        ).all()
        
        if running_jobs:
            logger.warning(f"Re-indexing job already running: {running_jobs[0].id}")
            raise ValueError("A re-indexing job is already in progress")
        
        # Count files to re-index
        total_files = await self.count_files()
        
        if total_files == 0:
            logger.warning("No files found to re-index")
            raise ValueError("No files found to re-index")
        
        # Create reindex job
        job = ReindexJob(
            status="queued",
            total_files=total_files,
            created_by_user_id=user.id
        )
        
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        
        logger.info(f"Created re-indexing job {job.id} for {total_files} files")
        
        return job
    
    async def run_reindex_background(self, job_id: uuid.UUID) -> None:
        """
        Run re-indexing as a background task.
        
        Args:
            job_id: Job ID to process
        """
        logger.info(f"Starting background re-indexing for job {job_id}")
        
        try:
            # Update job status to running
            job = self.db.query(ReindexJob).filter(ReindexJob.id == job_id).first()
            if not job:
                logger.error(f"Reindex job {job_id} not found")
                return
            
            job.status = "running"
            job.started_at = datetime.utcnow()
            self.db.commit()
            
            # Get all completed ingestion logs
            ingestion_logs = self.db.query(IngestionLog).filter(
                IngestionLog.status == "completed"
            ).order_by(IngestionLog.created_at).all()
            
            logger.info(f"Starting re-indexing of {len(ingestion_logs)} files")
            
            # Process each file
            for idx, log in enumerate(ingestion_logs, 1):
                try:
                    logger.info(f"Re-indexing file {idx}/{len(ingestion_logs)}: {log.file_name}")
                    
                    # Update progress
                    job.current_file = log.file_name
                    job.processed_files = idx - 1
                    self.db.commit()
                    
                    # Re-process the file using IngestionService
                    # Note: This re-runs the full ingestion pipeline
                    # In production, you might want to optimize this
                    await self._reindex_single_file(log)
                    
                    # Update success count
                    job.processed_files = idx
                    self.db.commit()
                    
                    logger.info(f"Successfully re-indexed {log.file_name} ({idx}/{len(ingestion_logs)})")
                    
                except Exception as e:
                    logger.error(f"Failed to re-index {log.file_name}: {e}")
                    job.failed_files += 1
                    self.db.commit()
                    # Continue with next file instead of failing entire job
            
            # Mark job as completed
            job.status = "completed"
            job.completed_at = datetime.utcnow()
            job.current_file = None
            self.db.commit()
            
            logger.info(f"Re-indexing job {job_id} completed: {job.processed_files} successful, {job.failed_files} failed")
            
        except Exception as e:
            logger.error(f"Re-indexing job {job_id} failed: {e}")
            job = self.db.query(ReindexJob).filter(ReindexJob.id == job_id).first()
            if job:
                job.status = "failed"
                job.completed_at = datetime.utcnow()
                job.current_file = None
                self.db.commit()
    
    async def _reindex_single_file(self, log: IngestionLog) -> None:
        """
        Re-index a single file from ingestion log.
        
        Args:
            log: IngestionLog entry to re-process
        """
        # Check if file still exists
        import os
        if not log.file_path or not os.path.exists(log.file_path):
            logger.warning(f"File not found for log {log.id}: {log.file_path}")
            raise FileNotFoundError(f"File not found: {log.file_name}")
        
        # Read file content
        with open(log.file_path, 'rb') as f:
            file_content = f.read()
        
        # Create a mock UploadFile for IngestionService
        from fastapi import UploadFile
        upload_file = UploadFile(
            filename=log.file_name,
            file=file_content,
            content_type=log.file_type
        )
        
        # Reset file pointer
        await upload_file.seek(0)
        
        # Get user who uploaded
        user = log.user
        if not user:
            logger.warning(f"No user found for log {log.id}")
            raise ValueError(f"User not found for file {log.file_name}")
        
        # Re-run ingestion pipeline
        # Note: This will create new Qdrant points
        # You may want to delete old points first
        await self.ingestion_service.process_upload(
            file=upload_file,
            user=user,
            temp_dir=None  # Use existing file
        )
        
        logger.debug(f"Re-indexed file {log.file_name}")
    
    def get_job_status(self, job_id: Optional[uuid.UUID] = None) -> Optional[dict]:
        """
        Get re-indexing job status.
        
        Args:
            job_id: Job ID (returns latest if None)
            
        Returns:
            dict: Job status information
        """
        if job_id:
            job = self.db.query(ReindexJob).filter(ReindexJob.id == job_id).first()
        else:
            job = self.db.query(ReindexJob).order_by(
                ReindexJob.created_at.desc()
            ).first()
        
        if not job:
            return None
        
        # Calculate progress
        percent_complete = 0
        if job.total_files > 0:
            percent_complete = int((job.processed_files / job.total_files) * 100)
        
        # Calculate timing
        elapsed_seconds = 0
        estimated_remaining_seconds = 0
        
        if job.started_at:
            if job.completed_at:
                elapsed_seconds = int((job.completed_at - job.started_at).total_seconds())
            else:
                elapsed_seconds = int((datetime.utcnow() - job.started_at).total_seconds())
                
                # Estimate remaining time based on current progress
                if job.processed_files > 0 and elapsed_seconds > 0:
                    files_per_second = job.processed_files / elapsed_seconds
                    remaining_files = job.total_files - job.processed_files
                    estimated_remaining_seconds = int(remaining_files / files_per_second)
        
        return {
            "job_id": str(job.id),
            "status": job.status,
            "progress": {
                "processed_files": job.processed_files,
                "total_files": job.total_files,
                "failed_files": job.failed_files,
                "percent_complete": percent_complete
            },
            "current_file": job.current_file,
            "timing": {
                "started_at": job.started_at.isoformat() if job.started_at else None,
                "completed_at": job.completed_at.isoformat() if job.completed_at else None,
                "elapsed_seconds": elapsed_seconds,
                "estimated_remaining_seconds": estimated_remaining_seconds
            }
        }
    
    def get_latest_job(self) -> Optional[dict]:
        """
        Get latest re-indexing job status.
        
        Returns:
            dict: Latest job status or None if no jobs exist
        """
        return self.get_job_status(job_id=None)
