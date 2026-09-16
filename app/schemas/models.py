"""Pydantic request/response models for the API."""

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


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