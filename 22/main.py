import re
import math

def show(deck):
    print(" ".join(str(item) for item in deck))

def deal_into_new_stack(deck):
    return list(reversed(deck))

def cut(deck, n):
    n = n % len(deck)
    if n >= 0:
        return deck[n:] + deck[:n]

def deal_with_increment(deck, n):
    if math.gcd(len(deck), n) != 1:
        raise ValueError("Can't deal with increment unless values are coprime")
    result = [None]*len(deck)
    for i, item in enumerate(deck):
        idx = (i*n)%len(deck)
        if result[idx] is not None:
            raise Exception(f"Dealt into same pile twice for deck length {len(deck)} and n {n}")
        result[idx] = item
    return result

deck = list(range(10007))

with open("input") as file:
    for line in file:
        line = line.strip()
        if line == "deal into new stack":
            deck = deal_into_new_stack(deck)
        elif m := re.match(r"cut (-?\d+)", line):
            deck = cut(deck, int(m.group(1)))
        elif m := re.match(r"deal with increment (\d+)", line):
            deck = deal_with_increment(deck, int(m.group(1)))
        else:
            raise Exception(f"Unrecognized line type {repr(line)}")

print(deck.index(2019))