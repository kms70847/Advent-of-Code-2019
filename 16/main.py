def rightmost_digit(x):
    if x >= 0:
        return x%10
    else:
        return -x%10

def pattern_coef(x,y):
    return [0,1,0,-1][((x+1)//(y+1))%4]

def tick(s):
    result = []
    for j in range(len(s)):
        total = 0
        for i,c in enumerate(s):
            c = int(c)
            #print(f"{c}*{pattern_coef(i,j):<2}", end= " ")
            total += int(c) * pattern_coef(i,j)
        result.append(str(rightmost_digit(total)))
        #print(f"= {total}({rightmost_digit(total)})")    
    return "".join(result)

with open("input") as file:
    s = file.read().strip()

for _ in range(100):
    s = tick(s)

print(s[:8])