"""
Monte Carlo Simulation Engine
Runs empirical simulations using NumPy and pure math to visualize the Law of Large Numbers
and Central Limit Theorem with real-time histogram binning and convergence paths.
"""

from typing import Dict, Any, List, Optional
import math
import numpy as np
from pydantic import BaseModel, Field

class MonteCarloRequest(BaseModel):
    experiment: str = Field(default="dice_sum", description="Experiment type: dice_sum, coin_toss, normal, exponential, poisson")
    sample_size: int = Field(default=1000, ge=10, le=100000, description="Number of simulation trials")
    params: Dict[str, float] = Field(default_factory=dict, description="Experiment parameters")
    num_bins: Optional[int] = Field(default=30, description="Number of histogram bins")

def normal_pdf(x: float, mu: float, sigma: float) -> float:
    z = (x - mu) / sigma
    return (1.0 / (sigma * math.sqrt(2.0 * math.pi))) * math.exp(-0.5 * z * z)

class MonteCarloEngine:
    @staticmethod
    def simulate(req: MonteCarloRequest) -> Dict[str, Any]:
        n = int(req.sample_size)
        exp = req.experiment.lower()
        p = req.params
        num_bins = req.num_bins or 30
        
        rng = np.random.default_rng()
        
        if exp == "dice_sum":
            num_dice = int(p.get("num_dice", 2))
            num_dice = max(1, min(12, num_dice))
            rolls = rng.integers(1, 7, size=(n, num_dice))
            samples = rolls.sum(axis=1)
            
            theo_mean = num_dice * 3.5
            theo_var = num_dice * (35.0 / 12.0)
            theo_std = float(math.sqrt(theo_var))
            title = f"Sum of {num_dice} Fair Dice (CLT Demonstration)"
            x_label = "Dice Sum Score"
            is_discrete = True
            
        elif exp == "coin_toss":
            prob_p = float(p.get("p", 0.5))
            num_flips = int(p.get("num_flips", 20))
            samples = rng.binomial(n=num_flips, p=prob_p, size=n)
            
            theo_mean = num_flips * prob_p
            theo_var = num_flips * prob_p * (1 - prob_p)
            theo_std = float(math.sqrt(theo_var))
            title = f"Coin Tossing (Heads in {num_flips} Tosses, p={prob_p:.2f})"
            x_label = "Number of Heads"
            is_discrete = True
            
        elif exp == "normal":
            mu = float(p.get("mu", 0.0))
            sigma = max(0.01, float(p.get("sigma", 1.0)))
            samples = rng.normal(loc=mu, scale=sigma, size=n)
            
            theo_mean = mu
            theo_var = sigma ** 2
            theo_std = sigma
            title = f"Gaussian Normal Sampling N({mu:.2f}, {sigma:.2f}²)"
            x_label = "Continuous Value X"
            is_discrete = False
            
        elif exp == "exponential":
            lam = max(0.01, float(p.get("lambda", 1.0)))
            samples = rng.exponential(scale=1.0 / lam, size=n)
            
            theo_mean = 1.0 / lam
            theo_var = 1.0 / (lam ** 2)
            theo_std = 1.0 / lam
            title = f"Exponential Waiting Times Exp(λ={lam:.2f})"
            x_label = "Waiting Time (s)"
            is_discrete = False
            
        elif exp == "poisson":
            lam = max(0.05, float(p.get("lambda", 4.0)))
            samples = rng.poisson(lam=lam, size=n)
            
            theo_mean = lam
            theo_var = lam
            theo_std = float(math.sqrt(lam))
            title = f"Poisson Event Counting Pois(λ={lam:.2f})"
            x_label = "Event Count k"
            is_discrete = True
            
        else: # default uniform sum (CLT)
            k = 3
            samples = rng.uniform(0, 1, size=(n, k)).sum(axis=1)
            theo_mean = k * 0.5
            theo_var = k * (1.0 / 12.0)
            theo_std = float(math.sqrt(theo_var))
            title = f"Sum of {k} Uniform Variables U(0,1)"
            x_label = "Sum Value"
            is_discrete = False

        emp_mean = float(np.mean(samples))
        emp_var = float(np.var(samples, ddof=1)) if n > 1 else 0.0
        emp_std = float(np.std(samples, ddof=1)) if n > 1 else 0.0
        
        # Law of large numbers convergence path
        cum_means = np.cumsum(samples) / np.arange(1, n + 1)
        step = max(1, n // 100)
        convergence_indices = list(range(0, n, step))
        if convergence_indices[-1] != n - 1:
            convergence_indices.append(n - 1)
            
        convergence_curve = [
            {"trial": int(i + 1), "running_mean": round(float(cum_means[i]), 4), "theo_mean": round(float(theo_mean), 4)}
            for i in convergence_indices
        ]
        
        # Build histogram
        if is_discrete:
            min_val = int(np.min(samples))
            max_val = int(np.max(samples))
            bins = np.arange(min_val - 0.5, max_val + 1.5, 1)
            counts, bin_edges = np.histogram(samples, bins=bins)
            bin_centers = np.arange(min_val, max_val + 1)
            freqs = counts / n
            
            theo_freqs = []
            if exp == "dice_sum":
                num_dice = int(p.get("num_dice", 2))
                prob_poly = np.array([0, 1/6, 1/6, 1/6, 1/6, 1/6, 1/6])
                curr_poly = prob_poly.copy()
                for _ in range(num_dice - 1):
                    curr_poly = np.convolve(curr_poly, prob_poly)
                for k in bin_centers:
                    p_theo = float(curr_poly[k]) if k < len(curr_poly) else 0.0
                    theo_freqs.append(round(p_theo, 5))
            elif exp == "coin_toss":
                num_flips = int(p.get("num_flips", 20))
                prob_p = float(p.get("p", 0.5))
                for k in bin_centers:
                    if 0 <= k <= num_flips:
                        val = math.comb(num_flips, k) * (prob_p ** k) * ((1 - prob_p) ** (num_flips - k))
                    else:
                        val = 0.0
                    theo_freqs.append(round(val, 5))
            elif exp == "poisson":
                lam = float(p.get("lambda", 4.0))
                for k in bin_centers:
                    if k >= 0:
                        val = math.exp(k * math.log(lam) - lam - math.lgamma(k + 1))
                    else:
                        val = 0.0
                    theo_freqs.append(round(val, 5))
            else:
                theo_freqs = [0.0] * len(bin_centers)
                
            histogram = [
                {
                    "x": int(center),
                    "count": int(count),
                    "frequency": round(float(freq), 5),
                    "theoretical": theo_freqs[idx] if idx < len(theo_freqs) else 0.0
                }
                for idx, (center, count, freq) in enumerate(zip(bin_centers, counts, freqs))
            ]
        else:
            counts, bin_edges = np.histogram(samples, bins=num_bins, density=True)
            bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
            
            theo_densities = []
            if exp == "normal":
                mu = float(p.get("mu", 0.0))
                sigma = float(p.get("sigma", 1.0))
                theo_densities = [round(normal_pdf(float(x), mu, sigma), 5) for x in bin_centers]
            elif exp == "exponential":
                lam = float(p.get("lambda", 1.0))
                theo_densities = [round(lam * math.exp(-lam * float(x)) if x >= 0 else 0.0, 5) for x in bin_centers]
            else:
                # CLT normal approx
                theo_densities = [round(normal_pdf(float(x), theo_mean, theo_std), 5) for x in bin_centers]
                
            histogram = [
                {
                    "x": round(float(center), 3),
                    "density": round(float(count), 5),
                    "bin_start": round(float(bin_edges[i]), 3),
                    "bin_end": round(float(bin_edges[i+1]), 3),
                    "theoretical": theo_densities[i]
                }
                for i, (center, count) in enumerate(zip(bin_centers, counts))
            ]
            
        error_mean_pct = abs(emp_mean - theo_mean) / abs(theo_mean) * 100 if theo_mean != 0 else abs(emp_mean - theo_mean) * 100
        
        return {
            "title": title,
            "experiment": exp,
            "sample_size": n,
            "is_discrete": is_discrete,
            "x_label": x_label,
            "empirical": {
                "mean": round(emp_mean, 4),
                "variance": round(emp_var, 4),
                "std_dev": round(emp_std, 4),
                "min": round(float(np.min(samples)), 4),
                "max": round(float(np.max(samples)), 4),
            },
            "theoretical": {
                "mean": round(theo_mean, 4),
                "variance": round(theo_var, 4),
                "std_dev": round(theo_std, 4)
            },
            "error_mean_pct": round(error_mean_pct, 2),
            "histogram": histogram,
            "convergence_curve": convergence_curve
        }
