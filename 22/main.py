import re
import math
import mod

def show(deck):
    print(" ".join(str(item) for item in deck))

def deal_into_new_stack(decksize):
    def _deal(idx):
        return decksize - idx - 1
    return _deal

def cut(decksize, n):
    def _cut(idx):
        return (idx + n) % decksize
    return _cut

def deal_with_increment(decksize, n):
    def _deal(idx):
        return mod.solve_coprime_modulus(n, idx, decksize)
    return _deal

def compose(funcs):
    def f(idx):
        for func in funcs[::-1]:
            idx = func(idx)
        return idx
    return f

def apply_multiple_times(f, amount):
    if amount == 1:
        return f
    elif amount % 2 == 1:
        g = apply_multiple_times(f, amount//2)
        return lambda n: f(g(g(n)))
    elif amount % 2 == 0:
        g = apply_multiple_times(f, amount//2)
        return lambda n: g(g(n))

def load_input_process(decksize):
    funcs = []
    with open("input") as file:
        for line in file:
            line = line.strip()
            if line == "deal into new stack":
                funcs.append(deal_into_new_stack(decksize))
            elif m := re.match(r"cut (-?\d+)", line):
                funcs.append(cut(decksize, int(m.group(1))))
            elif m := re.match(r"deal with increment (\d+)", line):
                funcs.append(deal_with_increment(decksize, int(m.group(1))))
            else:
                raise Exception(f"Unrecognized line type {repr(line)}")
    return compose(funcs)

#process = load_input_process(I forget what number it is)
#print(next(i for i in range(DECKSIZE) if process(i) == 2019))
#process = apply_multiple_times(process, 101741582076661)
#print(process(2020))

def periodicity(decksize, n):
    start = list(range(decksize))
    deck = start.copy()
    x = 0
    #print(deck)
    while True:
        x += 1
        deck = deal(deck,n)
        #print(deck)
        if deck == start:
            return x


def deal(deck, n):
    f = deal_with_increment(len(deck), n)
    return [deck[f(idx)] for idx in range(len(deck))]

import prettyprint
d = {}

limit = 40
for decksize in range(1, limit+1):
    for n in range(1, limit+1):
        if math.gcd(decksize,n) != 1:
            d[decksize, n] = " "
        else:
            d[decksize, n] = periodicity(decksize, n)

print(prettyprint.dict_print(d))