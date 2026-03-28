"""
Hardware configuration service.

Provides business logic for hardware profile management.
"""

import logging
from typing import Optional

from sqlalchemy import cast, String
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.student_profile import StudentProfile, HardwareConfig
from utils.pdf_hardware_constants import (
    HardwareType, 
    validate_sim_rig_config,
    get_pdf_page_references,
)

logger = logging.getLogger(__name__)


class HardwareConfigService:
    """Service for managing hardware configurations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_config(self, user_id: str) -> Optional[HardwareConfig]:
        """
        Get hardware config for user.
        
        Args:
            user_id: User ID (as string from JWT token)
            
        Returns:
            Optional[HardwareConfig]: Hardware config or None
        """
        # Cast UUID to string for comparison (works with SQLite and PostgreSQL)
        profile = self.db.query(StudentProfile).filter(
            cast(StudentProfile.user_id, String) == user_id
        ).first()
        
        if not profile:
            return None
        
        return profile.hardware_config
    
    def update_config(
        self,
        user_id: str,
        hardware_type: str,
        gpu_model: Optional[str] = None,
        gpu_vram_gb: Optional[int] = None,
        ubuntu_version: Optional[str] = None,
        edge_kit_type: Optional[str] = None,
        jetpack_version: Optional[str] = None,
        robot_model: Optional[str] = None,
        sensor_model: Optional[str] = None,
        additional_specs: Optional[dict] = None,
    ) -> HardwareConfig:
        """
        Create or update hardware config.
        
        Args:
            user_id: User ID
            hardware_type: Type (sim_rig or edge_kit)
            gpu_model: GPU model name
            gpu_vram_gb: GPU VRAM in GB
            ubuntu_version: Ubuntu version
            edge_kit_type: Edge device type
            jetpack_version: JetPack version
            robot_model: Robot model
            sensor_model: Sensor model
            additional_specs: Additional specs as JSON
            
        Returns:
            HardwareConfig: Updated config
            
        Raises:
            HTTPException: If validation fails
        """
        # Get or create profile — cast UUID to string for SQLite/PostgreSQL compatibility
        profile = self.db.query(StudentProfile).filter(
            cast(StudentProfile.user_id, String) == user_id
        ).first()
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found",
            )
        
        # Validate Sim Rig configuration
        if hardware_type == HardwareType.SIM_RIG.value:
            if gpu_vram_gb and not validate_sim_rig_config(gpu_vram_gb):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "error": "validation_error",
                        "message": "Sim Rig requires GPU with at least 12GB VRAM (PDF Page 5)",
                    },
                )
        
        # Get or create config
        config = profile.hardware_config
        if not config:
            config = HardwareConfig(student_profile_id=profile.id)
            self.db.add(config)
        
        # Update fields
        config.hardware_type = hardware_type
        config.gpu_model = gpu_model
        config.gpu_vram_gb = gpu_vram_gb
        config.ubuntu_version = ubuntu_version
        config.edge_kit_type = edge_kit_type
        config.jetpack_version = jetpack_version
        config.robot_model = robot_model
        config.sensor_model = sensor_model
        config.additional_specs = additional_specs or {}
        
        self.db.commit()
        self.db.refresh(config)
        
        logger.info(f"Hardware config updated for user {user_id}: {hardware_type}")
        return config
    
    def get_hardware_context_for_prompt(self, user_id: str) -> Optional[str]:
        """
        Get formatted hardware context for LLM prompt.
        
        Args:
            user_id: User ID
            
        Returns:
            Optional[str]: Formatted hardware context or None
        """
        config = self.get_config(user_id)
        if not config:
            return None
        
        from utils.pdf_hardware_constants import format_hardware_context_for_prompt
        
        return format_hardware_context_for_prompt(
            hardware_type=config.hardware_type,
            gpu_model=config.gpu_model,
            gpu_vram_gb=config.gpu_vram_gb,
            edge_kit_type=config.edge_kit_type,
            robot_model=config.robot_model,
            sensor_model=config.sensor_model,
        )
