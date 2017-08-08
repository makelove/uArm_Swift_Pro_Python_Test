#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2017, UFactory, Inc.
# All rights reserved.
#
# Author: Duke Fong <duke@ufactory.cc>


import sys, os
from time import sleep

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from uf.ufc import ufc_init
from uf.swift import Swift
from uf.utils.log import *

# logger_init(logging.VERBOSE)
# logger_init(logging.DEBUG)
logger_init(logging.INFO)

print('setup swift ...')

swift_iomap = {
    'pos_in': 'swift_pos_in',
    'pos_out': 'swift_pos_out',
    'service': 'swift_service'
}

ufc = ufc_init()
# swift = Swift(ufc, 'swift', swift_iomap, dev_port = '/dev/ttyACM0')
# swift = Swift(ufc, 'swift', swift_iomap, filters = {'hwid': 'USB VID:PID=2341:0042'})
swift = Swift(ufc, 'swift', swift_iomap)  # default by filters: {'hwid': 'USB VID:PID=2341:0042'}

print('setup test ...')


def pos_cb(msg):
    print('pos_cb: ' + msg)


test_ports = {
    'swift_pos': {'dir': 'out', 'type': 'topic'},
    'swift_pos_out': {'dir': 'in', 'type': 'topic', 'callback': pos_cb},
    'swift_service': {'dir': 'out', 'type': 'service'}
}

test_iomap = {
    'swift_pos': 'swift_pos_in',
    'swift_pos_out': 'swift_pos_out',
    'swift_service': 'swift_service'
}

# install handle for ports which are listed in the iomap
ufc.node_init('test', test_ports, test_iomap)

print('sleep 2 sec ...')
sleep(2)

print('enable report_pos: ' + test_ports['swift_service']['handle'].call('set report_pos on 0.2'))
# print('disable report_pos: ' + test_ports['swift_service']['handle'].call('set report_pos off'))

print('set X330 ...')
# topics are always async
# without 'G0', port 'pos' is dedicated for moving
test_ports['swift_pos']['handle'].publish('X350 Y0 Z50')

print('ret1: ' + test_ports['swift_service']['handle'].call('set cmd_sync G0 X340'))
print('ret2: ' + test_ports['swift_service']['handle'].call('set cmd_sync G0 X320'))
print('ret3: ' + test_ports['swift_service']['handle'].call('set cmd_sync G0 X300'))
print('ret4: ' + test_ports['swift_service']['handle'].call('set cmd_sync G0 X200'))
print('ret5: ' + test_ports['swift_service']['handle'].call('set cmd_sync G0 X190'))

print('done ...')
try:
    while True:
        sleep(1)
except KeyboardInterrupt as e:
    print('KeyboardInterrupt', e)
finally:
    print('ret5: ' + test_ports['swift_service']['handle'].call('set cmd_sync G0 X80 Y0 Z60'))
    # swift.set_position(x=60, y=0, z=40, speed=1800, wait=True)
