import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterValue


def generate_launch_description():
    pkg_share = get_package_share_directory('litearm_description')

    default_model_path = os.path.join(pkg_share, 'urdf', 'litearm_description.urdf')
    default_rviz_path = os.path.join(pkg_share, 'rviz', 'urdf.rviz')

    model_arg = DeclareLaunchArgument(
        name='model',
        default_value=default_model_path,
        description='URDF 文件的绝对路径',
    )
    gui_arg = DeclareLaunchArgument(
        name='gui',
        default_value='true',
        description='是否启动 joint_state_publisher_gui',
    )

    # 使用 xacro 处理 URDF（普通 urdf 也可正常通过）
    robot_description = {
        'robot_description': ParameterValue(
            Command(['xacro ', LaunchConfiguration('model')]),
            value_type=str,
        )
    }

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description],
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', default_rviz_path],
    )

    return LaunchDescription([
        model_arg,
        gui_arg,
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node,
    ])
