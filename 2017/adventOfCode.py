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
from enum import Enum
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

start_day = 1

""" DAY 20 """

class I:
    px = 0
    py = 1
    pz = 2
    vx = 3
    vy = 4
    vz = 5
    ax = 6
    ay = 7
    az = 8

def day20_parse_line(line):
    # p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
    return tuple([int(a) for a in re.findall("p=<(-?\d+),(-?\d+),(-?\d+)>, v=<(-?\d+),(-?\d+),(-?\d+)>, a=<(-?\d+),(-?\d+),(-?\d+)>", line)[0]])

def day20_parse_input(data):
    return [day20_parse_line(line) for line in data]

def day20_update_particle(particle):
    px, py, pz, vx, vy, vz, ax, ay, az = particle
    vx += ax
    vy += ay
    vz += az
    px += vx
    py += vy
    pz += vz
    return (px, py, pz, vx, vy, vz, ax, ay, az)

def day20_closest(particles):
    distances = [abs(particle[I.px]) + abs(particle[I.py]) +
                 abs(particle[I.pz]) for particle in particles]
    keep_going = True
    counter = 0
    prev_closest = 0
    while keep_going:
        particles = [day20_update_particle(particle) for particle in particles]
        old_distances = distances
        distances = [abs(particle[I.px]) + abs(particle[I.py]) +
                     abs(particle[I.pz]) for particle in particles]
        minimum = min(distances)
        keep_going = len([x for x in distances if x == minimum]) != 1
        # keep_going = False
        for i in range(len(particles)):
            if old_distances[i] > distances[i]:
                keep_going = True
                break

        closest = 0
        closest_dist = distances[closest]
        for i in range(len(distances)):
            if distances[i] < closest_dist:
                closest = i
                closest_dist = distances[closest]

        if prev_closest == closest:
            counter += 1

        prev_closest = closest
        keep_going = counter < 500
    return closest

def day20_left(particles):
    alive = [True for _ in range(len(particles))]
    keep_going = True
    counter = 0
    prev_alive_count = len(particles)
    while keep_going:
        particles = [day20_update_particle(particle) for particle in particles]
        collided = []
        for i in range(len(particles)):
            if alive[i]:
                for j in range(len(particles)):
                    particle_j = particles[j]
                    particle_i = particles[i]
                    if i != j and alive[j] and particle_i[I.px] == particle_j[I.px] and particle_i[I.py] == particle_j[I.py] and particle_i[I.pz] == particle_j[I.pz]:
                        collided.append(i)
        for col in collided:
            alive[col] = False

        alive_count = len([True for a in alive if a])
        if prev_alive_count == alive_count:
            counter += 1

        prev_alive_count = alive_count
        keep_going = counter < 50

    return alive_count

def day20_1(data):
    # data = read_input(2017, 2001)
    particles = day20_parse_input(data)
    return day20_closest(particles)

def day20_2(data):
    # data = read_input(2017, 2001)
    particles = day20_parse_input(data)
    return day20_left(particles)


""" DAY 21 """

def day21_rotate(pattern):
    if len(pattern) == 5:  # 2x2 grid
        # 0 1
        # 3 4
        # turns to
        # 3 0
        # 4 1
        return "".join([pattern[3], pattern[0], "/", pattern[4], pattern[1]])
    elif len(pattern) == 11:  # 3x3 grid
        # 0 1 2
        # 4 5 6
        # 8 9 10
        # turns to
        # 8  4 0
        # 9  5 1
        # 10 6 2
        return "".join([pattern[8], pattern[4], pattern[0], "/", pattern[9], pattern[5], pattern[1], "/", pattern[10], pattern[6], pattern[2]])

def day21_flip(pattern):
    if len(pattern) == 5:  # 2x2 grid
        # 0 1
        # 3 4
        # turns to
        # 1 0
        # 4 3
        return "".join([pattern[1], pattern[0], "/", pattern[4], pattern[3]])
    elif len(pattern) == 11:  # 3x3 grid
        # 0 1 2
        # 4 5 6
        # 8 9 10
        # turns to
        # 2 1 0
        # 6 5 4
        # 10 9 8
        return "".join([pattern[2], pattern[1], pattern[0], "/", pattern[6], pattern[5], pattern[4], "/", pattern[10], pattern[9], pattern[8]])

def day21_print_key(key):
    print()
    key = key.split("/")
    for r in key:
        line = ""
        for c in r:
            if c == "#":
                line += WHITE_SQUARE
            else:
                line += " "
        print(line)

def day21_print_board(board):
    for r in board:
        line = ""
        for c in r:
            if c == "#":
                line += WHITE_SQUARE
            else:
                line += " "
        print(line)

def day21_parse_input(data):
    rulebook = {}
    for line in data:
        # ../.. => .##/##./.#.
        # .../.../... => ..##/##../##../#.#.
        parts = line.split(" => ")
        left, right = (parts[0], parts[1].split("/"))

        # day21_print_key(left)
        rulebook[left] = right
    new_rulebook = {}
    for k in rulebook:
        new_rulebook[k] = rulebook[k]
        for _ in range(4):
            flip1 = day21_flip(k)
            rotate1 = day21_rotate(k)
            if flip1 not in new_rulebook:
                new_rulebook[flip1] = new_rulebook[k]
            if rotate1 not in new_rulebook:
                new_rulebook[rotate1] = new_rulebook[k]
            k = rotate1

    return new_rulebook

def day21_split(pattern):
    sub_patterns = []
    if len(pattern) % 2 == 0:
        for r in range(len(pattern) // 2):
            for c in range(len(pattern) // 2):
                sub_patterns.append([
                    [pattern[r * 2][c * 2], pattern[r * 2][c * 2 + 1]],
                    [pattern[r * 2 + 1][c * 2], pattern[r * 2 + 1][c * 2 + 1]]])
    elif len(pattern) % 3 == 0:
        for r in range(len(pattern) // 3):
            for c in range(len(pattern) // 3):
                sub_patterns.append([
                    [pattern[r * 3][c * 3], pattern[r * 3][c * 3 + 1],
                     pattern[r * 3][c * 3 + 2]],
                    [pattern[r * 3 + 1][c * 3], pattern[r * 3 + 1][c * 3 + 1],
                     pattern[r * 3 + 1][c * 3 + 2]],
                    [pattern[r * 3 + 2][c * 3], pattern[r * 3 + 2][c * 3 + 1],
                     pattern[r * 3 + 2][c * 3 + 2]]])

    return sub_patterns

def day21_join(subpatterns):
    size = int(math.sqrt(len(subpatterns)))
    square_size = len(subpatterns[0])
    total_pattern_size = size * square_size
    new_pattern = [["." for _ in range(total_pattern_size)]
                   for _ in range(total_pattern_size)]
    for r in range(total_pattern_size):
        for c in range(total_pattern_size):
            nr = r * total_pattern_size + c
            subpattern = ((nr % (square_size * square_size * size)) %
                          (size * square_size)) // square_size
            subpattern = ((nr // (square_size * square_size * size))
                          * size) + ((nr % (square_size * size)) // square_size)
            p = subpatterns[subpattern]
            cc = (nr % (square_size * size)) % square_size
            rr = (nr % (square_size * square_size * size)
                  ) // (square_size * size)
            new_pattern[r][c] = p[rr][cc]

    return new_pattern

def day21_solve(rules, start, iters):
    new_pattern = start
    for _ in range(iters):
        sub_patterns = day21_split(new_pattern)
        new_sub_patterns = []
        for sub_pattern in sub_patterns:
            key = ""
            for row in sub_pattern:
                for c in row:
                    key += c
                key += "/"
            key = key[:-1]
            if key not in rules:
                day21_print_key(key)
                raise ValueError(key)
            new_sub_patterns.append(rules[key])
        new_pattern = day21_join(new_sub_patterns)
    return new_pattern

def day21_1(data):
    iters = 5
    # data = read_input(2017, 2101)
    # iters = 2
    rules = day21_parse_input(data)
    start = ".#./..#/###"
    start = [[".", "#", "."],
             [".", ".", "#"],
             ["#", "#", "#"]]
    end = day21_solve(rules, start, iters)
    count = 0
    for r in end:
        for c in r:
            if c == "#":
                count += 1
    return count

def day21_2(data):
    iters = 18
    # data = read_input(2017, 2101)
    # iters = 2
    rules = day21_parse_input(data)
    start = ".#./..#/###"
    start = [[".", "#", "."],
             [".", ".", "#"],
             ["#", "#", "#"]]
    end = day21_solve(rules, start, iters)
    count = 0
    for r in end:
        for c in r:
            if c == "#":
                count += 1
    return count


""" Day 22 """

def day22_turn(pos, dr, dc):
    if pos == "#":
        return (dc, -dr)
    elif pos == ".":
        return (-dc, dr)
    elif pos == "W":
        return (dr, dc)
    elif pos == "F":
        return (-dr, -dc)

# If the current node is infected, it turns to its right.
#  Otherwise, it turns to its left. (Turning is done in-place; the current node does not change.)
# If the current node is clean, it becomes infected.
#  Otherwise, it becomes cleaned. (This is done after the node is considered for the purposes of changing direction.)
# The virus carrier moves forward one node in the direction it is facing.

def day22_print(grid, R, C, v_r, v_c):
    print()
    m = ""
    for r in range(R):
        line = ""
        for c in range(C):
            pos_r, pos_c = r - (R // 2), c - (C // 2)
            if (pos_r, pos_c) == (v_r, v_c):
                line += "."
            elif (pos_r, pos_c) in grid:
                line += WHITE_SQUARE
            else:
                line += " "
        m += line + "\n"
    print(m)
    time.sleep(.1)

def day22_1(data):
    # 25x25, starts on 12,12 face up
    R, C = (25, 25)
    print_R, print_C = 25, 25
    iters = 10000

    # data = read_input(2017, 2201)
    # R, C = (3, 3)
    # print_R, print_C = 9, 9
    # iters = 70

    grid = set()
    for r in range(R):
        for c in range(C):
            if data[r][c] == "#":
                # print(data[r][c])
                grid.add((r - (R // 2), c - (C // 2)))
    # print(grid)
    r, c = (0, 0)
    dr, dc = (-1, 0)
    count = 0
    for _ in range(iters):
        # day22_print(grid, print_R, print_C, r, c)
        pos = "#" if (r, c) in grid else "."
        dr, dc = day22_turn(pos, dr, dc)
        if pos == "#":
            grid.remove((r, c))
        else:
            count += 1
            grid.add((r, c))
        r, c = r + dr, c + dc
        # print(r, c, dr, dc)

    return count

def day22_2(data):
    # 25x25, starts on 12,12 face up
    R, C = (25, 25)
    print_R, print_C = 40, 40
    iters = 10000000

    # data = read_input(2017, 2201)
    # R, C = (3, 3)
    # print_R, print_C = 9, 9
    # iters = 10000000

    grid = set()
    weak = set()
    flagged = set()
    for r in range(R):
        for c in range(C):
            if data[r][c] == "#":
                # print(data[r][c])
                grid.add((r - (R // 2), c - (C // 2)))
    # print(grid)
    r, c = (0, 0)
    dr, dc = (-1, 0)
    count = 0
    for _ in range(iters):
        # day22_print(grid, print_R, print_C, r, c)

        # Decide which way to turn based on the current node:
        # If it is clean, it turns left.
        # If it is weakened, it does not turn, and will continue moving in the same direction.
        # If it is infected, it turns right.
        # If it is flagged, it reverses direction, and will go back the way it came.

        # Clean nodes become weakened.
        # Weakened nodes become infected.
        # Infected nodes become flagged.
        # Flagged nodes become clean.

        pos = "#" if (r, c) in grid else "W" if (
            r, c) in weak else "F" if (r, c) in flagged else "."
        dr, dc = day22_turn(pos, dr, dc)
        if pos == "#":
            grid.remove((r, c))
            flagged.add((r, c))
        elif pos == "W":
            count += 1
            weak.remove((r, c))
            grid.add((r, c))
        elif pos == "F":
            flagged.remove((r, c))
        else:
            weak.add((r, c))
        r, c = r + dr, c + dc
        # print(r, c, dr, dc)

    return count


""" DAY 23 """

class Instruction(Enum):
    snd = 0
    set_ = 1
    add = 2
    mul = 3
    mod = 4
    rcv = 5
    jgz = 6
    sub = 7
    jnz = 8

def is_number(n):
    try:
        # Type-casting the string to `float`.
        # If string is not a valid `float`,
        # it'll raise `ValueError` exception
        float(n)
    except ValueError:
        return False
    return True

def process(data):
    comm = data.rstrip().split(" ")
    comm[0] = "set_" if comm[0] == "set" else comm[0]
    op = Instruction[comm[0]]
    arg1 = comm[1]
    arg2 = 0
    if is_number(arg1):
        arg1 = int(arg1)
    if len(comm) == 3:
        arg2 = comm[2]
        if is_number(arg2):
            arg2 = int(arg2)
    return (op, arg1, arg2)

def day23_process(regMap, inst):
    comm = inst[0]
    arg1 = inst[1]
    arg2 = inst[2]
    jump = 1
    if not is_number(arg2):
        arg2 = regMap[arg2]

    if comm == Instruction.set_:
        regMap[arg1] = arg2
    elif comm == Instruction.mul:
        regMap[arg1] = regMap[arg1] * arg2
    elif comm == Instruction.jnz:
        val = regMap[arg1] if not is_number(arg1) else arg1
        if val != 0:
            jump = arg2
    elif comm == Instruction.sub:
        regMap[arg1] -= arg2
    else:
        assert False
    return jump

def day23_1(input_):
    input_ = [process(comm) for comm in input_]
    registerMap = {}
    for c in "abcdefgh":
        registerMap[c] = 0

    pc = 0
    count = 0
    while True:
        inst = input_[pc]
        if inst[0] == Instruction.mul:
            count += 1

        pc += day23_process(registerMap, inst)

        if not (0 <= pc < len(input_)):
            break

    return count

# 01: b = 79
# 02: c = b
# 03: if a != 0 jump to 5
# 04: jump to 9
# 05: b *= 100
# 06: b += 100000
# 07: c = b
# 08: c = 17000
# 09: f = 1
# 10: d = 2
# 11: e = 2
# 12: g = d
# 13: g *= e
# 14: g -= b
# 15: if g != 0 jump to 17
# 16: f = 0
# 17: e += 1
# 18: g = e
# 19: g -= b
# 20: if g != 0 jump to 12
# 21: d += 1
# 22: g = d
# 23: g -= b
# 24: if g != 0 jump to 11
# 25: if f != 0 jump to 27
# 26: h += 1
# 27: g = b
# 28: g -= c
# 29: if g != 0 jump to 31
# 30: HALT
# 31: g += 17
# 32: jump to 9

def day23_2(_):
    start = 79 * 100 + 100000
    h = 0
    for b in range(start, start + 17000 + 1, 17):
        for d in range(2, b):
            if b % d == 0:
                h += 1
                break
    return h


""" DAY 24 """

def day24_configs(data):
    ports = [tuple([int(p) for p in line.split("/")]) for line in data]
    res = []
    q = [(0, [], ports)]
    while q:
        pins, used, rest = q.pop()
        match = False
        for l, r in rest:
            if l == pins:
                match = True
                q.append(
                    (r, used + [(l, r)], [p for p in rest if p != (l, r)]))
            elif r == pins:
                match = True
                q.append(
                    (l, used + [(l, r)], [p for p in rest if p != (l, r)]))
        if not match:
            res.append(used)
            continue
    return res

def day24_strongest(res):
    m = 0
    for config in res:
        curr = 0
        for l, r in config:
            curr += l + r
        m = max(m, curr)
    return m

def day24_1(data):
    # data = read_input(2017, 2401)
    res = day24_configs(data)

    return day24_strongest(res)

def day24_2(data):
    # data = read_input(2017, 2401)
    res = day24_configs(data)

    m_size = max([len(c) for c in res])

    return day24_strongest([c for c in res if len(c) == m_size])


""" DAY 25 """

def day25_1(data):
    # data = read_input(2017, 2501)
    start_state = data[0].split("Begin in state ")[1].split(".")[0]
    steps = int(data[1].split("Perform a diagnostic checksum after ")[
        1].split(" steps.")[0])
    states = {}
    i = 3
    while i < len(data):
        # In state A:
        # If the current value is 0:
        #    - Write the value 1.
        #    - Move one slot to the right.
        #    - Continue with state B.
        # If the current value is 1:
        #    - Write the value 0.
        #    - Move one slot to the left.
        #    - Continue with state B.
        # print(data[i])
        state = data[i].split("In state ")[1].split(":")[0]
        on_0_write = int(
            data[i + 2].split("Write the value ")[1].split(".")[0])
        on_0_move = data[i + 3].split("Move one slot to the ")[1].split(".")[0]
        on_0_move = -1 if on_0_move == "left" else 1
        on_0_state = data[i + 4].split("Continue with state ")[1].split(".")[0]

        on_1_write = int(
            data[i + 6].split("Write the value ")[1].split(".")[0])
        on_1_move = data[i + 7].split("Move one slot to the ")[1].split(".")[0]
        on_1_move = -1 if on_1_move == "left" else 1
        on_1_state = data[i + 8].split("Continue with state ")[1].split(".")[0]

        states[state] = ((on_0_write, on_0_move, on_0_state),
                         (on_1_write, on_1_move, on_1_state))
        i += 10
    mem = {}
    curr = 0
    curr_state = start_state
    for i in range(steps):
        if curr not in mem:
            mem[curr] = 0
        on_write, on_move, on_state = states[curr_state][mem[curr]]
        mem[curr] = on_write
        curr += on_move
        curr_state = on_state
    return sum(mem.values())


start_day = 20

""" MAIN FUNCTION """
if __name__ == "__main__":
    for i_ in range(start_day, 26):
        execute_day(globals(), 2017, i_, 1)
        execute_day(globals(), 2017, i_, 2)
