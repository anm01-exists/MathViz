<<<<<<< HEAD
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
=======
# MathViz Unified

Interactive graph-algorithm visualizer: draw a graph in the browser editor,
pick an algorithm (BFS / DFS / Dijkstra), and get back an animated Manim video.

## Project layout

```
.
├── app/                     # FastAPI application (backend)
│   ├── main.py              # App factory: mounts /media, serves frontend, wires routers
│   ├── config.py            # Central paths & settings (env-overridable)
│   ├── api/                 # Blueprints: algorithms, render, examples, health
│   ├── services/            # pipeline.py (run algorithms -> animation JSON),
│   │                        # animation.py (animation state builders)
│   ├── algorithms/          # Portable BFS/DFS/Dijkstra + Graph (no web deps)
│   │   └── tests/           # Pytest unit tests for the algorithms
│   └── schemas/             # Pydantic request/response models
├── manim_engine/            # Manim rendering engine (Role 3)
│   ├── scenes.py            # BFS / DFS / Dijkstra / static scenes
│   ├── renderer.py          # CLI + programmatic render entry point
│   ├── layouts.py           # Node positioning (editor positions, circle fallback)
│   ├── schemas.py           # Animation-input validation/normalization
│   ├── styles.py            # Colors, fonts, grid
│   └── graph_primitives.py  # Manim graph drawing primitives
├── frontend/                # Single-page editor UI (index.html)
├── examples/                # Example graph JSON files
├── media/                   # Generated videos (gitignored, created at runtime)
└── scripts/                 # run.ps1 / run.sh launchers
```

## Quickstart

Requires Python 3.10+ and `ffmpeg` on PATH.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"

.\scripts\run.ps1            # or: python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 — draw a graph, run BFS/DFS/Dijkstra, watch the video.

## Tests

```powershell
pytest                    # algorithm unit tests
```

## API

| Method | Path                  | Description                                 |
| ------ | --------------------- | ------------------------------------------- |
| GET    | `/`                   | Frontend editor                             |
| GET    | `/media/{file}`       | Generated video files                       |
| POST   | `/api/algorithm/run`  | Run BFS/DFS/Dijkstra → animation JSON       |
| POST   | `/api/algorithm/convert` | Convert teammate format → animation schema |
| POST   | `/api/manim/render`   | Render animation JSON → MP4                 |
| GET    | `/api/examples`       | List example graphs                         |
| GET    | `/api/example/{name}` | Fetch one example graph                     |
| GET    | `/api/health`         | Health check                                |

## Rendering standalone

```powershell
python -m manim_engine.renderer examples/dijkstra_example.json --quality m
```

Output lands in `media/` (override with `--media-dir` or `MATHVIZ_MEDIA_DIR`).
>>>>>>> origin/main
