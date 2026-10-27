"""
Test suite for MathViz backend
"""

import sys
import os
# Ensure root is on python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.distributions import DistributionEngine, CalculateRequest
from backend.monte_carlo import MonteCarloEngine, MonteCarloRequest
from backend.empirical_fitting import EmpiricalAnalyzer, FitDataRequest

def test_normal():
    req = CalculateRequest(
        distribution="normal",
        params={"mu": 0.0, "sigma": 1.0},
        calc_mode="interval",
        a=-1.0,
        b=1.0
    )
    res = DistributionEngine.calculate(req)
    # 1 sigma rule: ~68.27%
    assert abs(res["prob"] - 0.682689) < 0.001
    assert res["mean"] == 0.0
    assert res["variance"] == 1.0
    print("[PASS] Normal distribution test passed: P(-1 <= X <= 1) =", res["prob_percentage"])

def test_binomial():
    req = CalculateRequest(
        distribution="binomial",
        params={"n": 10, "p": 0.5},
        calc_mode="equal",
        b=5
    )
    res = DistributionEngine.calculate(req)
    # Binomial(10, 0.5), k=5: (10 choose 5) * 0.5^10 = 252 / 1024 = 0.24609
    assert abs(res["prob"] - 0.24609) < 0.001
    assert res["mean"] == 5.0
    assert res["variance"] == 2.5
    print("[PASS] Binomial distribution test passed: P(X = 5) =", res["prob_percentage"])

def test_poisson():
    req = CalculateRequest(
        distribution="poisson",
        params={"lambda": 4.0},
        calc_mode="interval",
        a=0,
        b=4
    )
    res = DistributionEngine.calculate(req)
    assert res["mean"] == 4.0
    assert res["variance"] == 4.0
    print("[PASS] Poisson distribution test passed: P(0 <= X <= 4) =", res["prob_percentage"])

def test_exponential():
    req = CalculateRequest(
        distribution="exponential",
        params={"lambda": 2.0},
        calc_mode="interval",
        a=0.0,
        b=1.0
    )
    res = DistributionEngine.calculate(req)
    # P(0 <= X <= 1) for Exp(2) = 1 - e^-2 = 0.86466
    assert abs(res["prob"] - 0.86466) < 0.001
    assert res["mean"] == 0.5
    print("[PASS] Exponential distribution test passed: P(0 <= X <= 1) =", res["prob_percentage"])

def test_monte_carlo():
    req = MonteCarloRequest(
        experiment="dice_sum",
        sample_size=2000,
        params={"num_dice": 2}
    )
    res = MonteCarloEngine.simulate(req)
    assert res["sample_size"] == 2000
    assert abs(res["empirical"]["mean"] - 7.0) < 0.5
    assert len(res["histogram"]) > 0
    assert len(res["convergence_curve"]) > 0
    print("[PASS] Monte Carlo test passed: empirical mean =", res["empirical"]["mean"], "vs theoretical =", res["theoretical"]["mean"])

def test_empirical_fit():
    # Generate 100 samples from normal distribution
    import numpy as np
    rng = np.random.default_rng(42)
    sample_data = list(rng.normal(loc=10.0, scale=2.5, size=200))
    req = FitDataRequest(data=sample_data, fit_models=["normal"])
    res = EmpiricalAnalyzer.analyze_and_fit(req)
    assert res["sample_size"] == 200
    assert abs(res["metrics"]["mean"] - 10.0) < 0.5
    assert abs(res["fitted_models"]["normal"]["params"]["mu"] - 10.0) < 0.5
    print("[PASS] Empirical fit test passed: fitted mu =", res["fitted_models"]["normal"]["params"]["mu"])

def test_app_endpoints():
    from backend.app import calculate_distribution, compare_distributions, run_monte_carlo, fit_empirical_data, solve_scenario, CompareRequest, ScenarioSolveRequest
    
    # 1. calculate endpoint
    c_res = calculate_distribution(CalculateRequest(distribution="normal", params={"mu": 5.0, "sigma": 2.0}, calc_mode="interval", a=3.0, b=7.0))
    assert abs(c_res["prob"] - 0.682689) < 0.001
    print("[PASS] app endpoint calculate_distribution passed")

    # 2. compare endpoint
    comp_req = CompareRequest(
        distro_a=CalculateRequest(distribution="normal", params={"mu": 0, "sigma": 1}),
        distro_b=CalculateRequest(distribution="student_t", params={"df": 4})
    )
    comp_res = compare_distributions(comp_req)
    assert "distro_a" in comp_res and "distro_b" in comp_res
    print("[PASS] app endpoint compare_distributions passed")

    # 3. scenario endpoint
    scen_req = ScenarioSolveRequest(scenario_id="server_outage", params={"lambda": 4.0, "threshold": 6})
    scen_res = solve_scenario(scen_req)
    assert "prob_percentage" in scen_res
    print("[PASS] app endpoint solve_scenario passed")

if __name__ == "__main__":
    test_normal()
    test_binomial()
    test_poisson()
    test_exponential()
    test_monte_carlo()
    test_empirical_fit()
    test_app_endpoints()
    print("\nALL BACKEND & ENDPOINT TESTS PASSED SUCCESSFULLY!")
