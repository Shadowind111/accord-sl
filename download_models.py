# -*- coding: utf-8 -*-
"""Download the portable T2 model artifacts from Hugging Face."""
from __future__ import annotations

import os
from pathlib import Path

from huggingface_hub import snapshot_download

repo = os.environ.get("T2_HF_REPO", "YOUR_HF_USER/accord-sl-t2-v11")
target = Path(__file__).resolve().parent / "models"
target.mkdir(parents=True, exist_ok=True)
snapshot_download(
    repo_id=repo,
    repo_type="model",
    local_dir=str(target),
    allow_patterns=[
        "t2_locked_layers.joblib",
        "input_contract.json",
        "t2_feature_dictionary.csv",
        "experts/ebm_ga2m_interpretable.joblib",
        "experts/random_forest_balanced.joblib",
        "experts/tabpfn_full_t2_bounded.joblib",
        "experts/tabdpt_full_t2_bounded.joblib",
        "experts/autogluon_stacked_ensemble_bounded.joblib",
    ],
)
print(f"downloaded {repo} -> {target}")
