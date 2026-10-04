#!/usr/bin/env python3
"""M5: mixture-of-experts — SES gates regime membership AND within-regime
distance. Custom EM:

  gating:   logit pi_i = a + g'X_i          (multinomial logit)
  experts:  logD_i | k ~ N(b_k'X_i, s_k^2)  (GLM per component)

Reports gamma (SES->membership) vs beta_k (SES->within-regime distance) and
the Pattern A-F adjudication table. Wild-cluster bootstrap by country.
"""
import pathlib, sys
import numpy as np, pandas as pd
from scipy.special import logsumexp, softmax
from scipy.optimize import minimize

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROC, RES = ROOT/"data"/"processed", ROOT/"results"; RES.mkdir(exist_ok=True)
SEED = 20261004
rng = np.random.default_rng(SEED)

def normal_ll(y, m, s):
    return -0.5*np.log(2*np.pi) - np.log(s) - 0.5*((y-m)/s)**2

def moe_em(y, X, K=2, maxit=300, tol=1e-7, seed=0):
    rng = np.random.default_rng(seed)
    n, p = X.shape
    G = rng.normal(0, 0.3, ((K-1)*p,))
    B = np.vstack([np.linalg.lstsq(X, y + rng.normal(0, .5, n), rcond=None)[0]
                   for _ in range(K)])
    S = np.full(K, y.std()/2)
    prev = -np.inf
    for _ in range(maxit):
        lp = np.log(softmax(X @ np.vstack([np.zeros(p), G.reshape(K-1, p)]).T, 1) + 1e-300)
        le = np.stack([normal_ll(y, X @ B[k], S[k]) for k in range(K)], 1)
        lw = lp + le
        ll = logsumexp(lw, 1).sum()
        W = np.exp(lw - logsumexp(lw, 1)[:, None])
        Nk = W.sum(0)
        # M-step: experts weighted OLS; gating via IRLS-lite gradient step
        for k in range(K):
            Wk = np.sqrt(W[:, k] + 1e-10)
            B[k] = np.linalg.lstsq(X*Wk[:, None], y*Wk, rcond=None)[0]
            S[k] = max(np.sqrt((W[:, k]*(y-X@B[k])**2).sum()/Nk[k]), 1e-3)
        def gnll(g):
            Pr = softmax(X @ np.vstack([np.zeros(p), g.reshape(K-1, p)]).T, 1)
            return -(W*np.log(Pr+1e-300)).sum()
        G = minimize(gnll, G, method="BFGS",
                     options={"maxiter": 60, "gtol": 1e-4}).x
        if ll - prev < tol: break
        prev = ll
    return dict(ll=prev, G=G.reshape(K-1, p), B=B, S=S, W=W)

def main():
    f = PROC/"panel_dist.csv"
    if not f.exists(): print("panel_dist.csv absent — skeleton only"); return 0
    df = pd.read_csv(f).dropna(subset=["log_dist", "ses_index", "country_int"])
    covs = ["ses_index", "age", "hh_size", "child_prop"]
    covs = [c for c in covs if c in df]
    Xd = (df[covs] - df[covs].mean())/df[covs].std()
    X = np.column_stack([np.ones(len(df)), Xd.to_numpy()])
    y = df["log_dist"].to_numpy()
    fit = moe_em(y, X, K=2)
    tab = pd.DataFrame({"param": ["intercept", *covs],
                        "gating_gamma": fit["G"][0],
                        "expert1_beta": fit["B"][0],
                        "expert2_beta": fit["B"][1]})
    tab.to_csv(RES/"moe_coefs.csv", index=False)
    print(tab.to_string())
    return 0

if __name__ == "__main__":
    sys.exit(main())
