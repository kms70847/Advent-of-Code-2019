from geometry import Point
from collections import defaultdict
import intcomputer as ic

up = Point(0, -1)
down = Point(0, 1)
left = Point(-1,0)
right = Point(1,0)

clockwise = {up: right, right: down, down: left, left: up}
counterclockwise = {dir: clockwise[clockwise[clockwise[dir]]] for dir in clockwise.keys()}

def paint(starting_color):
    computer = ic.Computer(ic.load("input"))

    field = defaultdict(int)
    pos = Point(0,0)
    facing = up

    field[pos] = starting_color

    commands = []
    seen = set() #probably don't really need this
    while not computer.halted:
        if computer.needs_input():
            computer.send(field[pos])
        response = computer.tick()
        if response is not None:
            commands.append(response)
            if len(commands) == 2:
                color, direction = commands
                field[pos] = color
                seen.add(pos)
                if direction == 0:
                    facing = counterclockwise[facing]
                else:
                    facing = clockwise[facing]
                pos += facing
                commands.clear()

    return field

#part 1
print(len(paint(0)))

#part 2
field  = paint(1)
left   = min(p.x for p in field.keys())
right  = max(p.x for p in field.keys())
top    = min(p.y for p in field.keys())
bottom = max(p.y for p in field.keys())

rows = []
for j in range(top, bottom+1):
    row = []
    for i in range(left, right+1):
        row.append(" " if field[Point(i,j)] == 0 else "X")
    rows.append("".join(row))
print("\n".join(rows))