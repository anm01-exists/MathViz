import os
import re
import sys
import subprocess
from pathlib import Path
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .graph import Graph
from .bfs import bfs
from .dfs import dfs
from .dijkstra import dijkstra
from .integration.approximating_areas.schema import ApproximatingAreaInput
from .integration.approximating_areas.solver import approximating_area
from .integration.basic_integration.schema import BasicIntegrationInput
from .integration.basic_integration.solver import basic_integration

from .integration.definite_integral.schema import DefiniteIntegralInput
from .integration.definite_integral.solver import definite_integral

from .integration.fundamental_theorem.schema import FundamentalTheoremInput
from .integration.fundamental_theorem.solver import fundamental_theorem

from .integration.substitution.schema import SubstitutionInput
from .integration.substitution.solver import substitution

from .integration.integration_by_parts.schema import IntegrationByPartsInput
from .integration.integration_by_parts.solver import integration_by_parts

from .integration.applications.schema import ApplicationsInput
from .integration.applications.solver import applications

from .integration.area_under_curve.schema import AreaUnderCurveInput
from .integration.area_under_curve.solver import area_under_curve

from .integration.area_between_curves.schema import AreaBetweenCurvesInput
from .integration.area_between_curves.solver import area_between_curves


def clean_json(data):
    """
    Convert values that cannot be safely returned as JSON.
    Dijkstra uses infinity (inf) for unknown distances,
    so we convert inf to None.
    """

    if isinstance(data, dict):
        return {
            key: clean_json(value)
            for key, value in data.items()
        }

    if isinstance(data, list):
        return [
            clean_json(value)
            for value in data
        ]

    if data == float("inf"):
        return None

    return data


app = FastAPI(title="MathViz Graph API")
PROJECT_ROOT = Path(__file__).resolve().parent.parent

VIDEO_DIR = PROJECT_ROOT / "media" / "videos" / "dynamic_integration"
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

MANIM_FILE = PROJECT_ROOT / "manim" / "integration" / "dynamic_integration.py"

app.mount(
    "/generated-videos",
    StaticFiles(directory=str(VIDEO_DIR)),
    name="generated-videos",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "MathViz Graph API is running"
    }


@app.get("/bfs")
def run_bfs(start: str = "A"):
    graph = Graph()

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")

    result = bfs(graph, start)

    return clean_json(result)


@app.get("/dfs")
def run_dfs(start: str = "A"):
    graph = Graph()

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")

    result = dfs(graph, start)

    return clean_json(result)


@app.get("/dijkstra")
def run_dijkstra(
    start: str = "A",
    destination: str = "D"
):
    graph = Graph(weighted=True)

    graph.add_edge("A", "B", 4)
    graph.add_edge("A", "C", 2)
    graph.add_edge("B", "D", 1)
    graph.add_edge("C", "D", 3)

    result = dijkstra(graph, start, destination)

    return clean_json(result)


@app.post("/integration/approximating-area")
def run_approximating_area(data: ApproximatingAreaInput):

    result = approximating_area(data)

    return result.model_dump()
@app.post("/integration/basic-integration")
def run_basic_integration(data: BasicIntegrationInput):
    result = basic_integration(data)
    return result.model_dump()


@app.post("/integration/definite-integral")
def run_definite_integral(data: DefiniteIntegralInput):
    result = definite_integral(data)
    return result.model_dump()


@app.post("/integration/fundamental-theorem")
def run_fundamental_theorem(data: FundamentalTheoremInput):
    result = fundamental_theorem(data)
    return result.model_dump()


@app.post("/integration/substitution")
def run_substitution(data: SubstitutionInput):
    result = substitution(data)
    return result.model_dump()


@app.post("/integration/integration-by-parts")
def run_integration_by_parts(data: IntegrationByPartsInput):
    result = integration_by_parts(data)
    return result.model_dump()


@app.post("/integration/applications")
def run_applications(data: ApplicationsInput):
    result = applications(data)
    return result.model_dump()


@app.post("/integration/area-under-curve")
def run_area_under_curve(data: AreaUnderCurveInput):
    result = area_under_curve(data)
    return result.model_dump()


@app.post("/integration/area-between-curves")
def run_area_between_curves(data: AreaBetweenCurvesInput):
    result = area_between_curves(data)
    return result.model_dump()
@app.post("/integration/generate-video")
def generate_integration_video(data: BasicIntegrationInput):
    expression = data.function.strip()

    # Accept only basic mathematical expressions using x.
    allowed_pattern = r"^[0-9a-zA-Z_+\-*/().,\s^]+$"

    if not expression or not re.fullmatch(allowed_pattern, expression):
        raise HTTPException(
            status_code=400,
            detail="Please enter a valid mathematical expression.",
        )

    # Generate a unique filename for each requested equation.
    import hashlib

    video_name = hashlib.sha256(
        expression.encode("utf-8")
    ).hexdigest()[:16] + ".mp4"

    video_path = VIDEO_DIR / video_name

    # Reuse a video only when the exact expression has already rendered.
    marker_path = VIDEO_DIR / (video_name + ".txt")

    if video_path.exists() and marker_path.exists():
        if marker_path.read_text(encoding="utf-8") == expression:
            return {
                "function": expression,
                "video_url": f"/generated-videos/{video_name}",
            }

    if not MANIM_FILE.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Manim file not found: {MANIM_FILE}",
        )

    env = os.environ.copy()
    env["MATHVIZ_FUNCTION"] = expression

    python_executable = PROJECT_ROOT / "manim_env" / "Scripts" / "python.exe"

    try:
        completed = subprocess.run(
            [
                str(python_executable),
                "-m",
                "manim",
                "-ql",
                str(MANIM_FILE),
                "DynamicIntegration",
                "--media_dir",
                str(PROJECT_ROOT / "media"),
            ],
            cwd=str(PROJECT_ROOT),
            env=env,
            capture_output=True,
            text=True,
            timeout=180,
        )

    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=504,
            detail="Video generation took too long. Please try a simpler equation.",
        )

    if completed.returncode != 0:
        raise HTTPException(
            status_code=500,
            detail="Manim video generation failed. Check the backend terminal for details.",
        )

    rendered_video = (
        PROJECT_ROOT
        / "media"
        / "videos"
        / "dynamic_integration"
        / "480p15"
        / "DynamicIntegration.mp4"
    )

    if not rendered_video.exists():
        raise HTTPException(
            status_code=500,
            detail="Manim finished but the generated MP4 could not be found.",
        )

    import shutil

    shutil.copy2(rendered_video, video_path)
    marker_path.write_text(expression, encoding="utf-8")

    return {
        "function": expression,
        "video_url": f"/generated-videos/{video_name}",
    }