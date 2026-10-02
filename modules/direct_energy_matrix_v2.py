import numpy as np

class DirectEnergyMatrixV2:
    """
    Base Dual-Channel Harvesting Module (v2.0.0 Architecture).
    Calculates electrostatic DEC yield and supercritical CO2 Brayton thermal outputs.
    """
    def __init__(self, P_fusion_MW=1250.0, B0=20.0):
        self.P_fusion = P_fusion_MW
        self.B0 = B0
        self.eta_dec = 0.65       # 65% Direct Electrostatic DEC efficiency
        self.eta_brayton = 0.46   # 46% sCO2 Brayton thermal efficiency

    def compute_dual_channel_power(self):
        # 20% Alpha Channel / Charged particle fraction
        P_charged_MW = self.P_fusion * 0.20
        P_dec_MWe = P_charged_MW * self.eta_dec

        # 80% Neutron Thermal Channel + Blanket Multiplication Factor (1.15)
        P_thermal_MW = self.P_fusion * 0.80 * 1.15
        P_brayton_MWe = P_thermal_MW * self.eta_brayton

        P_gross_MWe = P_dec_MWe + P_brayton_MWe
        P_cryo_MW = 85.0  # REBCO HTS 20K cryopump load
        P_net_MWe = P_gross_MWe - P_cryo_MW

        return {
            "Fusion_Thermal_MW": self.P_fusion,
            "DEC_Electric_MWe": round(P_dec_MWe, 2),
            "Brayton_Electric_MWe": round(P_brayton_MWe, 2),
            "Gross_Electric_MWe": round(P_gross_MWe, 2),
            "House_Cryo_Load_MW": P_cryo_MW,
            "Net_Electric_MWe": round(P_net_MWe, 2),
            "Plant_Q_Factor": round(P_gross_MWe / P_cryo_MW, 2)
        }

if __name__ == "__main__":
    matrix = DirectEnergyMatrixV2()
    out = matrix.compute_dual_channel_power()
    print("v2.0 Base Yield:", out)
