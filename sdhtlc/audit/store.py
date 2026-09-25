import hashlib,json,sqlite3
from pathlib import Path

class AuditStore:
 def __init__(self,path="audit/audit.db"):
  Path(path).parent.mkdir(parents=True,exist_ok=True); self.db=sqlite3.connect(path); self.db.execute("CREATE TABLE IF NOT EXISTS audit(audit_id TEXT PRIMARY KEY,swap_id TEXT,policy_hash TEXT,proof_hash TEXT,attestation_root TEXT,arbitration_id TEXT,verdict TEXT,chain TEXT,block_ref TEXT,timestamp REAL,commitment TEXT)"); self.db.commit()
 def record(self,row):
  commitment=hashlib.sha256(json.dumps(row,sort_keys=True,default=str).encode()).hexdigest(); row=dict(row,commitment=commitment)
  self.db.execute("INSERT OR REPLACE INTO audit VALUES(?,?,?,?,?,?,?,?,?,?,?)",(row["audit_id"],row["swap_id"],row["policy_hash"],row["proof_hash"],row["attestation_root"],row.get("arbitration_id"),row["verdict"],row["chain"],row.get("block_ref","simulated"),row["timestamp"],commitment)); self.db.commit(); return commitment
 def verify(self,row,commitment): return hashlib.sha256(json.dumps(row,sort_keys=True,default=str).encode()).hexdigest()==commitment
