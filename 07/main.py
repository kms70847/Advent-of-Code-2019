import intcomputer
import functools
import itertools

@functools.lru_cache(None)
def amplify(signal, input):
    return intcomputer.execute(program, [signal, input])[-1]

def power(signals):
    output = 0
    for signal in signals:
        output = amplify(signal, output)
    return output


for filename in ("sample1", "sample2", "sample3", "input"):
    amplify.cache_clear()
    program = intcomputer.load(filename)

    x = max((signals for signals in itertools.permutations(range(5))), key=power)
    print(f"{filename}: Max thruster signal {power(x)} (from phase starting sequence {x})")