# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys
from collections import defaultdict

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
# pylint: enable=wrong-import-position

def day6_parse(inst):
    rest = None
    op = None
    if inst.startswith("turn on "):
        # turn on 0,0 through 999,999
        rest = inst[len("turn on "):]
        op = 1
    elif inst.startswith("toggle "):
        # toggle 0,0 through 999,0
        rest = inst[len("toggle "):]
        op = -1
    elif inst.startswith("turn off "):
        # turn off 499,499 through 500,500
        rest = inst[len("turn off "):]
        op = 0
    start, end = rest.split(" through ")
    start = [int(x) for x in start.split(",")]
    end = [int(x) for x in end.split(",")]

    assert start[0] >= 0 and start[0] < 1000
    assert start[1] >= 0 and start[1] < 1000
    assert end[0] >= 0 and end[0] < 1000
    assert end[1] >= 0 and end[1] < 1000
    return op, start, end

def day6_solve1(inst_list):
    lights = set()
    for inst in inst_list:
        op, start, end = day6_parse(inst)

        start_x, start_y = start
        end_x, end_y = end
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                if op == 1:
                    lights.add((x, y))
                elif op == 0:
                    if (x, y) in lights:
                        lights.remove((x, y))
                elif op == -1:
                    if (x, y) in lights:
                        lights.remove((x, y))
                    else:
                        lights.add((x, y))
                else:
                    assert False
    return lights

def day6_solve2(inst_list):
    lights = defaultdict(lambda: 0)
    for inst in inst_list:
        op, start, end = day6_parse(inst)

        start_x, start_y = start
        end_x, end_y = end
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                if op == 1:
                    lights[(x, y)] += 1
                elif op == 0:
                    lights[(x, y)] -= 1
                    if lights[(x, y)] < 0:
                        del lights[(x, y)]
                elif op == -1:
                    lights[(x, y)] += 2
                else:
                    assert False
    return lights

def day6_1(data):
    return len(day6_solve1(data))

def day6_2(data):
    return sum([v for v in day6_solve2(data).values()])


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2015)
