import intcomputer as ic


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
    " * 1": "",
    "1 * ": "",
    " + 0": "",
    "0 + ": "",
    "+ -": "- ",
}

mode_reprs = {
    ic.POSITION: "state[{}]",
    ic.IMMEDIATE: "{}",
    ic.RELATIVE: "state[relative_base + {}]"
}

def looks_like_instruction(opcode, mode):
    return opcode in ic.num_params and (mode==0 or len(str(mode)) <= ic.num_params[opcode])

def format_instruction(opcode, modes, params):
    formatted_params = [mode_reprs[mode].format(param) for mode, param in zip(modes, params)]
    line = opcode_reprs[opcode].format(*formatted_params)
    for k,v in peephole_optimizations.items():
        line = line.replace(k,v)
    return line
    

def looks_terminal(opcode, modes, params):
    if opcode == ic.HALT:
        return True
    if opcode == ic.JUMP_IF_TRUE and modes[0] == ic.IMMEDIATE and params[0] == 1:
        return True
    if opcode == ic.JUMP_IF_FALSE and modes[0] == ic.IMMEDIATE and params[0] == 0:
        return True
    return False

def dis(program, probable_data_ranges = None):
    if probable_data_ranges is None:
        probable_data_ranges = []
    pc = 0
    while pc < len(program):
        mode, opcode = divmod(program[pc], 100)
        if looks_like_instruction(opcode, mode) and not any(a <= pc < b for a,b in probable_data_ranges):
            modes = [(mode // (10**i))%10 for i in range(ic.num_params[opcode])]
            params = program[pc+1: pc+1+ic.num_params[opcode]]
            line = format_instruction(opcode, modes, params)
            line = f"{str(program[pc:pc+1+ic.num_params[opcode]]).strip('[]'):30} #{pc:4}: {line}"
            print(line)
            if looks_terminal(opcode, modes, params):
                print("\n")
            pc += 1 + len(params)
            #actual command
        else:
            line = f"{str(program[pc]) + ',':30} #{pc:4} (data)"
            print(line)
            pc += 1

data_ranges = (
    (639, float("inf")),
    (379, 393),
)
program = ic.load("input")
dis(program, data_ranges)