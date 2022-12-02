# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2022
DAY = 2
EXPECTED_1 = 15
EXPECTED_2 = 12


""" DAY 2 """

def day2_parse(data):
    plays = []
    for line in data:
        other, me = line.split(" ")
        plays.append((me, other))
    return plays

def day2_1(data):
    data = day2_parse(data)
    score = 0
    for me, other in data:
        if me == "X":
            score += 1
        elif me == "Y":
            score += 2
        else:
            score += 3

        if (me == "X" and other == "A") or \
           (me == "Y" and other == "B") or \
           (me == "Z" and other == "C"):
            score += 3
        elif (me == "X" and other == "C") or \
             (me == "Y" and other == "A") or \
             (me == "Z" and other == "B"):
            score += 6

    return score

def day2_2(data):
    data = day2_parse(data)
    score = 0
    for me, other in data:
        if me == "X":
            score += 0
        elif me == "Y":
            score += 3
        else:
            score += 6

        if other == "A":
            if me == "X":
                score += 3
            elif me == "Y":
                score += 1
            else:
                score += 2
        elif other == "B":
            if me == "X":
                score += 1
            elif me == "Y":
                score += 2
            else:
                score += 3
        elif other == "C":
            if me == "X":
                score += 2
            elif me == "Y":
                score += 3
            else:
                score += 1

    return score


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
