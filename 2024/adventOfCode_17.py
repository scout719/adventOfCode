# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
from copy import deepcopy
import math
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
from common.utils import RED_SMALL_SQUARE, main  # NOQA: E402
from common.utils import day_with_validation, WHITE_SQUARE, BLUE_CIRCLE  # NOQA: E402


YEAR = 2024
DAY = 17
EXPECTED_1 = "5,7,3,0"
EXPECTED_2 = None

def day17_parse(data: list[str]):
    parts = "\n".join(data).split("\n\n")

    registers = {}
    for line in parts[0].split("\n"):
        register, value = line.strip("Register ").split(":")
        registers[register] = int(value)

    program = [int(i) for i in parts[1].strip("Program: ").split(",")]
    return registers, program

def day17_print(rr, cc, walls, path):
    R = max(r for r, _ in walls) + 1
    C = max(c for _, c in walls) + 1
    show = ""
    for r in range(R):
        line = ""
        for c in range(C):
            if (r, c) in walls:
                line += WHITE_SQUARE
            elif r == rr and c == cc:
                line += RED_SMALL_SQUARE
            elif (r, c) in path:
                line += BLUE_CIRCLE
            else:
                line += " "
        show += line + "\n"
    print(show)
    sys.stdout.flush()

def day17_combo(registers, i):
    if 0 <= i <= 3:
        return i
    elif i == 4:
        return registers["A"]
    elif i == 5:
        return registers["B"]
    elif i == 6:
        return registers["C"]
    assert False, i

def day17_execute(registers, program):
    ic = 0
    outs: list[int] = []
    states = set()
    while ic < len(program):
        state = (ic, registers["A"], registers["B"], registers["C"])
        if state in states:
            return []
        states.add(state)
        inst = program[ic]
        if inst == 0 or inst == 6 or inst == 7:
            # adv, bdv, cdv
            ic += 1
            op = program[ic]
            num = registers["A"]
            den = day17_combo(registers, op)
            res = int(math.trunc(num / (2**den)))
            if inst == 0:
                registers["A"] = res
            elif inst == 6:
                registers["B"] = res
            elif inst == 7:
                registers["C"] = res
            else:
                assert False

        elif inst == 1:
            # bxl
            ic += 1
            op = program[ic]
            registers["B"] = registers["B"] ^ op
        elif inst == 2:
            # bst
            ic += 1
            op = program[ic]
            registers["B"] = day17_combo(registers, op) % 8
        elif inst == 3:
            # jnz
            ic += 1
            op = program[ic]
            if registers["A"] != 0:
                ic = op - 1
            else:
                ic += 1
        elif inst == 4:
            # bxc
            ic += 1
            op = program[ic]
            registers["B"] = registers["B"] ^ registers["C"]
        elif inst == 5:
            # out
            ic += 1
            op = program[ic]
            outs.append(day17_combo(registers, op) % 8)
        else:
            assert False

        ic += 1
    return outs

def day17_test(original_registers, program, i):
    registers = deepcopy(original_registers)
    registers["A"] = i
    return day17_execute(registers, program)

def day17_solve(data, part2):
    data = day17_parse(data)
    registers, program = data
    outs = day17_test(registers, program, registers["A"])
    if not part2:
        return ",".join(str(i) for i in outs)

    # Output repeats in cycles of powers of 8 so,
    # starting on the first state that has the desired amount of outputs (8^len(program)),
    # start looking for the target position

    # Eg. For 3 outputs only and powers of 3
    # ...
    # 00 - 1aA
    # 01 - 2aA
    # 02 - 3aA
    # 03 - 1bA
    # 04 - 2bA
    # 05 - 3bA
    # 06 - 1cA
    # 07 - 2cA
    # 08 - 3cA
    # 09 - 1aB
    # 10 - 2aB
    # 11 - 3aB
    # 12 - 1bB
    # 13 - 2bB
    # 14 - 3bB
    # 15 - 1cB
    # 16 - 2cB
    # 17 - 3cB
    # 18 - 1aC
    # 19 - 2aC
    # 20 - 3aC
    # 21 - 1bC
    # 22 - 2bC
    # 23 - 3bC
    # 24 - 1cC
    # 25 - 2cC
    # 26 - 3cC
    # If we want 2aC, we need position:
    # 3^3 to get 3 outputs
    # And 2 jumps on the last column (to get to C)
    # and 0 jumps on the middle column (to get to a)
    # and 1 jump on the first column (to get to 2)
    # So our target is 2 times 3^2 + 0 times 3^1 + 1 times 3^0 = 19
    TEST = len(program)
    i = 8**(len(program) - 1)
    curr = 0
    while curr < TEST:
        step = 8**(len(program) - 1 - curr)
        outs = day17_test(registers, program, i)
        while outs[-(curr + 1)] != program[-(curr + 1)]:
            i += step
            outs = day17_test(registers, program, i)
        curr += 1
    outs = day17_test(registers, program, i)
    assert tuple(program) == tuple(outs)
    return i

def day17_1(data):
    return day17_solve(data, False)

def day17_2(data):
    return day17_solve(data, True)


""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, {
        f"day{DAY}_1": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_1, 1, data),
        f"day{DAY}_2": lambda data: day_with_validation(globals(),
                                                        YEAR, DAY, EXPECTED_2, 2, data),
    }, YEAR)
