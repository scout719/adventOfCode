def parse_inst(line):
    # <3 char inst> <signal><value>
    val = int(line[5:])
    return [line[:3], -val if line[4] == '-' else val]

def parse_program(data):
    return [parse_inst(line) for line in data]

def comp_exec(inst, pc, value, acc):
    if inst == "nop":
        return (pc + 1, acc)
    elif inst == "acc":
        return (pc + 1, acc + value)
    elif inst == "jmp":
        return (pc + value, acc)
    raise NotImplementedError
