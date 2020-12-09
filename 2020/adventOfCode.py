# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
import functools
import math
import os
import sys
import time
from collections import defaultdict
from heapq import heappop, heappush
import copy

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
print(FILE_DIR)
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
sys.path.insert(0, FILE_DIR + "/../../")
import computer  # NOQA: E402
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

def day1_1(data):
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            a = int(data[i])
            b = int(data[j])
            if a + b == 2020:
                return a * b
    return None

def day1_2(data):
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            for k in range(j + 1, len(data)):
                a = int(data[i])
                b = int(data[j])
                c = int(data[k])
                if a + b + c == 2020:
                    return a * b * c
    return None


""" DAY 2 """

def day2_1(data):
    count = 0
    for line in data:
        # 6-10 w: wwwwwhwwwwwrpww
        policy = line.split(": ")[0]
        password = line.split(": ")[1]
        letter = policy.split(" ")[1][0]
        range_ = policy.split(" ")[0]
        min_ = int(range_.split("-")[0])
        max_ = int(range_.split("-")[1])
        count_letter = 0
        for c in password:
            if c == letter:
                count_letter += 1

        if min_ <= count_letter <= max_:
            count += 1

    return count

def day2_2(data):
    count = 0
    for line in data:
        # 6-10 w: wwwwwhwwwwwrpww
        policy = line.split(": ")[0]
        password = line.split(": ")[1]
        letter = policy.split(" ")[1][0]
        range_ = policy.split(" ")[0]
        min_ = int(range_.split("-")[0])
        max_ = int(range_.split("-")[1])

        if (password[min_ - 1] == letter and password[max_ - 1] != letter) or \
           (password[min_ - 1] != letter and password[max_ - 1] == letter):
            count += 1
    return count


""" DAY 3 """

def day3_solve(data, dx, dy):
    x, y = (0, 0)
    size = len(data)
    counter = 0
    while y < size:
        if data[y][x] == '#':
            counter += 1
        x += dx
        x = x % len(data[0])
        y += dy
    return counter

def day3_1(data):
    # data = read_input(2020, 301)
    return day3_solve(data, 3, 1)

def day3_2(data):
    # data = read_input(2020, 301)
    slopes = [
        (3, 1),
        (1, 1),
        (5, 1),
        (7, 1),
        (1, 2)
    ]
    return functools.reduce(lambda a, b: a * b, [day3_solve(data, dx, dy) for (dx, dy) in slopes])


""" DAY 3 """

def day4_process(data, f):
    # data = read_input(2020, 401)
    fields = {}
    expected = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    count = 0
    for line in data:
        if line == "":
            valid = all([k in fields for k in expected])
            if valid and f(fields):
                count += 1
            fields = {}
            continue
        for part in line.split(" "):
            fields[part.split(":")[0]] = part.split(":")[1]

    valid = all([k in fields for k in expected])
    if valid and f(fields):
        count += 1
    return count

def day4_valid(fields):
    valid = True
    for f in fields:
        a = fields[f]
        try:
            if f == "byr":
                valid &= len(a) == 4 and 1920 <= int(a) <= 2002
            if f == "iyr":
                valid &= len(a) == 4 and 2010 <= int(a) <= 2020
            if f == "eyr":
                valid &= len(a) == 4 and 2020 <= int(a) <= 2030
            if f == "hgt":
                s = a[-2:]
                if s == "cm":
                    valid &= 150 <= int(a[:-2]) <= 193
                elif s == "in":
                    valid &= 59 <= int(a[:-2]) <= 76
                else:
                    valid = False
            if f == "hcl":
                valid &= a[0] == "#" and len(a) == 7
                _ = int(a[1:], 16)
            if f == "ecl":
                valid &= a in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")
            if f == "pid":
                valid &= len(a) == 9 and a.isnumeric()
            if not valid:
                # print(f, a)
                break
        except ValueError:
            valid = False
            break
    return valid

def day4_1(data):
    # data = read_input(2020, 401)
    return day4_process(data, lambda a: True)

def day4_2(data):
    # data = read_input(2020, 401)
    return day4_process(data, day4_valid)


""" DAY 5 """

def day5_get_id(l):
    lo = 0
    hi = 127
    le = 0
    ri = 7
    for i in l:
        mid_r = lo + ((hi - lo) // 2)
        mid_s = le + ((ri - le) // 2)
        if i == "F":
            hi = mid_r
        elif i == "B":
            lo = mid_r + 1
        elif i == "L":
            ri = mid_s
        elif i == "R":
            le = mid_s + 1
    r = lo
    s = le

    return r * 8 + s

def day5_1(data):
    # data = read_input(2020, 501)
    return max([day5_get_id(l) for l in data])

def day5_2(data):
    # data = read_input(2020, 401)
    ids = [day5_get_id(l) for l in data]
    for r in range(128):
        for s in range(8):
            seat_id = r * 8 + s
            if ((seat_id - 1) in ids) and \
               ((seat_id + 1) in ids) and \
               (not seat_id in ids):
                return seat_id
    return None


""" DAY 6 """

def day6_solve(data):
    group = []
    count1 = 0
    count2 = 0

    # Add an extra line to process last group
    data.append("")
    for line in data:
        if line == "":
            ansMap = {}
            for person in group:
                for answer in person:
                    if answer in ansMap:
                        ansMap[answer] += 1
                    else:
                        ansMap[answer] = 1
            for answer in ansMap:
                count1 += 1
                if ansMap[answer] == len(group):
                    count2 += 1

            group = []
        else:
            assert len(line) <= 26
            group.append(line)

    return count1, count2

def day6_1(data):
    # data = read_input(2020, 601)
    return day6_solve(data)[0]

def day6_2(data):
    return day6_solve(data)[1]


""" DAY 7 """

def day7_parse(data):
    holds = {}
    for rule in data:
        outer_bag, rest = tuple(rule.split(" contain"))
        outer_bag = outer_bag.replace("bags", "bag")
        contents = {}
        if rest != " no other bags.":
            rest = rest[1:-1]  # strip white space and period
            for inner_rule in rest.split(", "):
                ammount = int(inner_rule.split(" ")[0])
                inner_bag = inner_rule.replace(
                    str(ammount) + " ", "").replace("bags", "bag")
                contents[inner_bag] = ammount
        holds[outer_bag] = contents
    return holds

def day7_1(data):
    # data = read_input(2020, 701)
    holds = day7_parse(data)
    can_be_in = {}
    for bag in holds:
        for inner_bag in holds[bag]:
            if inner_bag not in can_be_in:
                can_be_in[inner_bag] = set()
            can_be_in[inner_bag].add(bag)
    return day7_solve1(can_be_in)

def day7_solve1(can_be_in):
    stack = set(can_be_in["shiny gold bag"])
    result = set()
    while stack:
        bag = stack.pop()
        result.add(bag)
        if bag in can_be_in:
            for outer_bag in can_be_in[bag]:
                stack.add(outer_bag)
    return len(result)

def day7_size(holds, mem, bag):
    if bag in mem:
        return mem[bag]

    total = 1
    for inner_bag in holds[bag]:
        total += holds[bag][inner_bag] * (day7_size(holds, mem, inner_bag))

    mem[bag] = total
    return total

def day7_2(data):
    # data = read_input(2020, 702)
    holds = day7_parse(data)

    # outer_bag will include itself so decrease 1
    return day7_size(holds, {}, "shiny gold bag") - 1


""" DAY 8 """

def day8_run_program(program):
    program_counter = 0
    acc = 0
    seen = set([0])
    while True:
        inst, value = program[program_counter]
        next_pc, acc = computer.comp_exec(inst, program_counter, value, acc)
        if next_pc in seen or next_pc >= len(program):
            # Stop if repeated inst or if reached end of program
            return acc, next_pc in seen
        seen.add(next_pc)
        program_counter = next_pc

def day8_1(data):
    program = computer.parse_program(data)
    return day8_run_program(program)[0]

def day8_2(data):
    program = computer.parse_program(data)
    idx = -1
    while True:
        idx += 1
        old_inst = program[idx][0]
        if old_inst == "jmp":
            program[idx][0] = "nop"
        elif old_inst == "nop":
            program[idx][0] = "jmp"
        else:
            continue

        acc, infinite = day8_run_program(program)
        if not infinite:
            return acc

        program[idx][0] = old_inst
    return None


""" DAY 9 """

def day9_1(data):
    # data = read_input(2020, 901)
    preamble = 25
    buffer = set()
    for i, elem in enumerate(data):
        elem = int(elem)
        if i < preamble:
            buffer.add(elem)
            continue
        found = False
        for _, a1 in enumerate(buffer):
            for _, a2 in enumerate(buffer):
                if (a1 != a2) and (a1 + a2 == elem):
                    found = True
                    break
        if not found:
            return elem
        buffer = set(list(buffer)[1:])
        buffer.add(int(elem))
    return None

def day9_2(data):
    target = day9_1(data)
    # data = read_input(2020, 901)
    # val = 127
    data = [int(n) for n in data]
    lo, hi = 0, 1
    total = data[0] + data[1]
    while True:
        if total < target:
            hi += 1
            total += data[hi]
        elif total > target:
            total -= data[lo]
            lo += 1
        else:
            buffer = data[lo:hi + 1]
            return min(buffer) + max(buffer)

    return None


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2020)
