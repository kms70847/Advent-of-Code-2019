from geometry import Point
import intcomputer as ic

import msvcrt
import sys
import os
import time

def dir_input(prompt):
    codes = {b"H": "up", b"P": "down", b"K": "left", b"M": "right"}
    print(prompt, end="")
    sys.stdout.flush()
    while True:
        k = msvcrt.getch()
        if k == b"q":
            exit()
        elif k == b"\xe0":
            k = msvcrt.getch()
            if k in codes:
                print(codes[k])
                return codes[k]

def manual_explore():
    while True:
        show()
        dir = dir_input("Choose a direction: ")
        target = cur_pos + directions[dir]
        x = ["up", "down", "left", "right"].index(dir) + 1
        computer.send(x)
        reply = computer.tick_until_output()
        if reply == COLLIDED:
            field[target] = WALL
        elif reply == MOVED:
            field[target] = EMPTY
            cur_pos = target
        elif reply == MOVED_AND_FOUND_AIR:
            field[target] = AIR
            cur_pos = target
        else:
            print(f"Didn't understand reply from computer: {reply}")

def show():
    glyphs = {EMPTY: " ", WALL: "X", AIR: "!", None: "."}
    left, right, top, bottom = [f(getattr(p,d) for p in field.keys()) for d in "xy" for f in (min, max)]
    margin = 1
    rows = []
    for j in range(top-margin, bottom+margin+1):
        row = []
        for i in range(left-margin, right+margin+1):
            p = Point(i,j)
            if p == cur_pos:
                c = "@"
            elif p in to_visit:
                c = "?"
            else:
                c = glyphs[field.get(p)]
            row.append(c)
        rows.append("".join(row))
    os.system("cls")
    print("\n".join(rows))
    time.sleep(0.1)

def ancestors(p, origin_first=True):
    #return a list of all the points between the given one and the origin
    #The order is [origin, ..., p] by default. Use `origin_first=False` for [p, ..., origin].
    result = []
    while p is not None:
        result.append(p)
        p = parents[p]
    if origin_first:
        result.reverse()
    return result

def get_path(a,b):
    #return a list of all the points on the shortest path between the given points.
    #only works if the maze has been fully explored already.
    a_path = ancestors(a, False)
    b_path = ancestors(b, False)
    assert a_path[-1] == b_path[-1]
    while a_path and b_path and a_path[-1] == b_path[-1]:
        p = a_path.pop()
        b_path.pop()
    return a_path + [p] + list(reversed(b_path))

#cell states
EMPTY = 0
WALL = 1
AIR = 2

#possible replies from program
COLLIDED = 0
MOVED = 1
MOVED_AND_FOUND_AIR = 2

directions = {
    "up": Point(0,-1),
    "down": Point(0,1),
    "left": Point(-1, 0),
    "right": Point(1, 0)
}
opposite = {"up": "down", "left": "right", "down": "up", "right": "left"}

field = {Point(0,0): EMPTY}
cur_pos = Point(0,0)
to_visit = {cur_pos + dir for dir in directions.values()}
to_visit = set() #todo: remove this, I don't want it any more

computer = ic.Computer(ic.load("input"))
move = lambda dirname: computer.send(1 + ["up", "down", "left", "right"].index(dirname))

parents = {cur_pos: None}

path = []
i = 0
while True:
    i += 1
    #if i % 100 == 0: show()
    neighbors = {dirname: cur_pos + vec for dirname, vec in directions.items()}
    #look for an unexplored neighbor
    for dirname, delta in directions.items():
        target = cur_pos + delta
        if target not in field:
            parents[target] = cur_pos
            move(dirname)
            reply = computer.tick_until_output()
            if reply == COLLIDED:
                field[target] = WALL
            elif reply == MOVED or reply == MOVED_AND_FOUND_AIR:
                field[target] = {MOVED: EMPTY, MOVED_AND_FOUND_AIR: AIR}[reply]
                path.append(dirname)
                cur_pos = target
            break
    else:
        #couldn't find an unexplored neighbor. 
        #No point exploring this branch any more; backtrack to the previous step, or quit if we backtracked to origin.        
        if path:
            last_move = path.pop()
            move(opposite[last_move])
            assert computer.tick_until_output() != COLLIDED
            cur_pos = cur_pos - directions[last_move]
        else:
            #maze fully explored
            break

show()
print(f"Complete after {i} steps.")

p = next(p for p, cell in field.items() if cell == AIR)
print(len(ancestors(p)) - 1)

longest_path = max(
    (get_path(p, cand) for cand, cell in field.items() if cell != WALL), 
    key = len
)
print(len(longest_path)-1)