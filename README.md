# ACCORD-SL v11 research release

Research-use-only code for the ACCORD-SL two-tier opportunistic GIST case-finding workflow.

**Corresponding manuscript:** v13. **Model release:** v11.
**Not a medical device. Not for diagnosis, treatment, referral, or discharge decisions.**

## Locked contracts

- **T1 (Blood3 + age):** age, basophil percentage, ALT, albumin; five experts with equal 0.20 weights; mean-logit fusion; Platt calibration; **threshold 0.134**.
- **T2 (11 markers + age):** PTA, APTT, potassium, calcium, inorganic phosphate, CO2CP, chloride, sodium, hs-CRP, CRP, magnesium; Top-5 ensemble (EBM, TabPFN, TabDPT, AutoGluon, random forest); NNLS fusion; Platt calibration; **threshold 0.237**.

## Weights

Download the Release `v11.0.0` assets and place them under `models/`:

- `t1_blood3_bundle_v11_final.joblib` — T1 Blood3 bundle (threshold 0.134)
- `t2_models_v11.zip` — T2 locked artifacts (full ensemble)
- `t2_fast_cli_v11.zip` — T2 fast CLI package (EBM + random forest approximation)

## Run

```bash
pip install -r requirements.txt
python predict_t1.py --input synthetic_t1_example.csv --out t1_scored.csv
python predict_t2.py --input synthetic_t2_example.csv --out t2_scored.csv
```

## License

Code and API: MIT. Model weights and locked artifacts: CC BY-NC 4.0. No clinical use.
