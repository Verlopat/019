from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass
class TinyMLP:
    n_features: int
    hidden: int
    seed: int = 42

    def __post_init__(self) -> None:
        rng = np.random.default_rng(self.seed)
        self.w1 = rng.normal(0, 0.35, (self.n_features, self.hidden))
        self.b1 = np.zeros(self.hidden)
        self.w2 = rng.normal(0, 0.35, (self.hidden, 1))
        self.b2 = np.zeros(1)

    def logits(self, x: np.ndarray, activation: str = "relu") -> np.ndarray:
        z = x @ self.w1 + self.b1
        h = apply_activation(z, activation)
        return (h @ self.w2 + self.b2).reshape(-1)

    def predict(self, x: np.ndarray, activation: str = "relu") -> np.ndarray:
        return (self.logits(x, activation) >= 0).astype(int)

    def parameter_count(self) -> int:
        return int(self.w1.size + self.b1.size + self.w2.size + self.b2.size)

    def copy(self) -> "TinyMLP":
        out = TinyMLP(self.n_features, self.hidden, self.seed)
        out.w1 = self.w1.copy()
        out.b1 = self.b1.copy()
        out.w2 = self.w2.copy()
        out.b2 = self.b2.copy()
        return out

    def fit(self, x: np.ndarray, y: np.ndarray, epochs: int = 120, lr: float = 0.05) -> float:
        y2 = y.astype(float)
        for _ in range(epochs):
            z = x @ self.w1 + self.b1
            h = np.maximum(z, 0)
            logits = (h @ self.w2 + self.b2).reshape(-1)
            p = 1.0 / (1.0 + np.exp(-np.clip(logits, -40, 40)))
            dz2 = (p - y2)[:, None] / len(x)
            dw2 = h.T @ dz2
            db2 = dz2.sum(axis=0)
            dh = dz2 @ self.w2.T
            dz1 = dh * (z > 0)
            dw1 = x.T @ dz1
            db1 = dz1.sum(axis=0)
            self.w2 -= lr * dw2
            self.b2 -= lr * db2
            self.w1 -= lr * dw1
            self.b1 -= lr * db1
        pred = self.predict(x)
        return float(np.mean(pred == y))


def apply_activation(x: np.ndarray, name: str) -> np.ndarray:
    if name == "relu":
        return np.maximum(x, 0)
    if name == "square":
        return x * x
    if name == "poly_relu":
        return 0.5 * (x + x * np.tanh(x))
    if name == "piecewise":
        return np.where(x <= -1, 0.0, np.where(x >= 1, x, 0.5 * (x + x * x)))
    raise ValueError(f"unknown activation: {name}")


def make_dataset(n_samples: int, n_features: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    x = rng.normal(size=(n_samples, n_features))
    true_w = rng.normal(size=n_features)
    score = x @ true_w + 0.35 * rng.normal(size=n_samples)
    y = (score >= np.median(score)).astype(int)
    return x, y
