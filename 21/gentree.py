import json

def size(x):
    if isinstance(x, list):
        return sum(size(item) for item in x)
    else:
        return 1

def AND(a,b):
    if a == 0 or b == 0:
        return 0
    elif a == 1:
        return b
    elif b == 1:
        return a
    else:
        return ["and", a, b]

def OR(a,b):
    if a == 1 or b == 1:
        return 1
    elif a == 0:
        return b
    elif b == 0:
        return a
    else:
        return ["or", a, b]

def safe(idx, num_sensors):
    if idx >= num_sensors:
        return 1
    letter = "ABCDEFGHI"[idx] if idx < 9 else "?"
    return AND(f"{letter}", OR(safe(idx+4, num_sensors), safe(idx+1, num_sensors)))

print(json.dumps(safe(0,9), indent=1))