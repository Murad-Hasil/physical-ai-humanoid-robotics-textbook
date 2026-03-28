"""
User profile API endpoints for Phase 7 - Final Intelligence.

Provides REST API for user profile and hardware configuration management.
"""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from auth.middleware import require_auth, UserContext
from models.user import User
from models.student_profile import StudentProfile, HardwareConfig
from schemas.user_profile import (
    StudentProfileUpdate,
    HardwareConfigCreate,
    UserProfileResponse,
    HardwareConfigResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["User Profiles"])


@router.get("/user-profile", response_model=UserProfileResponse)
async def get_user_profile(
    current_user: UserContext = Depends(require_auth),
    db: Session = Depends(get_db),
):
    """
    Get current user's profile with hardware configuration.
    
    Returns complete user profile including skill_level and hardware_config.
    """
    # Get student profile
    student_profile = db.query(StudentProfile).filter(
        StudentProfile.user_id == current_user.user_id
    ).first()
    
    if not student_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
    
    # Build response
    hardware_config_response = None
    if student_profile.hardware_config:
        hardware_config_response = HardwareConfigResponse(
            id=str(student_profile.hardware_config.id),
            hardware_type=student_profile.hardware_config.hardware_type,
            gpu_model=student_profile.hardware_config.gpu_model,
            gpu_vram_gb=student_profile.hardware_config.gpu_vram_gb,
            ubuntu_version=student_profile.hardware_config.ubuntu_version,
            edge_kit_type=student_profile.hardware_config.edge_kit_type,
            jetpack_version=student_profile.hardware_config.jetpack_version,
            robot_model=student_profile.hardware_config.robot_model,
            created_at=student_profile.hardware_config.created_at,
            updated_at=student_profile.hardware_config.updated_at,
        )
    
    return UserProfileResponse(
        user_id=str(current_user.user_id),
        email=current_user.email,
        skill_level=student_profile.skill_level,
        display_name=student_profile.display_name,
        hardware_config=hardware_config_response,
        created_at=student_profile.created_at,
        updated_at=student_profile.updated_at,
    )


@router.put("/user-profile", response_model=UserProfileResponse)
async def update_user_profile(
    profile_update: StudentProfileUpdate,
    current_user: UserContext = Depends(require_auth),
    db: Session = Depends(get_db),
):
    """
    Update current user's profile (skill_level, display_name, bio, timezone).
    """
    # Get student profile
    student_profile = db.query(StudentProfile).filter(
        StudentProfile.user_id == current_user.user_id
    ).first()
    
    if not student_profile:
        # Create new profile if doesn't exist
        student_profile = StudentProfile(
            user_id=current_user.user_id,
            skill_level=str(profile_update.skill_level) if profile_update.skill_level else 'beginner',
        )
        db.add(student_profile)
    else:
        # Update existing profile
        if profile_update.skill_level:
            student_profile.skill_level = str(profile_update.skill_level)
        if profile_update.display_name:
            student_profile.display_name = profile_update.display_name
        if profile_update.bio:
            student_profile.bio = profile_update.bio
        if profile_update.timezone:
            student_profile.timezone = profile_update.timezone
    
    db.commit()
    db.refresh(student_profile)
    
    logger.info(f"User profile updated for user {current_user.user_id}")
    
    # Return updated profile
    return UserProfileResponse(
        user_id=str(current_user.user_id),
        email=current_user.email,
        skill_level=student_profile.skill_level,
        display_name=student_profile.display_name,
        hardware_config=None,
        created_at=student_profile.created_at,
        updated_at=student_profile.updated_at,
    )


@router.put("/user-profile/hardware-config", response_model=HardwareConfigResponse)
async def update_hardware_config(
    hardware_data: HardwareConfigCreate,
    current_user: UserContext = Depends(require_auth),
    db: Session = Depends(get_db),
):
    """
    Create or update user's hardware configuration.
    """
    # Get student profile
    student_profile = db.query(StudentProfile).filter(
        StudentProfile.user_id == current_user.user_id
    ).first()
    
    if not student_profile:
        # Create profile first if doesn't exist
        student_profile = StudentProfile(user_id=current_user.user_id)
        db.add(student_profile)
        db.flush()  # Get ID for relationship
    
    # Get existing hardware config
    hardware_config = db.query(HardwareConfig).filter(
        HardwareConfig.student_profile_id == student_profile.id
    ).first()
    
    if hardware_config:
        # Update existing
        hardware_config.hardware_type = hardware_data.hardware_type
        hardware_config.gpu_model = hardware_data.gpu_model
        hardware_config.gpu_vram_gb = hardware_data.gpu_vram_gb
        hardware_config.ubuntu_version = hardware_data.ubuntu_version
        hardware_config.edge_kit_type = hardware_data.edge_kit_type
        hardware_config.jetpack_version = hardware_data.jetpack_version
        hardware_config.robot_model = hardware_data.robot_model
        hardware_config.additional_specs = hardware_data.additional_specs
    else:
        # Create new
        hardware_config = HardwareConfig(
            student_profile_id=student_profile.id,
            hardware_type=hardware_data.hardware_type,
            gpu_model=hardware_data.gpu_model,
            gpu_vram_gb=hardware_data.gpu_vram_gb,
            ubuntu_version=hardware_data.ubuntu_version,
            edge_kit_type=hardware_data.edge_kit_type,
            jetpack_version=hardware_data.jetpack_version,
            robot_model=hardware_data.robot_model,
            additional_specs=hardware_data.additional_specs,
        )
        db.add(hardware_config)
    
    db.commit()
    db.refresh(hardware_config)
    
    logger.info(f"Hardware config updated for user {current_user.user_id}")
    
    return HardwareConfigResponse(
        id=str(hardware_config.id),
        hardware_type=hardware_config.hardware_type,
        gpu_model=hardware_config.gpu_model,
        gpu_vram_gb=hardware_config.gpu_vram_gb,
        ubuntu_version=hardware_config.ubuntu_version,
        edge_kit_type=hardware_config.edge_kit_type,
        jetpack_version=hardware_config.jetpack_version,
        robot_model=hardware_config.robot_model,
        created_at=hardware_config.created_at,
        updated_at=hardware_config.updated_at,
    )
