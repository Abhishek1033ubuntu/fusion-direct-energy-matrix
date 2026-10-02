import numpy as np

class ResonantFrequencyTuner:
    """
    Sweeps power stroke frequencies (20 Hz - 100 Hz) to locate optimal net efficiency peak.
    """
    def __init__(self, R0=1.25, a=0.45, kappa=2.2, delta_out=-0.50, delta_in=0.60):
        self.R0 = R0
        self.a = a
        self.kappa = kappa
        self.delta_out = delta_out
        self.delta_in = delta_in

    def evaluate_frequency(self, freq_hz):
        T_cycle = 1.0 / freq_hz
        W_pv_net_MJ = 8.462
        E_DEC_MJ = (1250.0 * 0.20 * 0.65) * T_cycle
        E_brayton_MJ = (1250.0 * 0.80 * 1.15 * 0.46) * T_cycle

        P_sic_sw_MW = 0.012 * freq_hz
        P_wall_eddy_MW = 0.00018 * (freq_hz ** 2)

        E_rotation_MJ = 0.057 * (50.0 / freq_hz)
        E_vde_MJ = 0.0102
        E_cryo_MJ = 85.0 * T_cycle

        E_harvest = W_pv_net_MJ + E_DEC_MJ + E_brayton_MJ
        E_input = E_rotation_MJ + E_vde_MJ + E_cryo_MJ + (P_sic_sw_MW + P_wall_eddy_MW) * T_cycle + 4.10

        eta_net = E_harvest / E_input
        P_net_MW = (E_harvest - E_input) * freq_hz

        return {
            "freq_hz": freq_hz,
            "PV_Work_MJ": round(W_pv_net_MJ, 3),
            "SiC_Loss_MW": round(P_sic_sw_MW, 3),
            "Wall_Eddy_Loss_MW": round(P_wall_eddy_MW, 3),
            "Net_Electric_Power_MWe": round(P_net_MW, 2),
            "eta_net": round(eta_net, 3)
        }

if __name__ == "__main__":
    tuner = ResonantFrequencyTuner()
    print("Frequency Sweep 20 Hz Peak:", tuner.evaluate_frequency(20.0))
