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
from copy import deepcopy
from collections import defaultdict
from heapq import heappop, heappush

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
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
# Day 1, part 1: 902451 (0.058 secs)
# Day 1, part 2: 85555470 (0.069 secs)

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
# Day 2, part 1: 519 (0.110 secs)
# Day 2, part 2: 708 (0.037 secs)

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
# Day 3, part 1: 292 (0.031 secs)
# Day 3, part 2: 9354744432 (0.019 secs)

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


""" DAY 4 """
# Day 4, part 1: 200 (0.049 secs)
# Day 4, part 2: 116 (0.050 secs)

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
# Day 5, part 1: 813 (0.054 secs)
# Day 5, part 2: 612 (0.028 secs)

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
# Day 6, part 1: 6683 (0.100 secs)
# Day 6, part 2: 3122 (0.029 secs)

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
# Day 7, part 1: 164 (0.110 secs)
# Day 7, part 2: 7872 (0.046 secs)

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
# Day 8, part 1: 1930 (0.061 secs)
# Day 8, part 2: 1688 (0.063 secs)

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
# Day 9, part 1: 2089807806 (0.124 secs)
# Day 9, part 2: 245848639 (0.029 secs)

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


""" DAY 10 """
# Day 10, part 1: 2059 (0.051 secs)
# Day 10, part 2: 86812553324672 (0.016 secs)

def day10_1(data):
    # data = read_input(2020, 1001)
    data = [int(x) for x in data]
    data = sorted(data)
    q = [(0, 0, data, [])]
    final_chain = []
    while q:
        _, curr, remaining, chain = heappop(q)
        a = curr

        if not remaining:
            final_chain = chain
            break

        for j in range(len(remaining)):
            b = remaining[j]

            if abs(a - b) <= 3:
                assert a < b
                new_l = chain[:]
                new_l.append((a, b))
                new_rest = [d for d in remaining if d != b]

                heappush(q, ((len(new_rest), b, new_rest, new_l)))

    diff_1 = 0
    diff_3 = 0
    for e1, e2 in final_chain:
        if abs(e1 - e2) == 1:
            diff_1 += 1
        elif abs(e1 - e2) == 3:
            diff_3 += 1
    return diff_1 * (diff_3 + 1)

def day10_2(data):
    # data = read_input(2020, 1001)
    data = [int(x) for x in data]
    data = sorted(data)
    return day10_combinations([0] + data, {})

def day10_combinations(available, mem):
    key = tuple(available)
    if key in mem:
        return mem[key]

    if len(available) == 1:
        return 1

    a = available[0]
    total = 0
    for i in range(1, 4):
        if i >= len(available):
            break
        b = available[i]
        if abs(a - b) <= 3:
            total += day10_combinations(available[i:], mem)
    mem[key] = total
    return total


""" DAY 11 """
# Day 11, part 1: 2254 (0.630 secs)
# Day 11, part 2: 2004 (0.912 secs)

def day11_adj(data, r, c, extend=False):
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if (dr == 0 and dc == 0):
                continue
            n_r, n_c = r + dr, c + dc
            found = False
            while (0 <= n_r < len(data)) and (0 <= n_c < len(data[n_r])):
                if data[n_r][n_c] == "L":
                    break
                if data[n_r][n_c] == "#":
                    found = True
                    break
                if not extend:
                    break
                n_r, n_c = n_r + dr, n_c + dc
            if found:
                count += 1
    return count

def day11_print(data):
    for line in data:
        print(str(line))

def day11_tick(seats, data, extended=False):
    stop = True
    new_data = deepcopy(data)
    for r, c in seats:
        if data[r][c] == "L" and day11_adj(data, r, c, extended) == 0:
            new_data[r][c] = "#"
            stop = False
        tolerance = 5 if extended else 4
        if data[r][c] == "#" and day11_adj(data, r, c, extended) >= tolerance:
            new_data[r][c] = "L"
            stop = False
    return new_data, stop

def day11_occupied(seats, data):
    count = 0
    for r, c in seats:
        if data[r][c] == "#":
            count += 1
    return count

def day11_seats(data):
    seats = []
    for r in range(len(data)):
        for c in range(len(data[0])):
            if data[r][c] == "L":
                seats.append((r, c))
    return seats

def day11_1(data):
    # data = read_input(2020, 1101)
    data = [list(line) for line in data]
    seats = day11_seats(data)
    stop = False
    while not stop:
        data, stop = day11_tick(seats, data)

    return day11_occupied(seats, data)

def day11_2(data):
    # data = read_input(2020, 1101)
    data = [list(line) for line in data]
    seats = day11_seats(data)
    stop = False
    while not stop:
        data, stop = day11_tick(seats, data, True)

    return day11_occupied(seats, data)


""" DAY 12 """
# Day 12, part 1: 636 (0.078 secs)
# Day 12, part 2: 26841 (0.076 secs)

def day12_print(dx, dy):
    if dx == 0 and dy == -1:
        print("^")
    elif dx == -1 and dy == 0:
        print("<")
    elif dx == 1 and dy == 0:
        print(">")
    elif dx == 0 and dy == 1:
        print("v")
    else:
        raise ValueError

def day12_solve(data, dx, dy, waypoint=False):
    x, y = 0, 0
    for action, val in data:
        if action == "N":
            if waypoint:
                dy -= val
            else:
                y -= val
        elif action == "S":
            if waypoint:
                dy += val
            else:
                y += val
        elif action == "E":
            if waypoint:
                dx += val
            else:
                x += val
        elif action == "W":
            if waypoint:
                dx -= val
            else:
                x -= val
        elif action == "L":
            steps = val // 90
            assert val % 90 == 0
            while steps > 0:
                n_dx = dy
                n_dy = -dx
                dx = n_dx
                dy = n_dy
                steps -= 1

        elif action == "R":
            steps = val // 90
            assert val % 90 == 0
            while steps > 0:
                n_dx = -dy
                n_dy = dx
                dx = n_dx
                dy = n_dy
                steps -= 1

        elif action == "F":
            x += val * dx
            y += val * dy
    return abs(x) + abs(y)

def day12_1(data):
    data = [(x[0], int(x[1:])) for x in data]
    return day12_solve(data, 1, 0)

def day12_2(data):
    data = [(x[0], int(x[1:])) for x in data]
    return day12_solve(data, 10, -1, True)


""" DAY 13 """
# Day 13, part 1: 2045 (0.038 secs)
# Day 13, part 2: 402251700208309 (0.073 secs)

def day13_1(data):
    # data = read_input(2020, 1301)
    early = int(data[0])
    buses = []
    for i in data[1].split(","):
        if i == "x":
            continue
        b_id = int(i)
        buses.append(b_id)
    x = early
    while True:
        for b in buses:
            if x % b == 0:
                return abs(early - x) * b
        x += 1
    return None

# Find A such that (A*N) % M == 1
def modinv(N, M):
    ans = 1
    total = N
    while True:
        if total % M == 1:
            assert (ans * N) % M == 1
            return ans
        ans += 1
        total += N

def day13_2(data):
    # data = read_input(2020, 1301)
    buses = []
    rem = []
    m = {}
    for i, e in enumerate(data[1].split(",")):
        if e == "x":
            continue
        b_id = int(e)
        buses.append(b_id)
        rem.append(-i % b_id)
        m[b_id] = i

    # These are Linear Diophantine equations
    # b[0]*x     = t -> t = 0 (mod b[0])
    # b[1]*y - 1 = t -> t = -1 (mod b[1])
    # b[2]*z - 2 = t -> t = -2 (mod(b[2]))

    # Use the Chinese remainder theorem to solve for t
    #   x = ( ∑(rem[i]*pp[i]*inv[i]) ) % prod
    # Where:
    #  rem[i] is the time after t
    #  prod is product of all IDs
    #  pp[i] is product of all divided by b[i]
    #  inv[i] = Modular Multiplicative Inverse of
    #           pp[i] with respect to b[i], i.e,
    #           value A such that (A*pp[i]) % b[i] == 1

    prod = 1
    for ID in buses:
        prod *= ID

    pp = [prod // ID for ID in buses]

    inv = [modinv(pp_i, buses[i]) for i, pp_i in enumerate(pp)]

    ans = 0
    for i in range(len(buses)):
        ans += rem[i] * pp[i] * inv[i]
    ans = ans % prod

    for ID in buses:
        assert (ans + m[ID]) % ID == 0
    return ans


""" DAY 14 """
# Day 14, part 1: 13105044880745 (0.076 secs)
# Day 14, part 2: 3505392154485 (0.610 secs)

def day14_1(data):
    # data = read_input(2020, 1401)
    memory = {}
    mask = ""
    maskAnd = 0
    maskOr = 0
    for line in data:
        if line[:4] == "mask":
            mask = line[7:]
            # keep only 0 to &
            maskAnd = int(mask.replace("X", "1"), 2)
            # keep only 1 to |
            maskOr = int(mask.replace("X", "0"), 2)
        else:
            addr = line.split("]")[0]
            addr = int(addr[4:])
            value = int(line.split(" = ")[1])

            binary = "{0:b}".format((value & maskAnd) | maskOr)
            memory[addr] = binary
    res = 0
    for addr in memory:
        res += int("".join(memory[addr]), 2)
    return res

def day14_2(data):
    # data = read_input(2020, 1401)
    memory = {}
    mask = ""
    maskOr = 0
    for line in data:
        if line[:4] == "mask":
            mask = line[7:]
            maskOr = int(mask.replace("X", "1"), 2)
        else:
            addr = line.split("]")[0]
            addr = int(addr[4:])
            value = int(line.split(" = ")[1])

            binary = "{0:b}".format(addr | maskOr)
            binary = "0" * (36 - len(binary)) + binary

            q = [binary]
            for i, c in enumerate(mask):
                if c != "X":
                    continue

                q2 = []
                for a in q:
                    a2 = list(a)
                    a2[i] = "1"
                    q2.append("".join(a2))
                    a2[i] = "0"
                    q2.append("".join(a2))
                q = q2
            # print("Processing: " + line + " Mask: " + mask)
            # print("Addresses: " + str([int(a,2) for a in q]))
            for a in q:
                addr = int(a, 2)
                memory[addr] = value
    res = 0
    for addr in memory:
        res += memory[addr]
    return res


""" DAY 15 """
# Day 15, part 1: 981 (0.097 secs)
# Day 15, part 2: 164878 (15.961 secs)

def day15_solve(data, target):
    ns = [int(n) for n in data[0].split(",")]
    timestamp = 1
    memory = {}
    last_n = 0
    for i, _ in enumerate(ns):
        memory[ns[i]] = [timestamp]
        last_n = ns[i]
        timestamp += 1

    while timestamp <= target:
        if last_n in memory:
            if len(memory[last_n]) == 1:
                last_n = 0
            else:
                last_n = memory[last_n][1] - memory[last_n][0]
        else:
            last_n = 0
        if last_n in memory:
            if len(memory[last_n]) == 1:
                memory[last_n].append(timestamp)
            else:
                memory[last_n][0] = memory[last_n][1]
                memory[last_n][1] = timestamp
        else:
            memory[last_n] = [timestamp]
        timestamp += 1
    return last_n

def day15_1(data):
    # data = read_input(2020, 1501)
    return day15_solve(data, 2020)

def day15_2(data):
    # data = read_input(2020, 1501)
    return day15_solve(data, 30000000)


""" DAY 16 """
# Day 16, part 1: 26053 (0.293 secs)
# Day 16, part 2: 1515506256421 (0.189 secs)

def day16_parse(data):
    rules = {}
    for line in data:
        line = line.rstrip()
        if line == "":
            break
        field = line.split(": ")[0]
        ranges = line.split(": ")[1].split(" or ")
        ranges = [tuple([int(e) for e in r.split("-")]) for r in ranges]
        rules[field] = ranges

    my_ticket = [int(e) for e in data[len(rules) + 2].split(",")]

    tickets = []
    for i in range(len(rules) + 5, len(data)):
        ticket = [int(e) for e in data[i].split(",")]
        tickets.append(ticket)

    return (rules, my_ticket, tickets)

def day16_valid_rule(rule, ticket_value):
    (fst_low, fst_high), (snd_low, snd_high) = rule
    return fst_low <= ticket_value <= fst_high or \
        snd_low <= ticket_value <= snd_high

def day16_any_rule(rules, ticket_value):
    for field in rules:
        (fst_low, fst_high), (snd_low, snd_high) = rules[field]
        if fst_low <= ticket_value <= fst_high or \
           snd_low <= ticket_value <= snd_high:
            return (True, field)
    return (False, None)

def day16_valid(rules, ticket):
    invalid_values = []
    valid = True
    for value in ticket:
        if not any([day16_valid_rule(rules[rule], value) for rule in rules]):
            invalid_values.append(value)
            valid = False

    return (valid, invalid_values)

def day16_1(data):
    # data = read_input(2020, 1601)

    rules, _, tickets = day16_parse(data)

    invalid_n = []
    total = 0
    for ticket in tickets:
        _, invalid_n = day16_valid(rules, ticket)
        total += sum(invalid_n)
    return total

def day16_2(data):
    # data = read_input(2020, 1601)

    rules, my_ticket, tickets = day16_parse(data)

    valid_tickets = []
    for ticket in tickets:
        valid, _ = day16_valid(rules, ticket)
        if valid:
            valid_tickets.append(ticket)

    valid_tickets.append(my_ticket)
    possible = {}
    for field in rules:
        possible[field] = list(range(len(my_ticket)))

    for ticket in valid_tickets:
        for i, ticket_value in enumerate(ticket):
            for field in rules:
                if len(possible[field]) == 1 or i not in possible[field]:
                    continue
                if not day16_valid_rule(rules[field], ticket_value):
                    possible[field].remove(i)
                    break

    # Reach a fixed state
    closed_fields = set()
    while len(closed_fields) != len(rules):
        for field in possible:
            possible_pos = possible[field]
            if len(possible_pos) == 1:
                if field not in closed_fields:
                    closed_fields.add(field)
                continue

            for pos in possible_pos:
                for other_field in closed_fields:
                    if pos == possible[other_field][0]:
                        possible[field].remove(pos)

    total = 1
    for field in possible:
        if field.startswith("departure"):
            total *= my_ticket[possible[field][0]]

    return total


""" DAY 17 """
# Day 17, part 1: 395 (1.397 secs)
# Day 17, part 2: 2296 (4.116 secs)

def day17_update_bounds(min_x, max_x, x):
    return (min(min_x, x - 1), max(max_x, x + 1))

def day17_boot(data, extra_dim):
    Y = len(data)
    X = len(data[0])
    active = set()
    for y in range(Y):
        for x in range(X):
            if data[y][x] == "#":
                active.add((y, x, 0, 0))

    min_x, max_x = -1, X + 1
    min_y, max_y = -1, Y + 1
    min_z, max_z = -1, 1
    min_w, max_w = -1, 1
    if not extra_dim:
        min_w = max_w = 0

    for _ in range(6):
        new_active = set(list(active))
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                for z in range(min_z, max_z + 1):
                    for w in range(min_w, max_w + 1):
                        count = 0
                        D_X = D_Y = D_Z = D_W = [-1, 0, 1]
                        if not extra_dim:
                            D_W = [0]
                        for d_x in D_X:
                            for d_y in D_Y:
                                for d_z in D_Z:
                                    for d_w in D_W:
                                        if d_x == d_y == d_z == d_w == 0:
                                            continue

                                        curr_x = x + d_x
                                        curr_y = y + d_y
                                        curr_z = z + d_z
                                        curr_w = w + d_w

                                        if (curr_x, curr_y, curr_z, curr_w) in active:
                                            count += 1

                        if (x, y, z, w) in active:
                            if not count in (2, 3):
                                new_active.remove((x, y, z, w))
                        else:
                            if count == 3:
                                new_active.add((x, y, z, w))

                                min_x, max_x = day17_update_bounds(
                                    min_x, max_x, x)
                                min_y, max_y = day17_update_bounds(
                                    min_y, max_y, y)
                                min_z, max_z = day17_update_bounds(
                                    min_z, max_z, z)
                                min_w, max_w = day17_update_bounds(
                                    min_w, max_w, w)

        active = new_active

    return len(active)

def day17_1(data):
    # data = read_input(2020, 1701)
    return day17_boot(data, False)

def day17_2(data):
    # data = read_input(2020, 1701)
    return day17_boot(data, True)


""" DAY 18 """
# Day 18, part 1: 650217205854 (0.249 secs)
# Day 18, part 2: 20394514442037 (0.147 secs)

def day18_parse(line):
    orig = []
    stack = [orig]
    for c in line:
        if c == "(":
            stack.append([])
        elif c == ")":
            last = stack.pop()
            stack[-1].append(last)
        else:
            c = int(c) if c.isdigit() else c
            stack[-1].append(c)
    return orig

def day18_eval(parsed, least_priority_op):
    if len(parsed) == 1:
        if isinstance(parsed[0], list):
            return day18_eval(parsed[0], least_priority_op)
        else:
            return parsed[0]
    else:
        last_op = day18_find_op(parsed, least_priority_op)
        left, op, right = parsed[:last_op], parsed[last_op], parsed[last_op + 1:]
        l = day18_eval(left, least_priority_op)
        r = day18_eval(right, least_priority_op)
        if op == "+":
            return l + r
        elif op == "*":
            return l * r
        else:
            assert False
    raise ValueError

def day18_find_op(expr, op):
    for i, c in enumerate(expr):
        if c == op:
            return i
    return len(expr) - 2

def day18_solve(data, least_priority_op=None):
    acc = 0
    for line in data:
        line = line.replace(" ", "")

        parsed = day18_parse(line)
        total = day18_eval(parsed, least_priority_op)
        acc += total

    return acc

def day18_1(data):
    # data = read_input(2020, 1801)
    return day18_solve(data)

def day18_2(data):
    # data = read_input(2020, 1801)
    return day18_solve(data, "*")


""" DAY 19 """
# Day 19, part 1: 213 (0.352 secs)
# Day 19, part 2: 325 (0.323 secs)

def day19_process(rules, pattern, line):
    if len(pattern) > len(line):
        return False

    for i, sub_p in enumerate(pattern):
        if not pattern[i].isdigit():
            if pattern[i] != line[i]:
                return False
        else:
            for rule in rules[sub_p]:
                if day19_process(rules, rule + pattern[i + 1:], line[i:]):
                    return True
            return False
    return len(pattern) == len(line)

def day19_solve(data, override):
    rules = {}
    validating = False
    count = 0
    for line in data:
        line = line.rstrip()
        if line == "":
            for r in override:
                rules[r] = override[r]
            validating = True
            continue

        if validating:
            valid = day19_process(rules, ["0"], line)
            if valid:
                count += 1
        else:
            # 99: "a"
            # 108: 118 99 | 96 36
            line = line.replace("\"", "")
            parts = line.split(": ")
            if "|" in parts[1]:
                parts[1] = parts[1].split(" | ")
            else:
                parts[1] = [parts[1]]
            parts[1] = [part.split(" ") for part in parts[1]]

            rules[parts[0]] = parts[1]
    return count

def day19_1(data):
    # data = read_input(2020, 1901)
    return day19_solve(data, {})

def day19_2(data):
    # data = read_input(2020, 1901)
    override = {
        "8": [["42"], ["42", "8"]],
        "11": [["42", "31"], ["42", "11", "31"]]
    }
    return day19_solve(data, override)


""" DAY 20 """
# Day 20, part 1: 14129524957217 (0.969 secs)
# Day 20, part 2: 1649 (0.511 secs)

def day20_positions(tile):
    return [
        tile,
        day20_flip_h(tile),
        day20_flip_v(tile),

        day20_rotate(tile),
        day20_rotate(day20_rotate(tile)),
        day20_rotate(day20_rotate(day20_rotate(tile))),

        day20_rotate(day20_flip_h(tile)),
        day20_rotate(day20_rotate(
            day20_rotate(day20_flip_h(tile)))),
    ]

def day20_parse(data):
    last_id = 0
    tiles = {}
    tile = []
    for line in data:
        # Tile 3769:
        # .#.#.#.#..
        if "Tile" in line:
            last_id = line.split(" ")[1][:-1]
        elif line:
            tile.append(line)
        else:
            tile = (tile, {"N": "N", "S": "S", "E": "E", "W": "W"})
            tiles[last_id] = day20_positions(tile)
            tile = []
    return tiles

def day20_flip_h(tile):
    tile, o = tile
    n_tile = [["_" for _ in range(len(tile[0]))] for _ in range(len(tile))]
    C = len(tile[0])
    for r in range(len(tile)):
        for c in range(len(tile[0])):
            n_tile[r][C - 1 - c] = tile[r][c]
    return (n_tile,
            {"N": o["N"],
             "S": o["S"],
             "E": o["W"],
             "W": o["E"]
             })

def day20_flip_v(tile):
    tile, o = tile
    n_tile = [["_" for _ in range(len(tile[0]))] for _ in range(len(tile))]
    R = len(tile)
    for r in range(len(tile)):
        for c in range(len(tile[0])):
            n_tile[R - 1 - r][c] = tile[r][c]
    return (n_tile,
            {"N": o["S"],
             "S": o["N"],
             "E": o["E"],
             "W": o["W"]
             })

def day20_rotate(tile):
    tile, o = tile
    n_tile = [["_" for _ in range(len(tile[0]))] for _ in range(len(tile))]
    R = len(tile)
    for r in range(len(tile)):
        for c in range(len(tile[0])):
            # Rotate counter-clockwise: r,c = -c, r
            # Add R-1 to move to first quadrant again
            n_tile[- c + (R - 1)][r] = tile[r][c]
    return (n_tile,
            {"N": o["E"],
             "S": o["W"],
             "E": o["S"],
             "W": o["N"]
             })

# "S" -> t2 is South of t1
def day20_relative_position(t1, t2):
    R = len(t1)
    C = len(t1[0])
    if all([t1[r][0] == t2[r][C - 1] for r in range(R)]):
        return "W"
    if all([t1[r][C - 1] == t2[r][0] for r in range(R)]):
        return "E"
    if all([t1[0][c] == t2[R - 1][c] for c in range(C)]):
        return "N"
    if all([t1[R - 1][c] == t2[0][c] for c in range(C)]):
        return "S"
    return None

def day20_neighbours(tiles):
    n = {}
    for t_id in tiles:
        tile = tiles[t_id][:1]
        n[t_id] = {}
        for o_t_id in tiles:
            if t_id == o_t_id:
                continue
            other_tile = tiles[o_t_id]
            for t1 in tile:
                for t2 in other_tile:
                    m = day20_relative_position(t1[0], t2[0])
                    if not m is None:
                        n[t_id][m] = o_t_id
                        break
    return n

def day20_print(tile):
    for r in range(len(tile)):
        line = ""
        for c in range(len(tile[0])):
            line += tile[r][c]
        print(line)
    print()

def day20_transform(fixed_left, fixed_top, to_transform, n, tiles):
    curr_pos_left = None
    for k in n[to_transform]:
        if n[to_transform][k] == fixed_left:
            curr_pos_left = k
    curr_pos_top = None
    for k in n[to_transform]:
        if n[to_transform][k] == fixed_top:
            curr_pos_top = k

    tile = tiles[to_transform][0]
    transform = {
        ("N", "W"): tile,
        ("N", "E"): day20_flip_h(tile),
        ("S", "W"): day20_flip_v(tile),

        ("E", "N"): day20_rotate(tile),
        ("S", "E"): day20_rotate(day20_rotate(tile)),
        ("W", "S"): day20_rotate(day20_rotate(day20_rotate(tile))),

        ("W", "N"): day20_rotate(day20_flip_h(tile)),
        ("E", "S"): day20_rotate(day20_rotate(day20_rotate(day20_flip_h(tile)))),

        (None, "E"): day20_flip_h(tile)
                     if "S" in n[to_transform] else  # NOQA
                     day20_rotate(day20_rotate(tile)),  # NOQA

        ("W", None): day20_flip_h(day20_rotate(day20_rotate(day20_rotate(tile))))
                     if "S" in n[to_transform] else  # NOQA
                     day20_rotate(day20_rotate(day20_rotate(tile))),  # NOQA

        ("N", None): day20_flip_h(tile)
                     if "W" in n[to_transform] else  # NOQA
                     tile,  # NOQA

        (None, "W"): day20_flip_v(tile)
                     if "N" in n[to_transform] else  # NOQA
                     tile,  # NOQA

        ("S", None): day20_flip_v(tile)
                     if "E" in n[to_transform] else  # NOQA
                     day20_rotate(day20_rotate(tile)),  # NOQA

        (None, "N"): day20_rotate(day20_flip_h(tile))
                     if "E" in n[to_transform] else  # NOQA
                     day20_rotate(tile),  # NOQA

        (None, "S"): day20_rotate(day20_rotate(day20_rotate(tile)))
                     if "E" in n[to_transform] else  # NOQA
                     day20_rotate(day20_rotate(  # NOQA
                         day20_rotate(day20_flip_h(tile)))),  # NOQA

        ("E", None): day20_rotate(day20_flip_v(tile))
                     if "N" in n[to_transform] else  # NOQA
                     day20_rotate(tile),  # NOQA
    }

    return transform[(curr_pos_top, curr_pos_left)]

def day20_apply(prev_o, mapping):
    n_o = {}
    for k in mapping:
        if mapping[k] in prev_o:
            n_o[k] = prev_o[mapping[k]]
    return n_o

def day20_build(n, tiles):
    corner = None
    n_tiles = len(n)
    for k in n:
        if len(n[k]) == 2 and \
           "S" in n[k].keys() and \
           "E" in n[k].keys():
            corner = k
    size = int(math.sqrt(n_tiles))

    pic_id = [[None for _ in range(size)] for _ in range(size)]
    pic = [["_" for _ in range(size)] for _ in range(size)]
    pic[0][0] = tiles[corner][0][0]

    # 1951    2311    3079
    # 2729    1427    2473
    # 2971    1489    1171
    # FOR SAMPLE ONLY
    # corner = "1951"
    # if corner == 1951:
    #     res = day20_flip_v(tiles[corner][0])
    #     n[corner] = day20_apply(n[corner], res[1])
    #     pic[0][0] = res[0]

    pic_id[0][0] = corner
    visited = set()
    for r in range(size - 1):
        for c in range(size):
            curr = pic_id[r][c]
            if c < size - 1:
                if not (r, c + 1) in visited:
                    # Fill tile East of current
                    visited.add((r, c + 1))
                    right = n[curr]["E"]
                    pic_id[r][c + 1] = right
                    res = day20_transform(
                        curr, pic_id[r - 1][c + 1] if r - 1 >= 0 else None, right, n, tiles)
                    pic[r][c + 1] = res[0]
                    n[right] = day20_apply(n[right], res[1])
            if not (r + 1, c) in visited:
                # Fill tile South of current
                visited.add((r + 1, c))
                bottom = n[curr]["S"]
                res = day20_transform(
                    pic_id[r + 1][c - 1] if c - 1 >= 0 else None, curr, bottom, n, tiles)

                pic_id[r + 1][c] = bottom
                pic[r + 1][c] = res[0]
                n[bottom] = day20_apply(n[bottom], res[1])

    tile_size = len(tiles[corner][0][0]) - 2
    glued_pic = [["_" for _ in range(size * (tile_size))]
                 for _ in range(size * (tile_size))]
    for r in range(len(pic)):
        for c in range(len(pic[0])):
            for r2 in range(1, len(pic[r][c]) - 1):
                for c2 in range(1, len(pic[r][c][0]) - 1):
                    glued_pic[r * tile_size +
                              (r2 - 1)][c * tile_size + (c2 - 1)] = pic[r][c][r2][c2]

    return glued_pic

def day20_find(tile):
    monster = ["                  # ",
               "#    ##    ##    ###",
               " #  #  #  #  #  #   "]
    monster_pos = []
    for r in range(len(monster)):
        for c in range(len(monster[0])):
            if monster[r][c] == "#":
                monster_pos.append((r, c))

    count = 0
    for r in range(len(tile) - (len(monster) - 1)):
        for c in range(len(tile[0]) - (len(monster[0]) - 1)):
            match = True
            for rr, cc in monster_pos:
                if tile[r + rr][c + cc] != "#":
                    match = False
                    break

            if match:
                for rr, cc in monster_pos:
                    tile[r + rr][c + cc] = "O"
                count += 1
    return count > 0

def day20_1(data):
    # data = read_input(2020, 2001)
    tiles = day20_parse(data)
    total = 1
    n = day20_neighbours(tiles)
    for k in n:
        if len(n[k]) == 2:
            total *= int(k)
    return total

def day20_2(data):
    # data = read_input(2020, 2001)
    tiles = day20_parse(data)
    n = day20_neighbours(tiles)
    completed = day20_build(n, tiles)
    tile = (completed, {"N": "N", "S": "S", "E": "E", "W": "W"})

    for config, _ in day20_positions(tile):
        monsters = day20_find(config)
        if monsters:
            count = 0
            for r in range(len(config)):
                for c in range(len(config[0])):
                    if config[r][c] == "#":
                        count += 1
            return count
    raise ValueError


""" DAY 21 """
# Day 21, part 1: 2461 (1.031 secs)
# Day 21, part 2: ltbj,nrfmm,pvhcsn,jxbnb,chpdjkf,jtqt,zzkq,jqnhd (0.907 secs)

def day21_parse(data):
    foods = []
    for line in data:
        # trh fvjkl sbzzf mxmxvkd (contains dairy)
        parts = line.split(" (contains ")
        foods.append((parts[0].split(" "), parts[1][:-1].split(", ")))
    return foods

def day21_extract_info(foods):
    table_i = defaultdict(set)
    counts = defaultdict(lambda: 0)
    for ing, al in foods:
        for i in ing:
            counts[i] += 1
            for a in al:
                table_i[i].add(a)
    return table_i, counts

def day21_solve_match(foods, table_i):
    impossible = set()
    solved = set()
    changed = True
    while changed:
        changed = False
        for ingredient in table_i:
            possibilites = set(table_i[ingredient])
            for allergen in table_i[ingredient]:
                possible = True

                for ing, al in foods:
                    valid = [i2 for i2 in ing if i2 not in impossible]
                    als = set()
                    if ingredient in valid:
                        als.add(allergen)
                    for i2 in valid:
                        if i2 == ingredient:
                            continue
                        for a2 in table_i[i2]:
                            if a2 == allergen:
                                continue
                            als.add(a2)
                    valid = True
                    for al3 in al:
                        if not al3 in als:
                            valid = False
                            break
                    if not valid:
                        possible = False
                        break
                if not possible:
                    possibilites.remove(allergen)
            table_i[ingredient] = possibilites
            if len(possibilites) == 1:
                match_allergen = list(possibilites)[0]
                if (match_allergen, ingredient) not in solved:
                    solved.add((match_allergen, ingredient))
                    changed = True
            if not possibilites:
                impossible.add(ingredient)

    return impossible, solved

def day21_1(data):
    # data = read_input(2020, 2101)
    foods = day21_parse(data)
    table_i, counts = day21_extract_info(foods)

    impossible, _ = day21_solve_match(foods, table_i)
    ans = sum([counts[i] for i in impossible])
    return ans

def day21_2(data):
    # data = read_input(2020, 2101)
    foods = day21_parse(data)
    table_i, _ = day21_extract_info(foods)

    _, solved = day21_solve_match(foods, table_i)
    res = ",".join([i for _, i in sorted(solved)])
    return res


""" DAY 22 """
# Day 22, part 1: 32815 (0.006 secs)
# Day 22, part 2: 30695 (2.181 secs)

def day22_parse(data):
    p1 = True
    cards = [[], []]
    for line in data:
        if "Player 1" in line:
            p1 = True
        elif "Player 2" in line:
            p1 = False
        elif line:
            if p1:
                cards[0].append(int(line))
            else:
                cards[1].append(int(line))
    return cards

def day22_score(p1, p2):
    ans = 0
    p = p1 if p1 else p2
    for i, c in enumerate(reversed(p)):
        ans += c * (i + 1)
    return ans

def day22_play(p1, p2, recursive):
    seen = set()
    while True:
        k = (tuple(p1), tuple(p2))
        if k in seen:
            return True, p1, p2
        seen.add(k)

        p1_c = p1[0]
        p2_c = p2[0]
        p1 = p1[1:]
        p2 = p2[1:]

        if recursive and len(p1) >= p1_c and len(p2) >= p2_c:
            winner_p1, _, _ = day22_play(p1[:p1_c], p2[:p2_c], recursive)
            if winner_p1:
                p1 = p1 + [p1_c, p2_c]
            else:
                p2 = p2 + [p2_c, p1_c]
        else:
            if p1_c > p2_c:
                p1 = p1 + [p1_c, p2_c]
            elif p2_c > p1_c:
                p2 = p2 + [p2_c, p1_c]
            else:
                assert False

        if not p1 or not p2:
            break

    return not p2, p1, p2

def day22_1(data):
    # data = read_input(2020, 2201)
    p1, p2 = day22_parse(data)

    _, p1, p2 = day22_play(p1, p2, False)

    return day22_score(p1, p2)

def day22_2(data):
    # data = read_input(2020, 2201)
    p1, p2 = day22_parse(data)

    _, p1, p2 = day22_play(p1, p2, True)

    return day22_score(p1, p2)


""" DAY 23 """
# Day 23, part 1: 36472598 (0.012 secs)
# Day 23, part 2: 90481418730 (5.123 secs)

class Cup:
    label = 0
    next_ = None
    prev_ = None

def day23_play(rounds, n_cups, cups):
    max_ = max(cups)
    for i in range(max_ + 1, n_cups + 1):
        cups.append(i)
    assert len(cups) == n_cups, len(cups)

    min_ = 1
    max_ = n_cups
    start, mem = day23_create_loop(cups)

    for _ in range(rounds):
        start = day23_round(start, min_, max_, mem)

    return mem

def day23_round(start: Cup, min_, max_, mem):
    after_sel = start
    selected = []
    for _ in range(4):
        after_sel = after_sel.next_
        selected.append(after_sel.label)
    selected = selected[:-1]

    # store pointers to first and last cups of selection
    start_sel = start.next_
    end_sel = after_sel.prev_

    # remove selection from the loop
    start.next_ = after_sel
    after_sel.prev_ = start

    # calculate the destination label
    dest_cup = after_sel
    dest_cup_i = start.label - 1
    if dest_cup_i < min_:
        dest_cup_i = max_
    while dest_cup_i in selected:
        dest_cup_i -= 1
        if dest_cup_i < min_:
            dest_cup_i = max_

    # get the destination cup
    dest_cup = mem[dest_cup_i]

    # insert the selection after the destination
    end_sel.next_ = dest_cup.next_
    dest_cup.next_.prev_ = end_sel

    start_sel.prev_ = dest_cup
    dest_cup.next_ = start_sel

    return start.next_

def day23_get_sequence(start: Cup):
    seen = set()
    l = []
    while start.label not in seen:
        seen.add(start.label)
        l.append(str(start.label))
        start = start.next_
    return l

def day23_create_loop(cups):
    prev_node = Cup()
    prev_node.label = cups[0]
    start = prev_node
    mem = {}
    mem[cups[0]] = start
    for label in cups[1:]:
        curr = Cup()
        curr.label = label
        mem[label] = curr
        prev_node.next_ = curr
        curr.prev_ = prev_node
        prev_node = curr

    # close the loop
    start.prev_ = prev_node
    prev_node.next_ = start

    return start, mem

def day23_1(data):
    # data = read_input(2020, 2301)
    cups = [int(x) for x in data[0]]
    rounds = 100
    n_cups = len(cups)

    mem = day23_play(rounds, n_cups, cups)

    return "".join(day23_get_sequence(mem[1])).replace("1", "")

def day23_2(data):
    # data = read_input(2020, 2301)
    cups = [int(x) for x in data[0]]
    rounds = 10000000
    n_cups = 1000000
    # rounds = 100
    # n_cups = 9

    mem = day23_play(rounds, n_cups, cups)

    return mem[1].next_.label * mem[1].next_.next_.label


""" DAY 24 """
# Day 24, part 1: 351 (0.016 secs)
# Day 24, part 2: 3869 (7.044 secs)

def day24_parse(data):
    tiles = []
    for line in data:
        curr_dir = ""
        curr_tile = []
        for c in list(line):
            curr_dir += c
            if curr_dir in ["e", "se", "sw", "w", "nw", "ne"]:
                curr_tile.append(curr_dir)
                curr_dir = ""

        tiles.append(curr_tile)

    return tiles

def day24_print(tiles_pos, min_x, max_x, min_y, max_y):

    grid = ""
    for y in range(min_y - 1, max_y + 2):
        line = ""
        for x in range(int(min_x - 1), int(max_x + 2)):
            if y % 2 != 0:
                dx = 0.5
            else:
                dx = 0
            pos = x + dx, y
            s = " "
            if tiles_pos[pos]:
                s = WHITE_SQUARE
            else:
                s = "."
            if dx == 0.5:
                line += " " + s
            else:
                line += s + " "
        grid += line + "\n"

    print("=" * 80)
    print()
    print(grid)
    print("=" * 80)
    time.sleep(.2)

def day24_move(dir_):
    if dir_ == "e":
        return 2, 0
    elif dir_ == "se":
        return 1, 1
    elif dir_ == "sw":
        return -1, 1
    elif dir_ == "w":
        return -2, 0
    elif dir_ == "nw":
        return -1, -1
    elif dir_ == "ne":
        return 1, -1
    else:
        assert False
    return None

def day24_flip(tiles_flips):
    tiles = {}
    for flip in tiles_flips:
        x, y = 0, 0
        for dir_ in flip:
            dx, dy = day24_move(dir_)
            x, y = x + dx, y + dy
        pos = (x, y)
        if pos not in tiles:
            tiles[pos] = True
        else:
            tiles[pos] = not tiles[pos]

    return tiles

def day24_new_flip(x, y, tiles_pos):
    count = 0
    edges = set()
    for dir_ in ["e", "se", "sw", "w", "nw", "ne"]:
        dx, dy = day24_move(dir_)
        nx, ny = x + dx, y + dy
        if (nx, ny) in tiles_pos:
            if tiles_pos[(nx, ny)]:
                count += 1
        else:
            edges.add((nx, ny))

    pos = (x, y)
    result = tiles_pos[pos] if pos in tiles_pos else False
    if result and count == 0 or count > 2:
        result = False
    elif not result and count == 2:
        result = True

    return result, edges

def day24_1(data):
    # data = read_input(2020, 2401)
    tiles_flips = day24_parse(data)

    tiles = day24_flip(tiles_flips)

    return sum([1 for x in tiles.values() if x])

def day24_2(data):
    # data = read_input(2020, 2401)
    tiles_flips = day24_parse(data)

    tiles_pos = day24_flip(tiles_flips)

    for _ in range(100):
        n_tiles_pos = {}
        edges = set()
        for t in tiles_pos:
            x, y = t
            new_flip, new_edges = day24_new_flip(x, y, tiles_pos)
            edges |= new_edges

            n_tiles_pos[t] = new_flip
        for x, y in edges:
            new_flip, _ = day24_new_flip(x, y, tiles_pos)
            n_tiles_pos[(x, y)] = new_flip

        tiles_pos = n_tiles_pos

    return sum([1 for x in tiles_pos.values() if x])


""" DAY 25 """
# Day 25, part 1: 16902792 (26.371 secs)

def day25_parse(data):
    return int(data[0]), int(data[1])

def day25_transform(s_n, l_s):
    # Fast implementation based on https://en.wikipedia.org/wiki/Modular_exponentiation
    s = 1
    base = s_n
    e = l_s
    while e > 0:
        if e % 2 == 1:
            s = s * base % 20201227
        e = e >> 1
        base = (base * base) % 20201227

    return s

def day25_get_loop_size(p_k):
    i = 0
    while True:
        curr_p_k = day25_transform(7, i)
        if curr_p_k == p_k:
            return i
        i += 1

def day25_1(data):
    # data = read_input(2020, 2501)
    c_p_k, d_p_k = day25_parse(data)
    v1 = day25_get_loop_size(c_p_k)
    return day25_transform(d_p_k, v1)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2020)
