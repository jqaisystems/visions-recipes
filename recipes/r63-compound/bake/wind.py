"""The winding for R63 · Compound: a ring of nails and four threads that, pass by pass, draw a flower. Read by the film and by
score/compose.py.

The picture is drawn in code (no image goes in): a flower head of twelve petals, a seed disc, a stem and two leaves, split into one
brightness map per thread. The film's thread is light on a dark board and adds up, so each map says how much light that thread's
colour should leave on each spot. From the nail it is on, a thread takes the pass (a straight line to another nail, never a near
neighbour) that covers the most light still owed, then takes that light off. A bone thread draws the whole flower first; coral, amber
and teal threads then wind over it. Every pass is baked here, so any frame of the film knows which passes are laid.

Needs NumPy and Pillow (for the proof sheet only).  Writes assets/wind.js (not committed) and work/wind-proof.png.
Usage: python bake/wind.py"""
import json, os
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N = 300                 # nails in the ring
R = 480.0               # ring radius, world units (about a pixel each in the wide shot)
S = 640                 # bake resolution across the ring
GAP = 16                # a pass never goes to a nail closer than this round the ring
# each thread: name, colour (linear rgb, for the proof), how many passes at most, how much light one pass leaves
THREADS = [
    ("bone", (0.93, 0.89, 0.80), 1500, 0.05),
    ("coral", (1.00, 0.31, 0.21), 320, 0.07),
    ("amber", (0.95, 0.70, 0.42), 160, 0.07),
    ("teal", (0.18, 0.84, 0.76), 200, 0.07),
]
PEN = {"bone": 0.03, "coral": 0.07, "amber": 0.07, "teal": 0.07}   # what a pass pays for crossing empty board
ALPHA = 1.15          # how bright one pass looks in the wide shot, per unit of light it carries
STOP = 0.002            # a thread stops early when no pass would still add this much light on average

# ---------------- the picture, in ring units: x right, y up, the ring is the unit circle
y, x = np.mgrid[0:S, 0:S].astype(np.float64)
u = (x - (S - 1) / 2) / (S / 2); v = ((S - 1) / 2 - y) / (S / 2)
sm = lambda a: np.clip(a, 0, 1) ** 2 * (3 - 2 * np.clip(a, 0, 1))
HC = (0.0, 0.17)                                   # the flower head's centre
du, dv = u - HC[0], v - HC[1]; rr = np.hypot(du, dv); a = np.arctan2(dv, du) + 0.13
lobe = np.abs(np.cos(6 * a))                       # twelve petals
rp = 0.17 + 0.33 * lobe ** 1.4                     # each petal's reach
edge = sm((rp - rr) / 0.035)                       # soft petal edges
along = np.clip((rr - 0.12) / np.maximum(rp - 0.12, 1e-3), 0, 1)
vein = 1 - 0.35 * np.exp(-(np.sin(6 * a) ** 2) / 0.006) * sm(along * 3)   # a darker crease down each petal
petal = edge * (rr > 0.11) * (0.45 + 0.55 * along ** 0.7) * vein
disc = sm((0.135 - rr) / 0.02)
seeds = disc * (0.18 + 0.5 * (np.cos(34 * rr + 7 * a) > 0.55))            # seeds in a spiral
rim = np.exp(-((rr - 0.135) / 0.018) ** 2)
# the stem: a slow curve from the head down to the ring
sx = 0.045 * np.sin((v + 1) * 2.1); stem = sm((0.022 - np.abs(u - sx)) / 0.01) * (v < HC[1] - 0.1) * (v > -1.0)
def leaf(cx, cy, ang, L, Wd):
    c, s = np.cos(ang), np.sin(ang); px = (u - cx) * c + (v - cy) * s; py = -(u - cx) * s + (v - cy) * c
    t = px / L; half = Wd * np.sqrt(np.clip(t * (1 - t), 0, None)) * 2
    inside = sm((half - np.abs(py)) / 0.012) * (t > 0) * (t < 1)
    return inside * (0.55 + 0.45 * (1 - np.exp(-(py / 0.008) ** 2)))           # a midrib
leaves = np.maximum(leaf(0.03, -0.42, np.pi * 0.86, 0.36, 0.11), leaf(0.05, -0.62, np.pi * 0.12, 0.34, 0.10))
green = np.maximum(stem * 0.8, leaves)
inring = sm((0.975 - np.hypot(u, v)) / 0.02)
MAPS = {
    "bone": np.maximum.reduce([petal * 0.62, seeds * 0.9, rim * 0.55, green * 0.42]) * inring,
    "coral": petal * sm((along - 0.35) / 0.3) * 0.75 * inring,
    "amber": np.maximum(petal * (1 - sm((along - 0.3) / 0.35)) * 0.8, rim * 0.95) * inring,
    "teal": green * 0.8 * inring,
}

# ---------------- the nails, and every pass as the pixels it covers
ang = np.pi / 2 - 2 * np.pi * np.arange(N) / N   # nail 0 at the top, then clockwise
NXw, NYw = R * np.cos(ang), R * np.sin(ang)
PX = (S - 1) / 2 + NXw / R * (S / 2) * 0.995; PY = (S - 1) / 2 - NYw / R * (S / 2) * 0.995
CACHE = {}
def pix(i, j):
    k = (i, j) if i < j else (j, i)
    if k not in CACHE:
        L = int(np.hypot(PX[i] - PX[j], PY[i] - PY[j])) + 1; t = np.linspace(0, 1, L)
        CACHE[k] = (np.rint(PY[i] + (PY[j] - PY[i]) * t).astype(np.int32) * S + np.rint(PX[i] + (PX[j] - PX[i]) * t).astype(np.int32))
    return CACHE[k]
ok = lambda i, j: min(abs(i - j), N - abs(i - j)) >= GAP

def wind(target, n, w, pen, start=None):
    res = target.flatten().copy(); res[res < 0.02] = -pen   # empty board costs: passes stay on the picture
    if start is None:   # start on the nail whose best pass covers the most light
        start = max(range(0, N, 3), key=lambda i: max(res[pix(i, j)].mean() for j in range(N) if ok(i, j)))
    cur, seq = start, [start]
    for _ in range(n):
        best, bj = -1.0, -1
        for j in range(N):
            if not ok(cur, j): continue
            s = res[pix(cur, j)].mean()
            if s > best: best, bj = s, j
        if best < STOP: break
        idx = pix(cur, bj); res[idx] -= w; cur = bj; seq.append(bj)
    return seq

OUT = []
for name, col, n, w in THREADS:
    seq = wind(MAPS[name], n, w, PEN[name], 0 if name == "bone" else None)
    OUT.append({"name": name, "seq": seq})
    print(f"{name}: {len(seq) - 1} passes from nail {seq[0]}")

wind_js = {"n": N, "r": R, "nails": [round(float(q), 2) for p in zip(NXw, NYw) for q in p], "threads": OUT}
os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
open(os.path.join(ROOT, "assets", "wind.js"), "w", encoding="utf-8").write("window.WIND=" + json.dumps(wind_js, separators=(",", ":")) + ";")

# ---------------- the proof: the target, the bone thread alone, and all four, drawn the way the film adds thread up
try:
    from PIL import Image
    D = 900; acc = np.zeros((D, D, 3))
    def lay(seq, col, alpha):
        for p in range(len(seq) - 1):
            i, j = seq[p], seq[p + 1]; L = int(np.hypot(NXw[i] - NXw[j], NYw[i] - NYw[j]) * D / (2 * R) * 2) + 1; t = np.linspace(0, 1, L)
            fx = D / 2 + (NXw[i] + (NXw[j] - NXw[i]) * t) * D / (2 * R) * 0.99; fy = D / 2 - (NYw[i] + (NYw[j] - NYw[i]) * t) * D / (2 * R) * 0.99
            x0 = np.floor(fx).astype(int); y0 = np.floor(fy).astype(int); ax = fx - x0; ay = fy - y0
            for ox, oy, ww in ((0, 0, (1 - ax) * (1 - ay)), (1, 0, ax * (1 - ay)), (0, 1, (1 - ax) * ay), (1, 1, ax * ay)):
                for c in range(3): np.add.at(acc[:, :, c], (np.clip(y0 + oy, 0, D - 1), np.clip(x0 + ox, 0, D - 1)), ww * 0.5 * alpha * col[c])
    tone = lambda c: np.clip((c / (1 + c * 0.6)) ** (1 / 2.2) * 255 + 8, 0, 255).astype(np.uint8)
    tgt = sum(MAPS[n_][:, :, None] * np.array(c_) for n_, c_, _, _ in THREADS)
    panels = [Image.fromarray(tone(tgt * 1.3)).resize((D, D))]
    lay(OUT[0]["seq"], THREADS[0][1], ALPHA * THREADS[0][3]); panels.append(Image.fromarray(tone(acc.copy())))
    for k in range(1, 4): lay(OUT[k]["seq"], THREADS[k][1], ALPHA * THREADS[k][3])
    panels.append(Image.fromarray(tone(acc)))
    sheet = Image.new("RGB", (D * 3 + 20, D), (0, 0, 0))
    for k, p in enumerate(panels): sheet.paste(p, (k * (D + 10), 0))
    os.makedirs(os.path.join(ROOT, "work"), exist_ok=True); sheet.save(os.path.join(ROOT, "work", "wind-proof.png"))
except ImportError:
    pass
