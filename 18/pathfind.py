from collections import defaultdict
from pq import PriorityQueue as PQ

def reconstruct_path(node, parents):
    result = []
    while node is not None:
        result.append(node)
        node = parents[node]
    return list(reversed(result))

def djikstra(start, neighbor_func, distance_func, goal_pred):
    visited = set()

    parents = {start: None}

    distances = {start: 0}
    queue = PQ()
    queue.add_task(start, distances[start])

    while not queue.empty():
        current = queue.pop_task()
        for neighbor in neighbor_func(current):
            if neighbor in visited:
                continue
            tentative_distance = distances[current] + distance_func(current, neighbor)
            if neighbor not in distances:
                queue.add_task(neighbor, tentative_distance)
                distances[neighbor] = tentative_distance
                parents[neighbor] = current
            elif tentative_distance < distances[neighbor]:
                queue.update_task(neighbor, tentative_distance)
                distances[neighbor] = tentative_distance
                parents[neighbor] = current
        visited.add(current)
        if goal_pred(current):
            return {"distance": distances[current], "path": reconstruct_path(current, parents), "parents": parents}

    return {"distance": float("inf"), "path": None, "parents": parents}