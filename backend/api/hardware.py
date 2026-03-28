"""
Hardware profile API endpoints.

Provides REST API for hardware configuration management.
"""

import logging
from typing import Literal, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.session import get_db
from auth.middleware import require_auth, UserContext
from services.hardware_config_service import HardwareConfigService
from utils.pdf_hardware_constants import get_pdf_page_references

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/student", tags=["Student Profile"])


# Request/Response Models
class HardwareConfigRequest(BaseModel):
    """Hardware config request model."""
    hardware_type: Literal["sim_rig", "edge_kit"]
    gpu_model: Optional[str] = None
    gpu_vram_gb: Optional[int] = None
    ubuntu_version: Optional[str] = None
    edge_kit_type: Optional[str] = None
    jetpack_version: Optional[str] = None
    robot_model: Optional[str] = None
    sensor_model: Optional[str] = None
    additional_specs: Optional[dict] = None


class HardwareConfigResponse(BaseModel):
    """Hardware config response model."""
    id: UUID
    student_profile_id: UUID
    hardware_type: str
    gpu_model: Optional[str]
    gpu_vram_gb: Optional[int]
    ubuntu_version: Optional[str]
    edge_kit_type: Optional[str]
    jetpack_version: Optional[str]
    robot_model: Optional[str]
    sensor_model: Optional[str]
    additional_specs: Optional[dict]
    
    class Config:
        from_attributes = True


# Endpoints
@router.get("/hardware-config", response_model=HardwareConfigResponse)
async def get_hardware_config(
    user: UserContext = Depends(require_auth),
    db: Session = Depends(get_db),
):
    """
    Get current user's hardware configuration.
    
    **Requires:** Authentication
    
    **Response:**
    - Hardware configuration details
    
    **Errors:**
    - 404: No hardware config set
    """
    service = HardwareConfigService(db)
    config = service.get_config(user.user_id)
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "not_found",
                "message": "No hardware configuration found. Please set up your hardware profile.",
            },
        )
    
    return config


@router.put("/hardware-config", response_model=HardwareConfigResponse)
async def update_hardware_config(
    request: HardwareConfigRequest,
    user: UserContext = Depends(require_auth),
    db: Session = Depends(get_db),
):
    """
    Create or update hardware configuration.
    
    **Requires:** Authentication
    
    **Request:**
    - `hardware_type`: "sim_rig" or "edge_kit"
    - `gpu_model`: GPU model (for Sim Rig)
    - `gpu_vram_gb`: GPU VRAM in GB (minimum 12 for Sim Rig)
    - `edge_kit_type`: Edge device type (for Edge Kit)
    - `robot_model`: Robot model (Unitree Go2/G1/Proxy)
    - `sensor_model`: Sensor model
    
    **Response:**
    - Updated hardware configuration
    """
    service = HardwareConfigService(db)
    
    config = service.update_config(
        user_id=user.user_id,
        hardware_type=request.hardware_type,
        gpu_model=request.gpu_model,
        gpu_vram_gb=request.gpu_vram_gb,
        ubuntu_version=request.ubuntu_version,
        edge_kit_type=request.edge_kit_type,
        jetpack_version=request.jetpack_version,
        robot_model=request.robot_model,
        sensor_model=request.sensor_model,
        additional_specs=request.additional_specs,
    )
    
    return config
