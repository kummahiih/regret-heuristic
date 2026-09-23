#!/usr/bin/env python3
"""Talker-count m-hat on dummy walks. Uncertainty log. Not in L.

m-hat = how many singular values of stacked h carry energy above tau.
1-source cloud vs 2-source cloud. Not ICA. Not Qwen. Not a camera.
"""

from __future__ import annotations

import torch
import torch.nn.functional as F


def source_count(H: torch.Tensor, rel: float = 0.05) -> int:
    """H: (n, d). Count singular values >= rel * s_max."""
    s = torch.linalg.svdvals(H)
    if s.numel() == 0 or float(s[0]) <= 0:
        return 0
    return int((s >= rel * s[0]).sum().item())


def main() -> None:
    torch.manual_seed(0)
    n, d = 32, 8
    v1 = F.normalize(torch.randn(d), dim=0)
    v2 = F.normalize(torch.randn(d), dim=0)
    v2 = F.normalize(v2 - v1 * torch.dot(v2, v1), dim=0)

    one = v1.unsqueeze(0) + 0.02 * torch.randn(n, d)
    two = torch.cat(
        [
            v1.unsqueeze(0) + 0.02 * torch.randn(n // 2, d),
            v2.unsqueeze(0) + 0.02 * torch.randn(n - n // 2, d),
        ],
        dim=0,
    )
    m_one = source_count(one)
    m_two = source_count(two)
    L_task, L_reg = 0.5, 0.0
    print("=== Source count dummy. m_hat not in L. ===")
    print(f"m_hat_1source={m_one} m_hat_2source={m_two}")
    print(f"L_task={L_task:.4f} L_reg={L_reg:.4f} L_total={L_task + L_reg:.4f}")
    print("L_total same for both clouds. Crowded hallway is not the slap.")
    print("Not Qwen. Not ICA. Not r.")


if __name__ == "__main__":
    main()
