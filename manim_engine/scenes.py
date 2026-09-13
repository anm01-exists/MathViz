"""Manim scenes for MathViz (Role 3) — Paper Aesthetic.

Every scene is driven by an input JSON file whose path is passed through
the MATHVIZ_INPUT_JSON environment variable (Manim CLI cannot forward
custom arguments, so the renderer sets this variable before invoking
`manim`). The JSON contains the graph plus the ordered states produced
by the Role 2 algorithm engine — scenes never re-implement algorithms.

Reproducible entry point: never call these scenes directly with hand
arguments; always go through renderer.py:

    python -m manim_engine.renderer examples/bfs_example.json --quality m

which sets MATHVIZ_INPUT_JSON and calls the correct scene below.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Manim loads this file standalone (`manim manim_engine/scenes.py ...`),
# which breaks relative imports — fall back to absolute package imports.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import (
    DOWN,
    UP,
    LEFT,
    RIGHT,
    FadeIn,
    Scene,
    Text,
    VGroup,
    Write,
    Rectangle,
    Line,
    config,
)

try:
    from .graph_primitives import MathVizGraph
    from .layouts import compute_positions
    from .schemas import normalize_input
    from .styles import (
        CAPTION_FONT_SIZE,
        TITLE_FONT_SIZE,
        PAPER_WHITE,
        INK_BLACK,
        INK_DARK,
        INK_MEDIUM,
        INK_LIGHT,
        PAPER_GRID_OPACITY,
        PAPER_GRID_SPACING,
    )
except ImportError:  # manim standalone file mode
    from manim_engine.graph_primitives import MathVizGraph
    from manim_engine.layouts import compute_positions
    from manim_engine.schemas import normalize_input
    from manim_engine.styles import (
        CAPTION_FONT_SIZE,
        TITLE_FONT_SIZE,
        PAPER_WHITE,
        INK_BLACK,
        INK_DARK,
        INK_MEDIUM,
        INK_LIGHT,
        PAPER_GRID_OPACITY,
        PAPER_GRID_SPACING,
    )

INPUT_ENV_VAR = "MATHVIZ_INPUT_JSON"

TITLES = {
    "bfs": "Breadth-First Search (BFS)",
    "dfs": "Depth-First Search (DFS)",
    "dijkstra": "Dijkstra — Shortest Path",
    "static": "Graph — Static View",
}


def load_payload() -> dict:
    path = os.environ.get(INPUT_ENV_VAR, "")
    if not path:
        # Fallback so `manim scenes.py BFSScene` without the renderer still
        # shows something instead of crashing: a tiny demo graph.
        return {
            "algorithm": "bfs",
            "graph": {
                "directed": False,
                "weighted": False,
                "nodes": [{"id": "A"}, {"id": "B"}, {"id": "C"}],
                "edges": [
                    {"source": "A", "target": "B"},
                    {"source": "B", "target": "C"},
                ],
            },
            "start": "A",
            "target": None,
            "states": [
                {"step": 0, "event": "init", "current": None,
                 "visited": [], "frontier": ["A"], "message": "Start BFS at A"},
                {"step": 1, "event": "visit", "current": "A",
                 "visited": ["A"], "frontier": ["B"], "message": "Visit A"},
                {"step": 2, "event": "visit", "current": "B",
                 "visited": ["A", "B"], "frontier": ["C"], "message": "Visit B"},
                {"step": 3, "event": "done", "current": None,
                 "visited": ["A", "B", "C"], "frontier": [],
                 "final_path": [], "message": "BFS complete"},
            ],
        }
    with open(path, "r", encoding="utf-8") as fh:
        raw = json.load(fh)
    return normalize_input(raw)


class _MathVizBase(Scene):
    algorithm = "static"
    show_distances = False

    def construct(self):
        # Set white background for paper aesthetic - must be in construct
        self.camera.background_color = PAPER_WHITE
        # Call the algorithm-specific construct
        self._play_states(load_payload())

    def _make_paper_bg(self, width: float, height: float) -> VGroup:
        """Create a subtle paper background with faint grid lines."""
        lines = VGroup()
        # Vertical lines
        x = -width / 2
        while x <= width / 2:
            line = Line(
                start=[x, -height / 2, 0],
                end=[x, height / 2, 0],
                stroke_color=INK_LIGHT,
                stroke_width=0.5,
                stroke_opacity=PAPER_GRID_OPACITY,
            )
            lines.add(line)
            x += PAPER_GRID_SPACING
        # Horizontal lines
        y = -height / 2
        while y <= height / 2:
            line = Line(
                start=[-width / 2, y, 0],
                end=[width / 2, y, 0],
                stroke_color=INK_LIGHT,
                stroke_width=0.5,
                stroke_opacity=PAPER_GRID_OPACITY,
            )
            lines.add(line)
            y += PAPER_GRID_SPACING
        return lines

    def _setup(self, payload: dict):
        algo = payload["algorithm"]
        title_text = TITLES.get(algo, TITLES["static"])
        if payload.get("start"):
            title_text += f"  —  start {payload['start']}"
            if payload.get("target"):
                title_text += f" → {payload['target']}"
        title = Text(title_text, font_size=TITLE_FONT_SIZE, color=INK_BLACK, weight="MEDIUM")
        title.to_edge(UP, buff=0.4)

        positions = compute_positions(payload["graph"]["nodes"])
        mv_graph = MathVizGraph(payload["graph"], positions)
        canvas = VGroup(mv_graph.vgroup())
        canvas.next_to(title, DOWN, buff=0.5).shift(UP * 0.2)

        # Paper background behind the graph
        frame_width = config.frame_width - 1.0
        frame_height = config.frame_height - 2.0
        paper_bg = self._make_paper_bg(frame_width, frame_height)
        paper_bg.move_to(canvas.get_center())

        caption = Text("", font_size=CAPTION_FONT_SIZE, color=INK_DARK)
        caption.to_edge(DOWN, buff=0.5)
        step_label = Text("", font_size=CAPTION_FONT_SIZE - 4, color=INK_MEDIUM)
        step_label.next_to(caption, UP, buff=0.1)

        # Add background first, then title, canvas, caption
        self.add(paper_bg, title, canvas, caption, step_label)
        return mv_graph, caption, step_label

    def _show_state(self, mv: MathVizGraph, caption, step_label,
                    state: dict, payload: dict, animate: bool = True):
        mv.apply_state(state, start=payload.get("start"),
                       target=payload.get("target"),
                       show_distances=self.show_distances)
        new_caption = Text(state.get("message", ""), font_size=CAPTION_FONT_SIZE, color=INK_DARK)
        new_caption.to_edge(DOWN, buff=0.5)
        total = max(len(payload.get("states", [])), 1)
        new_step = Text(f"step {state.get('step', 0) + 1}/{total} · {state.get('event', '')}",
                        font_size=CAPTION_FONT_SIZE - 4, color=INK_MEDIUM)
        new_step.next_to(new_caption, UP, buff=0.1)
        if animate:
            self.play(caption.animate.become(new_caption),
                      step_label.animate.become(new_step),
                      run_time=0.55)
        else:
            caption.become(new_caption)
            step_label.become(new_step)

    def _play_states(self, payload: dict):
        mv, caption, step_label = self._setup(payload)
        # Reveal the graph.
        self.play(FadeIn(mv.vgroup()), run_time=0.8)
        self.wait(0.3)
        states = payload.get("states", [])
        if not states:
            caption.become(Text("Empty graph — nothing to animate",
                               font_size=CAPTION_FONT_SIZE, color=INK_DARK).to_edge(DOWN, buff=0.5))
            self.wait(1.0)
            return
        for st in states:
            self._show_state(mv, caption, step_label, st, payload, animate=True)
            self.wait(0.35)
        self.wait(1.0)


class StaticGraphScene(_MathVizBase):
    """Render the graph once with no animation (Day-1 deliverable)."""

    algorithm = "static"

    def construct(self):
        # Override with static-specific logic
        self.camera.background_color = PAPER_WHITE
        payload = load_payload()
        mv, caption, step_label = self._setup(payload)
        self.play(Write(mv.vgroup()), run_time=1.2)
        info = f"{len(payload['graph']['nodes'])} nodes · " \
               f"{len(payload['graph']['edges'])} edges · " \
               f"{'directed' if payload['graph']['directed'] else 'undirected'} · " \
               f"{'weighted' if payload['graph']['weighted'] else 'unweighted'}"
        caption.become(Text(info, font_size=CAPTION_FONT_SIZE, color=INK_DARK).to_edge(DOWN, buff=0.5))
        self.wait(1.5)


class BFSScene(_MathVizBase):
    """Animate BFS: frontier (yellow) → current (orange) → visited (green)."""

    algorithm = "bfs"


class DFSScene(_MathVizBase):
    """Animate DFS: stack (yellow) → current (orange); backtracks re-highlight."""

    algorithm = "dfs"


class DijkstraScene(_MathVizBase):
    """Animate Dijkstra: distance labels, relaxation (orange edge), settle (green)."""

    algorithm = "dijkstra"
    show_distances = True