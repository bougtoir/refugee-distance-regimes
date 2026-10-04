# FEASIBILITY REPORT — SES × migration-distance mixture study (war refugees)

Date: 2026-10-04 (UTC). Scope: public-data-only feasibility audit for the research
question "does pre-displacement socioeconomic status shift cross-border refugee
migration distance directly, through latent migration-regime membership, or both?"

## 1. Verdict summary

**CONDITIONAL GO** — see `GO_NO_GO_DECISION.md` for the formal gate record.

The minimum analytic unit (origin subregion × destination × pre-displacement SES
proxy, one record) exists in **multiple public microdata sources** covering the
Ukraine displacement across 2022–2024 and ≥20 host countries. The binding
conditions are access mechanics and measurement, not existence:

1. UNHCR Microdata Library (MDL) microdata are **licensed**: free registration +
   use agreement, downloadable as SPSS/Stata/CSV. Not anonymous-downloadable; the
   code skeleton therefore ships an acquisition script that *documents* the
   required datasets and validates files once the analyst downloads them. This is
   standard academic access (MDL is the routine channel for UNHCR survey data).
2. **Pre-war income is not collected** in the Ukraine refugee surveys. The SES
   battery = education + pre-war occupation/activity + (in the Intentions
   series) pre-war **dwelling ownership**. Income questions exist but are
   post-displacement and are excluded from the primary SES definition by design.
3. All candidate surveys are **non-probability / convenience samples** — UNHCR
   states this explicitly. Findings are distributional/descriptive; causal claims
   require the identification caveats in `IDENTIFICATION_AND_SELECTION_BIAS.md`.
4. Destination is measured at **country level** in most datasets (subnational
   "region of interview" exists in some waves; free-text settlement of origin
   exists in the Intentions series). Distance outcomes are built as
   origin-oblast centroid → host-country reference point, with secondary
   border-step and transit-count outcomes (PPM round 1 codes up to 5 transit
   countries).

## 2. What the audit established

### 2.1 Core trio availability (Ukraine)

Audited via the UNHCR MDL public catalog: study descriptions and machine-readable
data dictionaries were scraped for 17 candidate datasets
(`results/unhcr_mdl_audit.csv`, per-variable labels preserved). Confirmed
co-occurrence on the same record:

| Construct | Confirmed datasets (catalog id) |
|---|---|
| Origin **oblast** (or region) | 839, 1031, 959, 1281, 1282, 783, 873, 934, 1064, 1214; settlement text in 873/934/1064 series |
| Destination (country of interview; some "region of interview" subnational) | all PPM and Intentions datasets |
| Education (highest level attained) | all above |
| Pre-war occupation / main activity | 839 ("profession or main activity in Ukraine"), 1031, 959, 1281, 1282 (phrased "prior to leaving Ukraine"), 1214 |
| Pre-war **home ownership** (dwelling owned in Ukraine, 23 Feb 2022) | 934 and other Intentions-series rounds |
| Displacement date (left Ukraine / arrived host) | all |
| Transit countries (1st–5th) + first country of arrival | **839 only** (PPM round 1) |
| Internally displaced within Ukraine before crossing | 839 |
| Relatives residing outside Ukraine (diaspora-network proxy) + their countries | 839 |
| Family separation / HH composition | all |
| Return intentions + reasons | all |
| Onward-move plans + destination + reasons | all (incl. 1282 departure/final-destination items) |
| Destination-selection motivation | all |

Largest harmonized household-level Ns (from study descriptions):
PPM R2 (1031) n≈17,708; PPM R3 (959) n≈21,340; PPM R1 (839) n≈1,409 per-country
files plus companion files; Intentions #2 (783) n≈4,800, #3 (873) n≈887,
#4 (934) n≈3,850, #5 (1275) n≈4,000, #6 (1276) n≈5,000; Border Monitoring (854)
n≈18,000.

### 2.2 Destination/outcome variation

Aggregate UNHCR stocks (acquired, `data/raw/macro/`): Ukrainian refugees recorded
in **85 asylum countries 2022–2024** — Moldova/Romania/Slovakia/Poland adjacent
arm vs. Germany/Czechia/UK/Spain/Italy/Ireland/Austria/Canada far arm. Great-circle
oblast→host distances span roughly 400–9,000 km with strongly non-degenerate
support. Sufficient variation for mixture identification.

### 2.3 Displacement ladder (selection)

- **IDP pre-step measured**: PPM R1 (839) asks whether the household was internally
  displaced within Ukraine before going abroad → directly codes the
  home→IDP→cross-border ladder stage for sampled crossers.
- **Origin population frame**: IOM DTM Ukraine General Population Survey (GPS)
  rounds (public reports on HDX/DTM; microdata request channel exists) gives the
  *non-displaced + IDP* distribution by oblast → enables first-stage
  "who crossed at all" modelling (Pattern F test) as a secondary analysis.
- UNHCR IDP intentions surveys (948, 1273, 1274) measure IDP-side intentions.

### 2.4 External validation (independent war, independent institutions)

- **Syria in Europe**: MDL catalog 1342 "Intentions Survey with Syrian Refugees
  and Asylum-Seekers in Europe – 2025" (n≈17,378 screened / 3,736 in scope):
  place of origin in Syria, arrival year, current European country, return
  intentions. SES detail thinner than Ukraine series — check education/occupation
  item at acquisition; still supports the core distance contrast.
- **Syria regional (fine subnational)**: catalog 403/406 "Survey of Syrian
  Refugees and Host Communities 2015–2016" (Kurdistan region + host communities):
  **source governorate**, education completed, **employment at time of leaving**,
  and a **pre-war asset module** ("did you own [asset] in September 2010" across
  ~7 asset classes + ownership proof + post-war asset state) — the strongest
  Mechanism-B (location-specific capital) instrument identified anywhere.
  Destination is regional (Erbil/KRI) — supports a *within-host-country*
  distance arm rather than cross-country.
- **Lebanon**: VASyR 2025 (1453) — district/place of origin + full SES/vulnerability
  modules; single host country → subnational distance arm.
- **Afghanistan**: DTM/UNHCR Border Monitoring inflow/outflow 2022–23 (1103/1104):
  province of residence in country of prior residence, education, exit reasons —
  return-flow geometry; usable as a robustness out-sample, not a primary arm.

### 2.5 Sources checked and excluded/flagged

| Source | Status |
|---|---|
| EUAA SAM (Survey of Arriving Migrants from Ukraine) | Microdata not openly published; dashboards only — secondary citation, not analytic source |
| IAB-BiB-FReDA-SOEP Ukrainian-refugee survey (Germany) | Gold-standard panel but contract-gated access (not "public") — listed as upgrade path |
| IOM DTM Ukraine refugee surveys | Reports open; microdata via DTM request — secondary |
| World Bank / HDX HAPI | Aggregate stocks only — used for destination-variation and population-frame checks |
| Venezuela R4V monitoring | Excluded by design (not armed-conflict induced) |
| Former Yugoslavia | No compatible public microdata identified |

## 3. Feasibility against the prompt's GO criteria

- origin ✓ (oblast; settlement text in Intentions series)
- destination ✓ (host country; onward/final destination in later waves)
- pre-war SES ✓ (education + occupation + home-ownership proxy; no pre-war income)
- distance variation ✓ (85 countries; orders of magnitude)
- single-war analysability ✓ (Ukraine alone supports the full model stack)

Not met / partial: pre-war income (absent → composite-SES caveat); representative
sampling (non-probability → inference caveat); route-level distance for most waves
(transit countries in R1 only).

## 4. Risks that remain after GO

1. Registration lead time for MDL access (mitigate: register early; the
   documentation PDFs and this audit are already local).
2. Harmonization burden across waves — occupation/education codings shift;
   `analysis/` builds a crosswalk layer first.
3. Settlement-name geocoding for finer origin resolution is optional and messy;
   primary design uses oblast centroids (deterministic, no API key).
4. Mixture-component interpretation must stay statistical-then-theoretical
   (prompt §2/§15); the DAG and SAP fix the pre-analysis guardrails.
