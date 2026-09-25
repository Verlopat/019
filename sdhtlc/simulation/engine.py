import time
from sdhtlc.core import *
from sdhtlc.compliance.policy import evaluate_credential
from sdhtlc.zk.proof import prove_compliance,verify_proof
from sdhtlc.compliance.attestors import AttestorNetwork
from sdhtlc.arbitration.committee import Member,select_committee
from sdhtlc.arbitration.faults import assign_malicious
from sdhtlc.arbitration.voting import resolve
from sdhtlc.crosschain.htlc import SDHTLC

def run_swap(method,row,credential,policy,seed,committee_size=5,fault_rate=0.0,byzantine=0.0,slash=.10,attestor_count=5):
 now=1750000000; secret,sh=make_secret()
 swap=Swap(row["swap_id"],sh,"ethereum","solana",row["amount"],time.time(),time.time()+60,time.time()+300); swap.state=SwapState.COMPLIANCE_PENDING
 root=credential.digest(); sanctions_root="synthetic-sanctions-root"
 proof=prove_compliance(swap.swap_id,credential,policy,root,sanctions_root,row["sanctions_clear"],now)
 truth=evaluate_credential(credential,policy,now,row["sanctions_clear"])
 verdict=None
 if method=="B0": decision=Decision.PASS; att=[]
 elif method=="B1": decision=Decision.PASS if truth else Decision.FAIL; att=[]
 else:
  att=AttestorNetwork(attestor_count,seed).attest(proof,credential,policy,now,row["sanctions_clear"],fault_rate)
  vals=[a.decision for a in att]
  if method=="B2": decision=Decision.PASS if vals.count(Decision.PASS)>=((attestor_count*2+2)//3) else Decision.FAIL
  elif method=="B3": decision=Decision.PASS if verify_proof(proof,swap.swap_id,policy,root,sanctions_root) else Decision.FAIL
  else:
   if not verify_proof(proof,swap.swap_id,policy,root,sanctions_root): decision=Decision.FAIL
   elif vals.count(Decision.PASS)==attestor_count: decision=Decision.PASS
   elif vals.count(Decision.FAIL)==attestor_count: decision=Decision.FAIL
   elif method=="B5": decision=Decision.FAIL
   else:
    swap.state=SwapState.ARBITRATION
    members=[Member(f"M{i}",1000.0) for i in range(20)]; assign_malicious(members,byzantine,seed)
    committee=select_committee(members,committee_size,seed,swap.swap_id)
    verdict=resolve(swap.swap_id,committee,att,truth,slash_rate=slash)
    decision=verdict.decision if verdict.quorum else Decision.FAIL
    if verdict.quorum: swap.arbitration_id=verdict.dispute_id
 SDHTLC("ethereum").compliance_gate(swap,decision)
 if decision==Decision.PASS:
  swap.state=SwapState.READY_TO_CLAIM; SDHTLC("ethereum").claim(swap,secret); swap.release_b=True; swap.release_a=True
 else:
  swap.refund_a=True; swap.refund_b=True; swap.state=SwapState.REFUNDED
 return {"swap_id":swap.swap_id,"method":method,"ground_truth":truth,"decision":decision.value,
 "atomicity_violation":int(swap.atomicity_violation),"unauthorized_release":int(decision==Decision.PASS and not truth),
 "completed":int(decision==Decision.PASS and truth),"refunded":int(decision!=Decision.PASS),
 "proof_ms":proof.generation_ms,"arb_ms":getattr(verdict,"latency_ms",0.0) if verdict else 0.0,
 "proof_size":proof.proof_size,"committee_size":committee_size if verdict else 0,
 "attestor_count":attestor_count,"gas":85000+(180000 if verdict else 0),
 "sol_cu":35000+(110000 if verdict else 0),"disclosure_count":0}
