BUG = "#"
EMPTY = "."

def tick(state):
    def in_range(x,y):
        return 0 <= x < 5 and 0 <= y < 5
    def neighbors(x,y):
        result = []
        for dx,dy in ((0,1), (1,0), (0,-1), (-1,0)):
            if in_range(x+dx, y+dy):
                result.append(state[y+dy][x+dx])
        return result
    def tick_tile(x,y):
        c = state[y][x]
        if c == BUG and neighbors(x,y).count(BUG) != 1:
            return EMPTY
        if c == EMPTY and neighbors(x,y).count(BUG) in (1,2):
            return BUG
        return c
    return tuple("".join(tick_tile(x,y) for x in range(5)) for y in range(5))

with open("input") as file:
    data = tuple(file.read().strip().split())

seen = {data}
t = 0
while True:
    t += 1
    data = tick(data)
    if data in seen: 
        break
    seen.add(data)

print(f"Loop detected at t={t}")
print("\n".join(data))
rating = sum((data[y][x]==BUG) * (2 ** (5*y+x)) for x in range(5) for y in range(5))
print(rating)