import re
re = re
import string
string = string
import sys
import functools
functools = functools
import os
os = os
file_dir = os.path.dirname(os.path.realpath(__file__))
import sys
sys.path.insert(0, file_dir + "\\..\\")
from common.utils import execute_day, read_input
from collections import deque
from collections import Counter
import multiprocessing as mp
mp = mp
import math
import time

start_day = 1

""" DAY 1 """

def day1_split_change(change):
    sign = change[0]
    value = int(change[1:])
    if sign == "+":
        return value
    else:
        return -value

def day1_1(data):
    frequency = 0
    for change in data:
        frequency += day1_split_change(change)
    return frequency

def day1_2(data):
    parsed_data = [day1_split_change(c) for c in data]
    frequency = 0
    found_frequencies = {"0": True}
    i = 0
    while True:
        frequency += parsed_data[i]
        key = str(frequency)
        if key in found_frequencies:
            return frequency
        else:
            found_frequencies[key] = True
        i+=1
        i = i % len(data)

""" DAY 2 """

def day2_sort_letters(box_id):
    letters = [l for l in box_id]
    return sorted(letters)

def day2_count_twice_thrice(box_id):
    sorted_letters = day2_sort_letters(box_id)
    counter = 0
    letter = ""
    has_twice = ""
    has_thrice = ""
    for curr_letter in sorted_letters:
        if letter == curr_letter:
            counter += 1
        else:
            if counter == 3:
                has_thrice = letter
            elif counter == 2:
                has_twice = letter
            letter = curr_letter
            counter = 1
    if counter == 3 and has_thrice == "":
        has_thrice = letter
    if counter == 2 and has_twice == "":
        has_twice = letter
    return (has_twice, has_thrice)

def day2_1(data):
    twice_counter = 0
    thrice_counter = 0
    for box_id in data:
        (twice, thrice) = day2_count_twice_thrice(box_id)
        if twice != "":
            twice_counter += 1
        if thrice != "":
            thrice_counter += 1
    return twice_counter * thrice_counter

def day2_letter_difference(box1, box2):
    if len(box1) != len(box2):
        raise ValueError("Boxes with different lengths: {0} & {1}".format(box1, box2))
    counter_diff = 0
    common_letters = ""
    for i in range(0, len(box1)):
        if box1[i] != box2[i]:
            counter_diff += 1
        else:
            common_letters += box1[i]
    return (counter_diff, common_letters)

def day2_2(data):
    for box_id1 in data:
        for box_id2 in data:
            (diff, letters) = day2_letter_difference(box_id1, box_id2)
            if diff == 1:
                return letters

""" DAY 3 """

def day3_build_fabric(size):
    return [[ 0 for y in range( size ) ] for x in range( size ) ]

def day3_process_claim(line):
    # #1 @ 1,3: 4x4
    return tuple([ int(x) for x in re.findall("#(\d+) @ (\d+),(\d+): (\d+)x(\d+)",line)[0]])

def day3_fill_claim(claim, fabric, size):
    (id_, left, top, width, height) = claim
    for i in range(width):
        for j in range(height):
            fabric[top + j][left + i] += 1

def day3_process_position(acc, pos):
    if pos > 1:
        return acc + 1
    return acc

def day3_process_row(acc, row):
    return functools.reduce(day3_process_position, row, acc)

def day3_1(data):
    size = 1000
    #data, size = (read_input(2018, 301), 8)
    fabric = day3_build_fabric(size)
    for claim in data:
        day3_fill_claim(day3_process_claim(claim), fabric, size)
    return functools.reduce(day3_process_row, fabric, 0)

def day3_check_prestine(claim, fabric):
    (id_, left, top, width, height) = claim
    for i in range(width):
        for j in range(height):
            if fabric[top + j][left + i] > 1:
                return ""
    return id_

def day3_2(data):
    size = 1000
    #data, size = (read_input(2018, 301), 8)
    fabric = day3_build_fabric(size)
    for claim in data:
        day3_fill_claim(day3_process_claim(claim), fabric, size)
    for claim in data:
        res = day3_check_prestine(day3_process_claim(claim), fabric)
        if res != "":
            return res

""" DAY 4 """

def day4_process_log(log):
    shift = re.findall("Guard #(\d+) begins shift",log)
    if len(shift) > 0:
        return ("shift", int(shift[0]))
    wake = re.findall("(wakes up)",log)
    if len(wake) > 0:
        return ("wake", 0)
    asleep = re.findall("(falls asleep)",log)
    if len(asleep) > 0:
        return ("asleep", 0)

def day4_parse_and_sort(data):
    # [1518-07-18 23:57] Guard #157 begins shift
    # [1518-04-18 00:44] wakes up
    # [1518-10-26 00:20] falls asleep
    parsed_data = [re.findall("\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.+)",line)[0] for line in data]
    parsed_data.sort(key=lambda elem : str(elem[1]) + str(elem[2] + str(elem[3]) + str(elem[4])))
    parsed_data = [tuple([int(log[0]), int(log[1]), int(log[2]), int(log[3]), int(log[4]), day4_process_log(log[5])]) for log in parsed_data]
    return parsed_data

def day4_process(data):
    ordered_log = day4_parse_and_sort(data)
    history = {}
    last_guard = -1
    last_asleep = -1
    sleeping = False
    curr_date = (0,0,0,0)
    for (year, month, day, hour, minute, log) in ordered_log:
        if log[0] == "shift":
            last_guard = log[1]
            if not last_guard in history:
                history[last_guard] = [0 for i in range(60)]
        elif log[0] == "wake":
            if sleeping:
                for i in range(last_asleep, minute):
                    history[last_guard][i] += 1
            sleeping = False
        elif log[0] == "asleep":
            sleeping = True
            last_asleep = minute
        curr_date = (month, day, hour, minute)
    return history

def day4_1(data):
    #data = read_input(2018, 401)
    history = day4_process(data)
    sleepiest_guard = sorted([(k, sum(v)) for k, v in history.items()], key=lambda elem: elem[1], reverse=True)[0][0]

    m = 0
    for i in range(60):
        if history[sleepiest_guard][i] > history[sleepiest_guard][m]:
            m = i
    return m * sleepiest_guard

def day4_2(data):
    #data = read_input(2018, 401)
    history = day4_process(data)
    sleepiest_guard = sorted([(k, max(v)) for k, v in history.items()], key=lambda elem: elem[1], reverse=True)[0][0]

    m = 0
    for i in range(60):
        if history[sleepiest_guard][i] > history[sleepiest_guard][m]:
            m = i
    return m * sleepiest_guard

""" DAY 5 """

def day5_should_destroy(first, second):
    return  first.lower() == second.lower() and first != second

def day5_colapse(polymer):
    new_polymer = list(polymer[:])
    i = 0
    while i < len(new_polymer) - 1:
        if day5_should_destroy(new_polymer[i], new_polymer[i+1]):
            del new_polymer[i]
            del new_polymer[i]
            i-=1
        else:
            i += 1
    return new_polymer

def day5_collapse_and_count(polymer):
    reduced_polymer = day5_colapse(polymer)
    return len(reduced_polymer)

def day5_1(data):
    #data = read_input(2018, 501)
    polymer = list(data[0])
    return day5_collapse_and_count(polymer)

def day5_remove_unit(polymer, letter):
    return [c for c in polymer if c != letter and c != letter.upper()]

def day5_2(data):
    #data = read_input(2018, 501)
    polymer = data[0]
    letters = list(string.ascii_lowercase)
    reduced_polymer = day5_colapse(list(polymer))
    min_val = sys.maxsize
    for letter in letters:
        temp_polymer = day5_remove_unit(reduced_polymer, letter)
        size = day5_collapse_and_count(temp_polymer)
        if size < min_val:
            min_val = size
    return min_val

""" DAY 6 """

def day6_debug_grid(grid):
    for row in grid:
        row_str = ""
        for pos in row:
            char = str(pos[0])
            if pos[1] == 0 and pos[0] != "_":
                char = chr(ord('A') + pos[0])
            row_str += " " + char
        print(row_str)
    print()

def day6_fill_grid(grid, coordinates):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            dists = [abs(coordinate[1]-i) + abs(coordinate[0]-j) for coordinate in coordinates]
            min_dist = 9999999999999
            min_id = 0
            for id in range(len(dists)):
                if dists[id] < min_dist:
                    min_id = id
                    min_dist = dists[id]
                elif dists[id] == min_dist:
                    min_id = "_"
                    min_dist = dists[id]
            grid[i][j] = (min_id, min_dist)

def day6_1(data):
    #data = read_input(2018, 601)
    coordinates = [(int(entry.split(", ")[0]), int(entry.split(", ")[1])) for entry in data]

    xs = [coordinate[0] for coordinate in coordinates]
    ys = [coordinate[1] for coordinate in coordinates]
    max_x = max(xs)
    max_y = max(ys)
    min_x = min(xs)
    min_y = min(ys)

    grid = [[(".", 0) for j in range(max_x + 1) ] for i in range(max_y + 1)]

    day6_fill_grid(grid, coordinates)
    #day6_debug_grid(grid)

    ids = [i for i in range(len(coordinates))]
    for i in range(len(grid)):
        if i == 0 or i == len(grid) - 1:
            for j in range(len(grid[i])):
                value = grid[i][j][0]
                if value in ids:
                    ids.remove(value)
        else:
            value = grid[i][0][0]
            if value in ids:
                ids.remove(value)
            value = grid[i][len(grid[i])-1][0]
            if value in ids:
                ids.remove(value)

    max_val = 0
    max_id = 0
    for id in ids:
        temp_count = 0
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j][0] == id:
                    temp_count += 1
        if temp_count > max_val:
            max_val = temp_count
            max_id = id

    return max_val

def day6_2(data):
    size = 10000
    #data, size = (read_input(2018, 601), 32)
    coordinates = [(int(entry.split(", ")[0]), int(entry.split(", ")[1])) for entry in data]

    xs = [coordinate[0] for coordinate in coordinates]
    ys = [coordinate[1] for coordinate in coordinates]
    max_x = max(xs)
    max_y = max(ys)

    max_val = 0
    max_id = 0
    counter = 0
    for i in range(max_y + 1):
        for j in range(max_x + 1):
            dists = functools.reduce(lambda acc, coordinate: acc + abs(coordinate[1]-i) + abs(coordinate[0]-j), coordinates, 0)
            if dists < size:
                counter += 1
    return counter

""" DAY 7 """

def day7_parse_inst(data):
    # Step C must be finished before step A can begin.
    parsed_data = [re.findall("Step ([A-Z]) must be finished before step ([A-Z]) can begin.",line)[0] for line in data]
    dependencies = {}
    letters = []
    for (req, step) in parsed_data:
        if not step in dependencies:
            dependencies[step] = []
        if not req in letters:
            letters.append(req)
        dependencies[step].append(req)

    for step, reqs in dependencies.items():
        reqs.sort()

    return (dependencies, letters)

def day7_inst_order(dependencies, letters):
    stack = []
    for letter in letters:
        if not letter in dependencies.keys():
            stack.append(letter)
    stack.sort()
    completed = []
    while len(stack) > 0:
        next_letter = stack.pop(0)
        completed.append(next_letter)
        for step, deps in dependencies.items():
            if not step in completed and not step in stack and all([dep in completed for dep in deps]):
                stack.append(step)
        stack.sort()
    return completed

def day7_1(data):
    #data = read_input(2018, 701)
    (dependencies, letters) = day7_parse_inst(data)
    return ''.join(day7_inst_order(dependencies, list(string.ascii_uppercase)))

def day7_worker(worker, completed):
    if not worker == None:
        (step, duration) = worker
        duration -= 1
        worker = (step, duration)
        if duration == 0:
            worker = None
            completed.append(step)
    return (completed, worker)

def day7_inst_order2(dependencies, letters, step_duration, workers):
    stack = []
    for letter in letters:
        if not letter in dependencies.keys():
            stack.append((letter, (ord(letter)-ord("A") + 1) + step_duration))
    stack.sort(key=lambda e: (e[1], e[0]))
    completed = []
    workers = [None for i in range(workers)]
    second = 0
    counter = 0
    while len(stack) > 0 or any([w != None for w in workers]):
        counter += 1
        for i in range(len(workers)):
            if workers[i] == None and len(stack) > 0:
                workers[i] = stack.pop(0)
            completed, worker = day7_worker(workers[i], completed)
            workers[i] = worker

        for step, deps in dependencies.items():
            if not step in completed and all([let[0] != step for let in stack]) and all([dep in completed for dep in deps]) and not any([w != None and w[0] == step for w in workers]):
                stack.append((step, (ord(step)-ord("A") + 1) + step_duration))
        stack.sort()
    return counter

def day7_2(data):
    step_duration = 60
    workers = 5
    letters = list(string.ascii_uppercase)
    #data, step_duration, letters, workers = (read_input(2018, 701), 0, ["A", "B", "C", "D", "E", "F"], 2)
    (dependencies, letters) = day7_parse_inst(data)
    return day7_inst_order2(dependencies, letters, step_duration, workers)

""" DAY 8 """

from enum import Enum
class PropertyDescription:
    Header = 1
    Metadata_Definition = 3
    Nodes_End = 2

def day8_process_operation(data, operation, curr_node, nodes, operations):
    if operation == PropertyDescription.Header:
        nodes = data.pop(0)
        metadata = data.pop(0)
        operations.insert(0, PropertyDescription.Nodes_End)
        for i in range(metadata):
            operations.insert(0, PropertyDescription.Metadata_Definition)
        for i in range(nodes):
            operations.insert(0, PropertyDescription.Header)
        new_node = ([], [], curr_node)
        curr_node[1].append(new_node)
        return (data, new_node, operations)

    if operation == PropertyDescription.Metadata_Definition:
        metadata = data.pop(0)
        curr_node[0].append(metadata)
        return (data, curr_node, operations)

    if operation == PropertyDescription.Nodes_End:
        return (data, curr_node[2], operations)

def day8_parse_tree(data):
    i = 0
    nodes = []
    # Metadata, children, parent
    curr_node = ([], [], None)
    operations = [PropertyDescription.Header]
    while len(operations) > 0:
        operation = operations.pop(0)
        data, curr_node, operations = day8_process_operation(data, operation, curr_node, nodes, operations)
    return curr_node[1][0]

def day8_sum_meta(node):
    counter = sum(node[0])
    for child in node[1]:
        counter += day8_sum_meta(child)
    return counter

def day8_1(data):
    #data = read_input(2018, 801)
    data = data[0].split(" ")
    tree = day8_parse_tree([int(n) for n in data])
    total = day8_sum_meta(tree)
    return total

def day8_node_value(node):
    metadata, children, parent = node
    if len(children) == 0:
        return sum(metadata)

    total = 0
    for meta in metadata:
        idx = meta - 1
        if idx >= 0 and idx < len(children):
            total += day8_node_value(children[idx])

    return total

def day8_2(data):
    #data = read_input(2018, 801)
    data = data[0].split(" ")
    tree = day8_parse_tree([int(n) for n in data])
    total = day8_node_value(tree)
    return total

""" DAY 9 """

class ListNode:
    def __init__(self, data):
        "constructor class to initiate this object"

        # store data
        self.data = data

        # store reference (next item)
        self.next = None

        # store reference (previous item)
        self.previous = None
        return

def day9_debug_marbles(marble_0, current_marble):
    curr = marble_0
    output = []
    while True:
        text = int(curr.data)
        if curr.data == current_marble.data:
            text = "({0})".format(curr.data)
        output.append(text)
        curr = curr.next
        if curr.data == marble_0.data:
            break
    print(output)

def day9_remove_marble(current_marble):
    prev_marble = current_marble.previous
    next_marble = current_marble.next
    prev_marble.next = next_marble
    next_marble.previous = prev_marble
    return next_marble

def day9_add_marble_before(current_marble, marble_value):
    new_node = ListNode(marble_value)
    new_node.previous = current_marble.previous
    new_node.next = current_marble
    new_node.previous.next = new_node
    current_marble.previous = new_node
    return new_node

def day9_play_game_mine(players, highest_marble):
    scores = [0 for i in range(players)]
    current_marble = ListNode(0)
    current_marble.previous = current_marble
    current_marble.next = current_marble
    marble_0 = current_marble
    next_marble = 1
    player = 0
    while(next_marble <= highest_marble):
        #day9_debug_marbles(marble_0, current_marble)
        if next_marble % 23 != 0:
            for i in range(2):
                current_marble = current_marble.next
            current_marble = day9_add_marble_before(current_marble, next_marble)
        else:
            scores[player] += next_marble
            for i in range(7):
                current_marble = current_marble.previous
            scores[player] += current_marble.data
            current_marble = day9_remove_marble(current_marble)
        next_marble += 1
        player = (player+1) % players
    return scores

def day9_play_game_optimized(players, highest_marble):
    scores = [0 for i in range(players)]
    marbles = deque([0])
    next_marble = 1
    player = 0
    while(next_marble <= highest_marble):
        #day9_debug_marbles2(marble_0, current_marble)
        if next_marble % 23 != 0:
            marbles.rotate(-2)
            marbles.appendleft(next_marble)
        else:
            scores[player] += next_marble
            marbles.rotate(7)
            scores[player] += marbles.popleft()
        next_marble += 1
        player = (player+1) % players
    return scores

def day9_parse_input(data):
    # 9 players; last marble is worth 25 points
    return tuple([int(a) for a in re.findall("(\d+) players; last marble is worth (\d+) points",data)[0]])

def day9_1(data):
    line = data[0]
    #data = read_input(2018, 901)
    #line = data[3]
    players, highest_marble = day9_parse_input(line)
    scores = day9_play_game_optimized(players, highest_marble)
    return max(scores)

def day9_2(data):
    line = data[0]
    #data = read_input(2018, 901)
    #line = data[5]
    players, highest_marble = day9_parse_input(line)
    scores = day9_play_game_optimized(players, highest_marble * 100)
    return max(scores)

""" DAY 10 """

class I:
    px = 0
    py = 1
    vx = 3
    vy = 4
    ax = 6
    ay = 7

def day10_parse_line(line):
    # position=< 32923,  43870> velocity=<-3, -4>
    return tuple([int(a) for a in re.findall("position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>",line)[0]])

def day10_parse_input(data):
    return [day10_parse_line(line) for line in data]

def day10_update_particle(particle):
    px, py, vx, vy = particle
    px += vx
    py += vy
    return (px, py, vx, vy)

def day10_board_size(particles):
    min_x = min([pos[0] for pos in particles])
    min_y = min([pos[1] for pos in particles])
    max_x = max([pos[0] for pos in particles])
    max_y = max([pos[1] for pos in particles])
    return (max_x - min_x, max_y - min_y)

def day10_print_particles(particles):
    min_x = min([pos[0] for pos in particles])
    min_y = min([pos[1] for pos in particles])
    max_x = max([pos[0] for pos in particles])
    max_y = max([pos[1] for pos in particles])

    for i in range(max_y - min_y +1):
        line = ""
        for j in range(max_x - min_x+1):
            found = False
            for particle in particles:
                if particle[0] == (j + min_x) and particle[1] == (min_y + i):
                    found = True
                    break
            if found:
                line += " #"
            else:
                line += " ."
        print(line)
    print()
    return (min_x, max_x, min_y, max_y)

def day10_resolve(particles):
    size_x, size_y = day10_board_size(particles)
    counter = 0
    while True:
        new_particles = [day10_update_particle(particle) for particle in particles]
        new_size_x, new_size_y = day10_board_size(new_particles)

        if(new_size_x > size_x and new_size_y > size_y):
            break
        size_x = new_size_x
        size_y = new_size_y
        particles = new_particles
        counter += 1
    return (particles, counter)

def day10_1(data):
    #data = read_input(2018, 1001)
    particles, counter = day10_resolve(day10_parse_input(data))
    day10_print_particles(particles)

def day10_2(data):
    #data = read_input(2018, 1001)
    particles, counter = day10_resolve(day10_parse_input(data))
    return counter

""" DAY 11 """

def day11_cell_value(serial, x, y):
    rack_id = x + 10
    level = rack_id * y
    level += serial
    level *= rack_id
    level = math.floor((level % 1000) / 100)
    level -= 5
    return level

def day11_grid(serial):
    return [[day11_cell_value(serial, x+1, y+1)  for x in range(300) ] for y in range(300)]

def day11_solve_exact_size_aux(memoization, grid, x, y, size):
    if size == 1:
        return grid[y][x]
    #current_total = day11_solve_exact_size(grid, x, y, size-1)
    key = str(x) + "_" + str(y) + "_" + str(size)
    if key in memoization:
        return memoization[key]
    around_size = 0
    for i in range(size-1):
        around_size += grid[y+i][x+size-1]
        around_size += grid[y+size-1][x+i]
    around_size += grid[y + size - 1][x + size -1]
    #if around_size > 0:
    value = day11_solve_exact_size_aux(memoization, grid, x, y, size-1) + around_size
    memoization[key] = value
    return value
    #else:
    #    return -99999999999999

def day11_solve_exact_size(memoization, grid, size):
    max_total = -99999999999
    coordinate = (1, 1)
    y = 0
    while(y <= len(grid) - size):
        x = 0
        while(x <= len(grid) - size):
            key = str(x) + "_" + str(y) + "_" + str(size)
            if key in memoization:
                current_total = memoization[key]
            else:
                around_size = 0
                for i in range(size-1):
                   around_size += grid[y+i][x+size-1]
                   around_size += grid[y+size-1][x+i]
                around_size += grid[y + size - 1][x + size -1]
                if around_size > 0:
                    current_total = day11_solve_exact_size_aux(memoization, grid, x, y, size)
                else:
                   x+=1
                   continue
            if current_total > max_total:
                max_total = current_total
                coordinate = (x+1, y+1)
            x += 1
        y += 1
    return (coordinate, max_total)

def day11_solve_range(grid, min_size, max_size):
    max_total = -9999999999
    coordinate = (1, 1)
    max_size_total = min_size
    memoization = {}
    for size in range(min_size, max_size+1):
        current_coordinate, current_total = day11_solve_exact_size(memoization, grid, size)
        if current_total > max_total:
            max_total = current_total
            coordinate = current_coordinate
            max_size_total = size
    return (coordinate, max_size_total)

def day11_1(data):
     #data = read_input(2018, 1101)
     memoization = {}
     serial = int(data[0])
     grid = day11_grid(serial)
     return day11_solve_exact_size(memoization, grid, 3)[0]

def day11_2(data):
    #data = read_input(2018, 1101)
    serial = int(data[0])
    grid = day11_grid(serial)
    return day11_solve_range(grid, 2, 299)

""" DAY 12 """

def day12_parse_input(data):
    initial_state = deque(re.findall("initial state: ([\.|#]*)",data[0])[0])
    rules = deque([])
    for rule in data[2:]:
        parts = rule.split(" => ")
        rules.append((parts[0], parts[1]))
    return (initial_state, rules)

def day12_get_rule(pots, rules, position):
    for rule in rules:
        prev = rule[0]
        match = True
        for i in range(len(prev)):
            match &= prev[i] == pots[position + i - 2]
        if match:
            return rule[1]
    return None

def day12_process_generation(pots, rules, start):
    new_pots = deque([])
    pots.appendleft(".")
    pots.appendleft(".")
    pots.appendleft(".")
    pots.appendleft(".")
    pots.append(".")
    pots.append(".")
    pots.append(".")
    pots.append(".")
    for i in range(2, len(pots)-2):
        result = day12_get_rule(pots, rules, i)
        if result == None:
            new_pots.append(pots[i])
        else:
            new_pots.append(result)

    start = start-2
    curr = new_pots[0]
    while curr == ".":
        new_pots.popleft()
        start += 1
        curr = new_pots[0]

    curr = new_pots[-1]
    while curr == ".":
        new_pots.pop()
        curr = new_pots[-1]
            
    return (new_pots, start)

def day12_solve(pots, rules, generations):
    memoization = {}
    history = deque([])
    start = 0
    for i in range(generations):
        history.append(("".join(pots), start))
        memoization["".join(pots)] = i
        #print("".join(pots))
        #print(start)
        pots, start = day12_process_generation(pots, rules, start)
        new_pots = "".join(pots)
        if new_pots in memoization:
            itera = memoization[new_pots]
            j = 0
            while(j < itera):
                history.popleft()
                j +=1
            pos = (generations-(i+1))%len(history)
            pos_shift = start - history[pos][1]

            iterations = math.floor((generations-(i+1))/len(history))
            pots = history[pos][0]
            start += pos_shift*iterations
            break

    total = 0
    for i in range(len(pots)):
        if pots[i] == "#":
            total += start + i
    
    return total

def day12_1(data):
    #data = read_input(2018, 1201)
    pots, rules = day12_parse_input(data)
    return day12_solve(pots, rules, 20)

def day12_2(data):
    #data = read_input(2018, 1201)
    pots, rules = day12_parse_input(data)
    return day12_solve(pots, rules, 50000000000)

""" Day 13 """

class Turn:
    Left = 0
    Straight = 1
    Right = 2

class Direction:
    Left = 0
    Up = 1
    Right = 2
    Down = 3

def day13_print_direction(dir):
    if dir == Direction.Up:
        return "^"
    elif dir == Direction.Down:
        return "v"
    elif dir == Direction.Left:
        return "<"
    elif dir == Direction.Right:
        return ">"

def day13_debug_map(map, positions):
    for y in range(len(map)):
        line = ""
        for x in range(len(map[y])):
            cart = [positions[k] for k in range(len(positions)) if positions[k][0] == x and positions[k][1] == y]
            if len(cart) == 1:
                cart = cart[0]
            else:
                cart = None

            if cart == None:
                line += map[y][x]
            else:
                line += day13_print_direction(cart[2])
        print(line)
    print()
    time.sleep(0.5)

def day13_get_cart_direction(pos):
    if pos == "^":
        return Direction.Up
    elif pos == "v":
        return Direction.Down
    elif pos =="<":
        return Direction.Left
    elif pos == ">":
        return Direction.Right
    return None

def day13_parse_input(data):
    map = []
    positions = []
    for row in range(len(data)):
        new_row = []
        for column in range(len(data[row])):
            direction = day13_get_cart_direction(data[row][column])
            if direction == None:
                new_row.append(data[row][column])
            else:
                positions.append((column, row, direction, Turn.Right))
                if direction == Direction.Left or direction == Direction.Right:
                    new_row.append("-")
                else:
                    new_row.append("|")
        map.append(new_row)
    return map, sorted(positions, key=lambda v: (v[0], v[1]))

def day13_direction_on_turn(direction, turn):
    if turn == Turn.Straight:
        return direction
    elif turn == Turn.Right:
        return (direction + 1) % 4
    else:
        return (direction + 3) % 4

def day13_next_turn(location, direction, last_turn):
    if location == "/":
        if direction == Direction.Up:
            return (Direction.Right, last_turn)
        if direction == Direction.Left:
            return (Direction.Down, last_turn)
        if direction == Direction.Right:
            return (Direction.Up, last_turn)
        if direction == Direction.Down:
            return (Direction.Left, last_turn)
    elif location == "\\":
        if direction == Direction.Up:
            return (Direction.Left, last_turn)
        if direction == Direction.Left:
            return (Direction.Up, last_turn)
        if direction == Direction.Right:
            return (Direction.Down, last_turn)
        if direction == Direction.Down:
            return (Direction.Right, last_turn)
    elif location == "+":
        turn = (last_turn + 1) % 3
        return (day13_direction_on_turn(direction, turn), turn)
    return direction, last_turn

def day13_get_direction_delta(direction):
    if direction == Direction.Up:
        return (0, -1)
    elif direction == Direction.Down:
        return (0, 1)
    elif direction == Direction.Left:
        return (-1, 0)
    elif direction == Direction.Right:
        return (1, 0)

def day13_move_cart(map, positions, cart):
    x = positions[cart][0]
    y = positions[cart][1]
    direction = positions[cart][2]
    last_turn = positions[cart][3]
    location = map[y][x]
    
    delta_x, delta_y = day13_get_direction_delta(direction)
    new_x, new_y = x + delta_x, y + delta_y
    for i in range(len(positions)):
        if i != cart and positions[i][0] == new_x and positions[i][1] == new_y:
            return "X", new_x, new_y, i
    
    new_direction, new_turn = day13_next_turn(map[new_y][new_x], direction, last_turn)

    return (new_x, new_y, new_direction, new_turn)

def day13_solve(map, positions):
    while True:
        #day13_debug_map(map, positions)
        for i in range(len(positions)):
            new_position = day13_move_cart(map, positions, i)
            if new_position[0] == "X":
                return new_position[1], new_position[2]
            positions[i] = new_position
        positions = sorted(positions, key=lambda v: (v[0], v[1]))

def day13_solve2(map, positions):
    while True:
        #day13_debug_map(map, positions)
        crashing_carts = []
        for i in range(len(positions)):
            new_position = day13_move_cart(map, positions, i)
            if new_position[0] == "X":
                crashing_carts.append(new_position[3])
                crashing_carts.append(i)
            else:
                positions[i] = new_position
        positions = [positions[i] for i in range(len(positions)) if not i in crashing_carts]
        if len(positions) == 1:
            return positions[0][0], positions[0][1]
        positions = sorted(positions, key=lambda v: (v[0], v[1]))

def day13_1(data):
    #data = read_input(2018, 1301)
    map, positions = day13_parse_input(data)
    return day13_solve(map, positions)

def day13_2(data):
    #data = read_input(2018, 1302)
    map, positions = day13_parse_input(data)
    return day13_solve2(map, positions)

""" DAY 14 """

def day14_debug_recipes(recipes, elves):
    out = ""
    for i in range(len(recipes)):
        recipe = recipes[i]
        if elves[0] == i:
            recipe = "({0})".format(recipe)
        elif elves[1] == i:
            recipe = "[{0}]".format(recipe)
        else:
            recipe = " {0} ".format(recipe)

        out += " " + str(recipe)
    print(out)

def day14_break_number(number):
    return [int(v) for v in str(number)]

def day14_solve(nr_recipes):
    recipes = [3, 7]
    elves = [0, 1]
    recipes_len = len(recipes)
    for i in range(nr_recipes+10):
        #day14_debug_recipes(recipes, elves)
        recipe_0 = recipes[elves[0]]
        recipe_1 = recipes[elves[1]]
        new_recipe = recipe_0 + recipe_1
        new_recipes = day14_break_number(new_recipe)
        recipes.extend(new_recipes)
        recipes_len += len(new_recipes)
        elves[0] = (elves[0] + recipe_0 + 1) % recipes_len
        elves[1] = (elves[1] + recipe_1 + 1) % recipes_len

    return recipes[nr_recipes:nr_recipes+10]

def day14_solve2(nr_recipes, value):
    recipes = [3, 7]
    elves = [0, 1]
    start = 0
    #value = str(nr_recipes)
    size = len(value)
    recipes_len = len(recipes)
    while True:
        #day14_debug_recipes(recipes, elves)
        recipe_0 = recipes[elves[0]]
        recipe_1 = recipes[elves[1]]
        new_recipe = recipe_0 + recipe_1
        new_recipes = day14_break_number(new_recipe)
        recipes.extend(new_recipes)
        recipes_len += len(new_recipes)
        elves[0] = (elves[0] + recipe_0 + 1) % recipes_len
        elves[1] = (elves[1] + recipe_1 + 1) % recipes_len
        if recipes_len - start > size:
            #day14_debug_recipes(recipes, [start, -1])
            while start < recipes_len - size:
                if str(recipes[start]) == value[0]:
                    tmp_value = "".join([str(r) for r in recipes[start:start + size]])
                    if tmp_value == value:
                        return start
                start += 1

    return recipes[nr_recipes:nr_recipes+10]

def day14_1(data):
    #data = ["9"]
    #data = ["5"]
    #data = ["18"]
    #data = ["2018"]

    nr_recipes = int(data[0])
    return "".join([str(i) for i in day14_solve(nr_recipes)])

def day14_2(data):
    #data = ["9"]
    #data = ["5"]
    #data = ["18"]
    #data = ["2018"]

    #data = ["59414"]
    nr_recipes = int(data[0])
    return day14_solve2(nr_recipes, data[0])

""" DAY 16 """

class Inst16:
    def addr(regs, a, b, c):
        regs[c] = regs[a] + regs[b]
        return regs
        
    def addi(regs, a, b, c):
        regs[c] = regs[a] + b
        return regs

    def mulr(regs, a, b, c):
        regs[c] = regs[a] * regs[b]
        return regs
        
    def muli(regs, a, b, c):
        regs[c] = regs[a] * b
        return regs

    def banr(regs, a, b, c):
        regs[c] = regs[a] & regs[b]
        return regs
        
    def bani(regs, a, b, c):
        regs[c] = regs[a] & b
        return regs

    def borr(regs, a, b, c):
        regs[c] = regs[a] | regs[b]
        return regs
        
    def bori(regs, a, b, c):
        regs[c] = regs[a] | b
        return regs

    def setr(regs, a, b, c):
        regs[c] = regs[a]
        return regs
        
    def seti(regs, a, b, c):
        regs[c] = a
        return regs
        
    def gtir(regs, a, b, c):
        if a > regs[b]:
            regs[c] = 1
        else:
            regs[c] = 0
        return regs
        
    def gtri(regs, a, b, c):
        if regs[a] > b:
            regs[c] = 1
        else:
            regs[c] = 0
        return regs
        
    def gtrr(regs, a, b, c):
        if regs[a] > regs[b]:
            regs[c] = 1
        else:
            regs[c] = 0
        return regs
        
    def eqir(regs, a, b, c):
        if a == regs[b]:
            regs[c] = 1
        else:
            regs[c] = 0
        return regs
        
    def eqri(regs, a, b, c):
        if regs[a] == b:
            regs[c] = 1
        else:
            regs[c] = 0
        return regs
        
    def eqrr(regs, a, b, c):
        if regs[a] == regs[b]:
            regs[c] = 1
        else:
            regs[c] = 0
        return regs
    
    ops = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

def day16_parse_input(data):
    samples = []
    i = 0
    while i < len(data):
        if data[i] == "":
            break
        # Before: [3, 2, 1, 1]
        # 9 2 1 2
        # After:  [3, 2, 2, 1]
        before = [ int(x) for x in re.findall("Before: \[(\d+), (\d+), (\d+), (\d+)\]",data[i])[0]]
        i+=1
        inst = [ int(x) for x in re.findall("(\d+) (\d+) (\d+) (\d+)",data[i])[0]]
        i+=1
        after = [ int(x) for x in re.findall("After:  \[(\d+), (\d+), (\d+), (\d+)\]",data[i])[0]]
        i+=1
        i+=1
        samples.append((before, inst, after))
    
    program = []
    while i < len(data):
        if data[i] != "":
            # 9 2 1 2
            inst = [ int(x) for x in re.findall("(\d+) (\d+) (\d+) (\d+)",data[i])[0]]
            program.append(inst)
        i+=1
        
    return samples, program

def day16_check_op(fun, before, inst, after):
    result = fun(before[:], inst[1], inst[2], inst[3])
    return all([result[i] == after[i] for i in range(len(result))])

def day16_check_sample(before, inst, after):
    ops = Inst16.ops
    counter = 0
    for op in ops:
        if day16_check_op(op, before, inst, after):
            counter += 1
    return counter

def day16_update_mapping(mapping, before, inst, after):
    ops = Inst16.ops
    counter = 0
    matched = []
    for op in ops:
        if day16_check_op(op, before, inst, after):
            matched.append(op)
    opcode = inst[0]
    prev_map = mapping[opcode]
    mapping[opcode] = [op for op in prev_map if op in matched]

def day16_solve1(samples):
    counter = 0
    for before, inst, after in samples:
        if day16_check_sample(before, inst, after) >= 3:
            counter += 1
    return counter

def day16_calculate_mapping(samples):
    mapping = [Inst16.ops for i in range(len(Inst16.ops))]
    for before, inst, after in samples:
        day16_update_mapping(mapping, before, inst, after)
    
    while True:
        for i in range(len(mapping)):
            if len(mapping[i]) == 1:
                op = mapping[i][0]
                for j in range(len(mapping)):
                    if i != j:
                        mapping[j] = [op2 for op2 in mapping[j] if op2 != op]
        if all([len(mapping[i]) == 1 for i in range(len(mapping))]):
            break
    mapping = [m[0] for m in mapping]
    return mapping

def day16_solve2(samples, program):
    mapping = day16_calculate_mapping(samples)

    regs = [0,0,0,0]
    for line in program:
        op = mapping[line[0]]
        regs = op(regs, line[1], line[2], line[3])
    return regs[0]

def day16_1(data):
    #data = read_input(2018, 1601)
    samples, program = day16_parse_input(data)
    return day16_solve1(samples)

def day16_2(data):
    #data = read_input(2018, 1601)
    samples, program = day16_parse_input(data)
    return day16_solve2(samples, program)

""" DAY 17 """

from struct import pack

class Bitmap():
  def __init__(s, width, height):
    s._bfType = 19778 # Bitmap signature
    s._bfReserved1 = 0
    s._bfReserved2 = 0
    s._bcPlanes = 1
    s._bcSize = 12
    s._bcBitCount = 24
    s._bfOffBits = 26
    s._bcWidth = width
    s._bcHeight = height
    s._bfSize = 26+s._bcWidth*3*s._bcHeight
    s.clear()

  def clear(s):
    s._graphics = [(0,0,0)]*s._bcWidth*s._bcHeight

  def setPixel(s, x, y, color):
    if isinstance(color, tuple):
      if x<0 or y<0 or x>s._bcWidth-1 or y>s._bcHeight-1:
        raise ValueError('Coords out of range')
      if len(color) != 3:
        raise ValueError('Color must be a tuple of 3 elems')
      s._graphics[y*s._bcWidth+x] = (color[2], color[1], color[0])
    else:
      raise ValueError('Color must be a tuple of 3 elems')

  def write(s, file):
    with open(file, 'wb') as f:
      f.write(pack('<HLHHL', 
                   s._bfType, 
                   s._bfSize, 
                   s._bfReserved1, 
                   s._bfReserved2, 
                   s._bfOffBits)) # Writing BITMAPFILEHEADER
      f.write(pack('<LHHHH', 
                   s._bcSize, 
                   s._bcWidth, 
                   s._bcHeight, 
                   s._bcPlanes, 
                   s._bcBitCount)) # Writing BITMAPINFO
      for px in s._graphics:
        f.write(pack('<BBB', *px))
      for i in range (0, (s._bcWidth*3) % 4):
        f.write(pack('B', 0))

class Day17_Type:
    clay = 0
    sand = 1
    water = 2
    settled = 3

    @staticmethod
    def render_square(square):
        if square == Day17_Type.clay:
            return "#"
        elif square == Day17_Type.sand:
            return "."
        elif square == Day17_Type.water:
            return "|"
        elif square == Day17_Type.settled:
            return "~"

    @staticmethod
    def render_square_rgb(square):
        if square == Day17_Type.clay:
            return (0, 0, 0)
        elif square == Day17_Type.sand:
            return (255, 255, 255)
        elif square == Day17_Type.water:
            return (102, 165, 255)
        elif square == Day17_Type.settled:
            return (0, 0, 255)

bitmap_counter = 0
def day17_debug_ground_bmp(ground, y):
    global bitmap_counter

    height = 100
    half = int(100/2)
    lower = max(y - half, 0)
    size = (y + half + 1) - lower
    b = Bitmap(436, size)
    b.clear()
    for i in range(lower, y + half + 1):
        for j in range(len(ground[i])):
            coord = y + half     - i
            b.setPixel(j, coord, Day17_Type.render_square_rgb(ground[i][j]))
    b.write('test/file{:09d}.bmp'.format(bitmap_counter))
    bitmap_counter += 1

def day17_debug_ground_ascii(ground, y):
    for i in range(y - 10, y + 11):
        line = ground[i]
        print("".join([Day17_Type.render_square(s) for s in line]))
    print()
    time.sleep(.1)

def day17_debug_full_ground_bmp(ground):
    size = len(ground)
    half = int(size / 2)
    b = Bitmap(436, size)
    b.clear()
    for i in range(len(ground)):
        for j in range(len(ground[i])):
            coord = (size-1) - i
            b.setPixel(j, coord, Day17_Type.render_square_rgb(ground[i][j]))
    b.write('test/a_full_ground.bmp')

def day17_parse_input(data):
    slices = []
    min_y = 9999999
    max_y = 0
    for line in data:
        if line[0] == "x":
            # x=501, y=3..7
            ground_slice = [ int(x) for x in re.findall("x=(\d+), y=(\d+)..(\d+)",line)[0]]
            slices.append(ground_slice)
            if ground_slice[1] < min_y:
                min_y = ground_slice[1]
            if ground_slice[2] > max_y:
                max_y = ground_slice[2]
        else:
            # y=501, x=3..7
            ground_slice = [ int(x) for x in re.findall("y=(\d+), x=(\d+)..(\d+)",line)[0]]
            for i in range(ground_slice[1], ground_slice[2]+1):
                ground_slice2 = (i, ground_slice[0], ground_slice[0])
                slices.append(ground_slice2)
                if ground_slice2[1] < min_y:
                    min_y = ground_slice2[1]
                if ground_slice2[2] > max_y:
                    max_y = ground_slice2[2]
    
    slices = sorted(slices, key=lambda s: s[0])
    min_x = slices[0][0] - 2
    max_x = slices[-1][0] + 2

    ground = [[ Day17_Type.sand for j in range(min_x, max_x)] for i in range(max_y + 2)]
    for s in slices:
        for i in range(s[1], s[2]+1):
            ground[i][s[0] - min_x] = Day17_Type.clay
    
    return ground, min_x, min_y

def day17_flow_water(ground, y, x):
    stack = deque([(y, x)])
    while(len(stack) > 0):
        i, j = stack.popleft()
        
        if i+1 >= len(ground) or i < 0 or j+1 >= len(ground[0]) or j-1 < 0:
            continue
        if ground[i][j] == Day17_Type.clay or ground[i][j] == Day17_Type.settled:
            continue

        if ground[i][j] == Day17_Type.sand:
            ground[i][j] = Day17_Type.water
        
        k = j-1
        left_wall = False
        right_wall = False
        keep_going = False
        while(k > 0):
            if ground[i][k] == Day17_Type.clay or ground[i][k] == Day17_Type.settled:
                left_wall = True
                break
            if ground[i][k] == Day17_Type.sand:
                keep_going = True
                break
            k -= 1
        
        k = j+1
        while(k < len(ground[i])):
            if ground[i][k] == Day17_Type.clay or ground[i][k] == Day17_Type.settled:
                right_wall = True
                break
            if ground[i][k] == Day17_Type.sand:
                keep_going = True
                break
            k += 1

        if left_wall and right_wall:
            ground[i][j] = Day17_Type.settled
        
        #day17_debug_ground_bmp(ground, i)
        
        if ground[i+1][j] == Day17_Type.clay or ground[i+1][j] == Day17_Type.settled:
            if ground[i][j-1] != ground[i][j]:
                stack.append((i, j-1))
            if ground[i][j+1] != ground[i][j]:
                stack.append((i, j+1))

        if ground[i][j] == Day17_Type.settled and ground[i-1][j] == Day17_Type.water:
                stack.append((i-1, j))

        if ground[i+1][j] != ground[i][j]:
            stack.append((i+1, j))

def day17_solve(ground, min_x, min_y):
    day17_flow_water(ground, 0, 500 - min_x)

    #day17_debug_full_ground_bmp(ground)
    
    counter_water = 0
    counter_retained = 0
    for i in range(len(ground)):
        for j in range(len(ground[i])):
            if i >= min_y:
                if ground[i][j] == Day17_Type.settled:
                    counter_water += 1
                    counter_retained += 1
                if ground[i][j] == Day17_Type.water:
                    counter_water += 1

    return counter_water, counter_retained

def day17_1(data):
    #data = read_input(2018, 1701)
    ground, min_x, min_y = day17_parse_input(data)
    return day17_solve(ground, min_x, min_y)[0]

def day17_2(data):
    #data = read_input(2018, 1701)
    ground, min_x, min_y = day17_parse_input(data)
    return day17_solve(ground, min_x, min_y)[1]

""" DAY 18 """

class AcreContents:
    open = "."
    trees = "|"
    lumberyard = "#"

    @staticmethod
    def count_states(state, adjacents):
        return len([True for a in adjacents if a == state])

    @staticmethod
    def next_state(current, adjacents):
        if current == AcreContents.open:
            if AcreContents.count_states(AcreContents.trees, adjacents) >= 3:
                return AcreContents.trees
        elif current == AcreContents.trees:
            if AcreContents.count_states(AcreContents.lumberyard, adjacents) >= 3:
                return AcreContents.lumberyard
        elif current == AcreContents.lumberyard:
            if AcreContents.count_states(AcreContents.lumberyard, adjacents) == 0 or AcreContents.count_states(AcreContents.trees, adjacents) == 0:
                return AcreContents.open
        return current

def day18_debug_area(area):
    for i in range(len(area)):
        out = ""
        for j in range(len(area[i])):
            out += area[i][j]
        print(out)
    print()

def day18_get_adjacent_cells(area, i_coord, j_coord):
    adjacency = [(i,j) for i in (-1,0,1) for j in (-1,0,1) if not (i == j == 0)] #the adjacency matrix
    result = []
    for di, dj in adjacency:
        if 0 <= (i_coord + di) < len(area) and 0 <= j_coord + dj < len(area[0]): #boundaries check
            #yielding is usually faster than constructing a list and returning it if you're just using it once
            result.append(area[i_coord + di][j_coord + dj])
    return result

def day18_compute_change(area, i, j):
    adjacents = day18_get_adjacent_cells(area, i, j)
    return AcreContents.next_state(area[i][j], adjacents)

def day18_process(area, minutes):
    prev_area = area
    history = deque([])
    memoization = {}
    for t in range(minutes):
        #day18_debug_area(prev_area)
        history.append(prev_area)
        memoization["".join(prev_area)] = t
        #print(t)
        new_area = []
        for i in range(len(prev_area)):
            new_area.append("")
            for j in range(len(prev_area[i])):
                new_state = day18_compute_change(prev_area, i, j)
                new_area[i] += new_state
        
        new_area_key = "".join(new_area)
        if new_area_key in memoization:
            itera = memoization[new_area_key]
            j = 0
            while(j < itera):
                history.popleft()
                j +=1
            pos = (minutes-(t+1))%len(history)
            prev_area = history[pos]
            break
        prev_area = new_area
    return prev_area

def day18_1(data):
    #data = read_input(2018, 1801)
    area = data
    new_area = day18_process(area, 10)
    trees = len([True for line in new_area for s in line if s == AcreContents.trees])
    lumberyards = len([True for line in new_area for s in line if s == AcreContents.lumberyard])
    return trees * lumberyards

def day18_2(data):
    #data = read_input(2018, 1801)
    area = data
    new_area = day18_process(area, 1000000000)
    trees = len([True for line in new_area for s in line if s == AcreContents.trees])
    lumberyards = len([True for line in new_area for s in line if s == AcreContents.lumberyard])
    return trees * lumberyards

""" DAY 19 """

class Inst19(Inst16):
    ops = {"addr": Inst16.addr, \
           "addi": Inst16.addi, \
           "mulr": Inst16.mulr, \
           "muli": Inst16.muli, \
           "banr": Inst16.banr, \
           "bani": Inst16.bani, \
           "borr": Inst16.borr, \
           "bori": Inst16.bori, \
           "setr": Inst16.setr, \
           "seti": Inst16.seti, \
           "gtir": Inst16.gtir, \
           "gtri": Inst16.gtri, \
           "gtrr": Inst16.gtrr, \
           "eqir": Inst16.eqir, \
           "eqri": Inst16.eqri, \
           "eqrr": Inst16.eqrr }

def day19_parse_input(data):
    pointer = int(data[0][-1])
    
    program = []
    for line in data[1:]:
        inst = [x for x in re.findall("(\w+) (\d+) (\d+) (\d+)", line)[0]]
        inst[0] = Inst19.ops[inst[0]]
        inst[1] = int(inst[1])
        inst[2] = int(inst[2])
        inst[3] = int(inst[3])
        program.append(inst)

    return pointer, program

def day19_run_program(pointer, program, start_0):
    regs = [start_0, 0, 0, 0, 0, 0]
    inst = regs[pointer]
    while inst >= 0 and inst < len(program):
        regs[pointer] = inst
        f, a, b, c = program[inst]
        f(regs, a, b, c)
        inst = regs[pointer]
        inst += 1
    return regs

def day19_1(data):
    #data = read_input(2018, 1901)
    pointer, program = day19_parse_input(data)
    return day19_run_program(pointer, program, 0)

def day19_2(data):
    #data = read_input(2018, 1901)
    pointer, program = day19_parse_input(data)
    return day19_run_program(pointer, program, 1)

""" DAY 20 """

def day20_calculate_paths(path):
    stack = deque([])
    paths = deque([])
    current_path = deque([""])
    for s in path:
        if s == "(":
            stack.append("")
        elif s == "|":
            for i in range(len(current_path)):
                curr = current_path[i]
                for j in range(len(stack)):
                    curr += stack[j]
                paths.append(curr)
            stack.pop()
            stack.append("")
        elif s == ")":
            for i in range(len(current_path)):
                curr = current_path[i]
                for j in range(len(stack)):
                    curr += stack[j]
                paths.append(curr)
            if len(stack) != 0:
                stack.pop()
            if len(stack) == 0:
                current_path = paths
        elif s == "^" or s == "$":
            continue
        else:
            if len(stack) == 0:
                for i in range(len(current_path)):
                    current_path[i] += s
            else:
                stack[-1] += s
    return current_path

def day20_merge_paths(first, second):
    new_paths = deque([])
    for path1 in first:
        for path2 in second:
            new_paths.append(path1 + path2)
    return new_paths

def day20_alternatives(curr, path):
    parts = [""]
    alternatives = []
    while path[curr] != ")":
        if path[curr] == "(":
            alternative_paths, curr = day20_alternatives(curr+1, path)
            parts = day20_merge_paths(parts, alternative_paths)
        elif path[curr] == "|":
            alternatives.extend(parts)
            parts = [""]
        else:
            parts = [p + path[curr] for p in parts]
        curr += 1

    return alternatives, curr

def day20_process(path):
    path = path[1:]
    paths = [""]
    curr = 0
    while path[curr] != "$":
        if path[curr] == "(":
            alternative_paths, curr = day20_alternatives(curr+1, path)
            paths = day20_merge_paths(paths, alternative_paths)
        elif path[curr] != ")":
            paths = [p + path[curr] for p in paths]
        
        curr += 1
    return paths

#def day20_1(data):
#    data = read_input(2018, 2001)
#    path = data[0]
#    return day20_process(path)

""" DAY 23 """

def day23_parse_input(data):
    # pos=<-5920414,66954528,45418976>, r=94041555
    bots = []
    for line in data:
        bot = [int(x) for x in re.findall("pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)", line)[0]]
        bots.append((bot[0], bot[1], bot[2], bot[3]))
    return sorted(bots, reverse=True, key=lambda b: b[3])

def day23_manhattan(x, y, z, other_x, other_y, other_z):
    return abs(x - other_x) + abs(y - other_y) + abs(z - other_z)
    
def day23_debug_space_bmp(area):
    size = len(area[0])
    size2 = len(area[0][0])
    half = int(size / 2)
    b = Bitmap(500, 500)
    b.clear()
    for i in range(len(area[0])):
        for j in range(len(area[0][i])):
            coord = (size-1) - i
            c = area[0][i][j]
            if c == 0:
                color = (255, 255, 255)
            else:
                color = (0, 0, 255)
            b.setPixel(j, coord, color)
    b.write('test/a_full_area.bmp')

def day23_bots_in_range(bots, bot):
    in_range = []
    x, y, z, signal = bot
    for other_bot in bots:
        other_x, other_y, other_z, other_signal = other_bot
        if day23_manhattan(x, y, z, other_x, other_y, other_z) <= signal:
            in_range.append(other_bot)
    return in_range

def day23_bounds(area, i, j, k):
    return i >= 0 and i < len(area) and j >= 0 and j < len(area[i]) and k >= 0 and k < len(area[i][j])

def day23_space(bots):
    min_x = sys.maxsize
    max_x = 0
    min_y = sys.maxsize
    max_y = 0
    min_z = sys.maxsize
    max_z = 0

    for x, y, z, r in bots:
        if x - r < min_x:
            min_x = x - r
        if x + r > max_x:
            max_x = x + r
        if y - r < min_y:
            min_y = y - r
        if y + r > max_y:
            max_y = y + r
        if z - r < min_z:
            min_z = z - z
        if z + r > max_z:
            max_z = z + r
    
    space = [[[0 for k in range(min_x, max_x+1)] for j in range(min_y, max_y+1)] for i in range(min_z, max_z+1)]

    for x, y, z, r in bots:
        for i in range(-r, r+1):
            for j in range(-r, r+1):
                for k in range(-r, r+1):
                    if day23_manhattan(x, y, z, x+k, y+j, z+i) <= r and day23_bounds(space, z+i-min_z, y+j-min_y, x+k-min_x):
                        space[z+i-min_z][y+j-min_y][x+k-min_x] += 1
    
    return (space, min_x, min_y, min_z)

def day23_space_paralel(bots):
    threads = 32
    pool = mp.Pool(processes=threads)
    min_x, max_x, min_y, max_y, min_z, max_z = day23_bounds(bots)
    #per_thread = max(math.floor(len(bots)/threads), 1)
    #last = len(bots) - (per_thread * (threads-1))
    #partial(multiply,2)
    process = range(min_z, max_z+1)#[bots[per_thread*i: per_thread*i+per_thread] for i in range(threads)]
    #print(process)
    results = pool.map(functools.partial(day23_space3, bots, min_x, max_x, min_y, max_y), process)
    pool.close()
    pool.join()
    #print(results)
    counters = Counter()
    for res in results:
        counters.update(res)
        #for key, value in res.most_common(None):
        #    counters[key] += value
    
    print(counters.most_common(10))
    return counters

def day23_expand_bots(bots):
    new_bots = deque([])
    for x, y, z, r in bots:
        for i in range(-r, r+1):
            for j in range(-r, r+1):
                for k in range(-r, r+1):
                    if day23_manhattan(x, y, z, x+k, y+j, z+i) <= r:
                        new_bots.append((x+k, y+j, z+i))
    return new_bots

def day23_space_paralel2(bots, best_bot):
    min_x, max_x, min_y, max_y, min_z, max_z = day23_bounds([best_bot])

    threads = 32
    pool = mp.Pool(processes=threads)
    #per_thread = max(math.floor(len(bots)/threads), 1)
    #last = len(bots) - (per_thread * (threads-1))
    #partial(multiply,2)
    process = range(min_z, max_z+1)#[bots[per_thread*i: per_thread*i+per_thread] for i in range(threads)]
    #print(process)
    results = pool.map(functools.partial(day23_new_bew, bots, min_x, max_x, min_y, max_y), process)
    pool.close()
    pool.join()
    #print(results)
    counters = Counter()
    for res in results:
        counters.update(res)
        #for key, value in res.most_common(None):
        #    counters[key] += value
    
    print(counters.most_common(10))
    return counters

def day23_space2(bots):
    counters = Counter()
    for x, y, z, r in bots:
        for i in range(-r, r+1):
            for j in range(-r, r+1):
                for k in range(-r, r+1):
                    if day23_manhattan(x, y, z, x+k, y+j, z+i) <= r:
                        key = "{0},{1},{2}".format(x+k, y+j, z+i)
                        #if key in counters:
                        counters[key] += 1
                        #else:
                        #    counters[key] = 1
    #sorted_counters = sorted(counters.items(), key=lambda kv: kv[1], reverse=True)
    #print(sorted_counters[0])
    print(counters.most_common(10))
    return counters

def day23_space2_new(bots):
    counters = Counter()
    for x, y, z in bots:
        key = "{0},{1},{2}".format(x, y, z)
        #if key in counters:
        counters[key] += 1
        #else:
        #    counters[key] = 1
    #sorted_counters = sorted(counters.items(), key=lambda kv: kv[1], reverse=True)
    #print(sorted_counters[0])
    #print(counters.most_common(10))
    return counters

def day23_bounds(bots):
    min_x = sys.maxsize
    max_x = 0
    min_y = sys.maxsize
    max_y = 0
    min_z = sys.maxsize
    max_z = 0

    for x, y, z, r in bots:
        if x - r < min_x:
            min_x = x - r
        if x + r > max_x:
            max_x = x + r
        if y - r < min_y:
            min_y = y - r
        if y + r > max_y:
            max_y = y + r
        if z - r < min_z:
            min_z = z - z
        if z + r > max_z:
            max_z = z + r
    
    return (min_x, max_x, min_y, max_y, min_z, max_z)

def day23_space3(bots, min_x, max_x, min_y, max_y, z2):
    counters = Counter()
    for j in range(min_y, max_y+1):
        for k in range(min_x, max_x+1):
            for x, y, z, r in bots:
                if day23_manhattan(x, y, z, k, j, z2) <= r:
                    key = "{0},{1},{2}".format(k, j, z2)
                    counters[key] += 1
    #print(counters.most_common(10))
    #print(z2)
    return counters


def day23_new_bew(bots, min_x, max_x, min_y, max_y, z2):
    counters = Counter()
    for j in range(min_y, max_y+1):
        for k in range(min_x, max_x+1):
            for x, y, z, r in bots:
                if day23_manhattan(x, y, z, k, j, z2) <= r:
                    key = "{0},{1},{2}".format(k, j, z2)
                    counters[key] += 1
    #print(counters.most_common(10))
    #print(z2)
    return counters

def day23_1(data):
    #data = read_input(2018, 2301)
    bots = day23_parse_input(data)
    return len(day23_bots_in_range(bots, bots[0]))

def day23_2(data):
    return
    # data = read_input(2018, 2302)
    bots = day23_parse_input(data)
    # min_x, max_x, min_y, max_y, min_z, max_z = day23_bounds(bots)
    # for i in range(min_z, max_z+1):
    #     for j in range(min_y, max_y+1):
    #         for k in range(min_x, max_x+1):
    #             m = 0
    # return

    # ranges = [(i, 0) for i in range(len(bots))]
    # for i in range(len(bots)):
    #     ranges[i] = (i, day23_bots_in_range(bots, bots[i]))
    # ranges = sorted(ranges, reverse=True, key=lambda e: e[1])
    # best_bot = bots[ranges[0][0]]
    #return day23_new_bew(bots, best_bot)


    day23_space_paralel(bots)
    #day23_space2(bots)
    return
    space, min_x, min_y, min_z = day23_space(bots)
    counter = 0
    coord = (0,0,0)
    for z in range(len(space)):
        for y in range(len(space[z])):
            for x in range(len(space[z][y])):
                if space[z][y][x] > counter:
                    counter = space[z][y][x]
                    coord = (x + min_x, y + min_y, z + min_z)
    return counter, coord

""" DAY 24 """

class P_24:
    Units = 0
    Hit_points = 1
    Immunity = 2
    Weakness = 3
    Attack_Power = 4
    Attack_Type = 5
    Initiative = 6
    Id = 7

def day24_parse_group(line, id):
    # 4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
    units, hit_points, immunity, weakness, attack_power, attack_type, initiative = re.findall("(\d+) units each with (\d+) hit points (?:\((?:immune to ((?:(?:\w+)(?:, )?)+)(?:; )?)?(?:weak to ((?:(?:\w+)(?:, )?)+))?\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)", line)[0]
    return (int(units), int(hit_points), immunity.split(", "), weakness.split(", "), int(attack_power), attack_type, int(initiative), id)

def day24_parse_input(data):
    groups = [[],[]]
    current_army = 0
    id_counter = 0

    for line in data:
        if line == "Immune System:":
            current_army = 0
            id_counter = 0
            continue
        elif line == "Infection:":
            current_army = 1
            id_counter = 0
            continue
        elif line == "":
            continue
        group = day24_parse_group(line, "{0}_{1}".format(current_army, id_counter))
        id_counter += 1
        groups[current_army].append(group)
    return groups

def day24_debug_armies(armies):
    print("Immune System:")
    day24_debug_army(armies[0])
    print("Infection:")
    day24_debug_army(armies[1])
    print()
 
def day24_debug_army(army):
    for group in army:
        if group[P_24.Units] > 0:
            print("Group {0} contains {1} units".format(group[P_24.Id], group[P_24.Units]))
 
def day24_debug_target(attack_id, defend_id, damage):
    print("Group {0} would deal defending group {1} {2} damage".format(attack_id, defend_id, damage))

def day24_parse_id(id):
    parts = id.split("_")
    return (int(parts[0]), int(parts[1]))

def day24_effective_power(group):
    return group[P_24.Units] * group[P_24.Attack_Power]

def day24_damage(attack_group, defend_group):
    damage = day24_effective_power(attack_group)
    attack_type = attack_group[P_24.Attack_Type]
    immunity = defend_group[P_24.Immunity]
    weakness = defend_group[P_24.Weakness]

    if attack_type in immunity:
        return 0
    elif attack_type in weakness:
        return 2*damage

    return damage

def day24_target_criteria(attack_group, defend_group):
    return (day24_damage(attack_group, defend_group), day24_effective_power(defend_group), defend_group[P_24.Initiative])

def day24_selection_criteria(group):
    return (day24_effective_power(group), group[P_24.Initiative])

def day24_select_target(group, opposing_army, targeted, include_zero):
    available = [enemy for enemy in opposing_army if enemy[P_24.Units] > 0 and enemy[P_24.Id] not in targeted]
    targets = sorted(available, reverse=True, key=lambda g: day24_target_criteria(group, g))
    if len(targets) == 0:
        return None
    elif len(targets) > 1 and day24_target_criteria(group, targets[0]) == day24_target_criteria(group, targets[1]):
        # Can't decide
        return None
    
    if day24_damage(group, targets[0]) == 0 and not include_zero:
        return None

    #day24_debug_target(group[P_24.Id], targets[0][P_24.Id], day24_damage(group, targets[0]))
    return targets[0][P_24.Id]

def day24_target_selection_phase(armies):
    targeting_map = {}
    for current_army in range(2):
        opposing_army = (current_army+1)%2
        army = sorted(armies[current_army], reverse=True, key=lambda g: day24_selection_criteria(g))
        for group in army:
            if group[P_24.Units] > 0:
                target = day24_select_target(group, armies[opposing_army], targeting_map.values(), include_zero=False)
                if target != None:
                    targeting_map[group[P_24.Id]] = target
    for current_army in range(2):
        opposing_army = (current_army+1)%2
        army = sorted(armies[current_army], reverse=True, key=lambda g: day24_selection_criteria(g))
        for group in army:
            if group[P_24.Units] > 0 and not (group[P_24.Id] in targeting_map.keys()):
                target = day24_select_target(group, armies[opposing_army], targeting_map.values(), include_zero=True)
                if target != None:
                    targeting_map[group[P_24.Id]] = target
    #print()
    return targeting_map

def day24_attack_phase(groups_by_initiative, armies, targeting_map):
    kills = 0
    for group_id in groups_by_initiative:
        attack_army_id, attack_group_id = day24_parse_id(group_id)
        attack_group = armies[attack_army_id][attack_group_id]
        if group_id in targeting_map:
            target_id = targeting_map[group_id]
            target_army_id, target_group_id = day24_parse_id(target_id)
            target_group = armies[target_army_id][target_group_id]
            if target_group[P_24.Units] > 0:
                damage = day24_damage(attack_group, target_group)
                dead_units = min(math.floor(damage/(target_group[P_24.Hit_points])), target_group[P_24.Units])
                kills += dead_units
                #print("Group {0} attacks defending group {1}, killing {2} units".format(group_id, target_id, dead_units))
                armies[target_army_id][target_group_id] = (target_group[P_24.Units] - dead_units, target_group[P_24.Hit_points], target_group[P_24.Immunity], target_group[P_24.Weakness], target_group[P_24.Attack_Power], target_group[P_24.Attack_Type], target_group[P_24.Initiative], target_group[P_24.Id])
        #print()
    return kills == 0

def day24_fight(armies):
    groups_by_initiative = [group[P_24.Id] for group in sorted([group for army in armies for group in army], reverse=True, key=lambda g: g[P_24.Initiative])]
    while any([group[P_24.Units] > 0 for group in armies[0]]) and any([group[P_24.Units] > 0 for group in armies[1]]):
        #day24_debug_armies(armies)
        targeting_map = day24_target_selection_phase(armies)
        stalemate = day24_attack_phase(groups_by_initiative, armies, targeting_map)
        if stalemate:
            break

    return armies

def day24_add_boost(army, boost):
    return [(target_group[P_24.Units], \
             target_group[P_24.Hit_points], \
             target_group[P_24.Immunity], \
             target_group[P_24.Weakness], \
             target_group[P_24.Attack_Power] + boost, \
             target_group[P_24.Attack_Type], \
             target_group[P_24.Initiative], \
             target_group[P_24.Id]) for target_group in army]

def day24_clone_army(army):
    return [(target_group[P_24.Units], \
             target_group[P_24.Hit_points], \
             target_group[P_24.Immunity], \
             target_group[P_24.Weakness], \
             target_group[P_24.Attack_Power], \
             target_group[P_24.Attack_Type], \
             target_group[P_24.Initiative], \
             target_group[P_24.Id]) for target_group in army]

def day24_test_boost(armies, boost):
    new_armies = [day24_clone_army(armies[0]), day24_clone_army(armies[1])]
    new_armies[0] = day24_add_boost(armies[0], boost)
    new_armies = day24_fight(new_armies)
    remaining = sum([group[P_24.Units] for group in new_armies[0]])
    other = sum([group[P_24.Units] for group in new_armies[1]])
    
    return (boost, remaining, other)

def day24_boost_immune(armies):
    remaining = 0
    other = 1
    boost = 1
    threads = 16
    pool = mp.Pool(processes=threads)
    while True:
        process = range(boost, boost + threads + 1)
        boost = boost + threads + 1

        results = pool.map(functools.partial(day24_test_boost, armies), process)
        success = [result for result in results if result[2] == 0]
        success = sorted(success, key=lambda x: x[0])
        if len(success) > 0:
            remaining = success[0][1]
            break
    pool.close()
    pool.join()
    return remaining

def day24_1(data):
    #data = read_input(2018, 2401)
    armies = day24_parse_input(data)
    result = day24_fight(armies)
    total1 = sum([group[P_24.Units] for group in armies[0]])
    total2 = sum([group[P_24.Units] for group in armies[1]])
    return max(total1, total2)

def day24_2(data):
    #data = read_input(2018, 2401)
    armies = day24_parse_input(data)
    return day24_boost_immune(armies)

""" DAY 25 """

def day25_manhattan(point1, point2):
    (a1, b1, c1, d1), (a2, b2, c2, d2) = (point1, point2)
    return abs(a1-a2) + abs(b1-b2) + abs(c1-c2) + abs(d1-d2)

def day25_constellations(points):
    constellations = []

    for point in points:
        belonging = []
        for i in range(len(constellations)):
            constellation = constellations[i]
            belongs = False
            for other in constellation:
                if day25_manhattan(point, other) <= 3:
                    belongs = True
                    break
            if belongs:
                belonging.append(i)

        if len(belonging) == 0:
            constellations.append(deque([point]))
        else:
            i = 0
            c = constellations[belonging[i]]
            c.append(point)
            i+=1
            while i < len(belonging):
                c.extend(constellations[belonging[i]])
                constellations[belonging[i]].clear()
                i+=1
    
    return [c for c in constellations if len(c) > 0]

def day25_parse_input(data):
    # -2,-2,-2,2

    points = deque([])
    for line in data:
        point = tuple([int(x) for x in re.findall("(-?\d+),(-?\d+),(-?\d+),(-?\d+)", line)[0]])
        points.append(point)

    return points

def day25_1(data):
    #data = read_input(2018, 2504)
    points = day25_parse_input(data)
    return len(day25_constellations(points))

# start_day = 25
""" MAIN FUNCTION """
if __name__ == "__main__":
    for i in range(start_day,26):
        execute_day(globals(), 2018, i, 1)
        execute_day(globals(), 2018, i, 2)