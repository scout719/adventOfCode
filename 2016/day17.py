# -*- coding: utf-8 -*-
from collections import deque
from hashlib import md5
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2016
DAY = 17
EXPECTED_1 = "DDRRRD"
EXPECTED_2 = 370

def day17_parse(data: list[str]):
    return data[0]

def day17_doors(passcode: str) -> dict[tuple[int, int], tuple[bool, str]]:
    digest = md5(passcode.encode()).hexdigest()
    return {
        (-1, 0): (digest[0] in "bcdef", "U"),
        (1, 0): (digest[1] in "bcdef", "D"),
        (0, -1): (digest[2] in "bcdef", "L"),
        (0, 1): (digest[3] in "bcdef", "R")
    }

def day17_solve(data, part2):
    data = day17_parse(data)
    passcode = data
    R, C = 4, 4
    er, ec = R - 1, C - 1
    q = deque()
    q.append((0, 0, ""))
    seen = set()
    paths = set()
    while q:
        r, c, path = q.popleft()

        if (r, c, path) in seen:
            continue
        seen.add((r, c, path))

        if (r, c) == (er, ec):
            if not part2:
                return path
            paths.add(path)
            continue

        for (dr, dc), (opened, move) in day17_doors(passcode + path).items():
            rr, cc = r + dr, c + dc
            if not opened or not (0 <= rr < R and 0 <= cc < C):
                continue
            q.append((rr, cc, path + move))
    return max(len(p) for p in paths)

def day17_1(data):
    return day17_solve(data, False)

def day17_2(data):
    return day17_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
