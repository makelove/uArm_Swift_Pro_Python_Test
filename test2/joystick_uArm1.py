# -*- coding: utf-8 -*-
#使用游戏手柄控制uArm Swift pro机械臂
import sys, os
from time import sleep

# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import evdev

device = evdev.InputDevice('/dev/input/event5')
print('device', device)
print('device.capabilities()', device.capabilities(verbose=True))

from uf.wrapper.swift_api import SwiftAPI
from uf.utils.log import *

logger_init(logging.VERBOSE)
# logger_init(logging.DEBUG)
# logger_init(logging.INFO)

print('setup swift ...')

# swift = SwiftAPI(dev_port = '/dev/ttyACM0')
# swift = SwiftAPI(filters = {'hwid': 'USB VID:PID=2341:0042'})
swift = SwiftAPI()  # default by filters: {'hwid': 'USB VID:PID=2341:0042'}

# def report_position(data):
#     print('data:', data)  # [x, y, z, r], r is wrist angle, ignore if not used
# swift.register_report_position_callback(report_position)
# swift.set_report_position(interval=0.5)  # 0.5 second (set 0 disable report)

print('sleep 2 sec ...')
sleep(2)

print('device info: ')
print(swift.get_device_info())

print('\nset X350 Y0 Z50 F500 ...')
swift.set_position(250, 0, 50, speed=1500)

swift.set_buzzer()
from evdev import categorize, ecodes

print('start control ...')
try:

    for event in device.read_loop():
        cate = categorize(event)
        if event.type == ecodes.EV_KEY:
            print('EV_KEY',  event)

        if event.type == ecodes.EV_ABS:
            print('EV_ABS',  event)
        if event.value == 0:
            continue

        # if event.code == 0:# Not good #左边摇杆
        #     x1 = 5 if event.value < 0 else -5
        #     pos = swift.get_position()
        #     x = pos[0]
        #     swift.set_position(x=x + x1)
        # if event.code == 1:
        #     y1 = 5 if event.value < 0 else -5
        #     pos = swift.get_position()
        #     y = pos[1]
        #     swift.set_position(y=y + y1)

        if event.code ==17:#good #左边，上和下
            x1 = 5 if event.value < 0 else -5
            pos=swift.get_position()
            x=pos[0]
            swift.set_position(x=x+x1)

        if event.code ==16:#左边，左和右
            y1 = 5 if event.value < 0 else -5
            pos=swift.get_position()
            y = pos[1]
            swift.set_position(y=y+y1)
        if event.code ==308:#右边，上-三角形
            z = 35
            swift.set_position(z=z)
        if event.code ==304:#右边，下-X
            z=2
            swift.set_position(z=z)
        if event.code == 307:#右边，左-正方形
            swift.set_pump(on=True)
        if event.code == 305:#右边，左-圆圈
            swift.set_pump(on=False)


        if event.code == 315:#Start键，退出
            print('break')
            break
            # while True:
            #     sleep(1)
except KeyboardInterrupt as e:
    print('KeyboardInterrupt', e)
finally:
    # print('ret5: ' + test_ports['swift_service']['handle'].call('set cmd_sync G0 X80 Y0 Z60'))
    swift.set_pump(on=False)
    swift.set_position(x=80, y=0, z=30, speed=1800, wait=True)
