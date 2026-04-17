"""Physical and unit-conversion constants used throughout the project."""

# CODATA 2018 value
HARTREE_TO_EV: float = 27.211386245988

HARTREE_TO_MILLIHARTREE: float = 1000.0

# Electrolyte salt labels used consistently across figures
SALT_LABELS: list[str] = ["LiPF6", "NaPF6", "LiFSI", "NaFSI"]

SALT_DISPLAY: dict[str, str] = {
    "LiPF6": r"LiPF$_6$",
    "NaPF6": r"NaPF$_6$",
    "LiFSI": "LiFSI",
    "NaFSI": "NaFSI",
}
