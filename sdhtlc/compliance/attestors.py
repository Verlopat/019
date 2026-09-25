import random,time
from sdhtlc.core import Attestation,Decision,canonical_hash
from .policy import evaluate_credential

class AttestorNetwork:
 def __init__(self,n=5,seed=1): self.n=n; self.seed=seed
 def attest(self,proof,credential,policy,now,sanctions_clear=True,fault_rate=0.0):
  r=random.Random(self.seed+hash(proof.swap_id)); truth=evaluate_credential(credential,policy,now,sanctions_clear); out=[]
  for i in range(self.n):
   if not proof.valid: d=Decision.FAIL
   elif r.random()<fault_rate: d=Decision.INDETERMINATE if r.random()<.5 else (Decision.FAIL if truth else Decision.PASS)
   else: d=Decision.PASS if truth else Decision.FAIL
   payload={"provider":f"CA{i+1}","result":d.value,"proof":proof.proof_id,"policy":policy.digest()}
   h=canonical_hash(payload); out.append(Attestation(f"CA{i+1}",d,policy.digest(),h,time.time(),h,"sig:"+h))
  return out
