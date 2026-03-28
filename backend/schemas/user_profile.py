"""
Pydantic schemas for user profile and hardware configuration.

Used for request/response validation in user profile endpoints.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class SkillLevel(str, Enum):
    """User skill level enumeration."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class HardwareType(str, Enum):
    """Hardware profile type enumeration."""
    SIM_RIG = "sim_rig"
    EDGE_KIT = "edge_kit"
    UNITREE = "unitree"


class HardwareConfigCreate(BaseModel):
    """Schema for creating/updating hardware configuration."""
    
    hardware_type: HardwareType = Field(..., description="Type of hardware setup")
    gpu_model: Optional[str] = Field(None, max_length=200, description="GPU model name")
    gpu_vram_gb: Optional[int] = Field(None, ge=1, le=128, description="GPU VRAM in GB")
    ubuntu_version: Optional[str] = Field(None, max_length=20, description="Ubuntu version")
    edge_kit_type: Optional[str] = Field(None, max_length=100, description="Edge device type")
    jetpack_version: Optional[str] = Field(None, max_length=20, description="JetPack version")
    robot_model: Optional[str] = Field(None, max_length=50, description="Robot model")
    additional_specs: Dict[str, Any] = Field(default_factory=dict, description="Additional specifications")
    
    class Config:
        use_enum_values = True


class HardwareConfigResponse(BaseModel):
    """Schema for hardware configuration response."""
    
    id: str
    hardware_type: str
    gpu_model: Optional[str]
    gpu_vram_gb: Optional[int]
    ubuntu_version: Optional[str]
    edge_kit_type: Optional[str]
    jetpack_version: Optional[str]
    robot_model: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        use_enum_values = True


class StudentProfileUpdate(BaseModel):
    """Schema for updating student profile."""
    
    skill_level: Optional[SkillLevel] = Field(None, description="User skill level")
    display_name: Optional[str] = Field(None, min_length=1, max_length=100, description="Display name")
    bio: Optional[str] = Field(None, max_length=1000, description="Biography")
    timezone: Optional[str] = Field(None, max_length=50, description="Timezone")
    
    class Config:
        use_enum_values = True


class UserProfileResponse(BaseModel):
    """Schema for complete user profile response."""
    
    user_id: str
    email: str
    skill_level: str
    display_name: Optional[str]
    hardware_config: Optional[HardwareConfigResponse]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        use_enum_values = True
