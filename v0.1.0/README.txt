# TRIGA Dimensions-Based Model

A dimensions-based Monte Carlo model of a TRIGA research reactor developed using [OpenMC](https://openmc.org/).

This project aims to develop and progressively refine a computational model of a TRIGA-type research reactor, starting from individual fuel elements and progressing toward a complete core representation.

---

## Project Status

**Current version:** `v0.1.0`

**Status:** Initial core model / preliminary simulation

The current version implements a simplified TRIGA fuel element arrangement using a hexagonal lattice.

---

## Model Description

The model is based on the dimensions and material specifications used in the corresponding MCNP model.

### Fuel

- Fuel type: U-ZrH
- Uranium enrichment: 20%
- Fuel density: 8.26 g/cm³
- Fuel radius: 1.76 cm
- Fuel active height: 35.6 cm

### Cladding

- Material: Aluminum
- Cladding radius: 1.865 cm

### Reflector

- Material: Graphite
- Density: 1.76 g/cm³
- Graphite radius: 29.05 cm

### Moderator

- Material: Light Water
- Density: 1.0 g/cm³

### Core Geometry

- Lattice type: Hexagonal
- Lattice pitch: 5.0 cm
- Core modeled using a hexagonal fuel-element arrangement

---

## Simulation

The model is currently simulated using the eigenvalue method.

### Configuration

| Parameter | Value |
|---|---:|
| OpenMC | 0.15.3 |
| Run mode | Eigenvalue |
| Batches | 100 |
| Inactive batches | 10 |
| Particles/batch | 1000 |
| OpenMP threads | 6 |
| MPI processes | 1 |
| Temperature | 294 K |
| Nuclear data | ENDF/B-VIII.0 |

---

## Preliminary Results

For version `v0.1.0`:

| Quantity | Result |
|---|---:|
| k-effective (Collision) | 1.04288 ± 0.00209 |
| k-effective (Track-length) | 1.04223 ± 0.00256 |
| k-effective (Absorption) | 1.04464 ± 0.00153 |
| **Combined k-effective** | **1.04450 ± 0.00155** |
| Leakage Fraction | 0.22513 ± 0.00060 |

These results are preliminary and are intended for model development and verification. They should not be interpreted as validation against experimental reactor data.

---

## Computational Environment

The simulation was performed on:

- CPU: Intel Core i5-9400F
- CPU cores/threads: 6 / 6
- RAM: 16 GB DDR4 2400 MHz
- GPU: NVIDIA GeForce GTX 1660 SUPER 6 GB
- Storage: HDD
- Host operating system: Windows
- Linux environment: WSL2
- Linux distribution: Fedora 44
- Python: 3.13
- OpenMC: 0.15.3

### Performance

For the reported simulation:

| Parameter | Value |
|---|---:|
| Total elapsed time | 42.605 s |
| Initialization | 34.561 s |
| Cross-section reading | 30.091 s |
| Monte Carlo simulation | 8.036 s |
| Active calculation rate | ~62,021 particles/s |

The cross-section loading time is reported separately because it represents a significant portion of the total execution time.

---

## Repository Structure

```text
TRIGA-Dimensions-Based-Model/
│
├── README.md
│
└── v0.1.0/
    ├── triga_v0.1.0.py
    ├── results.txt
    └── output.txt
