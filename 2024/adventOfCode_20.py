# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import deque
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402


YEAR = 2024
DAY = 20
EXPECTED_1 = None
EXPECTED_2 = 285

def day20_parse(data: list[str]):
    return data

def day20_t_to(walls, D, er, ec):
    to_target = {}
    q = deque([(0, er, ec)])
    while q:
        t, r, c = q.popleft()
        if (r, c) in to_target:
            continue
        to_target[(r, c)] = t

        for dr, dc in D:
            rr, cc = r + dr, c + dc
            if (rr, cc) not in walls:
                q.append((t + 1, rr, cc))
    return to_target

def day20_get_cheats(R, C, walls, D, max_cheat_t):
    cheats = set()
    for r in range(R):
        for c in range(C):
            if (r, c) in walls:
                continue

            q = deque([(0, r, c)])
            seen = set()
            while q:
                t, rr, cc = q.popleft()
                if t > max_cheat_t:
                    continue
                if (rr, cc) in seen:
                    continue
                seen.add((rr, cc))

                if (rr, cc) not in walls and (rr, cc) != (r, c):
                    cheats.add((r, c, rr, cc, t))

                for dr, dc in D:
                    rrr, ccc = rr + dr, cc + dc
                    if 0 <= rrr < R and 0 <= ccc < C:
                        q.append((t + 1, rrr, ccc))
    return cheats

def day20_solve(data, part2):
    data = day20_parse(data)
    walls = set()
    R = len(data)
    C = len(data[0])
    sr, sc = 0, 0
    er, ec = 0, 0
    for r in range(R):
        for c in range(C):
            p = data[r][c]
            if p == "#":
                walls.add((r, c))
            elif p == "S":
                sr, sc = r, c
            elif p == "E":
                er, ec = r, c
            else:
                assert p == "."

    D = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    to_end = day20_t_to(walls, D, er, ec)
    from_start = day20_t_to(walls, D, sr, sc)

    max_cheat_t = 20 if part2 else 2
    cheats = day20_get_cheats(R, C, walls, D, max_cheat_t)

    target = 50 if R == 15 else 100
    best = to_end[(sr, sc)]
    ans = 0
    for r, c, rr, cc, t in cheats:
        t_from_start = from_start[(r, c)]
        t_to_end = to_end[(rr, cc)]
        total = t_from_start + t + t_to_end
        if total < best and (best - total >= target):
            ans += 1
    return ans

def day20_1(data):
    return day20_solve(data, False)

def day20_2(data):
    return day20_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
