"""Data loading helpers that resolve paths relative to the project root."""

from pathlib import Path
import csv
import numpy as np

_PROJECT_ROOT = Path(__file__).resolve().parents[2]


def data_path(*parts: str) -> Path:
    """Return absolute path inside data/."""
    return _PROJECT_ROOT / "data" / Path(*parts)


def results_path(*parts: str) -> Path:
    """Return absolute path inside results/."""
    return _PROJECT_ROOT / "results" / Path(*parts)


def load_dissociation_dat(filename: str) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Load a dissociation .dat file with columns: distance, HF, VQE, CASCI (all in Ha)."""
    path = data_path("raw", "dissociation_curves", filename)
    data = np.loadtxt(path)
    return data[:, 0], data[:, 1], data[:, 2], data[:, 3]


def load_basis_convergence_csv(filename: str) -> tuple[list[str], np.ndarray]:
    """Load fixed-geometry basis-convergence CSV → (basis_labels, energies_Ha)."""
    path = data_path("raw", "basis_convergence", filename)
    labels, energies = [], []
    with open(path) as f:
        for row in csv.DictReader(f):
            labels.append(row["basis"])
            energies.append(float(row["energy_Ha"]))
    return labels, np.array(energies)


def load_dissociation_csv(filename: str):
    """Load relative-dissociation CSV → structured numpy array with named columns."""
    path = data_path("raw", "basis_convergence", filename)
    return np.genfromtxt(path, delimiter=",", names=True)
