# litearm

[English](README.md) | [简体中文](README.zh-CN.md)

URDF description package for the litearm SE arm, as a ROS 2 (ament_cmake)
package. Read this to build the model, view it in RViz2, or spawn it in
Gazebo.

It contains the 3D model (STL meshes), the URDF, an RViz2 configuration and
the launch files. You can open the arm in RViz2 and drag its joints from the
joint state GUI.

Kinematic chain: `base_link → joint1 → joint2 → … → joint7 → ee_link`.

The seven joints are revolute. The `ee_link` frame hangs off `joint7` on a
fixed joint. The whole arm weighs 2.7911 kg.

## Layout

```text
litearm/
├── package.xml                     # ament_cmake package manifest
├── CMakeLists.txt                  # build and install rules
├── urdf/
│   └── litearm.urdf                # the robot model
├── meshes/                         # 9 STL meshes (base_link, joint1..7, ee_link)
├── launch/
│   ├── display.launch.py           # RViz2 plus the joint state GUI
│   └── gazebo.launch.py            # spawn the model in an empty Gazebo world
├── rviz/
│   └── display.rviz                # RViz2 configuration (fixed frame base_link)
└── config/
    └── joint_names_litearm.yaml
```

## Where the model comes from

The URDF and the meshes are taken from the `litearm` package in the
`litearm-stm32` repository and are byte-identical to it. That is the current
model of this arm, the non-hollow revision. The URDF comes from
`litearm/urdf/litearm.urdf`; the meshes come from the non-hollow URDF package
shipped beside it. SolidWorks URDF Exporter produced the URDF.

Do not mix this model with the earlier `litearm_description` package the
repository used to publish under `SE/`. The two generations differ in link
naming (`Link*` versus `joint*`), joint zeroes, link lengths, masses and
inertias, and joint limits. They are not interchangeable.

## Requirements

- ROS 2 Humble
- `robot_state_publisher`, `joint_state_publisher_gui`, `rviz2`
- `gazebo_ros` as well, but only for `gazebo.launch.py`

Install the ROS 2 dependencies with:

```bash
sudo apt install ros-humble-robot-state-publisher \
                 ros-humble-joint-state-publisher-gui \
                 ros-humble-rviz2
```

## Build

Put this package in a colcon workspace. In this repository that workspace is
the `SE/` directory.

**Do not run the build with a conda `python3` on PATH.** If `python3` resolves
into a conda environment, it lacks `catkin_pkg` and colcon fails. Put the
system Python back first:

```bash
cd SE
source /opt/ros/humble/setup.bash

# Either deactivate conda:
conda deactivate
# Or drop miniconda from PATH:
export PATH=$(echo "$PATH" | tr ':' '\n' | grep -v miniconda | paste -sd:)

colcon build --packages-select litearm
```

## Run in RViz2

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash          # run this from the workspace root

ros2 launch litearm display.launch.py
```

This starts three nodes:

- **RViz2**, showing the arm with `base_link` as the fixed frame
- **joint_state_publisher_gui**, giving you a slider per joint
- **robot_state_publisher**

`display.launch.py` takes no arguments. The model path is fixed at
`urdf/litearm.urdf` inside this package. To load a different URDF, edit that
file and rebuild. **Do not expect a launch argument to override it** — there
is none.

## Run in Gazebo

```bash
ros2 launch litearm gazebo.launch.py
```

This starts an empty Gazebo world, publishes `robot_description`, and spawns
the model under the name `litearm`.

## Verify

```bash
# URDF syntax and kinematic tree
check_urdf install/litearm/share/litearm/urdf/litearm.urdf

# Running nodes; expect /robot_state_publisher, /joint_state_publisher_gui, /rviz2
ros2 node list

# Joint state rate, about 10 Hz by default
ros2 topic hz /joint_states

# One transform
ros2 run tf2_ros tf2_echo base_link joint1
```

## Note on the root link

`robot_state_publisher` may print this warning on startup. It does not affect
the RViz2 display and you can ignore it.

```text
[kdl_parser]: The root link base_link has an inertia specified in the URDF,
but KDL does not support a root link with an inertia.
```

SolidWorks URDF Exporter gives the root link an inertia. Only dynamics work
needs a workaround, and there it is an extra massless dummy link at the root.
