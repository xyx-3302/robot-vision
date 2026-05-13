from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
    # 修复：使用绝对路径，避免参数传递问题
    map_yaml_file = LaunchConfiguration(
        'map',
        default='/home/xyx/ros2_ws/maps/my_map.yaml')
    
    params_file = PathJoinSubstitution([
        FindPackageShare('robot_navigation'),
        'config',
        'nav2_params.yaml',
    ])
    bt_xml_file = PathJoinSubstitution([
        FindPackageShare('robot_navigation'),
        'behavior_trees',
        'navigate_to_pose_w_replanning_and_recovery.xml',
    ])

    # 修复：使用 nav2_bringup 的 bringup_launch.py，确保 map 参数传入
    nav2_bringup = PathJoinSubstitution([
        FindPackageShare('nav2_bringup'),
        'launch',
        'bringup_launch.py',
    ])
    
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(nav2_bringup),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'map': map_yaml_file,
            'params_file': params_file,
            'autostart': 'True',
            'default_bt_xml_filename': bt_xml_file,
        }.items(),
    )

    twist_mux = Node(
        package='twist_mux',
        executable='twist_mux',
        name='twist_mux',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'topics.joystick.topic': 'cmd_vel_joy',
            'topics.joystick.timeout': 0.5,
            'topics.joystick.priority': 100,
            'topics.navigation.topic': 'cmd_vel_nav',
            'topics.navigation.timeout': 0.5,
            'topics.navigation.priority': 50,
            'cmd_vel_out': 'cmd_vel',
        }],
        remappings=[('cmd_vel_out', '/cmd_vel')],
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'),
        DeclareLaunchArgument(
            'map',
            default_value=map_yaml_file,
            description='Full path to map YAML file to load'),
        nav2_launch,
        twist_mux,
    ])
