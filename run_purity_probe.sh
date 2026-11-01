#!/usr/bin/env bash
# Purity-law diagnostic on existing residual caches.
# Not a camera. Not handoverPass. Do not fill D.
set -u
cd "$(dirname "$0")"
mkdir -p results
LOG="results/purity-probe-$(date +%Y-%m-%d).log"
: >"$LOG"

# name|activations|labels|alpha
SPECS=(
  "qwen|results/prebutton_qwen_L-1.npy|results/prebutton_qwen_labels.npy|1.0"
  "mistral|results/prebutton_mistral_L-1.npy|results/prebutton_mistral_labels.npy|1.0"
  "llama8it|results/prebutton_llama8it_2026-11-01_L-1.npy|results/prebutton_llama8it_labels.npy|1.0"
  "gemma2bit|results/prebutton_gemma2bit_2026-11-01_L-1.npy|results/prebutton_gemma2bit_labels.npy|1.0"
  "gemma9bit|results/prebutton_gemma9bit_2026-11-01_L-1.npy|results/prebutton_gemma9bit_labels.npy|1.0"
)

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python3 "$@" 2>&1 | tee -a "$LOG" || echo "FAILED $*" | tee -a "$LOG"
}

for spec in "${SPECS[@]}"; do
  name=${spec%%|*}
  rest=${spec#*|}
  acts=${rest%%|*}
  rest2=${rest#*|}
  labels=${rest2%%|*}
  alpha=${rest2##*|}

  if [[ ! -f "$acts" || ! -f "$labels" ]]; then
    echo "skip $name: missing $acts or $labels" | tee -a "$LOG"
    continue
  fi
  run night_sims/purity_probe.py --activations "$acts" --labels "$labels" --alpha "$alpha"
done

echo "log=$LOG"
echo "Read s, alpha_star, underpowered. Do not average."
echo "Not a camera. Not handoverPass. Do not fill D."
