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
DAY = 6
EXPECTED_1 = 4277556
EXPECTED_2 = 3263827

def day6_parse(data: list[str]):
    F = {
        '+': lambda a, b: a + b,
        '*': lambda a, b: a * b,
    }
    ops = []
    # Store in which column does every number start
    # so that we can properly extract it with the respective padding
    starts = []
    for i, c in enumerate(data[-1]):
        if c != " ":
            starts.append(i - 1)
            ops.append(F[c])
        i += 1

    eqs = [[] for _ in range(len(ops))]
    for line in data[:-1]:
        curr = ""
        nums = []
        for j, c in enumerate(line):
            if j in starts:
                nums.append(curr)
                curr = ""
            else:
                curr += c
        nums.append(curr)

        for i, n in enumerate(nums):
            eqs[i].append(n)

    return eqs, ops

def day6_solve(data, part2):
    eqs, ops = day6_parse(data)
    total = 0
    for i, op in enumerate(ops):
        curr_eqs = eqs[i]
        if not part2:
            curr_eqs = [int(n) for n in eqs[i]]
        else:
            max_width = max(len(n) for n in curr_eqs)
            new_eqs = [0 for _ in range(max_width)]
            for i in range(max_width):
                curr_n = 0
                for n in curr_eqs:
                    if n[max_width - i - 1] == " ":
                        continue
                    curr_n *= 10
                    d = int(n[max_width - i - 1])
                    curr_n += d
                new_eqs[i] = curr_n
            curr_eqs = new_eqs

        curr = curr_eqs[0]
        for n in curr_eqs[1:]:
            curr = op(curr, n)
        total += curr

    return total

def day6_1(data):
    return day6_solve(data, False)

def day6_2(data):
    return day6_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
