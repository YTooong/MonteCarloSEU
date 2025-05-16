import numpy as np

# Simulation grid for upset mapping (64×64 memory array)
GRID_SIZE = 64

# Sensitive volume depth (meters)
PIXEL_DEPTH = 5e-6  # 5 micrometers

# Critical charge threshold (Coulomb)
Qc = 1.8e-16  # 0.18 fC

# NIST PSTAR stopping power data for protons in silicon (MeV*cm^2/mg)
PSTAR_energy = np.array([1, 5, 10, 20, 50, 100])
PSTAR_LET = np.array([0.2, 0.08, 0.03, 0.015, 0.010, 0.003])

def get_LET(energy_mev):
    """Interpolate LET (MeV·cm²/mg) for given energy(s) (MeV) in silicon."""
    # Supports both scalar and array inputs
    return np.interp(energy_mev, PSTAR_energy, PSTAR_LET)

# Convert sensitive volume to mass thickness (mg/cm²)
density_si = 2.33  # g/cm³ for silicon
density_si_mg = density_si * 1000  # mg/cm³
depth_cm = PIXEL_DEPTH * 100  # 5e-6 m = 5e-4 cm
mass_thickness_mg = density_si_mg * depth_cm  # mg/cm²

# Conversion from MeV to Coulomb: approximately 4.45e-14 C per MeV deposited
MEV_TO_COULOMB = 1.602e-13 / 3.6  # ~4.45e-14 C per MeV
# Energy deposit threshold (MeV) corresponding to Qc
E_threshold_MeV = Qc / MEV_TO_COULOMB

# Attenuation coefficients (mm⁻¹) for shielding materials
ATTENUATION = {
    "Aluminum": 0.008,
    "HDPE": 1e-3
}