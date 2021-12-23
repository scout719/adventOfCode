# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
from typing import Callable, Iterator, Union, Optional, List, ChainMap
import functools
import math
import os
from os.path import join
import sys
import time
from copy import deepcopy
from collections import Counter, defaultdict, deque
from heapq import heappop, heappush

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import read_input, main, clear  # NOQA: E402
from common.utils import day_with_validation, bcolors, WHITE_CIRCLE, WHITE_SQUARE  # NOQA: E402
from common.utils import BLUE_CIRCLE, RED_SMALL_SQUARE  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2021
DAY = 23
EXPECTED_1 = 12521  # 474140
EXPECTED_2 = 44169  # 2758514936282235


""" DAY 23 """

def day23_parse(data):
    return data

def day23_energy(c):
    E = {
        "A": 1,
        "B": 10,
        "C": 100,
        "D": 1000
    }
    return E[c]

def day23_room(c):
    E = {
        "A": 3,
        "B": 5,
        "C": 7,
        "D": 9
    }
    return E[c]

def day23_limits(rows):
    m = []
    for r in range(1, rows + 2):
        for c in range(1, 12):
            if r == 1 or c in [3, 5, 7, 9]:
                m.append((r, c))
    return m

def day23_heuristic(positions, limits, rows):
    reverse_positions = {}
    for char, p in positions.items():
        for v1 in p:
            reverse_positions[v1] = char
    remaining = 0
    for r, c in limits:
        if (r, c) in reverse_positions:
            char = reverse_positions[(r, c)]
            energy = day23_energy(char)
            if day23_room(char) != c:
                # effort to move to halway
                remaining += abs(r - 1) * energy
                # effort to move to correct room
                remaining += abs(day23_room(char) - c) * energy
                # effort to go to the back of room
                remaining += 2 * energy
            else:
                # effort to go to the back of room
                remaining += abs(rows + 1 - r) * energy
    return remaining

def day23_complete2(positions):
    return \
        all(c == 3 for _, c in positions["A"]) and \
        all(c == 5 for _, c in positions["B"]) and \
        all(c == 7 for _, c in positions["C"]) and \
        all(c == 9 for _, c in positions["D"])

def day23_move2(r, c, rr, cc, cost, occupied, rows, limits):

    D = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited = set()
    q = [(r, c, 0)]
    while q:
        rrr, ccc, e = heappop(q)
        if rrr == rr and ccc == cc:
            return e
        if (rrr, ccc) in visited:
            continue
        visited.add((rrr, ccc))
        for dr, dc in D:
            rrrr, cccc = rrr + dr, ccc + dc
            if (rrrr, cccc) in limits and (rrrr, cccc) not in occupied:
                heappush(q, (rrrr, cccc, e + cost))

    return 0

def day23_print2(positions, rows):
    B = [
        "#############",
        "#...........#",
        "###.#.#.#.###",
        "  #.#.#.#.#",
        "  #########"
    ]

    B2 = B[:3]
    for _ in range(rows - 2):
        B2.append("  #.#.#.#.#")
    B2 += B[3:]
    B = B2

    reverse_pos = {}
    for char in positions:
        for r, c in positions[char]:
            reverse_pos[(r, c)] = char
    for r in range(len(B)):
        row = ""
        for c in range(len(B[r])):
            if (r, c) in reverse_pos:
                row += reverse_pos[(r, c)]
            else:
                row += B[r][c]
        print(row)
    print()

def day23_solve3(positions_, rows, limits):
    hallway = [
        (1, 1),
        (1, 2),
        (1, 4),
        (1, 6),
        (1, 8),
        (1, 10),
        (1, 11)
    ]

    counter = 0
    q = [(day23_heuristic(positions_, limits, rows), 0, counter, [(0, 0)])]
    visited2 = {}
    costs = None
    states = {}
    states[counter] = positions_
    counter += 1
    while q:
        _, e2, new_pos_arr, path = heappop(q)
        new_pos = states[new_pos_arr]
        if day23_complete2(new_pos):
            # count = 0
            # for i, e in path:
            #     count += e
            #     print("Cost to reach following state:", e, "Total cost", count)
            #     day23_print2(states[i], rows)
            return e2
        if costs is not None and e2 >= costs:
            continue
        key = (tuple(sorted(new_pos["A"])), tuple(sorted(new_pos["B"])),
               tuple(sorted(new_pos["C"])), tuple(sorted(new_pos["D"])))
        if key in visited2 and visited2[key] <= e2:
            continue
        visited2[key] = e2
        occupied = new_pos["A"] + new_pos["B"] + \
            new_pos["C"] + new_pos["D"]

        reverse_pos = {}
        for char, p in new_pos.items():
            for v1 in p:
                reverse_pos[v1] = char

        for char in new_pos:
            for r, c in new_pos[char]:
                room = day23_room(char)
                if r != 1:  # in a room
                    # wrong room or blocking other
                    blocking = False
                    for rrr in range(r + 1, rows + 2):
                        blocking |= (rrr, c) in reverse_pos and day23_room(
                            reverse_pos[(rrr, c)]) != c
                    if room != c or blocking:
                        for rr, cc in hallway:  # try to move to hallway
                            e = day23_move2(
                                r, c, rr, cc, day23_energy(char), occupied, rows, limits)
                            if e != 0:
                                new_pos2 = deepcopy(new_pos)
                                new_pos2[char].remove((r, c))
                                new_pos2[char].append((rr, cc))
                                states[counter] = new_pos2
                                counter += 1
                                heappush(
                                    q, (day23_heuristic(positions_, limits, rows) + e2 + e, e2 + e, counter - 1, path + [(counter - 1, e)]))
                else:  # in hallway
                    added = False
                    for rr in range(rows + 1, 1, -1):
                        if added:
                            break
                        cc = room  # try to move to room
                        # if we don't block
                        blocking = False
                        for rrr in range(rr + 1, rows + 2):
                            blocking |= ((rrr, cc) in reverse_pos and day23_room(
                                reverse_pos[(rrr, cc)]) != cc)
                        if not blocking:
                            e = day23_move2(
                                r, c, rr, cc, day23_energy(char), occupied, rows, limits)
                            if e != 0:
                                new_pos2 = deepcopy(new_pos)
                                new_pos2[char].remove((r, c))
                                new_pos2[char].append((rr, cc))
                                states[counter] = new_pos2
                                counter += 1
                                heappush(
                                    q, (day23_heuristic(positions_, limits, rows) + e2 + e, e2 + e, counter - 1, path + [(counter - 1, e)]))
                                added = True
                                break  # moved to back of room
    assert False

def day23_1(data):
    data = day23_parse(data)
    positions = defaultdict(list)
    for r in range(len(data)):
        for c in range(len(data[r])):
            char = data[r][c]
            if char in "ABCD":
                positions[char].append((r, c))

    limits = day23_limits(2)
    return day23_solve3(positions, 2, limits)

def day23_2(data):
    data = day23_parse(data)
    positions = defaultdict(list)
    data2 = data[:3]
    data2.append("  #D#C#B#A#")
    data2.append("  #D#B#A#C#")
    data2 += data[3:]
    for r in range(len(data2)):
        for c in range(len(data2[r])):
            char = data2[r][c]
            if char in "ABCD":
                positions[char].append((r, c))

    limits = day23_limits(4)
    return day23_solve3(positions, 4, limits)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
