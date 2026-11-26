# Model card — ECG-Age frozen CNN–TCN–Transformer

## Summary

**Task:** Supervised regression of chronological age from a 10-second, standard 12-lead ECG. The output is **ECG-derived age** in years, not an independently validated measurement of biological aging.

**Associated manuscript:** Hussain I., Boyer R., Armoundas A. A., Scarpa J. R. *Morphology-aware deep learning for ECG-derived age estimation and its association with postoperative outcomes* (under review; no final DOI assigned).

**Release:** Architecture, frozen input processing and single-record WFDB inference source. **No trained weights are distributed.**

## Model specification

| Property | Frozen configuration |
| --- | --- |
| Framework | PyTorch |
| ECG duration | 10 seconds |
| Sample rate | 500 Hz |
| Physical leads | 12 standard leads |
| Model input | 24 channels × 5,000 samples |
| Input representation | 12 mean-centered physical ECG signals + 12 first differences |
| Attention | Input-channel softmax attention |
| Local feature extractor | Multiscale 1D CNN, kernels 3, 7, 15 |
| Temporal modeling | Five residual dilated TCN blocks (1, 2, 4, 8, 16) |
| Global modeling | Six Transformer blocks, hidden width 192, 4 heads |
| Output pooling | Equal-weight mixture of attention pooling and mean pooling |
| Head | LayerNorm and linear regression |
| Parameters | 3,532,674 |
| Inverse target normalization | `predicted_years = prediction_normalized × 20.83683569742911 + 55.045702521873395` |

The implementation and values in [configs/inference.json](../configs/inference.json) reflect the frozen inference configuration. No extra filtering, per-lead standardization, or signal rescaling is applied by the public single-record script.

## Study populations and reported evaluation

| Study group | N | MAE (years) | R² |
| --- | ---: | ---: | ---: |
| Non-surgical MIMIC-IV-ECG training | 68,005 | — | — |
| Non-surgical development | 9,716 | — | — |
| Non-surgical locked test | 19,431 | 7.364 | 0.787 |
| Surgery-linked MIMIC-IV domain shift | 58,447 | 7.810 | 0.613 |
| Independent EchoNext zero-shot | 5,278 | 8.905 | 0.470 |

The results are **reported in the under-review manuscript** and are not recomputed by this code-only package. The surgery-linked population was **not** used for model training or checkpoint selection. EchoNext zero-shot evaluation did not involve model retraining or recalibration.

The manuscript notes pronounced **age-dependent bias** in external validation. Its paired input ablation did not demonstrate a beneficial increment from derivative channels; retaining them here reproduces the frozen input contract, not a claim that they improve performance.

## Intended uses

- Research review of a published inference architecture.
- Software inspection and synthetic testing without patient data.
- Single-record research prediction with a separately authorized checkpoint and a compatible authorized WFDB recording.

## Out-of-scope uses

- Clinical diagnosis or management.
- Surgical risk estimation or postoperative complication classification.
- Measuring individualized cardiovascular or biological age with clinical validity.
- Processing arbitrary ECG sampling rates, missing leads, or other formats without independently validated preprocessing.
- Reproducing the manuscript's cohort-specific statistical analyses using this inference-only code.

## Limitations

1. **Age-gap interpretation:** ECG age gap is predicted ECG age minus chronological age; its distribution depends on age and domain. A positive gap is not proof of accelerated biological aging.
2. **Data constraints:** MIMIC-IV de-identification affects age interpretation, especially in the oldest patients.
3. **Transportability:** External validation displayed reduced performance and age-dependent bias compared with the internal locked test.
4. **Surgical chronology and outcomes:** Of the 58,447 original surgery-linked ECGs, 37,075 were on strictly earlier calendar days, 19,873 on the same day (within-day order unknown), and 1,499 on later days relative to the earliest major-surgery index. Source-defined mortality follow-up was not certified complete at one year; ICU use was not adjudicated as planned/unplanned. See [postoperative findings](POSTOPERATIVE_FINDINGS.md). The repository does not contain clinical prediction models.
5. **Signal requirements:** The single-record CLI requires exact leads, duration, and frequency. External EchoNext harmonization is not implemented here.
6. **Discrimination and interpretation:** Positive adjusted AgeGap–outcome associations do not establish clinical decision utility. Exploratory internal out-of-fold incremental AUROC changes were small, particularly in strictly earlier-date ECGs. Surgical-cohort cross-fitted residual categories are not the manuscript's development-frozen residual classes.\n7. **Reproducibility boundary:** Running the public synthetic test does not replicate cohort-level results. Model weights, protected waveforms, participant splits, and analysis pipelines are absent.

## Governance

Dataset licensing, checkpoint redistribution rights, ethical restrictions, and institutional approval remain applicable. No medical regulatory clearance is asserted. No explicit open-source license has been provided.
