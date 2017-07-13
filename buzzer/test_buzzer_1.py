# -*- coding: utf-8 -*-
# @Time    : 2017/7/11 上午8:45
# @Author  : play4fun
# @File    : test_buzzer_1.py
# @Software: PyCharm

"""
test_buzzer_1.py:
"""
import os

from uf.wrapper.swift_api import SwiftAPI
from uf.utils.log import *
from time import sleep

#
arm_move = False

logger_init(logging.INFO)
print('setup swift ...')

# def get_uarm_port():
#     TD
#     pass

port = '/dev/' + [x for x in os.listdir('/dev/') if x.startswith('cu.usbmodem')][0]
# swift = SwiftAPI(dev_port='/dev/cu.usbmodem1421')
print(port)
swift = SwiftAPI(dev_port=port)

sleep(0.5)

# swift.set_buzzer(freq = 1000, time = 200)
swift.set_buzzer(freq = 500, time = 10000)
# for x in range(100,5000,100):
#     print(x)
#     swift.set_buzzer(freq=x, time=200)
#     sleep(3)