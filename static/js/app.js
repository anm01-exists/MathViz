/**
 * MathViz Interactive Application Controller
 * Handles user interactions, two-way slider/number input sync,
 * multi-view navigation, and dynamic chart updates.
 */

const AppState = {
  currentView: 'overview-and-guide', // 'overview-and-guide' | 'discrete-distributions' | 'continuous-distributions' | 'distribution-sandbox-and-compare' | 'monte-carlo-simulator' | 'custom-data-lab' | 'cheatsheet-and-proofs'
  currentTab: 'normal',
  calcMode: 'interval',
  showCDF: false,
  showSigma: true,
  params: {
    normal: { mu: 0.0, sigma: 1.0 },
    binomial: { n: 20, p: 0.5 },
    poisson: { lambda: 4.5 },
    exponential: { lambda: 1.0 },
    uniform: { a: 0.0, b: 10.0 },
    student_t: { df: 5.0 }
  },
  interval: {
    a: -1.0,
    b: 1.0
  },
  compare: {
    distroA: { type: 'normal', params: { mu: 0, sigma: 1 }, mode: 'interval', a: -1, b: 1 },
    distroB: { type: 'student_t', params: { df: 3 }, mode: 'interval', a: -1, b: 1 }
  },
  monteCarlo: {
    experiment: 'dice_sum',
    sampleSize: 2000,
    params: { num_dice: 2, num_flips: 20, p: 0.5, lambda: 4.0, mu: 0.0, sigma: 1.0 }
  }
};

// Global reference
window.AppState = AppState;

// Switch top navigation page view
function switchView(viewName) {
  AppState.currentView = viewName;

  // Update top nav styling
  document.querySelectorAll('header nav a').forEach(a => {
    if (a.getAttribute('data-path') === viewName) {
      a.className = 'px-3 py-1.5 rounded-lg text-xs font-bold bg-primary text-on-primary shadow-sm whitespace-nowrap transition-all';
    } else {
      a.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold text-on-surface-variant hover:text-on-surface hover:bg-surface-container whitespace-nowrap transition-all';
    }
  });

  // Toggle view containers
  const views = [
    'viewOverview',
    'viewDiscrete',
    'viewContinuous',
    'viewCompare',
    'viewMonteCarlo',
    'viewCustomData',
    'viewCheatsheet'
  ];

  const viewMap = {
    'overview-and-guide': 'viewOverview',
    'discrete-distributions': 'viewDiscrete',
    'continuous-distributions': 'viewContinuous',
    'distribution-sandbox-and-compare': 'viewCompare',
    'monte-carlo-simulator': 'viewMonteCarlo',
    'custom-data-lab': 'viewCustomData',
    'cheatsheet-and-proofs': 'viewCheatsheet'
  };

  const targetId = viewMap[viewName] || 'viewOverview';
  views.forEach(v => {
    const el = document.getElementById(v);
    if (el) {
      if (v === targetId) {
        el.classList.remove('hidden');
      } else {
        el.classList.add('hidden');
      }
    }
  });

  // Trigger initializations for specific views
  if (viewName === 'distribution-sandbox-and-compare') {
    updateComparisonView();
  } else if (viewName === 'monte-carlo-simulator') {
    runMonteCarloSimulation();
  } else if (viewName === 'discrete-distributions') {
    updateDiscreteView();
  } else if (viewName === 'continuous-distributions') {
    updateContinuousView();
  } else if (viewName === 'custom-data-lab') {
    if (!AppState.customDataInitialized) {
      generateSampleData('normal');
      AppState.customDataInitialized = true;
    }
  }
}

// Switch Workbench Distribution Tab
function switchTab(tabKey) {
  AppState.currentTab = tabKey;

  // Update button styles
  document.querySelectorAll('#distroTabs .tab-btn').forEach(btn => {
    if (btn.getAttribute('data-tab') === tabKey) {
      btn.className = 'tab-btn px-3 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5 whitespace-nowrap bg-primary text-on-primary shadow-sm';
    } else {
      btn.className = 'tab-btn px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 hover:bg-surface-container-high whitespace-nowrap bg-transparent text-on-surface';
    }
  });

  const matrixSection = document.getElementById('matrixSection');
  const workbench = document.getElementById('interactiveWorkbench');

  if (tabKey === 'matrix') {
    workbench.classList.add('hidden');
    matrixSection.classList.remove('hidden');
    return;
  } else {
    workbench.classList.remove('hidden');
    matrixSection.classList.add('hidden');
  }

  // Adjust default intervals based on distribution
  if (tabKey === 'normal') {
    AppState.interval = { a: -1.0, b: 1.0 };
  } else if (tabKey === 'binomial') {
    AppState.interval = { a: 8, b: 12 };
  } else if (tabKey === 'poisson') {
    AppState.interval = { a: 2, b: 6 };
  } else if (tabKey === 'exponential') {
    AppState.interval = { a: 0.5, b: 2.0 };
  } else if (tabKey === 'uniform') {
    AppState.interval = { a: 2.0, b: 6.0 };
  }

  const inputA = document.getElementById('inputA');
  const inputB = document.getElementById('inputB');
  if (inputA) inputA.value = AppState.interval.a;
  if (inputB) inputB.value = AppState.interval.b;

  renderSliderControls();
  updateWorkbenchCalculations();
}

// Render sliders AND direct numeric input fields for the user
function renderSliderControls() {
  const container = document.getElementById('dynamicSliders');
  const title = document.getElementById('panelDistroTitle');
  const badge = document.getElementById('distroClassBadge');
  const tab = AppState.currentTab;

  let html = '';

  if (tab === 'normal') {
    title.innerText = 'Normal Distribution N(μ, σ²)';
    badge.innerText = 'Continuous PDF';
    badge.className = 'text-xs px-2.5 py-0.5 rounded-full bg-surface-container-highest text-primary font-label-sm';

    const mu = AppState.params.normal.mu;
    const sigma = AppState.params.normal.sigma;

    html = `
      <div class="space-y-1.5 p-2.5 bg-surface-container-low rounded-lg border border-surface-container">
        <div class="flex items-center justify-between text-xs font-label-md">
          <span class="font-bold text-on-surface">Mean (μ)</span>
          <div class="flex items-center gap-1.5">
            <span class="text-on-surface-variant text-[11px]">Exact value:</span>
            <input type="number" step="0.1" value="${mu}" id="numInputMu"
              oninput="syncParam('normal', 'mu', this.value, 'sliderMu')"
              class="w-16 px-1.5 py-0.5 text-center text-xs font-code-math bg-surface-container-lowest border border-outline-variant rounded font-bold text-primary focus:outline-none focus:ring-1 focus:ring-primary" />
          </div>
        </div>
        <input type="range" min="-5" max="5" step="0.1" value="${mu}" id="sliderMu"
          oninput="syncParam('normal', 'mu', this.value, 'numInputMu')" 
          class="w-full accent-primary cursor-pointer h-2 bg-surface-container rounded-lg" />
        <div class="flex justify-between text-[10px] text-on-surface-variant font-code-math">
          <span>-5.0</span><span>0.0</span><span>+5.0</span>
        </div>
      </div>

      <div class="space-y-1.5 p-2.5 bg-surface-container-low rounded-lg border border-surface-container">
        <div class="flex items-center justify-between text-xs font-label-md">
          <span class="font-bold text-on-surface">Standard Deviation (σ)</span>
          <div class="flex items-center gap-1.5">
            <span class="text-on-surface-variant text-[11px]">Exact value:</span>
            <input type="number" step="0.1" min="0.1" max="5" value="${sigma}" id="numInputSigma"
              oninput="syncParam('normal', 'sigma', this.value, 'sliderSigma')"
              class="w-16 px-1.5 py-0.5 text-center text-xs font-code-math bg-surface-container-lowest border border-outline-variant rounded font-bold text-primary focus:outline-none focus:ring-1 focus:ring-primary" />
          </div>
        </div>
        <input type="range" min="0.2" max="4" step="0.1" value="${sigma}" id="sliderSigma"
          oninput="syncParam('normal', 'sigma', this.value, 'numInputSigma')" 
          class="w-full accent-primary cursor-pointer h-2 bg-surface-container rounded-lg" />
        <div class="flex justify-between text-[10px] text-on-surface-variant font-code-math">
          <span>0.2</span><span>2.0</span><span>4.0</span>
        </div>
      </div>
    `;

  } else if (tab === 'binomial') {
    title.innerText = 'Binomial Distribution B(n, p)';
    badge.innerText = 'Discrete PMF';
    badge.className = 'text-xs px-2.5 py-0.5 rounded-full bg-secondary-fixed text-on-secondary-fixed font-label-sm';

    const n = AppState.params.binomial.n;
    const p = AppState.params.binomial.p;

    html = `
      <div class="space-y-1.5 p-2.5 bg-surface-container-low rounded-lg border border-surface-container">
        <div class="flex items-center justify-between text-xs font-label-md">
          <span class="font-bold text-on-surface">Trials Count (n)</span>
          <div class="flex items-center gap-1.5">
            <span class="text-on-surface-variant text-[11px]">Exact value:</span>
            <input type="number" step="1" min="1" max="100" value="${n}" id="numInputN"
              oninput="syncParam('binomial', 'n', this.value, 'sliderN')"
              class="w-16 px-1.5 py-0.5 text-center text-xs font-code-math bg-surface-container-lowest border border-outline-variant rounded font-bold text-primary focus:outline-none focus:ring-1 focus:ring-primary" />
          </div>
        </div>
        <input type="range" min="2" max="50" step="1" value="${n}" id="sliderN"
          oninput="syncParam('binomial', 'n', this.value, 'numInputN')" 
          class="w-full accent-primary cursor-pointer h-2 bg-surface-container rounded-lg" />
        <div class="flex justify-between text-[10px] text-on-surface-variant font-code-math">
          <span>2</span><span>25</span><span>50</span>
        </div>
      </div>

      <div class="space-y-1.5 p-2.5 bg-surface-container-low rounded-lg border border-surface-container">
        <div class="flex items-center justify-between text-xs font-label-md">
          <span class="font-bold text-on-surface">Success Probability (p)</span>
          <div class="flex items-center gap-1.5">
            <span class="text-on-surface-variant text-[11px]">Exact value:</span>
            <input type="number" step="0.01" min="0.01" max="0.99" value="${p}" id="numInputP"
              oninput="syncParam('binomial', 'p', this.value, 'sliderP')"
              class="w-16 px-1.5 py-0.5 text-center text-xs font-code-math bg-surface-container-lowest border border-outline-variant rounded font-bold text-primary focus:outline-none focus:ring-1 focus:ring-primary" />
          </div>
        </div>
        <input type="range" min="0.02" max="0.98" step="0.02" value="${p}" id="sliderP"
          oninput="syncParam('binomial', 'p', this.value, 'numInputP')" 
          class="w-full accent-primary cursor-pointer h-2 bg-surface-container rounded-lg" />
        <div class="flex justify-between text-[10px] text-on-surface-variant font-code-math">
          <span>0.02</span><span>0.50</span><span>0.98</span>
        </div>
      </div>
    `;

  } else if (tab === 'poisson') {
    title.innerText = 'Poisson Distribution Pois(λ)';
    badge.innerText = 'Discrete PMF';
    badge.className = 'text-xs px-2.5 py-0.5 rounded-full bg-secondary-fixed text-on-secondary-fixed font-label-sm';

    const lam = AppState.params.poisson.lambda;

    html = `
      <div class="space-y-1.5 p-2.5 bg-surface-container-low rounded-lg border border-surface-container">
        <div class="flex items-center justify-between text-xs font-label-md">
          <span class="font-bold text-on-surface">Rate Parameter (λ)</span>
          <div class="flex items-center gap-1.5">
            <span class="text-on-surface-variant text-[11px]">Exact value:</span>
            <input type="number" step="0.1" min="0.1" max="30" value="${lam}" id="numInputLam"
              oninput="syncParam('poisson', 'lambda', this.value, 'sliderLam')"
              class="w-16 px-1.5 py-0.5 text-center text-xs font-code-math bg-surface-container-lowest border border-outline-variant rounded font-bold text-primary focus:outline-none focus:ring-1 focus:ring-primary" />
          </div>
        </div>
        <input type="range" min="0.5" max="18" step="0.5" value="${lam}" id="sliderLam"
          oninput="syncParam('poisson', 'lambda', this.value, 'numInputLam')" 
          class="w-full accent-primary cursor-pointer h-2 bg-surface-container rounded-lg" />
        <div class="flex justify-between text-[10px] text-on-surface-variant font-code-math">
          <span>0.5</span><span>9.0</span><span>18.0</span>
        </div>
      </div>
    `;

  } else if (tab === 'exponential') {
    title.innerText = 'Exponential Distribution Exp(λ)';
    badge.innerText = 'Continuous PDF';
    badge.className = 'text-xs px-2.5 py-0.5 rounded-full bg-surface-container-highest text-primary font-label-sm';

    const lam = AppState.params.exponential.lambda;

    html = `
      <div class="space-y-1.5 p-2.5 bg-surface-container-low rounded-lg border border-surface-container">
        <div class="flex items-center justify-between text-xs font-label-md">
          <span class="font-bold text-on-surface">Rate Parameter (λ)</span>
          <div class="flex items-center gap-1.5">
            <span class="text-on-surface-variant text-[11px]">Exact value:</span>
            <input type="number" step="0.1" min="0.1" max="10" value="${lam}" id="numInputExpLam"
              oninput="syncParam('exponential', 'lambda', this.value, 'sliderExpLam')"
              class="w-16 px-1.5 py-0.5 text-center text-xs font-code-math bg-surface-container-lowest border border-outline-variant rounded font-bold text-primary focus:outline-none focus:ring-1 focus:ring-primary" />
          </div>
        </div>
        <input type="range" min="0.2" max="4.0" step="0.1" value="${lam}" id="sliderExpLam"
          oninput="syncParam('exponential', 'lambda', this.value, 'numInputExpLam')" 
          class="w-full accent-primary cursor-pointer h-2 bg-surface-container rounded-lg" />
        <div class="flex justify-between text-[10px] text-on-surface-variant font-code-math">
          <span>0.2</span><span>2.0</span><span>4.0</span>
        </div>
      </div>
    `;

  } else if (tab === 'uniform') {
    title.innerText = 'Continuous Uniform Distribution U(a, b)';
    badge.innerText = 'Continuous PDF';
    badge.className = 'text-xs px-2.5 py-0.5 rounded-full bg-surface-container-highest text-primary font-label-sm';

    const aBound = AppState.params.uniform.a;
    const bBound = AppState.params.uniform.b;

    html = `
      <div class="space-y-1.5 p-2.5 bg-surface-container-low rounded-lg border border-surface-container">
        <div class="flex items-center justify-between text-xs font-label-md">
          <span class="font-bold text-on-surface">Lower Bound (a)</span>
          <input type="number" step="0.5" value="${aBound}" id="numInputUniA"
            oninput="syncParam('uniform', 'a', this.value, 'sliderUniA')"
            class="w-16 px-1.5 py-0.5 text-center text-xs font-code-math bg-surface-container-lowest border border-outline-variant rounded font-bold text-primary focus:outline-none focus:ring-1 focus:ring-primary" />
        </div>
        <input type="range" min="-10" max="10" step="0.5" value="${aBound}" id="sliderUniA"
          oninput="syncParam('uniform', 'a', this.value, 'numInputUniA')" 
          class="w-full accent-primary cursor-pointer h-2 bg-surface-container rounded-lg" />
      </div>

      <div class="space-y-1.5 p-2.5 bg-surface-container-low rounded-lg border border-surface-container">
        <div class="flex items-center justify-between text-xs font-label-md">
          <span class="font-bold text-on-surface">Upper Bound (b)</span>
          <input type="number" step="0.5" value="${bBound}" id="numInputUniB"
            oninput="syncParam('uniform', 'b', this.value, 'sliderUniB')"
            class="w-16 px-1.5 py-0.5 text-center text-xs font-code-math bg-surface-container-lowest border border-outline-variant rounded font-bold text-primary focus:outline-none focus:ring-1 focus:ring-primary" />
        </div>
        <input type="range" min="-5" max="25" step="0.5" value="${bBound}" id="sliderUniB"
          oninput="syncParam('uniform', 'b', this.value, 'numInputUniB')" 
          class="w-full accent-primary cursor-pointer h-2 bg-surface-container rounded-lg" />
      </div>
    `;
  }

  container.innerHTML = html;
}

// Synchronize range slider and numeric text input
function syncParam(distroKey, paramName, value, targetElementId) {
  const numVal = parseFloat(value);
  if (!isNaN(numVal)) {
    AppState.params[distroKey][paramName] = numVal;
    const target = document.getElementById(targetElementId);
    if (target && target.value !== value) {
      target.value = value;
    }
    updateWorkbenchCalculations();
  }
}

// Calculation mode switch (Interval, Left tail, Right tail)
function setCalcMode(mode) {
  AppState.calcMode = mode;
  const btnInt = document.getElementById('modeIntervalBtn');
  const btnLess = document.getElementById('modeLessBtn');
  const btnGreater = document.getElementById('modeGreaterBtn');
  const inputsRow = document.getElementById('intervalInputs');

  [btnInt, btnLess, btnGreater].forEach(b => {
    if (b) {
      b.classList.remove('bg-primary', 'text-on-primary');
      b.classList.add('bg-surface-container', 'text-on-surface');
    }
  });

  if (mode === 'interval' && btnInt) {
    btnInt.classList.add('bg-primary', 'text-on-primary');
    btnInt.classList.remove('bg-surface-container', 'text-on-surface');
    if (inputsRow) {
      inputsRow.children[0].classList.remove('opacity-30', 'pointer-events-none');
      inputsRow.children[1].classList.remove('opacity-30', 'pointer-events-none');
    }
  } else if (mode === 'less' && btnLess) {
    btnLess.classList.add('bg-primary', 'text-on-primary');
    btnLess.classList.remove('bg-surface-container', 'text-on-surface');
    if (inputsRow) {
      inputsRow.children[0].classList.add('opacity-30', 'pointer-events-none');
      inputsRow.children[1].classList.remove('opacity-30', 'pointer-events-none');
    }
  } else if (mode === 'greater' && btnGreater) {
    btnGreater.classList.add('bg-primary', 'text-on-primary');
    btnGreater.classList.remove('bg-surface-container', 'text-on-surface');
    if (inputsRow) {
      inputsRow.children[0].classList.remove('opacity-30', 'pointer-events-none');
      inputsRow.children[1].classList.add('opacity-30', 'pointer-events-none');
    }
  }

  updateWorkbenchCalculations();
}

// Request calculation from backend and update charts & metrics
async function updateWorkbenchCalculations() {
  const inputA = document.getElementById('inputA');
  const inputB = document.getElementById('inputB');
  if (inputA) AppState.interval.a = parseFloat(inputA.value) || 0;
  if (inputB) AppState.interval.b = parseFloat(inputB.value) || 0;

  const distro = AppState.currentTab;
  const params = AppState.params[distro] || {};

  try {
    const data = await MathVizAPI.calculate(
      distro,
      params,
      AppState.calcMode,
      AppState.interval.a,
      AppState.interval.b
    );

    // Update displays
    document.getElementById('calcExpressionDisplay').innerText = data.expression || '';
    document.getElementById('calcResultDisplay').innerText = data.prob_percentage || '0.00%';
    document.getElementById('metricMean').innerText = data.mean !== undefined ? data.mean.toFixed(2) : '--';
    document.getElementById('metricVariance').innerText = data.variance !== undefined ? data.variance.toFixed(2) : '--';
    document.getElementById('metricStdDev').innerText = data.std_dev !== undefined ? data.std_dev.toFixed(2) : '--';
    document.getElementById('metricSkewness').innerText = data.skewness !== undefined ? data.skewness.toFixed(2) : '--';
    document.getElementById('domainRangeLabel').innerText = data.domain_label || '';
    document.getElementById('pdfFormulaTitle').innerText = data.formula_title || '';
    document.getElementById('pdfFormulaCode').innerText = data.formula_text || '';
    if (data.skew_formula) {
      document.getElementById('metricSkewFormula').innerText = data.skew_formula;
    }

    // Redraw SVG
    const svg = document.getElementById('distroSvg');
    MathVizCharts.renderDistribution(svg, data, {
      showCDF: AppState.showCDF,
      showSigma: AppState.showSigma
    });

  } catch (err) {
    console.error("Calculation update error:", err);
  }
}

// Reset Workbench Parameters to standard defaults
function resetPlotView() {
  if (AppState.currentTab === 'normal') {
    AppState.params.normal = { mu: 0, sigma: 1 };
    AppState.interval = { a: -1, b: 1 };
  } else if (AppState.currentTab === 'binomial') {
    AppState.params.binomial = { n: 20, p: 0.5 };
    AppState.interval = { a: 8, b: 12 };
  } else if (AppState.currentTab === 'poisson') {
    AppState.params.poisson = { lambda: 4.5 };
    AppState.interval = { a: 2, b: 6 };
  } else if (AppState.currentTab === 'exponential') {
    AppState.params.exponential = { lambda: 1.0 };
    AppState.interval = { a: 0.5, b: 2.0 };
  } else if (AppState.currentTab === 'uniform') {
    AppState.params.uniform = { a: 0.0, b: 10.0 };
    AppState.interval = { a: 2.0, b: 6.0 };
  }

  const inputA = document.getElementById('inputA');
  const inputB = document.getElementById('inputB');
  if (inputA) inputA.value = AppState.interval.a;
  if (inputB) inputB.value = AppState.interval.b;

  renderSliderControls();
  updateWorkbenchCalculations();
}

// Preset Loader
function loadPreset(presetName) {
  if (presetName === 'normal') {
    switchTab('normal');
    AppState.params.normal = { mu: 0.0, sigma: 1.0 };
    AppState.interval = { a: -1.0, b: 1.0 };
  } else if (presetName === 'coin') {
    switchTab('binomial');
    AppState.params.binomial = { n: 30, p: 0.5 };
    AppState.interval = { a: 12, b: 18 };
  } else if (presetName === 'rare') {
    switchTab('poisson');
    AppState.params.poisson = { lambda: 3.5 };
    AppState.interval = { a: 1, b: 5 };
  } else if (presetName === 'waiting') {
    switchTab('exponential');
    AppState.params.exponential = { lambda: 1.5 };
    AppState.interval = { a: 0.2, b: 1.5 };
  }
  const inputA = document.getElementById('inputA');
  const inputB = document.getElementById('inputB');
  if (inputA) inputA.value = AppState.interval.a;
  if (inputB) inputB.value = AppState.interval.b;

  renderSliderControls();
  updateWorkbenchCalculations();
}

// ==========================================
// SCENARIO SOLVER INTERACTION
// ==========================================
async function solveScenarioDynamic(scenarioId) {
  let params = {};
  if (scenarioId === 'server_outage') {
    const lam = parseFloat(document.getElementById('scenLamInput').value) || 3.2;
    const thresh = parseInt(document.getElementById('scenThreshInput').value) || 5;
    params = { lambda: lam, threshold: thresh };
  } else if (scenarioId === 'checkout_funnel') {
    const n = parseInt(document.getElementById('scenNInput').value) || 50;
    const p = parseFloat(document.getElementById('scenPInput').value) || 0.08;
    const kMin = parseInt(document.getElementById('scenKMinInput').value) || 6;
    params = { n, p, k_min: kMin };
  } else if (scenarioId === 'shaft_tolerance') {
    const mu = parseFloat(document.getElementById('scenMuInput').value) || 50.0;
    const sig = parseFloat(document.getElementById('scenSigmaInput').value) || 0.05;
    const lsl = parseFloat(document.getElementById('scenLslInput').value) || 49.90;
    const usl = parseFloat(document.getElementById('scenUslInput').value) || 50.10;
    params = { mu, sigma: sig, lower_spec: lsl, upper_spec: usl };
  }

  try {
    const res = await MathVizAPI.solveScenario(scenarioId, params);
    const resultEl = document.getElementById(`scenResult_${scenarioId}`);
    const stepsEl = document.getElementById(`scenSteps_${scenarioId}`);

    if (resultEl) resultEl.innerText = res.prob_percentage;
    if (stepsEl && res.steps) {
      stepsEl.innerHTML = res.steps.map(s => `<p class="text-xs text-on-surface-variant font-code-math">${s}</p>`).join('');
    }
  } catch (err) {
    console.error("Scenario solve failed:", err);
  }
}

// ==========================================
// MONTE CARLO SIMULATOR VIEW
// ==========================================
async function runMonteCarloSimulation() {
  const exp = document.getElementById('mcExperimentSelect')?.value || 'dice_sum';
  const size = parseInt(document.getElementById('mcSampleSizeSelect')?.value) || 2000;
  
  const statusEl = document.getElementById('mcStatusBadge');
  if (statusEl) {
    statusEl.innerText = 'Simulating...';
    statusEl.className = 'px-3 py-1 rounded-full bg-secondary-fixed text-on-secondary-fixed text-xs font-bold animate-pulse';
  }

  try {
    const data = await MathVizAPI.runMonteCarlo(exp, size, AppState.monteCarlo.params);

    // Update Metrics
    document.getElementById('mcEmpMean').innerText = data.empirical.mean.toFixed(3);
    document.getElementById('mcTheoMean').innerText = data.theoretical.mean.toFixed(3);
    document.getElementById('mcEmpVar').innerText = data.empirical.variance.toFixed(3);
    document.getElementById('mcTheoVar').innerText = data.theoretical.variance.toFixed(3);
    document.getElementById('mcErrorPct').innerText = `${data.error_mean_pct.toFixed(2)}%`;
    document.getElementById('mcTitle').innerText = data.title;

    // Render Charts
    const histSvg = document.getElementById('mcHistogramSvg');
    const convSvg = document.getElementById('mcConvergenceSvg');
    MathVizCharts.renderMonteCarlo(histSvg, data);
    MathVizCharts.renderConvergence(convSvg, data.convergence_curve);

    if (statusEl) {
      statusEl.innerText = `Done (${size.toLocaleString()} trials)`;
      statusEl.className = 'px-3 py-1 rounded-full bg-surface-container-highest text-primary text-xs font-bold';
    }
  } catch (err) {
    console.error("Monte Carlo error:", err);
    if (statusEl) {
      statusEl.innerText = 'Simulation Error';
      statusEl.className = 'px-3 py-1 rounded-full bg-error-container text-on-error-container text-xs font-bold';
    }
  }
}

// ==========================================
// DISTRIBUTION COMPARISON SANDBOX
// ==========================================
async function updateComparisonView() {
  const typeA = document.getElementById('compDistroA')?.value || 'normal';
  const typeB = document.getElementById('compDistroB')?.value || 'student_t';

  const distroA = {
    distribution: typeA,
    params: typeA === 'normal' ? { mu: 0, sigma: 1 } : { n: 20, p: 0.5 },
    calc_mode: 'interval',
    a: -2, b: 2
  };
  const distroB = {
    distribution: typeB,
    params: typeB === 'student_t' ? { df: 3 } : (typeB === 'poisson' ? { lambda: 10 } : { mu: 0, sigma: 1.5 }),
    calc_mode: 'interval',
    a: -2, b: 2
  };

  try {
    const compData = await MathVizAPI.compare(distroA, distroB);
    const svg = document.getElementById('compareSvg');
    MathVizCharts.renderComparison(svg, compData);

    // Update Comparison Metrics
    document.getElementById('compMeanA').innerText = compData.distro_a.mean?.toFixed(2) || '--';
    document.getElementById('compVarA').innerText = compData.distro_a.variance?.toFixed(2) || '--';
    document.getElementById('compMeanB').innerText = compData.distro_b.mean?.toFixed(2) || '--';
    document.getElementById('compVarB').innerText = compData.distro_b.variance?.toFixed(2) || '--';
  } catch (err) {
    console.error("Comparison error:", err);
  }
}

// ==========================================
// CUSTOM DATA LAB & EMPIRICAL FITTING
// ==========================================
function generateSampleData(type) {
  let sample = [];
  if (type === 'normal') {
    // Normal: Latency ~ N(120ms, 15ms)
    for (let i = 0; i < 150; i++) {
      const u1 = Math.random(), u2 = Math.random();
      const z = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
      sample.push(Number((120 + 15 * z).toFixed(2)));
    }
  } else if (type === 'exponential') {
    // Exponential: Time between events ~ Exp(λ=0.05)
    for (let i = 0; i < 150; i++) {
      const u = Math.random();
      sample.push(Number((-Math.log(1 - u) / 0.05).toFixed(2)));
    }
  } else if (type === 'uniform') {
    // Uniform ~ U(10, 50)
    for (let i = 0; i < 150; i++) {
      sample.push(Number((10 + Math.random() * 40).toFixed(2)));
    }
  }
  const textarea = document.getElementById('customDataInput');
  if (textarea) {
    textarea.value = sample.join(', ');
    analyzeCustomData();
  }
}

async function analyzeCustomData() {
  const text = document.getElementById('customDataInput')?.value || '';
  const numbers = text
    .split(/[,\s\n\t]+/)
    .map(s => parseFloat(s.trim()))
    .filter(n => !isNaN(n) && isFinite(n));

  if (numbers.length < 5) {
    alert("Please enter at least 5 valid numbers to analyze empirical distribution.");
    return;
  }

  try {
    const fitData = await MathVizAPI.fitEmpiricalData(numbers, ['normal', 'exponential', 'uniform']);

    // Update Summary Metrics
    document.getElementById('customSampleSize').innerText = fitData.sample_size;
    document.getElementById('customMean').innerText = fitData.metrics.mean.toFixed(2);
    document.getElementById('customMedian').innerText = fitData.metrics.median.toFixed(2);
    document.getElementById('customStdDev').innerText = fitData.metrics.std_dev.toFixed(2);
    document.getElementById('customVariance').innerText = fitData.metrics.variance.toFixed(2);
    document.getElementById('customSkewness').innerText = fitData.metrics.skewness.toFixed(2);
    document.getElementById('customKurtosis').innerText = fitData.metrics.kurtosis.toFixed(2);

    // Update Fitted Models Table
    const tbody = document.getElementById('fittedModelsTbody');
    if (tbody && fitData.fitted_models) {
      let trHtml = '';
      Object.entries(fitData.fitted_models).forEach(([key, model]) => {
        const paramStr = Object.entries(model.params).map(([k, v]) => `${k} = ${v}`).join(', ');
        const pvalColor = model.ks_pvalue > 0.05 ? 'text-emerald-600 font-bold' : 'text-error';
        trHtml += `
          <tr class="hover:bg-surface-container-low border-b border-surface-container">
            <td class="p-2.5 font-bold text-primary">${model.name}</td>
            <td class="p-2.5 font-code-math">${paramStr}</td>
            <td class="p-2.5 font-code-math">${model.ks_statistic.toFixed(4)}</td>
            <td class="p-2.5 font-code-math ${pvalColor}">${model.ks_pvalue.toFixed(4)} ${model.ks_pvalue > 0.05 ? '(Good Fit)' : '(Rejected)'}</td>
            <td class="p-2.5 font-code-math">${model.log_likelihood.toFixed(1)}</td>
          </tr>
        `;
      });
      tbody.innerHTML = trHtml;
    }

    // Render Chart
    const svg = document.getElementById('customDataSvg');
    MathVizCharts.renderEmpiricalFit(svg, fitData);

  } catch (err) {
    console.error("Custom data analysis failed:", err);
  }
}

// ==========================================
// DISCRETE & CONTINUOUS LABS
// ==========================================
async function updateDiscreteView() {
  const dType = document.getElementById('discSelect')?.value || 'binomial';
  let params = {};
  if (dType === 'binomial') {
    const n = parseInt(document.getElementById('discN')?.value) || 20;
    const p = parseFloat(document.getElementById('discP')?.value) || 0.5;
    params = { n, p };
  } else if (dType === 'poisson') {
    const lam = parseFloat(document.getElementById('discLam')?.value) || 4.0;
    params = { lambda: lam };
  } else if (dType === 'geometric') {
    const p = parseFloat(document.getElementById('discGeomP')?.value) || 0.3;
    params = { p };
  }

  const kLow = parseFloat(document.getElementById('discKLow')?.value) || 0;
  const kHigh = parseFloat(document.getElementById('discKHigh')?.value) || 10;

  try {
    const data = await MathVizAPI.calculate(dType, params, 'interval', kLow, kHigh);
    const svg = document.getElementById('discreteSvg');
    MathVizCharts.renderDistribution(svg, data, { showCDF: true });

    document.getElementById('discProbDisplay').innerText = data.prob_percentage;
    document.getElementById('discMeanDisplay').innerText = data.mean.toFixed(2);
    document.getElementById('discVarDisplay').innerText = data.variance.toFixed(2);
  } catch (err) {
    console.error("Discrete lab error:", err);
  }
}

async function updateContinuousView() {
  const cType = document.getElementById('contSelect')?.value || 'normal';
  let params = {};
  if (cType === 'normal') {
    const mu = parseFloat(document.getElementById('contMu')?.value) || 0.0;
    const sigma = parseFloat(document.getElementById('contSigma')?.value) || 1.0;
    params = { mu, sigma };
  } else if (cType === 'exponential') {
    const lam = parseFloat(document.getElementById('contExpLam')?.value) || 1.0;
    params = { lambda: lam };
  } else if (cType === 'student_t') {
    const df = parseFloat(document.getElementById('contDf')?.value) || 5.0;
    params = { df };
  }

  const xLow = parseFloat(document.getElementById('contXLow')?.value) || -1.96;
  const xHigh = parseFloat(document.getElementById('contXHigh')?.value) || 1.96;

  try {
    const data = await MathVizAPI.calculate(cType, params, 'interval', xLow, xHigh);
    const svg = document.getElementById('continuousSvg');
    MathVizCharts.renderDistribution(svg, data, { showCDF: true, showSigma: true });

    document.getElementById('contProbDisplay').innerText = data.prob_percentage;
    document.getElementById('contMeanDisplay').innerText = data.mean.toFixed(2);
    document.getElementById('contVarDisplay').innerText = data.variance.toFixed(2);
  } catch (err) {
    console.error("Continuous lab error:", err);
  }
}

// Search distributions filter
function searchDistributions(query) {
  const q = query.toLowerCase().trim();
  if (!q) return;

  if (q.includes('norm') || q.includes('gauss')) switchTab('normal');
  else if (q.includes('binom') || q.includes('coin')) switchTab('binomial');
  else if (q.includes('poiss') || q.includes('arrival')) switchTab('poisson');
  else if (q.includes('expon') || q.includes('wait') || q.includes('decay')) switchTab('exponential');
  else if (q.includes('unif')) switchTab('uniform');
  else if (q.includes('monte') || q.includes('sim')) switchView('monte-carlo-simulator');
  else if (q.includes('fit') || q.includes('data')) switchView('custom-data-lab');
  else if (q.includes('comp') || q.includes('matrix')) switchTab('matrix');
}

// Initialize on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
  renderSliderControls();
  updateWorkbenchCalculations();

  // Attach search bar listener
  const searchInput = document.getElementById('mainSearchInput');
  if (searchInput) {
    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        searchDistributions(searchInput.value);
      }
    });
  }

  // Toggles
  const toggleCDF = document.getElementById('toggleCDF');
  if (toggleCDF) {
    toggleCDF.addEventListener('change', () => {
      AppState.showCDF = toggleCDF.checked;
      updateWorkbenchCalculations();
    });
  }

  const toggleSigmaGrid = document.getElementById('toggleSigmaGrid');
  if (toggleSigmaGrid) {
    toggleSigmaGrid.addEventListener('change', () => {
      AppState.showSigma = toggleSigmaGrid.checked;
      updateWorkbenchCalculations();
    });
  }
});
