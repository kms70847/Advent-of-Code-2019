import itertools
import sys

import intcomputer as ic

def execute(springcode, verbose=False):
    """
    run the springcode and return the large integer if the bot succeeds.
    if the bot fails, return the row that killed it.
    prints all output if verbose is True.
    """
    computer = ic.Computer(ic.load("input"))
    for c in s:
        computer.send(ord(c))

    rows = [[]]
    #computer.program[1665] = 0 #flight mode
    while True:
        if computer.pc == 610:
            print(f"Packed data: {computer.program[753]:3}; unpacked data:", [computer.program[x] for x in range(716, 747)])
        # for i in range(726, 734):     #no gap mode
            # computer.program[i]= 1
        if (x := computer.tick()) is not None:
            if x > 256:
                return x
            else:
                if verbose:
                    print(chr(x), end="")
                if chr(x) == "\n":
                    rows[-1] = "".join(rows[-1])
                    if all(x in rows[-1] for x in "@#"):
                        return rows[-1].replace("@", ".")
                    rows.append([])
                else:
                    rows[-1].append(chr(x))

INCLUDE = 0
NEGATE = 1
OMIT = 2
def iter_springcodes(sensor_names):
    """springcode programs are equivalent to boolean logic statements of the form e.g.
    J = ~(A and (B and ~(C and E)))
    So we can iterate over them by choosing which registers to include, and which subexpressions to negate.
    """
    for actions in itertools.product((OMIT, NEGATE, INCLUDE), repeat=len(sensor_names)):
        program = []
        for action, sensor in zip(actions, sensor_names):
            if action == OMIT:
                continue

            if len(program) == 0:
                program.append(f"NOT {sensor} T")
            else:
                program.append(f"AND {sensor} T")

            if action == NEGATE:
                program.append(f"NOT T T")
                
        if len(program) == 0:
            #must have omitted every register. No point testing this one.
            continue

        program.append("NOT T J")
        yield "\n".join(program)


"""
Part 1 solution
eager jump
if any of A,B,C are holes, and D is solid, then jump
equivalently,
if all of A,B,C are solid, or D is a hole, don't jump

J = D and (~A or ~B or ~C)
J = D and ~(A and B and C)
J = D and ~(C and (B and (A)))
"""
s = """NOT A T
NOT T T
AND B T
AND C T
NOT T T
AND D T
NOT T T
NOT T J
WALK
"""

#finds a path to the first unseen tile as long as one exists
s = """OR F T
OR I T
AND E T
OR T J
OR H T
AND D T
OR G T
AND C T
OR F T
AND B T
OR T J
AND A J
NOT J J
RUN
"""

# #just walks forward
# s = """WALK\n"""

# #always jumps
# s = """NOT J J\nWALK\n"""

#J = NOT A
s = """NOT A J
RUN
"""

if (size:= len(s.split("\n"))) > 16:
    print(f"Warning: program is {size-1} lines long, which may be rejected")

print(execute(s, verbose=True))