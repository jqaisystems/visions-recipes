"""The carving for R61 · Stacked. One lattice of blocks, carved three times, so that three level lamps (0, 45 and 90 degrees) each
throw a word onto their own wall: CODE / VIDEO / IMAGE, then SKILLS / PROMPTS / PLAYBOOK, then YOUR / OWN / STACK. Every word is drawn as a mask at the same letter proportions. The solid is where every mask, pushed along
its own lamp direction, says yes. It is then thinned: blocks are taken away one at a time, in a seeded order, for as long as every
shadow stays exactly the same. The three lattices are then matched block to block, so each rebuild slides a block from where it
was to where it's needed, a row at a time where it can.
Needs NumPy and Pillow. Writes assets/blocks.js (not committed).  Usage: python bake/carve.py"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N, H = 104, 22                      # the lattice: N by N blocks across, H blocks high
DIRS = [(1, 0), (1, 1), (0, 1)]     # each lamp's direction across the floor: 0, 45 and 90 degrees
SETS = {                            # the word each lamp casts, in each lattice. Seen from the lamps' side, 0 degrees is on the left
    "a": ["CODE", "VIDEO", "IMAGE"],
    "b": ["SKILLS", "PROMPTS", "PLAYBOOK"],
    "c": ["YOUR", "OWN", "STACK"],
}
WGHT, WDTH = 800, 100
SQUEEZE = 0.84                      # every word is set at the same proportions: this much of its natural width
MAXW = 74                           # and no word is wider than this many blocks (the diagonal counts in half diagonals)


def font(px):
    f = ImageFont.truetype(os.path.join(ROOT, "assets", "fonts", "Archivo.ttf"), px)
    f.set_variation_by_axes([WGHT, WDTH]); return f


F = font(260)
_cap = Image.new("L", (600, 500), 0); ImageDraw.Draw(_cap).text((20, 60), "H", font=F, fill=255); CAP = _cap.getbbox()   # the cap height


def mask(word, diag):
    big = Image.new("L", (3600, 500), 0); ImageDraw.Draw(big).text((20, 60), word, font=F, fill=255)
    bb = big.getbbox(); big = big.crop((bb[0], CAP[1], bb[2], CAP[3]))
    w = min(MAXW, big.width / big.height * H * SQUEEZE)          # in blocks
    wd = int(round(w * (2 ** 0.5 if diag else 1)))               # a step along the diagonal is 0.71 of a block
    return np.array(big.resize((wd, H), Image.LANCZOS)) > 120


X, Z = np.meshgrid(np.arange(N), np.arange(N), indexing="ij")
def coord(d): c = -d[1] * X + d[0] * Z; return c - c.min()
C = [coord(d) for d in DIRS]


def setup(words):
    M = []
    for word, d, c in zip(words, DIRS, C):
        L = int(c.max()) + 1; mk = mask(word, d[0] and d[1]); wd = mk.shape[1]; o = (L - wd) // 2
        m = np.zeros((H, L), bool); m[:, o:o + wd] = mk; M.append(m)
    return M


def carve(words, seed, keep=None):
    M = setup(words)
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
    extra = [0, 0, 0]
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
    lost = [(w, int(m.sum()), int((m & (cc == 0)).sum()), ex) for w, m, cc, ex in zip(words, M, cnt, extra)]
    return V, full, lost, M


def match(P, Q):
    """Pair the blocks only P has with the blocks only Q has: within a row first, in order across it, then whatever is left over."""
    sp = set(map(tuple, P)); sq = set(map(tuple, Q))
    a = sorted(sp - sq); b = sorted(sq - sp); pairs = {}
    ra, rb = {}, {}
    for p in a: ra.setdefault(p[0], []).append(p)
    for q in b: rb.setdefault(q[0], []).append(q)
    la, lb = [], []
    for y in range(H):
        u, v = ra.get(y, []), rb.get(y, []); k = min(len(u), len(v))
        for p, q in zip(u[:k], v[:k]): pairs[p] = q
        la += u[k:]; lb += v[k:]
    for p, q in zip(la, lb): pairs[p] = q
    return pairs, [q for q in lb[len(la):]]


if __name__ == "__main__":
    Vb, fb, lostb, Mb = carve(SETS["b"], 61)
    Va, fa, losta, Ma = carve(SETS["a"], 61, keep=Vb)
    Vc, fc, lostc, Mc = carve(SETS["c"], 61, keep=Vb)
    for nm, V, f, lost in (("a", Va, fa, losta), ("b", Vb, fb, lostb), ("c", Vc, fc, lostc)): print(nm, "full", f, "kept", int(V.sum()), lost)
    print("shared a&b", int((Va & Vb).sum()), "b&c", int((Vb & Vc).sum()))
    if "--dry" in sys.argv: sys.exit()
    A, B, Cc = [[tuple(int(v) for v in p) for p in np.argwhere(V)] for V in (Va, Vb, Vc)]     # (y, x, z)
    ab, newb = match(A, B); bc, newc = match(B, Cc); sb, sc = set(B), set(Cc)
    ents = []                                   # each block: where it sits in a, in b and in c, or None
    for p in A:
        q = p if p in sb else ab.get(p); r = None
        if q is not None: r = q if q in sc else bc.get(q)
        ents.append((p, q, r))
    for q in newb: ents.append((None, q, q if q in sc else bc.get(q)))
    for r in newc: ents.append((None, None, r))
    assert sorted(e[1] for e in ents if e[1]) == sorted(B) and sorted(e[2] for e in ents if e[2]) == sorted(Cc)
    flat = lambda p: [-1, -1, -1] if p is None else [p[1], p[0], p[2]]      # x, y, z
    out = {"n": N, "h": H, "words": SETS, "ents": [flat(a) + flat(b) + flat(c) for a, b, c in ents],
           "lost": {"a": losta, "b": lostb, "c": lostc}}
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    open(os.path.join(ROOT, "assets", "blocks.js"), "w", encoding="utf-8").write("window.BLOCKS=" + json.dumps(out, separators=(",", ":")) + ";")
    # proof sheets: each lattice's shadows, drawn straight from the blocks
    os.makedirs(os.path.join(ROOT, "work"), exist_ok=True)
    for nm, V, M in (("a", Va, Ma), ("b", Vb, Mb), ("c", Vc, Mc)):
        rows = []
        for m, c in zip(M, C):
            p = np.zeros(m.shape, bool)
            for y in range(H): p[y, np.unique(c[V[y]])] = True
            img = np.full(m.shape + (3,), 240, np.uint8); img[p] = (30, 30, 34); img[m & ~p] = (230, 60, 30); img[p & ~m] = (40, 120, 230)
            rows.append(np.pad(img, ((2, 2), (2, 2 + 2 * N - m.shape[1]), (0, 0)), constant_values=255))
        Image.fromarray(np.concatenate(rows, 0)).resize((rows[0].shape[1] * 6, len(rows) * rows[0].shape[0] * 6), Image.NEAREST).save(os.path.join(ROOT, "work", f"carve-{nm}.png"))
    print("blocks", len(ents), "moved a>b", len(ab), "b>c", len(bc), "- wrote assets/blocks.js and work/carve-*.png")
