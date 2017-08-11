# -*- coding: utf-8 -*-
# @Time    : 2017/8/6 08:54
# @Author  : play4fun
# @File    : 转换坐标系.py
# @Software: PyCharm

"""
转换坐标系.py:摄像头-机械臂之间的坐标系，进行转换

x
y轴，分别测试
"""
import cv2
import numpy as np
from time import sleep

from uf.wrapper.swift_api import SwiftAPI
from uf.utils.log import *

# logger_init(logging.VERBOSE)
# logger_init(logging.DEBUG)
logger_init(logging.INFO)

print('setup swift ...')
swift = SwiftAPI()  # default by filters: {'hwid': 'USB VID:PID=2341:0042'}
print('sleep 2 sec ...')
sleep(2)
print('device info: ')
print(swift.get_device_info())

#
cap = cv2.VideoCapture(0)
cap.read()
cap.read()
cap.read()
cap.read()
cap.read()
cap.read()
if cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    cv2.waitKey(2000)
else:
    raise Exception('camera not open')

list_camera = []


def camera_get_weiqi_position():  # 摄像头获取 棋子的坐标
    ret, frame = cap.read()
    if ret is not True:
        raise Exception('camera not open')
    cv2.imshow('frame', frame)
    cv2.waitKey(500)

    img = cv2.medianBlur(frame, 5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=100, param2=30, minRadius=10, maxRadius=50)

    if circles is None:
        return (0, 0)
        # raise Exception('none circles')
        # exit(-1)

    circles = np.uint16(np.around(circles))
    print('多少个圆：', len(circles), circles)
    i = circles[0][0]
    x, y = i[0], i[1]
    return x, y


def uarm_move_camera_read(x1, y1, x2, y2):
    swift.set_position(x=x1, y=y1, z=80, wait=True)
    swift.set_position(x=x1, y=y1, z=3, wait=True)
    swift.set_pump(on=True)  # 吸取围棋

    swift.set_position(z=80, wait=True)
    swift.set_position(x=x2, y=y2, z=10, wait=True)
    swift.set_pump(on=False)  # 放下围棋
    sleep(1)
    swift.set_pump(on=False)  # 放下围棋
    # 重置
    swift.set_position(z=80, wait=True)
    swift.set_position(x=103, y=0, z=42, wait=True)

    cx, cy = camera_get_weiqi_position()
    return cx, cy  # 摄像头坐标


# 机械臂先移动
# 指定第一个坐标
# set_position

x, y = camera_get_weiqi_position()
print(x, y)
list_camera.append((x, y))
list_robot = [(175.7, 75.64), (201, 53), (251, -25), (271, 103), (324.68, 24.45)]

for (x1, y1), (x2, y2) in zip(list_robot[:-1], list_robot[1:]):
    print((x1, y1), (x2, y2))
    x, y = uarm_move_camera_read(x1, y1, x2, y2)
    print(x, y)
    list_camera.append((x, y))
    sleep(1)

# 使用机器学习来得出2坐标系之间的关系
# sklearn
print(list_robot)
# [(175.7, 75.64), (201, 53), (251, -25), (271, 103), (324.68, 24.45)]
print(list_camera)
# [(834, 234), (774, 294), (580, 414), (890, 478), (692, 610)]