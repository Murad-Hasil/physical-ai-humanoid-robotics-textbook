"""
IngestionLog model for tracking file upload and indexing operations.

Tracks all file uploads through the admin ingestion system.
"""

import uuid
from datetime import datetime
from typing import Optional, List

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship

from db.session import Base
from models.base import GUID


class IngestionLog(Base):
    """
    IngestionLog model for tracking file uploads.

    Attributes:
        id: Unique log identifier
        user_id: Admin user who initiated upload
        file_name: Original filename
        file_path: Temporary storage path during processing
        file_size: File size in bytes
        file_type: MIME type or extension
        status: Processing status (pending, processing, completed, failed)
        chunk_count: Number of chunks indexed to Qdrant
        error_message: Error details if failed
        qdrant_point_ids: IDs of indexed chunks in Qdrant
        started_at: Processing start timestamp
        completed_at: Processing end timestamp
        created_at: Upload timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "ingestion_logs"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    file_name = Column(String(500), nullable=False)
    file_path = Column(String(1000), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default="pending", index=True)
    chunk_count = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    qdrant_point_ids = Column(Text, nullable=True)  # JSON array stored as text
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="ingestion_logs")

    def __repr__(self):
        return f"<IngestionLog(id={self.id}, file_name={self.file_name}, status={self.status})>"
