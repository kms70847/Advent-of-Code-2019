import functools
import math
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
        return f"pos=<x={self.position.x:3}, y={self.position.y:3}, z={self.position.z:3}>, vel=<x={self.velocity.x:3}, y={self.velocity.y:3}, z={self.velocity.z:3}>"

def load():
    moons = []
    with open("input") as file:
        for line in file:
            x,y,z = [int(g) for g in re.findall("-?\d+", line)]
            moons.append(Moon(Point(x,y,z), Point(0,0,0)))
    return moons

def tick():
    for i in range(len(moons)):
        for j in range(len(moons)):
            moons[i].influence(moons[j])
    for moon in moons:
        moon.update()

def show():
    for moon in moons:
        print(moon)

def lcm(a,b):
    return a * b // math.gcd(a,b)

#part 1
moons = load()
#show()
for i in range(1000):
    tick()
    #print(f"\nAfter {i+1} steps:")
    #show()

print(sum(moon.energy() for moon in moons))



#part 2
"""
observation: since gravity does not fall off with distance, each axis of the system can be simulated independently.
In other words, the x position of each moon depends only on the x position of all moons, and not their y position or z position.
This means we can slice the system into three simpler one-dimensional systems, and try to detect the periodicity of each one by itself.
In the best case scenario, when the periods are coprime, this will take N**(1/3) time, where N is the periodicity of the whole system.
"""

def slice_axis_state(axis):
    return tuple((getattr(moon.position, axis), getattr(moon.velocity, axis)) for moon in moons)

#each axis gets its own dict of {state: last_seen_time}.
#not sure if it's strictly necessary to store the last seen time. Open question: is the first repeated state always identical to the state at time t=0?
#this seems to be the case for my input and all samples, but I don't know if it holds in general.
seen = {axis: {slice_axis_state(axis): 0} for axis in "xyz"}
periodicity = {axis: None for axis in "xyz"}
pending = set("xyz")
t = 0
while pending:
    tick()
    t += 1
    for axis in pending:
        state = slice_axis_state(axis)
        if state in seen[axis]:
            period = t - seen[axis][state]
            #print(f"Axis {axis} has period {period} starting at {seen[axis][state]}")
            periodicity[axis] = period
        else:
            seen[axis][state] = t
    pending = {axis for axis in pending if periodicity[axis] is None}

print(functools.reduce(lcm, periodicity.values()))