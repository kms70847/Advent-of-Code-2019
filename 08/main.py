with open("input") as file:
    data = list(map(int, file.read().strip()))

width = 25
height = 6
area = width*height
num_layers = len(data) // (width*height)

x = min(range(0, len(data), width*height), key=lambda i: data[i:i+area].count(0))
layer = data[x: x+area]
print(layer.count(1) * layer.count(2))

output = []
for j in range(height):
    row = []
    for i in range(width):
        pixel = 2
        for k in range(num_layers):
            x = data[k*area+j*width+i]
            if x in (0,1):
                pixel = x
                break
        row.append(" .?"[pixel])
    output.append("".join(row))
print("\n".join(output))