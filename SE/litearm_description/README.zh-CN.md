# litearm_description

[English](README.md) | [简体中文](README.zh-CN.md)

litearm SE 型号机械臂的 URDF 描述功能包（ROS 2 / ament_cmake）。想构建模型、在 RViz2 里查看、或在 Gazebo 中生成该臂时看这份。

包含机器人的 3D 模型（STL 网格）、URDF、RViz2 配置和启动文件。可在 RViz2 中打开该臂，并通过关节状态 GUI 拖动各关节。

运动链：`base_link → joint1 → joint2 → … → joint7 → ee_link`。

7 个关节均为 revolute。`ee_link` 坐标系经一个 fixed joint 挂在 `joint7` 上。整臂质量 2.7911 kg。

## 目录结构

```text
litearm_description/
├── package.xml                     # ament_cmake 包描述
├── CMakeLists.txt                  # 构建与安装规则
├── urdf/
│   └── litearm_description.urdf    # 机器人模型
├── meshes/                         # 9 个 STL 网格（base_link、joint1..7、ee_link）
├── launch/
│   ├── display.launch.py           # RViz2 + 关节状态 GUI
│   └── gazebo.launch.py            # 在空 Gazebo 世界中生成模型
├── rviz/
│   └── display.rviz                # RViz2 配置（Fixed Frame = base_link）
└── config/
    └── joint_names_litearm_description.yaml
```

## 模型来源

本包的 URDF 与网格取自 `litearm-stm32` 仓库中的 `litearm` 包，**逐字节一致**。那是该臂的当前模型，即「非空版」。URDF 来自 `litearm/urdf/litearm.urdf`，网格来自与它同处的「非空版 URDF 包」。URDF 由 SolidWorks URDF Exporter 导出。

**不要**把这个模型与仓库此前在 `SE/` 下发布的 `litearm_description` 包混用。两代模型在连杆命名（`Link*` 对 `joint*`）、关节零位、连杆尺寸、质量与惯量、关节限位上都不同，不可互换。

## 关于第 6 关节的轴向

**`joint6` 的 axis 是 `0 0 -1`，而其余各关节都是 `0 0 1`。这是刻意为之，不是 URDF 写错了。** 在实机上，第 6 关节的电机是**定子与转子反向安装**的，因此该关节的转向与常规安装的电机相反。**URDF 正是为了与物理硬件保持一致才故意改成这样的。不要把正负号「改回来」** —— 恢复成 `0 0 1` 会让模型与实机不符，任何以本 URDF 为输入的控制器或规划器都会把第 6 关节朝反方向驱动。

## 环境要求

- ROS 2 Humble
- `robot_state_publisher`、`joint_state_publisher_gui`、`rviz2`
- 另需 `gazebo_ros`，但仅 `gazebo.launch.py` 用到

安装这些 ROS 2 依赖：

```bash
sudo apt install ros-humble-robot-state-publisher \
                 ros-humble-joint-state-publisher-gui \
                 ros-humble-rviz2
```

## 构建

把本包放进一个 colcon 工作空间。在本仓库中，该工作空间就是 `SE/` 目录。

**不要在 PATH 上有 conda 的 `python3` 时构建。** 如果 `python3` 指向 conda 环境，它缺少 `catkin_pkg`，colcon 会失败。先把系统 Python 换回来：

```bash
cd SE
source /opt/ros/humble/setup.bash

# 方式一：退出 conda
conda deactivate
# 方式二：从 PATH 中剔除 miniconda
export PATH=$(echo "$PATH" | tr ':' '\n' | grep -v miniconda | paste -sd:)

colcon build --packages-select litearm_description
```

## 在 RViz2 中运行

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash          # 在工作空间根目录执行

ros2 launch litearm_description display.launch.py
```

会启动三个节点：

- **RViz2**，以 `base_link` 为 Fixed Frame 显示该臂
- **joint_state_publisher_gui**，每个关节一根滑条
- **robot_state_publisher**

`display.launch.py` **不接受参数**。模型路径固定为本包内的 `urdf/litearm_description.urdf`。要换 URDF，直接改该文件后重新构建。**不要指望用 launch 参数覆盖它** —— 没有这个参数。

## 在 Gazebo 中运行

```bash
ros2 launch litearm_description gazebo.launch.py
```

会启动一个空的 Gazebo 世界、发布 `robot_description`，并以模型名 `litearm_description` 生成实体。

## 验证

```bash
# URDF 语法与运动学树
check_urdf install/litearm_description/share/litearm_description/urdf/litearm_description.urdf

# 运行中的节点；应包含 /robot_state_publisher、/joint_state_publisher_gui、/rviz2
ros2 node list

# 关节状态发布频率，默认约 10 Hz
ros2 topic hz /joint_states

# 单个变换
ros2 run tf2_ros tf2_echo base_link joint1
```

## 关于根连杆

`robot_state_publisher` 启动时可能打印下面这条警告。它不影响 RViz2 显示，可以忽略。

```text
[kdl_parser]: The root link base_link has an inertia specified in the URDF,
but KDL does not support a root link with an inertia.
```

SolidWorks URDF Exporter 会给根连杆带上惯量属性。只有做动力学计算时才需要规避，届时在根部加一个无质量的 dummy link。
