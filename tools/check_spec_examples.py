#!/usr/bin/env python3
"""Validate documentation examples against schema/qson.schema.json.

- every ```json fence in spec/*.md and README.md that is a complete event (has trace_id, run_id and sequence) is wrapped
  as a one-event trace and validated; fences that are complete traces (have "events") are validated as-is;
- every examples/*.qson file is validated.
Exit 1 on any error. Requires jsonschema>=4.20.
"""
import json, re, sys
from pathlib import Path
from jsonschema import Draft7Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
V = Draft7Validator(json.loads((ROOT / "schema" / "qson.schema.json").read_text()), format_checker=FormatChecker())
errors, checked = [], 0
for md in sorted([*ROOT.glob("spec/*.md"), ROOT / "README.md"]):
    for i, block in enumerate(re.findall(r"```json\n(.*?)```", md.read_text(encoding="utf-8"), re.S), 1):
        try:
            obj = json.loads(block)
        except json.JSONDecodeError:
            continue  # illustrative fragment, not a standalone JSON document
        if isinstance(obj, dict) and "events" in obj:
            doc = obj
        elif isinstance(obj, dict) and {"trace_id", "run_id", "sequence"} <= set(obj):
            doc = {"qson_version": "1.0", "run_id": obj["run_id"], "events": [obj]}
        else:
            continue
        checked += 1
        errors += [f"{md.relative_to(ROOT)} json fence #{i}: {list(e.absolute_path)} {e.message}" for e in V.iter_errors(doc)]
for ex in sorted(ROOT.glob("examples/*.qson")):
    checked += 1
    errors += [f"{ex.relative_to(ROOT)}: {list(e.absolute_path)} {e.message}" for e in V.iter_errors(json.loads(ex.read_text()))]
print(f"checked {checked} documents; {len(errors)} errors")
for e in errors: print("  -", e)
sys.exit(1 if errors else 0)
