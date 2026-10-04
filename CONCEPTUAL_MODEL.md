# CONCEPTUAL MODEL

## Central question

For people who crossed an international border because of armed conflict:
does pre-displacement socioeconomic status (SES) shift migration distance
*itself*, does it shift the *probability of belonging to distinct latent
migration regimes*, or both?

## Two rival mechanisms

**Mechanism A — mobility capacity.** Longer moves require money, transport
access, valid documents, information, education, language, diaspora and
professional networks, and visa literacy. Higher SES raises attainable distance.
Sign prediction: SES ↑ → distance ↑ (within-regime and/or via membership in a
long-distance regime).

**Mechanism B — place attachment / location-specific capital.** Higher-SES
households hold more non-portable capital at origin: housing, land, businesses,
licences, status, clientele, institutional and social capital, recoverable
assets. Their expected value of return is larger and the option value of staying
geographically/institutionally close is higher. Sign prediction:
SES ↑ → distance ↓.

The two act in opposite directions; a single-process regression would estimate
a *net* effect that may mask both.

## Generative model

Observed distance for crosser *i*:

    D_i ~ π_i · f_cap(D | X_i)  +  (1 − π_i) · f_att(D | X_i)

- π_i — probability i is in the mobility-capacity-dominant regime
- 1−π_i — probability i is in the attachment-dominant regime
- f_cap, f_att — within-regime distance distributions (parameterized
  families estimated, not assumed; see MIXTURE_MODEL_SPECIFICATION.md)

Components are identified **statistically first** (shape of the empirical
distance distribution), interpreted **second** against covariates and theory.
No psychological-type labels are attached to components a priori.

## SES operationalization (pre-treatment only)

Legs, in priority order: pre-war occupation/activity → educational attainment →
pre-war home/dwelling ownership → occupation-based class → origin-oblast
socioeconomic indicators. Three encodings compared: individual indicators,
standardized index, latent SES factor. Education ≠ wealth ≠ class is stated
explicitly wherever education-only SES is used. Current income/employment are
post-treatment and banned from primary SES.

## Observable implications kept separate (prompt §14)

| Pattern | Signature | Reading |
|---|---|---|
| A | whole distribution shifts right with SES | capacity-dominant single process |
| B | whole distribution shifts left | attachment/return-value dominant |
| C | shape similar, far-component share rises with SES | regime-selection (π moves) |
| D | component means equal; only π depends on SES | pure route/regime selection |
| E | π constant; within-component distances move with SES | within-regime resource effect |
| F | poorest scarce among crossers yet far-regime share high among observed low-SES | selection reversal — requires stage-1 population frame |

## Causal diagram (see DAG.png / DAG_source.txt)

Key paths and threats:

- Conflict intensity at origin → who flees, how far, and is itself correlated
  with origin SES → adjust via origin-level conflict covariates.
- Border proximity/occupation → feasibility of leaving → selection into the
  crossers sample (collider if conditioned naively).
- Host-country pull factors (TP regime, welfare, labour access, diaspora) →
  destination availability ≠ choice → entered as destination-level
  availability/exposure, not as individual baseline confounders.
- Household composition/age/sex → both mobility capacity and attachment.
- Post-treatment variables (current income, current employment, experiences
  en route) → excluded from confounder set; usable only descriptively.
