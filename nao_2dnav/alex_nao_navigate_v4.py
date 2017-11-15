#!/usr/bin/env python
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseGoal
from move_base_msgs.msg import MoveBaseAction
#from actionlib/client import simple_action_client
from apriltags_ros.msg import AprilTagDetectionArray
from actionlib_msgs.msg import GoalID
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Quaternion
from std_msgs.msg import Header
from geometry_msgs.msg import TransformStamped

#Final Project script, will navigate Nao robot towards a goal, while stopping
#if an april tag is detected. Person has to signal that the coast is clear by
#showing nao a number 5 AprilTag

#Written by: Alex Hirst, 11/6/17
#Undergraduate Researcher, ASL, Cornell University


#define AprilTagPos class - used for apriltag detections
class AprilTagsPos():

    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 5
        self.id = 0.0


    def pose_callback(self,data):

        #print(type(data.detections[0]))
        #print(data.detections[0])

        #if there is no detection of AprilTags, do nothing
        if not data.detections:
            self.x = 0
            self.y = 0
            self.z = 5
            self.id = 0.0
        else:

            self.x = data.detections[0].pose.pose.position.x
            self.y = data.detections[0].pose.pose.position.y
            self.z = data.detections[0].pose.pose.position.z
            self.id = data.detections[0].id

class nao_position():

    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.quat = Quaternion()

        self.header = Header()


    def pose_callback(self,data):


        self.x = data.transform.translation.x
        self.y = data.transform.translation.y
        self.z = 0
        self.quat = data.transform.rotation

        self.header = data.header

class nao_goal_cls():

    def __init__(self):
        self.x = 100
        self.y = 100

        self.goal = PoseStamped()


    def pose_callback(self,data):


        #if there is no detection, do nothing
        print(data)
        self.x = data.pose.position.x
        self.y = data.pose.position.y

        self.goal = data


def main():

    #Definte z-distance at which tags are reacted to
    tag_ztol = 1.0

    #Create apriltagdetection object
    tag_pos = AprilTagsPos()
    #create a Nao position object
    nao_pos = nao_position()
    #create a goal objec to store goal in
    nao_goal = nao_goal_cls()

    #Start new subscriber node for AprilTags
    rospy.init_node('nao_navigate', anonymous=True)
    rospy.Subscriber("/tag_detections",AprilTagDetectionArray,tag_pos.pose_callback)
    rospy.Subscriber("/vicon/maecy_alex/maecy_alex", TransformStamped , nao_pos.pose_callback)
    rospy.Subscriber("move_base_simple/goal", PoseStamped , nao_goal.pose_callback)

    #Start goal and cancel publishers
    cancel_pub = rospy.Publisher('/move_base/cancel', GoalID, queue_size = 10)
    goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size = 10)
    cancel = GoalID()
    rospy.loginfo("ready")

    xdiff =  abs(nao_goal.y-nao_pos.y)
    ydiff =  abs(nao_goal.x-nao_pos.x)



    while ( (.15 < xdiff) and (.15 < ydiff) ):
        #rospy.loginfo("Start Loop")
        if ((tag_pos.z <= tag_ztol) and (tag_pos.id != 5.0)):
            rospy.loginfo("I see an obstacle")
            #Stop robot by publishing and empty GoalID object to /move_base/cancel
            cancel_pub.publish(cancel)
            rospy.sleep(2)
            while (tag_pos.id != 5.0):
                rospy.loginfo("Help, the obstacle is blocking me!")
                rospy.sleep(2)
            goal_pub.publish(nao_goal.goal)
            rospy.loginfo("The obstacle moved, I'll keep going now")

    rospy.loginfo("done")

if __name__ == '__main__':
    try:
        #testing our function
        main()
    except rospy.ROSInterruptException:
        pass
