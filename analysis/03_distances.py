#!/usr/bin/env python3
"""Distance construction: oblast-centroid -> host-capital haversine km.

Deterministic and offline: oblast polygons from acquired GADM file, host-country
capital coordinates embedded below (top asylum countries + fallback to UN
member-state capitals via country_centroids table).
"""
import json, math, pathlib, sys
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
RES = ROOT / "results"; RES.mkdir(exist_ok=True)

# Capital coordinates (lat, lon) for observed asylum countries.
CAPITALS = {
    "DEU": (52.52, 13.405), "POL": (52.23, 21.01), "CZE": (50.08, 14.44),
    "SVK": (48.15, 17.11), "HUN": (47.50, 19.04), "ROU": (44.43, 26.10),
    "MDA": (47.01, 28.86), "BGR": (42.70, 23.32), "AUT": (48.21, 16.37),
    "GBR": (51.51, -0.13), "IRL": (53.35, -6.26), "ESP": (40.42, -3.70),
    "ITA": (41.90, 12.50), "NLD": (52.37, 4.90), "BLR": (53.90, 27.56),
    "EST": (59.44, 24.75), "LVA": (56.95, 24.11), "LTU": (54.69, 25.28),
    "RUS": (55.76, 37.62), "CAN": (45.42, -75.70), "USA": (38.90, -77.04),
    "FRA": (48.86, 2.35), "CHE": (46.95, 7.45), "SWE": (59.33, 18.07),
    "NOR": (59.91, 10.75), "DNK": (55.68, 12.57), "FIN": (60.17, 24.94),
    "BEL": (50.85, 4.35), "PRT": (38.72, -9.14), "GRC": (37.98, 23.73),
    "HRV": (45.81, 15.98), "MNE": (42.44, 19.26), "GEO": (41.72, 44.79),
    "TUR": (39.93, 32.86), "ISR": (31.77, 35.21), "JPN": (35.68, 139.69),
    "AUS": (-35.28, 149.13), "NZL": (-41.29, 174.78), "ARG": (-34.60, -58.38),
    "BRA": (-15.79, -47.88), "MEX": (19.43, -99.13), "KOR": (37.57, 126.98),
    "CYP": (35.17, 33.36), "ISL": (64.15, -21.94), "LUX": (49.61, 6.13),
    "MLT": (35.90, 14.51), "SVN": (46.05, 14.51), "ALB": (41.33, 19.82),
    "MKD": (42.00, 21.43), "BIH": (43.86, 18.41), "SRB": (44.79, 20.45),
    "ARM": (40.18, 44.51), "AZE": (40.41, 49.87), "KAZ": (51.17, 71.43),
    "UZB": (41.31, 69.24), "KGZ": (42.87, 74.59), "ARE": (24.45, 54.38),
    "EGY": (30.04, 31.24), "MAR": (34.02, -6.84), "ZAF": (-25.75, 28.19),
    "IND": (28.61, 77.21), "CHN": (39.90, 116.41), "THA": (13.76, 100.50),
    "VNM": (21.03, 105.85), "SGP": (1.35, 103.82), "JOR": (31.95, 35.93),
    "LBN": (33.89, 35.50), "SAU": (24.71, 46.68), "COL": (4.61, -74.08),
    "PER": (-12.05, -77.04), "CHL": (-33.45, -70.67), "URY": (-34.90, -56.16),
    "PAK": (33.69, 73.06), "BGD": (23.81, 90.41), "MNG": (47.92, 106.92),
    "KEN": (-1.29, 36.82), "NGA": (9.06, 7.49), "TUN": (36.81, 10.18),
    "IRQ": (33.31, 44.36), "IRN": (35.69, 51.39), "VEN": (10.49, -66.88),
}

def hav(lat1, lon1, lat2, lon2):
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def ring_centroid(ring):
    """Signed-area centroid of a single linear ring (shoelace)."""
    a = cx = cy = 0.0
    for (x0, y0), (x1, y1) in zip(ring, ring[1:] + ring[:1]):
        t = x0*y1 - x1*y0
        a += t; cx += (x0+x1)*t; cy += (y0+y1)*t
    a *= 0.5
    if abs(a) < 1e-12:
        return 0.0, 0.0, 0.0
    return a, cx/(6*a), cy/(6*a)

def oblast_centroids():
    """True polygon centroids: area-weighted over all parts of a MultiPolygon,
    interior rings (holes) subtracted via signed area."""
    gj = json.load(open(RAW / "geo" / "gadm41_UKR_1.json"))
    out = {}
    for f in gj["features"]:
        name = f["properties"]["NAME_1"]
        coords = f["geometry"]["coordinates"]
        polys = coords if f["geometry"]["type"] == "MultiPolygon" else [coords]
        ta = tx = ty = 0.0
        for poly in polys:
            for i, ring in enumerate(poly):
                a, cx, cy = ring_centroid([list(pt) for pt in ring])
                if i > 0:  # hole: subtract
                    a = -abs(a)
                ta += a; tx += a*cx; ty += a*cy
        out[name] = (ty/ta, tx/ta)
    return out

def main():
    panel_path = PROC / "panel.csv"
    cents = oblast_centroids()
    (PROC / "oblast_centroids.csv").write_text(
        "oblast,lat,lon\n" + "".join(f"{k},{v[0]:.5f},{v[1]:.5f}\n"
        for k, v in cents.items()))
    print(f"oblast centroids: {len(cents)}")
    if not panel_path.exists():
        print("panel.csv absent — centroid table only (build 02 first)")
        return 0
    panel = pd.read_csv(panel_path)
    panel["o_lat"] = panel["oblast_origin"].map(lambda x: cents.get(x, (None,)*2)[0])
    panel["o_lon"] = panel["oblast_origin"].map(lambda x: cents.get(x, (None,)*2)[1])
    panel["d_lat"] = panel["country_int"].map(lambda x: CAPITALS.get(x, (None,)*2)[0])
    panel["d_lon"] = panel["country_int"].map(lambda x: CAPITALS.get(x, (None,)*2)[1])
    ok = panel[["o_lat","o_lon","d_lat","d_lon"]].notna().all(axis=1)
    unmapped = sorted(panel.loc[~ok, "country_int"].dropna().unique())
    if unmapped:
        print(f"WARNING: {len(unmapped)} host country code(s) absent from "
              f"CAPITALS, distances missing: {unmapped}")
    panel.loc[ok, "dist_km"] = [
        hav(a,b,c,d) for a,b,c,d in
        panel.loc[ok, ["o_lat","o_lon","d_lat","d_lon"]].itertuples(index=False)]
    panel["log_dist"] = panel["dist_km"].map(lambda d: math.log1p(d) if pd.notna(d) else None)
    panel.to_csv(PROC / "panel_dist.csv", index=False)
    print(panel["dist_km"].describe().to_string())
    print("missing dist:", (~ok).sum())
    return 0

if __name__ == "__main__":
    sys.exit(main())
