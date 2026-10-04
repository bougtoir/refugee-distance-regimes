# refugee_distance_regimes

Feasibility study + pre-registered design: does pre-displacement
socioeconomic status shift war refugees' migration distance through a single
process, or through membership in latent mobility-capacity vs place-attachment
regimes (finite-mixture / mixture-of-experts framing)?

Primary case: Ukraine (2022–2024). External validation arms: Syria (Europe
2025; Kurdistan 2015–16 with pre-war asset module; Lebanon VASyR 2025),
Afghanistan border-monitoring out-sample.

## Verdict

**CONDITIONAL GO** — `GO_NO_GO_DECISION.md`. Conditions: licensed UNHCR MDL
access (free registration), proxy-SES only (no pre-war income), non-probability
samples (associational claims only).

## Documents

`FEASIBILITY_REPORT.md` audit + verdict · `DATASET_INVENTORY.csv` 23 sources ·
`VARIABLE_AUDIT.csv` 33 variable rows · `LITERATURE_MAP.csv` 35 refs ·
`CONCEPTUAL_MODEL.md` + `DAG.png`/`DAG_source.txt` · `DISTANCE_DEFINITION.md` ·
`MIXTURE_MODEL_SPECIFICATION.md` · `IDENTIFICATION_AND_SELECTION_BIAS.md` ·
`PRELIMINARY_SAP.md` · `ROBUSTNESS_PLAN.md` · `NOVELTY_AUDIT.md` ·
`ANALYSIS_PLAN_FINAL.md` · `DATA_DOWNLOAD_AND_BUILD_PLAN.md`

## Pipeline (analysis/)

`01_acquire_data.py` verify/checksum inputs (+fetch open auxiliaries) →
`02_build_panel.py` harmonize waves → `03_distances.py` oblast-centroid→host-capital
haversine (works now on acquired GADM) → `04_descriptive.py` distribution audit →
`05_models.py` M0–M4 → `06_mixture_experts.py` M5 → `07_robustness.py` R1–R23.
`make_dag.py` renders DAG.png. `audit_unhcr_mdl.py` reproduces the MDL catalog
scrape behind `results/unhcr_mdl_audit.csv`.

## Data provenance

Licensed microdata are NOT committed. Open auxiliaries already persisted under
`data/raw/` (UNHCR aggregate stocks + demographics via HDX, GADM Ukraine ADM1,
questionnaire PDFs) with `data/raw/ACQUISITION_LEDGER.csv` checksums. Register
at microdata.unhcr.org and place datasets per `DATA_DOWNLOAD_AND_BUILD_PLAN.md`.

`pip install -r requirements.txt` · Python 3.10+ · seed 20261004.
