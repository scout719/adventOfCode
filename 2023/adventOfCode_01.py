# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys
from typing import List

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2023
DAY = 1
EXPECTED_1 = None
EXPECTED_2 = 281


""" DAY 1 """

def day1_parse(data) -> List[str]:
    return data

def day1_1(data: List[str]):
    data = day1_parse(data)
    total = 0
    for line in data:
        curr = ""
        for c in line:
            if c.isdigit():
                curr += c
                break
        for c in reversed(line):
            if c.isdigit():
                curr += c
                break
        total += int(curr)

    return total

def day1_get(val: str) -> str:
    mapping = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    sub = ""
    for c in val:
        sub = sub + c
        if sub in mapping:
            return mapping[sub]

    sub = ""
    for c in reversed(val):
        sub = c + sub
        if sub in mapping:
            return mapping[sub]

    return None

def day1_2(data):
    data = day1_parse(data)
    total = 0
    for line in data:
        curr = ""
        curr_n = ""
        for c in line:
            if c.isdigit():
                curr += c
                break
            curr_n += c
            v = day1_get(curr_n)
            if v is not None:
                curr += v
                break
        curr_n = ""
        for c in reversed(line):
            if c.isdigit():
                curr += c
                break
            curr_n = c + curr_n
            v = day1_get(curr_n)
            if v is not None:
                curr += v
                break
        print(curr)
        total += int(curr if curr != "" else "0")

    return total


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
