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

cap = cv2.VideoCapture(0)


# ret = cap.set(3, 640)
# ret = cap.set(4, 480)

def draw_line_rectangle(frame):
    rows, cols, ch = frame.shape  # (720, 1280, 3)
    half = int(cols / 2)
    # 中间
    cv2.line(frame, (half, 0), (half, rows), (0, 0, 255), 5)

    margin = 40
    # 左边
    up_left1 = (margin, margin)  # 左上点
    down_right1 = (cols - margin, rows - margin)  # 右下点
    # print(up_left, down_right)
    cv2.rectangle(frame, up_left1, down_right1, (0, 255, 0), 3)


# while (True):
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    # img = cv2.imread('../data/sudoku.jpg')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

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

    draw_line_rectangle(frame)
    cv2.imshow("houghlines", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
