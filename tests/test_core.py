import tempfile
from pathlib import Path
import unittest

import numpy as np

from proofaware.circuit import commitment, verify_commitment
from proofaware.model import TinyMLP, make_dataset
from proofaware.runner import next_run_dir


class CoreTests(unittest.TestCase):
    def test_commitment_round_trip(self):
        payload = {"x": 1, "model": "demo"}
        c = commitment(payload)
        self.assertTrue(verify_commitment(c, payload))
        self.assertFalse(verify_commitment(c, {"x": 2, "model": "demo"}))

    def test_model_is_deterministic(self):
        x, y = make_dataset(30, 4, 7)
        a = TinyMLP(4, 3, 7)
        b = TinyMLP(4, 3, 7)
        a.fit(x, y, epochs=5, lr=0.05)
        b.fit(x, y, epochs=5, lr=0.05)
        np.testing.assert_allclose(a.w1, b.w1)

    def test_run_numbering(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.assertEqual(next_run_dir(root).name, "test1")
            self.assertEqual(next_run_dir(root).name, "test2")


if __name__ == "__main__":
    unittest.main()
