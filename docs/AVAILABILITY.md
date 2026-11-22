# Code, data and checkpoint availability

**Scope:** Public *inference source* companion; not a mirror of the complete study.

## Available here

- Frozen 24-channel CNN–TCN–Transformer architecture.
- Frozen inference preprocessing and single-record WFDB CLI.
- Inference configuration and target-normalization metadata.
- Synthetic software checks and checkpoint compatibility checks.

## Not distributed

- Trained checkpoint or optimizer/training states.
- Protected or credentialed MIMIC-IV-ECG/MIMIC-IV waveform or clinical data.
- EchoNext waveform or participant-level data.
- Study splits, participant IDs, predicted individual-level ages or outcomes.
- Model-development scripts, feature extraction across study cohorts, clinical-outcome analysis, statistical analysis and figure-generation pipelines.
- Internal audit, reviewer response and manuscript drafts.

## Source access and permissions

The underlying MIMIC-IV-ECG/MIMIC-IV data must be obtained from [PhysioNet](https://physionet.org/) under applicable access requirements. External EchoNext use is governed by that dataset's conditions. Public repository access does not supersede source dataset agreements.

The trained compact checkpoint is not available for public download here. Its potential distribution is contingent on author and institutional approval and applicable rights. **Do not commit weights** or redistribute a checkpoint merely because the architecture is public.

This repository is public for inspection, but **no license grant has been issued**; public access should not be interpreted as permission to redistribute, modify or commercialize code.

## Relationship to the manuscript

The current under-review manuscript's Code Availability statement describes the original research repository as access-controlled and anticipates a limited release subject to approval. **This separate repository is a source-only companion and does not fulfill the manuscript's contemplated checkpoint distribution.** The final manuscript statement should be reconciled with the eventual authorized release *before publication*, without implying a model checkpoint is already public.

The manuscript's performance estimates were obtained through separate frozen study pipelines. A source-only smoke test does not reproduce the study or establish clinical validity.

## Responsible use

This software estimates ECG-derived age, not biological age, clinical disease status, or postoperative risk. It is not intended for medical decisions.
