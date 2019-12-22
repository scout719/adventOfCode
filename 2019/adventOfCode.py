# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=wrong-import-position
import _functools
import math
import os
import sys
import time
from _collections import defaultdict
from heapq import *
import copy

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
print(FILE_DIR)
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
sys.path.insert(0, FILE_DIR + "/../../")
from common.utils import read_input, main, clear  # NOQA: E402
from icComputer import ic_execute  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

WHITE_SQUARE = "█"
WHITE_CIRCLE = "•"
BLUE_CIRCLE = f"{bcolors.OKBLUE}{bcolors.BOLD}•{bcolors.ENDC}"
RED_SMALL_SQUARE = f"{bcolors.FAIL}{bcolors.BOLD}■{bcolors.ENDC}"

""" DAY 1 """

def day1_calc_fuel(mod):
    return math.floor(mod / 3) - 2

def day1_1(data):
    return _functools.reduce(lambda a, v: a + v, [day1_calc_fuel(int(m)) for m in data])

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

def day5_mode(insts, v, mode, rel_base=0, to_write=False):
    if to_write:
        return v + (rel_base if mode == 2 else 0)
    if mode == 1:
        return v
    else:
        return insts[v + (rel_base if mode == 2 else 0)]
    raise NotImplementedError

def day2_execute(op, pc, insts, inputs=None, outputs=None, rel_base=0, get_input=None):
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
        c_mode = modes % 10
        modes = modes // 10
        c = day5_mode(insts, c, c_mode, rel_base, True)
        insts[c] = day5_mode(insts, a, a_mode, rel_base) + \
            day5_mode(insts, b, b_mode, rel_base)
        return (pc + 4, insts, rel_base)
    elif op == 2:
        a = insts[pc + 1]
        b = insts[pc + 2]
        c = insts[pc + 3]
        a_mode = modes % 10
        modes = modes // 10
        b_mode = modes % 10
        modes = modes // 10
        c_mode = modes % 10
        modes = modes // 10
        c = day5_mode(insts, c, c_mode, rel_base, True)
        insts[c] = day5_mode(insts, a, a_mode, rel_base) * \
            day5_mode(insts, b, b_mode, rel_base)
        return (pc + 4, insts, rel_base)
    elif op == 3:
        a = insts[pc + 1]
        a_mode = modes % 10
        modes = modes // 10
        a = day5_mode(insts, a, a_mode, rel_base, True)
        if not get_input is None:
            inputs.append(get_input())
        insts[a] = inputs.pop(0)
        return (pc + 2, insts, rel_base)
    elif op == 4:
        a = insts[pc + 1]
        a_mode = modes % 10
        modes = modes // 10
        outputs.append(day5_mode(insts, a, a_mode, rel_base))
        return (pc + 2, insts, rel_base)
    elif op == 5:
        a = insts[pc + 1]
        b = insts[pc + 2]
        a_mode = modes % 10
        modes = modes // 10
        b_mode = modes % 10
        modes = modes // 10
        val = day5_mode(insts, a, a_mode, rel_base)
        if val != 0:
            pc = day5_mode(insts, b, b_mode, rel_base)
        else:
            pc = pc + 3
        return (pc, insts, rel_base)
    elif op == 6:
        a = insts[pc + 1]
        b = insts[pc + 2]
        a_mode = modes % 10
        modes = modes // 10
        b_mode = modes % 10
        modes = modes // 10
        val = day5_mode(insts, a, a_mode, rel_base)
        if val == 0:
            pc = day5_mode(insts, b, b_mode, rel_base)
        else:
            pc = pc + 3
        return (pc, insts, rel_base)
    elif op == 7:
        a = insts[pc + 1]
        b = insts[pc + 2]
        c = insts[pc + 3]
        a_mode = modes % 10
        modes = modes // 10
        b_mode = modes % 10
        modes = modes // 10
        c_mode = modes % 10
        modes = modes // 10
        c = day5_mode(insts, c, c_mode, rel_base, True)
        val1 = day5_mode(insts, a, a_mode, rel_base)
        val2 = day5_mode(insts, b, b_mode, rel_base)
        if val1 < val2:
            insts[c] = 1
        else:
            insts[c] = 0
        return (pc + 4, insts, rel_base)
    elif op == 8:
        a = insts[pc + 1]
        b = insts[pc + 2]
        c = insts[pc + 3]
        a_mode = modes % 10
        modes = modes // 10
        b_mode = modes % 10
        modes = modes // 10
        c_mode = modes % 10
        modes = modes // 10
        c = day5_mode(insts, c, c_mode, rel_base, True)
        val1 = day5_mode(insts, a, a_mode, rel_base)
        val2 = day5_mode(insts, b, b_mode, rel_base)
        if val1 == val2:
            insts[c] = 1
        else:
            insts[c] = 0
        return (pc + 4, insts, rel_base)
    elif op == 9:
        a = insts[pc + 1]
        a_mode = modes % 10
        val1 = day5_mode(insts, a, a_mode, rel_base)
        rel_base += val1
        return (pc + 2, insts, rel_base)
    raise NotImplementedError

def day2_run_program(insts):
    pc = 0
    while insts[pc] != 99:
        op = insts[pc]
        (pc, insts, _) = day2_execute(op, pc, insts)
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
        (pc, insts, _) = day2_execute(op, pc, insts, inputs, outputs)
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
    heappush(queue, (0, 'YOU'))
    count = 0
    while queue:
        s, curr = heappop(queue)
        if curr == "SAN":
            # Don't count the first and last hops
            return s - 2
        if visited[curr] > s:
            visited[curr] = s
        if curr in orbits:
            for next_orb in orbits[curr]:
                if visited[next_orb] >= s:
                    heappush(queue, (s + 1, next_orb))
        if curr in is_orbited_by:
            for prev_orb in is_orbited_by[curr]:
                if visited[prev_orb] >= s:
                    heappush(queue, (s + 1, prev_orb))
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

def day7_multiple_cpus(original_prog, max_cpus, phases):
    progs = {p: (False, 0, [i for i in original_prog],
                 [phases[p]], []) for p in range(0, max_cpus)}
    # Input for first cpus is 0
    progs[0][3].append(0)
    curr_cpu = 0
    while not all([finished for finished, _, _, _, _ in progs.values()]):
        ended, pc, insts, inputs, outputs = progs[curr_cpu]
        next_cpu = (curr_cpu + 1) % max_cpus
        if ended:
            curr_cpu = next_cpu
        if not ended:
            try:
                (pc, insts, _) = day2_execute(
                    insts[pc], pc, insts, inputs, outputs)
                if outputs:
                    progs[next_cpu][3].append(outputs.pop())
                progs[curr_cpu] = (insts[pc] == 99, pc, insts, inputs, outputs)
            except IndexError:
                # If there was an error the program is waiting for an input not available yet
                curr_cpu = next_cpu
    return progs

def day7_solve(prog, start_phase, total_amps):
    max_val = total_amps
    res = []
    from itertools import permutations
    perm = permutations(range(0 + start_phase, max_val + start_phase))
    for phase_config in list(perm):
        amps_states = day7_multiple_cpus(prog, max_val, phase_config)
        res.append(amps_states[0][3][-1])

    return max(res)

def day7_1(data):
    #data = read_input(2019, 701)
    data = data[0].split(",")
    data = [int(j) for j in data]
    return day7_solve(data, 0, 5)

def day7_2(data):
    # data = read_input(2019, 701)
    data = data[0].split(",")
    data = [int(j) for j in data]
    return day7_solve(data, 5, 5)

""" DAY 8 """

def day8_get_layers(data, width, height):
    layers = {}
    curr_layer = 0
    while curr_layer * width * height < len(data):
        layers[curr_layer] = {}
        for y in range(height):
            for x in range(width):
                pos = width * height * curr_layer + width * y + x
                layers[curr_layer][(x, y)] = data[pos]
        curr_layer += 1
    return layers

def day8_count_values(layers, layer):
    return functools.reduce(lambda a, k:
                            (a[0] + (1 if layers[layer][k] == 0 else 0),
                             a[1] + (1 if layers[layer][k] == 1 else 0),
                             a[2] + (1 if layers[layer][k] == 2 else 0)),
                            layers[layer], (0, 0, 0))

def day8_get_image(stack):
    image = ""
    for coord in stack:
        x, y = coord
        if x == 0:
            image += "\n"
        if stack[(x, y)] == 2:
            image += "#"
        elif stack[(x, y)] == 1:
            image += WHITE_SQUARE
        elif stack[(x, y)] == 0:
            image += " "
    return image

def day8_1(data):
    #data = read_input(2019, 801)
    data = [int(k) for k in data[0]]
    width = 25
    height = 6
    layers = day8_get_layers(data, width, height)
    values_count = {}
    for layer in layers:
        values_count[layer] = day8_count_values(layers, layer)
    min_layer = 0
    for layer in values_count:
        if values_count[layer][0] < values_count[min_layer][0]:
            min_layer = layer
    return values_count[min_layer][1] * values_count[min_layer][2]

def day8_2(data):
    #data = read_input(2019, 801)
    data = [int(k) for k in data[0]]
    width = 25
    height = 6
    layers = day8_get_layers(data, width, height)
    stack = {coord: 2 for coord in layers[0]}
    for layer in layers:
        for coord in layers[0]:
            if stack[coord] == 2:
                stack[coord] = layers[layer][coord]
                if False and stack[coord] != 2:
                    image = day8_get_image(stack)
                    clear()
                    print(image)
                    time.sleep(.05)

    return day8_get_image(stack)

""" DAY 9 """

def int_run(insts, inputs):
    pc = 0
    rel_base = 0
    outputs = []
    while insts[pc] != 99:
        op = insts[pc]
        (pc, insts, rel_base) = day2_execute(
            op, pc, insts, inputs, outputs, rel_base)
    return outputs

def day9_1(data):
    #data = read_input(2019,901)
    data = [int(k) for k in data[0].split(",")]
    data = [data[i] if i < len(data) else 0 for i in range(100000)]
    return int_run(data, [1])[0]

def day9_2(data):
    #data = read_input(2019,901)
    data = [int(k) for k in data[0].split(",")]
    data = [data[i] if i < len(data) else 0 for i in range(100000)]
    return int_run(data, [2])[0]

""" DAY 10 """

def day10_1(data):
    #data = read_input(2019,1001)
    asteroids_counts = {}
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == "#":
                asteroids_counts[(x, y)] = 0
    keys = asteroids_counts.keys()
    for key in keys:
        x1, y1 = key
        slopes = set()
        for key2 in keys:
            x2, y2 = key2
            if key != key2:
                slope = math.inf
                if y2 != y1:
                    slope = (x2 - x1) / (y2 - y1)
                y_dir = "+" if y2 > y1 else "-"
                x_dir = "+" if x2 > x1 else "-"
                slopes.add((slope, x_dir, y_dir))
        asteroids_counts[key] = len(slopes)
    max_asteroids = -1
    max_key = (0, 0)
    for key in asteroids_counts:
        if asteroids_counts[key] > max_asteroids:
            max_asteroids = asteroids_counts[key]
            max_key = key
    return asteroids_counts[max_key]

def day10_measure_angle(origin_x, origin_y, p1_x, p1_y, p2_x, p2_y):
    # negate y since its axis is inverted
    vector1_x = p1_x - origin_x
    vector1_y = -p1_y - -origin_y
    vector2_x = p2_x - origin_x
    vector2_y = -p2_y - -origin_y

    dot_product = vector1_x * vector2_x + vector1_y * vector2_y
    determinant = -vector1_x * vector2_y + vector1_y * vector2_x
    angle = math.atan2(determinant, dot_product)
    # move angle to [0, 2*pi]
    angle = (angle + 2 * math.pi) % (2 * math.pi)
    return angle

def day10_2(data):
    origin_x = 28
    origin_y = 29
    #data = read_input(2019,1001)
    #origin_x = 11
    #origin_y = 13
    asteroids = []
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if x == origin_x and y == origin_y:
                continue
            if char == "#":
                # Angle to initial laser position
                angle = day10_measure_angle(
                    origin_x, origin_y, origin_x, 0, x, y)
                # Distance to laser's asteroid
                dist = math.sqrt(math.pow(x - origin_x, 2) +
                                 math.pow(y - origin_y, 2))
                asteroids.append((angle, dist, x, y))

    asteroids.sort()
    laser_angle = 2 * math.pi - 0.000000000000001
    count = 0
    last_hit = (0, 0)
    while count < 200:
        new_asts = [(
            angle - laser_angle if angle - laser_angle > 0 else math.pi * 2 + angle - laser_angle,
            dist,
            angle,
            x,
            y) for angle, dist, x, y in asteroids]
        _, dist, angle, x, y = min(new_asts)
        asteroids.remove((angle, dist, x, y))
        laser_angle = angle
        last_hit = (x, y)
        count += 1

    return last_hit[0] * 100 + last_hit[1]

""" DAY 11 """

def day11_get_turn(dx, dy, d):
    if d == 1:
        if dx == 0 and dy == -1:
            return (1, 0)
        if dx == 1 and dy == 0:
            return (0, 1)
        if dx == 0 and dy == 1:
            return (-1, 0)
        if dx == -1 and dy == 0:
            return (0, -1)
    if d == 0:
        if dx == 0 and dy == -1:
            return (-1, 0)
        if dx == 1 and dy == 0:
            return (0, -1)
        if dx == 0 and dy == 1:
            return (1, 0)
        if dx == -1 and dy == 0:
            return (0, 1)

def day11_run_robot(insts, inputs, panels):
    pc = 0
    rel_base = 0
    outputs = []
    x, y = (0, 0)
    dx, dy = (0, -1)
    is_paint = True
    while insts[pc] != 99:
        op = insts[pc]
        (pc, insts, rel_base) = day2_execute(
            op, pc, insts, inputs, outputs, rel_base)
        if outputs:
            if is_paint:
                is_paint = False
                color = outputs.pop(0)
                panels[(x, y)] = color
                # day11_print(m)
            else:
                is_paint = True
                rotation = outputs.pop(0)
                dx, dy = day11_get_turn(dx, dy, rotation)
                x += dx
                y += dy
                if (x, y) in panels:
                    inputs.append(panels[(x, y)])
                else:
                    inputs.append(0)

    return panels

def day11_print(panels, min_x=0, max_x=42, min_y=0, max_y=5, should_print=True):
    image = ""
    for y in range(min_y, max_y + 1):
        image += "\n"
        for x in range(min_x, max_x + 1):
            if (x, y) in panels and panels[(x, y)] == 1:
                image += WHITE_SQUARE
            else:
                image += " "
    if should_print:
        time.sleep(.05)
        clear()
        print(image)
    return image

def day11_1(data):
    data = [int(d) for d in data[0].split(",")]
    data = [data[i] if i < len(data) else 0 for i in range(10000)]

    panels = day11_run_robot(data, [0], {})
    return len(panels.keys())

def day11_2(data):
    data = [int(d) for d in data[0].split(",")]
    data = [data[i] if i < len(data) else 0 for i in range(10000)]

    panels = day11_run_robot(data, [1], {})
    positions = panels.keys()
    min_x = min([pos[0] for pos in positions])
    max_x = max([pos[0] for pos in positions])
    min_y = min([pos[1] for pos in positions])
    max_y = max([pos[1] for pos in positions])

    return day11_print(panels, min_x, max_x, min_y, max_y, should_print=False)

""" DAY 12 """

def day12_apply_gravity(moons, vels):
    for i, moon1 in enumerate(moons):
        for _, moon2 in enumerate(moons):
            for c, _ in enumerate(moon1):
                if moon1[c] < moon2[c]:
                    vels[i][c] += 1
                if moon1[c] > moon2[c]:
                    vels[i][c] -= 1

def day12_apply_velocity(moons, vels):
    for i, moon in enumerate(moons):
        for c, _ in enumerate(moon):
            moon[c] += vels[i][c]

def day12_1(data):
    #data = read_input(2019,1201)
    data = [l.lstrip("<").rstrip(">") for l in data]
    data = [l.split(", ") for l in data]
    moons = [[int(m[2:]) for m in l]for l in data]
    vels = [[0 for p in m] for m in moons]

    step = 0
    while step < 1000:
        step += 1
        day12_apply_gravity(moons, vels)
        day12_apply_velocity(moons, vels)
    total = 0
    for i in range(len(moons)):
        total += sum([abs(moons[i][c]) for c in range(len(moons[i]))]) * \
            sum([abs(vels[i][c]) for c in range(len(vels[i]))])
    return total

def day12_calc_cycles(moons, vels):
    count = 0
    seen = [set(), set(), set()]
    repeated = 0
    results = [0, 0, 0]
    while repeated < 3:
        state = [[], [], []]
        for i, moon in enumerate(moons):
            for c, _ in enumerate(moon):
                state[c].append(moon[c])
                state[c].append(vels[i][c])

        for c in range(3):
            if results[c] == 0:
                state_c = tuple(state[c])
                if state_c in seen[c]:
                    repeated += 1
                    results[c] = count
                else:
                    seen[c].add(state_c)
            if repeated == 3:
                return results

        day12_apply_gravity(moons, vels)
        day12_apply_velocity(moons, vels)
        count += 1

    return results

def day12_lcm(a, b):
    return a * b // math.gcd(a, b)

def day12_2(data):
    #data = read_input(2019,1201)
    data = [l.lstrip("<").rstrip(">") for l in data]
    data = [l.split(", ") for l in data]
    moons = [[int(m[2:]) for m in l]for l in data]
    vels = [[0 for p in m] for m in moons]

    return functools.reduce(day12_lcm, day12_calc_cycles(moons, vels))

""" DAY 13 """

# IntCode logic:
def ic_run_13(insts, inputs, grid=None):
    if grid is None:
        grid = []

    def calculate_input():
        # day13_print(grid)
        b_x, p_x = (0, 0)
        for line in grid:
            for x, tile in enumerate(line):
                if tile == 4:
                    b_x = x
                if tile == 3:
                    p_x = x
        return -1 if p_x > b_x else 1 if p_x < b_x else 0
    pc = 0
    rel_base = 0
    outputs = []
    score = 0
    while insts[pc] != 99:
        op = insts[pc]
        (pc, insts, rel_base) = day2_execute(
            op, pc, insts, inputs, outputs, rel_base, calculate_input)
        if grid and len(outputs) == 3:
            x = outputs.pop(0)
            y = outputs.pop(0)
            tile_id = outputs.pop(0)
            if x == -1 and y == 0:
                score = tile_id
            else:
                grid[y][x] = tile_id
    return outputs, score

def day13_print(grid):
    time.sleep(0.05)
    clear()
    for line in grid:
        for tile in line:
            if tile == 1:
                print(WHITE_SQUARE, end="")
            elif tile == 2:
                print("#", end="")
            elif tile == 3:
                print("_", end="")
            elif tile == 4:
                print("O", end="")
            else:
                print(" ", end="")
        print()

def day13_1(data):
    data = [int(d) for d in data[0].split(",")]
    for i in range(1000):
        data.append(0)
    results, _ = ic_run_13(data, [])
    i = 0
    count = 0
    while i < len(results):
        tile_id = results[i + 2]
        i += 3
        if tile_id == 2:
            count += 1
    return count

def day13_2(data):
    data = [int(d) for d in data[0].split(",")]
    for _ in range(1000):
        data.append(0)
    backup = data[:]
    grid = [[0 for j in range(40)] for i in range(22)]
    _, _ = ic_run_13(data, [], grid)

    data = backup
    data[0] = 2
    _, score = ic_run_13(data, [], grid)
    return score

""" DAY 14 """

def day14_parse_input(data):
    reactions = []
    for line in data:
        # Split requirements from reaction
        parts = line.split(" => ")
        reaction_parts = parts[1].split(" ")
        reaction_quantity = int(reaction_parts[0])
        reaction_chemical = reaction_parts[1]
        requirements = parts[0].split(", ")
        for i, requirement in enumerate(requirements):
            requirement_parts = requirement.split(" ")
            requirement_quantity = int(requirement_parts[0])
            requirement_chemical = requirement_parts[1]
            requirements[i] = (requirement_quantity, requirement_chemical)
        reactions.append(
            (requirements, (reaction_quantity, reaction_chemical)))

    reqs_map = {}
    for reqs, (quantity, chemical) in reactions:
        reqs_map[chemical] = (quantity, reqs)
    return reqs_map

def day14_produce_fuel(reqs_map, amount, leftovers):
    to_produce_amount = defaultdict(int)
    to_produce_amount["FUEL"] = amount
    ore_amount = 0
    while to_produce_amount:
        next_chemical = next(iter(to_produce_amount))
        next_quantity = to_produce_amount[next_chemical]
        del to_produce_amount[next_chemical]
        if next_quantity > leftovers[next_chemical]:
            next_quantity -= leftovers[next_chemical]
            leftovers[next_chemical] = 0
        else:
            leftovers[next_chemical] -= next_quantity
            continue
        (prod_quantity, requirements) = reqs_map[next_chemical]
        multiplier = math.ceil(next_quantity / prod_quantity)
        leftovers[next_chemical] += prod_quantity * multiplier - next_quantity

        for required_quantity, required_chemical in requirements:
            total_required_quantity = required_quantity * multiplier
            if required_chemical == "ORE":
                ore_amount += total_required_quantity
            else:
                to_produce_amount[required_chemical] += total_required_quantity

    return (ore_amount, leftovers)

def day14_1(data):
    # data = read_input(2019, 1401)
    reqs_map = day14_parse_input(data)
    ore_amount, _ = day14_produce_fuel(reqs_map, 1, defaultdict(int))
    return ore_amount

def day14_2(data):
    # data = read_input(2019, 1401)
    reqs_map = day14_parse_input(data)
    max_fuel = 0
    leftovers = defaultdict(int)
    leftovers["ORE"] = 1000000000000
    fuel_to_produce = leftovers["ORE"]
    while fuel_to_produce > 0:
        leftovers_backup = copy.deepcopy(leftovers)
        ore_amount, leftovers = day14_produce_fuel(
            reqs_map, fuel_to_produce, leftovers)
        leftovers["ORE"] -= ore_amount
        if leftovers["ORE"] > 0:
            max_fuel += fuel_to_produce
        elif leftovers["ORE"] < 0:
            leftovers = leftovers_backup
        fuel_to_produce = fuel_to_produce // 2
    return max_fuel

""" DAY 15 """

def day15_int_run(insts, pc, rel_base, curr_move):
    outputs = []
    move_comm = [1, 4, 2, 3]

    def calculate_input():
        return move_comm[curr_move]
    while insts[pc] != 99:
        op = insts[pc]
        (pc, insts, rel_base) = day2_execute(
            op, pc, insts, [], outputs, rel_base, calculate_input)
        if outputs:
            return outputs.pop(0), insts, pc, rel_base
    return outputs

def day15_discover(insts, stop_at_oxygen):
    curr_move = 0
    move_delta = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    x, y = (0, 0)
    steps = 0
    moves_made = defaultdict(set)
    grid = defaultdict(lambda: " ")
    unexplored = []
    heappush(unexplored, (steps, x, y, 0, insts[:], 0, 0))
    heappush(unexplored, (steps, x, y, 1, insts[:], 0, 0))
    heappush(unexplored, (steps, x, y, 2, insts[:], 0, 0))
    heappush(unexplored, (steps, x, y, 3, insts[:], 0, 0))
    oxygen_x, oxygen_y = 0, 0
    while unexplored:
        steps, x, y, curr_move, insts, pc, rel_base = heappop(unexplored)
        code, insts, pc, rel_base = day15_int_run(
            insts, pc, rel_base, curr_move)
        # grid2 = copy.deepcopy(grid)
        # grid2[(x,y)] = RED_SMALL_SQUARE
        # day15_print_grid(grid2)
        if code == 0:
            moves_made[(x, y)].add(curr_move)
            dx, dy = move_delta[curr_move]
            wall_x, wall_y = x + dx, y + dy
            grid[(wall_x, wall_y)] = WHITE_SQUARE
            continue
        else:
            dx, dy = move_delta[curr_move]
            x, y = x + dx, y + dy
            steps += 1
            moves_made[(x, y)].add((curr_move + 2) % 4)
            for move in range(0, 4):
                if not move in moves_made[(x, y)]:
                    heappush(unexplored, (-steps, x, y,
                                          move, insts[:], pc, rel_base))
            if code == 2:
                oxygen_x, oxygen_y = x, y
                if stop_at_oxygen:
                    return steps, grid, oxygen_x, oxygen_y

    return steps, grid, oxygen_x, oxygen_y

def day15_parse_input(data):
    data = [int(d) for d in data[0].split(",")]
    for _ in range(1000):
        data.append(0)
    return data

max_t = -1
def day15_print_grid(grid, t=None):
    global max_t
    if not t is None:
        if t <= max_t:
            return
        max_t = t
    time.sleep(0.01)
    s = ""
    for y in range(-21, 20):
        s += "\n"
        for x in range(-21, 20):
            s += grid[(x, y)]
    clear()
    print(s)

def day15_1(data):
    data = day15_parse_input(data)
    steps, _, _, _ = day15_discover(data, True)
    return steps

def day15_2(data):
    data = day15_parse_input(data)
    _, grid, oxygen_x, oxygen_y = day15_discover(data, False)
    unfilled = [(0, oxygen_x, oxygen_y)]
    filled = set([(oxygen_x, oxygen_y)])
    max_minute = set()
    while unfilled:
        minute, x, y = unfilled.pop(0)
        grid[(x, y)] = BLUE_CIRCLE
        # day15_print_grid(grid, minute)
        max_minute.add(minute)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if abs(dx) == abs(dy):
                    continue
                next_x = x + dx
                next_y = y + dy
                if grid[(next_x, next_y)] != WHITE_SQUARE and not (next_x, next_y) in filled:
                    filled.add((next_x, next_y))
                    unfilled.append((minute + 1, next_x, next_y))
    return max(max_minute)

""" DAY 16 """

def day16_parse_input(data):
    return [d for d in data[0]]

def day16_1(data):
    #data = read_input(2019, 1601)
    data = day16_parse_input(data)
    data = [int(d) for d in data]
    size = len(data)
    half_size = size // 2
    workspace = [data, [0 for _ in range(size)]]
    data_idx = 0
    result_idx = 1
    for _ in range(100):
        res_pos = 0
        while res_pos < size:
            workspace[result_idx][res_pos] = 0
            value = 0
            i = res_pos
            while i < size:
                if res_pos > half_size:
                    pattern_idx = 1
                else:
                    pattern_idx = ((i + 1) // (res_pos + 1)) % 4

                if pattern_idx == 1:
                    v = workspace[data_idx][i]
                    value += v
                elif pattern_idx % 2 == 0:
                    i += res_pos + 1
                    continue
                elif pattern_idx == 3:
                    v = workspace[data_idx][i]
                    value -= v
                i += 1
            workspace[result_idx][res_pos] = abs(value) % 10
            res_pos += 1

        data_idx = (data_idx + 1) % 2
        result_idx = (result_idx + 1) % 2
    return ''.join([str(d) for d in workspace[data_idx][:8]])

def day16_2(data):
    #data = read_input(2019, 1601)
    data = day16_parse_input(data)
    offset = int(''.join(data[0:7]))
    data = data * 10000
    data = [int(d) for d in data]
    size = len(data)
    workspace = [data, [0 for _ in range(size)]]
    data_idx = 0
    result_idx = 1
    for _ in range(100):
        res_pos = offset

        total_remaining = sum(workspace[data_idx][res_pos - 1:])
        i = res_pos
        while i < size:
            total_remaining = total_remaining - workspace[data_idx][i - 1]
            workspace[result_idx][i] = abs(total_remaining) % 10
            i += 1

        data_idx = (data_idx + 1) % 2
        result_idx = (result_idx + 1) % 2
    return ''.join([str(d) for d in workspace[data_idx][offset:offset + 8]])

""" DAY 17 """

def day17_parse_input(data):
    return [int(d) for d in data[0].split(",")]

def day17_is_scaff(x, y, grid):
    return y >= 0 and y < len(grid) and \
        x >= 0 and x < len(grid[y]) and \
        grid[y][x] != " "

def day17_get_grid(insts):
    output = int_run_17(insts, [])
    view = ""
    grid = [[]]
    for c in output:
        if c == 35:
            view += WHITE_SQUARE
            grid[-1].append(WHITE_SQUARE)
        elif c == 46:
            view += " "
            grid[-1].append(" ")
        elif c == 10:
            view += "\n"
            grid.append([])
        else:
            view += f"{bcolors.FAIL}{bcolors.BOLD}{chr(c)}{bcolors.ENDC}"
            grid[-1].append(chr(c))

    # print(view)
    return grid

def day17_1(data):
    #data = read_input(2019, 1701)
    data = day17_parse_input(data)
    output = int_run_17(data, [])
    view = ""
    grid = day17_get_grid(data)

    inters = 0
    for y, row in enumerate(grid):
        for x, pos in enumerate(row):
            if pos != " ":
                adjacents = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                if all([day17_is_scaff(a, b, grid) for a, b in adjacents]):
                    inters += x * y

    return inters

def day17_2(data):
    #data = read_input(2019, 1701)
    data = day17_parse_input(data)
    data_backup = data[:]
    output = int_run_17(data, [])
    view = ""
    grid = day17_get_grid(data)

    robot_pos = (0, 0)
    for y, row in enumerate(grid):
        for x, pos in enumerate(row):
            if grid[y][x] != ' ' and grid[y][x] != WHITE_SQUARE:
                robot_pos = (x, y)
                break
        if robot_pos != (0, 0):
            break

    seen = set()
    x, y = robot_pos
    path2 = []
    d = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    curr_d = 1
    d_s = ["L", "R"]
    moves = 0
    while True:
        new_x, new_y = [sum(i) for i in zip(*[(x, y), d[curr_d]])]
        if day17_is_scaff(new_x, new_y, grid):
            moves += 1
            x, y = new_x, new_y
        else:
            d_l = (curr_d - 1) % 4
            d_r = (curr_d + 1) % 4
            new_x_l, new_y_l = [sum(i) for i in zip(*[(x, y), d[d_l]])]
            new_x_r, new_y_r = [sum(i) for i in zip(*[(x, y), d[d_r]])]
            if day17_is_scaff(new_x_l, new_y_l, grid):
                if moves != 0:
                    path2.append(moves)
                path2.append("L")
                moves = 0
                curr_d = d_l
            elif day17_is_scaff(new_x_r, new_y_r, grid):
                if moves != 0:
                    path2.append(moves)
                path2.append("R")
                moves = 0
                curr_d = d_r
            else:
                if moves != 0:
                    path2.append(moves)
                break

    # [A  B B A  B C C B A]
    data = data_backup
    data[0] = 2
    # [A, B, B, A, C, B, C, C, B, A]
    # A R,10,R,8,L,10,L,10
    # B R,8,L,6,L,6
    # C L,10,R,10,L,6
    main = [ord(c)
            for c in "A|,|B|,|B|,|A|,|C|,|B|,|C|,|C|,|B|,|A".split("|")] + [10]
    A = f"{ord('R')}|{ord(',')}|{ord('1')}|{ord('0')}|{ord(',')}|{ord('R')}|{ord(',')}|{ord('8')}|{ord(',')}|{ord('L')}|{ord(',')}|{ord('1')}|{ord('0')}|{ord(',')}|{ord('L')}|{ord(',')}|{ord('1')}|{ord('0')}|10".split("|")
    B = f"{ord('R')}|{ord(',')}|{ord('8')}|{ord(',')}|{ord('L')}|{ord(',')}|{ord('6')}|{ord(',')}|{ord('L')}|{ord(',')}|{ord('6')}|10".split("|")
    C = f"{ord('L')}|{ord(',')}|{ord('1')}|{ord('0')}|{ord(',')}|{ord('R')}|{ord(',')}|{ord('1')}|{ord('0')}|{ord(',')}|{ord('L')}|{ord(',')}|{ord('6')}|10".split("|")
    response = f"{ord('n')}|10".split("|")
    main = [int(d) for d in main]
    A = [int(d) for d in A]
    B = [int(d) for d in B]
    C = [int(d) for d in C]
    response = [int(d) for d in response]

    def get_program():
        c = ""
        if len(main) > 0:
            c = main.pop(0)
        elif len(A) > 0:
            c = A.pop(0)
        elif len(B) > 0:
            c = B.pop(0)
        elif len(C) > 0:
            c = C.pop(0)
        else:
            c = response.pop(0)
        return c
    output = int_run_17(data, [], get_program)
    return output[-1]

# IntCode logic:
def int_run_17(insts, inputs, calculate_input=None):
    insts = [insts[i] if i < len(insts) else 0 for i in range(10000)]
    pc = 0
    rel_base = 0
    outputs = []
    while insts[pc] != 99:
        op = insts[pc]
        (pc, insts, rel_base) = ic_execute(
            op, pc, insts, inputs, outputs, rel_base, calculate_input)
    return outputs

""" DAY 18 """

""" DAY 19 """

def day19_parse_input(data):
    return [int(d) for d in data[0].split(",")]

def day19_1(data):
    #data = read_input(2019, 1901)
    data = day19_parse_input(data)
    grid = [[0 for _ in range(50)] for _ in range(50)]
    count = 0

    def get_next_input():
        return pos.pop(0)

    for x in range(50):
        for y in range(50):
            pos = [x, y]
            grid[y][x] = int_run_19(data, [], get_next_input)[-1]
            count += grid[y][x]

    return count

def day19_calc_dims(data, x, y):
    def get_next_input():
        return pos.pop(0)
    orig_x, orig_y = x, y

    pos = [x, y]
    while int_run_19(data, [], get_next_input)[-1] == 1:
        x += 1
        pos = [x, y]
    width = x - orig_x
    if(width >= 100):
        orig_x = x - 100
        width = 100

    pos = [orig_x, y]
    while int_run_19(data, [], get_next_input)[-1] == 1:
        y += 1
        pos = [orig_x, y]
    height = y - orig_y

    return height, width, orig_x, orig_y

def day19_2(data):
    #data = read_input(2019, 1901)
    data = day19_parse_input(data)
    count = 0

    def get_next_input():
        return pos.pop(0)

    queue = [(0, 0)]
    while queue:
        x, y = queue.pop(0)
        pos = [x, y]
        v = int_run_19(data, [], get_next_input)[-1]
        if v == 1:
            height, width, orig_x, orig_y = day19_calc_dims(data, x, y)
            if height == 100 and width == 100:
                return orig_x * 10000 + orig_y
            y += 100 - height
            pos = [x, y]
            while int_run_19(data, [], get_next_input)[-1] == 0:
                x += 1
                pos = [x, y]
            queue.append((x, y))

    return count

# IntCode logic:
def int_run_19(insts, inputs, calculate_input=None):
    insts = [insts[i] if i < len(insts) else 0 for i in range(10000)]
    pc = 0
    rel_base = 0
    outputs = []
    while not outputs or insts[pc] != 99:
        op = insts[pc]
        (pc, insts, rel_base) = ic_execute(
            op, pc, insts, inputs, outputs, rel_base, calculate_input)
    return outputs

""" DAY 20 """

def day20_1(data):
    #data = read_input(2019, 2001)

    grid = []
    for r, row in enumerate(data):
        grid.append([])
        for c, tile in enumerate(row):
            grid[-1].append(tile)

    R = len(grid)
    C = len(grid[0])
    x = 3
    while grid[R // 2][x] == "." or grid[R // 2][x] == "#":
        x += 1
    left = [(2, 2), (x - 1, R - 3)]
    while grid[R // 2][x] != "." and grid[R // 2][x] != "#":
        x += 1
    right = [(x, 2), (C - 3, R - 3)]
    y = 3
    while grid[y][C // 2] == "." or grid[y][C // 2] == "#":
        y += 1
    top = [(2, 2), (C - 3, y - 1)]
    while grid[y][C // 2] != "." and grid[y][C // 2] != "#":
        y += 1
    bottom = [(2, y), (C - 3, R - 3)]

    ileftc = left[1][0]
    irightc = right[0][0]
    itopr = top[1][1]
    ibottomr = bottom[0][1]

    portals = defaultdict(lambda: [])
    for r, row in enumerate(grid):
        for c, t in enumerate(row):
            if t == ".":
                if r == 2:
                    p = grid[r - 2][c] + grid[r - 1][c]
                    portals[p].append((r, c))
                if r == R - 3:
                    p = grid[R - 2][c] + grid[R - 1][c]
                    portals[p].append((r, c))
                if c == 2:
                    p = grid[r][c - 2] + grid[r][c - 1]
                    portals[p].append((r, c))
                if c == C - 3:
                    p = grid[r][C - 2] + grid[r][C - 1]
                    portals[p].append((r, c))
                if r == itopr:
                    p = grid[itopr + 1][c] + grid[itopr + 2][c]
                    portals[p].append((r, c))
                if r == ibottomr:
                    p = grid[ibottomr - 2][c] + grid[ibottomr - 1][c]
                    portals[p].append((r, c))
                if c == ileftc:
                    p = grid[r][ileftc + 1] + grid[r][ileftc + 2]
                    portals[p].append((r, c))
                if c == irightc:
                    p = grid[r][irightc - 2] + grid[r][irightc - 1]
                    portals[p].append((r, c))

    rportals = {}
    for key in portals:
        if key != "AA" and key != "ZZ":
            rportals[portals[key][0]] = key
            rportals[portals[key][1]] = key

    # del portals["##"]
    #del portals["  "]
    del portals[".."]
    del portals[".#"]
    del portals["#."]

    q = [(0, portals["AA"][0])]
    seen = {}
    D = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    while q:
        steps, pos = heappop(q)
        if pos in seen and seen[pos] < steps:
            continue
        r, c = pos
        if portals["ZZ"][0] == pos:
            return steps
        seen[pos] = steps
        for d in range(4):
            rr, cc = r + D[d][1], c + D[d][0]
            if grid[rr][cc] == ".":
                heappush(q, (steps + 1, (rr, cc)))
        if pos in rportals:
            p = rportals[pos]
            for rr, cc in portals[p]:
                if (rr, cc) != pos:
                    heappush(q, (steps + 1, (rr, cc)))

    print(portals["ZZ"])
    return None

def day20_2(data):
    # data = read_input(2019, 2002)

    grid = []
    for r, row in enumerate(data):
        grid.append([])
        for c, tile in enumerate(row):
            grid[-1].append(tile)

    R = len(grid)
    C = len(grid[0])
    x = 3
    while grid[R // 2][x] == "." or grid[R // 2][x] == "#":
        x += 1
    left = [(2, 2), (x - 1, R - 3)]
    while grid[R // 2][x] != "." and grid[R // 2][x] != "#":
        x += 1
    right = [(x, 2), (C - 3, R - 3)]
    y = 3
    while grid[y][C // 2] == "." or grid[y][C // 2] == "#":
        y += 1
    top = [(2, 2), (C - 3, y - 1)]
    while grid[y][C // 2] != "." and grid[y][C // 2] != "#":
        y += 1
    bottom = [(2, y), (C - 3, R - 3)]

    ileftc = left[1][0]
    irightc = right[0][0]
    itopr = top[1][1]
    ibottomr = bottom[0][1]

    portals = defaultdict(lambda: [])
    for r, row in enumerate(grid):
        for c, t in enumerate(row):
            if t == ".":
                if r == 2:
                    p = grid[r - 2][c] + grid[r - 1][c]
                    portals[p].append((r, c, 1))
                if r == R - 3:
                    p = grid[R - 2][c] + grid[R - 1][c]
                    portals[p].append((r, c, 1))
                if c == 2:
                    p = grid[r][c - 2] + grid[r][c - 1]
                    portals[p].append((r, c, 1))
                if c == C - 3:
                    p = grid[r][C - 2] + grid[r][C - 1]
                    portals[p].append((r, c, 1))
                if r == itopr:
                    p = grid[itopr + 1][c] + grid[itopr + 2][c]
                    portals[p].append((r, c, -1))
                if r == ibottomr:
                    p = grid[ibottomr - 2][c] + grid[ibottomr - 1][c]
                    portals[p].append((r, c, -1))
                if c == ileftc:
                    p = grid[r][ileftc + 1] + grid[r][ileftc + 2]
                    portals[p].append((r, c, -1))
                if c == irightc:
                    p = grid[r][irightc - 2] + grid[r][irightc - 1]
                    portals[p].append((r, c, -1))
    # del portals["##"]
    #del portals["  "]
    try:
        del portals[".."]
    except:
        pass
    try:
        del portals[".#"]
    except:
        pass
    try:
        del portals["#."]
    except:
        pass

    rportals = {}
    for key in portals:
        if key != "AA" and key != "ZZ":
            rportals[portals[key][0]] = key
            rportals[portals[key][1]] = key

    start = (portals["AA"][0][0], portals["AA"][0][1])
    end = (portals["ZZ"][0][0], portals["ZZ"][0][1])
    q = [(0, 0, start)]
    seen = {}
    D = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    while q:
        steps, depth, pos = heappop(q)
        seen[(pos, depth)] = steps
        r, c = pos
        if depth == 0 and end == pos:
            return steps
        if (r, c, -1) in rportals:
            p = rportals[(r, c, -1)]
            for rr, cc, d_p in portals[p]:
                if d_p == 1:
                    if ((rr, cc), depth - 1) in seen and seen[((rr, cc), depth - 1)] < steps + 1:
                        continue
                    heappush(q, (steps + 1, depth - 1,
                                 (rr, cc)))
        for d in range(4):
            rr, cc = r + D[d][1], c + D[d][0]
            if grid[rr][cc] == ".":
                if ((rr, cc), depth) in seen and seen[((rr, cc), depth)] < steps + 1:
                    continue
                heappush(q, (steps + 1, depth, (rr, cc)))
        if depth != 0:
            if (r, c, 1) in rportals:
                p = rportals[(r, c, 1)]
                for rr, cc, d_p in portals[p]:
                    if d_p == -1:
                        if ((rr, cc), depth + 1) in seen and seen[((rr, cc), depth + 1)] < steps + 1:
                            continue
                        heappush(q, (steps + 1, depth + 1,
                                     (rr, cc)))

""" DAY 21 """

def day21_parse_input(data):
    return [int(d) for d in data[0].split(",")]

def day21_1(data):
    data = day21_parse_input(data)
    program = [
        "NOT A J",

        "NOT C T",
        "AND D T",
        "OR T J",
        "WALK"
    ]
    program = [inst + chr(10) for inst in program]
    program = [ord(c) for inst in program for c in inst]

    def get_char():
        return program.pop(0)
    output = int_run_21(data, [], get_char)

    # print("".join([chr(o) for o in output[:-1]]))
    return output[-1]

def day21_2(data):
    data = day21_parse_input(data)
    cmd = [
        "NOT A J",
        "AND D J",

        "NOT C T",
        "AND D T",
        "AND H T",
        "OR T J",

        "NOT B T",
        "AND D T",
        "AND H T",
        "OR T J",

        "RUN"
    ]
    program = [inst + chr(10) for inst in program]
    program = [ord(c) for inst in program for c in inst]

    def get_char():
        return program.pop(0)
    output = int_run_21(data, [], get_char)

    # print("".join([chr(o) for o in output[:-1]]))
    return output[-1]

def int_run_21(insts, inputs, calculate_input=None):
    insts = [insts[i] if i < len(insts) else 0 for i in range(10000)]
    pc = 0
    rel_base = 0
    outputs = []
    while not outputs or insts[pc] != 99:
        op = insts[pc]
        (pc, insts, rel_base) = ic_execute(
            op, pc, insts, inputs, outputs, rel_base, calculate_input)
    return outputs

""" DAY 22 """


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2019)
