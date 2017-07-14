# -*- coding: utf-8 -*-
# @Time    : 2017/7/8 下午12:46
# @Author  : play4fun
# @File    : test_api2.py
# @Software: PyCharm

"""
test_api2.py:
"""

from time import sleep

from uf.wrapper.swift_api import SwiftAPI
from uf.utils.log import *

logger_init(logging.INFO)

print('setup swift ...')

swift = SwiftAPI(dev_port='/dev/cu.usbmodem1421')

print('sleep 2 sec ...')
sleep(2)

print('device info: ')
print(swift.get_device_info())

# swift.set_position(x=120,z=80,y=30)


print('\nset X350 Y0 Z50 F500 ...')
# swift.set_position(350, 0, 50, speed=1500)

swift.set_position(x=300)
# sleep(3)
swift.set_position(y=190)

print('finished')
try:
    while True:
        sleep(1)
except KeyboardInterrupt as e:
    print('KeyboardInterrupt',e)