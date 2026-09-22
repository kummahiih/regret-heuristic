#!/usr/bin/env python3
"""Simulation of Failure Mode 2: Manifold Flattening against the Dynamic Detector."""

import torch
import torch.nn as nn
import torch.nn.functional as F

class DynamicDetector(nn.Module):
    def __init__(self, d: int, K: int = 3, noise_sigma: float = 0.01):
        super().__init__()
        self.K, self.noise_sigma = K, noise_sigma
        self.step_net = nn.Sequential(nn.Linear(d, d), nn.GELU(), nn.Linear(d, d))
        self.readout = nn.Linear(d, d)

    def forward(self, h: torch.Tensor) -> torch.Tensor:
        state = h
        for _ in range(self.K):
            noise = torch.randn_like(state) * self.noise_sigma
            state = state + self.step_net(state) + noise
        return self.readout(state)

def main():
    torch.manual_seed(42)
    d = 8
    
    # 1. The Detector is frozen (simulating a deployed or slow-moving sensor)
    detector = DynamicDetector(d)
    detector.requires_grad_(False)
    
    # 2. The Task Head is frozen (simulating standard task capability)
    task_head = nn.Linear(d, 2)
    task_head.requires_grad_(False)
    
    # 3. The Base Model (Optimizer) controls the latent representation h_base
    # It wants to solve the task (target class 1) AND hide from the detector (norm -> 0)
    h_base = nn.Parameter(torch.randn(1, d))
    target = torch.tensor([1])
    
    opt = torch.optim.Adam([h_base], lr=0.05)
    
    print("=== Adversarial Manifold Flattening ===")
    for step in [0, 50, 200]:
        h_intent = detector(h_base)
        
        L_task = F.cross_entropy(task_head(h_base), target)
        L_regret = h_intent.norm()  # Detector wants this high for evasion, model forces to 0
        L_total = L_task + L_regret
        
        print(f"Step {step:3d} | L_task: {L_task.item():.4f} | L_regret (Detector Signal): {L_regret.item():.4f}")
        print(f"          | Base Norm ||h_0||: {h_base.norm().item():.4f} | Intent Norm ||h_K||: {h_intent.norm().item():.4f}\n")
        
        if step < 200:
            for _ in range(50 if step == 0 else 150):
                h_intent = detector(h_base)
                loss = F.cross_entropy(task_head(h_base), target) + h_intent.norm()
                loss.backward()
                opt.step()
                opt.zero_grad()

if __name__ == "__main__":
    main()