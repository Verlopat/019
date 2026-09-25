from dataclasses import dataclass
import time
from sdhtlc.core import Decision,canonical_hash

@dataclass
class Verdict:
 dispute_id:str; decision:Decision; quorum:bool; committee:list[str]; signatures:list[str]; slashed:list[str]; latency_ms:float
 @property
 def certificate(self): return canonical_hash({"id":self.dispute_id,"decision":self.decision.value,"committee":self.committee,"signatures":self.signatures})

def resolve(dispute_id,committee,attestations,ground_truth,threshold_ratio=2/3,slash_rate=.10):
 t=time.perf_counter(); votes=[]
 for m in committee:
  if m.malicious: vote=Decision.FAIL if ground_truth else Decision.PASS
  else:
   ps=sum(a.decision==Decision.PASS for a in attestations); fs=sum(a.decision==Decision.FAIL for a in attestations)
   vote=Decision.PASS if ps>=fs else Decision.FAIL
  votes.append(vote)
 need=max(1,int(len(committee)*threshold_ratio+0.999999)); cp=votes.count(Decision.PASS); cf=votes.count(Decision.FAIL)
 if max(cp,cf)<need: decision=Decision.INDETERMINATE; quorum=False
 else: decision=Decision.PASS if cp>cf else Decision.FAIL; quorum=True
 correct=Decision.PASS if ground_truth else Decision.FAIL; slashed=[]
 for m,v in zip(committee,votes):
  if v!=correct: m.stake*=1-slash_rate; slashed.append(m.member_id)
 sig=["sig:"+canonical_hash({"m":m.member_id,"v":v.value}) for m,v in zip(committee,votes)]
 return Verdict(dispute_id,decision,quorum,[m.member_id for m in committee],sig,slashed,(time.perf_counter()-t)*1000)
