# Selective-Disclosure Compliance Arbitration for Cross-Chain Atomic Swaps

Research prototype implementing the specification in `idea(1).txt`.

Architecture: `VC → ZK compliance proof → multi-attestor compliance → PASS/FAIL/CONFLICT → stake-backed threshold arbitration → Ethereum/Solana SD-HTLC → privacy-preserving audit`.

The Python layer is an executable reference implementation and experiment controller. Circom, Solidity and Anchor/Rust sources define the real-chain integration points. Simulated measurements are explicitly labelled and are never presented as production-chain measurements.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m sdhtlc.run_experiment --experiment smoke
python3 -m sdhtlc.run_experiment --experiment all --seeds 20 --swaps-per-seed 1000
```

## Required evaluation

E1 correctness/atomicity; E2 compliance-fault tolerance; E3 arbitration scalability; E4 Byzantine/collusion resistance; E5 ZK overhead; E6 privacy/auditability.

Baselines: B0 Vanilla HTLC, B1 centralized compliance, B2 multi-attestor, B3 ZK compliance, B4 full SD-HTLC, B5 arbitration-disabled ablation.

The full configuration records 20 independent seeds and 1,000+ paired swaps per condition. Every result row includes experiment, seed, method and configuration hash.

## Layout

```
sdhtlc/{compliance,zk,arbitration,crosschain,simulation,evaluation,audit}
circuits/
ethereum/
solana/
configs/
tests/
results/
docs/
```

## Scientific boundary

The reference ZK layer is deterministic and testable but is not itself a Groth16 proof. Install Circom/snarkjs and use `circuits/compliance.circom` for actual proof generation. Ethereum gas and Solana CU are estimates until local-chain runners collect real receipts/logs. The prototype is not legal-compliance certification.
