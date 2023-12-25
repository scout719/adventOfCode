# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict
from copy import deepcopy
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2023
DAY = 22
EXPECTED_1 = 5
EXPECTED_2 = 7

""" DAY 22 """

def day22_parse(data: list[str]):
    bricks = []
    for line in data:
        a, b = line.split("~")
        a, b = tuple(int(c) for c in a.split(",")), tuple(int(c)
                                                          for c in b.split(","))
        if a > b:
            a, b = b, a
        bricks.append((a, b))
    return bricks

def day22_collapse(M, G):
    collapsed = set()
    moved = True
    while moved:
        moved = False
        for brick in sorted(M.keys(), key=lambda e: min(e[0][2], e[1][2])):
            (x1, y1, z1), (x2, y2, z2) = brick
            i = M[brick]
            zz = min(z1, z2)
            dz = 1
            while zz - dz > 0:
                clear = True
                for xx in range(x1, x2 + 1):
                    for yy in range(y1, y2 + 1):
                        k = (xx, yy, zz - dz)
                        if k in G:
                            clear = False
                            break
                    if not clear:
                        break
                if not clear:
                    break
                dz += 1

            # go back one
            dz -= 1
            if dz != 0:
                moved = True
                collapsed.add(M[brick])
                new_brick = (x1, y1, z1 - dz), (x2, y2, z2 - dz)
                # del M[brick]
                M.pop(brick)
                M[new_brick] = i
                for x in range(x1, x2 + 1):
                    for y in range(y1, y2 + 1):
                        for z in range(z1, z2 + 1):
                            k = (x, y, z)
                            # del G[k]
                            G.pop(k)

                        for z in range(z1 - dz, z2 - dz + 1):
                            k = (x, y, z)
                            G[k] = i
    return len(collapsed)

def day22_solve(bricks, part2):
    G = {}
    M = {}
    for i, brick in enumerate(bricks):
        (x1, y1, z1), (x2, y2, z2) = brick
        M[brick] = i
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    k = (x, y, z)
                    G[k] = i

    cubes = len(G.keys())
    day22_collapse(M, G)
    assert len(G.keys()) == cubes

    supports = defaultdict(set)
    supported_by = defaultdict(set)
    for brick, i in M.items():
        (x1, y1, z1), (x2, y2, z2) = brick
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                z = min(z1, z2)
                k = (x, y, z - 1)
                if k in G:
                    supports[G[k]].add(i)
                    supported_by[i].add(G[k])
    ans = 0
    not_needed = set()
    for _, i in M.items():
        if all(len(supported_by[b]) > 1 for b in supports[i]):
            ans += 1
            not_needed.add(i)
    if not part2:
        # high 712
        return ans

    collapsed = 0
    for i in set(M.values()).difference(not_needed):
        M2 = deepcopy(M)
        G2 = deepcopy(G)
        brick = None
        for k, v in M.items():
            if v == i:
                brick = k
                break
        assert brick, i
        M2.pop(brick)
        (x1, y1, z1), (x2, y2, z2) = brick
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    k = (x, y, z)
                    G2.pop(k)
        collapsed += day22_collapse(M2, G2)

    return collapsed

def day22_1(data):
    x = day22_parse(data)
    return day22_solve(x, False)

def day22_2(data: list[str]):
    x = day22_parse(data)
    return day22_solve(x, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
