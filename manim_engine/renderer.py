"""Reproducible rendering entry point for the MathViz Manim engine (Role 3).

Backend contract (one function, one command):
    from manim_engine.renderer import render_from_json
    video = render_from_json("examples/bfs_example.json")

CLI:
    python -m manim_engine.renderer examples/bfs_example.json --quality m
    python -m manim_engine.renderer examples/dijkstra_example.json --algorithm dijkstra --format mp4

Output convention:
    <media_dir>/<algorithm>_<input_stem>_<quality>.mp4
e.g. media/bfs_bfs_example_m.mp4

Quality flags: l = 480p, m = 720p (default), h = 1080p, k = 4k.
Requires: manim + ffmpeg on PATH (ffmpeg is bundled with most Manim
installs; on Windows run `winget install ffmpeg` or `choco install ffmpeg`
if rendering fails with "ffmpeg not found").
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from .schemas import VALID_ALGORITHMS, load_input_file
from .scenes import INPUT_ENV_VAR

SCENE_FOR_ALGORITHM = {
    "bfs": "BFSScene",
    "dfs": "DFSScene",
    "dijkstra": "DijkstraScene",
    "static": "StaticGraphScene",
}

QUALITY_TO_FLAG = {"l": "-ql", "m": "-qm", "h": "-qh", "k": "-qk"}


def get_scene_for_algorithm(algorithm: str) -> str:
    algo = str(algorithm).lower()
    if algo not in SCENE_FOR_ALGORITHM:
        raise ValueError(f"unknown algorithm '{algorithm}' (expected one of {sorted(SCENE_FOR_ALGORITHM)})")
    return SCENE_FOR_ALGORITHM[algo]


def _manim_exe() -> str:
    exe = shutil.which("manim")
    if exe:
        return exe
    return f"{sys.executable} -m manim"  # fallback: python -m manim


def render_from_json(input_json: str | Path, media_dir: str | Path = "media",
                     quality: str = "m", output_format: str = "mp4",
                     dry_run: bool = False) -> Path:
    """Render an animation input JSON to video. Returns the output video path."""
    quality = quality.lower()
    if quality not in QUALITY_TO_FLAG:
        raise ValueError(f"unknown quality '{quality}' (expected one of {sorted(QUALITY_TO_FLAG)})")
    output_format = output_format.lower().lstrip(".")
    if output_format not in ("mp4", "webm", "mov", "png", "gif"):
        raise ValueError(f"unsupported format '{output_format}'")

    input_path = Path(input_json).resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"input JSON not found: {input_path}")
    payload = load_input_file(str(input_path))  # validates early with clear errors
    scene = get_scene_for_algorithm(payload["algorithm"])

    media_dir = Path(media_dir).resolve()
    media_dir.mkdir(parents=True, exist_ok=True)
    out_name = f"{payload['algorithm']}_{input_path.stem}_{quality}.{output_format}"
    out_path = media_dir / out_name

    scenes_py = Path(__file__).resolve().parent / "scenes.py"
    manim_cmd = _manim_exe().split()
    cmd = [
        *manim_cmd,
        QUALITY_TO_FLAG[quality],
        f"--format={output_format}",
        f"--media_dir={media_dir}",
        "-o", out_name,
        str(scenes_py),
        scene,
    ]
    env = os.environ.copy()
    env[INPUT_ENV_VAR] = str(input_path)
    if dry_run:
        print("DRY RUN:", " ".join(cmd))
        return out_path
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"manim render failed (exit {result.returncode})\n"
            f"CMD: {' '.join(cmd)}\n--- stdout ---\n{result.stdout[-4000:]}\n"
            f"--- stderr ---\n{result.stderr[-4000:]}\n"
            "Hint: install ffmpeg (winget install ffmpeg) and run `manim --version`."
        )
    # Manim may nest output under media_dir/videos/scenes/...; locate it.
    if not out_path.exists():
        candidates = sorted(media_dir.rglob(out_name))
        if candidates:
            try:
                candidates[0].replace(out_path)
            except OSError:
                out_path = candidates[0]
    print(f"Rendered {payload['algorithm']} ({scene}) -> {out_path}")
    return out_path


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="MathViz Manim renderer (Role 3 entry point)")
    parser.add_argument("input", help="animation input JSON file")
    parser.add_argument("--media-dir", default="media", help="output directory")
    parser.add_argument("--quality", default="m", choices=["l", "m", "h", "k"])
    parser.add_argument("--format", default="mp4", dest="fmt",
                        help="mp4 (default), webm, mov, png (no ffmpeg needed), gif")
    parser.add_argument("--algorithm", default=None,
                        help="override algorithm in JSON (must still match states)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    if args.algorithm:
        # Validate + temporarily override for a one-off render.
        payload = load_input_file(args.input)
        if args.algorithm.lower() not in VALID_ALGORITHMS:
            raise SystemExit(f"unknown --algorithm '{args.algorithm}'")
        import tempfile

        with open(args.input, encoding="utf-8") as fh:
            raw = json.load(fh)
        raw["algorithm"] = args.algorithm.lower()
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
            json.dump(raw, tf)
            tmp = tf.name
        try:
            render_from_json(tmp, args.media_dir, args.quality, args.fmt, args.dry_run)
        finally:
            os.unlink(tmp)
    else:
        render_from_json(args.input, args.media_dir, args.quality, args.fmt, args.dry_run)


if __name__ == "__main__":
    main()
