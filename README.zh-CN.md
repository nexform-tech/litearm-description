# litearm-description

[English](README.md) | [简体中文](README.zh-CN.md)

litearm 系列机械臂的 URDF 描述仓库。想查看或仿真某一型号的 litearm 机械臂时，用这个仓库，不必翻固件仓或 SDK 仓。

每个硬件版本各占一个子目录，且都是一个可直接构建、可在 RViz2 中打开的 ROS 2 (ament_cmake) 功能包。

## 仓库结构

```text
litearm-description/
├── SE/                     # litearm SE
│   └── litearm_description/ # ROS 2 功能包：URDF、网格、launch、rviz
├── S/                      # litearm S
├── SL/                     # litearm SL
├── P/                      # litearm P
└── PL/                     # litearm PL
```

每个型号目录内均以相同结构组织各自的 ROS 2 功能包。

## 型号列表

| 型号 | 目录 | 功能包 | 状态 |
| --- | --- | --- | --- |
| SE | [`SE/`](SE/) | [`litearm_description`](SE/litearm_description/) | 已收录 |
| S | [`S/`](S/) | — | 待补充 |
| SL | [`SL/`](SL/) | — | 待补充 |
| P | [`P/`](P/) | — | 待补充 |
| PL | [`PL/`](PL/) | — | 待补充 |

## 快速开始

下面以 SE 为例。其他型号步骤相同，换成各自的目录与包名即可。

```bash
cd SE
source /opt/ros/humble/setup.bash
colcon build --packages-select litearm_description
source install/setup.bash
ros2 launch litearm_description display.launch.py
```

RViz2 会打开并显示该臂，关节状态 GUI 提供每个关节一根滑条。

各功能包各自记录自己的构建与使用方式，先看 [SE/litearm_description/README.zh-CN.md](SE/litearm_description/README.zh-CN.md)。

## 环境要求

- ROS 2 Humble
- colcon
- `robot_state_publisher`、`joint_state_publisher_gui`、`rviz2`
