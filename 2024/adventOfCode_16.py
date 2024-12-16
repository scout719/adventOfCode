# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from heapq import heappop, heappush
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import RED_SMALL_SQUARE, main  # NOQA: E402
from common.utils import day_with_validation, WHITE_SQUARE, BLUE_CIRCLE  # NOQA: E402


YEAR = 2024
DAY = 16
EXPECTED_1 = 11048  # 7036
EXPECTED_2 = 64  # 45

def day16_parse(data: list[str]):
    return data

def day16_print(rr, cc, walls, path):
    R = max(r for r, _ in walls) + 1
    C = max(c for _, c in walls) + 1
    show = ""
    for r in range(R):
        line = ""
        for c in range(C):
            if (r, c) in walls:
                line += WHITE_SQUARE
            elif r == rr and c == cc:
                line += RED_SMALL_SQUARE
            elif (r, c) in path:
                line += BLUE_CIRCLE
            else:
                line += " "
        show += line + "\n"
    print(show)
    sys.stdout.flush()

def day16_solve(data, part2):
    data = day16_parse(data)
    grid = data
    R = len(grid)
    C = len(grid[0])
    start_r, start_c = 0, 0
    end_r, end_c = 0, 0
    walls = set()
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "S":
                start_r, start_c = r, c
            elif grid[r][c] == "E":
                end_r, end_c = r, c
            elif grid[r][c] == "#":
                walls.add((r, c))
            else:
                assert grid[r][c] == "."

    ROTATIONS = {
        (0, -1): [(1, 0), (-1, 0)],
        (0, 1): [(1, 0), (-1, 0)],
        (-1, 0): [(0, 1), (0, -1)],
        (1, 0): [(0, 1), (0, -1)],
    }

    SCORE = {}

    q = [(abs(end_r - start_r) + abs(end_c - start_c),
          0, start_r, start_c, 0, 1, set())]
    tiles = set()
    best = 1e9
    while q:
        _, score, r, c, dr, dc, path = heappop(q)
        key = (r, c, dr, dc)
        if key in SCORE and SCORE[key] < score:
            continue
        SCORE[key] = score

        if (r, c) == (end_r, end_c):
            if not part2:
                return score
            best = min(best, score)
            if score > best:
                continue
            tiles |= path
            continue

        succ = [(r + dr, c + dc, dr, dc, 1)]
        for drr, dcc in ROTATIONS[(dr, dc)]:
            succ.append((r + drr, c + dcc, drr, dcc, 1001))

        for rr, cc, drr, dcc, cost in succ:
            if (rr, cc) in walls:
                continue

            el = (abs(end_r - rr) + abs(end_c - cc) + score + cost,
                  score + cost, rr, cc, drr, dcc, path | {(r, c)})
            heappush(q, el)

    return len(tiles) + 1

def day16_1(data):
    return day16_solve(data, False)

def day16_2(data):
    return day16_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
