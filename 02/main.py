import operator
import re


def result(noun, verb):
    with open("input") as file:
        program = [int(x) for x in re.findall(r"\d+", file.read())]

    program[1] = noun
    program[2] = verb

    pc = 0
    while 0 <= pc < len(program) and program[pc] != 99:
        opcode, a, b, dest = program[pc:pc+4]
        op = operator.add if opcode == 1 else operator.mul
        program[dest] = op(program[a], program[b])
        pc += 4

    return program[0]

print(result(12,2))

for noun in range(100):
    for verb in range(100):
        if result(noun, verb) == 19690720:
            print(100 * noun + verb)
            exit(0)