# -*- coding: utf-8 -*-
# @Time    : 2017/8/16 09:14
# @Author  : play4fun
# @File    : swift_utils.py
# @Software: PyCharm

"""
swift_utils.py:
"""
import _thread, os
from uf.wrapper.swift_api import SwiftAPI
from uf.utils.log import *
from math import ceil
from time import sleep

# logger_init(logging.VERBOSE)
logger_init(logging.INFO)


class Swift(SwiftAPI):
    '''
    自定义
    '''

    def __init__(self, step=1):
        self.swift = SwiftAPI()
        self.position = {'x': 0, 'y': 0, 'z': 0}
        # self.position = self.get_position()
        self.polar = {'x': 0, 'y': 0, 'z': 0}
        # self.polar = self.get_polar()
        self.destination = {}
        self.step = step

    def set_buzzer(self):
        self.swift.set_buzzer()

    def get_device_info(self):
        self.swift.get_device_info()

    def get_position(self):
        position = self.swift.get_position()
        if position is None:
            return self.position
        position = {'x': position[0], 'y': position[1], 'z': position[2]}
        self.position = position
        return position

    def get_polar(self):
        polar = self.swift.get_polar()
        if polar is None:
            return self.polar
        polar = {'x': polar[0], 'y': polar[1], 'z': polar[2]}
        self.polar = polar
        return polar

    def set_position(self, x=None, y=None, z=None,
                     speed=None, relative=False, wait=False):
        def choose(a1, a2, b):
            if b >= 0:
                return a1
            else:
                return a2

        if wait is False:
            # 新建一个线程，set_position
            # self.swift.set_position(x=x,y=y,z=z,speed=speed,relative=relative,wait=wait)
            print('新建一个线程')
            _thread.start_new_thread(self.set_position, (x, y, z, speed, relative, True))

        else:
            d = {'x': x, 'y': y, 'z': z}
            d2 = {k: v if v is not None else self.position[k] for k, v in d.items()}
            self.destination = d2

            # 计算需要走多少步
            x1 = self.destination['x'] - self.position['x']
            y1 = self.destination['y'] - self.position['y']
            z1 = self.destination['z'] - self.position['z']
            steps = max([ceil(abs(x1)), ceil(abs(y1)), ceil(abs(z1))])
            for step in range(0, int(steps)):
                x2 = self.position['x'] + x1 / steps

                # if abs(x2) >= abs(self.destination['x']):
                #     x2 = self.destination['x']
                x2 = choose(x2, self.destination['x'], x1)

                y2 = self.position['y'] + y1 / steps
                y2 = choose(y2, self.destination['y'], y1)

                z2 = self.position['z'] + z1 / steps
                z2 = choose(z2, self.destination['z'], z1)

                ret = self.swift.set_position(x=x2, y=y2, z=z2, wait=True)
                if ret is True:
                    self.position = self.get_position()
                    self.polar = self.get_polar()
                    print(self.position)

                else:
                    raise Exception('set_position Error')
            self.swift.set_position(x=self.destination['x'], y=self.destination['y'], z=self.destination['z'], wait=True)
            print('destination:', self.destination, self.position, x2, y2, z2)
            return True

    def reset1(self):
        x = 103
        y = 0
        z = 42
        speed = 400
        self.reset(x, y, z, speed)

    def reset(self, x, y, z, speed):
        # self.swift.reset()
        # self.set_servo_attach()
        sleep(0.1)
        # self.set_position(150, 0, 150, speed=200, wait=True)
        self.set_position(x, y, z, speed=speed, wait=True)
        self.set_pump(False)
        self.set_gripper(False)
        self.set_wrist(90)  # 指向，方向
