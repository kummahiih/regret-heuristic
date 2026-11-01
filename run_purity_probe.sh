#!/usr/bin/env bash
# Purity-law diagnostic on existing residual caches.
# Looks in both repos. Extracts labels from scenario dumps.
# Not a camera. Not handoverPass. Do not fill D.
set -u
cd "$(dirname "$0")"
mkdir -p results
LOG="results/purity-probe-$(date +%Y-%m-%d).log"
: >"$LOG"

INTENT="$HOME/dockers/intent-readout-search"

# name|dump|activations
SPECS=(
  "qwen|$INTENT/results/scenario_qwen_2026-10-12-0031.jsonl|$INTENT/results/prebutton_qwen_L-1.npy"
  "mistral|$INTENT/results/scenario_mistral_2026-10-12-0031.jsonl|$INTENT/results/prebutton_mistral_L-1.npy"
  "llama8it|$INTENT/results/scenario_llama8it_2026-11-01.jsonl|$INTENT/results/prebutton_llama8it_2026-11-01_L-1.npy"
  "gemma2bit|$INTENT/results/scenario_gemma2bit_2026-11-01.jsonl|$INTENT/results/prebutton_gemma2bit_2026-11-01_L-1.npy"
  "gemma9bit|$INTENT/results/scenario_gemma9bit_2026-11-01.jsonl|$INTENT/results/prebutton_gemma9bit_2026-11-01_L-1.npy"
)

extract_labels() {
  local dump="$1" out="$2"
  python3 - "$dump" "$out" << 'PY'
import json, sys, numpy as np
dump, out = sys.argv[1], sys.argv[2]
ys = []
with open(dump) as f:
    for line in f:
        d = json.loads(line)
        if d.get("arm") != "public" or d.get("button") not in ("YES", "NO"):
            continue
        ys.append(1 if d["button"] == "YES" else 0)
np.save(out, np.array(ys))
print(f"wrote {len(ys)} labels to {out}")
PY
}

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python3 "$@" 2>&1 | tee -a "$LOG" || echo "FAILED $*" | tee -a "$LOG"
}

for spec in "${SPECS[@]}"; do
  name=${spec%%|*}
  rest=${spec#*|}
  dump=${rest%%|*}
  acts=${rest##*|}

  if [[ ! -f "$dump" || ! -f "$acts" ]]; then
    echo "skip $name: missing $dump or $acts" | tee -a "$LOG"
    continue
  fi
  labels="results/purity_labels_${name}.npy"
  extract_labels "$dump" "$labels" | tee -a "$LOG"
  run night_sims/purity_probe.py --activations "$acts" --labels "$labels" --alpha 1.0
done

echo "log=$LOG"
echo "Read s, alpha_star, underpowered. Do not average."
echo "Not a camera. Not handoverPass. Do not fill D."
