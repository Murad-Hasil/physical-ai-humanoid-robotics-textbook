"""
ReindexJob model for tracking background re-indexing operations.

Tracks all re-indexing jobs triggered by admin users.
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db.session import Base
from models.base import GUID


class ReindexJob(Base):
    """
    ReindexJob model for tracking re-indexing operations.

    Attributes:
        id: Unique job identifier
        status: Job status (queued, running, completed, cancelled, failed)
        total_files: Total files to re-index
        processed_files: Files completed so far
        failed_files: Files that failed
        current_file: Currently processing file name
        started_at: Job start timestamp
        completed_at: Job end timestamp
        created_at: Job creation timestamp
        created_by_user_id: Admin who triggered the job
    """

    __tablename__ = "reindex_jobs"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    status = Column(String(50), nullable=False, default="queued", index=True)
    total_files = Column(Integer, nullable=False)
    processed_files = Column(Integer, nullable=False, default=0)
    failed_files = Column(Integer, nullable=False, default=0)
    current_file = Column(String(500), nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_by_user_id = Column(GUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    created_by_user = relationship("User")

    def __repr__(self):
        return f"<ReindexJob(id={self.id}, status={self.status}, progress={self.processed_files}/{self.total_files})>"
