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

        if len(stack) != 0 and not is_corrupted:
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


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2021)
