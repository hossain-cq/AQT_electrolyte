"""
Unified PySCF CASCI benchmark for FSI- and PF6- anions.

SKIPPED (heavy computation): This script performs quantum chemistry
calculations that require PySCF and ~24 CPU threads. Pre-computed
results are stored in data/raw/dissociation_curves/:
  - FSI_anion_CASCI.dat
  - PF6_anion_CASCI.dat

Usage:
    python scripts/casci_benchmark.py --anion fsi   [--basis cc-pVDZ]
    python scripts/casci_benchmark.py --anion pf6   [--basis cc-pVDZ]
    python scripts/casci_benchmark.py --anion all
"""

import argparse
import os
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]

# ── Geometries ─────────────────────────────────────────────────────────────

GEOMETRIES: dict[str, dict] = {
    "fsi": {
        "name": "FSI-",
        "charge": -1,
        "spin": 0,
        "ncas_orb": 5,
        "ncas_elec": 6,
        "output": "FSI_anion_CASCI.dat",
        "geom": """
N   0.0000   0.0000   0.0000
S   0.0000   1.4406  -0.4595
O   1.2581   1.8123  -1.0595
O  -1.2581   1.8123  -1.0595
F   0.0000   2.2257   1.0569
S   0.0000  -1.4406  -0.4595
O   1.2581  -1.8123  -1.0595
O  -1.2581  -1.8123  -1.0595
F   0.0000  -2.2257   1.0569
""",
    },
    "pf6": {
        "name": "PF6-",
        "charge": -1,
        "spin": 0,
        "ncas_orb": 5,
        "ncas_elec": 6,
        "output": "PF6_anion_CASCI.dat",
        "geom": """
P   0.0000   0.0000   0.0000
F   0.0000   0.0000   1.5790
F   0.0000   0.0000  -1.5790
F   0.0000   1.5790   0.0000
F   0.0000  -1.5790   0.0000
F   1.5790   0.0000   0.0000
F  -1.5790   0.0000   0.0000
""",
    },
}


def run_casci(anion_key: str, basis: str = "cc-pVDZ", n_threads: int = 24) -> None:
    """Run HF + CASCI for the specified anion and write results to data/raw/."""
    from pyscf import gto, scf, mcscf  # imported lazily — heavy dependency

    os.environ["OMP_NUM_THREADS"]    = str(n_threads)
    os.environ["MKL_NUM_THREADS"]    = str(n_threads)
    os.environ["OPENBLAS_NUM_THREADS"] = str(n_threads)

    cfg = GEOMETRIES[anion_key]
    output_path = _ROOT / "data" / "raw" / "dissociation_curves" / cfg["output"]

    mol = gto.Mole()
    mol.atom   = cfg["geom"]
    mol.basis  = basis
    mol.charge = cfg["charge"]
    mol.spin   = cfg["spin"]
    mol.unit   = "Angstrom"
    mol.build()

    mf = scf.RHF(mol)
    mf.kernel()

    cas = mcscf.CASCI(mf, cfg["ncas_orb"], cfg["ncas_elec"])
    cas.kernel()

    with open(output_path, "w") as f:
        f.write(f"# {cfg['name']} CASCI benchmark\n")
        f.write(f"# Basis: {basis}\n")
        f.write(f"HF_energy(Ha)     = {mf.e_tot:.10f}\n")
        f.write(f"CASCI_energy(Ha)  = {cas.e_tot:.10f}\n")

    print(f"{cfg['name']} — HF: {mf.e_tot:.8f} Ha  CASCI: {cas.e_tot:.8f} Ha")
    print(f"Written to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run PySCF CASCI benchmark.")
    parser.add_argument("--anion",   choices=["fsi", "pf6", "all"], default="all")
    parser.add_argument("--basis",   default="cc-pVDZ")
    parser.add_argument("--threads", type=int, default=24)
    args = parser.parse_args()

    targets = list(GEOMETRIES.keys()) if args.anion == "all" else [args.anion]
    for key in targets:
        run_casci(key, basis=args.basis, n_threads=args.threads)
