#!/usr/bin/env bash
# Complementary layout diagnostic: ask-removal and wider role bank.
# Not a camera. Do not fill D.
set -u
cd "$(dirname "$0")"
mkdir -p results
LOG="results/layout-complement-$(date +%Y-%m-%d).log"
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
  run night_sims/som_layout_complement.py --model "$model" --layer "$layer" \
    --dump "results/layout_complement_${name}.json"
done

echo "log=$LOG"
echo "Read topic_with_ask vs topic_no_ask. Read role purity on the wider bank."
echo "Not a camera. Do not fill D."
