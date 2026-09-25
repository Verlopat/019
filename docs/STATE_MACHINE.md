# SD-HTLC state machine

CREATED → COMPLIANCE_PENDING.

PASS → LOCKED → READY_TO_CLAIM → RELEASED.

HARD FAIL → REJECTED → REFUND.

CONFLICT/INDETERMINATE → ARBITRATION.

ARBITRATION PASS → LOCKED.

ARBITRATION FAIL → REJECTED.

NO QUORUM → no release; timeout → REFUND.

The settlement identity is bound to swap ID, hashlock, chain ID, policy hash and compliance/data-root commitments.
