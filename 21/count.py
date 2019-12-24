import sys
import re
from collections import Counter

if len(sys.argv) < 2:
    print("Please supply a pattern.")
    exit()
pattern = re.compile(sys.argv[1])
with open("dis.txt") as file:
    data = file.read()

c = Counter(pattern.findall(data))
for k,v in c.most_common():
    if v == 1:
        break
    print(k,v)

# >>> [chr(x) for x in [65, 79, 78, 87, 82]]
# ['A', 'O', 'N', 'W', 'R']