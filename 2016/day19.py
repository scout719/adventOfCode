# -*- coding: utf-8 -*-
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2016
DAY = 19
EXPECTED_1 = 53
EXPECTED_2 = 73

def day19_parse(data: list[str]):
    return int(data[0])

def day19_solve_naive(n_elves):
    line = [i + 1 for i in range(n_elves)]
    presents = {i + 1: 1 for i in range(n_elves)}

    i = 0
    while len(line) > 1:
        next_i = (i + 1) % len(line)
        curr = line[i]
        next_ = line[next_i]
        presents[curr] += presents[next_]
        presents[next_] = 0
        line.pop(next_i)
        if next_i < i:
            i -= 1
        i = (i + 1) % len(line)

    return line[0]

def day19_print(n_elves, line):
    line_str = ""
    for elf in range(1, n_elves + 1):
        if elf in line:
            line_str += f"{elf:3d}"
        else:
            line_str += "   "
    print(line_str)

def day19_solve_part2_naive(n_elves):
    line = [i + 1 for i in range(n_elves)]
    presents = {i + 1: 1 for i in range(n_elves)}

    i = 0
    while len(line) > 1:
        next_i = (i + len(line) // 2) % len(line)
        curr = line[i]
        next_ = line[next_i]
        presents[curr] += presents[next_]
        presents[next_] = 0
        line.pop(next_i)
        if next_i < i:
            i -= 1
        i = (i + 1) % len(line)

    return line[0]

def day19_solve(data, part2):
    data = day19_parse(data)
    n_elves = data

    if part2:
        # Find highest power of 3 below target
        power = 3
        while power < n_elves:
            power *= 3
        # step 1 back
        power //= 3

        # starting on the power,
        # count up until we reach the power value
        # then do jumps of 2
        curr = power
        res = 1
        while curr < n_elves - 1:
            if res < power:
                res += 1
            else:
                res += 2
            curr += 1
        # assert res == day19_solve_part2_naive(n_elves)
        return res
        # Print pattern
        # for i in range(1, 250):
        #     print(i, "=>", day19_solve_part2_naive(i))

    # 1,  29  step: 2 if step by step reaches hi, lo = lo + step and step *= 2
    # 3,  27  step: 4 if step by step not reach hi, hi = new hi and step *= 2
    # 3,  27  step: 8
    # 11, 27  step: 16
    # 27

    lo = 1
    hi = n_elves
    step = 2
    while lo != hi:
        if (hi - lo) % step == 0:
            lo = lo + step
        else:
            hi = lo + ((hi - lo) // step) * step
        step *= 2

    return lo

def day19_1(data):
    return day19_solve(data, False)

def day19_2(data):
    return day19_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
