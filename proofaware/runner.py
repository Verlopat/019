from __future__ import annotations

import json
import logging
import platform
import time
from pathlib import Path

import numpy as np

from .adversarial import boundary_attacks, evaluate_fail_closed
from .benchmarks import run_factorial, fit_cost_model
from .codesign import search_architecture
from .config import Config
from .model import TinyMLP, make_dataset


LOG = logging.getLogger("proofaware")


def next_run_dir(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    nums = []
    for p in root.glob("test*"):
        try:
            nums.append(int(p.name[4:]))
        except ValueError:
            pass
    path = root / f"test{max(nums, default=0) + 1}"
    path.mkdir()
    return path


def run(cfg: Config) -> Path:
    out = next_run_dir(Path("outputs"))
    start = time.perf_counter()
    np.random.seed(cfg.seed)

    x, y = make_dataset(cfg.n_samples, cfg.n_features, cfg.seed)
    split = int(0.75 * len(x))
    model = TinyMLP(cfg.n_features, 4, cfg.seed)
    train_acc = model.fit(x[:split], y[:split], cfg.epochs, cfg.learning_rate)
    test_acc = float(np.mean(model.predict(x[split:]) == y[split:]))

    benchmark_x = x[: min(cfg.benchmark_samples, len(x))]
    benchmark_y = y[: len(benchmark_x)]
    bench = run_factorial(model, benchmark_x, benchmark_y)
    bench.to_csv(out / "objective1_factorial.csv", index=False)
    cost_model = fit_cost_model(bench)

    chosen, candidates = search_architecture(model, x[:split], y[:split], cfg.co_design_budget)
    candidates.to_csv(out / "objective2_codesign_candidates.csv", index=False)

    attacks = boundary_attacks(model, x[split:], cfg.adversarial_samples, cfg.seed + 1)
    attacks.to_csv(out / "objective3_boundary_attacks.csv", index=False)
    gate = evaluate_fail_closed(model, x[split:], int(chosen["bits"]))

    manifest = {
        "project": "Proof-Aware Machine Learning for On-Chain Decision Systems",
        "run_directory": str(out),
        "seed": cfg.seed,
        "platform": platform.platform(),
        "python": platform.python_version(),
        "parameters": cfg.__dict__,
        "objective1": {
            "rows": len(bench),
            "cost_model": cost_model,
            "mean_accuracy_loss": float(bench["accuracy_loss"].mean()),
            "mean_constraints": float(bench["constraints"].mean()),
        },
        "objective2": {
            "selected_design": chosen,
            "candidate_count": len(candidates),
        },
        "objective3": {
            "attack_count": len(attacks),
            "decision_flip_rate": float(attacks["flip_found"].mean()),
            "fail_closed": gate,
        },
        "model": {
            "parameters": model.parameter_count(),
            "training_accuracy": train_acc,
            "holdout_accuracy": test_acc,
        },
        "elapsed_seconds": time.perf_counter() - start,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    LOG.info("Run complete: %s", out)
    return out
