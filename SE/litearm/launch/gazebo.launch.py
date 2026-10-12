import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg = get_package_share_directory('litearm')
    urdf_path = os.path.join(pkg, 'urdf', 'litearm.urdf')

    with open(urdf_path, 'r') as f:
        robot_description = f.read()

    gazebo_launch = os.path.join(
        get_package_share_directory('gazebo_ros'),
        'launch', 'empty_world.launch.py'
    )

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gazebo_launch)
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description}],
        ),
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            name='spawn_entity',
            arguments=['-file', urdf_path, '-urdf', '-model', 'litearm'],
            output='screen',
        ),
    ])
