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
            # Fallback to defaults matching NextGen suite
            self.config = {
                "phase2_structure": {"relative_permeability_ur": 1.0, "max_operating_temp_C": 750.0},
                "phase3_breeder": {"tritium_breeding_ratio": 1.15},
                "phase4_magnets": {"peak_field_Tesla": 20.0}
            }

        self.B_field = self.config["phase4_magnets"]["peak_field_Tesla"]
        self.mu_r = self.config["phase2_structure"]["relative_permeability_ur"]
        self.T_outlet = self.config["phase2_structure"]["max_operating_temp_C"]
        
    def calculate_charged_particle_gyroradius(self, v_perp=5.0e6, particle_type="alpha"):
        """
        Calculates Larmor radius under updated 20 T magnetic field.
        alpha: He-4 nucleus (m = 6.64e-27 kg, q = 3.20e-19 C)
        """
        if particle_type == "alpha":
            m = 6.64e-27
            q = 3.20e-19
        else:  # Deuterium/Tritium ion
            m = 4.17e-27
            q = 1.60e-19
            
        rho_g = (m * v_perp) / (q * self.B_field)
        return rho_g  # in meters

    def calculate_mhd_pressure_drop(self, fluid_velocity=1.5, channel_length=5.0, sigma_fluid=1.0e6):
        """
        Calculates MHD pressure drop across liquid Pb-17Li breeder channels.
        Non-magnetic wall (mu_r = 1.0) eliminates structural magnetic drag term.
        """
        # Hartmann number Ha = B * L * sqrt(sigma / eta)
        # Structural wall conductance ratio C_w is zero for non-magnetic / insulated V-alloy
        C_w = 0.01 if self.mu_r == 1.0 else 0.25  # Legacy steel had high magnetic/conductive drag
        
        # Hartmann pressure drop delta_P = sigma * v * B^2 * L * (C_w / (1 + C_w))
        delta_P = sigma_fluid * fluid_velocity * (self.B_field ** 2) * channel_length * (C_w / (1.0 + C_w))
        return delta_P / 1.0e6  # Convert to MPa

    def evaluate_energy_matrix(self, fusion_power_MW=1250.0, recirculating_power_MW=85.0):
        """
        Evaluates coupled direct energy conversion (DEC) + high-temp Brayton electric yield.
        """
        p_neutron = fusion_power_MW * 0.80
        p_alpha = fusion_power_MW * 0.20
        
        # 1. Direct Energy Conversion on Charged Particles (Alpha & Exhaust Ions)
        # Higher B-field enables 65% direct electrostatic deceleration efficiency
        dec_efficiency = 0.65
        p_dec_electric = p_alpha * dec_efficiency
        p_alpha_thermal_remaining = p_alpha * (1.0 - dec_efficiency)
        
        # 2. High-Temperature Thermal Brayton Cycle (750°C V-Alloy + Pb-17Li limit)
        brayton_efficiency = 0.46
        total_thermal_MW = (p_neutron * 1.15) + p_alpha_thermal_remaining
        p_brayton_electric = total_thermal_MW * brayton_efficiency
        
        # 3. Combined Matrix Output
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
    print("==================================================")
    print(" UPGRADED FUSION DIRECT ENERGY MATRIX (v2.0)     ")
    print("==================================================")
    print(f" Direct Energy Conversion (DEC) : {results['direct_energy_conversion_MWe']} MW(e)")
    print(f" High-Temp Brayton Generation   : {results['brayton_thermal_MWe']} MW(e)")
    print(f" Net Electric Generation        : {results['net_electric_MWe']} MW(e)")
    print(f" Plant Q-Factor                 : {results['plant_q_factor']}x")
    print("==================================================")
