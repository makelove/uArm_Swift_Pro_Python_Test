# -*- coding: utf-8 -*-
# @Time    : 2017/12/21 23:21
# @Author  : play4fun
# @File    : gcode_write_dragon.py
# @Software: PyCharm

"""
gcode_write_dragon.py:
毛笔字：龙
"""

import sys, os
from time import sleep

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from uf.ufc import ufc_init
from uf.comm.serial_ascii import SerialAscii
from uf.utils.log import *

logger_init(logging.VERBOSE)

print('setup ser_ascii ...')

ser_iomap = {
    'out': 'ser_out',
    'in': 'ser_in',
    'service': 'ser_service'
}

ufc = ufc_init()
ser_ascii = SerialAscii(ufc, 'ser_ascii', ser_iomap, filters={'hwid': 'USB VID:PID=2341:0042'})

print('setup test ...')
logger = logging.getLogger('test')


def ser_out_cb(msg):
    logger.debug('callback: ' + msg)


test_ports = {
    'ser_out': {'dir': 'in', 'type': 'topic', 'callback': ser_out_cb},
    'ser_in': {'dir': 'out', 'type': 'topic'},
    'ser_service': {'dir': 'out', 'type': 'service'}
}

test_iomap = {
    'ser_out': 'ser_out',
    'ser_in': 'ser_in',
    'ser_service': 'ser_service'
}

ufc.node_init('test', test_ports, test_iomap)

print('\nsleep 2 sec ...\n')
sleep(2)

# print('\nset X330 ...')
# test_ports['ser_in']['handle'].publish('G0 X300 Y0 Z50')



with open('long_0001.GCODE') as f:
    gcodes = f.readlines()

# print(gcodes)

for line in gcodes:#[:40]:
    if line.strip() == '':
        continue
    print(line)
    test_ports['ser_in']['handle'].publish(line)
    sleep(0.1)

while True:
    sleep(1)