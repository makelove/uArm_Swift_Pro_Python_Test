# -*- coding: utf-8 -*-
# @Time    : 2017/8/20 21:22
# @Author  : play4fun
# @File    : 解锁电机.py
# @Software: PyCharm

"""
解锁电机.py:
"""
from time import sleep
from uf.wrapper.swift_api import SwiftAPI
from uf.utils.log import *

#logger_init(logging.VERBOSE)
#logger_init(logging.DEBUG)
logger_init(logging.INFO)

print('setup swift ...')

#swift = SwiftAPI(dev_port = '/dev/ttyACM0')
#swift = SwiftAPI(filters = {'hwid': 'USB VID:PID=2341:0042'})
swift = SwiftAPI() # default by filters: {'hwid': 'USB VID:PID=2341:0042'}


print('sleep 2 sec ...')
sleep(2)

print('device info: ')
print(swift.get_device_info())