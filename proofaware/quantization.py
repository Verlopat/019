from __future__ import annotations

import numpy as np


def quantize(x: np.ndarray, bits: int) -> tuple[np.ndarray, float]:
    if bits < 2 or bits > 16:
        raise ValueError("bits must be between 2 and 16")
    qmax = 2 ** (bits - 1) - 1
    scale = max(float(np.max(np.abs(x))), 1e-9) / qmax
    return np.clip(np.rint(x / scale), -qmax, qmax).astype(np.int64), scale


def dequantize(q: np.ndarray, scale: float) -> np.ndarray:
    return q.astype(float) * scale


def quantized_inference(model, x: np.ndarray, bits: int, activation: str) -> np.ndarray:
    qw1, s1 = quantize(model.w1, bits)
    qb1, sb1 = quantize(model.b1, bits)
    qw2, s2 = quantize(model.w2, bits)
    qb2, sb2 = quantize(model.b2, bits)
    z = x @ dequantize(qw1, s1) + dequantize(qb1, sb1)
    if activation == "poly_relu":
        h = 0.5 * (z + z * np.tanh(z))
    elif activation == "piecewise":
        h = np.where(z <= -1, 0.0, np.where(z >= 1, z, 0.5 * (z + z * z)))
    elif activation == "square":
        h = z * z
    else:
        h = np.maximum(z, 0)
    return (h @ dequantize(qw2, s2) + dequantize(qb2, sb2)).reshape(-1)


def fixed_point_rescale(x: np.ndarray, bits: int) -> tuple[np.ndarray, float]:
    return quantize(x, bits)
