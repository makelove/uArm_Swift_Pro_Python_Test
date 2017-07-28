# -*- coding: utf-8 -*-
# @Time    : 2017/7/28 18:09
# @Author  : play4fun
# @File    : weiqi_test1.py
# @Software: PyCharm

"""
weiqi_test1.py:捡子
"""

from time import sleep

import cv2
import os
from uf.utils.log import *
#
from uf.wrapper.swift_api import SwiftAPI

import _thread, os
from skimage.measure import compare_mse as mse
import string, random

# import imutils
# imutils.is_cv2()


#
arm_move = False

logger_init(logging.INFO)


def init_uarm():
    print('setup swift ...')
    # port = '/dev/' + [x for x in os.listdir('/dev/') if x.startswith('cu.usbmodem')][0]
    # port = '/dev/' + [x for x in os.listdir('/dev/') if x.startswith('ttyA')][0]
    # swift = SwiftAPI(dev_port='/dev/cu.usbmodem1421')
    # print(port)
    # swift = SwiftAPI(dev_port=port)
    swift = SwiftAPI()

    sleep(2)

    # 复位
    # swift.set_position(x=60, y=0, z=50, speed=1800, wait=True)
    # swift.set_position(x=60, y=0, z=50, speed=1800, wait=False)
    # while swift.get_is_moving():
    #     sleep(0.1)
    swift.set_buzzer()
    return swift


swift = init_uarm()


def pick_place_poker(x, y, angle):  #
    global swift

    print('机械臂启动')
    swift.set_buzzer()
    swift.set_wrist(angle=90, wait=True)
    # 中间位置，高点
    # swift.set_position(x=176, y=0, z=165, speed=1800, wait=True)
    swift.set_position(x=x, y=y, z=165, speed=1800, wait=True)
    #
    # swift.set_position(x=207, y=-178, z=0, speed=1800, wait=True)
    swift.set_position(x=x, y=y, z=10, speed=1800, wait=True)  # TODO z=1
    return
    # 气泵
    swift.set_pump(on=True)

    # 中间位置，高点
    # swift.set_position(x=176, y=0, z=165, speed=1800, wait=True)
    swift.set_position(x=x, y=0, z=165, speed=1800, wait=True)

    swift.set_position(x=220, y=135, z=15, speed=1800, wait=True)
    sleep(1)
    angle0 = swift.get_servo_angle()[-1]
    print('现在角度:', angle0)
    # ret = swift.set_wrist(angle=abs(angle), wait=True)
    # ret = swift.set_wrist(angle=abs(angle-90), wait=True)
    # ret = swift.set_wrist(angle=abs(180), wait=True)
    # ret = swift.set_wrist(angle=abs(90 + angle), wait=True)
    # ret = swift.set_wrist(angle=abs(180 + angle), wait=True)
    ret = swift.set_wrist(angle=abs(angle0 + 90 - angle) + 90, wait=True)
    print('角度：', swift.get_servo_angle(), ret)  #
    sleep(1)
    # 气泵，释放扑克
    swift.set_pump(on=False)
    sleep(2)

    # final，复位
    swift.set_position(x=60, y=0, z=40, speed=1800, wait=True)
    swift.set_buzzer()


def rotate_poker(x, y, angle):
    global swift

    print('机械臂启动')

    angle0 = swift.get_servo_angle()[-1]
    print('初始角度:', angle0)

    swift.set_buzzer()
    # 中间位置，高点
    # swift.set_position(x=176, y=0, z=165, speed=1800, wait=True)
    swift.set_position(x=x, y=y, z=165, speed=1800, wait=True)
    #
    # swift.set_position(x=207, y=-178, z=0, speed=1800, wait=True)
    swift.set_position(x=x, y=y, z=2, speed=1800, wait=True)  # TODO z=1
    # 气泵
    swift.set_pump(on=True)

    swift.set_position(x=x, y=y, z=17, speed=1800, wait=True)  # 原地旋转
    sleep(1)
    # ret = swift.set_wrist(angle=angle + 90, wait=True)
    ret = swift.set_wrist(angle=180 - angle, wait=True)
    print('角度：', swift.get_servo_angle(), ret)  #
    sleep(1)
    # 气泵，释放扑克
    swift.set_pump(on=False)
    sleep(2)

    # final，复位
    swift.set_position(x=60, y=0, z=40, speed=1800, wait=True)
    swift.set_buzzer()


def move_thread(mx, my, angle):
    global arm_move
    print('开始 move_thread')
    try:
        # while True:
        #     sleep(1)
        if arm_move is True:
            x = my / 2 + 0
            y = (mx - 640) / 2 + 60
            print(mx, my, '-->', x, y)
            pick_place_poker(x, y, angle)
            # rotate_poker(x, y, angle)

    except KeyboardInterrupt as e:
        print('KeyboardInterrupt', e)
        # final，复位
    finally:
        # swift.set_position(x=60, y=0, z=40, speed=1800, wait=True)
        # swift.set_buzzer()

        #
        arm_move = False

        print('线程退出，机械臂复位')


# _thread.start_new_thread(move_thread, ())#NO

# 测试
# pick_place_poker()
# try:
#     while True:
#         sleep(1)
# except KeyboardInterrupt as e:
#     print('KeyboardInterrupt', e)
#     # final，复位
#     swift.set_position(x=60, y=0, z=40, speed=1800, wait=True)
#     swift.set_buzzer()
# exit(0)

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
rows, cols, ch = frame.shape  # (720, 1280, 3)
half = int(cols / 2)
up_left1 = (int(cols / 2 * 1 / 8), int(rows * 1 / 8))  # 左上点
down_right1 = (int(cols / 2 * 7 / 8), int(rows * 7 / 8))  # 右下点
up_left2 = (int(cols / 2 * 1 / 8 + cols / 2), int(rows * 1 / 8))  # 左上点
down_right2 = (int(cols / 2 * 7 / 8 + cols / 2), int(rows * 7 / 8))  # 右下点


def draw_line_rectangle(frame):
    rows, cols, ch = frame.shape  # (720, 1280, 3)
    half = int(cols / 2)
    # 中间
    cv2.line(frame, (half, 0), (half, rows), (0, 0, 255), 5)
    # 左边
    up_left1 = (int(cols / 2 * 1 / 8), int(rows * 1 / 8))  # 左上点
    down_right1 = (int(cols / 2 * 7 / 8), int(rows * 7 / 8))  # 右下点
    # print(up_left, down_right)
    cv2.rectangle(frame, up_left1, down_right1, (0, 255, 0), 3)

    # 右边
    up_left2 = (int(cols / 2 * 1 / 8 + cols / 2), int(rows * 1 / 8))  # 左上点
    down_right2 = (int(cols / 2 * 7 / 8 + cols / 2), int(rows * 7 / 8))  # 右下点
    # print(up_left, down_right)
    cv2.rectangle(frame, up_left2, down_right2, (255, 0, 0), 3)

    return up_left1, down_right1, up_left2, down_right2


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


cap = cv2.VideoCapture(0)

# ret = cap.set(3, 640)
# ret = cap.set(4, 480)

# margin = 60
margin = 30


def draw_line_rectangle(frame, margin):
    rows, cols, ch = frame.shape  # (720, 1280, 3)
    half = int(cols / 2)
    # 中间
    cv2.line(frame, (half, 0), (half, rows), (0, 0, 255), 2)

    # margin = 40
    # 左边
    up_left1 = (margin, margin)  # 左上点
    down_right1 = (cols - margin, rows - margin)  # 右下点
    # print(up_left, down_right)
    cv2.rectangle(frame, up_left1, down_right1, (0, 255, 0), 3)


ret, temp = cap.read()
tm = 0
while cap.isOpened():
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    if key == ord('s'):
        cv2.imwrite(id_generator() + '.jpg', frame2)

    # Capture frame-by-frame
    ret, frame = cap.read()
    m = mse(cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY), cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    # print('mse', m, '----\n')
    if abs(m - tm) < 2:  # 静止画面，不用重复计算
        continue
    else:
        temp = frame.copy()
        tm = m
    #
    # print(margin,frame.shape[0] - margin, margin,frame.shape[1] - margin)#40 680 40 1240
    frame2 = frame[margin:frame.shape[0] - margin, margin:frame.shape[1] - margin]  # .copy()
    # cv2.imshow('frame2', frame2)

    gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    # edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # HoughCircles(image, method, dp, minDist, circles=None, param1=None, param2=None, minRadius=None, maxRadius=None)
    # circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=100, param2=30, minRadius=10, maxRadius=40)

    # circles = circles1[0, :, :]  # 提取为二维
    # circles = np.uint16(np.around(circles1))
    # print(circles)

    cimg = frame2
    if circles is not None:
        print('len circles[0, :]',len(circles[0, :]))#有干扰，不止一个圆圈
        for i in circles[0, :]:
            # for i in circles[:]:
            # draw the outer circle
            cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)

            if arm_move is False:
                arm_move = True
                mx, my = i[0], i[1]
                angle0 = 0
                _thread.start_new_thread(move_thread, (mx, my, angle0))

    # cv2.imshow('detected circles', cimg)

    draw_line_rectangle(frame, margin)
    cv2.imshow("houghlines", frame)
    # cv2.imwrite('frame3.jpg', frame[margin:frame.shape[0] - margin, margin:frame.shape[1] - margin])

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

#
# final，复位
swift.set_position(x=60, y=10, z=40, speed=1800, wait=False)
swift.set_buzzer()
