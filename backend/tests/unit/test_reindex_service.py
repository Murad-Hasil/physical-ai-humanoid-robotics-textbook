"""
Unit tests for Reindex Service.

Tests re-indexing service for knowledge base management.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import uuid

from services.reindex_service import ReindexService
from models.reindex_job import ReindexJob
from models.ingestion_log import IngestionLog


class TestReindexService:
    """Test ReindexService functionality."""

    @pytest.fixture
    def mock_db(self):
        """Create mock database session."""
        db = MagicMock()
        return db

    @pytest.fixture
    def reindex_service(self, mock_db):
        """Create ReindexService instance."""
        return ReindexService(mock_db)

    @pytest.fixture
    def mock_user(self):
        """Create mock admin user."""
        user = MagicMock()
        user.id = uuid.uuid4()
        user.email = "admin@example.com"
        return user

    @pytest.fixture
    def mock_ingestion_log(self):
        """Create mock ingestion log."""
        log = MagicMock()
        log.id = uuid.uuid4()
        log.file_name = "test_file.pdf"
        log.file_path = "/tmp/test_file.pdf"
        log.file_type = "application/pdf"
        log.status = "completed"
        log.user = MagicMock()
        return log


class TestCountFiles(TestReindexService):
    """Test file counting functionality."""

    @patch('services.reindex_service.IngestionLog')
    async def test_count_files(self, mock_ingestion_log_model, mock_db):
        """Test counting files to re-index."""
        # Mock database query
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 42
        
        service = ReindexService(mock_db)
        count = await service.count_files()
        
        assert count == 42
        mock_query.count.assert_called_once()


class TestStartReindex(TestReindexService):
    """Test re-indexing start functionality."""

    @patch('services.reindex_service.IngestionLog')
    @patch('services.reindex_service.ReindexJob')
    async def test_start_reindex_success(self, mock_reindex_job_model, mock_ingestion_log_model, 
                                         mock_db, mock_user):
        """Test starting re-indexing successfully."""
        # Mock no running jobs
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = []
        
        # Mock file count
        mock_query.count.return_value = 10
        
        # Mock job creation
        mock_job = MagicMock()
        mock_job.id = uuid.uuid4()
        mock_job.status = "queued"
        mock_job.total_files = 10
        mock_reindex_job_model.return_value = mock_job
        
        service = ReindexService(mock_db)
        job = await service.start_reindex(mock_user)
        
        assert job is not None
        assert job.status == "queued"
        assert mock_db.add.called
        assert mock_db.commit.called

    @patch('services.reindex_service.ReindexJob')
    async def test_start_reindex_already_running(self, mock_reindex_job_model, mock_db, mock_user):
        """Test starting re-indexing when job already running."""
        # Mock existing running job
        mock_running_job = MagicMock()
        mock_running_job.id = uuid.uuid4()
        
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = [mock_running_job]
        
        service = ReindexService(mock_db)
        
        with pytest.raises(ValueError, match="already in progress"):
            await service.start_reindex(mock_user)

    @patch('services.reindex_service.IngestionLog')
    async def test_start_reindex_no_files(self, mock_ingestion_log_model, mock_db, mock_user):
        """Test starting re-indexing with no files."""
        # Mock no running jobs
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = []
        
        # Mock zero files
        mock_query.count.return_value = 0
        
        service = ReindexService(mock_db)
        
        with pytest.raises(ValueError, match="No files found"):
            await service.start_reindex(mock_user)


class TestGetJobStatus(TestReindexService):
    """Test job status retrieval."""

    @patch('services.reindex_service.ReindexJob')
    def test_get_job_status_by_id(self, mock_reindex_job_model, mock_db):
        """Test getting job status by ID."""
        # Mock job
        mock_job = MagicMock()
        mock_job.id = uuid.uuid4()
        mock_job.status = "running"
        mock_job.total_files = 100
        mock_job.processed_files = 45
        mock_job.failed_files = 2
        mock_job.current_file = "test.pdf"
        mock_job.started_at = datetime(2026, 3, 18, 10, 30, 0)
        mock_job.completed_at = None
        
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_job
        
        service = ReindexService(mock_db)
        status = service.get_job_status(mock_job.id)
        
        assert status is not None
        assert status["job_id"] == str(mock_job.id)
        assert status["status"] == "running"
        assert status["progress"]["processed_files"] == 45
        assert status["progress"]["total_files"] == 100
        assert status["progress"]["percent_complete"] == 45

    @patch('services.reindex_service.ReindexJob')
    def test_get_job_status_not_found(self, mock_reindex_job_model, mock_db):
        """Test getting status for non-existent job."""
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        
        service = ReindexService(mock_db)
        status = service.get_job_status(uuid.uuid4())
        
        assert status is None

    @patch('services.reindex_service.ReindexJob')
    def test_get_latest_job(self, mock_reindex_job_model, mock_db):
        """Test getting latest job."""
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.first.return_value = MagicMock()
        
        service = ReindexService(mock_db)
        status = service.get_latest_job()
        
        assert mock_query.first.called


class TestReindexJobModel:
    """Test ReindexJob model."""

    def test_job_creation(self):
        """Test creating a ReindexJob."""
        job = ReindexJob(
            status="queued",
            total_files=50,
            created_by_user_id=uuid.uuid4()
        )
        
        assert job.status == "queued"
        assert job.total_files == 50
        assert job.processed_files == 0
        assert job.failed_files == 0
        assert job.current_file is None
        assert job.id is not None

    def test_job_repr(self):
        """Test job string representation."""
        job = ReindexJob(
            status="running",
            total_files=100,
            processed_files=45,
            created_by_user_id=uuid.uuid4()
        )
        
        repr_str = repr(job)
        assert "running" in repr_str
        assert "45/100" in repr_str
