# -*- coding: utf-8 -*-
# @Time    : 2017/8/8 10:41
# @Author  : play4fun
# @File    : 检测扑克牌是否被吸住.py
# @Software: PyCharm

"""
检测扑克牌是否被吸住.py:

指定坐标
z=0，气泵吸起扑克牌
z=50 机械臂升起
超声波检测到扑克牌的距离
气泵放气，扔掉扑克牌
超声波检测到扑克牌的距离
打印 '扑克牌被丢掉，重来'
"""

#TODO


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

print('sleep 2 sec ...')
sleep(2)

print('device info: ')
print(swift.get_device_info())

# print('\nset X350 Y0 Z50 F500 ...')
# swift.set_position(350, 0, 50, speed=1500)

print('set X200 ...')
swift.set_position(x=200,y=0)
print('set X190 ...')
swift.set_position(x=170)

# make sure at least one position was sent to device before start checking
sleep(0.1)
# make sure corresponding topics was empty before start service call
# data through different topics and services does not guarantee the order
while swift.get_is_moving():
    sleep(0.1)

# test ultrasonic:

print('ultrasonic auto report...')


def ultrasonic_report_cb(value):
    z=swift.get_position()[-1]
    print('ultrasonic report value: {}'.format(value),'\t','Z:',z)


swift.register_ultrasonic_callback(ultrasonic_report_cb)
swift.set_report_ultrasonic(400)  # microsecond
sleep(1)

print('\nultrasonic check value...')

print('set Z100 ...')
swift.set_position(z=0, wait=True)
print('distance: {}'.format(swift.get_ultrasonic()))
sleep(1)

#气泵
swift.set_pump(on=True)
print('吸起 扑克牌')

#超声波的距离将保持为1
swift.set_position(z=5, wait=True)
print('distance: {}'.format(swift.get_ultrasonic()))
sleep(1)
swift.set_position(z=10, wait=True)
print('distance: {}'.format(swift.get_ultrasonic()))
sleep(1)
swift.set_position(z=30, wait=True)
print('distance: {}'.format(swift.get_ultrasonic()))
sleep(1)
swift.set_position(z=50, wait=True)
print('distance: {}'.format(swift.get_ultrasonic()))
sleep(1)
#气泵
swift.set_pump(on=False)
print('放气 扑克牌')

swift.set_position(z=70, wait=True)
print('distance: {}'.format(swift.get_ultrasonic()))
sleep(1)
swift.set_position(z=100, wait=True)
print('distance: {}'.format(swift.get_ultrasonic()))
sleep(1)
swift.set_position(z=120, wait=True)
print('distance: {}'.format(swift.get_ultrasonic()))
sleep(1)
print('set Z150 ...')
swift.set_position(z=150, wait=True)
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
    swift.set_position(x=100, y=0, z=60, speed=1800, wait=True)

'''
ultrasonic check value...
set Z100 ...
distance: 3
ultrasonic report value: 0 	 Z: 0.0
ultrasonic report value: 1 	 Z: 0.0
ultrasonic report value: 1 	 Z: 0.0
DEBUG: swift/pump: set value: on
ultrasonic report value: 1 	 Z: 0.0
ultrasonic report value: 1 	 Z: 0.0
ultrasonic report value: 1 	 Z: 0.0
吸起 扑克牌
distance: 1
ultrasonic report value: 1 	 Z: 5.0
ultrasonic report value: 1 	 Z: 5.0
ultrasonic report value: 1 	 Z: 5.0
distance: 1
ultrasonic report value: 0 	 Z: 10.0
ultrasonic report value: 1 	 Z: 10.0
ultrasonic report value: 1 	 Z: 10.0
distance: 1
ultrasonic report value: 1 	 Z: 30.0
ultrasonic report value: 1 	 Z: 30.0
ultrasonic report value: 1 	 Z: 30.0
distance: 1
ultrasonic report value: 0 	 Z: 50.0
ultrasonic report value: 1 	 Z: 50.0
ultrasonic report value: 1 	 Z: 50.0
DEBUG: swift/pump: set value: off
放气 扑克牌
distance: 1
ultrasonic report value: 5 	 Z: 70.0
ultrasonic report value: 6 	 Z: 70.0
ultrasonic report value: 6 	 Z: 70.0
distance: 6
ultrasonic report value: 8 	 Z: 100.0
ultrasonic report value: 9 	 Z: 100.0
ultrasonic report value: 9 	 Z: 100.0
distance: 9
ultrasonic report value: 9 	 Z: 120.0
ultrasonic report value: 11 	 Z: 120.0
ultrasonic report value: 11 	 Z: 120.0
set Z150 ...
distance: 11
done ...
distance: 11
distance: 14
KeyboardInterrupt 
'''