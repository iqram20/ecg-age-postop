#!/usr/bin/env python3
"""Standalone ECG-Age release gate. No patient data or training pipeline required.

Without --checkpoint, validates architecture, canonical leads, preprocessing,
and CLI dependencies using synthetic data. With --checkpoint, also verifies
checkpoint format, exact model parameters, and a CPU forward pass. Does not
claim clinical validation or repeat the manuscript test-set evaluation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.model import ECGAgeRegressor, count_trainable_parameters
from src.preprocessing import prepare_frozen_channels, fix_length
from scripts.infer_single import EXPECTED_PARAMETERS, load_model

LEADS = ("I","II","III","aVR","aVL","aVF","V1","V2","V3","V4","V5","V6")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--checkpoint",type=Path,help="Local approved compact inference checkpoint")
    args=parser.parse_args()
    metadata=json.loads((ROOT/"configs/inference.json").read_text())
    assert metadata["input"]["sampling_frequency_hz"]==500
    assert metadata["input"]["samples_per_lead"]==5000
    assert metadata["input"]["input_channels"]==24
    assert metadata["model"]["trainable_parameters"]==EXPECTED_PARAMETERS
    signal=torch.zeros((12,5000),dtype=torch.float32)
    signal[0]=torch.linspace(-1,1,5000)
    # Endpoint derivative must be zero, and mean centering physical-lead only.
    x=prepare_frozen_channels(signal)
    assert tuple(x.shape)==(24,5000)
    assert torch.allclose(x[:12].mean(dim=1),torch.zeros(12),atol=1e-6)
    assert x[12,0].item()==0.0
    assert torch.allclose(x[12,1:],x[0,1:]-x[0,:-1])
    assert tuple(fix_length(x).shape)==(24,5000)
    assert tuple(fix_length(x[:,:4700]).shape)==(24,5000)
    assert count_trainable_parameters(ECGAgeRegressor())==EXPECTED_PARAMETERS
    result={"status":"PASS_SYNTHETIC_STANDALONE",
            "expected_lead_order":list(LEADS),
            "input_shape":[1,24,5000],
            "parameter_count":EXPECTED_PARAMETERS,
            "checkpoint_test":"NOT_REQUESTED",
            "clinical_accuracy_verified":False}
    if args.checkpoint:
        model,mu,sd=load_model(args.checkpoint,torch.device("cpu"))
        assert np.isfinite(mu) and np.isfinite(sd) and sd>0
        with torch.inference_mode():
            y=model(x.unsqueeze(0))
        assert tuple(y.shape)==(1,) and torch.isfinite(y).all()
        result["checkpoint_test"]="PASS_CPU_FORWARD"
        result["checkpoint_path"]=args.checkpoint.name
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
