import numpy as np

def sample_power_law(N, E_min=1.0, E_max=100.0, alpha=2.0):
    """Sample N proton energies from a power-law spectrum dΦ ∝ E^-alpha."""
    if alpha == 1.0:
        # Special case (log-flat)
        return E_min * (E_max / E_min) ** np.random.rand(N)
    # Inverse‐CDF sampling for α≠1
    r = np.random.rand(N)
    inv_Emin = 1.0 / E_min
    inv_Emax = 1.0 / E_max
    inv_E = inv_Emin - r * (inv_Emin - inv_Emax)
    return 1.0 / inv_E

def load_creme_csv(filepath):
    """Load a CREME‑MC spectrum CSV with 'Energy[MeV], Flux' columns."""
    data = np.loadtxt(filepath, delimiter=',', comments='#')
    energies, flux = data[:, 0], data[:, 1]
    sort_idx = np.argsort(energies)
    energies = energies[sort_idx]
    flux = flux[sort_idx]
    cum_flux = np.cumsum(flux)
    cdf = cum_flux / cum_flux[-1]
    return energies, cdf

def sample_creme(N, energies, cdf):
    """Sample N energies from a CREME‑MC CDF."""
    r = np.random.rand(N)
    idx = np.searchsorted(cdf, r)
    idx = np.clip(idx, 1, len(cdf) - 1)
    lo, hi = idx - 1, idx
    frac = (r - cdf[lo]) / (cdf[hi] - cdf[lo] + 1e-12)
    return energies[lo] + frac * (energies[hi] - energies[lo])
