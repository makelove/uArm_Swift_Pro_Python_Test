# -*- coding: utf-8 -*-
# @Time    : 2017/8/26 22:57
# @Author  : play4fun
# @File    : 测试速度.py
# @Software: PyCharm

"""
测试速度.py:最高速度，还是1800
"""

from time import sleep
from uf.wrapper.swift_api import SwiftAPI
from uf.utils.log import *
from time import time

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

#
print('开始测试')
swift.set_buzzer()


def set_speed(speed=1800):
    print('速度：', speed)
    t1 = time()
    swift.set_position(x=152, y=0, z=10, speed=speed, wait=True)
    swift.set_position(x=152, y=130, z=118, speed=speed, wait=True)
    swift.set_position(x=152, y=-130, z=118, speed=speed, wait=True)
    t2 = time()

    swift.set_buzzer()
    print('finished,所需时间:',t2-t1,'秒')


set_speed()
# set_speed(2000)
# set_speed(2200)
# set_speed(2500)
set_speed(2800)
#
set_speed(10000)
set_speed(20000)
set_speed(30000)#的确快了很多,比默认速度快了4.2倍

#速度变化不是很明显
# for s in range(2000,30001,2000):#最高可设计30000
#     set_speed(s)

print('重置机械臂')
swift.set_buzzer()
swift.set_position(x=103, y=0, z=42, wait=True)
# swift.reset(x=103, y=0, z=42, speed=800)

sleep(5)

