import re
import string
import sys
import functools
import os
file_dir = os.path.dirname(os.path.realpath(__file__))
import sys
sys.path.insert(0, file_dir + "\\..\\")
from common.utils import execute_day, read_input

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
    from collections import deque
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
    from collections import deque
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
import math
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
    max_total = -9999
    coordinate = (1, 1)
    max_size_total = min_size
    memoization = {}
    for size in range(- max_size-1, min_size-1):
        current_coordinate, current_total = day11_solve_exact_size(memoization, grid, -size)
        if current_total > max_total:
            max_total = current_total
            coordinate = current_coordinate
            max_size_total = -size
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
    return day11_solve_range(grid, 1, 300)

#start_day = 11
""" MAIN FUNCTION """
if __name__ == "__main__":
    for i in range(start_day,26):
        execute_day(globals(), 2018, i, 1)
        execute_day(globals(), 2018, i, 2)