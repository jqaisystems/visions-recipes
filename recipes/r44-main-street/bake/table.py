"""Main Street: the one table, read by the film and by score/compose.py. A miniature town of exactly 500 fictional businesses.
120 bpm, 64 beats. Streets, shops, scores, the words built from tiny blocks. Every business, score and email is fictional.
Writes assets/table.js.  Usage: python bake/table.py"""
import json, math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BPM = 120; BEAT = 60 / BPM; BEATS = 64; SW, SH = 640, 360
rng = random.Random(44)
BW, BH, ROAD = 80, 60, 10          # blocks and the streets between them
WALL = [[0.93, 0.84, 0.69], [0.91, 0.66, 0.56], [0.71, 0.76, 0.60], [0.95, 0.77, 0.45], [0.60, 0.72, 0.80], [0.90, 0.88, 0.80], [0.84, 0.55, 0.47]]
ROOF = [[0.72, 0.31, 0.20], [0.33, 0.33, 0.40], [0.80, 0.56, 0.22], [0.50, 0.25, 0.22], [0.27, 0.40, 0.42]]
PLAZA = (3, 2); PARKS = {(0, 0), (6, 1), (1, 4), (7, 5), (4, 5)}

# ---------------- plots around every block, facing the street
plots = []
for bx in range(8):
    for bz in range(6):
        if (bx, bz) == PLAZA or (bx, bz) in PARKS: continue
        x0, z0 = bx * BW + ROAD, bz * BH + ROAD; x1, z1 = (bx + 1) * BW - ROAD + 2, (bz + 1) * BH - ROAD + 2
        for x in np.arange(x0 + 6, x1 - 4, 10.5):
            plots.append((float(x), z1 - 6, 0.0)); plots.append((float(x), z0 + 6, math.pi))
        for z in np.arange(z0 + 17, z1 - 15, 10.5):
            plots.append((x0 + 6, float(z), -math.pi / 2)); plots.append((x1 - 6, float(z), math.pi / 2))
rng.shuffle(plots)
assert len(plots) >= 500, len(plots)
plots = plots[:500]
A = "COPPER FERN HARBOUR JUNIPER QUILL SAFFRON BIRCH MARLOW EMBER LARK".split()
houses = []
for x, z, r in plots:
    houses.append({"x": round(x, 1), "z": round(z, 1), "r": round(r, 3), "w": round(rng.uniform(7.2, 9.6), 1), "d": round(rng.uniform(7, 9), 1), "h": round(rng.uniform(5.5, 13), 1), "g": round(rng.uniform(2, 4.4), 1), "c": rng.randrange(len(WALL)), "k": rng.randrange(len(ROOF)), "s": 0})
cx, cz = (PLAZA[0] + 0.5) * BW, (PLAZA[1] + 0.5) * BH
def dist(h, x, z): return math.hypot(h["x"] - x, h["z"] - z)
# the hero: facing a street near the plaza, with room for a queue
facing = [i for i, h in enumerate(houses) if h["r"] == 0.0 and 200 < h["x"] < 260 and 150 < h["z"] < 240]
hero = min(facing, key=lambda i: abs(houses[i]["x"] - 230) + abs(houses[i]["z"] - 190))
H = houses[hero]; H.update(w=13.0, d=9.5, h=10.0, g=4.0, c=1, k=0)
for i, h in enumerate(houses):
    if i != hero and abs(h["x"] - H["x"]) < 26 and 0 < h["z"] - H["z"] + 18 < 34 and h["r"] == 0.0 and abs(h["x"] - H["x"]) > 0: pass
near = sorted((i for i in range(500) if i != hero and houses[i]["r"] == 0.0 and abs(houses[i]["z"] - H["z"]) < 2), key=lambda i: abs(houses[i]["x"] - H["x"]))
rej = next(i for i in near if abs(houses[i]["x"] - H["x"]) > 26)
# scores
sc = [min(39, int(abs(rng.gauss(22, 11)))) for _ in range(500)]
for i in rng.sample(range(500), 120): sc[i] = rng.randint(40, 59)
free = [i for i in range(500) if i not in (hero, rej) and dist(houses[i], H["x"], H["z"]) > 42]
surv = []
rng.shuffle(free)
for i in free:
    if all(dist(houses[i], houses[j]["x"], houses[j]["z"]) > 60 for j in surv): surv.append(i)
    if len(surv) == 28: break
if len(surv) < 28:
    for i in free:
        if i not in surv and all(dist(houses[i], houses[j]["x"], houses[j]["z"]) > 34 for j in surv): surv.append(i)
        if len(surv) == 28: break
assert len(surv) == 28, len(surv)
surv += [hero, rej]
for i in surv: sc[i] = rng.randint(62, 96)
sc[hero] = 87; sc[rej] = 64
for i, h in enumerate(houses): h["s"] = sc[i]
contacted = [hero] + rng.sample([i for i in surv if i not in (hero, rej)], 5)
# found: from the plaza outwards, on the sixteenth; the note each one plays comes from its distance
for h in houses:
    d = dist(h, cx, cz); h["f"] = round(round((4 + 9.6 * (d / 340) ** 0.75) * 4) / 4 + rng.choice((0, 0, 0.25)), 2)
    h["gone"] = round(25.5 + 0.9 * (d / 340) ** 0.85 + 1.2 * (h["s"] / 100) ** 2, 3)
# the first five shops open by the van as it passes, on the first five notes
RT = [(220, 125), (320, 125), (365, 125), (365, 65), (565, 65), (565, 245), (165, 245), (165, 5), (5, 5), (5, 305), (565, 305)]
LEN = [math.hypot(RT[i + 1][0] - RT[i][0], RT[i + 1][1] - RT[i][1]) for i in range(len(RT) - 1)]
def vanpos(b):
    u = min(1, b / 14) ** 2.2 * sum(LEN)
    for i, l in enumerate(LEN):
        if u <= l or i == len(LEN) - 1: k = min(1, u / l); return RT[i][0] + (RT[i + 1][0] - RT[i][0]) * k, RT[i][1] + (RT[i + 1][1] - RT[i][1]) * k
        u -= l
for h in houses:
    for k in range(14, 56):
        vx, vz = vanpos(k / 4)
        if dist(h, vx, vz) < 58:
            h["f"] = min(h["f"], k / 4 + rng.choice((0, 0.25, 0.5)))
            break
taken = {hero, rej}
for bt in (0, 1, 2, 3, 3.5):
    vx, vz = vanpos(bt + 0.7); j = min((i for i in range(500) if i not in taken), key=lambda i: dist(houses[i], vx, vz) + (999 if houses[i]['z'] > vz - 5 else 0)); taken.add(j); houses[j]["f"] = bt
# a fresh search: new fictional businesses, nowhere near the contacted
fresh = []
for _ in range(900):
    x, z = rng.uniform(16, SW - 16), rng.uniform(16, SH - 16)
    if ((x // BW, z // BH) == PLAZA): continue
    if (x % BW) < ROAD + 4 or (z % BH) < ROAD + 4: continue
    if all(math.hypot(x - houses[c]["x"], z - houses[c]["z"]) > 34 for c in contacted) and all(math.hypot(x - a[0], z - a[1]) > 11 for a in fresh):
        fresh.append([round(x, 1), round(z, 1), round(46.5 + 1.8 * x / SW + rng.random() * 0.4, 2), rng.randrange(len(WALL)), rng.randrange(len(ROOF)), round(rng.uniform(5, 12), 1)])
    if len(fresh) == 150: break
trees = []
for _ in range(1400):
    x, z = rng.uniform(4, SW - 4), rng.uniform(4, SH - 4); b = (int(x // BW), int(z // BH)); inner = (x % BW) > ROAD + 2 and (z % BH) > ROAD + 2
    if not inner or math.hypot(x - H['x'], z - H['z']) < 62: continue
    if b in PARKS or (rng.random() < 0.3 and b != PLAZA and all(math.hypot(x - h["x"], z - h["z"]) > 10 for h in houses)):
        trees.append([round(x, 1), round(z, 1), round(rng.uniform(3.5, 8), 1), rng.randrange(3)])
    if len(trees) >= 520: break

# ---------------- type built from tiny blocks
_f = os.path.join(ROOT, "assets", "fonts", "Archivo.ttf")
CELL = 3.6


def word(t, zc, rows_h, maxw=590):
    f = ImageFont.truetype(_f, 400); vals = []
    for a in f.get_variation_axes():
        nm = a["name"]; nm = nm.decode() if isinstance(nm, bytes) else nm
        vals.append(900 if "eight" in nm else 70 if "idth" in nm else a["default"])
    f.set_variation_by_axes(vals)
    im = Image.new("L", (8000, 800)); ImageDraw.Draw(im).text((100, 100), t, font=f, fill=255)
    im = im.crop(im.getbbox()); asp = im.width / im.height
    hh = rows_h; ww = hh * asp
    if ww > maxw: ww = maxw; hh = ww / asp
    cols, rows = int(ww / CELL), int(hh / CELL)
    a = np.asarray(im.resize((cols, rows), Image.LANCZOS)) > 120
    x0, z0 = SW / 2 - cols * CELL / 2, zc - rows * CELL / 2
    return [[round(x0 + (j + 0.5) * CELL, 1), round(z0 + (i + 0.5) * CELL, 1)] for i in range(rows) for j in range(cols) if a[i, j]]


CORAL, GOLD, BONE, INK = [0.93, 0.27, 0.17], [0.96, 0.70, 0.13], [0.97, 0.93, 0.83], [0.07, 0.06, 0.09]
words = [
    {"a": 14, "b": 17.4, "c": CORAL, "h": 15, "cells": word("SEARCH", 150, 160)},
    {"a": 17.5, "b": 21, "c": GOLD, "h": 15, "cells": word("SCORE", 150, 160)},
    {"a": 26.5, "b": 28.2, "sp": 0.45, "c": BONE, "h": 13, "cells": word("BELOW 40:", 110, 120) + word("FILTERED OUT", 245, 92, 540)},
    {"a": 28.5, "b": 30.75, "c": GOLD, "h": 22, "cells": word("30", 150, 210)},
    {"a": 37, "b": 39.5, "sp": 0.45, "c": INK, "h": 12, "cells": word("SOMETHING", 62, 90, 610)},
    {"a": 37.5, "b": 39.5, "sp": 0.45, "c": INK, "h": 12, "cells": word("SPECIFIC", 178, 90, 570)},
    {"a": 37.75, "b": 39.5, "sp": 0.45, "c": INK, "h": 12, "cells": word("ABOUT THEM.", 296, 90, 530)},
    {"a": 44.875, "b": 47, "sp": 0.45, "c": INK, "h": 14, "cells": word("YOU DECIDE", 110, 118) + word("WHAT GOES OUT.", 245, 100, 520)},
    {"a": 48.75, "b": 52.75, "c": CORAL, "h": 15, "cells": word("NO PROSPECT", 110, 110) + word("EMAILED TWICE.", 240, 100, 510)},
]
table = {
    "dur": round(BEATS * BEAT, 4), "beat": BEAT, "bpm": BPM, "beats": BEATS, "sw": SW, "sh": SH, "bw": BW, "bh": BH, "road": ROAD, "cell": CELL,
    "wall": WALL, "roof": ROOF, "plaza": PLAZA, "parks": sorted(PARKS), "houses": houses, "surv": surv, "hero": hero, "rej": rej, "contacted": contacted,
    "fresh": fresh, "trees": trees, "words": words, "cx": cx, "cz": cz,
}
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE=" + json.dumps(table, separators=(",", ":")) + ";\n")
print("hero", H["x"], H["z"], "rej", houses[rej]["x"], houses[rej]["z"], "fresh", len(fresh), "trees", len(trees), "word cells", [len(w["cells"]) for w in words])
