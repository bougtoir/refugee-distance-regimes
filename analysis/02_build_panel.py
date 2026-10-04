#!/usr/bin/env python3
"""Harmonize licensed UNHCR MDL waves into the common panel schema.

Each dataset reader maps its native column names onto SCHEMA; anything
non-empty left unmapped aborts the build (strict-manifest rule).
Currently ships the schema + reader stubs: fill reader bodies once the
licensed files exist under data/raw/mdl/<catalog_id>/.
"""
import pathlib, sys
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
MDL = ROOT / "data" / "raw" / "mdl"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

SCHEMA = ["hhid", "wave", "survey_round", "country_int", "region_int",
          "oblast_origin", "settlement_raw", "edu_level", "prewar_activity",
          "home_owner_ua", "hh_size", "child_prop", "age", "sex",
          "disability", "sep_family", "prior_idp", "relatives_abroad",
          "left_ukr_ym", "arrived_ym", "transit_c1", "transit_c2",
          "transit_c3", "transit_c4", "transit_c5", "dest_reason",
          "return_intent", "onward_dest", "weight"]

# catalog_id -> reader function. Readers return a DataFrame with SCHEMA cols.
READERS = {}  # e.g. 839: read_ppm_r1, 959: read_ppm_r3, ...

def read_any(path):
    if path.suffix == ".csv": return pd.read_csv(path)
    if path.suffix in (".sav",): return pd.read_spss(path)
    if path.suffix in (".dta",): return pd.read_stata(path, convert_categoricals=False)
    raise ValueError(path)

SES_SOURCES = ["edu_level", "prewar_activity", "home_owner_ua"]

def derive_ses_index(panel):
    """Composite SES proxy: row-mean of per-indicator z-scores.

    Each indicator is coerced to numeric when possible, otherwise ranked by
    factorized category order. Non-varying indicators are dropped. Rows with
    no available indicator get NaN (models then exclude them by dropna).
    Per-indicator vs index-vs-latent-factor comparisons live in the
    robustness plan (R1-R3); this is the pre-registered baseline index.
    """
    zs = []
    for c in SES_SOURCES:
        if c not in panel:
            continue
        s = pd.to_numeric(panel[c], errors="coerce")
        if s.isna().all():
            s = pd.Series(pd.factorize(panel[c])[0],
                          index=panel.index, dtype="float")
            s[s < 0] = pd.NA
        if s.notna().sum() < 10 or s.std(skipna=True) == 0:
            continue
        zs.append((s - s.mean())/s.std())
    if not zs:
        panel["ses_index"] = pd.NA
    else:
        panel["ses_index"] = pd.concat(zs, axis=1).mean(axis=1)
    return panel

def main():
    frames = []
    for cid, reader in READERS.items():
        d = MDL / str(cid)
        if not d.exists():
            print(f"[skip] catalog {cid}: no files"); continue
        frames.append(reader(d))
    if not frames:
        print("No MDL data yet — schema emitted to data/processed/panel_schema.csv")
        pd.DataFrame(columns=SCHEMA).to_csv(OUT / "panel_schema.csv", index=False)
        return 0
    panel = pd.concat(frames, ignore_index=True)
    for c in SCHEMA:
        assert c in panel.columns, f"missing {c}"
    panel = derive_ses_index(panel)
    panel.to_csv(OUT / "panel.csv", index=False)
    print(f"panel: {len(panel)} rows -> {OUT/'panel.csv'}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
