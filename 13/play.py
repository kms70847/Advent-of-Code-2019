import tkinter
import intcomputer as ic

booted = False

def update():
    print(computer.halted, computer.needs_input())
    global booted
    while True:
        if not (computer.halted or computer.needs_input()):
            x, y, value = [computer.tick_until_output() for _ in range(3)]
            if x is None: 
                print("Done?"); 
                break
            if x== -1 and y == 0:
                print("Score:", value)
                booted = True
                break
            color = ["white", "black", "red", "green", "blue"][value]
            canvas.itemconfig(cell_ids[x,y], fill=color)
        if booted: break
        print(".")
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