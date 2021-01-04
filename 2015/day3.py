# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys
FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
# pylint: enable=wrong-import-position

def day3_1(data):
    pos = set([(0, 0)])
    x, y = 0, 0
    D = {
        "^": (0, -1),
        ">": (1, 0),
        "<": (-1, 0),
        "v": (0, 1)
    }
    for dir_ in data[0]:
        dx, dy = D[dir_]
        x, y = x + dx, y + dy
        pos.add((x, y))
    return len(pos)

def day3_2(data):
    pos = set([(0, 0)])
    x, y = 0, 0
    D = {
        "^": (0, -1),
        ">": (1, 0),
        "<": (-1, 0),
        "v": (0, 1)
    }
    curr_state = [(0, 0), (0, 0)]
    i = 0
    for dir_ in data[0]:
        x, y = curr_state[i]
        dx, dy = D[dir_]
        x, y = x + dx, y + dy
        curr_state[i] = (x, y)
        pos.add((x, y))
        i = (i + 1) % 2
    return len(pos)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2015)
