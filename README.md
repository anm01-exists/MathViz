# MathViz: Interactive Probability Studio

An academic, rigorous, and visually crystalline computational platform for statistical modeling and probability distributions. Designed using the **Empirical Light** design system with dynamic SVG vector rendering, synchronized slider and exact numeric input fields, and an active **FastAPI + NumPy** mathematical backend.

---

## 🚀 Quick Start

### 1. Requirements
- Python 3.10+
- Installed packages: `fastapi`, `uvicorn`, `numpy`, `pydantic`

### 2. Launch the Application
Run the launcher from the project directory:
```bash
python run.py
```
Open your browser and navigate to:
**[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🎯 Features

### 1. Real-Time Dynamic Graphing & Input Choice
- **Dual Parameter Tuning**: Every distribution parameter (Mean $\mu$, Std Dev $\sigma$, Trials $n$, Probability $p$, Rate $\lambda$, Bounds $a, b$) features **both** an interactive range slider AND a numeric text box (`<input type="number">`).
- **Synchronized Updates**: Dragging the slider updates the numeric text box; typing exact values immediately updates the slider and prompts real-time SVG redraw and statistical recalculation.
- **Interval Query Calculator**:
  - Probability inside interval $[a, b]$: $P(a \le X \le b)$
  - Left tail cumulative probability: $P(X \le x)$
  - Right tail survival probability: $P(X \ge x)$
  - Single point probability mass for discrete models: $P(X = k)$
- **Real-Time Visual Marks**:
  - Shaded integral area under the curve with sleek gradients.
  - Mean line ($\mu = \mathbb{E}[X]$) marker in dashed crimson with value annotations.
  - Empirical standard deviation markers ($\pm 1\sigma, \pm 2\sigma, \pm 3\sigma$).
  - Toggleable CDF $F(x)$ step/sigmoid curve overlay.

---

## 📑 Included Pages & Specialized Views

1. **Overview & Workbench (`overview-and-guide`)**:
   - The flagship probability workbench supporting Normal, Binomial, Poisson, Exponential, Uniform distributions, and the full cross-comparison matrix.
   - Includes real-world engineering problem solvers with user-adjustable inputs (Cloud Outage Poisson Risk, E-Commerce CRO Funnel, CNC Shaft Manufacturing Defect Rate).
2. **Discrete Distributions Lab (`discrete-distributions`)**:
   - Focused combinatorial exploration of Binomial, Poisson, and Geometric distributions.
   - Shows discrete stem bar plots and step CDFs.
3. **Continuous Distributions Lab (`continuous-distributions`)**:
   - Focused study of continuous densities (Gaussian Normal, Exponential, Student's t).
   - Real-time tail integration and critical values.
4. **Distribution Sandbox & Compare (`distribution-sandbox-and-compare`)**:
   - Superimpose two custom distributions on the same coordinate grid to analyze variance spread, kurtosis, and tail thickness.
5. **Monte Carlo Simulator (`monte-carlo-simulator`)**:
   - Live stochastic trial engine generating up to 50,000 true random iterations.
   - Real-time animated **Law of Large Numbers** running mean convergence curve ($\bar{X}_n \to \mu$).
   - Empirical frequency histogram plotted directly against theoretical density curves.
6. **Custom Data Lab & Empirical Fitting (`custom-data-lab`)**:
   - Allows users to type or paste their own raw data numbers (or generate synthetic measurement datasets).
   - Calculates sample size, mean, median, sample variance, standard deviation, skewness, and kurtosis.
   - Runs Maximum Likelihood Estimation (MLE) fitting for Normal, Exponential, and Uniform distributions.
   - Computes Kolmogorov-Smirnov test statistics ($D$), p-values (Good Fit vs. Rejected), and Log-Likelihoods.
7. **Cheatsheet & Proofs (`cheatsheet-and-proofs`)**:
   - Searchable mathematical formulas, Kolmogorov axioms, Central Limit Theorem statement, and formal proofs.

---

## 🛠 Backend Architecture & API Endpoints

- `POST /api/distribution/calculate`: Computes moments, closed-form formulas, and SVG coordinate points for any distribution.
- `POST /api/distribution/compare`: Aligns and compares two distributions over a shared domain.
- `POST /api/monte-carlo/simulate`: Executes empirical Monte Carlo trials, running mean convergence, and bin counts.
- `POST /api/empirical/fit`: Fits user-provided raw numerical data to theoretical probability models via MLE.
- `GET /api/scenarios`: Returns engineering case study presets.
- `POST /api/scenarios/solve`: Solves case studies dynamically based on user input parameters.
- `GET /api/health`: Health status of the MathViz computational kernel.
