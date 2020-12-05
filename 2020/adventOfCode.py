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
    #data = read_input(2020, 501)
    return max([day5_get_id(l) for l in data])

def day5_2(data):
    #data = read_input(2020, 401)
    ids = [day5_get_id(l) for l in data]
    for r in range(128):
        for s in range(8):
            seat_id = r * 8 + s
            if ((seat_id - 1) in ids) and \
               ((seat_id + 1) in ids) and \
               (not seat_id in ids):
                return seat_id
    return None


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2020)