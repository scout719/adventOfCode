# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import decimal
from heapq import heappop, heappush
import os
import sys


FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2024
DAY = 13
EXPECTED_1 = 480
EXPECTED_2 = None

def day13_parse(data: list[str]):
    # Button A: X+94, Y+34
    # Button B: X+22, Y+67
    # Prize: X=8400, Y=5400

    machines = []
    i = 0
    rep = ["Button A: ", "Button B: ", "Prize: ", "X+", "Y+", "X=", "Y="]
    new_data = []
    for line in data:
        for r in rep:
            line = line.replace(r, "")
        new_data.append(line)
    data = new_data
    while i < len(data):
        ax, ay = data[i].split(", ")
        bx, by = data[i + 1].split(", ")
        px, py = data[i + 2].split(", ")
        machines.append((decimal.Decimal(ax), decimal.Decimal(ay), decimal.Decimal(
            bx), decimal.Decimal(by), decimal.Decimal(px), decimal.Decimal(py)))
        i += 4
    return machines

def day13_cost(ax, ay, bx, by, px, py):
    q = [(0, px + py, 0, 0)]
    seen = set()
    while q:
        cost, dist, x, y = heappop(q)
        if x > px or y > py:
            continue
        if x == px and y == py:
            return cost
        if (x, y) in seen:
            continue
        seen.add((x, y))
        heappush(q, (cost + 3, dist - ax - ay, x + ax, y + ay))
        heappush(q, (cost + 1, dist - bx - by, x + bx, y + by))
    return None

def day13_solve(data, part2):
    data = day13_parse(data)
    decimal.setcontext(decimal.Context(prec=2000))
    machines = data
    ans = 0
    for ax, ay, bx, by, px, py in machines:
        if part2:
            px, py = 10000000000000 + px, 10000000000000 + py

        # k*ax + m * bx = px
        # k*ay + m * by = py
        # Consider only 'integer' solutions
        m = ((py / ay) - (px / ax)) / ((by / ay) - (bx / ax))
        margin_m = abs(round(m) - m)
        margin = 1e-100
        if margin_m < margin:
            k = (px / ax) - round(m) * (bx / ax)
            margin_k = abs(round(k) - k)
            if margin_k < margin:
                ans += 3 * round(k) + round(m)
        # Part 1 solution
        # cost = day13_cost(ax, ay, bx, by, px, py)
        # if cost:
        #     ans += cost
    return ans

def day13_1(data):
    return day13_solve(data, False)

def day13_2(data):
    # 28007972338388 low
    # 91586853503821 high
    # 75596115797987 wrong
    # 75631907391616 wrong
    # 60439165206075 wrong
    return day13_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
