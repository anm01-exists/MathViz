"""MathViz Manim engine package.

Role 3 — Manim Graph Visualization & Animation Engine.
All Manim scenes are driven by algorithm-state JSON, never by
re-implemented algorithm logic.
"""
from .renderer import get_scene_for_algorithm, render_from_json

__all__ = ["get_scene_for_algorithm", "render_from_json"]
