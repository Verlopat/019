from __future__ import annotations

import numpy as np
import pandas as pd


def certified_gate(model, x: np.ndarray, quantization_bits: int, threshold: float = 0.15) -> tuple[np.ndarray, np.ndarray]:
    logits = model.logits(x, "relu")
    bound = (2.0 ** (-quantization_bits)) * (1.0 + np.linalg.norm(model.w1, ord=2))
    margin = np.abs(logits)
    safe = margin > (bound + threshold)
    decision = (logits >= 0).astype(int)
    return decision, safe


def boundary_attacks(model, x: np.ndarray, n: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    ids = rng.choice(len(x), size=min(n, len(x)), replace=False)
    rows = []
    for idx in ids:
        xi = x[idx].copy()
        base = model.predict(xi[None, :])[0]
        direction = rng.normal(size=xi.shape)
        direction /= max(np.linalg.norm(direction), 1e-12)
        best = base
        best_eps = 0.0
        for eps in np.geomspace(1e-4, 0.8, 24):
            candidate = xi + eps * direction
            pred = model.predict(candidate[None, :])[0]
            if pred != base:
                best, best_eps = pred, float(eps)
                break
        rows.append({
            "sample": int(idx),
            "original_decision": int(base),
            "attacked_decision": int(best),
            "flip_found": bool(best != base),
            "epsilon": best_eps,
        })
    return pd.DataFrame(rows)


def evaluate_fail_closed(model, x: np.ndarray, bits: int) -> dict:
    decision, safe = certified_gate(model, x, bits)
    rejected = ~safe
    return {
        "samples": len(x),
        "safe_proof_rate": float(np.mean(safe)),
        "fail_closed_rate": float(np.mean(rejected)),
        "unsafe_decisions_blocked": int(np.sum(rejected)),
        "decision_count": int(np.sum(decision >= 0)),
    }
