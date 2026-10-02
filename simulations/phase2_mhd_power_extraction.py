import numpy as np

def compute_mhd_pulse_yield(v_peak=120.0, a=0.45, N_sectors=36, B0=20.0, R_load=0.85):
    """
    Calculates Faraday back-EMF and peak inductive pulse harvesting.
    """
    arc_length = (2.0 * np.pi * a) / N_sectors
    V_emf = B0 * arc_length * v_peak
    I_peak = V_emf / R_load
    P_peak_MW = (I_peak ** 2 * R_load) / 1e6
    
    return {
        "V_EMF_volts": round(float(V_emf), 2),
        "I_peak_amperes": round(float(I_peak), 2),
        "Peak_Harvest_Power_MW": round(float(P_peak_MW), 2)
    }

if __name__ == "__main__":
    print("Phase 2 MHD Yield:", compute_mhd_pulse_yield())
