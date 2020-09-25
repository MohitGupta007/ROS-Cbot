cmake_minimum_required(VERSION 2.8.3)
project(cbot_mission)

## Compile as C++11, supported in ROS Kinetic and newer
add_compile_options(-std=c++11)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  message_generation
  roscpp
  cbot_ros_msgs
  genmsg
  actionlib_msgs
  actionlib
)

include_directories(include ${catkin_INCLUDE_DIRS} ${Boost_INCLUDE_DIRS})

catkin_package(
  CATKIN_DEPENDS roscpp cbot_ros_msgs
  INCLUDE_DIRS include
)