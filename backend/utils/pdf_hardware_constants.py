"""
PDF Hardware Constants from "Hardware Reality" section (Page 5).

Provides constants and validation for PDF-specified hardware configurations.
"""

from enum import Enum
from typing import Dict, List, Optional


class HardwareType(str, Enum):
    """Hardware type enumeration."""
    SIM_RIG = "sim_rig"
    EDGE_KIT = "edge_kit"


class EdgeKitType(str, Enum):
    """Edge device type enumeration (PDF Page 5)."""
    JETSON_ORIN_NANO = "Jetson Orin Nano"
    JETSON_ORIN_NX = "Jetson Orin NX"
    JETSON_AGX_ORIN = "Jetson AGX Orin"


class RobotModel(str, Enum):
    """Robot model enumeration (PDF Page 5)."""
    UNITREE_GO2 = "Unitree Go2"
    UNITREE_G1 = "Unitree G1"
    PROXY = "Proxy"


class SensorModel(str, Enum):
    """Sensor model enumeration (PDF Page 5)."""
    REALSENSE_D435I = "RealSense D435i"
    REALSENSE_D455 = "RealSense D455"
    OAK_D = "OAK-D"


# PDF Page References
PDF_HARDWARE_REALITY_PAGE = 5
PDF_INFERENCE_SIM_TO_REAL_PAGE = 8


# Hardware constraints from PDF Page 5
HARDWARE_CONSTRAINTS = {
    HardwareType.SIM_RIG: {
        "min_gpu_vram_gb": 12,  # RTX 4070 Ti+ minimum
        "recommended_os": "Ubuntu 22.04",
        "use_cases": ["Simulation", "Training", "Heavy computation"],
        "description": "Workstation with high-end GPU for simulation and training",
    },
    HardwareType.EDGE_KIT: {
        "edge_devices": [e.value for e in EdgeKitType],
        "use_cases": ["Inference", "Sim-to-Real deployment"],
        "constraints": ["Resource-limited", "Power-efficient"],
        "description": "Edge device for deployment and inference (PDF Page 8)",
    },
}


# PDF Page 8: Inference/Sim-to-Real logic
INFERENCE_PRIORITIES = {
    "optimization": "resource-efficient",
    "deployment_target": "edge_device",
    "considerations": [
        "Memory constraints",
        "Power consumption",
        "Real-time performance",
        "CUDA/TensorRT optimization",
    ],
}


def get_hardware_type_description(hardware_type: HardwareType) -> str:
    """
    Get description for hardware type from PDF.
    
    Args:
        hardware_type: Hardware type
        
    Returns:
        str: Description
    """
    return HARDWARE_CONSTRAINTS.get(hardware_type, {}).get(
        "description", "Unknown hardware type"
    )


def validate_sim_rig_config(gpu_vram_gb: int) -> bool:
    """
    Validate Sim Rig configuration meets PDF Page 5 requirements.
    
    Args:
        gpu_vram_gb: GPU VRAM in GB
        
    Returns:
        bool: True if valid (>= 12GB for RTX 4070 Ti+)
    """
    return gpu_vram_gb >= HARDWARE_CONSTRAINTS[HardwareType.SIM_RIG]["min_gpu_vram_gb"]


def get_pdf_page_references(hardware_type: Optional[HardwareType] = None) -> List[int]:
    """
    Get PDF page references for hardware context.
    
    Args:
        hardware_type: Optional hardware type
        
    Returns:
        List[int]: List of relevant PDF page numbers
    """
    pages = [PDF_HARDWARE_REALITY_PAGE]  # Always include Page 5
    
    if hardware_type == HardwareType.EDGE_KIT:
        pages.append(PDF_INFERENCE_SIM_TO_REAL_PAGE)  # Add Page 8 for Edge Kit
    
    return pages


def format_hardware_context_for_prompt(
    hardware_type: str,
    gpu_model: Optional[str] = None,
    gpu_vram_gb: Optional[int] = None,
    edge_kit_type: Optional[str] = None,
    robot_model: Optional[str] = None,
    sensor_model: Optional[str] = None,
) -> str:
    """
    Format hardware profile into context string for Grok API prompt.
    
    Args:
        hardware_type: Type of hardware (sim_rig or edge_kit)
        gpu_model: GPU model name
        gpu_vram_gb: GPU VRAM in GB
        edge_kit_type: Edge device type
        robot_model: Robot model
        sensor_model: Sensor model
        
    Returns:
        str: Formatted hardware context for prompt injection
    """
    context_parts = []
    
    if hardware_type == HardwareType.SIM_RIG.value:
        context_parts.append(f"Student Hardware Profile: Sim Rig (Workstation)")
        if gpu_model:
            context_parts.append(f"- GPU: {gpu_model}")
        if gpu_vram_gb:
            context_parts.append(f"- VRAM: {gpu_vram_gb}GB")
        context_parts.append("- OS: Ubuntu 22.04 (assumed)")
        context_parts.append("- Use Case: Simulation, training, heavy computation")
        context_parts.append("- PDF Reference: Page 5 (Hardware Reality)")
        
    elif hardware_type == HardwareType.EDGE_KIT.value:
        context_parts.append(f"Student Hardware Profile: Edge Kit")
        if edge_kit_type:
            context_parts.append(f"- Device: {edge_kit_type}")
        context_parts.append("- Use Case: Inference, Sim-to-Real deployment")
        context_parts.append("- Constraints: Resource-limited, power-efficient")
        context_parts.append("- PDF Reference: Page 5 (Hardware Reality), Page 8 (Inference/Sim-to-Real)")
        context_parts.append("- Priority: Optimize for edge deployment")
    
    if robot_model:
        context_parts.append(f"- Robot: {robot_model}")
    if sensor_model:
        context_parts.append(f"- Sensor: {sensor_model}")
    
    return "\n".join(context_parts)
