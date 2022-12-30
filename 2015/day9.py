# -*- coding: utf-8 -*-
import os
import sys
from collections import defaultdict
from heapq import heappop, heappush

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2015
DAY = 9
EXPECTED_1 = None
EXPECTED_2 = None


""" DAY 9 """

def day9_parse(data):
    edges = defaultdict(list)
    for line in data:
        words = line.split()
        edges[words[0]].append((words[2], int(words[4])))
        edges[words[2]].append((words[0], int(words[4])))
    return edges

def day9_1(data):
    edges = day9_parse(data)
    q = []
    for key in edges.keys():
        q.append((0, key, [key]))
    while q:
        cost, curr, path = heappop(q)
        if len(path) == len(edges):
            return cost
        for (dest, cost2) in edges[curr]:
            if dest in path:
                continue
            heappush(q, (cost + cost2, dest, list(path) + [dest]))
    assert False

def day9_2(data):
    edges = day9_parse(data)
    q = []
    for key in edges.keys():
        q.append((0, key, [key]))
    best = 0
    while q:
        cost, curr, path = heappop(q)
        if len(path) == len(edges):
            if cost < best:
                best = cost
            continue
        for (dest, cost2) in edges[curr]:
            if dest in path:
                continue
            heappush(q, (cost - cost2, dest, list(path) + [dest]))
    return -best


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
