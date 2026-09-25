from dataclasses import dataclass,field
from enum import Enum
import hashlib,json,time,secrets

class Decision(str,Enum): PASS="PASS"; FAIL="FAIL"; INDETERMINATE="INDETERMINATE"
class SwapState(str,Enum):
 CREATED="CREATED"; COMPLIANCE_PENDING="COMPLIANCE_PENDING"; LOCKED="LOCKED"; REJECTED="REJECTED"
 ARBITRATION="ARBITRATION"; READY_TO_CLAIM="READY_TO_CLAIM"; RELEASED="RELEASED"; REFUNDABLE="REFUNDABLE"; REFUNDED="REFUNDED"

def canonical_hash(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()

@dataclass(frozen=True)
class Policy:
 version:str="1"; jurisdiction:str="EEA"; minimum_kyc_level:int=2; max_risk_score:int=70; require_sanctions_clear:bool=True
 def digest(self): return canonical_hash(self.__dict__)

@dataclass(frozen=True)
class Credential:
 credential_id:str; issuer_id:str; jurisdiction:str; kyc_level:int; issued_at:int; expires_at:int; revoked:bool; risk_score:int; wallet_binding:str; subject_secret:str
 def digest(self): return canonical_hash(self.__dict__)

@dataclass(frozen=True)
class ZKProof:
 proof_id:str; swap_id:str; policy_hash:str; credential_root:str; sanctions_root:str; wallet_commitment:str; nonce:str; valid:bool; proof_size:int; generation_ms:float
 def public_inputs(self): return {"swap_id":self.swap_id,"policy_hash":self.policy_hash,"credential_root":self.credential_root,"sanctions_root":self.sanctions_root,"wallet_commitment":self.wallet_commitment,"nonce":self.nonce}

@dataclass
class Attestation:
 provider_id:str; decision:Decision; policy_hash:str; root_hash:str; timestamp:float; evidence_hash:str; signature:str

@dataclass
class Swap:
 swap_id:str; secret_hash:str; chain_a:str; chain_b:str; amount:float; created_at:float; compliance_deadline:float; claim_deadline:float
 state:SwapState=SwapState.CREATED; compliance:Decision=Decision.INDETERMINATE; arbitration_id:str|None=None
 release_a:bool=False; release_b:bool=False; refund_a:bool=False; refund_b:bool=False; events:list=field(default_factory=list)
 def event(self,name,**data): self.events.append({"name":name,"ts":time.time(),**data})
 @property
 def atomicity_violation(self): return (self.release_a != self.release_b) and (self.release_a or self.release_b)

def make_secret():
 s=secrets.token_hex(32); return s,hashlib.sha256(s.encode()).hexdigest()
