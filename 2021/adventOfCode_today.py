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
EXPECTED_2 = None  # 2758514936282235


""" DAY 23 """

def day23_parse(data):
    return data
    pos = defaultdict(list)
    for r in range(len(data)):
        for c in range(len(data[r])):
            char = data[r][c]
            if char in "ABCD":
                pos[char].append((r, c))
    return pos

def day23_complete(board):
    return board[2][3] == "A" and \
        board[3][3] == "A" and \
        board[2][5] == "B" and \
        board[3][5] == "B" and \
        board[2][7] == "C" and \
        board[3][7] == "C" and \
        board[2][9] == "D" and \
        board[3][9] == "D"
    return (2, 3) in board["A"] and \
        (3, 3) in board["A"] and \
        (2, 5) in board["B"] and \
        (3, 5) in board["B"] and \
        (2, 7) in board["C"] and \
        (3, 7) in board["C"] and \
        (2, 9) in board["D"] and \
        (3, 9) in board["D"]

def day23_is_hallway(r, _):
    return r == 1

def day23_outside_room(r, c):
    return r == 1 and c in [3, 5, 7, 9]

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

def day23_print(board):
    for row in board:
        print(row)

def day23_move(r, c, board):

    D = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    moves = []
    char = board[r][c]
    assert char in ["A", "B", "C", "D"], (char, r, c)
    # day23_print(board)
    visited = set()
    q = [(0, r, c)]
    while q:
        e, rr, cc = q.pop()
        if (rr, cc) in visited:
            continue
        visited.add((rr, cc))
        for dr, dc in D:
            rrr, ccc = rr + dr, cc + dc
            if board[rrr][ccc] == ".":
                q.append((c + day23_energy(char), rrr, ccc))

        if r != rr or c != cc:
            if r == 1 and cc == day23_room(char):  # started in hallway
                moves.append((e, rr, cc))
            else:  # started in room
                if cc not in [3, 5, 7, 9]:
                    moves.append((e, rr, cc))

    return moves

def day23_key(board):
    p = defaultdict(list)
    for r in range(len(board)):
        for c in range(len(board[r])):
            char = board[r][c]
            if char in "ABCD":
                p[char].append((r, c))
    p = {k: tuple(sorted(v)) for k, v in p.items()}
    return tuple(sorted(p.items()))

def day23_solve(data):
    # energy, active pod, board
    q = [(0, (2, 3), [[c for c in r] for r in data]),
         (0, (2, 5), [[c for c in r] for r in data]),
         (0, (2, 7), [[c for c in r] for r in data]),
         (0, (2, 9), [[c for c in r] for r in data])]

    visited = set()
    while q:
        e, (r, c), board = heappop(q)
        key = day23_key(board)
        print(key)
        if key in visited:
            continue
        visited.add(key)

        if day23_complete(board):
            return e
        for ee, rr, cc in day23_move(r, c, board):
            bb = [[c for c in r] for r in board]
            bb[rr][cc] = bb[r][c]
            bb[r][c] = "."
            print(r, c, rr, cc)
            # day23_print(bb)

            heappush(q, (e + ee, (rr, cc), bb))
    assert False

    # energy, active pod, board
    q = [(0, (2, 3), {k: v for k, v in data.items()}),
         (0, (2, 5), {k: v for k, v in data.items()}),
         (0, (2, 7), {k: v for k, v in data.items()}),
         (0, (2, 9), {k: v for k, v in data.items()})]
    while q:
        energy, (r, c), board = heappop(q)
        if day23_complete(board):
            return energy


def day23_1(data):
    data = day23_parse(data)

    return day23_solve(data)

def day23_2(data):
    data = day23_parse(data)
    return data


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
