# -*- coding: utf-8 -*-
# @Time    : 2017/7/24 上午12:05
# @Author  : play4fun
# @File    : 机械臂-旋转-扑克牌-角度.py
# @Software: PyCharm

"""
机械臂-旋转-扑克牌-角度.py:
"""
from time import sleep
from uf.wrapper.swift_api import SwiftAPI
from uf.wrapper.swift_api import SERVO_HAND
from uf.utils.log import *

# logger_init(logging.VERBOSE)
# logger_init(logging.DEBUG)
logger_init(logging.INFO)

print('setup swift ...')

swift = SwiftAPI()

sleep(2)

print('\nset X350 Y0 Z50 F500 ...')
swift.set_position(230, 0, 70, speed=1500,wait=True)

# 下降到桌面
swift.set_position(230, 0, z=1, speed=1500,wait=True)

# 气泵
swift.set_pump(on=True)
#升起
swift.set_position(230, 0, 70, speed=1500,wait=True)
#旋转90度
print('角度：',swift.get_servo_angle())#[90.0, 74.85, 39.1, 90.0]
print('旋转90度')
ret=swift.set_wrist(angle=90+30,wait=True)#默认是90度
# ret=swift.set_servo_angle(servo_id=SERVO_HAND,angle=90+20,wait=True)
# if ret is False:
print('角度：',swift.get_servo_angle(),ret)#[90.0, 75.03, 38.83, 93.0]

sleep(1)

# 气泵
swift.set_pump(on=False)

#复位
print('done ...')
try:
    while True:
        sleep(1)
except KeyboardInterrupt as e:
    print('KeyboardInterrupt', e)
finally:
    # print('ret5: ' + test_ports['swift_service']['handle'].call('set cmd_sync G0 X80 Y0 Z60'))
    swift.set_position(x=100, y=0, z=10, speed=1800, wait=True)