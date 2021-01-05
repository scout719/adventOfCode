# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
# pylint: enable=wrong-import-position

def day8_count(line):
    code = len(line)
    line = line[1:-1]
    mem = 0
    i = 0
    while i < len(line):
        if line[i] == "\\":
            if line[i + 1] in ["\"", "\\"]:
                i += 1
            else:
                assert line[i + 1] == "x"
                i += 3
        mem += 1
        i += 1
    return code, mem

def day8_count_reverse(line):
    code = len(line)
    mem = 2
    i = 0
    while i < len(line):
        if line[i] in ["\\", "\""]:
            mem += 2
        else:
            mem += 1
        i += 1
    return code, mem

def day8_1(data):
    total_code = 0
    total_mem = 0
    for line in data:
        code, mem = day8_count(line)
        total_code += code
        total_mem += mem

    return total_code - total_mem

def day8_2(data):
    total_code = 0
    total_mem = 0
    for line in data:
        code, mem = day8_count_reverse(line)
        total_code += code
        total_mem += mem

    return total_mem - total_code


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2015)
