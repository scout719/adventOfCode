# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402


YEAR = 2024
DAY = 23
EXPECTED_1 = 7
EXPECTED_2 = "co,de,ka,ta"

def day23_parse(data: list[str]):
    E = defaultdict(set)
    for line in data:
        a, b = line.split("-")
        E[a].add(b)
        E[b].add(a)
    return E

def day23_solve(data, part2):
    data = day23_parse(data)
    conns = data
    comps = conns.keys()

    q = [([c]) for c in comps]
    groups = set()
    while q:
        group = q.pop()

        group_s = tuple(sorted(group))
        if group_s in groups:
            continue
        groups.add(group_s)

        for comp in group:
            for adj in conns[comp]:
                if all(comp2 in conns[adj] for comp2 in group if comp2 != comp):
                    q.append(group + [adj])
    if not part2:
        return len([1 for group in groups
                    if (len(group) == 3) and any(comp.startswith("t") for comp in group)])

    best = 0
    best_group = set()
    for group in groups:
        if len(group) > best:
            best = len(group)
            best_group = group
    return ",".join(best_group)

def day23_1(data):
    return day23_solve(data, False)

def day23_2(data):
    return day23_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
