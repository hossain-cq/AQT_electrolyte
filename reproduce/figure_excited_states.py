"""
Reproduce excited-state energy level diagram (VQE–qEOM results).

Excitation energies are precomputed values embedded directly; no data file
is required (values are reported as a table in the paper).
Saves output to results/figures/excitation_levels_colored.jpg.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from src.utils.constants import SALT_DISPLAY
from src.utils.plotting import apply_publication_style, save_figure
from src.utils.io import results_path

apply_publication_style()

# Excitation energies (eV) from VQE–qEOM: S1, S2, S3 for each salt
EXCITATION_DATA: dict[str, list[float]] = {
    "LiPF6": [13.18, 13.19, 13.19],
    "NaPF6": [12.40, 12.41, 12.41],
    "LiFSI": [8.79,  8.80,  10.16],
    "NaFSI": [8.36,  8.37,   9.61],
}

COLORS: dict[str, str] = {
    "LiPF6": "#1f77b4",
    "NaPF6": "#2ca02c",
    "LiFSI": "#d62728",
    "NaFSI": "#ff7f0e",
}

plt.rcParams.update({
    "figure.dpi": 600,
    "savefig.dpi": 600,
    "font.size": 12,
    "axes.labelsize": 14,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "axes.linewidth": 1.0,
})

molecules     = list(EXCITATION_DATA.keys())
x_positions   = list(range(len(molecules)))
half_width    = 0.35
label_offset  = 0.25
label_dx      = [-0.18, 0.0, 0.18]

fig, ax = plt.subplots(figsize=(6.6, 4.3))

for i, mol in enumerate(molecules):
    c = COLORS[mol]
    for j, energy in enumerate(EXCITATION_DATA[mol]):
        ax.hlines(energy, i - half_width, i + half_width, linewidth=2.2, color=c)
        ax.text(
            i + label_dx[j % len(label_dx)],
            energy - label_offset,
            f"S{j+1}",
            ha="center", va="top", fontsize=10, color=c,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85),
        )

ax.set_xticks(x_positions, [SALT_DISPLAY[m] for m in molecules])
ax.set_ylabel("Excitation Energy (eV)")
ax.set_ylim(0, 15)
ax.set_xlim(-0.5, len(molecules) - 0.5)
ax.tick_params(direction="out", length=4, width=0.8)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)

legend_handles = [
    Line2D([0], [0], color=COLORS[m], lw=3, label=SALT_DISPLAY[m])
    for m in molecules
]
ax.legend(handles=legend_handles, frameon=False, ncol=4,
          loc="upper center", bbox_to_anchor=(0.5, 1.08))

fig.tight_layout()
save_figure(fig, results_path("figures", "excitation_levels_colored.jpg"))
plt.close(fig)
print("Done.")
