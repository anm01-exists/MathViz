"""Deterministic graph layouts for MathViz.

Rule: if every node carries explicit x/y, those are used (scaled to fit).
Otherwise a deterministic circular layout sorted by node id is used, so the
same graph JSON always renders the same picture (Review-1 requirement).
No randomness anywhere.
"""

from __future__ import annotations

import math

CIRCLE_RADIUS = 2.2
X_SCALE = 1.0
Y_SCALE = 1.0
MAX_EXTENT = 3.0  # clamp manual coordinates into the Manim frame


def _clamp(v: float) -> float:
    return max(-MAX_EXTENT, min(MAX_EXTENT, v))


def compute_positions(nodes: list[dict]) -> dict[str, tuple[float, float, float]]:
    """Return {node_id: (x, y, 0)} for the given normalized node list."""
    ids = [n["id"] for n in nodes]
    manual = [n for n in nodes if n.get("x") is not None and n.get("y") is not None]
    if len(manual) == len(nodes):
        pos: dict[str, tuple[float, float, float]] = {}
        for n in nodes:
            pos[n["id"]] = (_clamp(float(n["x"])) * X_SCALE, _clamp(float(n["y"])) * Y_SCALE, 0.0)
        return pos
    # Deterministic circle, sorted by id so insertion order cannot change output.
    ordered = sorted(ids)
    n = len(ordered)
    pos = {}
    for i, nid in enumerate(ordered):
        angle = 2 * math.pi * i / n + math.pi / 2  # start at top
        pos[nid] = (CIRCLE_RADIUS * math.cos(angle), CIRCLE_RADIUS * math.sin(angle), 0.0)
    return pos
