# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
from typing import Callable, Iterator, Union, Optional, List
import functools
import math
import os
from os.path import join
import sys
import time
from copy import deepcopy
import ast
from collections import Counter, defaultdict
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
    _, _, m = day5_parse(data)
    counts = defaultdict(lambda: 0)
    # for y in range(max_y + 1):
    #     for x in range(max_x + 1):
    #         for x1, y1, x2, y2 in m:
    #             if x1 == x2 or y1 == y2:
    #                 if (x == x1 and day5_between(y, y1, y2)) \
    #                         or (y == y1 and day5_between(x, x1, x2)):
    #                     counts[(x, y)] += 1

    for x1, y1, x2, y2 in m:
        if x1 == x2 or y1 == y2:
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


""" DAY 6 """

def day6_parse(data):
    return [int(x) for x in data[0].split(",")]

def day6_1(data):
    # data = read_input(YEAR, DAY * 100 + 1)
    data = day6_parse(data)

    for _ in range(80):
        new_fish = []
        for i, n in enumerate(data):
            if n == 0:
                data[i] = 6
                new_fish.append(8)
            else:
                data[i] -= 1
        for n in new_fish:
            data.append((n))

    return len(data)

def day6_2(data):
    # data = read_input(YEAR, DAY * 100 + 1)
    data = day6_parse(data)
    fish = defaultdict(lambda: 0)
    for n in data:
        fish[n] += 1
    for _ in range(256):
        new_fish_data = defaultdict(lambda: 0)
        for k in fish.keys():
            if k == 0:
                new_fish_data[6] += fish[k]
                new_fish_data[8] += fish[k]
            else:
                new_fish_data[k - 1] += fish[k]
        fish = new_fish_data

    return sum(new_fish_data.values())


""" DAY 7 """

def day7_parse(data):
    return [int(x) for x in data[0].split(",")]

def day7_calculate(data, p1):
    min_pos, max_pos = min(data), max(data)
    max_fuel = None
    for i in range(min_pos, max_pos + 1):
        counter = 0
        for p in data:
            # for j in range(1, abs(p - i) + 1):
            #     counter += j
            #     if max_fuel and counter > max_fuel:
            #         break
            dist = abs(p - i)
            counter += dist if p1 else (dist * (dist + 1)) / 2
            if max_fuel and counter > max_fuel:
                break

        max_fuel = counter if not max_fuel else min(max_fuel, counter)
    return int(max_fuel)


def day7_1(data):
    # data = read_input(YEAR, DAY * 100 + 1)
    data = day7_parse(data)
    return day7_calculate(data, True)

def day7_2(data):
    # data = read_input(YEAR, DAY * 100 + 1)
    data = day7_parse(data)
    return day7_calculate(data, False)


""" DAY 8 """

def day8_parse(data):
    d = []
    for l in data:
        parts = l.split(" | ")
        d.append((parts[0].split(), parts[1].split()))
    return d

def day8_1(data):
    data = day8_parse(data)
    count = 0
    for _, value in data:
        for x in value:
            if len(x) in [2, 4, 3, 7]:
                count += 1
    return count

def day8_fixed_point(segments):
    # Go through all alternatives,
    # if segment X has alternatives 1, 2 and 3
    # and segment Y has alternatives 1 and 2
    # we can conclude that X is 3
    modified_segments = False
    new_information = True
    while new_information:
        new_information = False
        for s, ps in segments.items():
            if len(ps) == 1:
                continue

            for s2, ps2 in segments.items():
                if s2 != s:
                    if len(ps) > len(ps2) and ps2.issubset(ps):
                        segments[s] = ps.difference(ps2)
                        new_information = True
                        modified_segments = True
    return segments, modified_segments

def day8_calculate_outputs(segments, outputs):
    result = {
        "abcefg": 0,
        "cf": 1,
        "acdeg": 2,
        "acdfg": 3,
        "bcdf": 4,
        "abdfg": 5,
        "abdefg": 6,
        "acf": 7,
        "abcdefg": 8,
        "abcdfg": 9
    }
    mapping = {}
    for adg, v in segments.items():
        mapping[v.pop()] = adg
    decoded_out = ""
    for d in outputs:
        decoded_str = ""
        for c in d:
            decoded_str += mapping[c]

        decoded_str = "".join(sorted(decoded_str))
        decoded_digit = str(result[decoded_str])
        decoded_out += decoded_digit
    return int(decoded_out)

def day8_2(data):
    data = day8_parse(data)
    total = 0
    #   0:      1:      2:      3:      4:
    #  aaaa    ....    aaaa    aaaa    ....
    # b    c  .    c  .    c  .    c  b    c
    # b    c  .    c  .    c  .    c  b    c
    #  ....    ....    dddd    dddd    dddd
    # e    f  .    f  e    .  .    f  .    f
    # e    f  .    f  e    .  .    f  .    f
    #  gggg    ....    gggg    gggg    ....

    #   5:      6:      7:      8:      9:
    #  aaaa    aaaa    aaaa    aaaa    aaaa
    # b    .  b    .  .    c  b    c  b    c
    # b    .  b    .  .    c  b    c  b    c
    #  dddd    dddd    ....    dddd    dddd
    # .    f  e    f  .    f  e    f  .    f
    # .    f  e    f  .    f  e    f  .    f
    #  gggg    gggg    ....    gggg    gggg

    for signal, outputs in data:

        segments = {
            "a": set(),
            "b": set(),
            "c": set(),
            "d": set(),
            "e": set(),
            "f": set(),
            "g": set(),
        }
        for x in signal:
            # 1 is made up of only C and F
            if len(x) == 2:
                for c in x:
                    segments["c"].add(c)
                    segments["f"].add(c)

            # 4 is made up of B, D, C and F
            # Since C and F are set from previous
            # iteration, add alternatives for B and D
            elif len(x) == 4:
                for c in x:
                    segments["b"].add(c)
                    segments["d"].add(c)
                    # segments["c"].add(c)
                    # segments["f"].add(c)

            # 7 is made up of A, C and F
            # Since C and F are set from previous
            # iteration, add alternative for A
            elif len(x) == 3:
                for c in x:
                    segments["a"].add(c)
                    # segments["c"].add(c)
                    # segments["f"].add(c)

        # 2, 3 and 5 share A, D and G
        # So, save the alternatives that
        # appear in all of them
        all_5 = [x for x in signal if len(x) == 5]
        counts = Counter()
        for x in all_5:
            for c in x:
                counts[c] += 1
        adg = ""
        for c, count in counts.items():
            if count == len(all_5):
                adg += c
        assert len(adg) == 3

        # All digits except 1, 4 and 7 share G
        # So, save the alternatives that
        # appear in all of them in G
        all_g = [x for x in signal if len(x) not in [2, 4, 3]]
        counts3 = Counter()
        for x in all_g:
            for c in x:
                counts3[c] += 1
        for c, count in counts3.items():
            if count == len(all_g):
                segments["g"].add(c)

        # 0, 6 and 9 share A, B, F and G
        # So, save the alternatives that
        # appear in all of them
        all_6 = [x for x in signal if len(x) == 6]
        counts2 = Counter()
        for x in all_6:
            for c in x:
                counts2[c] += 1
        abfg = ""
        for c, count in counts2.items():
            if count == len(all_6):
                abfg += c
        assert len(abfg) == 4

        # When we reach this point, all
        # segments except E have an alternative
        # So save the remaining ones
        used = []
        for l in segments.values():
            for c in l:
                used.append(c)
        all_s = "abcdefg"
        for c in all_s:
            if not c in used:
                segments["e"] = set([c])

        adg_bak = adg
        abfg_bak = abfg
        new_information = True
        while new_information:
            new_information = False

            # Simplify alternatives by eliminating redundant ones
            segments, new_information = day8_fixed_point(segments)

            adg = adg_bak
            abfg = abfg_bak

            # Use the relation between A, D and G
            # to narrow the results
            pattern = "adg"
            if len(segments["a"]) == 1:
                pattern = pattern.replace("a", "")
                adg = adg.replace(list(segments["a"])[0], "")
            if len(segments["d"]) == 1:
                pattern = pattern.replace("d", "")
                adg = adg.replace(list(segments["d"])[0], "")
            if len(segments["g"]) == 1:
                pattern = pattern.replace("g", "")
                adg = adg.replace(list(segments["g"])[0], "")
            if len(adg) == 1:
                segments[pattern] = set([adg])
                new_information = True

            # Use the relation between A, B, F and G
            # to narrow the results
            pattern = "abfg"
            if len(segments["a"]) == 1:
                pattern = pattern.replace("a", "")
                abfg = abfg.replace(list(segments["a"])[0], "")
            if len(segments["b"]) == 1:
                pattern = pattern.replace("b", "")
                abfg = abfg.replace(list(segments["b"])[0], "")
            if len(segments["f"]) == 1:
                pattern = pattern.replace("f", "")
                abfg = abfg.replace(list(segments["f"])[0], "")
            if len(segments["g"]) == 1:
                pattern = pattern.replace("g", "")
                abfg = abfg.replace(list(segments["g"])[0], "")
            if len(abfg) == 1:
                segments[pattern] = set([abfg])
                new_information = True

        total += day8_calculate_outputs(segments, outputs)

    return total


""" DAY 9 """

def day9_parse(data):
    return [[int(x) for x in line] for line in data]

def day9_lowest(data):
    D = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    R = len(data)
    C = len(data[0])
    lowest_pos = []
    for r in range(R):
        for c in range(C):
            curr = data[r][c]
            lowest = True
            for dr, dc in D:
                rr, cc = r + dr, c + dc
                if 0 <= rr < R and 0 <= cc < C:
                    curr2 = data[rr][cc]
                    if curr >= curr2:
                        lowest = False
            if lowest:
                lowest_pos.append((r, c))
    return lowest_pos

def day9_1(data):
    data = day9_parse(data)

    total = 0
    for r, c in day9_lowest(data):
        total += data[r][c] + 1
    return total

def day9_move_up(data, r, c, R, C):
    if data[r][c] == 9:
        return set()

    curr = data[r][c]
    res = set([(r, c)])
    D = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for dr, dc in D:
        rr, cc = r + dr, c + dc
        if 0 <= rr < R and 0 <= cc < C:
            if curr < data[rr][cc]:
                res = res.union(day9_move_up(data, rr, cc, R, C))
    return res

def day9_2(data):
    data = day9_parse(data)

    R = len(data)
    C = len(data[0])
    sizes = []

    sizes = []
    lowest = day9_lowest(data)
    for r, c in lowest:
        visited = set()
        visited = day9_move_up(data, r, c, R, C)
        sizes.append(len(visited))
    total = 1
    sizes = sorted(sizes)[-3:len(sizes)]
    for x in sizes:
        total *= x
    return total


""" DAY 10 """

def day10_parse(data):
    return data

def day10_separate(data):
    corrupted = []
    rest = []
    mapping = {
        ")": "(",
        "]": "[",
        "}": "{",
        ">": "<"
    }
    opening_chars = mapping.values()
    for l in data:
        stack = []
        is_corrupted = False
        for c in l:
            if c in opening_chars:
                stack.append(c)
            else:
                last = stack[-1]
                stack = stack[0:-1]
                # if c == ")" and last != "(" or \
                #         c == "]" and last != "[" or \
                #         c == "}" and last != "{" or \
                #         c == ">" and last != "<":
                assert c in mapping
                if mapping[c] != last:
                    is_corrupted = True
                    corrupted.append((l, c))
                    break

        if stack and not is_corrupted:
            rest.append((l, stack))
    return corrupted, rest

def day10_1(data):
    data = day10_parse(data)

    points = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137
    }
    total = 0
    corrupted, _ = day10_separate(data)
    for _, c in corrupted:
        total += points[c]

    return total

def day10_2(data):
    data = day10_parse(data)
    _, rest = day10_separate(data)
    points = {
        "(": 1,
        "[": 2,
        "{": 3,
        "<": 4
    }
    scores = []
    for _, stack in rest:
        total = 0
        for c in reversed(stack):
            total *= 5
            total += points[c]
        scores.append(total)
        scores.sort()
    return scores[len(scores) // 2]


""" DAY 11 """

def day11_parse(data):
    return [[int(x) for x in line] for line in data]

def day11_solve(data):
    flashes_by_step = {}
    data = day11_parse(data)
    R = len(data)
    C = len(data[0])

    for step in range(1, 500):

        # clear()
        # print(step)
        # for r in range(R):
        #     row = ""
        #     for c in range(C):
        #         if data[r][c] == 0:
        #             row += WHITE_SQUARE
        #         else:
        #             row += " "
        #     print(row)
        # print()
        # time.sleep(.1)

        flashes = 0
        q = set()
        for r in range(R):
            for c in range(C):
                data[r][c] += 1
                if data[r][c] > 9:
                    q.add((r, c))
        flashed = set()
        while q:
            r, c = q.pop()
            data[r][c] = 0
            flashed.add((r, c))
            flashes += 1
            if flashes == R * C:
                return flashes_by_step, step
            D = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                 (0, 1), (1, -1), (1, 0), (1, 1)]
            for dr, dc in D:
                rr, cc = r + dr, c + dc
                if 0 <= rr < R and 0 <= cc < C:
                    if (rr, cc) not in flashed:
                        data[rr][cc] += 1
                        if data[rr][cc] > 9:
                            q.add((rr, cc))
        flashes_by_step[step] = flashes

    assert False

def day11_1(data):
    data = day11_parse(data)

    flashes_by_step, _ = day11_solve(data)
    return sum([v for k, v in flashes_by_step.items() if k <= 100])

def day11_2(data):
    data = day11_parse(data)

    _, step = day11_solve(data)
    return step


""" DAY 12 """

def day12_parse(data):
    graph = defaultdict(list)
    for line in data:
        start, finish = line.split("-")
        graph[start].append(finish)
        graph[finish].append(start)
    return graph

def day12_1(data):
    data = day12_parse(data)

    q = [("start", ["start"], set())]
    paths = []
    while q:
        curr, path, visited = q.pop()
        for next_cave in data[curr]:
            if next_cave == "start" or \
                    next_cave[0].islower() and next_cave in visited:
                continue
            if next_cave == "end":
                paths.append(path)
            else:
                q.append((next_cave,
                          path + [next_cave],
                          set(list(visited) + [next_cave])))
    return len(paths)

def day12_2(data):
    data = day12_parse(data)

    q = [("start", ["start"], set(), False)]
    paths = []
    while q:
        curr, path, visited, small_twice = q.pop()
        for next_cave in data[curr]:
            if next_cave == "start" or \
                    (next_cave[0].islower() and next_cave in visited
                     and small_twice):
                continue
            if next_cave == "end":
                paths.append(path)
            else:
                if next_cave[0].islower():
                    q.append(
                        (next_cave,
                         path + [next_cave],
                         set(list(visited) + [next_cave]),
                         small_twice or (next_cave in visited)))
                else:
                    q.append(
                        (next_cave,
                         path + [next_cave],
                         set(list(visited) + [next_cave]),
                         small_twice))
    return len(paths)


""" DAY 13 """

def day13_parse(data):
    points = set()
    i = 0
    for line in data:
        if line:
            x, y = line.split(",")
            points.add((int(x), int(y)))
            i += 1
        else:
            break
    folds = []
    for line in data[i + 1:]:
        first, second = line.split("=")
        along = first.split("fold along ")[1]
        folds.append((along, int(second)))

    return points, folds

def day13_fold(points, fold):
    point = fold[1]
    new_points = set()
    for x, y in points:
        if fold[0] == "x":
            assert x != point, x
            if x > point:
                # new_points.add((C - c - 1, r))
                new_points.add((point - (x - point), y))
            else:
                new_points.add((x, y))
        if fold[0] == "y":
            assert y != point, y
            if y > point:
                # new_points.add((c, R - r - 1))
                new_points.add((x, point - (y - point)))
            else:
                new_points.add((x, y))
    return new_points

def day13_print(points):
    C = max([x for x, _ in points]) + 1
    R = max([y for _, y in points]) + 1
    for r in range(R):
        row = ""
        for c in range(C):
            if (c, r) in points:
                row += WHITE_SQUARE
            else:
                row += " "
        print(row)

def day13_1(data):
    points, folds = day13_parse(data)

    new_points = day13_fold(points, folds[0])

    return len(new_points)

def day13_2(data):
    points, folds = day13_parse(data)
    for fold in folds:
        points = day13_fold(points, fold)

    day13_print(points)
    return None


""" DAY 14 """

def day14_parse(data):
    m = {}
    temp = data[0]

    for line in data[2:]:
        left, right = line.split(" -> ")
        m[left] = right
    return temp, m

def day14_1(data):
    temp, m = day14_parse(data)

    s = temp
    for _ in range(10):
        n = s[0]
        for j in range(len(s) - 1):
            curr = s[j:j + 2]
            n += m[curr]
            n += curr[1]
        s = n
    vals = Counter(s)
    return max(vals.values()) - min(vals.values())

# Try 1
def day14_divide(curr, DP, m):
    if len(curr) == 2:
        return curr[0] + m[curr] + curr[1]

    if curr in DP:
        return DP[curr]

    if len(curr) % 2 == 0:

        mid = len(curr) // 2
        left = curr[:mid]
        right = curr[mid:]
        mid_c = left[-1] + right[0]
        assert mid_c in m, mid_c
        DP[curr] = day14_divide(left, DP, m) + m[mid_c] + \
            day14_divide(right, DP, m)
        return DP[curr]
    else:

        rest = curr[-2:]
        n_curr = curr[:-1]
        DP[curr] = day14_divide(n_curr, DP, m) + m[rest] + rest[-1]
        return DP[curr]

def day14_2(data):
    temp, m = day14_parse(data)
    freq = Counter()
    for j in range(len(temp) - 1):
        curr = temp[j:j + 2]
        freq[curr] += 1

    for _ in range(40):
        new_freq = Counter()
        for pair in freq:
            n1 = pair[0] + m[pair]
            n2 = m[pair] + pair[1]
            new_freq[n1] += freq[pair]
            new_freq[n2] += freq[pair]
        freq = new_freq

    final_c = Counter()
    for k in freq:
        final_c[k[1]] += freq[k]
    # Counter({'N': 2, 'C': 1, 'B': 1})
    # Counter({'N': 2, 'C': 2, 'B': 2, 'H': 1})
    # Counter({'B': 6, 'C': 4, 'N': 2, 'H': 1})
    # Counter({'B': 11, 'N': 5, 'C': 5, 'H': 4})
    # Counter({'B': 23, 'N': 11, 'C': 10, 'H': 5})
    final_c[temp[0]] += 1
    return max(final_c.values()) - min(final_c.values())


""" DAY 15 """

def day15_parse(data):
    G = []
    for line in data:
        G.append([int(x) for x in line])
    return G

def day15_flood(G):
    R = len(G)
    C = len(G[0])
    q = [(G[R - 1][C - 1], R - 1, C - 1)]
    risks = defaultdict(lambda: -1)
    risks[(R - 1, C - 1)] = G[R - 1][C - 1]
    while q:
        risk, r, c = heappop(q)
        if r == 0 and c == 0:
            return risk

        D = [(0, -1), (-1, 0), (1, 0), (0, 1)]
        for dr, dc in D:
            rr = r + dr
            cc = c + dc
            if 0 <= rr < R and 0 <= cc < C:
                curr = G[rr][cc] + risks[(r, c)]
                if risks[(rr, cc)] == -1 or curr < risks[(rr, cc)]:
                    risks[(rr, cc)] = curr
                    heappush(q, (curr, rr, cc))
    assert False

def day15_1(data):
    G = day15_parse(data)
    # Remove cost of initial position
    return day15_flood(G) - G[0][0]

def day15_2(data):
    data = day15_parse(data)
    G = day15_parse(data)
    R = len(G)
    C = len(G[0])

    new_G = []
    for r in range(R * 5):
        row = []
        for c in range(C * 5):
            pos = G[r % R][c % C]
            pos += r // R + c // C

            # If we wanted between 1 and 3:
            # 4 -> 3 -> 3%3 = 0 -> 1
            # N -> N-1 -> N-1 % MAX -> +1
            pos = ((pos - 1) % 9) + 1
            row.append(pos)
        new_G.append(row)

    # Remove cost of initial position
    return day15_flood(new_G) - new_G[0][0]


""" DAY 16 """

def day16_parse(data):
    return ("{:0" + str(len(data[0] * 4)) + "b}").format(int(data[0], 16))

def day16_decode(pack):
    if pack == "":
        return "", [], 0
    ver = int(pack[0:3], 2)
    id_ = int(pack[3:6], 2)
    rest = pack[6:]
    total_size = 6
    number = ""
    packs = []
    if id_ == 4:
        go = True
        i = 0
        while go:
            if rest[0] == "1":
                number += rest[1:1 + 4]
                rest = rest[1 + 4:]
            else:
                number += rest[1:1 + 4]
                rest = rest[1 + 4:]
                go = False
            i += 5
            total_size += 5
        return rest, [(ver, id_, [int(number, 2)])], total_size
    else:
        if rest[0] == "0":
            size = int(rest[1:16], 2)
            rest = rest[16:]
            total_size += 16
            go = True
            sub_size = 0
            while go:
                rest, inner_packs, inner_size = day16_decode(rest)
                total_size += inner_size
                sub_size += inner_size
                packs += inner_packs
                if sub_size == size:
                    go = False
                assert sub_size <= size, (size, sub_size)
        else:
            count = int(rest[1:12], 2)
            rest = rest[12:]
            total_size += 12
            for _ in range(count):
                rest, inner_packs, size = day16_decode(rest)
                total_size += size
                packs += inner_packs
    return rest, [(ver, id_, packs)], total_size

def day16_sum(packs):
    total = 0
    for p in packs:
        ver, id_, inner_packs = p
        if id_ == 4:
            total += ver
        else:
            total += ver + day16_sum(inner_packs)
    return total

def day16_process(packs):
    total = 0
    _, id_, inner_packs = packs
    if id_ == 0:
        # print("(", end="")
        for _, pack in enumerate(inner_packs):
            total += day16_process(pack)
        #     if i != len(inner_packs) - 1:
        #         print("+", end="")
        # print(")", end="")
        return total
    elif id_ == 1:
        total = 1
        # print("(", end="")
        for _, pack in enumerate(inner_packs):
            total *= day16_process(pack)
        #     if i != len(inner_packs) - 1:
        #         print("*", end="")
        # print(")", end="")
        return total
    elif id_ == 2:
        # print("min(", end="")
        total = min([day16_process(pack) for pack in inner_packs])
        # print(")", end="")
        return total
    elif id_ == 3:
        # print("max(", end="")
        total = max([day16_process(pack) for pack in inner_packs])
        # print(")", end="")
        return total
    elif id_ == 4:
        # print(f" {inner_packs[0]} ", end="")
        return inner_packs[0]
    elif id_ == 5:
        # print("(", end="")
        left = day16_process(
            inner_packs[0])
        # print(">", end="")
        right = day16_process(inner_packs[1])
        total = 1 if left > right else 0
        # print(")", end="")
        return total
    elif id_ == 6:
        # print("(", end="")
        left = day16_process(
            inner_packs[0])
        # print("<", end="")
        right = day16_process(inner_packs[1])
        total = 1 if left < right else 0
        # print(")", end="")
        return total
    elif id_ == 7:
        # print("(", end="")
        left = day16_process(
            inner_packs[0])
        # print("==", end="")
        right = day16_process(inner_packs[1])
        total = 1 if left == right else 0
        # print(")", end="")
        return total
    else:
        assert False

def day16_1(data):
    data = day16_parse(data)
    _, packs, _ = day16_decode(data)
    return day16_sum(packs)


def day16_2(data):
    data = day16_parse(data)
    _, packs, _ = day16_decode(data)
    return day16_process(packs[0])


""" DAY 17 """

def day17_parse(data):
    pos = data[0].split("target area: ")[1]
    x, y = pos.split(", ")
    min_x, max_x = x.split("..")
    min_x = int(min_x.replace("x=", ""))
    max_x = int(max_x)
    min_y, max_y = y.split("..")
    min_y = int(min_y.replace("y=", ""))
    max_y = int(max_y)

    return min_x, max_x, min_y, max_y

def day17_all_vels(min_x, max_x, min_y, max_y):
    ans = []
    for dx in range(1, max_x + 1):
        dy = min_y - 1
        while dy < 200:  # Magic 200, can this be calculated?
            dy += 1
            curr_x, curr_y = 0, 0
            i_dx = dx
            i_dy = dy
            top_y = 0
            while curr_y >= min_y and curr_x <= max_x:
                curr_x += dx
                curr_y += dy
                dx -= 1 if dx != 0 else 0
                dy -= 1
                top_y = max(top_y, curr_y)
                if min_x <= curr_x <= max_x and min_y <= curr_y <= max_y:
                    ans.append((top_y, i_dx, i_dy))
                    break
            dy = i_dy
            dx = i_dx

    return ans

def day17_1(data):
    min_x, max_x, min_y, max_y = day17_parse(data)
    return max(day17_all_vels(min_x, max_x, min_y, max_y))[0]

def day17_2(data):
    min_x, max_x, min_y, max_y = day17_parse(data)
    return len(day17_all_vels(min_x, max_x, min_y, max_y))


""" DAY 18 """

class Node:
    def __init__(self) -> None:
        self.left = None
        self.right = None
        self.parent = None

    def __str__(self) -> str:
        return f"[{self.left},{self.right}]"

    def __repr__(self) -> str:
        return self.__str__()

def day18_tree(pair, parent):
    l, r = pair
    curr = Node()
    if not isinstance(l, int):
        l = day18_tree(l, curr)
    if not isinstance(r, int):
        r = day18_tree(r, curr)
    curr.left = l
    curr.right = r
    curr.parent = parent
    return curr

def day18_parse(data):
    x = []
    for line in data:
        x.append(day18_tree(ast.literal_eval(line), None))
    return x

def day18_add_left(v, node):
    # [[[[[[1,2],[9,8]],1],2],3],4]
    #                           |
    #     4                  |       4
    #                   |       3
    #                |      2
    #             |     1
    #         |      |
    #     1      2 9    8
    #                           |
    #             |                                 1
    #      4                 |       4
    #                   |       3
    #                |      2
    #             |     1
    #          9    8
    if node is None or node.parent is None:
        return
    sibling = node.parent.left
    if sibling == node:
        return day18_add_left(v, node.parent)
    elif isinstance(sibling, int):
        node.parent.left += v
    else:
        curr = sibling
        while not isinstance(curr.right, int):
            curr = curr.right
        curr.right += v

def day18_add_right(v, node):
    if node is None or node.parent is None:
        return
    sibling = node.parent.right
    if sibling == node:
        return day18_add_right(v, node.parent)
    elif isinstance(sibling, int):
        node.parent.right += v
    else:
        curr = sibling
        while not isinstance(curr.left, int):
            curr = curr.left
        curr.left += v

def day18_explode(curr, d):
    if curr is None or isinstance(curr, int):
        return False
    if d == 4:
        assert isinstance(curr.left, int) and isinstance(curr.right, int)
        day18_add_left(curr.left, curr)
        day18_add_right(curr.right, curr)
        if curr.parent.left == curr:
            curr.parent.left = 0
        else:
            curr.parent.right = 0
        return True
    else:
        exploded = day18_explode(curr.left, d + 1)
        if not exploded:
            exploded = day18_explode(curr.right, d + 1)
        return exploded

def day18_split(pair):
    splitted = False
    if not isinstance(pair.left, int):
        splitted = day18_split(pair.left)
    else:
        if pair.left >= 10:
            splitted = True
            curr = Node()
            curr.parent = pair
            curr.left = pair.left // 2
            curr.right = pair.left - curr.left
            pair.left = curr

    if not splitted:
        if not isinstance(pair.right, int):
            splitted = day18_split(pair.right)
        else:
            if pair.right >= 10:
                splitted = True
                curr = Node()
                curr.parent = pair
                curr.left = pair.right // 2
                curr.right = pair.right - curr.left
                pair.right = curr
    return splitted

def day18_add(p1, p2):
    curr = Node()
    curr.left = p1
    curr.right = p2
    p1.parent = curr
    p2.parent = curr
    return curr

def day18_reduce(curr):
    reduced = True
    while reduced:
        # #print(curr)
        reduced = day18_explode(curr, 0)
        if not reduced:
            reduced = day18_split(curr)

def day18_mag(pair):
    mag = 0
    if isinstance(pair.left, int):
        mag += 3 * pair.left
    else:
        mag += 3 * day18_mag(pair.left)
    if isinstance(pair.right, int):
        mag += 2 * pair.right
    else:
        mag += 2 * day18_mag(pair.right)
    return mag


def day18_1(data):
    data = day18_parse(data)
    # #print(data)
    curr = data[0]
    day18_reduce(curr)
    rest = data[1:]
    while rest:
        n = rest[0]
        day18_reduce(n)
        rest = rest[1:]
        curr = day18_add(curr, n)
        day18_reduce(curr)
    return day18_mag(curr)

def day18_clone(pair):
    assert pair is not None
    if isinstance(pair, int):
        return pair
    curr = Node()
    curr.left = day18_clone(pair.left)
    curr.right = day18_clone(pair.right)
    if not isinstance(curr.left, int):
        curr.left.parent = curr
    if not isinstance(curr.right, int):
        curr.right.parent = curr
    return curr

def day18_2(data_str):
    data = day18_parse(data_str)
    m = None
    for i in range(len(data)):
        for j in range(len(data)):
            if i != j:
                l = day18_clone(data[i])
                r = day18_clone(data[j])
                day18_reduce(l)
                day18_reduce(r)
                a = day18_add(l, r)
                day18_reduce(a)
                mag = day18_mag(a)
                if m is None or mag > m:
                    m = mag
                l = day18_clone(data[j])
                r = day18_clone(data[i])
                day18_reduce(l)
                day18_reduce(r)
                a = day18_add(l, r)
                day18_reduce(a)
                mag = day18_mag(a)
                if m is None or mag > m:
                    m = mag
    return m


""" DAY 19 """

def day19_parse(data):
    scanner = []
    a_s = {}
    for line in data:
        if not line:
            continue
        if "scanner" in line:
            s_id = int(line.replace("--- scanner ", "").replace(" ---", ""))
            scanner = []
            a_s[s_id] = scanner
        else:
            scanner.append(tuple([int(x) for x in line.split(",")]))

    return a_s

def day19_apply(x, y, z, t_x, t_y, t_z):
    x_ = x * t_x[0] + y * t_x[1] + z * t_x[2]
    y_ = x * t_y[0] + y * t_y[1] + z * t_y[2]
    z_ = x * t_z[0] + y * t_z[1] + z * t_z[2]
    return x_, y_, z_


def day19_bruteforce(beacons, diffs, positions, i, DP, already_compared):
    R = [
        ((1, 0, 0), (0, 1, 0), (0, 0, 1)),     # dx,dy,dz
        ((-1, 0, 0), (0, 1, 0), (0, 0, 1)),    # -dx,dy,dz
        ((1, 0, 0), (0, -1, 0), (0, 0, 1)),    # dx,-dy,dz
        ((-1, 0, 0), (0, -1, 0), (0, 0, 1)),    # -dx,-dy,dz
        ((1, 0, 0), (0, 1, 0), (0, 0, -1)),    # dx,dy,-dz
        ((-1, 0, 0), (0, 1, 0), (0, 0, -1)),    # -dx,dy,-dz
        ((1, 0, 0), (0, -1, 0), (0, 0, -1)),    # dx,-dy,-dz
        ((-1, 0, 0), (0, -1, 0), (0, 0, -1))    # -dx,-dy,-dz
    ]
    D = [(0, 1, 2),  # x,y,z
         (0, 2, 1),  # x,z,y
         (1, 0, 2),  # y,x,z
         (1, 2, 0),  # y,z,x
         (2, 0, 1),  # z,x,y
         (2, 1, 0)   # z,y,x
         ]

    for i_x, i_y, i_z in D:
        for r in R:
            t_x, t_y, t_z = r[i_x], r[i_y], r[i_z]
            # for each rotation
            # t_X is a tripplet with the multiplicative of each component for each component
            # Eg. t_x = (0,-1,0) -> x is -y from the original coordinate
            key = (t_x, t_y, t_z, i)
            if not key in DP:
                # coordinated of the beacon with rotation applied
                transformed_beacons = [day19_apply(
                    x, y, z, t_x, t_y, t_z) for x, y, z in beacons]

                # relative positions of each beacon to every other beacon
                diffs2 = {(x, y, z):
                          {(x2 - x, y2 - y, z2 - z)
                           for x2, y2, z2 in transformed_beacons}
                          for x, y, z in transformed_beacons}
                DP[key] = diffs2

            diffs2 = DP[key]
            for scanner_i in diffs:
                key = (i, scanner_i, t_x, t_y, t_z)
                if key in already_compared:
                    continue
                already_compared.add(key)
                # for each already known scanner
                inner_diffs = diffs[scanner_i]
                for inner_beacon in inner_diffs:
                    # for each beacon's relative positions
                    inner_rel_pos = inner_diffs[inner_beacon]
                    for other_beacon in diffs2:
                        # for each beacon's relative positions on the current scanner
                        other_rel_pos = diffs2[other_beacon]

                        # if there is an intersection of at least 12 points,
                        # we found the correct orientation
                        if len(other_rel_pos.intersection(inner_rel_pos)) >= 12:
                            assert scanner_i == 0 or scanner_i in positions
                            pos = tuple(
                                map(lambda i, j: i - j, inner_beacon, other_beacon))
                            if scanner_i != 0:
                                # if the match we found is not scanner 0, translate it to 0
                                pos = tuple(
                                    map(lambda i, j: i + j, pos, positions[scanner_i]))
                            return diffs2, pos
    return None, None

def day19_solve(a_s):
    diffs = {0: {}}
    positions = {0: (0, 0, 0)}
    diffs[0] = {(x, y, z):
                {(x2 - x, y2 - y, z2 - z)
                 for x2, y2, z2 in a_s[0]}
                for x, y, z in a_s[0]}

    solved = set([0])
    DP = {}
    already_compared = set()
    while len(solved) != len(a_s):
        for i in a_s:
            # for each scanner
            if i not in solved:
                diffs2, pos = day19_bruteforce(
                    a_s[i], diffs, positions, i, DP, already_compared)
                if diffs2 is not None:
                    diffs[i] = diffs2
                    positions[i] = pos
                    solved.add(i)
                    # break

    return diffs, positions

def day19_1(data):

    a_s = day19_parse(data)

    diffs, _ = day19_solve(a_s)
    beacons = 0
    for scanner_i in diffs:
        # for each already known scanner
        inner_diffs = diffs[scanner_i]
        for inner_beacon in inner_diffs:
            # for each beacon's relative positions
            found = False
            inner_rel_pos = inner_diffs[inner_beacon]
            for scanner_i2 in diffs:
                if scanner_i2 <= scanner_i:
                    continue
                diffs2 = diffs[scanner_i2]
                for other_beacon in diffs2:
                    # for each beacon's relative positions on the current scanner
                    other_rel_pos = diffs2[other_beacon]

                    # if there is an intersection of at least 12 points, we found a matching beacon
                    if len(other_rel_pos.intersection(inner_rel_pos)) >= 2:
                        found = True
                        break
            if not found:
                beacons += 1

    return beacons

def day19_2(data):
    a_s = day19_parse(data)

    _, positions = day19_solve(a_s)

    dists = []
    for s1 in positions:
        x1 = positions[s1][0]
        y1 = positions[s1][1]
        z1 = positions[s1][2]
        for s2 in positions:
            x2 = positions[s2][0]
            y2 = positions[s2][1]
            z2 = positions[s2][2]
            dists.append(abs(x2 - x1) + abs(y2 - y1) + abs(z2 - z1))

    return max(dists)


""" DAY 20 """

def day20_parse(data):
    algo = data[0]

    img = []
    for line in data[2:]:
        img.append(line)

    return algo, img

def day20_get_pixel(algo, r, c, G, old_min, old_max, outside_lit):
    DR = [-1, 0, 1]
    DC = [-1, 0, 1]
    n = ""
    for dr in DR:
        for dc in DC:
            rr, cc = r + dr, c + dc
            if not (old_min <= rr <= old_max and old_min <= cc <= old_max):
                if outside_lit:
                    n += "1"
                else:
                    n += "0"
                continue
            if G[(rr, cc)]:
                n += "1"
            else:
                n += "0"
    v = int(n, 2)
    return algo[v]

def day20_print(G, old_min, old_max):
    counter = 0
    for r in range(old_min, old_max):
        line = ""
        for c in range(old_min, old_max):
            if G[(r, c)]:
                line += "#"
                counter += 1
            else:
                line += " "
        print(line + "|")

def day20_solve(img, algo, t):
    R = len(img)
    C = len(img[0])
    old_min = 0
    old_max = R - 1

    G = defaultdict(bool)
    for r in range(R):
        for c in range(C):
            assert img[r][c] in ["#", "."], img[r][c]
            if img[r][c] == "#":
                G[(r, c)] = True

    outside_lit = False

    for _ in range(t):
        G2 = defaultdict(bool)
        for r in range(old_min - 1, old_max + 2):
            for c in range(old_min - 1, old_max + 2):
                p = day20_get_pixel(algo, r, c, G, old_min,
                                    old_max, outside_lit)
                if p == "#":
                    G2[(r, c)] = True
        old_min -= 1
        old_max += 1
        G = G2
        if algo[0] == "#":
            outside_lit = not outside_lit
        # day20_print(G, old_min, old_max)

    return sum(G.values())

def day20_1(data):
    algo, img = day20_parse(data)

    return day20_solve(img, algo, 2)

def day20_2(data):
    algo, img = day20_parse(data)

    return day20_solve(img, algo, 50)


""" DAY 21 """

def day21_parse(data):
    p1 = int(data[0].split("Player 1 starting position: ")[1])
    p2 = int(data[1].split("Player 2 starting position: ")[1])
    return p1, p2

def day21_1(data):
    p1, p2 = day21_parse(data)
    die = 1
    s1, s2 = 0, 0
    players = [p1, p2]
    scores = [s1, s2]
    curr = 0
    while True:
        launch = die + die + 1 + die + 2
        die = die + 3
        players[curr] += launch
        players[curr] = ((players[curr] - 1) % 10) + 1
        scores[curr] += players[curr]
        if scores[curr] >= 1000:
            return scores[(curr + 1) % 2] * (die - 1)
        curr = (
            curr + 1) % 2

def day21_total_outcomes(p1_, p2_):
    # In 1 round, these are the possible new positions for a pawn
    # (x+3 x+4 x+4 x+5 x+5 x+5 x+6 x+6 x+7)
    # (x+4 x+5 x+5 x+6 x+6 x+6 x+7 x+7 x+8)
    # (x+5 x+6 x+6 x+7 x+7 x+7 x+8 x+8 x+9)

    outcomes = [
        (3, 1),
        (4, 3),
        (5, 6),
        (6, 7),
        (7, 6),
        (8, 3),
        (9, 1)
    ]
    total_1 = 0
    total_2 = 0
    game_situations = defaultdict(int)
    game_situations[(p1_, 0, p2_, 0)] = 1
    while sum(game_situations.values()) != 0:
        # print(possible_positions_scores)
        next_game_situations = defaultdict(int)
        for (p1, s1, p2, s2) in game_situations:
            # how many boards are in this situation
            curr_n = game_situations[(p1, s1, p2, s2)]
            for jmp1, n1 in outcomes:
                new_p1 = p1 + jmp1
                new_p1 = ((new_p1 - 1) % 10) + 1
                new_s1 = s1 + new_p1
                if new_s1 >= 21:
                    # p1 wins
                    total_1 += n1 * curr_n
                else:
                    for jmp2, n2 in outcomes:
                        new_p2 = p2 + jmp2
                        new_p2 = ((new_p2 - 1) % 10) + 1
                        new_s2 = s2 + new_p2
                        if new_s2 >= 21:
                            # p2 wins
                            total_2 += n1 * n2 * curr_n
                        else:
                            next_game_situations[(new_p1, new_s1, new_p2,
                                                  new_s2)] += n1 * n2 * curr_n
        game_situations = next_game_situations
    return max(total_1, total_2)


def day21_2(data):
    p1, p2 = day21_parse(data)

    return day21_total_outcomes(p1, p2)


""" DAY 22 """

class OctaNode:
    def __init__(self, x1, x2, y1, y2, z1, z2, on, parent) -> None:
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2
        self.on = on
        self.parent = parent
        self.top_left_front: OctaNode = None
        self.top_right_front: OctaNode = None
        self.bottom_left_front: OctaNode = None
        self.bottom_right_front: OctaNode = None
        self.top_left_back: OctaNode = None
        self.top_right_back: OctaNode = None
        self.bottom_left_back: OctaNode = None
        self.bottom_right_back: OctaNode = None

    def children(self) -> List["OctaNode"]:
        return [self.top_left_front,
                self.top_right_front,
                self.bottom_left_front,
                self.bottom_right_front,
                self.top_left_back,
                self.top_right_back,
                self.bottom_left_back,
                self.bottom_right_back]

    def set_on(self, on):
        self.on = on

        self.top_left_front: OctaNode = None
        self.top_right_front: OctaNode = None
        self.bottom_left_front: OctaNode = None
        self.bottom_right_front: OctaNode = None
        self.top_left_back: OctaNode = None
        self.top_right_back: OctaNode = None
        self.bottom_left_back: OctaNode = None
        self.bottom_right_back: OctaNode = None

    def apply(self, x1_, x2_, y1_, y2_, z1_, z2_, on):
        if x2_ < self.x1 or x1_ >= self.x2 or \
                y2_ < self.y1 or y1_ >= self.y2 or \
                z2_ < self.z1 or z1_ >= self.z2:
            # no intersection
            return
        if x1_ <= self.x1 and self.x2 - 1 <= x2_ and \
                y1_ <= self.y1 and self.y2 - 1 <= y2_ and \
                z1_ <= self.z1 and self.z2 - 1 <= z2_:
            # This tree is fully inside the zone
            self.set_on(on)
            return

        if self.is_leaf():
            assert self.x2 - self.x1 != 0 and self.y2 - \
                self.y1 != 0 and self.z2 - self.z1 != 0
            # There is an intesection with our limits, just divide

            if self.x1 < x1_ < self.x2:
                mid_x = x1_
            elif self.x1 < x2_ < self.x2:
                mid_x = x2_
            elif x1_ <= self.x1 and self.x2 - 1 <= x2_:
                mid_x = self.x1
            else:
                mid_x = self.x1 + 1

            if self.y1 < y1_ < self.y2:
                mid_y = y1_
            elif self.y1 < y2_ < self.y2:
                mid_y = y2_
            elif y1_ <= self.y1 and self.y2 - 1 <= y2_:
                mid_y = self.y1
            else:
                mid_y = self.y1 + 1

            if self.z1 < z1_ < self.z2:
                mid_z = z1_
            elif self.z1 < z2_ < self.z2:
                mid_z = z2_
            elif z1_ <= self.z1 and self.z2 - 1 <= z2_:
                mid_z = self.z1
            else:
                mid_z = self.z1 + 1

            assert self.x1 <= mid_x and mid_x < self.x2 and \
                self.y1 <= mid_y and mid_y < self.y2 and \
                self.z1 <= mid_z and mid_z < self.z2

            self.top_left_front: OctaNode = OctaNode(
                self.x1, mid_x, mid_y, self.y2, mid_z, self.z2, self.on, self)
            self.top_right_front: OctaNode = OctaNode(
                mid_x, self.x2, mid_y, self.y2, mid_z, self.z2, self.on, self)
            self.bottom_left_front: OctaNode = OctaNode(
                self.x1, mid_x, self.y1, mid_y, mid_z, self.z2, self.on, self)
            self.bottom_right_front: OctaNode = OctaNode(
                mid_x, self.x2, self.y1, mid_y, mid_z, self.z2, self.on, self)
            self.top_left_back: OctaNode = OctaNode(
                self.x1, mid_x, mid_y, self.y2, self.z1, mid_z, self.on, self)
            self.top_right_back: OctaNode = OctaNode(
                mid_x, self.x2, mid_y, self.y2, self.z1, mid_z, self.on, self)
            self.bottom_left_back: OctaNode = OctaNode(
                self.x1, mid_x, self.y1, mid_y, self.z1, mid_z, self.on, self)
            self.bottom_right_back: OctaNode = OctaNode(
                mid_x, self.x2, self.y1, mid_y, self.z1, mid_z, self.on, self)
        for c in self.children():
            if c.x2 - c.x1 == 0 or c.y2 - c.y1 == 0 or c.z2 - c.z1 == 0:
                continue
            assert c.x2 - c.x1 >= 0 or c.y2 - c.y1 >= 0 or c.z2 - c.z1 >= 0
            c.apply(x1_, x2_, y1_, y2_, z1_, z2_, on)

    def is_leaf(self):
        leaf = all(c is None for c in self.children())
        any_none = any(c is None for c in self.children())
        assert leaf or not any_none
        return leaf

    def total_on(self):
        if self.x2 - self.x1 == 0 or self.y2 - self.y1 == 0 or self.z2 - self.z1 == 0:
            return 0
        if self.is_leaf():
            if not self.on:
                return 0
            x_rad = abs(self.x2 - self.x1)
            y_rad = abs(self.y2 - self.y1)
            z_rad = abs(self.z2 - self.z1)
            return x_rad * y_rad * z_rad
        else:
            return sum([c.total_on() for c in self.children()])

def day22_parse(data):
    robots = []
    for line in data:
        # on x=10..12,y=10..12,z=10..12
        on = line.startswith("on")
        line = line.replace("on ", "").replace("off ", "")
        x, y, z = line.split(",")
        x = x.replace("x=", "")
        x1, x2 = [int(v) for v in x.split("..")]
        y = y.replace("y=", "")
        y1, y2 = [int(v) for v in y.split("..")]
        z = z.replace("z=", "")
        z1, z2 = [int(v) for v in z.split("..")]
        robots.append((x1, x2, y1, y2, z1, z2, on))

    return robots

def day22_1(data):
    robots = day22_parse(data)
    n = OctaNode(-50, 50 + 1, -50, 50 + 1, -50, 50 + 1, False, None)

    for _, (x1, x2, y1, y2, z1, z2, on) in enumerate(robots):
        n.apply(x1, x2, y1, y2, z1, z2, on)

    return n.total_on()

    # lo = -50
    # hi = 50
    # all_on = set()
    # for x in range(lo, hi + 1):
    #     for y in range(lo, hi + 1):
    #         for z in range(lo, hi + 1):
    #             for x1, x2, y1, y2, z1, z2, on in robots:
    #                 if x1 <= x <= x2 and y1 <= y <= y2 and z1 <= z <= z2:
    #                     if on:
    #                         all_on.add((x, y, z))
    #                     else:
    #                         if (x, y, z) in all_on:
    #                             all_on.remove((x, y, z))
    # return len(all_on)

def day22_2(robots):
    robots = day22_parse(robots)

    min_x = min(x for x, _, _, _, _, _, _ in robots)
    min_y = min(y for _, _, y, _, _, _, _ in robots)
    min_z = min(z for _, _, _, _, z, _, _ in robots)
    max_x = max(x for _, x, _, _, _, _, _ in robots)
    max_y = max(y for _, _, _, y, _, _, _ in robots)
    max_z = max(z for _, _, _, _, _, z, _ in robots)

    n = OctaNode(min_x, max_x + 1, min_y, max_y +
                 1, min_z, max_z + 1, False, None)

    for _, (x1, x2, y1, y2, z1, z2, on) in enumerate(robots):
        n.apply(x1, x2, y1, y2, z1, z2, on)

    return n.total_on()


""" DAY 23 """

def day23_parse(data):
    return data

def day23_energy(c):
    E = {
        "A": 1,
        "B": 10,
        "C": 100,
        "D": 1000
    }
    return E[c]

def day23_room(c):
    E = {
        "A": 3,
        "B": 5,
        "C": 7,
        "D": 9
    }
    return E[c]

def day23_limits(rows):
    m = []
    for r in range(1, rows + 2):
        for c in range(1, 12):
            if r == 1 or c in [3, 5, 7, 9]:
                m.append((r, c))
    return m

def day23_heuristic(positions, limits, rows):
    remaining = 0
    for r, c in limits:
        if (r, c) in positions:
            char = positions[(r, c)]
            energy = day23_energy(char)
            if day23_room(char) != c:
                # effort to move to halway
                remaining += abs(r - 1) * energy
                # effort to move to correct room
                remaining += abs(day23_room(char) - c) * energy
                # effort to go to the back of room
                remaining += 2 * energy
            else:
                # effort to go to the back of room
                remaining += abs(rows + 1 - r) * energy
    return remaining

def day23_is_complete(positions, rows):
    for r in range(2, rows + 2):
        if not (r, 3) in positions or positions[(r, 3)] != "A":
            return False
        if not (r, 5) in positions or positions[(r, 5)] != "B":
            return False
        if not (r, 7) in positions or positions[(r, 7)] != "C":
            return False
        if not (r, 9) in positions or positions[(r, 9)] != "D":
            return False
    return True

def day23_move_to(curr_r, curr_c, dest_r, dest_c, cost, occupied, limits):

    D = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited = set()
    q = [(curr_r, curr_c, 0)]
    while q:
        r, c, energy = heappop(q)
        if r == dest_r and c == dest_c:
            return energy
        if (r, c) in visited:
            continue
        visited.add((r, c))
        for dr, dc in D:
            rr, cc = r + dr, c + dc
            if (rr, cc) in limits and (rr, cc) not in occupied:
                heappush(q, (rr, cc, energy + cost))

    return 0

def day23_print(positions, rows):
    B = [
        "#############",
        "#...........#",
        "###.#.#.#.###",
        "  #.#.#.#.#",
        "  #########"
    ]

    B2 = B[:3]
    for _ in range(rows - 2):
        B2.append("  #.#.#.#.#")
    B2 += B[3:]
    B = B2

    for r in range(len(B)):
        row = ""
        for c in range(len(B[r])):
            if (r, c) in positions:
                row += positions[(r, c)]
            else:
                row += B[r][c]
        print(row)
    print()

def day23_solve(positions, rows, limits):
    hallway = [
        (1, 1),
        (1, 2),
        (1, 4),
        (1, 6),
        (1, 8),
        (1, 10),
        (1, 11)
    ]

    counter = 0
    q = [(day23_heuristic(positions, limits, rows), 0, counter)]
    visited2 = {}
    costs = None
    states = {}
    states[counter] = positions
    counter += 1
    while q:
        _, energy, new_pos_i = heappop(q)
        new_positions = states[new_pos_i]
        if day23_is_complete(new_positions, rows):
            return energy
        if costs is not None and energy >= costs:
            continue
        key = tuple(sorted((char, r, c)
                    for (r, c), char in new_positions.items()))
        if key in visited2 and visited2[key] <= energy:
            continue
        visited2[key] = energy
        occupied = new_positions.keys()

        for (r, c), char in new_positions.items():
            room = day23_room(char)
            if r != 1:  # in a room
                blocking = False
                for rrr in range(r + 1, rows + 2):
                    blocking |= (rrr, c) in new_positions and day23_room(
                        new_positions[(rrr, c)]) != c
                # wrong room or blocking other
                if room != c or blocking:
                    for rr, cc in hallway:  # try to move to hallway
                        new_energy = day23_move_to(
                            r, c, rr, cc, day23_energy(char), occupied, limits)
                        if new_energy != 0:
                            new_pos2 = {k: v for k, v in new_positions.items()}
                            new_pos2[(rr, cc)] = char
                            new_pos2.pop((r, c))
                            states[counter] = new_pos2
                            counter += 1
                            heur = day23_heuristic(new_pos2, limits, rows)
                            heappush(
                                q, (heur + energy + new_energy, energy + new_energy, counter - 1))
            else:  # in hallway
                added = False
                for rr in range(rows + 1, 1, -1):
                    if added:
                        break
                    # try to move to room
                    cc = room
                    blocking = False
                    for rrr in range(rr + 1, rows + 2):
                        blocking |= ((rrr, cc) in new_positions and day23_room(
                            new_positions[(rrr, cc)]) != cc)
                    # if we don't block
                    if not blocking:
                        new_energy = day23_move_to(
                            r, c, rr, cc, day23_energy(char), occupied, limits)
                        if new_energy != 0:
                            new_pos2 = {k: v for k, v in new_positions.items()}
                            new_pos2[(rr, cc)] = char
                            new_pos2.pop((r, c))
                            states[counter] = new_pos2
                            counter += 1
                            heur = day23_heuristic(new_pos2, limits, rows)
                            heappush(
                                q, (heur + energy + new_energy, energy + new_energy, counter - 1))
                            added = True
                            break  # moved to back of room
    assert False

def day23_1(data):
    data = day23_parse(data)
    positions = {}
    for r in range(len(data)):
        for c in range(len(data[r])):
            char = data[r][c]
            if char in "ABCD":
                positions[(r, c)] = char

    limits = day23_limits(2)
    return day23_solve(positions, 2, limits)

def day23_2(data):
    data = day23_parse(data)
    positions = {}
    data2 = data[:3]
    data2.append("  #D#C#B#A#")
    data2.append("  #D#B#A#C#")
    data2 += data[3:]
    for r in range(len(data2)):
        for c in range(len(data2[r])):
            char = data2[r][c]
            if char in "ABCD":
                positions[(r, c)] = char

    limits = day23_limits(4)
    return day23_solve(positions, 4, limits)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2021)
