from __future__ import annotations

import os
from dataclasses import dataclass


def _int(name: str, default: int) -> int:
    return int(os.getenv(name, str(default)))


def _float(name: str, default: float) -> float:
    return float(os.getenv(name, str(default)))


@dataclass(frozen=True)
class Config:
    seed: int = _int("SEED", 42)
    n_samples: int = _int("N_SAMPLES", 240)
    n_features: int = _int("N_FEATURES", 8)
    n_classes: int = _int("N_CLASSES", 2)
    epochs: int = _int("EPOCHS", 120)
    learning_rate: float = _float("LEARNING_RATE", 0.05)
    benchmark_samples: int = _int("BENCHMARK_SAMPLES", 96)
    co_design_budget: int = _int("CO_DESIGN_BUDGET", 2500)
    adversarial_samples: int = _int("ADVERSARIAL_SAMPLES", 400)
