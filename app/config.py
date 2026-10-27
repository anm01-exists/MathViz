"""Central configuration: paths and settings, overridable via environment."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Runtime locations (gitignored output lives under media/).
MEDIA_DIR = Path(os.environ.get("MATHVIZ_MEDIA_DIR", BASE_DIR / "media"))
FRONTEND_DIR = BASE_DIR / "frontend"
EXAMPLES_DIR = BASE_DIR / "examples"

TEMP_DIR = BASE_DIR  # render endpoint writes scratch animation JSON next to the app

VERSION = "1.0.0"


def ensure_dirs() -> None:
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)


def as_pythonpath() -> str:
    """Value for PYTHONPATH when spawning the Manim renderer subprocess."""
    return str(BASE_DIR)