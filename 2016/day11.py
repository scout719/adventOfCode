# -*- coding: utf-8 -*-
from collections import deque
from copy import deepcopy
import functools
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
EXPECTED_2 = None

def day11_parse(data: list[str]):
    floors: list[list[tuple[int, bool]]] = [[] for _ in range(4)]
    types = {}
    counter = 0
    for i, line in enumerate(data):
        # The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
        # The fourth floor contains nothing relevant.
        parts = line.split("contains ")[1].split(", ")
        if "nothing relevant" in parts[0]:
            continue

        for part in parts:
            typ, kind = part.strip("and a").strip(
                ".").replace("-compatible", "").split(" ")
            if typ not in types:
                types[typ] = counter
                counter += 1
            floors[i].append((types[typ], kind == "generator"))

    return floors

@functools.cache
def day11_can_enter(obj: tuple[str, str], floor: tuple[tuple[int, bool]]):
    typ, is_generator = obj
    # can't enter if it would fry another chip
    if is_generator:
        for obj2_typ, obj2_is_generator in floor:
            if not obj2_is_generator and \
               obj2_typ != typ and \
               (obj2_typ, True) not in floor:
                return False
        return True
    assert not is_generator
    for obj2_typ, obj2_is_generator in floor:
        if obj2_is_generator and \
           obj2_typ != typ and \
           (typ, True) not in floor:
            return False
    return True

def day11_validate(floor):
    return day11_validate_aux(tuple(floor))

@functools.cache
def day11_validate_aux(floor):
    for obj1 in floor:
        if not day11_can_enter(obj1, floor):
            return False
    return True

def day11_solve(data, part2):
    data = day11_parse(data)
    floors = data
    if part2:
        max_typ = max(max(typ for typ, _ in floor)
                      for floor in floors if len(floor) > 0)
        floors[0] += [(max_typ + 1, True), (max_typ + 1, False),
                      (max_typ + 2, True), (max_typ + 2, False)]
        assert day11_validate(floors[0]) and day11_validate(floors[1]) and \
            day11_validate(floors[2]) and day11_validate(floors[3])
    total = sum(len(floor) for floor in floors)
    q: deque[tuple[int, int, list[list[tuple[int, bool]]]]] = \
        deque([(0, 0, deepcopy(floors))])
    seen = set()
    while q:
        cost, e, floors = q.popleft()
        if len(floors[-1]) == total:
            return cost

        state = (e, tuple(tuple(sorted(objs)) for objs in floors))
        if state in seen:
            continue
        seen.add(state)

        for delta in [-1, 1]:
            new_e = e + delta
            if 0 <= new_e < 4:
                for i, obj1 in enumerate(floors[e]):
                    new_floors = [list(floor)
                                  for floor in floors]
                    new_floors[new_e].append(obj1)
                    new_floors[e].remove(obj1)
                    if day11_validate(new_floors[new_e]) and day11_validate(new_floors[e]):
                        el = (cost + 1, new_e, new_floors)
                        q.append(el)
                    j = i + 1
                    while j < len(floors[e]):
                        obj2 = floors[e][j]
                        j += 1

                        assert obj1 != obj2

                        new_floors = [list(floor)
                                      for floor in floors]
                        new_floors[new_e].append(obj1)
                        new_floors[new_e].append(obj2)
                        new_floors[e].remove(obj1)
                        new_floors[e].remove(obj2)
                        if not day11_validate(new_floors[new_e]) or not day11_validate(new_floors[e]):
                            continue
                        el = (cost + 1, new_e, new_floors)
                        q.append(el)
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
