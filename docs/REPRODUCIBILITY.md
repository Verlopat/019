# Reproducibility checklist

Record before a full run:

- Python/Rust/Solidity/Circom/snarkjs versions
- OS and hardware
- repository commit
- experiment configuration hash
- random seeds
- credential dataset hash
- sanctions snapshot hash/root
- circuit hash and proving-key hash when using real Groth16
- deployed Ethereum contract addresses and chain ID
- Solana program ID and cluster
- transaction hashes/signatures
- gas used/gas price/block
- compute units/fee/slot
- raw result file hash

The Python simulation keeps paired seeds and workloads identical across methods. Full E1 is 20 seeds × 10,000 swaps per method; other experiments follow the matrices in configs/experiments.yaml.
