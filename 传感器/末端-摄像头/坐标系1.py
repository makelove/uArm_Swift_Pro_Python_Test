# -*- coding: utf-8 -*-
# @Time    : 2017/8/12 22:07
# @Author  : play4fun
# @File    : 坐标系1.py
# @Software: PyCharm

"""
坐标系1.py:
"""

import cv2
import numpy as np
from time import sleep
import _thread, os
from swift_utils import Swift


# from uf.wrapper.swift_api import SwiftAPI
# from uf.utils.log import *
#
# logger_init(logging.VERBOSE)
# logger_init(logging.DEBUG)
# logger_init(logging.INFO)


print('setup swift ...')
# swift = SwiftAPI()  # default by filters: {'hwid': 'USB VID:PID=2341:0042'}
swift = Swift()
print('sleep 2 sec ...')
sleep(2)
print('device info: ')
print(swift.get_device_info())
sleep(4)

# 上升到最高点
swift.set_position(x=152, y=0, speed=1800, wait=True)
sleep(3)
swift.set_position(x=152, y=81, z=148, speed=1800, wait=True)
sleep(5)

#
cap = cv2.VideoCapture(0)


# 画线
def draw_line_rectangle(frame, margin, polar):
    print('polar:rotation, stretch, height', polar, '倾斜角度', polar[0])
    rows, cols, ch = frame.shape  # (720, 1280, 3)
    half_v = int(cols / 2)
    half_h = int(rows / 2)
    # 中间,竖线
    cv2.line(frame, (half_v, 0), (half_v, rows), (0, 0, 255), 3)
    m1 = 20
    cv2.line(frame, (half_v - m1, 0), (half_v - m1, rows), (0, 255, 0), 1)
    cv2.line(frame, (half_v + m1, 0), (half_v + m1, rows), (0, 255, 0), 1)
    # 横线
    cv2.line(frame, (0, half_h), (cols, half_h), (0, 0, 255), 4)

    # margin = 40
    # 左边
    up_left1 = (margin, margin)  # 左上点
    down_right1 = (cols - margin, rows - margin)  # 右下点
    # print(up_left, down_right)
    cv2.rectangle(frame, up_left1, down_right1, (0, 255, 0), 3)


is_moving = False


def move_thread(x, y, z, speed, wait=False):
    global swift

    print('机械臂启动')
    swift.set_buzzer()
    global is_moving
    is_moving = True
    # swift.set_position(x=x, y=y, z=z, speed=1000, wait=True)
    ret = swift.set_position(x=x, y=y, z=z, speed=1000, wait=True)
    if ret is False:
        raise Exception(f'set_position错误x{x}y{y}z{z}')
    # sleep(2)
    is_moving = False
    print('完成 move_thread')
    swift.set_buzzer()


def is_move():
    global is_moving
    move = swift.get_is_moving()
    print('移动？', move)
    is_moving = True if move is True else False
    return is_moving


# if is_move() is False:#不移动时，获取极坐标
#     polar = swift.get_polar()

polar=[0,0,0]
def get_polar():
    global polar
    polar = swift.get_polar()
    print('thread get_polar',polar)



print('imshow')
ret, frame = cap.read()
cv2.imshow('frame', frame)
cv2.waitKey(1000)

postive = False
margin = 40
while cap.isOpened():
    print('waitKey(50)')
    key = cv2.waitKey(50)
    if key == ord("q"):
        break
    # _thread.start_new_thread(is_move, ())

    if not swift.get_is_moving2():#阻塞线程
    # if is_moving is False:
        is_moving = True
        if postive is False:
            print('-71')
            swift.set_position(x=172, y=-71, z=148, speed=1800,wait=False)
            # _thread.start_new_thread(move_thread, (132, -71, 118, 1800, True))
            postive = True

        else:
            print('71')
            swift.set_position(x=172, y=-71, z=148, speed=1800, wait=False)
            # _thread.start_new_thread(move_thread, (92, 50, 158, 1800, True))
            # _thread.start_new_thread(move_thread, (132, 71, 108, 1800, True))
            postive = False
            #

    ret, frame = cap.read()

    # 识别围棋
    img = cv2.medianBlur(frame, 5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=100, param2=30, minRadius=10, maxRadius=50)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        print('多少个圆：', len(circles), circles)
        for i in circles[0, :]:
            # for i in circles[:]:
            # draw the outer circle
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)

    # 极坐标 #阻碍？
    # polar = swift.get_polar()
    polar = swift.polar
    # _thread.start_new_thread(get_polar, ())
    # polar = [1, 2, 3]
    draw_line_rectangle(frame, margin, polar)
    cv2.imshow('frame', frame)

cv2.destroyAllWindows()

# 重置
swift.set_position(z=80, wait=True)
swift.set_position(x=103, y=0, z=42, wait=True)
