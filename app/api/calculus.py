"""Calculus solving and visualization endpoints."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from fastapi import APIRouter, HTTPException

from app import config
from app.algorithms.calculus import (
    solve_chain_rule,
    solve_continuity,
    solve_derivative,
    solve_derivative_applications,
    solve_limit,
    solve_limit_at_infinity,
    solve_one_sided_limit,
    solve_power_rule,
    solve_product_rule,
    solve_quotient_rule,
    solve_sum_rule,
    solve_tangent_line,
    solve_two_sided_limit,
)
from app.schemas.models import (
    CalculusSolveRequest,
    CalculusSolveResponse,
    RenderResponse,
)

router = APIRouter(
    prefix="/api/calculus",
    tags=["calculus"],
)


# ============================================================
# Calculus problem type -> solver
# ============================================================

def solve_problem(request: CalculusSolveRequest) -> dict:
    """Run the appropriate calculus solver and return its solution."""

    problem_type = request.problem_type.lower().strip()

    if problem_type == "limit":
        if request.point is None:
            raise HTTPException(
                status_code=400,
                detail="Point is required for a limit.",
            )

        return solve_limit(
            request.expression,
            request.variable,
            request.point,
        )

    if problem_type == "one_sided_limit":
        if request.point is None or request.direction is None:
            raise HTTPException(
                status_code=400,
                detail="Point and direction are required for a one-sided limit.",
            )

        return solve_one_sided_limit(
            request.expression,
            request.variable,
            request.point,
            request.direction,
        )

    if problem_type == "two_sided_limit":
        if request.point is None:
            raise HTTPException(
                status_code=400,
                detail="Point is required for a two-sided limit.",
            )

        return solve_two_sided_limit(
            request.expression,
            request.variable,
            request.point,
        )

    if problem_type == "limit_at_infinity":
        return solve_limit_at_infinity(
            request.expression,
            request.variable,
            request.direction or "+",
        )

    if problem_type == "continuity":
        if request.point is None:
            raise HTTPException(
                status_code=400,
                detail="Point is required for continuity.",
            )

        return solve_continuity(
            request.expression,
            request.variable,
            request.point,
        )

    if problem_type == "derivative":
        return solve_derivative(
            request.expression,
            request.variable,
        )

    if problem_type == "tangent_line":
        if request.point is None:
            raise HTTPException(
                status_code=400,
                detail="Point is required for a tangent line.",
            )

        return solve_tangent_line(
            request.expression,
            request.variable,
            request.point,
        )

    if problem_type == "power_rule":
        return solve_power_rule(
            request.expression,
            request.variable,
        )

    if problem_type == "sum_rule":
        return solve_sum_rule(
            request.expression,
            request.variable,
        )

    if problem_type == "product_rule":
        return solve_product_rule(
            request.expression,
            request.variable,
        )

    if problem_type == "quotient_rule":
        return solve_quotient_rule(
            request.expression,
            request.variable,
        )

    if problem_type == "chain_rule":
        return solve_chain_rule(
            request.expression,
            request.variable,
        )

    if problem_type == "derivative_applications":
        return solve_derivative_applications(
            request.expression,
            request.variable,
        )

    raise HTTPException(
        status_code=400,
        detail=f"Unsupported calculus problem type: {problem_type}",
    )


# ============================================================
# Calculus -> Manim scene mapping
# ============================================================

CALCULUS_SCENES = {
    "limit": "LimitFromJSON",
    "one_sided_limit": "OneSidedLimitFromJSON",
    "two_sided_limit": "TwoSidedLimitFromJSON",
    "limit_at_infinity": "LimitAtInfinityFromJSON",
    "continuity": "ContinuityFromJSON",
    "derivative": "DerivativeFromJSON",
    "tangent_line": "TangentLineFromJSON",
    "power_rule": "PowerRuleFromJSON",
    "sum_rule": "SumRuleFromJSON",
    "product_rule": "ProductRuleFromJSON",
    "quotient_rule": "QuotientRuleFromJSON",
    "chain_rule": "ChainRuleFromJSON",
    "derivative_applications": "DerivativeApplicationsFromJSON",
}


# ============================================================
# Solve endpoint
# ============================================================

@router.post(
    "/solve",
    response_model=CalculusSolveResponse,
)
async def solve_calculus(
    request: CalculusSolveRequest,
):
    """Solve a supported calculus problem and return structured steps."""

    try:
        problem_type = request.problem_type.lower().strip()

        solution = solve_problem(request)

        return CalculusSolveResponse(
            problem_type=problem_type,
            solution=solution,
        )

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


# ============================================================
# Render endpoint
# ============================================================

@router.post(
    "/render",
    response_model=RenderResponse,
)
async def render_calculus(
    request: CalculusSolveRequest,
):
    """Solve a calculus problem and render its corresponding Manim scene."""

    try:
        problem_type = request.problem_type.lower().strip()

        if problem_type not in CALCULUS_SCENES:
            raise HTTPException(
                status_code=400,
                detail=f"No Manim scene available for: {problem_type}",
            )

        # --------------------------------------------------------
        # 1. Solve the calculus problem
        # --------------------------------------------------------

        solution = solve_problem(request)

        # --------------------------------------------------------
        # 2. Write solution JSON to a temporary file
        # --------------------------------------------------------

        tmp = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            delete=False,
            dir=str(config.TEMP_DIR),
            encoding="utf-8",
        )

        json.dump(solution, tmp, indent=2)
        tmp.close()

        input_json = Path(tmp.name)

        # --------------------------------------------------------
        # 3. Select the Manim scene
        # --------------------------------------------------------

        scene_name = CALCULUS_SCENES[problem_type]

        # --------------------------------------------------------
        # 4. Prepare output
        # --------------------------------------------------------

        config.MEDIA_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_name = f"calculus_{problem_type}.mp4"
        output_path = config.MEDIA_DIR / output_name

        # --------------------------------------------------------
        # 5. Run Manim
        # --------------------------------------------------------

        command = [
            sys.executable,
            "-m",
            "manim",
            "-qm",
            "--format=mp4",
            f"--media_dir={config.MEDIA_DIR}",
            "-o",
            output_name,
            str(
                config.BASE_DIR
                / "manim_engine"
                / "calculus_scenes.py"
            ),
            scene_name,
        ]

        env = os.environ.copy()

        # Calculus scenes read the JSON through this variable.
        env["MATHVIZ_INPUT_JSON"] = str(input_json)

        # Make sure Python can import the MathViz package.
        env["PYTHONPATH"] = config.as_pythonpath()

        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=str(config.BASE_DIR),
            env=env,
            timeout=300,
        )

        log = (
            process.stdout
            + "\n"
            + process.stderr
        )

        # --------------------------------------------------------
        # 6. Check Manim result
        # --------------------------------------------------------

        if process.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=(
                    "Calculus Manim render failed.\n\n"
                    f"{log[-8000:]}"
                ),
            )

        # --------------------------------------------------------
        # 7. Find the newly rendered video
        # --------------------------------------------------------

        matches = list(
            config.MEDIA_DIR.rglob(output_name)
        )

        # Do not select the old final video already sitting
        # directly in MEDIA_DIR.
        matches = [
            path
            for path in matches
            if path.resolve() != output_path.resolve()
        ]

        if not matches:
            raise HTTPException(
                status_code=500,
                detail=(
                    "Manim completed, but the output video "
                    "could not be found.\n\n"
                    f"{log[-8000:]}"
                ),
            )

        # If several matching files exist, use the newest one.
        source_path = max(
            matches,
            key=lambda path: path.stat().st_mtime,
        )

        # Replace the old final video with the newly rendered one.
        try:
            source_path.replace(output_path)
        except OSError:
            import shutil

            shutil.copy2(
                source_path,
                output_path,
            )

        # --------------------------------------------------------
        # 8. Return URL for the frontend video player
        # --------------------------------------------------------

        return RenderResponse(
            video_url=f"/media/{output_path.name}",
            filename=output_path.name,
            log=log,
        )

    except HTTPException:
        raise

    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=500,
            detail="Calculus video rendering timed out.",
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )

    finally:
        # --------------------------------------------------------
        # 9. Remove temporary JSON file
        # --------------------------------------------------------

        try:
            if "input_json" in locals():
                input_json.unlink(missing_ok=True)
        except OSError:
            pass