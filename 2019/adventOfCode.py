# pylint: disable=unused-import
# pylint: disable=import-error
# pylint: disable=wrong-import-position
import functools
import math
import multiprocessing as mp
import os
import re
import string
import sys
import time
from collections import Counter, deque
import heapq
from enum import Enum
from struct import pack

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "\\..\\")
sys.path.insert(0, FILE_DIR + "\\..\\..\\")
from common.utils import execute_day  # NOQA: E402
# pylint: enable=unused-import
# pylint: enable=import-error
# pylint: enable=wrong-import-position

""" DAY 1 """

def day1_calc_fuel(mod):
    return math.floor(mod / 3) - 2

def day1_1(data):
    return functools.reduce(lambda a, v: a+v, [day1_calc_fuel(int(m)) for m in data])

def day1_2(data):
    total = 0
    for mod_s in data:
        mod = int(mod_s)
        temp_fuel = day1_calc_fuel(mod)
        while temp_fuel > 0:
            total += temp_fuel
            temp_fuel = day1_calc_fuel(temp_fuel)
    return total

""" MAIN FUNCTION """

def main(specific_day):
    initial_day = 1
    end_day = 25
    if specific_day is not None:
        initial_day = specific_day
        end_day = specific_day

    for day in range(initial_day, end_day + 1):
        execute_day(globals(), 2019, day, 1)
        execute_day(globals(), 2019, day, 2)

if __name__ == "__main__":
    start_day = None
    if len(sys.argv) > 1:
        try:
            if len(sys.argv) > 2:
                raise ValueError
            start_day = int(sys.argv[1])
        except ValueError:
            print("Usage: adventOfCode.py [<day>]")
            sys.exit(1)
    main(start_day)
