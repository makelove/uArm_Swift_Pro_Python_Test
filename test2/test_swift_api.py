#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2017, UFactory, Inc.
# All rights reserved.
#
# Author: Duke Fong <duke@ufactory.cc>


import sys, os
from time import sleep

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from uf.wrapper.swift_api import SwiftAPI
from uf.utils.log import *

# logger_init(logging.VERBOSE)
# logger_init(logging.DEBUG)
logger_init(logging.INFO)

print('setup swift ...')

# swift = SwiftAPI(dev_port = '/dev/ttyACM0')
# swift = SwiftAPI(filters = {'hwid': 'USB VID:PID=2341:0042'})
swift = SwiftAPI()  # default by filters: {'hwid': 'USB VID:PID=2341:0042'}


def report_position(data):
    print('data:', data)  # [x, y, z, r], r is wrist angle, ignore if not used


swift.register_report_position_callback(report_position)
swift.set_report_position(interval=0.5)  # 0.5 second (set 0 disable report)

print('sleep 2 sec ...')
sleep(2)

print('device info: ')
print(swift.get_device_info())

print('\nset X350 Y0 Z50 F500 ...')
swift.set_position(350, 0, 50, speed=1500)

print('set X340 ...')
swift.set_position(x=340)
print('set X320 ...')
swift.set_position(x=320)
print('set X300 ...')
swift.set_position(x=300)
print('set X200 ...')
swift.set_position(x=200)
print('set X190 ...')
swift.set_position(x=190)

# make sure at least one position was sent to device before start checking
sleep(0.1)
# make sure corresponding topics was empty before start service call
# data through different topics and services does not guarantee the order
while swift.get_is_moving():
    sleep(0.1)

print('set Z100 ...')
swift.set_position(z=100, wait=True)
print('set Z150 ...')
swift.set_position(z=150, wait=True)

swift.set_buzzer()

print('done ...')
try:
    while True:
        sleep(1)
except KeyboardInterrupt as e:
    print('KeyboardInterrupt', e)
finally:
    # print('ret5: ' + test_ports['swift_service']['handle'].call('set cmd_sync G0 X80 Y0 Z60'))
    swift.set_position(x=80, y=0, z=60, speed=1800, wait=True)
