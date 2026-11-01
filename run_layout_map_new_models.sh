#!/usr/bin/env bash
# Expected vs measured room layout on the three new instruct models.
# Diagnostic only. Not a camera. Do not fill D.
set -u
cd "$(dirname "$0")"
mkdir -p results
LOG="results/layout-map-new-models-$(date +%Y-%m-%d).log"
: >"$LOG"

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python3 "$@" 2>&1 | tee -a "$LOG" || echo "FAILED $*" | tee -a "$LOG"
}

SPECS=(
  "llama8it|meta-llama/Llama-3.1-8B-Instruct|8"
  "gemma2bit|google/gemma-2-2b-it|8"
  "gemma9bit|google/gemma-2-9b-it|10"
)

for spec in "${SPECS[@]}"; do
  name=${spec%%|*}
  rest=${spec#*|}
  model=${rest%|*}
  layer=${rest##*|}
  run night_sims/som_layout_run.py --model "$model" --layer "$layer" \
    --dump "results/layout_map_${name}.json"
done

echo "log=$LOG"
echo "Read purity, NMI, ARI. Compare to the topic-shuffle null."
echo "Not a camera. Not a claim that SOM nodes are rooms. Do not fill D."
