import re
from geometry import Point

class Moon:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
    def influence(self, target):
        cmp = lambda a, b: -1 if a < b else (1 if a > b else 0)
        target.velocity.x += cmp(self.position.x, target.position.x)
        target.velocity.y += cmp(self.position.y, target.position.y)
        target.velocity.z += cmp(self.position.z, target.position.z)
    def update(self):
        self.position += self.velocity
    def energy(self):
        magnitude = lambda p: abs(p.x) + abs(p.y) + abs(p.z)
        return magnitude(self.position) * magnitude(self.velocity)
    def __repr__(self):
        return f"<pos=<x={self.position.x:3}, y={self.position.y:3}, z={self.position.z:3}>>, vel=<x={self.velocity.x:3}, y={self.velocity.y:3}, z={self.velocity.z:3}>"

def tick():
    for i in range(len(moons)):
        for j in range(len(moons)):
            moons[i].influence(moons[j])
    for moon in moons:
        moon.update()

def show():
    for moon in moons:
        print(moon)

moons = []
with open("input") as file:
    for line in file:
        x,y,z = [int(g) for g in re.findall("-?\d+", line)]
        moons.append(Moon(Point(x,y,z), Point(0,0,0)))

show()
for i in range(1000):
    tick()
    print(f"\nAfter {i+1} steps:")
    show()

print(sum(moon.energy() for moon in moons))