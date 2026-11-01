#!/usr/bin/env bash
# Paired baseline comparison.
# Needs prediction arrays. Not a camera. Not handoverPass. Do not fill D.
set -u
cd "$(dirname "$0")"
mkdir -p results
LOG="results/paired-baseline-$(date +%Y-%m-%d).log"
: >"$LOG"

echo "paired baseline. McNemar and bootstrap. not a camera. Do not fill D." | tee -a "$LOG"
echo "needs probe, note, both, labels npy files. not a camera." | tee -a "$LOG"

# placeholder: the prediction arrays do not yet exist
echo "skip: prediction arrays not yet extracted" | tee -a "$LOG"
echo "log=$LOG"
echo "Not a camera. Not handoverPass. Do not fill D."
