import re

def fuel_series(x):
    seq = []
    while True:
        x = x // 3 - 2
        if x <= 0: break
        seq.append(x)
    return seq

with open("input") as file:
    data = [fuel_series(int(x)) for x in re.findall(r"\d+", file.read())]

#part 1
print(sum(seq[0] for seq in data))

#part 2
print(sum(sum(seq) for seq in data))