"""Example graph endpoints."""

import json

from fastapi import APIRouter, HTTPException

from app import config

router = APIRouter(prefix="/api", tags=["examples"])


@router.get("/examples")
async def list_examples():
    """List available example files."""
    files = sorted(f.name for f in config.EXAMPLES_DIR.glob('*.json'))
    return {"examples": files}


@router.get("/example/{name}")
async def get_example(name: str):
    """Get an example file."""
    path = config.EXAMPLES_DIR / name
    if not path.exists():
        raise HTTPException(status_code=404, detail="Example not found")
    with open(path) as f:
        return json.load(f)