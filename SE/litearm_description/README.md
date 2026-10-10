# litearm_description

litearm SE 版本的 机械臂的 URDF 描述功能包（ROS 2 / ament_cmake）。

包含机器人的 3D 模型（STL 网格）、URDF 描述文件、RViz 配置和启动文件，可在 RViz2 中可视化模型并通过 GUI 拖动关节。

运动链：`base_link → Link1 → Link2 → … → Link7 → ee_frame_link`

---

## 目录结构

```
litearm_description/
├── package.xml              # ROS 2 包描述（ament_cmake）
├── CMakeLists.txt           # 构建与安装规则
├── urdf/
│   └── litearm_description.urdf     # 机器人 URDF 模型
├── meshes/                  # 各连杆的 STL 网格
├── launch/
│   └── display.launch.py     # 启动 RViz + 关节控制 GUI
├── rviz/
│   └── urdf.rviz            # RViz2 显示配置
└── config/
    └── joint_names_litearm_description.yaml
```

---

## 环境要求

- ROS 2 Humble
- 依赖包：`robot_state_publisher`、`joint_state_publisher_gui`、`rviz2`、`xacro`

如缺少依赖，可安装：

```bash
sudo apt install ros-humble-robot-state-publisher \
                 ros-humble-joint-state-publisher-gui \
                 ros-humble-rviz2 \
                 ros-humble-xacro
```

---

## 构建

> ⚠️ **注意**：如果系统默认的 `python3` 指向 conda 环境（缺少 `catkin_pkg`），colcon 构建会失败。
> 构建前请先让系统 Python 生效（`conda deactivate`，或从 PATH 中排除 miniconda）。

将本包放入某个 colcon 工作空间（本仓库中即 `SE/` 目录），然后：

```bash
cd <工作空间>          # 例如 litearm-description/SE
source /opt/ros/humble/setup.bash

# 若默认 python3 是 conda，需先切回系统 python：
conda deactivate                                              # 方式一
# 或：export PATH=$(echo "$PATH" | tr ':' '\n' | grep -v miniconda | paste -sd:)   # 方式二

colcon build --packages-select litearm_description
```

---

## 运行（在 RViz 中打开）

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash          # 在工作空间根目录执行

ros2 launch litearm_description display.launch.py
```

启动后会打开：

- **RViz2** — 显示机械臂模型（Fixed Frame 为 `base_link`）
- **joint_state_publisher_gui** — 提供关节滑条，可实时拖动各关节观察运动

### 可选启动参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `model` | 包内 `urdf/litearm_description.urdf` | 指定要加载的 URDF 文件绝对路径 |
| `gui` | `true` | 是否启动关节控制 GUI |

示例：

```bash
ros2 launch litearm_description display.launch.py model:=/path/to/other.urdf
```

---

## 验证

```bash
# 检查 URDF 是否有效
check_urdf install/litearm_description/share/litearm_description/urdf/litearm_description.urdf

# 查看运行中的节点
ros2 node list        # 应包含 /robot_state_publisher /joint_state_publisher_gui /rviz2

# 查看关节状态发布频率（默认约 10Hz）
ros2 topic hz /joint_states

# 查看某个 TF 变换
ros2 run tf2_ros tf2_echo base_link Link1
```

---

## 说明

启动时 `robot_state_publisher` 可能输出如下警告，**不影响 RViz 显示**，可忽略：

```
[kdl_parser]: The root link base_link has an inertia specified in the URDF,
but KDL does not support a root link with an inertia.
```

该 URDF 由 SolidWorks URDF Exporter 导出，根连杆带有惯量属性。仅在做动力学计算时才需要在根部添加一个无质量的 dummy link 作为规避。
