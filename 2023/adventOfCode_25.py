# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import Counter, defaultdict, deque
from copy import deepcopy
from heapq import heappop, heappush
from math import lcm
import os
import sys
import z3

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import WHITE_SQUARE, day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2023
DAY = 25
EXPECTED_1 = 54
EXPECTED_2 = None

""" DAY 25 """

def day25_parse(data: list[str]):
    E = defaultdict(set)
    for line in data:
        left, right = line.split(": ")
        right = right.split(" ")
        for c in right:
            E[left].add(c)
            E[c].add(left)
    return E

def day25_reach(E, c, skip):
    q = deque([c])
    seen = set()
    while q:
        curr = q.popleft()
        if curr in seen:
            continue
        seen.add(curr)
        for c in E[curr]:
            if c not in seen and c != skip:
                q.append(c)
    return len(seen)

def day25_graphviz(E):
    print("""strict graph ip_map {
    fontname="Helvetica,Arial,sans-serif"
    node [fontname="Helvetica,Arial,sans-serif"]
    edge [fontname="Helvetica,Arial,sans-serif"]
 """)
    for e, l in E.items():
        for c in l:
            print(f"""
    {e} -- {c} [label=\"{e}-{c}\"]""", end="")
    print()
    print("}")

def day25_1(data):
    E = day25_parse(data)
    total = len(E.keys())

    # day25_graphviz(E)

    E = sorted(E.items(), key=lambda e: len(e[1]))

    # Evenly distribute nodes across both sides
    in_left = {k: i % 2 == 0 for i, (k, _) in enumerate(E)}

    # Move nodes across sides minimizing the edges
    # crossing the boundary
    fixed = False
    while not fixed:
        fixed = True
        for origin, edges in E:
            nodes_across = sum(in_left[origin] != in_left[dest]
                               for dest in edges)
            if nodes_across > 1:
                # We should only stop once we only
                # have 1 edge across the boundary
                fixed = False
                in_left[origin] = not in_left[origin]

    in_left_count = sum(in_left.values())
    # We can't end up with all nodes in one side
    assert 0 < in_left_count < total
    return in_left_count * (total - in_left_count)

def day25_2(_: list[str]):
    return "Merry Xmas!"


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
