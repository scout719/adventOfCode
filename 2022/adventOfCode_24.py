# -*- coding: utf-8 -*-
import os
import sys

from collections import defaultdict, deque

from typing import Callable, Dict, Iterator, Union, Optional, List, ChainMap
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
# pylint: disable-next=wrong-import-position
from common.utils import main, day_with_validation, RED_SMALL_SQUARE, WHITE_SQUARE  # NOQA: E402

YEAR = 2022
DAY = 24
EXPECTED_1 = 18
EXPECTED_2 = 54

""" DAY 24 """

def day24_parse(data):
    m = defaultdict(list)
    s_c = 0
    e_c = 0
    R = len(data)
    C = len(data[0])
    for r, line in enumerate(data):
        for c, char in enumerate(line):
            if r == 0:
                if char == ".":
                    s_c = c
            if r == len(data) - 1:
                if char == ".":
                    e_c = c
            if char == "<":
                m[(r, c)].append((0, -1))
            if char == "v":
                m[(r, c)].append((1, 0))
            if char == ">":
                m[(r, c)].append((0, 1))
            if char == "^":
                m[(r, c)].append((-1, 0))
    return m, (s_c, e_c), (R, C)

def day24_print(r, c, m, R, C):
    for rr in range(R):
        line = ""
        for cc in range(C):
            if len(m[(rr, cc)]) == 0:
                if (rr, cc) == (r, c):
                    line += WHITE_SQUARE
                else:
                    if cc == 0 or cc == C-1 or \
                       rr == 0 or rr == R-1:
                        line += "#"
                    else:
                        line += " "
            elif len(m[(rr, cc)]) > 1:
                line += str(len(m[(rr, cc)]))
            else:
                dr, dc = m[(rr, cc)][0]
                line += "<" if (dr, dc) == (0, -1) else \
                    ">" if (dr, dc) == (0, 1) else \
                    "v" if (dr, dc) == (1, 0) else "^"
        print(line)
    print()

def day24_solve(t, r, c, bs_t, R, C, e_c, s_c, DP):
    if r == R - 1 and c == e_c:
        return t

    k = (r, c, t)
    if k in DP:
        return DP[k]

    if t + 1 in bs_t:
        curr_m = bs_t[t + 1]
    else:
        new_m = defaultdict(list)
        for (rr, cc), bs in bs_t[t].items():
            for dr, dc in bs:
                rrr, ccc = rr + dr, cc + dc
                if rrr == R - 1:
                    assert dr == 1
                    rrr = 1
                elif rrr == 0:
                    assert dr == -1
                    rrr = R - 2
                elif ccc == C - 1:
                    assert dc == 1
                    ccc = 1
                elif ccc == 0:
                    assert dc == -1
                    ccc = C - 2

                new_m[(rrr, ccc)].append((dr, dc))
        bs_t[t + 1] = new_m
        curr_m = new_m

    D = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]
    ans = 1e9
    for dr, dc in D:
        rr, cc = r + dr, c + dc
        if len(curr_m[(rr, cc)]) > 0:
            continue
        if not (0 <= rr < R and 0 <= cc < C):
            continue
        if rr == 0 and cc != s_c:
            continue
        if rr == R - 1 and cc != e_c:
            continue
        if cc == 0 or cc == C - 1:
            continue
        ans = min(ans, day24_solve(t + 1, rr, cc, bs_t, R, C, e_c, s_c, DP))
    DP[k] = ans
    return ans


def day24_get_bs(bs_t, t, R, C):
    if t in bs_t:
        return bs_t[t]
    else:
        new_m = defaultdict(list)
        for (rr, cc), bs in bs_t[t - 1].items():
            for dr, dc in bs:
                rrr, ccc = rr + dr, cc + dc
                if rrr == R - 1:
                    assert dr == 1
                    rrr = 1
                elif rrr == 0:
                    assert dr == -1
                    rrr = R - 2
                elif ccc == C - 1:
                    assert dc == 1
                    ccc = 1
                elif ccc == 0:
                    assert dc == -1
                    ccc = C - 2

                new_m[(rrr, ccc)].append((dr, dc))
        bs_t[t] = new_m
        return new_m


def day24_1(data):
    m, (s_c, e_c), (R, C) = day24_parse(data)

    # seen_m = set()
    # t = 0
    # curr_m = m
    # while True:
    #     t+=1
    #     l = deque([])
    #     for (rr,cc),bs in curr_m.items():
    #         for (dr,dc) in bs:
    #             l.append((rr,cc,dr,dc))
    #     k = (tuple(sorted(l)))
    #     if k in seen_m:
    #         assert False, t
    #         continue

    #     new_m = defaultdict(list)
    #     for (rr,cc),bs in curr_m.items():
    #         for dr,dc in bs:
    #             rrr,ccc = rr+dr, cc+dc
    #             if rrr == R-1:
    #                 assert dr == 1
    #                 rrr = 1
    #             elif rrr == 0:
    #                 assert dr == -1
    #                 rrr = R-2
    #             if ccc == C-1:
    #                 assert dc == 1
    #                 ccc = 1
    #             elif ccc == 0:
    #                 assert dc == -1
    #                 ccc = C-2

    #             new_m[(rrr,ccc)].append((dr,dc))
    #     curr_m = new_m

    bs_t = {}
    bs_t[0] = m
    # return day24_solve(0, 0, s_c, bs_t, R,C,e_c, s_c, {})
    q = [(0, (abs(e_c - s_c) + R - 1), (0, s_c), m)]
    q = [((0,0), 0, (0, s_c))]
    # q = deque(q)
    seen = set()
    D = [(1, 0), (0, 1), (0,-1), (-1, 0), (0, 0)]
    print(s_c, e_c)
    print(sum(len(v) for v in m.values()))
    best = 1e9
    while q:
        (_,w), t, (r, c) = heappop(q)
        # print(t)
        # _, t, (r,c) = q.popleft()
        # print(cost,r,c,curr_m[(r,c)])
        # if cost == 6:
        #     assert False
        # if len(m[(r,c)]) != 0:
        #     continue
        if (r, c) == (R - 1, e_c):
            return t

        curr_m = day24_get_bs(bs_t, t, R, C)
        # day24_print(r, c, curr_m, R, C)
        # time.sleep(.5)
        l = []
        for (rr, cc), bs in curr_m.items():
            for (dr, dc) in bs:
                if (rr,cc) < (r,c):
                    continue
                l.append((rr, cc, dr, dc))

        k = (r, c, tuple(sorted(l)))
        if k in seen:
            # print("x")
            continue
        seen.add(k)
        moved = False
        for dr, dc in D:
            # if moved: continue
            rr, cc = r + dr, c + dc
            new_m = day24_get_bs(bs_t, t + 1, R, C)
            if len(new_m[(rr, cc)]) > 0:
                continue
            if not (0 <= rr < R and 0 <= cc < C):
                continue
            if rr == 0:
                continue
            if rr == R - 1 and cc != e_c:
                continue
            if cc == 0:
                continue
            if cc == C - 1:
                continue
            # if dr==dc==0:
            #     continue
            moved = True
            w2 = 1 if dr==dc==0 else 0
            heappush(q, (((abs(e_c - cc) +
                     abs(R - 1 - rr))+t+1,0), t + 1, (rr, cc)))
            # heappush(q, ((0), t+1, (r+dr, c+dc), deepcopy(new_m)))
            # q.append(((0), t+1, (rr,cc)))
        # if not moved:
        #     heappush(q, (t + 1 + (abs(e_c - c) +
        #              abs(R - 1 - r)), t + 1, (r, c)))

    # 355
    # 354
    # 356
    return best

def day24_2(data):
    m, (s_c, e_c), (R, C) = day24_parse(data)

    # seen_m = set()
    # t = 0
    # curr_m = m
    # while True:
    #     t+=1
    #     l = deque([])
    #     for (rr,cc),bs in curr_m.items():
    #         for (dr,dc) in bs:
    #             l.append((rr,cc,dr,dc))
    #     k = (tuple(sorted(l)))
    #     if k in seen_m:
    #         assert False, t
    #         continue

    #     new_m = defaultdict(list)
    #     for (rr,cc),bs in curr_m.items():
    #         for dr,dc in bs:
    #             rrr,ccc = rr+dr, cc+dc
    #             if rrr == R-1:
    #                 assert dr == 1
    #                 rrr = 1
    #             elif rrr == 0:
    #                 assert dr == -1
    #                 rrr = R-2
    #             if ccc == C-1:
    #                 assert dc == 1
    #                 ccc = 1
    #             elif ccc == 0:
    #                 assert dc == -1
    #                 ccc = C-2

    #             new_m[(rrr,ccc)].append((dr,dc))
    #     curr_m = new_m

    bs_t = {}
    bs_t[0] = m
    # return day24_solve(0, 0, s_c, bs_t, R,C,e_c, s_c, {})
    q = [(0, (abs(e_c - s_c) + R - 1), (0, s_c), m)]
    q = [((0,0), 0, (0, s_c))]
    # q = deque(q)
    seen = set()
    D = [(1, 0), (0, 1), (0,-1), (-1, 0), (0, 0)]
    print(s_c, e_c)
    print(sum(len(v) for v in m.values()))
    best = 1e9
    while q:
        (_,w), t, (r, c) = heappop(q)
        # print(t)
        # _, t, (r,c) = q.popleft()
        # print(cost,r,c,curr_m[(r,c)])
        # if cost == 6:
        #     assert False
        # if len(m[(r,c)]) != 0:
        #     continue
        if (r, c) == (R - 1, e_c):
            best = t
            break
            # return t

        curr_m = day24_get_bs(bs_t, t, R, C)
        # day24_print(r, c, curr_m, R, C)
        # time.sleep(.5)
        l = []
        for (rr, cc), bs in curr_m.items():
            for (dr, dc) in bs:
                if (rr,cc) < (r,c):
                    continue
                l.append((rr, cc, dr, dc))

        k = (r, c, tuple(sorted(l)))
        if k in seen:
            # print("x")
            continue
        seen.add(k)
        moved = False
        for dr, dc in D:
            # if moved: continue
            rr, cc = r + dr, c + dc
            new_m = day24_get_bs(bs_t, t + 1, R, C)
            if len(new_m[(rr, cc)]) > 0:
                continue
            if not (0 <= rr < R and 0 <= cc < C):
                continue
            if rr == 0:
                continue
            if rr == R - 1 and cc != e_c:
                continue
            if cc == 0:
                continue
            if cc == C - 1:
                continue
            # if dr==dc==0:
            #     continue
            moved = True
            w2 = 1 if dr==dc==0 else 0
            heappush(q, (((abs(e_c - cc) +
                     abs(R - 1 - rr))+t+1,0), t + 1, (rr, cc)))
            # heappush(q, ((0), t+1, (r+dr, c+dc), deepcopy(new_m)))
            # q.append(((0), t+1, (rr,cc)))
        # if not moved:
        #     heappush(q, (t + 1 + (abs(e_c - c) +
        #              abs(R - 1 - r)), t + 1, (r, c)))

    q = [((0,0), best, (R-1, e_c))]
    # q = deque(q)
    seen = set()
    D = [(1, 0), (0, 1), (0,-1), (-1, 0), (0, 0)]
    # best = 1e9
    while q:
        (_,w), t, (r, c) = heappop(q)
        # print(t)
        # _, t, (r,c) = q.popleft()
        # print(cost,r,c,curr_m[(r,c)])
        # if cost == 6:
        #     assert False
        # if len(m[(r,c)]) != 0:
        #     continue
        if (r, c) == (0, s_c):
            best += t
            break

        curr_m = day24_get_bs(bs_t, t, R, C)
        # day24_print(r, c, curr_m, R, C)
        # time.sleep(.5)
        l = []
        for (rr, cc), bs in curr_m.items():
            for (dr, dc) in bs:
                if (rr,cc) > (r,c):
                    continue
                l.append((rr, cc, dr, dc))

        k = (r, c, tuple(sorted(l)))
        if k in seen:
            # print("x")
            continue
        seen.add(k)
        moved = False
        for dr, dc in D:
            # if moved: continue
            rr, cc = r + dr, c + dc
            new_m = day24_get_bs(bs_t, t + 1, R, C)
            if len(new_m[(rr, cc)]) > 0:
                continue
            if not (0 <= rr < R and 0 <= cc < C):
                continue
            if rr == 0:
                continue
            if rr == R - 1 and cc != s_c:
                continue
            if cc == 0:
                continue
            if cc == C - 1:
                continue
            # if dr==dc==0:
            #     continue
            moved = True
            w2 = 1 if dr==dc==0 else 0
            heappush(q, (((abs(e_c - cc) +
                     abs(R - 1 - rr))+t+1,0), t + 1, (rr, cc)))
    q = [((0,0), best, (0, s_c))]
    # q = deque(q)
    seen = set()
    D = [(1, 0), (0, 1), (0,-1), (-1, 0), (0, 0)]
    # best = 1e9
    while q:
        (_,w), t, (r, c) = heappop(q)
        # print(t)
        # _, t, (r,c) = q.popleft()
        # print(cost,r,c,curr_m[(r,c)])
        # if cost == 6:
        #     assert False
        # if len(m[(r,c)]) != 0:
        #     continue
        if (r, c) == (R-1, e_c):
            best += t
            break

        curr_m = day24_get_bs(bs_t, t, R, C)
        # day24_print(r, c, curr_m, R, C)
        # time.sleep(.5)
        l = []
        for (rr, cc), bs in curr_m.items():
            for (dr, dc) in bs:
                if (rr,cc) < (r,c):
                    continue
                l.append((rr, cc, dr, dc))

        k = (r, c, tuple(sorted(l)))
        if k in seen:
            # print("x")
            continue
        seen.add(k)
        moved = False
        for dr, dc in D:
            # if moved: continue
            rr, cc = r + dr, c + dc
            new_m = day24_get_bs(bs_t, t + 1, R, C)
            if len(new_m[(rr, cc)]) > 0:
                continue
            if not (0 <= rr < R and 0 <= cc < C):
                continue
            if rr == 0:
                continue
            if rr == R - 1 and cc != e_c:
                continue
            if cc == 0:
                continue
            if cc == C - 1:
                continue
            # if dr==dc==0:
            #     continue
            moved = True
            w2 = 1 if dr==dc==0 else 0
            heappush(q, (((abs(e_c - cc) +
                     abs(R - 1 - rr))+t+1,0), t + 1, (rr, cc)))
    # 355
    # 354
    # 356
    return best


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
