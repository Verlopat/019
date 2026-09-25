# Baselines

B0 Vanilla HTLC: no compliance gate.

B1 HTLC + centralized compliance: one deterministic compliance authority.

B2 HTLC + multi-attestor: distributed attestors, no arbitration.

B3 HTLC + ZK compliance: cryptographic compliance gate, no arbitration.

B4 Full proposed SD-HTLC: ZK + five attestors + threshold arbitration + audit commitment.

B5 Full system with arbitration disabled: conflict safely aborts/refunds.

zkPACT and Chainlink ACE are literature comparators, not reproduced experimental baselines unless equivalent source implementations and conditions are available.
