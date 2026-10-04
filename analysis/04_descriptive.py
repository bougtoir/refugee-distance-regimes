#!/usr/bin/env python3
"""Phase-3 descriptive distribution audit (pre-hypothesis).

Reads data/processed/panel_dist.csv. Emits SES-stratified density/ECDF figures
and a moments table. Hartigan dip test reported descriptively only — country
spikes/institutional modes are audited separately.
"""
import pathlib, sys
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROC, RES = ROOT/"data"/"processed", ROOT/"results"; RES.mkdir(exist_ok=True)

# Hartigan dip statistic — vendored implementation of Johannes Bauer's
# Python port (https://github.com/tatome/dip_test) of Hartigan & Hartigan
# (1985), Annals of Statistics 13:70-84. np.msort replaced by np.sort for
# numpy>=1.25 compatibility; otherwise faithful to the reference code.

def _gcm_(cdf, idxs):
    work_cdf, work_idxs = cdf, idxs
    gcm, touchpoints = [work_cdf[0]], [0]
    while len(work_cdf) > 1:
        distances = work_idxs[1:] - work_idxs[0]
        slopes = (work_cdf[1:] - work_cdf[0]) / distances
        minslope = slopes.min()
        mi = np.where(slopes == minslope)[0][0] + 1
        gcm.extend(work_cdf[0] + distances[:mi] * minslope)
        touchpoints.append(touchpoints[-1] + mi)
        work_cdf, work_idxs = work_cdf[mi:], work_idxs[mi:]
    return np.array(gcm), np.array(touchpoints)

def _lcm_(cdf, idxs):
    g, t = _gcm_(1 - cdf[::-1], idxs.max() - idxs[::-1])
    return 1 - g[::-1], len(cdf) - 1 - t[::-1]

def _touch_diffs_(part1, part2, touchpoints):
    diff = np.abs(part2[touchpoints] - part1[touchpoints])
    return diff.max(), diff

def dip_statistic(x):
    """Hartigan dip statistic (descriptive use only)."""
    import collections
    x = x[~np.isnan(x)]
    if len(x) < 5: return np.nan
    counts = collections.Counter(x)
    idxs = np.sort(list(counts.keys()))
    histogram = np.array([counts[i] for i in idxs])
    if len(idxs) <= 4 or idxs[0] == idxs[-1]:
        return 0.0
    cdf = np.cumsum(histogram, dtype=float); cdf /= cdf[-1]
    work_idxs, work_cdf = idxs, cdf
    work_histogram = histogram.astype(float) / histogram.sum()
    D, left, right = 0, [0], [1]
    while True:
        left_part, left_tp = _gcm_(work_cdf - work_histogram, work_idxs)
        right_part, right_tp = _lcm_(work_cdf, work_idxs)
        d_left, left_diffs = _touch_diffs_(left_part, right_part, left_tp)
        d_right, right_diffs = _touch_diffs_(left_part, right_part, right_tp)
        if d_right > d_left:
            xr = right_tp[d_right == right_diffs][-1]
            xl = left_tp[left_tp <= xr][-1]
            d = d_right
        else:
            xl = left_tp[d_left == left_diffs][0]
            xr = right_tp[right_tp >= xl][0]
            d = d_left
        left_diff = np.abs(left_part[:xl+1] - work_cdf[:xl+1]).max()
        right_diff = np.abs(right_part[xr:] - work_cdf[xr:]
                            + work_histogram[xr:]).max()
        if d <= D or xr == 0 or xl == len(work_cdf):
            return max(np.abs(cdf[:len(left)] - left).max(),
                       np.abs(cdf[-len(right)-1:-1] - right).max()) / 2
        D = max(D, left_diff, right_diff)
        work_cdf, work_idxs = work_cdf[xl:xr+1], work_idxs[xl:xr+1]
        work_histogram = work_histogram[xl:xr+1]
        left[len(left):] = left_part[1:xl+1]
        right[:0] = right_part[xr:-1]

def main():
    p = PROC/"panel_dist.csv"
    if not p.exists(): print("panel_dist.csv absent"); return 0
    df = pd.read_csv(p).dropna(subset=["log_dist"])
    df["ses_bin"] = pd.cut(df.get("ses_index", df["edu_level"]),
                           bins=5, labels=False)
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
    for s, g in df.groupby("ses_bin"):
        xs = np.sort(g["log_dist"])
        ax[0].plot(xs, np.linspace(0, 1, len(xs)), label=f"SES {s}")
        g["log_dist"].plot.kde(ax=ax[1], label=f"SES {s}")
    ax[0].set_title("ECDF log distance by SES"); ax[0].legend()
    ax[1].set_title("Density log distance by SES"); ax[1].legend()
    fig.tight_layout(); fig.savefig(RES/"dist_by_ses.png", dpi=150)
    tab = df.groupby("ses_bin")["log_dist"].agg(
        ["count","mean","std","skew"]).round(3)
    tab["dip"] = df.groupby("ses_bin")["log_dist"].apply(dip_statistic)
    tab.to_csv(RES/"dist_moments.csv")
    print(tab.to_string())
    return 0

if __name__ == "__main__":
    sys.exit(main())
