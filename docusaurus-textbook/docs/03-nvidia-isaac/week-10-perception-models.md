---
id: week-10-perception-models
title: Week 10 - Perception Models
sidebar_label: Week 10 - Perception Models
sidebar_position: 10
description: Vision models, sensor fusion, and perception pipelines for humanoid robot environmental understanding
---

# Week 10 - Perception Models

## Learning Objectives

By the end of this week, you will be able to:

- Implement vision models for object detection and segmentation
- Configure sensor fusion for multi-modal perception
- Deploy perception pipelines in Isaac Sim
- Integrate perception with robot control systems

## Overview

Perception is the foundation of Physical AI, enabling robots to understand their environment through vision, depth sensing, and multi-modal sensor fusion. This week covers state-of-the-art perception models and their deployment in robotics systems.

### Perception Stack Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Perception Stack                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐       │
│  │   Vision     │  │    Depth     │  │      Audio       │       │
│  │   Models     │  │   Sensing    │  │   Processing     │       │
│  │              │  │              │  │                  │       │
│  │  - YOLO      │  │  - Stereo    │  │  - Speech        │       │
│  │  - Segment   │  │  - LiDAR     │  │  - Sound         │       │
│  │  - Detect    │  │  - ToF       │  │  - Localization  │       │
│  └──────────────┘  └──────────────┘  └──────────────────┘       │
│                                                                  │
│              ┌──────────────────────────────┐                    │
│              │      Sensor Fusion           │                    │
│              │  (Kalman Filter, BEV)        │                    │
│              └──────────────────────────────┘                    │
│                          │                                       │
│              ┌───────────▼───────────┐                           │
│              │   Scene Understanding │                           │
│              └───────────────────────┘                           │
└─────────────────────────────────────────────────────────────────┘
```

## Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **GPU** | RTX 3060 (12GB) | RTX 4090 (24GB) |
| **Camera** | RGB-D (Realsense D435) | Stereo + ToF |
| **LiDAR** | 16-channel | 32+ channel |
| **Compute** | Jetson Orin Nano | Jetson Orin AGX |

## Vision Models

### Object Detection with YOLO

```python
#!/usr/bin/env python3
"""
YOLO Object Detection for Robotics
Processes camera images and publishes detections to ROS 2
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2D, Detection2DArray
from cv_bridge import CvBridge
import torch
import cv2
import numpy as np

class YOLODetectionNode(Node):
    def __init__(self):
        super().__init__('yolo_detection')
        
        # Load YOLO model
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
        self.model.conf = 0.5  # Confidence threshold
        
        self.bridge = CvBridge()
        
        # Subscriber
        self.camera_sub = self.create_subscription(
            Image, '/camera/color/image_raw',
            self.camera_callback, 10)
        
        # Publisher
        self.detections_pub = self.create_publisher(
            Detection2DArray, '/detections', 10)
        
        self.get_logger().info('YOLO Detection Node initialized')
    
    def camera_callback(self, msg: Image):
        """Process camera image and detect objects"""
        # Convert to OpenCV
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='rgb8')
        
        # Run YOLO inference
        results = self.model(cv_image)
        detections = results.pandas().xyxy[0]
        
        # Convert to ROS 2 messages
        detection_array = Detection2DArray()
        detection_array.header = msg.header
        detection_array.header.frame_id = 'camera_link'
        
        for _, detection in detections.iterrows():
            det_msg = Detection2D()
            det_msg.id = str(int(detection['class']))
            det_msg.results[0].hypothesis.class_id = detection['name']
            det_msg.results[0].hypothesis.score = float(detection['confidence'])
            
            # Bounding box
            det_msg.bbox.center.position.x = (detection['xmin'] + detection['xmax']) / 2
            det_msg.bbox.center.position.y = (detection['ymin'] + detection['ymax']) / 2
            det_msg.bbox.size_x = detection['xmax'] - detection['xmin']
            det_msg.bbox.size_y = detection['ymax'] - detection['ymin']
            
            detection_array.detections.append(det_msg)
        
        self.detections_pub.publish(detection_array)
        self.get_logger().debug(f'Detected {len(detections)} objects')

def main(args=None):
    rclpy.init(args=args)
    node = YOLODetectionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Semantic Segmentation

```python
#!/usr/bin/env python3
"""
Semantic Segmentation for Scene Understanding
Uses DeepLabV3+ for pixel-level classification
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import torch
from torchvision import transforms
import cv2
import numpy as np

class SegmentationNode(Node):
    def __init__(self):
        super().__init__('segmentation_node')
        
        # Load segmentation model
        self.model = torch.hub.load(
            'pytorch/vision:v0.10.0',
            'deeplabv3_resnet50',
            pretrained=True
        )
        self.model.eval()
        
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        
        self.bridge = CvBridge()
        
        # Subscriber
        self.camera_sub = self.create_subscription(
            Image, '/camera/color/image_raw',
            self.segmentation_callback, 10)
        
        # Publisher
        self.segmentation_pub = self.create_publisher(
            Image, '/segmentation/output', 10)
        
        # COCO class colors
        self.colors = np.random.randint(0, 255, size=(91, 3), dtype=np.uint8)
        
        self.get_logger().info('Segmentation Node initialized')
    
    def segmentation_callback(self, msg: Image):
        """Process image and generate segmentation mask"""
        # Convert to OpenCV
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='rgb8')
        
        # Preprocess
        input_tensor = self.transform(cv_image).unsqueeze(0)
        
        # Inference
        with torch.no_grad():
            output = self.model(input_tensor)['out'][0]
        
        # Get prediction
        output_predictions = output.argmax(0)
        mask = output_predictions.byte().cpu().numpy()
        
        # Colorize mask
        colored_mask = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
        for class_id in np.unique(mask):
            colored_mask[mask == class_id] = self.colors[class_id]
        
        # Publish
        seg_msg = self.bridge.cv2_to_imgmsg(colored_mask, encoding='bgr8')
        seg_msg.header = msg.header
        self.segmentation_pub.publish(seg_msg)

def main(args=None):
    rclpy.init(args=args)
    node = SegmentationNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Depth Perception

### Stereo Depth Processing

```python
#!/usr/bin/env python3
"""
Stereo Depth Processing
Computes depth from stereo camera pairs
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge
import cv2
import numpy as np

class StereoDepthNode(Node):
    def __init__(self):
        super().__init__('stereo_depth_node')
        
        self.bridge = CvBridge()
        
        # Subscribers
        self.left_sub = self.create_subscription(
            Image, '/stereo/left/image_raw',
            self.left_callback, 10)
        self.right_sub = self.create_subscription(
            Image, '/stereo/right/image_raw',
            self.right_callback, 10)
        
        # Publisher
        self.depth_pub = self.create_publisher(
            Image, '/depth/image_raw', 10)
        
        # Stereo matcher
        self.stereo = cv2.StereoSGBM_create(
            minDisparity=0,
            numDisparities=16*9,
            blockSize=5,
            P1=8*3*5**2,
            P2=32*3*5**2,
            disp12MaxDiff=1,
            uniquenessRatio=10,
            speckleWindowSize=100,
            speckleRange=32
        )
        
        self.left_image = None
        self.right_image = None
        
        self.get_logger().info('Stereo Depth Node initialized')
    
    def left_callback(self, msg: Image):
        self.left_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='mono8')
        self.try_compute_depth(msg.header)
    
    def right_callback(self, msg: Image):
        self.right_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='mono8')
        self.try_compute_depth(msg.header)
    
    def try_compute_depth(self, header):
        if self.left_image is not None and self.right_image is not None:
            # Compute disparity
            disparity = self.stereo.compute(self.left_image, self.right_image)
            
            # Convert to depth (simplified)
            baseline = 0.12  # meters
            focal_length = 718.856  # pixels
            with np.errstate(divide='ignore'):
                depth = (focal_length * baseline) / (disparity.astype(np.float32) / 16.0)
                depth[depth > 100] = 0  # Clip max depth
            
            # Normalize for visualization
            depth_vis = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX)
            depth_vis = np.uint8(depth_vis)
            depth_color = cv2.applyColorMap(depth_vis, cv2.COLORMAP_JET)
            
            # Publish
            depth_msg = self.bridge.cv2_to_imgmsg(depth_color, encoding='bgr8')
            depth_msg.header = header
            depth_msg.header.frame_id = 'camera_link'
            self.depth_pub.publish(depth_msg)
            
            self.left_image = None
            self.right_image = None

def main(args=None):
    rclpy.init(args=args)
    node = StereoDepthNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Sensor Fusion

### Multi-Modal Fusion

```python
#!/usr/bin/env python3
"""
Multi-Modal Sensor Fusion
Fuses camera, LiDAR, and IMU data for robust perception
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, PointCloud2, Imu
from nav_msgs.msg import Odometry
import numpy as np
from pykalman import KalmanFilter

class SensorFusionNode(Node):
    def __init__(self):
        super().__init__('sensor_fusion_node')
        
        # Subscribers
        self.camera_sub = self.create_subscription(
            Image, '/camera/color/image_raw',
            self.camera_callback, 10)
        self.lidar_sub = self.create_subscription(
            PointCloud2, '/lidar/points',
            self.lidar_callback, 10)
        self.imu_sub = self.create_subscription(
            Imu, '/imu/data',
            self.imu_callback, 10)
        
        # Publisher
        self.odom_pub = self.create_publisher(Odometry, '/fused_odom', 10)
        
        # Kalman Filter for state estimation
        self.kf = KalmanFilter(
            transition_matrices=np.eye(6),
            observation_matrices=np.eye(6),
            initial_state_mean=np.zeros(6),
            initial_state_covariance=np.eye(6) * 0.1,
            transition_covariance=np.eye(6) * 0.01,
            observation_covariance=np.eye(6) * 0.1
        )
        
        self.state = np.zeros(6)  # [x, y, z, vx, vy, vz]
        
        self.get_logger().info('Sensor Fusion Node initialized')
    
    def camera_callback(self, msg: Image):
        """Process visual odometry from camera"""
        # Visual odometry processing
        pass
    
    def lidar_callback(self, msg: PointCloud2):
        """Process LiDAR point cloud"""
        # LiDAR odometry processing
        pass
    
    def imu_callback(self, msg: Imu):
        """Process IMU data"""
        # Update state with IMU
        linear_accel = msg.linear_acceleration
        self.state[3] += linear_accel.x * 0.01  # Integrate acceleration
        self.state[4] += linear_accel.y * 0.01
        self.state[5] += linear_accel.z * 0.01
        
        # Publish fused odometry
        self.publish_odometry(msg.header)
    
    def publish_odometry(self, header):
        """Publish fused odometry"""
        odom_msg = Odometry()
        odom_msg.header = header
        odom_msg.child_frame_id = 'base_link'
        
        odom_msg.pose.pose.position.x = self.state[0]
        odom_msg.pose.pose.position.y = self.state[1]
        odom_msg.pose.pose.position.z = self.state[2]
        
        odom_msg.twist.twist.linear.x = self.state[3]
        odom_msg.twist.twist.linear.y = self.state[4]
        odom_msg.twist.twist.linear.z = self.state[5]
        
        self.odom_pub.publish(odom_msg)

def main(args=None):
    rclpy.init(args=args)
    node = SensorFusionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Isaac Sim Perception Integration

### Synthetic Data Generation

```python
# Isaac Sim synthetic data configuration
from omni.isaac.synthetic_utils import SyntheticDataHelper

# Configure perception sensors
perception_config = {
    'camera': {
        'resolution': (1920, 1080),
        'fov': 60,
        'frame_rate': 30
    },
    'lidar': {
        'channels': 64,
        'max_range': 100.0,
        'frame_rate': 10
    },
    'annotations': [
        'bounding_box_2d_tight',
        'bounding_box_3d',
        'segmentation',
        'depth',
        'normal'
    ]
}

# Generate synthetic dataset
sd_helper = SyntheticDataHelper()
sd_helper.generate_dataset(
    num_frames=10000,
    output_dir='/data/synthetic',
    config=perception_config
)
```

## Resources

### Documentation

- [Isaac ROS Perception](https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_image_pipeline/index.html)
- [PyTorch Vision](https://pytorch.org/vision/stable/index.html)
- [OpenCV Documentation](https://docs.opencv.org/)

### Models

- [YOLOv5](https://github.com/ultralytics/yolov5)
- [DeepLabV3](https://pytorch.org/hub/pytorch_vision_deeplabv3_resnet101/)
- [Segment Anything](https://github.com/facebookresearch/segment-anything)

## Exercises

1. **Object Detection**: Implement YOLO detection for robot environment
2. **Depth Processing**: Create stereo depth estimation pipeline
3. **Sensor Fusion**: Fuse camera and IMU data for state estimation
4. **Synthetic Data**: Generate synthetic training data in Isaac Sim

## Next Steps

Proceed to [Week 11 - Humanoid Robot Basics](../04-humanoid/week-11-humanoid-robot-basics.md) to begin humanoid development.
