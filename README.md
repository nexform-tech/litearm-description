# litearm-description

[English](README.md) | [简体中文](README.zh-CN.md)

URDF descriptions for the litearm arm family. Use this repository to inspect
or simulate a litearm arm without going through the firmware or SDK
repositories.

Every litearm hardware version lives in its own subdirectory, and each one is
a buildable ROS 2 (ament_cmake) package you can open in RViz2.

## Repository layout

```text
litearm-description/
├── SE/                     # litearm SE
│   └── litearm_description/ # ROS 2 package: URDF, meshes, launch, rviz
├── S/                      # litearm S
├── SL/                     # litearm SL
├── P/                      # litearm P
└── PL/                     # litearm PL
```

Each model directory holds its own ROS 2 package in the same layout.

## Model matrix

| Model | Directory | Package | Status |
| --- | --- | --- | --- |
| SE | [`SE/`](SE/) | [`litearm_description`](SE/litearm_description/) | Available |
| S | [`S/`](S/) | — | Pending |
| SL | [`SL/`](SL/) | — | Pending |
| P | [`P/`](P/) | — | Pending |
| PL | [`PL/`](PL/) | — | Pending |

## Quick start

SE is the worked example. Other models follow the same steps with their own
directory and package name.

```bash
cd SE
source /opt/ros/humble/setup.bash
colcon build --packages-select litearm_description
source install/setup.bash
ros2 launch litearm_description display.launch.py
```

RViz2 opens showing the arm, and the joint state GUI gives you a slider per
joint.

Each package documents its own build and use. Start with
[SE/litearm_description/README.md](SE/litearm_description/README.md).

## Requirements

- ROS 2 Humble
- colcon
- `robot_state_publisher`, `joint_state_publisher_gui`, `rviz2`
