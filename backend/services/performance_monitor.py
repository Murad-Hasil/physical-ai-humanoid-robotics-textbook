"""
Performance monitoring service for tracking API metrics.

Provides in-memory performance tracking with automatic aggregation.
"""

from collections import deque
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class RAGStepType(str, Enum):
    """RAG pipeline step types for detailed tracking."""
    EMBEDDING = "embedding"              # Query embedding generation
    SEARCH = "search"                    # Qdrant vector search
    CONTEXT_ASSEMBLY = "context_assembly" # Formatting retrieved documents
    LLM_CALL = "llm_call"                # Grok API response generation


@dataclass
class MetricSample:
    """Single performance metric sample."""
    timestamp: datetime
    endpoint: str
    method: str
    latency_ms: float
    status_code: int
    user_id: Optional[str] = None
    step_type: Optional[str] = None  # RAG step type if applicable


class PerformanceMonitor:
    """
    Singleton performance monitor for API metrics.
    
    Stores metrics in-memory with automatic eviction of old samples.
    Provides aggregated statistics (avg, p95, p99) on demand.
    """
    
    _instance: Optional['PerformanceMonitor'] = None
    _max_samples: int = 1000
    _sample_window: timedelta = timedelta(hours=1)
    
    def __new__(cls) -> 'PerformanceMonitor':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.latencies = deque(maxlen=cls._max_samples)
        return cls._instance
    
    def record_latency(
        self,
        endpoint: str,
        method: str,
        latency_ms: float,
        status_code: int,
        user_id: Optional[str] = None
    ) -> None:
        """
        Record a single request latency.

        Args:
            endpoint: API endpoint path
            method: HTTP method
            latency_ms: Request duration in milliseconds
            status_code: HTTP response status code
            user_id: User ID if authenticated
        """
        sample = MetricSample(
            timestamp=datetime.utcnow(),
            endpoint=endpoint,
            method=method,
            latency_ms=latency_ms,
            status_code=status_code,
            user_id=user_id
        )
        self.latencies.append(sample)

    def record_step_latency(
        self,
        step_name: str,
        latency_ms: float,
        endpoint: str = "rag_pipeline",
        user_id: Optional[str] = None
    ) -> None:
        """
        Record latency for a specific RAG pipeline step.

        Args:
            step_name: RAG step type (embedding, search, context_assembly, llm_call)
            latency_ms: Step duration in milliseconds
            endpoint: Endpoint that triggered the step
            user_id: User ID if authenticated
        """
        sample = MetricSample(
            timestamp=datetime.utcnow(),
            endpoint=endpoint,
            method="STEP",
            latency_ms=latency_ms,
            status_code=200,
            user_id=user_id,
            step_type=step_name
        )
        self.latencies.append(sample)
    
    def _get_recent_samples(self) -> List[MetricSample]:
        """Get samples within the time window."""
        cutoff = datetime.utcnow() - self._sample_window
        return [s for s in self.latencies if s.timestamp > cutoff]
    
    def _calculate_percentile(self, values: List[float], percentile: float) -> float:
        """Calculate percentile from a list of values."""
        if not values:
            return 0.0
        sorted_values = sorted(values)
        index = int(len(sorted_values) * percentile / 100)
        return sorted_values[min(index, len(sorted_values) - 1)]
    
    def get_metrics(self) -> Dict:
        """
        Get aggregated performance metrics.
        
        Returns:
            Dictionary with avg, p95, p99 latencies and request count
        """
        samples = self._get_recent_samples()
        
        if not samples:
            return {
                "avg_latency_ms": 0,
                "p95_latency_ms": 0,
                "p99_latency_ms": 0,
                "request_count": 0,
                "sample_window_minutes": int(self._sample_window.total_seconds() / 60)
            }
        
        latencies = [s.latency_ms for s in samples]
        
        return {
            "avg_latency_ms": round(sum(latencies) / len(latencies), 2),
            "p95_latency_ms": round(self._calculate_percentile(latencies, 95), 2),
            "p99_latency_ms": round(self._calculate_percentile(latencies, 99), 2),
            "request_count": len(samples),
            "sample_window_minutes": int(self._sample_window.total_seconds() / 60)
        }
    
    def get_metrics_by_endpoint(self, endpoint: str) -> Dict:
        """
        Get metrics for a specific endpoint.

        Args:
            endpoint: API endpoint path

        Returns:
            Dictionary with metrics for the specified endpoint
        """
        samples = [s for s in self._get_recent_samples() if s.endpoint == endpoint]

        if not samples:
            return {
                "endpoint": endpoint,
                "avg_latency_ms": 0,
                "p95_latency_ms": 0,
                "request_count": 0
            }

        latencies = [s.latency_ms for s in samples]

        return {
            "endpoint": endpoint,
            "avg_latency_ms": round(sum(latencies) / len(latencies), 2),
            "p95_latency_ms": round(self._calculate_percentile(latencies, 95), 2),
            "request_count": len(samples)
        }

    def get_metrics_by_step(self, step_name: str) -> Dict:
        """
        Get metrics for a specific RAG pipeline step.

        Args:
            step_name: RAG step type (embedding, search, context_assembly, llm_call)

        Returns:
            Dictionary with avg, p95, p99 latencies and sample count for the step
        """
        samples = [s for s in self._get_recent_samples() if s.step_type == step_name]

        if not samples:
            return {
                "step_name": step_name,
                "avg_latency_ms": 0,
                "p95_latency_ms": 0,
                "p99_latency_ms": 0,
                "sample_count": 0
            }

        latencies = [s.latency_ms for s in samples]

        return {
            "step_name": step_name,
            "avg_latency_ms": round(sum(latencies) / len(latencies), 2),
            "p95_latency_ms": round(self._calculate_percentile(latencies, 95), 2),
            "p99_latency_ms": round(self._calculate_percentile(latencies, 99), 2),
            "sample_count": len(samples)
        }
    
    def clear(self) -> None:
        """Clear all stored metrics."""
        self.latencies.clear()


# Convenience function for middleware
def get_performance_monitor() -> PerformanceMonitor:
    """Get the singleton PerformanceMonitor instance."""
    return PerformanceMonitor()
