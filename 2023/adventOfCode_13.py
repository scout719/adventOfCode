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
EXPECTED_1 = 405
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

def day13_mirror(R, C, rows: Mapping[int, Set[int]], cols: Mapping[int, Set[int]]):
    mirror_rows = set()
    mirror_columns = set()
    for r in range(R - 1):
        mirror = True
        i = 0
        row_up, row_down = r - i, r + i + 1
        while 0 <= row_up < row_down < R:
            if rows[row_up] != rows[row_down]:
                mirror = False
                break
            i += 1
            row_up, row_down = r - i, r + i + 1
        if mirror:
            mirror_rows.add(r + 1)
    for c in range(C - 1):
        mirror = True
        i = 0
        col_left, col_right = c - i, c + i + 1
        while 0 <= col_left < col_right < C:
            if cols[col_left] != cols[col_right]:
                mirror = False
                break
            i += 1
            col_left, col_right = c - i, c + i + 1
        if mirror:
            mirror_columns.add(c + 1)

    return mirror_rows, mirror_columns

def day13_get_data(pattern):
    R = len(pattern)
    C = len(pattern[0])
    rows = defaultdict(set)
    cols = defaultdict(set)
    for r in range(R):
        for c in range(C):
            if pattern[r][c] == "#":
                rows[r].add(c)
                cols[c].add(r)
    return R, C, rows, cols

def day13_single_mirror(R, C, rows, cols):
    mirror_rows, mirror_cols = day13_mirror(R, C, rows, cols)
    assert len(mirror_rows) + \
        len(mirror_cols) == 1, f"{mirror_rows} {mirror_cols}"
    return (mirror_rows.pop() if mirror_rows else 0,
            mirror_cols.pop() if mirror_cols else 0)

def day13_1(data):
    patterns = day13_parse(data)
    ans_r = 0
    ans_c = 0
    for pattern in patterns:
        R, C, rows, cols = day13_get_data(pattern)

        mirror_row, mirror_col = day13_single_mirror(R, C, rows, cols)
        ans_r += mirror_row
        ans_c += mirror_col
    return 100 * ans_r + ans_c

def day13_2(data: List[str]):
    patterns = day13_parse(data)
    ans_r = 0
    ans_c = 0
    for p in patterns:
        R, C, rows, cols = day13_get_data(p)
        mirror_row, mirror_col = day13_single_mirror(R, C, rows, cols)
        found = False
        for r in range(R):
            for c in range(C):
                n_rows = deepcopy(rows)
                n_cols = deepcopy(cols)
                if c in n_rows[r]:
                    n_rows[r].remove(c)
                else:
                    n_rows[r].add(c)

                if r in n_cols[c]:
                    n_cols[c].remove(r)
                else:
                    n_cols[c].add(r)

                mirror_rows, mirror_cols = day13_mirror(
                    R, C, n_rows, n_cols)
                mirror_rows -= set([mirror_row])
                mirror_cols -= set([mirror_col])
                if mirror_rows:
                    ans_r += mirror_rows.pop()
                    found = True
                    break
                if mirror_cols:
                    ans_c += mirror_cols.pop()
                    found = True
                    break
            if found:
                break
        board = "\n".join(p)
        assert found, f"\n{R} {C} \n{board}"

    return 100 * ans_r + ans_c


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
