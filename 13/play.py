import tkinter
import intcomputer as ic

AUTOMATIC_CONTROL = True
booted = False

ball_x = None
paddle_x = None

def cmp(a,b):
    if a < b: return -1
    elif a == b: return 0
    else: return 1

def update():
    global booted
    global ball_x
    global paddle_x
    while True:
        if computer.needs_input() and AUTOMATIC_CONTROL:
            computer.send(cmp(ball_x, paddle_x))
        if not (computer.halted or computer.needs_input()):
            x, y, value = [computer.tick_until_output() for _ in range(3)]
            if x is None: #probably needs input again
                break
            if x== -1 and y == 0:
                print("Score:", value)
                booted = True
                break
            if value == 3: paddle_x = x
            if value == 4: ball_x = x
            color = ["white", "black", "red", "green", "blue"][value]
            canvas.itemconfig(cell_ids[x,y], fill=color)
        if booted: break
    root.after(10, update)

program = ic.load("input")
program[0] = 2
computer = ic.Computer(program)

root = tkinter.Tk()

cols = 46
rows = 24
cell_size = 10

canvas = tkinter.Canvas(root, width=cell_size*cols, height=cell_size*rows)
canvas.pack()

cell_ids = {}
for i in range(cols):
    for j in range(rows):
        id = canvas.create_rectangle(i*cell_size, j*cell_size, (i+1)*cell_size, (j+1)*cell_size, outline="gray", fill="white")
        cell_ids[i,j] = id

button_frame = tkinter.Frame(root)
button_frame.pack()
tkinter.Button(button_frame, text="left", command=lambda: computer.send(-1)).grid(row=0,column=0)
tkinter.Button(button_frame, text="==", command=lambda: computer.send(0)).grid(row=0,column=1)
tkinter.Button(button_frame, text="right", command=lambda: computer.send(1)).grid(row=0,column=2)

root.after(10, update)
root.mainloop()