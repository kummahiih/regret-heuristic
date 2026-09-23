#!/usr/bin/env python3
"""Learn D from train-topic deceptive leftovers. Held-out topic never builds D.

CPU dummy. Not Qwen. Not z in the loss.
Random-prototype baseline: same K, same dim, no labels.
"""

from __future__ import annotations

import torch
import torch.nn.functional as F


def hinge(r: torch.Tensor, bank: torch.Tensor, tau: float) -> torch.Tensor:
    r_n = F.normalize(r, dim=-1, eps=1e-12)
    p_n = F.normalize(bank, dim=-1, eps=1e-12)
    return F.relu((r_n @ p_n.T).max(dim=-1).values - tau)


def main() -> None:
    torch.manual_seed(0)
    d, tau, n_per, n_topics = 8, 0.3, 4, 4
    topics = [f"t{i}" for i in range(n_topics)]
    plan = F.normalize(torch.randn(d), dim=0)
    topic_mu = F.normalize(torch.randn(n_topics, d), dim=-1)
    rows = []
    for i, t in enumerate(topics):
        for _ in range(n_per):
            noise = 0.05 * torch.randn(d)
            hon = F.normalize(topic_mu[i] + noise, dim=0)
            dec = F.normalize(topic_mu[i] + 0.4 * plan + noise, dim=0)
            rows.append((t, "honest", hon))
            rows.append((t, "deceptive", dec))

    hold = topics[-1]
    train = [r for r in rows if r[0] != hold]
    test = [r for r in rows if r[0] == hold]
    learned = []
    for t in topics[:-1]:
        learned.append(torch.stack([h for tt, s, h in train if tt == t and s == "deceptive"]).mean(0))
    D_learn = torch.stack(learned)
    D_rand = torch.randn_like(D_learn)

    def report(name, bank):
        dec = hinge(torch.stack([h for _, s, h in test if s == "deceptive"]), bank, tau)
        hon = hinge(torch.stack([h for _, s, h in test if s == "honest"]), bank, tau)
        print(
            f"{name} hold={hold} "
            f"L_reg_dec={float(dec.mean()):.4f} L_reg_hon={float(hon.mean()):.4f} "
            f"gap={float(dec.mean() - hon.mean()):.4f} K={bank.shape[0]}"
        )

    print("=== Learned D vs random D. Held-out topic not in D. Dummy vectors. ===")
    print(f"train_topics={topics[:-1]} n_train={len(train)} n_test={len(test)}")
    report("learned", D_learn)
    report("random ", D_rand)
    print("z not in L. Tags built D on train only. Not a camera. Not Qwen.")


if __name__ == "__main__":
    main()
