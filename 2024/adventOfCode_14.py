# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import WHITE_SQUARE, main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2024
DAY = 14
EXPECTED_1 = None
EXPECTED_2 = None

def day14_parse(data: list[str]):
    robots = []
    for line in data:
        pos, vel = line.split(" ")
        c, r = pos.strip("p=").split(",")
        vc, vr = vel.strip("v=").split(",")
        robots.append((int(r), int(c), int(vr), int(vc)))
    return robots

def day14_show(R, C, robots):
    robots = [(r, c) for r, c, _, _ in robots]
    print("#" * 100)
    for r in range(R):
        line = ""
        for c in range(C):
            if (r, c) in robots:
                line += WHITE_SQUARE
            else:
                line += " "
        print(line)
    print()
    print("#" * 100)

def day14_solve(data, part2):
    data = day14_parse(data)
    robots = data
    R, C = 103, 101
    if len(data) < 50:
        R, C = 7, 11
    for t in range(100000 if part2 else 100):
        # new_robots = []
        # for r, c, vr, vc in robots:
        #     new_robots.append(((r + vr) % R, (c + vc) % C, vr, vc))
        robots = [((r + vr) % R, (c + vc) % C, vr, vc)
                  for r, c, vr, vc in robots]
        occupied = {(r, c) for r, c, _, _ in robots}
        for r in range(R):
            seq = 0
            max_seq = 0
            for c in range(C):
                if (r, c) in occupied:
                    seq += 1
                else:
                    max_seq = max(max_seq, seq)
                    seq = 0
            if max_seq > 30:
                day14_show(R, C, robots)
                return t + 1

    top_left = [(r, c) for r, c, _, _ in robots if r < R // 2 and c < C // 2]
    top_right = [(r, c) for r, c, _, _ in robots if r < R // 2 and c > C // 2]
    bottom_left = [(r, c)
                   for r, c, _, _ in robots if r > R // 2 and c < C // 2]
    bottom_right = [(r, c)
                    for r, c, _, _ in robots if r > R // 2 and c > C // 2]
    return len(top_left) * len(top_right) * len(bottom_left) * len(bottom_right)

def day14_1(data):
    return day14_solve(data, False)

def day14_2(data):
    # 28007972338388 low
    # 91586853503821 high
    # 75596115797987 wrong
    # 75631907391616 wrong
    # 60439165206075 wrong
    return day14_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
