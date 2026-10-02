import numpy as np
import json
import os

class DirectEnergyMatrixV2:
    """
    Direct Energy Matrix Solver v2.0
    Cross-integrated with NextGen Tokamak Materials Suite parameters.
    """
    def __init__(self, config_path="./config/materials_bridge_config.json"):
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                self.config = json.load(f)["ingested_parameters"]
        else:
            self.config = {
                "phase2_structure": {"relative_permeability_ur": 1.0, "max_operating_temp_C": 750.0},
                "phase3_breeder": {"tritium_breeding_ratio": 1.15},
                "phase4_magnets": {"peak_field_Tesla": 20.0}
            }

        self.B_field = self.config["phase4_magnets"]["peak_field_Tesla"]
        self.mu_r = self.config["phase2_structure"]["relative_permeability_ur"]
        self.T_outlet = self.config["phase2_structure"]["max_operating_temp_C"]
        
    def calculate_charged_particle_gyroradius(self, v_perp=5.0e6, particle_type="alpha"):
        if particle_type == "alpha":
            m, q = 6.64e-27, 3.20e-19
        else:
            m, q = 4.17e-27, 1.60e-19
            
        rho_g = (m * v_perp) / (q * self.B_field)
        return rho_g

    def calculate_mhd_pressure_drop(self, fluid_velocity=1.5, channel_length=5.0, sigma_fluid=1.0e6):
        C_w = 0.01 if self.mu_r == 1.0 else 0.25
        delta_P = sigma_fluid * fluid_velocity * (self.B_field ** 2) * channel_length * (C_w / (1.0 + C_w))
        return delta_P / 1.0e6

    def evaluate_energy_matrix(self, fusion_power_MW=1250.0, recirculating_power_MW=85.0):
        p_neutron = fusion_power_MW * 0.80
        p_alpha = fusion_power_MW * 0.20
        
        dec_efficiency = 0.65
        p_dec_electric = p_alpha * dec_efficiency
        p_alpha_thermal_remaining = p_alpha * (1.0 - dec_efficiency)
        
        brayton_efficiency = 0.46
        total_thermal_MW = (p_neutron * 1.15) + p_alpha_thermal_remaining
        p_brayton_electric = total_thermal_MW * brayton_efficiency
        
        gross_electric_MW = p_dec_electric + p_brayton_electric
        net_electric_MW = gross_electric_MW - recirculating_power_MW
        plant_q_factor = net_electric_MW / recirculating_power_MW
        
        return {
            "fusion_power_MW": fusion_power_MW,
            "toroidal_field_Tesla": self.B_field,
            "direct_energy_conversion_MWe": round(p_dec_electric, 2),
            "brayton_thermal_MWe": round(p_brayton_electric, 2),
            "gross_electric_MWe": round(gross_electric_MW, 2),
            "net_electric_MWe": round(net_electric_MW, 2),
            "plant_q_factor": round(plant_q_factor, 2)
        }

if __name__ == "__main__":
    engine = DirectEnergyMatrixV2()
    results = engine.evaluate_energy_matrix()
    print("Direct Energy Conversion (DEC):", results['direct_energy_conversion_MWe'], "MW(e)")
    print("High-Temp Brayton Generation  :", results['brayton_thermal_MWe'], "MW(e)")
    print("Net Electric Generation       :", results['net_electric_MWe'], "MW(e)")
    print("Plant Q-Factor                :", results['plant_q_factor'], "x")
