---
id: week-09-isaac-ros-integration
title: Week 9 - Isaac ROS Integration
sidebar_label: Week 9 - Isaac ROS Integration
sidebar_position: 9
description: Deep integration between Isaac Sim and ROS 2, including ROS 2 control, navigation, and perception pipelines
---

# Week 9 - Isaac ROS Integration

## Learning Objectives

By the end of this week, you will be able to:

- Configure Isaac Sim ROS 2 bridge for bidirectional communication
- Implement ROS 2 control with Isaac Sim
- Integrate navigation and perception pipelines
- Deploy ROS 2 packages with Isaac Sim simulation

## Overview

Isaac ROS provides a comprehensive set of packages for integrating Isaac Sim with ROS 2, enabling seamless simulation-to-reality workflows for robotics development.

### Isaac ROS Packages

| Package | Purpose |
|---------|---------|
| **isaac_ros_bridge** | ROS 2 ↔ Isaac Sim communication |
| **isaac_ros_control** | ROS 2 control framework integration |
| **isaac_ros_perception** | Vision and sensor processing |
| **isaac_ros_navigation** | Navigation stack integration |
| **isaac_ros_manipulation** | Motion planning and control |

## Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **GPU** | RTX 3060 (12GB) | RTX 4090 (24GB) |
| **CPU** | 8 cores | 16 cores |
| **RAM** | 32GB | 64GB |
| **Network** | 1 Gbps | 10 Gbps |

## ROS 2 Bridge Configuration

### Bridge Setup

```python
#!/usr/bin/env python3
"""
Isaac Sim ROS 2 Bridge Configuration
Establishes bidirectional communication between Isaac Sim and ROS 2
"""

from omni.isaac.kit import SimulationApp
simulation_app = SimulationApp({"headless": False})

from omni.isaac.core import World
from omni.isaac.ros2_bridge import ROS2Bridge, register_ros2_bridge_extensions
from sensor_msgs.msg import Image, JointState, LaserScan
from geometry_msgs.msg import Twist, PoseStamped
import rclpy
from rclpy.node import Node

class IsaacROSBridge(Node):
    def __init__(self):
        super().__init__('isaac_ros_bridge')
        
        # Publishers (Isaac Sim → ROS 2)
        self.camera_pub = self.create_publisher(Image, '/camera/color/image_raw', 10)
        self.joint_state_pub = self.create_publisher(JointState, '/joint_states', 10)
        self.lidar_pub = self.create_publisher(LaserScan, '/scan', 10)
        
        # Subscribers (ROS 2 → Isaac Sim)
        self.cmd_vel_sub = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        self.joint_cmd_sub = self.create_subscription(
            JointState, '/joint_commands', self.joint_cmd_callback, 10)
        
        self.get_logger().info('Isaac ROS 2 Bridge initialized')
    
    def cmd_vel_callback(self, msg: Twist):
        """Handle velocity commands from ROS 2"""
        self.get_logger().debug(f'Received cmd_vel: linear={msg.linear}, angular={msg.angular}')
        # Apply to robot in Isaac Sim
        # robot.set_velocity(msg.linear.x, msg.angular.z)
    
    def joint_cmd_callback(self, msg: JointState):
        """Handle joint commands from ROS 2"""
        self.get_logger().debug(f'Received joint command for {len(msg.name)} joints')
        # Apply joint positions to robot in Isaac Sim
        # robot.set_joint_positions(msg.position, msg.name)
    
    def publish_camera(self, image_data):
        """Publish camera image from Isaac Sim"""
        msg = Image()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'camera_link'
        msg.height = image_data.shape[0]
        msg.width = image_data.shape[1]
        msg.encoding = 'rgb8'
        msg.data = image_data.tobytes()
        self.camera_pub.publish(msg)
    
    def publish_joint_states(self, joint_names, positions, velocities):
        """Publish joint states from Isaac Sim"""
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = joint_names
        msg.position = positions
        msg.velocity = velocities
        self.joint_state_pub.publish(msg)

def main():
    # Initialize ROS 2
    rclpy.init()
    bridge_node = IsaacROSBridge()
    
    # Initialize Isaac Sim
    world = World(stage_units_in_meters=1.0)
    world.scene.add_default_ground_plane()
    
    # Simulation loop with ROS 2 spin
    while rclpy.ok():
        rclpy.spin_once(bridge_node, timeout_sec=0.0)
        world.step(render=True)
    
    bridge_node.destroy_node()
    rclpy.shutdown()
    simulation_app.close()

if __name__ == '__main__':
    main()
```

## ROS 2 Control Integration

### Controller Configuration

```yaml
# config/isaac_ros2_control.yaml
controller_manager:
  ros__parameters:
    update_rate: 100  # Hz
    
    joint_state_broadcaster:
      type: joint_state_broadcaster/JointStateBroadcaster
    
    joint_trajectory_controller:
      type: joint_trajectory_controller/JointTrajectoryController
    
    effort_controller:
      type: effort_controllers/JointGroupEffortController

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

effort_controller:
  ros__parameters:
    joints:
      - left_arm_shoulder_joint
      - right_arm_shoulder_joint
    interface_name: effort
```

### Isaac Sim ROS 2 Control Plugin

```python
# Isaac Sim ROS 2 control implementation
from omni.isaac.core.controllers import BaseController
from omni.isaac.core.robots import Robot
import numpy as np

class IsaacROS2Controller(BaseController):
    def __init__(self, robot: Robot, controller_name: str = "joint_trajectory_controller"):
        super().__init__()
        self.robot = robot
        self.controller_name = controller_name
        self.joint_indices = self.robot.get_dof_indices()
    
    def apply_action(self, action):
        """Apply trajectory action to robot"""
        if action is not None:
            positions = action.get("positions", None)
            velocities = action.get("velocities", None)
            
            if positions is not None:
                self.robot.set_joint_positions(positions, self.joint_indices)
            
            if velocities is not None:
                self.robot.set_joint_velocities(velocities, self.joint_indices)
    
    def forward(self, observation):
        """Compute control action"""
        # Implement control logic
        return {"positions": observation.target_positions}
```

## Navigation Integration

### Nav2 Configuration for Isaac Sim

```yaml
# config/nav2_params.yaml
amcl:
  ros__parameters:
    use_sim_time: True
    alpha1: 0.2
    alpha2: 0.2
    alpha3: 0.2
    alpha4: 0.2
    alpha5: 0.2
    base_frame_id: "base_link"
    beam_skip_distance: 0.5
    beam_skip_error_threshold: 0.9
    beam_skip_threshold: 0.3
    do_beamskip: false
    global_frame_id: "map"
    lambda_short: 0.1
    laser_likelihood_max_dist: 2.0
    laser_max_range: 100.0
    laser_min_range: -1.0
    laser_model_type: "likelihood_field"
    max_beams: 60
    max_particles: 2000
    min_particles: 500
    odom_frame_id: "odom"
    pf_err: 0.05
    pf_z: 0.99
    recovery_alpha_fast: 0.0
    recovery_alpha_slow: 0.0
    resample_interval: 1
    robot_model_type: "nav2_amcl::DifferentialMotionModel"
    save_pose_rate: 0.5
    sigma_hit: 0.2
    tf_broadcast: true
    transform_tolerance: 1.0
    update_min_a: 0.2
    update_min_d: 0.25
    z_hit: 0.5
    z_max: 0.05
    z_rand: 0.5
    z_short: 0.05
    scan_topic: /scan

bt_navigator:
  ros__parameters:
    use_sim_time: True
    global_frame: map
    robot_base_frame: base_link
    odom_topic: /odom
    bt_loop_duration: 10
    default_server_timeout: 20
    enable_groot_monitoring: True
    groot_zmq_publisher_port: 1666
    groot_zmq_server_port: 1667
    plugin_lib_names:
      - nav2_compute_path_to_pose_action_bt_node
      - nav2_compute_path_through_poses_action_bt_node
      - nav2_follow_path_action_bt_node
      - nav2_back_up_action_bt_node
      - nav2_spin_action_bt_node
      - nav2_wait_action_bt_node
      - nav2_clear_costmap_service_bt_node
      - nav2_is_stuck_condition_bt_node
      - nav2_goal_reached_condition_bt_node
      - nav2_goal_updated_condition_bt_node
      - nav2_initial_pose_received_condition_bt_node
      - nav2_reinitialize_global_localization_service_bt_node
      - nav2_rate_controller_bt_node
      - nav2_distance_controller_bt_node
      - nav2_speed_controller_bt_node
      - nav2_truncate_path_action_bt_node
      - nav2_goal_updater_node_bt_node
      - nav2_recovery_node_bt_node
      - nav2_pipeline_sequence_bt_node
      - nav2_round_robin_node_bt_node
      - nav2_transform_available_condition_bt_node
      - nav2_time_expired_condition_bt_node
      - nav2_path_expiring_timer_condition
      - nav2_distance_traveled_condition_bt_node
      - nav2_single_trigger_bt_node
      - nav2_is_battery_low_condition_bt_node
      - nav2_navigate_through_poses_action_bt_node
      - nav2_navigate_to_pose_action_bt_node
      - nav2_remove_passed_goals_action_bt_node
      - nav2_planner_selector_bt_node
      - nav2_controller_selector_bt_node
      - nav2_goal_checker_selector_bt_node

controller_server:
  ros__parameters:
    use_sim_time: True
    controller_frequency: 20.0
    min_x_velocity_threshold: 0.001
    min_y_velocity_threshold: 0.5
    min_theta_velocity_threshold: 0.001
    failure_tolerance: 0.3
    progress_checker_plugin: "progress_checker"
    goal_checker_plugins: ["general_goal_checker"]
    controller_plugins: ["FollowPath"]
    
    progress_checker:
      plugin: "nav2_controller::SimpleProgressChecker"
      required_movement_radius: 0.5
      movement_time_allowance: 10.0
    
    general_goal_checker:
      stateful: True
      plugin: "nav2_controller::SimpleGoalChecker"
      xy_goal_tolerance: 0.25
      yaw_goal_tolerance: 0.25
    
    FollowPath:
      plugin: "nav2_controller::DWBController"
      debug_trajectory_details: True
      min_vel_x: 0.0
      min_vel_y: 0.0
      max_vel_x: 0.5
      max_vel_y: 0.0
      max_vel_theta: 1.0
      min_speed_xy: 0.0
      max_speed_xy: 0.5
      min_speed_theta: 0.0
      acc_lim_x: 2.5
      acc_lim_y: 0.0
      acc_lim_theta: 3.2
      decel_lim_x: -2.5
      decel_lim_y: 0.0
      decel_lim_theta: -3.2
      vx_samples: 20
      vy_samples: 0
      vtheta_samples: 40
      sim_time: 2.0
      linear_granularity: 0.05
      angular_granularity: 0.025
      transform_tolerance: 0.2
      xy_goal_tolerance: 0.05
      trans_stopped_velocity: 0.25
      short_circuit_trajectory_evaluation: True
      stateful: True
      critics: ["RotateToGoal", "Oscillation", "BaseObstacle", "PathAlign", "PathDist", "GoalDist"]
      BaseObstacle.scale: 0.02
      PathAlign.scale: 32.0
      PathAlign.forward_point_distance: 0.1
      GoalDist.scale: 24.0
      RotateToGoal.scale: 32.0
      RotateToGoal.slowing_factor: 5.0
      RotateToGoal.lookahead_time: -1.0
```

## Perception Pipeline

### Camera Data Processing

```python
#!/usr/bin/env python3
"""
Isaac Sim Perception Pipeline
Processes camera data from Isaac Sim for ROS 2 consumption
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class IsaacPerceptionNode(Node):
    def __init__(self):
        super().__init__('isaac_perception')
        
        self.bridge = CvBridge()
        
        # Subscriber for Isaac Sim camera
        self.camera_sub = self.create_subscription(
            Image, '/camera/color/image_raw',
            self.camera_callback, 10)
        
        # Publishers for processed data
        self.depth_pub = self.create_publisher(Image, '/camera/depth/image_raw', 10)
        self.features_pub = self.create_publisher(Image, '/camera/features', 10)
        
        self.get_logger().info('Isaac Perception Node initialized')
    
    def camera_callback(self, msg: Image):
        """Process camera image from Isaac Sim"""
        # Convert ROS image to OpenCV
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='rgb8')
        
        # Convert to BGR for OpenCV
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
        
        # Process image (example: edge detection)
        edges = cv2.Canny(cv_image, 100, 200)
        edges_color = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        
        # Publish processed image
        depth_msg = self.bridge.cv2_to_imgmsg(edges_color, encoding='bgr8')
        depth_msg.header = msg.header
        self.features_pub.publish(depth_msg)
        
        self.get_logger().debug(f'Processed image: {msg.width}x{msg.height}')

def main(args=None):
    rclpy.init(args=args)
    node = IsaacPerceptionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Complete Integration Example

### Launch File

```python
# launch/isaac_ros2_integration.launch.py

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Isaac Sim launch
    isaac_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('isaac_ros2_bridge'),
                'launch',
                'isaac_sim.launch.py'
            ])
        ]),
        launch_arguments={
            'usd_path': '/path/to/humanoid_scene.usd'
        }.items()
    )
    
    # ROS 2 control
    ros2_control = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=['config/isaac_ros2_control.yaml'],
        output='screen'
    )
    
    # Navigation
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('nav2_bringup'),
                'launch',
                'navigation_launch.py'
            ])
        ]),
        launch_arguments={
            'params_file': 'config/nav2_params.yaml',
            'use_sim_time': 'True'
        }.items()
    )
    
    # Perception
    perception = Node(
        package='isaac_perception',
        executable='perception_node',
        output='screen'
    )
    
    return LaunchDescription([
        DeclareLaunchArgument('usd_path'),
        isaac_sim,
        ros2_control,
        nav2,
        perception,
    ])
```

## Resources

### Documentation

- [Isaac ROS Documentation](https://nvidia-isaac-ros.github.io/)
- [ROS 2 Control](https://control.ros.org/)
- [Nav2 Documentation](https://navigation.ros.org/)

### Packages

- [isaac_ros_common](https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_common)
- [isaac_ros_image_pipeline](https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_image_pipeline)

## Exercises

1. **Bridge Setup**: Configure ROS 2 bridge for bidirectional communication
2. **Control Integration**: Implement ROS 2 control with Isaac Sim
3. **Navigation Stack**: Set up Nav2 for robot navigation in Isaac Sim
4. **Perception Pipeline**: Create a camera processing pipeline

## Next Steps

Proceed to [Week 10 - Perception Models](./week-10-perception-models.md) for vision and sensor processing.
