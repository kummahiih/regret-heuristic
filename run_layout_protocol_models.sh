#!/usr/bin/env bash
# Layout diagnostic on the original protocol models.
# HF names. Continues on failure. Not a camera. Do not fill D.
set -u
cd "$(dirname "$0")"
mkdir -p results
LOG="results/layout-protocol-models-$(date +%Y-%m-%d).log"
: >"$LOG"

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python3 "$@" 2>&1 | tee -a "$LOG" || echo "FAILED $*" | tee -a "$LOG"
}

# name|hf-id|layer  (layer ~0.3 depth, same rule as the 7B rows)
SPECS=(
  "qwen|Qwen/Qwen2.5-7B-Instruct|8"
  "mistral|mistralai/Mistral-7B-Instruct-v0.3|9"
  "aya8|CohereForAI/aya-expanse-8b|10"
  "gemma3|google/gemma-3-4b-it|8"
  "falcon3|tiiuae/Falcon3-7B-Instruct|8"
  "phi4|microsoft/Phi-4-mini-instruct|10"
  "granite|ibm-granite/granite-4.2-8b|12"
  "qwen35|Qwen/Qwen3.5-9B|10"
)

for spec in "${SPECS[@]}"; do
  name=${spec%%|*}
  rest=${spec#*|}
  model=${rest%|*}
  layer=${rest##*|}
  echo "===== $name $model layer=$layer =====" | tee -a "$LOG"
  run night_sims/som_layout_run.py --model "$model" --layer "$layer" \
    --dump "results/layout_map_${name}.json"
  run night_sims/som_layout_complement.py --model "$model" --layer "$layer" \
    --dump "results/layout_complement_${name}.json"
done

echo "log=$LOG"
echo "Read purity. Compare to the topic-shuffle null."
echo "Not a camera. Do not fill D."
