# -*- coding: utf-8 -*-
import os
import re
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
# pylint: disable=wrong-import-position
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402

YEAR = 2016
DAY = 21
EXPECTED_1 = "decab"
EXPECTED_2 = None

def day21_parse(data: list[str]):
    return data

def day21_solve(data, part2):
    data = day21_parse(data)
    password = list("abcdefgh")

    if part2:
        password = list("fbgdceah")
        data = list(reversed(data))

    if len(data) < 20:
        password = list("abcde")

    for line in data:
        res = re.match(r"swap position (\d+) with position (\d+)", line)
        if res is not None:
            a, b = [int(g) for g in res.groups()]
            password[a], password[b] = password[b], password[a]
        res = re.match(r"swap letter ([a-z]) with letter ([a-z])", line)
        if res is not None:
            a, b = res.groups()
            password = [a if c == b else b if c == a else c for c in password]
        res = re.match(r"rotate (left|right) (\d+) steps?", line)
        if res is not None:
            direction, steps = res.groups()
            steps = int(steps)
            delta = -1 if direction == "left" else 1
            if part2:
                delta *= -1
            new_password = [c for c in password]
            for i, c in enumerate(password):
                new_password[(i + delta * steps) % len(password)] = c
            password = new_password
        res = re.match(r"rotate based on position of letter ([a-z])", line)
        if res is not None:
            if part2:
                for steps in range(10):
                    # unrotate
                    tmp_password = [c for c in password]
                    for i, c in enumerate(password):
                        tmp_password[(i + (-1 * steps)) % len(password)] = c

                    letter = res.groups()[0]
                    idx = tmp_password.index(letter)
                    delta = 1
                    steps = 1 + idx + (1 if idx >= 4 else 0)
                    new_password2 = [c for c in tmp_password]
                    for i, c in enumerate(tmp_password):
                        new_password2[(i + delta * steps) %
                                      len(tmp_password)] = c
                    if "".join(new_password2) == "".join(password):
                        password = tmp_password
                        break
            else:
                letter = res.groups()[0]
                idx = password.index(letter)
                delta = 1
                steps = 1 + idx + (1 if idx >= 4 else 0)
                new_password = [c for c in password]
                for i, c in enumerate(password):
                    new_password[(i + delta * steps) % len(password)] = c
                password = new_password
        res = re.match(r"reverse positions (\d+) through (\d+)", line)
        if res is not None:
            a, b = [int(g) for g in res.groups()]
            password = password[:a] + \
                list(reversed(password[a:b + 1])) + password[b + 1:]
        res = re.match(r"move position (\d+) to position (\d+)", line)
        if res is not None:
            a, b = [int(g) for g in res.groups()]
            if part2:
                a, b = b, a
            c = password[a]
            password.remove(c)
            password.insert(b, c)
    return "".join(password)

def day21_1(data):
    return day21_solve(data, False)

def day21_2(data):
    return day21_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
