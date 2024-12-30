# -*- coding: utf-8 -*-
from collections import deque
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
DAY = 22
EXPECTED_1 = None
EXPECTED_2 = None

def day22_parse(data: list[str]):
    nodes = {}
    for line in data:
        # Filesystem              Size  Used  Avail  Use%
        res = re.match(
            r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+\d+%", line)
        if res is not None:
            x, y, size, used, available = [int(g) for g in res.groups()]
            assert used + available == size
            nodes[(x, y)] = (size, used)
    return nodes

def day22_solve(data, part2):
    data = day22_parse(data)
    nodes = data
    pairs = set()
    for i, ((x1, y1), (size1, used1)) in enumerate(nodes.items()):
        for j, ((x2, y2), (size2, used2)) in enumerate(nodes.items()):
            if j <= i:
                continue
            if 0 < used1 <= (size2 - used2):
                pairs.add((x1, y1, x2, y2))
            if 0 < used2 <= (size1 - used1):
                pairs.add((x1, y1, x2, y2))
    if not part2:
        return len(pairs)

    free_nodes = [(x, y) for (x, y), (_, used) in nodes.items() if used == 0]
    assert len(free_nodes) == 1
    free_x, free_y = free_nodes[0]

    max_x, max_y = max(x for x, _ in nodes), max(y for _, y in nodes)
    end_x, end_y = (0, 0)
    g_x, g_y = max_x, 0
    q = deque()
    q.append((0, g_x, g_y, free_x, free_y))
    seen = set()
    while q:
        steps, g_x, g_y, free_x, free_y = q.popleft()
        key = (g_x, g_y, free_x, free_y)
        if key in seen:
            continue
        seen.add(key)
        if (g_x, g_y) == (end_x, end_y):
            return steps

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            xx, yy = free_x + dx, free_y + dy
            if not (0 <= xx <= max_x and 0 <= yy <= max_y):
                continue
            if nodes[(xx, yy)][1] > nodes[(free_x, free_y)][0]:
                continue
            if (xx, yy) == (g_x, g_y):
                q.append((steps + 1, free_x, free_y, xx, yy))
            else:
                q.append((steps + 1, g_x, g_y, xx, yy))

def day22_1(data):
    return day22_solve(data, False)

def day22_2(data):
    return day22_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
