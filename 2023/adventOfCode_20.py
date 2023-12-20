# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict
from copy import deepcopy
from math import lcm
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import day_with_validation  # NOQA: E402
from common.utils import main  # NOQA: E402

YEAR = 2023
DAY = 20
EXPECTED_1 = 11687500
EXPECTED_2 = None

""" DAY 20 """

def day20_parse(data: list[str]):
    modules = {}
    for line in data:
        module, dest = line.split(" -> ")
        if module == "broadcaster":
            module_type, module_name = (None, module)
        else:
            module_type, module_name = (module[0], module[1:])
        dest = dest.split(", ")
        modules[module_name] = (module_type, dest)
    return modules

def day20_solve(x, part2):
    modules = x
    high = 0
    low = 0
    T = 1000 if not part2 else int(1e10)
    ff = defaultdict(bool)
    con = {}
    for m, (typ, dest) in modules.items():
        if typ == "&":
            con[m] = {}
    for m, (typ, dest) in modules.items():
        for k, mem in con.items():
            if k in dest:
                mem[m] = 0
    for t in range(T):
        _, start = modules["broadcaster"]
        q = [("broadcaster", module, 0) for module in start]
        low += 1
        while q:
            new_q = []
            for src, module, pulse in q:
                if pulse == 1:
                    high += 1
                else:
                    assert pulse == 0
                    if part2 and module == "rx":
                        return t + 1
                    low += 1
                if module not in modules:
                    # ignore
                    continue
                typ, dest = modules[module]
                if typ == "%":
                    if pulse == 1:
                        # ignore high
                        pass
                    else:
                        ff[module] = not ff[module]
                        if ff[module]:
                            new_pulse = 1
                        else:
                            new_pulse = 0
                        for dest_module in dest:
                            new_q.append((module, dest_module, new_pulse))
                elif typ == "&":
                    con[module][src] = pulse
                    if all(last_pulse == 1 for last_pulse in con[module].values()):
                        new_pulse = 0
                    else:
                        new_pulse = 1

                    for dest_module in dest:
                        new_q.append((module, dest_module, new_pulse))
                else:
                    assert False
            q = new_q

    return low * high

def day20_1(data):
    x = day20_parse(data)
    # low 281157474
    return day20_solve(x, False)

def day20_partial(modules, counters, target_module):
    modules = deepcopy(modules)
    # Remove other counters
    for m in counters:
        if m != target_module:
            del modules[m]

    return day20_solve(modules, True)

def day20_2(data: list[str]):
    modules = day20_parse(data)
    # find aggregator of rx
    aggr = None
    for m, (_, l) in modules.items():
        if "rx" in l:
            assert not aggr
            aggr = m
    assert aggr

    # Get all counters
    counters = []
    for m, (_, l) in modules.items():
        if aggr in l:
            counters.append(m)

    ans = []
    for c in counters:
        ans.append(day20_partial(modules, counters, c))
    return lcm(*ans)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
