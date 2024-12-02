# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict
from email.policy import default
import os
import sys
from typing import Counter, List

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2024
DAY = 2
EXPECTED_1 = 2
EXPECTED_2 = 4


""" DAY 2 """

def day2_parse(data):
    reports = []
    for l in data:
        reports.append([int(x) for x in l.split()])
    return reports

def day2_test(r, idx):
    i = 1
    prev = r[0]
    diff = r[1] - prev
    if diff == 0:
        return False
    signal = diff / abs(diff)
    safe = signal != 0
    while safe and i < len(r):
        curr_diff = r[i] - prev
        curr_dist = abs(curr_diff)
        if not 1 <= curr_dist <= 3:
            safe = False
            break
        curr_signal = curr_diff / curr_dist

        safe = curr_signal == signal
        prev = r[i]
        i += 1
    return safe


def day2_1(data):
    reports = day2_parse(data)
    c = 0
    for r in reports:
        if day2_test(r, None):
            c += 1
    return c

def day2_2(data):
    reports = day2_parse(data)
    c = 0
    for r in reports:
        if day2_test(r, None):
            c += 1
        else:
            for i in range(len(r)):
                r2 = r[:i] + r[i + 1:]
                if day2_test(r2, None):
                    c += 1
                    break
    return c


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
