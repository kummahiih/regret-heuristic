#!/usr/bin/env python3
"""SOM expected-vs-measured layout diagnostic.
Promoted to protocol only if a node/prototype passes the topic-transfer gate.
"""
import argparse, torch
from collections import Counter

class MiniSOM:
    def __init__(self, m, n, dim, sigma=1.5, lr=0.3, steps=20):
        self.m, self.n = m, n
        self.weights = torch.randn(m * n, dim)
        self.sigma, self.lr, self.steps = sigma, lr, steps
    def winners(self, X):
        # (N, nodes)
        d = ((X.unsqueeze(1) - self.weights.unsqueeze(0))**2).sum(-1)
        return d.argmin(dim=1)
    def train(self, X):
        for _ in range(self.steps):
            for x in X:
                idx = int(((self.weights - x)**2).sum(-1).argmin())
                # crude neighborhood
                for j in range(self.weights.shape[0]):
                    dist = abs(j - idx) / max(self.m, self.n)
                    if dist < self.sigma:
                        self.weights[j] += self.lr * (x - self.weights[j]) * (1 - dist/self.sigma)

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
        print("smoke ok — diagnostic only until gate")
