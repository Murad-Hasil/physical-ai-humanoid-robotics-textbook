---
id: week-06-introduction-to-gazebo
title: Week 6 - Introduction to Gazebo
sidebar_label: Week 6 - Introduction to Gazebo
sidebar_position: 6
description: Gazebo simulation fundamentals, installation, and basic scene creation
---

# Week 6 - Introduction to Gazebo

## Learning Objectives

By the end of this week, you will be able to:

- Understand Gazebo simulation architecture and capabilities
- Install and configure Gazebo for ROS 2 integration
- Create basic simulation environments
- Launch Gazebo with ROS 2 nodes

## Overview

Gazebo is an open-source 3D robotics simulator that provides accurate physics simulation, sensor modeling, and environment generation. It integrates seamlessly with ROS 2 for robot development and testing.

### Gazebo Versions

| Version | ROS 2 Compatibility | Status |
|---------|---------------------|--------|
| **Gazebo Classic (Gazebo 11)** | ROS 2 Foxy, Galactic | Legacy |
| **Gazebo Sim (Gazebo Harmonic)** | ROS 2 Humble, Iron | Recommended |
| **Gazebo Ionic** | ROS 2 Jazzy | Latest |

## Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **GPU** | NVIDIA GTX 1060 (6GB) | NVIDIA RTX 3060 (12GB) |
| **CPU** | 4 cores | 8+ cores |
| **RAM** | 8GB | 16GB+ |
| **Storage** | 10GB free space | 50GB SSD |

## Installation

### Gazebo Sim (Harmonic) with ROS 2 Humble

```bash
#!/bin/bash
# Gazebo Sim Installation for ROS 2 Humble

# Add OSRF packages repository
sudo apt update
sudo apt install lsb-release wget gnupg -y
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" > /etc/apt/sources.list.d/gazebo-stable.list'
wget https://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -

# Install Gazebo Sim Harmonic
sudo apt update
sudo apt install gz-harmonic -y

# Install ROS 2 Gazebo plugins
sudo apt install ros-humble-gz-ros2-control ros-humble-gz-sim -y

# Install Gazebo ROS 2 bridge
sudo apt install ros-humble-ros-gzgarden -y

# Verify installation
gz sim --version
```

### Verification

```bash
# Check Gazebo version
gz sim --version

# List available Gazebo commands
gz --help

# Launch Gazebo empty world
gz sim empty.sdf
```

## Gazebo Architecture

### Simulation Components

```
┌─────────────────────────────────────────────────────────────┐
│                      Gazebo Simulation                       │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │   Physics    │  │   Rendering  │  │     Sensors      │   │
│  │    Engine    │  │    Engine    │  │      Models      │   │
│  │              │  │              │  │                  │   │
│  │  - ODE       │  │  - OGRE      │  │  - Camera        │   │
│  │  - Bullet    │  │  - Materials │  │  - LiDAR         │   │
│  │  - DART      │  │  - Lighting  │  │  - IMU           │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
│                                                              │
│              ┌──────────────────────────────┐                │
│              │      ROS 2 Bridge            │                │
│              │  (gz-ros2-control, ros-gzg)  │                │
│              └──────────────────────────────┘                │
│                          │                                   │
│              ┌───────────▼───────────┐                       │
│              │    ROS 2 Middleware   │                       │
│              └───────────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

### World File Structure (SDF)

```xml
<?xml version="1.0" ?>
<sdf version="1.9">
  <world name="humanoid_simulation">
    
    <!-- Physics configuration -->
    <physics type="ode">
      <real_time_update_rate>1000</real_time_update_rate>
      <real_time_factor>1</real_time_factor>
    </physics>
    
    <!-- Scene configuration -->
    <scene>
      <ambient>0.4 0.4 0.4 1</ambient>
      <background>0.7 0.7 0.7 1</background>
      <shadows>true</shadows>
    </scene>
    
    <!-- Ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>
    
    <!-- Sun light -->
    <include>
      <uri>model://sun</uri>
    </include>
    
    <!-- Robot model -->
    <include>
      <uri>model://humanoid_robot</uri>
      <pose>0 0 0.5 0 0 0</pose>
    </include>
    
  </world>
</sdf>
```

## Basic Simulation

### Launching Gazebo with ROS 2

```python
#!/usr/bin/env python3
"""
Gazebo Simulation Launch File
Launches Gazebo with robot model and ROS 2 bridge
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Declare arguments
    world_arg = DeclareLaunchArgument(
        'world',
        default_value='empty.sdf',
        description='Gazebo world file to load'
    )
    
    # Gazebo server
    gz_server = ExecuteProcess(
        cmd=['gz', 'sim', '-r', '-s', LaunchConfiguration('world')],
        output='screen'
    )
    
    # Gazebo client (GUI)
    gz_client = ExecuteProcess(
        cmd=['gz', 'sim', '-g'],
        output='screen'
    )
    
    # ROS 2 bridge
    ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
        output='screen'
    )
    
    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': open('path/to/robot.urdf').read()}],
        output='screen'
    )
    
    return LaunchDescription([
        world_arg,
        gz_server,
        gz_client,
        ros_gz_bridge,
        robot_state_publisher,
    ])
```

### Creating a Simple World

```xml
<!-- worlds/simple_room.sdf -->
<?xml version="1.0" ?>
<sdf version="1.9">
  <world name="simple_room">
    
    <physics type="ode">
      <real_time_update_rate>1000</real_time_update_rate>
    </physics>
    
    <scene>
      <ambient>0.3 0.3 0.3 1</ambient>
      <background>0.5 0.5 0.5 1</background>
    </scene>
    
    <!-- Ground plane -->
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
            </plane>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
            </plane>
          </geometry>
          <material>
            <ambient>0.8 0.8 0.8 1</ambient>
            <diffuse>0.8 0.8 0.8 1</diffuse>
          </material>
        </visual>
      </link>
    </model>
    
    <!-- Box obstacle -->
    <model name="box_obstacle">
      <pose>2 0 0.5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>1 1 1</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>1 1 1</size>
            </box>
          </geometry>
          <material>
            <ambient>1 0 0 1</ambient>
            <diffuse>1 0 0 1</diffuse>
          </material>
        </visual>
      </link>
    </model>
    
  </world>
</sdf>
```

## ROS 2 Integration

### Gazebo ROS 2 Control

```yaml
# config/gazebo_ros2_control.yaml
controller_manager:
  ros__parameters:
    update_rate: 100  # Hz
    
    joint_state_broadcaster:
      type: joint_state_broadcaster/JointStateBroadcaster
    
    joint_trajectory_controller:
      type: joint_trajectory_controller/JointTrajectoryController

joint_trajectory_controller:
  ros__parameters:
    joints:
      - left_arm_shoulder
      - right_arm_shoulder
      - left_knee
      - right_knee
    command_interfaces:
      - position
      - velocity
    state_interfaces:
      - position
      - velocity
```

### Launch File with ROS 2 Control

```python
# launch/humanoid_gazebo.launch.py

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gz_ros2_control'),
                'launch',
                'gz_sim.launch.py'
            ])
        ]),
        launch_arguments={
            'gz_args': '-r empty.sdf'
        }.items()
    )
    
    # Spawn robot
    spawn_robot = Node(
        package='gz_ros2_control',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'humanoid_robot'
        ],
        output='screen'
    )
    
    # Load controllers
    load_controllers = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster', 'joint_trajectory_controller'],
        output='screen'
    )
    
    return LaunchDescription([
        gazebo,
        RegisterEventHandler(
            OnProcessStart(
                target_action=gazebo,
                on_start=[spawn_robot]
            )
        ),
        RegisterEventHandler(
            OnProcessStart(
                target_action=spawn_robot,
                on_start=[load_controllers]
            )
        ),
    ])
```

## Resources

### Documentation

- [Gazebo Sim Documentation](https://gazebosim.org/docs)
- [Gazebo ROS 2 Control](https://github.com/ros-controls/gz_ros2_control)
- [SDF Specification](http://sdformat.org/spec)

### Tutorials

- [Gazebo Basics Tutorial](https://gazebosim.org/tutorials)
- [ROS 2 + Gazebo Integration](https://docs.ros.org/en/humble/Tutorials/Intermediate/ROS2-with-Gazebo.html)

## Exercises

1. **Installation**: Install Gazebo Sim and verify with `gz sim --version`
2. **World Creation**: Create a simple world with ground plane and obstacles
3. **ROS 2 Bridge**: Launch Gazebo with ROS 2 clock publishing
4. **Visualization**: Use RViz2 to visualize Gazebo simulation data

## Next Steps

Proceed to [Week 7 - Robot Modeling in Gazebo](./week-07-robot-modeling-in-gazebo.md) for URDF robot descriptions and simulation.
