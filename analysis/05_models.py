#!/usr/bin/env python3
"""M0-M4 benchmarks + finite-mixture EM (Gaussian on log distance).

M5 mixture-of-experts lives in 06_mixture_experts.py.
Multi-start EM with >=50 restarts; BIC/AIC/ICL/entropy selection table.
"""
import pathlib, sys
import numpy as np, pandas as pd
import statsmodels.api as sm

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROC, RES = ROOT/"data"/"processed", ROOT/"results"; RES.mkdir(exist_ok=True)
SEED = 20261004
rng = np.random.default_rng(SEED)

def em_gauss_mix(y, K, restarts=50, maxit=500, tol=1e-8):
    best = None
    for r in range(restarts):
        pi = rng.dirichlet(np.ones(K))
        qs = np.quantile(y, np.linspace(.1, .9, K)) + rng.normal(0, .1, K)
        mu, sd = qs.copy(), np.full(K, y.std()/2)
        ll_prev = -np.inf
        for _ in range(maxit):
            dens = np.stack([pi[k]*np.exp(-0.5*((y-mu[k])/sd[k])**2)
                             /(sd[k]*np.sqrt(2*np.pi)) for k in range(K)], 1)
            den = dens.sum(1); den[den==0] = 1e-300
            w = dens/den[:, None]
            ll = np.log(den).sum()
            Nk = w.sum(0); Nk[Nk==0] = 1e-10
            pi = Nk/len(y)
            mu = (w*y[:, None]).sum(0)/Nk
            sd = np.sqrt((w*(y[:, None]-mu[None, :])**2).sum(0)/Nk) + 1e-6
            if ll - ll_prev < tol: break
            ll_prev = ll
        if best is None or ll > best["ll"]:
            best = dict(ll=ll, pi=pi, mu=mu, sd=sd, w=w)
    return best

def criteria(best, n, k_params):
    ll, w = best["ll"], best["w"]
    bic = -2*ll + k_params*np.log(n); aic = -2*ll + 2*k_params
    cl = (w*np.log(w+1e-300)).sum()
    icl = bic - 2*cl  # ICL = BIC + 2*classification-entropy penalty
    ent = 1 + cl/(n*np.log(len(best["pi"])))
    return dict(bic=bic, aic=aic, icl=icl, entropy=ent)

def main():
    f = PROC/"panel_dist.csv"
    if not f.exists(): print("panel_dist.csv absent — skeleton only"); return 0
    df = pd.read_csv(f).dropna(subset=["log_dist", "ses_index"])
    y = df["log_dist"].to_numpy(); n = len(y)
    X = sm.add_constant(df[["ses_index"]])
    m1 = sm.OLS(y, X).fit(cov_type="cluster",
        cov_kwds={"groups": df["country_int"]})
    rows = [{"model": "M1_linear", "beta_ses": m1.params[1],
             "se": m1.bse[1], "bic": m1.bic}]
    for K in (1, 2, 3):
        b = em_gauss_mix(y, K)
        kp = 3*K - 1
        rows.append({"model": f"M4_K{K}", "ll": b["ll"],
                     **criteria(b, n, kp)})
        np.save(RES/f"mix_K{K}_post.npy", b["w"])
    pd.DataFrame(rows).to_csv(RES/"model_selection.csv", index=False)
    print(pd.DataFrame(rows).to_string())
    return 0

if __name__ == "__main__":
    sys.exit(main())
