"""The winding for R64 · Gist: a board covered in nails, every nail a saved signal, and one thread wound only along passes that
stay inside the word BRIEF, the way a hand-made string-art sign is made. The board is split into six theme patches, so every nail
also gets a theme. The board and its signals are a demo: no links, headlines or sources.
Needs NumPy, SciPy and Pillow.  Writes assets/wind.js (not committed) and a proof sheet to work/.
Usage: python bake/wind.py [--dry]"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1920, 1080              # the nailed area of the board, in world units (one unit is one pixel in the wide shot)
GAP = 20                       # nail spacing
JITTER = 5.0                   # how far each nail sits off the grid
SEED = 64
WORDS = ["BRIEF"]              # the word the thread winds
FIT = (0.80, 0.56)             # the most of the board's width and height the word may fill
LINE_GAP = 70
WGHT, WDTH = 800, 100
GROW, EDGE_OUT, EDGE_IN = 4, 12, 10         # a pass may stray this far outside a letter; nails within this band of its edge carry thread
MIN_PASS = 1.5 * GAP
MAX_PASSES = 300                            # per letter
STOP = 0.03                                 # stop a letter once no pass would cover this much bare letter
THEMES = 6                                  # the board's theme patches (they carry no labels on screen)
TAGS = 12                                   # nails that show a source-type tag as they land
rng = np.random.default_rng(SEED)


def font(px):
    f = ImageFont.truetype(os.path.join(ROOT, "assets", "fonts", "Archivo.ttf"), px)
    f.set_variation_by_axes([WGHT, WDTH]); return f


def layout(words, fw, fh):
    """The words set as large as fits, centred, as a mask on the board's raster (row 0 at the top)."""
    for px in range(560, 80, -4):
        f = font(px); d = ImageDraw.Draw(Image.new("L", (8, 8)))
        bs = [d.textbbox((0, 0), t, font=f) for t in words]
        ww = max(b[2] - b[0] for b in bs); hh = sum(b[3] - b[1] for b in bs) + LINE_GAP * (len(bs) - 1)
        if ww <= fw * W and hh <= fh * H: break
    im = Image.new("L", (W, H), 0); d = ImageDraw.Draw(im); y = (H - hh) / 2
    for t, b in zip(words, bs):
        d.text(((W - (b[2] - b[0])) / 2 - b[0], y - b[1]), t, font=f, fill=255); y += b[3] - b[1] + LINE_GAP
    return np.asarray(im) > 127, px


gx, gy = np.meshgrid(np.arange(GAP / 2, W, GAP), np.arange(GAP / 2, H, GAP))
NAIL = np.stack([gx.ravel(), gy.ravel()], 1) + rng.uniform(-JITTER, JITTER, (gx.size, 2))
NXI = np.clip(NAIL[:, 0].astype(int), 0, W - 1); NYI = np.clip(NAIL[:, 1].astype(int), 0, H - 1)
T = np.linspace(0.03, 0.97, 48)


def letters_in_order(mask):
    lab, n = ndimage.label(mask)
    cs = ndimage.center_of_mass(mask, lab, range(1, n + 1)); sl = ndimage.find_objects(lab)
    tops = sorted({s[0].start for s in sl}); lines = []
    for t in tops:
        if not lines or t - lines[-1] > 40: lines.append(t)
    line_of = lambda s: min(range(len(lines)), key=lambda k: abs(lines[k] - s[0].start))
    order = sorted(range(n), key=lambda k: (line_of(sl[k]), cs[k][1]))
    return [lab == k + 1 for k in order]


def wind_letter(part, mask, start_near):
    grown = ndimage.binary_dilation(mask, iterations=GROW)
    near = ndimage.binary_dilation(part, iterations=EDGE_OUT)
    edge = near & ~ndimage.binary_erosion(part, iterations=EDGE_IN)
    ids = np.where(edge[NYI, NXI])[0]
    P = NAIL[ids]
    sx = P[:, None, None, 0] + (P[None, :, None, 0] - P[:, None, None, 0]) * T
    sy = P[:, None, None, 1] + (P[None, :, None, 1] - P[:, None, None, 1]) * T
    SX = np.clip(sx.astype(int), 0, W - 1); SY = np.clip(sy.astype(int), 0, H - 1)
    ok = grown[SY, SX].mean(2) > 0.985
    ln = np.hypot(*(P[None] - P[:, None]).transpose(2, 0, 1)); ok &= ln > MIN_PASS
    cover = np.zeros((H, W), np.float32)
    cur = int(np.argmin(np.hypot(*(P - start_near).T))); passes = []; used = np.zeros_like(ok)
    def gains(rows):
        bare = 1.0 - np.minimum(cover[SY[rows], SX[rows]], 1.0)
        return np.where(ok[rows] & ~used[rows], bare.mean(-1) * np.minimum(ln[rows] / 120, 1.5), -1.0)
    for _ in range(MAX_PASSES):
        g = gains(cur); nx = int(g.argmax())
        if g[nx] < STOP:                     # nothing worth winding from here: tie off and restart behind the board, at the best pass left
            G = gains(slice(None)); a, nx = np.unravel_index(int(G.argmax()), G.shape)
            if G[a, nx] < STOP: break
            passes.append([int(ids[cur]), int(ids[a]), 0]); cur = int(a)
        used[cur, nx] = used[nx, cur] = True
        seg = Image.new("L", (W, H), 0); ImageDraw.Draw(seg).line([tuple(P[cur]), tuple(P[nx])], fill=255, width=14)
        cover += np.asarray(seg, np.float32) / 255 * 0.35
        passes.append([int(ids[cur]), int(ids[nx]), 1]); cur = int(nx)
    return passes


def themes():
    """Six patches of topic: each nail takes the theme of the nearest of six seeds, set out in a jittered three by two."""
    seeds = np.array([[(c + 0.5) / 3 * W + rng.uniform(-110, 110), (r + 0.5) / 2 * H + rng.uniform(-80, 80)] for r in range(2) for c in range(3)])
    d = np.hypot(NAIL[:, None, 0] - seeds[None, :, 0], NAIL[:, None, 1] - seeds[None, :, 1])
    d += rng.uniform(0, 26, d.shape)          # a ragged border between patches, not a ruled line
    return d.argmin(1), seeds


PAL = [(255, 98, 72), (242, 180, 106), (47, 214, 195), (150, 196, 120), (118, 170, 228), (186, 146, 222)]
def proof(passes, th, name):
    base = np.array([22, 20, 18], np.float32); thr = np.array([236, 226, 210], np.float32)
    lay = Image.new("L", (W, H), 0); d = ImageDraw.Draw(lay)
    for a, b, v in passes:
        if v: d.line([tuple(NAIL[a]), tuple(NAIL[b])], fill=255, width=1)
    acc = np.asarray(lay, np.float32)[..., None] / 255 * 0.9
    out = Image.fromarray((base + (thr - base) * acc).astype(np.uint8)); d = ImageDraw.Draw(out)
    for i, (x, y) in enumerate(NAIL):
        c = tuple(int(q * 0.6) for q in PAL[th[i]]); d.ellipse([x - 1.6, y - 1.6, x + 1.6, y + 1.6], fill=c)
    out.save(os.path.join(ROOT, "work", f"proof-{name}.png"))


os.makedirs(os.path.join(ROOT, "work"), exist_ok=True)
mask, px = layout(WORDS, *FIT)
passes, end = [], np.array([0.0, H / 2])
for part in letters_in_order(mask):
    mine = wind_letter(part, mask, end)
    if passes: passes.append([passes[-1][1], mine[0][0], 0])         # the thread runs behind the board to the next letter
    passes += mine; end = NAIL[mine[-1][1]]
# the pass held back for the reviewer is the longest of the last sixty, moved to the end so the wait reads from across the board;
# hidden jumps behind the board keep the thread one continuous run
vis_i = [j for j, p in enumerate(passes) if p[2]][-60:]
k = max(vis_i, key=lambda j: np.hypot(*(NAIL[passes[j][0]] - NAIL[passes[j][1]])))
held = passes.pop(k); passes.insert(k, [held[0], held[1], 0])
passes += [[passes[-1][1], held[0], 0], held]
used = {p for a, b, v in passes if v for p in (a, b)}
th, seeds = themes()
vis = [p for p in passes if p[2]]
lens = [float(np.hypot(*(NAIL[a] - NAIL[b]))) for a, b, v in vis]
far = np.where([i not in used for i in range(len(NAIL))])[0]
tags = [int(i) for i in rng.choice(far, TAGS, replace=False)]
print(f"{' / '.join(WORDS):10s} size {px}px  passes {len(vis):4d}  nails used {len(used):4d} of {len(NAIL)}  "
      f"pass length {min(lens):.0f} to {max(lens):.0f}  themes {np.bincount(th).tolist()}")
proof(passes, th, "brief")
out = {"w": W, "h": H, "gap": GAP, "nails": [round(float(v), 1) for v in NAIL.ravel()], "passes": passes,
       "theme": th.tolist(), "seeds": [[round(float(v), 1) for v in s] for s in seeds], "tags": tags}
if "--dry" not in sys.argv:
    open(os.path.join(ROOT, "assets", "wind.js"), "w", encoding="utf-8").write("window.WIND=" + json.dumps(out, separators=(",", ":")) + ";")
    print("wrote assets/wind.js")
