# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from copy import deepcopy
from functools import cache
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2025
DAY = 12
EXPECTED_1 = 2
EXPECTED_2 = 2

def day12_parse(data: list[str]):
    shapes = []
    regions = []
    curr_shape = set()
    row = 0
    for line in data:
        if "x" in line:
            # Regions
            sz, qtt = line.split(":")
            R, C = sz.split("x")
            R, C = int(R), int(C)
            qtts = []
            for j, count in enumerate(qtt.strip().split(" ")):
                count = int(count)
                if count > 0:
                    qtts.append((j, count))
            regions.append((R, C, qtts))

        elif ":" in line:
            # New shape
            pass
        elif not line:
            # Finished a new shape
            shapes.append(curr_shape)
            curr_shape = set()
            row = 0
        else:
            # Mid shape
            assert "." in line or "#" in line
            for col, pos in enumerate(list(line)):
                if pos == "#":
                    curr_shape.add((row, col))
            row += 1

    return shapes, regions

def day12_print(shape):
    line = ""
    for r in range(3):
        for c in range(3):
            if (r, c) in shape:
                line += "#"
            else:
                line += "."
        print(line)
        line = ""
    print()

def day12_flip(shape):
    for r, c in shape:
        yield (r, 2 - c)

def day12_rotate(shape):
    for r, c in shape:
        # add 2 to column to 'move' to positive quadrant
        yield (c, -r + 2)

def day12_contains(shape: set[tuple[int, int]], shapes: list[set[tuple[int, int]]]):
    for shape2 in shapes:
        if shape == shape2:
            return True
    return False

@cache
def day12_shapes(shape):
    shapes = []

    others = [
        shape,
        set(day12_flip(shape)),
        set(day12_rotate(shape)),
        set(day12_rotate(day12_flip(shape))),
        set(day12_rotate(day12_rotate(shape))),
        set(day12_rotate(day12_rotate(day12_flip(shape)))),
        set(day12_rotate(day12_rotate(day12_rotate(shape)))),
        set(day12_rotate(day12_rotate(day12_rotate(day12_flip(shape))))),
    ]
    for shape2 in others:
        if not day12_contains(shape2, shapes):
            shapes.append(shape2)

    return shapes

def day12_fits(free: set[tuple[int, int]], shape):
    for r, c in free:
        # Try to place the shape at (r,c)
        for new_shape in day12_shapes(frozenset(shape)):
            occupied = set()
            for rr, cc in new_shape:
                if not (r + rr, c + cc) in free:
                    occupied = set()
                    break
                occupied.add((r + rr, c + cc))

            if occupied:
                return occupied

    return set()

def day12_possible(free: set[tuple[int, int]], shapes, left: list[int], space_needed):
    if len(left) == 0:
        return True

    if len(free) < space_needed:
        return False

    for i in left:
        fits = day12_fits(free, shapes[i])
        if fits:
            new_left = deepcopy(left)
            new_left.remove(i)
            new_free = free.difference(fits)
            if day12_possible(new_free, shapes, new_left, space_needed - len(shapes[i])):
                return True
            else:
                # Shape fitted but lead to impossible situation, keep trying
                pass
        else:
            return False
    return False


def day12_solve(data, _):
    shapes, regions = day12_parse(data)

    total = 0
    for R, C, qtts in regions:
        left = []
        space_needed = 0
        for i, n in qtts:
            for _ in range(n):
                left.append(i)
                space_needed += len(shapes[i])
        free = set((r, c) for r in range(R) for c in range(C))
        if day12_possible(free, shapes, left, space_needed):
            total += 1

    return total

def day12_1(data):
    return day12_solve(data, False)

def day12_2(data):
    return day12_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
