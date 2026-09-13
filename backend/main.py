"""
MathViz Unified Backend - FastAPI server bridging Frontend (Role 1) and Manim Engine (Role 3).

Endpoints:
- GET  /                    -> Serve frontend
- POST /api/algorithm/run   -> Run BFS/DFS/Dijkstra on graph, return animation states
- POST /api/algorithm/convert -> Convert teammate format to animation schema
- POST /api/manim/render    -> Render Manim video from animation schema
- GET  /api/media/{filename} -> Serve generated video
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
import json
import subprocess
import tempfile
import os
import uuid
from pathlib import Path
import sys

# Add algorithms to path
ALGORITHMS_PATH = Path(__file__).parent / "algorithms"
sys.path.insert(0, str(ALGORITHMS_PATH))

# Add manim_engine to path
MANIM_ENGINE_PATH = Path(__file__).parent.parent / "manim_engine"
sys.path.insert(0, str(MANIM_ENGINE_PATH.parent))  # Add unified root so manim_engine is importable

from manim_engine.schemas import normalize_input, normalize_graph
from manim_engine.layouts import compute_positions

# Import Role 2 algorithms
from algorithms.graph import Graph as Role2Graph
from algorithms.bfs import bfs as role2_bfs
from algorithms.dfs import dfs as role2_dfs
from algorithms.dijkstra import dijkstra as role2_dijkstra

app = FastAPI(title="MathViz Unified API", version="1.0.0")

# CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
EXAMPLES_DIR = PROJECT_ROOT / "examples"
MEDIA_DIR = PROJECT_ROOT / "media_out"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
MANIM_RENDERER = PROJECT_ROOT / "manim_engine" / "renderer.py"

MEDIA_DIR.mkdir(exist_ok=True)

# Serve media files
app.mount("/media", StaticFiles(directory=str(MEDIA_DIR)), name="media")


# ============================================================
# Pydantic Models
# ============================================================

class Node(BaseModel):
    id: str
    x: Optional[float] = None
    y: Optional[float] = None
    label: Optional[str] = None


class Edge(BaseModel):
    source: str
    target: str
    weight: Optional[float] = None


class GraphInput(BaseModel):
    directed: bool = False
    weighted: bool = False
    nodes: List[Node]
    edges: List[Edge]


class AlgorithmRunRequest(BaseModel):
    algorithm: str = Field(..., pattern="^(bfs|dfs|dijkstra)$")
    graph: GraphInput
    start: str
    target: Optional[str] = None


class AlgorithmRunResponse(BaseModel):
    animation_input: Dict[str, Any]
    traversal: List[str]
    distances: Optional[Dict[str, float]] = None
    path: Optional[List[str]] = None


class ConvertRequest(BaseModel):
    # Teammate's format
    algorithm: str
    start: str
    destination: Optional[str] = None
    target: Optional[str] = None
    traversal: Optional[List[str]] = None
    distances: Optional[Dict[str, Union[float, int]]] = None
    path: Optional[List[str]] = None
    states: Optional[List[Dict[str, Any]]] = None


class ConvertResponse(BaseModel):
    converted: Dict[str, Any]


class RenderRequest(BaseModel):
    animation_input: Dict[str, Any]
    quality: str = Field(default="m", pattern="^(l|m|h|k)$")


class RenderResponse(BaseModel):
    video_url: str
    filename: str
    log: str


# ============================================================
# Algorithm Implementations (Role 2 logic)
# ============================================================

def role2graph_to_animation_input(role2_result: dict, graph_input: GraphInput, target: Optional[str] = None) -> dict:
    """Convert Role 2 algorithm output (teammate format) to animation schema."""
    return convert_teammate_format(role2_result)


def run_bfs(graph: GraphInput, start: str, target: Optional[str] = None) -> AlgorithmRunResponse:
    """Run BFS using Role 2 algorithm and return animation-ready states."""
    # Build Role 2 graph
    g = Role2Graph(directed=graph.directed, weighted=graph.weighted)
    for n in graph.nodes:
        g.add_node(n.id)
    for e in graph.edges:
        g.add_edge(e.source, e.target, e.weight)
    
    # Run Role 2 BFS
    result = role2_bfs(g, start)
    
    # Convert to animation schema
    animation_input = role2graph_to_animation_input(result, graph, target)
    
    # Validate
    normalize_input(animation_input)
    
    return AlgorithmRunResponse(
        animation_input=animation_input,
        traversal=result.get("traversal", []),
        path=animation_input.get("states", [])[-1].get("final_path") if target else None
    )


def run_dfs(graph: GraphInput, start: str) -> AlgorithmRunResponse:
    """Run DFS using Role 2 algorithm and return animation-ready states."""
    # Build Role 2 graph
    g = Role2Graph(directed=graph.directed, weighted=graph.weighted)
    for n in graph.nodes:
        g.add_node(n.id)
    for e in graph.edges:
        g.add_edge(e.source, e.target, e.weight)
    
    # Run Role 2 DFS
    result = role2_dfs(g, start)
    
    # Convert to animation schema
    animation_input = role2graph_to_animation_input(result, graph)
    
    # Validate
    normalize_input(animation_input)
    
    return AlgorithmRunResponse(
        animation_input=animation_input,
        traversal=result.get("traversal", [])
    )


def run_dijkstra(graph: GraphInput, start: str, destination: Optional[str] = None) -> AlgorithmRunResponse:
    """Run Dijkstra using Role 2 algorithm and return animation-ready states."""
    if not graph.weighted:
        raise ValueError("Dijkstra requires a weighted graph")
    
    # Build Role 2 graph
    g = Role2Graph(directed=graph.directed, weighted=True)
    for n in graph.nodes:
        g.add_node(n.id)
    for e in graph.edges:
        w = e.weight if e.weight is not None else 1.0
        g.add_edge(e.source, e.target, w)
    
    # Run Role 2 Dijkstra
    result = role2_dijkstra(g, start, destination)
    
    # Convert to animation schema
    animation_input = role2graph_to_animation_input(result, graph, destination)
    
    # Validate
    normalize_input(animation_input)
    
    return AlgorithmRunResponse(
        animation_input=animation_input,
        traversal=result.get("traversal", []) if "traversal" in result else [],
        distances=result.get("distances"),
        path=result.get("path")
    )


# ============================================================
# Teammate Format Converter
# ============================================================

def convert_teammate_format(data: dict) -> dict:
    """Convert teammate's result format to animation schema."""
    from copy import deepcopy
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


# ============================================================
# API Endpoints
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve the frontend HTML."""
    with open(FRONTEND_DIR / "index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.post("/api/algorithm/run", response_model=AlgorithmRunResponse)
async def run_algorithm(request: AlgorithmRunRequest):
    """Run BFS/DFS/Dijkstra on the given graph and return animation-ready states."""
    try:
        if request.algorithm == "bfs":
            return run_bfs(request.graph, request.start, request.target)
        elif request.algorithm == "dfs":
            return run_dfs(request.graph, request.start)
        elif request.algorithm == "dijkstra":
            if not request.graph.weighted:
                raise HTTPException(status_code=400, detail="Dijkstra requires a weighted graph")
            return run_dijkstra(request.graph, request.start, request.target)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown algorithm: {request.algorithm}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/algorithm/convert", response_model=ConvertResponse)
async def convert_format(request: ConvertRequest):
    """Convert teammate's result format to animation schema."""
    try:
        data = request.model_dump(exclude_none=True)
        converted = convert_teammate_format(data)
        # Validate the converted output
        normalize_input(converted)
        return ConvertResponse(converted=converted)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/manim/render", response_model=RenderResponse)
async def render_manim(request: RenderRequest):
    """Render Manim video from animation schema."""
    try:
        # Validate input
        normalize_input(request.animation_input)

        # Write to temp file
        tmp = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, dir=PROJECT_ROOT)
        json.dump(request.animation_input, tmp)
        tmp.close()
        input_json = tmp.name

        try:
            cmd = [
                sys.executable, '-m', 'manim_engine.renderer',
                input_json,
                '--quality', request.quality,
                '--media-dir', str(MEDIA_DIR)
            ]
            env = os.environ.copy()
            env['PYTHONPATH'] = str(PROJECT_ROOT)
            proc = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT, env=env, timeout=300)
            log = proc.stdout + '\n' + proc.stderr
            if proc.returncode != 0:
                raise HTTPException(status_code=500, detail=f"Render failed: {log}")

            stem = Path(input_json).stem
            algo = request.animation_input.get('algorithm', 'static')
            expected = f"{algo}_{stem}_{request.quality}.mp4"
            out_path = MEDIA_DIR / expected
            if not out_path.exists():
                matches = list(MEDIA_DIR.rglob(f"{algo}_{stem}_{request.quality}.mp4"))
                if not matches:
                    raise HTTPException(status_code=500, detail=f"Output not found: {log}")
                out_path = matches[0]

            return RenderResponse(
                video_url=f"/media/{out_path.name}",
                filename=out_path.name,
                log=log
            )
        finally:
            try:
                os.unlink(input_json)
            except:
                pass
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/examples")
async def list_examples():
    """List available example files."""
    files = sorted(f.name for f in EXAMPLES_DIR.glob('*.json'))
    return {"examples": files}


@app.get("/api/example/{name}")
async def get_example(name: str):
    """Get an example file."""
    path = EXAMPLES_DIR / name
    if not path.exists():
        raise HTTPException(status_code=404, detail="Example not found")
    with open(path) as f:
        return json.load(f)


@app.get("/api/health")
async def health():
    return {"status": "ok", "manim_engine": "loaded"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)