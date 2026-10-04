# ROBUSTNESS PLAN (pre-registered battery)

SES encoding
- R1 education-only | R2 occupation-only | R3 composite index | R4 +home-ownership
  (Intentions arm only)

Outcome
- R5 geographic km (primary) | R6 border-step count | R7 transit-country count
  (839) | R8 destination country as discrete choice (latent-class logit fallback)

Sample/structure
- R9 remove extreme distances (>99.9 pct and non-European destinations)
- R10 leave-one-host-country-out (12-country jackknife)
- R11 leave-one-origin-oblast-out
- R12 early wave (2022) vs late wave (2024) split
- R13 households with children vs without
- R14 single-wave replication: every model re-fit in 959 (largest wave) alone

Mechanism lenses (descriptive, post-treatment flagged)
- R15 return-intention stratification (intends return vs not) — attachment
  channel proxy, labelled conditioning-on-post-treatment
- R16 destination-reason subgroups (family/work/safety/cost)

Selection stress tests
- R17 exclude oblasts directly bordering any host country (mechanical short D)
- R18 venue-type IPW (border vs assistance-point vs collective-site sampling)
- R19 Pattern-F check: oblast-level SES of crossers vs IOM GPS population frame
  (does the crosser SES distribution shift vs the exposed distribution?)

Model stability
- R20 distribution-family swap (Normal(log), Gamma, log-Normal, Weibull)
- R21 50-restart stability; label-switching audit
- R22 SES placebo shuffle within country (must flatten γ)
- R23 wild-cluster bootstrap CIs vs CR2 sandwich CIs

Reporting rule: every robustness result reported even when it overturns the
primary pattern; no "successful" subset highlighted.
