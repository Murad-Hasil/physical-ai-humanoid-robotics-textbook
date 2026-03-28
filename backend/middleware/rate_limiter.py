"""
Rate limiting middleware for API protection.

Implements token bucket rate limiting per user/IP.
"""

import logging
import time
from collections import defaultdict
from typing import Dict, Callable
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Token bucket rate limiter.
    
    Limits requests per user/IP to prevent API abuse.
    """
    
    def __init__(self, requests_per_minute: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            requests_per_minute: Maximum requests per minute
        """
        self.requests_per_minute = requests_per_minute
        self.buckets: Dict[str, Dict] = defaultdict(lambda: {
            "tokens": requests_per_minute,
            "last_update": time.time()
        })
    
    def _get_bucket_key(self, request: Request) -> str:
        """Get rate limit bucket key from request."""
        # Try to get user ID from auth header
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            # Use token hash as key (simplified - in production use actual user ID)
            return f"user:{auth_header[7:27]}"
        
        # Fallback to IP address
        client_ip = request.client.host if request.client else "unknown"
        return f"ip:{client_ip}"
    
    def _refill_tokens(self, key: str) -> None:
        """Refill tokens based on elapsed time."""
        bucket = self.buckets[key]
        now = time.time()
        elapsed = now - bucket["last_update"]
        
        # Add tokens based on elapsed time
        tokens_to_add = elapsed * (self.requests_per_minute / 60.0)
        bucket["tokens"] = min(
            self.requests_per_minute,
            bucket["tokens"] + tokens_to_add
        )
        bucket["last_update"] = now
    
    def is_allowed(self, request: Request) -> bool:
        """
        Check if request is allowed.
        
        Args:
            request: FastAPI request
            
        Returns:
            True if allowed, False if rate limited
        """
        key = self._get_bucket_key(request)
        self._refill_tokens(key)
        
        bucket = self.buckets[key]
        
        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return True
        
        return False
    
    def get_remaining(self, request: Request) -> int:
        """Get remaining requests for current window."""
        key = self._get_bucket_key(request)
        self._refill_tokens(key)
        return int(self.buckets[key]["tokens"])


# Global rate limiters
upload_limiter = RateLimiter(requests_per_minute=10)  # 10 uploads/minute
general_limiter = RateLimiter(requests_per_minute=60)  # 60 requests/minute
reindex_limiter = RateLimiter(requests_per_minute=10)  # 10 re-index operations/minute per user


async def rate_limit_dependency(request: Request, calls: int = 10) -> None:
    """
    Rate limiting dependency for FastAPI routes.
    
    Args:
        request: FastAPI request
        calls: Number of calls allowed per minute
        
    Raises:
        HTTPException: If rate limit exceeded
    """
    limiter = RateLimiter(requests_per_minute=calls)
    
    if not limiter.is_allowed(request):
        remaining = limiter.get_remaining(request)
        
        logger.warning(
            f"Rate limit exceeded for {limiter._get_bucket_key(request)}"
        )
        
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "rate_limit_exceeded",
                "message": "Too many requests. Please try again later.",
                "details": {
                    "retry_after_seconds": 60,
                    "limit": calls,
                }
            },
            headers={
                "X-RateLimit-Limit": str(calls),
                "X-RateLimit-Remaining": str(remaining),
                "Retry-After": "60",
            }
        )
