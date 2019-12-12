# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=wrong-import-position
import os
import sys
from icComputer import ic_execute

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
print(FILE_DIR)
sys.path.insert(0, FILE_DIR + "/../")
sys.path.insert(0, FILE_DIR + "/../../")
from common.utils import read_input, main, clear  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

WHITE_SQUARE = "█"

# IntCode logic:
# def ic_run(insts, inputs):
#     pc = 0
#     rel_base = 0
#     outputs = []
#     while insts[pc] != 99:
#         op = insts[pc]
#         (pc, insts, rel_base) = ic_execute(
#             op, pc, insts, inputs, outputs, rel_base)
#     return outputs

""" MAIN FUNCTION """

def day13_1(data):
    pass

if __name__ == "__main__":
    main(sys.argv, globals(), 2019)
