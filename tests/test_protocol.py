import unittest
from sdhtlc.core import *
from sdhtlc.compliance.credentials import generate_credentials
from sdhtlc.compliance.policy import evaluate_credential
from sdhtlc.zk.proof import prove_compliance,verify_proof
from sdhtlc.arbitration.committee import Member,select_committee
from sdhtlc.arbitration.voting import resolve

class ProtocolTests(unittest.TestCase):
 def setUp(self):
  self.c=generate_credentials(20,7)[0]; self.p=Policy()
 def test_invalid_proof_never_verifies(self):
  z=prove_compliance("s",self.c,self.p,self.c.digest(),"root",False)
  self.assertFalse(verify_proof(z,"s",self.p,self.c.digest(),"root"))
 def test_replay_binding(self):
  z=prove_compliance("s",self.c,self.p,self.c.digest(),"root",True)
  self.assertFalse(verify_proof(z,"different",self.p,self.c.digest(),"root"))
 def test_no_quorum_is_not_pass(self):
  ms=[Member(str(i),100) for i in range(3)]
  v=resolve("d",ms,[],True,threshold_ratio=1.0)
  self.assertFalse(v.quorum); self.assertEqual(v.decision,Decision.INDETERMINATE)
 def test_threshold_verdict(self):
  ms=[Member(str(i),100) for i in range(5)]
  from sdhtlc.core import Attestation
  a=[Attestation(str(i),Decision.PASS,self.p.digest(),"r",0,"e","s") for i in range(5)]
  v=resolve("d",ms,a,True)
  self.assertEqual(v.decision,Decision.PASS); self.assertTrue(v.quorum)

if __name__=="__main__": unittest.main()
