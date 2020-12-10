from enum import Enum
from collections import deque

input__ = "set i 31\n" + "set a 1\n" + "mul p 17\n" + "jgz p p\n" + "mul a 2\n" + "add i -1\n" + \
    "jgz i -2\n" + "add a -1\n" + "set i 127\n" + "set p 826\n" + "mul p 8505\n" + \
    "mod p a\n" + "mul p 129749\n" + "add p 12345\n" + "mod p a\n" + "set b p\n" + \
    "mod b 10000\n" + "snd b\n" + "add i -1\n" + "jgz i -9\n" + "jgz a 3\n" + "rcv b\n" + \
    "jgz b -1\n" + "set f 0\n" + "set i 126\n" + "rcv a\n" + "rcv b\n" + "set p a\n" + \
    "mul p -1\n" + "add p b\n" + "jgz p 4\n" + "snd a\n" + "set a b\n" + "jgz 1 3\n" + \
    "snd b\n" + "set f 1\n" + "add i -1\n" + "jgz i -11\n" + "snd a\n" + "jgz f -16\n" + \
    "jgz a -19"

day18_last_snd = "LAST_SND"

def is_number(n):
    try:
        # Type-casting the string to `float`.
        # If string is not a valid `float`,
        # it'll raise `ValueError` exception
        float(n)
    except ValueError:
        return False
    return True

def day18_get(map_, reg):
    if not reg in map_:
        map_[reg] = 0
    return map_[reg]

def day18_snd(map_, val):
    global day18_last_snd
    value = val
    if not is_number(val):
        value = day18_get(map_, val)
    map_[day18_last_snd] = value

def day18_set(map_, reg, val):
    map_[reg] = val

def day18_add(map_, reg, val):
    value = day18_get(map_, reg) + val
    map_[reg] = value

def day18_mul(map_, reg, val):
    value = day18_get(map_, reg) * val
    map_[reg] = value

def day18_mod(map_, reg, val):
    value = day18_get(map_, reg) % val
    map_[reg] = value


global snd_count
global count
snd_count = 0
count = False

class Instruction(Enum):
    snd = 0
    set_ = 1
    add = 2
    mul = 3
    mod = 4
    rcv = 5
    jgz = 6

def process(data):
    comm = data.split(" ")
    comm[0] = "set_" if comm[0] == "set" else comm[0]
    op = Instruction[comm[0]]
    arg1 = comm[1]
    arg2 = 0
    if is_number(arg1):
        arg1 = int(arg1)
    if len(comm) == 3:
        arg2 = comm[2]
        if is_number(arg2):
            arg2 = int(arg2)
    return (op, arg1, arg2)

def day18_jgz(map_, reg):
    value = reg
    if not is_number(reg):
        value = day18_get(map_, reg)
    return value > 0

def day18_process(map_, inst, queue, otherQueue):
    global snd_count
    global count
    global day18_last_snd
    comm = inst[0]
    arg1 = inst[1]
    arg2 = inst[2]
    jump = 1
    if not is_number(arg2):
        arg2 = day18_get(map_, arg2)
    if comm == Instruction.snd:
        day18_snd(map_, arg1)
        if count:
            snd_count += 1
        value = map_[day18_last_snd]
        otherQueue.append(value)
    elif comm == Instruction.set_:
        day18_set(map_, arg1, arg2)
    elif comm == Instruction.add:
        day18_add(map_, arg1, arg2)
    elif comm == Instruction.mul:
        day18_mul(map_, arg1, arg2)
    elif comm == Instruction.mod:
        day18_mod(map_, arg1, arg2)
    elif comm == Instruction.rcv:
        if len(queue) != 0:
            value = queue.popleft()
            day18_set(map_, arg1, value)
        else:
            # print("sleeping...")
            return 0
    elif comm == Instruction.jgz:
        #print("jump? " + str(parts[1]))
        if day18_jgz(map_, arg1):
            #print("jumping: " + str(parts[2]))
            jump = arg2
    return jump

def day18_2(input_):
    global snd_count
    global count
    input_ = [process(comm) for comm in input_]
    print(input_)
    # return
    registerMap = [{"p": 0}, {"p": 1}]
    queue = [deque(), deque()]
    terminated = [False, False]
    inst = [0, 0]
    curr_prog = 0
    deadLockCheck = 0
    counter = 0
    while True:
        counter += 1
        if counter % 10000 == 0:
            print(snd_count)
        if (inst[curr_prog] < 0 or inst[curr_prog] >= len(input_)):
            print("##########################################")

        jump = day18_process(
            registerMap[curr_prog],
            input_[inst[curr_prog]],
            queue[curr_prog],
            queue[(curr_prog + 1) % 2])
        if jump == 0:
            deadLockCheck += 1
            if deadLockCheck == 2:
                terminated[0] = True
                terminated[1] = True
        else:
            deadLockCheck = 0

        inst[curr_prog] += jump

        if (inst[curr_prog] < 0 or inst[curr_prog] >= len(input_)):
            terminated[curr_prog] = True
        if (terminated[0] and terminated[1]):
            break

        curr_prog += 1
        curr_prog = curr_prog % 2
        if terminated[curr_prog]:
            curr_prog += 1
            curr_prog = curr_prog % 2
        count = curr_prog == 1

    return snd_count

#input = "set a 1\nadd a 2\nmul a a\nmod a 5\nsnd a\nset a 0\nrcv a\njgz a -1\nset a 1\njgz a -2";
#   input = "snd 1\nsnd 2\nsnd p\nrcv a\nrcv b\nrcv c\nrcv d"


print("18_2 - " + str(day18_2(input__.split("\n"))))
