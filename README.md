# Quantum Simulation of Battery Electrolyte Salts

**Published in Advanced Quantum Technologies**  
DOI: [10.1002/qute.202500871](https://doi.org/10.1002/qute.202500871)

---

## What this repository contains

This is the code and data repository for our study on applying quantum computing
algorithms to battery electrolyte molecules. We study four salts — **LiPF₆, NaPF₆,
LiFSI, and NaFSI** — using:

- **VQE + UCCSD** ansatz for ground-state energies and dissociation curves
- **VQE–qEOM** for excited-state energies (S₁–S₃)
- **SQD** (Sample-based Quantum Diagonalization) on IBM Quantum hardware
- **CASCI** classical benchmarks via PySCF

All quantum simulations use [Qiskit](https://qiskit.org/) and
[qiskit-nature](https://qiskit-community.github.io/qiskit-nature/).
SQD calculations use [ffsim](https://github.com/qiskit-community/ffsim)
and IBM Quantum Runtime.

---

## Reproduce the figures

All paper figures can be reproduced from precomputed data — no quantum hardware needed.

```bash
git clone https://github.com/<your-username>/AQT_electrolyte.git
cd AQT_electrolyte
conda env create -f environment.yml   # recommended
conda activate aqt-electrolyte
python check_env.py                   # verify setup — fix any errors shown
python run_all.py                     # reproduce all figures
```

Output is written to `results/figures/`.  
To reproduce a single figure:

```bash
python run_all.py --fig dissociation   # Fig: dissociation curves
python run_all.py --fig excited        # Fig: excitation energy levels
python run_all.py --fig basis          # Fig: NaPF6 basis-set convergence
python run_all.py --fig sqd            # verify SQD figure outputs
```

---

## Paper figures

| Figure | File | Description |
|--------|------|-------------|
| Fig. 1 | `workflow_1.jpg` | Quantum simulation workflow |
| Fig. 2 | `active_space_1.jpg` | Active-space orbital selection |
| Fig. 3 | `selected_active_space_all.jpg` | Active spaces for all four salts |
| Fig. 4 | `qubit_reduction_new.jpg` | Ground-state energy vs. qubit count |
| Fig. 5 | `basis_set_testing_final.jpg` | NaPF₆ basis-set convergence |
| Fig. 6 | `vqe_anstz_optimizations.jpg` | VQE ansatz comparison (LiPF₆) |
| Fig. 7 | `dissociatoin_relative_energy.jpg` | Dissociation curves (all four salts) |
| Fig. 8 | `energy_deviation_disso.jpg` | Energy deviation from exact diagonalisation |
| Fig. 9 | `excitation_levels_electrolytes.jpg` | Excited-state energies from VQE–qEOM |
| SQD | `*_sqd_convergence_plot.jpg` | SQD convergence for each salt |

All figures are in `results/figures/`. The LaTeX source is in `paper/revised_main.tex`.

---

## Repository structure

```
AQT_electrolyte/
├── README.md
├── requirements.txt          # pip-installable dependencies
├── config.yaml               # all parameters used in the paper
├── run_all.py                # reproduce all figures in one command
│
├── data/raw/
│   ├── dissociation_curves/  # HF, VQE, CASCI energies at cc-pVTZ (.dat)
│   └── basis_convergence/    # NaPF6 energies across basis sets (.csv)
│
├── reproduce/                # one script per figure group
│   ├── figure_dissociation_curves.py
│   ├── figure_excited_states.py
│   ├── figure_basis_convergence.py
│   ├── figure_qubit_vs_energy.py
│   └── figure_sqd_convergence.py
│
├── src/utils/                # shared I/O, plotting, and constants
│
├── notebooks/                # full analysis notebooks (VQE, SQD per salt)
│
├── scripts/
│   └── casci_benchmark.py    # PySCF CASCI benchmark (heavy computation)
│
├── results/figures/          # all paper figures
└── paper/                    # revised_main.tex + figure files
```

---

## Notebooks

The `notebooks/` directory contains the full calculation notebooks for each salt:

| Notebook | Contents |
|----------|----------|
| `NaPF6_salt.ipynb` | VQE convergence, dissociation, basis-set study |
| `NaPF6_new.ipynb` | Extended NaPF₆ analysis with GPU support |
| `Li_salt.ipynb` | LiPF₆ VQE, ansatz comparison, excitations |
| `LiPF6_new.ipynb` | Extended LiPF₆ dissociation and orbital spectra |
| `NaFSI_salt.ipynb` | NaFSI VQE–FCI comparison, dissociation |
| `LiFSI_salt.ipynb` | LiFSI VQE–FCI comparison, orbital energies |
| `NaPF6_SQD_ffsim_qiskit.ipynb` | SQD convergence — NaPF₆ |
| `LiPF6_SQD_ffsim_qiskit.ipynb` | SQD convergence — LiPF₆ |
| `NaFSI_SQD_ffsim_qiskit.ipynb` | SQD convergence — NaFSI |
| `LiFSI_SQD_ffsim_qiskit.ipynb` | SQD convergence — LiFSI |

> SQD notebooks require an IBM Quantum account and GPU access to re-run.

---

## Installation

**Recommended — conda (most reliable):**

```bash
conda env create -f environment.yml
conda activate aqt-electrolyte
```

**Alternative — pip:**

```bash
pip install -r requirements.txt
```

**Check your environment before running anything:**

```bash
python check_env.py
```

This prints a clear pass/fail for every dependency and data file. Run it first if you hit any error.

---

## Troubleshooting

**`ImportError: cannot import name 'VQE' from 'qiskit_algorithms'`**  
→ Qiskit version mismatch. Use the conda environment: `conda env create -f environment.yml`

**`ModuleNotFoundError: No module named 'qiskit_nature'`**  
→ Run `pip install qiskit-nature==0.7.2` or use the conda environment above.

**`ModuleNotFoundError: No module named 'ffsim'`**  
→ ffsim is only needed for the SQD notebooks, not for `run_all.py`. Install with `pip install ffsim`. Requires a C++ compiler (`apt install build-essential` on Linux, Xcode on Mac).

**`FileNotFoundError: data/raw/...`**  
→ Run scripts from the repository root, not from inside a subdirectory.  
→ Check `python check_env.py` to see which files are missing.

**`SyntaxError` on `list[str]` or `X | Y` type hints**  
→ You are using Python < 3.10. Upgrade to Python 3.10 or later.

**SQD notebooks fail with IBM Quantum authentication error**  
→ SQD requires an IBM Quantum account. Set your token:  
```python
from qiskit_ibm_runtime import QiskitRuntimeService
QiskitRuntimeService.save_account(channel="ibm_quantum", token="YOUR_TOKEN")
```

**`figure_qubit_vs_energy.py` raises FileNotFoundError**  
→ `qubit_optimization_data.dat` is not included in this repository.
This file contains raw qubit-sweep results. The final paper figure (`qubit_reduction_new.jpg`) is already in `results/figures/`.

---

## Citation

If you use this code or data, please cite:

```bibtex
@article{hossain2025electrolyte,
  title   = {Quantum Simulation of Battery Electrolyte Salts Using
             Variational Quantum Algorithms and Sample-Based Quantum Diagonalization},
  journal = {Advanced Quantum Technologies},
  year    = {2025},
  doi     = {10.1002/qute.202500871}
}
```
