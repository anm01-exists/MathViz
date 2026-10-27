"""Convert a teammate's result format into the animation schema."""

from copy import deepcopy


def convert_teammate_format(data: dict) -> dict:
    """Convert teammate's result format to animation schema."""
    import math

    algo = str(data.get("algorithm", "")).lower()
    start = data.get("start")
    destination = data.get("destination") or data.get("target")
    traversal = data.get("traversal", [])
    distances = data.get("distances", {})
    path = data.get("path", [])
    their_states = data.get("states", [])

    if "dijkstra" in algo:
        if not start or not distances:
            raise ValueError("Dijkstra input needs 'start' and 'distances'")

        nodes = [{"id": k} for k in distances.keys()]
        edges = []
        for i in range(len(path) - 1):
            edges.append({"source": path[i], "target": path[i+1]})
            edges.append({"source": path[i+1], "target": path[i]})

        parent = {}
        for i in range(1, len(path)):
            parent[path[i]] = path[i-1]

        sorted_nodes = sorted(distances.keys(), key=lambda k: distances[k] if distances[k] is not None else float('inf'))

        states = []
        step = 0

        states.append({
            "step": step,
            "event": "init",
            "current": None,
            "visited": [],
            "finalized": [],
            "frontier": sorted_nodes,
            "distances": {k: (None if v is None else float(v)) for k, v in distances.items()},
            "parent": {},
            "selected_edges": [],
            "final_path": [],
            "message": f"Init: dist({start})=0, rest=∞"
        })
        step += 1

        visited = []
        finalized = []
        for node in sorted_nodes:
            if node not in distances or distances[node] is None:
                continue
            visited.append(node)
            finalized.append(node)
            frontier = [n for n in sorted_nodes if n not in finalized]
            current_edges = []
            if node in parent:
                current_edges.append([parent[node], node])
            states.append({
                "step": step,
                "event": "finalize",
                "current": node,
                "visited": deepcopy(visited),
                "finalized": deepcopy(finalized),
                "frontier": frontier,
                "distances": {k: (None if v is None else float(v)) for k, v in distances.items()},
                "parent": deepcopy(parent),
                "current_edge": {"source": parent[node], "target": node} if node in parent else None,
                "selected_edges": [list(e) for e in zip(path[:-1], path[1:])],
                "final_path": deepcopy(path) if node == destination else [],
                "message": f"Settle {node} (dist={distances[node]})" + (f" = target" if node == destination else "")
            })
            step += 1
            if destination and node == destination:
                break

        states.append({
            "step": step,
            "event": "path_found",
            "current": None,
            "visited": deepcopy(visited),
            "finalized": deepcopy(finalized),
            "frontier": [],
            "distances": {k: (None if v is None else float(v)) for k, v in distances.items()},
            "parent": deepcopy(parent),
            "selected_edges": [list(e) for e in zip(path[:-1], path[1:])],
            "final_path": deepcopy(path),
            "message": f"Shortest path {' -> '.join(path)}, cost {distances.get(destination, '?')}"
        })

        return {
            "algorithm": "dijkstra",
            "start": start,
            "target": destination,
            "graph": {"directed": False, "weighted": True, "nodes": nodes, "edges": edges},
            "states": states
        }

    elif "dfs" in algo:
        if not start or not traversal:
            raise ValueError("DFS input needs 'start' and 'traversal'")

        nodes = [{"id": n} for n in traversal]
        edges = []
        for i in range(len(traversal) - 1):
            edges.append({"source": traversal[i], "target": traversal[i+1]})
            edges.append({"source": traversal[i+1], "target": traversal[i]})

        states = []
        visited = []
        parent = {}

        if their_states:
            for i, s in enumerate(their_states):
                current = s.get("current")
                backtracking = s.get("backtracking", False)

                if current and current not in visited:
                    visited.append(current)
                    idx = traversal.index(current) if current in traversal else -1
                    if idx > 0:
                        parent[current] = traversal[idx - 1]

                event = "backtrack" if backtracking else "visit"
                frontier = [n for n in traversal if n not in visited]

                states.append({
                    "step": i,
                    "event": event,
                    "current": current,
                    "visited": deepcopy(visited),
                    "frontier": frontier,
                    "parent": deepcopy(parent),
                    "current_edge": [parent[current], current] if current in parent else None,
                    "selected_edges": [list(e) for e in zip(traversal[:-1], traversal[1:])][:len(visited)],
                    "final_path": deepcopy(traversal) if i == len(their_states) - 1 else [],
                    "message": s.get("message", f"{event.capitalize()} {current}" if current else "Done")
                })
        else:
            for i, node in enumerate(traversal):
                visited.append(node)
                if i > 0:
                    parent[node] = traversal[i-1]
                states.append({
                    "step": i,
                    "event": "visit",
                    "current": node,
                    "visited": deepcopy(visited),
                    "frontier": traversal[i+1:],
                    "parent": deepcopy(parent),
                    "current_edge": [parent[node], node] if node in parent else None,
                    "selected_edges": [list(e) for e in zip(traversal[:i], traversal[1:i+1])],
                    "final_path": deepcopy(traversal) if i == len(traversal) - 1 else [],
                    "message": f"Visit {node}"
                })
            states.append({
                "step": len(traversal),
                "event": "done",
                "current": None,
                "visited": deepcopy(visited),
                "frontier": [],
                "parent": deepcopy(parent),
                "selected_edges": [list(e) for e in zip(traversal[:-1], traversal[1:])],
                "final_path": deepcopy(traversal),
                "message": f"DFS complete. Order: {' -> '.join(traversal)}"
            })

        return {
            "algorithm": "dfs",
            "start": start,
            "graph": {"directed": False, "weighted": False, "nodes": nodes, "edges": edges},
            "states": states
        }

    elif "bfs" in algo:
        if not start or not traversal:
            raise ValueError("BFS input needs 'start' and 'traversal'")

        nodes = [{"id": n} for n in traversal]
        edges = []
        for i in range(len(traversal) - 1):
            edges.append({"source": traversal[i], "target": traversal[i+1]})
            edges.append({"source": traversal[i+1], "target": traversal[i]})

        states = []
        visited = []
        parent = {}

        if their_states:
            for i, s in enumerate(their_states):
                current = s.get("current")
                their_visited = s.get("visited", [])
                their_queue = s.get("queue", [])

                if current and current not in visited:
                    visited.append(current)
                    idx = traversal.index(current) if current in traversal else -1
                    if idx > 0:
                        parent[current] = traversal[idx - 1]

                queue = [n for n in their_queue if n not in visited] + [n for n in traversal if n not in visited and n not in their_queue]

                states.append({
                    "step": i,
                    "event": "visit" if current else "init",
                    "current": current,
                    "visited": deepcopy(visited),
                    "frontier": queue,
                    "parent": deepcopy(parent),
                    "current_edge": [parent[current], current] if current and current in parent else None,
                    "selected_edges": [list(e) for e in zip(traversal[:len(visited)-1], traversal[1:len(visited)])],
                    "final_path": deepcopy(traversal) if i == len(their_states) - 1 else [],
                    "message": f"Visit {current}" if current else "Start BFS"
                })
        else:
            queue = [start]
            for i, node in enumerate(traversal):
                if node in queue:
                    queue.remove(node)
                visited.append(node)
                if i > 0:
                    parent[node] = traversal[i-1]
                queue.extend([n for n in traversal[i+1:] if n not in visited and n not in queue])
                states.append({
                    "step": i,
                    "event": "visit",
                    "current": node,
                    "visited": deepcopy(visited),
                    "frontier": deepcopy(queue),
                    "parent": deepcopy(parent),
                    "current_edge": [parent[node], node] if node in parent else None,
                    "selected_edges": [list(e) for e in zip(traversal[:len(visited)-1], traversal[1:len(visited)])],
                    "final_path": deepcopy(traversal) if i == len(traversal) - 1 else [],
                    "message": f"Dequeue {node}. Visit {node}"
                })
            states.append({
                "step": len(traversal),
                "event": "done",
                "current": None,
                "visited": deepcopy(visited),
                "frontier": [],
                "parent": deepcopy(parent),
                "selected_edges": [list(e) for e in zip(traversal[:-1], traversal[1:])],
                "final_path": deepcopy(traversal),
                "message": f"BFS complete. Order: {' -> '.join(traversal)}"
            })

        return {
            "algorithm": "bfs",
            "start": start,
            "graph": {"directed": False, "weighted": False, "nodes": nodes, "edges": edges},
            "states": states
        }

    else:
        raise ValueError(f"Unknown algorithm: {data.get('algorithm')}")