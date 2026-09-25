class EthereumAdapter:
 name="ethereum"
 def estimate_gas(self,operation): return {"create":85000,"lock":90000,"claim":65000,"refund":52000,"verify":145000,"arbitrate":180000}.get(operation,100000)
 def record(self,receipt): return {"chain":"ethereum","tx_hash":receipt.get("tx_hash","simulated"),"gas_used":receipt.get("gas_used",self.estimate_gas(receipt.get("operation","create"))),"status":receipt.get("status",1)}
