"""
Reproduce dissociation curve figures (HF / VQE-UCCSD / CASCI) at cc-pVTZ level.

Paper figures: dissociation of LiFSI, LiPF6, and NaPF6 ion pairs.
Reads precomputed data from data/raw/dissociation_curves/.
Saves outputs to results/figures/.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt
from src.utils.io import load_dissociation_dat, results_path
from src.utils.plotting import apply_publication_style, style_axes, save_figure

apply_publication_style()

_SALTS = {
    "LiFSI": {
        "dat": "lifsI_ccpvtz_dissociation.dat",
        "xlabel": "Li–N Distance (Å)",
        "out": "LiFSI_dissociation_VQE_vs_CASCI_UCCSD_ccpVTZ.jpg",
    },
    "LiPF6": {
        "dat": "lipf6_ccpvtz_dissociation.dat",
        "xlabel": "Li–F Distance (Å)",
        "out": "LiPF6_dissociation_VQE_vs_CASCI_UCCSD_ccpVTZ.jpg",
    },
    "NaPF6": {
        "dat": "napf6_ccpvtz_dissociation.dat",
        "xlabel": "Na–F Distance (Å)",
        "out": "NaPF6_dissociation_VQE_vs_CASCI_UCCSD_ccpVTZ.jpg",
    },
}


def plot_dissociation(salt: str, cfg: dict) -> None:
    distances, hf, vqe, casci = load_dissociation_dat(cfg["dat"])

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.plot(distances, casci, color="green",  linestyle="-",  marker="s",
            markersize=6, linewidth=2.5, label="CASCI (Exact)")
    ax.plot(distances, vqe,   color="red",    linestyle="-",  marker="o",
            markersize=6, linewidth=2,   label="VQE (UCCSD)")
    ax.plot(distances, hf,    color="black",  linestyle="--", linewidth=2,
            label="Hartree–Fock")

    ax.set_xlabel(cfg["xlabel"], fontsize=14, fontweight="bold")
    ax.set_ylabel("Total Energy (Ha)", fontsize=14, fontweight="bold")
    ax.tick_params(labelsize=12)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontweight("bold")
    ax.legend(fontsize=12, frameon=False)
    style_axes(ax)

    fig.tight_layout()
    save_figure(fig, results_path("figures", cfg["out"]))
    plt.close(fig)


if __name__ == "__main__":
    for salt, cfg in _SALTS.items():
        print(f"Plotting {salt} dissociation curve …")
        plot_dissociation(salt, cfg)
    print("Done.")
