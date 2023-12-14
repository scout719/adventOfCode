# -*- coding: utf-8 -*-
import os
import sys
from collections import defaultdict

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import day_with_validation, main  # NOQA: E402

YEAR = 2022
DAY = 17
EXPECTED_1 = 3068
EXPECTED_2 = 1514285714288

""" DAY 17 """

def day17_parse(data):
    return list(data[0])

def day17_shape(t):
    shapes = [
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
        [(0, 0), [1, 0], (2, 0), (3, 0)],
        [[0, 0], (0, 1), (1, 0), (1, 1)]
    ]
    return shapes[t % 5]

def day17_print(G):
    max_r = max(r for r, _ in G) if G else 3
    for r in range(max_r, -1, -1):
        line = "|"
        for c in range(0, 7):
            if (r, c) in G:
                line += "#"
            else:
                line += " "
        line += "|"
        print(line)
    print("-" * 9)
    print()

def day17_make_move(grid, grid_width, t, max_r, jets, curr_jet):
    shape = day17_shape(t)
    shape = [(max_r + 3 + 1 + rr, cc + 2) for rr, cc in shape]
    moving = True
    while moving:
        jet = jets[curr_jet]
        curr_jet += 1
        curr_jet %= len(jets)
        dc = 0
        if jet == "<":
            dc = -1
        else:
            assert jet == ">"
            dc = 1

        is_pushed = True
        for rr, cc in shape:
            if not (0 <= cc + dc < grid_width) or (rr, cc + dc) in grid:
                is_pushed = False
                break
        if is_pushed:
            shape = [(rr, cc + dc) for rr, cc in shape]

        can_drop = True
        for rr, cc in shape:
            if (rr - 1, cc) in grid or rr - 1 < 0:
                can_drop = False
                break

        if can_drop:
            shape = [(rr - 1, cc) for rr, cc in shape]
        else:
            moving = False
    return curr_jet, shape

def day17_1(data):
    jets = day17_parse(data)
    grid_width = 7
    grid = set()
    curr_jet = 0
    max_r = -1
    for t in range(2022):
        curr_jet, shape = day17_make_move(
            grid, grid_width, t, max_r, jets, curr_jet)

        for r, c in shape:
            grid.add((r, c))
            max_r = max(max_r, r)
    return max_r + 1

def day17_2(data):
    jets = day17_parse(data)
    grid_width = 7
    grid = set()
    buffer_lines = 10
    curr_jet = 0
    buffers_memory = defaultdict(list)
    max_r = -1
    max_t = 1000000000000
    found_cycle = False
    t = 0
    while t < max_t:
        if not found_cycle:
            curr_buffer = []
            for l in range(buffer_lines):
                line = set(c for r, c in grid if r == max_r - l)
                curr_buffer.append(line)
            key = (t % 5, curr_jet)
            skip_iteration = False
            for buffer, buffer_t, buffer_max_r in buffers_memory[key]:
                equal = True
                for l in range(buffer_lines):
                    if buffer[l] != curr_buffer[l]:
                        equal = False
                        break
                if equal:
                    t_cycle = t - buffer_t
                    reps = (max_t - t) // t_cycle
                    height = max_r - buffer_max_r
                    max_r += height * reps
                    # max_t = 11, t = 4, max_r = 10
                    # buffer_t = 1, buffer_max_r = 5, t_cycle = 3
                    # reps = (11-4)//3=2
                    # height = 10-5=5
                    # max_t = 10+5*2=20
                    # t -> 4 + 3*2
                    t += t_cycle * reps
                    # Add buffer again with new row number
                    for l in range(buffer_lines):
                        for c in buffer[l]:
                            grid.add((max_r - l, c))
                    skip_iteration = True
                    found_cycle = True

            buffers_memory[key].append((curr_buffer, t, max_r))
            if skip_iteration:
                continue

        curr_jet, shape = day17_make_move(
            grid, grid_width, t, max_r, jets, curr_jet)

        for r, c in shape:
            grid.add((r, c))
            max_r = max(max_r, r)
        t += 1
    return max_r + 1


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
