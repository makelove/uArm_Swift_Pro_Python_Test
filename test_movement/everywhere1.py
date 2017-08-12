# -*- coding: utf-8 -*-
# @Time    : 2017/7/9 上午8:01
# @Author  : play4fun
# @File    : everywhere1.py
# @Software: PyCharm

"""
everywhere1.py:
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

# swift.reset()

# 获取位置
# TODO 新建多线程，在后台监控位置，每隔1秒，打印一次
fvalues = swift.get_position()
print('现在位置：', fvalues)  # [104.29, 13.51, 36.49]#原点
polar = swift.get_polar()#球坐标系（Spherical coordinate system）
print('极点：', polar)  # [355.11, 122.35, 42.17]
# xp,yp,zp=polar
xp, yp, zp = [355.11, 122.35, 42.17]

# swift.set_position(x=120,z=80,y=30)


# print('\nset X350 Y0 Z50 F500 ...')
# swift.set_position(350, 0, 50, speed=1500)

# swift.set_position(x=300, wait=True)
# sleep(3)
# swift.set_position(y=190, wait=True)

sleep(1)

tmpx = 0
tmpy = 0
tmpz = 0
try:
    while True:
        # 获取位置
        values = swift.get_position()
        x, y, z = values
        print('现在位置：', values)

        try:
            tmpx = max(x, tmpx, xn)
            tmpy = max(y, tmpy, yn)
            tmpz = max(z, tmpz, zn)
        except:
            tmpx = x
            tmpy = y
            tmpz = z

        # 向前运动10步
        step=30
        xn = x + step
        yn = y + step
        zn = z + step
        print(xn, yn, zn)
        # if xn==tmpx:
        #     break
        # posrs=swift.set_position(x=xn, y=0, z=0, wait=True)
        # print('set_position：',posrs)
        if xn != tmpx:
            # swift.set_position(x=xn,y=0,z=0, wait=True)
            swift.set_position(x=xn, y=-yp, z=20, speed=2000,wait=True)
        elif yn != tmpy:
            swift.set_position(x=x, y=yn, z=20, speed=2500, wait=True)
        # elif zn != tmpz:
        #     swift.set_position(x=int(x / 2), y=int(y / 2), z=zn, wait=True)
        # else:# 到达极点
        #     #复位
        #     swift.set_position(x=30, y=0, z=0, wait=True)
        #     #回到初始位置
        #     swift.set_position(x=fvalues[0], y=fvalues[1], z=fvalues[2], wait=True)
        else:
            break

        # 睡眠3秒
        # sleep(1)

        polar = swift.get_polar()
        print('极点：', polar)
        print('------')
except KeyboardInterrupt as e:
    print('KeyboardInterrupt', e)

except Exception as e:
    print('Error', e)
finally:
    print('finally')
    # swift.reset()#重置，复位？
    swift.set_position(x=60, y=0, z=40, speed=1800, wait=True)
    # swift.set_position(x=0, y=0, z=0, wait=True)

print('finished')
exit(0)
#
# try:
#     while True:
#         sleep(1)
# except KeyboardInterrupt as e:
#     print('KeyboardInterrupt', e)
