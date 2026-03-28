"""
Pydantic schemas for translation requests and responses.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime
from enum import Enum


class TranslationStatus(str, Enum):
    """Translation status enumeration."""
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    PUBLISHED = "published"


class TranslationUpdate(BaseModel):
    """Schema for updating/creating translations."""
    
    language_code: str = Field(..., description="Language code (e.g., 'ur-Latn')")
    translated_content: Optional[str] = Field(None, description="Translated content (if None, generate via AI)")
    status: Optional[TranslationStatus] = Field(None, description="Translation status")
    review_notes: Optional[str] = Field(None, max_length=1000, description="Admin review notes")
    
    class Config:
        use_enum_values = True


class TranslationResponse(BaseModel):
    """Schema for translation response."""
    
    chapter_id: str
    translated_content: str
    language_code: str
    status: str
    updated_at: str
    
    class Config:
        from_attributes = True


class TranslationStatsResponse(BaseModel):
    """Schema for translation statistics."""
    
    total_chapters: int
    translated_chapters: int
    published_chapters: int
    draft_chapters: int
    coverage_percentage: float
    by_language: Dict[str, Dict[str, int]]
