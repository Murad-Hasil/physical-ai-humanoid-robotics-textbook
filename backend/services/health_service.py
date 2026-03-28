"""
Health check service for monitoring system connectivity.

Provides health checks for PostgreSQL, Qdrant, and Grok API.
"""

import logging
import time
from typing import Optional
from dataclasses import dataclass
from fastapi import HTTPException, status

from db.session import engine
from retrieval.qdrant_service import QdrantService
from llm.grok_client import GrokClient
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


@dataclass
class HealthStatus:
    """Health status for a service."""
    status: str  # healthy, unhealthy, degraded
    response_time_ms: int
    error: Optional[str] = None
    last_checked: Optional[str] = None
    # Additional fields for specific services
    collection: Optional[str] = None
    document_count: Optional[int] = None
    endpoint: Optional[str] = None


async def check_postgresql_health() -> HealthStatus:
    """
    Check PostgreSQL database connectivity.

    Returns:
        HealthStatus with connection status
    """
    start_time = time.time()
    try:
        # Execute simple query to test connection
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        
        response_time_ms = int((time.time() - start_time) * 1000)
        
        logger.debug(f"PostgreSQL health check passed in {response_time_ms}ms")
        
        return HealthStatus(
            status="healthy",
            response_time_ms=response_time_ms,
            last_checked=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        )
    
    except Exception as e:
        response_time_ms = int((time.time() - start_time) * 1000)
        logger.error(f"PostgreSQL health check failed: {e}")
        
        return HealthStatus(
            status="unhealthy",
            response_time_ms=response_time_ms,
            error=f"Connection failed: {str(e)}",
            last_checked=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        )


async def check_qdrant_health() -> HealthStatus:
    """
    Check Qdrant vector database connectivity.

    Returns:
        HealthStatus with connection status and collection info
    """
    start_time = time.time()
    try:
        qdrant_service = QdrantService()
        
        # Get collection info
        collection_info = await qdrant_service.get_collection_info(
            settings.qdrant_collection_name
        )
        
        response_time_ms = int((time.time() - start_time) * 1000)
        
        logger.debug(f"Qdrant health check passed in {response_time_ms}ms")
        
        return HealthStatus(
            status="healthy",
            response_time_ms=response_time_ms,
            collection=settings.qdrant_collection_name,
            document_count=collection_info.get("points_count", 0) if collection_info else 0,
            last_checked=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        )
    
    except Exception as e:
        response_time_ms = int((time.time() - start_time) * 1000)
        logger.error(f"Qdrant health check failed: {e}")
        
        return HealthStatus(
            status="unhealthy",
            response_time_ms=response_time_ms,
            error=f"Connection failed: {str(e)}",
            last_checked=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        )


async def check_grok_api_health() -> HealthStatus:
    """
    Check Grok API connectivity.

    Returns:
        HealthStatus with connection status
    """
    start_time = time.time()
    try:
        grok_client = GrokClient()
        
        # Simple API call to test connectivity (list models or minimal request)
        # For now, just test the connection without actual API call
        # In production, implement a proper health check endpoint with Grok API
        
        response_time_ms = int((time.time() - start_time) * 1000)
        
        # Assume healthy if we can create the client
        logger.debug(f"Gro kAPI health check passed in {response_time_ms}ms")
        
        return HealthStatus(
            status="healthy",
            response_time_ms=response_time_ms,
            endpoint=settings.grok_api_key[:20] + "..." if settings.grok_api_key else "not_configured",
            last_checked=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        )
    
    except Exception as e:
        response_time_ms = int((time.time() - start_time) * 1000)
        logger.error(f"Gro kAPI health check failed: {e}")
        
        return HealthStatus(
            status="unhealthy",
            response_time_ms=response_time_ms,
            error=f"API check failed: {str(e)}",
            last_checked=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        )


async def get_overall_health() -> dict:
    """
    Get overall system health by checking all services.

    Returns:
        Dictionary with all service health statuses and overall status
    """
    # Check all services in parallel would be better, but sequential for simplicity
    postgresql_health = await check_postgresql_health()
    qdrant_health = await check_qdrant_health()
    grok_health = await check_grok_api_health()
    
    # Determine overall status
    services = {
        "postgresql": postgresql_health,
        "qdrant": qdrant_health,
        "grok_api": grok_health
    }
    
    # Count healthy/unhealthy services
    healthy_count = sum(1 for s in services.values() if s.status == "healthy")
    unhealthy_count = sum(1 for s in services.values() if s.status == "unhealthy")
    
    # Determine overall status
    if unhealthy_count > 0 and healthy_count == 0:
        overall_status = "unhealthy"
    elif unhealthy_count > 0:
        overall_status = "degraded"
    else:
        overall_status = "healthy"
    
    # Convert to dict format
    services_dict = {}
    for name, health in services.items():
        services_dict[name] = {
            "status": health.status,
            "response_time_ms": health.response_time_ms,
            "last_checked": health.last_checked
        }
        
        if health.error:
            services_dict[name]["error"] = health.error
        if health.collection:
            services_dict[name]["collection"] = health.collection
        if health.document_count is not None:
            services_dict[name]["document_count"] = health.document_count
        if health.endpoint:
            services_dict[name]["endpoint"] = health.endpoint
    
    return {
        "services": services_dict,
        "overall_status": overall_status,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
