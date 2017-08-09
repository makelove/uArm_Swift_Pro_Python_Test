# -*- coding: utf-8 -*-
# @Time    : 2017/8/9 09:12
# @Author  : play4fun
# @File    : 检测障碍物-停止运动.py
# @Software: PyCharm

"""
检测障碍物-停止运动.py:
"""

import sys, os
from time import sleep

from uf.wrapper.swift_with_ultrasonic import SwiftWithUltrasonic
from uf.utils.log import *

# logger_init(logging.VERBOSE)
logger_init(logging.DEBUG)
# logger_init(logging.INFO)
# logger_init(logging.ERROR)

print('setup swift ...')

# swift = SwiftAPI(dev_port = '/dev/ttyACM0')
# swift = SwiftAPI(filters = {'hwid': 'USB VID:PID=2341:0042'})
swift = SwiftWithUltrasonic()  # default by filters: {'hwid': 'USB VID:PID=2341:0042'}

uArm_move = True


def set_position(x=None, y=None, z=None, wait=False,speed=1800):#不行。TODO 离障碍物越来越近
    gx, gy, gz = swift.get_position()
    print(gx, gy, gz)
    x = x if x is not None else gx
    y = y if y is not None else gy
    z = z if z is not None else gz

    while True:
        distence = swift.get_ultrasonic()
        print('distence',distence)
        if distence > 0:
            ret = swift.set_position(x=x, y=y, z=z, wait=wait,speed=speed)
            if ret:
                break
        else:
            print('有障碍物，停止运动')
            sleep(0.5)


print('sleep 2 sec ...')
sleep(2)

print('device info: ')
print(swift.get_device_info())

print('set X200 ...')
swift.set_position(x=200, y=0)
print('set X190 ...')
swift.set_position(x=170,z=70)

# make sure at least one position was sent to device before start checking
sleep(0.1)
# make sure corresponding topics was empty before start service call
# data through different topics and services does not guarantee the order
while swift.get_is_moving():
    sleep(0.1)

# test ultrasonic:

print('ultrasonic auto report...')


def ultrasonic_report_cb(value):
    z = swift.get_position()[-1]
    print('ultrasonic report value: {}'.format(value), '\t', 'Z:', z)


swift.register_ultrasonic_callback(ultrasonic_report_cb)
swift.set_report_ultrasonic(400)  # microsecond
sleep(1)

print('\nultrasonic check value...')

print('set Z100 ...')
set_position(z=0, wait=True)
print('distance: {}'.format(swift.get_ultrasonic()))
sleep(1)

# 气泵
swift.set_pump(on=True)
print('吸起 扑克牌')

# 超声波的距离将保持为1
set_position(z=5, wait=True)
print('distance: {}'.format(swift.get_ultrasonic()))
sleep(1)
set_position(z=10, wait=True)
print('distance: {}'.format(swift.get_ultrasonic()))
sleep(1)
set_position(z=30, wait=True)
print('distance: {}'.format(swift.get_ultrasonic()))
sleep(1)
set_position(z=50, wait=True)
print('distance: {}'.format(swift.get_ultrasonic()))
sleep(1)
# 气泵
swift.set_pump(on=False)
print('放气 扑克牌')

set_position(z=70, wait=True)
print('distance: {}'.format(swift.get_ultrasonic()))
sleep(1)
set_position(z=100, wait=True)
print('distance: {}'.format(swift.get_ultrasonic()))
sleep(1)
set_position(z=120, wait=True)
print('distance: {}'.format(swift.get_ultrasonic()))
sleep(1)
print('set Z150 ...')
set_position(z=150, wait=True)
print('distance: {}'.format(swift.get_ultrasonic()))

swift.set_buzzer()

swift.register_ultrasonic_callback(None)

print('done ...')
try:
    while True:
        print('distance: {}'.format(swift.get_ultrasonic()))
        sleep(1)
except KeyboardInterrupt as e:
    print('KeyboardInterrupt', e)
finally:
    set_position(x=100, y=0, z=60, speed=1800, wait=True)
