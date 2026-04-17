"""
Reproduce Figure 4: relative energy vs. number of qubits for all four salts.

Input: data/raw/qubit_optimization_data.dat
  Columns: qubits, LiPF6(Ha), NaPF6(Ha), LiFSI(Ha), NaFSI(Ha)
  (header row skipped automatically)

Output: results/figures/Figure4_relative_energy_vs_qubits.jpg

NOTE: qubit_optimization_data.dat was not found in the original repository
(only the plotting script exists). If you have this file, place it at
data/raw/qubit_optimization_data.dat and re-run this script.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

from src.utils.io import data_path, results_path
from src.utils.plotting import apply_publication_style, style_axes, save_figure
from src.utils.constants import SALT_DISPLAY

apply_publication_style()

_DATA_FILE = data_path("raw", "qubit_optimization_data.dat")

if not _DATA_FILE.exists():
    raise FileNotFoundError(
        f"Missing data file: {_DATA_FILE}\n"
        "Place qubit_optimization_data.dat in data/raw/ to reproduce this figure."
    )

raw   = np.loadtxt(_DATA_FILE, skiprows=1)
qubits = raw[:, 0].astype(int)
salts  = ["LiPF6", "NaPF6", "LiFSI", "NaFSI"]

relative = {
    salt: (raw[:, i + 1] - raw[-1, i + 1]) * 1000   # mHa relative to max-qubit result
    for i, salt in enumerate(salts)
}

markers = ["o", "s", "^", "d"]

fig, ax = plt.subplots(figsize=(7, 5))
for (salt, rel_e), marker in zip(relative.items(), markers):
    ax.plot(qubits, rel_e, marker=marker, linewidth=2, label=SALT_DISPLAY[salt])

ax.set_xlabel("Number of qubits", fontsize=14, fontweight="bold")
ax.set_ylabel("Relative energy ΔE (mHa)", fontsize=14, fontweight="bold")
for lbl in ax.get_xticklabels() + ax.get_yticklabels():
    lbl.set_fontweight("bold")
ax.legend(prop=FontProperties(weight="bold", size=12), frameon=False)
style_axes(ax)
fig.tight_layout()

save_figure(fig, results_path("figures", "Figure4_relative_energy_vs_qubits.jpg"))
plt.close(fig)
print("Done.")
