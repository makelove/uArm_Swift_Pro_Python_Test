# -*- coding: utf-8 -*-
# @Time    : 2017/11/22 23:16
# @Author  : play4fun
# @File    : aiy_press_button1.py
# @Software: PyCharm

"""
aiy_press_button1.py:
"""

import sys, os
from time import sleep

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from uf.wrapper.swift_api import SwiftAPI
from uf.utils.log import *

logger_init(logging.VERBOSE)
# logger_init(logging.DEBUG)
# logger_init(logging.INFO)

print('setup swift ...')

# swift = SwiftAPI(dev_port = '/dev/ttyACM0')
# swift = SwiftAPI(filters = {'hwid': 'USB VID:PID=2341:0042'})
swift = SwiftAPI()  # default by filters: {'hwid': 'USB VID:PID=2341:0042'}
print('sleep 2 sec ...')
sleep(2)

print('device info: ')
print(swift.get_device_info())

print('\nset X350 Y0 Z50 F500 ...')
swift.set_position(200, 0, 150, speed=1500,wait=True)

swift.set_buzzer()
sleep(2)

for i in range(1):#3
    swift.set_position(z=109, speed=1500,wait=True)
    swift.set_buzzer()
    sleep(1)
    swift.set_position(z=120, speed=1500, wait=True)
    sleep(2)

print('done ...')
swift.reset(z=200)
try:
    while True:
        sleep(1)
except KeyboardInterrupt as e:
    print('KeyboardInterrupt', e)
finally:
    # print('ret5: ' + test_ports['swift_service']['handle'].call('set cmd_sync G0 X80 Y0 Z60'))
    swift.set_position(x=80, y=0, z=60, speed=1800, wait=True)