# -*- coding: utf-8 -*-
# @Time    : 2017/11/22 23:16
# @Author  : play4fun
# @File    : aiy_press_button1.py
# @Software: PyCharm

"""
aiy_press_button1.py:
"""
import subprocess

import sys, os
from time import sleep

#
say_list=[
"tell me a joke",
"Tell me a scary story",
"make me laugh",
"tell me about Thanksgiving",
"Sing a song",
"play little apple"]

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from uf.wrapper.swift_api import SwiftAPI
from uf.utils.log import *

logger_init(logging.VERBOSE)
# logger_init(logging.DEBUG)
# logger_init(logging.INFO)

print('setup swift ...')

# swift = SwiftAPI(dev_port = '/dev/ttyACM0')
# swift = SwiftAPI(filters = {'hwid': 'USB VID:PID=2341:0042'})
swift = SwiftAPI()  # default by filters: {'hwid': 'USB VID:PID=2341:0042'}
print('sleep 2 sec ...')
sleep(2)

print('device info: ')
print(swift.get_device_info())
sleep(2)
print('\nset X350 Y0 Z50 F500 ...')
swift.set_position(150, -100, 150,wait=True)
sleep(2)
print('\nset X350 Y0 Z50 F500 ...')
swift.set_position(x=280, y=0, z=140, wait=True)

swift.set_buzzer()
sleep(2)

# for i in range(1):#3
for words in say_list:#3
    swift.set_position(x=280,y=0,z=109,wait=True)
    swift.set_buzzer()


    # subprocess.call(['say', 'good morning,how are you'])
    # subprocess.call(['say', 'sing happy birthday'])
    subprocess.call(['say', words])

    # sleep(1)
    swift.set_position(z=140, wait=True)

    sleep(15)

print('done ...')
swift.reset(z=200)
try:
    while True:
        sleep(1)
except KeyboardInterrupt as e:
    print('KeyboardInterrupt', e)
finally:
    swift.reset()
    # swift.set_position(x=90, y=0, z=70, speed=1800, wait=True)