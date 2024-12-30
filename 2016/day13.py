# -*- coding: utf-8 -*-
from collections import deque
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import BLUE_CIRCLE, WHITE_SQUARE, main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2016
DAY = 13
EXPECTED_1 = None
EXPECTED_2 = None

def day13_parse(data: list[str]):
    return int(data[0])

def day13_wall(r, c, fav):
    x, y = c, r
    value = x * x + 3 * x + 2 * x * y + y + y * y
    value += fav
    cnt = 0
    while value != 0:
        cnt += value & 1
        value = value >> 1
    return cnt % 2 == 1

def day13_print(seen, fav):
    R = max(r for r, _ in seen)
    C = max(c for r, c in seen)
    for r in range(R):
        line = ""
        for c in range(C):
            if (r, c) in seen:
                assert not day13_wall(r, c, fav)
                line += BLUE_CIRCLE
            elif day13_wall(r, c, fav):
                assert (r, c) not in seen
                line += WHITE_SQUARE
            else:
                line += " "
        print(line)
    print()

def day13_solve(data, part2):
    data = day13_parse(data)
    fav_number = data
    er, ec = 39, 31

    # fav_number = 10
    # er, ec = 4, 7

    r, c = 1, 1
    q: deque[tuple[int, int, int]] = deque([(0, 1, 1)])
    seen = set()
    while q:
        cost, r, c = q.popleft()
        if (r, c) in seen:
            continue
        seen.add((r, c))

        if not part2 and (r, c) == (er, ec):
            return cost

        if part2:
            if cost == 50:
                continue

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            rr, cc = r + dr, c + dc
            if rr < 0 or cc < 0 or day13_wall(rr, cc, fav_number):
                continue

            q.append((cost + 1, rr, cc))

    # day13_print(p2, fav_number)
    return len(seen)

def day13_1(data):
    # high 291
    # high 283
    return day13_solve(data, False)

def day13_2(data):
    return day13_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
