import collections
import math

def try_int(x):
    try:
        return int(x)
    except:
        return x

def try_ints(seq):
    return list(map(try_int, seq))
    
def calc(filename, fuel_amt=1):
    d = {}
    with open(filename) as file:
        for line in file:
            requirements, result = line.split(" => ")
            result_amt, result = try_ints(result.split())
            d[result] = {"amt": result_amt, "ingredients": []}
            for requirement in requirements.split(", "):
                req_amt, req = try_ints(requirement.split())
                d[result]["ingredients"].append((req, req_amt))

    quantities = collections.defaultdict(int, {"FUEL": fuel_amt})
    
    while any(key != "ORE" and value > 0 for key, value in quantities.items()):
        x = next(k for k,v in quantities.items() if k != "ORE" and v > 0)
        m = int(math.ceil(quantities[x] / d[x]["amt"])) 
        quantities[x] -= d[x]["amt"] * m
        for req, req_amt in d[x]["ingredients"]:
            quantities[req] += req_amt * m

    return quantities["ORE"]

def reverse_calc(filename):
    target = 1000000000000
    l = 1
    f = lambda x: calc(filename, x)
    assert f(1) < target
    r = l * 2
    while f(r) < target:
        r *= 2
    while r-l > 1:
        mid = (r+l) // 2
        if f(mid) < target:
            l = mid
        else:
            r = mid
    return l

print(calc("input"))
print(reverse_calc("input"))