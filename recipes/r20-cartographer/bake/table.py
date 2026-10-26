"""R20 · Cartographer. The one table: the map of one made-up business (its coast, six regions and a relief of where
the hours go), the twelve opportunities with their payoff, cost and risk, which are knocked flat, the ranking with a
reason for each, the three-phase route and the film's clock.
Writes ../assets/table.js for the film and table.json for the score, so every sound lands on what you see.
Heights are relative: the film shows no hours, no savings and no ROI.
Usage: python table.py   (standard library only, seeded)"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
rng = random.Random(20)

# the clock of the film, in seconds
T = dict(
    lamp=[0.2, 1.6],                  # the lamp comes up over the chart table
    audit=[3.8, 8.0],                 # the survey ring sweeps out from the centre, the fog lifts, the land rises
    pins=8.9, pinGap=0.17,            # the opportunities drop in, one every 0.17 s
    knock=[11.5, 11.8, 12.1, 12.4],   # four are knocked flat
    rank=13.9, rankGap=0.12,          # the standing pins lift off and line up along the table's edge
    tags=15.0,
    dividers=17.9, legs=[[18.3, 19.8], [19.95, 21.3], [21.45, 22.45]],
    compass=[22.5, 23.4],
    sink=[23.7, 24.5],                # the relief settles into the paper, the route is printed on it
    lift=[24.6, 25.2], roll=[25.0, 26.3], tie=[26.3, 26.7],
    word=[26.8, 28.4], end=29.0,
)
SWEEP_TURNS = 2                       # the survey beam turns twice while the ring opens

# the map: the table is x -8.8..8.8, z -5.5..5.5 (z grows toward the camera); the island is the business
MAP_W, MAP_D = 17.6, 11.0
NX, NZ, CELL = 150, 94, 0.108
COAST = dict(rx=7.3, rz=4.35, waves=[[3, 0.07, 1.1], [5, 0.05, 2.3], [9, 0.035, 0.4], [14, 0.02, 5.0]])


def coast_r(th):
    # the coast's distance from the centre at angle th, as a fraction of the base ellipse
    return 1 + sum(a * math.sin(k * th + p) for k, a, p in COAST["waves"])


def on_land(x, z):
    th = math.atan2(z / COAST["rz"], x / COAST["rx"])
    return math.hypot(x / COAST["rx"], z / COAST["rz"]) < coast_r(th)


COASTLINE = []
for k in range(360):
    th = 2 * math.pi * k / 360
    f = coast_r(th)
    COASTLINE.append([round(COAST["rx"] * f * math.cos(th), 3), round(COAST["rz"] * f * math.sin(th), 3)])

# six regions; hours is relative, it only sets how high the land rises
REGIONS = [
    dict(name="Quotes", x=-4.3, z=1.3, hours=1.0),
    dict(name="Support", x=0.2, z=1.9, hours=0.9),
    dict(name="Finance", x=4.6, z=1.4, hours=0.62),
    dict(name="Content", x=4.2, z=-2.3, hours=0.48),
    dict(name="Sales", x=0.6, z=-2.5, hours=0.56),
    dict(name="Hiring", x=-3.9, z=-2.5, hours=0.34),
]


def region_of(x, z):
    return min(range(len(REGIONS)), key=lambda i: (x - REGIONS[i]["x"]) ** 2 + (z - REGIONS[i]["z"]) ** 2)


# smooth value noise for the texture of the land
GRID = [[rng.random() for _ in range(40)] for _ in range(40)]


def vnoise(x, z):
    gx, gz = (x + 9) * 1.4, (z + 6) * 1.4
    i, j = int(gx), int(gz)
    fx, fz = gx - i, gz - j
    sx, sz = fx * fx * (3 - 2 * fx), fz * fz * (3 - 2 * fz)
    a, b = GRID[i][j], GRID[i + 1][j]
    c, d = GRID[i][j + 1], GRID[i + 1][j + 1]
    return (a + (b - a) * sx) * (1 - sz) + (c + (d - c) * sx) * sz


def height(x, z):
    h = 0.06
    for rg in REGIONS:
        d2 = (x - rg["x"]) ** 2 + (z - rg["z"]) ** 2
        h += 1.55 * rg["hours"] * math.exp(-d2 / (2 * 1.45 ** 2))
    h += 0.22 * (vnoise(x, z) - 0.4)
    # the land slopes down to the coast
    th = math.atan2(z / COAST["rz"], x / COAST["rx"])
    edge = coast_r(th) - math.hypot(x / COAST["rx"], z / COAST["rz"])
    h *= min(1, max(0.12, edge / 0.22))
    return max(0.04, round(h / 0.06) * 0.06)        # stepped like contour lines


# the columns: one per land cell; [i, j, height in hundredths, region]
X0, Z0 = -(NX - 1) / 2 * CELL, -(NZ - 1) / 2 * CELL
COLS = []
for j in range(NZ):
    for i in range(NX):
        x, z = X0 + i * CELL, Z0 + j * CELL
        if on_land(x, z):
            COLS.append([i, j, int(round(height(x, z) * 100)), region_of(x, z)])

# the opportunities: payoff, cost and risk from 0 (low) to 1 (high); rank 0 means knocked flat (not worth building)
PINS = [
    dict(name="Quote drafting", x=-3.8, z=2.1, payoff=0.92, cost=0.3, risk=0.2, rank=1, why="The biggest pile of hours, low risk"),
    dict(name="Inbox triage", x=0.2, z=2.6, payoff=0.8, cost=0.25, risk=0.15, rank=2, why="Every day, and easy to undo"),
    dict(name="Invoice matching", x=4.2, z=1.7, payoff=0.74, cost=0.3, risk=0.2, rank=3, why="Repetitive, and the rules are clear"),
    dict(name="Repurposing posts", x=5.0, z=-1.6, payoff=0.66, cost=0.35, risk=0.25, rank=4, why="Ends the weekly scramble"),
    dict(name="Lead follow-up drafts", x=1.8, z=-2.4, payoff=0.64, cost=0.4, risk=0.3, rank=5, why="Your voice, kept in review"),
    dict(name="Answer library", x=-0.7, z=-0.2, payoff=0.6, cost=0.5, risk=0.25, rank=6, why="Builds on the inbox triage"),
    dict(name="Interview scheduling", x=-3.4, z=-2.6, payoff=0.5, cost=0.45, risk=0.2, rank=7, why="Small, but it comes every week"),
    dict(name="Pricing from past jobs", x=-6.0, z=-0.5, payoff=0.72, cost=0.8, risk=0.45, rank=8, why="A bigger play, needs clean data first"),
    dict(name="A chatbot for everything", x=2.6, z=-0.3, payoff=0.4, cost=0.85, risk=0.8, rank=0, why="Not worth building"),
    dict(name="Auto-screen CVs", x=-5.3, z=-3.0, payoff=0.35, cost=0.5, risk=0.9, rank=0, why="Not worth building"),
    dict(name="Rebuild the books", x=6.0, z=0.3, payoff=0.45, cost=0.95, risk=0.75, rank=0, why="Not worth building"),
    dict(name="Video at scale", x=3.2, z=-3.6, payoff=0.3, cost=0.8, risk=0.6, rank=0, why="Not worth building"),
]
DROP_ORDER = [0, 8, 2, 5, 9, 4, 1, 10, 7, 3, 11, 6]   # the order they land in, scattered over the map
for n, k in enumerate(DROP_ORDER):
    PINS[k]["drop"] = round(T["pins"] + T["pinGap"] * n, 3)
KNOCKED = [k for k, p in enumerate(PINS) if p["rank"] == 0]
for n, k in enumerate(KNOCKED):
    PINS[k]["knock"] = T["knock"][n]
for p in PINS:
    p["region"] = region_of(p["x"], p["z"])
    p["h"] = round(1.4 + 0.5 * p["payoff"] if p["rank"] == 0 else 2.5 - 0.15 * (p["rank"] - 1), 3)
    if p["rank"]:
        p["rankT"] = round(T["rank"] + T["rankGap"] * (p["rank"] - 1), 3)

# the route: three legs through the ranked pins, in order
PHASES = [dict(name="First", span="0 to 3 months", ranks=[1, 2, 3]),
          dict(name="Second", span="3 to 6 months", ranks=[3, 4, 5, 6]),
          dict(name="Third", span="6 to 12 months", ranks=[6, 7, 8])]
STRIDE = 1.6                           # the dividers' step along the route, in table units
SEG = 100                              # route samples between two ranked pins

WAY = [next(p for p in PINS if p["rank"] == k) for k in range(1, 9)]


def catmull(p0, p1, p2, p3, u):
    return [0.5 * (2 * b + (-a + c) * u + (2 * a - 5 * b + 4 * c - d) * u * u + (-a + 3 * b - 3 * c + d) * u ** 3)
            for a, b, c, d in zip(p0, p1, p2, p3)]


def drape(x, z):
    # the route rides just above the tallest column under it, so the relief never cuts through the line
    best = 0.0
    for dx in (-0.16, 0, 0.16):
        for dz in (-0.16, 0, 0.16):
            if on_land(x + dx, z + dz):
                best = max(best, height(x + dx, z + dz))
    return best + 0.08


P2 = [[w["x"], w["z"]] for w in WAY]
P2 = [P2[0]] + P2 + [P2[-1]]
ROUTE = []
for k in range(len(WAY) - 1):
    for n in range(SEG if k < len(WAY) - 2 else SEG + 1):
        x, z = catmull(P2[k], P2[k + 1], P2[k + 2], P2[k + 3], n / SEG)
        ROUTE.append([x, drape(x, z), z])
ys = [p[1] for p in ROUTE]
for i, p in enumerate(ROUTE):                       # widen the lift a little so the line clears every corner
    p[1] = round(max(ys[max(0, i - 3): i + 4]), 3)
    p[0], p[2] = round(p[0], 3), round(p[2], 3)
ARC = [0.0]
for a, b in zip(ROUTE, ROUTE[1:]):
    ARC.append(round(ARC[-1] + math.dist(a, b), 4))

# the strides: each leg is cut into whole strides; a stride is [t0, t1, from, planted, to] as arc lengths
STRIDES = []
for k, ph in enumerate(PHASES):
    a0, a1 = ARC[(ph["ranks"][0] - 1) * SEG], ARC[(ph["ranks"][-1] - 1) * SEG]
    t0, t1 = T["legs"][k]
    n = max(1, round((a1 - a0) / STRIDE))
    ph["arc"] = [a0, a1]
    for j in range(n):
        prev = STRIDES[-1][3] if STRIDES else a0          # the free foot starts where the last planted foot was
        STRIDES.append([round(t0 + (t1 - t0) * j / n, 3), round(t0 + (t1 - t0) * (j + 1) / n, 3),
                        prev, round(a0 + (a1 - a0) * j / n, 4), round(a0 + (a1 - a0) * (j + 1) / n, 4)])

TABLE = dict(T=T, sweepTurns=SWEEP_TURNS, map=dict(w=MAP_W, d=MAP_D, nx=NX, nz=NZ, cell=CELL, x0=X0, z0=Z0),
             coast=COASTLINE, regions=REGIONS, cols=COLS, pins=PINS, knocked=KNOCKED, phases=PHASES, stride=STRIDE,
             seg=SEG, route=ROUTE, arc=ARC, strides=STRIDES)
with open(os.path.join(HERE, "..", "assets", "table.js"), "w", encoding="utf-8", newline="\n") as f:
    f.write("window.TABLE = " + json.dumps(TABLE, ensure_ascii=False, separators=(",", ":")) + ";\n")
with open(os.path.join(HERE, "table.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump({k: v for k, v in TABLE.items() if k not in ("cols", "route", "arc")}, f, ensure_ascii=False, indent=1)
print("route length:", ARC[-1], "strides:", len(STRIDES), [s[:2] for s in STRIDES][:4], [p["arc"] for p in PHASES])
print("columns:", len(COLS), "max height:", max(c[2] for c in COLS) / 100, "pins:", len(PINS))
for k, p in enumerate(PINS):
    print(k, p["name"], REGIONS[p["region"]]["name"], "rank", p["rank"], "h", p["h"])
