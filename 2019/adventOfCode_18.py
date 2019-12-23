# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=wrong-import-position
from timeit import default_timer as timer
import math
import itertools
from heapq import *
from _collections import defaultdict
from functools import *
import time
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
print(FILE_DIR)
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
sys.path.insert(0, FILE_DIR + "/../../")
from common.utils import read_input, main, clear  # NOQA: E402
from icComputer import ic_execute  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

WHITE_SQUARE = "█"
WHITE_CIRCLE = "•"

def day18_parse_input(data):
    return [str(d) for d in data]

def all_dist2(k, r, c, grid):
    D = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    m = []
    q = [(r, c, 0)]
    seen = {(r, c): 0}
    dists = {}
    while q:
        rr, cc, count = heappop(q)

        for d in range(0, 4):
            rrr, ccc = rr + D[d][0], cc + D[d][1]
            if not (rrr, ccc) in seen or seen[(rrr, ccc)] > count + 1:
                seen[(rrr, ccc)] = count + 1
                p = grid[rrr][ccc]
                if p == '.' or p == "@" or p == "1" or p == "2" or p == "3" or p == "4":
                    heappush(q, (rrr, ccc, count + 1))
                elif p != "#":
                    dists[p] = (rrr, ccc, count + 1)
    return dists

def n_pos2(p, grid, dists, ks):
    D = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    m = []
    q = [(p, 0)]
    seen = set([p])
    while q:
        pp, steps = q.pop()
        for ppp in dists[pp]:
            if not ppp in seen:
                seen.add(ppp)
                r, c, s = dists[pp][ppp]
                if ord('A') <= ord(ppp) <= ord('Z') and ppp.lower() in ks:
                    q.append((ppp, steps + s))
                elif ord('a') <= ord(ppp) <= ord('z'):
                    if ppp in ks:
                        q.append((ppp, steps + s))
                    else:
                        m.append((ppp, steps + s))
    return m

def day18_1(data):
    # data = read_input(2019, 1801)
    data = day18_parse_input(data)
    total_keys = {}
    grid = []
    doors = {}
    for r, row in enumerate(data):
        grid.append([])
        for c, p in enumerate(row):
            grid[r].append(p)
            if ord('a') <= ord(p) <= ord('z'):
                total_keys[p] = (r, c)
            elif ord('A') <= ord(p) <= ord('Z'):
                doors[p] = (r, c)
            elif p == '@':
                total_keys[p] = (r, c)
                start = r, c

    dists = {}
    for key in total_keys:
        r, c = total_keys[key]
        dists[key] = all_dist2(key, r, c, grid)
    for door in doors:
        r, c = doors[door]
        dists[door] = all_dist2(door, r, c, grid)

    q = [(0, "@", [])]

    min_res = None
    seen3 = {}
    total_keys_n = len(total_keys.keys()) - 1  # remove @
    seen = set()
    while q:
        steps, key, ks = heappop(q)

        k2 = tuple([steps, key, tuple(ks)])
        if k2 in seen:
            continue
        seen.add(k2)

        if total_keys_n == len(ks):
            return steps

        for other_key, s in n_pos2(key, grid, dists, ks):
            n_ks = sorted(ks + [other_key])
            k = tuple([other_key] + n_ks)
            if k in seen3 and seen3[k] < steps + s:
                continue
            seen3[k] = steps + s
            heappush(q, (steps + s, other_key, n_ks))
    return min_res

def day18_2(data):
    if len(sys.argv) > 1:
        data = read_input(2019, str(sys.argv[1]))
    data = day18_parse_input(data)
    total_keys = {}
    grid = []
    doors = {}
    for r, row in enumerate(data):
        grid.append([])
        for c, p in enumerate(row):
            grid[r].append(p)
            if ord('a') <= ord(p) <= ord('z'):
                total_keys[p] = (r, c)
            elif ord('A') <= ord(p) <= ord('Z'):
                doors[p] = (r, c)
            elif p == '@':
                start = r, c
    D = [-1, 0, 1]
    count = 1
    robots = []
    for i in range(3):
        for j in range(3):
            rr, cc = start[0] + D[i], start[1] + D[j]
            if abs(D[i]) + abs(D[j]) == 2:
                grid[rr][cc] = str(count)
                total_keys[str(count)] = (rr, cc)
                robots.append((rr, cc))
                count += 1
            else:
                grid[rr][cc] = "#"
    dists = {}
    for key in total_keys:
        r, c = total_keys[key]
        dists[key] = all_dist2(key, r, c, grid)
    for door in doors:
        r, c = doors[door]
        dists[door] = all_dist2(door, r, c, grid)
    # 1, 2
    # 3, 4

    for key in total_keys:
        r, c = total_keys[key]
        if r <= robots[0][0] and c <= robots[0][1]:
            total_keys[key] = (r, c, 1)
        if r >= robots[1][0] and c <= robots[1][1]:
            total_keys[key] = (r, c, 3)
        if r <= robots[2][0] and c >= robots[2][1]:
            total_keys[key] = (r, c, 2)
        if r >= robots[0][0] and c >= robots[0][1]:
            total_keys[key] = (r, c, 4)    
            
    q = [(0, ["1", "2", "3", "4"], [[],[],[],[]], [])]

    min_res = None
    seen3 = {}
    total_keys_n = len(total_keys.keys()) - 4  # remove @
    cc = 0
    t = 0
    seen = set()
    while q:
        steps, robots, ks_r, ks = heappop(q)
        
        k2 = tuple([steps, tuple(robots), tuple(ks_r[0]), tuple(ks_r[1]), tuple(ks_r[2]), tuple(ks_r[3])])
        if k2 in seen:
            continue
        seen.add(k2)

        # if len(seen3) > 2000:
        #     d_ks = []
        #     for k in seen3:
        #         if len(k) < len(ks)-4:
        #             d_ks.append(k)
        #     for k in d_ks:
        #         del seen3[k]
        c+=1
        if c % 10000 == 0:
            print(steps, ks, len(ks), total_keys_n, len(seen3), t)
        if total_keys_n == len(ks):
            return steps
        
        for i in range(4):
            key = robots[i]
            # start = timer()
            for other_key, s in n_pos2(key, grid, dists, ks):
                # t = (timer() - start)*1000
                n_ks = sorted(ks + [other_key])
                # n_ks2 = ks_r[i] + [other_key]
                # n_ks_r = ks_r[:]
                # n_ks_r[i] = n_ks2
                n_robots = robots[:]
                n_robots[i] = other_key
                k = tuple(n_robots + n_ks)
                if k in seen3 and seen3[k] < steps + s:
                    continue
                seen3[k] = steps + s
                #q.append((steps + s, n_robots, n_ks))
                heappush(q, (steps + s, n_robots, ks_r , n_ks))
    return min_res

""" MAIN FUNCTION """

if __name__ == "__main__":
    main([""], globals(), 2019)
