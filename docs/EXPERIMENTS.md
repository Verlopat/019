# Experimental protocol

All major experiments use paired workloads. The same seed generates the same credentials, swaps, policy, and fault schedule for every compared method.

## E1
10,000 swaps/method/seed, 20 seeds. Measure AVI, refund correctness and state-machine violations.

## E2
Fault rates 0–50%. Compare B1, B2 and B4. Measure USR, SCR, arbitration trigger rate, refunds and latency.

## E3
Committee sizes 3/5/7/9 and attestor counts 3/5/7. Measure arbitration latency, vote/communication overhead, gas/CU and AVR.

## E4
Byzantine fractions 0–40%, slash rates 5/10/25/50%. Compare empirical collusion success with the binomial threshold model.

## E5
Run the Circom circuit at increasing Merkle depth and policy complexity. Record proof generation time, verification time, proof size, Ethereum gas and Solana CU. The Python reference values are simulation-only.

## E6
Compare B0/B1/B3/B4. Count publicly emitted sensitive attributes and verify that audit commitments match off-chain records.

For every condition report mean, median, SD, 95% bootstrap CI, P95, P99 and effect size. Use paired permutation tests; McNemar's test is reserved for paired binary outcomes. Apply Benjamini-Hochberg correction when testing multiple configurations.

The measurement clock uses t0 swap creation, t1 proof submission, t2 compliance acceptance, t3/t4 chain locks, t5/t6 claims and t7 final settlement.
