#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import time
import random
import numpy as np
from math import pi as PI

min_laser = 0
min_laser_index = 0
laser_range_th = 0.7
initial_time = time.time()
obstacle_detection_buffer = [-1, -1, -1]  #------------ -1: normal, 0: left turn, 1: right turn
obstacle_detection_buffer_index = 0
obstacle_detection_time_flag = 0

def millis():
	return (time.time() - initial_time) * 1000

def callback(data):
	laser_angular_range = 100
	laser = LaserScan()
	print type(data)
	middle_index = int((data.angle_max - data.angle_min)/data.angle_increment)/2
	angle_increment_degree = data.angle_increment * (180/PI)
	print 'middle_index ', middle_index
	print 'angle_increment_degree ', angle_increment_degree
	for i in range(int(laser_angular_range/angle_increment_degree)):
		laser.ranges.append(data.ranges[middle_index-int(laser_angular_range/angle_increment_degree/2)+i])
	
		#laser.intensities.append(data.intensities[middle_index-int(laser_angular_range/angle_increment_degree/2)+i])
	
	####################################################
	laser.header = data.header
	laser.header.frame_id = 'laser'
	laser.angle_min = -laser_angular_range/2 * (PI/180)

	laser.angle_max = laser_angular_range/2 * (PI/180)
	laser.angle_increment = data.angle_increment
	laser.time_increment = data.time_increment
	laser.scan_time = data.scan_time
	laser.range_min = data.range_min
	laser.range_max = data.range_max
	print laser.angle_increment
	print (laser.angle_max - laser.angle_min)/laser.angle_increment - len(laser.ranges) 
	#####################################################

	print time.time()
	laser_pub.publish(laser)


rospy.init_node('laser_listener', anonymous=True)
rospy.Subscriber("/scan", LaserScan, callback)

pub = rospy.Publisher('RosAria/cmd_vel', Twist, queue_size=10)
laser_pub = rospy.Publisher('scan3', LaserScan, queue_size=1000)
rate = rospy.Rate(40)

while not rospy.is_shutdown():
	# rospy.sleep(0.01)
	rospy.spin()
	


