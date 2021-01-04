# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys
import hashlib

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
# pylint: enable=wrong-import-position

def day4_solve(key, nr):
    i = 0
    while True:
        curr = (key + str(i))
        digest = hashlib.md5(curr.encode()).hexdigest()
        if digest.startswith("0" * nr):
            return i
        i += 1

def day4_1(data):
    return day4_solve(data[0], 5)

def day4_2(data):
    return day4_solve(data[0], 6)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2015)
