# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
import functools
import math
import os
from os.path import join
import sys
import time
from copy import deepcopy
from collections import defaultdict
from heapq import heappop, heappush

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import read_input, main, clear  # NOQA: E402
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

def day1_parse(data):
    return [int(x) for x in data]
    # return data

def day1_1(data):
    # data = read_input(2021, 101)
    data = day1_parse(data)
    greater = 0
    for i in range(len(data)):
        if i == 0:
            continue
        if data[i] > data[i - 1]:
            greater += 1
    return greater


def day1_2(data):
    # data = read_input(2021, 101)
    data = day1_parse(data)
    greater = 0
    for i in range(len(data)):
        if i in (0, 1, 2):
            continue
        prev = data[i - 3] + data[i - 2] + data[i - 1]
        curr = data[i - 2] + data[i - 1] + data[i]
        if curr > prev:
            greater += 1
    return greater


""" DAY 2 """

def day2_parse(data):
    return [s.split() for s in data]

def day2_1(data):
    # data = read_input(2021, 201)
    data = day2_parse(data)
    pos = 0
    depth = 0
    for comm, val in data:
        if comm == "forward":
            pos += int(val)
        elif comm == "up":
            depth -= int(val)
        elif comm == "down":
            depth += int(val)
    return depth * pos

def day2_2(data):
    # data = read_input(2021, 201)
    data = day2_parse(data)
    pos = 0
    depth = 0
    aim = 0
    for comm, val in data:
        if comm == "forward":
            pos += int(val)
            depth += aim * int(val)
        elif comm == "up":
            aim -= int(val)
        elif comm == "down":
            aim += int(val)
    return depth * pos


""" DAY 3 """

def day3_parse(data):
    return data

def day3_freq(data, bit):
    n_0 = 0
    n_1 = 0
    for j in range(len(data)):
        curr = data[j][bit]
        if curr == "0":
            n_0 += 1
        else:
            n_1 += 1
    if n_0 > n_1:
        return ("0", "1")
    else:
        return ("1", "0")


def day3_1(data):
    # data = read_input(2021, 301)
    data = day3_parse(data)
    n_bits = len(data[0])
    gamma = ""
    epsilon = ""
    for i in range(n_bits):
        most, least = day3_freq(data, i)
        gamma += most
        epsilon += least

    gamma = int(gamma, 2)
    epsilon = int(epsilon, 2)
    return gamma * epsilon


def day3_2(data):
    # data = read_input(2021, 301)
    data = day3_parse(data)
    n_bits = len(data[0])
    data_copy = ["" + y for y in data]
    for i in range(n_bits):
        most, _ = day3_freq(data, i)
        data = [v for v in data if v[i] == most]
        if len(data) == 1:
            break

    oxygen = int(data[0], 2)
    data = data_copy

    for i in range(n_bits):
        _, least = day3_freq(data, i)
        data = [v for v in data if v[i] == least]
        if len(data) == 1:
            break

    co2 = int(data[0], 2)
    return co2 * oxygen


""" DAY 4 """

def day4_parse(data):
    nums = [int(x) for x in data[0].split(",")]

    boards = []
    size = 0
    for line in data[1:]:
        if line == "":
            boards.append([])
            size += 1
            continue
        boards[-1].append([])
        for n in line.split():
            boards[-1][-1].append([int(n), False])

    return nums, boards

def day4_score(board):
    total = 0
    for r in range(len(board)):
        for c in range(len(board[r])):
            if not board[r][c][1]:
                total += board[r][c][0]
    return total

def day4_won(board):
    for r in range(len(board)):
        if all([board[r][c][1] for c in range(len(board[r]))]):
            return True
    for c in range(len(board[0])):
        if all([board[r][c][1] for r in range(len(board))]):
            return True
    return False

def day4_1(data):
    # data = read_input(YEAR, DAY * 100 + 1)
    nums, boards = day4_parse(data)
    for n in nums:
        for b in range(len(boards)):
            board = boards[b]
            for l in range(len(board)):
                line = board[l]
                for p in range(len(line)):
                    c = line[p][0]
                    if c == n:
                        boards[b][l][p][1] = True
        for b in range(len(boards)):
            board = boards[b]
            if day4_won(board):
                return n * day4_score(board)
    return None

def day4_2(data):
    # data = read_input(YEAR, DAY * 100 + 1)
    nums, boards = day4_parse(data)
    won = [False for _ in range(len(boards))]
    for n in nums:
        for b in range(len(boards)):
            board = boards[b]
            for l in range(len(board)):
                line = board[l]
                for p in range(len(line)):
                    c = line[p][0]
                    if c == n:
                        boards[b][l][p][1] = True
        for b in range(len(boards)):
            board = boards[b]
            if day4_won(board):
                won[b] = True
                if sum(won) == len(boards):
                    return n * day4_score(board)
    return None


""" DAY 5 """

def day5_parse(data):
    m = []
    max_x = 0
    max_y = 0
    for line in data:
        parts = line.split(" -> ")
        fst = parts[0].split(",")
        snd = parts[1].split(",")
        max_x = max(max_x, int(fst[0]))
        max_x = max(max_x, int(snd[0]))
        max_y = max(max_y, int(fst[1]))
        max_y = max(max_y, int(snd[1]))
        m.append((int(fst[0]), int(fst[1]), int(snd[0]), int(snd[1])))
    return max_x, max_y, m

def day5_between(x, x1, x2):
    return x1 <= x <= x2 or x2 <= x <= x1

def day5_1(data):
    # data = read_input(YEAR, DAY * 100 + 1)
    max_x, max_y, m = day5_parse(data)
    counts = defaultdict(lambda: 0)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            for x1, y1, x2, y2 in m:
                if x1 == x2 or y1 == y2:
                    if (x == x1 and day5_between(y, y1, y2)) \
                            or (y == y1 and day5_between(x, x1, x2)):
                        counts[(x, y)] += 1

    count = 0
    for k in counts:
        if counts[k] >= 2:
            count += 1
    return count


def day5_2(data):
    # data = read_input(YEAR, DAY * 100 + 1)
    _, _, m = day5_parse(data)
    counts = defaultdict(lambda: 0)
    for x1, y1, x2, y2 in m:
        if x1 == x2 or y1 == y2 or (abs(x1 - x2) == abs(y1 - y2)):
            dx, dy = 0, 0
            if x2 - x1 != 0:
                dx = (x2 - x1) / abs(x2 - x1)
            if y2 - y1 != 0:
                dy = (y2 - y1) / abs(y2 - y1)

            curr_x, curr_y = x1, y1
            while curr_x != x2 or curr_y != y2:
                counts[(curr_x, curr_y)] += 1
                curr_x, curr_y = curr_x + dx, curr_y + dy
            # Count final position (x2,y2) as well
            counts[(curr_x, curr_y)] += 1

    count = 0
    for k in counts:
        if counts[k] >= 2:
            count += 1
    return count


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2021)
