"""Single visual language shared by every MathViz Manim scene.

Paper aesthetic: white background, ink-like colors, subtle textures.
"""

from __future__ import annotations

try:
    from manim import (
        BLUE_D,
        BLUE_E,
        GRAY,
        GREEN,
        GREEN_E,
        ORANGE,
        RED,
        WHITE,
        YELLOW,
        YELLOW_E,
        GREY,
        GREY_BROWN,
        GREY_E,
    )
except Exception:  # pragma: no cover - allows docs/tests without manim installed
    BLUE_D = BLUE_E = GRAY = GREEN = GREEN_E = ORANGE = RED = WHITE = YELLOW = YELLOW_E = GREY = GREY_BROWN = GREY_E = "#ffffff"

# Paper color palette
PAPER_WHITE = WHITE
INK_BLACK = "#1a1a2e"
INK_DARK = "#2d2d44"
INK_MEDIUM = "#4a4a6a"
INK_LIGHT = "#6b6b8a"
ACCENT_BLUE = "#2563eb"
ACCENT_BLUE_DARK = "#1d4ed8"
ACCENT_ORANGE = "#ea580c"
ACCENT_GREEN = "#16a34a"
ACCENT_GREEN_DARK = "#15803d"
ACCENT_RED = "#dc2626"
ACCENT_YELLOW = "#ca8a04"
ACCENT_YELLOW_DARK = "#a16207"
EDGE_GREY = "#9ca3af"
EDGE_GREY_LIGHT = "#d1d5db"
NODE_BLUE = "#3b82f6"
NODE_BLUE_DARK = "#1e40af"

NODE_RADIUS = 0.38
NODE_STROKE_WIDTH = 2.5
EDGE_STROKE_WIDTH = 3.0
PATH_STROKE_WIDTH = 6.0

# Node fill colors per state — paper/ink theme
NODE_STYLE = {
    "default": {"fill": NODE_BLUE, "stroke": INK_DARK},
    "start": {"fill": ACCENT_BLUE_DARK, "stroke": ACCENT_YELLOW_DARK},
    "target": {"fill": ACCENT_BLUE_DARK, "stroke": ACCENT_RED},
    "frontier": {"fill": ACCENT_YELLOW_DARK, "stroke": INK_DARK},
    "current": {"fill": ACCENT_ORANGE, "stroke": INK_DARK},
    "visited": {"fill": ACCENT_GREEN_DARK, "stroke": INK_DARK},
    "finalized": {"fill": ACCENT_GREEN, "stroke": INK_DARK},
    "path": {"fill": ACCENT_GREEN, "stroke": ACCENT_YELLOW_DARK},
}

EDGE_STYLE = {
    "default": {"color": EDGE_GREY, "width": EDGE_STROKE_WIDTH},
    "current": {"color": ACCENT_ORANGE, "width": PATH_STROKE_WIDTH},
    "selected": {"color": ACCENT_GREEN, "width": PATH_STROKE_WIDTH},
    "path": {"color": ACCENT_YELLOW_DARK, "width": PATH_STROKE_WIDTH},
    "faded": {"color": EDGE_GREY_LIGHT, "width": 2.0},
}

CAPTION_FONT_SIZE = 24
DIST_LABEL_FONT_SIZE = 20
WEIGHT_FONT_SIZE = 22
TITLE_FONT_SIZE = 30

# Paper texture: subtle grid/dots for background
PAPER_GRID_OPACITY = 0.04
PAPER_GRID_SPACING = 0.5