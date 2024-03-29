# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict
from copy import deepcopy
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2023
DAY = 19
EXPECTED_1 = 19114
EXPECTED_2 = 167409079868000

""" DAY 19 """

def day19_parse(data: list[str]):
    i = 0
    workflows: dict[str, list[tuple[None | tuple[str, str, int], str]]] = {}
    while data[i] != "":
        line = data[i]
        i += 1
        label, rest = line.split("{")
        rest = rest.rstrip("}")
        rules_ = rest.split(",")
        rules: list[tuple[None | tuple[str, str, int], str]] = []
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
    parts: list[dict[str, int]] = []
    while i < len(data):
        # {x=787,m=2655,a=1222,s=2876}
        line = data[i]
        i += 1
        line = line.lstrip("{").rstrip("}")
        ratings = line.split(",")
        ratings = {
            rating.split("=")[0]: int(rating.split("=")[1])
            for rating in ratings}
        parts.append(ratings)

    return workflows, parts

def day19_1(data):
    workflow, parts = day19_parse(data)
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

def day19_2(data: list[str]):
    workflow, _ = day19_parse(data)
    res: dict[str, list[dict[str, tuple[int, int]]]] = defaultdict(list)
    res["in"] = [{
        "x": (1, 4001),
        "m": (1, 4001),
        "a": (1, 4001),
        "s": (1, 4001),
    }]
    q = ["in"]
    while q:
        curr = q.pop()

        if curr in ["R", "A"]:
            continue

        states = res[curr]

        rules = workflow[curr]
        for cond, name in rules:
            q.append(name)
            if not cond:
                res[name] += deepcopy(states)
            else:
                rating, op, val = cond

                if op == ">":
                    left: tuple[int, int] = (0, 0)
                    right: tuple[int, int] = (0, 0)
                    for i, st in enumerate(states):
                        r_start, r_end = st[rating]
                        if r_end <= val:
                            left = (r_start, r_end)
                        elif r_start > val:
                            right = (r_start, r_end)
                        else:
                            assert r_start < val <= r_end
                            left = (r_start, val + 1)
                            if val < r_end - 1:
                                right = (val + 1, r_end)
                        n_st = deepcopy(st)
                        n_st[rating] = right
                        states[i][rating] = left
                        res[name].append(n_st)
                else:
                    assert op == "<"
                    left: tuple[int, int] = (0, 0)
                    right: tuple[int, int] = (0, 0)
                    for i, st in enumerate(states):
                        r_start, r_end = st[rating]
                        if r_end <= val:
                            left = (r_start, r_end)
                        elif r_start > val:
                            right = (r_start, r_end)
                        else:
                            assert r_start < val <= r_end
                            left = (r_start, val)
                            if val < r_end - 1:
                                right = (val, r_end)
                        n_st = deepcopy(st)
                        n_st[rating] = left
                        states[i][rating] = right
                        res[name].append(n_st)
    ans = 0
    for st in res["A"]:
        x_min, x_max = st["x"]
        m_min, m_max = st["m"]
        a_min, a_max = st["a"]
        s_min, s_max = st["s"]
        ans += (x_max - x_min) * (m_max - m_min) * \
            (a_max - a_min) * (s_max - s_min)
    return ans


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
