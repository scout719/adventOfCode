# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import deque
import functools
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402


YEAR = 2024
DAY = 21
EXPECTED_1 = 126384
EXPECTED_2 = None  # 285

def day21_parse(data: list[str]):
    return data

@functools.cache
def day21_path_to_key(pad_str: str, r, c, er, ec):
    pad = pad_str.split("\n")
    D = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    R, C = len(pad), len(pad[0])
    DR = {
        (-1, 0): "^",
        (1, 0): "v",
        (0, -1): "<",
        (0, 1): ">"
    }

    q = deque()
    q.append((0, r, c, []))
    seen = {}
    possibilities: list[list[str]] = []
    best = 1e9
    while q:
        steps, rr, cc, moves = q.popleft()
        if best != 1e9 and steps > best:
            continue
        if (rr, cc) == (er, ec):
            possibilities.append(moves + ["A"])
            best = steps
            continue
        if (rr, cc) in seen and seen[(rr, cc)] > steps:
            continue
        seen[(rr, cc)] = steps

        for dr, dc in D:
            rrr, ccc = rr + dr, cc + dc
            if 0 <= rrr < R and 0 <= ccc < C and pad[rrr][ccc] != "X":
                q.append((steps + 1, rrr, ccc, moves + [DR[(dr, dc)]]))
    return possibilities

@functools.cache
def day21_moves_arrow(moves_: str, i, robots) -> int:
    pad = [
        ['X', '^', 'A'],
        ['<', 'v', '>']]
    pad_str = "\n".join("".join(line) for line in pad)
    R = 2
    C = 3
    pos = {}
    for r in range(R):
        for c in range(C):
            pos[pad[r][c]] = (r, c)

    r, c = pos["A"]
    moves_n = 0
    for m in moves_:
        tr, tc = pos[m]
        m2 = day21_path_to_key(pad_str, r, c, tr, tc)
        best = len(m2[0]) if i == robots else day21_moves_arrow(
            "".join(m2[0]), i + 1, robots)
        if i != robots:
            for m_ in m2:
                x = day21_moves_arrow("".join(m_), i + 1, robots)
                if x < best:
                    best = x
        moves_n += best
        r, c, = tr, tc
        assert pad[r][c] != "X"
        assert pad[r][c] == m
    return moves_n

def day21_moves_num(code, robots) -> int:
    pad = [
        ['7', '8', '9'],
        ['4', '5', '6'],
        ['1', '2', '3'],
        ['X', '0', 'A']]
    pad_str = "\n".join("".join(line) for line in pad)
    R = 4
    C = 3
    pos = {}
    for r in range(R):
        for c in range(C):
            pos[pad[r][c]] = (r, c)

    r, c = pos["A"]
    moves_n = 0
    for k in code:
        tr, tc = pos[k]
        m2 = day21_path_to_key(pad_str, r, c, tr, tc)
        best = day21_moves_arrow("".join(m2[0]), 1, robots)
        for m_ in m2:
            x = day21_moves_arrow("".join(m_), 1, robots)
            if x < best:
                best = x
        moves_n += best
        r, c, = tr, tc
        assert pad[r][c] != "X"
        assert pad[r][c] == k
    return moves_n

def day21_solve(data, part2):
    data = day21_parse(data)
    codes = data
    ans = 0
    for code in codes:
        moves = day21_moves_num(code, 25 if part2 else 2)
        ans += moves * int(code[:-1])
    return ans

def day21_1(data):
    # 239088 high
    return day21_solve(data, False)

def day21_2(data):
    # 12976000000000 low
    return day21_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
