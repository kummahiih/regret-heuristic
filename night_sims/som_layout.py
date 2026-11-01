#!/usr/bin/env python3
"""SOM expected-vs-measured layout diagnostic.
Promoted to protocol only if a node/prototype passes the topic-transfer gate.

Prototype only. --smoke runs on synthetic data. Neighborhood is true 2-D Euclidean.
"""
import argparse, torch
from collections import Counter

class MiniSOM:
    def __init__(self, m, n, dim, sigma=1.5, lr=0.3, steps=20):
        self.m, self.n = m, n
        self.weights = torch.randn(m, n, dim)
        self.sigma, self.lr, self.steps = sigma, lr, steps
    def winners(self, X):
        # X: (N, dim) -> (N,) flat indices
        d = ((X.unsqueeze(1).unsqueeze(1) - self.weights.unsqueeze(0))**2).sum(-1)
        return d.view(X.shape[0], -1).argmin(dim=1)
    def train(self, X):
        coords = torch.stack(torch.meshgrid(
            torch.arange(self.m), torch.arange(self.n), indexing="ij"
        ), dim=-1).float()  # (m, n, 2)
        for _ in range(self.steps):
            for x in X:
                # winner
                dist2 = ((self.weights - x)**2).sum(-1)
                i, j = divmod(int(dist2.argmin()), self.n)
                # 2-D Euclidean neighborhood
                delta = coords - torch.tensor([i, j], dtype=torch.float)
                dist = delta.norm(dim=-1)
                neigh = (dist < self.sigma).float()
                self.weights += (
                    self.lr * neigh.unsqueeze(-1) * (x - self.weights)
                    * (1 - dist.unsqueeze(-1) / self.sigma).clamp(min=0)
                )

def purity(assign, labels):
    n = len(labels)
    pure = 0
    for k in set(assign.tolist()):
        labs = [labels[i] for i in range(n) if assign[i] == k]
        if labs:
            pure += Counter(labs).most_common(1)[0][1]
    return pure / n

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if args.smoke:
        X = torch.randn(30, 8)
        labels = [i % 3 for i in range(30)]
        som = MiniSOM(3, 3, 8)
        som.train(X)
        assign = som.winners(X)
        print("som purity", purity(assign, labels))
        print("smoke ok — prototype only, 2-D neighborhood")
    else:
        print("no real activation loader yet; use --smoke")
