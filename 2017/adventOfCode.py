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
        #keep_going = False
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
    #data = read_input(2017, 2001)
    particles = day20_parse_input(data)
    return day20_closest(particles)

def day20_2(data):
    #data = read_input(2017, 2001)
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
            subpattern = ((nr // (square_size*square_size*size))*size)+ ((nr%(square_size*size))//square_size)
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
    #data = read_input(2017, 2101)
    #iters = 2
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
    #data = read_input(2017, 2101)
    #iters = 2
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


start_day = 21
""" MAIN FUNCTION """
if __name__ == "__main__":
    for i_ in range(start_day, 26):
        execute_day(globals(), 2017, i_, 1)
        execute_day(globals(), 2017, i_, 2)
