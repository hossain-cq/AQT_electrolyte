"""
Reproduce Figure 5: NaPF6 basis-set convergence + dissociation curves.

Generates three output files:
  - Figure5_side_by_side.png    (panels a + b combined)
  - Figure5a_basis_convergence.png
  - Figure5b_dissociation_curves.png

Reads from data/raw/basis_convergence/.
Saves to results/figures/.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

from src.utils.io import load_basis_convergence_csv, load_dissociation_csv, results_path
from src.utils.plotting import (
    apply_publication_style,
    style_axes,
    save_figure,
    MARKERS,
    COLORS,
)

apply_publication_style()

# ── Load data ──────────────────────────────────────────────────────────────
basis_labels, fixed_energies = load_basis_convergence_csv(
    "NaPF6_fixed_geometry_energies.csv"
)
reference_energy        = fixed_energies[-1]           # cc-pVTZ is last row
relative_energies_mHa   = (fixed_energies - reference_energy) * 1000.0

diss = load_dissociation_csv("NaPF6_dissociation_relative_ccpVTZ.csv")
distances  = diss["distance_A"]
basis_sets = [n for n in diss.dtype.names if n != "distance_A"]

# ── Side-by-side figure ────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5), constrained_layout=True)

ax1.bar(basis_labels, relative_energies_mHa,
        color="#f4c77a", edgecolor="black", linewidth=1.2)
ax1.set_xlabel("Basis set", fontweight="bold")
ax1.set_ylabel("Relative energy ΔE (mHa)", fontweight="bold")
ax1.set_title("(a) Basis-set convergence (fixed geometry)", fontweight="bold")

for i, basis in enumerate(basis_sets):
    ax2.plot(distances, diss[basis],
             marker=MARKERS[i % 4], color=COLORS[i % 4], label=basis)
ax2.set_xlabel("Na–F distance (Å)", fontweight="bold")
ax2.set_ylabel("Relative energy ΔE (Ha)", fontweight="bold")
ax2.set_title("(b) Dissociation curves (relative to cc-pVTZ)", fontweight="bold")
ax2.legend(prop=FontProperties(weight="bold"), frameon=False)

for ax in (ax1, ax2):
    style_axes(ax)

save_figure(fig, results_path("figures", "Figure5_side_by_side.png"))
plt.close(fig)

# ── Panel (a) standalone ──────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 5))
ax.bar(basis_labels, relative_energies_mHa,
       color="#f4c77a", edgecolor="black", linewidth=1.2)
ax.set_xlabel("Basis set", fontweight="bold")
ax.set_ylabel("Relative energy ΔE (mHa)", fontweight="bold")
style_axes(ax)
fig.tight_layout()
save_figure(fig, results_path("figures", "Figure5a_basis_convergence.png"))
plt.close(fig)

# ── Panel (b) standalone ──────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 5))
for i, basis in enumerate(basis_sets):
    ax.plot(distances, diss[basis],
            marker=MARKERS[i % 4], color=COLORS[i % 4], label=basis)
ax.set_xlabel("Na–F distance (Å)", fontweight="bold")
ax.set_ylabel("Relative energy ΔE (Ha)", fontweight="bold")
ax.legend(prop=FontProperties(weight="bold", size=12), frameon=False)
style_axes(ax)
fig.tight_layout()
save_figure(fig, results_path("figures", "Figure5b_dissociation_curves.png"))
plt.close(fig)

print("Done.")
