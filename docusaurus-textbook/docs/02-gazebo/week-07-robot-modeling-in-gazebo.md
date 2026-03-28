---
id: week-07-robot-modeling-in-gazebo
title: Week 7 - Robot Modeling in Gazebo
sidebar_label: Week 7 - Robot Modeling in Gazebo
sidebar_position: 7
description: Create URDF robot descriptions, configure physics properties, and integrate with Gazebo simulation
---

# Week 7 - Robot Modeling in Gazebo

## Learning Objectives

By the end of this week, you will be able to:

- Create URDF robot descriptions for humanoid robots
- Configure physics properties (mass, inertia, friction)
- Add sensors and actuators to robot models
- Integrate URDF models with Gazebo simulation

## Overview

URDF (Unified Robot Description Format) is the standard XML format for describing robot models in ROS. Gazebo extends URDF with simulation-specific elements for physics, sensors, and actuators.

## URDF Structure

### Basic URDF Elements

```
┌─────────────────────────────────────────────────────────────┐
│                        URDF Robot                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐                                            │
│  │    Link     │──┐                                         │
│  │             │  │                                         │
│  │  - Visual   │  │                                         │
│  │  - Collision│  │                                         │
│  │  - Inertial │  │                                         │
│  └─────────────┘  │                                         │
│                   │                                         │
│  ┌─────────────┐  │  ┌─────────────┐                        │
│  │    Joint    │◀─┴──│    Link     │                        │
│  │             │     │             │                        │
│  │  - Type     │     │  - Visual   │                        │
│  │  - Axis     │     │  - Collision│                        │
│  │  - Limits   │     │  - Inertial │                        │
│  └─────────────┘     └─────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

## Complete Humanoid URDF

### Main URDF File

```xml
<?xml version="1.0" ?>
<robot name="humanoid_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">
  
  <!-- Materials -->
  <material name="black">
    <color rgba="0 0 0 1"/>
  </material>
  <material name="white">
    <color rgba="1 1 1 1"/>
  </material>
  <material name="red">
    <color rgba="1 0 0 1"/>
  </material>
  
  <!-- Base Link -->
  <link name="base_link">
    <inertial>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>
  
  <!-- Torso Link -->
  <link name="torso_link">
    <visual>
      <origin xyz="0 0 0.3" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.1" length="0.4"/>
      </geometry>
      <material name="white"/>
    </visual>
    <collision>
      <origin xyz="0 0 0.3" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.1" length="0.4"/>
      </geometry>
    </collision>
    <inertial>
      <origin xyz="0 0 0.3" rpy="0 0 0"/>
      <mass value="5.0"/>
      <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.1" iyz="0" izz="0.05"/>
    </inertial>
  </link>
  
  <!-- Torso Joint -->
  <joint name="torso_joint" type="fixed">
    <parent link="base_link"/>
    <child link="torso_link"/>
    <origin xyz="0 0 0" rpy="0 0 0"/>
  </joint>
  
  <!-- Left Arm Shoulder -->
  <link name="left_arm_shoulder_link">
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <sphere radius="0.05"/>
      </geometry>
      <material name="red"/>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <sphere radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <mass value="1.5"/>
      <inertia ixx="0.005" ixy="0" ixz="0" iyy="0.005" iyz="0" izz="0.005"/>
    </inertial>
  </link>
  
  <joint name="left_arm_shoulder_joint" type="revolute">
    <parent link="torso_link"/>
    <child link="left_arm_shoulder_link"/>
    <origin xyz="0 0.15 0.35" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-3.14" upper="3.14" effort="50" velocity="3.0"/>
  </joint>
  
  <!-- Left Arm Elbow -->
  <link name="left_arm_elbow_link">
    <visual>
      <origin xyz="0 0 -0.15" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.03" length="0.3"/>
      </geometry>
      <material name="white"/>
    </visual>
    <collision>
      <origin xyz="0 0 -0.15" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.03" length="0.3"/>
      </geometry>
    </collision>
    <inertial>
      <origin xyz="0 0 -0.15" rpy="0 0 0"/>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.005"/>
    </inertial>
  </link>
  
  <joint name="left_arm_elbow_joint" type="revolute">
    <parent link="left_arm_shoulder_link"/>
    <child link="left_arm_elbow_link"/>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="3.14" effort="30" velocity="3.0"/>
  </joint>
  
  <!-- Right Arm (mirrored) -->
  <link name="right_arm_shoulder_link">
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <sphere radius="0.05"/>
      </geometry>
      <material name="red"/>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <sphere radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <mass value="1.5"/>
      <inertia ixx="0.005" ixy="0" ixz="0" iyy="0.005" iyz="0" izz="0.005"/>
    </inertial>
  </link>
  
  <joint name="right_arm_shoulder_joint" type="revolute">
    <parent link="torso_link"/>
    <child link="right_arm_shoulder_link"/>
    <origin xyz="0 -0.15 0.35" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-3.14" upper="3.14" effort="50" velocity="3.0"/>
  </joint>
  
  <!-- Left Leg Hip -->
  <link name="left_leg_hip_link">
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <sphere radius="0.06"/>
      </geometry>
      <material name="black"/>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <sphere radius="0.06"/>
      </geometry>
    </collision>
    <inertial>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <mass value="2.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>
  
  <joint name="left_leg_hip_joint" type="revolute">
    <parent link="base_link"/>
    <child link="left_leg_hip_link"/>
    <origin xyz="0 0.08 0" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="5.0"/>
  </joint>
  
  <!-- Left Leg Knee -->
  <link name="left_leg_knee_link">
    <visual>
      <origin xyz="0 0 -0.2" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.04" length="0.4"/>
      </geometry>
      <material name="white"/>
    </visual>
    <collision>
      <origin xyz="0 0 -0.2" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.04" length="0.4"/>
      </geometry>
    </collision>
    <inertial>
      <origin xyz="0 0 -0.2" rpy="0 0 0"/>
      <mass value="2.5"/>
      <inertia ixx="0.02" ixy="0" ixz="0" iyy="0.02" iyz="0" izz="0.01"/>
    </inertial>
  </link>
  
  <joint name="left_leg_knee_joint" type="revolute">
    <parent link="left_leg_hip_link"/>
    <child link="left_leg_knee_link"/>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="2.5" effort="80" velocity="5.0"/>
  </joint>
  
  <!-- Right Leg (mirrored) -->
  <link name="right_leg_hip_link">
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <sphere radius="0.06"/>
      </geometry>
      <material name="black"/>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <sphere radius="0.06"/>
      </geometry>
    </collision>
    <inertial>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <mass value="2.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>
  
  <joint name="right_leg_hip_joint" type="revolute">
    <parent link="base_link"/>
    <child link="right_leg_hip_link"/>
    <origin xyz="0 -0.08 0" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="5.0"/>
  </joint>
  
  <!-- Gazebo Plugin for ROS 2 Control -->
  <gazebo>
    <plugin filename="gz_ros2_control-system" name="gz_ros2_control::GazeboSimROS2ControlPlugin">
      <parameters>$(find humanoid_description)/config/gazebo_ros2_control.yaml</parameters>
      <robot_param>robot_description</robot_param>
      <robot_param_node>robot_state_publisher</robot_param_node>
    </plugin>
  </gazebo>
  
</robot>
```

### Xacro Macro for Modular Design

```xml
<?xml version="1.0" ?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">
  
  <!-- Arm Macro -->
  <xacro:macro name="arm" params="prefix parent *origin">
    
    <link name="${prefix}_arm_shoulder_link">
      <visual>
        <geometry>
          <sphere radius="0.05"/>
        </geometry>
      </visual>
      <collision>
        <geometry>
          <sphere radius="0.05"/>
        </geometry>
      </collision>
      <inertial>
        <mass value="1.5"/>
        <inertia ixx="0.005" ixy="0" ixz="0" iyy="0.005" iyz="0" izz="0.005"/>
      </inertial>
    </link>
    
    <joint name="${prefix}_arm_shoulder_joint" type="revolute">
      <parent link="${parent}"/>
      <child link="${prefix}_arm_shoulder_link"/>
      <xacro:insert_block name="origin"/>
      <axis xyz="0 0 1"/>
      <limit lower="-3.14" upper="3.14" effort="50" velocity="3.0"/>
    </joint>
    
  </xacro:macro>
  
  <!-- Use the macro -->
  <xacro:arm prefix="left" parent="torso_link">
    <origin xyz="0 0.15 0.35" rpy="0 0 0"/>
  </xacro:arm>
  
  <xacro:arm prefix="right" parent="torso_link">
    <origin xyz="0 -0.15 0.35" rpy="0 0 0"/>
  </xacro:arm>
  
</robot>
```

## Gazebo Sensor Plugins

### Camera Sensor

```xml
<!-- Add to URDF link -->
<link name="camera_link">
  <visual>
    <geometry>
      <box size="0.05 0.05 0.05"/>
    </geometry>
  </visual>
</link>

<gazebo reference="camera_link">
  <sensor type="camera" name="head_camera">
    <update_rate>30.0</update_rate>
    <camera name="head">
      <horizontal_fov>1.3962634</horizontal_fov>
      <image>
        <width>640</width>
        <height>480</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.02</near>
        <far>300</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
      <frame_name>camera_link</frame_name>
      <camera_name>head_camera</camera_name>
    </plugin>
  </sensor>
</gazebo>
```

### LiDAR Sensor

```xml
<gazebo reference="base_link">
  <sensor type="gpu_lidar" name="head_lidar">
    <pose>0 0 0.5 0 0 0</pose>
    <visualize>true</visualize>
    <update_rate>10</update_rate>
    <lidar>
      <scan>
        <horizontal>
          <samples>720</samples>
          <resolution>1</resolution>
          <min_angle>-3.14159</min_angle>
          <max_angle>3.14159</max_angle>
        </horizontal>
      </scan>
      <range>
        <min>0.1</min>
        <max>30.0</max>
        <resolution>0.01</resolution>
      </range>
    </lidar>
    <plugin name="lidar_controller" filename="libgazebo_ros_ray_sensor.so">
      <ros>
        <argument>~/out:=/scan</argument>
      </ros>
      <output_type>sensor_msgs/LaserScan</output_type>
      <frame_name>base_link</frame_name>
    </plugin>
  </sensor>
</gazebo>
```

### IMU Sensor

```xml
<gazebo reference="base_link">
  <sensor type="imu" name="imu_sensor">
    <always_on>true</always_on>
    <update_rate>100</update_rate>
    <visualize>true</visualize>
    <plugin name="imu_controller" filename="libgazebo_ros_imu_sensor.so">
      <ros>
        <argument>~/out:=/imu/data</argument>
      </ros>
      <frame_name>base_link</frame_name>
    </plugin>
  </sensor>
</gazebo>
```

## ROS 2 Control Configuration

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
      - left_arm_shoulder_joint
      - left_arm_elbow_joint
      - right_arm_shoulder_joint
      - right_arm_elbow_joint
      - left_leg_hip_joint
      - left_leg_knee_joint
      - right_leg_hip_joint
      - right_leg_knee_joint
    command_interfaces:
      - position
      - velocity
    state_interfaces:
      - position
      - velocity
    state_publish_rate: 50.0
    action_monitor_rate: 20.0
```

## Launch File

```python
# launch/humanoid_gazebo.launch.py

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    urdf_path = PathJoinSubstitution([
        FindPackageShare('humanoid_description'),
        'urdf',
        'humanoid_robot.urdf.xacro'
    ])
    
    world_path = PathJoinSubstitution([
        FindPackageShare('humanoid_gazebo'),
        'worlds',
        'humanoid_world.sdf'
    ])
    
    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': open(urdf_path).read()
        }]
    )
    
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
            'gz_args': ['-r ', world_path]
        }.items()
    )
    
    # Spawn entity
    spawn_entity = Node(
        package='gz_ros2_control',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'humanoid_robot'
        ],
        output='screen'
    )
    
    # Load controllers
    joint_state_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
    )
    
    trajectory_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_trajectory_controller'],
    )
    
    return LaunchDescription([
        DeclareLaunchArgument('world', default_value=world_path),
        robot_state_publisher,
        gazebo,
        spawn_entity,
        joint_state_spawner,
        trajectory_spawner,
    ])
```

## Resources

### Documentation

- [URDF Specification](http://wiki.ros.org/urdf)
- [Xacro Documentation](http://wiki.ros.org/xacro)
- [Gazebo ROS 2 Control](https://github.com/ros-controls/gz_ros2_control)

### Tools

- [check_urdf](http://wiki.ros.org/urdf/Tutorials/How%20to%20parse%20a%20URDF%20document) - URDF validation
- [urdf_to_graphviz](http://wiki.ros.org/urdf_parser) - URDF visualization

## Exercises

1. **URDF Creation**: Create a URDF for a simple 2-DOF arm
2. **Xacro Conversion**: Convert the URDF to use Xacro macros
3. **Sensor Integration**: Add camera and IMU sensors to the robot model
4. **Gazebo Launch**: Launch the robot in Gazebo and verify controller loading

## Next Steps

Proceed to [Week 8 - Introduction to Isaac Sim](../03-nvidia-isaac/week-08-introduction-to-isaac-sim.md) for GPU-accelerated simulation.
