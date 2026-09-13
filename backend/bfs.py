from collections import deque


def bfs(graph, start):
    if start not in graph.nodes:
        raise ValueError(f"Start node '{start}' does not exist.")

    visited = set()
    queue = deque([start])
    states = []
    traversal = []

    visited.add(start)

    while queue:
        current = queue.popleft()
        traversal.append(current)

        states.append({
            "step": len(states) + 1,
            "current": current,
            "visited": list(traversal),
            "queue": list(queue)
        })

        for neighbor in graph.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return {
        "algorithm": "BFS",
        "start": start,
        "traversal": traversal,
        "states": states
    }