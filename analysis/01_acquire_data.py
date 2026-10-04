#!/usr/bin/env python3
"""Verify/acquire inputs for the refugee-distance study.

Licensed UNHCR MDL microdata cannot be bulk-downloaded: the analyst places
files under data/raw/mdl/<catalog_id>/ after registering (see
DATA_DOWNLOAD_AND_BUILD_PLAN.md). This script records what exists, checksums
it into data/raw/ACQUISITION_LEDGER.csv, and downloads the open auxiliaries.
"""
import csv, hashlib, os, sys, urllib.request, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)
LEDGER = RAW / "ACQUISITION_LEDGER.csv"

REQUIRED_MDL = [839, 1031, 959, 1281, 1282, 783, 934, 1275, 1276]
OPTIONAL_MDL = [1342, 403, 406, 1453, 948, 1273, 1274, 854]

OPEN_AUX = {
    "macro/unhcr_ukr_origin_stock.csv":
        "https://data.humdata.org/dataset/6acc9e7f-d1f5-453f-b23b-1f8df7ae6533/"
        "resource/3799eae4-f77f-4496-a766-7c63d05b0480/download/"
        "end_year_population_totals_originating_ukr.csv",
    "macro/unhcr_ukr_origin_demographics.csv":
        "https://data.humdata.org/dataset/6acc9e7f-d1f5-453f-b23b-1f8df7ae6533/"
        "resource/de8f7315-ba84-47f4-baac-37743ab6d658/download/"
        "demographics_originating_ukr.csv",
    "geo/gadm41_UKR_1.json":
        "https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_UKR_1.json",
}
UA = {"User-Agent": "Mozilla/5.0"}

def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

def fetch(rel, url):
    dest = RAW / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 10000:
        print(f"  [have] {rel}"); return
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        f.write(r.read())
    print(f"  [get ] {rel} -> {dest.stat().st_size} bytes")

def main():
    print("Open auxiliaries:")
    for rel, url in OPEN_AUX.items():
        fetch(rel, url)
    missing, present = [], []
    for cid in REQUIRED_MDL + OPTIONAL_MDL:
        d = RAW / "mdl" / str(cid)
        files = list(d.glob("*")) if d.exists() else []
        (present if files else missing).append(cid)
    print(f"\nMDL datasets present: {present or 'none'}")
    print(f"MDL datasets MISSING: {missing}")
    if [c for c in REQUIRED_MDL if c in missing]:
        print("NOTE: required waves absent — download via MDL login before panel build.")

    # Ledger: fixed 10-column schema. Existing rows keep their curated
    # metadata; checksum rows only refresh size/sha256/acquired_utc so a
    # re-run never degrades a manually curated entry.
    COLS = ["file", "source_name", "source_url", "identifier_version",
            "acquired_utc", "acquisition_method", "license_or_terms",
            "notes", "size_bytes", "sha256"]
    existing = {}
    if LEDGER.exists():
        with open(LEDGER, newline="") as f:
            for row in csv.DictReader(f):
                existing[row["file"]] = row
    now = __import__("datetime").datetime.now(
        __import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for p in sorted(RAW.rglob("*")):
        if not p.is_file() or p.name == "ACQUISITION_LEDGER.csv":
            continue
        rel = str(p.relative_to(RAW))
        row = existing.get(rel, {c: "" for c in COLS})
        row["file"] = rel
        row["size_bytes"] = p.stat().st_size
        row["sha256"] = sha(p)
        if not row.get("acquired_utc"):
            row["acquired_utc"] = now
        if not row.get("acquisition_method"):
            row["acquisition_method"] = "local file (analyst-placed)"
        existing[rel] = row
    with open(LEDGER, "w", newline="") as f:
        w = csv.DictWriter(f, COLS)
        w.writeheader()
        w.writerows([existing[k] for k in sorted(existing)])
    print(f"ledger updated: {len(existing)} files")

if __name__ == "__main__":
    sys.exit(main())
