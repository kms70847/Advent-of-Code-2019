def count(layer, x):
    assert isinstance(layer, list) and isinstance(layer[0], list) and isinstance(layer[0][0], int)
    return sum(col.count(x) for col in layer)

with open("input") as file:
    data = iter(map(int, file.read().strip()))

width = 25
height = 6
layers = []
while True:
    try:
        layer = []
        for j in range(height):
            row = []
            for i in range(width):
                row.append(next(data))
            layer.append(row)
        layers.append(layer)
    except StopIteration:
        break


output = []
for j in range(height):
    row = []
    for i in range(width):
        pixel = 2
        for layer in layers:
            if layer[j][i] in (0,1):
                pixel = layer[j][i]
                break
        row.append(" .?"[pixel])
    output.append("".join(row))
print("\n".join(output))