#!/usr/bin/env bash
# Layout diagnostic on the original protocol models.
# Prefer local weights (MODELS_ROOT or HF cache). HF name is the fallback.
# Continues on failure. Not a camera. Do not fill D.
set -u
cd "$(dirname "$0")"
mkdir -p results
LOG="results/layout-protocol-models-$(date +%Y-%m-%d).log"
: >"$LOG"

# Where the intent-readout-search models/ tree lives.
# Example: MODELS_ROOT=../intent-readout-search/models
# Default: sibling intent-readout-search/models, or set MODELS_ROOT.
MODELS_ROOT="${MODELS_ROOT:-$HOME/dockers/intent-readout-search/models}"
HF="${HF_HOME:-${HF_HUB:-/media/pauli/datapata/hf}}/hub"
# also check the intent-readout-search HF cache if HF_HOME is unset
if [[ -z "${HF_HOME:-}" && -d "/media/pauli/datapata/hf/hub" ]]; then
  HF="/media/pauli/datapata/hf/hub"
fi

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

# name|local-subdir|hf-id|layer
SPECS=(
  "qwen|Qwen2.5-7B-Instruct|Qwen/Qwen2.5-7B-Instruct|8"
  "mistral|Mistral-7B-Instruct-v0.3|mistralai/Mistral-7B-Instruct-v0.3|9"
  "aya8|aya-expanse-8b|CohereForAI/aya-expanse-8b|10"
  "gemma3|gemma-3-4b-it|google/gemma-3-4b-it|8"
  "falcon3|Falcon3-7B-Instruct|tiiuae/Falcon3-7B-Instruct|8"
  "phi4|Phi-4-mini-instruct|microsoft/Phi-4-mini-instruct|10"
  "granite|granite-4.2-8b|ibm-granite/granite-4.2-8b|12"
  "qwen35|Qwen3.5-9B|Qwen/Qwen3.5-9B|10"
)

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python3 "$@" 2>&1 | tee -a "$LOG" || echo "FAILED $*" | tee -a "$LOG"
}

for spec in "${SPECS[@]}"; do
  name=${spec%%|*}
  rest=${spec#*|}
  localdir=${rest%%|*}
  rest=${rest#*|}
  hfid=${rest%%|*}
  layer=${rest##*|}

  path=""
  if [[ -n "$MODELS_ROOT" ]]; then
    path=$(first_dir "$MODELS_ROOT/$localdir") || true
  fi
  if [[ -z "$path" ]]; then
    # HF cache snapshots
    for snap in "$HF"/models--*/snapshots/*; do
      [[ -d "$snap" ]] || continue
      if [[ "$(basename "$(dirname "$(dirname "$snap")")")" == *"${localdir}"* ]]; then
        path=$(first_dir "$snap") || true
        [[ -n "$path" ]] && break
      fi
    done
  fi
  if [[ -z "$path" ]]; then
    path="$hfid"
    echo "USE $name hf=$hfid (no local weights)" | tee -a "$LOG"
  else
    echo "USE $name path=$path layer=$layer" | tee -a "$LOG"
  fi

  run night_sims/som_layout_run.py --model "$path" --layer "$layer" \
    --dump "results/layout_map_${name}.json"
  run night_sims/som_layout_complement.py --model "$path" --layer "$layer" \
    --dump "results/layout_complement_${name}.json"
done

echo "log=$LOG"
echo "Read purity. Compare to the topic-shuffle null."
echo "Not a camera. Do not fill D."
