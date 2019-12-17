import intcomputer as ic
for x in (1,5):
    print(ic.Computer(ic.load("input"), [x]).tick_until_blocked()[-1])