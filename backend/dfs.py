def dfs(graph, start):
    if start not in graph.nodes:
        raise ValueError(f"Start node '{start}' does not exist.")

    visited = set()
    traversal = []
    states = []

    def visit(node):
        visited.add(node)
        traversal.append(node)

        states.append({
            "step": len(states) + 1,
            "current": node,
            "visited": list(traversal),
            "backtracking": False
        })

        for neighbor in graph.get_neighbors(node):
            if neighbor not in visited:
                visit(neighbor)

        states.append({
            "step": len(states) + 1,
            "current": node,
            "visited": list(traversal),
            "backtracking": True
        })

    visit(start)

    return {
        "algorithm": "DFS",
        "start": start,
        "traversal": traversal,
        "states": states
    }