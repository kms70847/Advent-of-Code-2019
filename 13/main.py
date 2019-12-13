import intcomputer as ic

import os
def show():
    os.system("cls")
    rows = []
    for j in range(30):
        row = []
        for i in range(70):
            tile = field.get((i,j), 0)
            row.append(" X+-O"[tile])
        rows.append("".join(row))
    print("\n".join(rows))

program = ic.load("input")
program[0] = 2
computer = ic.Computer(program)
field = {}
while not computer.halted:
    if computer.needs_input():
        computer.send(0)
    x, y, id = [computer.tick_until_output() for _ in range(3)]
    field[x,y] = id
    show()

#print(sum(1 for tile in field.values() if tile == 2))