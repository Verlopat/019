from __future__ import annotations

from itertools import product
import numpy as np
import pandas as pd

from .circuit import operation_profile
from .quantization import quantized_inference


def search_architecture(base_model, x, y, budget: int) -> tuple[dict, pd.DataFrame]:
    rows = []
    for hidden, bits, activation, backend in product(
        (2, 4, 8, 12), (4, 8), ("relu", "poly_relu", "piecewise"), ("finite_field", "lookup_relu")
    ):
        m = base_model.__class__(base_model.n_features, hidden, base_model.seed)
        m.fit(x, y, epochs=60, lr=0.05)
        profile = operation_profile(hidden, m.n_features, activation, backend)
        if profile["constraints"] > budget:
            continue
        if backend == "finite_field":
            pred = m.predict(x, activation)
        else:
            pred = (quantized_inference(m, x, bits, activation) >= 0).astype(int)
        acc = float(np.mean(pred == y))
        objective = profile["constraints"] + 5000 * max(0.0, 0.80 - acc)
        rows.append({
            "hidden": hidden,
            "bits": bits,
            "activation": activation,
            "backend": backend,
            "accuracy": acc,
            "constraints": profile["constraints"],
            "objective": objective,
        })
    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("co-design budget rejected every candidate")
    chosen = df.sort_values(["objective", "constraints"]).iloc[0].to_dict()
    return chosen, df
