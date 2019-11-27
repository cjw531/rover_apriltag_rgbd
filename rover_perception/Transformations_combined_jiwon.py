#!/usr/bin/env python
import geometry_msgs
import rospy

import tf
import turtlesim.msg
from geometry_msgs.msg._PoseStamped import PoseStamped
import math
import threading
import sys
import time
import os

home_dir = os.path.abspath(__file__).split('catkin_ws')[0]
sys.path.append(os.path.join(home_dir, 'catkin_ws/src'))

from rover_utils.constants import *

# Taken from Transformations.combined.py

tag_pose_castor = None
tag_pose_CRABBER = None
listener = None
tag_pose_CRABBER_intel = None

CASTOR_ORIGINAL_TAG = "/tag_8"
CRABBER_ORIGINAL_TAG = "/tag_0"

CASTOR_TAG    = "faster_tag_8"
CRABBER_TAG   = "faster_tag_0"
CRABBER_TAG_intel = "faster_tag_0_intel"
 

CASTOR_ROVER = "/bag/rover"
CRABBER_ROVER = "/stone/rover"

CASTOR_ROVER_ARM = "/bag/rover_arm"
CRABBER_ROVER_ARM = "/stone/rover_arm"

CASTOR_ROVER_REVERSE = "/bag/rover_reverse"
CASTOR_ONBOARD_CAMERA = "/bag/camera"

prev_tag = [0.0, 0.0, 0.0]
prev_pose = [0.0, 0.0, 0.0]

def getTransform(from_tf, to_tf, rate):

    global listener

    rate = rospy.Rate(rate)

    success = False
    trans = -1
    rot = -1
    while (not success):
        try:
            (trans, rot) = listener.lookupTransform(from_tf, to_tf, rospy.Time(0))
            success = True

        except (tf.LookupException):
            print "Error - Transformation from ", from_tf , " -> ", to_tf
            rospy.sleep(0.1)
            continue
        except (tf.ConnectivityException, tf.ExtrapolationException):
            # print "Extrapolation"
            continue

        rate.sleep()

    return (trans,rot)

# Tag 0
def get_castor_tf_thread():

    print "Started Castor Thread"
    global tag_pose_castor

    rate = 15
    ros_rate = rospy.Rate(rate)

    while not rospy.is_shutdown():

        trans, rot = getTransform(FRAME.CAMERA, CASTOR_ORIGINAL_TAG, rate)

        tag_pose_castor = (trans, rot)

        # print "Castor Tag TF: ", tag_pose_castor
        ros_rate.sleep()

# Tag 8
def get_crabber_tf_thread():

    print "Started Crabber Thread"
    global tag_pose_CRABBER

    rate = 15
    ros_rate = rospy.Rate(rate)

    while not rospy.is_shutdown():

        trans, rot = getTransform(FRAME.CAMERA, CRABBER_ORIGINAL_TAG, rate)

        tag_pose_CRABBER = (trans, rot)

        # print "CRABBER Tag TF: ", tag_pose_CRABBER
        ros_rate.sleep()

if __name__ == '__main__':
    global tag_pose_CRABBER_intel
    global tag_pose_CRABBER
    global prev_tag, prev_pose

    rospy.init_node('tf_broadcaster_combined')

    print ("starting...")
    
    listener = tf.TransformListener()
    time.sleep(1)

    t1 = threading.Thread(target=get_castor_tf_thread)
    t1.start()

    t2 = threading.Thread(target=get_crabber_tf_thread)
    t2.start()

    print "Get tf only once"

    rate = 15
    trans_intel, rot_intel = getTransform(FRAME.CAMERA, CRABBER_ORIGINAL_TAG, rate)
    tag_pose_CRABBER_intel = (trans_intel, rot_intel)

    rate = rospy.Rate(30)
    br = tf.TransformBroadcaster()

    while not rospy.is_shutdown():

        # Castor
        if(tag_pose_castor != None):

            # print "Castor Tag TF: ", tag_pose_castor


            br.sendTransform(tag_pose_castor[0],
                         tag_pose_castor[1],
                         rospy.Time.now(),
                         CASTOR_TAG,
                         FRAME.CAMERA)

            # TODO: Measure Z offset
            # br.sendTransform((0.16108, 0.002 , -0.041), # Before more finer measurement
            br.sendTransform((0.206, 0.011 , -0.115), #  For some moronic reason, we added ad delta to 18.6cm
                                tf.transformations.quaternion_from_euler( 0.0, 0.0, 0.0),
                                rospy.Time.now(),
                                CASTOR_ROVER_ARM,
                                CASTOR_TAG)

            # TODO: Measure Z Offset
            # br.sendTransform((-0.045, -0.002 , -0.144), # Adeded y = 9.6mm
            br.sendTransform((-0.045, -0.002 , -0.08), # Adeded y = 9.6mm
                        tf.transformations.quaternion_from_euler(0.0, 0.0, 0),
                        rospy.Time.now(),
                        CASTOR_ROVER,
                        CASTOR_ROVER_ARM)

            br.sendTransform((-0.05965, 0.000 , -0.05379), # Adeded y = 9.6mm
                        tf.transformations.quaternion_from_euler(math.radians(90), math.radians(0), math.radians(90)),
                        rospy.Time.now(),
                        CASTOR_ONBOARD_CAMERA,
                        CASTOR_TAG)
            
            br.sendTransform((0.009, -0.141, 0.221), # Adeded y = 9.6mm
                        tf.transformations.quaternion_from_euler(math.radians(-90), math.radians(-90), math.radians(0)),
                        rospy.Time.now(),
                        "/bag/rover_from_camera",
                        CASTOR_ONBOARD_CAMERA)


        # CRABBER
        if(tag_pose_CRABBER != None):

            # print "CRABBER Tag TF: ", tag_pose_CRABBER


            br.sendTransform(tag_pose_CRABBER[0],
                         tag_pose_CRABBER[1],
                         rospy.Time.now(),
                         CRABBER_TAG,
                         FRAME.CAMERA)


            br.sendTransform((0.185, 0.00 , -0.045), #  x =  rounded for 179.69mm from previous value of 0.19m
                             tf.transformations.quaternion_from_euler( 0.0, 0.0, 0.0),
                             rospy.Time.now(),
                             CRABBER_ROVER_ARM,
                             CRABBER_TAG)

            br.sendTransform((-0.038, 0.0 , -0.144), # Adeded y = 9.6mm
                     tf.transformations.quaternion_from_euler(0.0, 0.0, 0.0),
                     rospy.Time.now(),
                     CRABBER_ROVER,
                     CRABBER_ROVER_ARM)

         # CRABBER_intel
        if(tag_pose_CRABBER_intel != None):

            br.sendTransform(tag_pose_CRABBER_intel[0],
                         tag_pose_CRABBER_intel[1],
                         rospy.Time.now(),
                         CRABBER_TAG_intel,
                         FRAME.CAMERA)
            
            # from tag0 to intel
            br.sendTransform((-0.125674,0.0, 0.0),
                        tf.transformations.quaternion_from_euler(math.radians(0), math.radians(0), math.radians(180)),
                        rospy.Time.now(),
                        "/camera_odom_frame",
                        CRABBER_TAG_intel)

        # Listener for txt
        try:
            (trans_odom_to_tag, rot_odom_to_tag) = listener.lookupTransform('/camera_odom_frame', CRABBER_TAG, rospy.Time(0))
            (trans_odom_to_pose, rot_odom_to_pose) = listener.lookupTransform('/camera_odom_frame', "/camera_pose_frame", rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            print "Error - Transformation"
            rospy.sleep(0.1)
            continue
        
        trans_odom_to_tag = [trans_odom_to_tag[0] + 0.125674, trans_odom_to_tag[1], trans_odom_to_tag[2]]
        round_tag = [round(e, 1) for e in trans_odom_to_tag]
        if (prev_tag != round_tag):
            print "----------"
            print "Odom to TAG:"
            print(rospy.Time.now(), round_tag)
            prev_tag = round_tag

        round_pose = [round(e, 1) for e in trans_odom_to_pose]
        if (prev_pose != round_pose):
            print "++++++++++"
            print "Odom to Pose:"
            print(rospy.Time.now(), round_pose)
            prev_pose = round_pose
        

        rate.sleep()

    rospy.spin()
