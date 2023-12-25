# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys
from typing import List

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2023
DAY = 9
EXPECTED_1 = 114
EXPECTED_2 = 2


""" DAY 9 """

def day9_parse(data: List[str]):
    return [[int(x) for x in line.split()] for line in data]

def day9_predict(hist, part2):
    s = [hist]
    while set(s[-1]) != {0}:
        n_s = []
        c_s = s[-1]
        for i in range(len(c_s) - 1):
            n_s.append(c_s[i + 1] - c_s[i])
        s.append(n_s)

    i = len(s) - 1
    while i > 0:
        c_d = s[i - 1]
        if part2:
            s[i - 1] = [c_d[0] - s[i][0]] + c_d
        else:
            c_d.append(c_d[-1] + s[i][-1])
        i -= 1
    return s[0][0] if part2 else s[0][-1]

def day9_solve(hists, part2):
    ans = 0
    for hist in hists:
        ans += day9_predict(hist, part2)
    return ans

def day9_1(data: List[str]):
    hists = day9_parse(data)
    # low 1901217886
    return day9_solve(hists, False)

def day9_2(data: List[str]):
    hists = day9_parse(data)
    return day9_solve(hists, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
