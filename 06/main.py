from collections import defaultdict
import itertools

children = defaultdict(list)
parents = {"COM": None}
with open("input") as file:
    for line in file:
        parent, child = line.strip().split(")")
        children[parent].append(child)
        parents[child] = parent

def orbits(node, depth=0):
    return depth + sum(orbits(child, depth+1) for child in children[node])

def ancestors(node):
    """
    find all elements in the tree directly between the node and the root.
    the root appears first in the output, and the node appears last.
    """
    result = []
    while node is not None:
        result.append(node)
        node = parents[node]
    return result[::-1]

my_path = ancestors("YOU")
santa_path = ancestors("SAN")
num_common_ancestors = sum(1 for a,b in zip(my_path, santa_path) if a == b)
print(len(my_path) + len(santa_path) - 2*num_common_ancestors - 2)