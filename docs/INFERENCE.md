# Running the ECG-Age standalone inference

This guide documents the **frozen** command-line workflow. It does not retrain, fine-tune, recalibrate, or evaluate the clinical study.

## 1. Installation

Use a Python 3.10 environment and install the recorded dependencies:

```bash
git clone https://github.com/iqram20/ecg-age-postop.git
cd ecg-age-postop
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Other operating systems or accelerators may require an environment-appropriate PyTorch installation.

## 2. Synthetic smoke test — no weights required

```bash
python scripts/validate_standalone.py
```

When successful, the program emits a JSON object whose `status` is `PASS_SYNTHETIC_STANDALONE` and whose `clinical_accuracy_verified` is `false`.

The test checks core preprocessing shape, centering and derivative construction, normalization metadata, and architecture parameter count. It **does not test actual model accuracy**.

## 3. Input contract

Provide a locally authorized WFDB ECG record with:

| Requirement | Exact accepted value |
| --- | --- |
| Sampling rate | 500 Hz |
| Duration | 10 seconds |
| Samples | 5,000 per lead |
| Leads | I, II, III, aVR, aVL, aVF, V1–V6 |
| Signal | WFDB physical `p_signal` |
| Files | matching `.hea` and `.dat` |
| CLI path | record stem; a `.hea` or `.dat` suffix is also stripped |
| Input tensor | `[1, 24, 5000]` |

Lead names are normalized case-insensitively, and channels are reordered to canonical lead order. The code rejects unexpected lead sets, lengths and sample rates. Non-finite waveform entries are replaced with zero; missing leads are **not** synthesized. The script does **not** resample.

## 4. Frozen processing and architecture

1. Read the 12 physical ECG leads through `wfdb.rdrecord`.
2. Convert to float32 and replace non-finite values with zeros.
3. Mean-center each physical lead; **do not divide by standard deviation** or apply an arbitrary amplitude gain.
4. Compute the first-order temporal difference of each centered lead (first sample difference = 0).
5. Concatenate centered signals and derivatives to give 24 channels.
6. Run the trained CNN–TCN–Transformer in `eval()` mode.
7. Convert normalized age to years:

```text
ECG-derived age = normalized prediction × 20.83683569742911
                  + 55.045702521873395
```

The source checkpoint lineage is checked if the compact checkpoint includes a `source_checkpoint_sha256` field. The checkpoint is loaded with PyTorch's `weights_only=True` option; this is **not** a substitute for obtaining checkpoint files from a trusted authorized source.

## 5. Real ECG inference — external checkpoint required

This repository does **not** ship a trained checkpoint. With a compatible authorized compact checkpoint stored outside the Git checkout:

```bash
python scripts/validate_standalone.py \
  --checkpoint /secure/path/ecg_age_frozen_inference.pt

python scripts/infer_single.py \
  --checkpoint /secure/path/ecg_age_frozen_inference.pt \
  --wfdb-record /secure/path/to/record_stem \
  --device cpu \
  --json
```

The output contains the fields:

```json
{
  "predicted_ecg_age_years": 0.0,
  "normalized_model_output": 0.0,
  "age_mean": 55.045702521873395,
  "age_std": 20.83683569742911,
  "device": "cpu",
  "checkpoint_sha256": "sha256-of-your-local-checkpoint"
}
```

**This JSON is a field illustration, not a genuine predicted age or test result.**

For GPU inference, select `--device cuda` if CUDA and a suitable PyTorch installation are available. Cross-device bitwise identity is not guaranteed or claimed.

## 6. What has already been checked?

In the private study environment, the frozen standalone script passed the synthetic check, CPU checkpoint forward pass, and one authorized MIMIC-IV-ECG record. Three successive CPU inferences on that record yielded the same output (zero observed difference). This does not substitute for the study's full locked-test or external validation.

## 7. Common failures

- **`FileNotFoundError: ... .hea`** — path must point to a real WFDB record stem with adjacent header and data files.
- **Wrong rate/duration/leads** — this standalone CLI intentionally rejects unsupported records, rather than silently harmonizing them.
- **No checkpoint** — synthetic checks work without weights, real predictions do not.
- **Checkpoint mismatch** — use the compatible, separately authorized compact artifact corresponding to the frozen architecture and normalization.
- **PyTorch nested-tensor warning** — a nonfatal Transformer implementation warning was observed in the tested environment.

Do not paste or publish real WFDB data, identifiers, or patient-level JSON prediction outputs into public issues or commits.
