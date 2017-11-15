# nao-navigate
Fall 2017 Project - ASL Cornell 
By: Alex Hirst 

Purpose: 
The package is designed to autonomously navigate a Nao humanoid robot through a given mapped workspace. AprilTags are detected using Nao’s camera on its forehead, and will alert the user if an obstacle label with an AprilTag is detected. The package is written in Python and ROS. 

Software Requirements: 
ROS Indigo
Nao Driver package (see http://wiki.ros.org/nao_bringup for how to connect nao to ROS)
AprilTag Package (see: http://wiki.ros.org/apriltags_ros )
vicon_bridge Package (see: http://wiki.ros.org/vicon_bridge )
Choregraphe (see: https://www.ald.softbankrobotics.com/en/robots/tools )

Startup Instructions: 
Turn on Nao Robot, launch using the command: “$ roslaunch nao_bringup nao_full_py.launch nao_ip:=<my_nao_ip> roscore_ip:=<my_comp_ip>  ”
Turn on Vicon System. Connect to vicon, turn on AprilTag monitoring, start navigation stack, and start RVIZ using the command: “$ roslaunch nao_2dnav nao_nav.launch ”
Run the alex_nao_navigate script of your choice. (v3 or v4)
