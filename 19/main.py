import intcomputer as ic
from functools import lru_cache
import itertools

@lru_cache(None)
def get(x,y):
    computer = ic.Computer(ic.load("input"))
    computer.send(x)
    computer.send(y)
    return computer.tick_until_output()


#part 1
print(sum(get(x,y) for x in range(50) for y in range(50)))



#part 2

"""
Represent left and right lines as functions
L(y) = m_l*y + b_l
R(y) = m_r*y + b_r

assume that both lines pass through the origin, so b_l and b_r are both zero

L(y) = m_l*y
R(y) = m_r*y

determine y such that
R(y) = 100 + L(y+100)

m_r*y = 100 + m_l*(y+100)
m_r*y = 100 + m_l*y + m_l*100
m_r*y - m_l*y = 100 + m_l*100
y(m_r - m_l) = 100(m_l+1)
y = 100 * (m_l + 1) / (m_r - m_l)
"""

#estimate slopes by locating edges of beam at y=50
y=50
m_l = None
for x in range(50):
    val = get(x, y)
    if val == 1 and m_l is None:
        m_l = x / y
    if val == 0 and m_l is not None:
        m_r = x / y
        break


#boundaries here are inclusive -- IOW, right and bottom are the last coordinates in the rect
#let's use 101 in place of 100 here -- it's better to overshoot the solution than undershoot it.
top = int(101 * (m_l + 1) / (m_r - m_l))
right = int(m_r * top)
left = right - 99
bottom = top + 99

assert get(left, bottom) == 1, "bottom-left not within beam"
assert get(right, top) == 1, "top-right not within beam"


#estimate probably overshot the actual smallest point, so move back up towards the origin until there's no more wiggle room
while True:
    moved = False
    #look for candidate positions closer to the origin. We need to examine positions that are more than 1 or 2 units away, because the edges of the beam might be too sawtooth-shaped for a fine-resolution search.
    margin = 5
    for dx, dy in itertools.product(range(-margin, 0), range(-margin, 0)):
        if get(left+dx, bottom+dy) == 1 and get(right+dx, top+dy) == 1:
            left += dx
            right += dx
            top += dy
            bottom += dy
            moved = True
            break
    if not moved: break

print(left * 10000 + top)