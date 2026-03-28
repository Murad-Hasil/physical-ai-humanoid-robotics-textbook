---
id: week-11-humanoid-robot-basics
title: Week 11 - Humanoid Robot Basics
sidebar_label: Week 11 - Humanoid Robot Basics
sidebar_position: 11
description: Humanoid robot kinematics, dynamics, balance control, and locomotion fundamentals
---

# Week 11 - Humanoid Robot Basics

## Learning Objectives

By the end of this week, you will be able to:

- Understand humanoid robot kinematics and dynamics
- Implement inverse kinematics for arm and leg control
- Design balance control algorithms for bipedal locomotion
- Configure whole-body control for coordinated movement

## Overview

Humanoid robots present unique challenges in control due to their high degrees of freedom, underactuated dynamics, and balance requirements. This week covers the fundamentals of humanoid robot control.

### Humanoid Robot Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Humanoid Robot System                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐         │
│  │    Head     │  │    Arms     │  │      Torso       │         │
│  │   (2 DOF)   │  │  (7 DOF ea) │  │     (3 DOF)      │         │
│  └─────────────┘  └─────────────┘  └──────────────────┘         │
│                                                                  │
│  ┌─────────────┐                    ┌──────────────────┐         │
│  │  Left Leg   │                    │   Right Leg      │         │
│  │   (6 DOF)   │                    │    (6 DOF)       │         │
│  │  - Hip (3)  │                    │   - Hip (3)      │         │
│  │  - Knee (1) │                    │   - Knee (1)     │         │
│  │  - Ankle(2) │                    │   - Ankle (2)    │         │
│  └─────────────┘                    └──────────────────┘         │
│                                                                  │
│              Total: ~28-32 Degrees of Freedom                    │
└─────────────────────────────────────────────────────────────────┘
```

## Hardware Requirements

| Component | Specification | Purpose |
|-----------|---------------|---------|
| **Actuators** | Dynamixel XM/XL series | Joint actuation |
| **IMU** | 9-axis (accel + gyro + mag) | Balance sensing |
| **Force Sensors** | FSR in feet | Ground contact detection |
| **Compute** | Jetson Orin / Intel NUC | Onboard processing |
| **Battery** | 6S LiPo (22.2V) | Power system |

## Kinematics

### Forward Kinematics

```python
#!/usr/bin/env python3
"""
Humanoid Robot Forward Kinematics
Computes end-effector position from joint angles
"""

import numpy as np
from typing import List, Tuple

class HumanoidKinematics:
    def __init__(self):
        # Link lengths (meters)
        self.l_thigh = 0.4
        self.l_shin = 0.4
        self.l_upper_arm = 0.3
        self.l_forearm = 0.3
        self.l_torso = 0.5
        self.l_hip_offset = 0.1
    
    def rotation_matrix(self, axis: str, angle: float) -> np.ndarray:
        """Create rotation matrix around specified axis"""
        c, s = np.cos(angle), np.sin(angle)
        if axis == 'x':
            return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
        elif axis == 'y':
            return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
        elif axis == 'z':
            return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    
    def leg_forward_kinematics(self, joint_angles: List[float], side: str = 'left') -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute foot position and orientation from joint angles
        
        Args:
            joint_angles: [hip_roll, hip_pitch, hip_yaw, knee_pitch, ankle_pitch, ankle_roll]
            side: 'left' or 'right'
        
        Returns:
            position: (x, y, z) position of foot
            orientation: 3x3 rotation matrix
        """
        hip_roll, hip_pitch, hip_yaw, knee_pitch, ankle_pitch, ankle_roll = joint_angles
        
        # Base offset
        offset = self.l_hip_offset if side == 'right' else -self.l_hip_offset
        
        # Homogeneous transformation matrices
        T_hip = np.eye(4)
        T_hip[0, 3] = offset
        T_hip[:3, :3] = self.rotation_matrix('x', hip_roll) @ \
                        self.rotation_matrix('y', hip_pitch) @ \
                        self.rotation_matrix('z', hip_yaw)
        
        # Thigh
        T_thigh = np.eye(4)
        T_thigh[2, 3] = -self.l_thigh
        T_thigh[:3, :3] = self.rotation_matrix('y', knee_pitch)
        
        # Shin
        T_shin = np.eye(4)
        T_shin[2, 3] = -self.l_shin
        T_shin[:3, :3] = self.rotation_matrix('y', ankle_pitch) @ \
                         self.rotation_matrix('x', ankle_roll)
        
        # Composite transformation
        T_total = T_hip @ T_thigh @ T_shin
        
        position = T_total[:3, 3]
        orientation = T_total[:3, :3]
        
        return position, orientation
    
    def arm_forward_kinematics(self, joint_angles: List[float], side: str = 'left') -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute hand position and orientation from joint angles
        
        Args:
            joint_angles: [shoulder_pitch, shoulder_roll, shoulder_yaw, elbow_pitch, elbow_yaw, wrist_pitch, wrist_roll]
            side: 'left' or 'right'
        
        Returns:
            position: (x, y, z) position of hand
            orientation: 3x3 rotation matrix
        """
        # Implementation similar to leg kinematics
        # Simplified for brevity
        pass

# Example usage
if __name__ == '__main__':
    kinematics = HumanoidKinematics()
    
    # Left leg joint angles (radians)
    left_leg_angles = [0.0, -0.2, 0.0, 0.4, -0.2, 0.0]
    
    position, orientation = kinematics.leg_forward_kinematics(left_leg_angles, 'left')
    print(f"Foot position: {position}")
    print(f"Foot orientation:\n{orientation}")
```

### Inverse Kinematics

```python
#!/usr/bin/env python3
"""
Humanoid Robot Inverse Kinematics
Computes joint angles from desired end-effector position
"""

import numpy as np
from scipy.optimize import minimize
from typing import List, Optional

class HumanoidInverseKinematics:
    def __init__(self, kinematics: HumanoidKinematics):
        self.kinematics = kinematics
        self.joint_limits = {
            'hip_roll': (-0.5, 0.5),
            'hip_pitch': (-0.5, 0.5),
            'hip_yaw': (-0.5, 0.5),
            'knee_pitch': (0.0, 2.5),
            'ankle_pitch': (-0.5, 0.5),
            'ankle_roll': (-0.3, 0.3),
        }
    
    def objective(self, joint_angles: np.ndarray, target_position: np.ndarray) -> float:
        """Objective function: minimize distance to target"""
        current_position, _ = self.kinematics.leg_forward_kinematics(joint_angles.tolist())
        return np.linalg.norm(current_position - target_position)
    
    def solve(self, target_position: np.ndarray, initial_guess: Optional[np.ndarray] = None, 
              side: str = 'left') -> np.ndarray:
        """
        Solve inverse kinematics using optimization
        
        Args:
            target_position: Desired foot position (x, y, z)
            initial_guess: Initial joint angles (default: standing pose)
            side: 'left' or 'right'
        
        Returns:
            joint_angles: Solution joint angles
        """
        if initial_guess is None:
            initial_guess = np.array([0.0, -0.1, 0.0, 0.3, -0.2, 0.0])
        
        # Bounds for optimization
        bounds = [
            self.joint_limits['hip_roll'],
            self.joint_limits['hip_pitch'],
            self.joint_limits['hip_yaw'],
            self.joint_limits['knee_pitch'],
            self.joint_limits['ankle_pitch'],
            self.joint_limits['ankle_roll'],
        ]
        
        # Optimize
        result = minimize(
            self.objective,
            initial_guess,
            args=(target_position,),
            method='L-BFGS-B',
            bounds=bounds
        )
        
        if result.success:
            return result.x
        else:
            raise RuntimeError(f"IK failed: {result.message}")

# Example usage
if __name__ == '__main__':
    kinematics = HumanoidKinematics()
    ik = HumanoidInverseKinematics(kinematics)
    
    # Target foot position
    target = np.array([0.0, -0.1, -0.8])
    
    # Solve IK
    joint_angles = ik.solve(target, side='left')
    print(f"Joint angles: {joint_angles}")
    
    # Verify with forward kinematics
    position, _ = kinematics.leg_forward_kinematics(joint_angles.tolist(), 'left')
    print(f"Verified position: {position}")
```

## Balance Control

### Zero Moment Point (ZMP) Control

```python
#!/usr/bin/env python3
"""
ZMP Balance Control for Humanoid Robot
Implements Zero Moment Point based balance control
"""

import numpy as np
from typing import Tuple

class ZMPController:
    def __init__(self):
        # Robot parameters
        self.mass = 50.0  # kg
        self.com_height = 0.8  # m (center of mass height)
        self.gravity = 9.81  # m/s^2
        
        # Foot dimensions
        self.foot_length = 0.25  # m
        self.foot_width = 0.12  # m
        
        # ZMP support polygon
        self.support_polygon = self._compute_support_polygon()
    
    def _compute_support_polygon(self) -> np.ndarray:
        """Compute support polygon from foot positions"""
        # Simplified: rectangular support area
        return np.array([
            [-self.foot_length/2, -self.foot_width/2],
            [self.foot_length/2, -self.foot_width/2],
            [self.foot_length/2, self.foot_width/2],
            [-self.foot_length/2, self.foot_width/2],
        ])
    
    def compute_zmp(self, com_position: np.ndarray, com_acceleration: np.ndarray,
                    foot_forces: np.ndarray) -> np.ndarray:
        """
        Compute Zero Moment Point from CoM state and foot forces
        
        Args:
            com_position: Center of mass position (x, y, z)
            com_acceleration: CoM acceleration (x, y, z)
            foot_forces: Ground reaction forces from each foot
        
        Returns:
            zmp_position: (x, y) ZMP location
        """
        x, y, z = com_position
        ax, ay, az = com_acceleration
        
        # ZMP equations (simplified linear inverted pendulum)
        zmp_x = x - (z / self.gravity) * ax
        zmp_y = y - (z / self.gravity) * ay
        
        return np.array([zmp_x, zmp_y])
    
    def is_stable(self, zmp_position: np.ndarray) -> bool:
        """Check if ZMP is within support polygon"""
        # Point-in-polygon test
        from matplotlib.path import Path
        polygon = Path(self.support_polygon)
        return polygon.contains_point(zmp_position)
    
    def compute_balance_correction(self, zmp_position: np.ndarray, 
                                   current_velocity: np.ndarray) -> np.ndarray:
        """
        Compute corrective action to maintain balance
        
        Args:
            zmp_position: Current ZMP location
            current_velocity: Current CoM velocity
        
        Returns:
            correction: Desired CoM acceleration correction
        """
        if self.is_stable(zmp_position):
            return np.array([0.0, 0.0])
        
        # Compute distance to support polygon boundary
        # Simple proportional control
        kp = 10.0
        kd = 2.0
        
        # Find closest point on support polygon boundary
        from scipy.spatial import distance
        distances = [distance.euclidean(zmp_position, p) for p in self.support_polygon]
        closest_idx = np.argmin(distances)
        closest_point = self.support_polygon[closest_idx]
        
        # Error vector (pointing toward support polygon)
        error = closest_point - zmp_position
        
        # PD control
        correction = kp * error - kd * current_velocity[:2]
        
        return correction

# Example usage
if __name__ == '__main__':
    controller = ZMPController()
    
    # Robot state
    com_pos = np.array([0.0, 0.0, 0.8])
    com_accel = np.array([0.5, 0.1, 0.0])
    foot_forces = np.array([245.0, 245.0])  # N per foot
    
    # Compute ZMP
    zmp = controller.compute_zmp(com_pos, com_accel, foot_forces)
    print(f"ZMP position: {zmp}")
    
    # Check stability
    stable = controller.is_stable(zmp)
    print(f"Stable: {stable}")
    
    if not stable:
        correction = controller.compute_balance_correction(zmp, np.array([0.1, 0.05, 0.0]))
        print(f"Balance correction: {correction}")
```

## Locomotion Control

### Walking Pattern Generator

```python
#!/usr/bin/env python3
"""
Humanoid Walking Pattern Generator
Generates foot trajectories for bipedal locomotion
"""

import numpy as np
from typing import List, Tuple

class WalkingPatternGenerator:
    def __init__(self):
        # Walking parameters
        self.step_length = 0.3  # m
        self.step_height = 0.05  # m
        self.step_time = 0.5  # s
        self.double_support_time = 0.1  # s
        self.hip_offset = 0.1  # m
    
    def generate_foot_trajectory(self, start_pos: np.ndarray, end_pos: np.ndarray,
                                  time: float) -> np.ndarray:
        """
        Generate smooth foot trajectory using quintic polynomial
        
        Args:
            start_pos: Starting foot position (x, y, z)
            end_pos: Target foot position (x, y, z)
            time: Normalized time (0 to 1)
        
        Returns:
            position: Foot position at given time
        """
        # Quintic polynomial coefficients for smooth motion
        # s(t) = 10t³ - 15t⁴ + 6t⁵
        s = 10 * time**3 - 15 * time**4 + 6 * time**5
        
        # Horizontal motion
        x = start_pos[0] + s * (end_pos[0] - start_pos[0])
        y = start_pos[1] + s * (end_pos[1] - start_pos[1])
        
        # Vertical motion (parabolic arc)
        if time < 0.5:
            z = start_pos[2] + 4 * self.step_height * time
        else:
            z = start_pos[2] + 4 * self.step_height * (1 - time)
        
        return np.array([x, y, z])
    
    def generate_walking_pattern(self, num_steps: int, direction: str = 'forward') -> List[Tuple[np.ndarray, np.ndarray]]:
        """
        Generate complete walking pattern
        
        Args:
            num_steps: Number of steps to generate
            direction: 'forward', 'backward', 'left', 'right'
        
        Returns:
            trajectories: List of (left_foot_traj, right_foot_traj) for each step
        """
        trajectories = []
        
        # Initial positions
        left_pos = np.array([0.0, self.hip_offset, 0.0])
        right_pos = np.array([0.0, -self.hip_offset, 0.0])
        
        for step in range(num_steps):
            # Determine step direction
            if direction == 'forward':
                step_offset = np.array([self.step_length, 0, 0])
            elif direction == 'backward':
                step_offset = np.array([-self.step_length, 0, 0])
            elif direction == 'left':
                step_offset = np.array([0, self.step_length, 0])
            elif direction == 'right':
                step_offset = np.array([0, -self.step_length, 0])
            
            # Alternate legs
            if step % 2 == 0:
                # Left leg swing
                left_target = left_pos + step_offset
                right_target = right_pos
                
                # Generate trajectory
                left_traj = [self.generate_foot_trajectory(left_pos, left_target, t/100) 
                            for t in range(101)]
                right_traj = [right_pos] * 101
                
                left_pos = left_target
            else:
                # Right leg swing
                right_target = right_pos + step_offset
                left_target = left_pos
                
                # Generate trajectory
                right_traj = [self.generate_foot_trajectory(right_pos, right_target, t/100) 
                             for t in range(101)]
                left_traj = [left_pos] * 101
                
                right_pos = right_target
            
            trajectories.append((np.array(left_traj), np.array(right_traj)))
        
        return trajectories

# Example usage
if __name__ == '__main__':
    generator = WalkingPatternGenerator()
    
    # Generate 4 steps forward
    patterns = generator.generate_walking_pattern(4, 'forward')
    
    for i, (left_traj, right_traj) in enumerate(patterns):
        print(f"Step {i+1}: Left foot ends at {left_traj[-1]}, Right foot ends at {right_traj[-1]}")
```

## Whole-Body Control

### Task-Space Control

```python
#!/usr/bin/env python3
"""
Whole-Body Task-Space Control
Coordinates multiple tasks for humanoid robot
"""

import numpy as np
from typing import List, Dict

class WholeBodyController:
    def __init__(self, num_joints: int):
        self.num_joints = num_joints
        
        # Task weights
        self.task_weights = {
            'balance': 1.0,
            'foot_placement': 0.8,
            'arm_reach': 0.5,
            'posture': 0.3,
        }
    
    def compute_jacobian(self, joint_angles: np.ndarray, task_type: str) -> np.ndarray:
        """Compute task Jacobian for specified task"""
        # Simplified: return random Jacobian
        # In practice, compute from kinematics
        if task_type == 'balance':
            return np.random.randn(2, self.num_joints)
        elif task_type == 'foot_placement':
            return np.random.randn(6, self.num_joints)
        elif task_type == 'arm_reach':
            return np.random.randn(3, self.num_joints)
        else:
            return np.random.randn(self.num_joints, self.num_joints)
    
    def compute_control(self, joint_angles: np.ndarray, 
                        tasks: Dict[str, Dict]) -> np.ndarray:
        """
        Compute joint torques for multiple tasks
        
        Args:
            joint_angles: Current joint configuration
            tasks: Dictionary of task specifications
                {task_name: {'error': error_vector, 'jacobian': J}}
        
        Returns:
            torques: Joint torque commands
        """
        # Weighted sum of task controls
        total_torque = np.zeros(self.num_joints)
        
        for task_name, task_spec in tasks.items():
            weight = self.task_weights.get(task_name, 0.5)
            error = task_spec['error']
            J = task_spec.get('jacobian', self.compute_jacobian(joint_angles, task_name))
            
            # Task-space control: τ = J^T * (Kp * error + Kd * error_dot)
            Kp = 100.0
            Kd = 10.0
            
            task_torque = J.T @ (Kp * error)
            total_torque += weight * task_torque
        
        return total_torque

# Example usage
if __name__ == '__main__':
    controller = WholeBodyController(num_joints=28)
    
    # Current state
    joint_angles = np.zeros(28)
    
    # Task specifications
    tasks = {
        'balance': {'error': np.array([0.01, 0.02])},
        'foot_placement': {'error': np.array([0.0, 0.0, 0.01, 0.0, 0.0, 0.0])},
        'arm_reach': {'error': np.array([0.05, 0.0, 0.02])},
    }
    
    # Compute control
    torques = controller.compute_control(joint_angles, tasks)
    print(f"Joint torques: {torques[:8]}...")  # Print first 8
```

## Resources

### Documentation

- [Humanoid Robotics: A Reference Guide](https://www.researchgate.net/publication/Humanoid_Robotics)
- [Modern Robotics Textbook](http://hades.mech.northwestern.edu/index.php/Modern_Robotics)
- [ROS 2 Control](https://control.ros.org/)

### Libraries

- [Pinocchio](https://github.com/stack-of-tasks/pinocchio) - Rigid body dynamics
- [Bullet3](https://github.com/bulletphysics/bullet3) - Physics engine
- [OSQP](https://osqp.org/) - Optimization solver

## Exercises

1. **Forward Kinematics**: Implement FK for a 6-DOF leg
2. **Inverse Kinematics**: Solve IK for foot placement
3. **ZMP Control**: Implement ZMP-based balance controller
4. **Walking Pattern**: Generate walking trajectories for multiple steps

## Next Steps

Proceed to [Week 12 - Conversational AI Integration](./week-12-conversational-ai-integration.md) for language model integration.
