#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2017, UFactory, Inc.
# All rights reserved.
#
# Author: Duke Fong <duke@ufactory.cc>


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

# print('set X340 ...')
# swift.set_position(x=340)
# print('set X320 ...')
# swift.set_position(x=320)
# print('set X300 ...')
# swift.set_position(x=300)
print('set X200 ...')
swift.set_position(x=200)
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
    print('ultrasonic report value: {}'.format(value),'Z:',z)


swift.register_ultrasonic_callback(ultrasonic_report_cb)
swift.set_report_ultrasonic(100)  # microsecond
sleep(1)

print('\nultrasonic check value...')

print('set Z100 ...')
swift.set_position(z=0, wait=True)
print('distance: {}'.format(swift.get_ultrasonic()))
sleep(1)
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

# while True:
#     print('distance: {}'.format(swift.get_ultrasonic()))
#     sleep(1)

print('done ...')
try:
    while True:
        print('distance: {}'.format(swift.get_ultrasonic()))
        sleep(1)
except KeyboardInterrupt as e:
    print('KeyboardInterrupt', e)
finally:
    # print('ret5: ' + test_ports['swift_service']['handle'].call('set cmd_sync G0 X80 Y0 Z60'))
    swift.set_position(x=100, y=0, z=60, speed=1800, wait=True)
