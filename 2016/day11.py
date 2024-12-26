# -*- coding: utf-8 -*-
from collections import defaultdict, deque
from copy import deepcopy
from heapq import heappop, heappush
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2016
DAY = 11
EXPECTED_1 = 11
EXPECTED_2 = 30

def day11_parse(data: list[str]):
    floors = [[] for _ in range(4)]
    for i, line in enumerate(data):
        # The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
        # The fourth floor contains nothing relevant.
        parts = line.split("contains ")[1].split(", ")
        if "nothing relevant" in parts[0]:
            continue
        floors[i].extend(part.strip("and a").strip(".").replace("-compatible", "")
                         for part in parts)

    return floors

def day11_can_leave(obj: str, floor: int, floors: list[list[str]]):
    if obj.endswith("microchip"):
        return True
    assert obj.endswith("generator")
    typ = obj.split(" ")[0]
    return not f"{typ} microchip" in floors[floor] or \
        all(obj2 == obj or obj2.endswith("microchip")
            for obj2 in floors[floor])

def day11_can_enter(obj: str, floor: int, floors: list[list[str]]):
    # can't enter if it would fry another chip
    if obj.endswith("generator"):
        return True
    assert obj.endswith("microchip")
    typ = obj.split(" ")[0]
    return f"{typ} generator" in floors[floor] or \
        not any(obj2.endswith("microchip") for obj2 in floors[floor])

def day11_compatible(obj1: str, obj2: str):
    
    return obj1.endswith("generator") or obj2.endswith("generator")

def day11_same_type(obj1: str, obj2: str):
    typ1 = obj1.split(" ")[0]
    typ2 = obj2.split(" ")[0]
    if typ1 == typ2:
        assert obj1.endswith("generator") and obj2.endswith("microchip") or \
            obj2.endswith("generator") and obj1.endswith("microchip")
    return typ1 == typ2

def day11_cost(floors):
    return 0
    ans = 0
    for i, objs in enumerate(floors):
        ans += (3 - i) * len(objs)
    return ans

def day11_validate(floors):
    for objs in floors:
        for obj1 in objs:
            if obj1.endswith("generator"):
                continue
            for obj2 in objs:
                if obj1 == obj2:
                    continue

                if day11_same_type(obj1, obj2):
                    continue

                if obj1.endswith("generator"):
                    continue

                typ1 = obj1.split(" ")[0]
                typ2 = obj2.split(" ")[0]
                if not (f"{typ1} generator" in objs or
                        f"{typ2} generator" in objs):
                    assert False

def day11_solve(data, part2):
    data = day11_parse(data)
    floors = data
    total = sum(len(floor) for floor in floors)
    q: list[tuple[int, int, int, list[list[str]]]
            ] = [(day11_cost(floors), 0, 0, deepcopy(floors))]
    while q:
        _, cost, e, floors = heappop(q)
        if len(floors[-1]) == total:
            return cost

        for delta in [-1, 1]:
            new_e = e + delta
            if 0 <= new_e < 4:
                el = (day11_cost(floors), cost +
                      1, new_e, deepcopy(floors))
                heappush(q, el)
                for i, obj1 in enumerate(floors[e]):
                    if day11_can_leave(obj1, e, floors) and day11_can_enter(obj1, new_e, floors):
                        new_floors = deepcopy(floors)
                        new_floors[new_e].append(obj1)
                        new_floors[e].remove(obj1)
                        el = (day11_cost(new_floors),
                              cost + 1, new_e, new_floors)
                        day11_validate(new_floors)
                        heappush(q, el)
                    for j, obj2 in enumerate(floors[e]):
                        if j <= i:
                            continue
                        if not day11_compatible(obj1, obj2):
                            continue

                        assert obj1 != obj2

                        if day11_same_type(obj1, obj2) or \
                            (day11_can_leave(obj1, e, floors) and day11_can_enter(obj1, new_e, floors) and
                             day11_can_leave(obj2, e, floors) and day11_can_enter(obj2, new_e, floors)):
                            new_floors = deepcopy(floors)
                            new_floors[new_e].append(obj1)
                            new_floors[new_e].append(obj2)
                            new_floors[e].remove(obj1)
                            new_floors[e].remove(obj2)
                            el = (day11_cost(new_floors),
                                  cost + 1, new_e, new_floors)
                            day11_validate(new_floors)
                            heappush(q, el)

    assert False

def day11_1(data):
    # wrong 23
    # wrong 21
    return day11_solve(data, False)

def day11_2(data):
    return day11_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
