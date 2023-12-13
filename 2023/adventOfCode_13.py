# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict
from copy import deepcopy
import os
import string
import sys
from typing import List, Mapping, Tuple, Set

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2023
DAY = 13
EXPECTED_1 = None  # 405
EXPECTED_2 = 400


""" DAY 13 """

def day13_parse(data: List[str]):
    patterns = []
    pattern = []
    for line in data:
        if line:
            pattern.append(line)
        else:
            patterns.append(pattern)
            pattern = []
    if pattern:
        patterns.append(pattern)

    return patterns

def day13_mirror(p, R, C, rows: Mapping[int, Set[int]], cols: Mapping[int, Set[int]], opposite, old_m_r=None, old_m_c=None):
    rows = deepcopy(rows)
    cols = deepcopy(cols)
    if opposite:
        r, c = opposite
        if c in rows[r]:
            rows[r].remove(c)
            # if not rows[r]:
            #     rows.pop(r, None)
        else:
            rows[r].add(c)

        if r in cols[c]:
            cols[c].remove(r)
            # if not cols[c]:
            #     cols.pop(c, None)
        else:
            cols[c].add(r)
    m_r = -1
    m_c = -1
    for r in range(R - 1):
        mirror = True
        i = 0
        rr_u = r - i
        rr_d = r + i + 1
        while 0 <= rr_u < rr_d < R:
            if rows[rr_u] != rows[rr_d]:
                mirror = False
                break
            i += 1
            rr_u = r - i
            rr_d = r + i + 1
        if mirror:
            m_r = r
            if old_m_r and m_r+1 == old_m_r:
                continue
            break
    for c in range(C - 1):
        mirror = True
        i = 0
        cc_l = c - i
        cc_r = c + i + 1
        while 0 <= cc_l < cc_r < C:
            if cols[cc_l] != cols[cc_r]:
                mirror = False
                break
            i += 1
            cc_l = c - i
            cc_r = c + i + 1
        if mirror:
            m_c = c
            if old_m_c and m_c+1 == old_m_c:
                continue
            break

    return m_r + 1, m_c + 1


def day13_1(data):
    patterns = day13_parse(data)
    rs = []
    cs = []
    rs2 = 0
    cs2 = 0
    for p in patterns:
        R = len(p)
        C = len(p[0])
        rows = defaultdict(set)
        cols = defaultdict(set)
        points = set()
        for r in range(R):
            for c in range(C):
                if p[r][c] == "#":
                    rows[r].add(c)
                    cols[c].add(r)
                    points.add((r, c))

        m_r, m_c = day13_mirror(p, R, C, rows, cols, None)
        rs2 += m_r
        cs2 += m_c
    return 100 * rs2 + cs2

def day13_2(data: List[str]):
    patterns = day13_parse(data)
    rs = []
    cs = []
    rs2 = 0
    cs2 = 0
    for p in patterns:
        # print("\n".join(p))
        R = len(p)
        C = len(p[0])
        rows = defaultdict(set)
        cols = defaultdict(set)
        points = set()
        for r in range(R):
            for c in range(C):
                if p[r][c] == "#":
                    rows[r].add(c)
                    cols[c].add(r)
                    points.add((r, c))

        m_r, m_c = day13_mirror(p, R, C, rows, cols, None)
        f = False
        for rr in range(R):
            found = False
            for cc in range(C):
                # 10, 6
                m_r2, m_c2 = day13_mirror(
                    p, R, C, rows, cols, (rr, cc), m_r, m_c) 
                if m_r2 == 0 and m_c2 == 0:
                    continue
                if m_r2 != m_r:
                    rs2 += m_r2
                    found = True
                    f = True
                    break
                elif m_c2 != m_c:
                    cs2 += m_c2
                    found = True
                    f = True
                    break
            if found:
                break
        board = "\n".join(p)
        assert f, f"\n{R} {C} \n{board}\n, {m_r}, {m_c}"

    # 22299 low
    return 100 * rs2 + cs2


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
