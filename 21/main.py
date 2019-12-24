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
    while True:
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

s = """NOT D T
NOT T J
WALK
"""

"""
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
RUN
"""

"""
broken JIT jump

if A is a hole:
    J = 1
else:
    if B is a hole and E is a hole:
        J = 1
    else:
        if C is a hole and F is a hole:
            J = 1
        else:
            if D is a hole and G is a hole:
                J = 1
            else:
                J = 0

J = (~A) or (~B and ~E) or (~C and ~F) or (~D and ~G)
J = ~(A) or ~(B or E) or ~(C or F) or ~(D or G)
J = ~(A and (B or E) and (C or F) and (D or G))
J = ~(A and ((B or E) and ((C or F) and (D or G))))

T = G
T = T or D
J = F
J = C or J
T = T and J
J = E
J = J or B
T = T and J
T = T and A
T = not T
J = T
"""

s = """NOT G T
NOT T T
OR D T
NOT F J
NOT J J
OR C J
AND J T
NOT E J
NOT J J
OR B J
AND J T
AND A T
NOT T J
RUN
"""

"""
every case jump
J = (~A or (A and ~B and ~C and D and ~E)):
J = (~A or (A and (~B and (~C and (D and ~E))))):
J = ~(A and ~(A and ~(B or (C or ~(D and ~E))))):


"""

s = """NOT E T
AND D T
NOT T T
OR C T
OR B T
NOT T T
AND A T
NOT T T
AND A T
NOT T J
RUN
"""

s = """NOT E J
NOT J J
OR H J
AND D J
OR G J
AND C J
OR F J
AND B J
OR E J
AND A J
NOT J J
RUN
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

if (size:= len(s.split("\n"))) > 16:
    print(f"Warning: program is {size-1} lines long, which may be rejected")

print(execute(s, verbose=True))