#!/usr/bin/env python
# ip cam to ROS example

import cv2
import urllib 
import numpy as np
import sys
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


#---------------------- this is the part to tranform ipcam image to ROS image msgs-------------------#########
class image_converter:
    def __init__(self):
            self.image_pub = rospy.Publisher("camera/image_raw", Image, queue_size=10)
            self.bridge = CvBridge()

    def converter(self, cv_image):
        try:
            ros_image = self.bridge.cv2_to_imgmsg(cv_image,  encoding="bgr8")
        except CvBridgeError as e:
            print(e)
            pass
        try:
            ros_image.header.frame_id = 'ip_cam'
            ros_image.header.seq += 1
            ros_image.header.stamp = rospy.Time.now()
            self.image_pub.publish(ros_image)
        except CvBridgeError as e:
            print(e)
            pass
#------------------------------------------------------------------------------------------------------------------------#

if __name__ == '__main__':

    ip = "192.168.0." + raw_input('type in your ipcam ip: 192.168.0.')
    port = raw_input('port: ')
    
    try:
        # stream = urllib.urlopen('http://192.168.10.123:7060/axis-cgi/mjpg/video.cgi?resolution=640x480')
        # stream=urllib.urlopen('http://admin:admin@' + ip + '/MJPEG.CGI')
        # stream=urllib.urlopen('http://admin:admin@192.168.0.194/MJPEG.CGI')
        # stream = urllib.urlopen('http://192.168.0.194:3333/MJPEG.CGI')
        print ip + ':' + port + '/MJPEG.CGI'
        stream = urllib.urlopen('http://' + ip + ':' + port + '/MJPEG.CGI')
        print 'Connect to the ip cam successfully!'

    except:
        print 'Can not connect to the ip cam'

    bytes=''   #---------------------------------- This is used to read image bytes from ipcam

    rospy.init_node('image_converter', anonymous=True)
    ic = image_converter()
    r = rospy.Rate(30)
    while not rospy.is_shutdown():
        bytes+=stream.read(1024)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a!=-1 and b!=-1:
            jpg = bytes[a:b+2]
            bytes= bytes[b+2:]

            i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),1)
            ic.converter(i)
            r.sleep()
        
