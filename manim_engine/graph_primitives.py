"""Reusable Manim graph primitives for MathViz (Role 3).

MathVizGraph builds, owns and updates every mobject for one graph:
circles + labels for nodes, lines/arrows + weight labels for edges,
and per-node Dijkstra distance labels.

Nothing here knows about BFS/DFS/Dijkstra logic. Callers (scenes.py)
only pass already-computed states (see schemas.py) and this class
translates them into colors / captions.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import (
    WHITE,
    Arrow,
    Circle,
    Line,
    Rectangle,
    Text,
    VGroup,
)

try:
    from .layouts import compute_positions
    from .styles import (
        DIST_LABEL_FONT_SIZE,
        EDGE_STYLE,
        NODE_RADIUS,
        NODE_STROKE_WIDTH,
        NODE_STYLE,
        WEIGHT_FONT_SIZE,
    )
except ImportError:  # manim standalone file mode
    from manim_engine.layouts import compute_positions
    from manim_engine.styles import (
        DIST_LABEL_FONT_SIZE,
        EDGE_STYLE,
        NODE_RADIUS,
        NODE_STROKE_WIDTH,
        NODE_STYLE,
        WEIGHT_FONT_SIZE,
    )


def _edge_key(source: str, target: str, directed: bool) -> tuple:
    if directed:
        return (source, target)
    return tuple(sorted((source, target)))


class MathVizGraph:
    """Owns all mobjects for one static graph plus dynamic highlights."""

    def __init__(self, graph: dict, positions: dict | None = None) -> None:
        self.graph = graph
        self.directed: bool = bool(graph.get("directed", False))
        self.weighted: bool = bool(graph.get("weighted", False))
        self.positions: dict = positions or compute_positions(graph["nodes"])
        self.node_circles: dict[str, Circle] = {}
        self.node_labels: dict[str, Text] = {}
        self.dist_labels: dict[str, Text] = {}
        # (edge_key, index) -> {"line": ..., "weight": ...|None, "source":, "target":}
        self.edge_mobjects: dict[tuple, dict] = {}
        self._build()

    # ------------------------------------------------------------------ build
    def _node_mobject(self, nid: str, label: str) -> VGroup:
        circle = Circle(
            radius=NODE_RADIUS,
            color=NODE_STYLE["default"]["stroke"],
            stroke_width=NODE_STROKE_WIDTH,
            fill_color=NODE_STYLE["default"]["fill"],
            fill_opacity=1.0,
        )
        circle.move_to(self.positions[nid])
        text = Text(label, font_size=26, color=WHITE)
        text.move_to(self.positions[nid])
        self.node_circles[nid] = circle
        self.node_labels[nid] = text
        return VGroup(circle, text)

    def _shorten(self, start, end) -> tuple:
        """Shorten an edge so it touches circle borders instead of centers."""
        import numpy as np

        vec = end - start
        dist = float(sum(float(v) ** 2 for v in vec) ** 0.5) or 1.0
        unit = vec / dist
        return (start + unit * (NODE_RADIUS + 0.02), end - unit * (NODE_RADIUS + 0.06))

    def _edge_mobject(self, source: str, target: str, weight) -> VGroup:
        import numpy as np

        s = np.array(self.positions[source], dtype=float)
        t = np.array(self.positions[target], dtype=float)
        if source == target:  # self-loop: small circle above the node
            loop = Circle(radius=NODE_RADIUS * 0.7, color=EDGE_STYLE["default"]["color"],
                          stroke_width=EDGE_STYLE["default"]["width"])
            loop.next_to(s, [0, 1, 0], buff=0.05)
            parts: list = [loop]
        elif self.directed:
            a, b = self._shorten(s, t)
            parts = [Arrow(a, b, buff=0.02, stroke_width=EDGE_STYLE["default"]["width"],
                           color=EDGE_STYLE["default"]["color"])]
        else:
            a, b = self._shorten(s, t)
            parts = [Line(a, b, stroke_width=EDGE_STYLE["default"]["width"],
                          color=EDGE_STYLE["default"]["color"])]
        weight_mob = None
        if self.weighted and weight is not None:
            mid = (s + t) / 2.0
            if source == target:
                mid = mid + [0, 0.9, 0]
            bg = Rectangle(width=0.62, height=0.38, fill_color="#000000",
                           fill_opacity=0.75, stroke_opacity=0)
            bg.move_to(mid)
            txt = Text(_fmt_weight(weight), font_size=WEIGHT_FONT_SIZE, color=WHITE)
            txt.move_to(mid)
            weight_mob = VGroup(bg, txt)
            parts.append(weight_mob)
        group = VGroup(*parts)
        return group

    def _build(self) -> None:
        self.root = VGroup()
        # Edges first (under nodes).
        counter: dict[tuple, int] = {}
        for e in self.graph["edges"]:
            key = _edge_key(e["source"], e["target"], self.directed)
            idx = counter.get(key, 0)
            counter[key] = idx + 1
            group = self._edge_mobject(e["source"], e["target"], e.get("weight"))
            line = group[0]
            weight_mob = group[1] if len(group) > 1 else None
            self.edge_mobjects[(key, idx)] = {
                "line": line, "weight": weight_mob,
                "source": e["source"], "target": e["target"],
            }
            self.root.add(group)
        for n in self.graph["nodes"]:
            self.root.add(self._node_mobject(n["id"], n.get("label", n["id"])))

    # ---------------------------------------------------------------- helpers
    def vgroup(self) -> VGroup:
        return self.root

    def matching_edges(self, source: str, target: str) -> list[dict]:
        """All rendered edges between two nodes (handles undirected flip)."""
        key = _edge_key(source, target, self.directed)
        return [v for (k, _), v in self.edge_mobjects.items() if k == key]

    def all_edge_entries(self) -> Iterable[dict]:
        return self.edge_mobjects.values()

    # ----------------------------------------------------------------- updates
    def set_node_style(self, nid: str, style: str) -> None:
        circle = self.node_circles.get(nid)
        if circle is None:
            return
        spec = NODE_STYLE.get(style, NODE_STYLE["default"])
        circle.set_fill(spec["fill"], opacity=1.0)
        circle.set_stroke(spec["stroke"], width=NODE_STROKE_WIDTH + (1.5 if style in ("current", "path") else 0))

    def set_edge_style(self, source: str, target: str, style: str) -> None:
        spec = EDGE_STYLE.get(style, EDGE_STYLE["default"])
        for entry in self.matching_edges(source, target):
            entry["line"].set_color(spec["color"])
            entry["line"].set_stroke(width=spec["width"])

    def reset_styles(self) -> None:
        for nid in self.node_circles:
            self.set_node_style(nid, "default")
        for entry in self.all_edge_entries():
            entry["line"].set_color(EDGE_STYLE["default"]["color"])
            entry["line"].set_stroke(width=EDGE_STYLE["default"]["width"])

    # ------------------------------------------------------- distance labels
    def ensure_dist_labels(self) -> None:
        """Create per-node Dijkstra distance captions (called once)."""
        import numpy as np

        for nid, circle in self.node_circles.items():
            if nid in self.dist_labels:
                continue
            label = Text("d=inf", font_size=DIST_LABEL_FONT_SIZE, color=WHITE)
            label.next_to(circle, [0, -1, 0], buff=0.12)
            self.dist_labels[nid] = label
            self.root.add(label)

    def set_distance(self, nid: str, value: float | None) -> None:
        label = self.dist_labels.get(nid)
        if label is None:
            return
        txt = "d=inf" if value is None else f"d={_fmt_weight(value)}"
        # Replace text in place to keep the mobject identity for animations.
        new = Text(txt, font_size=DIST_LABEL_FONT_SIZE, color=WHITE)
        new.next_to(self.node_circles[nid], [0, -1, 0], buff=0.12)
        label.become(new)

    # ------------------------------------------------------- state application
    def apply_state(self, state: dict, start: str | None = None,
                    target: str | None = None, show_distances: bool = False) -> None:
        """Recolor nodes/edges from one normalized state (no animation here)."""
        self.reset_styles()
        visited = set(state.get("visited", []))
        frontier = set(state.get("frontier", []))
        finalized = set(state.get("finalized", []))
        current = state.get("current")
        final_path = list(state.get("final_path", []))
        selected = list(state.get("selected_edges", []))
        current_edge = state.get("current_edge")

        if show_distances:
            self.ensure_dist_labels()
            for nid in self.node_circles:
                self.set_distance(nid, state.get("distances", {}).get(nid, None))

        # Base layers: finalized > visited > frontier.
        for nid in visited:
            self.set_node_style(nid, "visited")
        for nid in finalized:
            self.set_node_style(nid, "finalized")
        for nid in frontier:
            if nid != current:
                self.set_node_style(nid, "frontier")
        # Selected tree edges underneath current/path highlights.
        for ref in selected:
            if isinstance(ref, dict):
                self.set_edge_style(ref["source"], ref["target"], "selected")
        if current_edge and isinstance(current_edge, dict):
            self.set_edge_style(current_edge["source"], current_edge["target"], "current")
        if start is not None and start in self.node_circles and current != start and start not in visited:
            self.set_node_style(start, "start")
        if target is not None and target in self.node_circles and target not in visited:
            if current != target:
                self.set_node_style(target, "target")
        if current is not None and current in self.node_circles:
            self.set_node_style(current, "current")
        # Final path wins over everything.
        if final_path:
            for nid in final_path:
                if nid in self.node_circles:
                    self.set_node_style(nid, "path")
            for u, v in zip(final_path[:-1], final_path[1:]):
                self.set_edge_style(u, v, "path")


def _fmt_weight(w) -> str:
    try:
        f = float(w)
    except (TypeError, ValueError):
        return str(w)
    return str(int(f)) if f.is_integer() else str(round(f, 2))
