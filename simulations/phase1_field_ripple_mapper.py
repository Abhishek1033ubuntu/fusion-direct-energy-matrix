# =====================================================================
# PHASE 1: 36-SECTOR TOKAMAK VACUUM MAGNETIC FIELD & RIPPLE MAPPER
# Domain: 3D Field Superposition, Sector Modulation & Ripple Bounds
# Repository: fusion-direct-energy-matrix
# Environment: Python 3.x / Google Colab
# =====================================================================

import os
import numpy as np
import matplotlib.pyplot as plt

os.makedirs("../figures", exist_ok=True)
os.makedirs("figures", exist_ok=True)

N_sectors = 36                  # 36 independent field/harvesting sectors
R_0 = 6.2                       # Major radius (m)
a_minor = 2.0                   # Minor radius (m)
B_0 = 5.3                       # Nominal on-axis field (Tesla)

phi_coils = np.linspace(0, 2 * np.pi, N_sectors, endpoint=False)
phi_grid = np.linspace(0, 2 * np.pi, 1000)

def compute_toroidal_field(sector_current_factors):
    B_total = np.zeros_like(phi_grid)
    for i, phi_c in enumerate(phi_coils):
        d_phi = phi_grid - phi_c
        d_phi = (d_phi + np.pi) % (2 * np.pi) - np.pi
        w_coil = 2.0 * np.pi / N_sectors
        shape_factor = np.exp(- (d_phi / (0.4 * w_coil))**2)
        B_total += (B_0 / N_sectors) * sector_current_factors[i] * (1.0 + 0.8 * shape_factor)
    return B_total

currents_baseline = np.ones(N_sectors)
currents_harvesting_10pct = np.ones(N_sectors)
harvesting_sectors = [8, 9, 26, 27]
currents_harvesting_10pct[harvesting_sectors] = 0.90 

B_base = compute_toroidal_field(currents_baseline)
B_harv_10 = compute_toroidal_field(currents_harvesting_10pct)

def calculate_ripple_percent(B_field):
    return ((np.max(B_field) - np.min(B_field)) / (np.max(B_field) + np.min(B_field))) * 100.0

ripple_base = calculate_ripple_percent(B_base)
ripple_harv_10 = calculate_ripple_percent(B_harv_10)

print(f"=== PHASE 1 RIPPLE MAPPING RESULTS ===")
print(f"Baseline Toroidal Field Ripple  : {ripple_base:.3f} %")
print(f"10% Sector Harvesting Ripple    : {ripple_harv_10:.3f} % (SAFE ZONE < 0.75%)")
