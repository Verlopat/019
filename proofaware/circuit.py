from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import time
import numpy as np


@dataclass(frozen=True)
class CircuitSpec:
    backend: str
    quantization_bits: int
    activation: str
    field_bits: int = 254


FIELD = 2**61 - 1


def operation_profile(hidden: int, features: int, activation: str, backend: str) -> dict:
    linear = features * hidden + hidden
    output = hidden + 1
    nonlinear = hidden
    if activation == "square":
        nonlinear *= 1.0
    elif activation == "poly_relu":
        nonlinear *= 3.0
    elif activation == "piecewise":
        nonlinear *= 4.0
    else:
        nonlinear *= 2.0
    backend_factor = {
        "native_float": 0.15,
        "int8_poly": 0.45,
        "finite_field": 1.0,
        "lookup_relu": 0.72,
    }[backend]
    constraints = int((linear + output + nonlinear) * backend_factor * 10)
    return {
        "linear_ops": int(linear),
        "nonlinear_ops": int(nonlinear),
        "constraints": constraints,
        "total_arithmetic_ops": int(linear + output + nonlinear),
    }


def field_encode(values: np.ndarray, scale: int = 1000) -> np.ndarray:
    return np.mod(np.rint(values * scale).astype(object), FIELD).astype(object)


def commitment(payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def simulate_proof(model, x: np.ndarray, spec: CircuitSpec) -> dict:
    profile = operation_profile(model.hidden, model.n_features, spec.activation, spec.backend)
    start = time.perf_counter()
    logits = model.logits(x, spec.activation)
    trace_hash = hashlib.sha256(np.asarray(logits, dtype=np.float64).tobytes()).hexdigest()
    elapsed = time.perf_counter() - start
    proof_payload = {
        "backend": spec.backend,
        "bits": spec.quantization_bits,
        "activation": spec.activation,
        "trace_hash": trace_hash,
        "samples": len(x),
    }
    return {
        **profile,
        "proof_size_bytes": 192 + 32 * len(spec.activation) + spec.quantization_bits,
        "verification_gas_estimate": 85000 + 35 * profile["constraints"],
        "prover_time_s": max(elapsed * (1 + profile["constraints"] / 1000), 0.000001),
        "peak_memory_mb": 16 + profile["constraints"] * 0.004,
        "proof_commitment": commitment(proof_payload),
    }


def verify_commitment(commitment_value: str, payload: dict) -> bool:
    return commitment(payload) == commitment_value
