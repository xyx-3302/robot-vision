from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    map_yaml_file = LaunchConfiguration('map', default='/home/xyx/ros2_ws/maps/my_map.yaml')
    params_file = PathJoinSubstitution([
        FindPackageShare('robot_navigation'),
        'config',
        'nav2_params.yaml',
    ])

    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'yaml_filename': map_yaml_file,
        }],
    )

    amcl = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[params_file, {'use_sim_time': use_sim_time}],
    )

    planner_server = Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[params_file, {'use_sim_time': use_sim_time}],
    )

    controller_server = Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        output='screen',
        parameters=[params_file, {'use_sim_time': use_sim_time}],
    )

    bt_navigator = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[params_file, {'use_sim_time': use_sim_time}],
    )

    # 添加 lifecycle manager 自动激活所有节点
    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_navigation',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'autostart': True,
            'node_names': ['map_server', 'amcl', 'planner_server', 'controller_server', 'bt_navigator'],
        }],
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
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('map', default_value=map_yaml_file),
        map_server,
        amcl,
        planner_server,
        controller_server,
        bt_navigator,
        lifecycle_manager,
        twist_mux,
    ])
