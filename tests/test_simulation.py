import unittest
from sdhtlc.simulation.workload import generate_workload
from sdhtlc.simulation.engine import run_swap
from sdhtlc.compliance.credentials import generate_credentials
from sdhtlc.core import Policy

class SimulationTests(unittest.TestCase):
 def test_end_to_end_valid_and_invalid_paths(self):
  cs=generate_credentials(100,1); p=Policy()
  row=next(generate_workload(1,1)); r=run_swap("B4",row,cs[row["credential"]],p,1)
  self.assertIn(r["decision"],{"PASS","FAIL"})
  self.assertEqual(r["atomicity_violation"],0)
 def test_reproducible_workload(self):
  self.assertEqual(list(generate_workload(3,4)),list(generate_workload(3,4)))

if __name__=="__main__": unittest.main()
