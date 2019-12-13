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

def cmp(a,b):
    if a < b: return -1
    elif a == b: return 0
    else: return 1

#part 1
program = ic.load("input")
computer = ic.Computer(program)
field = {}
while not computer.halted:
    if computer.needs_input():
        computer.send(0)
    x, y, id = [computer.tick_until_output() for _ in range(3)]
    field[x,y] = id

print(sum(1 for tile in field.values() if tile == 2))


#part 2
program = ic.load("input")
program[0] = 2
computer = ic.Computer(program)

paddle_x = None
ball_x = None
score = None
#strategy: make the paddle's x coordinate trail behind the ball's x coordinate by exactly one.
#possibly we could make them exactly equal, but then we'd have to guess the direction the ball will move on the next frame.
while not computer.halted:
    if computer.needs_input():
        computer.send(cmp(ball_x, paddle_x))
    x, y, value = [computer.tick_until_output() for _ in range(3)]
    if x == -1 and y == 0:
        score = value
    elif value == 3:
        paddle_x = x
    elif value == 4:
        ball_x = x

print(score)