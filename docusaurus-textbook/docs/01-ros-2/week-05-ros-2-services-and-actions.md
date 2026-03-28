---
id: week-05-ros-2-services-and-actions
title: Week 5 - ROS 2 Services and Actions
sidebar_label: Week 5 - ROS 2 Services and Actions
sidebar_position: 5
description: Implement synchronous services and asynchronous actions for robot control
---

# Week 5 - ROS 2 Services and Actions

## Learning Objectives

By the end of this week, you will be able to:

- Implement synchronous request/response communication with services
- Create asynchronous goal-based communication with actions
- Design service and action interfaces for robot control
- Handle long-running tasks with feedback and cancellation

## Overview

While topics provide continuous data streams, services and actions enable structured communication patterns:

- **Services**: Synchronous request/response for immediate operations
- **Actions**: Asynchronous goal-based communication for long-running tasks with feedback

## Service Communication

### Service Architecture

```
┌─────────────┐         Request         ┌─────────────┐
│   Client    │ ───────────────────────▶│   Server    │
│             │                         │             │
│             │ ◀───────────────────────│             │
└─────────────┘        Response         └─────────────┘
     (Blocks until response received)
```

### Service Definition

```yaml
# srv/GetJointState.srv
# Get current joint state

string joint_name      # Request: joint to query
---
float64 position       # Response: current position
float64 velocity       # Response: current velocity
float64 effort         # Response: current effort
bool is_moving         # Response: movement status
```

### Python Service Server

```python
#!/usr/bin/env python3
"""
ROS 2 Service Server for Joint State Queries
"""

import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
from humanoid_interfaces.srv import GetJointState

class JointStateService(Node):
    def __init__(self):
        super().__init__('joint_state_service')
        
        # Simulated joint states (in real system, read from hardware)
        self.joint_states = {
            'left_arm_shoulder': {'position': 0.5, 'velocity': 0.0, 'effort': 0.0},
            'right_arm_shoulder': {'position': -0.5, 'velocity': 0.0, 'effort': 0.0},
            'left_knee': {'position': 0.0, 'velocity': 0.0, 'effort': 0.0},
            'right_knee': {'position': 0.0, 'velocity': 0.0, 'effort': 0.0},
        }
        
        # Create service
        self.service = self.create_service(
            GetJointState, 'get_joint_state', self.get_joint_state_callback)
        
        self.get_logger().info('Joint State Service ready')
    
    def get_joint_state_callback(self, request, response):
        """Handle joint state queries"""
        joint_name = request.joint_name
        
        if joint_name in self.joint_states:
            state = self.joint_states[joint_name]
            response.position = state['position']
            response.velocity = state['velocity']
            response.effort = state['effort']
            response.is_moving = abs(state['velocity']) > 0.01
            self.get_logger().info(f'Served joint state for: {joint_name}')
        else:
            self.get_logger().warn(f'Unknown joint: {joint_name}')
            response.position = 0.0
            response.velocity = 0.0
            response.effort = 0.0
            response.is_moving = False
        
        return response

def main(args=None):
    rclpy.init(args=args)
    node = JointStateService()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Python Service Client

```python
#!/usr/bin/env python3
"""
ROS 2 Service Client for Joint State Queries
"""

import rclpy
from rclpy.node import Node
from humanoid_interfaces.srv import GetJointState

class JointStateClient(Node):
    def __init__(self):
        super().__init__('joint_state_client')
        self.client = self.create_client(GetJointState, 'get_joint_state')
        
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting...')
    
    def send_request(self, joint_name):
        """Send joint state request"""
        request = GetJointState.Request()
        request.joint_name = joint_name
        
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        
        if future.result() is not None:
            response = future.result()
            self.get_logger().info(
                f'Joint: {joint_name}, '
                f'Position: {response.position:.3f}, '
                f'Velocity: {response.velocity:.3f}'
            )
            return response
        else:
            self.get_logger().error('Service call failed')
            return None

def main(args=None):
    rclpy.init(args=args)
    node = JointStateClient()
    
    # Query multiple joints
    joints = ['left_arm_shoulder', 'right_knee', 'left_knee']
    for joint in joints:
        node.send_request(joint)
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Action Communication

### Action Architecture

```
┌─────────────┐         Goal          ┌─────────────┐
│   Client    │ ─────────────────────▶│   Server    │
│             │                       │             │
│             │ ◀─────────────────────│             │
└─────────────┘       Feedback        └─────────────┘
     (Non-blocking, receives periodic updates)

┌─────────────┐        Result         ┌─────────────┐
│   Client    │ ◀─────────────────────│   Server    │
│             │   (When goal completes)│             │
└─────────────┘                       └─────────────┘
```

### Action Definition

```yaml
# action/MoveToPosition.action
# Action to move robot to target position

geometry_msgs/PoseStamped target_pose   # Goal: target position
float64 timeout                         # Goal: maximum time allowed
---
geometry_msgs/PoseStamped final_pose    # Result: achieved position
bool success                            # Result: whether goal was achieved
string message                          # Result: status message
---
geometry_msgs/PoseStamped current_pose  # Feedback: current position
float64 elapsed_time                    # Feedback: time elapsed
float64 distance_remaining              # Feedback: distance to goal
```

### Python Action Server

```python
#!/usr/bin/env python3
"""
ROS 2 Action Server for Robot Navigation
"""

import rclpy
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from humanoid_interfaces.action import MoveToPosition
from geometry_msgs.msg import PoseStamped
import math
import time

class NavigationActionServer(Node):
    def __init__(self):
        super().__init__('navigation_action_server')
        
        self._action_server = ActionServer(
            self,
            MoveToPosition,
            'move_to_position',
            execute_callback=self.execute_callback,
            callback_group=ReentrantCallbackGroup(),
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback)
        
        self.get_logger().info('Navigation Action Server ready')
    
    def goal_callback(self, goal_request):
        """Accept or reject goal requests"""
        # Validate goal
        if goal_request.target_pose.pose.position.z < 0:
            self.get_logger().warn('Rejected: Invalid target position')
            return GoalResponse.REJECT
        
        self.get_logger().info('Goal accepted')
        return GoalResponse.ACCEPT
    
    def cancel_callback(self, goal_handle):
        """Handle cancellation requests"""
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT
    
    async def execute_callback(self, goal_handle):
        """Execute the navigation goal"""
        self.get_logger().info('Executing navigation goal')
        
        feedback_msg = MoveToPosition.Feedback()
        result = MoveToPosition.Result()
        
        # Simulated navigation
        start_time = time.time()
        target = goal_request.target_pose.pose.position
        current_position = PoseStamped()
        current_position.pose.position.x = 0.0
        current_position.pose.position.y = 0.0
        current_position.pose.position.z = 0.0
        
        # Navigation loop
        while True:
            # Check for cancellation
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result.success = False
                result.message = 'Goal canceled'
                self.get_logger().info('Goal canceled')
                return result
            
            # Update current position (simulated)
            elapsed = time.time() - start_time
            progress = min(elapsed / goal_request.timeout, 1.0)
            
            current_position.pose.position.x = target.x * progress
            current_position.pose.position.y = target.y * progress
            
            # Calculate distance remaining
            dx = target.x - current_position.pose.position.x
            dy = target.y - current_position.pose.position.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Publish feedback
            feedback_msg.current_pose = current_position
            feedback_msg.elapsed_time = elapsed
            feedback_msg.distance_remaining = distance
            goal_handle.publish_feedback(feedback_msg)
            
            self.get_logger().debug(f'Progress: {progress*100:.1f}%')
            
            # Check completion
            if progress >= 1.0:
                break
            
            await asyncio.sleep(0.1)
        
        # Goal succeeded
        goal_handle.succeed()
        result.final_pose = current_position
        result.success = True
        result.message = 'Navigation completed successfully'
        
        self.get_logger().info('Navigation goal completed')
        return result

def main(args=None):
    rclpy.init(args=args)
    node = NavigationActionServer()
    
    executor = MultiThreadedExecutor()
    rclpy.spin(node, executor=executor)
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Python Action Client

```python
#!/usr/bin/env python3
"""
ROS 2 Action Client for Robot Navigation
"""

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from humanoid_interfaces.action import MoveToPosition
from geometry_msgs.msg import Pose, Point, Quaternion

class NavigationActionClient(Node):
    def __init__(self):
        super().__init__('navigation_action_client')
        self._action_client = ActionClient(
            self, MoveToPosition, 'move_to_position')
    
    def send_goal(self, x, y, z, timeout=30.0):
        """Send navigation goal"""
        self.get_logger().info('Waiting for action server...')
        self._action_client.wait_for_server()
        
        goal_msg = MoveToPosition.Goal()
        goal_msg.target_pose.pose.position = Point(x=x, y=y, z=z)
        goal_msg.target_pose.pose.orientation = Quaternion(w=1.0)
        goal_msg.timeout = timeout
        
        self.get_logger().info(f'Sending goal: ({x}, {y}, {z})')
        
        send_goal_future = self._action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback)
        
        send_goal_future.add_done_callback(self.goal_response_callback)
    
    def goal_response_callback(self, future):
        """Handle goal response"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected')
            return
        
        self.get_logger().info('Goal accepted')
        
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.result_callback)
    
    def feedback_callback(self, feedback_msg):
        """Handle feedback"""
        feedback = feedback_msg.feedback
        self.get_logger().info(
            f'Feedback: Position=({feedback.current_pose.pose.position.x:.2f}, '
            f'{feedback.current_pose.pose.position.y:.2f}), '
            f'Distance={feedback.distance_remaining:.2f}m')
    
    def result_callback(self, future):
        """Handle result"""
        result = future.result().result
        self.get_logger().info(
            f'Result: Success={result.success}, Message={result.message}')

def main(args=None):
    rclpy.init(args=args)
    node = NavigationActionClient()
    node.send_goal(1.0, 2.0, 0.0, timeout=30.0)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Comparison: Topics vs Services vs Actions

| Feature | Topics | Services | Actions |
|---------|--------|----------|---------|
| **Pattern** | Publish/Subscribe | Request/Response | Goal/Feedback/Result |
| **Communication** | One-to-many | One-to-one | One-to-one |
| **Blocking** | Non-blocking | Blocking | Non-blocking |
| **Feedback** | Continuous messages | None | Periodic feedback |
| **Cancellation** | Not supported | Not supported | Supported |
| **Use Case** | Sensor data, state | Quick queries | Long-running tasks |

## Resources

### Documentation

- [ROS 2 Services](https://docs.ros.org/en/humble/Concepts/About-Services.html)
- [ROS 2 Actions](https://docs.ros.org/en/humble/Concepts/About-Actions.html)
- [Action Interface Tutorial](https://docs.ros.org/en/humble/Tutorials/Intermediate/Writing-an-Action-Server-Client/Py.html)

### Tools

- [ros2 service](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Introspection-with-ROS2-Service.html) - Service introspection
- [ros2 action](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Introspection-with-ROS2-Action.html) - Action introspection

## Exercises

1. **Service Implementation**: Create a service that returns robot battery status
2. **Action Server**: Implement an action server for arm movement with feedback
3. **Client Integration**: Create a client that uses both services and actions
4. **Error Handling**: Add timeout and retry logic to service calls

## Next Steps

Proceed to [Week 6 - Introduction to Gazebo](../02-gazebo/week-06-introduction-to-gazebo.md) to begin robot simulation.
