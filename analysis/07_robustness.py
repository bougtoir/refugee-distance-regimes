#!/usr/bin/env python3
"""Robustness battery R1-R23 runner (see ROBUSTNESS_PLAN.md).

Each arm is a function returning a small dict of diagnostics; the table is
written to results/robustness_table.csv. Arms requiring absent columns or
files are recorded as 'skipped' — never silently omitted.
"""
import pathlib, sys
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROC, RES = ROOT/"data"/"processed", ROOT/"results"; RES.mkdir(exist_ok=True)

ARMS = [f"R{i}" for i in range(1, 24)]

def main():
    f = PROC/"panel_dist.csv"
    rows = []
    if not f.exists():
        for r in ARMS:
            rows.append({"arm": r, "status": "skipped", "reason": "panel absent"})
    else:
        df = pd.read_csv(f)
        for r in ARMS:
            rows.append({"arm": r, "status": "todo",
                         "reason": "implement per ROBUSTNESS_PLAN"})
    pd.DataFrame(rows).to_csv(RES/"robustness_table.csv", index=False)
    print(pd.DataFrame(rows).to_string())
    return 0

if __name__ == "__main__":
    sys.exit(main())
