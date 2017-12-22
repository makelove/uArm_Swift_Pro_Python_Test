# -*- coding: utf-8 -*-
# @Time    : 2017/12/22 16:55
# @Author  : play4fun
# @File    : log_to_gcode.py
# @Software: PyCharm

"""
log_to_gcode.py:
从日志中生成gocde
"""

x = '''
/Users/play/.py3/bin/python3.6 /Users/play/github/Robot_Arm_Write_Chinese/py/uArm_draw1.py
想draw哪个汉字？个
swift/serial_ascii: INFO: choose device: /dev/cu.usbmodem1411
swift/serial_ascii: INFO: /dev/cu.usbmodem1411:
setup swift ...
swift/serial_ascii: INFO:   hwid        : "USB VID:PID=2341:0042 LOCATION=20-1"
swift/serial_ascii: INFO:   manufacturer: "Arduino (www.arduino.cc)"
swift/serial_ascii: INFO:   product     : "Arduino Mega 2560"
swift/serial_ascii: INFO:   description : "Arduino Mega 2560"
sleep 2 sec ...
swift/serial_ascii: VERBOSE: -> start
swift/serial_ascii: VERBOSE: -> echo:Marlin 1.1.0-RC7
swift/serial_ascii: VERBOSE: -> echo: Last Updated: 2016-07-31 12:00 | Author: (none, default config)
swift/serial_ascii: VERBOSE: -> Compiled: Nov  8 2017
swift/serial_ascii: VERBOSE: -> echo: Free Memory: 2386  PlannerBufferBytes: 924
swift/serial_ascii: VERBOSE: -> echo:Hardcoded Default Settings Loaded
swift/serial_ascii: VERBOSE: -> echo:Steps per unit:
swift/serial_ascii: VERBOSE: -> echo:  M92 X320.00 Y320.00 Z320.00 E84.88
swift/serial_ascii: VERBOSE: -> echo:Maximum feedrates (mm/s):
swift/serial_ascii: VERBOSE: -> echo:  M203 X2000.00 Y2000.00 Z2000.00 E25.00
swift/serial_ascii: VERBOSE: -> echo:Maximum Acceleration (mm/s2):
swift/serial_ascii: VERBOSE: -> echo:  M201 X2000 Y2000 Z2000 E10000
swift/serial_ascii: VERBOSE: -> echo:Accelerations: P=printing, R=retract and T=travel
swift/serial_ascii: VERBOSE: -> echo:  M204 P25.00 R25.00 T100.00
swift/serial_ascii: VERBOSE: -> echo:Advanced variables: S=Min feedrate (mm/s), T=Min travel feedrate (mm/s), B=minimum segment time (ms), X=maximum XY jerk (mm/s),  Z=maximum Z jerk (mm/s),  E=maximum E jerk (mm/s)
swift/serial_ascii: VERBOSE: -> echo:  M205 S0.00 T0.00 B20000 X1.00 Z1.00 E5.00
swift/serial_ascii: VERBOSE: -> echo:Home offset (mm)
swift/serial_ascii: VERBOSE: -> echo:  M206 X0.00 Y0.00 Z0.00
swift/serial_ascii: VERBOSE: -> echo:PID settings:
swift/serial_ascii: VERBOSE: -> echo:  M301 P22.20 I1.08 D114.00
swift/serial_ascii: VERBOSE: -> echo:Filament settings: Disabled
swift/serial_ascii: VERBOSE: -> echo:  M200 D1.75
swift/serial_ascii: VERBOSE: -> echo:  M200 D0
解锁电机
设置好毛笔swift/serial_ascii: VERBOSE: <- #1 M2019
swift/serial_ascii: VERBOSE: -> $1 ok
swift/serial_ascii: VERBOSE: -> @5 V1
swift/ptc_ascii: VERBOSE: report: @5 V1
g
解锁电机
swift/serial_ascii: VERBOSE: <- #2 P2220
swift/serial_ascii: VERBOSE: <- #3 M17
swift/serial_ascii: VERBOSE: <- #4 M2210 F1000 T200
swift/serial_ascii: VERBOSE: -> $2 ok X98.85 Y1.52 Z37.51
pos [98.85, 1.52, 37.51]
swift/serial_ascii: VERBOSE: -> $3 ok
swift/serial_ascii: VERBOSE: -> $4 ok
swift/serial_ascii: VERBOSE: <- #5 G0 Z57.51
------
503.0 129.0
swift/serial_ascii: VERBOSE: -> $5 ok
swift/serial_ascii: VERBOSE: <- #6 G0 X149.14999999999998 Y14.42 Z37.51
swift/serial_ascii: VERBOSE: -> $6 ok
323.0 381.0
swift/serial_ascii: VERBOSE: <- #7 G0 X131.14999999999998 Y39.620000000000005 Z37.51
swift/serial_ascii: VERBOSE: -> $7 ok
swift/serial_ascii: VERBOSE: <- #8 G0 X111.35 Y54.42 Z37.51
125.0 529.0
swift/serial_ascii: VERBOSE: -> $8 ok
swift/serial_ascii: VERBOSE: <- #9 G0 Z57.51
swift/serial_ascii: VERBOSE: -> $9 ok
------
swift/serial_ascii: VERBOSE: <- #10 G0 X146.85 Y20.22 Z37.51
480.0 187.0
swift/serial_ascii: VERBOSE: -> $10 ok
750.0 442.0
swift/serial_ascii: VERBOSE: <- #11 G0 X173.85 Y45.720000000000006 Z37.51
swift/serial_ascii: VERBOSE: -> $11 ok
955.0 473.0
swift/serial_ascii: VERBOSE: <- #12 G0 X194.35 Y48.82 Z37.51
swift/serial_ascii: VERBOSE: -> $12 ok
swift/serial_ascii: VERBOSE: <- #13 G0 Z57.51
swift/serial_ascii: VERBOSE: -> $13 ok
------
swift/serial_ascii: VERBOSE: <- #14 G0 X148.14999999999998 Y40.32 Z37.51
493.0 388.0
swift/serial_ascii: VERBOSE: -> $14 ok
swift/serial_ascii: VERBOSE: <- #15 G0 X148.64999999999998 Y82.82 Z37.51
498.0 813.0
swift/serial_ascii: VERBOSE: -> $15 ok
swift/serial_ascii: VERBOSE: <- #16 G0 Z57.51
swift/serial_ascii: VERBOSE: -> $16 ok
swift/serial_ascii: VERBOSE: <- #17 M17
重置机械臂
swift/serial_ascii: VERBOSE: <- #18 M2210 F1000 T200
swift/serial_ascii: VERBOSE: <- #19 G0 X103 Y0 Z42 F800
swift/serial_ascii: VERBOSE: -> $17 ok
swift/serial_ascii: VERBOSE: -> $18 ok
swift/serial_ascii: VERBOSE: -> $19 ok
swift/pump: DEBUG: set value: off
swift/serial_ascii: VERBOSE: <- #20 M2231 V0
swift/serial_ascii: VERBOSE: -> $20 ok
swift/serial_ascii: VERBOSE: <- #21 P2231
swift/serial_ascii: VERBOSE: -> $21 ok V0
swift/gripper: DEBUG: set value: off
swift/serial_ascii: VERBOSE: <- #22 M2232 V0
swift/serial_ascii: VERBOSE: -> $22 ok
swift/serial_ascii: VERBOSE: <- #23 P2232
swift/serial_ascii: VERBOSE: -> $23 ok V0

Process finished with exit code 0

'''

for y in x.split('\n'):
    if 'G0' in y:
        z = y.split('G0')
        print('G0 ' + ' '.join(z[1:]))
