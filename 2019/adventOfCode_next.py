# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=wrong-import-position
# from _heapq import *
# from _collections import defaultdict
# import time
from heapq import *
from collections import defaultdict
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

def day21_parse_input(data):
    return [int(d) for d in data[0].split(",")]

def day21_1(data):
    # data = read_input(2019, 2101)
    data = day21_parse_input(data)
    cmd = ["AND A J", "AND B T", "AND T J", "AND C T", "AND T J", "AND D J", "NOT J J", "WALK"]
    cmd = [ "NOT C T", "NOT B T", "AND T J", "NOT D T", "AND T J","NOT A T", "OR T J",  "WALK"]
    cmd2 = []
    for c in cmd:
        for c2 in c:
            cmd2.append(ord(c2))
        cmd2.append(10)
    def g_i():
        print(cmd2)
        return cmd2.pop(0)
    output = int_run_21(data, [], g_i)

    w_r = [False, False]


    return "".join([chr(o) for o in output])

def day21_2(data):
    # data = read_input(2019, 2101)
    data = day21_parse_input(data)
    return None

# IntCode logic:
def int_run_21(insts, inputs, calculate_input=None):
    insts = [insts[i] if i < len(insts) else 0 for i in range(10000)]
    pc = 0
    rel_base = 0
    outputs = []
    while not outputs or insts[pc] != 99:
        op = insts[pc]
        (pc, insts, rel_base) = ic_execute(
            op, pc, insts, inputs, outputs, rel_base, calculate_input)
    return outputs

""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2019)
