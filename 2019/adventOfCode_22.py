# -*- coding: utf-8 -*-
# pylint: disable=import-error
# pylint: disable=wrong-import-position
# from _heapq import *
# from _collections import defaultdict
# import time
from timeit import default_timer as timer
from heapq import *
from collections import defaultdict
import os
import sys

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
print(FILE_DIR)
sys.path.insert(0, FILE_DIR + "/")
sys.path.insert(0, FILE_DIR + "/../")
sys.path.insert(0, FILE_DIR + "/../../")
from common.utils import read_input, main, clear  # NOQA: E402
from icComputer import ic_execute  # NOQA: E402
# pylint: enable=import-error
# pylint: enable=wrong-import-position

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

WHITE_SQUARE = "█"
WHITE_CIRCLE = "•"
BLUE_CIRCLE = f"{bcolors.OKBLUE}{bcolors.BOLD}•{bcolors.ENDC}"
RED_SMALL_SQUARE = f"{bcolors.FAIL}{bcolors.BOLD}■{bcolors.ENDC}"

# To deal into new stack, create a new stack of cards by dealing the top card of the deck onto the top of the new stack repeatedly until you run out of cards:

def new_stack(deck):
    print("NS")
    i = 0
    l = len(deck)
    l2 = l // 2
    while i < l2:
        i += 1
        tmp = deck[i]
        deck[i] = deck[l - 1 - i]
        deck[l - 1 - i] = tmp

# To cut N cards, take the top N cards off the top of the deck and move them as a single unit to the bottom of the deck, retaining their order. For example, to cut 3:

def cutN(deck, n):
    print("CUT")
    if n >= 0:
        cut = deck[0:n]
        remaining = deck[n:]
        return remaining + cut
    else:
        cut = deck[n:]
        remaining = deck[0:n]
        return cut + remaining

# To deal with increment N, start by clearing enough space on your table to lay out all of the cards individually in a long line. Deal the top card into the leftmost position. Then, move N positions to the right and deal the next card there. If you would move into a position past the end of the space on your table, wrap around and keep counting from the leftmost card again. Continue this process until you run out of cards.

def incs(deck, n):
    print("INCS")
    l = len(deck)
    n_d = [0 for _ in range(l)]
    i = 0
    for c in deck:
        n_d[i] = c
        i = (i + n) % l
    return n_d

# To deal into new stack, create a new stack of cards by dealing the top card of the deck onto the top of the new stack repeatedly until you run out of cards:

def new_stack2(l, n):
    # print("NS")
    return l - 1 - n

# To cut N cards, take the top N cards off the top of the deck and move them as a single unit to the bottom of the deck, retaining their order. For example, to cut 3:

def cutN2(l, n, n2):
    # print("CUT", n, n2)
    if n < 0:
        n = l + n
    # if n >= 0:
    if n2 >= l - n:
        return n2 - (l - n)
    else:
        return n2 + n
    # else:
        # n = abs(n)
        # if n2 < n:
        #     return l - 1 - n2
        # else:
        #     return n2 - n

# To deal with increment N, start by clearing enough space on your table to lay out all of the cards individually in a long line. Deal the top card into the leftmost position. Then, move N positions to the right and deal the next card there. If you would move into a position past the end of the space on your table, wrap around and keep counting from the leftmost card again. Continue this process until you run out of cards.

def incs2(l, n, n2):
    # print("INCS", n, n2)
    i = 0
    count = 0

    if n2 > n:
        count += n2 // n
        i = count * n
    # print(i, count)
    while True:
        assert count < l, count
        if n2 > i:
            x = ((n2 - i) // n)
            count += x
            i = i + x * n
        # print(2, i, count)
        if i == n2:
            return count
        # count += 1
        # i += n
        # print("next", i, count)
        # if i == n2:
            # return count
        x = (l // n) - 1
        count += x
        i = (i + n * x) % l
        # print ("wrap", x, i, count)

    # while i != n2:

    #     count += 1
    #     i = (i + n)%l
    return count

def day22_parse_input(data):
    insts = []
    for line in data:
        if line == "deal into new stack":
            insts .append((0, 0))
        elif "cut " in line:
            n = line.split("cut ")[-1]
            insts .append((1, int(n)))
        else:
            n = line.split("deal with increment ")[-1]
            insts .append((2, int(n)))
    return insts

def day22_1(data):
    #data = read_input(2019, 2203)
    data = day22_parse_input(data)
    deck = [i for i in range(10007)]
    # deck = [i for i in range(10)]
    pos = []
    for d, n in data:
        if d == 0:
            new_stack(deck)
        elif d == 1:
            deck = cutN(deck, n)
        else:
            deck = incs(deck, n)
        pos.append(deck.index(2019))
    print(pos)
    return deck.index(2019)

def day22_2(data):
    # 119315717514047
    #data = read_input(2019, 2203)
    data = day22_parse_input(data)
    # deck = [i for i in range(119315717514047)]
    # deck = [i for i in range(10007)]
    # deck = [i for i in range(10)]
    mem = []
    mem_m = set()
    l = 119315717514047
    it = 101741582076661
    nn = 2020
    # l = 10007
    # it = 1
    # nn = 4703
    correct = [9769, 5723, 3336, 3340, 724, 9282, 3166, 4296, 1855, 6347, 3659, 9202, 3692, 9981, 9331, 3311, 1757, 837, 5170, 1225, 4693, 4284, 8271, 8928, 7763, 7957, 2049, 7944, 3510, 3154, 6852, 2704, 7302, 2432, 5543, 4463, 7459, 8323, 714, 9292, 4287, 5719, 7190, 114, 9892, 2187, 2524, 7572, 2476,
               1343, 2327, 8370, 8274, 8052, 2455, 3601, 9651, 5062, 3902, 6104, 7601, 4848, 1738, 649, 7788, 1599, 7582, 6154, 5297, 4709, 7511, 207, 2481, 4049, 5384, 1408, 4254, 5752, 3230, 3518, 1716, 8290, 3725, 4893, 216, 8856, 1150, 4249, 9451, 6206, 5280, 2239, 5300, 3577, 8731, 1275, 6258, 5440, 5303, 4703]
    # pos = []
    seen = set()
    seen2 = []
    m = {}
    r_data = list(reversed(data))
    for i in range(it):
        if nn in seen:
            ii = seen2.index(nn)
            iii = (it - i) % (i - ii)
            print(ii, iii)
            return seen2[ii + iii]
        assert not (nn in seen)
        seen.add(nn)
        seen2.append(nn)
        if i % 1000 == 0:
            print(i, it)
        # start = timer()
        for d, n in r_data:
            if l == 10007:
                true_n = correct.pop()
                assert true_n == nn
            # pos.insert(0, nn)
            if d == 0:
                nn = new_stack2(l, nn)
            elif d == 1:
                nn = cutN2(l, n, nn)
            else:
                nn = incs2(l, n, nn)
            # print(nn)
        # print((timer() - start)/1000)
    print(pos)
    return nn

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def day22_2(data):
    # 119315717514047
    #data = read_input(2019, 2203)
    data = day22_parse_input(data)
    # deck = [i for i in range(119315717514047)]
    # deck = [i for i in range(10007)]
    # deck = [i for i in range(10)]
    mem = []
    mem_m = set()
    l = 119315717514047
    it = 101741582076661
    nn = 2020
    # l = 10007
    it = 1
    # nn = 4703
    correct = [9769, 5723, 3336, 3340, 724, 9282, 3166, 4296, 1855, 6347, 3659, 9202, 3692, 9981, 9331, 3311, 1757, 837, 5170, 1225, 4693, 4284, 8271, 8928, 7763, 7957, 2049, 7944, 3510, 3154, 6852, 2704, 7302, 2432, 5543, 4463, 7459, 8323, 714, 9292, 4287, 5719, 7190, 114, 9892, 2187, 2524, 7572, 2476,
               1343, 2327, 8370, 8274, 8052, 2455, 3601, 9651, 5062, 3902, 6104, 7601, 4848, 1738, 649, 7788, 1599, 7582, 6154, 5297, 4709, 7511, 207, 2481, 4049, 5384, 1408, 4254, 5752, 3230, 3518, 1716, 8290, 3725, 4893, 216, 8856, 1150, 4249, 9451, 6206, 5280, 2239, 5300, 3577, 8731, 1275, 6258, 5440, 5303, 4703]
    # pos = []
    seen = set()
    seen2 = []
    m = {}
    r_data = list(reversed(data))
    for i in range(it):
        if nn in seen:
            ii = seen2.index(nn)
            iii = (it - i) % (i - ii)
            print(ii, iii)
            return seen2[ii + iii]
        assert not (nn in seen)
        seen.add(nn)
        seen2.append(nn)
        if i % 1000 == 0:
            print(i, it)
        # start = timer()
        a,b = 1,0
        nn2 = nn
        nn3 = nn
        nn4 = nn
        nn4_l = []
        a2,b2 = 1,0
        for d, n in r_data:
            if l == 10007:
                true_n = correct.pop()
                assert true_n == nn
            # pos.insert(0, nn)
            if d == 0:
                nn = new_stack2(l, nn)
                a,b = -a, l-1-b
                a2,b2 = -a2, l-1-b2
                nn2 = (nn2*a + b)%l
                nn3 = (nn3*a + b)
            elif d == 1:
                nn = cutN2(l, n, nn)
                if n < 0:
                    n = l + n
                a,b = a,b + n
                a2,b2 = a2, b2+n
                nn2 = (nn2*a + b)%l
                nn3 = (nn3*a + b)
            else:
                nn = incs2(l, n, nn)
                a,b = a*n,b
                a2,b2 = a2*modinv(n,l), b2*modinv(n,l)
                nn2 = (nn2*a + b)%l
                nn3 = (nn3*a + b)
            # print(nn, nn2, nn3)
            # print(nn)
            nn4_l.insert(0, (4703*a2 + b2)%l)
        print(" " ,nn4_l)
        print(a2,b2)
        print()
        nn2, nn3 = nn, nn
        a,b = 1,0
        nn4 = 4703
        print(nn)
        nn2_l = []
        for d, n in data:
            if d == 0:
                a,b = -a, l-1-b
                nn2 = (nn*a + b)%l
                nn3 = (nn3*a + b)
            elif d == 1:
                if n < 0:
                    n = l + n
                a,b = a,b - n
                nn2 = (nn*a + b)%l
                nn3 = (nn3*a + b)
            else:
                a,b = a*n,b*n
                nn2 = (nn*a + b)%l
                nn3 = (nn3*a + b)
            nn2_l.append(nn2)
            # print(nn, nn2, nn3)
        print(nn2_l)
        print(nn, nn2, nn3%l)
        # print((timer() - start)/1000)
    # print(pos)
    print("hehe")
    import math
    print(((2020*a2 + b2) ** 101741582076661) % l)
    from decimal import Decimal
    print(Decimal(2020*a2 + b2) ** 101741582076661 % l)
    print("hehe")
    print(power(2020*a2 + b2, 101741582076661, l))
    print((2020*a2 + b2)**101741582076661)
    return nn


# Iterative Function to calculate 
# (x^y)%p in O(log y)  
def power(x, y, p) : 
    res = 1     # Initialize result 
  
    # Update x if it is more 
    # than or equal to p 
    x = x % p  
  
    while (y > 0) : 
          
        # If y is odd, multiply 
        # x with result 
        if ((y & 1) == 1) : 
            res = (res * x) % p 
  
        # y must be even now 
        y = y >> 1      # y = y/2 
        x = (x * x) % p 
          
    return res 
      
""" MAIN FUNCTION """

if __name__ == "__main__":
    main(sys.argv, globals(), 2019)
