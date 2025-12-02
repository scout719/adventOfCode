# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2025
DAY = 2
EXPECTED_1 = 1227775554
EXPECTED_2 = 4174379265

def day2_parse(data: list[str]):
    ranges = data[0].split(",")
    return [(int(r.split("-")[0]), int(r.split("-")[1])) for r in ranges]

def day2_valid(id_, part2):
    id_sz = len(id_)
    if not part2:
        if id_sz % 2 != 0:
            return True
        mid = id_sz // 2
        return id_[0:mid] != id_[mid:]

    for sz in range(1, id_sz):
        if id_sz % sz != 0:
            continue
        curr = id_[0:sz]
        i = sz
        invalid = True
        while i + sz <= id_sz:
            next_ = id_[i:i + sz]
            i = i + sz
            if curr != next_:
                invalid = False
                break
        if invalid:
            return False

    return True

def day2_solve(data, part2):
    ranges = day2_parse(data)

    total = 0
    for start, end in ranges:
        for i in range(start, end + 1):
            if not day2_valid(str(i), part2):
                total += i
    return total

def day2_1(data):
    return day2_solve(data, False)

def day2_2(data):
    return day2_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
