"""
Empirical Data Analyzer & Distribution Fitting
Analyzes custom user-entered datasets, calculates moments & percentiles,
and fits theoretical probability distributions via Maximum Likelihood Estimation
using pure NumPy and math.
"""

from typing import Dict, Any, List, Optional
import math
import numpy as np
from pydantic import BaseModel, Field

class FitDataRequest(BaseModel):
    data: List[float] = Field(..., description="Array of numbers provided by user")
    fit_models: Optional[List[str]] = Field(default=["normal", "exponential"], description="Models to fit")
    num_bins: Optional[int] = Field(default=20, description="Number of histogram bins")

def normal_cdf(x: float, mu: float, sigma: float) -> float:
    return 0.5 * (1.0 + math.erf((x - mu) / (sigma * math.sqrt(2.0))))

def normal_pdf(x: float, mu: float, sigma: float) -> float:
    z = (x - mu) / sigma
    return (1.0 / (sigma * math.sqrt(2.0 * math.pi))) * math.exp(-0.5 * z * z)

def kolmogorov_pvalue(d_stat: float, n: int) -> float:
    """Asymptotic p-value for Kolmogorov-Smirnov test."""
    if d_stat <= 0:
        return 1.0
    lambda_val = (math.sqrt(n) + 0.12 + 0.11 / math.sqrt(n)) * d_stat
    # Kolmogorov sum
    p = 0.0
    for k in range(1, 101):
        term = 2.0 * ((-1) ** (k - 1)) * math.exp(-2.0 * (k ** 2) * (lambda_val ** 2))
        p += term
        if abs(term) < 1e-6:
            break
    return max(0.0, min(1.0, p))

class EmpiricalAnalyzer:
    @staticmethod
    def analyze_and_fit(req: FitDataRequest) -> Dict[str, Any]:
        arr = np.array(req.data, dtype=float)
        arr = arr[np.isfinite(arr)]
        n = len(arr)
        
        if n < 3:
            raise ValueError("At least 3 valid numeric values are required for empirical analysis.")
            
        mean = float(np.mean(arr))
        variance = float(np.var(arr, ddof=1)) if n > 1 else 0.0
        std_dev = float(np.std(arr, ddof=1)) if n > 1 else 0.0
        median = float(np.median(arr))
        min_val = float(np.min(arr))
        max_val = float(np.max(arr))
        q25, q75 = np.percentile(arr, [25, 75])
        iqr = float(q75 - q25)
        
        # Sample skewness and excess kurtosis
        diff = arr - mean
        m2 = float(np.mean(diff ** 2))
        m3 = float(np.mean(diff ** 3))
        m4 = float(np.mean(diff ** 4))
        skewness = float(m3 / (m2 ** 1.5)) if m2 > 0 else 0.0
        kurtosis = float(m4 / (m2 ** 2) - 3.0) if m2 > 0 else 0.0
        
        num_bins = min(50, max(5, req.num_bins or 20))
        counts, bin_edges = np.histogram(arr, bins=num_bins, density=True)
        raw_counts, _ = np.histogram(arr, bins=bin_edges)
        bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
        
        sorted_arr = np.sort(arr)
        models = req.fit_models or ["normal", "exponential"]
        fitted_results = {}
        
        # Normal Fit (MLE: mu = mean, sigma = std)
        if "normal" in models and std_dev > 0:
            mu_hat = mean
            sigma_hat = std_dev
            
            # KS test
            d_max = 0.0
            for i, x in enumerate(sorted_arr):
                f_theo = normal_cdf(float(x), mu_hat, sigma_hat)
                d1 = abs((i + 1) / n - f_theo)
                d2 = abs(i / n - f_theo)
                d_max = max(d_max, d1, d2)
                
            ks_pval = kolmogorov_pvalue(d_max, n)
            
            log_lik = 0.0
            for x in arr:
                pdf_val = max(1e-12, normal_pdf(float(x), mu_hat, sigma_hat))
                log_lik += math.log(pdf_val)
                
            xs_curve = np.linspace(min_val - 0.1 * (max_val - min_val), max_val + 0.1 * (max_val - min_val), 100)
            fitted_results["normal"] = {
                "name": "Normal Distribution",
                "params": {"mu": round(mu_hat, 4), "sigma": round(sigma_hat, 4)},
                "ks_statistic": round(d_max, 4),
                "ks_pvalue": round(ks_pval, 4),
                "log_likelihood": round(log_lik, 2),
                "curve": [
                    {"x": round(float(x), 4), "y": round(normal_pdf(float(x), mu_hat, sigma_hat), 5)}
                    for x in xs_curve
                ]
            }
            
        # Exponential Fit (only if all non-negative)
        if "exponential" in models and np.all(arr >= 0) and mean > 0:
            lambda_hat = 1.0 / mean
            
            # KS test
            d_max = 0.0
            for i, x in enumerate(sorted_arr):
                f_theo = 1.0 - math.exp(-lambda_hat * float(x)) if x >= 0 else 0.0
                d1 = abs((i + 1) / n - f_theo)
                d2 = abs(i / n - f_theo)
                d_max = max(d_max, d1, d2)
                
            ks_pval = kolmogorov_pvalue(d_max, n)
            log_lik = n * math.log(lambda_hat) - lambda_hat * float(np.sum(arr))
            
            xs_curve = np.linspace(0, max_val * 1.1, 100)
            fitted_results["exponential"] = {
                "name": "Exponential Distribution",
                "params": {"lambda": round(lambda_hat, 4)},
                "ks_statistic": round(d_max, 4),
                "ks_pvalue": round(ks_pval, 4),
                "log_likelihood": round(log_lik, 2),
                "curve": [
                    {"x": round(float(x), 4), "y": round(lambda_hat * math.exp(-lambda_hat * float(x)), 5)}
                    for x in xs_curve
                ]
            }
            
        # Uniform Fit
        if "uniform" in models and max_val > min_val:
            a_hat = min_val
            b_hat = max_val
            width = b_hat - a_hat
            
            d_max = 0.0
            for i, x in enumerate(sorted_arr):
                f_theo = (float(x) - a_hat) / width
                d1 = abs((i + 1) / n - f_theo)
                d2 = abs(i / n - f_theo)
                d_max = max(d_max, d1, d2)
                
            ks_pval = kolmogorov_pvalue(d_max, n)
            log_lik = -n * math.log(width)
            
            xs_curve = np.linspace(a_hat - 0.1 * width, b_hat + 0.1 * width, 100)
            fitted_results["uniform"] = {
                "name": "Uniform Distribution",
                "params": {"a": round(a_hat, 4), "b": round(b_hat, 4)},
                "ks_statistic": round(d_max, 4),
                "ks_pvalue": round(ks_pval, 4),
                "log_likelihood": round(log_lik, 2),
                "curve": [
                    {"x": round(float(x), 4), "y": round(1.0 / width if a_hat <= x <= b_hat else 0.0, 5)}
                    for x in xs_curve
                ]
            }

        histogram_points = [
            {
                "bin_start": round(float(bin_edges[i]), 3),
                "bin_end": round(float(bin_edges[i+1]), 3),
                "center": round(float(bin_centers[i]), 3),
                "count": int(raw_counts[i]),
                "density": round(float(counts[i]), 5)
            }
            for i in range(len(counts))
        ]
        
        return {
            "sample_size": n,
            "metrics": {
                "mean": round(mean, 4),
                "median": round(median, 4),
                "variance": round(variance, 4),
                "std_dev": round(std_dev, 4),
                "min": round(min_val, 4),
                "max": round(max_val, 4),
                "q25": round(float(q25), 4),
                "q75": round(float(q75), 4),
                "iqr": round(iqr, 4),
                "skewness": round(skewness, 4),
                "kurtosis": round(kurtosis, 4)
            },
            "histogram": histogram_points,
            "fitted_models": fitted_results
        }
