# -*- coding: utf-8 -*-
# @Time    : 2017/12/14 23:33
# @Author  : play4fun
# @File    : t1.py
# @Software: PyCharm

"""
t1.py:
"""
from time import sleep
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
sleep(2)
# swift.reset()
swift.set_position(x=200, wait=True)
sleep(3)
print(swift.get_position())
sleep(3)
swift.set_position(y=0, wait=True)
sleep(3)

# swift.set_position(x=200,y=0, z=45, wait=True)
swift.set_position(z=45, wait=True)
sleep(2)
for x in range(0, 180):
    swift.set_wrist(angle=x, wait=True)
    sleep(0.2)
swift.set_buzzer()
sleep(2)
swift.set_position(x=200, y=0, z=50, wait=True)

#
swift.set_position(x=230, y=0, z=45, wait=True)
sleep(2)
for x in range(0, 180):
    swift.set_wrist(angle=x, wait=True)
    sleep(0.2)
swift.set_buzzer()
sleep(2)

swift.reset()
while True:
    sleep(1)
