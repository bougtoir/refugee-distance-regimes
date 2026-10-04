# DISTANCE DEFINITIONS

Multiple pre-registered outcomes; no single "distance" is privileged.

## A. Geographic distance (PRIMARY)

Origin point = centroid of the respondent's **oblast of residence before
departure** (GADM 4.1 admin-1, acquired `data/raw/geo/gadm41_UKR_1.json`;
population-weighted centroid computed as robustness via GHS-POP if adopted later).

Destination point = host-country reference:

- primary: **capital city coordinates** of the country of interview (deterministic,
  no API); justified because within-country location is unobserved for most waves.
- secondary: "region/place of interview" centroid where the wave provides it
  (PPM 1281/1282 region-of-interview fields) — sensitivity arm.
- never origin-capital → host-capital (prompt §12.7); oblast centroid is the floor.

Metric: great-circle (haversine) distance in km, log1p-transformed for modelling.

Known distortion, stated upfront: host-*country* destination censors
within-country spread (e.g., all Germany records get Berlin distance); this
compresses far-tail variance → makes mixture detection *conservative*, not
inflated. Documented as a limitation.

## B. Border-step distance (secondary)

Count of international borders crossed = f(route): computable for PPM R1 (839)
from first-arrival + up-to-5 transit countries; for other waves approximated as
1 (direct neighbour) vs 2+ from first-country vs interview-country mismatch where
available. Reported as ordinal outcome, not continuous.

## C. Transit complexity (secondary)

Transit-country count (R1 only), transfer count proxy; reported descriptively.

## D. Travel-network distance (optional secondary)

Road/rail network distance origin-oblast → host capital via OSRM/OSM public data
if a reproducible no-key pipeline is feasible; otherwise dropped (no API-key
dependence allowed).

## E. Friction-adjusted effective distance (secondary only)

Composite index NEVER used as primary (arbitrary weights banned by prompt). If
computed at all: preregistered equal-weight z-score bundle of {visa restriction,
diaspora stock in destination, linguistic distance} appended as robustness.

## Derived coding notes

- Same-country-origin restriction: all Ukraine origins; origin oblasts = GADM ADM1.
- Occupied/Crimea/Sevastopol oblasts retained with occupation-status flag (origin
  confounder, not exclusion).
- Distances where origin oblast is "don't know/prefer not" → missing, never
  imputed to capital.
- Outlier policy: >99.9th percentile distance flagged, winsorized only in a
  robustness arm, never in primary.
