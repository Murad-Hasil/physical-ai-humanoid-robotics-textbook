"""
Unit tests for Health Service.

Tests health check functions for PostgreSQL, Qdrant, and Grok API.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from services.health_service import (
    HealthStatus,
    check_postgresql_health,
    check_qdrant_health,
    check_grok_api_health,
    get_overall_health,
)


class TestHealthStatus:
    """Test HealthStatus dataclass."""

    def test_healthy_status(self):
        """Test healthy status creation."""
        status = HealthStatus(
            status="healthy",
            response_time_ms=15,
            last_checked="2026-03-18T10:30:00Z"
        )
        
        assert status.status == "healthy"
        assert status.response_time_ms == 15
        assert status.error is None

    def test_unhealthy_status(self):
        """Test unhealthy status with error."""
        status = HealthStatus(
            status="unhealthy",
            response_time_ms=5000,
            error="Connection timeout",
            last_checked="2026-03-18T10:30:00Z"
        )
        
        assert status.status == "unhealthy"
        assert status.error == "Connection timeout"


@pytest.mark.asyncio
class TestPostgreSQLHealth:
    """Test PostgreSQL health checks."""

    @patch('services.health_service.engine')
    async def test_postgresql_healthy(self, mock_engine):
        """Test PostgreSQL health check when healthy."""
        # Mock successful connection
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        
        result = await check_postgresql_health()
        
        assert result.status == "healthy"
        assert result.response_time_ms >= 0
        assert result.error is None
        assert result.last_checked is not None

    @patch('services.health_service.engine')
    async def test_postgresql_unhealthy(self, mock_engine):
        """Test PostgreSQL health check when unhealthy."""
        # Mock connection failure
        mock_engine.connect.side_effect = Exception("Connection refused")
        
        result = await check_postgresql_health()
        
        assert result.status == "unhealthy"
        assert result.error is not None
        assert "Connection refused" in result.error


@pytest.mark.asyncio
class TestQdrantHealth:
    """Test Qdrant health checks."""

    @patch('services.health_service.QdrantService')
    @patch('services.health_service.settings')
    async def test_qdrant_healthy(self, mock_settings, mock_qdrant_service_class):
        """Test Qdrant health check when healthy."""
        # Mock Qdrant service
        mock_qdrant = MagicMock()
        mock_qdrant_service_class.return_value = mock_qdrant
        mock_qdrant.get_collection_info = MagicMock(return_value={
            "points_count": 15234
        })
        mock_settings.qdrant_collection_name = "test-collection"
        
        result = await check_qdrant_health()
        
        assert result.status == "healthy"
        assert result.collection == "test-collection"
        assert result.document_count == 15234

    @patch('services.health_service.QdrantService')
    async def test_qdrant_unhealthy(self, mock_qdrant_service_class):
        """Test Qdrant health check when unhealthy."""
        # Mock Qdrant service failure
        mock_qdrant = MagicMock()
        mock_qdrant_service_class.return_value = mock_qdrant
        mock_qdrant.get_collection_info.side_effect = Exception("Connection refused")
        
        result = await check_qdrant_health()
        
        assert result.status == "unhealthy"
        assert result.error is not None


@pytest.mark.asyncio
class TestGrokAPIHealth:
    """Test Grok API health checks."""

    @patch('services.health_service.settings')
    async def test_grok_healthy(self, mock_settings):
        """Test Grok API health check when healthy."""
        mock_settings.grok_api_key = "test-key-123"
        
        result = await check_grok_api_health()
        
        assert result.status == "healthy"
        assert result.response_time_ms >= 0


@pytest.mark.asyncio
class TestOverallHealth:
    """Test overall health aggregation."""

    @patch('services.health_service.check_postgresql_health')
    @patch('services.health_service.check_qdrant_health')
    @patch('services.health_service.check_grok_api_health')
    async def test_all_healthy(self, mock_grok, mock_qdrant, mock_postgres):
        """Test overall health when all services are healthy."""
        # Mock all healthy
        mock_postgres.return_value = HealthStatus("healthy", 15)
        mock_qdrant.return_value = HealthStatus("healthy", 45)
        mock_grok.return_value = HealthStatus("healthy", 234)
        
        result = await get_overall_health()
        
        assert result["overall_status"] == "healthy"
        assert result["services"]["postgresql"]["status"] == "healthy"
        assert result["services"]["qdrant"]["status"] == "healthy"
        assert result["services"]["grok_api"]["status"] == "healthy"

    @patch('services.health_service.check_postgresql_health')
    @patch('services.health_service.check_qdrant_health')
    @patch('services.health_service.check_grok_api_health')
    async def test_one_unhealthy(self, mock_grok, mock_qdrant, mock_postgres):
        """Test overall health when one service is unhealthy."""
        # Mock one unhealthy
        mock_postgres.return_value = HealthStatus("healthy", 15)
        mock_qdrant.return_value = HealthStatus("unhealthy", 5000, error="Timeout")
        mock_grok.return_value = HealthStatus("healthy", 234)
        
        result = await get_overall_health()
        
        assert result["overall_status"] == "degraded"
        assert result["services"]["qdrant"]["status"] == "unhealthy"
        assert result["services"]["qdrant"]["error"] == "Timeout"

    @patch('services.health_service.check_postgresql_health')
    @patch('services.health_service.check_qdrant_health')
    @patch('services.health_service.check_grok_api_health')
    async def test_all_unhealthy(self, mock_grok, mock_qdrant, mock_postgres):
        """Test overall health when all services are unhealthy."""
        # Mock all unhealthy
        mock_postgres.return_value = HealthStatus("unhealthy", 5000, error="Down")
        mock_qdrant.return_value = HealthStatus("unhealthy", 5000, error="Down")
        mock_grok.return_value = HealthStatus("unhealthy", 5000, error="Down")
        
        result = await get_overall_health()
        
        assert result["overall_status"] == "unhealthy"
