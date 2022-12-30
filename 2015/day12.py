# -*- coding: utf-8 -*-
import os
import sys
import json

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2015
DAY = 12
EXPECTED_1 = None
EXPECTED_2 = None


""" DAY 12 """

def day12_parse(data):
    return data[0]

def day12_sum(obj, p2):
    if isinstance(obj, int):
        return obj
    if isinstance(obj, str):
        return 0
    if isinstance(obj, list):
        return sum(day12_sum(child, p2) for child in obj)
    if isinstance(obj, dict):
        if p2 and ("red" in obj.values()):
            return 0
        else:
            return sum(day12_sum(obj[child], p2) for child in obj)


def day12_1(data):
    data = day12_parse(data)
    obj = json.loads(data)
    return day12_sum(obj, False)

def day12_2(data):
    data = day12_parse(data)
    obj = json.loads(data)
    return day12_sum(obj, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
