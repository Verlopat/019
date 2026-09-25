# Proof-Aware Machine Learning for On-Chain Decision Systems

Research prototype implementing the three sequential objectives from the project synopsis:

1. Objective 1 — Cost–fidelity characterisation: a factorial benchmark varies proving backend, quantisation and activation strategy and records proving-time estimates, memory, proof size, verification gas, constraints and accuracy loss.
2. Objective 2 — Proof-aware co-design: a small architecture search uses the measured cost structure to jointly select hidden width, precision, activation and circuit backend under a constraint budget.
3. Objective 3 — Adversarial validation: boundary-oriented perturbations are generated and a conservative certified gate fails closed when the model/circuit approximation margin cannot establish decision stability.

## Important research-status note

This repository is a reproducible research prototype, not a claim of a production zk-SNARK implementation. The proving backends currently use transparent cost models and deterministic proof commitments so the complete experiment runs with ordinary Python and no paid service. A real Groth16/Plonk/Halo2 backend can be attached later behind the same circuit interface; its measurements should replace, rather than be mixed with, the simulator measurements.

The commitment produced by the prototype is a cryptographic artifact for experiment traceability. It is not a zero-knowledge proof.

## Run

Ubuntu/Linux:

    git clone https://github.com/Verlopat/019.git
    cd 019
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python3 Main.py

Every execution creates a new directory:

    outputs/test1/
    outputs/test2/
    outputs/test3/

Each run contains:

- manifest.json — complete configuration, metrics and selected design
- objective1_factorial.csv — factorial benchmark
- objective2_codesign_candidates.csv — co-design search space
- objective3_boundary_attacks.csv — adversarial boundary results

## Tests

    python3 -m unittest discover -s tests -v

## Configuration

Copy .env.example to .env and change values if required. The default configuration is intentionally small enough for a normal laptop.

## Reproducibility

Every manifest records the random seed, Python version, platform, model size, experimental parameters and elapsed runtime. The output directory is never reused.

## Scientific interpretation

The benchmark deliberately keeps the cost model explicit. The five primary cost quantities are:

- prover time
- peak prover memory
- proof size
- verification gas estimate
- accuracy loss relative to the floating-point baseline

The adversarial stage reports decision flips and the proportion of inputs rejected by the fail-closed stability gate.

These outputs are intended to support figures and tables in a research paper; they should not be presented as measurements of a specific deployed proving system until a real proving backend is connected.
