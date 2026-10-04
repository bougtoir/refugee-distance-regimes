# ANALYSIS PLAN FINAL

Umbrella: everything in PRELIMINARY_SAP.md stands; this file fixes the concrete
pipeline that `analysis/` implements.

## Data build (deterministic, re-runnable)

1. `01_acquire_data.py` — verifies licensed MDL files placed under
   `data/raw/mdl/<catalog_id>/`; logs checksums to
   `data/raw/ACQUISITION_LEDGER.csv`; fetches open auxiliaries
   (UNHCR aggregate stocks, GADM) automatically.
2. `02_build_panel.py` — per-dataset readers emit the common schema:
   `hhid, wave, survey_round, country_int, region_int, oblast_origin,
   settlement_raw, edu_level, prewar_activity, home_owner_ua, hh_size,
   child_prop, age, sex, disability, sep_family, prior_idp, relatives_abroad,
   left_ukr_ym, arrived_ym, transit_c1..c5, dest_reason, return_intent,
   onward_dest, weight`.
   Unmapped variables dropped silently = build FAILS on unmapped non-empty
   column (strict manifest, per repo convention).
3. `03_distances.py` — GADM oblast centroids + embedded capital-coord table →
   `dist_km`, `log_dist`; border-step and transit counts.
4. `04_descriptive.py` — distribution audit figures/tables to `results/`.
5. `05_models.py` — M0–M4 (single-process + K-component EM mixtures).
6. `06_mixture_experts.py` — M5 gating+component model, wild-cluster bootstrap.
7. `07_robustness.py` — R1–R23 battery → `results/robustness_table.csv`.
8. `08_external_validation.py` — Syria arms (1342; 403/406) same schema.

## Pattern adjudication (pre-registered decision rules)

- Pattern A/B: sign & CI of pooled SES coefficient in M1/M3 (net gradient).
- Pattern C: K≥2 selected AND within-k SES effects ~0 AND γ_SES significant.
- Pattern D: same as C with component means statistically equal.
- Pattern E: K≥2 AND γ_SES ~0 AND ≥1 β_k significant.
- Pattern F: crosser SES distribution shifted right vs origin frame AND low-SES
  crossers' far-regime posterior share > pooled share.
Ties/ambiguity reported as "indeterminate" — no forced label.

## Deliverable chain

panel.csv → distance table → descriptive pack → model objects (pickle) →
pattern table → robustness table → manuscript-ready figures (later session).
