from collections import defaultdict
import itertools

import intcomputer as ic
from geometry import Point

EMPTY = "."
SCAFFOLD = "#"

up = Point(0,-1)
down = Point(0,1)
left = Point(-1,0)
right = Point(1,0)

deltas = [up, down, left, right]
cw = {up: right, right: down, down: left, left: up}
ccw = {v:k for k,v in cw.items()}

def iter_output():
    computer = ic.Computer(ic.load("input"))
    while not computer.halted:
        x = computer.tick()
        if x is not None:
            yield(chr(x))

def longpath():
    p = next(p for p, cell in field.items() if cell not in ".#")
    print(p)

    bot_glyphs = {"^": up, "v": down, "<": left, ">": right}
    facing = bot_glyphs[field[p]]

    path = []
    while True:
        if field[p+facing] == SCAFFOLD:
            path.append("1")
            p = p + facing
        elif field[p + cw[facing]] == SCAFFOLD:
            path.append("R")
            facing = cw[facing]
        elif field[p + ccw[facing]] == SCAFFOLD:
            path.append("L")
            facing = ccw[facing]
        else:
            #no obvious place to go next
            break

    #squish consecutive 1 commands into single commands
    path = [str(len(list(v))) if k == "1" else k*len(list(v)) for k,v in itertools.groupby(path)]
    print(path)
    print(f"\nEnded at {p}")


field = defaultdict(lambda: EMPTY)

x = 0
y = 0
for c in iter_output():
    if c == "\n":
        y += 1
        x = 0
    else:
        field[Point(x,y)] = c
        x += 1


#part 1
intersections = []
for p, cell in list(field.items()):
    if cell != EMPTY:
        neighboring_scaffolds = 0
        for delta in deltas:
            neighbor = p + delta
            if field[neighbor] != EMPTY:
                neighboring_scaffolds += 1
        if neighboring_scaffolds > 2:
            intersections.append(p)

print(sum(p.x*p.y for p in intersections))

#part 2
#value determined by looking at the output of longpath() very intently
s = "B,A,B,C,A,C,A,C,B,C\nL,8,R,10,R,6\nR,12,L,10,R,12\nR,12,L,10,R,10,L,8\nn\n"

computer = ic.Computer(ic.load("input"))
computer.program[0] = 2

for c in s:
    computer.send(ord(c))

while not computer.halted:
    x = computer.tick()
    if x is not None:
        if x > 256:
            print(x)
        else:
            #print(chr(x), end="")
            pass