"""
run_all.py — Reproduce all paper figures from precomputed data.

Usage:
    python run_all.py              # run all figures
    python run_all.py --fig 2      # run a specific figure group

This script ONLY reads existing processed data from data/ and writes
figure files to results/figures/.  It does NOT trigger heavy VQE,
SQD, or DFT computations.

Heavy-computation scripts (casci_benchmark.py, graphene_bandstructure.py,
and the SQD notebooks) are excluded by design.
"""

import argparse
import importlib
import sys
import traceback
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(_ROOT))

# ── Figure pipeline (ordered by paper figure number) ─────────────────────
FIGURE_SCRIPTS: list[dict] = [
    {
        "id": "dissociation",
        "label": "Dissociation curves (LiFSI, LiPF6, NaPF6)",
        "module": "reproduce.figure_dissociation_curves",
    },
    {
        "id": "excited",
        "label": "Excited-state energy levels (VQE–qEOM)",
        "module": "reproduce.figure_excited_states",
    },
    {
        "id": "qubit",
        "label": "Relative energy vs. number of qubits",
        "module": "reproduce.figure_qubit_vs_energy",
        "optional": True,   # data file may be absent
    },
    {
        "id": "basis",
        "label": "NaPF6 basis-set convergence + dissociation (Figure 5)",
        "module": "reproduce.figure_basis_convergence",
    },
    {
        "id": "sqd",
        "label": "SQD convergence figures (verify pre-generated outputs)",
        "module": "reproduce.figure_sqd_convergence",
    },
]


def run_figure(entry: dict) -> bool:
    label    = entry["label"]
    module   = entry["module"]
    optional = entry.get("optional", False)

    print(f"\n{'─'*60}")
    print(f"  {label}")
    print(f"{'─'*60}")
    try:
        mod = importlib.import_module(module)
        # Modules execute at import time; nothing further needed.
        _ = mod
        print("  [OK]")
        return True
    except FileNotFoundError as exc:
        if optional:
            print(f"  [SKIPPED] Missing data: {exc}")
            return True
        print(f"  [ERROR] {exc}")
        return False
    except Exception:
        print(f"  [ERROR]")
        traceback.print_exc()
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reproduce paper figures from precomputed data."
    )
    parser.add_argument(
        "--fig",
        metavar="ID",
        help="Run only the figure with this id (dissociation|excited|qubit|basis|sqd).",
    )
    args = parser.parse_args()

    targets = (
        [e for e in FIGURE_SCRIPTS if e["id"] == args.fig]
        if args.fig
        else FIGURE_SCRIPTS
    )

    if not targets:
        print(f"Unknown figure id '{args.fig}'. "
              f"Available: {[e['id'] for e in FIGURE_SCRIPTS]}")
        sys.exit(1)

    results = [run_figure(e) for e in targets]

    print(f"\n{'='*60}")
    ok  = sum(results)
    tot = len(results)
    print(f"  {ok}/{tot} figure groups completed successfully.")
    if ok == tot:
        print("  All outputs written to results/figures/")
    print(f"{'='*60}\n")

    if not all(results):
        sys.exit(1)


if __name__ == "__main__":
    main()
