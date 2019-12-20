import functools
import sys

import pathfind
from geometry import Point

up, down, left, right = Point(0,-1), Point(0,1), Point(-1,0), Point(1,0)

def solve(field):
    def get_immediate_neighbors(state):
        immediate_neighbors = []
        landmarks, keys_collected = state
        for landmark in landmarks:
            for key in keys.keys():
                if key in keys_collected:
                    continue
                if (landmark, key) not in graph:
                    continue
                if all(obstacle.lower() in keys_collected for obstacle in graph[landmark, key][1]):
                    neighbor = (landmarks.replace(landmark, key), "".join(sorted(keys_collected+key)))
                    immediate_neighbors.append(neighbor)
        return immediate_neighbors

    def get_paths_to_landmarks(p):
        """
        find the distance from the given position to every landmark in the field.
        """
        parents = pathfind.djikstra(
            start= p,
            neighbor_func = lambda p: [n for n in [p+delta for delta in [up, down, left, right]] if field[n] not in "#"],
            distance_func = lambda a, b: 1,
            goal_pred = lambda p: None
        )["parents"]

        results = {}
        for k, k_pos in landmarks.items():
            if k_pos in parents:
                results[k] = pathfind.reconstruct_path(k_pos, parents)
        return results


    def distance(state_a, state_b):
        #determine which bot moved between these states
        for a,b in zip(state_a[0], state_b[0]):
            if a != b:
                break
        else:
            raise Exception(f"No apparent movement between {state_a} and {state_b}")
        return graph[a,b][0]

    bot_symbols = "".join(v for v in field.values() if not v.isalpha() and v not in ".#")

    #coordinates of all keys and the starting point
    landmarks = {v:k for k,v in field.items() if v not in ".#" and not v.isupper()}

    #coordiantes of just keys
    keys = {k:v for k,v in landmarks.items() if k.islower()}

    #undirected graph that indicates the distance between landmarks, and the obstacles between them,
    #where an "obstacle" can be a door or a key.
    graph = {}

    for a, a_pos in landmarks.items():
        paths = get_paths_to_landmarks(a_pos)
        for b, b_pos in landmarks.items():
            if a == b: continue
            obstacles = []
            if b in paths:
                path = paths[b]
                for p in path[1:-1]:
                    if field[p] not in ".#" + bot_symbols:
                        obstacles.append(field[p])
                graph[a,b] = (len(path)-1, obstacles)
                graph[b,a] = (len(path)-1, obstacles)


    #use djikstra's algorithm to find the best path through the maze.
    #each node in the graph being searched is a (landmarks, keys_collected) tuple.
    #the distance between nodes is equal to the number of steps required to get from one state to the next.
    print(pathfind.djikstra(
        start= (bot_symbols, bot_symbols),
        neighbor_func = get_immediate_neighbors,
        distance_func = distance,
        goal_pred = lambda state: len(state[1]) == len(bot_symbols) + len(keys)
    )["distance"])


field = {}
with open("input") as file:
    for j, line in enumerate(file):
        for i, c in enumerate(line.strip()):
            field[Point(i,j)] = c
#part 1
solve(field)

#part 2
p = next(k for k,v in field.items() if v == "@")

#the problem description uses four @ symbols for its bots, but my code assumes all landmarks have unique characters,
#so I'll assign "!$&" to the other bots.
s = """
@#!
###
$#&
""".strip()
for dy, line in enumerate(s.split("\n"), -1):
    for dx, c in enumerate(line, -1):
        field[p + Point(dx,dy)] = c

solve(field)