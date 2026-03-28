"""
Curriculum models for Phase 7 - Final Intelligence feature.

Models for 13-week curriculum, chapter content, personalized summaries, and translations.
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime, ForeignKey, Text, Float, JSON,
    CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import relationship

from db.session import Base
from models.base import GUID, TimestampMixin


class CurriculumWeek(Base, TimestampMixin):
    """
    Represents one week of the 13-week Physical AI curriculum.
    
    Attributes:
        week_number: Week number (1-13)
        title: Week title (e.g., "Introduction to Physical AI")
        description: Week description and learning objectives
        order: Display order (should match week_number)
        estimated_hours: Expected time commitment
        prerequisites: JSON array of prerequisite week numbers
    """
    
    __tablename__ = "curriculum_weeks"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    week_number = Column(Integer, unique=True, nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    sort_order = Column(Integer, nullable=False)  # Renamed from 'order' to avoid SQL reserved keyword
    estimated_hours = Column(Integer, nullable=True)
    prerequisites = Column(JSON, default=list)  # [1, 2] means weeks 1 and 2 are prerequisites
    
    # Relationships
    chapters = relationship(
        "Chapter",
        back_populates="curriculum_week",
        cascade="all, delete-orphan",
        order_by="Chapter.sort_order",
    )
    
    __table_args__ = (
        CheckConstraint("week_number BETWEEN 1 AND 13", name="check_week_number"),
        CheckConstraint("sort_order >= 1", name="check_sort_order_positive"),
    )
    
    def __repr__(self):
        return f"<CurriculumWeek(week={self.week_number}, title={self.title})>"


class Chapter(Base, TimestampMixin):
    """
    Represents a single chapter/lesson within a curriculum week.
    
    Attributes:
        title: Chapter title
        content: Full markdown content
        order: Display order within week
        estimated_time: Expected time to complete (e.g., "2 hours")
        tags: JSON array of topic tags
        hardware_relevant: Which hardware profiles this applies to
    """
    
    __tablename__ = "chapters"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    curriculum_week_id = Column(GUID(), ForeignKey("curriculum_weeks.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)  # Full markdown content
    sort_order = Column(Integer, nullable=False)  # Renamed from 'order'
    estimated_time = Column(String(50), nullable=True)  # e.g., "2 hours"
    tags = Column(JSON, default=list)  # ["ros2", "middleware", "fundamentals"]
    hardware_relevant = Column(JSON, default=lambda: ["sim_rig", "edge_kit"])  # Applies to which hardware
    
    # Relationships
    curriculum_week = relationship("CurriculumWeek", back_populates="chapters")
    summaries = relationship(
        "ChapterSummary",
        back_populates="chapter",
        cascade="all, delete-orphan",
    )
    translations = relationship(
        "Translation",
        back_populates="chapter",
        cascade="all, delete-orphan",
    )
    
    __table_args__ = (
        CheckConstraint("sort_order >= 1", name="check_chapter_sort_order_positive"),
        UniqueConstraint('curriculum_week_id', 'sort_order', name='unique_chapter_order_per_week'),
    )
    
    def __repr__(self):
        return f"<Chapter(title={self.title}, week={self.curriculum_week_id})>"


class ChapterSummary(Base, TimestampMixin):
    """
    Personalized chapter summary based on hardware profile and skill level.
    
    This is the cached output from the PersonalizationService.
    Generated on first request, then reused for same (chapter, hardware, skill) combination.
    
    Attributes:
        summary_content: Personalized markdown summary
        hardware_profile_type: Target hardware (sim_rig, edge_kit, unitree)
        skill_level: Target skill level (beginner, intermediate, advanced)
        generated_by: LLM model used (e.g., "grok-2")
        token_count: Tokens used for generation (for cost tracking)
    """
    
    __tablename__ = "chapter_summaries"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(GUID(), ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, index=True)
    summary_content = Column(Text, nullable=False)  # Personalized markdown
    hardware_profile_type = Column(String(20), nullable=False)  # sim_rig, edge_kit, unitree
    skill_level = Column(String(20), nullable=False)  # beginner, intermediate, advanced
    generated_by = Column(String(50), nullable=True)  # LLM model identifier
    token_count = Column(Integer, nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    chapter = relationship("Chapter", back_populates="summaries")
    
    __table_args__ = (
        UniqueConstraint(
            'chapter_id', 
            'hardware_profile_type', 
            'skill_level', 
            name='unique_summary_per_combination'
        ),
        CheckConstraint(
            "hardware_profile_type IN ('sim_rig', 'edge_kit', 'unitree')",
            name="check_hardware_profile_type"
        ),
        CheckConstraint(
            "skill_level IN ('beginner', 'intermediate', 'advanced')",
            name="check_skill_level_summary"
        ),
    )
    
    def __repr__(self):
        return f"<ChapterSummary(chapter={self.chapter_id}, hw={self.hardware_profile_type}, skill={self.skill_level})>"


class Translation(Base, TimestampMixin):
    """
    Roman Urdu translation of chapter content.
    
    Attributes:
        translated_content: Full translated markdown content
        language_code: IETF language tag (e.g., "ur-Latn" for Roman Urdu)
        status: Translation status (draft, in_review, published)
        translated_by: Source (e.g., "grok-2-ai", "human-admin")
        review_notes: Admin notes for translation quality
    """
    
    __tablename__ = "translations"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(GUID(), ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, index=True)
    translated_content = Column(Text, nullable=False)
    language_code = Column(String(20), nullable=False)  # e.g., "ur-Latn"
    status = Column(String(20), default='draft', nullable=False, index=True)  # draft, in_review, published
    translated_by = Column(String(50), nullable=True)  # "grok-2-ai" or user ID
    review_notes = Column(Text, nullable=True)
    
    # Relationships
    chapter = relationship("Chapter", back_populates="translations")
    
    __table_args__ = (
        UniqueConstraint(
            'chapter_id', 
            'language_code', 
            name='unique_translation_per_language'
        ),
        CheckConstraint(
            "status IN ('draft', 'in_review', 'published')",
            name="check_translation_status"
        ),
    )
    
    def __repr__(self):
        return f"<Translation(chapter={self.chapter_id}, lang={self.language_code}, status={self.status})>"
