import intcomputer as ic
import re
import sys

ASUSME_RELATIVE_CALL_STACK_IDIOM = True

opcode_names = {int((t:=line.split(" = "))[1]): t[0] for line in """ADD = 1
MUL = 2
INPUT = 3
OUTPUT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUALS = 8
ADJUST_RELATIVE_BASE = 9
HALT = 99""".split("\n")}

opcode_reprs = {
    ic.ADD: "{2} = {0} + {1}",
    ic.MUL: "{2} = {0} * {1}",
    ic.INPUT: "{0} = input()",
    ic.OUTPUT: "print({0})",
    ic.JUMP_IF_TRUE: "if {0}: GOTO {1}",
    ic.JUMP_IF_FALSE: "if not {0}: GOTO {1}",
    ic.LESS_THAN: "{2} = {0} < {1}",
    ic.EQUALS: "{2} = {0} == {1}",
    ic.ADJUST_RELATIVE_BASE: "relative_base += {0}",
    ic.HALT: "exit()"
}

peephole_optimizations = {
    "if 1: ": "",
    "if not 0: ": "",
    "+= -": "-= ",
    #reduce addition / multiplication identities, e.g `1 * x`, `y + 0`, to reduced form, e.g. `x`, `y`.
    #use word boundaries to ensure that `q * 10` and `10 + z` don't get reduced to `q0` and `1z`
    re.compile(re.escape(" * 1") + r"\b"): "",
    re.compile(r"\b" + re.escape("1 * ")): "",
    re.compile(re.escape(" + 0") + r"\b"): "",
    re.compile(r"\b" + re.escape("0 + ")): "",
    "+ -": "- ",
}

mode_reprs = {
    ic.POSITION: "state[{}]",
    ic.IMMEDIATE: "{}",
    ic.RELATIVE: "state[relative_base + {}]"
}

def looks_terminal(opcode, modes, params):
    return opcode == ic.HALT or looks_like_unconditional_jump(opcode, modes, params)

def looks_like_unconditional_jump(opcode, modes, params):
    if opcode == ic.JUMP_IF_TRUE and modes[0] == ic.IMMEDIATE and params[0] == 1:
        return True
    if opcode == ic.JUMP_IF_FALSE and modes[0] == ic.IMMEDIATE and params[0] == 0:
        return True
    return False

class InstructionParseError(Exception):
    pass

class Instruction:
    def __init__(self, opcode, modes, params, address):
        self.opcode = opcode
        self.modes = modes
        self.params = params
        self.address = address

    def is_unconditional_jump(self):
        if self.opcode == ic.JUMP_IF_TRUE and self.modes[0] == ic.IMMEDIATE and self.params[0] == 1:
            return True
        if self.opcode == ic.JUMP_IF_FALSE and self.modes[0] == ic.IMMEDIATE and self.params[0] == 0:
            return True
        return False

    def is_jump(self):
        return self.opcode in (ic.JUMP_IF_TRUE, ic.JUMP_IF_FALSE)

    def is_terminal(self):
        return self.opcode == ic.HALT or self.is_unconditional_jump()

    def looks_like_call(self):
        """
        return True if this instruction appears to be doing `state[relative_base] = ...`.
        For programs that follow the "relative call stack" idiom, this instruction means that a function call is about to occur,
        And afterwards execution will jump back to the instruction 7 values down.
        """

        #this approach doesn't work because the operators could be in a didfferent order, or the operator could be ADD
        #return self.opcode == ic.MUL and self.modes == [1,1,2] and self.params[0] == self.address + 7

        return bool(re.search(r"state\[relative_base\] = \d+", self.format()))

    def direct_descendants(self):
        """
        Return a list of addresses that the program may execute after this one.
        Not bulletproof; identifying exactly and only all real descendants would require solving the halting problem.
        For example, this function will return [] for an unconditional jump whose target is specified in a non-immediate mode.
        """
        results = []
        #everything but halt and unconditional jump can potentially lead to the instruction immediately following it
        if not self.is_terminal():
            results.append(self.address + 1 + len(self.params))

        if self.is_jump() and self.modes[1] == ic.IMMEDIATE:
            results.append(self.params[1])

        if ASUSME_RELATIVE_CALL_STACK_IDIOM and self.looks_like_call():
            #probably pushing the return address onto the stack for a subsequent function call.
            #`state[relative_base] = addr` can be done with either a MUL or ADD instruction, with parameters in any order,
            #so finding the address is easier after formatting with peephole optimizations.
            addr = int(self.format().split(" = ")[1])
            results.append(addr)
    
        return results

    def format(self):
        formatted_params = [mode_reprs[mode].format(param) for mode, param in zip(self.modes, self.params)]
        line = opcode_reprs[self.opcode].format(*formatted_params)
        for k,v in peephole_optimizations.items():
            if isinstance(k, str):
                line = line.replace(k,v)
            else: #must be a re.compile object
                line = k.sub(v, line)
        return line

    @staticmethod
    def from_program(program, pc):
        
        mode, opcode = divmod(program[pc], 100)
        if opcode not in ic.num_params:
            raise InstructionParseError(f"Unrecognized opcode {opcode}")
        if mode != 0 and len(str(mode)) > ic.num_params[opcode]:
            raise InstructionParseError(f"expected {ic.num_params[opcode]} modes, got {len(str(mode))}")
        modes = [(mode // (10**i))%10 for i in range(ic.num_params[opcode])]
        if any(mode not in {ic.POSITION, ic.IMMEDIATE, ic.RELATIVE} for mode in modes):
            raise InstructionParseError(f"unrecognized addressing modes {modes}")
        params = program[pc+1: pc+1+ic.num_params[opcode]]
        return Instruction(opcode, modes, params, pc)


def dis(program, decompile_reachable_only=False):

    #identify which instructions are reachable from the beginning of the program.
    if decompile_reachable_only:
        seen = set()
        to_visit = set()
        to_visit.add(0)

        while to_visit:
            pc = to_visit.pop()
            instruction = Instruction.from_program(program, pc)
            seen.add(pc)

            #determine which addresses are reachable from here
            for addr in instruction.direct_descendants():
                if addr not in seen:
                    to_visit.add(addr)
    else:
        seen = set()
        for pc in range(len(program)):
            try:
                Instruction.from_program(program, pc)
                seen.add(pc)
            except InstructionParseError:
                pass

    pc = 0
    while pc < len(program):
        if pc in seen:
            instruction = Instruction.from_program(program, pc)
            line = instruction.format()
            line = f"{str(program[pc:pc+1+len(instruction.params)]).strip('[]'):30} #{pc:4}: {line}"
            print(line)
            if instruction.is_terminal():
                print("\n")
            pc += 1 + len(instruction.params)
        else:
            line = f"{str(program[pc]) + ',':30} #{pc:4} (data)"
            print(line)
            pc += 1

if __name__ == "__main__":
    filename = "input" if len(sys.argv) < 2 else sys.argv[1]
    program = ic.load(filename)
    dis(program)