# -*- coding: utf-8 -*-
# @Time    : 2017/7/26 23:02
# @Author  : play4fun
# @File    : utils.py
# @Software: PyCharm

"""
utils.py:
"""
import string

import random


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))