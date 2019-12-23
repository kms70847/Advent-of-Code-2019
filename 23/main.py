import intcomputer as ic

computers = [ic.Computer(ic.load("input"), [i]) for i in range(50)]
output_bufs = [[] for _ in range(50)]

IDLE = 0
BUSY = 1

time = 0
idle_states = [BUSY for _ in range(50)]

part_one_answered = False

nat_x = None
nat_y = None
last_sent_y = None
while True:
    time += 1
    for idx, (computer, output_buf) in enumerate(zip(computers, output_bufs)):
        if computer.needs_input():
            computer.send(-1)
            if computer.program[61] == 1:
                idle_states[idx] = IDLE
        x = computer.tick()
        if x is not None:
            output_buf.append(x)
            if len(output_buf) == 3:
                pc, x,y = output_buf
                output_buf.clear()
                if pc == 255:
                    if not part_one_answered:
                        print(y)
                        part_one_answered = True
                    nat_x = x
                    nat_y = y
                else:
                    computers[pc].send(x)
                    computers[pc].send(y)
                    idle_states[pc] = BUSY
    if all(state == IDLE for state in idle_states):
        computers[0].send(nat_x)
        computers[0].send(nat_y)
        idle_states[0] = BUSY
        if nat_y == last_sent_y:
            print(nat_y)
            exit()
        last_sent_y = nat_y