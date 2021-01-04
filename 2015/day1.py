# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys
FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
# pylint: enable=wrong-import-position

def day1_1(data):
    floor = 0
    for c in data[0]:
        if c == "(":
            floor += 1
        elif c == ")":
            floor -= 1
        else:
            assert False, c
    return floor

def day1_2(data):
    floor = 0
    i = 0
    for c in data[0]:
        i += 1
        if c == "(":
            floor += 1
        elif c == ")":
            floor -= 1
        else:
            assert False, c
        if floor == -1:
            return i
    assert False
    return None


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2015)
