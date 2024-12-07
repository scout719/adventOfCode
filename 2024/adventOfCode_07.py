# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2024
DAY = 7
EXPECTED_1 = 3749
EXPECTED_2 = 11387


""" DAY 7 """

def day7_parse(data: list[str]):
    eqs = []
    for l in data:
        parts = l.split(" ")
        left, right = parts[0].strip(":"), parts[1:]
        eqs.append((int(left), [int(r) for r in right]))
    return eqs

def day7_recurse(acc, right, i, target, part2):
    if i == len(right):
        yield acc
    elif acc > target:
        return []
    else:
        yield from day7_recurse(acc + right[i], right, i + 1, target, part2)
        yield from day7_recurse(acc * right[i], right, i + 1, target, part2)
        if part2:
            yield from day7_recurse(int(str(acc) + str(right[i])), right, i + 1, target, part2)


def day7_solve(data, part2):
    data = day7_parse(data)
    ans = 0
    for left, right in data:
        for r in day7_recurse(right[0], right, 1, left, part2):
            if left == r:
                ans += left
                break
    return ans

def day7_1(data):
    return day7_solve(data, False)

def day7_2(data):
    return day7_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
