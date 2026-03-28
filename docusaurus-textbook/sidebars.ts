import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    // Introduction
    'introduction-to-physical-ai',

    // Prerequisites
    'prerequisites',

    // Weeks 1–2: Foundation
    {
      type: 'category',
      label: 'Weeks 1–2: Introduction to Physical AI',
      link: {
        type: 'generated-index',
        title: 'Weeks 1–2: Introduction to Physical AI',
        description: 'Foundations of Physical AI, embodied intelligence, sensor systems, and course architecture overview.',
      },
      items: [
        'foundation/week-01-introduction-to-physical-ai',
        'foundation/week-02-physical-ai-architecture',
      ],
    },

    // Weeks 3–5: ROS 2 Fundamentals
    {
      type: 'category',
      label: 'Weeks 3–5: ROS 2 Fundamentals',
      link: {
        type: 'generated-index',
        title: 'Weeks 3–5: ROS 2 Fundamentals',
        description: 'ROS 2 architecture, nodes, topics, services, actions, and building Python packages for humanoid control.',
      },
      items: [
        'ros-2/week-03-introduction-to-ros-2',
        'ros-2/week-04-ros-2-nodes-and-topics',
        'ros-2/week-05-ros-2-services-and-actions',
      ],
    },

    // Weeks 6–7: Robot Simulation (Gazebo)
    {
      type: 'category',
      label: 'Weeks 6–7: Robot Simulation (Gazebo)',
      link: {
        type: 'generated-index',
        title: 'Weeks 6–7: Robot Simulation with Gazebo',
        description: 'Physics simulation, URDF/SDF robot models, sensor simulation, and Unity visualization.',
      },
      items: [
        'gazebo/week-06-introduction-to-gazebo',
        'gazebo/week-07-robot-modeling-in-gazebo',
      ],
    },

    // Weeks 8–10: NVIDIA Isaac Platform
    {
      type: 'category',
      label: 'Weeks 8–10: NVIDIA Isaac Platform',
      link: {
        type: 'generated-index',
        title: 'Weeks 8–10: NVIDIA Isaac Platform',
        description: 'Isaac Sim, Isaac ROS, GPU-accelerated perception, reinforcement learning, and sim-to-real transfer.',
      },
      items: [
        'nvidia-isaac/week-08-introduction-to-isaac-sim',
        'nvidia-isaac/week-09-isaac-ros-integration',
        'nvidia-isaac/week-10-perception-models',
      ],
    },

    // Weeks 11–13: Humanoid Development & Conversational AI
    {
      type: 'category',
      label: 'Weeks 11–13: Humanoid & Conversational AI',
      link: {
        type: 'generated-index',
        title: 'Weeks 11–13: Humanoid Development & Conversational AI',
        description: 'Humanoid kinematics, locomotion, GPT integration, voice commands, and capstone project.',
      },
      items: [
        'humanoid/week-11-humanoid-robot-basics',
        'humanoid/week-12-conversational-ai-integration',
        'humanoid/week-13-complete-humanoid-system',
      ],
    },
  ],
};

export default sidebars;
