import hashlib,time
from sdhtlc.core import ZKProof

def prove_compliance(swap_id,c,p,credential_root,sanctions_root,sanctions_clear=True,now=1750000000):
 t=time.perf_counter(); valid=(c.jurisdiction==p.jurisdiction and c.kyc_level>=p.minimum_kyc_level and c.expires_at>now and not c.revoked and c.risk_score<=p.max_risk_score and (sanctions_clear or not p.require_sanctions_clear))
 nonce=hashlib.sha256(f"{swap_id}:{c.subject_secret}:{p.version}".encode()).hexdigest(); wc=hashlib.sha256((c.wallet_binding+nonce).encode()).hexdigest()
 pid=hashlib.sha256(f"groth16-reference:{swap_id}:{nonce}:{valid}".encode()).hexdigest()
 return ZKProof(pid,swap_id,p.digest(),credential_root,sanctions_root,wc,nonce,valid,192,max(.01,(time.perf_counter()-t)*1000))

def verify_proof(proof,swap_id,p,credential_root,sanctions_root):
 return proof.valid and proof.swap_id==swap_id and proof.policy_hash==p.digest() and proof.credential_root==credential_root and proof.sanctions_root==sanctions_root
