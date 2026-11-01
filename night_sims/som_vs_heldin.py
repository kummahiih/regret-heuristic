#!/usr/bin/env python3
"""Score SOM topic purity against the protocol held-in-topic gap.

Reads the SOM dumps already written and the protocol pair_contrast dumps
if they exist. Prints a table. Does not re-run models.

Not a camera. Do not fill D.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def load_jsonl(path):
    if not path.is_file():
        return []
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def main() -> int:
    print("som vs held-in: diagnostic only. Not a camera. Do not fill D.")
    root = Path("results")
    # SOM dumps from the first layout run
    som_files = sorted(root.glob("layout_map_*.json"))
    if not som_files:
        print("no layout_map dumps. run the layout diagnostic first.")
        return 1
    print(f"som dumps={len(som_files)}")
    for f in som_files:
        row = json.loads(f.read_text())
        print(f"  {f.name} n_topic={row.get('n_topic')} null={row.get('null_purity_mean')}")
    # protocol held-in dumps, if present
    proto = Path("../intent-readout-search/results")
    if not proto.is_dir():
        print("no protocol results tree. skip held-in comparison.")
        return 0
    held = sorted(proto.glob("pair_contrast_*.jsonl"))
    print(f"protocol dumps={len(held)}")
    for f in held[:5]:
        rows = load_jsonl(f)
        if not rows:
            continue
        gaps = [r.get("held_in_gap") for r in rows if "held_in_gap" in r]
        if gaps:
            print(f"  {f.name} n={len(gaps)} mean_gap={sum(gaps)/len(gaps):.3f}")
    print("Not a camera. Do not fill D.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
