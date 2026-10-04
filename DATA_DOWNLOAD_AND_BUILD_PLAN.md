# DATA DOWNLOAD & BUILD PLAN

## Step 1 — register (human, once)

Create a free account at https://microdata.unhcr.org and request/download
("Get Microdata") each dataset below into `data/raw/mdl/<catalog_id>/`.
Typical format: .sav/.dta/.csv + documentation PDF.

Priority A (primary panel):
- 839  PPM May–Dec 2022 (route + IDP + diaspora fields)
- 1031 PPM Oct 2022–Feb 2023
- 959  PPM Feb–Jun 2023 (n≈21,340)
- 1281 PPM Oct 2023–Apr 2024
- 1282 PPM Jul–Oct 2024
- 783  Intentions #2 Sep 2022 (home ownership)
- 934  Intentions #4 Jun 2023 (home ownership + settlement)
- 1275 / 1276 Intentions #5/#6 2024

Priority B (external validation):
- 1342 Syria intentions Europe 2025
- 403/406 Syrian refugees & host communities 2015–16 (asset module)
- 1453 VASyR Lebanon 2025

Priority C (ladder/auxiliary):
- 948/1273/1274 IDP intentions
- IOM DTM GPS round tables (public reports) — population frame by oblast

## Step 2 — open auxiliaries (scripted, already acquired)

- `data/raw/macro/unhcr_ukr_origin_stock.csv` — UNHCR end-year stocks
  origin→asylum (85 destinations; destination-variation frame)
- `data/raw/macro/unhcr_ukr_origin_demographics.csv` — age/sex/location
  breakdown by asylum country
- `data/raw/geo/gadm41_UKR_1.json` — oblast boundaries (centroids)
- `data/raw/unhcr_mdl_docs/*.pdf` — questionnaires for 783/934/959/1282

## Step 3 — build

`python analysis/01_acquire_data.py` verifies placement + checksums, then
`02_build_panel.py` → `03_distances.py`. Everything downstream runs offline.

## Non-availability fallbacks

- If a wave cannot be downloaded, the panel proceeds with acquired waves and
  DATASET_INVENTORY.csv marks it absent — no silent substitution.
- No third-party raw records are re-published: licensed microdata stays local;
  the public mirror carries code + aggregate/derived outputs only
  (EXCLUDE_MAP covers data/raw).
