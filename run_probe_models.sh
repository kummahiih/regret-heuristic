#!/usr/bin/env bash
# Probe run across the granted models. Continues on failure.
# 4-bit load is the default in probe_run.py.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p results
LOG="results/probe-models-$(date +%Y-%m-%d).log"
: >"$LOG"

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python3 probe_run.py --model "$1" 2>&1 | tee -a "$LOG" || echo "FAILED $1" | tee -a "$LOG"
}

# Access granted
run meta-llama/Llama-3.1-8B
run meta-llama/Llama-3.1-8B-Instruct
run google/gemma-2-2b
run google/gemma-2-2b-it
run google/gemma-2-9b-it

echo "log=$LOG"
echo "Not a strategy readout. Do not fill D."
