"""The carving for R58 · Casting. One lattice of blocks, carved so that each level lamp throws a different exact word.
Every word is drawn as a mask. The solid is where every mask, pushed along its own lamp's direction, says yes. It is then thinned:
blocks are taken away one at a time, in a seeded order, for as long as every shadow stays exactly the same. What's left looks like a
tangle and casts perfect words. Two lattices are carved: one for three lamps and one for four, sharing as many blocks as they can.
Needs NumPy and Pillow. Writes assets/blocks.js (not committed).  Usage: python bake/carve.py"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N, H = 104, 22                      # the lattice: N by N blocks across, H blocks high
LAMPS = [                           # each lamp: the word it casts, its direction across the floor (dx, dz), and how wide the word sits
    ("RESEARCH", (1, 0), 0.84),
    ("DRAFT", (1, 1), 0.58),
    ("REVIEW", (0, 1), 0.82),
    ("PUBLISH", (-1, 1), 0.64),
]
WGHT, WDTH = 800, 100


def font(px):
    f = ImageFont.truetype(os.path.join(ROOT, "assets", "fonts", "Archivo.ttf"), px)
    f.set_variation_by_axes([WGHT, WDTH]); return f


def mask(word, w, h):
    F = font(260); big = Image.new("L", (3000, 400), 0); ImageDraw.Draw(big).text((20, 20), word, font=F, fill=255)
    big = big.crop(big.getbbox()).resize((w, h), Image.LANCZOS); return np.array(big) > 120


X, Z = np.meshgrid(np.arange(N), np.arange(N), indexing="ij")
def coord(d): c = -d[1] * X + d[0] * Z; return c - c.min()


def setup(k):
    M, C = [], []
    for word, d, fr in LAMPS[:k]:
        c = coord(d); L = int(c.max()) + 1; wd = int(round(L * fr)); o = (L - wd) // 2
        m = np.zeros((H, L), bool); m[:, o:o + wd] = mask(word, wd, H); M.append(m); C.append(c)
    return M, C


def carve(k, seed, keep=None):
    M, C = setup(k)
    V = np.ones((H, N, N), bool)
    for m, c in zip(M, C): V &= m[:, c]
    full = int(V.sum())
    cnt = []
    for m, c in zip(M, C):
        cc = np.zeros(m.shape, int)
        for y in range(H): np.add.at(cc[y], c[V[y]], 1)
        cnt.append(cc)
    rng = np.random.default_rng(seed); idx = np.argwhere(V); rng.shuffle(idx)
    if keep is not None:   # thin the blocks the other lattice doesn't have first, so the two share as many as they can
        idx = np.array(sorted(idx.tolist(), key=lambda p: bool(keep[p[0], p[1], p[2]])))
    for y, x, z in idx:
        if all(cc[y, c[x, z]] > 1 for cc, c in zip(cnt, C)):
            V[y, x, z] = False
            for cc, c in zip(cnt, C): cc[y, c[x, z]] -= 1
    # repair: a pixel no block can cast gets one block anyway, placed where it costs least: where the other words are already on,
    # or failing that where its stray pixel only thickens the edge of a letter
    def edge(m, y, c):
        return any(0 <= y + a < m.shape[0] and 0 <= c + b < m.shape[1] and m[y + a, c + b] for a, b in ((0, 1), (0, -1), (1, 0), (-1, 0)))
    extra = [0] * k
    for i, (m, c, cc) in enumerate(zip(M, C, cnt)):
        for y, cv in np.argwhere(m & (cc == 0)):
            best = None
            for x, z in np.argwhere(c == cv):
                cost = 0
                for j, (mj, cj) in enumerate(zip(M, C)):
                    if j == i: continue
                    q = cj[x, z]
                    if not mj[y, q]: cost += 1 if edge(mj, y, q) else 10
                if best is None or cost < best[0]: best = (cost, x, z)
            _, x, z = best; V[y, x, z] = True
            for j, (mj, cj) in enumerate(zip(M, C)):
                if cnt[j][y, cj[x, z]] == 0 and not mj[y, cj[x, z]]: extra[j] += 1
                cnt[j][y, cj[x, z]] += 1
    lost = []
    for (word, d, fr), m, c, cc, ex in zip(LAMPS, M, C, cnt, extra):
        lost.append((word, int(m.sum()), int((m & (cc == 0)).sum()), ex))
    # how many shadows need each block: a block is needed by a shadow when it's the only one casting some pixel of it
    need = np.zeros(V.shape, int)
    for c, cc in zip(C, cnt):
        for y in range(H): need[y][V[y]] += (cc[y, c[V[y]]] == 1)
    return V, need, full, lost


if __name__ == "__main__":
    V4, need4, f4, lost4 = carve(4, 58)
    V3, need3, f3, lost3 = carve(3, 58, keep=V4)
    print("4 lamps: full", f4, "kept", int(V4.sum()), lost4)
    print("3 lamps: full", f3, "kept", int(V3.sum()), lost3, "shared with 4:", int((V3 & V4).sum()))
    if "--dry" in sys.argv: sys.exit()
    pts = lambda V, nd: [[int(x), int(y), int(z), int(nd[y, x, z])] for y, x, z in np.argwhere(V)]
    out = {"n": N, "h": H, "lamps": [[w, list(d), fr] for w, d, fr in LAMPS], "three": pts(V3, need3), "four": pts(V4, need4),
           "lost": {"three": lost3, "four": lost4}}
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    open(os.path.join(ROOT, "assets", "blocks.js"), "w", encoding="utf-8").write("window.BLOCKS=" + json.dumps(out, separators=(",", ":")) + ";")
    # proof sheets: each lattice's shadows, drawn straight from the blocks
    for nm, V in (("three", V3), ("four", V4)):
        M, C = setup(4 if nm == "four" else 3); rows = []
        for m, c in zip(M, C):
            p = np.zeros(m.shape, bool)
            for y in range(H): p[y, np.unique(c[V[y]])] = True
            img = np.full(m.shape + (3,), 240, np.uint8); img[p] = (30, 30, 34); img[m & ~p] = (230, 60, 30); img[p & ~m] = (40, 120, 230)
            rows.append(np.pad(img, ((2, 2), (2, 2 + 2 * N - m.shape[1]), (0, 0)), constant_values=255))
        os.makedirs(os.path.join(ROOT, "work"), exist_ok=True)
        Image.fromarray(np.concatenate(rows, 0)).resize((rows[0].shape[1] * 6, len(rows) * rows[0].shape[0] * 6), Image.NEAREST).save(os.path.join(ROOT, "work", f"carve-{nm}.png"))
    print("wrote assets/blocks.js and work/carve-*.png")
