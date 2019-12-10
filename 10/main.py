import itertools
import math
from collections import deque

def iter_positive_ordered_coprime_pairs(max_manhattan_distance):
    """
    generate all coprime pairs of integers (m,n) with m > n > 0, and m+n <= max_manhattan_distance
    """
    to_visit = {(2,1), (3,1)}
    while to_visit:
        m,n = to_visit.pop()
        if m+n > max_manhattan_distance:
            continue
        yield (m,n)
        to_visit.add((2*m-n, m))
        to_visit.add((2*m+n, m))
        to_visit.add((m+2*n, n))

def iter_coprime_pairs(max_manhattan_distance):
    """
    generate all comprime pairs of integers, including ones whose elements are negative or zero.
    """
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if not (i == j == 0):
                yield (i,j)
    for x, y in iter_positive_ordered_coprime_pairs(max_manhattan_distance):
        for a in (-1,1):
            for b in (-1,1):
                yield (x*a, b*y)
                yield (b*y, x*a)

def in_range(x,y):
    return 0 <= x < width and 0 <= y < height

def visible_from(pos):
    x,y = pos
    #find the maximum manhattan distance between the current position and the most distant corner of the field.
    d = max(x, width-1-x) + max(y, height-1-y)
    for i,j in iter_coprime_pairs(d):
        for mul in itertools.count(1):
            candidate_x = x+mul*i
            candidate_y = y+mul*j
            if in_range(candidate_x, candidate_y):
                if field[candidate_y][candidate_x] == "#":
                    yield (candidate_x, candidate_y)
                    break
            else:
                break

with open("input") as file:
    field = file.read().strip().split("\n")

height = len(field)
width = len(field[0])

asteroids = set()
for j, row in enumerate(field):
    for i, c in enumerate(row):
        if c == "#":
            asteroids.add((i,j))

detect_count = lambda x: sum(1 for _ in visible_from(x))

#part 1
best = max(asteroids, key=detect_count)
print(detect_count(best))

#part 2
angle = lambda p: math.atan2(p[1] - best[1], p[0] - best[0])
to_zap = list(visible_from(best))
assert any(angle(p) == -math.pi/2 for p in to_zap), "can't order to_zap list unless at least one asteroid is due north of base"
to_zap.sort(key = angle)
to_zap = deque(to_zap)
while angle(to_zap[0]) != -math.pi/2:
    to_zap.append(to_zap.popleft())

for _ in range(200):
    p = to_zap.popleft()
    dx,dy = p[0] - best[0], p[1] - best[1]
    m = math.gcd(dx, dy)
    for i in itertools.count(m+1):
        cand_x = best[0] + (dx // m) * i
        cand_y = best[1] + (dy // m) * i
        if in_range(cand_x, cand_y):
            if field[cand_y][cand_x] == "#":
                to_zap.append((cand_x, cand_y))
                break
        else:
            break

print(p[0]*100 + p[1])