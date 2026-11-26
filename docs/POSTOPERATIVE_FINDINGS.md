# Postoperative findings and interpretation (manuscript revision 2)

This document provides **aggregate, manuscript-linked context** for the *under-review* study, *Morphology-aware deep learning for ECG-derived age estimation and its association with postoperative outcomes*. It does not release the study's statistical-analysis code, patient records, mortality labels, event dates, predicted ages, or executable clinical risk models. The public repository remains **inference source only**, without trained weights.

## Cohort and source-outcome limits

The original frozen surgery-linked cohort comprised 58,447 people (one selected ECG per patient). Date-level comparison to the earliest major-procedure index found:

| ECG acquisition date relative to surgery index | Participants |
| --- | ---: |
| Strictly earlier calendar day | 37,075 |
| Same calendar day; intra-day ordering unknown | 19,873 |
| Later calendar day | 1,499 |
| Total | 58,447 |

The separate admission-consistent timing cohort excluded 50 index-after-discharge records (n = 58,397); its strictly earlier ECG subset was n = 37,031. These are **not interchangeable populations**. A same-day ECG cannot be certified preoperative from procedure calendar dates alone.

The primary observational associations retain the frozen source-defined 30-day mortality, 1-year mortality, AKI, ICU utilization, 30-day readmission, and 1-year MACE indicators. Death-date matching against MIMIC-IV 3.1 verified concordance of the 13,057 observed dates, **not complete 365-day follow-up** from each surgical index. AKI measurement availability and linkage are imperfect; ICU use does not distinguish planned from unplanned admission; some readmissions and nonfatal MACE outside contributing facilities may be missed. Accordingly, findings are **retrospective associations**, not causal perioperative effects.

## Reported primary association results

The full frozen cohort's multivariable-adjusted odds ratios per +10-year **raw ECG AgeGap** were:

| Source-defined endpoint | Adjusted OR (95% CI) |
| --- | --- |
| Recorded 30-day mortality | 1.224 (1.157–1.294) |
| Recorded 1-year mortality | 1.153 (1.116–1.191) |
| Recorded postoperative AKI | 1.123 (1.094–1.154) |
| Recorded ICU indicator | 1.100 (1.076–1.125) |
| Recorded 30-day readmission | 1.043 (1.017–1.070) |
| Recorded 1-year MACE | 1.141 (1.089–1.195) |

The adjusted models included chronological age, age squared, sex, ischemic heart disease, heart failure, cerebrovascular disease, high-risk surgery, diabetes, renal dysfunction, and non-elective urgency. Significant regression coefficients do **not** imply strong patient-level discrimination or decision benefit.

## Exploratory head-to-head mortality discrimination

An additional exploratory comparison used five-fold stratified out-of-fold logistic predictions on the original full and strictly earlier-date cohorts. Evaluation retained the natural event distribution, without 1:1 survivor undersampling, oversampling, or class weighting. The clinical baseline included age and age squared, sex, the individual RCRI-related components, and urgency.

| Cohort | Recorded outcome | Events | Clinical AUROC | Clinical + raw AgeGap AUROC | Paired ΔAUROC (95% bootstrap CI) |
| --- | --- | ---: | ---: | ---: | --- |
| Full (n = 58,447) | 30-day mortality | 2,290 | 0.80732 | 0.81001 | +0.00269 (+0.00086 to +0.00452) |
| Full (n = 58,447) | 1-year mortality | 7,195 | 0.76983 | 0.77135 | +0.00152 (+0.00062 to +0.00240) |
| Strictly earlier (n = 37,075) | 30-day mortality | 1,231 | 0.82586 | 0.82650 | +0.00065 (−0.00149 to +0.00243) |
| Strictly earlier (n = 37,075) | 1-year mortality | 4,451 | 0.77912 | 0.78024 | +0.00111 (+0.00015 to +0.00209) |

In the strictly earlier-date subgroup, standalone AUROCs for **predicted ECG age / raw AgeGap / surgical cross-fitted age residual / exploratory ±5-year residual categories** were **0.6966 / 0.4795 / 0.5895 / 0.5755** for 30-day mortality and **0.6907 / 0.5194 / 0.5733 / 0.5621** for 1-year mortality. The exploratory residual **was derived through cross-fitting in the surgical cohort** and is **not** the independently development-frozen residual reported in the manuscript's main age-residualization analysis (which uses ±1 development SD categories). The category thresholds, regression strategy and evaluation cohort therefore should not be conflated.

Within clinical models containing chronological age, raw AgeGap and predicted ECG age are mathematically reparameterizations: predicted ECG age = chronological age + AgeGap. Their out-of-fold predictions in this comparison were numerically near-identical. A weak *standalone* AgeGap AUROC does not imply that it contains no conditional mortality association.

Intervals above were obtained from 1,000 class-stratified **paired bootstrap resamples of fixed out-of-fold risks**. They do not incorporate refitting the outcome models, do not adjust for multiple exploratory comparisons, and do not establish external validation or clinically meaningful net benefit. **Changes in AUROC are very small**, and the earlier-date 30-day interval includes zero.

## Release boundary

This public repository permits inspection of the frozen inference architecture and input processing **only**; it does not provide:

- Trained model checkpoints or individual patient predictions.
- MIMIC-IV or external patient-level clinical/ECG data.
- Clinical risk prediction code, statistical-analysis pipeline, or supplementary figure/table generation source.
- Exact study-cohort membership and outcome labeling machinery.

Scientific estimates above are reported for context, not reproduced by the software here. For more details on permitted uses, see [MODEL_CARD.md](MODEL_CARD.md) and [AVAILABILITY.md](AVAILABILITY.md). The manuscript remains under review; do not cite these repository notes as an accepted journal publication.
