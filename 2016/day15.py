# -*- coding: utf-8 -*-
import os
import re
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2016
DAY = 15
EXPECTED_1 = 5
EXPECTED_2 = None

def day15_parse(data: list[str]):
    # Disc #1 has 5 positions; at time=0, it is at position 4.
    discs = [(0, 0) for _ in range(len(data))]
    for line in data:
        m = re.match(
            r"Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).", line)
        if m is not None:
            i, n_pos, pos = m.groups()
            discs[int(i) - 1] = (int(n_pos), int(pos))
        else:
            assert False, line
    return discs

def day15_solve(data, part2):
    data = day15_parse(data)
    discs = data
    if part2:
        discs.append((11, 0))
    for t in range(int(1e9)):
        success = True
        for i, (n_pos, pos) in enumerate(discs, 1):
            if (pos + t + i) % n_pos != 0:
                success = False
                break
        if success:
            return t
    assert False

def day15_1(data):
    return day15_solve(data, False)

def day15_2(data):
    return day15_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
