#!/usr/bin/env python3
"""Render the study DAG as PNG (no Graphviz; plain matplotlib).

DAG_source.txt holds the human-readable node/edge specification this script
renders — keep the two in sync.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "DAG.png"

NODES = {
    "SES":       (1.0, 7.0, "SES_pre\n(edu / prewar occup.\n/ home ownership)"),
    "CONF":      (1.0, 9.0, "Origin conflict\nintensity / occupation"),
    "BORD":      (1.0, 5.0, "Border proximity /\ntransport access"),
    "HH":        (1.0, 3.0, "Household comp.\nage / sex"),
    "DIAS":      (3.6, 9.0, "Relatives abroad\n(pre-existing diaspora)"),
    "FLEE":      (3.6, 5.5, "Crossed border\n[Flee = 1, CONDITIONED]"),
    "REGIME":    (6.2, 7.5, "Latent regime R\n(π_i gating)"),
    "HOST":      (6.2, 3.2, "Host-country pull\n(TP regime, diaspora,\nlabor access, welfare)"),
    "DIST":      (8.8, 6.5, "Migration distance D\n(dest country / km /\nborder steps / transit)"),
    "ROUTE":     (8.8, 4.0, "Route events\n(transit, en-route vars)"),
    "CURSES":    (8.8, 1.6, "Current income /\nemployment (post-treat.)"),
}
EDGES = [
    ("SES","REGIME"), ("SES","DIST"), ("SES","FLEE"), ("SES","CURSES"),
    ("CONF","FLEE"), ("CONF","DIST"),
    ("BORD","FLEE"), ("BORD","DIST"),
    ("HH","FLEE"), ("HH","DIST"), ("HH","REGIME"),
    ("DIAS","REGIME"), ("DIAS","DIST"), ("DIAS","HOST"),
    ("REGIME","DIST"),
    ("HOST","DIST"),
    ("DIST","ROUTE"), ("FLEE","ROUTE"),
    ("ROUTE","CURSES"), ("DIST","CURSES"),
]

fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 10.6); ax.set_ylim(0.6, 10.2); ax.axis("off")
pos = {}
for k, (x, y, label) in NODES.items():
    sel = k == "FLEE"
    box = FancyBboxPatch((x-1.15, y-0.55), 2.3, 1.15,
                         boxstyle="round,pad=0.06",
                         fc="#ffd9d9" if sel else "#e8f0fe",
                         ec="#b03030" if sel else "#35507a", lw=1.4)
    ax.add_patch(box)
    ax.text(x, y+0.03, label, ha="center", va="center", fontsize=8.5)
    pos[k] = (x, y)
for a, b in EDGES:
    x1, y1 = pos[a]; x2, y2 = pos[b]
    arr = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                          mutation_scale=13, lw=1.1, color="#444",
                          shrinkA=16, shrinkB=16,
                          connectionstyle="arc3,rad=0.12")
    ax.add_patch(arr)
ax.text(3.6, 4.6, "conditioning on Flee=1\ninduces collider bias", fontsize=7.5,
        color="#b03030", ha="center", style="italic")
ax.text(0.2, 0.9, "Solid nodes = pre-treatment/baseline or exogenous level variables. "
                  "ROUTE & CURSES are post-treatment: excluded from the confounder set.",
        fontsize=8, color="#555")
plt.tight_layout(); plt.savefig(OUT, dpi=200); print("wrote", OUT)
