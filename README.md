# robot-vision
# 机器人视觉感知与自主导航系统

## 一、项目简介
基于 ROS2 Humble + Gazebo 的多传感器融合机器人视觉感知与导航系统，实现环境感知→地图构建→定位→路径规划→自主导航的完整闭环。

## 系统架构
- **仿真环境**: Gazebo Classic + 自定义世界
- **传感器**: 2D LiDAR + RGB-D 相机 + IMU
- **SLAM**: Cartographer (2D) / RTAB-Map (3D)
- **定位**: AMCL + EKF
- **导航**: Nav2 + DWB 局部规划器
- **手动干预**: twist_mux 键盘遥控

## 二、快速开始

### 安装依赖
bash
sudo apt install ros-humble-nav2-bringup ros-humble-cartographer-ros \
  ros-humble-rtabmap-ros ros-humble-twist-mux

### 编译
cd ~/ros2_ws
  colcon build --symlink-install
  source install/setup.bash

### 启动仿真
ros2 launch robot_gazebo gazebo_sim.launch.py
ros2 launch robot_navigation nav2_simple.launch.py map:=~/ros2_ws/maps/my_map.yaml

---

## 三、环境要求

- **OS**: Ubuntu 22.04 LTS
- **ROS2**: Humble Hawksbill
- **IDE**: VSCode
- **Gazebo**: Gazebo Classic 11.10.2

### 安装系统依赖

bash
sudo apt update
sudo apt install -y \
  ros-humble-desktop \
  ros-humble-gazebo-ros \
  ros-humble-cartographer-ros \
  ros-humble-slam-toolbox \
  ros-humble-nav2-bringup \
  ros-humble-nav2-simple-commander \
  ros-humble-rtabmap-ros \
  ros-humble-twist-mux \
  ros-humble-teleop-twist-keyboard \
  ros-humble-xacro \
  python3-colcon-common-extensions
## 四、项目构建


### 1. 编译
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release

### 2. 加载环境
source install/setup.bash
#### 建议添加到 ~/.bashrc
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
source ~/ros2_ws/install/setup.bash
ros2 launch robot_gazebo gazebo_sim.launch.py

## 五、快速开始
### 1、一键启动仿真环境（终端1）
source ~/ros2_ws/install/setup.bash
ros2 launch robot_gazebo gazebo_sim.launch.py
### 2、建图
source ~/ros2_ws/install/setup.bash
ros2 launch robot_gazebo gazebo_sim.launch.py
#### 终端 2：source ~/ros2_ws/install/setup.bash
ros2 launch robot_slam cartographer_2d.launch.py
#### 终端 3：（启用遥控）
ros2 run teleop_twist_keyboard teleop_twist_keyboard
