import time
from sdhtlc.core import Swap,SwapState,Decision,canonical_hash

class SDHTLC:
 def __init__(self,chain): self.chain=chain
 def compliance_gate(self,swap,decision):
  if decision==Decision.PASS: swap.compliance=decision; swap.state=SwapState.LOCKED; swap.event("LOCK",chain=self.chain)
  else: swap.compliance=decision; swap.state=SwapState.REJECTED; swap.event("REJECT",reason=decision.value)
 def claim(self,swap,secret):
  if swap.state not in (SwapState.LOCKED,SwapState.READY_TO_CLAIM): return False
  if canonical_hash(secret)!=swap.secret_hash or time.time()>swap.claim_deadline: return False
  swap.state=SwapState.RELEASED; swap.event("RELEASE",chain=self.chain)
  if self.chain==swap.chain_a: swap.release_a=True
  else: swap.release_b=True
  return True
 def refund(self,swap):
  if time.time()<swap.claim_deadline and swap.state!=SwapState.REJECTED: return False
  if self.chain==swap.chain_a: swap.refund_a=True
  else: swap.refund_b=True
  swap.state=SwapState.REFUNDED; swap.event("REFUND",chain=self.chain); return True
