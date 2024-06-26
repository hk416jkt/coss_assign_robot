import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, TextSubstitution, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('loop_rate', default_value='20'),
        DeclareLaunchArgument('wheel_radius', default_value='0.035'),
        DeclareLaunchArgument('wheel_base', default_value='0.220'),
        # Node(
        #     name='rplidar_composition',
        #     package='rplidar_ros',
        #     executable='rplidar_composition',
        #     output='screen',
        #     parameters=[{
        #         'serial_port': '/dev/mylidar',
        #         'serial_baudrate': 115200,  # A1 / A2
        #         # 'serial_baudrate': 256000, # A3
        #         'frame_id': 'laser',
        #         'inverted': False,
        #         'angle_compensate': True,
        #     }],
        # ),
         Node(
            package='ydlidar_ros2_driver',
            executable='ydlidar_ros2_driver_node',
            #name='ydlidar_node',
            name='ydlidar_ros2_driver_node',
            output='screen',
            parameters=[{
                'serial_port': '/dev/mylidar',
                'serial_baudrate': 128000,  # Baud rate might vary based on your ydlidar model
                'frame_id': 'base_scan',
                'inverted': False,
                'angle_compensate': True,
            }],
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_link_to_laser',
            # output='screen',
            arguments=['0.025', '0.0', '0.225', '0.0', '0.0', '0.0', '1.0', 'base_link', 'laser'],
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_link_to_base_footprint',
            # output='screen',
            arguments=['0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '1.0', 'base_link', 'base_footprint'],
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
            parameters=[{
                'linear_gain': 500.0,
                'angular_gain': 250.0,
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
        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource([
        #         PathJoinSubstitution([
        #             FindPackageShare('circle_node'),
        #             'launch',
        #             'include',
        #             'teleo_launch.py'
        #         ])
        #     ]),
        # )
    ])

