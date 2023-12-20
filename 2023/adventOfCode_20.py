# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict
from email.policy import default
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
    for m, (typ, _) in modules.items():
        if typ == "&":
            con[m] = {}
    for m, (typ, l) in modules.items():
        for k, v in con.items():
            if k in l:
                v[m] = 0
    for t in range(T):
        _, next_ = modules["broadcaster"]
        q = [("broadcaster", m, 0) for m in next_]
        low += 1
        print(t)
        while q:
            n_q = []
            for src, m_n, pulse in q:
                if pulse == 1:
                    high += 1
                else:
                    assert pulse == 0
                    if part2 and m_n == "rx":
                        return t+1
                    low += 1
                if m_n not in modules:
                    # ignore
                    continue
                typ, l = modules[m_n]
                if typ == "%":
                    if pulse == 1:
                        # ignore high
                        pass
                    else:
                        ff[m_n] = not ff[m_n]
                        if ff[m_n]:
                            n_p = 1
                            # high += 1
                        else:
                            n_p = 0
                            # low += 1
                        for n in l:
                            n_q.append((m_n, n, n_p))
                elif typ == "&":
                    con[m_n][src] = pulse
                    if all(v == 1 for v in con[m_n].values()):
                        n_p = 0
                        # low += 1
                    else:
                        n_p = 1
                        # high += 1

                    for n in l:
                        n_q.append((m_n, n, n_p))
                else:
                    assert False
            q = n_q

    return low * high

def day20_1(data):
    x = day20_parse(data)
    # low 281157474
    return day20_solve(x, False)

def day20_2(data: list[str]):
    x = day20_parse(data)
    return day20_solve(x, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
