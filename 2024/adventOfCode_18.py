# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import deque
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import RED_SMALL_SQUARE, main  # NOQA: E402
from common.utils import day_with_validation, WHITE_SQUARE, BLUE_CIRCLE  # NOQA: E402


YEAR = 2024
DAY = 18
EXPECTED_1 = 22
EXPECTED_2 = "6,1"

def day18_parse(data: list[str]):
    return [(int(line.split(",")[0]), int(line.split(",")[1])) for line in data]

def day18_print(rr, cc, walls, path):
    R = max(r for r, _ in walls) + 1
    C = max(c for _, c in walls) + 1
    show = ""
    for r in range(R):
        line = ""
        for c in range(C):
            if (r, c) in walls:
                line += WHITE_SQUARE
            elif r == rr and c == cc:
                line += RED_SMALL_SQUARE
            elif (r, c) in path:
                line += BLUE_CIRCLE
            else:
                line += " "
        show += line + "\n"
    print(show)
    sys.stdout.flush()

def day18_steps(n_bytes, X, Y):
    sx, sy = 0, 0
    ex, ey = X - 1, Y - 1
    seen = set()
    q = deque([(0, sx, sy)])
    D = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while q:
        steps, x, y = q.popleft()
        if (x, y) == (ex, ey):
            return steps

        if (x, y) in seen:
            continue
        seen.add((x, y))
        for dx, dy in D:
            xx, yy = x + dx, y + dy
            if 0 <= xx < X and 0 <= yy < Y and not (x, y) in n_bytes:
                q.append((steps + 1, xx, yy))
    return None

def day18_solve(data, part2):
    data = day18_parse(data)
    _bytes = data
    X, Y = 71, 71
    n = 1024
    if _bytes[0] == (5, 4):
        X, Y = 7, 7
        n = 12

    if not part2:
        return day18_steps(_bytes[:n], X, Y)

    lo = 1
    hi = len(_bytes) - 1
    while lo != hi - 1:
        mid = lo + (hi - lo) // 2
        steps = day18_steps(_bytes[:mid], X, Y)
        if steps is None:
            hi = mid
        else:
            lo = mid

    assert day18_steps(_bytes[:lo], X, Y) is not None
    assert day18_steps(_bytes[:hi], X, Y) is None
    x, y = _bytes[lo]
    return f"{x},{y}"

def day18_1(data):
    return day18_solve(data, False)

def day18_2(data):
    return day18_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
