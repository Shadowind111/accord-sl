# ACCORD-SL data dictionary (summary)

## Cohort and outcomes
- `analysis_unit_hash`: de-identified inpatient admission-linked participant identifier.
- `label`: `1` = pathology- and immunohistochemistry-confirmed gastrointestinal stromal tumour (GIST); `0` = contemporaneous symptomatic non-GIST inpatient control.
- `split`: `development` (n=1,313; 219 GIST, 1,094 controls), `validation_lock` (n=282; 47 GIST, 235 controls), `audit_lock` (n=280; 47 GIST, 233 controls), `external_CEX_2` (n=1,759; 298 GIST, 1,461 controls), `external_CEX_1` (n=1,260; 210 external GIST cases paired with 1,050 internal matched controls).
- `age`: age in years at index admission.
- `sex`: sex assigned at birth recorded in the hospital information system (`1` = female, `0` = male; available in the internal cohort [845/1,875, 45·1% female]; unavailable in CEX-1 and CEX-2 exports).

## T1 contract (Blood3 + age; 4 predictors)
- `age`: age in years.
- `basophil_pct`: basophil percentage (%).
- `alt`: alanine aminotransferase (ALT, U/L).
- `albumin`: serum albumin (g/L).

## T2 contract (11 routine quantitative blood markers + age; 12 predictors)
- `pta`: prothrombin activity (PTA, %).
- `aptt`: activated partial thromboplastin time (APTT, s).
- `potassium`: serum potassium (mmol/L).
- `calcium`: serum total calcium (mmol/L).
- `phosphate`: serum inorganic phosphate (mmol/L).
- `co2cp`: carbon dioxide combining power (CO2CP, mmol/L).
- `chloride`: serum chloride (mmol/L).
- `sodium`: serum sodium (mmol/L).
- `hs_crp`: high-sensitivity C-reactive protein (hs-CRP, mg/L).
- `crp`: C-reactive protein (CRP, mg/L).
- `magnesium`: serum magnesium (mmol/L).
- `age`: age in years (shared demographic covariate; T1 and T2 laboratory markers are completely disjoint across 14 routine quantitative blood tests).

## Derived workflow variables
- `T1_probability`: calibrated T1 ensemble probability (equal 0·20 weights across 5 experts).
- `T2_probability`: Platt-calibrated T2 ensemble probability (NNLS logit weights across Top-5 experts).
- `t1_positive`: `1` if `T1_probability >= 0·134` (locked T1 gatekeeper threshold), else `0` (silent stop).
- `t2_positive`: `1` if `T2_probability >= 0·237` (locked T2 confirmation threshold), else `0`.
- `dual_positive`: `1` if `t1_positive == 1` and `t2_positive == 1` (triggers non-interruptive clinician queue alert), else `0`.
- `y_true` / `y_pred`: observed pathological status and sequential workflow binary alert status.

## Missingness and preprocessing governance
- Item-level measurement counts and percentages are reported in Table 1 and Supplementary Table S1.
- All imputers and preprocessors were fitted strictly within development cross-validation folds (fold-fitted median imputation for T1; fold-fitted Bayesian-ridge `IterativeImputer` for T2) and applied in transform-only mode during internal validation, post-lock audit, CEX-2, and CEX-1 inference.
- CEX-1 cases had 0% measurement for PTA, APTT, hs-CRP, and CRP; unmeasured T2 markers were conditionally imputed from the seven observed T2 electrolyte markers and age using the locked development `IterativeImputer`.
