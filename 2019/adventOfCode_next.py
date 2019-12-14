# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=wrong-import-position
import time
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

WHITE_SQUARE = "█"

def day15_parse_input(data):
    return data

def day15_1(data):
    # data = read_input(2019, 1401)
    data = day15_parse_input(data)
    return None

def day15_2(data):
    # data = read_input(2019, 1401)
    data = day15_parse_input(data)
    return None

# IntCode logic:
# def int_run(insts, inputs):
#     def calculate_input():
#         return 0
#     pc = 0
#     rel_base = 0
#     outputs = []
#     while insts[pc] != 99:
#         op = insts[pc]
#         (pc, insts, rel_base) = day2_execute(
#             op, pc, insts, inputs, outputs, rel_base, calculate_input)
#     return outputs

""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2019)
