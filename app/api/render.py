"""Manim video rendering endpoint."""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from fastapi import APIRouter, HTTPException
from manim_engine.schemas import normalize_input

from app import config
from app.schemas.models import RenderRequest, RenderResponse

router = APIRouter(prefix="/api/manim", tags=["render"])


@router.post("/render", response_model=RenderResponse)
async def render_manim(request: RenderRequest):
    """Render Manim video from animation schema."""
    try:
        # Validate input
        normalize_input(request.animation_input)

        # Write to temp file
        tmp = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, dir=str(config.TEMP_DIR))
        json.dump(request.animation_input, tmp)
        tmp.close()
        input_json = tmp.name

        try:
            cmd = [
                sys.executable, '-m', 'manim_engine.renderer',
                input_json,
                '--quality', request.quality,
                '--media-dir', str(config.MEDIA_DIR)
            ]
            env = os.environ.copy()
            env['PYTHONPATH'] = config.as_pythonpath()
            proc = subprocess.run(cmd, capture_output=True, text=True,
                                  cwd=str(config.BASE_DIR), env=env, timeout=300)
            log = proc.stdout + '\n' + proc.stderr
            if proc.returncode != 0:
                raise HTTPException(status_code=500, detail=f"Render failed: {log}")

            stem = Path(input_json).stem
            algo = request.animation_input.get('algorithm', 'static')
            expected = f"{algo}_{stem}_{request.quality}.mp4"
            out_path = config.MEDIA_DIR / expected
            if not out_path.exists():
                matches = list(config.MEDIA_DIR.rglob(f"{algo}_{stem}_{request.quality}.mp4"))
                if not matches:
                    raise HTTPException(status_code=500, detail=f"Output not found: {log}")
                out_path = matches[0]

            return RenderResponse(
                video_url=f"/media/{out_path.name}",
                filename=out_path.name,
                log=log,
            )
        finally:
            try:
                os.unlink(input_json)
            except OSError:
                pass
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))