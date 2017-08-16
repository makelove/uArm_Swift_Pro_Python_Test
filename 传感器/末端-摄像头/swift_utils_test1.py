# -*- coding: utf-8 -*-
# @Time    : 2017/8/16 10:17
# @Author  : play4fun
# @File    : swift_utils_test1.py
# @Software: PyCharm

"""
swift_utils_test1.py:
"""

from swift_utils import Swift
from time import sleep


swift=Swift()
print('sleep 2 sec ...')
sleep(2)
print('device info: ')
print(swift.get_device_info())
sleep(4)

print(swift.get_position())
print(swift.get_polar())
# swift.set_servo_attach()#锁死电机
# sleep(1)
# swift.set_servo_detach()#解锁电机
# sleep(10)

# 上升到最高点
swift.set_position(x=152, y=0,z=20, speed=1800, wait=True)
sleep(5)
swift.set_position(x=152, y=81, z=148, speed=1800, wait=True)
sleep(5)

swift.reset1()

exit(0)