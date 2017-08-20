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

# logger_init(logging.VERBOSE)
# logger_init(logging.DEBUG)
logger_init(logging.INFO)

print('setup swift ...')

# swift = SwiftAPI(dev_port = '/dev/ttyACM0')
# swift = SwiftAPI(filters = {'hwid': 'USB VID:PID=2341:0042'})
swift = SwiftAPI()  # default by filters: {'hwid': 'USB VID:PID=2341:0042'}

print('sleep 2 sec ...')
sleep(2)

print('device info: ')
print(swift.get_device_info())

#
print('开始测试')
swift.set_buzzer()
swift.set_buzzer()

print('解锁电机')
swift.set_servo_detach()
sleep(10)
swift.set_buzzer()#TODO 哔哔2声
swift.set_buzzer()
sleep(2)

print('解锁电机')
swift.set_servo_attach()
sleep(3)

print('重置机械臂')
swift.set_buzzer()
swift.reset(x=103,
            y=0,
            z=42,
            speed=800)
