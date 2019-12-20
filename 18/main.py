from geometry import Point
from pathfind import djikstra

up, down, left, right = Point(0,-1), Point(0,1), Point(-1,0), Point(1,0)

field = {}
parents = {}

def path_to_start(p):
    result = []
    while p is not None:
        result.append(p)
        p = parents[p]
    return result

def path_between(a,b):
    a_path = path_to_start(a)
    b_path = path_to_start(b)
    assert a_path and b_path and a_path[-1] == b_path[-1], f"path between {a} and {b} fails preconditions"
    while a_path and b_path and a_path[-1] == b_path[-1]:
        x = a_path.pop()
        b_path.pop()
    a_path.append(x)
    a_path.extend(reversed(b_path))
    return a_path

def get_immediate_neighbors(state):
    immediate_neighbors = []
    landmark, keys_collected = state
    for key in keys.keys():
        if key in keys_collected:
            continue
        if all(obstacle.lower() in keys_collected for obstacle in graph[landmark, key][1]):
            neighbor = (key, keys_collected+(key,))
            immediate_neighbors.append(neighbor)
    return immediate_neighbors

def distance(state_a, state_b):
    path = path_between(landmarks[state_a[0]], landmarks[state_b[0]])
    return len(path)-1

def shortest_tour(cur, keys_collected=None):
    raise Exception("Deprecated")
#    print(f"shortest_tour({cur}, {keys_collected})")
    if keys_collected is None:
        keys_collected = (cur,)
    #find all immediate neighbors of the current landmark.
    #this is any key that can be reached from this landmark without crossing through a locked door or an uncollected key.
    immediate_neighbors = []
    for key in keys.keys():
        if key in keys_collected: 
            continue
        if all(obstacle.lower() in keys_collected for obstacle in graph[cur, key][1]):
            immediate_neighbors.append(key)

#    print(f"Immediate neighbors of {cur} when holding {keys_collected}: {immediate_neighbors}")

    if not immediate_neighbors:
        #nothing left to collect, so I guess we're done.
        return 0

    return min(graph[cur, key][0] + shortest_tour(key, keys_collected + (key,)) for key in immediate_neighbors)        

with open("sample4") as file:
    for j, line in enumerate(file):
        for i, c in enumerate(line.strip()):
            field[Point(i,j)] = c

#coordinates of all keys and the starting point
landmarks = {v:k for k,v in field.items() if v not in ".#" and not v.isupper()}
keys = {k:v for k,v in landmarks.items() if k.islower()}

start = landmarks["@"]
parents[start] = None
to_visit = {start}
while to_visit:
    to_visit_next = set()
    for p in to_visit:
        for delta in (up, down, left, right):
            neighbor = p + delta
            if neighbor not in parents:
                parents[neighbor] = p
                if field[neighbor] != "#":
                    to_visit_next.add(neighbor)
    to_visit = to_visit_next


#fully connected graph that indicates the distance between landmarks, and the obstacles between them
#where an "obstacle" can be a door or a key.
graph = {}

for a in landmarks.keys():
    for b in landmarks.keys():
        if a == b: continue
        obstacles = []
        path = path_between(landmarks[a],landmarks[b])
        for p in path[1:-1]:
            if field[p] not in ".#@":
                obstacles.append(field[p])
        graph[a,b] = (len(path)-1, obstacles)
        graph[b,a] = (len(path)-1, obstacles)


#use djikstra's algorithm to find the best path through the maze.
#each node in the graph being searched is a (landmark, keys_collected) tuple.
#the distance between nodes is equal to the number of steps required to get from one state to the next.
print(djikstra(
    start= ("@", ("@",)),
    neighbor_func = get_immediate_neighbors,
    distance_func = distance,
    goal_pred = lambda state: len(state[1]) == 1+len(keys)
))