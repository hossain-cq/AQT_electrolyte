"""Shared matplotlib style and figure-saving helpers."""

from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt


PUBLICATION_RCPARAMS: dict = {
    "font.family": "serif",
    "font.size": 14,
    "axes.labelsize": 14,
    "axes.titlesize": 14,
    "legend.fontsize": 12,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "figure.dpi": 600,
    "savefig.dpi": 600,
    "lines.linewidth": 2.5,
    "lines.markersize": 7,
}

MARKERS = ["o", "s", "^", "D"]
COLORS  = ["#1f77b4", "#2ca02c", "#d62728", "#9467bd"]


def apply_publication_style() -> None:
    mpl.rcParams.update(PUBLICATION_RCPARAMS)


def style_axes(ax: plt.Axes, spine_lw: float = 1.5) -> None:
    """Apply uniform spine and tick styling to an axes."""
    for spine in ax.spines.values():
        spine.set_linewidth(spine_lw)
    ax.grid(True, linestyle="--", linewidth=1, alpha=0.6)
    ax.tick_params(labelsize=12, width=spine_lw)


def save_figure(fig: plt.Figure, output_path: Path, dpi: int = 600) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
    print(f"Saved: {output_path}")
