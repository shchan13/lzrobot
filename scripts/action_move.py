#!/usr/bin/env python
import roslib; roslib.load_manifest('mybot_navigation')
import rospy
import actionlib
from std_msgs.msg import String

#move_base_msgs
from move_base_msgs.msg import *

def simple_move(data):

    #Simple Action Client
    sac = actionlib.SimpleActionClient('move_base', MoveBaseAction )

    #create goal
    goal = MoveBaseGoal()

    if data == 'point left':
        #set goal
        goal.target_pose.pose.position.x = 1.0
        goal.target_pose.pose.orientation.w = 1.0
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()

    #start listner
    sac.wait_for_server()

    #send goal
    sac.send_goal(goal)

    #finish
    sac.wait_for_result()

    #print result
    print sac.get_result()


if __name__ == '__main__':
    rospy.loginfo('initialization+')
    rospy.init_node('action_move', anonymous=True)
    rospy.Subscriber('/TfAction/action', String, simple_move, queue_size=1)
    rospy.spin()
