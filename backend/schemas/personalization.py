"""
Pydantic schemas for personalization requests and responses.
"""

from pydantic import BaseModel, Field
from typing import Optional


class ChapterSummaryResponse(BaseModel):
    """Schema for personalized chapter summary response."""
    
    chapter_id: str
    summary_content: str
    hardware_profile_type: str
    skill_level: str
    generated_at: str
    
    class Config:
        from_attributes = True


class PersonalizationRegenerateRequest(BaseModel):
    """Schema for requesting summary regeneration (admin)."""
    
    hardware_profile: Optional[str] = Field(None, description="Filter by hardware profile")
    skill_level: Optional[str] = Field(None, description="Filter by skill level")
