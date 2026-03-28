"""
Hardware context service for RAG personalization.

Fetches user hardware profile and formats it for LLM prompt injection.
"""

import logging
from typing import Optional

from sqlalchemy.orm import Session

from services.hardware_config_service import HardwareConfigService
from utils.pdf_hardware_constants import (
    PDF_HARDWARE_REALITY_PAGE,
    PDF_INFERENCE_SIM_TO_REAL_PAGE,
    HardwareType,
    get_pdf_page_references,
)

logger = logging.getLogger(__name__)


class HardwareContextService:
    """
    Service for injecting hardware context into LLM prompts.
    
    This service fetches the user's hardware profile and creates
    a context string that should be prepended to the Grok API prompt.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.hardware_service = HardwareConfigService(db)
    
    def get_user_context(self, user_id: str) -> Optional[dict]:
        """
        Get user hardware context.
        
        Args:
            user_id: User ID
            
        Returns:
            Optional[dict]: Hardware context dict or None
        """
        config = self.hardware_service.get_config(user_id)
        if not config:
            return None
        
        return {
            "hardware_type": config.hardware_type,
            "gpu_model": config.gpu_model,
            "gpu_vram_gb": config.gpu_vram_gb,
            "edge_kit_type": config.edge_kit_type,
            "robot_model": config.robot_model,
            "sensor_model": config.sensor_model,
            "pdf_pages": get_pdf_page_references(config.hardware_type),
        }
    
    def inject_context(self, system_prompt: str, user_id: str) -> str:
        """
        Inject hardware context into system prompt.
        
        Args:
            system_prompt: Original system prompt
            user_id: User ID
            
        Returns:
            str: Augmented system prompt with hardware context
        """
        config = self.hardware_service.get_config(user_id)
        
        if not config:
            # No hardware profile - return original prompt
            logger.info(f"No hardware profile for user {user_id}, using generic prompt")
            return system_prompt
        
        # Build hardware context string
        context_parts = [
            "<Hardware Context>",
            "Student Hardware Profile (PDF Page 5 - Hardware Reality):",
        ]
        
        if config.hardware_type == HardwareType.SIM_RIG.value:
            context_parts.extend([
                f"- Type: Sim Rig (Workstation)",
                f"- GPU: {config.gpu_model or 'High-end GPU'} ({config.gpu_vram_gb or '12'}GB VRAM)",
                f"- OS: Ubuntu 22.04 (assumed)",
                f"- Use Case: Simulation, training, heavy computation",
                f"- Guidance: Provide workstation-optimized commands",
            ])
        elif config.hardware_type == HardwareType.EDGE_KIT.value:
            context_parts.extend([
                f"- Type: Edge Kit",
                f"- Device: {config.edge_kit_type or 'Jetson Orin'}",
                f"- Use Case: Inference, Sim-to-Real deployment (PDF Page 8)",
                f"- Constraints: Resource-limited, power-efficient",
                f"- Guidance: Prioritize edge-optimized approaches, mention TensorRT/JetPack",
            ])
        
        if config.robot_model:
            context_parts.append(f"- Robot: {config.robot_model}")
        if config.sensor_model:
            context_parts.append(f"- Sensor: {config.sensor_model}")
        
        # Add PDF page references
        pdf_pages = get_pdf_page_references(config.hardware_type)
        context_parts.append(f"- PDF References: Pages {', '.join(map(str, pdf_pages))}")
        
        # Add instruction to respect textbook content
        context_parts.extend([
            "",
            "IMPORTANT: Use this hardware context to tailor your advice,",
            "but DO NOT override the textbook's specific technical steps.",
            "If the textbook provides specific instructions, follow them",
            "while adapting for the user's hardware constraints.",
            "</Hardware Context>",
        ])
        
        hardware_context = "\n".join(context_parts)
        
        # Inject context after system prompt
        augmented_prompt = f"{system_prompt}\n\n{hardware_context}"
        
        logger.info(
            f"Injected hardware context for user {user_id}: {config.hardware_type}"
        )
        
        return augmented_prompt
    
    def get_pdf_page_references(self, hardware_type: str) -> list[int]:
        """
        Get relevant PDF page references for hardware type.
        
        Args:
            hardware_type: Hardware type
            
        Returns:
            list[int]: PDF page numbers
        """
        return get_pdf_page_references(hardware_type)
