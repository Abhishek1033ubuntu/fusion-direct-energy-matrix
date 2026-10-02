import numpy as np

def map_toroidal_field_ripple(N_sectors=36, current_draw_ratio=0.10):
    """
    Maps 36-sector toroidal field modulation and verifies alpha particle confinement.
    """
    phi = np.linspace(0, 2*np.pi, 360)
    B_base = 20.0  # Tesla
    
    # Sector modulation ripple
    B_phi = B_base * (1.0 - current_draw_ratio * np.sin(N_sectors * phi / 2.0)**2)
    
    B_max = np.max(B_phi)
    B_min = np.min(B_phi)
    delta_ripple = (B_max - B_min) / (B_max + B_min)
    
    is_confined = delta_ripple < 0.0075  # Must stay below 0.75% threshold
    
    return {
        "N_sectors": N_sectors,
        "B_max_Tesla": round(float(B_max), 2),
        "B_min_Tesla": round(float(B_min), 2),
        "Global_Ripple_Percent": round(float(delta_ripple * 100), 3),
        "Alpha_Particle_Confinement": "SAFE" if is_confined else "UNSAFE"
    }

if __name__ == "__main__":
    res = map_toroidal_field_ripple()
    print("Phase 1 Ripple Mapping:", res)
