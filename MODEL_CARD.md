# Model card: T2-ACCORD-SL (v11) and T1-ACCORD-SL (r3)

## 1. Model details

- **Model name:** ACCORD-SL (accessibility-constrained, decision-utility Super Learner)
- **Versions:** T1 r3; T2 v11 (numeric hs-CRP/CRP re-lock)
- **Model type:** locked ensemble of five heterogeneous tabular experts with weighted fusion, Platt-style calibration and a prespecified operating threshold
- **Developed by:** The Seventh Affiliated Hospital, Sun Yat-sen University, Shenzhen, China
- **Intended setting:** secondary/tertiary hospital inpatient care, before specialist confirmation of a gastrointestinal stromal tumour (GIST)
- **Release status:** research prototype with portable T2 scoring package; not a medical device; not for clinical decision-making

## 2. Intended use

### 2.1 Intended use

T2-ACCORD-SL is intended for **research evaluation of opportunistic risk stratification** among symptomatic inpatients whose routine laboratory data are already available. It estimates the probability that a patient belongs to the GIST-risk spectrum and is intended to support, not replace, the decision to complete specialist assessment (imaging, endoscopy/EUS, pathology, molecular testing).

T1-ACCORD-SL is a lower-burden pre-screen intended to test whether a minimal laboratory set can trigger information completion or clinical review in settings where the full T2 panel is not yet available.

### 2.2 Not intended use

- Not a diagnostic test for GIST.
- Not a stand-alone screening test in the general population.
- Not validated for asymptomatic individuals, outpatients, children, or patients without the specified laboratory items.
- Not for triage decisions without local recalibration and prospective workflow evaluation.
- Not for use as the sole basis for referral, treatment, or discharge.

## 3. Inputs

### 3.1 T2 contract (11 laboratory items + age)

| Module | Items |
|---|---|
| Coagulation | prothrombin activity (PT%), activated partial thromboplastin time (APTT) |
| Electrolytes | potassium, calcium, inorganic phosphate, carbon dioxide binding capacity, chloride, sodium, magnesium |
| Inflammation | high-sensitivity C-reactive protein (hs-CRP), C-reactive protein (CRP) |
| Demographic | age (years) |

### 3.2 T1 contract (20 laboratory items + age)

| Module | Items |
|---|---|
| Complete blood count | basophil percentage |
| Liver enzymes | alanine aminotransferase |
| Liver function | albumin |
| Urinalysis dipstick | urine ketone, urine leukocyte esterase (two source fields), specific gravity, pH, turbidity (two source fields), bilirubin, occult blood (two source fields), colour, urobilinogen, protein, faecal occult blood, nitrite, glucose, urine occult blood/red cells |

The two contracts are mutually exclusive; their union is 31 laboratory items. Age is included as a covariate.

### 3.3 Input format

- One row per patient.
- Numeric laboratory values in the units used during development; `<`/`>` prefixes are stripped and the boundary value is used.
- Missing values are allowed; the locked preprocessor applies training-fitted imputation.
- Categorical urinalysis results should use the source categories; the released demo accepts the numeric codes used in the accompanying example.

## 4. Outputs

- `raw_score`: weighted ensemble probability before calibration.
- `calibrated_score`: calibrated probability.
- `high_risk`: 1 if `calibrated_score >= 0.05` (locked T2 threshold), otherwise 0.
- `near_threshold`: 1 if the score is within ±0.02 of the threshold, otherwise 0.

The locked T2 threshold of 0.05 is a **sensitivity-first research operating point**. It is not a deployment default; at this threshold the internal flag rate was 73.8%.

## 5. Training data

- 1,875 analysis-ready records: 313 pathology-confirmed GISTs and 1,562 matched non-GIST controls.
- Single tertiary centre, 1 September 2019 to 1 September 2025.
- Matched case–control design (up to 1:5), matched on report year and age; GIST prevalence in the analysis cohort was 16.7%, not a natural prevalence.
- Development/out-of-fold: 1,313 records (219 GISTs); locked internal validation: 282 records (47 GISTs); held-out test subset: 280 records (47 GISTs; previously read and used only for exploratory audit).
- External evaluation: CEX-1 (Fourth Affiliated Hospital of China Medical University; 210 GISTs, case-only) and CEX-2 (Sixth Affiliated Hospital, Sun Yat-sen University; 298 GISTs and 1,461 symptom-matched, tumour-enriched non-GIST controls).

## 6. Performance

### 6.1 Internal locked validation (282 records, 47 GISTs)

| Metric | T1 r3 | T2 v11 |
|---|---:|---:|
| AUROC | 0.746 | 0.767 |
| AUPRC (baseline 0.167) | 0.361 | 0.501 |
| Brier score | — | 0.116 |
| Calibration slope | — | 0.995 |
| ECE (10-bin) | — | 0.034 |
| Sensitivity | 0.468 | 0.936 |
| PPV | 0.386 | 0.212 |
| Flag rate | 20.2% | 73.8% |
| Net benefit (pt=0.05) | 0.031 | 0.125 |

### 6.2 External evaluation (CEX-2, 1,759 records, 298 GISTs)

| Input | AUROC (95% CI) | AUPRC (95% CI) | Calibration slope | Top-20% sensitivity | Top-20% PPV |
|---|---:|---:|---:|---:|---:|
| 8 model-compatible items (primary) | 0.628 (0.594–0.659) | 0.220 (0.193–0.256) | 0.420 | 0.258 | 0.219 |
| 11 items with manual PT/Mg/CRP | 0.668 | 0.250 | 0.612 | 0.295 | 0.250 |

CEX-1 (210 GISTs, case-only): 90.5% flagged at 0.05; 2.4% at the internal top-20% threshold (0.269); 0.5% at the top-10% threshold (0.340).

### 6.3 Prevalence-adjusted yield

Because the development and external cohorts were matched/enriched, observed PPV and net benefit are not natural-prevalence estimates. At a plausible inpatient prevalence of 1%, the top-20% policy had PPV 1.4% and required 73 workups per detected case; at 5%, PPV 6.7% and 15 workups per case. The model is a risk-stratification/triage aid, not a population screening test.

## 7. Calibration and transportability

- Internal calibration was strong (slope 0.995).
- External calibration was poor (slope 0.420 for the 8-item primary analysis; 0.612 after manual completion).
- Discrimination fell from 0.751 (internal 8/11 benchmark) to 0.628 (CEX-2), and AUPRC from 0.465 to 0.220.
- Absolute thresholds did not transport: the 0.05 threshold flagged 90.5% of CEX-1 cases but the internal top-20% threshold flagged only 2.4%.
- Local recalibration, assay harmonisation and completion of PT/CRP/Mg are required before any cross-centre use.

## 8. Limitations

- Matched case–control design, not a consecutive deployment cohort.
- CEX-2 controls were symptom-matched and tumour-enriched; CEX-1 had no independent controls.
- Only 8 of 11 T2 items were available in the CEX-2 raw export; PT/CRP/Mg were manually abstracted for sensitivity analyses.
- Carbon dioxide binding capacity was observable in only 14.7% of CEX-2 records and is not equivalent to total CO2.
- No temporal validation; the held-out test subset had been read previously.
- No formal usability evaluation or prospective clinical impact data.
- Sex and other demographic fields were incomplete in internal controls and CEX-1; fairness could not be fully assessed.
- The fast demonstration uses EBM + random forest only; full mode loads all five experts. Both are research-only and not a validated reproduction of the locked ensemble outside the tested examples.

## 9. Ethical and regulatory considerations

- Use only de-identified data.
- Do not use for diagnosis, treatment, referral, or discharge decisions.
- Do not use outside the intended population or without local calibration.
- Report the model card, input contract, threshold and calibration status whenever the model is evaluated.
- The model is not approved by any regulatory authority.

## 10. Files and contact

- `models/`: portable locked layers, five expert artifacts and input contracts.
- `predict_t2.py`: T2 scoring entry point (`--mode fast` or `--mode full`).
- `app.py`: local Gradio batch demonstration.
- `../release_cli/`: tested minimal Docker CLI image (`accord-sl-t2-cli`).
- `Dockerfile`: Gradio image template (not built in this environment).
- `synthetic_example.csv`: synthetic input example (no patient data).
- `MANIFEST.json`: SHA-256 hashes of the locked artifacts.

Contact: corresponding authors of the accompanying manuscript.

## 11. License

- Source code: MIT.
- Model weights and locked artifacts: CC BY-NC 4.0.
- No clinical use; commercial use requires separate permission.
