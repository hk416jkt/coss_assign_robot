import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, TextSubstitution, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    share_dir = get_package_share_directory('ydlidar_ros2_driver')
    rviz_config_file = os.path.join(share_dir, 'config','ydlidar.rviz')
    parameter_file_y = LaunchConfiguration('params_file_y')
    
    return LaunchDescription([
        DeclareLaunchArgument('loop_rate', default_value='20'),
        DeclareLaunchArgument('wheel_radius', default_value='0.035'),
        DeclareLaunchArgument('wheel_base', default_value='0.220'),
        DeclareLaunchArgument('params_file_y', default_value=os.path.join(
                                             share_dir, 'params', 'ydlidar.yaml'),
                                            description='FPath to the ROS2 parameters file to use.'),

        Node(
            package='ydlidar_ros2_driver',
            executable='ydlidar_ros2_driver_node',
            name='ydlidar_ros2_driver_node',
            output='screen',
            parameters=[parameter_file_y]
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_link_to_laser',
            arguments=['--x', '0.025', '--z', '0.225', '--frame-id', 'base_link', '--child-frame-id', 'laser_frame'],
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_link_to_base_footprint',
            arguments=['--frame-id', 'base_link', '--child-frame-id', 'base_footprint'],
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('circle_node'),
                    'launch',
                    'include',
                    'serial_driver.launch.py'
                ])
            ]),
        ),
        Node(
            package='circle_node',
            name='jara_controller',
            executable='jara_controller',
            output='screen',
            parameters=[{
                'wheel_radius': LaunchConfiguration('wheel_radius'),
                'wheel_base': LaunchConfiguration('wheel_base'),
                'loop_rate': LaunchConfiguration('loop_rate'),
            }],
        ),
        Node(
            package='circle_node',
            name='jara_driver',
            executable='jara_driver',
            parameters=[{
                'loop_rate': LaunchConfiguration('loop_rate'),
            }],
        ),
        Node(
            package='circle_node',
            name='jara_odometry',
            executable='jara_odometry',
            parameters=[{
                'loop_rate': LaunchConfiguration('loop_rate'),
                'wheel_radius': LaunchConfiguration('wheel_radius'),
                'wheel_base': LaunchConfiguration('wheel_base'),
                'encoder_resolution': 1200,
            }],
        ),
    ])
