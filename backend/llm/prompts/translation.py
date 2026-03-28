"""
Prompt templates for Roman Urdu translation with technical term preservation.

These templates ensure technical terminology remains in English while
translating explanatory prose to conversational Roman Urdu.
"""

TRANSLATION_PROMPT_TEMPLATE = """
You are an expert technical translator specializing in AI, robotics, and engineering education.

## TASK
Translate the following technical content from English to Roman Urdu (Urdu written in Latin script).

## CRITICAL PRESERVATION RULES - DO NOT TRANSLATE THESE:

### 1. Code and Technical Syntax
- DO NOT translate code blocks (keep exactly as-is)
- DO NOT translate function names, class names, variable names
- DO NOT translate API endpoints, URLs, or file paths
- DO NOT translate terminal commands or shell scripts

### 2. Technical Terminology (Keep in English)
- Hardware: GPU, CPU, VRAM, RAM, SSD, CUDA cores, Tensor cores, Jetson, Orin, RTX, LiDAR, IMU
- Software/Frameworks: Python, C++, ROS, ROS 2, Docker, Kubernetes, FastAPI, React, Docusaurus, PyTorch, TensorFlow, TensorRT
- AI/ML: RAG, embeddings, vector database, Qdrant, LLM, Grok, fine-tuning, inference, training
- Robotics: SLAM, navigation, perception, planning, control, sensors, actuators, kinematics, dynamics
- File Formats: URDF, SDF, MJCF, XML, JSON, YAML, Markdown
- Commands: ros2 launch, docker run, pip install, git clone, etc.

### 3. Proper Nouns
- DO NOT translate product names (Isaac Gym, Omniverse, JetPack, DeepStream)
- DO NOT translate company names (NVIDIA, Unitree, Boston Dynamics)
- DO NOT translate project names

## TRANSLATION GUIDELINES

### What TO Translate:
- Explanatory prose and descriptions
- Tutorial instructions and step-by-step guides
- Conceptual explanations
- Examples (except code)
- Warnings, notes, and tips

### Translation Style:
- Use conversational Roman Urdu (as spoken in Pakistan/India)
- Keep sentences clear and concise
- Maintain technical accuracy
- Use common Roman Urdu words (e.g., "hai", "mein", "ko", "se", "par")
- Make it accessible for learners

### What NOT to Translate:
- Anything listed in preservation rules above
- Mathematical equations and formulas
- Figure and table labels (keep bilingual if needed)

## OUTPUT REQUIREMENTS
1. Preserve ALL markdown formatting (headers, lists, bold, italics)
2. Keep code blocks with their language tags (```python, ```bash, etc.)
3. Maintain the same structure as the original
4. Output ONLY the translation - no preamble or commentary

## CONTENT TO TRANSLATE
{content}

## ROMAN URDU TRANSLATION
"""

# Common technical terms that should NEVER be translated
TECHNICAL_TERMS_PRESERVATION = {
    # Hardware
    'GPU', 'CPU', 'VRAM', 'RAM', 'SSD', 'HDD', 'CUDA', 'Tensor Core', 'RTX', 'GTX',
    'Jetson', 'Orin', 'Nano', 'NX', 'AGX', 'LiDAR', 'IMU', 'RGB', 'Depth Camera',
    
    # Software & Frameworks
    'Python', 'C++', 'JavaScript', 'TypeScript', 'ROS', 'ROS 2', 'Docker', 'Kubernetes',
    'FastAPI', 'React', 'Docusaurus', 'PyTorch', 'TensorFlow', 'TensorRT', 'ONNX',
    'OpenCV', 'NumPy', 'Pandas', 'Matplotlib',
    
    # AI/ML
    'RAG', 'LLM', 'Grok', 'API', 'SDK', 'CLI', 'GUI', 'IDE',
    'embedding', 'vector', 'database', 'Qdrant', 'inference', 'training', 'fine-tuning',
    'model', 'neural network', 'deep learning', 'machine learning', 'AI', 'ML',
    
    # Robotics
    'URDF', 'SDF', 'MJCF', 'SLAM', 'navigation', 'perception', 'planning', 'control',
    'sensor', 'actuator', 'kinematics', 'dynamics', 'end effector', 'DOF',
    'Unitree', 'Go2', 'G1', 'Proxy', 'humanoid', 'quadruped',
    
    # Tools & Platforms
    'Isaac Gym', 'Omniverse', 'JetPack', 'DeepStream', 'CUDA Toolkit',
    'GitHub', 'GitLab', 'VS Code', 'Linux', 'Ubuntu', 'Windows', 'macOS',
    
    # Commands
    'ros2 launch', 'ros2 run', 'docker run', 'docker build', 'pip install',
    'git clone', 'git push', 'git pull', 'npm install', 'make', 'cmake',
}


def validate_translation_preservation(translation: str, original: str) -> list:
    """
    Validate that technical terms are preserved in translation.
    
    Args:
        translation: Translated text
        original: Original English text
        
    Returns:
        List of terms that were incorrectly translated
    """
    issues = []
    translation_lower = translation.lower()
    
    for term in TECHNICAL_TERMS_PRESERVATION:
        # Check if term appears in original but not in translation
        if term.lower() in original.lower():
            if term.lower() not in translation_lower and term not in translation:
                # Term might have been translated - flag for review
                issues.append(f"Term '{term}' may have been translated")
    
    return issues
