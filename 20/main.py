from geometry import Point
import pathfind

up, down, left, right = Point(0,-1), Point(0,1), Point(-1,0), Point(1,0)

def get_neighbors(state):
    problem_part, depth, p = state

    results = []
    for delta in [up, down, left, right]:
        if field[p+delta] == ".":
            results.append((problem_part, depth, p+delta))
    if p in inner_warps:
        results.append((problem_part, depth+1, inner_warps[p]))
    if p in outer_warps:
        if problem_part == 1 or depth > 0:
            results.append((problem_part, depth-1, outer_warps[p]))
    return results

field = {}
with open("input") as file:
    for j, line in enumerate(file):
        for i, c in enumerate(line.strip("\n")):
            field[Point(i,j)] = c

#search for tagged coordinates
coord_tags = {}
for p, c in field.items():
    if c.isalpha():
        #found part of a tag. But we only care about the character directly adjacent to the walkable path.
        for delta in (up, down, left, right):
            if field.get(p+delta) == ".":
                #found tag's root.
                tag_name = "".join(sorted(c + field[p-delta]))
                coord_tags[p+delta] = tag_name

tag_coords = {}
for p, tag in coord_tags.items():
    tag_coords.setdefault(tag, []).append(p)

center = Point(
    max(p.x for p in field.keys())/2,
    max(p.y for p in field.keys())/2,
)

outer_warps = {} #warps that take you deeper into the maze
inner_warps = {} #warps that bring you closer to the entrance/exit layer of the maze
for tag, coords in tag_coords.items():
    if len(coords) == 2:
        a,b = coords
        #determine which of the pair is on the inner wall, and which is on the outer.
        #we could use manhattan or euclidean distance from center, but these might fail for mazes with large inner radii.
        #so let's try this instead.
        measure = lambda p: max(abs(p.x-center.x), abs(p.y-center.y))
        inner_p, outer_p = sorted((a,b), key=measure)
        outer_warps[outer_p] = inner_p
        inner_warps[inner_p] = outer_p

start = tag_coords["AA"][0]
end = tag_coords["ZZ"][0]

for problem_part in (1,2):
    x = pathfind.djikstra(
        start = (problem_part, 0, start), 
        neighbor_func = get_neighbors, 
        distance_func = lambda a,b: 1, 
        goal_pred = lambda state: state[2] == end and (problem_part == 1 or state[1] == 0)
    )
    print(x["distance"])