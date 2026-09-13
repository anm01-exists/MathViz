---
name: MathViz Graph Engine
colors:
  surface: '#faf8ff'
  surface-dim: '#d7d9e8'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f3ff'
  surface-container: '#ebedfc'
  surface-container-high: '#e5e7f6'
  surface-container-highest: '#dfe2f1'
  on-surface: '#171b26'
  on-surface-variant: '#3d494c'
  inverse-surface: '#2c303b'
  inverse-on-surface: '#eef0ff'
  outline: '#6d797d'
  outline-variant: '#bcc9cd'
  surface-tint: '#00687a'
  primary: '#00687a'
  on-primary: '#ffffff'
  primary-container: '#06b6d4'
  on-primary-container: '#00424f'
  inverse-primary: '#4cd7f6'
  secondary: '#006b5f'
  on-secondary: '#ffffff'
  secondary-container: '#6df5e1'
  on-secondary-container: '#006f64'
  tertiary: '#855300'
  on-tertiary: '#ffffff'
  tertiary-container: '#e79400'
  on-tertiary-container: '#563400'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#acedff'
  primary-fixed-dim: '#4cd7f6'
  on-primary-fixed: '#001f26'
  on-primary-fixed-variant: '#004e5c'
  secondary-fixed: '#71f8e4'
  secondary-fixed-dim: '#4fdbc8'
  on-secondary-fixed: '#00201c'
  on-secondary-fixed-variant: '#005048'
  tertiary-fixed: '#ffddb8'
  tertiary-fixed-dim: '#ffb95f'
  on-tertiary-fixed: '#2a1700'
  on-tertiary-fixed-variant: '#653e00'
  background: '#faf8ff'
  on-background: '#171b26'
  surface-variant: '#dfe2f1'
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  code-lg:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
  code-md:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '400'
    lineHeight: 14px
    letterSpacing: 0.02em
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.04em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '600'
    lineHeight: 12px
    letterSpacing: 0.06em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-mobile: 0.75rem
  margin: 1.5rem
  margin-mobile: 0.75rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1.25rem
  space-xl: 2rem
---

## Brand & Style

This design system targets researchers, computer science educators, and systems engineers navigating complex algorithmic graph topologies. The aesthetic is precision-engineered, ultra-focused, and highly technical, blending modern light-mode ergonomics with high-contrast computational clarity. 

Key design principles:
- **Instrument-Grade Clarity:** The UI feels like an interactive research terminal or digital oscilloscope rather than a consumer dashboard. Chrome is quiet, letting topological structures and execution pipelines command attention.
- **Topological Signaling:** Dynamic states (e.g., node visits, edge weights, frontier sets) leverage luminous, functionally codified accents against clean light-surface plates to minimize cognitive fatigue during prolonged analysis.
- **Computational Utility:** Interface elements maximize pixel efficiency, structural geometric precision, and monospaced visual balance.

## Colors

The palette leverages high-contrast luminescence against clean structural surfaces to create distinct foreground-to-canvas separation:

- **Canvas & Surface Base:** Crisp light slate (`#F8FAFC`) anchors the primary computational canvas. Layered surfaces, inspectors, and floating docks utilize tinted neutral tones (`#FFFFFF` and `#F1F5F9`) with subtle border delineations (`#CBD5E1`).
- **Primary & Secondary Signals (Inspection & Nodes):** Cyan (`#06B6D4`) serves as the primary system accent for targeted nodes, interactive tool selections, and focused interface triggers. Teal (`#14B8A6`) signifies resolved computation, verified states, and settled edge connections.
- **Tertiary Highlight (Dynamic Execution):** Amber/Orange (`#F59E0B`) is reserved strictly for active execution states: the traversal frontier, path highlights, relaxation steps, and playback cursor positions.
- **Semantic State Coding:**
  - *Unvisited Node/Edge:* Low-contrast muted slate (`#94A3B8`).
  - *Frontier / Evaluating:* Pulsing Amber (`#F59E0B`).
  - *Visited / Closed Set:* Stabilized Teal (`#14B8A6`).
  - *Optimal Path / Selected Flow:* Luminous Cyan (`#06B6D4`) with outer radial luminescence.
  - *Negative Cycle / Critical Alert:* Crimson Rose (`#F43F5E`).

## Typography

Typography splits into two distinct functional disciplines:
- **Inter** executes all natural-language UI, navigation, labels, and modal communications. It provides neutral, crystal-clear readability without eccentricities that distract from complex visualizations.
- **JetBrains Mono** handles all mathematical coordinates, adjacency matrices, weight indicators, JSON algorithmic state payloads, complexity notations ($O(V + E)$), and step counters. 

All numbers within data tables, coordinate readouts, and playback bars must use tabular lining figures (`font-variant-numeric: tabular-nums`) to prevent layout jitter during frame-by-frame traversal execution.

## Layout & Spacing

The layout is built around an edge-to-edge interactive canvas surrounded by docked or floating tool panels:
- **Desktop Grid & Workspace:** Full viewport canvas (`100vw`, `100vh`) with an anchored left-hand toolbar (48px fixed width), a collapsible right-hand algorithm inspector/matrix pane (320px–420px variable width), and a centered floating playback bar docked 24px above the bottom viewport edge.
- **Mobile Reflow:** The viewport maximizes the graph canvas. Toolbars collapse into an absolute top-left floating icon island. The inspector and step-by-step playback controls transition into a bottom swipeable sheet drawer with discrete snaps: peek (64px, playback only), half-sheet (matrix and node stats), and full-screen (raw JSON and algorithm parameterization).
- **Rhythm:** Spacing follows a compact 4px base unit. Data-dense panels (matrix viewports, edge lists) strictly enforce `space-xs` and `space-sm` gaps to maximize visible graph information without scrolling.

## Elevation & Depth

Visual hierarchy uses tonal surface layering combined with low-contrast structural outlines, augmented by chromatic glow effects for execution states:

- **Level 0 (Canvas Base):** Solid light background `#F8FAFC` with a faint coordinate dot-grid rendered at 10% opacity (`#CBD5E1`).
- **Level 1 (Docked Containers & Sidebars):** Background `#FFFFFF` framed with a 1px crisp outline of `#CBD5E1`. Zero blur shadows; flat, structural plane separation.
- **Level 2 (Floating Palettes & Toolbars):** Background `#FFFFFF` at 85% opacity with `backdrop-filter: blur(12px)`. Outlines use `#CBD5E1`. Elevated via an ambient soft drop shadow: `0 12px 32px -4px rgba(0, 0, 0, 0.08)`.
- **Level 3 (Modals & Command Palettes):** Background `#FFFFFF` with a 1px luminous rim of `rgba(6, 182, 212, 0.3)` and a clean shadow: `0 24px 48px -8px rgba(0, 0, 0, 0.12)`.
- **Dynamic Optical Elevation (Active Nodes/Edges):** Interactive graph elements do not use traditional heavy drop shadows. Active states emit radial luminescence using their respective functional hex:
  - Frontier: `box-shadow: 0 0 16px rgba(245, 158, 11, 0.35)`.
  - Optimal/Shortest Path: `box-shadow: 0 0 18px rgba(6, 182, 212, 0.4)`.

## Shapes

This design system uses a strict **Soft (Level 1)** geometric standard to preserve a sharp, clinical CAD-tool profile:
- Primary buttons, input fields, inspector cards, and tool docks use `0.25rem` (4px) corner radii.
- Larger overlays, modal dialogs, and slide-up drawers utilize `0.5rem` (8px) corner radii.
- **Exceptions:**
  - Topological Nodes: Symmetrical circles (`border-radius: 9999px`) maintaining pure geometric radial balance.
  - Step counter badges and algorithm status pills: Fully rounded pill-shapes (`border-radius: 9999px`) to visually contrast against the angular UI panels.

## Components

### Buttons & Interactive Triggers
- **Primary Action (Run / Step Forward):** Solid cyan fill (`#06B6D4`), label in `#FFFFFF` (Inter 600). Hover shifts to `#0891b2` with rapid 150ms ease transition. Active/press scales to 0.98.
- **Secondary (Pause / Reset):** Transparent surface with a 1px border of `#CBD5E1`, text in `#1E293B`. Hover fills with `#F1F5F9` and illuminates the border with `#94A3B8`.
- **Icon Toolbar Buttons:** 36x36px squares, 4px radius, transparent background with muted text (`#64748B`). Active state displays an illuminated cyan border with background `rgba(6, 182, 212, 0.1)`.

### Chips & Status Indicators
- **Node Status Pills:** Rendered in `label-sm` (JetBrains Mono).
  - *Frontier:* Background `rgba(245, 158, 11, 0.15)`, text `#D97706`, 1px solid `rgba(245, 158, 11, 0.3)`.
  - *Visited:* Background `rgba(20, 184, 166, 0.15)`, text `#0D9488`, 1px solid `rgba(20, 184, 166, 0.3)`.
  - *Shortest Path:* Background `rgba(6, 182, 212, 0.15)`, text `#0891b2`, 1px solid `#06B6D4`.

### Graph Nodes & Edges
- **Nodes:** 32px to 48px circles. Default border: 2px solid `#94A3B8`, interior `#FFFFFF`. Node value or key centered in `code-md` font.
- **Edges:** 2px stroke width (`#CBD5E1`). Directed arrows rendered with crisp equilateral heads. Active paths scale stroke to 3px with solid `#06B6D4` or `#F59E0B` and an optical glow. Edge weight tags are displayed on a compact `11px` JetBrains Mono capsule centered on the edge path.

### Inputs & Matrix Controllers
- **Adjacency Cells / Numerical Inputs:** Monospaced input boxes, text right-aligned. Background `#FFFFFF`, 1px border `#CBD5E1`. Focused state: 1px outline `#06B6D4` with zero ring-offset.
- **Matrix View:** Dense grid of square cells separated by 1px rules of `#E2E8F0`. Zero values dimmed to `#94A3B8`; positive connection weights highlighted in `#0D9488`.

### Floating Playback Bar
- Centered dock containing: Previous Step, Play/Pause toggle, Next Step, Progress Scrubber, and Speed Multiplier (`0.5x`, `1x`, `2x`, `MAX`).
- Scrubber track: 4px height `#E2E8F0`, filled buffer in `#06B6D4`, current step thumb a 12px circular amber pip (`#F59E0B`) with hover expansion.

### Inspector Cards
- Modular cards containing algorithm state metadata (Queue, Stack, Distances table). Light plate `#FFFFFF`, border `#CBD5E1`, headers in `label-md` uppercase text with an accent indicator line.