# -*- coding: utf-8 -*-
"""Download the portable T1/T2 model artifacts from Hugging Face."""
from __future__ import annotations

import os
from pathlib import Path

from huggingface_hub import snapshot_download

repo = os.environ.get("ACCORD_HF_REPO", "YOUR_HF_USER/accord-sl-v11")
target = Path(__file__).resolve().parent / "models"
target.mkdir(parents=True, exist_ok=True)
snapshot_download(
    repo_id=repo,
    repo_type="model",
    local_dir=str(target),
    allow_patterns=[
        "t1_locked_layers.joblib",
        "t1_input_contract.json",
        "t2_locked_layers.joblib",
        "input_contract.json",
        "t2_feature_dictionary.csv",
        "t1_experts/*",
        "experts/*",
    ],
)
print(f"downloaded {repo} -> {target}")
