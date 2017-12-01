# nao-navigate
##Fall 2017 Project - ASL Cornell 
###By: Alex Hirst 

**Purpose:** 
The package is designed to autonomously navigate a Nao humanoid robot through a given mapped workspace. AprilTags are detected using Nao’s camera on its forehead, and will alert the user if an obstacle label with an AprilTag is detected. The package is written in Python and ROS. 

**Software Requirements:** 

- ROS Indigo

- Nao Driver package (see http://wiki.ros.org/nao_bringup for how to connect nao to ROS)

- AprilTag Package (see: http://wiki.ros.org/apriltags_ros )

- vicon_bridge Package (see: http://wiki.ros.org/vicon_bridge )

- Choregraphe (see: https://www.ald.softbankrobotics.com/en/robots/tools )


**Startup Instructions:** 

1. Turn on Nao Robot, launch using the command: “$ roslaunch nao_bringup nao_full_py.launch nao_ip:=<my_nao_ip> roscore_ip:=<my_comp_ip>  ”

2. If desired, turn off Nao's awareness using Choregraphe. This stops the head from moving around.

3. Turn on Vicon System. Connect to vicon, turn on AprilTag monitoring, start navigation stack, and start RVIZ using the command: “$ roslaunch nao_2dnav nao_nav.launch ”

4. Run the alex_nao_navigate script of your choice. (v3 or v4)

5. Tell Nao a goal using RVIZ (set 2D goal).


**Troubleshooting Tips**

P: Nao doesn't resume walking after obstacle is moved/signaled to do so.

A: Ensure that the alex_nao_navigate script is running *before* you enter the 2d goal. Script records goal, and republishes it. Thus it needs the goal initially to record for future use. 

