# GO / NO-GO DECISION

**Verdict: CONDITIONAL GO** (recorded 2026-10-04, before any analysis).

## Gate criteria

| Criterion | Result |
|---|---|
| origin + destination + pre-war SES in same/linkable data | PASS — oblast × host country × education/occupation/ownership in 5+ UNHCR MDL datasets |
| sufficient distance variation | PASS — 85 asylum countries, ~0.4–9k km |
| single-war analysable | PASS — Ukraine alone supports full stack |

## Why CONDITIONAL, not GO

1. Access mechanics: microdata are licensed — free MDL registration + use
   agreement required. No anonymous bulk download exists. The build plan
   assumes registration succeeds; if it fails, study reverts to NO-GO for
   individual-level analysis (aggregate-only redesign is a different paper).
2. SES is proxy-only: no pre-war income anywhere in the Ukraine series;
   home-ownership exists only in the Intentions waves. Composite-SES claims
   must be hedged accordingly.
3. All candidate samples are non-probability (provider-stated). The study
   remains descriptive-structural; causal or prevalence claims are out of
   scope by design.
4. Destination resolution is country-level for most waves; fine-grained
   distance is only partially recoverable (region-of-interview fields,
   settlement free-text in Intentions).
5. Transit-route data exist only in PPM round 1 (839); border-step outcomes
   degrade to coarse proxies elsewhere.

## Conditions attached to the GO

C1. Analyst registers at microdata.unhcr.org and downloads the listed datasets;
    acquisition script `analysis/01_acquire_data.py` validates checksums/rows.
C2. Primary claims limited to associational structure of the observed distance
    distribution among crossers; stage-0→1 selection analysis explicitly
    secondary.
C3. Composite-SES caveat in every output using education/occupation proxies.
C4. Syria external-validation arm is best-effort; its absence must not block
    the Ukraine paper (within-war paper remains complete).
C5. Systematic literature search before submission (novelty audit is
    literature-map based, not exhaustive).

## What would force NO-GO downstream

- MDL registration denied or datasets withdrawn.
- Occupation/education missingness >30% on core waves making SES unstable.
- Mixture estimation degenerates (K=1 everywhere AND single-process nonlinear
  fits are flat) — then the honest paper is M1–M3 plus a distance-decay
  description; decision recorded, not hidden.
