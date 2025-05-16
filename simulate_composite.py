import numpy as np
from sampling import sample_power_law, sample_creme
from chip import ATTENUATION, get_LET, mass_thickness_mg, E_threshold_MeV

def run_composite_simulation(num_events, layers, use_creme=False, creme_data=None):
    """
    Monte Carlo SEU simulation for multiple shielding layers.
    layers: list of (material, thickness_mm) tuples.
    """
    # 1. 采样能量
    if use_creme and creme_data is not None:
        energies = sample_creme(num_events, *creme_data)
    else:
        energies = sample_power_law(num_events)

    # 2. 透射概率叠加
    surv_prob = np.ones(num_events)
    for material, thickness in layers:
        mu = ATTENUATION.get(material, 0.0)
        surv_prob *= np.exp(-mu * thickness)

    # 3. 筛选存活质子
    survived = np.random.rand(num_events) < surv_prob
    E_surv = energies[survived]

    # 4. 计算沉积并判定 SEU
    LET_vals = get_LET(E_surv)
    E_dep = LET_vals * mass_thickness_mg
    upset_mask = E_dep >= E_threshold_MeV
    num_upsets = np.count_nonzero(upset_mask)

    return num_upsets, survived.sum()
