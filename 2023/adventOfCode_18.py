# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2023
DAY = 18
EXPECTED_1 = 62
EXPECTED_2 = -1

""" DAY 18 """

def day18_parse(data: list[str]):
    plan = []
    for line in data:
        dir_, meters, color = line.split(" ")
        meters = int(meters)
        color = color.lstrip("(").rstrip(")")
        plan.append((dir_, meters, color))
    return plan

def day18_inside(cubes, r, c):
    if (r, c) in cubes:
        return True

    min_r = min(r for r, c in cubes)

    print(r, c, end=" ")
    inside = False
    while r >= min_r:
        if (r, c) in cubes:
            inside = not inside
            while (r, c) in cubes:
                r -= 1
        else:
            r -= 1
    print(inside)
    return inside

def day18_show(cubes):
    min_r = min(r for r, c in cubes)
    max_r = max(r for r, c in cubes)
    min_c = min(c for r, c in cubes)
    max_c = max(c for r, c in cubes)
    for r in range(min_r, max_r + 1):
        line = ""
        for c in range(min_c, max_c + 1):
            if (r, c) in cubes:
                line += "#"
            else:
                line += "."
        print(line)


def day18_solve(plan, part2):
    cubes = set()
    by_r = defaultdict(set)
    by_c = defaultdict(set)
    cubes.add((0, 0))
    by_r[0].add(0)
    by_c[0].add(0)
    r, c = (0, 0)
    for dir_, meters, _ in plan:
        # r, c = curr
        if dir_ == "U":
            dr, dc = -1, 0
        elif dir_ == "R":
            dr, dc = 0, 1
        elif dir_ == "D":
            dr, dc = 1, 0
        else:
            assert dir_ == "L"
            dr, dc = 0, -1
        i = 0
        while i < meters:
            i += 1
            r, c = r + dr, c + dc
            cubes.add((r, c))
            by_r[r].add(c)
            by_c[c].add(r)

    # day18_show(cubes)

    left_top = min(cubes)
    seen = set()
    q = [(left_top[0] + 1, left_top[1] + 1)]
    while q:
        r, c = q.pop()
        k = (r, c)
        if k in seen:
            continue
        seen.add(k)
        D = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for dr, dc in D:
            rr, cc = r + dr, c + dc
            if (rr, cc) not in cubes:
                q.append((rr, cc))
    return len(cubes) + len(seen)

def day18_1(data):
    plan = day18_parse(data)
    return day18_solve(plan, False)

def day18_2(data: list[str]):
    plan = day18_parse(data)
    return day18_solve(plan, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
