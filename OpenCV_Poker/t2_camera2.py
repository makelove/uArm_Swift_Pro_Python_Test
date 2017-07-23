# -*- coding: utf-8 -*-
# @Time    : 2017/7/9 上午11:19
# @Author  : play4fun
# @File    : t2_camera.py
# @Software: PyCharm

"""
t2_camera.py:
"""

import numpy as np
import cv2

import _thread, os
# import imutils
# imutils.is_cv2()

#
from uf.wrapper.swift_api import SwiftAPI
from uf.utils.log import *
from time import sleep
import random,string


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


#
arm_move = False

logger_init(logging.INFO)


def init_uarm():
    print('setup swift ...')
    port = '/dev/' + [x for x in os.listdir('/dev/') if x.startswith('cu.usbmodem')][0]
    # port = '/dev/' + [x for x in os.listdir('/dev/') if x.startswith('ttyA')][0]
    # swift = SwiftAPI(dev_port='/dev/cu.usbmodem1421')
    print(port)
    swift = SwiftAPI(dev_port=port)

    sleep(2)

    # 复位
    swift.set_position(x=60, y=0, z=50, speed=1800, wait=True)
    # swift.set_position(x=60, y=0, z=50, speed=1800, wait=False)
    # while swift.get_is_moving():
    #     sleep(0.1)
    swift.set_buzzer()
    return swift


# swift=init_uarm()


def pick_place_poker(x, y):  #
    global swift

    print('机械臂启动')
    swift.set_buzzer()
    # 中间位置，高点
    # swift.set_position(x=176, y=0, z=165, speed=1800, wait=True)
    swift.set_position(x=x, y=y, z=165, speed=1800, wait=True)
    #
    # swift.set_position(x=207, y=-178, z=0, speed=1800, wait=True)
    swift.set_position(x=x, y=y, z=0, speed=1800, wait=True)  # TODO z=1
    # 气泵
    swift.set_pump(on=True)

    # 中间位置，高点
    # swift.set_position(x=176, y=0, z=165, speed=1800, wait=True)
    swift.set_position(x=x, y=0, z=165, speed=1800, wait=True)

    swift.set_position(x=220, y=135, z=30, speed=1800, wait=True)
    # 气泵，释放扑克
    swift.set_pump(on=False)
    sleep(2)

    # final，复位
    swift.set_position(x=60, y=0, z=40, speed=1800, wait=True)
    swift.set_buzzer()


def move_thread(mx, my):
    global arm_move
    print('开始 move_thread')
    try:
        # while True:
        #     sleep(1)
        if arm_move is True:
            x = my / 2 + 50
            y = (mx - 640) / 2 + 30
            print(mx, my, '-->', x, y)
            pick_place_poker(x, y)

    except KeyboardInterrupt as e:
        print('KeyboardInterrupt', e)
        # final，复位
    finally:
        swift.set_position(x=60, y=0, z=40, speed=1800, wait=True)
        swift.set_buzzer()

        #
        arm_move = False

        print('线程退出，机械臂复位')


# _thread.start_new_thread(move_thread, ())

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


# while (True):
while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # 划线
    up_left1, down_right1, up_left2, down_right2 = draw_line_rectangle(frame)

    # ROI
    # frame2 = frame[80:560, 90:630]#
    frame2 = frame[up_left1[1]:down_right1[1], up_left1[0]:down_right1[0]]  #
    # print(up_left1[0],down_right1[0], up_left1[1],down_right1[1])
    # cv2.imshow('frame2', frame2)

    # cv2.waitKey(0)
    # break

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    #
    # ret, thresh = cv2.threshold(src=gray, thresh=127, maxval=255, type=cv2.THRESH_BINARY)  # src, thresh, maxval, type

    thresh = cv2.Canny(gray, 50, 150, apertureSize=3)

    #
    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    try:
        hierarchy = hierarchy[0]
    except:
        hierarchy = []

    height, width = thresh.shape
    min_x, min_y = width, height
    max_x = max_y = 0

    #最大的contour

    # computes the bounding box for the contour, and draws it on the frame,
    for contour, hier in zip(contours, hierarchy):

        #
        c = contour
        # print('边数：', len(c))
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        if len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(contour)
            min_x, max_x = min(x, min_x), max(x + w, max_x)
            min_y, max_y = min(y, min_y), max(y + h, max_y)

            if w > 80 or h > 80:
                # cv2.rectangle(frame2, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # print('rectangle:',x, y, w, h)#rectangle: 151 205 123 181
                pass
            if arm_move is False:
                if w > 100 and h > 140:  # TODO 识别出扑克牌
                    # 重心
                    M = cv2.moments(contour)
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    print('重心:', cx, cy)

                    # 找出中心点
                    mx = x + w / 2
                    my = y + h / 2
                    print('中心:', mx, my)
                    # 多线程，发送到机械臂
                    # pick_place_poker(move=True)

                    arm_move = True
                    # _thread.start_new_thread(move_thread, (mx, my))

    # Display the resulting frame
    cv2.namedWindow('frame', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('frame', frame)
    cv2.imshow('frame2', frame2)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    if key == ord('s'):
        cv2.imwrite(id_generator()+'.jpg', frame2)  # TODO 随机文件名

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

#
# final，复位
swift.set_position(x=60, y=10, z=40, speed=1800, wait=False)
swift.set_buzzer()
