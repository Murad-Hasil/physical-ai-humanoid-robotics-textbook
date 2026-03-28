---
id: week-02-physical-ai-architecture
title: Week 2 - Physical AI Architecture
sidebar_label: Week 2 - Physical AI Architecture
sidebar_position: 2
description: Complete Physical AI system architecture, software stack, and integration patterns
---

# Week 2 - Physical AI Architecture

## Learning Objectives

By the end of this week, you will be able to:

- Understand the complete Physical AI system architecture
- Identify software components and their interactions
- Design integration patterns for perception, reasoning, and action
- Plan your development workflow across the 13-week curriculum

## Overview

A complete Physical AI system integrates multiple software layers working in concert. This week we explore the architecture that connects perception models, language understanding, and robot control.

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Physical AI System                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │  Perception │  │  Reasoning  │  │        Action           │  │
│  │             │  │             │  │                         │  │
│  │  - Vision   │  │  - LLM/VLA  │  │  - Motion Planning      │  │
│  │  - Audio    │  │  - Planning │  │  - Control Policies     │  │
│  │  - Sensors  │  │  - Memory   │  │  - Actuation            │  │
│  └──────┬──────┘  └──────┬──────┘  └────────────┬────────────┘  │
│         │                │                       │               │
│         └────────────────┼───────────────────────┘               │
│                          │                                       │
│              ┌───────────▼───────────┐                           │
│              │    ROS 2 Middleware   │                           │
│              │    (Communication)    │                           │
│              └───────────┬───────────┘                           │
│                          │                                       │
│         ┌────────────────┼────────────────┐                      │
│         │                │                │                      │
│  ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐              │
│  │  Simulation │  │  Digital    │  │  Physical   │              │
│  │  (Isaac)    │  │  Twin       │  │  Robot      │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
└─────────────────────────────────────────────────────────────────┘
```

### Software Stack Layers

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Hardware** | RTX GPU, Jetson Orin | Compute platform |
| **OS** | Ubuntu 22.04 LTS | Base operating system |
| **Middleware** | ROS 2 Humble | Robot communication |
| **Simulation** | Isaac Sim, Gazebo | Virtual environments |
| **Perception** | Vision models, VLA | Environmental understanding |
| **Reasoning** | LLM, Planning | Decision making |
| **Control** | Motion planning, RL policies | Robot actuation |

## ROS 2 Integration

### Node Architecture

```python
#!/usr/bin/env python3
"""
Physical AI System Coordinator Node
Coordinates perception, reasoning, and action modules
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, JointState
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class PhysicalAICoordinator(Node):
    def __init__(self):
        super().__init__('physical_ai_coordinator')
        
        # Perception subscribers
        self.vision_sub = self.create_subscription(
            Image, '/camera/color/image_raw',
            self.vision_callback, 10)
        
        # Reasoning subscribers
        self.language_sub = self.create_subscription(
            String, '/vla/command',
            self.language_callback, 10)
        
        # Action publishers
        self.joint_pub = self.create_publisher(
            JointState, '/joint_commands', 10)
        self.base_pub = self.create_publisher(
            Twist, '/cmd_vel', 10)
        
        self.get_logger().info('Physical AI Coordinator initialized')
    
    def vision_callback(self, msg: Image):
        """Process visual input"""
        self.get_logger().debug(f'Received image: {msg.header.stamp}')
    
    def language_callback(self, msg: String):
        """Process language commands"""
        self.get_logger().info(f'Received command: {msg.data}')
    
    def publish_joint_command(self, joint_names, positions):
        """Send joint commands to robot"""
        msg = JointState()
        msg.name = joint_names
        msg.position = positions
        self.joint_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = PhysicalAICoordinator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Digital Twin Architecture

### Simulation-to-Reality Pipeline

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   Isaac Sim      │────▶│   ROS 2 Bridge   │────▶│   Physical Robot │
│   (Virtual)      │     │   (Middleware)   │     │   (Real)         │
└──────────────────┘     └──────────────────┘     └──────────────────┘
        │                        │                        │
        │   USD Scene            │   Topics/Services      │   Hardware
        │   Physics Engine       │   Messages             │   Drivers
        │   Synthetic Data       │   Actions              │   Sensors
```

## Curriculum Integration

### Module Dependencies

```
Week 1-2:  Foundation (Introduction & Architecture)
              │
              ▼
Week 3-5:  Module 1: ROS 2 Fundamentals
              │
              ▼
Week 6-7:  Module 2: Gazebo Simulation
              │
              ▼
Week 8-10: Module 3: NVIDIA Isaac Platform
              │
              ▼
Week 11-13: Module 4: Humanoid Development
```

## Resources

### Documentation

- [ROS 2 Architecture](https://docs.ros.org/en/humble/The-ROS2-Project/index.html)
- [NVIDIA Isaac Sim Architecture](https://docs.omniverse.nvidia.com/isaacsim/latest/architecture.html)
- [Gazebo Simulation](https://gazebosim.org/docs)

### Tools

- [RViz2](https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz2/RViz2-User-Guide.html) - ROS 2 visualization
- [Foxglove Studio](https://foxglove.dev/) - Robotics data visualization
- [Webots](https://cyberbotics.com/) - Alternative simulation platform

## Exercises

1. **Architecture Diagram**: Draw your own system architecture diagram for a specific humanoid robot task
2. **ROS 2 Node Creation**: Create a simple ROS 2 publisher/subscriber pair
3. **Component Mapping**: Map each curriculum module to a layer in the architecture stack

## Next Steps

Proceed to [Week 3 - Introduction to ROS 2](../01-ros-2/week-03-introduction-to-ros-2.md) to begin hands-on ROS 2 development.
