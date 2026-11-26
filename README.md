# ECG-Age: Morphology-Aware Deep Learning for ECG-Derived Age Estimation

**Research software companion** to the manuscript *“Morphology-aware deep learning for ECG-derived age estimation and its association with postoperative outcomes”* (under review).

A focused Python implementation of the frozen **CNN–TCN–Transformer** ECG-age inference architecture. It converts a 10-second, 12-lead waveform into a supervised estimate of **ECG-derived age in years**.

> **Release boundary:** This repository contains **inference source code and model configuration only**. It intentionally does **not** include trained weights, patient-level data, the study's model-training pipelines, or postoperative outcome modeling code. A separately authorized compatible checkpoint is needed to generate actual age predictions.

[Model documentation](docs/MODEL_CARD.md) · [Inference and reproducibility guide](docs/INFERENCE.md) · [Code and data availability](docs/AVAILABILITY.md)

---

## Study at a glance

The model was developed using the non-surgical MIMIC-IV-ECG cohort, evaluated in a locked holdout and a separate surgery-linked cohort, and tested without retraining on the independent EchoNext cohort.

| Evaluation population | Participants | Frozen-model MAE | R² |
| :-- | --: | --: | --: |
| MIMIC-IV-ECG non-surgical **locked test** | 19,431 | 7.364 years | 0.787 |
| MIMIC-IV surgery-linked **domain shift** | 58,447 | 7.810 years | 0.613 |
| **EchoNext** external zero-shot validation | 5,278 | 8.905 years | 0.470 |

These are **manuscript-reported cohort-level results**, not metrics recalculated by this public repository. Training and development partitions contained 68,005 and 9,716 non-surgical participants, respectively. Results should be interpreted in the context of age-dependent prediction bias, domain shift, de-identification, and ascertainment limitations documented in the manuscript.

### Clinical relevance and interpretation

ECG-derived age provides a deep learning–based estimate of age-associated cardiovascular characteristics captured by the 12-lead electrocardiogram. The difference between ECG-derived age and chronological age (ECG AgeGap) is a retrospective ECG phenotype; it is **not** an independently validated measure of biological aging. In the frozen study, greater AgeGap was associated with six *recorded*, surgery-linked outcomes after adjustment for measured clinical factors. These associations are not causal and do not establish prospective risk-prediction utility.

**Surgical timing matters:** Among 58,447 surgery-linked participants, 37,075 ECGs were dated strictly before the earliest major-surgery index calendar date, 19,873 were dated on the same day (within-day ordering unavailable), and 1,499 were dated afterward. The manuscript therefore distinguishes the original surgery-linked sample from restricted calendar-date analyses. Recorded 1-year mortality follow-up was not independently complete for every participant, and ICU use was not adjudicated as planned or unplanned.

**Incremental discrimination is small:** In exploratory five-fold out-of-fold clinical-model comparisons on the strictly earlier-index-date subgroup (n = 37,075), the clinical-only AUROC was 0.82586 for recorded 30-day mortality and 0.77912 for recorded 1-year mortality. Adding raw AgeGap gave AUROCs of 0.82650 and 0.78024 (paired ΔAUROC +0.00065 [95% bootstrap CI −0.00149 to +0.00243] and +0.00111 [95% CI +0.00015 to +0.00209], respectively). These fixed-prediction bootstrap intervals do **not** include model-refitting uncertainty, and differences are not evidence of validated clinical utility. No survivors were undersampled to balance mortality classes.

The additional exploratory *surgical-cohort cross-fitted* age residual used for those comparisons is **not** the separate development-frozen residual used elsewhere in the manuscript. The strictly earlier-index cohort (n = 37,075) is also distinct from the manuscript's admission-consistent strictly earlier cohort (n = 37,031). See [study-results interpretation](docs/POSTOPERATIVE_FINDINGS.md).

This repository provides frozen ECG-Age **inference source only**; it does not ship the mortality models, patient-level data, underlying study workflows, or model weights. Prospective independent validation is required before individual clinical use.

## How the model works

```text
12-lead ECG (10 seconds, 500 Hz)
        │
        ▼
Per-lead mean centering (physical amplitude preserved)
        │
        ├── 12 centered ECG channels
        └── 12 first temporal-difference channels
        │
        ▼
24-channel input [batch, 24, 5000]
        │
        ▼
Input-channel attention
        │
        ▼
Multiscale 1D CNN (kernel sizes 3, 7, 15)
        │
        ▼
Residual dilated TCN (dilations 1, 2, 4, 8, 16)
        │
        ▼
Transformer encoder (6 blocks, width 192, 4 heads)
        │
        ▼
Attention pooling + mean pooling (equal weights)
        │
        ▼
Regression head → normalized age → age in years
```

The frozen architecture contains **3,532,674 trainable parameters**. The derivative channels are part of the frozen model input, but the manuscript's ablation analyses **did not establish an accuracy benefit from adding them**.

## Quick start

**Prerequisites:** Python 3.10 and a platform-compatible PyTorch installation. The pinned dependencies are recorded in [requirements.txt](requirements.txt); use an isolated environment.

```bash
git clone https://github.com/iqram20/ecg-age-postop.git
cd ecg-age-postop
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

# Does not require model weights or patient ECG data
python scripts/validate_standalone.py
```

The synthetic check reports `PASS_SYNTHETIC_STANDALONE` when its architecture and preprocessing assertions pass. It **does not** assess clinical prediction accuracy.

### Single ECG inference

With a **separately approved, compatible** compact checkpoint and an ECG that you are authorized to use:

```bash
python scripts/infer_single.py \
  --checkpoint /secure/path/ecg_age_frozen_inference.pt \
  --wfdb-record /secure/path/to/wfdb_record_stem \
  --device cpu \
  --json
```

Specify the WFDB **record stem** (the corresponding `.hea` and `.dat` files must exist). Only a 10-second, 500-Hz, 12-lead record with 5,000 samples is accepted; the standalone CLI does not resample or perform the external-cohort harmonization used in the manuscript.

The JSON contains `predicted_ecg_age_years`, `normalized_model_output`, `age_mean`, `age_std`, `device`, and `checkpoint_sha256`. **No downloadable model weights are provided in this repository.**

For exact accepted leads, preprocessing, checkpoint compatibility and interpretation, see the [inference guide](docs/INFERENCE.md).

## Repository contents

```text
ecg-age-postop/
├── configs/
│   └── inference.json          # frozen inference settings
├── docs/
│   ├── AVAILABILITY.md         # data, weights and code release boundary
│   ├── INFERENCE.md            # installation, input contract and CLI
│   └── MODEL_CARD.md           # model purpose, evaluation and limitations
├── scripts/
│   ├── infer_single.py         # WFDB single-record prediction
│   └── validate_standalone.py  # synthetic + optional local checkpoint test
├── src/
│   ├── model.py                # CNN–TCN–Transformer definition
│   └── preprocessing.py        # frozen inference preprocessing
├── .gitignore
├── CITATION.cff
├── README.md
└── requirements.txt
```

## Validation and reproducibility boundaries

In the controlled study environment, the standalone implementation passed synthetic architecture/preprocessing checks, a checkpoint CPU forward pass, real WFDB single-record inference, and a three-run deterministic repeatability check. These are **software function checks** and are **not** a new evaluation of the full manuscript cohorts.

The full manuscript metrics depend on separately governed cohort definitions, authorized source data, frozen predictions, and analysis workflows **not distributed here**. Source availability alone does not establish weight availability or reproduce the published results without the requisite data and approvals.

## Data, checkpoint and publication status

- **MIMIC-IV-ECG/MIMIC-IV:** obtain directly via [PhysioNet](https://physionet.org/) under applicable credentialing and data-use requirements. Data are **not mirrored here**.
- **EchoNext:** independent external evaluation followed the source dataset's applicable access/use requirements; its harmonization and analysis pipeline are **not** part of this single-record CLI.
- **Weights:** not distributed. Potential distribution of a compact checkpoint depends on author, institutional and third-party permissions.
- **Original study repository:** maintained separately and not mirrored by this public source-only repository.
- **Manuscript:** under review; journal acceptance, final DOI, and publisher-endorsed reproducibility have **not** been claimed.

See [availability details](docs/AVAILABILITY.md) before attempting to redistribute code, data, or weights.

## Citation

For the scientific model, please cite the manuscript **when a definitive publication record is available**. The title is:

> Hussain I., Boyer R., Armoundas A. A., Scarpa J. R. *Morphology-aware deep learning for ECG-derived age estimation and its association with postoperative outcomes.* Manuscript under review.

For repository metadata, see [CITATION.cff](CITATION.cff). Do not invent a journal reference, DOI, or accepted status while review is ongoing.

## License and intended use

**No open-source license is currently granted for this repository.** Public visibility does not, by itself, confer redistribution, modification or commercial-use permission. The authors may add an appropriate license following institutional review.

**Research and educational inspection only. Not a medical device; not for diagnosis, treatment selection, perioperative risk stratification, or individual biological-age interpretation.**
