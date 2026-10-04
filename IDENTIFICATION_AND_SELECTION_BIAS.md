# IDENTIFICATION & SELECTION-BIAS PLAN

## The core problem

We observe P(distance | crossed border, sampled by survey), while the
scientific estimand is P(displacement outcome | conflict-exposed population).
Conditioning on crossing opens collider paths (SES → Flee ← conflict/border →
distance) and, because all surveys are non-probability, adds venue-selection
bias (enumerated at borders, centres, assistance points — systematically
missing those who moved privately/far early).

## Stage model (estimands, not just covariates)

Stage 0 → 1: home/IDP → crossed border.
Stage 1 → 2: neighbouring → regional/long-distance destination.
Stage 2+: onward moves (PPM 2024 waves, intentions' onward-plan items).

Primary paper arm = stage 1→2 conditional distribution (stated as such — no
causal-population claim). Stage 0→1 modelled in a secondary analysis using IOM
DTM GPS population estimates (non-displaced + IDP by oblast) as the exposed
frame and UNHCR IDP-intentions surveys for the IDP layer.

## Design guards (prompt §12 audit)

1. Current income / current employment — banned from SES and from adjustment sets.
2. Host-country conditions entered as destination-level *availability*
   characteristics of the choice set, never as individual confounders in the
   within-regime model.
3. En-route variables (transit hardship, documents seized, employer abuse) —
   post-treatment, descriptive only.
4. Collider exposure stated in paper limitations; IPW robustness arm weights by
   inverse propensity of appearing in a venue sample (venue-type model), not by
   "being a refugee".
5. Destination *availability* vs *choice*: alternatives set = all asylum
   countries receiving Ukrainians (85, per UNHCR stock data) with exposure
   covariates; choice model respects the choice-set structure.
6. Origin distance computed from oblast centroid, not capital (§12.7).
7. Mixture components interpreted statistically before theory (§12.8).
8. No pooled cross-war analysis without war-level fixed effects and
   within-war replication (Syria arm estimated separately; pooling only for a
   meta-style comparison table).
9. Cross-sectional identification = associational; language in paper limited to
   "regime structure and covariate gradients", not individual decision
   mechanisms.
10. Occupied-territory and border-region origins flagged; their distance floor
    is mechanically short → origin fixed effects + border-proximity control,
    plus a robustness arm excluding oblasts bordering a host country.

## Instrument/identification options considered and rejected

- No plausible IV for SES among crossers — none claimed.
- Border-closure/policy discontinuities differ by wave → used only as
  descriptive stratifiers (early vs late displacement wave robustness).
