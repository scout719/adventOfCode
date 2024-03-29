# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2022
DAY = 1
EXPECTED_1 = 24000
EXPECTED_2 = 45000


""" DAY 1 """

def day1_parse(data):
    elfs = []
    curr = []
    for line in data:
        if line == "":
            elfs.append(curr)
            curr = []
        else:
            curr.append(int(line))
    elfs.append(curr)
    return elfs

def day1_1(data):
    data = day1_parse(data)
    res = [sum(elf) for elf in data]
    return max(res)

def day1_2(data):
    data = day1_parse(data)
    res = [sum(elf) for elf in data]
    res = sorted(res, reverse=True)
    return sum(res[0:3])


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
