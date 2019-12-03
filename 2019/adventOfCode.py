# pylint: disable=unused-import
# pylint: disable=import-error
# pylint: disable=wrong-import-position
import functools
import math
import multiprocessing as mp
import os
import re
import string
import sys
import time
from collections import Counter, deque
import heapq
from enum import Enum
from struct import pack

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
print(FILE_DIR)
sys.path.insert(0, FILE_DIR + "/../")
sys.path.insert(0, FILE_DIR + "/../../")
from common.utils import execute_day, read_input  # NOQA: E402
# pylint: enable=unused-import
# pylint: enable=import-error
# pylint: enable=wrong-import-position

""" DAY 1 """

def day1_calc_fuel(mod):
    return math.floor(mod / 3) - 2

def day1_1(data):
    return functools.reduce(lambda a, v: a+v, [day1_calc_fuel(int(m)) for m in data])

def day1_2(data):
    total = 0
    for mod_s in data:
        mod = int(mod_s)
        temp_fuel = day1_calc_fuel(mod)
        while temp_fuel > 0:
            total += temp_fuel
            temp_fuel = day1_calc_fuel(temp_fuel)
    return total

""" DAY 2 """

def day2_execute(op, pc, insts):
    if op == 1:
        a = insts[pc+1]
        b = insts[pc+2]
        c = insts[pc+3]
        insts[c] = insts[a] + insts[b]
        return (pc + 4, insts)
    elif op == 2:
        a = insts[pc+1]
        b = insts[pc+2]
        c = insts[pc+3]
        insts[c] = insts[a] * insts[b]
        return (pc + 4, insts)
    raise NotImplementedError

def day2_run_program(insts):
    pc = 0
    while insts[pc] != 99:
        op = insts[pc]
        (pc, insts) = day2_execute(op, pc, insts)
    return insts

def day2_1(data):
    data = data[0].split(',')
    #data = read_input(2019, 201)[0].split(',')
    data = [int(x) for x in data]
    data[1] = 12
    data[2] = 2
    return day2_run_program(data)[0]

def day2_2(data):
    data = data[0].split(',')
    backup = [int(x) for x in data]
    for i in range(99):
        for j in range(99):
            data = [int(x) for x in backup]
            data[1] = i
            data[2] = j
            result = day2_run_program(data)
            if result[0] == 19690720:
                return 100 * result[1] + result[2]

def day3_get_dir(dir):
    ori = dir[0]
    amount = int(dir[1:])
    if ori == 'L':
        return (-1, 0, amount)
    elif ori == 'R':
        return (1, 0, amount)
    elif ori == 'U':
        return (0, -1, amount)
    else:
        return (0, 1, amount)

def day3_solve_wire(map, path, char):
    x, y = (0, 0)
    steps = 0
    for dir in path:
        dx, dy, amount = day3_get_dir(dir)
        for i in range(0, amount):
            steps += 1
            newx = x + dx
            newy = y + dy
            coord = str(newx) + "," + str(newy)
            if coord in map:
                v = map[coord]
                if char == 'A':
                    v = (v[0], steps, v[2])
                else:
                    v = (v[0], v[1], steps)
                if v[0] != char:
                    map[coord] = ('X', v[1], v[2])
            else:
                v = (char, 0, 0)
                if char == 'A':
                    v = (v[0], steps, v[2])
                else:
                    v = (v[0], v[1], steps)
                map[coord] = v 
            x, y = (newx, newy)
            #print(dir)
            #print(coord)

def day3_1(data):
    #data = read_input(2019, 301)
    data1 = data[0].split(",")
    data2 = data[1].split(",")
    map = {}
    day3_solve_wire(map, data1, 'A')
    day3_solve_wire(map, data2, 'B')
    m = -1
    for k in map:
        if map[k][0] == 'X':
            parts = k.split(',')
            t = abs(int(parts[0])) + abs(int(parts[1]))
            print(t)
            print("---")
            v = map[k][1] + map[k][2]
            if v < m or m == -1:
                m = v
    print(m)

    return 0

""" MAIN FUNCTION """

def main(specific_day):
    initial_day = 1
    end_day = 25
    if specific_day is not None:
        initial_day = specific_day
        end_day = specific_day

    for day in range(initial_day, end_day + 1):
        execute_day(globals(), 2019, day, 1)
        execute_day(globals(), 2019, day, 2)

if __name__ == "__main__":
    start_day = None
    if len(sys.argv) > 1:
        try:
            if len(sys.argv) > 2:
                raise ValueError
            start_day = int(sys.argv[1])
        except ValueError:
            print("Usage: adventOfCode.py [<day>]")
            sys.exit(1)
    main(start_day)
