import re
import copy
import collections

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

class Computer:
    def __init__(self, program, inputs=None):
        self.program = program[:]
        self.inputs = collections.deque(inputs[:] if inputs is not None else [])
        self.outputs = []
        self.pc = 0
        self.halted = False

    def needs_input(self):
        return self.program[self.pc]%100 == INPUT and len(self.inputs) == 0

    
    def send(self, x):
        """
        add x to the input queue.
        """
        self.inputs.appendleft( x)

    def tick(self):
        """
        Advance state by one instruction.
        If an output opcode is executed, return its result; otherwise, return None.
        """
        advance_pc = True
        mode, opcode = divmod(self.program[self.pc], 100)
        if opcode not in num_params:
            raise Exception(f"Unrecognized opcode {opcode}")

        params = [self.program[self.pc+1+i] for i in range(num_params[opcode])]
        modes = [(mode // (10**i))%10 for i in range(num_params[opcode])]

        fetch = lambda x: params[x] if modes[x] == IMMEDIATE else self.program[params[x]]

        output = None

        if opcode == ADD:
            self.program[params[2]] = fetch(0) + fetch(1)
        elif opcode == MUL:
            self.program[params[2]] = fetch(0) * fetch(1)
        elif opcode == INPUT:
            self.program[params[0]] = self.inputs.pop()
        elif opcode == OUTPUT:
            output = self.program[params[0]]
            self.outputs.append(output)
        elif opcode == JUMP_IF_TRUE:
            if fetch(0) != 0:
                self.pc = fetch(1)
                advance_pc = False
        elif opcode == JUMP_IF_FALSE:
            if fetch(0) == 0:
                self.pc = fetch(1)
                advance_pc = False
        elif opcode == LESS_THAN:
            self.program[params[2]] = 1 if fetch(0) < fetch(1) else 0
        elif opcode == EQUALS:
            self.program[params[2]] = 1 if fetch(0) == fetch(1) else 0
        elif opcode == HALT:
            self.halted = True
            return
        else:
            raise Exception(f"opcode {opcode} not implemented yet.")

        if advance_pc:
            self.pc += 1 + num_params[opcode]

        return output

def load(filename):
    with open(filename) as file:
        return [int(x) for x in re.findall("-?\d+", file.read())]

def execute(program, inputs):
    computer = Computer(program, inputs)
    while not computer.halted:
        computer.tick()
    return computer.outputs