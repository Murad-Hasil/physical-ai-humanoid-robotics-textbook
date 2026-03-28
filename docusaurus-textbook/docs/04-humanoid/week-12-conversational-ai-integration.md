---
id: week-12-conversational-ai-integration
title: Week 12 - Conversational AI Integration
sidebar_label: Week 12 - Conversational AI Integration
sidebar_position: 12
description: Integrate large language models and vision-language models for natural human-robot interaction
---

# Week 12 - Conversational AI Integration

## Learning Objectives

By the end of this week, you will be able to:

- Integrate large language models (LLMs) with robot control systems
- Implement vision-language-action (VLA) models for robot control
- Design natural language interfaces for robot commands
- Build multimodal perception-language pipelines

## Overview

Conversational AI enables natural human-robot interaction through language. This week covers integrating LLMs and VLA models with Physical AI systems for intuitive robot control.

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│              Conversational AI System                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐       │
│  │   Speech     │  │   Language   │  │      Vision      │       │
│  │   Input      │  │   Model      │  │   Understanding  │       │
│  │              │  │              │  │                  │       │
│  │  - ASR       │  │  - LLM       │  │  - Object        │       │
│  │  - VAD       │  │  - VLA       │  │  - Scene         │       │
│  └──────────────┘  └──────────────┘  └──────────────────┘       │
│           │               │                    │                 │
│           └───────────────┼────────────────────┘                 │
│                           │                                      │
│              ┌────────────▼────────────┐                         │
│              │   Command Interpreter   │                         │
│              │   (Intent + Parameters) │                         │
│              └────────────┬────────────┘                         │
│                           │                                      │
│              ┌────────────▼────────────┐                         │
│              │    Action Generator     │                         │
│              │   (Robot Commands)      │                         │
│              └────────────┬────────────┘                         │
│                           │                                      │
│              ┌────────────▼────────────┐                         │
│              │    Robot Controller     │                         │
│              └─────────────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

## Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **GPU** | RTX 3060 (12GB) | RTX 4090 (24GB) |
| **Memory** | 32GB RAM | 64GB RAM |
| **Storage** | 500GB SSD | 1TB NVMe |
| **Microphone** | USB array | ReSpeaker 4-mic |
| **Edge** | Jetson Orin Nano | Jetson Orin AGX |

## LLM Integration

### ROS 2 LLM Service

```python
#!/usr/bin/env python3
"""
LLM Service for Robot Command Interpretation
Processes natural language and generates robot commands
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from humanoid_interfaces.srv import InterpretCommand
import openai
from typing import Dict, List
import json

class LLMCommandInterpreter(Node):
    def __init__(self):
        super().__init__('llm_command_interpreter')
        
        # Initialize LLM client
        self.client = openai.OpenAI(api_key='your-api-key')
        
        # Service server
        self.service = self.create_service(
            InterpretCommand, 'interpret_command', self.interpret_callback)
        
        # System prompt for robot commands
        self.system_prompt = """You are a robot command interpreter. Convert natural language 
        commands into structured robot actions. Available actions:
        
        - move_to: Move to a location (parameters: x, y, z)
        - pick_up: Pick up an object (parameters: object_name)
        - place: Place an object (parameters: location)
        - wave: Wave hand (parameters: hand, duration)
        - walk_forward: Walk forward (parameters: distance)
        - turn: Turn in place (parameters: angle, direction)
        - stop: Stop current action
        
        Respond ONLY with valid JSON in this format:
        {"action": "action_name", "parameters": {"param1": value1, "param2": value2}}
        """
        
        self.get_logger().info('LLM Command Interpreter initialized')
    
    def interpret_callback(self, request, response):
        """Interpret natural language command"""
        command = request.command
        
        try:
            # Call LLM
            llm_response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": command}
                ],
                temperature=0.1,
                max_tokens=200
            )
            
            # Parse response
            response_text = llm_response.choices[0].message.content.strip()
            parsed = json.loads(response_text)
            
            # Populate response
            response.action = parsed['action']
            response.parameters = json.dumps(parsed['parameters'])
            response.success = True
            response.message = "Command interpreted successfully"
            
            self.get_logger().info(f'Interpreted: {command} -> {parsed["action"]}')
            
        except Exception as e:
            response.success = False
            response.message = f"Interpretation failed: {str(e)}"
            self.get_logger().error(f'LLM interpretation error: {e}')
        
        return response

def main(args=None):
    rclpy.init(args=args)
    node = LLMCommandInterpreter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Service Definition

```yaml
# srv/InterpretCommand.srv
# Interpret natural language command

string command    # Input: natural language command
---
string action     # Output: interpreted action name
string parameters # Output: action parameters (JSON)
bool success      # Output: interpretation success
string message    # Output: status message
```

## Vision-Language Models

### VLA Model Integration

```python
#!/usr/bin/env python3
"""
Vision-Language-Action Model for Robot Control
Processes visual input and language commands to generate actions
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import torch
import numpy as np
from transformers import AutoProcessor, AutoModelForVision2Seq

class VLARobotController(Node):
    def __init__(self):
        super().__init__('vla_robot_controller')
        
        # Load VLA model (e.g., RT-2, OpenFlamingo)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model_name = 'openflamingo/OpenFlamingo-9B-vitl-mpt1b'
        
        try:
            self.processor = AutoProcessor.from_pretrained(self.model_name)
            self.model = AutoModelForVision2Seq.from_pretrained(
                self.model_name,
                device_map='auto'
            )
            self.get_logger().info(f'VLA model loaded: {self.model_name}')
        except Exception as e:
            self.get_logger().error(f'Failed to load VLA model: {e}')
            self.model = None
        
        self.bridge = CvBridge()
        
        # Subscribers
        self.camera_sub = self.create_subscription(
            Image, '/camera/color/image_raw',
            self.camera_callback, 10)
        self.command_sub = self.create_subscription(
            String, '/language_command',
            self.command_callback, 10)
        
        # Publishers
        self.action_pub = self.create_publisher(
            String, '/robot_action', 10)
        
        # State
        self.latest_image = None
        self.pending_command = None
        
        self.get_logger().info('VLA Robot Controller initialized')
    
    def camera_callback(self, msg: Image):
        """Store latest camera image"""
        self.latest_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='rgb8')
    
    def command_callback(self, msg: String):
        """Process language command with visual context"""
        self.pending_command = msg.data
        
        if self.latest_image is not None and self.model is not None:
            self.process_vla_command()
    
    def process_vla_command(self):
        """Process VLA command"""
        try:
            # Prepare inputs
            vision_x = torch.from_numpy(self.latest_image).unsqueeze(0).unsqueeze(0)
            lang_x = self.pending_command
            
            # Generate action
            generated_text = self.model.generate(
                vision_x=vision_x.to(self.device),
                lang_x=lang_x,
                max_new_tokens=50,
                num_beams=3,
                temperature=0.7
            )
            
            # Parse action
            action_text = self.processor.decode(generated_text[0])
            self.get_logger().info(f'VLA output: {action_text}')
            
            # Publish action
            action_msg = String()
            action_msg.data = action_text
            self.action_pub.publish(action_msg)
            
        except Exception as e:
            self.get_logger().error(f'VLA processing error: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = VLARobotController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Speech Recognition

### Voice Command Interface

```python
#!/usr/bin/env python3
"""
Voice Command Interface for Robot Control
Processes speech input and converts to text commands
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import speech_recognition as sr
import pyaudio
import numpy as np

class VoiceCommandNode(Node):
    def __init__(self):
        super().__init__('voice_command_node')
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        # Publisher
        self.command_pub = self.create_publisher(String, '/language_command', 10)
        
        # Timer for continuous listening
        self.timer = self.create_timer(0.1, self.listen_callback)
        
        self.is_listening = True
        self.get_logger().info('Voice Command Node initialized')
    
    def listen_callback(self):
        """Listen for voice commands"""
        if not self.is_listening:
            return
        
        try:
            with self.microphone as source:
                # Listen for speech
                audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=5)
            
            # Recognize speech using Google Speech Recognition
            command = self.recognizer.recognize_google(audio)
            self.get_logger().info(f'Heard: {command}')
            
            # Publish command
            msg = String()
            msg.data = command
            self.command_pub.publish(msg)
            
        except sr.WaitTimeoutError:
            pass  # No speech detected
        except sr.UnknownValueError:
            pass  # Speech not understood
        except sr.RequestError as e:
            self.get_logger().error(f'Speech recognition error: {e}')
        except Exception as e:
            self.get_logger().error(f'Voice command error: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = VoiceCommandNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Complete Integration

### Conversational Robot System

```python
#!/usr/bin/env python3
"""
Complete Conversational AI Robot System
Integrates speech, language, vision, and robot control
"""

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from humanoid_interfaces.srv import InterpretCommand
import asyncio

class ConversationalRobotSystem(Node):
    def __init__(self):
        super().__init__('conversational_robot_system')
        
        # Subscribers
        self.command_sub = self.create_subscription(
            String, '/language_command',
            self.command_callback, 10)
        self.interpreted_sub = self.create_subscription(
            String, '/robot_action',
            self.action_callback, 10)
        
        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.feedback_pub = self.create_publisher(String, '/system_feedback', 10)
        
        # Service client
        self.interpret_client = self.create_client(
            InterpretCommand, 'interpret_command')
        
        while not self.interpret_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for interpret service...')
        
        self.get_logger().info('Conversational Robot System initialized')
    
    def command_callback(self, msg: String):
        """Process incoming language command"""
        command = msg.data
        self.get_logger().info(f'Received command: {command}')
        
        # Send to LLM for interpretation
        request = InterpretCommand.Request()
        request.command = command
        
        future = self.interpret_client.call_async(request)
        future.add_done_callback(self.interpret_callback)
    
    def interpret_callback(self, future):
        """Handle interpretation result"""
        try:
            response = future.result()
            
            if response.success:
                action = response.action
                params = response.parameters
                self.get_logger().info(f'Action: {action}, Params: {params}')
                
                # Execute action
                self.execute_action(action, params)
            else:
                self.send_feedback(f"Could not understand: {response.message}")
                
        except Exception as e:
            self.get_logger().error(f'Interpretation error: {e}')
    
    def execute_action(self, action: str, params: str):
        """Execute robot action"""
        import json
        param_dict = json.loads(params)
        
        if action == 'move_to':
            # Navigate to position
            self.get_logger().info(f'Navigating to {param_dict}')
        elif action == 'walk_forward':
            # Move forward
            distance = param_dict.get('distance', 1.0)
            cmd_vel = Twist()
            cmd_vel.linear.x = 0.3
            self.cmd_vel_pub.publish(cmd_vel)
            self.get_logger().info(f'Walking forward {distance}m')
        elif action == 'stop':
            # Stop
            cmd_vel = Twist()
            self.cmd_vel_pub.publish(cmd_vel)
            self.get_logger().info('Stopping')
        elif action == 'wave':
            # Wave hand (would control arm joints)
            self.get_logger().info('Waving hand')
        else:
            self.get_logger().warn(f'Unknown action: {action}')
    
    def send_feedback(self, message: str):
        """Send system feedback"""
        msg = String()
        msg.data = message
        self.feedback_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = ConversationalRobotSystem()
    
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Resources

### Documentation

- [OpenAI API](https://platform.openai.com/docs)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [SpeechRecognition Library](https://pypi.org/project/SpeechRecognition/)

### Models

- [GPT-4](https://openai.com/gpt-4) - Language model
- [RT-2](https://robotics-transformer-x.github.io/) - Vision-language-action model
- [OpenFlamingo](https://github.com/mlfoundations/open_flamingo) - Open VLA model

## Exercises

1. **LLM Integration**: Set up LLM service for command interpretation
2. **Voice Interface**: Implement speech recognition for robot commands
3. **VLA Pipeline**: Create vision-language processing pipeline
4. **Complete System**: Integrate all components for conversational control

## Next Steps

Proceed to [Week 13 - Complete Humanoid System](./week-13-complete-humanoid-system.md) for final integration.
