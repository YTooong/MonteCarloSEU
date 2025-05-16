import os
import numpy as np
import matplotlib.pyplot as plt
from simulate import run_simulation

# 确保输出目录存在
os.makedirs('results', exist_ok=True)

# 参数
NUM_PROTONS = 100000  # 每个厚度点的质子事件数
thickness_range = np.linspace(0, 50, 11)  # 0 到 50 mm，11 个点

# 1. 铝 vs HDPE 屏蔽曲线
al_upset_rates = []
hdpe_upset_rates = []
for t in thickness_range:
    upsets_al, _ = run_simulation(NUM_PROTONS, layers=[("Aluminum", t)])
    upsets_hd, _ = run_simulation(NUM_PROTONS, layers=[("HDPE", t)])
    al_upset_rates.append(upsets_al / NUM_PROTONS)
    hdpe_upset_rates.append(upsets_hd / NUM_PROTONS)

plt.figure()
plt.plot(thickness_range, al_upset_rates, 'o-', label='Aluminum')
plt.plot(thickness_range, hdpe_upset_rates, 's--', label='HDPE')
plt.xlabel('Shield Thickness (mm)')
plt.ylabel('SEU Probability per Proton')
plt.title('SEU Rate vs. Shielding Thickness (Al vs. HDPE)')
plt.legend()
plt.grid(True)
plt.savefig('results/hdpe_vs_al.png')
plt.close()

# 2. 质量效率曲线：SEU vs 屏蔽质量面密度 (g/cm^2)
density_Al = 2.70   # g/cm^3
density_HDPE = 0.94 # g/cm^3
mass_range = np.linspace(0, 50, 11)  # 0 到 50 g/cm^2
al_mass_rates = []
hdpe_mass_rates = []
for m in mass_range:
    t_al = (m / density_Al) * 10   # g/cm2 → mm
    t_hd = (m / density_HDPE) * 10
    up_al, _ = run_simulation(NUM_PROTONS, layers=[("Aluminum", t_al)])
    up_hd, _ = run_simulation(NUM_PROTONS, layers=[("HDPE", t_hd)])
    al_mass_rates.append(up_al / NUM_PROTONS)
    hdpe_mass_rates.append(up_hd / NUM_PROTONS)

plt.figure()
plt.plot(mass_range, al_mass_rates, 'o-', label='Aluminum')
plt.plot(mass_range, hdpe_mass_rates, 's--', label='HDPE')
plt.xlabel('Shield Mass Areal Density (g/cm²)')
plt.ylabel('SEU Probability per Proton')
plt.title('SEU Rate vs. Shielding Mass (Al vs. HDPE)')
plt.legend()
plt.grid(True)
plt.savefig('results/mass_vs_seu.png')
plt.close()
