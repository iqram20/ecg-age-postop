# ECG-Age — standalone inference source

A minimal, self-contained **research-only** command-line implementation for estimating ECG-derived age from a standard 12-lead WFDB electrocardiogram using the frozen morphology-aware CNN–TCN–Transformer architecture.

**This repository publishes inference source code only, not a trained checkpoint.** A separately authorized compatible compact checkpoint is required for actual predictions. This source release does not include clinical datasets, patient predictions, training pipelines, postoperative outcome analysis, or reviewer materials.

## What's included

- `src/model.py` — frozen model architecture (3,532,674 trainable parameters)
- `src/preprocessing.py` — inference preprocessing: mean-centered physical leads and first temporal derivatives
- `scripts/infer_single.py` — WFDB single-record inference
- `scripts/validate_standalone.py` — synthetic preprocessing/architecture test; optional local checkpoint CPU forward-pass test
- `configs/inference.json` — input contract and frozen normalization metadata
- `requirements.txt` — recorded runtime dependency versions

## Requirements and setup

Python 3.10 is the tested Athena environment. The requirement versions reflect the original environment; installing on a different OS or accelerator may require a compatible PyTorch wheel.

```bash
git clone https://github.com/iqram20/ecg-age-postop.git
cd ecg-age-postop
python -m pip install -r requirements.txt
python scripts/validate_standalone.py
```

The synthetic check does **not** require model weights or patient data.

## Input

Use an authorized 10-second WFDB record with exactly **12 physical leads** (I, II, III, aVR, aVL, aVF, V1–V6), **500 Hz**, and **5,000 samples**. Both the `.hea` and `.dat` files must be present; pass the record stem without the extension.

The script verifies the lead set and reorders the channels, mean-centers each physical lead **without amplitude normalization**, and concatenates the first time difference for a `[1, 24, 5000]` input. It does **not** resample input signals.

## Run inference (with a locally authorized checkpoint)

```bash
python scripts/validate_standalone.py \
  --checkpoint /secure/path/to/ecg_age_frozen_inference.pt

python scripts/infer_single.py \
  --checkpoint /secure/path/to/ecg_age_frozen_inference.pt \
  --wfdb-record /secure/path/to/authorized_record \
  --device cpu \
  --json
```

The output includes the predicted ECG-derived age in years, normalized output, normalizing mean/SD, device, and checkpoint SHA-256. Predictions require **external approved weights** and are not possible from this code alone.

Frozen inverse normalization: `age_years = model_output * 20.83683569742911 + 55.045702521873395`.

## Verification scope

The source pipeline previously passed synthetic input tests and CPU checkpoint forward testing in its controlled research environment. A previously authorized single-record ECG prediction was deterministic across three CPU runs. Those tests are **functional checks**, not independent reproduction of cohort-wide study metrics on a new installation.

## Data protection and model availability

No model weights, waveform files, identifiable records, cohort manifests, internal analysis scripts, or private manuscript/reviewer files are distributed here. The absence of a checkpoint is intentional. The availability, reuse rights, and possible later distribution of weights are subject to author, institutional, and third-party dataset/weight restrictions. Do **not** commit private patient data or any checkpoint unless separately authorized.

This research model is not a validated patient-level biological-age measurement and must not be used for diagnosis, treatment, or perioperative decisions.
