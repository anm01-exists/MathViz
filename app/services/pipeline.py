"""Orchestration: run graph algorithms and hand off animation JSON for rendering."""

from typing import Optional

from manim_engine.schemas import normalize_input

from app.algorithms.bfs import bfs as role2_bfs
from app.algorithms.dfs import dfs as role2_dfs
from app.algorithms.dijkstra import dijkstra as role2_dijkstra
from app.algorithms.graph import Graph as Role2Graph
from app.schemas.models import AlgorithmRunResponse, GraphInput
from app.services.animation import (
    _bfs_animation_states,
    _bfs_parents,
    _dfs_animation_states,
    _dfs_parents,
    _dijkstra_animation_states,
)


def _graph_dict(graph_input: GraphInput) -> dict:
    """Return the user's graph as an animation-schema graph object."""
    nodes = []
    for n in graph_input.nodes:
        node = {"id": n.id}
        # Preserve explicit layout positions so the animation matches the editor.
        if n.x is not None and n.y is not None:
            node["x"] = n.x
            node["y"] = n.y
        nodes.append(node)
    return {
        "directed": graph_input.directed,
        "weighted": graph_input.weighted,
        "nodes": nodes,
        "edges": [
            {"source": e.source, "target": e.target, "weight": e.weight}
            for e in graph_input.edges
        ],
    }


def _build_graph(graph: GraphInput) -> Role2Graph:
    g = Role2Graph(directed=graph.directed, weighted=graph.weighted)
    for n in graph.nodes:
        g.add_node(n.id)
    for e in graph.edges:
        g.add_edge(e.source, e.target, e.weight)
    return g


def run_bfs(graph: GraphInput, start: str, target: Optional[str] = None) -> AlgorithmRunResponse:
    """Run BFS and return animation-ready states."""
    g = _build_graph(graph)
    result = role2_bfs(g, start)
    parent, children = _bfs_parents(g, start)

    animation_input = {
        "algorithm": "bfs",
        "graph": _graph_dict(graph),
        "start": start,
        "target": target,
        "states": _bfs_animation_states(result.get("states", []), parent, children),
    }
    normalize_input(animation_input)

    return AlgorithmRunResponse(
        animation_input=animation_input,
        traversal=result.get("traversal", []),
        path=[],
    )


def run_dfs(graph: GraphInput, start: str) -> AlgorithmRunResponse:
    """Run DFS and return animation-ready states."""
    g = _build_graph(graph)
    result = role2_dfs(g, start)
    parent, children = _dfs_parents(g, start)

    animation_input = {
        "algorithm": "dfs",
        "graph": _graph_dict(graph),
        "start": start,
        "states": _dfs_animation_states(result.get("states", []), parent, children, result.get("traversal", [])),
    }
    normalize_input(animation_input)

    return AlgorithmRunResponse(
        animation_input=animation_input,
        traversal=result.get("traversal", []),
        path=[],
    )


def run_dijkstra(graph: GraphInput, start: str, destination: Optional[str] = None) -> AlgorithmRunResponse:
    """Run Dijkstra and return animation-ready states."""
    if not graph.weighted:
        raise ValueError("Dijkstra requires a weighted graph (enable the Weighted toggle)")

    g = Role2Graph(directed=graph.directed, weighted=True)
    for n in graph.nodes:
        g.add_node(n.id)
    for e in graph.edges:
        g.add_edge(e.source, e.target, e.weight if e.weight is not None else 1.0)

    result = role2_dijkstra(g, start, destination)

    node_ids = [n.id for n in graph.nodes]
    states, settled, last_prev, last_dists = _dijkstra_animation_states(
        result.get("states", []), node_ids, destination
    )

    parent_live = {k: v for k, v in last_prev.items() if v}
    final_path = result.get("path", [])
    is_target = bool(destination) and final_path and final_path[-1] == destination

    # Mark the final path on the last state and append a completion state.
    for st in states:
        if is_target and st["current"] == destination:
            st["final_path"] = list(final_path)
    states.append({
        "step": len(states),
        "event": "path_found" if is_target else "done",
        "current": None,
        "visited": list(settled),
        "finalized": list(settled),
        "frontier": [],
        "distances": last_dists,
        "parent": parent_live,
        "selected_edges": [[last_prev[v], v] for v in settled if last_prev.get(v)],
        "final_path": list(final_path),
        "message": (
            f"Shortest path: {' -> '.join(final_path)} (cost {last_dists.get(destination)})"
            if is_target else
            "Dijkstra complete — target unreachable" if destination else "Dijkstra complete"
        ),
    })

    animation_input = {
        "algorithm": "dijkstra",
        "graph": _graph_dict(graph),
        "start": start,
        "target": destination,
        "states": states,
    }
    normalize_input(animation_input)

    return AlgorithmRunResponse(
        animation_input=animation_input,
        traversal=list(settled),
        distances={k: (None if v == float("inf") else v) for k, v in last_dists.items()},
        path=final_path,
    )