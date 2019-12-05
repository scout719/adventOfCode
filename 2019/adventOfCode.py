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
from enum import IntEnum
from struct import pack

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
print(FILE_DIR)
sys.path.insert(0, FILE_DIR + "/../")
sys.path.insert(0, FILE_DIR + "/../../")
from common.utils import execute_day, read_input, main  # NOQA: E402
# pylint: enable=unused-import
# pylint: enable=import-error
# pylint: enable=wrong-import-position

""" DAY 1 """

def day1_calc_fuel(mod):
    return math.floor(mod / 3) - 2

def day1_1(data):
    return functools.reduce(lambda a, v: a + v, [day1_calc_fuel(int(m)) for m in data])

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

# Intcode computer code

def day5_read(insts, v, mode):
    if mode == 0:
        return insts[v]
    if mode == 1:
        return v

def day2_execute(op, pc, insts, inputs=[], outputs=[]):
    modes = op // 100
    op = op % 100
    if op == 1:
        a = insts[pc + 1]
        b = insts[pc + 2]
        c = insts[pc + 3]
        a_mode = modes % 10
        modes = modes // 10
        b_mode = modes % 10
        modes = modes // 10
        insts[c] = day5_read(insts, a, a_mode) + day5_read(insts, b, b_mode)
        return (pc + 4, insts)
    elif op == 2:
        a = insts[pc + 1]
        b = insts[pc + 2]
        c = insts[pc + 3]
        a_mode = modes % 10
        modes = modes // 10
        b_mode = modes % 10
        modes = modes // 10
        insts[c] = day5_read(insts, a, a_mode) * day5_read(insts, b, b_mode)
        return (pc + 4, insts)
    elif op == 3:
        a = insts[pc + 1]
        insts[a] = inputs.pop()
        return (pc + 2, insts)
    elif op == 4:
        a = insts[pc + 1]
        a_mode = modes % 10
        modes = modes // 10
        outputs.append(day5_read(insts, a, a_mode))
        return (pc + 2, insts)
    elif op == 5:
        a = insts[pc + 1]
        b = insts[pc + 2]
        a_mode = modes % 10
        modes = modes // 10
        b_mode = modes % 10
        modes = modes // 10
        val = day5_read(insts, a, a_mode)
        if val != 0:
            pc = day5_read(insts, b, b_mode)
        else:
            pc = pc + 3
        return (pc, insts)
    elif op == 6:
        a = insts[pc + 1]
        b = insts[pc + 2]
        a_mode = modes % 10
        modes = modes // 10
        b_mode = modes % 10
        modes = modes // 10
        val = day5_read(insts, a, a_mode)
        if val == 0:
            pc = day5_read(insts, b, b_mode)
        else:
            pc = pc + 3
        return (pc, insts)
    elif op == 7:
        a = insts[pc + 1]
        b = insts[pc + 2]
        c = insts[pc + 3]
        a_mode = modes % 10
        modes = modes // 10
        b_mode = modes % 10
        modes = modes // 10
        val1 = day5_read(insts, a, a_mode)
        val2 = day5_read(insts, b, b_mode)
        if val1 < val2:
            insts[c] = 1
        else:
            insts[c] = 0
        return (pc + 4, insts)
    elif op == 8:
        a = insts[pc + 1]
        b = insts[pc + 2]
        c = insts[pc + 3]
        a_mode = modes % 10
        modes = modes // 10
        b_mode = modes % 10
        modes = modes // 10
        val1 = day5_read(insts, a, a_mode)
        val2 = day5_read(insts, b, b_mode)
        if val1 == val2:
            insts[c] = 1
        else:
            insts[c] = 0
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

""" DAY 2 """

def day3_get_delta(move):
    orientation = move[0]
    amount = int(move[1:])
    if orientation == 'L':
        return (-1, 0, amount)
    elif orientation == 'R':
        return (1, 0, amount)
    elif orientation == 'U':
        return (0, -1, amount)
    else:
        return (0, 1, amount)

def day3_solve_wire(wires_map, path, char):
    x, y = (0, 0)
    steps = 0
    for move in path:
        dx, dy, amount = day3_get_delta(move)
        for _ in range(0, amount):
            steps += 1
            newx, newy = (x + dx, y + dy)
            coord = str(newx) + "," + str(newy)
            value = (char, 0, 0)
            if coord in wires_map:
                value = wires_map[coord]
                if value[0] != char:
                    value = ('X', value[1], value[2])
            if char == 'A':
                value = (value[0], steps, value[2])
            else:
                value = (value[0], value[1], steps)
            wires_map[coord] = value
            x, y = (newx, newy)

def day3_fill_map(data, wires_map):
    #data = read_input(2019, 301)
    data1 = data[0].split(",")
    data2 = data[1].split(",")
    day3_solve_wire(wires_map, data1, 'A')
    day3_solve_wire(wires_map, data2, 'B')

def day3_1(data):
    wires_map = {}
    day3_fill_map(data, wires_map)
    min_dist = -1
    for k in wires_map:
        if wires_map[k][0] == 'X':
            parts = k.split(',')
            curr_dist = abs(int(parts[0])) + abs(int(parts[1]))
            if curr_dist < min_dist or min_dist == -1:
                min_dist = curr_dist
    return min_dist

def day3_2(data):
    wires_map = {}
    day3_fill_map(data, wires_map)
    min_steps = -1
    for k in wires_map:
        if wires_map[k][0] == 'X':
            curr_steps = wires_map[k][1] + wires_map[k][2]
            if curr_steps < min_steps or min_steps == -1:
                min_steps = curr_steps
    return min_steps

""" DAY 4 """

def day4_is_valid(password, part2=False):
    leftfover = password
    prev_digit = password % 10
    leftfover = password // 10
    has_double = False
    repeat_count = 1
    is_decreasing = True
    while leftfover > 0:
        digit = leftfover % 10
        if digit == prev_digit:
            repeat_count += 1
            if not part2:
                has_double = True
        elif digit > prev_digit:
            is_decreasing = False
            break
        else:
            if repeat_count == 2:
                has_double = True
            repeat_count = 1
        prev_digit = digit
        leftfover = leftfover // 10
    if repeat_count == 2:
        has_double = True
    return has_double and is_decreasing

def day4_next_value(curr):
    value = str(curr)
    size = len(value)
    new_value = [int(value[i]) for i in range(0, size)]
    pos = 1
    has_increased = False
    should_increase = False
    while pos < size:
        if should_increase:
            new_value[pos] = (new_value[pos] + 1) % 10
            if pos != size - 1:
                new_value[pos + 1] = new_value[pos]
            if new_value[pos] == 0:
                should_increase = True
                pos -= 1
            else:
                should_increase = False
            continue

        if pos == 0:
            pos += 1
            continue

        if new_value[pos] >= new_value[pos - 1]:
            if pos == size - 1 and not has_increased:
                has_increased = True
                should_increase = True
            else:
                pos += 1
        else:
            has_increased = True
            should_increase = True
    return int("".join([str(i) for i in new_value]))

def day4_1(data):
    low = int(data[0].split('-')[0])
    high = int(data[0].split('-')[1])
    count = 0
    curr = low
    while curr <= high:
        if day4_is_valid(curr):
            count += 1
        curr = day4_next_value(curr)
    return count

def day4_2(data):
    low = int(data[0].split('-')[0])
    high = int(data[0].split('-')[1])
    count = 0
    curr = low
    while curr <= high:
        if day4_is_valid(curr, part2=True):
            count += 1
        curr = day4_next_value(curr)
    return count

""" DAY 5 """

def day5_run_program(insts, inputs):
    pc = 0
    outputs = []
    while insts[pc] != 99:
        op = insts[pc]
        (pc, insts) = day2_execute(op, pc, insts, inputs, outputs)
    return outputs

def day5_1(data):
    data = data[0].split(',')
    #data = read_input(2019, 501)[0].split(',')
    data = [int(x) for x in data]
    return day5_run_program(data, [1])[-1]

def day5_2(data):
    data = data[0].split(',')
    #data = read_input(2019, 501)[0].split(',')
    data = [int(x) for x in data]
    return day5_run_program(data, [5])[0]

""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2019)
