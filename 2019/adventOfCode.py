
# pylint: disable=unused-import
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
# pylint: enable=unused-import

# pylint: disable=W0611
# pylint: disable=C0413
FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "\\..\\")
from common.utils import execute_day, read_input
# pylint: enable=W0611
# pylint: enable=C0413

""" DAY 1 """
def day1_1(data):
    return data

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
