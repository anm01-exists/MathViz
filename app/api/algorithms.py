"""Algorithm execution endpoints: run and convert."""

from fastapi import APIRouter, HTTPException

from manim_engine.schemas import normalize_input

from app.algorithms.converter import convert_teammate_format
from app.schemas.models import (
    AlgorithmRunRequest,
    AlgorithmRunResponse,
    ConvertRequest,
    ConvertResponse,
)
from app.services.pipeline import run_bfs, run_dfs, run_dijkstra

router = APIRouter(prefix="/api/algorithm", tags=["algorithms"])


@router.post("/run", response_model=AlgorithmRunResponse)
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


@router.post("/convert", response_model=ConvertResponse)
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