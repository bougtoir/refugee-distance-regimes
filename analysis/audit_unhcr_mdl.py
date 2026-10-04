#!/usr/bin/env python3
"""Audit UNHCR Microdata Library datasets for the refugee-distance feasibility study.

Scrapes public catalog metadata (study description + data dictionary) for a
curated list of candidate datasets and emits a variable audit CSV. Microdata
themselves are licensed-access (free registration); we only read metadata.
"""
import csv, json, re, time, urllib.request, sys, pathlib

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
BASE = "https://microdata.unhcr.org/index.php/catalog/{cid}"
OUT = pathlib.Path(__file__).resolve().parents[1] / "results"
OUT.mkdir(exist_ok=True)

# Candidate datasets: (catalog_id, short label)
DATASETS = [
    (839, "UNHCR PPM May-Dec 2022 (multi-country file)"),
    (1031, "UNHCR PPM Oct 2022-Feb 2023"),
    (959, "UNHCR PPM Feb-Jun 2023"),
    (1281, "UNHCR PPM Oct 2023-Apr 2024"),
    (1282, "UNHCR PPM Jul-Oct 2024"),
    (854, "UNHCR Border Monitoring arrivals 2022"),
    (783, "UNHCR Intentions & Perspectives #2 Sep 2022"),
    (873, "UNHCR Intentions & Perspectives #3 Feb 2023"),
    (934, "UNHCR Intentions & Perspectives #4 Jun 2023"),
    (1064, "UNHCR Intentions & Perspectives 2023"),
    (1275, "UNHCR Intentions refugees #5 Feb 2024"),
    (1276, "UNHCR Intentions refugees #6 Aug 2024"),
    (976, "Access to Socio-Economic Rights TP holders 2023"),
    (948, "IDP intentions #2 May 2023"),
    (1273, "IDP intentions #3 Feb 2024"),
    (1274, "IDP intentions #4 Aug 2024"),
    (1214, "SEIS Jun/Jul 2024"),
]

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="ignore")

def strip(t):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)).strip()

rows = []
for cid, label in DATASETS:
    rec = {"catalog_id": cid, "dataset": label, "url": BASE.format(cid=cid)}
    try:
        h = get(BASE.format(cid=cid))
    except Exception as e:
        rec["error"] = str(e); rows.append(rec); continue
    m = re.search(r'id="dataset-title">.*?<span>(.*?)</span>', h, re.S)
    rec["title"] = strip(m.group(1)) if m else ""
    m = re.search(r'id="dataset-country">(.*?)</span>.*?id="dataset-year">(.*?)</span>', h, re.S)
    if m:
        rec["countries"] = strip(m.group(1)); rec["years"] = strip(m.group(2))
    # sample size mentions
    mm = re.findall(r"([0-9][0-9,\.]+)\s*(?:household|individual|interviews|respondents)", strip(h), re.I)
    rec["n_mentions"] = "; ".join(sorted(set(mm))[:5])
    # data dictionary: discover data files, then fetch variable lists per file
    try:
        names = []
        dd = get(BASE.format(cid=cid) + "/data-dictionary")
        files = sorted(set(re.findall(r'data-dictionary/([A-Za-z0-9_]+)\?file_name=', dd)))
        if not files:
            files = ["data"]
        for fn in files[:6]:
            try:
                d = get(BASE.format(cid=cid) + f"/data-dictionary/{fn}?file_name={fn}")
                vr = re.findall(r'class="var-id"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', d, re.S)
                names += [f"[{fn}] " + strip(t) for _, t in vr]
            except Exception:
                pass
            time.sleep(0.3)
        rec["n_vars"] = len(names)
        rec["variables"] = " || ".join(names)
        low = [n.lower() for n in names]
        def has(*pats):
            return any(any(p in v for p in pats) for v in low)
        rec["has_origin_oblast"] = has("oblast of origin", "region of origin", "region do you come from", "from which oblast")
        rec["has_destination"] = has("country of interview", "this country", "place of interview", "host country")
        rec["has_education"] = has("education")
        rec["has_prewar_activity"] = has("prior to leaving ukraine", "before leaving ukraine", "activity prior", "before the war", "prior to 24 february", "pre-war")
        rec["has_income_assets"] = has("income", "asset", "savings", "salar", "wage")
        rec["has_route"] = has("transit", "route", "travelled through", "other countries")
        rec["has_displacement_date"] = has("when did you leave", "leave ukraine", "left ukraine", "departure")
        rec["has_hh_comp"] = has("household", "children")
        rec["has_return_intent"] = has("return", "go back")
        rec["has_dest_reason"] = has("motivated you", "why this country", "come to this country", "destination")
    except Exception as e:
        rec["dd_error"] = str(e)
    rows.append(rec)
    time.sleep(0.5)

cols = ["catalog_id","dataset","title","countries","years","n_mentions","n_vars",
        "has_origin_oblast","has_destination","has_education","has_prewar_activity",
        "has_income_assets","has_route","has_displacement_date","has_hh_comp",
        "has_return_intent","has_dest_reason","url","variables","error","dd_error"]
with open(OUT / "unhcr_mdl_audit.csv", "w", newline="") as f:
    w = csv.DictWriter(f, cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
print(f"wrote {len(rows)} rows -> {OUT/'unhcr_mdl_audit.csv'}")
