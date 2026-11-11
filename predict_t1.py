#!/usr/bin/env python
"""ACCORD-SL T1 Blood3 scorer (research use only).

Model: v11 locked T1 ensemble (five experts, equal weights, mean-logit fusion,
Platt calibration). Operating threshold: 0.134.
"""
from pathlib import Path
import argparse
import joblib
import numpy as np
import pandas as pd

FEATURES = ["age", "嗜碱细胞百分比", "丙氨酸氨基转移酶", "血白蛋白"]
DEFAULT_BUNDLE = Path(__file__).resolve().parent / "models" / "t1_blood3_bundle_v11_final.joblib"


def score(df: pd.DataFrame, bundle_path: Path = DEFAULT_BUNDLE) -> pd.DataFrame:
    bundle = joblib.load(bundle_path)
    missing = [c for c in FEATURES if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    X = df[FEATURES].apply(pd.to_numeric, errors="coerce")
    probs = np.column_stack([m.predict_proba(X)[:, 1] for m in bundle["models"].values()])
    eps = 1e-6
    logits = np.log(np.clip(probs, eps, 1 - eps) / (1 - np.clip(probs, eps, 1 - eps)))
    fused = np.average(logits, axis=1, weights=bundle["weights"])
    p = bundle["platt"].predict_proba(fused.reshape(-1, 1))[:, 1]
    threshold = float(bundle["threshold"])
    out = df.copy()
    out["t1_probability"] = p
    out["t1_positive"] = (p >= threshold).astype(int)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--bundle", default=str(DEFAULT_BUNDLE))
    a = ap.parse_args()
    df = pd.read_csv(a.input)
    score(df, Path(a.bundle)).to_csv(a.out, index=False)
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
