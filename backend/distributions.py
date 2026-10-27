"""
Statistical Distribution Engine
Provides theoretical calculations, moments, probability density/mass,
cumulative distributions, and interval evaluations using NumPy and math.
"""

from typing import Dict, Any, List, Optional
import math
import numpy as np
from pydantic import BaseModel, Field

class CalculateRequest(BaseModel):
    distribution: str = Field(..., description="Distribution type: normal, binomial, poisson, exponential, uniform, student_t, geometric")
    params: Dict[str, float] = Field(default_factory=dict, description="Distribution parameters (e.g. mu, sigma, n, p, lambda)")
    calc_mode: str = Field(default="interval", description="Calculation mode: interval, less, greater, equal")
    a: Optional[float] = Field(default=-1.0, description="Lower limit or threshold")
    b: Optional[float] = Field(default=1.0, description="Upper limit")
    num_points: Optional[int] = Field(default=150, description="Number of points to sample for curve/plot")

def normal_cdf(x: float, mu: float, sigma: float) -> float:
    return 0.5 * (1.0 + math.erf((x - mu) / (sigma * math.sqrt(2.0))))

def normal_pdf(x: float, mu: float, sigma: float) -> float:
    z = (x - mu) / sigma
    return (1.0 / (sigma * math.sqrt(2.0 * math.pi))) * math.exp(-0.5 * z * z)

class DistributionEngine:
    @staticmethod
    def calculate_normal(mu: float, sigma: float, a: float, b: float, mode: str, num_points: int = 150) -> Dict[str, Any]:
        sigma = max(1e-4, float(sigma))
        mu = float(mu)
        
        mean = mu
        variance = sigma ** 2
        std_dev = sigma
        skewness = 0.0
        kurtosis = 0.0
        
        x_min = mu - 4.2 * sigma
        x_max = mu + 4.2 * sigma
        
        if mode == "less":
            prob = normal_cdf(b, mu, sigma)
            expr = f"P(X ≤ {b:.2f})"
            shaded_a = x_min
            shaded_b = b
        elif mode == "greater":
            prob = 1.0 - normal_cdf(a, mu, sigma)
            expr = f"P(X ≥ {a:.2f})"
            shaded_a = a
            shaded_b = x_max
        else: # interval [a, b]
            low, high = min(a, b), max(a, b)
            prob = normal_cdf(high, mu, sigma) - normal_cdf(low, mu, sigma)
            expr = f"P({low:.2f} ≤ X ≤ {high:.2f})"
            shaded_a = low
            shaded_b = high
            
        prob = max(0.0, min(1.0, prob))
        
        xs = np.linspace(x_min, x_max, num_points)
        points = []
        for x in xs:
            x_f = float(x)
            points.append({
                "x": round(x_f, 4),
                "y": round(normal_pdf(x_f, mu, sigma), 5),
                "cdf": round(normal_cdf(x_f, mu, sigma), 5)
            })
            
        return {
            "distribution": "normal",
            "type": "continuous",
            "name": f"Normal Distribution N({mu:.2f}, {sigma:.2f}²)",
            "formula_title": "Probability Density Function f(x):",
            "formula_text": "f(x) = (1 / (σ √(2π))) · exp(-0.5 · ((x - μ) / σ)²)",
            "domain_label": "(-∞, +∞)",
            "mean": round(mean, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "skewness": round(skewness, 4),
            "kurtosis": round(kurtosis, 4),
            "skew_formula": "Symmetric (0.00)",
            "prob": round(prob, 5),
            "prob_percentage": f"{prob * 100:.2f}%",
            "expression": expr,
            "x_min": round(x_min, 4),
            "x_max": round(x_max, 4),
            "shaded_range": [round(shaded_a, 4), round(shaded_b, 4)],
            "points": points,
            "markers": {
                "mean": round(mu, 4),
                "sigmas": [
                    {"label": "-3σ", "x": round(mu - 3 * sigma, 4)},
                    {"label": "-2σ", "x": round(mu - 2 * sigma, 4)},
                    {"label": "-1σ", "x": round(mu - 1 * sigma, 4)},
                    {"label": "+1σ", "x": round(mu + 1 * sigma, 4)},
                    {"label": "+2σ", "x": round(mu + 2 * sigma, 4)},
                    {"label": "+3σ", "x": round(mu + 3 * sigma, 4)},
                ]
            }
        }

    @staticmethod
    def calculate_binomial(n: int, p: float, a: float, b: float, mode: str) -> Dict[str, Any]:
        n = max(1, int(round(n)))
        p = max(0.0001, min(0.9999, float(p)))
        
        mean = float(n * p)
        variance = float(n * p * (1 - p))
        std_dev = float(math.sqrt(variance))
        skewness = float((1 - 2 * p) / math.sqrt(variance)) if variance > 0 else 0.0
        kurtosis = float((1 - 6 * p * (1 - p)) / variance) if variance > 0 else 0.0
        
        def pmf(k: int) -> float:
            if 0 <= k <= n:
                return math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))
            return 0.0
            
        a_int = int(math.ceil(a))
        b_int = int(math.floor(b))
        
        if mode == "less":
            prob = sum(pmf(k) for k in range(0, min(n, b_int) + 1)) if b_int >= 0 else 0.0
            expr = f"P(X ≤ {b_int})"
            selected_k = [k for k in range(0, n + 1) if k <= b_int]
        elif mode == "greater":
            prob = sum(pmf(k) for k in range(max(0, a_int), n + 1)) if a_int <= n else 0.0
            expr = f"P(X ≥ {a_int})"
            selected_k = [k for k in range(0, n + 1) if k >= a_int]
        elif mode == "equal":
            k_val = int(round(b))
            prob = pmf(k_val) if 0 <= k_val <= n else 0.0
            expr = f"P(X = {k_val})"
            selected_k = [k_val] if 0 <= k_val <= n else []
        else: # interval
            low = max(0, a_int)
            high = min(n, b_int)
            prob = sum(pmf(k) for k in range(low, high + 1)) if high >= low else 0.0
            expr = f"P({low} ≤ X ≤ {high})"
            selected_k = [k for k in range(low, high + 1)]
            
        prob = max(0.0, min(1.0, prob))
        
        points = []
        cum_p = 0.0
        for k in range(0, n + 1):
            pk = pmf(k)
            cum_p += pk
            points.append({
                "x": k,
                "y": round(pk, 5),
                "cdf": round(min(1.0, cum_p), 5),
                "in_selection": k in selected_k
            })
            
        return {
            "distribution": "binomial",
            "type": "discrete",
            "name": f"Binomial Distribution B(n={n}, p={p:.2f})",
            "formula_title": "Probability Mass Function P(X = k):",
            "formula_text": "P(X = k) = (n! / (k!(n-k)!)) · p^k · (1 - p)^(n - k)",
            "domain_label": f"{{0, 1, ..., {n}}}",
            "mean": round(mean, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "skewness": round(skewness, 4),
            "kurtosis": round(kurtosis, 4),
            "skew_formula": "(1-2p) / √(np(1-p))",
            "prob": round(prob, 5),
            "prob_percentage": f"{prob * 100:.2f}%",
            "expression": expr,
            "x_min": 0,
            "x_max": n,
            "selected_k": selected_k,
            "points": points,
            "markers": {
                "mean": round(mean, 4)
            }
        }

    @staticmethod
    def calculate_poisson(lambda_param: float, a: float, b: float, mode: str) -> Dict[str, Any]:
        lam = max(0.05, float(lambda_param))
        mean = lam
        variance = lam
        std_dev = math.sqrt(lam)
        skewness = 1.0 / math.sqrt(lam)
        kurtosis = 1.0 / lam
        
        def pmf(k: int) -> float:
            if k < 0:
                return 0.0
            # Use log-gamma to avoid overflow for large k
            log_p = k * math.log(lam) - lam - math.lgamma(k + 1)
            return math.exp(log_p)
            
        a_int = int(math.ceil(a))
        b_int = int(math.floor(b))
        k_max = max(18, int(math.ceil(lam + 4.5 * std_dev)))
        
        if mode == "less":
            prob = sum(pmf(k) for k in range(0, min(k_max, b_int) + 1)) if b_int >= 0 else 0.0
            expr = f"P(X ≤ {b_int})"
            selected_k = [k for k in range(0, k_max + 1) if k <= b_int]
        elif mode == "greater":
            prob = sum(pmf(k) for k in range(max(0, a_int), k_max + 1)) if a_int <= k_max else 0.0
            expr = f"P(X ≥ {a_int})"
            selected_k = [k for k in range(0, k_max + 1) if k >= a_int]
        elif mode == "equal":
            k_val = int(round(b))
            prob = pmf(k_val) if k_val >= 0 else 0.0
            expr = f"P(X = {k_val})"
            selected_k = [k_val] if 0 <= k_val <= k_max else []
        else: # interval
            low = max(0, a_int)
            high = b_int
            prob = sum(pmf(k) for k in range(low, high + 1)) if high >= low else 0.0
            expr = f"P({low} ≤ X ≤ {high})"
            selected_k = [k for k in range(low, high + 1)]
            
        prob = max(0.0, min(1.0, prob))
        
        points = []
        cum_p = 0.0
        for k in range(0, k_max + 1):
            pk = pmf(k)
            cum_p += pk
            points.append({
                "x": k,
                "y": round(pk, 5),
                "cdf": round(min(1.0, cum_p), 5),
                "in_selection": k in selected_k
            })
            
        return {
            "distribution": "poisson",
            "type": "discrete",
            "name": f"Poisson Distribution Pois(λ={lam:.2f})",
            "formula_title": "Probability Mass Function P(X = k):",
            "formula_text": "P(X = k) = (λ^k · e^(-λ)) / k!",
            "domain_label": "{0, 1, 2, ... ∞}",
            "mean": round(mean, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "skewness": round(skewness, 4),
            "kurtosis": round(kurtosis, 4),
            "skew_formula": "1 / √λ",
            "prob": round(prob, 5),
            "prob_percentage": f"{prob * 100:.2f}%",
            "expression": expr,
            "x_min": 0,
            "x_max": k_max,
            "selected_k": selected_k,
            "points": points,
            "markers": {
                "mean": round(mean, 4)
            }
        }

    @staticmethod
    def calculate_exponential(lambda_param: float, a: float, b: float, mode: str, num_points: int = 150) -> Dict[str, Any]:
        lam = max(0.01, float(lambda_param))
        mean = 1.0 / lam
        variance = 1.0 / (lam ** 2)
        std_dev = 1.0 / lam
        skewness = 2.0
        kurtosis = 6.0
        
        def pdf(x: float) -> float:
            return lam * math.exp(-lam * x) if x >= 0 else 0.0
            
        def cdf(x: float) -> float:
            return 1.0 - math.exp(-lam * x) if x >= 0 else 0.0
            
        x_min = 0.0
        x_max = max(5.0, 5.0 / lam)
        
        if mode == "less":
            prob = cdf(b)
            expr = f"P(X ≤ {max(0.0, b):.2f})"
            shaded_a = 0.0
            shaded_b = max(0.0, b)
        elif mode == "greater":
            prob = 1.0 - cdf(a)
            expr = f"P(X ≥ {max(0.0, a):.2f})"
            shaded_a = max(0.0, a)
            shaded_b = x_max
        else: # interval
            low = max(0.0, min(a, b))
            high = max(0.0, max(a, b))
            prob = cdf(high) - cdf(low)
            expr = f"P({low:.2f} ≤ X ≤ {high:.2f})"
            shaded_a = low
            shaded_b = high
            
        prob = max(0.0, min(1.0, prob))
        
        xs = np.linspace(x_min, x_max, num_points)
        points = []
        for x in xs:
            x_f = float(x)
            points.append({
                "x": round(x_f, 4),
                "y": round(pdf(x_f), 5),
                "cdf": round(cdf(x_f), 5)
            })
            
        return {
            "distribution": "exponential",
            "type": "continuous",
            "name": f"Exponential Distribution Exp(λ={lam:.2f})",
            "formula_title": "Probability Density Function f(x):",
            "formula_text": "f(x) = λ · e^(-λ x)   for x ≥ 0",
            "domain_label": "[0, +∞)",
            "mean": round(mean, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "skewness": round(skewness, 4),
            "kurtosis": round(kurtosis, 4),
            "skew_formula": "Invariant: 2.00",
            "prob": round(prob, 5),
            "prob_percentage": f"{prob * 100:.2f}%",
            "expression": expr,
            "x_min": round(x_min, 4),
            "x_max": round(x_max, 4),
            "shaded_range": [round(shaded_a, 4), round(shaded_b, 4)],
            "points": points,
            "markers": {
                "mean": round(mean, 4)
            }
        }

    @staticmethod
    def calculate_uniform(a_bound: float, b_bound: float, a: float, b: float, mode: str, num_points: int = 150) -> Dict[str, Any]:
        low_bound = min(a_bound, b_bound)
        high_bound = max(a_bound, b_bound)
        if high_bound - low_bound < 1e-4:
            high_bound = low_bound + 1.0
            
        width = high_bound - low_bound
        mean = (low_bound + high_bound) / 2.0
        variance = (width ** 2) / 12.0
        std_dev = math.sqrt(variance)
        skewness = 0.0
        kurtosis = -1.2
        
        def pdf(x: float) -> float:
            return (1.0 / width) if (low_bound <= x <= high_bound) else 0.0
            
        def cdf(x: float) -> float:
            if x < low_bound: return 0.0
            if x > high_bound: return 1.0
            return (x - low_bound) / width
            
        margin = width * 0.2
        x_min = low_bound - margin
        x_max = high_bound + margin
        
        if mode == "less":
            prob = cdf(b)
            expr = f"P(X ≤ {b:.2f})"
            shaded_a = low_bound
            shaded_b = min(high_bound, max(low_bound, b))
        elif mode == "greater":
            prob = 1.0 - cdf(a)
            expr = f"P(X ≥ {a:.2f})"
            shaded_a = min(high_bound, max(low_bound, a))
            shaded_b = high_bound
        else: # interval
            val_a = min(a, b)
            val_b = max(a, b)
            prob = cdf(val_b) - cdf(val_a)
            expr = f"P({val_a:.2f} ≤ X ≤ {val_b:.2f})"
            shaded_a = min(high_bound, max(low_bound, val_a))
            shaded_b = min(high_bound, max(low_bound, val_b))
            
        prob = max(0.0, min(1.0, prob))
        
        xs = np.linspace(x_min, x_max, num_points)
        points = []
        for x in xs:
            x_f = float(x)
            points.append({
                "x": round(x_f, 4),
                "y": round(pdf(x_f), 5),
                "cdf": round(cdf(x_f), 5)
            })
            
        return {
            "distribution": "uniform",
            "type": "continuous",
            "name": f"Uniform Distribution U({low_bound:.2f}, {high_bound:.2f})",
            "formula_title": "Probability Density Function f(x):",
            "formula_text": f"f(x) = 1 / ({high_bound:.2f} - {low_bound:.2f}) = {1.0/width:.4f} for x ∈ [{low_bound:.2f}, {high_bound:.2f}]",
            "domain_label": f"[{low_bound:.2f}, {high_bound:.2f}]",
            "mean": round(mean, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "skewness": round(skewness, 4),
            "kurtosis": round(kurtosis, 4),
            "skew_formula": "Symmetric (0.00)",
            "prob": round(prob, 5),
            "prob_percentage": f"{prob * 100:.2f}%",
            "expression": expr,
            "x_min": round(x_min, 4),
            "x_max": round(x_max, 4),
            "shaded_range": [round(shaded_a, 4), round(shaded_b, 4)],
            "points": points,
            "markers": {
                "mean": round(mean, 4)
            }
        }

    @staticmethod
    def calculate_geometric(p: float, a: float, b: float, mode: str) -> Dict[str, Any]:
        p = max(0.01, min(0.99, float(p)))
        mean = 1.0 / p
        variance = (1 - p) / (p ** 2)
        std_dev = math.sqrt(variance)
        skewness = (2 - p) / math.sqrt(1 - p)
        kurtosis = 6.0 + (p ** 2) / (1 - p)
        
        def pmf(k: int) -> float:
            return ((1 - p) ** (k - 1)) * p if k >= 1 else 0.0
            
        def cdf(k: int) -> float:
            return 1.0 - ((1 - p) ** k) if k >= 1 else 0.0
            
        k_max = max(15, int(math.ceil(mean + 4 * std_dev)))
        a_int = int(math.ceil(a))
        b_int = int(math.floor(b))
        
        if mode == "less":
            prob = cdf(b_int)
            expr = f"P(X ≤ {b_int})"
            selected_k = [k for k in range(1, k_max + 1) if k <= b_int]
        elif mode == "greater":
            prob = 1.0 - cdf(a_int - 1) if a_int >= 1 else 1.0
            expr = f"P(X ≥ {a_int})"
            selected_k = [k for k in range(1, k_max + 1) if k >= a_int]
        elif mode == "equal":
            k_val = int(round(b))
            prob = pmf(k_val)
            expr = f"P(X = {k_val})"
            selected_k = [k_val] if 1 <= k_val <= k_max else []
        else: # interval
            low = max(1, a_int)
            high = b_int
            prob = sum(pmf(k) for k in range(low, high + 1)) if high >= low else 0.0
            expr = f"P({low} ≤ X ≤ {high})"
            selected_k = [k for k in range(low, high + 1)]
            
        prob = max(0.0, min(1.0, prob))
        
        points = []
        cum_p = 0.0
        for k in range(1, k_max + 1):
            pk = pmf(k)
            cum_p += pk
            points.append({
                "x": k,
                "y": round(pk, 5),
                "cdf": round(min(1.0, cum_p), 5),
                "in_selection": k in selected_k
            })
            
        return {
            "distribution": "geometric",
            "type": "discrete",
            "name": f"Geometric Distribution Geom(p={p:.2f})",
            "formula_title": "Probability Mass Function P(X = k):",
            "formula_text": "P(X = k) = (1 - p)^(k - 1) · p   for k = 1, 2, ...",
            "domain_label": "{1, 2, 3, ... ∞}",
            "mean": round(mean, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "skewness": round(skewness, 4),
            "kurtosis": round(kurtosis, 4),
            "skew_formula": "(2-p) / √(1-p)",
            "prob": round(prob, 5),
            "prob_percentage": f"{prob * 100:.2f}%",
            "expression": expr,
            "x_min": 1,
            "x_max": k_max,
            "selected_k": selected_k,
            "points": points,
            "markers": {
                "mean": round(mean, 4)
            }
        }

    @staticmethod
    def calculate_student_t(df: float, a: float, b: float, mode: str, num_points: int = 150) -> Dict[str, Any]:
        df = max(1.0, float(df))
        
        # Student-t PDF formula: Γ((ν+1)/2) / (√(πν) Γ(ν/2)) * (1 + t^2/ν)^(-(ν+1)/2)
        coef = math.exp(math.lgamma((df + 1) / 2.0) - math.lgamma(df / 2.0)) / math.sqrt(math.pi * df)
        
        def pdf(t: float) -> float:
            return coef * ((1.0 + (t * t) / df) ** (-(df + 1.0) / 2.0))
            
        # Numerical integration for CDF
        def cdf(t_val: float) -> float:
            if t_val == 0: return 0.5
            # integrate from 0 to t_val
            ts = np.linspace(0, abs(t_val), 100)
            ys = [pdf(t) for t in ts]
            area = float(np.trapezoid(ys, ts)) if hasattr(np, 'trapezoid') else float(np.trapz(ys, ts))
            return 0.5 + area if t_val > 0 else 0.5 - area
            
        mean = 0.0 if df > 1 else float("nan")
        variance = float(df / (df - 2)) if df > 2 else float("nan")
        std_dev = float(math.sqrt(variance)) if df > 2 else float("nan")
        skewness = 0.0 if df > 3 else float("nan")
        kurtosis = float(6 / (df - 4)) if df > 4 else float("nan")
        
        x_min = -5.0
        x_max = 5.0
        
        if mode == "less":
            prob = cdf(b)
            expr = f"P(T ≤ {b:.2f})"
            shaded_a = x_min
            shaded_b = b
        elif mode == "greater":
            prob = 1.0 - cdf(a)
            expr = f"P(T ≥ {a:.2f})"
            shaded_a = a
            shaded_b = x_max
        else: # interval
            low, high = min(a, b), max(a, b)
            prob = cdf(high) - cdf(low)
            expr = f"P({low:.2f} ≤ T ≤ {high:.2f})"
            shaded_a = low
            shaded_b = high
            
        prob = max(0.0, min(1.0, prob))
        
        xs = np.linspace(x_min, x_max, num_points)
        points = []
        for x in xs:
            x_f = float(x)
            points.append({
                "x": round(x_f, 4),
                "y": round(pdf(x_f), 5),
                "cdf": round(cdf(x_f), 5)
            })
            
        return {
            "distribution": "student_t",
            "type": "continuous",
            "name": f"Student's t-Distribution t(df={df:.1f})",
            "formula_title": "Probability Density Function f(t):",
            "formula_text": "f(t) = Γ((ν+1)/2) / (√(πν) Γ(ν/2)) · (1 + t²/ν)^(-(ν+1)/2)",
            "domain_label": "(-∞, +∞)",
            "mean": 0.0 if math.isnan(mean) else round(mean, 4),
            "variance": 0.0 if math.isnan(variance) else round(variance, 4),
            "std_dev": 0.0 if math.isnan(std_dev) else round(std_dev, 4),
            "skewness": 0.0 if math.isnan(skewness) else round(skewness, 4),
            "kurtosis": 0.0 if math.isnan(kurtosis) else round(kurtosis, 4),
            "skew_formula": "Symmetric (0.00)",
            "prob": round(prob, 5),
            "prob_percentage": f"{prob * 100:.2f}%",
            "expression": expr,
            "x_min": x_min,
            "x_max": x_max,
            "shaded_range": [round(shaded_a, 4), round(shaded_b, 4)],
            "points": points,
            "markers": {
                "mean": 0.0
            }
        }

    @staticmethod
    def calculate(req: CalculateRequest) -> Dict[str, Any]:
        d = req.distribution.lower()
        p = req.params
        mode = req.calc_mode.lower()
        a = req.a if req.a is not None else -1.0
        b = req.b if req.b is not None else 1.0
        num_points = req.num_points or 150
        
        if d in ("normal", "gaussian"):
            mu = p.get("mu", 0.0)
            sigma = p.get("sigma", 1.0)
            return DistributionEngine.calculate_normal(mu, sigma, a, b, mode, num_points)
        elif d == "binomial":
            n = int(p.get("n", 20))
            prob_p = p.get("p", 0.5)
            return DistributionEngine.calculate_binomial(n, prob_p, a, b, mode)
        elif d == "poisson":
            lam = p.get("lambda", 4.5)
            return DistributionEngine.calculate_poisson(lam, a, b, mode)
        elif d == "exponential":
            lam = p.get("lambda", 1.0)
            return DistributionEngine.calculate_exponential(lam, a, b, mode, num_points)
        elif d == "uniform":
            a_bound = p.get("a", 0.0)
            b_bound = p.get("b", 10.0)
            return DistributionEngine.calculate_uniform(a_bound, b_bound, a, b, mode, num_points)
        elif d == "geometric":
            prob_p = p.get("p", 0.3)
            return DistributionEngine.calculate_geometric(prob_p, a, b, mode)
        elif d in ("student_t", "t"):
            df = p.get("df", 5.0)
            return DistributionEngine.calculate_student_t(df, a, b, mode, num_points)
        else:
            return DistributionEngine.calculate_normal(0.0, 1.0, a, b, mode, num_points)
