
def ic_mode(insts, v, mode, rel_base=0, to_write=False):
    if to_write:
        return v + (rel_base if mode == 2 else 0)
    if mode == 1:
        return v
    else:
        return insts[v + (rel_base if mode == 2 else 0)]
    raise NotImplementedError

def ic_execute(op, pc, insts, inputs=None, outputs=None, rel_base=0):
    if inputs is None:
        inputs = []
    if outputs is None:
        outputs = []
    modes = op // 100
    op = op % 100
    if op == 1:
        a = insts[pc + 1]
        b = insts[pc + 2]
        c = insts[pc + 3]
        a_mode = modes % 10
        modes = modes // 10
        b_mode = modes % 10
        modes = modes // 10
        c_mode = modes % 10
        modes = modes // 10
        c = ic_mode(insts, c, c_mode, rel_base, True)
        insts[c] = ic_mode(insts, a, a_mode, rel_base) + \
            ic_mode(insts, b, b_mode, rel_base)
        return (pc + 4, insts, rel_base)
    elif op == 2:
        a = insts[pc + 1]
        b = insts[pc + 2]
        c = insts[pc + 3]
        a_mode = modes % 10
        modes = modes // 10
        b_mode = modes % 10
        modes = modes // 10
        c_mode = modes % 10
        modes = modes // 10
        c = ic_mode(insts, c, c_mode, rel_base, True)
        insts[c] = ic_mode(insts, a, a_mode, rel_base) * \
            ic_mode(insts, b, b_mode, rel_base)
        return (pc + 4, insts, rel_base)
    elif op == 3:
        a = insts[pc + 1]
        a_mode = modes % 10
        modes = modes // 10
        a = ic_mode(insts, a, a_mode, rel_base, True)
        insts[a] = inputs.pop(0)
        return (pc + 2, insts, rel_base)
    elif op == 4:
        a = insts[pc + 1]
        a_mode = modes % 10
        modes = modes // 10
        outputs.append(ic_mode(insts, a, a_mode, rel_base))
        return (pc + 2, insts, rel_base)
    elif op == 5:
        a = insts[pc + 1]
        b = insts[pc + 2]
        a_mode = modes % 10
        modes = modes // 10
        b_mode = modes % 10
        modes = modes // 10
        val = ic_mode(insts, a, a_mode, rel_base)
        if val != 0:
            pc = ic_mode(insts, b, b_mode, rel_base)
        else:
            pc = pc + 3
        return (pc, insts, rel_base)
    elif op == 6:
        a = insts[pc + 1]
        b = insts[pc + 2]
        a_mode = modes % 10
        modes = modes // 10
        b_mode = modes % 10
        modes = modes // 10
        val = ic_mode(insts, a, a_mode, rel_base)
        if val == 0:
            pc = ic_mode(insts, b, b_mode, rel_base)
        else:
            pc = pc + 3
        return (pc, insts, rel_base)
    elif op == 7:
        a = insts[pc + 1]
        b = insts[pc + 2]
        c = insts[pc + 3]
        a_mode = modes % 10
        modes = modes // 10
        b_mode = modes % 10
        modes = modes // 10
        c_mode = modes % 10
        modes = modes // 10
        c = ic_mode(insts, c, c_mode, rel_base, True)
        val1 = ic_mode(insts, a, a_mode, rel_base)
        val2 = ic_mode(insts, b, b_mode, rel_base)
        if val1 < val2:
            insts[c] = 1
        else:
            insts[c] = 0
        return (pc + 4, insts, rel_base)
    elif op == 8:
        a = insts[pc + 1]
        b = insts[pc + 2]
        c = insts[pc + 3]
        a_mode = modes % 10
        modes = modes // 10
        b_mode = modes % 10
        modes = modes // 10
        c_mode = modes % 10
        modes = modes // 10
        c = ic_mode(insts, c, c_mode, rel_base, True)
        val1 = ic_mode(insts, a, a_mode, rel_base)
        val2 = ic_mode(insts, b, b_mode, rel_base)
        if val1 == val2:
            insts[c] = 1
        else:
            insts[c] = 0
        return (pc + 4, insts, rel_base)
    elif op == 9:
        a = insts[pc + 1]
        a_mode = modes % 10
        val1 = ic_mode(insts, a, a_mode, rel_base)
        rel_base += val1
        return (pc + 2, insts, rel_base)
    raise NotImplementedError
