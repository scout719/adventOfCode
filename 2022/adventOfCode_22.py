# -*- coding: utf-8 -*-
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable-next=wrong-import-position
from common.utils import main, day_with_validation  # NOQA: E402

YEAR = 2022
DAY = 22
EXPECTED_1 = 6032
EXPECTED_2 = 5031

""" DAY 22 """

def day22_parse(data):
    is_occupied = {}
    for r, line in enumerate(data):
        if not line:
            break
        for c, char in enumerate(line):
            if char == ".":
                is_occupied[(r, c)] = True
            elif char == "#":
                is_occupied[(r, c)] = False

    path = []
    curr = ""
    for char in data[-1]:
        if char in ["R", "L"]:
            path.append((int(curr), char))
            curr = ""
        else:
            curr += char
    path.append((int(curr), ""))
    return (is_occupied, path)

def day22_rotate(dr, dc, rotate):
    if rotate == "R":
        # 0, 1 -> 1,0
        # 0,-1 -> -1 ,0
        # 1,0 -> 0,-1
        # -1,0 -> 0,1
        dr, dc = dc, -dr
    elif rotate == "L":
        # 0, 1 -> -1,0
        # 0,-1 -> 1 ,0
        # 1,0 -> 0,1
        # -1,0 -> 0,-1
        dr, dc = -dc, dr
    return dr, dc


def day22_1(data):
    is_occupied, path = day22_parse(data)
    positions = set(k for k in is_occupied)
    R = max(r for r, c in positions) + 1
    C = max(c for r, c in positions) + 1
    r = min(r for r, c in positions)
    c = min(c for rr, c in positions if rr == r)
    dr, dc = (0, 1)
    for steps, rotate in path:
        for _ in range(steps):
            rr, cc = r + dr, c + dc
            if (rr, cc) not in positions:
                while (rr, cc) not in positions:
                    rr, cc = (rr + dr) % R, (cc + dc) % C
            if is_occupied[(rr, cc)]:
                r, c = rr, cc
        dr, dc = day22_rotate(dr, dc, rotate)

    facing = 0
    if (dr, dc) == (0, 1):
        facing = 0
    elif (dr, dc) == (1, 0):
        facing = 1
    elif (dr, dc) == (0, -1):
        facing = 2
    else:
        facing = 3
    # 43474
    return (r + 1) * 1000 + (c + 1) * 4 + facing

def day22_face_real(r, c, region_size):
    #  |  1122
    #  |  1122
    #  |  44
    #  |  44
    #  |5566
    #  |5566
    #  |33
    #  |33
    if 0 <= r < region_size:
        if region_size <= c < region_size * 2:
            return 1
        else:
            assert region_size * 2 <= c < region_size * 3
            return 2
    if region_size <= r < region_size * 2:
        assert region_size <= c < region_size * 2
        return 4
    if region_size * 2 <= r < region_size * 3:
        if 0 <= c < region_size:
            return 5
        else:
            assert region_size <= c < region_size * 2
            return 6
    assert region_size * 3 <= r < region_size * 4
    assert 0 <= c < region_size
    return 3

def day22_face_example(r, c, region_size):
    if 0 <= r < region_size:
        assert region_size * 2 <= c < region_size * 3
        return 1
    if region_size <= r < region_size * 2:
        if 0 <= c < region_size:
            return 2
        elif region_size <= c < region_size * 2:
            return 3
        else:
            assert region_size * 2 <= c < region_size * 3
            return 4
    assert region_size * 2 <= r < region_size * 3
    if region_size * 2 <= c < region_size * 3:
        return 5
    assert region_size * 3 <= c < region_size * 4
    return 6

def day22_overflow_real(rr, cc, dr, dc, face, region_size):
    #  |  1122
    #  |  1122
    #  |  44
    #  |  44
    #  |5566
    #  |5566
    #  |33
    #  |33
    if face == 1:
        if dr == -1:
            assert rr == -1
            rr, cc = region_size * 3 + (cc - region_size), 0
            ddr, ddc = 0, 1
            assert day22_face_real(rr, cc, region_size) == 3
        elif dc == -1:
            assert cc == region_size - 1
            rr, cc = region_size * 3 - 1 - rr, 0
            ddr, ddc = 0, 1
            assert day22_face_real(rr, cc, region_size) == 5
    elif face == 2:
        if dr == -1:
            assert rr == -1
            rr, cc = region_size * 4 - 1, cc - region_size * 2
            ddr, ddc = -1, 0
            assert day22_face_real(rr, cc, region_size) == 3
        elif dr == 1:
            assert rr == region_size
            rr, cc = region_size + (cc - region_size * 2), region_size * 2 - 1
            ddr, ddc = 0, -1
            assert day22_face_real(rr, cc, region_size) == 4
        else:
            assert dc == 1 and cc == region_size * 3
            rr, cc = region_size * 2 + \
                (region_size - 1 - rr), region_size * 2 - 1
            ddr, ddc = 0, -1
            assert day22_face_real(rr, cc, region_size) == 6
    elif face == 3:
        if dr == 1:
            assert rr == 4 * region_size
            rr, cc = 0, region_size * 2 + cc
            ddr, ddc = 1, 0
            assert day22_face_real(rr, cc, region_size) == 2
        elif dc == 1:
            assert cc == region_size
            rr, cc = region_size * 3 - 1, region_size + (rr - region_size * 3)
            ddr, ddc = -1, 0
            assert day22_face_real(rr, cc, region_size) == 6
        else:
            assert dc == -1 and cc == -1
            rr, cc = 0, region_size + (rr - region_size * 3)
            ddr, ddc = 1, 0
            assert day22_face_real(rr, cc, region_size) == 1
    elif face == 4:
        if dc == -1:
            assert cc == region_size - 1
            rr, cc = region_size * 2, rr - region_size
            ddr, ddc = 1, 0
            assert day22_face_real(rr, cc, region_size) == 5
        else:
            assert dc == 1
            assert cc == region_size * 2
            rr, cc = region_size - 1, region_size * 2 + (rr - region_size)
            ddr, ddc = -1, 0
            assert day22_face_real(rr, cc, region_size) == 2
    elif face == 5:
        if dr == -1:
            assert rr == region_size * 2 - 1
            rr, cc = region_size + cc, region_size
            ddr, ddc = 0, 1
            assert day22_face_real(rr, cc, region_size) == 4
        else:
            assert dc == -1 and cc == -1
            rr, cc = region_size - 1 - (rr - region_size * 2), region_size
            ddr, ddc = 0, 1
            assert day22_face_real(rr, cc, region_size) == 1
    else:
        assert face == 6
        if dr == 1:
            assert rr == region_size * 3
            rr, cc = region_size * 3 + (cc - region_size), region_size - 1
            ddr, ddc = 0, -1
            assert day22_face_real(rr, cc, region_size) == 3
        else:
            assert dc == 1 and cc == region_size * 2
            rr, cc = region_size * 3 - 1 - rr, region_size * 3 - 1
            ddr, ddc = 0, -1
            assert day22_face_real(rr, cc, region_size) == 2

    return (rr, cc, ddr, ddc)

def day22_overflow_example(rr, cc, dr, dc, face, region_size):
    if face == 1:
        if dr == -1:
            assert rr == -1
            rr, _ = region_size * 3 - 1, cc
            ddr, ddc = 1, 0
            assert day22_face_example(rr, cc, region_size) == 2
        elif dc == -1:
            assert cc == region_size * 2 - 1
            rr, cc = region_size, region_size + region_size - rr
            ddr, ddc = 1, 0
            assert day22_face_example(rr, cc, region_size) == 3
        else:
            assert dc == 1 and cc == region_size * 3
            rr, cc = region_size * 3 - 1 - rr, region_size * 4 - 1
            ddr, ddc = 0, -1
            assert day22_face_example(rr, cc, region_size) == 6
    elif face == 2:
        if dr == -1:
            assert rr == region_size - 1
            rr, cc = 0, region_size * 2 + (region_size - 1 - cc)
            ddr, ddc = 1, 0
            assert day22_face_example(rr, cc, region_size) == 1
        elif dc == -1:
            assert cc == -1
            _, cc = rr, region_size * 3 - 1
            ddr, ddc = 0, -1
            assert day22_face_example(rr, cc, region_size) == 6
        else:
            assert dr == 1 and rr == region_size * 2
            rr, cc = region_size * 2 - 1, region_size * \
                2 + (region_size - 1 - cc)
            ddr, ddc = -1, 0
            assert day22_face_example(rr, cc, region_size) == 5
    elif face == 3:
        if dr == -1:
            assert rr == region_size - 1
            rr, cc = cc - region_size, region_size * 2
            ddr, ddc = 0, 1
            assert day22_face_example(rr, cc, region_size) == 1
        else:
            assert dr == 1 and rr == region_size * 2
            rr, cc = region_size * 3 - 1 - (cc - region_size), region_size * 2
            ddr, ddc = 0, 1
            assert day22_face_example(rr, cc, region_size) == 5
    elif face == 4:
        assert dc == 1 and cc == region_size * 3
        rr, cc = region_size * 2, region_size * 4 - 1 - (rr - region_size)
        ddr, ddc = 1, 0
        assert day22_face_example(rr, cc, region_size) == 6
    elif face == 5:
        if dr == 1:
            assert rr == region_size * 3
            rr, cc = region_size * 2 - 1, region_size - \
                1 - (cc - region_size * 2)
            ddr, ddc = -1, 0
            assert day22_face_example(rr, cc, region_size) == 2
        else:
            assert dc == -1 and cc == region_size * 2 - 1
            rr, cc = region_size * 2 - 1, region_size + (rr - region_size * 2)
            ddr, ddc = -1, 0
            assert day22_face_example(rr, cc, region_size) == 3
    else:
        assert face == 6
        if dr == 1:
            assert rr == region_size * 3
            rr, cc = region_size * 2 - 1 - (cc - region_size * 3), 0
            ddr, ddc = 0, 1
            assert day22_face_example(rr, cc, region_size) == 2
        elif dr == -1:
            assert rr == region_size * 2 - 1
            rr, cc = region_size * 2 - 1 - \
                (cc - region_size * 3), region_size * 3 - 1
            ddr, ddc = 0, -1
            assert day22_face_example(rr, cc, region_size) == 4
        else:
            # print(r,c, rr,cc ,dr,dc,f)
            assert dc == 1 and cc == region_size * 4
            rr, cc = region_size * 3 - 1 - rr, region_size * 3 - 1
            ddr, ddc = 0, -1
            assert day22_face_example(rr, cc, region_size) == 1

    return (rr, cc, ddr, ddc)

def day22_2(data):
    is_ocuppied, path = day22_parse(data)
    positions = set(k for k in is_ocuppied)
    R = max(r for r, c in positions) + 1
    r = min(r for r, c in positions)
    c = min(c for rr, c in positions if rr == r)
    dr, dc = (0, 1)
    L = 50 if R > 20 else 4
    for st, d in path:
        for _ in range(st):
            rr, cc = r + dr, c + dc
            ddr, ddc = dr, dc
            if (rr, cc) not in positions:
                if R <= 20:
                    face = day22_face_example(r, c, L)
                    rr, cc, ddr, ddc = day22_overflow_example(
                        rr, cc, dr, dc, face, L)
                else:
                    face = day22_face_real(r, c, L)
                    rr, cc, ddr, ddc = day22_overflow_real(
                        rr, cc, dr, dc, face, L)
                assert (rr, cc) in positions, (rr, cc)

            if is_ocuppied[(rr, cc)]:
                r, c = rr, cc
                dr, dc = ddr, ddc
        dr, dc = day22_rotate(dr, dc, d)

    facing = 0
    if (dr, dc) == (0, 1):
        facing = 0
    elif (dr, dc) == (1, 0):
        facing = 1
    elif (dr, dc) == (0, -1):
        facing = 2
    else:
        facing = 3
    # 43474
    return (r + 1) * 1000 + (c + 1) * 4 + facing


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
