"""Clatter: the one flip schedule, read by the film and by score/compose.py.
A wall of 300 x 100 split-flap tiles, five boards of 100 rows, so each 60-tile row is one of 500 fictional businesses.
112 bpm, 64 beats. Every change on the wall is an event here: which tile, when, to what, in how many flaps.
Every business, score and email is fictional.
Writes assets/table.js, assets/events.js and bake/flips.npz (the last two are generated, not committed).  Usage: python bake/table.py"""
import base64, json, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BPM = 112; BEAT = 60 / BPM; BEATS = 64; COLS, ROWS = 300, 100; TA = 1.7; STEP = 0.035
CHARS = " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,:;'?!/-@&()+=·"
IDX = {ch: i for i, ch in enumerate(CHARS)}
DIM, BONE, ACC, ON_BONE, ON_ACC = 0, 1, 2, 3, 4
rng = np.random.default_rng(44); py = random.Random(44)
HERO, REJ = 146, 163

# ---------------- 500 fictional businesses
A = "COPPER FERN HARBOUR JUNIPER QUILL SAFFRON BIRCH MARLOW EMBER LARK THISTLE ORCHARD WREN COBALT PEBBLE SABLE ROWAN DRIFT HAZEL MOSS LINDEN FABLE KESTREL OTTER CLOVER HOLLOW NETTLE AMBLE".split()
T = [("BAKERY", "BAKERY"), ("BARBERS", "BARBER"), ("FLOWERS", "FLORIST"), ("JOINERY", "JOINERY"), ("DENTAL", "DENTIST"), ("COFFEE", "CAFE"), ("TAILORS", "TAILOR"), ("GARAGE", "GARAGE"), ("YOGA", "STUDIO"), ("PRINT", "PRINTER"), ("BREWING", "BREWERY"), ("BIKES", "BIKE SHOP"), ("GOODS", "HOMEWARE"), ("PETS", "PET SHOP"), ("BOOKS", "BOOKSHOP"), ("CERAMICS", "POTTERY"), ("ROOFING", "ROOFER"), ("LAW", "SOLICITOR")]
P = "PORT ALDER,EAST MERE,KELLOW,BRANTHAM,OLD QUAY,SALTHOLM,NORTH FEN,WYNDALE,ASHCOMBE,TARRANT".split(",")
sc = np.clip(np.abs(rng.normal(22, 11, 500)), 0, 39).astype(int)
cold = rng.choice(500, 120, replace=False); sc[cold] = rng.integers(40, 60, 120)
free = [i for i in range(500) if i not in (HERO, REJ) and not (100 <= i < 200 and 43 <= i % 100 <= 66)]
step = len(free) // 28
surv = [free[k * step + int(rng.integers(0, step))] for k in range(28)] + [HERO, REJ]
sc[surv] = rng.integers(62, 97, 30); sc[HERO] = 87; sc[REJ] = 64
contacted = [HERO] + [surv[i] for i in (2, 9, 14, 20, 25)]


def band(s): return "STRONG" if s >= 80 else "WARM" if s >= 60 else "COLD" if s >= 40 else "OUT"


names = []
for i in range(500):
    a, (t, ind) = py.choice(A), py.choice(T)
    names.append((f"{a} {t}", ind, py.choice(P)))
names[HERO] = ("TIDAL BAKERY", "BAKERY", "PORT ALDER"); names[REJ] = ("FERN JOINERY", "JOINERY", "EAST MERE")


def rowtext(i, score=None, status=""):
    n, ind, town = names[i]; s_ = "" if score is None else str(score)
    return f"{n[:19]:<19} {ind[:12]:<12} {town[:11]:<11} {s_:>3} {status[:9]:<9}"


def x0(i): return (i // 100) * 60 + 1
def y0(i): return i % 100
def cell(col, row): return row * COLS + col


SC_X = 19 + 1 + 12 + 1 + 11 + 1; ST_X = SC_X + 4

# ---------------- the wall while it's being written, and the log of what changes
c = np.zeros(COLS * ROWS, np.uint8); s = np.zeros(COLS * ROWS, np.uint8); z = np.zeros(COLS * ROWS, np.uint8)
log = []


def put(cells, chars, styles, beat, n=None, zz=None):
    """Only tiles that actually change flip. beat, chars, styles and zz may be scalars or arrays over cells."""
    cells = np.asarray(cells); m = len(cells)
    ch = np.broadcast_to(chars, (m,)).astype(np.uint8); st = np.broadcast_to(styles, (m,)).astype(np.uint8)
    zv = z[cells] if zz is None else np.broadcast_to(zz, (m,)).astype(np.uint8)
    b = np.broadcast_to(beat, (m,)).astype(np.float64)
    k = (c[cells] != ch) | (s[cells] != st) | (z[cells] != zv)
    if not k.any(): return
    nn = rng.integers(2, 6, m) if n is None else np.broadcast_to(n, (m,))
    log.append((cells[k], (b[k] * BEAT).astype(np.float32), ch[k], st[k], nn[k].astype(np.uint8), zv[k]))
    c[cells[k]] = ch[k]; s[cells[k]] = st[k]; z[cells[k]] = zv[k]


def text(col, row, t, style, beat, per=0.0, n=None, zz=None):
    cells = np.array([cell(col + i, row) for i in range(len(t))])
    chars = np.array([IDX[x] for x in t]); beats = beat + per * np.arange(len(t)) if per else beat
    put(cells, chars, style, beats, n, zz)


def q(b, g=0.25): return np.round(np.asarray(b) / g) * g


# ---------------- type made of tiles
_f = os.path.join(ROOT, "assets", "fonts", "Archivo.ttf")


def word(t, row0, rows, maxcols=272):
    """A mask over the wall: t set in Archivo, corrected for the tile's shape, centred."""
    f = ImageFont.truetype(_f, 400); vals = []
    for a in f.get_variation_axes():
        nm = a["name"]; nm = nm.decode() if isinstance(nm, bytes) else nm
        vals.append(900 if "eight" in nm else 62 if "idth" in nm else a["default"])
    f.set_variation_by_axes(vals)
    im = Image.new("L", (7000, 800)); ImageDraw.Draw(im).text((100, 100), t, font=f, fill=255)
    im = im.crop(im.getbbox()); asp = im.width / im.height
    cols = int(round(rows * TA * asp)); r0 = row0
    if cols > maxcols:
        nr = int(round(maxcols / asp / TA)); r0 = row0 + (rows - nr) // 2; rows = nr; cols = maxcols
    a = np.asarray(im.resize((cols, rows), Image.LANCZOS)) > 110
    out = np.zeros((ROWS, COLS), bool); xx = (COLS - cols) // 2; out[r0:r0 + rows, xx:xx + cols] = a
    return out


def lines(pairs):
    out = np.zeros((ROWS, COLS), bool)
    for t, r0, rw in pairs: out |= word(t, r0, rw)
    return out


Y, X = np.mgrid[0:ROWS, 0:COLS]; ALL = (Y * COLS + X).ravel(); XR = X.ravel(); YR = Y.ravel()
D = np.hypot(XR - 150, (YR - 50) * TA); DMAX = D.max()
data = np.zeros(COLS * ROWS, np.uint8)


def row_cells(i): return np.array([cell(x0(i) + k, y0(i)) for k in range(58)])
def row_chars(t): return np.array([IDX[x] for x in t])


# ---------------- 1. one tile, then a sentence, tile by tile
msg = "500 COLD RESULTS."; col0 = 134
t_i = q(3.6 * (np.arange(len(msg)) / len(msg)) ** 0.62, 0.125)
for k, ch in enumerate(msg):
    if ch != " ": put([cell(col0 + k, 50)], IDX[ch], BONE, t_i[k], n=2 if k else 1)

# ---------------- 2. the search: rows arrive from the middle out, on the sixteenth, as the camera pulls back
order = q([4 + 9.4 * (np.hypot(x0(i) + 29 - 150, (y0(i) - 50) * TA) / 175) ** 0.72 for i in range(500)])
for i in range(500):
    cl = row_cells(i); data[cl] = row_chars(rowtext(i))
    put(cl, data[cl], BONE, order[i] + np.arange(58) * 0.006)
rest = ALL[c[ALL] != data[ALL]]; put(rest, data[rest], DIM, 4.0)


# ---------------- 3. words made of the data, pushed out of the wall
def mosaic(m, beat, fill=ON_ACC, sweep=0.75, zz=30, under=DIM):
    mm = m.ravel(); b = q(beat + sweep * XR / COLS, 0.125)
    put(ALL[mm], data[ALL[mm]], fill, b[mm], zz=zz)
    if under is not None: put(ALL[~mm], data[ALL[~mm]], under, b[~mm], zz=0)


def shimmer(m, a, b, frac=0.05):
    """A few tiles of a held word re-flip on each sixteenth, so it stays alive and the groove stays in the flaps."""
    cl = ALL[m.ravel()]
    for tb in np.arange(a, b, 0.25):
        pick = cl[rng.random(len(cl)) < frac * (1.6 if (tb % 1) == 0 else 1)]
        put(pick, c[pick], s[pick], tb, n=2, zz=np.where(z[pick] % 2 == 0, z[pick] + 5, z[pick] - 5))


W1 = word("SEARCH", 8, 60); W2 = word("SCORE", 8, 60)
mosaic(W1, 14); mosaic(word("BY INDUSTRY AND LOCATION", 76, 14), 14.75, ON_BONE, 0.5, 12, None); shimmer(W1, 15, 17.25)
mosaic(W2, 17.5); mosaic(word("0 TO 100, WITH A WRITTEN REASON", 76, 14), 18.25, ON_BONE, 0.5, 12, None); shimmer(W2, 18.5, 20.75)

# ---------------- 4. every score spins, then settles
put(ALL, data[ALL], DIM, q(21 + 0.5 * D / DMAX, 0.125), zz=0)
for i in range(500):
    xx, yy = x0(i), y0(i); settle = 24.0 + 0.75 * (sc[i] / 100); sc3 = [cell(xx + SC_X + k, yy) for k in range(3)]
    for tb in np.arange(21.75, settle, 0.25):
        v = f"{int(rng.integers(0, 100)):>3}"; put(sc3, [IDX[x] for x in v], ACC, tb, n=1)
    st = ACC if sc[i] >= 60 else BONE if sc[i] >= 40 else DIM
    put(sc3, [IDX[x] for x in f"{sc[i]:>3}"], st, q(settle, 0.125), n=2)
    put([cell(xx + ST_X + k, yy) for k in range(9)], [IDX[x] for x in f"{band(sc[i]):<9}"], st, q(settle + 0.125, 0.125), n=2)
    if sc[i] >= 60: cl = row_cells(i)[:SC_X]; put(cl, data[cl], BONE, 24.875)

# ---------------- 5. the drop
od = q(25.5 + 1.1 * (D / DMAX) ** 0.8, 0.125)
for i in np.where(sc < 40)[0]:
    cl = row_cells(i); put(cl, 0, DIM, od[cl], n=4)


def solid(m, beat, style=ON_BONE, sweep=0.25, zz=25):
    mm = m.ravel(); put(ALL[mm], 0, style, q(beat + sweep * XR[mm] / COLS, 0.125), zz=zz)


def unsolid(m, beat, sweep=0.25):
    mm = m.ravel(); put(ALL[mm], 0, DIM, q(beat + sweep * XR[mm] / COLS, 0.125), zz=0)


BELOW = lines([("BELOW 40:", 8, 44), ("FILTERED OUT", 56, 36)])
solid(BELOW, 26.625); unsolid(BELOW, 27.75)
for i in np.where((sc >= 40) & (sc < 60))[0]:
    cl = row_cells(i); put(cl, 0, DIM, q(27.75 + 0.5 * D[cl] / DMAX, 0.125), n=4)
for i in surv:
    cl = row_cells(i); data[cl] = row_chars(rowtext(i, sc[i], band(sc[i]))); put(cl, data[cl], ACC, 28.25)
W30 = word("30", 6, 66); solid(W30, 28.75, ON_ACC, 0.25, 40); solid(word("QUALIFIED, OUT OF 500", 76, 15), 29.25, ON_BONE, 0.25, 15); shimmer(W30, 29.5, 30.25, 0.04)
unsolid(lines([("30", 6, 66), ("QUALIFIED, OUT OF 500", 76, 15)]), 30.5)
for i in surv:
    cl = row_cells(i); put(cl, data[cl], BONE if i in (HERO, REJ) else DIM, 30.75)

# ---------------- 6. one business, close up
hx, hy = x0(HERO), y0(HERO)
text(hx, hy - 1, "FICTIONAL BUSINESS · DEMO DATA", ACC, 31.75, 0.03)
text(hx + SC_X, hy, " 87", ON_ACC, 34.0, 0, n=9, zz=8)
text(hx, hy + 1, "NO WEBSITE. SOCIAL PAGE ONLY.", BONE, 34.75, 0.055, n=3)

# ---------------- 7. the flip, written across the whole wall
put(ALL, 0, ON_ACC, q(37 + 0.6 * np.hypot(XR - (hx + SC_X), (YR - hy) * TA) / 300, 0.0625), n=2, zz=0)
for m_, bs in ((word("SOMETHING", 6, 27), 37.25), (word("SPECIFIC", 36, 27), 37.75), (word("ABOUT THEM.", 66, 27), 38.25)):
    mm = m_.ravel(); put(ALL[mm], 0, DIM, q(bs + 0.2 * XR[mm] / COLS, 0.0625), n=2, zz=22)

# ---------------- 8. the draft, typed by the wall; a person decides
put(ALL, 0, DIM, q(39 + 0.5 * D / DMAX, 0.0625), n=2, zz=0)
put(row_cells(HERO), row_chars(rowtext(HERO, 87, "HOLD")), BONE, 39.25)
put(row_cells(REJ), row_chars(rowtext(REJ, 64, "HOLD")), BONE, 39.25)
mail = [(48, "DRAFT · NOT SENT · DEMO TEXT", ACC), (49, "TO   HELLO@TIDALBAKERY.DEMO", BONE), (51, "HI TIDAL BAKERY,", BONE),
        (52, "THE QUEUE OUTSIDE YOUR SHOP IS LOVELY, BUT THERE'S", BONE), (53, "NO WEBSITE TO SEND THOSE PEOPLE TO.", BONE),
        (54, "COULD I SHOW YOU WHAT A BRAND OF YOUR OWN", BONE), (55, "WOULD LOOK LIKE?", BONE)]
b_ = 39.5
for r_, t, st in mail:
    text(hx, r_, t, st, b_, 0.0125, n=2); b_ += len(t) * 0.0125 + 0.05


def button(col, label, style, beat, n=2, zz=0):
    for r_ in (57, 58, 59):
        tx = f"{label:^13}" if r_ == 58 else " " * 13
        text(col, r_, tx, style, beat, 0.01, n=n, zz=zz)


button(hx, "APPROVE", ON_BONE, 42.0); button(hx + 16, "REJECT", ON_BONE, 42.0)
button(hx, "APPROVE", ON_ACC, 42.625, n=3, zz=10)
text(x0(REJ) + ST_X, y0(REJ), "REJECTED ", ON_BONE, 43.25, 0.01, n=2)
put(row_cells(REJ), 0, DIM, 43.75 + (57 - np.arange(58)) * 0.012, n=4)
near = ALL[(XR >= hx - 1) & (XR < hx + 59) & (YR >= hy - 2) & (YR <= 66)]; put(near, 0, DIM, q(44.625 + 0.2 * (XR[near] - hx) / 60, 0.0625), n=2, zz=0)
solid(lines([("YOU DECIDE", 8, 42), ("WHAT GOES OUT.", 54, 38)]), 44.875)

# ---------------- 9. never twice: a fresh search crosses the wall and can't change the contacted
put(ALL, 0, DIM, q(46 + 0.5 * D / DMAX, 0.125), n=3, zz=0)
locked = np.zeros(COLS * ROWS, bool)
for i in contacted:
    cl = row_cells(i); data[cl] = row_chars(rowtext(i, sc[i], "CONTACTED")); put(cl, data[cl], ON_BONE, 46.5, n=3, zz=14); locked[cl] = True
py2 = random.Random(45)
for i in range(500):
    if i in contacted: continue
    a, (tt, ind) = py2.choice(A), py2.choice(T); names[i] = (f"{a} {tt}", ind, py2.choice(P))
    cl = row_cells(i); data[cl] = row_chars(rowtext(i, int(rng.integers(0, 100)), ""))
    put(cl, data[cl], DIM, q(47 + 1.6 * x0(i) / 300 + rng.uniform(0, 0.25), 0.125) + np.arange(58) * 0.004)
mm = lines([("NO PROSPECT", 8, 40), ("EMAILED TWICE.", 52, 40)]).ravel() & ~locked
put(ALL[mm], data[ALL[mm]], ON_ACC, q(49 + 0.75 * XR[mm] / COLS, 0.125), zz=25)
M_ = np.zeros(COLS * ROWS, bool); M_[mm] = True; shimmer(M_.reshape(ROWS, COLS), 50, 52.25)
put(ALL[mm], data[ALL[mm]], DIM, q(52.5 + 0.25 * XR[mm] / COLS, 0.125), zz=0)

# ---------------- 10. the close: the wall empties towards the first tile, and the last flap falls
col_l, row_l = 150, 50; lc = cell(col_l, row_l)
d2 = np.hypot(XR - col_l, (YR - row_l) * TA); o_ = q(53.25 + 3.2 * (1 - d2 / d2.max()) ** 0.7, 0.0625)
others = ALL[ALL != lc]; put(others, 0, DIM, o_[others], n=3, zz=0)
put([lc], IDX["·"], BONE, 55.5, n=2)
put([lc], 0, DIM, 56.75, n=1)

# ---------------- out
cells = np.concatenate([l[0] for l in log]); ts = np.concatenate([l[1] for l in log]); chs = np.concatenate([l[2] for l in log])
sts = np.concatenate([l[3] for l in log]); nss = np.concatenate([l[4] for l in log]); zs = np.concatenate([l[5] for l in log])
o = np.lexsort((ts, cells)); cells, ts, chs, sts, nss, zs = cells[o], ts[o], chs[o], sts[o], nss[o], zs[o]
off = np.searchsorted(cells, np.arange(COLS * ROWS + 1)).astype(np.uint32)
b64 = lambda a: base64.b64encode(a.tobytes()).decode()
open(os.path.join(ROOT, "assets", "events.js"), "w").write("window.EV=" + json.dumps({"off": b64(off), "t": b64(ts), "c": b64(chs), "s": b64(sts), "n": b64(nss), "z": b64(zs)}) + ";\n")
np.savez_compressed(os.path.join(ROOT, "bake", "flips.npz"), t=ts, n=nss, x=(cells % COLS).astype(np.uint16), step=STEP)
meta = {"dur": round(BEATS * BEAT, 4), "beat": round(BEAT, 6), "bpm": BPM, "beats": BEATS, "cols": COLS, "rows": ROWS, "ta": TA, "step": STEP, "chars": CHARS, "hx": hx, "hy": hy, "scx": SC_X}
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE=" + json.dumps(meta, ensure_ascii=False) + ";\n")
print("events", len(ts), "steps", int(nss.sum()), "MB", round(os.path.getsize(os.path.join(ROOT, "assets", "events.js")) / 1e6, 1), "dur", meta["dur"])
