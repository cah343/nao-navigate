#!/usr/bin/env python
import rospy
import geometry_msgs.msg
import tf
from std_msgs.msg import Header
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import Quaternion
from tf import TransformBroadcaster

#publishes odom to baselink tf messages for ROS nav stack
#Alex Hirst, 11/7/17

#define position/orientation class
class vicon_to_odo():

    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.quat = Quaternion()
        self.header = Header()


    def pose_callback(self,data):

        #if there is no detection, do nothing
        if not data.header:
            self.x = 0.0
            self.y = 0.0
            self.quat = Quaternion()
        else:

            self.x = data.transform.translation.x
            self.y = data.transform.translation.y
            self.quat = data.transform.rotation

            self.header = data.header

#define velocity class
class vel_to_odo():

    def __init__(self):

        self.twstmsg = Twist()

    def pose_callback(self,data):

        self.twstmsg = data


def main():

    #Create Vicon data object, call nav_data
    nav_data = vicon_to_odo()
    #Create velocity data object, call vel_data
    vel_data = vel_to_odo()

    #Start New Node Subscriber Node
    rospy.init_node('vicon_to_odo', anonymous=True)
    #Subscribe to vicon data
    rospy.Subscriber("/vicon/maecy_alex/maecy_alex", TransformStamped , nav_data.pose_callback)
    #subscribe to velocity data
    rospy.Subscriber("/cmd_vel", Twist, vel_data.pose_callback)

    #Define odometry Publisher
    odom_pub = rospy.Publisher('/nav_msgs', Odometry, queue_size = 10)
    odom = Odometry()

    #define transform boradcaster
    odom_broadcaster = TransformBroadcaster()


    #Set rate of update
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():


        #First, publish the transform from base_link to odom
        odom_trans = TransformStamped()
        odom_trans = nav_data

        odom_trans.header.frame_id = "nav_odometry"
        odom_trans.child_frame_id = "nav_base_link"

        x = nav_data.x
        y = nav_data.y
        quat_1 = nav_data.quat.x
        quat_2 = nav_data.quat.y
        quat_3 = nav_data.quat.z
        quat_4 = nav_data.quat.w

        #Send the transform, note that the base_link and odometry frames had to be
        #renamed in order to avoid conflict with frames that nao publishes
        odom_broadcaster.sendTransform((x,y,0), (quat_1,quat_2,quat_3,quat_4), rospy.Time.now(), "nav_base_link","nav_odometry" )



        #next, publish the odometry Message, odom is already defined, see above in pub section
        odom.header = nav_data.header
        odom.header.frame_id = "nav_odometry"

        #set position
        odom.pose.pose.position.x = nav_data.x
        odom.pose.pose.position.y = nav_data.y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation = nav_data.quat

        #set velocities
        odom.child_frame_id = "nav_base_link"
        odom.twist.twist = vel_data.twstmsg

        #publish the odom Message
        odom_pub.publish(odom)


        rate.sleep()



if __name__ == '__main__':
    try:
        #testing our function
        main()
    except rospy.ROSInterruptException:
        pass
