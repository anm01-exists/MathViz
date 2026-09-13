"""Graph + state JSON contracts for the MathViz Manim engine.

These schemas are deliberately shared with Role 1 (frontend) and
Role 2 (algorithm engine) so all three layers speak the same language.

Graph JSON
----------
{
  "directed": false,          # bool, default False
  "weighted": false,          # bool, default False
  "nodes": [
    {"id": "A"},                          # minimal
    {"id": "B", "x": 1.0, "y": 0.5},      # optional manual position
    {"id": "C", "label": "C"}             # optional display label
  ],
  "edges": [
    {"source": "A", "target": "B"},            # unweighted
    {"source": "B", "target": "C", "weight": 4}  # weighted
  ]
}

Top-level animation input JSON
------------------------------
{
  "algorithm": "bfs",         # bfs | dfs | dijkstra | static
  "graph": { ... },           # graph object above (or graph inline at top level)
  "start": "A",               # optional start node
  "target": "E",              # optional destination (BFS/Dijkstra)
  "states": [ ... ]           # ordered state/event objects
}

State / event object (every field except step/event is optional;
the renderer tolerates missing fields so Role 2 can emit minimal states)
--------------------------------------------------------------------------
{
  "step": 0,
  "event": "init",            # init|visit|enqueue|dequeue|examine|relax|
                              # finalize|backtrack|push|pop|path_found|done|...
  "current": "A",             # node being processed now (or null)
  "visited": ["A"],           # nodes already visited / settled
  "frontier": ["B", "C"],     # queue (BFS) / stack (DFS) / frontier set
                              # aliases accepted: queue, stack, frontier_nodes
  "distances": {"A": 0, "B": 4, "C": null},  # Dijkstra only (null = inf)
  "parent": {"B": "A", "C": "A"},            # predecessor map (null = none)
  "current_edge": {"source": "A", "target": "B"},  # edge under examination
                              # also accepts ["A", "B"] form
  "selected_edges": [["A", "B"]],  # tree/path edges to emphasize
  "final_path": ["A", "B", "D"],   # highlighted at the end
  "finalized": ["A"],         # Dijkstra settled nodes (subset of visited)
  "message": "Visit A (dist=0)"    # human-readable caption
}
"""

from __future__ import annotations

import math
from typing import Any

VALID_ALGORITHMS = ("bfs", "dfs", "dijkstra", "static")


def _as_id(value: Any) -> str:
    return str(value)


def normalize_graph(graph: dict) -> dict:
    """Validate a graph dict and return a normalized copy.

    Raises ValueError with a clear message on invalid input.
    """
    if not isinstance(graph, dict):
        raise ValueError("graph must be an object")
    directed = bool(graph.get("directed", False))
    weighted = bool(graph.get("weighted", False))
    raw_nodes = graph.get("nodes", [])
    raw_edges = graph.get("edges", [])
    if not isinstance(raw_nodes, list) or len(raw_nodes) == 0:
        raise ValueError("graph.nodes must be a non-empty list")
    if not isinstance(raw_edges, list):
        raise ValueError("graph.edges must be a list")

    nodes: list[dict] = []
    seen: set[str] = set()
    for n in raw_nodes:
        if isinstance(n, str):
            nid = n
            nx, ny, label = None, None, n
        elif isinstance(n, dict) and "id" in n:
            nid = _as_id(n["id"])
            nx = n.get("x", None)
            ny = n.get("y", None)
            label = str(n.get("label", nid))
        else:
            raise ValueError(f"invalid node entry: {n!r} (expected {{'id': ...}})")
        if nid in seen:
            raise ValueError(f"duplicate node id: {nid}")
        seen.add(nid)
        nodes.append({"id": nid, "x": nx, "y": ny, "label": label})

    edges: list[dict] = []
    for i, e in enumerate(raw_edges):
        if not isinstance(e, dict):
            raise ValueError(f"invalid edge entry at index {i}: {e!r}")
        if "source" not in e or "target" not in e:
            raise ValueError(f"edge at index {i} needs 'source' and 'target'")
        src, tgt = _as_id(e["source"]), _as_id(e["target"])
        if src not in seen:
            raise ValueError(f"edge {src}->{tgt} references unknown node '{src}'")
        if tgt not in seen:
            raise ValueError(f"edge {src}->{tgt} references unknown node '{tgt}'")
        w = e.get("weight", None)
        if w is not None:
            try:
                w = float(w)
            except (TypeError, ValueError):
                raise ValueError(f"edge {src}->{tgt} has non-numeric weight {e['weight']!r}")
            if not math.isfinite(w):
                raise ValueError(f"edge {src}->{tgt} has non-finite weight")
            if w < 0:
                # Dijkstra cannot handle negatives; keep the edge but flag it.
                raise ValueError(f"edge {src}->{tgt} has negative weight {w} (Dijkstra requires >= 0)")
        elif weighted:
            # Weighted mode without an explicit weight defaults to 1.
            w = 1.0
        edges.append({
            "source": src,
            "target": tgt,
            "weight": w,
            "id": str(e.get("id", f"e{i}")),
        })

    return {"directed": directed, "weighted": weighted, "nodes": nodes, "edges": edges}


def _normalize_edge_ref(ref: Any) -> dict | None:
    if ref is None:
        return None
    if isinstance(ref, (list, tuple)) and len(ref) == 2:
        return {"source": _as_id(ref[0]), "target": _as_id(ref[1])}
    if isinstance(ref, dict) and "source" in ref and "target" in ref:
        return {"source": _as_id(ref["source"]), "target": _as_id(ref["target"])}
    raise ValueError(f"invalid edge reference: {ref!r} (expected {{source,target}} or [u,v])")


def normalize_state(state: dict, step_default: int = 0) -> dict:
    """Validate one state object and return a normalized copy."""
    if not isinstance(state, dict):
        raise ValueError(f"state must be an object, got {state!r}")
    out: dict[str, Any] = {}
    out["step"] = int(state.get("step", step_default))
    out["event"] = str(state.get("event", "step"))
    cur = state.get("current", None)
    out["current"] = None if cur is None else _as_id(cur)
    for key in ("visited", "frontier", "finalized", "final_path"):
        vals = state.get(key, [])
        # Accept common aliases emitted by algorithm code.
        if key == "frontier" and not vals:
            for alias in ("queue", "stack", "frontier_nodes"):
                if state.get(alias):
                    vals = state[alias]
                    break
        if vals is None:
            vals = []
        if not isinstance(vals, list):
            raise ValueError(f"state field '{key}' must be a list")
        out[key] = [_as_id(v) for v in vals]
    dist = state.get("distances", {})
    if dist is None:
        dist = {}
    if not isinstance(dist, dict):
        raise ValueError("state field 'distances' must be an object")
    norm_dist: dict[str, float | None] = {}
    for k, v in dist.items():
        if v is None or (isinstance(v, str) and v.lower() in ("inf", "infinity", "none")):
            norm_dist[_as_id(k)] = None
        else:
            try:
                norm_dist[_as_id(k)] = float(v)
            except (TypeError, ValueError):
                raise ValueError(f"invalid distance for node {k!r}: {v!r}")
    out["distances"] = norm_dist
    parent = state.get("parent", state.get("predecessor", state.get("parents", {})))
    if parent is None:
        parent = {}
    if not isinstance(parent, dict):
        raise ValueError("state field 'parent' must be an object")
    out["parent"] = {}
    for k, v in parent.items():
        if v is None or (isinstance(v, str) and v.lower() in ("null", "none", "")):
            out["parent"][_as_id(k)] = None
        else:
            out["parent"][_as_id(k)] = _as_id(v)
    out["current_edge"] = _normalize_edge_ref(state.get("current_edge", state.get("edge", None)))
    sel = state.get("selected_edges", state.get("tree_edges", [])) or []
    if not isinstance(sel, list):
        raise ValueError("state field 'selected_edges' must be a list")
    out["selected_edges"] = [_normalize_edge_ref(e) for e in sel]
    out["message"] = str(state.get("message", f"Step {out['step']}: {out['event']}"))
    # Keep any extra scalar flags (e.g. relaxed: true) without failing.
    if "relaxed" in state:
        out["relaxed"] = bool(state["relaxed"])
    return out


def normalize_input(payload: dict) -> dict:
    """Validate a full animation input file. Returns normalized dict."""
    if not isinstance(payload, dict):
        raise ValueError("input JSON must be an object")
    algorithm = str(payload.get("algorithm", "static")).lower()
    if algorithm not in VALID_ALGORITHMS:
        raise ValueError(f"unknown algorithm '{algorithm}' (expected one of {VALID_ALGORITHMS})")
    # Graph may be nested under 'graph' or inline at the top level.
    graph_src = payload.get("graph", None)
    if graph_src is None and "nodes" in payload:
        graph_src = {k: payload[k] for k in ("directed", "weighted", "nodes", "edges") if k in payload}
    if graph_src is None:
        raise ValueError("input needs a 'graph' object (or top-level nodes/edges)")
    graph = normalize_graph(graph_src)
    node_ids = {n["id"] for n in graph["nodes"]}
    for ref_key in ("start", "target"):
        ref = payload.get(ref_key, None)
        if ref is not None and _as_id(ref) not in node_ids:
            raise ValueError(f"'{ref_key}' node '{ref}' is not in graph.nodes")
    raw_states = payload.get("states", [])
    if raw_states is None:
        raw_states = []
    if not isinstance(raw_states, list):
        raise ValueError("'states' must be a list")
    states = [normalize_state(s, i) for i, s in enumerate(raw_states)]
    # Dijkstra inputs must be weighted (or at least carry weights).
    if algorithm == "dijkstra" and not graph["weighted"]:
        # Allow it if every edge actually has a weight; else warn by auto-enabling.
        if all(e["weight"] is not None for e in graph["edges"]):
            graph["weighted"] = True
        else:
            raise ValueError("dijkstra requires a weighted graph (set graph.weighted=true and give edge weights)")
    return {
        "algorithm": algorithm,
        "graph": graph,
        "start": None if payload.get("start") is None else _as_id(payload["start"]),
        "target": None if payload.get("target") is None else _as_id(payload["target"]),
        "states": states,
    }


def load_input_file(path: str) -> dict:
    """Read + validate an animation input JSON file."""
    import json

    with open(path, "r", encoding="utf-8") as fh:
        payload = json.load(fh)
    return normalize_input(payload)
