# MathViz Unified

Interactive graph-algorithm visualizer: draw a graph in the browser editor,
pick an algorithm (BFS / DFS / Dijkstra), and get back an animated Manim video.

## Project layout

```
.
├── app/                     # FastAPI application (backend)
│   ├── main.py              # App factory: mounts /media, serves frontend, wires routers
│   ├── config.py            # Central paths & settings (env-overridable)
│   ├── api/                 # Blueprints: algorithms, render, examples, health
│   ├── services/            # pipeline.py (run algorithms -> animation JSON),
│   │                        # animation.py (animation state builders)
│   ├── algorithms/          # Portable BFS/DFS/Dijkstra + Graph (no web deps)
│   │   └── tests/           # Pytest unit tests for the algorithms
│   └── schemas/             # Pydantic request/response models
├── manim_engine/            # Manim rendering engine (Role 3)
│   ├── scenes.py            # BFS / DFS / Dijkstra / static scenes
│   ├── renderer.py          # CLI + programmatic render entry point
│   ├── layouts.py           # Node positioning (editor positions, circle fallback)
│   ├── schemas.py           # Animation-input validation/normalization
│   ├── styles.py            # Colors, fonts, grid
│   └── graph_primitives.py  # Manim graph drawing primitives
├── frontend/                # Single-page editor UI (index.html)
├── examples/                # Example graph JSON files
├── media/                   # Generated videos (gitignored, created at runtime)
└── scripts/                 # run.ps1 / run.sh launchers
```

## Quickstart

Requires Python 3.10+ and `ffmpeg` on PATH.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"

.\scripts\run.ps1            # or: python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 — draw a graph, run BFS/DFS/Dijkstra, watch the video.

## Tests

```powershell
pytest                    # algorithm unit tests
```

## API

| Method | Path                  | Description                                 |
| ------ | --------------------- | ------------------------------------------- |
| GET    | `/`                   | Frontend editor                             |
| GET    | `/media/{file}`       | Generated video files                       |
| POST   | `/api/algorithm/run`  | Run BFS/DFS/Dijkstra → animation JSON       |
| POST   | `/api/algorithm/convert` | Convert teammate format → animation schema |
| POST   | `/api/manim/render`   | Render animation JSON → MP4                 |
| GET    | `/api/examples`       | List example graphs                         |
| GET    | `/api/example/{name}` | Fetch one example graph                     |
| GET    | `/api/health`         | Health check                                |

## Rendering standalone

```powershell
python -m manim_engine.renderer examples/dijkstra_example.json --quality m
```

Output lands in `media/` (override with `--media-dir` or `MATHVIZ_MEDIA_DIR`).