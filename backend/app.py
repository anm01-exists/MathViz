"""
MathViz - Interactive Probability Studio Backend
FastAPI server providing high-precision theoretical statistics,
Monte Carlo simulation mechanics, and empirical distribution fitting.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import os

from backend.distributions import DistributionEngine, CalculateRequest
from backend.monte_carlo import MonteCarloEngine, MonteCarloRequest
from backend.empirical_fitting import EmpiricalAnalyzer, FitDataRequest

app = FastAPI(
    title="MathViz Probability Studio API",
    description="Computational probability and statistical distribution analytics kernel.",
    version="2.0.0"
)

# Enable CORS for local development and multi-port setups
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompareRequest(BaseModel):
    distro_a: CalculateRequest
    distro_b: CalculateRequest

class ScenarioSolveRequest(BaseModel):
    scenario_id: str
    params: Dict[str, float]

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "MathViz Kernel", "version": "2.0.0"}

@app.post("/api/distribution/calculate")
def calculate_distribution(req: CalculateRequest):
    try:
        return DistributionEngine.calculate(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/distribution/compare")
def compare_distributions(req: CompareRequest):
    try:
        res_a = DistributionEngine.calculate(req.distro_a)
        res_b = DistributionEngine.calculate(req.distro_b)
        
        # Calculate combined x range
        x_min = min(res_a.get("x_min", 0), res_b.get("x_min", 0))
        x_max = max(res_a.get("x_max", 10), res_b.get("x_max", 10))
        
        return {
            "distro_a": res_a,
            "distro_b": res_b,
            "domain": [x_min, x_max]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/monte-carlo/simulate")
def run_monte_carlo(req: MonteCarloRequest):
    try:
        return MonteCarloEngine.simulate(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/empirical/fit")
def fit_empirical_data(req: FitDataRequest):
    try:
        return EmpiricalAnalyzer.analyze_and_fit(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/scenarios")
def get_scenarios():
    return {
        "scenarios": [
            {
                "id": "server_outage",
                "title": "Cloud Server Outage Risk",
                "category": "High Reliability Engineering",
                "distribution": "poisson",
                "description": "Datacenter outage occurrence analysis using Poisson counting process.",
                "default_params": {"lambda": 3.2, "threshold": 5},
                "param_metadata": [
                    {"key": "lambda", "label": "Expected Monthly Outages (λ)", "min": 0.5, "max": 15.0, "step": 0.1, "value": 3.2},
                    {"key": "threshold", "label": "Critical Threshold (k)", "min": 1, "max": 20, "step": 1, "value": 5}
                ]
            },
            {
                "id": "checkout_funnel",
                "title": "E-Commerce Checkout Funnel",
                "category": "Growth & CRO Analytics",
                "distribution": "binomial",
                "description": "Conversion cohort analysis using Bernoulli trials and Binomial distribution.",
                "default_params": {"n": 50, "p": 0.08, "k_min": 6},
                "param_metadata": [
                    {"key": "n", "label": "Cohort Sample Visitors (n)", "min": 10, "max": 200, "step": 5, "value": 50},
                    {"key": "p", "label": "Baseline Conversion Rate (p)", "min": 0.01, "max": 0.50, "step": 0.01, "value": 0.08},
                    {"key": "k_min", "label": "Target Minimum Orders", "min": 1, "max": 30, "step": 1, "value": 6}
                ]
            },
            {
                "id": "shaft_tolerance",
                "title": "Precision Shaft Diameter Tolerance",
                "category": "Precision Manufacturing",
                "distribution": "normal",
                "description": "Quality defect rate estimation for industrial CNC machining under Normal process noise.",
                "default_params": {"mu": 50.0, "sigma": 0.05, "lower_spec": 49.90, "upper_spec": 50.10},
                "param_metadata": [
                    {"key": "mu", "label": "Nominal Target Mean (mm)", "min": 10.0, "max": 100.0, "step": 0.1, "value": 50.0},
                    {"key": "sigma", "label": "Process Standard Dev σ (mm)", "min": 0.01, "max": 0.20, "step": 0.01, "value": 0.05},
                    {"key": "lower_spec", "label": "Lower Spec Limit (LSL)", "min": 49.0, "max": 50.0, "step": 0.01, "value": 49.90},
                    {"key": "upper_spec", "label": "Upper Spec Limit (USL)", "min": 50.0, "max": 51.0, "step": 0.01, "value": 50.10}
                ]
            }
        ]
    }

@app.post("/api/scenarios/solve")
def solve_scenario(req: ScenarioSolveRequest):
    s_id = req.scenario_id
    p = req.params
    
    if s_id == "server_outage":
        lam = float(p.get("lambda", 3.2))
        k = int(p.get("threshold", 5))
        # P(X >= k) = 1 - P(X <= k - 1)
        res = DistributionEngine.calculate_poisson(lam, k, 100, mode="greater")
        return {
            "scenario_id": s_id,
            "result_label": f"Probability of {k} or more outages P(X ≥ {k}):",
            "prob": res["prob"],
            "prob_percentage": res["prob_percentage"],
            "steps": [
                f"Rate parameter λ = {lam:.2f} events/interval",
                f"Evaluation condition: k ≥ {k}",
                f"P(X ≥ {k}) = 1 - ∑_{{i=0}}^{{{k-1}}} (λⁱ e^{{-λ}}) / i! = {res['prob_percentage']}"
            ],
            "distribution_data": res
        }
    elif s_id == "checkout_funnel":
        n = int(p.get("n", 50))
        prob_p = float(p.get("p", 0.08))
        k_min = int(p.get("k_min", 6))
        res = DistributionEngine.calculate_binomial(n, prob_p, k_min, n, mode="greater")
        expected_orders = n * prob_p
        return {
            "scenario_id": s_id,
            "result_label": f"Probability of at least {k_min} conversions P(X ≥ {k_min}):",
            "prob": res["prob"],
            "prob_percentage": res["prob_percentage"],
            "steps": [
                f"Cohort sample size n = {n}, conversion probability p = {prob_p:.2%}",
                f"Expected conversions E[X] = n · p = {expected_orders:.1f}",
                f"P(X ≥ {k_min}) = 1 - ∑_{{i=0}}^{{{k_min-1}}} (n choose i) pⁱ (1-p)^{{n-i}} = {res['prob_percentage']}"
            ],
            "distribution_data": res
        }
    elif s_id == "shaft_tolerance":
        mu = float(p.get("mu", 50.0))
        sigma = max(0.001, float(p.get("sigma", 0.05)))
        lsl = float(p.get("lower_spec", 49.90))
        usl = float(p.get("upper_spec", 50.10))
        
        in_spec_res = DistributionEngine.calculate_normal(mu, sigma, lsl, usl, mode="interval")
        defect_rate = max(0.0, 1.0 - in_spec_res["prob"])
        z_low = (lsl - mu) / sigma
        z_high = (usl - mu) / sigma
        
        return {
            "scenario_id": s_id,
            "result_label": f"Process Defect Rate (Out of Spec):",
            "prob": round(defect_rate, 5),
            "prob_percentage": f"{defect_rate * 100:.2f}%",
            "steps": [
                f"Nominal target μ = {mu:.2f} mm, process noise σ = {sigma:.3f} mm",
                f"Z-scores: Z_LSL = ({lsl} - {mu})/{sigma} = {z_low:.2f}, Z_USL = ({usl} - {mu})/{sigma} = {z_high:.2f}",
                f"In-Spec yield = Φ({z_high:.2f}) - Φ({z_low:.2f}) = {in_spec_res['prob_percentage']}",
                f"Defect rate = 1 - Yield = {defect_rate * 100:.2f}%"
            ],
            "distribution_data": in_spec_res
        }
    else:
        raise HTTPException(status_code=404, detail="Scenario not found")

# Static files mount
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def serve_root():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "MathViz Backend Active. Place UI in static/index.html"}
