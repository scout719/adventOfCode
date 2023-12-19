# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict
import os
import sys
from tracemalloc import start

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2023
DAY = 19
EXPECTED_1 = 19114
EXPECTED_2 = -1

""" DAY 19 """

def day19_parse(data: list[str]):
    i = 0
    workflows = {}
    while data[i] != "":
        line = data[i]
        i += 1
        label, rest = line.split("{")
        rest = rest.rstrip("}")
        rules_ = rest.split(",")
        rules = []
        for rule in rules_:
            if ":" in rule:
                cond, name = rule.split(":")
                op = "<" if "<" in cond else ">"
                cond_r, val = cond.split(op)
                val = int(val)
                cond = (cond_r, op, val)
            else:
                cond = None
                name = rule
            rules.append((cond, name))
        workflows[label] = rules

    i += 1
    parts = []
    while i < len(data):
        # {x=787,m=2655,a=1222,s=2876}
        line = data[i]
        i += 1
        line = line.lstrip("{").rstrip("}")
        ratings = line.split(",")
        ratings = {rating.split("=")[0]: int(
            rating.split("=")[1]) for rating in ratings}
        parts.append(ratings)

    return workflows, parts

def day19_solve(x, part2):
    workflow, parts = x
    ans = 0
    for part in parts:
        curr_name = "in"
        while curr_name not in ["A", "R"]:
            rules = workflow[curr_name]
            for cond, name in rules:
                if not cond:
                    curr_name = name
                    break
                else:
                    rat, op, val = cond
                    rat_val = part[rat]
                    if op == ">":
                        if rat_val > val:
                            curr_name = name
                            break
                    else:
                        assert op == "<"
                        if rat_val < val:
                            curr_name = name
                            break

        if curr_name == "A":
            ans += sum(part.values())
        elif curr_name == "R":
            # reject
            pass

    return ans

def day19_1(data):
    x = day19_parse(data)
    return day19_solve(x, False)

def day19_2(data: list[str]):
    x = day19_parse(data)
    return day19_solve(x, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
