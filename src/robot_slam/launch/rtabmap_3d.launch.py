from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
    rtabmap_node = Node(
        package='rtabmap_slam',
        executable='rtabmap',
        name='rtabmap',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'frame_id': 'base_link',
            'odom_frame_id': 'odom',
            'subscribe_depth': True,
            'subscribe_scan': True,
            'approx_sync': True,
            'RGBD/NeighborLinkRefining': 'true',
            'RGBD/ProximityBySpace': 'true',
            'RGBD/AngularUpdate': '0.01',
            'RGBD/LinearUpdate': '0.01',
            'Optimizer/Slam2D': 'true',
            'Reg/Strategy': '1',
            'Icp/CorrespondenceRatio': '0.3',
            'Vis/MinInliers': '10',
            'PointCloud/DepthFiltering': 'true',
            'PointCloud/DepthFilteringRadius': '0.5',
            'PointCloud/DepthFilteringNeighbors': '5',
        }],
        remappings=[
            ('rgb/image', '/camera/color/image_raw'),
            ('rgb/camera_info', '/camera/color/camera_info'),
            ('depth/image', '/camera/depth/image_rect_raw'),
            ('scan', '/scan'),
            ('odom', '/odom'),
        ],
    )
    
    rtabmap_viz = Node(
        package='rtabmap_viz',
        executable='rtabmap_viz',
        parameters=[{'use_sim_time': use_sim_time}],
        remappings=[
            ('rgb/image', '/camera/color/image_raw'),
            ('rgb/camera_info', '/camera/color/camera_info'),
            ('depth/image', '/camera/depth/image_rect_raw'),
            ('scan', '/scan'),
            ('odom', '/odom'),
        ],
    )
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'),
        rtabmap_node,
        rtabmap_viz,
    ])