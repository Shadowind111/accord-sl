# T1/T2 ACCORD-SL research package

**Status:** research prototype. Not a medical device. Not for diagnosis, referral, treatment, or discharge decisions.

This package contains the T1-ACCORD-SL and T2-ACCORD-SL model cards, portable locked artifacts, Python scoring entry points, synthetic examples, a combined Gradio demonstration and a Docker template. T1 is a low-burden pre-screen; T2 is specialist-priority scoring with the five-expert ensemble (EBM, TabPFN, TabDPT, AutoGluon, random forest). Both tiers have been smoke-tested on synthetic data. A Docker CLI image for T2 (`../release_cli/`) has been built and tested. The combined Gradio app was tested locally.

## Contents

| File | Purpose |
|---|---|
| `MODEL_CARD.md` | Intended use, inputs, outputs, performance, limitations |
| `models/` | Portable T1/T2 locked layers, five expert artifacts per tier and input contracts |
| `predict_t1.py` | T1 scoring entry point (`--mode fast` or `--mode full`) |
| `predict_t2.py` | T2 scoring entry point (`--mode fast` or `--mode full`) |
| `app_both.py` | Combined T1/T2 Gradio demonstration |
| `synthetic_t1_example.csv` | Three synthetic T1 patients (no real data) |
| `synthetic_example.csv` | Three synthetic T2 patients (no real data) |
| `synthetic_scored.csv` | Example output from the fast mode |
| `requirements.txt` | Minimal dependencies for the fast demo |
| `requirements-full.txt` | Additional dependencies for the five-expert mode |
| `Dockerfile` | Container template; mount the locked artifacts at `/models` |
| `MANIFEST.json` | SHA-256 hashes of the locked artifacts |

## Quick start (Windows, project environment)

The script defaults to the development paths. If the artifacts are elsewhere, set:

```powershell
$env:T2_ROOT = "D:\pythonProject\v10\v11_t2_numeric_20261104\full_relock_v3"
$env:T2_LAYERS = "$env:T2_ROOT\accord_sl\t2_original_accord_sl\t2_original_accord_sl_locked_layers.joblib"
$env:T2_EXPERTS = "$env:T2_ROOT\models\t2_expert_pool\expert_model_artifacts"
```

Run the synthetic examples:

```powershell
python predict_t2.py --input synthetic_example.csv --out synthetic_scored.csv --mode fast
python predict_t1.py --input synthetic_t1_example.csv --out synthetic_t1_scored.csv --mode fast
```

Run the combined web demo:

```powershell
python app_both.py
# open http://127.0.0.1:7862
```

## Input CSV

One row per patient. Friendly column names are accepted and mapped to the locked raw feature names:

| Friendly name | Locked feature | Unit / note |
|---|---|---|
| `age` | `s0_age_years_raw` | years |
| `pt_activity` | `raw_lab_02b4c70e60_first_result` | % |
| `hs_crp` | `raw_lab_0e007fa586_first_result` | mg/L |
| `potassium` | `raw_lab_15b244e231_first_result` | mmol/L |
| `calcium` | `raw_lab_1b2ae3b1ce_first_result` | mmol/L |
| `aptt` | `raw_lab_30ef0a2b99_first_result` | s |
| `phosphate` | `raw_lab_4d6eb6773c_first_result` | mmol/L |
| `co2_binding` | `raw_lab_50206d459c_first_result` | mmol/L |
| `chloride` | `raw_lab_6f82e52447_first_result` | mmol/L |
| `crp` | `raw_lab_9669c140d7_first_result` | mg/L |
| `magnesium` | `raw_lab_a615156159_first_result` | mmol/L |
| `sodium` | `raw_lab_b7e6d36365_first_result` | mmol/L |

Missing values are allowed; the locked preprocessor applies training-fitted imputation.

## Output CSV

| Column | Meaning |
|---|---|
| `raw_score` | Weighted ensemble probability before calibration |
| `calibrated_score` | Calibrated probability |
| `high_risk` | 1 if `calibrated_score >= 0.05` |
| `near_threshold` | 1 if within ±0.02 of 0.05 |
| `<expert>__probability` | Individual expert probabilities |

The 0.05 threshold is a sensitivity-first research operating point, not a deployment default.

## Modes

- **fast**: EBM + random forest, weights renormalised. This is a demonstration approximation and does **not** reproduce the locked five-expert ensemble.
- **full**: all five locked experts. The portable artifacts in `models/experts/` have been re-saved with standard sklearn preprocessors; full mode has been smoke-tested with the project environment.

## Tested Docker CLI image

A minimal CLI image is in `../release_cli/` and has been built and run on synthetic data:

```bash
cd ../release_cli
docker build -t accord-sl-t2-cli .
docker run --rm -v "$PWD:/data" accord-sl-t2-cli \
  --input /data/synthetic_example.csv --out /data/synthetic_scored.csv --mode fast
```

## Gradio demo

Run locally (tested):

```bash
python app.py
# http://127.0.0.1:7860
```

The Gradio Dockerfile in this folder is a template. A full Gradio image was not built in this environment because the registry/network blocked the complete Gradio dependency install. The CLI image above is the validated container path.

## Reproducibility notes

- The locked artifacts were produced by the v11 T2 re-lock (`v11_t2_summary.json`).
- The calibration layer expects the logit of the weighted ensemble.
- The final expert artifacts may be full-data refits; their individual probabilities can differ from the stored out-of-fold predictions. Use the package for demonstration and prospective research, not as a claim of exact reproduction of the published validation predictions.

## License

- Source code: MIT (`LICENSE`).
- Model weights and locked artifacts: CC BY-NC 4.0 (`LICENSE-WEIGHTS`).
- No clinical use; commercial use requires permission.

## Disclaimer

This package is for research evaluation only. It is not approved by any regulatory authority. Do not use it as a stand-alone screening or diagnostic test. Any clinical use requires local recalibration, assay harmonisation, prospective workflow evaluation, and ethics/governance approval.
