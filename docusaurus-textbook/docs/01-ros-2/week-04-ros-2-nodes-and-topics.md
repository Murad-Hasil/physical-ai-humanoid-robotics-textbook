---
id: week-04-ros-2-nodes-and-topics
title: Week 4 - ROS 2 Nodes and Topics
sidebar_label: Week 4 - ROS 2 Nodes and Topics
sidebar_position: 4
description: Create ROS 2 nodes, implement publish/subscribe patterns, and work with custom messages
---

# Week 4 - ROS 2 Nodes and Topics

## Learning Objectives

By the end of this week, you will be able to:

- Create ROS 2 nodes in Python and C++
- Implement publish/subscribe communication patterns
- Define custom message types
- Use QoS policies for reliable communication

## Overview

Nodes and topics form the foundation of ROS 2 communication. Nodes are executable processes that perform computation, while topics are named buses for data exchange using the publish/subscribe pattern.

## Node Architecture

### Node Lifecycle

```
┌─────────────┐
│   Created   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Active    │ ◀─────── spin() / spin_once()
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Destroyed  │
└─────────────┘
```

### Python Node Implementation

```python
#!/usr/bin/env python3
"""
ROS 2 Node with Publisher and Subscriber
Demonstrates bidirectional communication
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32
from sensor_msgs.msg import Image
import numpy as np

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')
        
        # Declare parameters
        self.declare_parameter('robot_name', 'humanoid_01')
        self.declare_parameter('control_rate', 100.0)  # Hz
        
        # Get parameters
        self.robot_name = self.get_parameter('robot_name').value
        control_rate = self.get_parameter('control_rate').value
        
        # Publishers
        self.command_pub = self.create_publisher(
            String, f'/{self.robot_name}/commands', 10)
        self.status_pub = self.create_publisher(
            String, f'/{self.robot_name}/status', 10)
        
        # Subscribers
        self.sensor_sub = self.create_subscription(
            String, f'/{self.robot_name}/sensors',
            self.sensor_callback, 10)
        
        # Timer for periodic publishing
        self.timer = self.create_timer(1.0 / control_rate, self.control_loop)
        
        self.get_logger().info(f'Robot Controller initialized: {self.robot_name}')
    
    def sensor_callback(self, msg: String):
        """Process incoming sensor data"""
        self.get_logger().debug(f'Received sensor data: {msg.data}')
        # Process and republish status
        status_msg = String()
        status_msg.data = f'Status: Processing {msg.data}'
        self.status_pub.publish(status_msg)
    
    def control_loop(self):
        """Main control loop"""
        command_msg = String()
        command_msg.data = f'Command from {self.robot_name}'
        self.command_pub.publish(command_msg)

def main(args=None):
    rclpy.init(args=args)
    node = RobotController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### C++ Node Implementation

```cpp
// robot_controller.cpp
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include <memory>
#include <chrono>

class RobotController : public rclcpp::Node
{
public:
    RobotController()
    : Node("robot_controller"), count_(0)
    {
        // Declare parameters
        this->declare_parameter<std::string>("robot_name", "humanoid_01");
        this->declare_parameter<double>("control_rate", 100.0);
        
        // Get parameters
        std::string robot_name = this->get_parameter("robot_name").as_string();
        double control_rate = this->get_parameter("control_rate").as_double();
        
        // Publishers
        command_publisher_ = this->create_publisher<std_msgs::msg::String>(
            "/" + robot_name + "/commands", 10);
        status_publisher_ = this->create_publisher<std_msgs::msg::String>(
            "/" + robot_name + "/status", 10);
        
        // Subscribers
        sensor_subscription_ = this->create_subscription<std_msgs::msg::String>(
            "/" + robot_name + "/sensors", 10,
            std::bind(&RobotController::sensor_callback, this, std::placeholders::_1));
        
        // Timer
        auto period = std::chrono::milliseconds(static_cast<int>(1000.0 / control_rate));
        timer_ = this->create_wall_timer(
            period, std::bind(&RobotController::control_loop, this));
        
        RCLCPP_INFO(this->get_logger(), "Robot Controller initialized: %s", robot_name.c_str());
    }

private:
    void sensor_callback(const std_msgs::msg::String::SharedPtr msg)
    {
        RCLCPP_DEBUG(this->get_logger(), "Received sensor data: %s", msg->data.c_str());
        
        auto status_msg = std_msgs::msg::String();
        status_msg.data = "Status: Processing " + msg->data;
        status_publisher_->publish(status_msg);
    }
    
    void control_loop()
    {
        auto command_msg = std_msgs::msg::String();
        command_msg.data = "Command from humanoid_01";
        command_publisher_->publish(command_msg);
        count_++;
    }
    
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr command_publisher_;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr status_publisher_;
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr sensor_subscription_;
    rclcpp::TimerBase::SharedPtr timer_;
    size_t count_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<RobotController>());
    rclcpp::shutdown();
    return 0;
}
```

## Custom Messages

### Defining Custom Message Types

```yaml
# msg/JointCommand.msg
# Joint command for humanoid robot actuation

string joint_name      # Name of the joint
float64 position       # Desired position (radians)
float64 velocity       # Desired velocity (rad/s)
float64 effort         # Desired effort (Nm)
float64 stiffness      # Stiffness gain
float64 damping        # Damping gain
```

### Package Configuration for Custom Messages

```python
# setup.py
from setuptools import setup
from glob import glob
import os

package_name = 'humanoid_interfaces'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'msg'), glob('msg/*.msg')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Your Name',
    author_email='your.email@example.com',
    description='Custom interfaces for humanoid robot',
    license='Apache 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'controller = humanoid_interfaces.controller:main',
        ],
    },
)
```

```xml
<!-- package.xml -->
<?xml version="1.0"?>
<package format="3">
  <name>humanoid_interfaces</name>
  <version>0.1.0</version>
  <description>Custom interfaces for humanoid robot</description>
  
  <maintainer email="your.email@example.com">Your Name</maintainer>
  <license>Apache 2.0</license>
  
  <buildtool_depend>ament_cmake</buildtool_depend>
  <buildtool_depend>ament_cmake_python</buildtool_depend>
  
  <depend>std_msgs</depend>
  <depend>sensor_msgs</depend>
  <depend>geometry_msgs</depend>
  
  <build_depend>rosidl_default_generators</build_depend>
  <exec_depend>rosidl_default_runtime</exec_depend>
  
  <member_of_group>rosidl_interface_packages</member_of_group>
  
  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
```

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.8)
project(humanoid_interfaces)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/JointCommand.msg"
  "msg/HumanoidState.msg"
  "srv/GetJointState.srv"
  DEPENDENCIES std_msgs sensor_msgs
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
```

## QoS Policies

### Quality of Service Configuration

```python
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSDurabilityPolicy

# Reliable communication (for critical commands)
reliable_qos = QoSProfile(
    reliability=QoSReliabilityPolicy.RELIABLE,
    durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
    depth=10
)

# Best-effort communication (for sensor data)
sensor_qos = QoSProfile(
    reliability=QoSReliabilityPolicy.BEST_EFFORT,
    durability=QoSDurabilityPolicy.VOLATILE,
    depth=100
)

# Create publishers with different QoS
self.command_pub = self.create_publisher(
    String, '/commands', reliable_qos)
self.sensor_pub = self.create_publisher(
    Image, '/camera/image', sensor_qos)
```

## Resources

### Documentation

- [ROS 2 Nodes](https://docs.ros.org/en/humble/Concepts/About-Nodes.html)
- [ROS 2 Topics](https://docs.ros.org/en/humble/Concepts/About-Topics.html)
- [ROS 2 Interfaces](https://docs.ros.org/en/humble/Concepts/About-Interfaces.html)
- [QoS Policies](https://docs.ros.org/en/humble/Concepts/About-Quality-of-Service-Settings.html)

### Tools

- [ros2 interface](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Introspection-with-ROS2-Interface.html) - Interface introspection
- [rqt_graph](http://wiki.ros.org/rqt_graph) - Node graph visualization

## Exercises

1. **Publisher/Subscriber Pair**: Create a node pair that communicates via custom messages
2. **Multi-Node System**: Launch 3+ nodes that communicate through topics
3. **QoS Experiment**: Test different QoS policies and observe behavior
4. **C++ Conversion**: Convert the Python node to C++ (or vice versa)

## Next Steps

Proceed to [Week 5 - ROS 2 Services and Actions](./week-05-ros-2-services-and-actions.md) for synchronous and asynchronous communication patterns.
