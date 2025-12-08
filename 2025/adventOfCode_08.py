# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict
from heapq import heappop, heappush
from math import sqrt
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2025
DAY = 8
EXPECTED_1 = 40
EXPECTED_2 = 25272

def day8_parse(data: list[str]):
    boxes = []
    for line in data:
        x, y, z = line.split(",")
        x = int(x)
        y = int(y)
        z = int(z)
        boxes.append((x, y, z))
    return boxes

def day8_solve(data, part2):
    boxes = day8_parse(data)

    # For part2 we want to connect them all
    max_connections = 1000 if not part2 else sys.maxsize
    if len(boxes) == 20:
        max_connections = 10 if not part2 else sys.maxsize

    dists_heap = []
    seen = set()
    for x, y, z in boxes:
        for xx, yy, zz in boxes:
            if (x, y, z) == (xx, yy, zz) or (x, y, z, xx, yy, zz) in seen:
                continue
            seen.add((xx, yy, zz, x, y, z))
            dist = sqrt(
                (xx - x) * (xx - x) + (yy - y) * (yy - y) + (zz - z) * (zz - z))
            heappush(dists_heap, (dist, (x, y, z), (xx, yy, zz)))

    groups: list[set[tuple[int, int, int]]] = []
    seen = set()
    groups_reverse = defaultdict(int)

    connection_made = 0
    while dists_heap and connection_made < max_connections:
        connection_made += 1
        _, box1, box2 = heappop(dists_heap)
        if box1 in seen and box2 in seen:
            if groups_reverse[box1] != groups_reverse[box2]:
                # join groups
                left = groups_reverse[box1]
                right = groups_reverse[box2]
                for box3 in groups[right]:
                    groups_reverse[box3] = left
                groups[left] = groups[left].union(groups[right])
                groups[right].clear()

        never_seen = not (box1 in seen or box2 in seen)
        seen.add(box1)
        seen.add(box2)

        if never_seen:
            groups_reverse[box1] = len(groups)
            groups_reverse[box2] = len(groups)
            groups.append(set([box1, box2]))

        for i, group in enumerate(groups):
            if box1 in group:
                groups_reverse[box2] = i
                group.add(box2)
                break
            if box2 in group:
                groups_reverse[box1] = i
                group.add(box1)
                break

        if part2:
            if any(len(boxes) == len(group) for group in groups):
                return box1[0] * box2[0]

    total = 1
    for sz in sorted(groups, key=lambda g: -len(g))[0:3]:
        total *= len(sz)
    return total

def day8_1(data):
    return day8_solve(data, False)

def day8_2(data):
    return day8_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
