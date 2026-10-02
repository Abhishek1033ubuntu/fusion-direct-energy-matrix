import numpy as np

class VDEControlSimulator:
    """
    3D Vertical Displacement Event (VDE) Simulator for kappa = 2.20 elongation.
    """
    def __init__(self, R0=1.25, a=0.45, kappa=2.2, Ip_MA=12.0, B0=20.0):
        self.R0 = R0
        self.a = a
        self.kappa = kappa
        self.Ip = Ip_MA * 1e6
        self.B0 = B0
        self.n_s = 1.45
        self.B_pol = 1.50
        self.K_z = (2.0 * np.pi * self.Ip * self.B_pol * self.n_s) / self.R0
        self.gamma_vde = 64.9

    def run_vde_simulation(self, t_sim=0.040, dt=1e-5, Z_init_m=0.005):
        steps = int(t_sim / dt)
        t = np.linspace(0, t_sim, steps)

        Z = np.zeros(steps)
        dZ_dt = np.zeros(steps)
        I_coil = np.zeros(steps)
        P_control_W = np.zeros(steps)

        Z[0] = Z_init_m

        L_coil = 1.2e-4
        R_coil = 0.015
        B_per_A = 2.5e-6

        K_P = 1.35 * self.K_z
        K_D = 0.015 * self.K_z

        for i in range(1, steps):
            F_unstable = self.K_z * Z[i-1]
            F_control = -(K_P * Z[i-1] + K_D * dZ_dt[i-1])
            F_net = F_unstable + F_control
            C_damp = self.K_z / self.gamma_vde
            
            dZ_dt[i] = F_net / C_damp
            Z[i] = Z[i-1] + dZ_dt[i] * dt

            B_required = np.abs(F_control) / (2.0 * np.pi * self.R0 * self.Ip)
            I_coil[i] = B_required / B_per_A

            dI_dt = (I_coil[i] - I_coil[i-1]) / dt
            P_control_W[i] = (I_coil[i] ** 2) * R_coil + L_coil * I_coil[i] * np.abs(dI_dt)

        P_avg_MW = np.mean(P_control_W) / 1e6
        E_vde_control_MJ = P_avg_MW * 0.020

        return {
            "Z_max_excursion_mm": round(float(np.max(np.abs(Z)) * 1000.0), 2),
            "I_coil_peak_kA": round(float(np.max(I_coil) / 1e3), 2),
            "P_control_avg_MW": round(float(P_avg_MW), 3),
            "VDE_Energy_Cost_per_cycle_MJ": round(float(E_vde_control_MJ), 4)
        }

if __name__ == "__main__":
    vde = VDEControlSimulator()
    print("VDE Control Output:", vde.run_vde_simulation())
