#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import ComputePathToPose, FollowPath

class SimpleNavigator(Node):
    def __init__(self):
        super().__init__('simple_navigator')
        self.goal_sub = self.create_subscription(PoseStamped, '/goal_pose', self.goal_callback, 10)
        self.compute_path_client = ActionClient(self, ComputePathToPose, 'compute_path_to_pose')
        self.follow_path_client = ActionClient(self, FollowPath, 'follow_path')
        self.get_logger().info('Simple navigator started. Publish to /goal_pose to navigate.')
        self.current_goal = None
    
    def goal_callback(self, msg):
        self.get_logger().info(f'Goal received: ({msg.pose.position.x:.2f}, {msg.pose.position.y:.2f})')
        self.current_goal = msg
        self.send_planning_request()
    
    def send_planning_request(self):
        if not self.compute_path_client.wait_for_server(timeout_sec=3.0):
            self.get_logger().error('Planner server not available!')
            return
        
        goal = ComputePathToPose.Goal()
        goal.goal = self.current_goal
        goal.planner_id = 'GridBased'
        
        self.get_logger().info('Sending path planning request...')
        future = self.compute_path_client.send_goal_async(goal)
        future.add_done_callback(self.planning_response_callback)
    
    def planning_response_callback(self, future):
        try:
            goal_handle = future.result()
        except Exception as e:
            self.get_logger().error(f'Failed to get goal handle: {e}')
            return
            
        if not goal_handle or not goal_handle.accepted:
            self.get_logger().error('Path planning rejected!')
            return
        
        self.get_logger().info('Path planning accepted, waiting for result...')
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.planning_result_callback)
    
    def planning_result_callback(self, future):
        try:
            result = future.result()
        except Exception as e:
            self.get_logger().error(f'No result received from planner: {e}')
            return
            
        path_result = result.result
        
        if not path_result or not path_result.path.poses:
            self.get_logger().error('No path found!')
            return
        
        self.get_logger().info(f'Path found: {len(path_result.path.poses)} waypoints')
        self.send_follow_path(path_result.path)
    
    def send_follow_path(self, path):
        if not self.follow_path_client.wait_for_server(timeout_sec=3.0):
            self.get_logger().error('Controller server not available!')
            return
        
        follow_goal = FollowPath.Goal()
        follow_goal.path = path
        follow_goal.controller_id = 'FollowPath'
        
        self.get_logger().info('Sending follow path request...')
        future = self.follow_path_client.send_goal_async(follow_goal)
        future.add_done_callback(self.follow_response_callback)
    
    def follow_response_callback(self, future):
        try:
            follow_handle = future.result()
        except Exception as e:
            self.get_logger().error(f'Failed to get follow path handle: {e}')
            return
            
        if follow_handle and follow_handle.accepted:
            self.get_logger().info('Robot is moving to goal!')
        else:
            self.get_logger().error('Controller rejected path!')

def main():
    rclpy.init()
    node = SimpleNavigator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
