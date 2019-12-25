import intcomputer as ic
import json
import sys
import os
import re

SAVE_FILENAME = "game.sav"

def ask(prompt):
    while True:
        x = input(prompt)
        if x.lower() in ("y", "yes"):
            return True
        elif x.lower() in ("n", "no"):
            return False
        else:
            print("Sorry, I didn't understand that response.")

def load():
    with open(SAVE_FILENAME) as file:
        return ic.Computer.loads(file.read())

def play():
    if os.path.exists(SAVE_FILENAME) and ask("Load previous save? "):
        computer = load()
    else:
        computer = ic.Computer(ic.load("input"))

    while True:
        if computer.needs_input():
            command = input()
            if command == "save":
                with open(SAVE_FILENAME, "w") as file:
                    file.write(computer.dumps())
                print("Saved. Command?")
            else:
                command = command + "\n"
                for c in command:
                    computer.send(ord(c))
        else:
            x = computer.tick()
            if x is not None:
                print(chr(x), end="")
                sys.stdout.flush()

def iter_subsets(seq):
    if len(seq) == 0:
        yield []
    else:
        for right in iter_subsets(seq[1:]):
            yield right
            yield [seq[0]] + right

all_items = ["pointer", "mutex", "asterisk", "space law space brochure", "monolith", "mouse", "food ration", "sand"]
def try_loadout(items):
    to_drop = set(all_items) - set(items)
    commands = [f"drop {item}\n" for item in to_drop]

    #only works if you have a saved game where you are carrying all safe inventory items, and are standing to the west of the security checkpoint.
    computer = load() 
    computer.send_str("".join(commands))
    while not computer.needs_input(): 
        computer.tick()
    computer.send_str("east\n")

    computer.outputs.clear()
    time = 0
    while not computer.needs_input():
        computer.tick()
        time += 1
        if time > 100000:
            break

    output = "".join(chr(x) for x in computer.outputs)
    
    if m := re.search(f"get in by typing (\d+) on the keypad", output):
        return int(m.group(1))
    elif m := re.search(r"Alert! Droids on this ship are (.*?) than the detected value!", output):
        return m.group(1)
    else:
        raise Exception(f"Can't parse response {repr(output)}")

for inv in iter_subsets(all_items):
    result = try_loadout(inv)
    if isinstance(result, int):
        print(result)
        break