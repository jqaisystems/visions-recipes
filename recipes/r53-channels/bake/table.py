"""The one table for R53 · Channels, read by the film and by score/compose.py: the beat grid, the islands, every channel the fingertip cuts,
the streams that run down them, and the captions. The workflow is a demo. Writes assets/table.js (not committed).  Usage: python bake/table.py"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1920, 1080
PORTRAIT = H > W
P = PORTRAIT
BPM = 96; BEAT = 60 / BPM; BEATS = 58

# ---------------- a single-stroke font, drawn by hand. x 0 to .7, y 0 to 1
F = {
    "A": "0,0 .35,1 .7,0|.13,.38 .57,.38", "B": "0,0 0,1 .45,1 .62,.88 .62,.64 .45,.52 0,.52|.45,.52 .68,.4 .68,.13 .48,0 0,0", "C": ".68,.82 .5,1 .2,1 0,.78 0,.22 .2,0 .5,0 .68,.18",
    "D": "0,0 0,1 .4,1 .68,.75 .68,.25 .4,0 0,0", "E": ".68,1 0,1 0,0 .68,0|0,.52 .5,.52", "F": ".68,1 0,1 0,0|0,.52 .5,.52", "G": ".68,.82 .5,1 .2,1 0,.78 0,.22 .2,0 .5,0 .68,.2 .68,.46 .38,.46",
    "H": "0,0 0,1|.68,0 .68,1|0,.52 .68,.52", "I": ".14,1 .14,0", "J": ".6,1 .6,.2 .42,0 .18,0 0,.2", "K": "0,0 0,1|.68,1 0,.42|.22,.58 .7,0", "L": "0,1 0,0 .62,0",
    "M": "0,0 0,1 .38,.35 .76,1 .76,0", "N": "0,0 0,1 .68,0 .68,1", "O": ".2,0 0,.22 0,.78 .2,1 .5,1 .7,.78 .7,.22 .5,0 .2,0", "P": "0,0 0,1 .46,1 .66,.84 .66,.6 .46,.44 0,.44",
    "R": "0,0 0,1 .46,1 .66,.84 .66,.6 .46,.44 0,.44|.36,.44 .7,0", "S": ".66,.84 .48,1 .2,1 .02,.84 .02,.64 .2,.52 .5,.48 .68,.34 .68,.16 .5,0 .2,0 0,.16",
    "T": "0,1 .7,1|.35,1 .35,0", "U": "0,1 0,.22 .2,0 .5,0 .7,.22 .7,1", "V": "0,1 .35,0 .7,1", "W": "0,1 .2,0 .4,.7 .6,0 .8,1", "Y": "0,1 .35,.48 .7,1|.35,.48 .35,0",
    "X": "0,1 .68,0|0,0 .68,1", "Z": "0,1 .68,1 0,0 .68,0",
    "'": ".1,1 .06,.76", "-": ".04,.44 .44,.44", ".": ".06,.05 .06,0", ",": ".08,.08 .02,-.14",
}
GL = {c: [[tuple(float(v) for v in p.split(",")) for p in st.split()] for st in s.split("|")] for c, s in F.items()}
WID = {c: max(q[0] for st in g for q in st) for c, g in GL.items()}


def width(s, h, track=0.28):
    return sum((WID.get(c, 0.34) + track) * h for c in s) - track * h


def text(s, cx, y, h, align="c", track=0.28):
    wd = width(s, h, track); x = cx - (wd / 2 if align == "c" else 0); out = []
    for c in s:
        for st in GL.get(c, []): out.append([[round(x + a * h, 1), round(y - b * h, 1)] for a, b in st])
        x += (WID.get(c, 0.34) + track) * h
    return out


def fit(s, cx, y, h, wd, align="c"):
    return text(s, cx, y, min(h, h * wd / width(s, h)), align)


# ---------------- marks: the sheet of sand, raised blocks on it, and lines cut into them
def sheet(x, y, w, h, r=40): return ["sheet", round(x, 1), round(y, 1), round(w, 1), round(h, 1), r]
def block(x, y, w, h, r=18): return ["block", round(x, 1), round(y, 1), round(w, 1), round(h, 1), r]
def disc(x, y, r): return ["disc", round(x, 1), round(y, 1), round(r, 1)]
def cut(strokes, wd): return ["cut", wd, strokes]
def sand(strokes, wd): return ["sand", wd, strokes]
def bar(x, y, w): return [[round(x, 1), round(y, 1)], [round(x + w, 1), round(y, 1)]]
def poly(pts): return [[round(x, 1), round(y, 1)] for x, y in pts]


def chaikin(pts, n=3):
    for _ in range(n):
        q = [pts[0]]
        for a, b in zip(pts, pts[1:]): q += [(a[0] * 0.75 + b[0] * 0.25, a[1] * 0.75 + b[1] * 0.25), (a[0] * 0.25 + b[0] * 0.75, a[1] * 0.25 + b[1] * 0.75)]
        q.append(pts[-1]); pts = q
    return pts


def thin(pts, step):
    """Keep points about step apart, so a channel is a few dozen segments and not hundreds."""
    out = [pts[0]]; acc = 0
    for a, b in zip(pts, pts[1:]):
        acc += math.hypot(b[0] - a[0], b[1] - a[1])
        if acc >= step: out.append(b); acc = 0
    if out[-1] != pts[-1]: out.append(pts[-1])
    return out


def length(pts): return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


# ---------------- the table: five tools as islands of sand, shapes only, and one place in the middle for the decision layer
SX0, SY0, SX1, SY1 = 70, 290, W - 70, H - 46       # the sheet
C = (960, 664); RB = 64                             # the decision layer: a basin
ISL = {
    "mail": (170, 352, 300, 200), "form": (190, 770, 240, 220),
    "grid": (1450, 330, 330, 216), "card": (1484, 596, 300, 170), "chat": (1430, 834, 270, 150),
}
PERSON = (1790, 878)


def island_marks():
    m = []
    x, y, w, h = ISL["mail"]; m.append(block(x, y, w, h, 16))
    m.append(cut([poly([(x + 24, y + 26), (x + w / 2, y + h * 0.56), (x + w - 24, y + 26)])], 12))
    m.append(cut([poly([(x + 24, y + h - 26), (x + w * 0.38, y + h * 0.52)]), poly([(x + w - 24, y + h - 26), (x + w * 0.62, y + h * 0.52)])], 9))
    x, y, w, h = ISL["form"]; m.append(block(x, y, w, h, 14))
    m.append(cut([bar(x + 30, y + 50, w * 0.42)], 16))
    m.append(cut([poly([(x + 30, y + 92 + i * 42), (x + w - 30, y + 92 + i * 42), (x + w - 30, y + 116 + i * 42), (x + 30, y + 116 + i * 42), (x + 30, y + 92 + i * 42)]) for i in range(3)], 6))
    x, y, w, h = ISL["grid"]; m.append(block(x, y, w, h, 12))
    m.append(cut([bar(x + 22, y + 28 + i * 40, w - 44) for i in range(5)] + [[[x + 22 + j * (w - 44) / 4, y + 28], [x + 22 + j * (w - 44) / 4, y + 188]] for j in range(5)], 7))
    x, y, w, h = ISL["card"]; m.append(block(x, y, w, h, 18))
    m.append(cut([poly([(x + 68 + 34 * math.cos(a * math.pi / 10), y + h / 2 + 34 * math.sin(a * math.pi / 10)) for a in range(21)])], 9))
    m.append(cut([bar(x + 130, y + 62, w * 0.42), bar(x + 130, y + 98, w * 0.3)], 12))
    x, y, w, h = ISL["chat"]; m.append(block(x, y, w, h, 46))
    m.append(block(x + w - 100, y - 26, 60, 54, 10))
    m.append(cut([bar(x + 46, y + 60, w * 0.6), bar(x + 46, y + 96, w * 0.4)], 12))
    px, py = PERSON; m.append(disc(px, py - 70, 30)); m.append(block(px - 52, py - 30, 104, 130, 46))
    return m


landscape = [sheet(SX0, SY0, SX1 - SX0, SY1 - SY0)] + island_marks()

# ---------------- the channels: each one a route the fingertip draws on the map, and later widens into a riverbed
MOUTH = {"mail": (520, 470), "form": (470, 868)}
ROUTE_IN = {
    "mail": [MOUTH["mail"], (640, 486), (770, 556), (860, 620), (C[0] - RB + 6, C[1] - 18)],
    "form": [MOUTH["form"], (600, 852), (750, 790), (860, 720), (C[0] - RB + 8, C[1] + 26)],
}
ROUTE_OUT = {
    "grid": [(C[0] + RB - 8, C[1] - 28), (1090, 590), (1230, 500), (1360, 452), (1440, 440)],
    "card": [(C[0] + RB - 2, C[1] + 6), (1140, 676), (1300, 684), (1420, 684), (1476, 682)],
    "chat": [(C[0] + RB - 10, C[1] + 34), (1110, 760), (1240, 850), (1360, 900), (1424, 908)],
}
FORK_AT = 0.62                                       # the person's channel leaves the chat channel here
PERSON_IN = (PERSON[0] - 58, PERSON[1] + 96)
FURROW = [(440, 352), (520, 318), (640, 336), (760, 312), (880, 340), (1000, 314), (1120, 342), (1240, 316), (1340, 336), (1444, 356)]   # the old way: dug by hand, crooked

R_MAP, R_CH, R_FUR = 4.5, 15.0, 8.0
segs, keys, strokes = [], [], []
L = lambda a, b: math.hypot(a[0] - b[0], a[1] - b[1])
NEVER = 1e4


def chan(pts, t0, t1, r0, r1, w0, w1, e0=NEVER, e1=NEVER, kind="chan"):
    """A cut: drawn from t0 to t1 by length, widened from r0 to r1 between w0 and w1, and smoothed away between e0 and e1."""
    tot = length(pts); acc = 0
    for a, b in zip(pts, pts[1:]):
        d = L(a, b); f0, f1 = acc / tot, (acc + d) / tot; acc += d
        segs.append([round(a[0], 1), round(a[1], 1), round(b[0], 1), round(b[1], 1),
                     round(t0 + (t1 - t0) * f0, 4), round(t0 + (t1 - t0) * f1, 4), r0, r1,
                     round(w0 + (w1 - w0) * f0, 4), round(w0 + (w1 - w0) * f1, 4), round(e0 + (e1 - e0) * f0, 4), round(e0 + (e1 - e0) * f1, 4)])
    strokes.append([kind, t0, t1])


def finger_along(pts, t0, t1, lift=0.22):
    keys.append([round(t0 - lift, 4), pts[0][0] + 26, pts[0][1] - 18, 0.45]); keys.append([round(t0, 4), pts[0][0], pts[0][1], 0.0])
    tot = length(pts); acc = 0
    for a, b in zip(pts, pts[1:]):
        acc += L(a, b); keys.append([round(t0 + (t1 - t0) * acc / tot, 4), b[0], b[1], 0.0])
    keys.append([round(t1 + lift, 4), pts[-1][0] + 30, pts[-1][1] - 22, 0.45])


def smooth(pts): return thin(chaikin(pts, 3), 26)


path_in = {k: smooth(v) for k, v in ROUTE_IN.items()}
path_out = {k: smooth(v) for k, v in ROUTE_OUT.items()}
cp = path_out["chat"]; fi = int(len(cp) * FORK_AT); FORK = cp[fi]
path_person = smooth([FORK, (FORK[0] + 60, FORK[1] + 70), (FORK[0] + 200, 1004), (PERSON_IN[0] - 90, 1004), PERSON_IN])
ring = [(C[0] + RB * math.cos(a * math.pi / 10), C[1] + RB * math.sin(a * math.pi / 10)) for a in range(21)]
path_fur = thin(chaikin(FURROW, 3), 22)

# ---- the beats
clickOn = 1.0
# 1 your tools: the work piles up beside them, and the old crooked furrow carries a trickle by hand
chan(path_fur, -10, -10, R_FUR, R_FUR, -10, -10, 43.0, 44.6, "furrow")
# 2 the map: the fingertip draws every route thin, the basin as a ring, then a tick in the corner
MAP = [("mail", path_in["mail"], 8.6, 9.3), ("form", path_in["form"], 9.5, 10.2), ("ring", ring, 10.4, 11.0),
       ("grid", path_out["grid"], 11.2, 11.7), ("card", path_out["card"], 11.85, 12.3), ("chat", path_out["chat"], 12.45, 12.95), ("person", path_person, 13.05, 13.4)]
OPEN = {"mail": (16.0, 16.7), "form": (16.1, 16.8), "grid": (16.9, 17.5), "card": (17.0, 17.6), "chat": (17.1, 17.7), "person": (17.6, 18.0)}
keys.append([7.6, W + 260, H + 320, 1.0])
for name, pts, t0, t1 in MAP:
    if name == "ring": chan(pts, t0, t1, R_MAP, R_MAP, NEVER, NEVER, kind="ring")
    else: chan(pts, t0, t1, R_MAP, R_CH, OPEN[name][0], OPEN[name][1], kind=name)
    finger_along(pts, t0, t1)
TICK = [(1150, 986), (1174, 1010), (1222, 958)]
chan(TICK, 13.75, 14.0, 4.0, 4.0, NEVER, NEVER, kind="tick"); finger_along(TICK, 13.75, 14.0)
keys.append([15.0, W + 300, H + 360, 1.0])
# 3 the channels open, and the basin with them
segs.append([C[0], C[1], C[0], C[1], -10, -10, 0.0, RB - 6, 16.55, 16.55, NEVER, NEVER])
OPEN_AT = 16.3                                      # the first grains leave the piles
# 5 when it fails: a ridge falls into the card channel, the work backs up, a mark opens beside it, and the fingertip clears it
oc = path_out["card"]; BLOCK_AT = 0.42; bi = int(len(oc) * BLOCK_AT); BLOCK = oc[bi]
FAIL = {"route": "card", "frac": BLOCK_AT, "at": 30.0, "clear": 35.8, "pt": [round(BLOCK[0], 1), round(BLOCK[1], 1)]}
ALERT = (BLOCK[0] + 10, BLOCK[1] - 76)
segs.append([ALERT[0], ALERT[1], ALERT[0], ALERT[1], -10, -10, 0.0, 20.0, 31.5, 31.5, 36.4, 36.4])
aring = [(ALERT[0] + 46 * math.cos(a * math.pi / 8), ALERT[1] + 46 * math.sin(a * math.pi / 8)) for a in range(17)]
chan(aring, 31.6, 31.9, 3.5, 3.5, NEVER, NEVER, 36.2, 36.5, kind="alert")
keys.append([34.4, W + 260, H + 320, 1.0])
CLR = [(BLOCK[0] - 70, BLOCK[1] + 6), (BLOCK[0] + 70, BLOCK[1] - 4)]
finger_along(CLR, 35.5, 35.8, 0.3)
keys.append([36.6, W + 300, H + 360, 1.0])
# 6 the shadow run: the old furrow and the new route side by side, arriving together, then the old one is smoothed away
SHADOW = [40.0, 41.0, 42.0]
keys.append([42.2, W + 260, H + 320, 1.0])
finger_along(path_fur, 43.0, 44.6, 0.3)
keys.append([45.3, W + 300, H + 360, 1.0])
strokes.append(["sweep", 43.0, 44.6])

# ---------------- captions, laid in sand on the bare strip above the table, each one flowing out of the last
CX = W / 2; CAPY = 214; CAPH = 64; CAPW = 1500
CAPS = [
    ("YOUR TOOLS.", None, 1.0),
    ("WORK STUCK BETWEEN THEM.", 4.4, 6.0),
    ("THE MAP COMES FIRST.", 7.2, 8.6),
    ("YOU APPROVE IT.", 12.6, 14.0),
    ("NOTHING REPLACED. JUST CONNECTED.", 16.4, 18.0),
    ("ROUTED. SUMMARISED.", 20.6, 22.0),
    ("TO THE RIGHT PERSON.", 24.8, 26.0),
    ("EVERY RUN LOGGED.", 28.6, 30.0),
    ("FAILURES ALERT.", 30.8, 32.0),
    ("NOTHING DROPS SILENTLY.", 32.8, 34.0),
    ("SHADOW RUN FIRST.", 37.0, 38.0),
    ("THEN CUTOVER.", 42.8, 44.0),
    ("THE CODE. THE KEYS.|THE DOCS. YOURS.", 46.6, 48.0),
]
captions = []
for s, b0, b1 in CAPS:
    lines = s.split("|"); st = []
    for i, l in enumerate(lines):
        y = CAPY if len(lines) == 1 else CAPY - 52 + i * 92
        st += fit(l, CX, y, CAPH if len(lines) == 1 else 58, CAPW)
    captions.append([b0, b1, [sand(st, 11)]])

# ---------------- the streams: where the work comes from and where it goes
streams = {
    "mouth": {k: list(v) for k, v in MOUTH.items()},
    "in": {k: [list(map(lambda q: round(q, 1), p)) for p in v] for k, v in path_in.items()},
    "out": {k: [list(map(lambda q: round(q, 1), p)) for p in v] for k, v in path_out.items()},
    "person": [list(map(lambda q: round(q, 1), p)) for p in path_person],
    "forkAt": fi, "fur": [list(map(lambda q: round(q, 1), p)) for p in path_fur],
    "basin": [C[0], C[1], RB], "rch": R_CH, "rfur": R_FUR,
    "dest": {"grid": [1452, 452], "card": [1486, 682], "chat": [1434, 920], "person": list(PERSON_IN), "furrow": [1452, 372]},
    "isl": {k: list(ISL[k]) for k in ("grid", "card", "chat")} | {"person": [PERSON[0] - 48, PERSON[1] - 26, 96, 120], "furrow": list(ISL["grid"])},
    "open": OPEN_AT, "inboundEnd": 51.0, "personAt": 27.0, "shadow": SHADOW,
    "furTrickle": [[1.4, 3.2], [4.6, 6.6]], "fail": FAIL, "stop": 52.0,
}

clickOff = 54.0; logo = 54.35

table = {
    "w": W, "h": H, "bpm": BPM, "beat": BEAT, "beats": BEATS, "dur": BEATS * BEAT,
    "clickOn": clickOn, "clickOff": clickOff, "logo": logo,
    "landscape": landscape, "captions": captions, "segs": segs, "keys": sorted(keys, key=lambda k: k[0]), "strokes": strokes,
    "streams": streams, "alert": [round(ALERT[0], 1), round(ALERT[1], 1), 31.5, 36.4], "sheet": [SX0, SY0, SX1, SY1],
}
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE=" + json.dumps(table, separators=(",", ":"), ensure_ascii=False) + ";")
print("dur", table["dur"], "segs", len(segs), "keys", len(keys), "captions", len(captions))
