# robot-vision
# 机器人视觉感知与自主导航系统

## 项目简介
基于 ROS2 Humble + Gazebo 的多传感器融合机器人视觉感知与导航系统，实现环境感知→地图构建→定位→路径规划→自主导航的完整闭环。

## 系统架构
- **仿真环境**: Gazebo Classic + 自定义世界
- **传感器**: 2D LiDAR + RGB-D 相机 + IMU
- **SLAM**: Cartographer (2D) / RTAB-Map (3D)
- **定位**: AMCL + EKF
- **导航**: Nav2 + DWB 局部规划器
- **手动干预**: twist_mux 键盘遥控

## 快速开始

### 安装依赖
```bash
sudo apt install ros-humble-nav2-bringup ros-humble-cartographer-ros \
  ros-humble-rtabmap-ros ros-humble-twist-mux

### 编译
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash

###启动仿真
ros2 launch robot_gazebo gazebo_sim.launch.py
ros2 launch robot_navigation nav2_simple.launch.py map:=~/ros2_ws/maps/my_map.yaml
