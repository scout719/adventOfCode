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
from common.utils import day_with_validation # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2022
DAY = 2
EXPECTED_1 = 15
EXPECTED_2 = 12


""" DAY 1 """

def day2_parse(data):
    strat = []
    for line in data:
        other, mine = line.split(" ")
        strat.append((ord(other) - ord('A'), ord(mine) - ord("X")))
    return strat

def day2_1(data):
    data = day2_parse(data)
    score = 0
    for other, mine in data:
        # type of hand (0 base index)
        score += mine + 1

        # outcome
        # 0 -> loss
        # 1 -> draw
        # 2 -> win
        outcome = ((mine - other) + 1) % 3
        score += outcome * 3
    return score

def day2_2(data):
    data = day2_parse(data)
    score = 0
    for other, outcome in data:
        # outcome
        score += outcome * 3

        # convert from 0, 1, 2 to -1, 0, 1
        # -1 -> loss
        #  0 -> draw
        #  1 -> win
        delta = outcome - 1
        # type of hand
        score += (other + delta) % 3
        # convert to 1 base index
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
