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
# swift.set_position(230, 0, 70, speed=1500,wait=True)
swift.set_position(230, 0, 2, speed=1500,wait=True)#原地旋转
#旋转90度
print('角度：',swift.get_servo_angle())#[90.09, 74.76, 39.27, 93.0]
print('旋转90度')
ret=swift.set_wrist(angle=90-90,wait=True)#默认是90度
print('角度：',swift.get_servo_angle(),ret)#[90.09, 74.94, 39.01, 104.0]
sleep(1)
ret=swift.set_wrist(angle=90-60,wait=True)#
print('角度：',swift.get_servo_angle(),ret)#[90.09, 75.03, 38.92, 15.0]
sleep(1)
ret=swift.set_wrist(angle=90-30,wait=True)#
print('角度：',swift.get_servo_angle(),ret)#[90.09, 75.03, 38.92, 52.0]
sleep(1)
ret=swift.set_wrist(angle=90+0,wait=True)#
print('角度：',swift.get_servo_angle(),ret)#[90.09, 75.03, 38.92, 65.0]
sleep(1)
ret=swift.set_wrist(angle=90+30,wait=True)#
print('角度：',swift.get_servo_angle(),ret)#[90.09, 75.03, 38.92, 94.0]
sleep(1)
ret=swift.set_wrist(angle=90+60,wait=True)#
print('角度：',swift.get_servo_angle(),ret)#[90.09, 75.03, 38.92, 118.0]
sleep(1)
ret=swift.set_wrist(angle=90+90,wait=True)#
# ret=swift.set_servo_angle(servo_id=SERVO_HAND,angle=90+20,wait=True)
# if ret is False:
print('角度：',swift.get_servo_angle(),ret)#[90.09, 75.03, 38.92, 168.0]
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
    swift.set_position(x=100, y=0, z=20, speed=1800, wait=True)