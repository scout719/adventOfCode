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


""" DAY 10 """

def day10_1(data):
    # data = read_input(2020, 1001)
    data = [int(x) for x in data]
    data = sorted(data)
    q = [(0, 0, data, [])]
    final_chain = []
    while q:
        _, curr, remaining, chain = heappop(q)
        a = curr

        if len(remaining) == 0:
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
            #print("Processing: " + line + " Mask: " + mask)
            #print("Addresses: " + str([int(a,2) for a in q]))
            for a in q:
                addr = int(a, 2)
                memory[addr] = value
    res = 0
    for addr in memory:
        res += memory[addr]
    return res


""" DAY 15 """

def parse_inst(line):
    # <3 char inst> <signal><value>
    val = int(line[5:])
    return [line[:3], -val if line[4] == '-' else val]

def parse_program(data):
    return [parse_inst(line) for line in data]

def comp_exec(inst, pc, value, acc):
    if inst == "nop":
        return (pc + 1, acc)
    elif inst == "acc":
        return (pc + 1, acc + value)
    elif inst == "jmp":
        return (pc + value, acc)
    raise NotImplementedError

def day15_solve(data, target):
    ns = [int(d) for d in data[0].split(",")]
    ts = 1
    mem = {}
    last = 0
    for i, _ in enumerate(ns):
        mem[ns[i]] = [ts]
        last = ns[i]
        ts += 1

    while ts <= target:
        if last in mem:
            if len(mem[last]) == 1:
                last = 0
            else:
                last = mem[last][1] - mem[last][0]
        else:
            last = 0
        if last in mem:
            if len(mem[last]) == 1:
                mem[last].append(ts)
            else:
                mem[last][0] = mem[last][1]
                mem[last][1] = ts
        else:
            mem[last] = [ts]
        ts += 1
    return last

def day15_1(data):
    # data = read_input(2020, 1501)
    return day15_solve(data, 2020)

def day15_2(data):
    # data = read_input(2020, 1501)
    return day15_solve(data, 30000000)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2020)
