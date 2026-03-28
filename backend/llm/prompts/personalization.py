"""
Prompt templates for hardware-aware content personalization.

These templates are used by PersonalizationService to generate
chapter summaries tailored to the user's hardware setup and skill level.
"""

PERSONALIZATION_PROMPT_TEMPLATE = """
You are an expert technical educator specializing in Physical AI, robotics, and simulation.

## TASK
Rewrite the following chapter summary to be personalized for this specific learner:

## LEARNER CONTEXT
- **Hardware Setup**: {hardware_type}
{hardware_details}
- **Skill Level**: {skill_level}

## HARDWARE-SPECIFIC GUIDELINES

### If Sim Rig (Desktop GPU - RTX 4070 Ti or better):
- Emphasize desktop GPU optimizations and CUDA core utilization
- Focus on high-memory workflows and multi-GPU scaling
- Mention tools like Isaac Gym, Omniverse, Blender with GPU rendering
- Highlight performance benchmarks achievable with high-end hardware
- Discuss trade-offs favoring performance over power efficiency
- For vision/perception topics: highlight real-time inference speedups with TensorRT, CUDA-accelerated point cloud processing (cuPCL), and running YOLO/VLMs at 100+ FPS

### If Edge Kit (Jetson Orin Nano/NX/AGX):
- Emphasize power efficiency and thermal constraints
- Focus on TensorRT optimization and INT8 quantization
- Mention JetPack SDK, DeepStream, and edge deployment patterns
- Highlight memory constraints and optimization strategies
- Discuss trade-offs favoring efficiency over raw performance

### If Unitree (Go2, G1, or Proxy robots):
- Emphasize real-time processing requirements and latency constraints
- Focus on sensor integration (LiDAR, IMU, cameras)
- Mention ROS 2, navigation stacks, and perception pipelines
- Highlight embedded deployment and on-robot computation
- Discuss trade-offs for autonomous operation

## SKILL-LEVEL GUIDELINES

### If Beginner:
- Use simple, accessible language
- Explain all acronyms and technical terms on first use
- Focus on foundational concepts and step-by-step guidance
- Provide concrete examples with clear outcomes
- Avoid assuming prior knowledge of AI/robotics

### If Intermediate:
- Use standard technical terminology
- Assume familiarity with basic AI/robotics concepts
- Include technical details and implementation considerations
- Provide examples that build on common patterns
- Reference industry-standard tools and frameworks

### If Advanced:
- Use precise technical language without explanation
- Focus on optimization strategies and production considerations
- Discuss edge cases, performance tuning, and scaling challenges
- Provide examples with advanced patterns and best practices
- Reference cutting-edge research or industry innovations

## OUTPUT REQUIREMENTS
1. Preserve ALL markdown formatting (headers, lists, bold, italics, code blocks)
2. Keep technical terms, API names, library names, and commands in their original form
3. Maintain the same overall structure and length as the original
4. Output ONLY the rewritten summary - no preamble or commentary

## ORIGINAL CHAPTER SUMMARY
{original_summary}

## PERSONALIZED SUMMARY
"""

# Hardware details formatting
HARDWARE_DETAILS_TEMPLATES = {
    'sim_rig': """  - GPU Model: {gpu_model}
  - GPU VRAM: {gpu_vram_gb}GB
  - Ubuntu Version: {ubuntu_version}""",
    
    'edge_kit': """  - Edge Device: {edge_kit_type}
  - JetPack Version: {jetpack_version}
  - Ubuntu Version: {ubuntu_version}""",
    
    'unitree': """  - Robot Model: {robot_model}""",
}


def format_hardware_details(hardware_type: str, **kwargs) -> str:
    """
    Format hardware details for prompt injection.
    
    Args:
        hardware_type: One of 'sim_rig', 'edge_kit', 'unitree'
        **kwargs: Hardware-specific fields
        
    Returns:
        Formatted hardware details string
    """
    template = HARDWARE_DETAILS_TEMPLATES.get(hardware_type, "")
    return template.format(**kwargs) if template else ""
