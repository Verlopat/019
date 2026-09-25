from sdhtlc.core import Credential,Policy

def evaluate_credential(c,p,now,sanctions_clear=True):
 return c.jurisdiction==p.jurisdiction and c.kyc_level>=p.minimum_kyc_level and c.expires_at>now and not c.revoked and c.risk_score<=p.max_risk_score and (sanctions_clear or not p.require_sanctions_clear)
