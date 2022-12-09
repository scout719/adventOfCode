# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-enumerate
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main, day_with_validation  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

YEAR = 2022
DAY = 9
EXPECTED_1 = 88
EXPECTED_2 = 36


""" DAY 9 """

def day9_parse(data):
    motions = []
    for line in data:
        direction, steps = line.split(" ")
        steps = int(steps)
        motions.append((direction, steps))
    return motions

def day9_move_head(head, direction) -> tuple:
    if direction == "U":
        head = (head[0] - 1, head[1])
    elif direction == "D":
        head = (head[0] + 1, head[1])
    elif direction == "R":
        head = (head[0], head[1] + 1)
    elif direction == "L":
        head = (head[0], head[1] - 1)

    return head

def day9_get_delta(a, b):
    return 0 if a == b else (a - b) / abs(a - b)

def day9_follow_up(rope):
    i = 0
    while i < len(rope) - 1:
        head = rope[i]
        tail = rope[i + 1]

        dr = day9_get_delta(head[0], tail[0])
        dc = day9_get_delta(head[1], tail[1])
        # Moved UP or DOWN
        if abs(head[0] - tail[0]) == 2:
            tail = (tail[0] + dr, tail[1] + dc)
        # Moved RIGHT or LEFT
        elif abs(head[1] - tail[1]) == 2:
            tail = (tail[0] + dr, tail[1] + dc)
        rope[i] = head
        rope[i + 1] = tail
        i += 1
    return rope

def day9_solve(motions, size):
    rope = [(0, 0) for _ in range(size)]
    visited = set([rope[-1]])
    for direction, steps in motions:
        for _ in range(steps):
            head = rope[0]
            head = day9_move_head(head, direction)
            rope[0] = head
            rope = day9_follow_up(rope)

            visited.add(rope[-1])

    return len(visited)

def day9_1(data):
    motions = day9_parse(data)
    return day9_solve(motions, 2)


def day9_2(data):
    motions = day9_parse(data)
    # 2128
    return day9_solve(motions, 10)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
