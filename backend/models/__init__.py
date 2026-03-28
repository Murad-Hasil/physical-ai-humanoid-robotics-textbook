"""
Database models for the application.

Exports all model classes for easy importing.
"""

from models.base import BaseModel, TimestampMixin
from models.user import User
from models.student_profile import StudentProfile, HardwareConfig, CurriculumProgress, ChatSession, ChatMessage
from models.ingestion_log import IngestionLog
from models.reindex_job import ReindexJob
from models.curriculum import CurriculumWeek, Chapter, ChapterSummary, Translation

__all__ = [
    "BaseModel",
    "TimestampMixin",
    "User",
    "StudentProfile",
    "HardwareConfig",
    "CurriculumProgress",
    "ChatSession",
    "ChatMessage",
    "IngestionLog",
    "ReindexJob",
    "CurriculumWeek",
    "Chapter",
    "ChapterSummary",
    "Translation",
]
