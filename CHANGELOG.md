# Changelog

All notable changes to the `fusion-direct-energy-matrix` project will be documented in this file.

## [2.1.0] - 2026-10-02

### Added
- **Asymmetric Power Stroke Cycle Solver (`modules/phase2_power_stroke_solver.py`):** Integrated time-dependent Miller geometry ($R_0=1.25\text{ m}, a=0.45\text{ m}, \kappa=2.20, \delta_{\text{out}}=-0.50, \delta_{\text{in}}=+0.60$) generating $8.462\text{ MJ}$ of net $P\,dV$ mechanical work per cycle.
- **3D Vertical Displacement Control (VDE) Module (`simulations/phase4_vde_control_simulator.py`):** Active PD feedback stabilization for $\kappa = 2.20$ elongation, clamping excursions to $5.0\text{ mm}$ with $3.76\text{ kA-turns}$ peak current ($0.0102\text{ MJ/cycle}$ overhead).
- **Resonant Pulse Frequency Optimization (`simulations/phase4_frequency_tuner.py`):** Validated $20\text{ Hz}$ as the peak resonant frequency, minimizing wall eddy losses ($0.072\text{ MW}$) and SiC switching dissipation ($0.24\text{ MW}$).

### Changed
- Toroidal rotation Mach number optimized from $M_\phi = 0.45$ to $M_\phi = 0.15$, reducing momentum drive cost by $86.4\%$.
- Net energy extraction ratio upgraded from $\eta_{\text{net}} = 1.015\times$ to **$\eta_{\text{net}} = 3.008\times$** ($574.57\text{ MW(e)}$ net output).

## [2.0.0] - 2026-09-15

### Added
- Dual-channel harvesting framework (65% electrostatic DEC + 46% Brayton thermal).
- Cross-integration with `nextgen-tokamak-materials-suite`.
- Modular 32-unit Tokamak Battery array configuration.
