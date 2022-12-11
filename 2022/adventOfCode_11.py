# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
import functools
import os
import sys
from collections import Counter

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main, day_with_validation  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2022
DAY = 11
EXPECTED_1 = 10605
EXPECTED_2 = 2713310158


""" DAY 11 """

def day11_parse(data):
    monkeys = {}
    i = 0
    while i < len(data):
        line = data[i]
        i += 1
        if not line:
            continue
        # Monkey 7:
        curr_monkey = int(line.split("Monkey ")[1].split(":")[0])
        line = data[i]
        i += 1
        #   Starting items: 95, 65, 58, 76
        items = line.split("Starting items: ")[1].split(", ")
        items = [int(it) for it in items]
        line = data[i]
        i += 1
        #   Operation: new = old + 5
        op, amt = line.split("old ")[1].split(" ")
        line = data[i]
        i += 1
        # Test: divisible by 7
        divisor = int(line.split("divisible by ")[1])
        line = data[i]
        i += 1
        #     If true: throw to monkey 3
        if_true = int(line.split("monkey ")[1])
        line = data[i]
        i += 1
        #     If true: throw to monkey 3
        if_false = int(line.split("monkey ")[1])
        monkeys[curr_monkey] = (items, (op, amt), divisor, (if_true, if_false))

    return monkeys

def day11_turn(monkeys, c_m, c, divide, lcm):
    m = monkeys[c_m]
    m_i, op_, d, out = m
    op, amt = op_
    tr, fa = out
    while m_i:
        c[c_m] += 1
        curr = m_i.pop(0)
        v = 0
        if amt == "old":
            v = curr
        else:
            v = int(amt)
        if op == "*":
            curr *= v
        elif op == "+":
            curr += v
        elif op == "-":
            curr -= v
        else:
            assert False
        if divide:
            curr //= 3
        else:
            curr %= lcm
        if curr % d == 0:
            monkeys[tr][0].append(curr)
        else:
            monkeys[fa][0].append(curr)

# which mokey will have this item with which worry
# and through which monkeys did it pass through
def day11_turn_v2(monkeys, curr_monkey, curr_item, lcm):
    counter = Counter()
    while True:
        counter[curr_monkey] += 1
        _, op, d, out = monkeys[curr_monkey]
        op, amt = op
        if_true, if_false = out
        value = 0
        if amt == "old":
            value = curr_item
        else:
            value = int(amt)
        if op == "*":
            curr_item *= value
        elif op == "+":
            curr_item += value
        elif op == "-":
            curr_item -= value
        else:
            assert False
        curr_item %= lcm
        if curr_item % d == 0:
            if if_true < curr_monkey:
                return (counter, if_true, curr_item)
            else:
                curr_monkey = if_true
        else:
            if if_false < curr_monkey:
                return (counter, if_false, curr_item)
            else:
                curr_monkey = if_false

def day11_1(data):
    monkeys = day11_parse(data)
    counter = Counter()
    for _ in range(20):
        for curr_monkey in range(len(monkeys)):
            day11_turn(monkeys, curr_monkey, counter, True, 0)

    busiest_monkeys = sorted(counter.values())[-2:]
    return busiest_monkeys[0] * busiest_monkeys[1]

def day11_2(data):
    # Original solution 🤦🏻‍♂️
    # monkeys = day11_parse(data)
    # items = {}
    # i = 0
    # for curr_monkey, monkey in monkeys.items():
    #     monkey_items = monkey[0]
    #     for item in monkey_items:
    #         items[i] = (item, curr_monkey)
    #         i += 1

    # counter = Counter()
    # lcm = functools.reduce(
    #     lambda x, y: x * y, (d for _, _, d, _ in monkeys.values()))
    # for _ in range(10000):
    #     items2 = {}
    #     for item in items.keys():
    #         curr_worry, curr_monkey = items[item]
    #         counter2, next_monkey, next_worry = day11_turn2(
    #             monkeys, curr_monkey, curr_worry, lcm)
    #         items2[item] = (next_worry, next_monkey)
    #         for curr_monkey in counter2:
    #             counter[curr_monkey] += counter2[curr_monkey]
    #     items = items2
    # busiest_monkeys = sorted(counter.values())[-2:]
    # return busiest_monkeys[0] * busiest_monkeys[1]

    monkeys = day11_parse(data)
    lcm = functools.reduce(
        lambda x, y: x * y, (divisor for _, _, divisor, _ in monkeys.values()))
    counter = Counter()
    for _ in range(10000):
        for curr_monkey in range(len(monkeys)):
            day11_turn(monkeys, curr_monkey, counter, False, lcm)

    busiest_monkeys = sorted(counter.values())[-2:]
    return busiest_monkeys[0] * busiest_monkeys[1]


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
