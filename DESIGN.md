---
name: Empirical Light
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#444653'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#757684'
  outline-variant: '#c4c5d5'
  surface-tint: '#3755c3'
  primary: '#00288e'
  on-primary: '#ffffff'
  primary-container: '#1e40af'
  on-primary-container: '#a8b8ff'
  inverse-primary: '#b8c4ff'
  secondary: '#0051d5'
  on-secondary: '#ffffff'
  secondary-container: '#316bf3'
  on-secondary-container: '#fefcff'
  tertiary: '#003a46'
  on-tertiary: '#ffffff'
  tertiary-container: '#005362'
  on-tertiary-container: '#3cccea'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dde1ff'
  primary-fixed-dim: '#b8c4ff'
  on-primary-fixed: '#001453'
  on-primary-fixed-variant: '#173bab'
  secondary-fixed: '#dbe1ff'
  secondary-fixed-dim: '#b4c5ff'
  on-secondary-fixed: '#00174b'
  on-secondary-fixed-variant: '#003ea8'
  tertiary-fixed: '#acedff'
  tertiary-fixed-dim: '#4cd7f6'
  on-tertiary-fixed: '#001f26'
  on-tertiary-fixed-variant: '#004e5c'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 3rem
    fontWeight: '700'
    lineHeight: 3.5rem
    letterSpacing: -0.03em
  display-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 2.25rem
    fontWeight: '700'
    lineHeight: 2.75rem
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 2rem
    fontWeight: '600'
    lineHeight: 2.5rem
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 1.5rem
    fontWeight: '600'
    lineHeight: 2rem
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 1.25rem
    fontWeight: '600'
    lineHeight: 1.75rem
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 1.125rem
    fontWeight: '400'
    lineHeight: 1.75rem
  body-md:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: '400'
    lineHeight: 1.5rem
  body-sm:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: '400'
    lineHeight: 1.25rem
  label-md:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: '600'
    lineHeight: 1.25rem
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 0.75rem
    fontWeight: '500'
    lineHeight: 1rem
    letterSpacing: 0.02em
  code-math:
    fontFamily: Inter
    fontSize: 0.9375rem
    fontWeight: '400'
    lineHeight: 1.5rem
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-sm: 1rem
  gutter-lg: 2rem
  margin: 1rem
  margin-md: 2rem
  margin-lg: 3rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system embodies an academic, rigorous, and visually crystalline atmosphere engineered for interactive exploration of probability and statistical models. It bridges the authority of scholarly research with modern, responsive computational interfaces.

The emotional baseline is clarity, precision, and intellectual calm. The interface prioritizes reducing cognitive overhead so dynamic distribution curves, Monte Carlo simulations, and mathematical proofs can be read without distraction. 

The aesthetic is Modern Scholarly Minimalism:
- Base canvases are clinical, crisp, and high-key.
- Density is calibrated to balance technical data density with generous negative space.
- Interactive controls evoke tactile physical laboratory instruments without gratuitous skeuomorphism.

## Colors

The palette establishes structural hierarchy and analytical categorization. 

### Structure & Neutral Anchors
- **Canvas Base:** `#f8fafc` (Slate 50) sets an expansive, soft ambient backdrop that prevents eye strain during prolonged analysis.
- **Surface Layer:** `#ffffff` forms cards, calculator decks, and control panels.
- **Divider & Border Rules:** `#e2e8f0` provides crisp structural definition.
- **Ink Primary:** `#0f172a` (Slate 900) ensures accessible contrast for mathematical formulas, parameters, and prose.
- **Ink Muted:** `#475569` and `#64748b` for metadata, notation notes, and secondary axes.

### Brand & Interactive Elements
- **Brand Primary:** `#1e40af` (Deep Navy) anchors navigation, primary structural markers, and core call-to-action buttons.
- **Brand Secondary / Interactive Action:** `#2563eb` provides clear interactive affordances for active states, selected slider handles, and toggles.

### Distribution & Data Accents
A specialized 4-channel chromatic taxonomy designates comparative statistical layers across chart components:
- **Distribution Alpha (Indigo):** `#6366f1` (Gaussian / Theoretical Normal)
- **Distribution Beta (Cyan):** `#06b6d4` (Poisson / Empirical Samples)
- **Distribution Gamma (Emerald):** `#10b981` (Confidence Intervals / Null Hypothesis True)
- **Distribution Delta (Amber):** `#f59e0b` (P-Value Boundaries / Critical Rejection Regions)

## Typography

The typographic hierarchy accommodates standard technical layout alongside KaTeX / LaTeX mathematical expressions.

- **Headlines (Plus Jakarta Sans):** Selected for its geometric clarity and open counters. It provides an approachable entry point to complex statistical subject matter without feeling cold or overly commercial.
- **Body & Controls (Inter):** The baseline workhorse. Calibrated x-height and distinctive tabular figures (`tnum`) ensure numbers, confidence scores, and matrix vectors stay aligned vertically in dense data arrays.
- **KaTeX / Math Integration:** Formulas rendered inline or as block equations harmoniously inherit baseline height from Inter via `body-md` and `body-lg`. KaTeX's default TeX-rendered fonts (`KaTeX_Main`, `KaTeX_Math`) align seamlessly with the vertical rhythm of the surrounding Inter prose.

## Layout & Spacing

The layout is built upon an adaptive 12-column fluid grid system engineered for dual-pane interactive workbenches (parameter controls on one side, dynamic canvas visualization on the other).

- **Desktop (>= 1200px):** 12-column grid, `margin-lg` (3rem) edge offset, and `gutter-lg` (2rem). Supports a split-screen layout: a 4-column parameter inspector docked alongside an 8-column real-time rendering chart.
- **Tablet (768px - 1199px):** 8-column grid with `gutter` (1.5rem). Modules stack into a vertical flow: interactive inputs become sticky parameter strips directly above the visualization canvas.
- **Mobile (< 768px):** 4-column fluid layout with `margin` (1rem) and `gutter-sm` (1rem). Complex math matrices reflow into horizontal scrollable viewports.

Spacing rhythm relies exclusively on multiples of 4px/8px to match visual graphing intervals.

## Elevation & Depth

Visual hierarchy uses subtle ambient shadows, low-contrast boundary lines, and layered white surfaces rather than heavy drop-shadows.

- **Level 0 (Base Canvas):** `#f8fafc`. The non-interactive foundation across all layouts.
- **Level 1 (Structural Surfaces & Cards):** `#ffffff` with a hairline border of `1px solid #e2e8f0` and an ambient shadow: `0 1px 3px 0 rgba(15, 23, 42, 0.04), 0 1px 2px -1px rgba(15, 23, 42, 0.04)`.
- **Level 2 (Active Simulators & Hovered Panels):** Raised cards and active experiment containers receive: `0 4px 6px -1px rgba(15, 23, 42, 0.05), 0 2px 4px -2px rgba(15, 23, 42, 0.03)`.
- **Level 3 (Modals, Math Overlays & Floating Toolbars):** Overlaid floating distribution readouts and inspect popovers utilize `0 10px 15px -3px rgba(15, 23, 42, 0.08), 0 4px 6px -4px rgba(15, 23, 42, 0.03)` combined with a frosted backdrop (`backdrop-filter: blur(8px); background-color: rgba(255, 255, 255, 0.92)`).

## Shapes

The interface specifies a consistent `roundedness: 2` scale, standardizing container and component radii:
- Standard interactive elements (inputs, toolbars, buttons) implement `0.5rem` (8px).
- Module frames, simulation viewports, and primary structural cards feature `rounded-xl` (`1rem` / 16px) to keep scientific data feeling welcoming and modern.
- Interactive range sliders and quantitative status badges use pill borders (`9999px`) to emphasize fluidity and drag-based manipulation.

## Components

### Buttons
- **Primary:** Filled with `#1e40af`, text in pure white. Height of 40px, padding `0 1.25rem`, radius `0.5rem`. Smooth transition into hover background `#1d4ed8`.
- **Secondary / Action:** Surface `#ffffff`, border `1px solid #e2e8f0`, text `#1e40af`. On hover, background shifts to `#eff6ff` (Navy 50) and border turns `#bfdbfe`.
- **Icon / Math Symbol Controls:** Fixed 36px x 36px square buttons with centered Greek notation or operation glyphs ($\int, \Sigma, \mu, \sigma$), subtle gray border on hover.

### Distribution Chips & Tags
- Pill-shaped (`rounded-full`) tags displaying distribution parameters ($\mu = 0$, $\sigma^2 = 1$).
- Backgrounds use 10% opacity tints of the distribution colors (`#e0e7ff` for Indigo, `#cffafe` for Cyan, `#d1fae5` for Emerald, `#fef3c7` for Amber) with solid matching borders and dark tinted text.

### Interactive Sliders & Inputs
- **Range Sliders:** 6px track height with background `#e2e8f0`. Active fill corresponds to the distribution color currently being adjusted. Thumb handle is a 20px circle (`#ffffff`) with a 2px solid `#2563eb` border and Level 2 elevation shadow.
- **Numeric Field Inputs:** Pure white surface, `1px solid #cbd5e1`, 0.5rem radius. Focus state swaps the border to `#2563eb` with a 3px outer ring tinted at `rgba(37, 99, 235, 0.15)`. Font variant is set strictly to `font-feature-settings: "tnum"`.

### Cards & Analytical Decks
- Framed in `rounded-xl` with Level 1 elevation and crisp `1px solid #e2e8f0` stroke.
- Header bars are partitioned by a horizontal rule, cleanly separating LaTeX hypothesis statements from real-time rendered SVG density plots below.

### Formula & Proof Displays
- Styled block quotes for theorem cards: crisp left-border of 3px in `#1e40af`, soft background `#f8fafc`, padding `1rem 1.25rem`, displaying centered high-resolution KaTeX rendering.