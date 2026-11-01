#!/usr/bin/env bash
# Higher-n OT rooms. n=16. Continues on failure.
# Not a camera. Do not fill D.
set -u
cd "$(dirname "$0")"
mkdir -p results
LOG="results/ot-high-n-$(date +%Y-%m-%d).log"
: >"$LOG"

MODELS_ROOTS=(
  "$HOME/dockers/regret-heuristic/models"
  "$HOME/dockers/intent-readout-search/models"
)

SPECS=(
  "qwen|Qwen2.5-7B-Instruct|Qwen/Qwen2.5-7B-Instruct"
  "mistral|Mistral-7B-Instruct-v0.3|mistralai/Mistral-7B-Instruct-v0.3"
  "aya8|aya-expanse-8b|CohereForAI/aya-expanse-8b"
  "gemma3|gemma-3-4b-it|google/gemma-3-4b-it"
  "falcon3|Falcon3-7B-Instruct|tiiuae/Falcon3-7B-Instruct"
  "granite|granite-4.2-8b|ibm-granite/granite-4.2-8b"
  "qwen35|Qwen3.5-9B|Qwen/Qwen3.5-9B"
  "llama8it|meta-llama/Llama-3.1-8B-Instruct|meta-llama/Llama-3.1-8B-Instruct"
  "gemma2bit|google/gemma-2-2b-it|google/gemma-2-2b-it"
  "gemma9bit|google/gemma-2-9b-it|google/gemma-2-9b-it"
)

weights_ok() {
  local d="$1"
  [[ -d "$d" ]] || return 1
  python3 - "$d" << 'PY'
import json, sys
from pathlib import Path
d = Path(sys.argv[1])
idx = d / "model.safetensors.index.json"
if idx.is_file():
    shards = set(json.loads(idx.read_text()).get("weight_map", {}).values())
    missing = [s for s in shards if not (d / s).is_file()]
    sys.exit(1 if missing else 0)
sys.exit(0 if list(d.glob("*.safetensors")) or list(d.glob("*.bin")) else 1)
PY
}

first_dir() {
  local c
  for c in "$@"; do
    weights_ok "$c" || continue
    echo "$c"
    return 0
  done
  return 1
}

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python3 "$@" 2>&1 | tee -a "$LOG" || echo "FAILED $*" | tee -a "$LOG"
}

for spec in "${SPECS[@]}"; do
  name=${spec%%|*}
  rest=${spec#*|}
  localdir=${rest%%|*}
  hfid=${rest##*|}

  path=""
  for root in "${MODELS_ROOTS[@]}"; do
    cand="$root/$localdir"
    echo "  check $cand" | tee -a "$LOG"
    path=$(first_dir "$cand") || true
    [[ -n "$path" ]] && break
  done
  if [[ -z "$path" ]]; then
    path="$hfid"
    echo "USE $name hf=$hfid (no local weights)" | tee -a "$LOG"
  else
    echo "USE $name path=$path" | tee -a "$LOG"
  fi

  run night_sims/ot_rooms.py --model "$path" --n-samples 16 --tau 0.5 \
    --dump "results/ot_high_n_${name}.jsonl"
done

echo "log=$LOG"
echo "Read mass, in_room, ot. Do not average."
echo "Not a camera. Do not fill D."
