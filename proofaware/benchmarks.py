from __future__ import annotations

from itertools import product
import numpy as np
import pandas as pd

from .circuit import CircuitSpec, simulate_proof
from .quantization import quantized_inference


BACKENDS = ("native_float", "int8_poly", "finite_field", "lookup_relu")
BITS = (4, 8)
ACTIVATIONS = ("relu", "poly_relu", "square", "piecewise")


def run_factorial(model, x: np.ndarray, y: np.ndarray) -> pd.DataFrame:
    baseline = model.predict(x, "relu")
    rows = []
    for backend, bits, activation in product(BACKENDS, BITS, ACTIVATIONS):
        spec = CircuitSpec(backend, bits, activation)
        proof = simulate_proof(model, x, spec)
        if backend == "int8_poly":
            logits = quantized_inference(model, x, bits, activation)
            pred = (logits >= 0).astype(int)
        else:
            pred = model.predict(x, activation)
        accuracy = float(np.mean(pred == y))
        baseline_accuracy = float(np.mean(baseline == y))
        rows.append({
            "backend": backend,
            "quantization_bits": bits,
            "activation": activation,
            "accuracy": accuracy,
            "baseline_accuracy": baseline_accuracy,
            "accuracy_loss": baseline_accuracy - accuracy,
            **{k: v for k, v in proof.items() if k != "proof_commitment"},
        })
    return pd.DataFrame(rows)


def fit_cost_model(df: pd.DataFrame) -> dict:
    work = df["constraints"].to_numpy(float)
    nonlin = df["nonlinear_ops"].to_numpy(float)
    y = np.log1p(df["prover_time_s"].to_numpy(float))
    X = np.column_stack([np.ones(len(df)), np.log1p(work), np.log1p(nonlin)])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ coef
    rmse = float(np.sqrt(np.mean((pred - y) ** 2)))
    return {
        "intercept": float(coef[0]),
        "log_constraints": float(coef[1]),
        "log_nonlinear_ops": float(coef[2]),
        "log_rmse": rmse,
        "r_squared": float(1 - np.sum((y - pred) ** 2) / max(np.sum((y - y.mean()) ** 2), 1e-12)),
    }
