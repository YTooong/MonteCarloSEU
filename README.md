# MonteCarloSEU – Monte Carlo Simulation of Radiation-Induced Upsets (extended for HDPE shielding)

📖 中文版本：[README_CN.md](README_CN.md)

## Usage Instructions

After cloning the repository and installing requirements, run the simulation scripts to generate results. For example:

```bash
git clone https://github.com/youruser/MonteCarloSEU.git
cd MonteCarloSEU
pip install -r requirements.txt
python plot_results.py
python plot_results_composite.py
```

By default, `plot_results.py` will output figures to `results/` including `hdpe_vs_al.png`, `mass_vs_seu.png` (pure material comparisons) and `plot_results_composite.py` will output `composite_curve.png` and `combined_curve.png` (composite vs. pure comparisons). You can adjust parameters in these scripts (such as the number of events `NUM_PROTONS` or the thickness ranges) to explore different scenarios. The simulation uses a default ~E^–2 proton spectrum.

To use a custom spectrum (e.g., a CREME-MC spectrum), place a CSV file (e.g., `creme_spectrum.csv`) in the repository and modify the code to load it:

```python
energies, cdf = load_creme_csv('creme_spectrum.csv')
# ... then call run_simulation(..., use_creme=True, creme_data=(energies, cdf))
```

This will switch the source spectrum to your provided distribution. The shielding configuration can be adjusted via the `layers` parameter. For instance, to simulate 5 mm Al + 10 mm HDPE, set:

```python
layers=[("Aluminum", 5), ("HDPE", 10)]
```

in `run_simulation` or `run_composite_simulation`. The code is documented with comments for clarity and now supports multi-layer shielding inputs.

## CREME-MC Spectrum Format

Ensure the CSV is formatted as two columns: Energy (MeV) and Flux (arbitrary units) or cumulative distribution. The `load_creme_csv` function will sort and normalize it to a CDF.

## Note on Units and Parameters

Maintain consistency of units when changing inputs: energies in MeV, dimensions in mm (for shielding thickness) and μ in mm⁻¹, LET in MeV•cm²/mg, etc. The PSTAR stopping power table for silicon is in `chip.py` and can be extended or refined if needed (e.g., adding more energy points or using data for a different semiconductor). The attenuation coefficients for materials are defined in `chip.py` (we include values for Aluminum and HDPE; additional materials can be added to the `ATTENUATION` dictionary).

For large runs (>10^6 events), enabling Numba JIT (already used in `simulate.py`) can significantly speed up execution. Ensure you have sufficient memory for arrays when increasing `NUM_PROTONS`.

## Citation Guidance

If you use this simulation framework for academic or engineering work, please cite the sources of the physical data we employed. For example:

- Proton stopping powers from **NIST PSTAR (2021)**
- HDPE material properties from **NIST (n.d.)** and **PDG (2017)**
- Critical charge value from **Zhang et al. (2024)**

