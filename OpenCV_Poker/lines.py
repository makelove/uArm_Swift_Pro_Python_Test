# -*- coding: utf-8 -*-
# @Time    : 2017/7/26 19:24
# @Author  : play4fun
# @File    : lines.py
# @Software: PyCharm

"""
lines.py:
"""

import cv2
import numpy as np
from skimage.measure import compare_mse as mse
from OpenCV_Poker.utils import id_generator

cap = cv2.VideoCapture(0)

# ret = cap.set(3, 640)
# ret = cap.set(4, 480)

margin = 40


def draw_line_rectangle(frame, margin):
    rows, cols, ch = frame.shape  # (720, 1280, 3)
    half = int(cols / 2)
    # 中间
    cv2.line(frame, (half, 0), (half, rows), (0, 0, 255), 5)

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
        cv2.imwrite(id_generator() + '.jpg', frame)


    # Capture frame-by-frame
    ret, frame = cap.read()
    m = mse(cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY), cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    print('mse', m, '----\n')
    # if m < 150:#静止画面，不用重复计算
    if abs(m - tm) < 2:  # 静止画面，不用重复计算
        continue
    else:
        temp = frame
        tm = m
    #
    # print(margin,frame.shape[0] - margin, margin,frame.shape[1] - margin)#40 680 40 1240
    frame2 = frame[margin:frame.shape[0] - margin, margin:frame.shape[1] - margin]#.copy()
    # cv2.imshow('frame2', frame2)


    gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    image, contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 200]  # 过滤太小的contour
    print(len(contours))
    # edges = cv2.drawContours(edges, contours, -1, (255, 255, 255), 3)
    frame = cv2.drawContours(frame2, contours, -1, (0, 0, 255), 3)
    # cv2.imshow('edges', edges)

    #
    for contour in contours:
        #
        c = contour
        # print('边数：', len(c))
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        if len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(contour)
            print(x, y, w, h)
            # cv2.rectangle(frame2, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # 画4条线
            cv2.line(frame, (x, y), (x, x + h), (255, 0, 0), 2)
            cv2.line(frame, (x, y), (x + w, y), (255, 255, 0), 2)
            cv2.line(frame, (x, y + h), (x + w, y + h), (0, 0, 255), 2)
            cv2.line(frame, (x + w, y), (x + w, y + h), (0, 0, 0), 2)

    minLineLength = 100
    maxLineGap = 10
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength, maxLineGap)
    if lines is None:
        continue
    print("Len of lines:", len(lines))
    # print(lines)

    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # 检测长方形



    draw_line_rectangle(frame, margin)
    cv2.imshow("houghlines", frame)
    # cv2.imwrite('frame3.jpg', frame[margin:frame.shape[0] - margin, margin:frame.shape[1] - margin])



# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
