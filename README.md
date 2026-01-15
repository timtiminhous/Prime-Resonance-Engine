# Prime Resonance Engine

**A specialized implementation of the Einstein Toolkit for Prime Resonance Singularity Sweeps.**

## Overview
This repository contains the source code, thorn configurations, and analysis scripts for the **Prime Resonance Engine**. It is built on top of the [Einstein Toolkit](https://einsteintoolkit.org) (Cactus Framework) and creates a reproducible scientific environment for testing high-precision numerical relativity coupled with custom number-theoretic resonance logic.

The core objective of this codebase is to provide a stable, containerized environment to run the `PrimeResonance_FullET.par` simulation and associated singularity verification scripts.

## Repository Structure

* **`/Cactus`**: The modified source code and Thorns for the Einstein Toolkit.
* **`Dockerfile`**: A complete Arch Linux-based build definition. It handles the complex dependency chain (OpenMPI, HDF5, GSL, BLAS, LAPACK) so the simulation environment is identical across machines.
* **`verify_30030.py`**: Verification logic for the Prime Resonance modulus (30030).
* **`check_zeta_singularity.py`**: Analysis script for Zeta function singularity detection.
* **`singularity_sweep.py`**: The primary sweep logic.
* **`PrimeResonance_FullET.par`**: The "Gold" parameter file for the full simulation run.

## 🚀 Quick Start (Docker)

To ensure reproducibility, it is highly recommended to run this engine within the provided Docker container. This bypasses all system-library conflicts.

### 1. Build the Image
```bash
docker build -t primeresonance-et:release-v1 .
