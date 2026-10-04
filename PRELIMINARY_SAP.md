# PRELIMINARY STATISTICAL ANALYSIS PLAN (v0.1, pre-registration draft)

## Estimands

E1: association between pre-war SES and log migration distance among
    conflict-induced cross-border displaced persons (net associational gradient).
E2: number and geometry of latent components of the log-distance distribution.
E3: SES gradient in regime-membership probability π_i (mixture-of-experts γ).
E4: SES gradient within each estimated component (β_k).
E5 (secondary): stage-0→1 selection — who crosses at all (Pattern F).

## Sample

Inclusion: usual residence in Ukraine on/before escalation; crossed an
international border citing conflict/safety; interviewed in a host country.
Exclusions: pre-war diaspora, economic movers, tourists/students, third-country
nationals without Ukraine residence, IDPs (separate arm), non-Ukraine-source rows.

Primary datasets: UNHCR MDL PPM rounds (839/1031/959/1281/1282) + Intentions
rounds (783/873/934/1064-66/1275-76), household file, respondent-reported
household. Pooled with wave fixed effects; single-wave replication.

## Variables

- Outcome: log haversine km, oblast-centroid → host-capital; secondaries per
  DISTANCE_DEFINITION.md.
- SES: education ladder; pre-war activity/occupation (recoded to white/blue/
  not-working/agri/other + ISCO-ish ordering); home ownership (Intentions arm);
  three encodings compared.
- Baseline covariates: age, sex, HH size, children proportion, disability flag,
  family separation, relatives abroad, prior internal displacement, departure
  month (wave), documents held.
- Origin level: oblast conflict intensity/occupation (public ACLED-derived
  measure; acquisition step in build plan), border distance of oblast, urban/rural.
- Destination level (availability, not confounder): host TP policy period,
  diaspora stock (UNHCR data), GDP pc, asylum-country indicator set.

## Analysis sequence

1. Build/crosswalk layer (variables harmonized across waves; code frozen).
2. Descriptive: SES-stratified density/ECDF/histograms of log D; heaping and
   country-spike audit; multimodality diagnostics (descriptive only).
3. M1–M3 benchmarks (linear log, GAM, quantile).
4. M4 mixtures K=1..3 per family; selection criteria per specification.
5. M5 mixture-of-experts.
6. Pattern adjudication table A–F filled from fitted objects (pre-registered
   decision rules, not narrative).
7. Robustness battery (ROBUSTNESS_PLAN.md).
8. External validation: Syria Europe (1342) + Syria KRI asset arm (403/406).

## Software

Python: pandas numpy scipy statsmodels scikit-learn geopandas pyproj shapely
matplotlib; stepmix/flexmix-equivalent custom EM if no maintained OSS covers
mixture-of-experts; wild-bootstrap via own code. Fixed seed = 20261004.
No API keys at analysis time; all inputs under data/raw + data/processed.
