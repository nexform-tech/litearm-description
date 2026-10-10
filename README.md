# litearm-description

litearm 系列机械臂的 URDF 描述仓库。

本仓库集中存放 litearm **全系列** 机械臂的 URDF 模型、3D 网格、RViz 配置及 ROS 2 启动文件。每个硬件版本以独立子目录组织，均为可直接构建、可在 RViz2 中可视化的 ROS 2 (ament_cmake) 功能包。

---

## 目录结构

仓库按机械臂型号分目录，每个型号下是一个或多个 ROS 2 功能包：

```
litearm-description/
├── SE/                      # litearm SE 型号
│   └── litearm_description/        # ROS 2 功能包（URDF + 网格 + launch + rviz）
├── S/                       # litearm S 型号
├── SL/                      # litearm SL 型号
├── P/                       # litearm P 型号
└── PL/                      # litearm PL 型号
```

> 每个型号目录内均以相同结构组织各自的 ROS 2 功能包。

---

## 型号列表

| 型号 | 目录 | 功能包 | 状态 |
|------|------|--------|------|
| SE | [`SE/`](SE/) | [`litearm_description`](SE/litearm_description/) | ✅ 已收录 |
| S | [`S/`](S/) | — | 🚧 待补充 |
| SL | [`SL/`](SL/) | — | 🚧 待补充 |
| P | [`P/`](P/) | — | 🚧 待补充 |
| PL | [`PL/`](PL/) | — | 🚧 待补充 |

---

## 快速开始

以 SE 版本为例（其他系列步骤一致，替换对应目录/包名即可）：

```bash
cd SE
source /opt/ros/humble/setup.bash
colcon build --packages-select litearm_description
source install/setup.bash
ros2 launch litearm_description display.launch.py
```

启动后将打开 RViz2 显示机械臂模型，并可通过关节控制 GUI 实时拖动关节。

各功能包的详细构建与使用说明见对应目录下的 README，例如 [SE/litearm_description/README.md](SE/litearm_description/README.md)。

---

## 环境要求

- ROS 2 Humble
- colcon 构建工具
- 依赖：`robot_state_publisher`、`joint_state_publisher_gui`、`rviz2`、`xacro`
