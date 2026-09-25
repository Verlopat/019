# Security invariants

1. Invalid ZK proof cannot authorize release.
2. Expired/revoked credentials cannot authorize release.
3. Proofs are bound to swap ID, policy hash and data roots, preventing replay across swaps/policies.
4. No arbitration quorum means no release; the safe outcome is timeout/refund.
5. Threshold certificates are independently verified by the receiving chain.
6. Audit records contain commitments, not raw identity.
7. Atomicity is violated only if exactly one chain releases.

The threat model permits provider faults, Byzantine attestors/arbitrators, message delay, malformed proofs, replay attempts and dispute spam. It assumes cryptographic primitives, issuer signatures and finalized chain history are not broken.
