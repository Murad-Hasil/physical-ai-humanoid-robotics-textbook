"""
Student profile, hardware config, curriculum progress, and chat models.

All models for Phase 3 - Auth & Personalization feature.
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime, ForeignKey, Text, Float, JSON,
    CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import relationship

from db.session import Base
from models.base import GUID


class StudentProfile(Base):
    """
    Student profile with extended information.
    
    Attributes:
        id: Unique profile identifier
        user_id: Reference to User
        display_name: Student's preferred name
        avatar_url: Profile picture URL
        bio: Student biography
        timezone: Student's timezone
        total_weeks_completed: Cached count of completed weeks
    """
    
    __tablename__ = "student_profiles"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    display_name = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    timezone = Column(String(50), default="UTC")
    skill_level = Column(String(20), default='beginner', nullable=False)
    total_weeks_completed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Constraints
    __table_args__ = (
        CheckConstraint("skill_level IN ('beginner', 'intermediate', 'advanced')", name="check_skill_level"),
    )

    # Relationships
    user = relationship("User", back_populates="profile")
    hardware_config = relationship(
        "HardwareConfig",
        back_populates="student_profile",
        uselist=False,
        cascade="all, delete-orphan",
    )
    curriculum_progress = relationship(
        "CurriculumProgress",
        back_populates="student_profile",
        cascade="all, delete-orphan",
    )
    
    def __repr__(self):
        return f"<StudentProfile(id={self.id}, user_id={self.user_id})>"


class HardwareConfig(Base):
    """
    Hardware configuration from PDF "Hardware Reality" (Page 5).
    
    Attributes:
        hardware_type: Type (sim_rig or edge_kit)
        gpu_model: GPU model name
        gpu_vram_gb: GPU VRAM in GB
        ubuntu_version: Ubuntu version
        edge_kit_type: Edge device type
        jetpack_version: JetPack version
        robot_model: Robot model
        sensor_model: Sensor model
        additional_specs: Flexible JSON field for other specs
    """
    
    __tablename__ = "hardware_configs"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    student_profile_id = Column(GUID(), ForeignKey("student_profiles.id", ondelete="CASCADE"), unique=True, nullable=False)
    hardware_type = Column(String(20), nullable=False)  # "sim_rig" or "edge_kit"
    gpu_model = Column(String(200), nullable=True)
    gpu_vram_gb = Column(Integer, nullable=True)
    ubuntu_version = Column(String(20), nullable=True)
    edge_kit_type = Column(String(100), nullable=True)
    jetpack_version = Column(String(20), nullable=True)
    robot_model = Column(String(50), nullable=True)
    sensor_model = Column(String(100), nullable=True)
    additional_specs = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    student_profile = relationship("StudentProfile", back_populates="hardware_config")
    
    # Constraints (PDF Page 5 "Hardware Reality")
    __table_args__ = (
        CheckConstraint("hardware_type IN ('sim_rig', 'edge_kit')", name="check_hardware_type"),
        CheckConstraint("edge_kit_type IN ('Jetson Orin Nano', 'Jetson Orin NX', 'Jetson AGX Orin', NULL)", name="check_edge_kit_type"),
        CheckConstraint("robot_model IN ('Unitree Go2', 'Unitree G1', 'Proxy', NULL)", name="check_robot_model"),
    )
    
    def __repr__(self):
        return f"<HardwareConfig(id={self.id}, type={self.hardware_type})>"


class CurriculumProgress(Base):
    """
    Curriculum progress tracking for Weeks 1-13.
    
    Attributes:
        week_number: Week number (1-13)
        module_id: Module identifier (e.g., "01-ros-2")
        completed_at: Completion timestamp
        score_percentage: Assessment score (0-100)
        notes: Student notes for this week
    """
    
    __tablename__ = "curriculum_progress"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    student_profile_id = Column(GUID(), ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    week_number = Column(Integer, nullable=False)
    module_id = Column(String(50), nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    score_percentage = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    student_profile = relationship("StudentProfile", back_populates="curriculum_progress")
    
    # Constraints (Weeks 1-13)
    __table_args__ = (
        CheckConstraint("week_number BETWEEN 1 AND 13", name="check_week_number"),
        CheckConstraint("score_percentage BETWEEN 0 AND 100 OR score_percentage IS NULL", name="check_score_percentage"),
        UniqueConstraint('student_profile_id', 'week_number', 'module_id', name='unique_progress_record'),
    )
    
    def __repr__(self):
        return f"<CurriculumProgress(week={self.week_number}, module={self.module_id})>"


class ChatSession(Base):
    """
    Chat session with hardware context tracking.
    
    Attributes:
        title: Session title
        hardware_context_injected: Whether hardware profile was injected
        hardware_type_at_session: Hardware type at time of session
        message_count: Cached message count
    """
    
    __tablename__ = "chat_sessions"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=True)
    hardware_context_injected = Column(Boolean, default=False)
    hardware_type_at_session = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, index=True)
    message_count = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="chat_sessions")
    messages = relationship(
        "ChatMessage",
        back_populates="chat_session",
        cascade="all, delete-orphan",
    )
    
    def __repr__(self):
        return f"<ChatSession(id={self.id}, user_id={self.user_id})>"


class ChatMessage(Base):
    """
    Individual chat message with hardware context snapshot.
    
    Attributes:
        role: Message role (user, assistant, system)
        content: Message content
        selected_text: User-selected text for context
        hardware_profile_snapshot: Hardware context at time of message
        pdf_page_references: PDF pages referenced
        sources: Source attributions
        confidence_score: RAG confidence (0.0-1.0)
        tokens_used: Token count for cost tracking
    """
    
    __tablename__ = "chat_messages"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    chat_session_id = Column(GUID(), ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    selected_text = Column(Text, nullable=True)
    hardware_profile_snapshot = Column(JSON, nullable=True)
    pdf_page_references = Column(JSON, nullable=True)
    sources = Column(JSON, nullable=True)
    confidence_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    tokens_used = Column(Integer, nullable=True)
    
    # Relationships
    chat_session = relationship("ChatSession", back_populates="messages")
    
    def __repr__(self):
        return f"<ChatMessage(id={self.id}, role={self.role})>"
