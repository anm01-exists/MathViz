"""
MathViz Unified API - FastAPI server bridging the interactive frontend and the Manim engine.

Endpoints:
- GET  /                         -> Serve frontend
- GET  /media/{filename}         -> Serve generated video
- POST /api/algorithm/run        -> Run BFS/DFS/Dijkstra, return animation states
- POST /api/algorithm/convert    -> Convert teammate format to animation schema
- POST /api/manim/render         -> Render Manim video from animation schema
- GET  /api/examples             -> List example graph files
- GET  /api/example/{name}       -> Fetch one example graph
- GET  /api/health               -> Health check
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app import config
from app.api import algorithms, examples, health, render

DESCRIPTION = __doc__ or "MathViz Unified API"


def create_app() -> FastAPI:
    config.ensure_dirs()

    app = FastAPI(title="MathViz Unified API", version=config.VERSION, description=DESCRIPTION)

    # CORS for frontend development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Serve generated media
    app.mount("/media", StaticFiles(directory=str(config.MEDIA_DIR)), name="media")

    # API routers
    app.include_router(algorithms.router)
    app.include_router(render.router)
    app.include_router(examples.router)
    app.include_router(health.router)

    @app.get("/", response_class=HTMLResponse)
    async def serve_frontend():
        """Serve the frontend HTML."""
        with open(config.FRONTEND_DIR / "index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)