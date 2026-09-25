class SolanaAdapter:
 name="solana"
 def estimate_cu(self,operation): return {"create":35000,"lock":42000,"claim":30000,"refund":25000,"verify":95000,"arbitrate":110000}.get(operation,50000)
 def record(self,receipt): return {"chain":"solana","signature":receipt.get("signature","simulated"),"compute_units":receipt.get("compute_units",self.estimate_cu(receipt.get("operation","create"))),"status":receipt.get("status",1)}
