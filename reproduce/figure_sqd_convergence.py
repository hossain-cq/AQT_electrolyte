"""
SQD (Sample-based Quantum Diagonalization) convergence figures.

Pre-generated figures are already present in results/figures/:
  - LiFSI_sqd_convergence_plot.jpg
  - LiPF6_sqd_convergence_plot.jpg
  - NaFSI_sqd_convergence_plot.jpg
  - NaPF6_sqd_convergence_plot.jpg

These were produced by the SQD notebooks (see notebooks/ directory):
  NaPF6_SQD_ffsim_qiskit.ipynb, LiFSI_SQD_ffsim_qiskit.ipynb,
  LiPF6_SQD_ffsim_qiskit.ipynb, NaFSI_SQD_ffsim_qiskit.ipynb

SKIPPED (heavy computation): Re-running SQD calculations requires IBM Quantum
access (qiskit-ibm-runtime) and several hours of GPU/QPU time.
The saved figures in results/figures/ are the canonical outputs.

This script verifies those outputs exist and reports their status.
"""

from pathlib import Path

_ROOT    = Path(__file__).resolve().parents[1]
_FIGURES = _ROOT / "results" / "figures"

EXPECTED = [
    "LiFSI_sqd_convergence_plot.jpg",
    "LiPF6_sqd_convergence_plot.jpg",
    "NaFSI_sqd_convergence_plot.jpg",
    "NaPF6_sqd_convergence_plot.jpg",
]

if __name__ == "__main__":
    print("Checking SQD convergence figure outputs …")
    all_ok = True
    for fname in EXPECTED:
        p = _FIGURES / fname
        status = "OK" if p.exists() else "MISSING"
        if not p.exists():
            all_ok = False
        print(f"  [{status}] {p.relative_to(_ROOT)}")

    if all_ok:
        print("\nAll SQD figures present in results/figures/.")
    else:
        print("\nSome figures missing. Re-run the SQD notebooks to regenerate.")
    print("\nNOTE: SKIPPED (heavy computation) — IBM Quantum / GPU required.")
