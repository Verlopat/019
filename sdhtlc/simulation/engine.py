import time,random
from sdhtlc.core import *
from sdhtlc.compliance.policy import evaluate_credential
from sdhtlc.zk.proof import prove_compliance,verify_proof
from sdhtlc.compliance.attestors import AttestorNetwork
from sdhtlc.arbitration.committee import Member,select_committee
from sdhtlc.arbitration.faults import assign_malicious
from sdhtlc.arbitration.voting import resolve
from sdhtlc.crosschain.htlc import SDHTLC
from sdhtlc.crosschain.relay import make_certificate,verify_certificate

def run_swap(method,row,credential,policy,seed,committee_size=5,fault_rate=0.0,byzantine=.0,slash=.1):
 now=1750000000; secret,sh=make_secret(); swap=Swap(row["swap_id"],sh,"ethereum","solana",row["amount"],time.time(),time.time()+60,time.time()+300); swap.state=SwapState.COMPLIANCE_PENDING
 root=credential.digest(); sanctions_root="synthetic-sanctions-root"
 proof=prove_compliance(swap.swap_id,credential,policy,root,sanctions_root,row["sanctions_clear"],now)
 truth=evaluate_credential(credential,policy,now,row["sanctions_clear"])
 if method=="B0": decision=Decision.PASS; att=[]; verdict=None
 elif method=="B1": decision=Decision.PASS if truth else Decision.FAIL; att=[]; verdict=None
 else:
  att=AttestorNetwork(5,seed).attest(proof,credential,policy,now,row["sanctions_clear"],fault_rate)
  vals=[a.decision for a in att]
  if method=="B2": decision=Decision.PASS if vals.count(Decision.PASS)>=3 else Decision.FAIL; verdict=None
  elif method=="B3": decision=Decision.PASS if verify_proof(proof,swap.swap_id,policy,root,sanctions_root) else Decision.FAIL; verdict=None
  else:
   if not verify_proof(proof,swap.swap_id,policy,root,sanctions_root): decision=Decision.FAIL; verdict=None
   elif vals.count(Decision.PASS)==5: decision=Decision.PASS; verdict=None
   elif vals.count(Decision.FAIL)==5: decision=Decision.FAIL; verdict=None
   elif method=="B5": decision=Decision.FAIL; verdict=None
   else:
    swap.state=SwapState.ARBITRATION; members=[Member(f"M{i}",1000.0) for i in range(20)]; assign_malicious(members,byzantine,seed); committee=select_committee(members,committee_size,seed,swap.swap_id); verdict=resolve(swap.swap_id,committee,att,truth,slash_rate=slash); decision=verdict.decision
    if verdict.quorum: swap.arbitration_id=verdict.dispute_id
    else: decision=Decision.FAIL
 SDHTLC("ethereum").compliance_gate(swap,decision)
 if decision==Decision.PASS:
  swap.state=SwapState.READY_TO_CLAIM; SDHTLC("ethereum").claim(swap,secret); swap.release_b=True; swap.release_a=True
 else:
  swap.refund_a=True; swap.refund_b=True; swap.state=SwapState.REFUNDED
 return {"swap_id":swap.swap_id,"method":method,"ground_truth":truth,"decision":decision.value,"atomicity_violation":int(swap.atomicity_violation),"unauthorized_release":int(decision=="PASS" and not truth),"completed":int(decision=="PASS" and truth),"refunded":int(decision!="PASS"),"proof_ms":proof.generation_ms,"arb_ms":getattr(verdict,"latency_ms",0.0) if verdict else 0.0,"proof_size":proof.proof_size,"committee_size":committee_size if verdict else 0,"gas":85000+(180000 if verdict else 0),"sol_cu":35000+(110000 if verdict else 0),"disclosure_count":0}
