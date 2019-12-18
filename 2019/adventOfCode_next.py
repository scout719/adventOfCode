# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=wrong-import-position
# from _heapq import *
# from _collections import defaultdict
# import time
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
print(FILE_DIR)
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
sys.path.insert(0, FILE_DIR + "/../../")
from common.utils import read_input, main, clear  # NOQA: E402
from icComputer import ic_execute  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

WHITE_SQUARE = "█"
WHITE_CIRCLE = "•"
BLUE_CIRCLE = f"{bcolors.OKBLUE}{bcolors.BOLD}•{bcolors.ENDC}"
RED_SMALL_SQUARE = f"{bcolors.FAIL}{bcolors.BOLD}■{bcolors.ENDC}"

def day19_parse_input(data):
    return [int(d) for d in data[0].split(",")]

def day19_1(data):
    #data = read_input(2019, 1901)
    data = day19_parse_input(data)
    output = int_run_19(data, [])
    return output

def day19_2(data):
    #data = read_input(2019, 1901)
    data = day19_parse_input(data)
    output = int_run_19(data, [])
    return output

# IntCode logic:
def int_run_19(insts, inputs, calculate_input=None):
    insts = [insts[i] if i < len(insts) else 0 for i in range(10000)]
    pc = 0
    rel_base = 0
    outputs = []
    while insts[pc] != 99:
        op = insts[pc]
        (pc, insts, rel_base) = ic_execute(
            op, pc, insts, inputs, outputs, rel_base, calculate_input)
    return outputs

""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2019)