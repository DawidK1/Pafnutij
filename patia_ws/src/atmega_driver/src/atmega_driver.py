#!/usr/bin/python

from smbus import SMBus
import rospy
import numpy
from time import sleep
from geometry_msgs.msg import Twist

DEV_ADDR = 0x44
LEFT_WHEEL_ADDR = 1
RIGHT_WHEEL_ADDR = 2
CASTER_WHEEL_ADDR = 3

MAX_TRANS_SPEED = 0.56
WHEEL_WIDTH = 0.145


bus = SMBus(1)

last_update = 0


def saturate(a):
    if a > 1:
        return 1
    elif a < -1:
        return -1
    return a


def set_wheels(left, right, caster):
    l_dir = 1
    r_dir = 1
    if left < 0:
        l_dir = 0
    if right < 0:
        r_dir = 0

    caster = saturate(caster)
    left = saturate(left)
    right = saturate(right)
    try:
        bus.write_byte_data(DEV_ADDR, LEFT_WHEEL_ADDR,
                            abs(int(left*16)*2) + l_dir)
        bus.write_byte_data(DEV_ADDR, RIGHT_WHEEL_ADDR,
                            abs(int(right*16)*2) + r_dir)
        bus.write_byte_data(DEV_ADDR, CASTER_WHEEL_ADDR,
                            int((-caster + 1.0)*115))

    except Exception as e:
        print(e)


def cmd_vel_callback(data):
    global last_update
    # data = Twist()
    last_update = rospy.get_time()
    vel_left = (data.linear.x - numpy.sin(data.angular.z) /
                (2*WHEEL_WIDTH))/MAX_TRANS_SPEED
    vel_right = (data.linear.x + numpy.sin(data.angular.z) /
                 (2*WHEEL_WIDTH))/MAX_TRANS_SPEED

    sum_of_wheels = abs(vel_left) + abs(vel_right)
    if sum_of_wheels > 0:
        caster_pos = (vel_left - vel_right)/sum_of_wheels
    else:
        caster_pos = 0
    set_wheels(vel_left, vel_right, caster_pos)


rospy.init_node("atmega_driver")

rospy.Subscriber("cmd_vel", Twist, cmd_vel_callback)
rate = rospy.Rate(3)
while not rospy.is_shutdown():
    if rospy.get_time() - last_update:
        set_wheels(0, 0, 0)
    rate.sleep()
# set_wheels(1, -1, -1)
# sleep(3)
# sleep(1)
# set_wheels(0, 0, 0)
