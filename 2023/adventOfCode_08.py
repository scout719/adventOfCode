# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from math import lcm
import os
import sys
from typing import List, Mapping, Tuple

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2023
DAY = 8
EXPECTED_1 = None
EXPECTED_2 = 6

""" DAY 8 """

def day8_parse(data: List[str]):
    inst = data[0]
    M: Mapping[str, List[str]] = {}
    for line in data[2:]:
        orig, dest = line.split(" = ")
        dest = dest.replace("(", "")
        dest = dest.replace(")", "")
        dest = dest.split(", ")
        M[orig] = dest
    return inst, M

def day8_next(curr_dir, M, s) -> str:
    if curr_dir == "L":
        return M[s][0]
    else:
        assert curr_dir == "R"
        return M[s][1]

def day8_1(data: List[str]):
    inst, M = day8_parse(data)
    node = "AAA"
    curr_i = 0
    count = 0
    while node != "ZZZ":
        count += 1
        curr_dir = inst[curr_i]
        curr_i = (curr_i + 1) % len(inst)
        node = day8_next(curr_dir, M, node)

    return count

def day8_cycle(inst, M, node):
    seen: Mapping[Tuple[int, str], int] = {}
    path: List[str] = [node]
    curr_i = 0
    count = 0
    while True:
        curr_dir = inst[curr_i]
        curr_i = (curr_i + 1) % len(inst)
        count += 1
        node = day8_next(curr_dir, M, node)
        k = (curr_i, node)
        if k in seen:
            # find the position on path where the loop starts
            return len(path) - path.index(node)
        path += [node]
        seen[k] = count

def day8_2(data: List[str]):
    # 23147 low
    # 23519 low
    inst, M = day8_parse(data)
    starts: List[str] = []
    for node in M:
        if node.endswith("A"):
            starts.append(node)

    cycles = []
    for start in starts:
        cycles.append(day8_cycle(inst, M, start))

    return lcm(*cycles)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
