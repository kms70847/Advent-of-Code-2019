from collections import defaultdict
from pq import PriorityQueue as PQ

def djikstra(start, neighbor_func, distance_func, goal_pred):
    visited = set()

    distances = {start: 0}
    queue = PQ()
    queue.add_task(start, distances[start])

    while True:
        current = queue.pop_task()
        for neighbor in neighbor_func(current):
            if neighbor in visited:
                continue
            tentative_distance = distances[current] + distance_func(current, neighbor)
            if neighbor not in distances:
                queue.add_task(neighbor, tentative_distance)
                distances[neighbor] = tentative_distance
            elif tentative_distance < distances[neighbor]:
                queue.update_task(neighbor, tentative_distance)
                distances[neighbor] = tentative_distance
        visited.add(current)
        if goal_pred(current):
            return distances[current]