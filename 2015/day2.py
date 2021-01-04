# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys
FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
# pylint: enable=wrong-import-position

def day2_parse(data):
    return [[int(d) for d in line.split("x")] for line in data]

def day2_1(data):
    dims = day2_parse(data)
    ans = 0
    for l, w, h in dims:
        ans += 2 * l * w + 2 * w * h + 2 * h * \
            l + min(l * w, min(w * h, h * l))
    return ans

def day2_2(data):
    dims = day2_parse(data)
    ans = 0
    for l, w, h in dims:
        side1 = l * 2 + w * 2
        side2 = w * 2 + h * 2
        side3 = h * 2 + l * 2
        ans += min(side1, min(side2, side3)) + l * w * h
    return ans


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2015)
