---
id: prerequisites
title: Hardware Prerequisites
sidebar_label: Hardware Requirements
sidebar_position: 0
description: Complete hardware requirements for Physical AI & Humanoid Robotics development
---

# Hardware Prerequisites

This document outlines the hardware requirements for developing and deploying Physical AI and Humanoid Robotics systems. Specifications are categorized by use case and budget level.

## Development Workstation

### RTX Workstation Specifications

| Component | Minimum | Recommended | High-End |
|-----------|---------|-------------|----------|
| **GPU** | NVIDIA RTX 3060 (12GB) | NVIDIA RTX 3080 Ti (12GB) | NVIDIA RTX 4090 (24GB) |
| **CPU** | Intel i5-12600K / AMD Ryzen 5 5600X | Intel i7-13700K / AMD Ryzen 7 7700X | Intel i9-13900K / AMD Ryzen 9 7950X |
| **RAM** | 32 GB DDR4 | 64 GB DDR5 | 128 GB DDR5 |
| **Storage** | 500 GB NVMe SSD | 1 TB NVMe SSD | 2 TB NVMe SSD + 4 TB HDD |
| **PSU** | 650W 80+ Gold | 850W 80+ Gold | 1200W 80+ Platinum |
| **Network** | Gigabit Ethernet | Gigabit Ethernet + WiFi 6 | 10GbE + WiFi 6E |

### GPU Requirements by Module

| Module | Minimum GPU | Recommended GPU | VRAM Required |
|--------|-------------|-----------------|---------------|
| ROS 2 | Integrated / GTX 1650 | RTX 3060 | 4 GB |
| Digital Twin | RTX 3060 | RTX 3080 | 8 GB |
| NVIDIA Isaac | RTX 3060 (12GB) | RTX 4090 (24GB) | 12 GB |
| VLA Training | RTX 3090 (24GB) | A100 (40-80GB) | 24 GB |

### NVIDIA GPU Compatibility

```
Supported GPU Architectures:
├── Ampere (RTX 30xx, A100)
│   ├── Full support for all modules
│   └── Recommended for Isaac Sim
├── Ada Lovelace (RTX 40xx)
│   ├── Best performance for Isaac Sim
│   └── DLSS 3.0 support
├── Hopper (H100)
│   ├── Datacenter training
│   └── VLA model training
└── Jetson Orin (Edge)
    ├── Edge deployment
    └── Real-time inference
```

## Jetson Edge Deployment Kit

### Jetson Orin Series Comparison

| Specification | Orin Nano | Orin NX | AGX Orin |
|---------------|-----------|---------|----------|
| **GPU** | Ampere (1024 CUDA) | Ampere (1024 CUDA) | Ampere (2048 CUDA) |
| **Tensor Cores** | 32 | 32 | 64 |
| **CPU** | 6-core ARM Cortex-A78AE | 6-core ARM Cortex-A78AE | 12-core ARM Cortex-A78AE |
| **Memory** | 4-8 GB LPDDR5 | 8-16 GB LPDDR5 | 32-64 GB LPDDR5 |
| **Storage** | microSD / NVMe | microSD / NVMe | NVMe / eMMC |
| **Power** | 7-15W | 10-25W | 15-60W |
| **AI Performance** | 20-40 TOPS | 70-100 TOPS | 100-275 TOPS |
| **Price** | ~$199 | ~$399 | ~$1999 |

### Recommended Jetson Kit

```
Jetson Edge Development Kit:
├── Jetson Orin NX 16GB (Recommended for most applications)
├── Carrier Board with:
│   ├── 2x Gigabit Ethernet
│   ├── 4x USB 3.2
│   ├── 2x CSI Camera interfaces
│   ├── GPIO / I2C / SPI / UART
│   └── M.2 Key M for NVMe SSD
├── Power Supply: 19V/65W
├── Cooling: Active heatsink with fan
└── Enclosure: IP65 rated for robotics
```

### Peripheral Requirements

| Peripheral | Specification | Purpose |
|------------|---------------|---------|
| **Camera** | Intel RealSense D435i / OAK-D | Depth perception, VLA input |
| **LiDAR** | Ouster OS0-16 / Velodyne VLP-16 | Navigation, mapping |
| **IMU** | Xsens MTi-300 / Bosch BMI088 | State estimation, balance |
| **Motor Controller** | ODrive v3.6 / T-Motor AK Series | Joint actuation |
| **Battery** | 6S LiPo 22000mAh / LiFePO4 25.6V | Power system |

## Robot Hardware Specifications

### Humanoid Robot Platform

| Component | Specification | Notes |
|-----------|---------------|-------|
| **DOF** | 20-40 degrees of freedom | Full humanoid |
| **Height** | 1.2 - 1.8 meters | Human-scale |
| **Weight** | 30 - 80 kg | Depends on payload |
| **Payload** | 5 - 20 kg | End-effector capacity |
| **Actuators** | Brushless DC with harmonic drives | High torque density |
| **Sensors** | Force-torque, IMU, encoders | Proprioception |

### Sensor Suite

```
Recommended Sensor Configuration:
├── Vision
│   ├── RGB-D Camera (head): Intel RealSense D455
│   ├── Stereo Cameras (eyes): OV9281 global shutter
│   └── Event Camera (optional): Prophesee Gen4
├── Proprioception
│   ├── IMU: Xsens MTi-670 (head)
│   ├── Joint Encoders: Absolute magnetic (all joints)
│   └── Force-Torque: ATI Mini40 (ankles, wrists)
├── Exteroception
│   ├── LiDAR: Ouster OS0-16 (torso)
│   ├── Ultrasonic: HC-SR04 (collision avoidance)
│   └── Tactile: GelSight / tactile fingers
└── Audio
    ├── Microphone Array: ReSpeaker 4-mic
    └── Speaker: 3W mono
```

## Development Environment Setup

### Software Prerequisites

```bash
# Operating System
Ubuntu 22.04 LTS (Jammy Jellyfish)

# ROS 2 Distribution
ROS 2 Humble Hawksbill

# Python Version
Python 3.10+

# CUDA Version
CUDA 11.8 / 12.1 (for Isaac Sim and VLA training)

# Docker
NVIDIA Container Toolkit (for Isaac Sim containers)
```

### Environment Variables

```bash
# ~/.bashrc configuration

# ROS 2
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=0

# Isaac Sim
export ISAACSIM_PATH="${HOME}/.local/share/ov/pkg/isaac-sim"
export LD_LIBRARY_PATH="${ISAACSIM_PATH}/exts/isaac-sim:${LD_LIBRARY_PATH}"

# CUDA
export CUDA_HOME=/usr/local/cuda
export LD_LIBRARY_PATH="${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}"
export PATH="${CUDA_HOME}/bin:${PATH}"

# Jetson (if applicable)
export JETSON_STATS=/home/nvidia/jetson-stats
```

## Network Requirements

### Multi-Robot Communication

| Requirement | Specification | Notes |
|-------------|---------------|-------|
| **Latency** | < 10 ms | Real-time control |
| **Bandwidth** | > 100 Mbps | Camera streams |
| **Jitter** | < 1 ms | Deterministic control |
| **Protocol** | UDP/TCP with QoS | ROS 2 DDS |

### Recommended Network Setup

```
Network Architecture:
├── Management Network (1 GbE)
│   ├── SSH access
│   ├── File transfer
│   └── Monitoring
├── Real-time Network (10 GbE or TSN)
│   ├── Robot control
│   ├── Sensor data
│   └── Low-latency communication
└── WiFi 6E (optional)
    ├── Mobile robot communication
    └── Remote monitoring
```

## Budget Estimates

### Development Setup Costs

| Tier | Workstation | Jetson Kit | Sensors | Total |
|------|-------------|------------|---------|-------|
| **Entry** | $1,500 | $400 | $500 | $2,400 |
| **Professional** | $3,500 | $800 | $2,000 | $6,300 |
| **Research** | $8,000 | $2,500 | $10,000 | $20,500 |

### Cloud Alternatives

For teams without local GPU resources:

| Provider | Instance | Hourly Rate | Use Case |
|----------|----------|-------------|----------|
| AWS | g5.2xlarge (A10G) | ~$1.00/hr | VLA training |
| GCP | a2-highgpu-1g (A100) | ~$3.00/hr | Large-scale training |
| Lambda Labs | 1x RTX 4090 | ~$0.50/hr | Isaac Sim, training |
| RunPod | 1x RTX 3090 | ~$0.40/hr | Cost-effective training |

## Troubleshooting

### Common Hardware Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| GPU Memory | OOM errors in Isaac Sim | Reduce scene complexity, use smaller textures |
| Thermal | Throttling during training | Improve cooling, reduce ambient temperature |
| Network | High latency in ROS 2 | Use wired connection, check QoS settings |
| Jetson Power | Unexpected shutdowns | Use adequate power supply, check current limits |

## Resources

- [NVIDIA GPU Support Matrix](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html)
- [Jetson Developer Guide](https://docs.nvidia.com/jetson/archives/r35.4.1/DeveloperGuide/index.html)
- [ROS 2 Hardware Guide](https://docs.ros.org/en/humble/The-ROS2-Project/Contributing/Hardware.html)

## Next Steps

After verifying your hardware setup, proceed to:

1. **Module 1**: ROS 2 Fundamentals
2. **Module 2**: Digital Twin Simulation
3. **Module 3**: NVIDIA Isaac Platform
4. **Module 4**: Vision-Language-Action Models
