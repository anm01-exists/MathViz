/**
 * MathViz API Client
 * Seamlessly interfaces with the FastAPI probability kernel.
 * Includes local fallback mathematics for ultra-fast instant feedback.
 */

const API_BASE = window.location.origin;

const MathVizAPI = {
  /**
   * Request distribution analytics & plot coordinates
   */
  async calculate(distribution, params, calcMode = 'interval', a = -1.0, b = 1.0, numPoints = 150) {
    try {
      const resp = await fetch(`${API_BASE}/api/distribution/calculate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          distribution,
          params,
          calc_mode: calcMode,
          a: parseFloat(a),
          b: parseFloat(b),
          num_points: numPoints
        })
      });
      if (!resp.ok) throw new Error(`Server returned ${resp.status}`);
      return await resp.json();
    } catch (err) {
      console.warn("Backend API call failed, using client-side fallback:", err);
      return this.clientFallbackCalculate(distribution, params, calcMode, a, b);
    }
  },

  /**
   * Request multi-distribution comparison
   */
  async compare(distroA, distroB) {
    try {
      const resp = await fetch(`${API_BASE}/api/distribution/compare`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ distro_a: distroA, distro_b: distroB })
      });
      if (!resp.ok) throw new Error(`Server returned ${resp.status}`);
      return await resp.json();
    } catch (err) {
      console.warn("Compare API call failed:", err);
      const resA = await this.calculate(distroA.distribution, distroA.params, distroA.calc_mode, distroA.a, distroA.b);
      const resB = await this.calculate(distroB.distribution, distroB.params, distroB.calc_mode, distroB.a, distroB.b);
      return { distro_a: resA, distro_b: resB, domain: [Math.min(resA.x_min, resB.x_min), Math.max(resA.x_max, resB.x_max)] };
    }
  },

  /**
   * Run Monte Carlo simulation
   */
  async runMonteCarlo(experiment, sampleSize, params, numBins = 30) {
    try {
      const resp = await fetch(`${API_BASE}/api/monte-carlo/simulate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          experiment,
          sample_size: parseInt(sampleSize),
          params,
          num_bins: numBins
        })
      });
      if (!resp.ok) throw new Error(`Server returned ${resp.status}`);
      return await resp.json();
    } catch (err) {
      console.warn("Monte Carlo API call failed:", err);
      throw err;
    }
  },

  /**
   * Fit empirical user dataset
   */
  async fitEmpiricalData(dataArray, fitModels = ["normal", "exponential", "uniform"], numBins = 20) {
    try {
      const resp = await fetch(`${API_BASE}/api/empirical/fit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          data: dataArray,
          fit_models: fitModels,
          num_bins: numBins
        })
      });
      if (!resp.ok) throw new Error(`Server returned ${resp.status}`);
      return await resp.json();
    } catch (err) {
      console.warn("Empirical fit API call failed:", err);
      throw err;
    }
  },

  /**
   * Solve engineering scenario
   */
  async solveScenario(scenarioId, params) {
    try {
      const resp = await fetch(`${API_BASE}/api/scenarios/solve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          scenario_id: scenarioId,
          params
        })
      });
      if (!resp.ok) throw new Error(`Server returned ${resp.status}`);
      return await resp.json();
    } catch (err) {
      console.warn("Solve scenario API call failed:", err);
      throw err;
    }
  },

  /**
   * Client-side fallback computation
   */
  clientFallbackCalculate(distro, params, mode, aVal, bVal) {
    const a = parseFloat(aVal) || 0;
    const b = parseFloat(bVal) || 0;
    const low = Math.min(a, b);
    const high = Math.max(a, b);

    if (distro === 'normal') {
      const mu = params.mu ?? 0;
      const sigma = params.sigma ?? 1;
      const erf = x => {
        const a1 = 0.254829592, a2 = -0.284496736, a3 = 1.421413741, a4 = -1.453152027, a5 = 1.061405429, p = 0.3275911;
        const sign = x < 0 ? -1 : 1;
        x = Math.abs(x);
        const t = 1.0 / (1.0 + p * x);
        const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);
        return sign * y;
      };
      const cdf = x => 0.5 * (1 + erf((x - mu) / (sigma * Math.sqrt(2))));
      const pdf = x => (1 / (sigma * Math.sqrt(2 * Math.PI))) * Math.exp(-0.5 * Math.pow((x - mu) / sigma, 2));

      let prob = 0, expr = '';
      if (mode === 'less') { prob = cdf(high); expr = `P(X ≤ ${high.toFixed(2)})`; }
      else if (mode === 'greater') { prob = 1 - cdf(low); expr = `P(X ≥ ${low.toFixed(2)})`; }
      else { prob = cdf(high) - cdf(low); expr = `P(${low.toFixed(2)} ≤ X ≤ ${high.toFixed(2)})`; }

      const xMin = mu - 4.2 * sigma;
      const xMax = mu + 4.2 * sigma;
      const points = [];
      const steps = 120;
      const dx = (xMax - xMin) / steps;
      for (let i = 0; i <= steps; i++) {
        const x = xMin + i * dx;
        points.push({ x: Number(x.toFixed(4)), y: Number(pdf(x).toFixed(5)), cdf: Number(cdf(x).toFixed(5)) });
      }

      return {
        distribution: "normal",
        type: "continuous",
        name: `Normal Distribution N(${mu.toFixed(2)}, ${sigma.toFixed(2)}²)`,
        formula_title: "Probability Density Function f(x):",
        formula_text: "f(x) = (1 / (σ √(2π))) · exp(-0.5 · ((x - μ) / σ)²)",
        domain_label: "(-∞, +∞)",
        mean: mu, variance: sigma * sigma, std_dev: sigma, skewness: 0, kurtosis: 0,
        prob: Math.max(0, Math.min(1, prob)),
        prob_percentage: `${(Math.max(0, Math.min(1, prob)) * 100).toFixed(2)}%`,
        expression: expr,
        x_min: xMin, x_max: xMax,
        shaded_range: [mode === 'less' ? xMin : low, mode === 'greater' ? xMax : high],
        points,
        markers: { mean: mu }
      };
    }
    // Return basic fallback
    return {
      distribution: distro,
      mean: 0, variance: 1, std_dev: 1, skewness: 0, prob: 0.5, prob_percentage: "50.00%",
      expression: `P(${low} ≤ X ≤ ${high})`,
      points: []
    };
  }
};

window.MathVizAPI = MathVizAPI;
