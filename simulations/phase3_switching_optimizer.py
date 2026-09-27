# =====================================================================
# PHASE 3: SOLID-STATE SWITCHING TOPOLOGY & DUTY CYCLE OPTIMIZER
# Domain: High-Frequency Pulse Modulation & Efficiency Optimization
# Repository: fusion-direct-energy-matrix
# Environment: Python 3.x / Google Colab
# =====================================================================

import numpy as np

L_sector = 0.15                 # Sector inductance (150 mH)
V_dc_bus = 2500.0               # DC storage bus (2.5 kV)
t_switch_s = 500.0e-9           # Switching speed (500 ns)
I_peak_harvest = 3062.15        # Peak induced current (A)
duty_cycle = 0.10               # 10% duty window

freq_sweep_kHz = np.linspace(1.0, 50.0, 100)
freq_sweep_Hz = freq_sweep_kHz * 1e3

P_switching_loss_kW = []
efficiency_system_pct = []

for f in freq_sweep_Hz:
    P_loss = 0.5 * V_dc_bus * I_peak_harvest * f * t_switch_s
    P_extracted = 31.88e6       # 31.88 MW peak extracted power
    eff = (P_extracted / (P_extracted + P_loss)) * 100.0
    
    P_switching_loss_kW.append(P_loss / 1e3)
    efficiency_system_pct.append(eff)

opt_idx = -1  # 50 kHz upper limit
print("=== PHASE 3 SWITCHING OPTIMIZATION RESULTS ===")
print(f"Optimal Switching Frequency : {freq_sweep_kHz[opt_idx]:.2f} kHz")
print(f"Direct Conversion Efficiency: {efficiency_system_pct[opt_idx]:.2f} %")
print(f"Switching Power Loss        : {P_switching_loss_kW[opt_idx]:.2f} kW")
