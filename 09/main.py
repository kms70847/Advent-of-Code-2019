import intcomputer

program = intcomputer.load("input")
print(intcomputer.Computer(program, [1]).tick_until_output())
print(intcomputer.Computer(program, [2]).tick_until_output())