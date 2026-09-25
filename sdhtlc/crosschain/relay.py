from sdhtlc.core import canonical_hash

def make_certificate(verdict,swap_id,policy_hash):
 return {"swap_id":swap_id,"policy_hash":policy_hash,"verdict":verdict.decision.value,"committee":verdict.committee,"signatures":verdict.signatures,"certificate":verdict.certificate}

def verify_certificate(cert,required=1):
 return bool(cert.get("swap_id") and cert.get("policy_hash") and len(cert.get("signatures",[]))>=required and cert.get("certificate"))
