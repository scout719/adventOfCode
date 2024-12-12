# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2024
DAY = 12
EXPECTED_1 = 1184
EXPECTED_2 = 368

def day12_parse(data: list[str]):
    grid = [["_" for _ in range(len(data[0]) + 2)]]
    for line in data:
        grid_line = ["_"]
        for c in line:
            grid_line.append(c)
        grid_line.append("_")
        grid.append(grid_line)
    grid.append(["_" for _ in range(len(data[0]) + 2)])
    return grid

def day12_print(R, C, points, ch):
    for r in range(R):
        line = ""
        for c in range(C):
            if (r, c) in points:
                line += ch
            else:
                line += "."
        print(line)
    print()

def day12_solve(data, part2):
    data = day12_parse(data)
    R = len(data)
    C = len(data[0])
    D = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited = set((r, c) for r in range(R)
                  for c in range(C) if data[r][c] != "_")
    regions = []
    while visited:
        r, c = visited.pop()
        q = [(r, c)]
        typ = data[r][c]
        seen = set()
        while q:
            rr, cc = q.pop()
            if (rr, cc) in seen:
                continue
            seen.add((rr, cc))
            for dr, dc in D:
                rrr, ccc = rr + dr, cc + dc
                if data[rrr][ccc] == typ:
                    q.append((rrr, ccc))
        visited -= seen
        regions.append(seen)

    ans = 0
    for region in regions:
        area = len(region)
        fence = []
        typ = None
        fence2 = set()
        points = set()
        points2 = []
        for r, c in region:
            typ = data[r][c]

            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dc == dr == 0:
                        continue

                    rr, cc = r + dr, c + dc
                    # Is diag?
                    if dr != 0 and dc != 0:
                        # Cross section
                        # ......
                        # ...BB.
                        # ...BB.  L__ this corner needs to be accounted for as well
                        # .BB...
                        # .BB...
                        # ......
                        if (rr, cc) in region and ((r, cc) not in region and (rr, c) not in region):
                            fr = min(rr, r) + (max(rr, r) - min(r, rr)) / 2
                            fc = min(cc, c) + (max(cc, c) - min(c, cc)) / 2
                            fence2.add((fr, fc))
                            points.add((fr, fc))

                    if (rr, cc) not in region:
                        fr = min(rr, r) + (max(rr, r) - min(r, rr)) / 2
                        fc = min(cc, c) + (max(cc, c) - min(c, cc)) / 2
                        fence2.add((fr, fc))

            for dr, dc in D:
                rr, cc = r + dr, c + dc
                if data[rr][cc] != data[r][c]:
                    fence.append((rr, cc))

        new_fence2 = set()
        # keep only corners
        for fr, fc in fence2:
            if fr % 1 != 0:
                if (fr - 0.5, fc) in fence2 and (fr + 0.5, fc) in fence2:
                    continue
            if fc % 1 != 0:
                if (fr, fc - 0.5) in fence2 and (fr, fc + 0.5) in fence2:
                    continue
            if fr % 1 == 0 or fc % 1 == 0:
                continue
            new_fence2.add((fr, fc))
        # if part2:
            # print(typ, fence2)
            # day12_print(R * 2, C * 2, list((r * 2 // 1, c * 2 // 1)
            #             for r, c in fence2), "X")
            # day12_print(R * 2, C * 2, list((r * 2 // 1, c * 2 // 1)
            #             for r, c in new_fence2), "X")
            # day12_print(R * 2, C * 2, list((r * 2 // 1, c * 2 // 1)
            #             for r, c in points), "X")
        fence2 = new_fence2
        if part2:
            ans += area * (len(fence2) + len(points) * 2)
        else:
            ans += area * len(fence)
    return ans

def day12_1(data):
    return day12_solve(data, False)

def day12_2(data):
    # 833998 low
    return day12_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
