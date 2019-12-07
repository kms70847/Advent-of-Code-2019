import re

ADD = 1
MUL = 2
INPUT = 3
OUTPUT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUALS = 8
HALT = 99

POSITION = 0
IMMEDIATE = 1

num_params = {ADD: 3, MUL: 3, INPUT: 1, OUTPUT: 1, JUMP_IF_TRUE: 2, JUMP_IF_FALSE: 2, LESS_THAN: 3, EQUALS: 3, HALT: 0}

def load(filename):
    with open(filename) as file:
        return [int(x) for x in re.findall("-?\d+", file.read())]

def execute(program, inputs, print_outputs=False):
    program = program[:]
    inputs = inputs[::-1]

    pc = 0
    outputs = []

    while True:
        advance_pc = True
        mode, opcode = divmod(program[pc], 100)
        if opcode not in num_params:
            raise Exception(f"Unrecognized opcode {opcode}")
        #print(pc, mode, opcode)
        params = [program[pc+1+i] for i in range(num_params[opcode])]
        modes = [(mode // (10**i))%10 for i in range(num_params[opcode])]
        #print("  ", params, modes)
        fetch = lambda x: params[x] if modes[x] == IMMEDIATE else program[params[x]]
        if opcode == ADD:
            program[params[2]] = fetch(0) + fetch(1)
        elif opcode == MUL:
            program[params[2]] = fetch(0) * fetch(1)
        elif opcode == INPUT:
            program[params[0]] = inputs.pop()
        elif opcode == OUTPUT:
            x = program[params[0]]
            outputs.append(x)
            if print_outputs:
                print(x)
        elif opcode == JUMP_IF_TRUE:
            if fetch(0) != 0:
                pc = fetch(1)
                advance_pc = False
        elif opcode == JUMP_IF_FALSE:
            if fetch(0) == 0:
                pc = fetch(1)
                advance_pc = False
        elif opcode == LESS_THAN:
            program[params[2]] = 1 if fetch(0) < fetch(1) else 0
        elif opcode == EQUALS:
            program[params[2]] = 1 if fetch(0) == fetch(1) else 0
        elif opcode == HALT:
            break
        else:
            raise Exception(f"opcode {opcode} not implemented yet.")

        if advance_pc:
            pc += 1 + num_params[opcode]
    return outputs