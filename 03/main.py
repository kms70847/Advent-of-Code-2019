import re

def manhattan(a,b=0):
    return int(abs(a.real-b.real) + abs(a.imag-b.imag))

def get_points(directions):
    p = 0
    result = [p]
    for segment in directions.split(","):
        dirname = segment[0]
        dist = int(segment[1:])
        delta = 1j ** ("RDLU".index(dirname))
        for _ in range(dist):
            p += delta
            result.append(p)
    return result

def get_timings(directions):
    d = {}
    for t, p in enumerate(get_points(directions)):
        if p not in d:
            d[p] = t
    return d

timings = []
with open("input") as file:
    for line in file:
        timings.append(get_timings(line))

assert len(timings)==2
overlaps = set(timings[0].keys()).intersection(timings[1].keys())
overlaps.remove(0)

p = min(overlaps, key=manhattan)
print(manhattan(p))

time = lambda p: sum(timing[p] for timing in timings)
p = min(overlaps, key=lambda p: time(p))
print(time(p))