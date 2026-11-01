#!/usr/bin/env python3
"""Brief smoke: load tiny random data, check probe_run imports and hinge math. No model."""
import json, torch, torch.nn.functional as F
from pathlib import Path

def hinge(vec, bank, tau):
    v = F.normalize(vec.unsqueeze(0), dim=-1)
    b = F.normalize(bank, dim=-1)
    return max(float((v @ b.T).max().clamp(-1,1)), 0.0)  # simplified

print("smoke hinge ok", hinge(torch.randn(16), torch.randn(4,16), 0.0))
print("CUDA available:", torch.cuda.is_available())
print("smoke done")
