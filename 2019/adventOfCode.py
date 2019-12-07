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

def day5_mode(insts, v, mode):
    if mode == 0:
        return insts[v]
    if mode == 1:
        return v
    raise NotImplementedError

def day2_execute(op, pc, insts, inputs=None, outputs=None):
    if inputs is None:
        inputs = []
    if outputs is None:
        outputs = []
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
        insts[c] = day5_mode(insts, a, a_mode) + day5_mode(insts, b, b_mode)
        return (pc + 4, insts)
    elif op == 2:
        a = insts[pc + 1]
        b = insts[pc + 2]
        c = insts[pc + 3]
        a_mode = modes % 10
        modes = modes // 10
        b_mode = modes % 10
        modes = modes // 10
        insts[c] = day5_mode(insts, a, a_mode) * day5_mode(insts, b, b_mode)
        return (pc + 4, insts)
    elif op == 3:
        a = insts[pc + 1]
        insts[a] = inputs.pop()
        return (pc + 2, insts)
    elif op == 4:
        a = insts[pc + 1]
        a_mode = modes % 10
        modes = modes // 10
        outputs.append(day5_mode(insts, a, a_mode))
        return (pc + 2, insts)
    elif op == 5:
        a = insts[pc + 1]
        b = insts[pc + 2]
        a_mode = modes % 10
        modes = modes // 10
        b_mode = modes % 10
        modes = modes // 10
        val = day5_mode(insts, a, a_mode)
        if val != 0:
            pc = day5_mode(insts, b, b_mode)
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
        val = day5_mode(insts, a, a_mode)
        if val == 0:
            pc = day5_mode(insts, b, b_mode)
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
        val1 = day5_mode(insts, a, a_mode)
        val2 = day5_mode(insts, b, b_mode)
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
        val1 = day5_mode(insts, a, a_mode)
        val2 = day5_mode(insts, b, b_mode)
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
    # data = read_input(2019, 201)[0].split(',')
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
    # data = read_input(2019, 301)
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
    # data = read_input(2019, 501)[0].split(',')
    data = [int(x) for x in data]
    return day5_run_program(data, [1])[-1]

def day5_2(data):
    data = data[0].split(',')
    # data = read_input(2019, 501)[0].split(',')
    data = [int(x) for x in data]
    return day5_run_program(data, [5])[0]

""" DAY 6 """

def day6_get_orbits(data):
    orbits = {}
    is_orbited_by = {}
    for line in data:
        orbited_obj = line[0]
        orbits_obj = line[1]
        orbits_val = []
        if orbits_obj in orbits:
            orbits_val = orbits[orbits_obj]
        is_orbited_val = []
        if orbited_obj in is_orbited_by:
            is_orbited_val = is_orbited_by[orbited_obj]
        is_orbited_val.append(orbits_obj)
        orbits_val.append(orbited_obj)
        orbits[orbits_obj] = orbits_val
        is_orbited_by[orbited_obj] = is_orbited_val
    return (orbits, is_orbited_by)

def day6_part1(data):
    orbits, _ = day6_get_orbits(data)
    total_orbits = 0
    visited = {obj: False for obj in orbits}
    # COM is the only one that doesn't orbit
    visited["COM"] = False
    for obj in orbits:
        for obj_key in visited.keys():
            visited[obj_key] = False
        queue = [obj]
        count = 0
        while queue:
            curr = queue.pop()
            if curr == "COM":
                # COM is the only one that doesn't orbit
                continue
            visited[obj] = True
            for next_obj in orbits[curr]:
                if not visited[next_obj]:
                    queue.append(next_obj)
                    count += 1
        total_orbits += count
    return total_orbits

def day6_part2(data):
    orbits, is_orbited_by = day6_get_orbits(data)
    visited = {obj: sys.maxsize for obj in orbits}
    # COM is the only one that doesn't orbit
    visited['COM'] = sys.maxsize
    queue = []
    heapq.heappush(queue, (0, 'YOU'))
    count = 0
    while queue:
        s, curr = heapq.heappop(queue)
        if curr == "SAN":
            # Don't count the first and last hops
            return s - 2
        if visited[curr] > s:
            visited[curr] = s
        if curr in orbits:
            for next_orb in orbits[curr]:
                if visited[next_orb] >= s:
                    heapq.heappush(queue, (s + 1, next_orb))
        if curr in is_orbited_by:
            for prev_orb in is_orbited_by[curr]:
                if visited[prev_orb] >= s:
                    heapq.heappush(queue, (s + 1, prev_orb))
    raise AssertionError

def day6_1(data):
    # data = read_input(2019, 601)
    data = [l.split(')') for l in data]
    return day6_part1(data)

def day6_2(data):
    # data = read_input(2019, 601)
    data = [l.split(')') for l in data]
    return day6_part2(data)

""" DAY 7 """

def t(insts, max_cpus, phases):
    progs = {p:(False, 0, [i for i in insts], [phases[p]], []) for p in range(0, max_cpus)}
    progs[0][3].append(0)
    curr = 0
    while not all([finished for finished, _, _, _, _ in progs.values()]):
        f, pc, insts, inputs, outputs = progs[curr]
        next_p = (curr+1) % max_cpus
        if f:
            curr = next_p
        if not f:
            try:
                (pc, insts) = day2_execute(insts[pc], pc, insts, inputs, outputs)
                if outputs:
                    f, p, i, ii, o = progs[next_p]
                    progs[next_p][3].append(outputs.pop())
                progs[curr] = (insts[pc] == 99, pc, insts, inputs, outputs)
            except IndexError:
                curr = next_p
    return progs


def r(back, phases, max_val):
    inputs = []
    outputs = [0]
    print(phases)
    for i in range(0, max_val):
        insts = [k for k in back]
        inputs = [phases[i], outputs[0]]
        outputs = []    
        pc = 0
        while insts[pc] != 99:
            op = insts[pc]
            (pc, insts) = day2_execute(op, pc, insts, inputs, outputs)
    return outputs[0]

def day7_1(data):
    # data = read_input(2019, 701)
    data = data[0].split(",")
    data = [int(j) for j in data]
    backup = [k for k in data]
    max_val = 4+1
    res = []
    from itertools import permutations
    perm = permutations(range(0, max_val)) 
    #for i,j,k,l,m in list(perm):
    i=4
    j=3
    k=2
    l=1
    m=0

    print([i,j,k,l,m])
    ps = t(backup, max_val, [i,j,k,l,m])
    print(ps[0][3][-1])
    res.append(ps[0][3][-1])

    return max(res)

def day7_2(data):
    # data = read_input(2019, 701)
    return None

""" MAIN FUNCTION """

if __name__ == "__main__":
    main(["", "7"], globals(), 2019)
