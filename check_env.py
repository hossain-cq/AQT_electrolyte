"""
check_env.py — Run this first if you encounter any errors.

    python check_env.py

It checks Python version, required packages, and data files.
No computation is performed.
"""

import sys

REQUIRED_PYTHON = (3, 10)
PASS = "[  OK  ]"
FAIL = "[ FAIL ]"
WARN = "[ WARN ]"

errors = []
warnings = []

# ── 1. Python version ─────────────────────────────────────────────────────
print("\n── Python ───────────────────────────────────────────────")
v = sys.version_info
if v >= REQUIRED_PYTHON:
    print(f"{PASS} Python {v.major}.{v.minor}.{v.micro}")
else:
    msg = f"Python {v.major}.{v.minor} found — need >= {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]}"
    print(f"{FAIL} {msg}")
    errors.append(msg)

# ── 2. Core packages ──────────────────────────────────────────────────────
print("\n── Core packages ────────────────────────────────────────")

CORE = {
    "numpy":      "1.24",
    "matplotlib": "3.7",
    "scipy":      "1.11",
    "yaml":       "6.0",
}

for pkg, min_ver in CORE.items():
    try:
        mod = __import__(pkg)
        ver = getattr(mod, "__version__", "?")
        print(f"{PASS} {pkg}=={ver}")
    except ImportError:
        msg = f"{pkg} not installed (pip install {pkg})"
        print(f"{FAIL} {msg}")
        errors.append(msg)

# ── 3. Quantum packages ───────────────────────────────────────────────────
print("\n── Quantum packages ─────────────────────────────────────")

QUANTUM = {
    "qiskit":            ("qiskit", "1.0"),
    "qiskit_nature":     ("qiskit-nature", "0.7"),
    "qiskit_algorithms": ("qiskit-algorithms", "0.3"),
    "qiskit_aer":        ("qiskit-aer", "0.14"),
    "pyscf":             ("pyscf", "2.4"),
    "ffsim":             ("ffsim", "0.0.35"),
}

for mod_name, (pkg_name, min_ver) in QUANTUM.items():
    try:
        mod = __import__(mod_name)
        ver = getattr(mod, "__version__", "?")
        print(f"{PASS} {pkg_name}=={ver}")
    except ImportError:
        if mod_name == "ffsim":
            msg = f"ffsim not installed — needed only for SQD notebooks (pip install ffsim)"
            print(f"{WARN} {msg}")
            warnings.append(msg)
        else:
            msg = f"{pkg_name} not installed (pip install {pkg_name})"
            print(f"{FAIL} {msg}")
            errors.append(msg)

# ── 4. Qiskit API compatibility check ────────────────────────────────────
print("\n── Qiskit API compatibility ─────────────────────────────")
try:
    from qiskit_nature.second_q.drivers import PySCFDriver          # noqa: F401
    from qiskit_nature.second_q.mappers import JordanWignerMapper   # noqa: F401
    from qiskit_algorithms import VQE                               # noqa: F401
    print(f"{PASS} qiskit-nature second_q API available")
    print(f"{PASS} qiskit-algorithms VQE available")
except ImportError as e:
    msg = (
        f"Qiskit API mismatch: {e}\n"
        "         This usually means mismatched qiskit/qiskit-nature versions.\n"
        "         Fix: conda env create -f environment.yml"
    )
    print(f"{FAIL} {msg}")
    errors.append(str(e))

# ── 5. Data files ─────────────────────────────────────────────────────────
print("\n── Data files ───────────────────────────────────────────")
from pathlib import Path

ROOT = Path(__file__).parent
DATA_FILES = [
    "data/raw/dissociation_curves/lifsI_ccpvtz_dissociation.dat",
    "data/raw/dissociation_curves/lipf6_ccpvtz_dissociation.dat",
    "data/raw/dissociation_curves/napf6_ccpvtz_dissociation.dat",
    "data/raw/dissociation_curves/FSI_anion_CASCI.dat",
    "data/raw/dissociation_curves/PF6_anion_CASCI.dat",
    "data/raw/basis_convergence/NaPF6_fixed_geometry_energies.csv",
    "data/raw/basis_convergence/NaPF6_dissociation_relative_ccpVTZ.csv",
]
OPTIONAL_FILES = [
    "data/raw/qubit_optimization_data.dat",
]

for f in DATA_FILES:
    p = ROOT / f
    if p.exists():
        print(f"{PASS} {f}")
    else:
        msg = f"Missing required data file: {f}"
        print(f"{FAIL} {msg}")
        errors.append(msg)

for f in OPTIONAL_FILES:
    p = ROOT / f
    if p.exists():
        print(f"{PASS} {f}")
    else:
        print(f"{WARN} {f}  (optional — needed only for figure_qubit_vs_energy.py)")
        warnings.append(f"Optional file missing: {f}")

# ── Summary ───────────────────────────────────────────────────────────────
print("\n── Summary ──────────────────────────────────────────────")
if not errors and not warnings:
    print("  All checks passed. Run:  python run_all.py\n")
elif not errors:
    print(f"  {len(warnings)} warning(s), no errors. Core reproduction will work.")
    for w in warnings:
        print(f"    • {w}")
    print()
else:
    print(f"  {len(errors)} error(s) found — fix these before running:\n")
    for e in errors:
        print(f"    ✗ {e}")
    print()
    print("  Recommended fix:")
    print("    conda env create -f environment.yml")
    print("    conda activate aqt-electrolyte")
    print("    python check_env.py\n")
    sys.exit(1)
