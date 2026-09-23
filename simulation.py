#!/usr/bin/env python3
"""Toy illustration of the prototype-hinge loss (NOT an alignment proof)."""

from __future__ import annotations

import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F


class DummyEncoder(nn.Module):
    def __init__(self, input_dim: int = 16, d: int = 8):
        super().__init__()
        self.proj = nn.Linear(input_dim, d, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.proj(x)


class DynamicDetector(nn.Module):
    def __init__(self, hidden_dim: int, intent_dim: int, K: int = 3, noise_sigma: float = 0.05):
        super().__init__()
        self.K = K
        self.noise_sigma = noise_sigma
        
        # The transition map (step function)
        self.step_net = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim)
        )
        
        # The final static readout
        self.readout = nn.Linear(hidden_dim, intent_dim)

    def forward(self, h: torch.Tensor) -> torch.Tensor:
        # h is the base activation from the model, shape: [batch, hidden_dim]
        state = h
        
        # The K-step Relaxation Loop
        for _ in range(self.K):
            noise = torch.randn_like(state) * self.noise_sigma if self.noise_sigma > 0 else 0.0
            state = state + self.step_net(state) + noise
            
        z_intent = self.readout(state)
        return z_intent


def regret_loss(
    h_intent: torch.Tensor,
    prototypes: torch.Tensor,
    tau: float = 0.3,
) -> torch.Tensor:
    h_n = F.normalize(h_intent, dim=-1, eps=1e-12)
    p_n = F.normalize(prototypes, dim=-1, eps=1e-12)
    s_star = (h_n @ p_n.T).max(dim=-1).values
    return F.relu(s_star - tau).mean()


def main() -> None:
    parser = argparse.ArgumentParser(description="Toy regret-heuristic simulation")
    parser.add_argument("--sensor", type=str, choices=["static", "deterministic", "stochastic"], default="static",
                        help="Sensor architecture to test evasion against.")
    args = parser.parse_args()

    # 1. FIXED GEOMETRY: Initialize data, prototypes, and base model with a strict seed
    # This guarantees the "far" (evasion) vectors and the task are mathematically identical across all runs.
    torch.manual_seed(0)
    input_dim, d, num_prototypes = 16, 8, 3
    tau = 0.3
    lambda_reg = 0.5
    
    encoder = DummyEncoder(input_dim=input_dim, d=d)
    task_head = nn.Linear(d, 2)
    prototypes = torch.randn(num_prototypes, d)
    prototypes.requires_grad_(False)
    
    with torch.no_grad():
        W = encoder.proj.weight
        pinvW = torch.linalg.pinv(W)
        near_h = F.normalize(prototypes[:2], dim=-1)
        Q, _ = torch.linalg.qr(prototypes.T)
        null = torch.randn(2, d)
        null = null - null @ Q @ Q.T
        far_h = F.normalize(null, dim=-1)  # Orthogonal to prototypes
        near_x = near_h @ pinvW.T
        far_x = far_h @ pinvW.T
        
    x = torch.cat([near_x, far_x], dim=0)
    B = x.shape[0]
    y = torch.randint(0, 2, (B,))

    # 2. SENSOR INITIALIZATION: Uses a separate seed so it doesn't shift the dataset.
    torch.manual_seed(42)
    if args.sensor == "static":
        detector = nn.Linear(d, d)
    elif args.sensor == "deterministic":
        detector = DynamicDetector(hidden_dim=d, intent_dim=d, K=3, noise_sigma=0.0)
    elif args.sensor == "stochastic":
        detector = DynamicDetector(hidden_dim=d, intent_dim=d, K=3, noise_sigma=0.01)

    # REVIEW FIX: The detector must be frozen to test evasion. 
    # If added to Adam, it will just learn to output zeros to minimize the hinge.
    detector.requires_grad_(False)
    
    # Optimizer only touches the base model
    params = list(encoder.parameters()) + list(task_head.parameters())
    opt = torch.optim.Adam(params, lr=1e-2)

    def compute_losses():
        h_base = encoder(x)
        L_task = F.cross_entropy(task_head(h_base), y)
        h_intent = detector(h_base)
            
        L_regret = regret_loss(h_intent, prototypes, tau=tau)
        L_total = L_task + lambda_reg * L_regret
        L_near = regret_loss(h_intent[:2], prototypes, tau=tau)
        L_far = regret_loss(h_intent[2:], prototypes, tau=tau)
        return h_intent, L_task, L_regret, L_total, L_near, L_far

    def report_split(L_task, L_regret):
        """Print encoder grads. Must not leave .grad for Adam."""
        opt.zero_grad(set_to_none=True)
        L_task.backward(retain_graph=True)
        g_task = float(encoder.proj.weight.grad.norm())
        opt.zero_grad(set_to_none=True)
        L_regret.backward(retain_graph=True)
        g_reg = float(encoder.proj.weight.grad.norm())
        opt.zero_grad(set_to_none=True)
        return g_task, g_reg

    h_intent, L_task, L_regret, L_total, L_near, L_far = compute_losses()
    g_task, g_reg = report_split(L_task, L_regret)
    L_total.backward()
    g_tot = float(encoder.proj.weight.grad.norm())
    
    print("=== Toy regret-heuristic simulation (A/B/C Controlled Evasion Test) ===")
    print(f"Sensor Mode: {args.sensor.upper()}")
    print(f"Batch size B={B}, input_dim={input_dim}, d={d}, K={getattr(detector, 'K', 0)}, tau={tau}")
    print(
        f"Before step: L_task={L_task.item():.4f}  L_regret={L_regret.item():.4f}  "
        f"L_total={L_total.item():.4f}"
    )
    print(f"  group L_near={L_near.item():.4f}  L_far={L_far.item():.4f} (Evasion gap)")
    print(
        f"  encoder grad norms: task={g_task:.6f}  hinge={g_reg:.6f}  total={g_tot:.6f}"
    )
    
    opt.step()
    opt.zero_grad(set_to_none=True)
    
    h_intent2, L_task2, L_regret2, L_total2, L_near2, L_far2 = compute_losses()
    g_task2, g_reg2 = report_split(L_task2, L_regret2)
    L_total2.backward()
    g_tot2 = float(encoder.proj.weight.grad.norm())
    
    print(
        f"After 1 Adam step: L_task={L_task2.item():.4f}  L_regret={L_regret2.item():.4f}  "
        f"L_total={L_total2.item():.4f}"
    )
    print(f"  group L_near={L_near2.item():.4f}  L_far={L_far2.item():.4f}")
    print(
        f"  encoder grad norms: task={g_task2:.6f}  hinge={g_reg2:.6f}  total={g_tot2:.6f}"
    )
    print("Script finished successfully. This is NOT evidence of alignment or deception detection.")

if __name__ == "__main__":
    main()