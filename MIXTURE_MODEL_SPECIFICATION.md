# MIXTURE MODEL SPECIFICATION (pre-analysis)

## Model ladder

M0 null: D ⊥ SES (intercept-only).
M1 monotonic positive: E[log D] = β0 + β1·SES, β1 > 0.
M2 monotonic negative: β1 < 0.
M3 single-process nonlinear: GAM/spline SES → log D; quantile regression across τ.
M4 finite mixture (primary):
    log D_i ~ Σ_{k=1..K} π_k(?) · Normal_k(log D | μ_k(X_i), σ_k²)
    K ∈ {1,2,3} compared; K=2 first candidate.
    Alternate families per component: Normal(log D), Gamma(D), log-Normal(D),
    Weibull(D) — family chosen by fit diagnostics, not convenience.
M5 mixture-of-experts (primary inferential target):
    logit π_i(X_i) = α + γ1·SES_i + γ2·origin_i + γ3·HH_i + γ4·wave_i + ...
    within each k: log D_i|k ~ f_k(β_k·SES_i + δ_k·X_i + σ_k)

Separates (a) SES→membership (γ) from (b) SES→within-regime distance (β_k).
If destination resolves only to discrete countries and the continuous fit is
fragile, fall back to **latent-class conditional logit** over destination
alternatives (class-specific destination taste parameters) — preregistered
fallback, not a fishing licence.

## Component interpretation discipline

Components are labelled by their estimated geometry (e.g. "near/host-adjacent"
vs "far") and only then mapped to capacity/attachment theory via their
covariate signatures. If the far component's members are *less* educated,
mechanism-A labelling is rejected, not rescued.

## Estimation

- EM (flexmix-style) or direct ML with BFGS multi-start: ≥50 random restarts;
  report initialization sensitivity (share of restarts reaching global max).
- Weights: none in primary (non-probability samples); survey-provided weights
  used in robustness where present (Intentions series supplies weight var).
- Inference: cluster-robust SEs by country-of-interview (few clusters →
  wild-cluster bootstrap as default, CR2 as sensitivity).
- Model selection: BIC primary; AIC, ICL, entropy (target >0.8 for usable
  classification), bootstrap LRT (1 vs 2 vs 3 components, ≥500 bootstraps as
  feasible), out-of-sample log-loss via 5-fold CV.

## Falsification built in

- If K=1 is selected, report M1–M3 result honestly — no forced mixture.
- Posterior-membership entropy near 0.5 for most units → weak separation
  flagged; mixture claims downgraded to "suggestive".
- Institutional spike audit: component modes must not coincide mechanically
  with a single host country (destination==component degeneracy check).
- Dip test (Hartigan) on log D reported as *descriptive only*, per prompt.
- Placebo: shuffle SES within country — membership gradient must vanish.
