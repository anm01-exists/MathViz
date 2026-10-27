/**
 * MathViz Chart Rendering Engine
 * Dynamic, high-resolution SVG plotting for continuous density functions,
 * discrete probability mass stems, CDF overlays, confidence markers,
 * Monte Carlo convergence paths, and empirical curve fitting.
 */

const MathVizCharts = {
  /**
   * Render distribution chart (Continuous or Discrete)
   */
  renderDistribution(svgElement, data, options = {}) {
    if (!svgElement || !data) return;
    const showCDF = options.showCDF ?? false;
    const showSigma = options.showSigma ?? true;

    const width = 700;
    const height = 320;
    const pad = { top: 25, right: 35, bottom: 42, left: 55 };
    const chartW = width - pad.left - pad.right;
    const chartH = height - pad.top - pad.bottom;

    let svgInner = `
      <defs>
        <linearGradient id="primaryAreaGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#1e40af" stop-opacity="0.38"/>
          <stop offset="100%" stop-color="#1e40af" stop-opacity="0.04"/>
        </linearGradient>
        <linearGradient id="compareGradB" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.30"/>
          <stop offset="100%" stop-color="#06b6d4" stop-opacity="0.03"/>
        </linearGradient>
      </defs>
    `;

    // Horizontal grid lines
    for (let i = 0; i <= 4; i++) {
      const y = pad.top + (chartH / 4) * i;
      svgInner += `<line x1="${pad.left}" y1="${y}" x2="${width - pad.right}" y2="${y}" stroke="#e2e8f0" stroke-dasharray="3,3" />`;
    }

    if (data.type === 'continuous') {
      const points = data.points || [];
      if (points.length === 0) return;

      const xMin = data.x_min ?? points[0].x;
      const xMax = data.x_max ?? points[points.length - 1].x;
      const maxY = Math.max(...points.map(p => p.y));
      const yMax = maxY > 0 ? maxY * 1.18 : 1.0;

      const scaleX = x => pad.left + ((x - xMin) / (xMax - xMin)) * chartW;
      const scaleY = y => pad.top + chartH - (y / yMax) * chartH;

      // Shaded Probability Area
      if (data.shaded_range && data.shaded_range.length === 2) {
        const [a, b] = data.shaded_range;
        const boundedA = Math.max(xMin, Math.min(xMax, a));
        const boundedB = Math.max(xMin, Math.min(xMax, b));

        if (boundedB > boundedA) {
          const areaPoints = points.filter(p => p.x >= boundedA && p.x <= boundedB);
          let pathD = `M ${scaleX(boundedA)} ${scaleY(0)}`;
          areaPoints.forEach(p => {
            pathD += ` L ${scaleX(p.x)} ${scaleY(p.y)}`;
          });
          pathD += ` L ${scaleX(boundedB)} ${scaleY(0)} Z`;
          svgInner += `<path d="${pathD}" fill="url(#primaryAreaGrad)" />`;
        }
      }

      // Continuous PDF line
      let curveD = '';
      points.forEach((p, idx) => {
        curveD += (idx === 0 ? 'M' : 'L') + ` ${scaleX(p.x)} ${scaleY(p.y)}`;
      });
      svgInner += `<path d="${curveD}" fill="none" stroke="#00288e" stroke-width="2.5" stroke-linejoin="round" />`;

      // Optional CDF overlay
      if (showCDF) {
        let cdfD = '';
        points.forEach((p, idx) => {
          const scaledCdfY = p.cdf * (yMax / 1.18);
          cdfD += (idx === 0 ? 'M' : 'L') + ` ${scaleX(p.x)} ${scaleY(scaledCdfY)}`;
        });
        svgInner += `<path d="${cdfD}" fill="none" stroke="#316bf3" stroke-width="2" stroke-dasharray="4,4" />`;
      }

      // Sigma markers
      if (showSigma && data.markers && data.markers.sigmas) {
        data.markers.sigmas.forEach(s => {
          if (s.x >= xMin && s.x <= xMax) {
            const xPos = scaleX(s.x);
            svgInner += `
              <line x1="${xPos}" y1="${scaleY(0)}" x2="${xPos}" y2="${scaleY(yMax * 0.45)}" stroke="#94a3b8" stroke-dasharray="2,2" />
              <text x="${xPos}" y="${height - pad.bottom + 16}" fill="#64748b" font-size="10" text-anchor="middle" font-family="Inter">${s.label}</text>
            `;
          }
        });
      }

      // Mean marker
      if (data.markers && data.markers.mean !== undefined) {
        const meanX = data.markers.mean;
        if (meanX >= xMin && meanX <= xMax) {
          const xPos = scaleX(meanX);
          svgInner += `
            <line x1="${xPos}" y1="${scaleY(0)}" x2="${xPos}" y2="${pad.top}" stroke="#ba1a1a" stroke-width="1.8" stroke-dasharray="4,3" />
            <text x="${xPos}" y="${height - pad.bottom + 16}" fill="#ba1a1a" font-size="11" font-weight="bold" text-anchor="middle" font-family="Inter">μ=${meanX.toFixed(2)}</text>
          `;
        }
      }

      // X-Axis
      svgInner += `<line x1="${pad.left}" y1="${scaleY(0)}" x2="${width - pad.right}" y2="${scaleY(0)}" stroke="#475569" stroke-width="1.5" />`;

    } else {
      // Discrete Distribution (Stem Bars)
      const points = data.points || [];
      if (points.length === 0) return;

      const kMax = data.x_max ?? points[points.length - 1].x;
      const maxY = Math.max(...points.map(p => p.y));
      const yMax = maxY > 0 ? maxY * 1.25 : 1.0;

      const scaleX = k => pad.left + (k / (kMax || 1)) * chartW;
      const scaleY = y => pad.top + chartH - (y / yMax) * chartH;
      const barWidth = Math.max(5, (chartW / (kMax + 1)) * 0.65);

      points.forEach(p => {
        const xPos = scaleX(p.x) - barWidth / 2;
        const barH = (p.y / yMax) * chartH;
        const fillColor = p.in_selection ? '#00288e' : '#cbd5e1';

        svgInner += `
          <rect x="${xPos}" y="${scaleY(p.y)}" width="${barWidth}" height="${barH}" rx="2" fill="${fillColor}" class="transition-colors hover:opacity-80">
            <title>k=${p.x}: P(X=${p.x}) = ${(p.y * 100).toFixed(2)}%</title>
          </rect>
        `;

        if (kMax <= 25 || p.x % 2 === 0) {
          svgInner += `<text x="${scaleX(p.x)}" y="${height - pad.bottom + 16}" fill="#64748b" font-size="10" text-anchor="middle" font-family="Inter">${p.x}</text>`;
        }
      });

      // CDF Step function
      if (showCDF) {
        let stepD = `M ${pad.left} ${scaleY(0)}`;
        points.forEach(p => {
          const scaledCdfY = p.cdf * (maxY / 1.25);
          stepD += ` L ${scaleX(p.x) - barWidth / 2} ${scaleY(scaledCdfY)} L ${scaleX(p.x) + barWidth / 2} ${scaleY(scaledCdfY)}`;
        });
        svgInner += `<path d="${stepD}" fill="none" stroke="#316bf3" stroke-width="2" stroke-dasharray="3,3" />`;
      }

      // Mean line
      if (data.markers && data.markers.mean !== undefined) {
        const meanX = data.markers.mean;
        if (meanX <= kMax) {
          const xPos = scaleX(meanX);
          svgInner += `
            <line x1="${xPos}" y1="${scaleY(0)}" x2="${xPos}" y2="${pad.top}" stroke="#ba1a1a" stroke-width="1.8" stroke-dasharray="4,2" />
            <text x="${xPos}" y="${height - pad.bottom + 30}" fill="#ba1a1a" font-size="11" font-weight="bold" text-anchor="middle" font-family="Inter">E[X]=${meanX.toFixed(2)}</text>
          `;
        }
      }

      svgInner += `<line x1="${pad.left}" y1="${scaleY(0)}" x2="${width - pad.right}" y2="${scaleY(0)}" stroke="#475569" stroke-width="1.5" />`;
    }

    svgElement.innerHTML = svgInner;
  },

  /**
   * Render dual comparison chart (Overlays Distro A & Distro B)
   */
  renderComparison(svgElement, compData) {
    if (!svgElement || !compData) return;
    const resA = compData.distro_a;
    const resB = compData.distro_b;
    const [xMin, xMax] = compData.domain;

    const width = 700;
    const height = 320;
    const pad = { top: 25, right: 35, bottom: 40, left: 50 };
    const chartW = width - pad.left - pad.right;
    const chartH = height - pad.top - pad.bottom;

    const maxYA = resA.points ? Math.max(...resA.points.map(p => p.y)) : 0;
    const maxYB = resB.points ? Math.max(...resB.points.map(p => p.y)) : 0;
    const yMax = Math.max(maxYA, maxYB) * 1.2 || 1.0;

    const scaleX = x => pad.left + ((x - xMin) / (xMax - xMin || 1)) * chartW;
    const scaleY = y => pad.top + chartH - (y / yMax) * chartH;

    let svgInner = '';
    // Grid
    for (let i = 0; i <= 4; i++) {
      const y = pad.top + (chartH / 4) * i;
      svgInner += `<line x1="${pad.left}" y1="${y}" x2="${width - pad.right}" y2="${y}" stroke="#e2e8f0" stroke-dasharray="3,3" />`;
    }

    // Render Distro A (Primary Navy/Blue)
    if (resA.type === 'continuous' && resA.points) {
      let curveA = '';
      resA.points.forEach((p, idx) => {
        curveA += (idx === 0 ? 'M' : 'L') + ` ${scaleX(p.x)} ${scaleY(p.y)}`;
      });
      svgInner += `<path d="${curveA}" fill="none" stroke="#00288e" stroke-width="2.5" />`;
    } else if (resA.points) {
      const barW = Math.max(4, chartW / (resA.points.length * 2));
      resA.points.forEach(p => {
        svgInner += `<rect x="${scaleX(p.x) - barW}" y="${scaleY(p.y)}" width="${barW}" height="${(p.y / yMax) * chartH}" fill="#00288e" opacity="0.85" rx="1" />`;
      });
    }

    // Render Distro B (Secondary Amber/Cyan)
    if (resB.type === 'continuous' && resB.points) {
      let curveB = '';
      resB.points.forEach((p, idx) => {
        curveB += (idx === 0 ? 'M' : 'L') + ` ${scaleX(p.x)} ${scaleY(p.y)}`;
      });
      svgInner += `<path d="${curveB}" fill="none" stroke="#06b6d4" stroke-width="2.5" stroke-dasharray="5,2" />`;
    } else if (resB.points) {
      const barW = Math.max(4, chartW / (resB.points.length * 2));
      resB.points.forEach(p => {
        svgInner += `<rect x="${scaleX(p.x)}" y="${scaleY(p.y)}" width="${barW}" height="${(p.y / yMax) * chartH}" fill="#06b6d4" opacity="0.85" rx="1" />`;
      });
    }

    // Axis
    svgInner += `<line x1="${pad.left}" y1="${scaleY(0)}" x2="${width - pad.right}" y2="${scaleY(0)}" stroke="#475569" stroke-width="1.5" />`;
    svgElement.innerHTML = svgInner;
  },

  /**
   * Render Monte Carlo empirical histogram & theoretical curve
   */
  renderMonteCarlo(svgElement, mcData) {
    if (!svgElement || !mcData || !mcData.histogram) return;
    const hist = mcData.histogram;

    const width = 700;
    const height = 300;
    const pad = { top: 25, right: 35, bottom: 40, left: 50 };
    const chartW = width - pad.left - pad.right;
    const chartH = height - pad.top - pad.bottom;

    const maxVal = Math.max(
      ...hist.map(h => mcData.is_discrete ? h.frequency : h.density),
      ...hist.map(h => h.theoretical || 0)
    );
    const yMax = maxVal > 0 ? maxVal * 1.25 : 1.0;

    const minX = hist[0].bin_start !== undefined ? hist[0].bin_start : hist[0].x;
    const maxX = hist[hist.length - 1].bin_end !== undefined ? hist[hist.length - 1].bin_end : hist[hist.length - 1].x;

    const scaleX = x => pad.left + ((x - minX) / (maxX - minX || 1)) * chartW;
    const scaleY = y => pad.top + chartH - (y / yMax) * chartH;

    let svgInner = '';
    for (let i = 0; i <= 4; i++) {
      const y = pad.top + (chartH / 4) * i;
      svgInner += `<line x1="${pad.left}" y1="${y}" x2="${width - pad.right}" y2="${y}" stroke="#e2e8f0" stroke-dasharray="3,3" />`;
    }

    // Draw Histogram Bars
    hist.forEach((h, idx) => {
      const val = mcData.is_discrete ? h.frequency : h.density;
      const bStart = h.bin_start !== undefined ? h.bin_start : h.x - 0.45;
      const bEnd = h.bin_end !== undefined ? h.bin_end : h.x + 0.45;
      const x0 = scaleX(bStart);
      const x1 = scaleX(bEnd);
      const barW = Math.max(2, x1 - x0 - 1);
      const barH = (val / yMax) * chartH;

      svgInner += `
        <rect x="${x0}" y="${scaleY(val)}" width="${barW}" height="${barH}" fill="#1e40af" opacity="0.65" rx="1.5">
          <title>${h.x}: Emp=${(val * 100).toFixed(2)}% | Theo=${((h.theoretical || 0) * 100).toFixed(2)}%</title>
        </rect>
      `;

      if (idx % Math.ceil(hist.length / 10) === 0) {
        svgInner += `<text x="${scaleX(h.x)}" y="${height - pad.bottom + 16}" fill="#64748b" font-size="10" text-anchor="middle" font-family="Inter">${h.x}</text>`;
      }
    });

    // Draw Theoretical Overlay Curve
    let theoD = '';
    hist.forEach((h, idx) => {
      const y = h.theoretical || 0;
      theoD += (idx === 0 ? 'M' : 'L') + ` ${scaleX(h.x)} ${scaleY(y)}`;
    });
    svgInner += `<path d="${theoD}" fill="none" stroke="#ba1a1a" stroke-width="2.5" />`;

    svgInner += `<line x1="${pad.left}" y1="${scaleY(0)}" x2="${width - pad.right}" y2="${scaleY(0)}" stroke="#475569" stroke-width="1.5" />`;
    svgElement.innerHTML = svgInner;
  },

  /**
   * Render Law of Large Numbers (Convergence Curve)
   */
  renderConvergence(svgElement, curveData) {
    if (!svgElement || !curveData || curveData.length === 0) return;

    const width = 700;
    const height = 180;
    const pad = { top: 20, right: 35, bottom: 35, left: 55 };
    const chartW = width - pad.left - pad.right;
    const chartH = height - pad.top - pad.bottom;

    const allMeans = curveData.map(c => c.running_mean);
    const theoMean = curveData[0].theo_mean;
    const minM = Math.min(theoMean * 0.7, ...allMeans);
    const maxM = Math.max(theoMean * 1.3, ...allMeans);
    const maxTrials = curveData[curveData.length - 1].trial;

    const scaleX = t => pad.left + (t / maxTrials) * chartW;
    const scaleY = m => pad.top + chartH - ((m - minM) / (maxM - minM || 1)) * chartH;

    let svgInner = '';
    // Theoretical Line
    const theoY = scaleY(theoMean);
    svgInner += `
      <line x1="${pad.left}" y1="${theoY}" x2="${width - pad.right}" y2="${theoY}" stroke="#ba1a1a" stroke-width="2" stroke-dasharray="4,2" />
      <text x="${width - pad.right + 4}" y="${theoY + 4}" fill="#ba1a1a" font-size="10" font-weight="bold">μ</text>
    `;

    // Running Mean Path
    let pathD = '';
    curveData.forEach((c, idx) => {
      pathD += (idx === 0 ? 'M' : 'L') + ` ${scaleX(c.trial)} ${scaleY(c.running_mean)}`;
    });
    svgInner += `<path d="${pathD}" fill="none" stroke="#00288e" stroke-width="2" />`;

    svgInner += `<line x1="${pad.left}" y1="${height - pad.bottom}" x2="${width - pad.right}" y2="${height - pad.bottom}" stroke="#94a3b8" />`;
    svgElement.innerHTML = svgInner;
  },

  /**
   * Render Empirical Fitting Chart
   */
  renderEmpiricalFit(svgElement, fitData) {
    if (!svgElement || !fitData || !fitData.histogram) return;
    const hist = fitData.histogram;

    const width = 700;
    const height = 300;
    const pad = { top: 25, right: 35, bottom: 40, left: 55 };
    const chartW = width - pad.left - pad.right;
    const chartH = height - pad.top - pad.bottom;

    const maxDensity = Math.max(...hist.map(h => h.density));
    const yMax = maxDensity > 0 ? maxDensity * 1.3 : 1.0;

    const minX = hist[0].bin_start;
    const maxX = hist[hist.length - 1].bin_end;

    const scaleX = x => pad.left + ((x - minX) / (maxX - minX || 1)) * chartW;
    const scaleY = y => pad.top + chartH - (y / yMax) * chartH;

    let svgInner = '';
    for (let i = 0; i <= 4; i++) {
      const y = pad.top + (chartH / 4) * i;
      svgInner += `<line x1="${pad.left}" y1="${y}" x2="${width - pad.right}" y2="${y}" stroke="#e2e8f0" stroke-dasharray="3,3" />`;
    }

    // Histogram Bars
    hist.forEach(h => {
      const x0 = scaleX(h.bin_start);
      const x1 = scaleX(h.bin_end);
      const barW = Math.max(2, x1 - x0 - 1);
      const barH = (h.density / yMax) * chartH;

      svgInner += `
        <rect x="${x0}" y="${scaleY(h.density)}" width="${barW}" height="${barH}" fill="#316bf3" opacity="0.5" rx="1">
          <title>Range: [${h.bin_start}, ${h.bin_end}] | Count: ${h.count} | Density: ${h.density}</title>
        </rect>
      `;
    });

    // Fitted Models Curves
    const colors = { normal: '#00288e', exponential: '#ba1a1a', uniform: '#10b981' };
    if (fitData.fitted_models) {
      Object.entries(fitData.fitted_models).forEach(([key, model]) => {
        if (model.curve) {
          let curveD = '';
          model.curve.forEach((p, idx) => {
            if (p.x >= minX && p.x <= maxX) {
              curveD += (curveD === '' ? 'M' : 'L') + ` ${scaleX(p.x)} ${scaleY(p.y)}`;
            }
          });
          const strokeColor = colors[key] || '#000000';
          svgInner += `<path d="${curveD}" fill="none" stroke="${strokeColor}" stroke-width="2.5" />`;
        }
      });
    }

    svgInner += `<line x1="${pad.left}" y1="${scaleY(0)}" x2="${width - pad.right}" y2="${scaleY(0)}" stroke="#475569" stroke-width="1.5" />`;
    svgElement.innerHTML = svgInner;
  }
};

window.MathVizCharts = MathVizCharts;
