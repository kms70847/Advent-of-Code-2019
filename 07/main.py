import intcomputer as ic
import functools
import itertools

@functools.lru_cache(None)
def amplify(signal, input):
    return ic.Computer(program, [input, signal]).tick_until_blocked()[-1]

def power(signals):
    output = 0
    for signal in signals:
        output = amplify(signal, output)
    return output

def feedback_power(signals):
    computers = [ic.Computer(program, [signal]) for signal in signals]
    computers[0].send(0)
    while not computers[-1].halted:
        if all (c.halted or c.needs_input() for c in computers):
            raise Exception("Deadlock")
        for i, c in enumerate(computers):
            if not c.needs_input() and not c.halted:
                out = c.tick()
                if out is not None:
                    computers[(i+1)%len(computers)].send(out)
    return computers[-1].outputs[-1]

program = ic.load("input")

#part 1
x = max((signals for signals in itertools.permutations(range(5))), key=power)
print("".join(map(str, x)))

#part 2
x = max((signals for signals in itertools.permutations(range(5, 10))), key=feedback_power)
print(feedback_power(x))