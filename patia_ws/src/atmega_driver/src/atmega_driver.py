#!/usr/bin/python

from smbus import SMBus
import rospy
import numpy
from time import sleep

DEV_ADDR = 0x44
LEFT_WHEEL_ADDR = 1
RIGHT_WHEEL_ADDR = 2
CASTER_WHEEL_ADDR = 3

bus = SMBus(1)


def set_wheels(left, right, caster):
    l_dir = 0
    r_dir = 0
    if left < 0:
        l_dir = 1
    if right < 0:
        r_dir = 1

    bus.write_byte_data(DEV_ADDR, LEFT_WHEEL_ADDR, abs(int(left*16)*2) + l_dir)
    bus.write_byte_data(DEV_ADDR, RIGHT_WHEEL_ADDR,
                        abs(int(right*16)*2) + r_dir)
    bus.write_byte_data(DEV_ADDR, CASTER_WHEEL_ADDR, int((-caster + 1)*128))


for i in numpy.linspace(-1, 1, 60):
    set_wheels(i, i, i)
    sleep(1.0)
set_wheels(0, 0, 0)
