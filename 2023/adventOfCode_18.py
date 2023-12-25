# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
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
EXPECTED_2 = 952408144115

""" DAY 18 """

def day18_parse(data: list[str]):
    plan = []
    for line in data:
        dir_, meters, color = line.split(" ")
        meters = int(meters)
        color = color.lstrip("(").rstrip(")")
        plan.append((dir_, meters, color))
    return plan

def day18_show(cubes):
    min_r = min(r for r, _ in cubes)
    max_r = max(r for r, _ in cubes)
    min_c = min(c for _, c in cubes)
    max_c = max(c for _, c in cubes)
    for r in range(min_r, max_r + 1):
        line = ""
        for c in range(min_c, max_c + 1):
            if (r, c) in cubes:
                line += "#"
            else:
                line += "."
        print(line)

def day18_get_delta(dir_):
    if dir_ == "U":
        dr, dc = -1, 0
    elif dir_ == "R":
        dr, dc = 0, 1
    elif dir_ == "D":
        dr, dc = 1, 0
    else:
        assert dir_ == "L"
        dr, dc = 0, -1
    return dr, dc

def day18_solve(plan, _):
    cubes = set()
    cubes.add((0, 0))
    r, c = (0, 0)
    for dir_, meters, _ in plan:
        dr, dc = day18_get_delta(dir_)
        i = 0
        while i < meters:
            i += 1
            r, c = r + dr, c + dc
            cubes.add((r, c))

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

    DIRS = {"0": "R", "1": "D", "2": "L", "3": "U"}
    lines = []
    r, c = (0, 0)
    for _, _, color in plan:
        color = color.lstrip("#")
        meters = int(color[:-1], base=16)
        dir_ = DIRS[color[-1]]

        dr, dc = day18_get_delta(dir_)

        rr, cc = r + dr * meters, c + dc * meters
        new_r, new_c = rr, cc
        if rr < r:
            r, rr = rr, r
        if cc < c:
            c, cc = cc, c
        lines.append((r, c, rr, cc))
        r, c = new_r, new_c

    min_r = min(r for r, c, _, _ in lines)
    min_c = min(c for r, c, _, _ in lines)

    all_c = sorted({c for _, c, _, cc in lines if c == cc})
    points = set()
    area = 0
    prev_c = min_c
    for c in all_c:
        assert len(points) % 2 == 0, f"{points} {c=} {prev_c=}"

        # vertical lines on this column
        ver_lines = sorted([(rr, rrr)
                           for rr, cc, rrr, ccc in lines if c == cc == ccc])
        starts: set[int] = {rr for rr, cc, rrr,
                            _ in lines if cc == c and rr == rrr}
        ends: set[int] = {rr for rrr, _, rr,
                          cc in lines if cc == c and rr == rrr}
        assert len(starts.intersection(ends)) == 0

        new_points = points
        prev_r = min_r - 1
        sort_points = sorted(points)
        i = 0
        while i < len(sort_points) - 1:
            a = sort_points[i]
            b = sort_points[i + 1]
            i += 2

            assert a not in starts
            assert b not in starts
            # Add area from previous step
            area += (b + 1 - a) * (c - prev_c)

            for rr, rrr in ver_lines:
                assert rr < rrr
                if rr == prev_r and rrr == a:
                    # line 'joins' last section with this one, so remove a
                    new_points.remove(a)
                elif rr == a and rrr == b:
                    # line ends this section, remove both
                    new_points.remove(a)
                    new_points.remove(b)
                    # add area from this column
                    area += (b + 1 - a)
                elif rr <= prev_r:
                    # already processed
                    pass
                elif prev_r < rr < rrr < a:
                    # outside, new section stating
                    new_points.add(rr)
                    new_points.add(rrr)
                elif rr < rrr == a:
                    # expanding current section upwards
                    new_points.add(rr)
                    new_points.remove(a)
                elif a == rr < rrr:
                    # shrinking current section downwards
                    new_points.add(rrr)
                    new_points.remove(a)
                    # add shrunk area from this column
                    area += (rrr - a)
                elif a < rr < rrr < b:
                    # inside cutting
                    new_points.add(rr)
                    new_points.add(rrr)
                    # add line cut from this column
                    area += (rrr - (rr + 1))
                elif rr < rrr == b:
                    # shrinking current section upwards
                    new_points.add(rr)
                    new_points.remove(b)
                    # add shrunk area from this column
                    area += (b - rr)
                elif b == rr < rrr:
                    # expanding current section downwards
                    new_points.add(rrr)
                    new_points.remove(b)
                else:
                    assert b < rr < rrr, f"{a=} {b=} {rr=} {rrr=} {prev_r=}"
                    break

            prev_r = b
        for rr, rrr in ver_lines:
            assert rr < rrr
            if rr <= prev_r:
                # already processed
                pass
            else:
                assert prev_r < rr < rrr, f"{prev_r=} {rr=} {rrr=}"
                # outside, new section stating
                new_points.add(rr)
                new_points.add(rrr)

        points = new_points
        prev_c = c

    assert len(points) == 0, f"{points=}"
    return area


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
