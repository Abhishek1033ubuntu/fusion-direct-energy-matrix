import numpy as np

def optimize_sic_switching(f_switch_kHz=50.0, P_harvest_MW=31.88):
    """
    Evaluates SiC MOSFET high-frequency inverter switching losses.
    """
    E_loss_per_switch_J = 0.0019138  # Joules per pulse
    P_loss_kW = (E_loss_per_switch_J * f_switch_kHz * 1000.0) / 1000.0
    loss_fraction = (P_loss_kW / (P_harvest_MW * 1000.0)) * 100.0
    
    return {
        "Switching_Frequency_kHz": f_switch_kHz,
        "Switching_Loss_kW": round(float(P_loss_kW), 2),
        "Loss_Fraction_Percent": round(float(loss_fraction), 3)
    }

if __name__ == "__main__":
    print("Phase 3 SiC Switching:", optimize_sic_switching())
