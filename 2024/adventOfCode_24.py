# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from collections import defaultdict, deque
from copy import deepcopy
import functools
from itertools import permutations
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import main  # NOQA: E402
from common.utils import day_with_validation  # NOQA: E402


YEAR = 2024
DAY = 24
EXPECTED_1 = None
EXPECTED_2 = "z00,z01,z02,z05"

def day24_parse(data: list[str]):
    wires, gates_str = "\n".join(data).split("\n\n")
    wires = [w.split(": ") for w in wires.split("\n")]
    wires = {w: bool(int(v)) for w, v in wires}

    gates = set()
    for gate in gates_str.split("\n"):
        w1, op, w2, _, w3 = gate.split(" ")
        gates.add((w1, op, w2, w3))
    return wires, gates

def day24_get_value(wires, s):
    ans = 0
    for w in wires:
        if not w.startswith(s) or not wires[w]:
            continue

        bit = int(w.strip(s))
        v = 1
        while bit > 0:
            v = v << 1
            bit -= 1
        ans += v
    return ans

def day24_execute(wires, gates):
    OPS = {
        "AND": lambda a, b: a & b,
        "OR": lambda a, b: a | b,
        "XOR": lambda a, b: a ^ b,
    }
    wires_gates = defaultdict(list)
    for gate in gates:
        w1, _, w2, _ = gate
        wires_gates[w1].append(gate)
        wires_gates[w2].append(gate)

    ready = set()
    for wire in wires:
        for gate in wires_gates[wire]:
            w1, _, w2, _ = gate
            if w1 in wires and w2 in wires:
                ready.add(gate)

    q = deque(ready)
    seen = set()
    while q:
        gate = q.popleft()
        w1, op, w2, w3 = gate
        assert w1 in wires and w2 in wires
        if gate in seen:
            return None
        seen.add(gate)

        if w3 in wires:
            return None

        assert op in OPS
        wires[w3] = OPS[op](wires[w1], wires[w2])

        for gate2 in wires_gates[w3]:
            a, _, b, _ = gate2
            if a in wires and b in wires:
                q.append(gate2)

    return seen

@functools.cache
def day24_perms2(used_outs, outs, n):
    return list(day24_perms2_inner(used_outs, outs, n))

def day24_perms2_inner(used_outs, outs, n):
    perms = day24_perms(used_outs, outs)
    if n == 1:
        yield from [{p} for p in perms]
    else:
        for o1, o2 in perms:
            perms2 = day24_perms2(used_outs, outs, n - 1)
            for perm in perms2:
                if all(o1 not in p and o2 not in p for p in perm):
                    yield {(o1, o2)} | perm

def day24_perms(used_outs, outs):
    for o1 in outs:
        for o2 in used_outs:
            if o1 < o2:
                yield (o1, o2)

def day24_solve(data, part2):
    data = day24_parse(data)
    wires, gates = data

    if not part2:
        _ = day24_execute(wires, gates)
        ans = day24_get_value(wires, "z")
        return ans

    targetOp = (lambda a, b: a & b) if len(
        wires) < 50 else (lambda a, b: a + b)

    original_gates = deepcopy(gates)
    original_wires = deepcopy(wires)
    max_b = int(sorted(wires)[-1].strip("y"))
    b = 0
    swapped = set()
    outs = {w3 for _, _, _, w3 in gates}
    while b <= max_b:
        print(b)
        new_wires = {f"x{i:02d}": True for i in range(b + 1)}
        new_wires["y00"] = False
        i = 0
        while i < b:
            new_wires[f"y{i:02d}"] = True
            i += 1
        b += 1
        # new_wires = deepcopy(original_wires)
        new_wires_original = deepcopy(new_wires)
        used = day24_execute(new_wires, gates)
        assert used is not None
        used_outs = {w3 for _, _, _, w3 in used}

        x, y, z = day24_get_value(new_wires, "x"), day24_get_value(
            new_wires, "y"), day24_get_value(new_wires, "z")
        if z == targetOp(x, y):
            continue
        found = False
        # print(x, y, z, targetOp(x, y))
        n_swap = 1
        while n_swap <= 4:
            assert len(swapped) // 2 + n_swap <= 4

            print(f"generating {n_swap}")
            # swaps = {p for p in permutations(
            #     outs, n_swap * 2) if any(o in p for o in used_outs)}
            swaps = day24_perms2(tuple(sorted(used_outs - swapped)),
                                 tuple(sorted(outs - swapped)), n_swap)
            print(f"done {len(swaps)}")
            # print(list(day24_perms(tuple(used_outs), tuple(outs))))
            # print(list(day24_perms2(tuple(used_outs), tuple(outs), 2)))
            # print(list(day24_perms2(tuple(used_outs), tuple(outs), 1)))
            print(list(p for p in swaps if any(
                o1 == "z00" or o2 == "z00" for o1, o2 in p)))
            # assert False
            for p in swaps:
                # print(p)
                to_swap = []
                for o_a, o_b in p:
                    i = 0
                    gate_a = None
                    gate_b = None
                    for gate in gates:
                        _, _, _, w3 = gate
                        if w3 == o_a:
                            assert gate_a is None
                            gate_a = gate

                        if w3 == o_b:
                            assert gate_b is None
                            gate_b = gate

                    assert gate_a is not None and gate_b is not None
                    to_swap.append((gate_a, gate_b))
                # print(to_swap)
                new_gates = deepcopy(gates)
                for gate_a, gate_b in to_swap:
                    w1_a, op_a, w2_a, w3_a = gate_a
                    w1_b, op_b, w2_b, w3_b = gate_b
                    new_gates.remove(gate_a)
                    new_gates.remove(gate_b)
                    new_gates.add((w1_a, op_a, w2_a, w3_b))
                    new_gates.add((w1_b, op_b, w2_b, w3_a))
                new_wires = deepcopy(new_wires_original)
                # print("executing")
                res = day24_execute(new_wires, new_gates)
                # print("done")
                x, y, z = day24_get_value(new_wires, "x"), day24_get_value(
                    new_wires, "y"), day24_get_value(new_wires, "z")
                if res is not None and z == targetOp(x, y):
                    new_wires = deepcopy(original_wires)
                    res = day24_execute(new_wires, new_gates)
                    # print("done")
                    x, y, z = day24_get_value(new_wires, "x"), day24_get_value(
                        new_wires, "y"), day24_get_value(new_wires, "z")
                    if not (res is not None and z == targetOp(x, y)):
                        continue

                    gates = new_gates

                    for gate_a, gate_b in to_swap:
                        w1_a, op_a, w2_a, w3_a = gate_a
                        w1_b, op_b, w2_b, w3_b = gate_b
                        assert w3_a not in swapped and w3_b not in swapped
                        swapped.add(w3_a)
                        swapped.add(w3_b)
                        print(to_swap)
                    found = True
                    break
                # print(to_swap)
            if found:
                break
            n_swap += 1
        print(swapped, b, used)
        assert found, (swapped, b, used)

    return ",".join(sorted(list(swapped)))
    wires = {
        "x02": 1, "x01": 1, "x00": 1,
        "y02": 0, "y01": 0, "y00": 1}
    used = day24_execute(wires, gates)
    print(used)
    x, y, z = day24_get_value(wires, "x"), day24_get_value(
        wires, "y"), day24_get_value(wires, "z")
    return f"{x}({x:b})", f"{y}({y:b})", f"{z}{z:b}", f"{x+y}({(x+y):b})"

def day24_1(data):
    return day24_solve(data, False)

def day24_2(data):
    return day24_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
