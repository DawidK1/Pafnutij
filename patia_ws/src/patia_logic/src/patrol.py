#!/usr/bin/python
import rospy
import numpy as np

from geometry_msgs.msg import PoseStamped
from time import sleep
import random

def prep_pos(x,y,th):
    pos = PoseStamped()
    pos.header.frame_id = 'map'
    pos.pose.position.x = x
    pos.pose.position.y = y
    pos.pose.orientation.z = np.sin(th/2)
    pos.pose.orientation.w = np.cos(th/2)
    return pos


next_to_door = prep_pos(4.57, -0.63,-0.13)

next_to_tables = prep_pos(2.7,-0.22, 2.33)

under_bed = prep_pos(1.04,4.2, -1.606)
next_to_pc = prep_pos(1.99, -1.02, 3.11)

next_to_warderobe = prep_pos(2.33, 4.24, 1.104)

poses = [next_to_door, next_to_tables, under_bed, next_to_pc, next_to_warderobe]

goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=5)

rospy.init_node("random_patrol")
rate = rospy.Rate(1/120.0)
while not rospy.is_shutdown():
    next_goal = random.choice(poses)
    rospy.loginfo("Next goal!")
    next_goal.header.stamp = rospy.get_rostime()
    print(next_goal)
    goal_pub.publish(next_goal)
    rate.sleep()