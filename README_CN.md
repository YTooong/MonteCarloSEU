
### 📄 中文（README\_CN.md）



项目：MonteCarloSEU – 辐射诱发单粒子翻转的蒙特卡罗模拟（扩展支持 HDPE 屏蔽）

使用说明：克隆仓库并安装所需依赖后，可运行模拟脚本生成结果图表。例如：

```bash
git clone https://github.com/youruser/MonteCarLoSEU.git
cd MonteCarLoSEU
pip install -r requirements.txt  # 安装依赖库
python plot_results.py
python plot_results_composite.py
````

默认情况下，`plot_results.py` 会将生成的图表输出至 `results/` 目录，包括 `hdpe_vs_al.png`、`mass_vs_seu.png`（纯材料比较），而 `plot_results_composite.py` 会输出 `composite_curve.png` 和 `combined_curve.png`（组合材料比较）图像。

运行后，这些图像将保存至 `results/` 文件夹中。你可以根据需要调整脚本中的参数（如事件数 `NUM_PROTONS`、屏蔽厚度范围 `thickness_range`）来探索不同场景。默认使用简化的质子能谱（Φ ∝ E^–2）。若使用自定义谱（如 CREME-MC 提供的谱），请将光谱数据 CSV 文件（如 `creme_spectrum.csv`）放入仓库根目录，并修改代码：

```python
energies, cdf = load_creme_csv('creme_spectrum.csv')
# 然后在运行模拟时传入 use_creme=True, creme_data=(energies, cdf)
```

这样即可将源谱切换为您提供的分布。屏蔽配置可通过 `layers` 参数进行调整。例如，若模拟 5 mm 铝 + 10 mm HDPE 的双层屏蔽，可在 `run_simulation` 或 `run_composite_simulation` 中设置：

```python
layers = [("Aluminum", 5), ("HDPE", 10)]
```

代码已注释清晰，并支持多层屏蔽输入。

---

### 关于 CREME-MC 能谱的说明：

如上所述，若希望采用 CREME-MC 太空质子能谱，请将 `use_creme` 设置为 `True`，并提供供 `load_creme_csv` 读取的 `creme_data`（能量和对应累积分布）。请确保 CSV 文件包含两列：

* 能量（单位 MeV）
* 通量或累积概率

`load_creme_csv` 函数将对其排序并归一化为标准 CDF。

---

### 注意单位和参数说明：

请确保单位统一：

* 能量用 MeV 表示
* 屏蔽厚度单位为 mm
* μ（用于屏蔽系数）为 mm⁻¹
* LET 单位为 MeV·cm²/mg

`chip.py` 文件中预置了 PSTAR 能量损耗表（Stopping Power）。你也可以在该文件中扩展能量点或添加其他材料。材料的衰减系数定义在 `chip.py` 中（当前包括铝和 HDPE）；你也可以将其他材料添加到 `ATTENUATION` 字典中。

---

### 性能建议：

对于大规模模拟（如 N > 10⁶），建议启用 Numba JIT 加速（`simulate.py` 中已默认启用）。

---

### 引用指南：

若将该框架用于学术或工程用途，请引用所使用的物理数据来源：

* NIST PSTAR (2021)
* NIST 材料数据库（无日期）
* PDG (2017)
* Zhang 等人 (2024)

例如：

> “我们使用了一套基于 \[您的姓名] 开发的蒙特卡罗 SEU 模拟框架，结合了 NIST 的质子阻止本领数据和现代 SEU 参数，用于评估屏蔽效果。”

本项目中的代码与文档已按 APA 风格标注了所有参考文献，方便读者查阅。

---

请参考英文版 `README.md` 和上述说明，以再现实验结果并根据自身需求调整模拟。例如，您可以测试不同的屏蔽材料、器件参数或辐射能谱，从而将本框架应用于特定航天电子可靠性评估中。


