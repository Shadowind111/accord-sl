# Model card: ACCORD-SL two-tier opportunistic GIST case-finding workflow

## 1. Model details
- **Model name:** ACCORD-SL (Accessibility-Constrained, Calibrated-probability, Operational-Risk Decision Super Learner)
- **Version:** v11 locked model release (corresponding manuscript: v13); T1 Blood3 threshold 0.134; T2 threshold 0.237
- **Architecture:**
  - **Tier 1 (T1 gatekeeper):** Locked ensemble of five prespecified heterogeneous tabular learners — Explainable Boosting Machine (EBM), XGBoost histogram (`xgboost_hist`), TabPFN, subsampled gradient boosting, and radial-basis-function support vector machine (`SVM-RBF`) — combined with equal `0·20` weights on the Blood3 + age contract.
  - **Tier 2 (T2 specialty prioritisation):** Locked Top-5 ensemble selected from 26 candidate learners via a predefined seven-dimension clinical-statistical composite score — EBM (`0·219`), TabPFN (`0·206`), TabDPT (`0·196`), AutoGluon stacked ensemble (`0·196`), and balanced random forest (`0·183`) — combined via non-negative least squares (NNLS) on out-of-fold logits followed by Platt scaling.
- **Developed by:** Department of General Practice and Department of Gastrointestinal Surgery, The Seventh Affiliated Hospital, Sun Yat-sen University, Shenzhen, China.
- **Intended setting:** Secondary and tertiary hospital inpatient care, operating silently on routine admission laboratory streams before specialist diagnostic confirmation of gastrointestinal stromal tumour (GIST).
- **Release status:** Research prototype and formative clinical decision-support API; not a certified medical device; not for autonomous clinical diagnosis.

## 2. Intended use
### 2.1 Primary intended use
ACCORD-SL is designed for **opportunistic pre-diagnostic risk stratification and triage** among symptomatic adult inpatients whose routine blood counts and biochemistry panels have already been generated during standard clinical care.
- **T1 (Blood3 + age)** acts as a high-sensitivity front-end gatekeeper (`threshold >= 0·134`). Patients below `0·134` terminate silently; patients at or above `0·134` enter silent backend deferral without interrupting clinicians until routine inpatient T2 assays are available.
- **T2 (11 routine markers + age)** evaluates T1-positive inpatients (`threshold >= 0·237`). Only **dual-positive** patients (`T1 >= 0·134` and `T2 >= 0·237`) trigger a non-interruptive clinician task-queue notification recommending consideration of contrast-enhanced CT or endoscopic ultrasound (EUS).

### 2.2 Out-of-scope use
- Not a standalone diagnostic blood test for GIST and must never replace endoscopy, EUS, imaging, histopathology, or molecular testing.
- Negative triage scores must never be used to rule out GIST or override clinical red-flag indications (e.g., gastrointestinal bleeding, palpable mass, severe anaemia, or weight loss).
- Not validated for asymptomatic general-population screening, paediatric populations, or uncalibrated cross-hospital deployment without local assay verification and threshold recalibration.

## 3. Input contracts (14 disjoint routine quantitative blood markers + age)
### 3.1 Tier 1 (T1 Blood3 contract: 3 laboratory items + age)
| Module | Features |
|---|---|
| Demographic | Age (years) |
| Complete blood count | Basophil percentage (%) |
| Liver function / enzymes | Alanine aminotransferase (ALT, U/L), serum albumin (g/L) |

*(Note: An earlier 20-item exploratory T1 contract containing 17 semi-quantitative urinalysis dipstick fields was simplified to Blood3 during cross-centre coding governance to avoid ordinal urinalysis coding drift; CEX-2 T1 estimates are therefore reported as exploratory, whereas CEX-2 T2 is the primary external validation.)*

### 3.2 Tier 2 (T2 inpatient contract: 11 laboratory items + age)
| Module | Features |
|---|---|
| Demographic | Age (years) |
| Coagulation | Prothrombin activity (PTA, %), activated partial thromboplastin time (APTT, s) |
| Electrolytes & acid–base | Potassium (mmol/L), calcium (mmol/L), inorganic phosphate (mmol/L), carbon dioxide combining power (CO2CP, mmol/L), chloride (mmol/L), sodium (mmol/L), magnesium (mmol/L) |
| Inflammation | High-sensitivity C-reactive protein (hs-CRP, mg/L), C-reactive protein (CRP, mg/L) |

## 4. Locked thresholds and backend workflow outputs
- `T1_probability`: calibrated T1 probability (`locked threshold = 0·134`).
- `T2_probability`: Platt-calibrated T2 probability (`locked threshold = 0·237`).
- `workflow_state`:
  - `SILENT_STOP_T1` (`T1 < 0·134`): no alert generated (`36·2%` of internal validation cohort; NPV `93·1%`).
  - `SILENT_DEFERRAL_T1_POS` (`T1 >= 0·134` while awaiting T2 or `T2 < 0·237`): held silently in backend without pop-up alerts; ~two-thirds of T1-positive false alarms are filtered out by T2.
  - `QUEUE_ALERT_DUAL_POS` (`T1 >= 0·134` and `T2 >= 0·237`): routes a non-interruptive advisory notification to the clinician task queue (`20·9%` internal alert rate; `24·4%` in CEX-2).

## 5. Development and validation cohorts
- **Internal cohort (The Seventh Affiliated Hospital, Sun Yat-sen University, Shenzhen; Sept 1, 2019 – Sept 1, 2025):** 1,875 analysis-ready records (313 pathology-confirmed GIST and 1,562 hierarchically age- and year-matched symptomatic non-GIST controls [310 at 1:5 and 3 at 1:4 matching] drawn from 5,534 eligible symptomatic inpatients [5·7% GIST]; 845/1,875 [45·1%] female).
  - **Development set:** `n=1,313` (219 GIST, 1,094 controls; 595 females, 718 males).
  - **Locked internal validation set (primary internal test):** `n=282` (47 GIST, 235 controls; 116 females, 166 males).
  - **Post-lock audit set (partition-stability audit):** `n=280` (47 GIST, 233 controls; 134 females, 146 males).
- **External validation cohort CEX-2 (The Sixth Affiliated Hospital, Sun Yat-sen University, Guangzhou):** `n=1,759` randomly sampled inpatients (298 pathologically confirmed GIST and 1,461 symptom-matched, gastrointestinal tumour-enriched non-GIST controls; prevalence `16·9%`).
- **External sensitivity cohort CEX-1 (The Fourth Affiliated Hospital of China Medical University, Shenyang):** `n=210` pathologically confirmed GIST inpatients (lacking native controls and lacking PTA, APTT, hs-CRP, and CRP), paired with `1,050` internal matched controls (`n=1,260`) and evaluated both unweighted and with overlap weighting (`effective sample size = 133`; weighted baseline `0·50`).

## 6. Quantitative performance summary
### 6.1 Core discrimination, calibration, operating characteristics, and 5%-prevalence workload
| Analysis | n | AUROC (95% CI) | AUPRC (95% CI) | Calib. slope | Brier / ECE | Sens. | Spec. | Raw PPV | NPV | Alert rate | 5% PPV | 5% NNE |
|---|---:|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| Internal validation — T1 | 282 | 0·701 (0·618–0·779) | 0·289 (0·204–0·391) | 1·459 | 0·131 / 0·031 | 0·851 | 0·404 | 0·222 | 0·931 | 0·638 | 0·070 | 14·3 |
| Internal validation — T2 all-comers | 282 | 0·767 (0·689–0·838) | 0·501 (0·368–0·632) | 0·995 | 0·116 / 0·034 | 0·574 | 0·821 | 0·391 | 0·906 | 0·245 | 0·144 | 6·9 |
| Internal validation — T2 \| T1+ | 180 | — | — | — | — | 0·625 | 0·757 | 0·424 | 0·876 | 0·328 | — | — |
| Internal validation — sequential | 282 | — | — | — | — | 0·532 | 0·855 | 0·424 | 0·901 | 0·209 | 0·162 | 6·2 |
| Post-lock audit — T1 | 280 | 0·624 (0·538–0·708) | 0·221 (0·158–0·306) | — | — | 0·809 | 0·403 | 0·215 | 0·913 | 0·632 | 0·067 | 15·0 |
| Post-lock audit — T2 all-comers | 280 | 0·733 (0·651–0·809) | 0·333 (0·231–0·452) | — | — | 0·426 | 0·781 | 0·282 | 0·871 | 0·254 | 0·093 | 10·8 |
| Post-lock audit — sequential | 280 | — | — | — | — | 0·383 | 0·837 | 0·321 | 0·871 | 0·200 | 0·110 | 9·1 |
| Combined held-out — T2 | 562 | 0·752 (0·696–0·804) | 0·408 (0·324–0·496) | — | — | — | — | — | — | — | — | — |
| Combined held-out — sequential | 562 | — | — | — | — | 0·457 | 0·846 | 0·374 | 0·886 | 0·205 | 0·135 | 7·4 |
| CEX-2 — T1 (exploratory) | 1,759 | 0·626 (0·592–0·658) | 0·230 (0·201–0·264) | 0·861 | 0·148 / 0·039 | 0·836 | 0·372 | 0·213 | 0·917 | 0·663 | 0·065 | 15·3 |
| CEX-2 — T2 all-comers (primary) | 1,759 | 0·668 (0·636–0·699) | 0·250 (0·218–0·293) | 0·612 | 0·140 / 0·045 | 0·483 | 0·739 | 0·274 | 0·875 | 0·299 | 0·089 | 11·3 |
| CEX-2 — T2 \| T1+ | 1,167 | — | — | — | — | 0·522 | 0·674 | 0·303 | 0·839 | 0·368 | — | — |
| CEX-2 — sequential | 1,759 | — | — | — | — | 0·436 | 0·795 | 0·303 | 0·874 | 0·244 | 0·101 | 9·9 |
| CEX-1 unweighted — sequential | 1,260 | — | — | — | — | 0·081 | 0·826 | 0·085 | 0·818 | 0·159 | 0·024 | 41·9 |
| CEX-1 weighted — sequential | 1,260 | — | — | — | — | 0·092 | 0·942 | 0·613 | 0·509 | 0·075 | 0·077 | 13·0 |

*(Decision-curve net benefit at the locked thresholds in internal validation: `0·065` for T1 at `0·134` and `0·049` for T2 at `0·237`.)*

### 6.2 Formative clinician usability evaluation (`n=12` physicians)
- **Prototype ratings (mean out of 5, Modal / Banner / Queue):** Clarity `5·00 / 4·75 / 4·50`; Urgency `4·33 / 3·17 / 2·50`; Trust `4·00 / 3·25 / 3·00`; Workflow intrusiveness `4·33 / 2·75 / 1·25` (higher = more intrusive); Actionability `5·00 / 4·67 / 4·83`.
- **Workflow & human-in-the-loop safety:** `8/12 (66·7%)` preferred the non-interruptive Queue; `11/12 (91·7%)` opposed alerting before T2 completion; `12/12 (100%)` required repeat-alert suppression after clinical action; `9/12 (75·0%)` appropriately overrode discordant high model scores when clinical pre-test probability was low. Mean System Usability Scale (SUS) score was `73·75 (SD 5·38)`, perceived alert fatigue `1·67/5`, and overall model trust `2·33/5`.

## 7. Limitations and governance requirements
- Retrospective matched case-control (internal) and tumour-enriched (CEX-2) sampling; prospective evaluation in consecutive unselected admissions is required before clinical deployment.
- CEX-1 lacked native non-GIST controls and lacked four core T2 coagulation/inflammation markers (PTA, APTT, hs-CRP, CRP), causing conditionally imputed T2 probabilities to contract toward the mean and fall below the fixed `0·237` threshold (`sensitivity 0·081` unweighted / `0·092` weighted). Local assay completion and threshold recalibration are mandatory before cross-centre use.
- Sex was available internally (`45·1%` female) but unavailable in CEX-1 and CEX-2 exports.

## 8. License and contact
- **License:** MIT License for source code and API; model weights and locked artifacts are CC BY-NC 4.0.
- **Contact:** Prof Changhua Zhang (`zhangchanghua@sysush.com`), Department of Gastrointestinal Surgery, The Seventh Affiliated Hospital, Sun Yat-sen University, No. 628 Zhenyuan Road, Guangming District, Shenzhen 518107, Guangdong, China.
