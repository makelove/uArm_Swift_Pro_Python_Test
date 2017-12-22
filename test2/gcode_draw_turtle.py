# -*- coding: utf-8 -*-
# @Time    : 2017/12/21 23:50
# @Author  : play4fun
# @File    : gcode_draw_turtle.py
# @Software: PyCharm

"""
gcode_draw_turtle.py:
"""

import turtle
from time import sleep

with open('long_0001.GCODE') as f:
    gcodes = f.readlines()


# print(gcodes)

def parse_line(line):
    sp1 = line.split()
    x = y = z = None
    for sp in sp1:
        if sp.startswith('X'):
            x = float(sp[1:])
        if sp.startswith('Y'):
            y = float(sp[1:])
        if sp.startswith('Z'):
            z = float(sp[1:])
    return x, y, z

z49 =49
for line in gcodes:  # [:40]:
    if line.strip() == '':
        continue
    print(line)
    # test_ports['ser_in']['handle'].publish(line)
    x, y, z=parse_line(line)
    if z!=z49:
        turtle.up()
        sleep(2)
    else:
        turtle.down()
    if x is not None and y is not None:
        turtle.goto(x,y)
        sleep(0.1)

while True:
    sleep(1)
