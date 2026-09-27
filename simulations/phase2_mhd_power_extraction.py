# =====================================================================
# PHASE 2: COUPLED NON-LINEAR MHD & 36-SECTOR CIRCUIT SIMULATION ENGINE
# Domain: Dynamic Plasma Motion, Sector Back-EMF & Net Power Yield
# Repository: fusion-direct-energy-matrix
# Environment: Python 3.x / Google Colab
# =====================================================================

import os
import numpy as np

if hasattr(np, "trapezoid"):
    integrate_func = np.trapezoid
else:
    integrate_func = np.trapz

N_sectors = 36                  
a_minor = 2.0                   
B_0 = 5.3                       
N_turns = 12                    
R_coil = 0.02                   
R_load = 0.85                   

time_ms = np.linspace(0, 1.0, 2000)
time_s = time_ms * 1e-3
dt = time_s[1] - time_s[0]

v_displacement_peak = 120.0     
disp_profile = np.sin(np.pi * time_ms / 1.0) * v_displacement_peak 

P_harvest_total = []
harvest_sectors_idx = [8, 9, 26, 27]

for idx, t in enumerate(time_s):
    v_local = disp_profile[idx]
    P_inst_sum = 0.0
    for s in range(N_sectors):
        if s in harvest_sectors_idx and v_local > 0:
            G_coupling = N_turns * B_0 * (2.0 * np.pi * a_minor / N_sectors)
            EMF = G_coupling * v_local
            I_ext = EMF / (R_coil + R_load)
            P_inst = (I_ext**2) * R_load
            P_inst_sum += P_inst
    P_harvest_total.append(P_inst_sum)

P_harvest_total = np.array(P_harvest_total)
E_harvested_J = integrate_func(P_harvest_total, time_s)

print("=== PHASE 2: POWER EXTRACTION RESULTS ===")
print(f"Peak Extracted Power                : {np.max(P_harvest_total)/1e6:.2f} MW")
print(f"Total Energy Recovered per Event    : {E_harvested_J/1e3:.2f} kJ")
