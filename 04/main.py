import itertools

def pairs(seq):
    for i in range(1, len(seq)):
        yield seq[i-1], seq[i]

with open("input") as file:
    left, right = map(int, file.read().split("-"))

p1_total = 0
p2_total = 0

for x in range(left, right+1):
    x = str(x)
    if any(b < a for a,b in pairs(x)): continue
    has_run = False
    has_size_2_run = False
    for k,v in itertools.groupby(x):
        count = len(list(v))
        if count > 1:
            has_run = True
        if count == 2:
            has_size_2_run = True
    if has_run:
        p1_total += 1
    if has_size_2_run:
        p2_total += 1

print(p1_total)
print(p2_total)