import rospy
from nav_msgs.msg import Path 
import time


def main():
    rospy.init_node('store_path', anonymous=True)
    sub = rospy.Subscriber('/move_base/DWAPlannerROS/global_plan', Path, get_path)
    
    rospy.spin()
    return 


def get_path(message):
    poses = message.poses
    print('============================')
    for each_pose in poses:
        print(each_pose.pose.position.x)
    



if __name__ == '__main__':
    main()
