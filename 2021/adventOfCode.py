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
    for signal, value in data:

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
            if len(x) == 2:
                for c in x:
                    segments["c"].add(c)
                    segments["f"].add(c)
            elif len(x) == 4:
                for c in x:
                    segments["b"].add(c)
                    # segments["c"].add(c)
                    segments["d"].add(c)
                    # segments["f"].add(c)
            elif len(x) == 3:
                for c in x:
                    segments["a"].add(c)
                    # segments["c"].add(c)
                    # segments["f"].add(c)

        all_5 = [x for x in signal if len(x) == 5]
        counts = Counter()
        for x in all_5:
            for c in x:
                counts[c] += 1
        k = ""
        for c, count in counts.items():
            if count == len(all_5):
                k += c
        assert len(k) == 3

        all_g = [x for x in signal if len(x) not in [2, 4, 3]]
        counts3 = Counter()
        for x in all_g:
            for c in x:
                counts3[c] += 1
        k3 = ""
        for c, count in counts3.items():
            if count == len(all_g):
                k3 += c
                segments["g"].add(c)

        all_6 = [x for x in signal if len(x) == 6]
        counts2 = Counter()
        for x in all_6:
            for c in x:
                counts2[c] += 1
        k2 = ""
        for c, count in counts2.items():
            if count == len(all_6):
                k2 += c
        assert len(k2) == 4

        all_s = "abcdefg"
        used = []
        for l in segments.values():
            for c in l:
                used.append(c)
        for c in all_s:
            if not c in used:
                segments["e"] = set([c])

        k_bak = k
        k2_bak = k2
        changed2 = True
        while changed2:
            changed2 = False

            change = True
            while change:
                change = False
                for s, ps in segments.items():
                    if len(ps) == 1:
                        continue

                    for s2, ps2 in segments.items():
                        if s2 != s:
                            if len(ps2) > 0 and len(ps) > len(ps2) and ps2.issubset(ps):
                                segments[s] = ps.difference(ps2)
                                change = True
                                changed2 = True

            k = k_bak
            k2 = k2_bak

            pos = "adg"
            if len(segments["a"]) == 1:
                pos = pos.replace("a", "")
                k = k.replace(list(segments["a"])[0], "")
            if len(segments["d"]) == 1:
                pos = pos.replace("d", "")
                k = k.replace(list(segments["d"])[0], "")
            if len(segments["g"]) == 1:
                pos = pos.replace("g", "")
                k = k.replace(list(segments["g"])[0], "")
            if len(k) == 1:
                segments[pos] = set([k])
                changed2 = True

            pos = "abfg"
            if len(segments["a"]) == 1:
                pos = pos.replace("a", "")
                k2 = k2.replace(list(segments["a"])[0], "")
            if len(segments["b"]) == 1:
                pos = pos.replace("b", "")
                k2 = k2.replace(list(segments["b"])[0], "")
            if len(segments["f"]) == 1:
                pos = pos.replace("f", "")
                k2 = k2.replace(list(segments["f"])[0], "")
            if len(segments["g"]) == 1:
                pos = pos.replace("g", "")
                k2 = k2.replace(list(segments["g"])[0], "")
            if len(k2) == 1:
                segments[pos] = set([k2])
                changed2 = True

        mapping = {}
        for k, v in segments.items():
            mapping[v.pop()] = k
        output = ""
        for d in value:
            decoded_d = ""
            decoded = ""
            for c in d:
                decoded += mapping[c]

            decoded = "".join(sorted(decoded))
            decoded_d += str(result[decoded])
            output += decoded_d
        total += int(output)

    return total


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2021)
