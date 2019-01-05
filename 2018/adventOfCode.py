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

# pylint: disable=W0611
# pylint: disable=C0413
FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "\\..\\")
from common.utils import execute_day, read_input
# pylint: enable=W0611
# pylint: enable=C0413

START_DAY = 1

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
        i += 1
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
    for i, _ in enumerate(box1):
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
    raise ValueError

""" DAY 3 """

def day3_build_fabric(size):
    return [[0 for y in range(size)] for x in range(size)]

def day3_process_claim(line):
    # #1 @ 1,3: 4x4
    return tuple([int(x) for x in re.findall(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", line)[0]])

def day3_fill_claim(claim, fabric):
    (_, left, top, width, height) = claim
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
        day3_fill_claim(day3_process_claim(claim), fabric)
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
        day3_fill_claim(day3_process_claim(claim), fabric)
    for claim in data:
        res = day3_check_prestine(day3_process_claim(claim), fabric)
        if res != "":
            return res

    raise ValueError

""" DAY 4 """

def day4_process_log(log):
    shift = re.findall(r"Guard #(\d+) begins shift", log)
    if shift:
        return ("shift", int(shift[0]))
    wake = re.findall(r"(wakes up)", log)
    if wake:
        return ("wake", 0)
    asleep = re.findall(r"(falls asleep)", log)
    if asleep:
        return ("asleep", 0)

    raise ValueError

def day4_parse_and_sort(data):
    # [1518-07-18 23:57] Guard #157 begins shift
    # [1518-04-18 00:44] wakes up
    # [1518-10-26 00:20] falls asleep
    parsed_data = [re.findall(r"\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.+)", line)[0] for line in data]
    parsed_data.sort(key=lambda elem: str(elem[1]) + str(elem[2] + str(elem[3]) + str(elem[4])))
    parsed_data = [ \
                    tuple([
                        int(log[0]),
                        int(log[1]),
                        int(log[2]),
                        int(log[3]),
                        int(log[4]),
                        day4_process_log(log[5])]) \
                    for log in parsed_data]
    return parsed_data

def day4_process(data):
    ordered_log = day4_parse_and_sort(data)
    history = {}
    last_guard = -1
    last_asleep = -1
    sleeping = False
    for (_, _, _, _, minute, log) in ordered_log:
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
    return history

def day4_1(data):
    #data = read_input(2018, 401)
    history = day4_process(data)
    sleepiest_guard = sorted(
        [(k, sum(v)) for k, v in history.items()],
        key=lambda elem: elem[1],
        reverse=True)[0][0]

    m = 0
    for i in range(60):
        if history[sleepiest_guard][i] > history[sleepiest_guard][m]:
            m = i
    return m * sleepiest_guard

def day4_2(data):
    #data = read_input(2018, 401)
    history = day4_process(data)
    sleepiest_guard = sorted(
        [(k, max(v)) for k, v in history.items()],
        key=lambda elem: elem[1],
        reverse=True)[0][0]

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
            i -= 1
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
    for i, _ in enumerate(grid):
        for j, _ in enumerate(grid[i]):
            dists = [abs(coordinate[1]-i) + abs(coordinate[0]-j) for coordinate in coordinates]
            min_dist = sys.maxsize
            min_id = 0
            for id_, _ in enumerate(dists):
                if dists[id_] < min_dist:
                    min_id = id_
                    min_dist = dists[id_]
                elif dists[id_] == min_dist:
                    min_id = "_"
                    min_dist = dists[id_]
            grid[i][j] = (min_id, min_dist)

def day6_1(data):
    #data = read_input(2018, 601)
    coordinates = [(int(entry.split(", ")[0]), int(entry.split(", ")[1])) for entry in data]

    max_x = max([coordinate[0] for coordinate in coordinates])
    max_y = max([coordinate[1] for coordinate in coordinates])

    grid = [[(".", 0) for j in range(max_x + 1)] for i in range(max_y + 1)]

    day6_fill_grid(grid, coordinates)
    #day6_debug_grid(grid)

    ids = [i for i in range(len(coordinates))]
    for i, _ in enumerate(grid):
        if i in (0, len(grid) - 1):
            for j, _ in enumerate(grid[i]):
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
    for id_ in ids:
        temp_count = 0
        for i, _ in enumerate(grid):
            for j, _ in enumerate(grid[i]):
                if grid[i][j][0] == id_:
                    temp_count += 1
        if temp_count > max_val:
            max_val = temp_count

    return max_val

def day6_2(data):
    size = 10000
    #data, size = (read_input(2018, 601), 32)
    coordinates = [(int(entry.split(", ")[0]), int(entry.split(", ")[1])) for entry in data]

    max_x = max([coordinate[0] for coordinate in coordinates])
    max_y = max([coordinate[1] for coordinate in coordinates])

    counter = 0
    for i in range(max_y + 1):
        for j in range(max_x + 1):
            dists = functools.reduce(
                lambda acc, coordinate, i_=i, j_=j:
                acc + abs(coordinate[1]-i_) + abs(coordinate[0]-j_),
                coordinates,
                0)
            if dists < size:
                counter += 1
    return counter

""" DAY 7 """

def day7_parse_inst(data):
    # Step C must be finished before step A can begin.
    parsed_data = [
        re.findall(r"Step ([A-Z]) must be finished before step ([A-Z]) can begin.", line)[0]
        for line in data]
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
    while stack:
        next_letter = stack.pop(0)
        completed.append(next_letter)
        for step, deps in dependencies.items():
            if not step in completed and \
               not step in stack and \
               all([dep in completed for dep in deps]):
                stack.append(step)
        stack.sort()
    return completed

def day7_1(data):
    #data = read_input(2018, 701)
    (dependencies, _) = day7_parse_inst(data)
    return ''.join(day7_inst_order(dependencies, list(string.ascii_uppercase)))

def day7_worker(worker, completed):
    if not worker is None:
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
    counter = 0
    while stack or any([not w is None for w in workers]):
        counter += 1
        for i, _ in enumerate(workers):
            if workers[i] is None and stack:
                workers[i] = stack.pop(0)
            completed, worker = day7_worker(workers[i], completed)
            workers[i] = worker

        for step, deps in dependencies.items():
            if not step in completed and \
               all([let[0] != step for let in stack]) and \
               all([dep in completed for dep in deps]) and \
               not any([not w is None and w[0] == step for w in workers]):
                stack.append((step, (ord(step)-ord("A") + 1) + step_duration))
        stack.sort()
    return counter

def day7_2(data):
    step_duration = 60
    workers = 5
    letters = list(string.ascii_uppercase)
    # data, step_duration, letters, workers = \
    #     (read_input(2018, 701), 0, ["A", "B", "C", "D", "E", "F"], 2)
    (dependencies, letters) = day7_parse_inst(data)
    return day7_inst_order2(dependencies, letters, step_duration, workers)

""" DAY 8 """

class PropertyDescription(Enum):
    Header = 1
    Metadata_Definition = 3
    Nodes_End = 2

def day8_process_operation(data, operation, curr_node, nodes, operations):
    if operation == PropertyDescription.Header:
        nodes = data.pop(0)
        metadata = data.pop(0)
        operations.insert(0, PropertyDescription.Nodes_End)
        for _ in range(metadata):
            operations.insert(0, PropertyDescription.Metadata_Definition)
        for _ in range(nodes):
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

    raise ValueError

def day8_parse_tree(data):
    nodes = []
    # Metadata, children, parent
    curr_node = ([], [], None)
    operations = [PropertyDescription.Header]
    while operations:
        operation = operations.pop(0)
        data, curr_node, operations = \
            day8_process_operation(data, operation, curr_node, nodes, operations)
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
    metadata, children, _ = node
    if not children:
        return sum(metadata)

    total = 0
    for meta in metadata:
        idx = meta - 1
        if 0 <= idx < len(children):
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
    #marble_0 = current_marble
    next_marble = 1
    player = 0
    while next_marble <= highest_marble:
        #day9_debug_marbles(marble_0, current_marble)
        if next_marble % 23 != 0:
            for _ in range(2):
                current_marble = current_marble.next
            current_marble = day9_add_marble_before(current_marble, next_marble)
        else:
            scores[player] += next_marble
            for _ in range(7):
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
    while next_marble <= highest_marble:
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
    return tuple([int(a)
                  for a in
                  re.findall(r"(\d+) players; last marble is worth (\d+) points", data)[0]])

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

def day10_parse_line(line):
    # position=< 32923,  43870> velocity=<-3, -4>
    res = re.findall(r"position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>", line)[0]
    return tuple([int(a) for a in res])

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
    particles, _ = day10_resolve(day10_parse_input(data))
    day10_print_particles(particles)

def day10_2(data):
    #data = read_input(2018, 1001)
    _, counter = day10_resolve(day10_parse_input(data))
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
    return [[day11_cell_value(serial, x+1, y+1)  for x in range(300)] for y in range(300)]

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
    while y <= len(grid) - size:
        x = 0
        while x <= len(grid) - size:
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
                    x += 1
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
    initial_state = deque(re.findall(r"initial state: ([\.|#]*)", data[0])[0])
    rules = deque([])
    for rule in data[2:]:
        parts = rule.split(" => ")
        rules.append((parts[0], parts[1]))
    return (initial_state, rules)

def day12_get_rule(pots, rules, position):
    for rule in rules:
        prev = rule[0]
        match = True
        for i, _ in enumerate(prev):
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
        if result is None:
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
            while j < itera:
                history.popleft()
                j += 1
            pos = (generations-(i+1))%len(history)
            pos_shift = start - history[pos][1]

            iterations = math.floor((generations-(i+1))/len(history))
            pots = history[pos][0]
            start += pos_shift*iterations
            break

    total = 0
    for i, _ in enumerate(pots):
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

class Turn(Enum):
    Left = 0
    Straight = 1
    Right = 2

class Direction(Enum):
    Left = 0
    Up = 1
    Right = 2
    Down = 3

def day13_print_direction(dir_):
    if dir_ == Direction.Up:
        return "^"
    elif dir_ == Direction.Down:
        return "v"
    elif dir_ == Direction.Left:
        return "<"
    elif dir_ == Direction.Right:
        return ">"

    raise ValueError

def day13_debug_map(map_, positions):
    for y, _ in enumerate(map_):
        line = ""
        for x, _ in enumerate(map_[y]):
            cart = [positions[k]
                    for k in range(len(positions))
                    if positions[k][0] == x and positions[k][1] == y]
            if len(cart) == 1:
                cart = cart[0]
            else:
                cart = None

            if cart is None:
                line += map_[y][x]
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
    elif pos == "<":
        return Direction.Left
    elif pos == ">":
        return Direction.Right
    return None

def day13_parse_input(data):
    map_ = []
    positions = []
    for row, _ in enumerate(data):
        new_row = []
        for column, _ in enumerate(data[row]):
            direction = day13_get_cart_direction(data[row][column])
            if direction is None:
                new_row.append(data[row][column])
            else:
                positions.append((column, row, direction, Turn.Right))
                if direction in (Direction.Left, Direction.Right):
                    new_row.append("-")
                else:
                    new_row.append("|")
        map_.append(new_row)
    return map_, sorted(positions, key=lambda v: (v[0], v[1]))

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

    return ValueError

def day13_move_cart(map_, positions, cart):
    x = positions[cart][0]
    y = positions[cart][1]
    direction = positions[cart][2]
    last_turn = positions[cart][3]

    delta_x, delta_y = day13_get_direction_delta(direction)
    new_x, new_y = x + delta_x, y + delta_y
    for i, _ in enumerate(positions):
        if i != cart and positions[i][0] == new_x and positions[i][1] == new_y:
            return "X", new_x, new_y, i

    new_direction, new_turn = day13_next_turn(map_[new_y][new_x], direction, last_turn)

    return (new_x, new_y, new_direction, new_turn)

def day13_solve(map_, positions):
    while True:
        #day13_debug_map(map, positions)
        for i, _ in enumerate(positions):
            new_position = day13_move_cart(map_, positions, i)
            if new_position[0] == "X":
                return new_position[1], new_position[2]
            positions[i] = new_position
        positions = sorted(positions, key=lambda v: (v[0], v[1]))

def day13_solve2(map_, positions):
    while True:
        #day13_debug_map(map, positions)
        crashing_carts = []
        for i, _ in enumerate(positions):
            new_position = day13_move_cart(map_, positions, i)
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
    map_, positions = day13_parse_input(data)
    return day13_solve(map_, positions)

def day13_2(data):
    #data = read_input(2018, 1302)
    map_, positions = day13_parse_input(data)
    return day13_solve2(map_, positions)

""" DAY 14 """

def day14_debug_recipes(recipes, elves):
    out = ""
    for i, _ in enumerate(recipes):
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
    for _ in range(nr_recipes+10):
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
    @staticmethod
    def addr(regs, a, b, c):
        regs[c] = regs[a] + regs[b]
        return regs

    @staticmethod
    def addi(regs, a, b, c):
        regs[c] = regs[a] + b
        return regs

    @staticmethod
    def mulr(regs, a, b, c):
        regs[c] = regs[a] * regs[b]
        return regs

    @staticmethod
    def muli(regs, a, b, c):
        regs[c] = regs[a] * b
        return regs

    @staticmethod
    def banr(regs, a, b, c):
        regs[c] = regs[a] & regs[b]
        return regs

    @staticmethod
    def bani(regs, a, b, c):
        regs[c] = regs[a] & b
        return regs

    @staticmethod
    def borr(regs, a, b, c):
        regs[c] = regs[a] | regs[b]
        return regs

    @staticmethod
    def bori(regs, a, b, c):
        regs[c] = regs[a] | b
        return regs

    @staticmethod
    def setr(regs, a, _, c):
        regs[c] = regs[a]
        return regs

    @staticmethod
    def seti(regs, a, _, c):
        regs[c] = a
        return regs

    @staticmethod
    def gtir(regs, a, b, c):
        if a > regs[b]:
            regs[c] = 1
        else:
            regs[c] = 0
        return regs

    @staticmethod
    def gtri(regs, a, b, c):
        if regs[a] > b:
            regs[c] = 1
        else:
            regs[c] = 0
        return regs

    @staticmethod
    def gtrr(regs, a, b, c):
        if regs[a] > regs[b]:
            regs[c] = 1
        else:
            regs[c] = 0
        return regs

    @staticmethod
    def eqir(regs, a, b, c):
        if a == regs[b]:
            regs[c] = 1
        else:
            regs[c] = 0
        return regs

    @staticmethod
    def eqri(regs, a, b, c):
        if regs[a] == b:
            regs[c] = 1
        else:
            regs[c] = 0
        return regs

    @staticmethod
    def eqrr(regs, a, b, c):
        if regs[a] == regs[b]:
            regs[c] = 1
        else:
            regs[c] = 0
        return regs

    ops = [
        addr.__func__,
        addi.__func__,
        mulr.__func__,
        muli.__func__,
        banr.__func__,
        bani.__func__,
        borr.__func__,
        bori.__func__,
        setr.__func__,
        seti.__func__,
        gtir.__func__,
        gtri.__func__,
        gtrr.__func__,
        eqir.__func__,
        eqri.__func__,
        eqrr.__func__
        ]

def day16_parse_input(data):
    samples = []
    i = 0
    while i < len(data):
        if data[i] == "":
            break
        # Before: [3, 2, 1, 1]
        # 9 2 1 2
        # After:  [3, 2, 2, 1]
        before = [int(x) for x in re.findall(r"Before: \[(\d+), (\d+), (\d+), (\d+)\]", data[i])[0]]
        i += 1
        inst = [int(x) for x in re.findall(r"(\d+) (\d+) (\d+) (\d+)", data[i])[0]]
        i += 1
        after = [int(x) for x in re.findall(r"After:  \[(\d+), (\d+), (\d+), (\d+)\]", data[i])[0]]
        i += 1
        i += 1
        samples.append((before, inst, after))

    program = []
    while i < len(data):
        if data[i] != "":
            # 9 2 1 2
            inst = [int(x) for x in re.findall(r"(\d+) (\d+) (\d+) (\d+)", data[i])[0]]
            program.append(inst)
        i += 1

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
        for i, _ in enumerate(mapping):
            if len(mapping[i]) == 1:
                op = mapping[i][0]
                for j, _ in enumerate(mapping):
                    if i != j:
                        mapping[j] = [op2 for op2 in mapping[j] if op2 != op]
        if all([len(mapping[i]) == 1 for i in range(len(mapping))]):
            break
    mapping = [m[0] for m in mapping]
    return mapping

def day16_solve2(samples, program):
    mapping = day16_calculate_mapping(samples)

    regs = [0, 0, 0, 0]
    for line in program:
        op = mapping[line[0]]
        regs = op(regs, line[1], line[2], line[3])
    return regs[0]

def day16_1(data):
    #data = read_input(2018, 1601)
    samples, _ = day16_parse_input(data)
    return day16_solve1(samples)

def day16_2(data):
    #data = read_input(2018, 1601)

    samples, program = day16_parse_input(data)
    return day16_solve2(samples, program)

""" DAY 17 """

class Bitmap():

    def __init__(self, width, height):
        self._bfType = 19778 # Bitmap signature
        self._bfReserved1 = 0
        self._bfReserved2 = 0
        self._bcPlanes = 1
        self._bcSize = 12
        self._bcBitCount = 24
        self._bfOffBits = 26
        self._bcWidth = width
        self._bcHeight = height
        self._bfSize = 26+self._bcWidth*3*self._bcHeight
        self.clear()

    def clear(self):
        self._graphics = [(0, 0, 0)]*self._bcWidth*self._bcHeight

    def setPixel(self, x, y, color):
        if isinstance(color, tuple):
            if x < 0 or y < 0 or x > self._bcWidth-1 or y > self._bcHeight-1:
                raise ValueError('Coords out of range')
            if len(color) != 3:
                raise ValueError('Color must be a tuple of 3 elems')
            self._graphics[y*self._bcWidth+x] = (color[2], color[1], color[0])
        else:
            raise ValueError('Color must be a tuple of 3 elems')

    def write(self, file):
        with open(file, 'wb') as f:
            f.write(pack('<HLHHL',
                         self._bfType,
                         self._bfSize,
                         self._bfReserved1,
                         self._bfReserved2,
                         self._bfOffBits)) # Writing BITMAPFILEHEADER
            f.write(pack('<LHHHH',
                         self._bcSize,
                         self._bcWidth,
                         self._bcHeight,
                         self._bcPlanes,
                         self._bcBitCount)) # Writing BITMAPINFO
            for px in self._graphics:
                f.write(pack('<BBB', *px))
            for _ in range(0, (self._bcWidth*3) % 4):
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
        raise ValueError

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

        raise ValueError

bitmap_counter = 0
def day17_debug_ground_bmp(ground, y):
# pylint: disable=W0603
    global bitmap_counter
# pylint: enable=W0603

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
    b = Bitmap(436, size)
    b.clear()
    for i, _ in enumerate(ground):
        for j, _ in enumerate(ground[i]):
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
            ground_slice = [int(x) for x in re.findall(r"x=(\d+), y=(\d+)..(\d+)", line)[0]]
            slices.append(ground_slice)
            if ground_slice[1] < min_y:
                min_y = ground_slice[1]
            if ground_slice[2] > max_y:
                max_y = ground_slice[2]
        else:
            # y=501, x=3..7
            ground_slice = [int(x) for x in re.findall(r"y=(\d+), x=(\d+)..(\d+)", line)[0]]
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

    ground = [[Day17_Type.sand for j in range(min_x, max_x)] for i in range(max_y + 2)]
    for s in slices:
        for i in range(s[1], s[2]+1):
            ground[i][s[0] - min_x] = Day17_Type.clay

    return ground, min_x, min_y

def day17_flow_water(ground, y, x):
    stack = deque([(y, x)])
    while stack:
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
        while k > 0:
            if ground[i][k] == Day17_Type.clay or ground[i][k] == Day17_Type.settled:
                left_wall = True
                break
            if ground[i][k] == Day17_Type.sand:
                break
            k -= 1

        k = j+1
        while k < len(ground[i]):
            if ground[i][k] == Day17_Type.clay or ground[i][k] == Day17_Type.settled:
                right_wall = True
                break
            if ground[i][k] == Day17_Type.sand:
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
    for i, _ in enumerate(ground):
        for j, _ in enumerate(ground[i]):
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
            if AcreContents.count_states(AcreContents.lumberyard, adjacents) == 0 or \
               AcreContents.count_states(AcreContents.trees, adjacents) == 0:
                return AcreContents.open
        return current

def day18_debug_area(area):
    for i, _ in enumerate(area):
        out = ""
        for j, _ in enumerate(area[i]):
            out += area[i][j]
        print(out)
    print()

def day18_get_adjacent_cells(area, i_coord, j_coord):
    # the adjacency matrix
    adjacency = [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if not i == j == 0]
    result = []
    for di, dj in adjacency:
        if 0 <= (i_coord + di) < len(area) and 0 <= j_coord + dj < len(area[0]): #boundaries check
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
        new_area = []
        for i, _ in enumerate(prev_area):
            new_area.append("")
            for j, _ in enumerate(prev_area[i]):
                new_state = day18_compute_change(prev_area, i, j)
                new_area[i] += new_state

        new_area_key = "".join(new_area)
        if new_area_key in memoization:
            itera = memoization[new_area_key]
            j = 0
            while j < itera:
                history.popleft()
                j += 1
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
           "eqrr": Inst16.eqrr}

def day19_parse_input(data):
    pointer = int(data[0][-1])

    program = []
    for line in data[1:]:
        inst = [x for x in re.findall(r"(\w+) (\d+) (\d+) (\d+)", line)[0]]
        inst[0] = Inst19.ops[inst[0]]
        inst[1] = int(inst[1])
        inst[2] = int(inst[2])
        inst[3] = int(inst[3])
        program.append(inst)

    return pointer, program

def day19_run_program(pointer, program, start_0, day, part):
    regs = [start_0, 0, 0, 0, 0, 0]
    inst = regs[pointer]
    counter = Counter()
    last = 0
    while 0 <= inst < len(program):
        # Make register 1 have the value of 2 * 5 right away (first loop)
        if day == 19 and inst == 4 and regs[1]/regs[2] == regs[5] and regs[2] < regs[3]/regs[5]:
            regs[2] = int(regs[3]/regs[5])
            regs[1] = regs[2]*regs[5]

        # Make register 2 have the value of 3 (second loop)
        if day == 19 and inst == 9 and regs[2] < regs[3]:
            regs[2] = regs[3]

        if day == 21 and inst == 28:
            if part == 1:
                return regs[5]
            value = regs[5]
            if counter[value] == 0:
                counter[value] = 1
                last = value
            else:
                return last

        regs[pointer] = inst
        f, a, b, c = program[inst]
        f(regs, a, b, c)
        inst = regs[pointer]
        inst += 1
    return regs

def day19_1(data):
    #data = read_input(2018, 1901)
    pointer, program = day19_parse_input(data)
    return day19_run_program(pointer, program, 0, 19, 1)[0]

def day19_2(data):
    #data = read_input(2018, 1901)
    pointer, program = day19_parse_input(data)
    return day19_run_program(pointer, program, 1, 19, 2)[0]

""" DAY 20 """

class PathNode:
    def __init__(self, pos, dist, path):
        "constructor class to initiate this object"

        # store data
        self.pos = pos
        self.dist = dist
        self.path = path

    def __repr__(self):
        return "({0},{1}) - {2} - {3}".format(self.pos[0], self.pos[1], self.dist, self.path)

def day20_move(pos, direction):
    x, y = pos
    if direction == "N":
        return (x, y + 1)
    if direction == "S":
        return (x, y - 1)
    if direction == "W":
        return (x - 1, y)
    if direction == "E":
        return (x + 1, y)
    raise ValueError

def day20_update_locations(direction, current_locations, history):
    for node in current_locations:
        pos = day20_move(node.pos, direction)
        node.pos = pos
        node.dist += 1
        key = "{0}_{1}".format(node.pos[0], node.pos[1])
        if not key in history:
            history[key] = node.dist
        elif node.dist < history[key]:
            history[key] = node.dist
        node.path = node.path + direction

def day20_alternatives(index, path, locations, distances):
    new_locations = []
    current_locations = [PathNode(n.pos, n.dist, n.path) for n in locations]
    while path[index] != ")":
        if path[index] == "(":
            current_locations, index = \
                day20_alternatives(index+1, path, current_locations, distances)
        elif path[index] == "|":
            new_locations.extend(current_locations)
            current_locations = [PathNode(n.pos, n.dist, n.path) for n in locations]
        else:
            day20_update_locations(path[index], current_locations, distances)
        index += 1
    new_locations.extend(current_locations)

    # Remove redundant paths
    result = {}
    for l in new_locations:
        key = "{0}_{1}".format(l.pos[0], l.pos[1])
        if key not in result:
            result[key] = l
        elif l.dist < result[key].dist:
            result[key] = l
    new_locations = result.values()
    return new_locations, index

def day20_get_rooms_distances(path):
    path = path[1:]
    index = 0
    distances = {}
    current_locations = [PathNode((0, 0), 0, "")]
    while path[index] != "$":
        if path[index] == "(":
            current_locations, index = \
                day20_alternatives(index+1, path, current_locations, distances)
        elif path[index] != ")":
            day20_update_locations(path[index], current_locations, distances)
        index += 1
    return distances

def day20_1(data):
    #data = read_input(2018, 2001)
    path = data[0]
    distances = day20_get_rooms_distances(path).values()
    best = sorted(distances, reverse=True, key=lambda v: v)[0]
    return best

def day20_2(data):
    #data = read_input(2018, 2001)
    path = data[0]
    distances = day20_get_rooms_distances(path).values()
    return len([d for d in distances if d >= 1000])

""" DAY 21 """

def day21_1(data):
    pointer, program = day19_parse_input(data)
    return day19_run_program(pointer, program, 1, 21, 1)

def day21_2(data):
    pointer, program = day19_parse_input(data)
    return day19_run_program(pointer, program, 1, 21, 2)

""" DAY 22 """

class Day22_Type:
    rocky = 0
    wet = 1
    narrow = 2

    @staticmethod
    def get_type(erosion_level):
        return erosion_level % 3

    @staticmethod
    def repr(tool):
        if tool == Day22_Type.rocky:
            return "."
        if tool == Day22_Type.wet:
            return "="
        if tool == Day22_Type.narrow:
            return "|"
        return None

class Day22_Tools:
    gear = 0
    torch = 1
    neither = 2

    @staticmethod
    def allowed_tool(region_type, tool):
        if region_type == Day22_Type.rocky:
            return tool in (Day22_Tools.gear, Day22_Tools.torch)
        if  region_type == Day22_Type.wet:
            return tool in (Day22_Tools.gear, Day22_Tools.neither)
        if  region_type == Day22_Type.narrow:
            return tool in (Day22_Tools.torch, Day22_Tools.neither)
        raise ValueError

    @staticmethod
    def repr(tool):
        if tool == Day22_Tools.torch:
            return "torch"
        if tool == Day22_Tools.gear:
            return "gear"
        if tool == Day22_Tools.neither:
            return "neither"
        return None

    tools = [gear, torch, neither]

class Day22_Path_Node:
    def __init__(self, x, y, delta_x, delta_y, tool, minutes, path):
        self.pos = (x, y)
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.tool = tool
        self.minutes = minutes
        self.path = path

    def __lt__(self, other): # For x < y
        return (self.minutes  + abs(self.delta_x)  + abs(self.delta_y)) < \
               (other.minutes + abs(other.delta_x) + abs(other.delta_y))

    def __eq__(self, other): # For x == y
        return self.pos == other.pos and \
               self.delta_x == other.delta_x and \
               self.delta_y == other.delta_y and \
               self.tool == other.tool and \
               self.minutes == other.minutes

    def __gt__(self, other): # For x > y
        return not self == other and not self < other

    def __le__(self, other): # For x <= y
        return self == other or self < other

    def __ne__(self, other): # For x != y OR x <> y
        return not self == other

    def __ge__(self, other): # For x >= y
        return self == other or self > other

    def __repr__(self):
        return "[{4}] ({0},{1}) - with {2} in {3} minutes".format(
            self.pos[0],
            self.pos[1],
            Day22_Tools.repr(self.tool),
            self.minutes,
            self.minutes + abs(self.delta_x) + abs(self.delta_y))

def day22_parse_input(data):
    depth = int(data[0].split(" ")[1])
    target = data[1].split(" ")[1]
    target_coords = tuple([int(x) for x in target.split(",")])
    return depth, target_coords

def day22_geologic_index(pos, target, depth, memory):
    if memory[pos] != 0:
        return memory[pos]
    x, y = pos
    value = 0
    if x == y == 0 or pos == target:
        value = 0
    elif x == 0:
        value = y * 48271
    elif y == 0:
        value = x * 16807
    else:
        left = day22_erosion_level((x-1, y), target, depth, memory)
        up = day22_erosion_level((x, y-1), target, depth, memory)
        value = left * up
    memory[pos] = value
    return value

def day22_erosion_level(pos, target, depth, memory):
    index = day22_geologic_index(pos, target, depth, memory)
    return (index + depth) % 20183

def day22_get_terrain(depth, target):
    total = 0
    terrain = {}
    memory = Counter()
    for x in range(0, target[0] + 1):
        for y in range(0, target[1] + 1):
            pos = (x, y)
            erosion = day22_erosion_level(pos, target, depth, memory)
            region_type = Day22_Type.get_type(erosion)
            total += region_type
            terrain[pos] = region_type
    return total, (terrain, memory)

def day22_debug_map(terrain, depth, target, node):
    for y in range(0, target[1] + 5):
        line = ""
        for x in range(0, target[0] + 5):
            erosion = day22_erosion_level((x, y), target, depth, terrain[1])
            terrain[0][(x, y)] = Day22_Type.get_type(erosion)
            if node.x == x and node.y == y:
                line += Day22_Tools.repr(node.tool)[0]
            elif x == target[0] and y == target[1]:
                line += "T"
            else:
                line += Day22_Type.repr(terrain[(x, y)])
        print(line)
    print()
    time.sleep(.5)

def day22_total_risk(depth, target):
    total, _ = day22_get_terrain(depth, target)
    return total

def day22_new_nodes(node, terrain, depth, target, delta_x, delta_y):
    node_x, node_y = node.pos
    new_x, new_y = node_x + delta_x, node_y + delta_y
    if new_x < 0 or new_y < 0:
        return []
    if (new_x, new_y) not in terrain[0]:
        erosion = day22_erosion_level((new_x, new_y), target, depth, terrain[1])
        terrain[0][(new_x, new_y)] = Day22_Type.get_type(erosion)
    new_terrain = terrain[0][(new_x, new_y)]
    alternatives = []
    for tool in Day22_Tools.tools:
        if Day22_Tools.allowed_tool(new_terrain, tool):
            if tool == node.tool:
                alternatives = [
                    Day22_Path_Node(new_x,
                                    new_y,
                                    target[0] - new_x,
                                    target[1] - new_y,
                                    tool,
                                    node.minutes + 1,
                                    node.path + [node])
                                ]
                break
            elif Day22_Tools.allowed_tool(terrain[0][node.pos], tool):
                alternatives.append(
                    Day22_Path_Node(
                        node_x,
                        node_y,
                        target[0] - node_x,
                        target[1] - node_y,
                        tool,
                        node.minutes + 7,
                        node.path + [node])
                    )
    return alternatives

def day22_manhattan_adjacency():
    return [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if not i == j and (i == 0 or j == 0)]

def day22_find_path(depth, target):
    _, terrain = day22_get_terrain(depth, target)

    heap = [
        Day22_Path_Node(0, 0, target[0], target[1], Day22_Tools.torch, 0, [])
    ]
    heapq.heapify(heap)
    visited = {}
    while heap:
        node = heapq.heappop(heap)
        if node.pos == target and node.tool == Day22_Tools.torch:
            return node

        for delta_x, delta_y in day22_manhattan_adjacency():
            for new_node in day22_new_nodes(node, terrain, depth, target, delta_x, delta_y):
                new_node_x, new_node_y = new_node.pos
                key = (new_node_x, new_node_y, new_node.tool)
                if key not in visited or (visited[key] > new_node.minutes):
                    visited[key] = new_node.minutes
                    heapq.heappush(heap, new_node)

    raise ValueError

def day22_1(data):
    #data = read_input(2018, 2201)
    depth, target = day22_parse_input(data)
    return day22_total_risk(depth, target)

def day22_2(data):
    #data = read_input(2018, 2201)
    depth, target = day22_parse_input(data)
    node = day22_find_path(depth, target)

    # _, terrain = day22_get_terrain(depth, target)
    # for n in node.path:
    #     day22_debug_map(terrain, depth, target, n)
    return node.minutes

""" DAY 23 """

def day23_parse_input(data):
    # pos=<-5920414,66954528,45418976>, r=94041555
    bots = []
    for line in data:
        bot = [int(x) for x in re.findall(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)", line)[0]]
        bots.append(((bot[0], bot[1], bot[2]), bot[3]))
    return sorted(bots, reverse=True, key=lambda b: b[1])

def day23_manhattan(bot, other_bot):
    x, y, z = bot
    other_x, other_y, other_z = other_bot
    return abs(x - other_x) + abs(y - other_y) + abs(z - other_z)

def day23_bots_in_range(bots, bot):
    in_range = []
    bot_coord, signal = bot
    for other_bot in bots:
        other_bot_coord, _ = other_bot
        if day23_manhattan(bot_coord, other_bot_coord) <= signal:
            in_range.append(other_bot)
    return in_range

def day23_bounds(bots):
    min_x = min_y = min_z = sys.maxsize
    max_x = max_y = max_z = 0

    for coord, r in bots:
        x, y, z = coord
        min_x = min(x - r, min_x)
        max_x = max(x + r, max_x)
        min_y = min(y - r, min_y)
        max_y = max(y + r, max_y)
        min_z = min(z - r, min_z)
        max_z = max(z + r, max_z)

    return (min_x, max_x, min_y, max_y, min_z, max_z)

def day23_squared(v):
    return v*v

def day23_intersect(zone, coord, r):
    min_x, max_x, min_y, max_y, min_z, max_z = zone
    x, y, z = coord
    dist_squared = r * r

    if x < min_x:
        dist_squared -= day23_squared(x - min_x)
    elif x > max_x:
        dist_squared -= day23_squared(x - max_x)

    if y < min_y:
        dist_squared -= day23_squared(y - min_y)
    elif y > max_y:
        dist_squared -= day23_squared(y - max_y)

    if z < min_z:
        dist_squared -= day23_squared(z - min_z)
    elif z > max_z:
        dist_squared -= day23_squared(z - max_z)

    return dist_squared > 0

def day23_corners(zone):
    min_x, max_x, min_y, max_y, min_z, max_z = zone
    for x in (min_x, max_x):
        for y in (min_y, max_y):
            for z in (min_z, max_z):
                yield (x, y, z)

def day23_bots_in_reach(bots, zone):
    if zone is None:
        return []

    min_x, max_x, min_y, max_y, min_z, max_z = zone

    in_reach = deque([])
    for bot in bots:
        coord, r = bot
        x, y, z = coord

        # Bot is inside zone
        if min_x <= x <= max_x and \
           min_y <= y <= max_y and \
           min_z <= z <= max_z:
            in_reach.append(bot)
            continue

        # Sphere of bot's signal doesn't intersect zone
        if not day23_intersect(zone, coord, r):
            continue

        # Is any corner of the zone within the bot's signal?
        for corner in day23_corners(zone):
            if day23_manhattan(coord, corner) <= r:
                in_reach.append(bot)
                break

    return in_reach

def day23_get_subzones(zone):
    min_x, max_x, min_y, max_y, min_z, max_z = zone
    len_x = max_x - min_x
    half_x = math.floor(len_x / 2)
    len_y = max_y - min_y
    half_y = math.floor(len_y / 2)
    len_z = max_z - min_z
    half_z = math.floor(len_z / 2)

    if len_x == 0 or len_y == 0 or len_z == 0:
        return [None]

    zone_1 = (min_x, min_x + half_x, min_y, min_y + half_y, min_z, min_z + half_z)
    zone_2 = (min_x, min_x + half_x, min_y, min_y + half_y, min_z + half_z + 1, max_z)
    zone_3 = (min_x, min_x + half_x, min_y + half_y + 1, max_y, min_z, min_z + half_z)
    zone_4 = (min_x, min_x + half_x, min_y + half_y + 1, max_y, min_z + half_z + 1, max_z)
    zone_5 = (min_x + half_x + 1, max_x, min_y, min_y + half_y, min_z, min_z + half_z)
    zone_6 = (min_x + half_x + 1, max_x, min_y, min_y + half_y, min_z + half_z + 1, max_z)
    zone_7 = (min_x + half_x + 1, max_x, min_y + half_y + 1, max_y, min_z, min_z + half_z)
    zone_8 = (min_x + half_x + 1, max_x, min_y + half_y + 1, max_y, min_z + half_z + 1, max_z)

    return (zone_1, zone_2, zone_3, zone_4, zone_5, zone_6, zone_7, zone_8)

def day23_thread_worker(bots, zone):
    return (zone, day23_bots_in_reach(bots, zone))

def day23_bot_count_in_subzones(bots, zone, pool):
    zones_to_process = day23_get_subzones(zone)
    results = pool.map(functools.partial(day23_thread_worker, bots), zones_to_process)

    most_bots_count = max([len(r[1]) for r in results])

    if most_bots_count == 0:
        return []

    # Negative count to be used on heapq
    return [(-most_bots_count, r[0])
            for r in results
            if len(r[1]) == most_bots_count
           ]

def day23_zone_dimensions(zone):
    min_x, max_x, min_y, max_y, min_z, max_z = zone
    return (max_x - min_x, max_y - min_y, max_z - min_z)

def day23_get_locations_counts(bots, best_zones):
    locations = deque([])
    for zone, _ in best_zones:
        min_x, max_x, min_y, max_y, min_z, max_z = zone
        for x2 in range(min_x, max_x+1):
            for y2 in range(min_y, max_y+1):
                for z2 in range(min_z, max_z+1):
                    test_coord = (x2, y2, z2)
                    counter = 0
                    for coord, r in bots:
                        if day23_manhattan(coord, test_coord) <= r:
                            counter += 1
                    locations.append((test_coord, counter))
    return locations

def day23_calculate_best_distance(best_locations):
    locations_distances = []
    for location in best_locations:
        locations_distances.append(day23_manhattan(location, (0, 0, 0)))

    return sorted(locations_distances, reverse=True)[0]

def day23_best_location(bots, zone):
    heap = [(0, zone)]
    heapq.heapify(heap)
    best_zones = []
    max_bot_count = 0

    # Create pool for parallel work
    threads = 4
    pool = mp.Pool(processes=threads)

    while heap:
        bot_count, zone = heapq.heappop(heap)

        # Count is negative because of heapq
        bot_count = -bot_count

        # Skip if this count is worst than what we've already encoutered
        if bot_count < max_bot_count:
            continue

        dim_x, dim_y, dim_z = day23_zone_dimensions(zone)
        min_dim = 2
        if min_dim in (dim_x, dim_y, dim_z):
            if bot_count > max_bot_count:
                max_bot_count = bot_count
            best_zones.append((zone, bot_count))
        else:
            for new_zone in day23_bot_count_in_subzones(bots, zone, pool):
                heapq.heappush(heap, new_zone)

    # End thread pool
    pool.close()
    pool.join()

    max_bot_count = max([z[1] for z in best_zones])
    # Keep only the best zones
    best_zones = [z for z in best_zones if z[1] == max_bot_count]

    locations = day23_get_locations_counts(bots, best_zones)

    max_bot_count = max([l[1] for l in locations])
    # Keep only the best locations
    locations = [l[0] for l in locations if l[1] == max_bot_count]
    return day23_calculate_best_distance(locations)

def day23_1(data):
    #data = read_input(2018, 2301)
    bots = day23_parse_input(data)
    return len(day23_bots_in_range(bots, bots[0]))

def day23_2(data):
    #data = read_input(2018, 2302)
    bots = day23_parse_input(data)
    starting_zone = day23_bounds(bots)
    return day23_best_location(bots, starting_zone)

""" DAY 24 """

class P_24(Enum):
    Units = 0
    Hit_points = 1
    Immunity = 2
    Weakness = 3
    Attack_Power = 4
    Attack_Type = 5
    Initiative = 6
    Id = 7

def day24_parse_group(line, id_):
# pylint: disable=C0301
    # 4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
    units, hit_points, immunity, weakness, attack_power, attack_type, initiative = \
        re.findall(r"(\d+) units each with (\d+) hit points (?:\((?:immune to ((?:(?:\w+)(?:, )?)+)(?:; )?)?(?:weak to ((?:(?:\w+)(?:, )?)+))?\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)", line)[0]
    return (int(units), int(hit_points), immunity.split(", "), weakness.split(", "), int(attack_power), attack_type, int(initiative), id_)
# pylint: enable=C0301

def day24_parse_input(data):
    groups = [[], []]
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
    print("Group {0} would deal defending group {1} {2} damage"
          .format(attack_id, defend_id, damage))

def day24_parse_id(id_):
    parts = id_.split("_")
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
    return (day24_damage(attack_group, defend_group),
            day24_effective_power(defend_group),
            defend_group[P_24.Initiative])

def day24_selection_criteria(group):
    return (day24_effective_power(group), group[P_24.Initiative])

def day24_select_target(group, opposing_army, targeted, include_zero):
    available = [enemy
                 for enemy in opposing_army
                 if enemy[P_24.Units] > 0 and enemy[P_24.Id] not in targeted]
    targets = sorted(available, reverse=True, key=lambda g: day24_target_criteria(group, g))
    if not targets:
        return None
    elif len(targets) > 1 and \
         day24_target_criteria(group, targets[0]) == day24_target_criteria(group, targets[1]):
        # Can't decide
        return None

    if day24_damage(group, targets[0]) == 0 and not include_zero:
        return None

    return targets[0][P_24.Id]

def day24_target_selection_phase(armies):
    targeting_map = {}
    for include_zero in (False, True):
        for current_army in range(2):
            opposing_army = (current_army+1)%2
            army = sorted(armies[current_army], reverse=True, key=day24_selection_criteria)
            for group in army:
                if group[P_24.Units] > 0 and not group[P_24.Id] in targeting_map.keys():
                    target = day24_select_target(group,
                                                 armies[opposing_army],
                                                 targeting_map.values(),
                                                 include_zero=include_zero)
                    if not target is None:
                        targeting_map[group[P_24.Id]] = target
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
                max_units = math.floor(damage/(target_group[P_24.Hit_points]))
                dead_units = min(max_units, target_group[P_24.Units])
                kills += dead_units
                armies[target_army_id][target_group_id] = \
                    (target_group[P_24.Units] - dead_units,
                     target_group[P_24.Hit_points],
                     target_group[P_24.Immunity],
                     target_group[P_24.Weakness],
                     target_group[P_24.Attack_Power],
                     target_group[P_24.Attack_Type],
                     target_group[P_24.Initiative],
                     target_group[P_24.Id])
    return kills == 0

def day24_fight(armies):
    groups_by_initiative = \
        [group[P_24.Id]
         for group in
         sorted([group for army in armies for group in army],
                reverse=True,
                key=lambda g: g[P_24.Initiative])]
    while any([group[P_24.Units] > 0 for group in armies[0]]) and \
          any([group[P_24.Units] > 0 for group in armies[1]]):
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
    boost = 1
    threads = 16
    pool = mp.Pool(processes=threads)
    while True:
        process = range(boost, boost + threads + 1)
        boost = boost + threads + 1

        results = pool.map(functools.partial(day24_test_boost, armies), process)
        success = [result for result in results if result[2] == 0]
        success = sorted(success, key=lambda x: x[0])
        if success:
            remaining = success[0][1]
            break
    pool.close()
    pool.join()
    return remaining

def day24_1(data):
    #data = read_input(2018, 2401)
    armies = day24_parse_input(data)
    armies = day24_fight(armies)
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
        for i, _ in enumerate(constellations):
            constellation = constellations[i]
            belongs = False
            for other in constellation:
                if day25_manhattan(point, other) <= 3:
                    belongs = True
                    break
            if belongs:
                belonging.append(i)

        if not belonging:
            constellations.append(deque([point]))
        else:
            i = 0
            c = constellations[belonging[i]]
            c.append(point)
            i += 1
            while i < len(belonging):
                c.extend(constellations[belonging[i]])
                constellations[belonging[i]].clear()
                i += 1

    return [c for c in constellations if len(c) > 0]

def day25_parse_input(data):
    # -2,-2,-2,2

    points = deque([])
    for line in data:
        point = tuple([int(x) for x in re.findall(r"(-?\d+),(-?\d+),(-?\d+),(-?\d+)", line)[0]])
        points.append(point)

    return points

def day25_1(data):
    #data = read_input(2018, 2504)
    points = day25_parse_input(data)
    return len(day25_constellations(points))

START_DAY = 1
""" MAIN FUNCTION """
def main():
    for day in range(START_DAY, 26):
        execute_day(globals(), 2018, day, 1)
        execute_day(globals(), 2018, day, 2)

if __name__ == "__main__":
    main()
