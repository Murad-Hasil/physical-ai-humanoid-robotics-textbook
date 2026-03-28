---
id: week-03-introduction-to-ros-2
title: Week 3 - Introduction to ROS 2
sidebar_label: Week 3 - Introduction to ROS 2
sidebar_position: 3
description: ROS 2 fundamentals, installation, workspace setup, and core concepts
---

# Week 3 - Introduction to ROS 2

## Learning Objectives

By the end of this week, you will be able to:

- Understand ROS 2 architecture and core concepts
- Install and configure ROS 2 Humble on Ubuntu 22.04
- Create and manage ROS 2 workspaces
- Use essential ROS 2 CLI tools

## Overview

ROS 2 (Robot Operating System 2) is the industry-standard middleware for robotics development. It provides communication primitives, hardware abstraction, and tools for building complex robotic systems.

### Why ROS 2?

- **Distributed Architecture**: Nodes can run on different machines
- **Real-time Support**: Deterministic communication for control systems
- **Security**: Built-in DDS security features
- **Modern C++/Python**: Support for latest language features
- **Industry Adoption**: Used by Boston Dynamics, NVIDIA, and major robotics companies

## Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 4 cores | 8+ cores |
| **RAM** | 8GB | 16GB+ |
| **Network** | 1 Gbps Ethernet | 10 Gbps for multi-robot |
| **OS** | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |

## Installation

### ROS 2 Humble Installation

```bash
#!/bin/bash
# ROS 2 Humble Installation Script for Ubuntu 22.04

# Set locale
sudo apt update && sudo apt install locales -y
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Add ROS 2 repository
sudo apt install software-properties-common -y
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | sudo apt-key add -
echo "deb http://packages.ros.org/ros2/ubuntu jammy main" | sudo tee /etc/apt/sources.list.d/ros2.list

# Install ROS 2 Humble
sudo apt update
sudo apt install ros-humble-desktop -y

# Install development tools
sudo apt install ros-dev-tools -y

# Install rosdep
sudo apt install python3-rosdep -y
sudo rosdep init
rosdep update

# Source ROS 2
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc

# Verify installation
ros2 --version
```

### Verification

```bash
# Check ROS 2 version
ros2 --version

# Check available commands
ros2 --help

# List available packages
ros2 pkg list | head -20
```

## Workspace Setup

### Creating a ROS 2 Workspace

```bash
# Create workspace directory
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws

# Initialize workspace
colcon build --symlink-install

# Source the workspace
source install/setup.bash

# Verify workspace
echo $ROS_DOMAIN_ID
```

### Workspace Structure

```
ros2_ws/
├── src/              # Source code
│   ├── package_1/
│   └── package_2/
├── build/            # Build artifacts (generated)
├── install/          # Installation files (generated)
└── log/              # Log files (generated)
```

## Core Concepts

### ROS 2 Graph

```
┌─────────────┐      Topics      ┌─────────────┐
│   Node 1    │ ◀──────────────▶ │   Node 2    │
│  (Publisher)│    (Messages)    │ (Subscriber)│
└─────────────┘                  └─────────────┘
       │                                │
       │         Services               │
       │ ◀────────────────────────────▶ │
       │         (Request/Response)     │
       │                                │
       │         Actions                │
       │ ◀────────────────────────────▶ │
       │    (Goal/Feedback/Result)      │
```

### Key Terminology

| Term | Definition |
|------|------------|
| **Node** | Executable that performs computation |
| **Topic** | Named bus for data exchange (publish/subscribe) |
| **Message** | Data structure for topics |
| **Service** | Synchronous request/response communication |
| **Action** | Asynchronous goal-based communication |
| **Package** | Organizational unit for ROS 2 code |
| **Workspace** | Directory containing ROS 2 packages |

## Essential CLI Tools

### Package Management

```bash
# List all packages
ros2 pkg list

# Get package information
ros2 pkg info demo_nodes_cpp

# List executables in a package
ros2 pkg executables demo_nodes_cpp

# Create a new package
ros2 pkg create my_package --build-type ament_python --dependencies rclpy
```

### Node Management

```bash
# List running nodes
ros2 node list

# Get node information
ros2 node info /talker

# Run a node
ros2 run demo_nodes_cpp talker
```

### Topic Management

```bash
# List active topics
ros2 topic list

# Get topic information
ros2 topic info /chatter

# Echo topic messages
ros2 topic echo /chatter

# Publish a message
ros2 topic pub /chatter std_msgs/msg/String "data: 'Hello ROS 2'"
```

## Code Example: Simple Publisher

```python
#!/usr/bin/env python3
"""
Simple ROS 2 Publisher Node
Publishes string messages to a topic
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SimplePublisher(Node):
    def __init__(self):
        super().__init__('simple_publisher')
        self.publisher_ = self.create_publisher(
            String, 'chatter', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.counter = 0
    
    def timer_callback(self):
        msg = String()
        msg.data = f'Hello ROS 2! Count: {self.counter}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data}')
        self.counter += 1

def main(args=None):
    rclpy.init(args=args)
    node = SimplePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Resources

### Documentation

- [ROS 2 Official Documentation](https://docs.ros.org/en/humble/)
- [ROS 2 Tutorials](https://docs.ros.org/en/humble/Tutorials.html)
- [ROS 2 Design Articles](https://design.ros2.org/)

### Tools

- [colcon](https://colcon.readthedocs.io/) - Build tool
- [rosdep](https://docs.ros.org/en/humble/Tutorials/Intermediate/Rosdep.html) - Dependency manager

## Exercises

1. **Installation Verification**: Complete ROS 2 installation and verify with `ros2 --version`
2. **Workspace Creation**: Create a ROS 2 workspace and build it
3. **Publisher Node**: Create and run the simple publisher node
4. **CLI Exploration**: Use `ros2 node list`, `ros2 topic list`, and `ros2 topic echo`

## Next Steps

Proceed to [Week 4 - ROS 2 Nodes and Topics](./week-04-ros-2-nodes-and-topics.md) for deeper exploration of ROS 2 communication.
