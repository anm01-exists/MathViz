import heapq


def dijkstra(graph, start, destination=None):
    if start not in graph.nodes:
        raise ValueError(f"Start node '{start}' does not exist.")

    if not graph.weighted:
        raise ValueError("Dijkstra requires a weighted graph.")

    if destination is not None and destination not in graph.nodes:
        raise ValueError(f"Destination node '{destination}' does not exist.")

    distances = {node: float("inf") for node in graph.nodes}
    previous = {node: None for node in graph.nodes}

    distances[start] = 0

    priority_queue = [(0, start)]
    states = []

    while priority_queue:
        current_distance, current = heapq.heappop(priority_queue)

        if current_distance > distances[current]:
            continue

        states.append({
            "step": len(states) + 1,
            "current": current,
            "distances": dict(distances),
            "previous": dict(previous)
        })

        if destination is not None and current == destination:
            break

        for neighbor, weight in graph.get_neighbors(current):
            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor)
                )

    path = []

    if destination is not None:
        if distances[destination] == float("inf"):
            path = []
        else:
            current = destination

            while current is not None:
                path.append(current)
                current = previous[current]

            path.reverse()

    return {
        "algorithm": "Dijkstra",
        "start": start,
        "destination": destination,
        "distances": distances,
        "path": path,
        "states": states
    }