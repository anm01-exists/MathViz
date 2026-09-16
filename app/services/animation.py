"""Build animation-ready state lists from raw algorithm results.

These helpers translate Role-2 algorithm output (BFS/DFS/Dijkstra) and the user's
graph into the animation schema consumed by the Manim engine.
"""

from collections import deque


def _nid(neighbor):
    """Unwrap (node, weight) tuples returned by weighted adjacency."""
    return neighbor[0] if isinstance(neighbor, tuple) else neighbor


def _fmt_num(v):
    """Trim floats for captions: 3.0 -> 3, 0.5 -> 0.5."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return str(v)
    return str(int(f)) if f.is_integer() else str(round(f, 2))


def _bfs_parents(g, start):
    """Return (parent, children) maps from a BFS rooted at start."""
    parent = {start: None}
    children = {}
    seen = {start}
    q = deque([start])
    while q:
        u = q.popleft()
        for nb in g.get_neighbors(u):
            v = _nid(nb)
            if v not in seen:
                seen.add(v)
                parent[v] = u
                children.setdefault(u, []).append(v)
                q.append(v)
    return parent, children


def _dfs_parents(g, start):
    """Return (parent, children) maps from a DFS rooted at start."""
    parent = {start: None}
    children = {}
    seen = {start}

    def visit(u):
        for nb in g.get_neighbors(u):
            v = _nid(nb)
            if v not in seen:
                seen.add(v)
                parent[v] = u
                children.setdefault(u, []).append(v)
                visit(v)

    visit(start)
    return parent, children


def _tree_edges(parent, ordered):
    return [[parent[v], v] for v in ordered if parent.get(v)]


def _parent_map(parent):
    return {v: p for v, p in parent.items() if p is not None}


def _bfs_animation_states(role2_states, parent, children):
    final_visited = list(role2_states[-1]["visited"]) if role2_states else []
    states = []
    for i, s in enumerate(role2_states):
        cur = s["current"]
        visited = list(s["visited"])
        added = children.get(cur, [])
        if i == 0:
            msg = f"Start BFS at {cur} — queue: [{cur}]" + (f" → explore {', '.join(added)}" if added else "")
        elif added:
            msg = f"Dequeue {cur} → neighbours {', '.join(added)} join queue"
        else:
            msg = f"Dequeue {cur} → no new neighbours"
        states.append({
            "step": i,
            "event": "init" if i == 0 else "dequeue",
            "current": cur,
            "visited": visited,
            "frontier": list(s["queue"]),
            "parent": _parent_map(parent),
            "current_edge": {"source": parent[cur], "target": cur} if parent.get(cur) else None,
            "selected_edges": _tree_edges(parent, visited),
            "final_path": [],
            "message": msg,
        })
    states.append({
        "step": len(role2_states),
        "event": "done",
        "current": None,
        "visited": final_visited,
        "frontier": [],
        "parent": _parent_map(parent),
        "selected_edges": _tree_edges(parent, final_visited),
        "final_path": [],
        "message": f"BFS complete — order: {' → '.join(final_visited)}",
    })
    return states


def _dfs_animation_states(role2_states, parent, children, traversal):
    final_visited = list(role2_states[-1]["visited"]) if role2_states else []
    states = []
    for i, s in enumerate(role2_states):
        cur = s["current"]
        backtrack = s.get("backtracking", False)
        visited = list(s["visited"])
        if backtrack:
            msg = f"Backtrack from {cur} → no unvisited neighbours remain"
        elif parent.get(cur):
            msg = f"Visit {cur} (came from {parent[cur]})"
        else:
            msg = f"Visit {cur} (root of DFS)"
        states.append({
            "step": i,
            "event": "backtrack" if backtrack else "visit",
            "current": cur,
            "visited": visited,
            "frontier": [],
            "parent": _parent_map(parent),
            "current_edge": {"source": parent[cur], "target": cur} if (parent.get(cur) and not backtrack) else None,
            "selected_edges": _tree_edges(parent, visited),
            "final_path": [],
            "message": msg,
        })
    states.append({
        "step": len(role2_states),
        "event": "done",
        "current": None,
        "visited": final_visited,
        "frontier": [],
        "parent": _parent_map(parent),
        "selected_edges": _tree_edges(parent, final_visited),
        "final_path": [],
        "message": f"DFS complete — order: {' → '.join(traversal)}",
    })
    return states


def _dijkstra_animation_states(role2_states, node_ids, destination):
    settled = []
    states = []
    last_prev = {}
    last_dists = {}
    for i, s in enumerate(role2_states):
        cur = s["current"]
        if cur and cur not in settled:
            settled.append(cur)
        dists = s.get("distances", {})
        prev = s.get("previous", {})
        last_prev = prev
        last_dists = dists
        parent_live = {k: v for k, v in prev.items() if v}
        frontier = [n for n in node_ids if n not in settled and dists.get(n, float("inf")) != float("inf")]
        is_target = bool(destination) and cur == destination
        # Descriptive caption: settle cur, via predecessor, with edge weight.
        pred = prev.get(cur)
        if is_target:
            msg = f"Reached target {cur} (d={dists.get(cur)})"
        elif pred:
            w = None
            try:
                w = dists.get(cur) - dists.get(pred)
            except TypeError:
                pass
            extra = f" via {pred}" + (f" (edge {_fmt_num(w)})" if w is not None else "")
            msg = f"Settle {cur} (d={dists.get(cur)}){extra}"
        else:
            msg = f"Settle {cur} (d={dists.get(cur)}) — start node"
        states.append({
            "step": i,
            "event": "finalize",
            "current": cur,
            "visited": list(settled),
            "finalized": list(settled),
            "frontier": frontier,
            "distances": dists,
            "parent": parent_live,
            "current_edge": {"source": pred, "target": cur} if pred else None,
            "selected_edges": [[prev[v], v] for v in settled if prev.get(v)],
            "final_path": [],
            "message": msg,
        })
        if is_target:
            break
    return states, settled, last_prev, last_dists