"""The one table for R52 · Same Sand, read by the film and by score/compose.py: the beat grid, the pours, every picture the sand flows into,
and the fingertip at the review. The brand, the brief and every draft are demos. Writes assets/table.js (not committed).  Usage: python bake/table.py"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1920, 1080
PORTRAIT = H > W
BPM = 96; BEAT = 60 / BPM; BEATS = 58

# ---------------- a single-stroke font, drawn by hand. x 0 to .7, y 0 to 1
F = {
    "A": "0,0 .35,1 .7,0|.13,.38 .57,.38", "B": "0,0 0,1 .45,1 .62,.88 .62,.64 .45,.52 0,.52|.45,.52 .68,.4 .68,.13 .48,0 0,0", "C": ".68,.82 .5,1 .2,1 0,.78 0,.22 .2,0 .5,0 .68,.18",
    "D": "0,0 0,1 .4,1 .68,.75 .68,.25 .4,0 0,0", "E": ".68,1 0,1 0,0 .68,0|0,.52 .5,.52", "F": ".68,1 0,1 0,0|0,.52 .5,.52", "G": ".68,.82 .5,1 .2,1 0,.78 0,.22 .2,0 .5,0 .68,.2 .68,.46 .38,.46",
    "H": "0,0 0,1|.68,0 .68,1|0,.52 .68,.52", "I": ".14,1 .14,0", "J": ".6,1 .6,.2 .42,0 .18,0 0,.2", "K": "0,0 0,1|.68,1 0,.42|.22,.58 .7,0", "L": "0,1 0,0 .62,0",
    "M": "0,0 0,1 .38,.35 .76,1 .76,0", "N": "0,0 0,1 .68,0 .68,1", "O": ".2,0 0,.22 0,.78 .2,1 .5,1 .7,.78 .7,.22 .5,0 .2,0", "P": "0,0 0,1 .46,1 .66,.84 .66,.6 .46,.44 0,.44",
    "R": "0,0 0,1 .46,1 .66,.84 .66,.6 .46,.44 0,.44|.36,.44 .7,0", "S": ".66,.84 .48,1 .2,1 .02,.84 .02,.64 .2,.52 .5,.48 .68,.34 .68,.16 .5,0 .2,0 0,.16",
    "T": "0,1 .7,1|.35,1 .35,0", "U": "0,1 0,.22 .2,0 .5,0 .7,.22 .7,1", "V": "0,1 .35,0 .7,1", "W": "0,1 .2,0 .4,.7 .6,0 .8,1", "Y": "0,1 .35,.48 .7,1|.35,.48 .35,0",
    "X": "0,1 .68,0|0,0 .68,1", "Z": "0,1 .68,1 0,0 .68,0", "Ê": ".68,1 0,1 0,0 .68,0|0,.52 .5,.52|.12,1.14 .34,1.34 .56,1.14",
    "'": ".1,1 .06,.76", "-": ".04,.44 .44,.44", ".": ".06,.05 .06,0", ",": ".08,.08 .02,-.14", "?": ".02,.8 .2,1 .46,1 .64,.82 .64,.62 .32,.4 .32,.24|.32,.04 .32,0",
}
GL = {c: [[tuple(float(v) for v in p.split(",")) for p in st.split()] for st in s.split("|")] for c, s in F.items()}
WID = {c: max(q[0] for st in g for q in st) for c, g in GL.items()}


def width(s, h, track=0.28):
    return sum((WID.get(c, 0.34) + track) * h for c in s) - track * h


def text(s, cx, y, h, align="c", track=0.28):
    """Strokes for a line of text. y is the baseline, in pixels from the top."""
    wd = width(s, h, track); x = cx - (wd / 2 if align == "c" else 0); out = []
    for c in s:
        for st in GL.get(c, []): out.append([[round(x + a * h, 1), round(y - b * h, 1)] for a, b in st])
        x += (WID.get(c, 0.34) + track) * h
    return out


def fit(s, cx, y, h, wd, align="c"):
    return text(s, cx, y, min(h, h * wd / width(s, h)), align)


# ---------------- a picture is a list of marks: blocks of sand, lines cut into them, and lines of sand laid on the bare table
def block(x, y, w, h, r=18): return ["block", round(x, 1), round(y, 1), round(w, 1), round(h, 1), r]
def cut(strokes, wd): return ["cut", wd, strokes]
def sand(strokes, wd): return ["sand", wd, strokes]
def bar(x, y, w, wd): return [[round(x, 1), round(y, 1)], [round(x + w, 1), round(y, 1)]]


pics, morphs, pours, taps, keys = [], [], [], [], []


def pic(marks):
    pics.append(marks); return len(pics) - 1


def flow(p, b0, b1, travel=1.0):
    """The sand flows by itself from whatever it is into picture p, landing exactly on b1."""
    morphs.append([b0, b1, p, travel])


CX, CY = W / 2, H * 0.56
P = PORTRAIT
CAPY = 196 if not P else 430      # captions, laid as lines of sand on the bare table
CH = 70; CW = W - (260 if not P else 140); CAPW = 11


def caption(s, y=CAPY, h=CH):
    """A caption. A | is where it breaks onto a second line in the 9:16 cut; in 16:9 it's a space."""
    if not P: return sand(fit(s.replace("|", " "), CX, y, h, CW), CAPW)
    st = []
    for i, l in enumerate(s.split("|")): st += fit(l, CX, y + i * h * 1.45, h, CW)
    return sand(st, CAPW)


# ---- 1 light on, and one pile poured in
clickOn = 1.0
pours.append([1.2, 4.6, CX, CY, 0])          # a thin stream of dark sand builds one pile

# ---- 2 one brief: a card, with the demo brief cut into it
def brief(x, y, w, h):
    m = [block(x, y, w, h)]
    m.append(cut(fit("BRIEF", x + 56, y + 118, 74, w * 0.5, "l"), 13))
    m.append(cut([bar(x + 58, y + 190 + i * 58, (w - 116) * (1.0, 0.84, 0.92, 0.6)[i], 0) for i in range(4)], 15))
    return m


BW, BH = (780, 470) if not P else (820, 480)
p_brief = pic(brief(CX - BW / 2, CY - BH / 2, BW, BH) + [caption("ONE BRIEF.")])
flow(p_brief, 4.8, 7.0, 0.6)

# ---- 3 the voice: a stream of the tinted sand poured on, and pulled through the card as it changes
pours.append([7.4, 8.8, CX - BW * 0.18, CY - 20, 1])
p_voice = pic(brief(CX - BW / 2 - 30, CY - BH / 2 + 10, BW + 60, BH - 20) + [caption("IN YOUR VOICE.")])
flow(p_voice, 8.4, 11.0, 0.8)

# ---- 4 the stock phrase, struck through, and gone
if not P:
    SPL = [("IN TODAY'S FAST-PACED WORLD...", H * 0.47)]; SPH = 92; SPW = W - 300; SB = block(CX - 520, H * 0.70, 1040, 250)
else:
    SPL = [("IN TODAY'S", H * 0.40), ("FAST-PACED WORLD...", H * 0.40 + 150)]; SPH = 96; SPW = W - 120; SB = block(CX - 420, H * 0.62, 840, 330)
phrase = []; strike = []
for s, y in SPL:
    phrase += fit(s, CX, y, SPH, SPW); sw = min(SPW, width(s, SPH))
    strike.append([[round(CX - sw / 2 - 30, 1), round(y - 40, 1)], [round(CX + sw / 2 + 30, 1), round(y - 30, 1)]])
p_stock = pic([SB, sand(phrase, 13)])
flow(p_stock, 11.2, 13.0, 0.8)
p_struck = pic([SB, sand(phrase, 13), sand(strike, 16)])
flow(p_struck, 13.0, 14.0, 0.4)
p_out = pic(brief(CX - BW / 2, CY - BH / 2 + 30, BW, BH - 40) + [caption("ANTI-PATTERNS OUT.")])
flow(p_out, 14.0, 16.0, 1.0)

# ---- 5 the formats: each one a different shape, and each one the same sand
def post(x, y, s):
    m = [block(x, y, s, s)]
    m.append(cut([[[x + 60, y + 60], [x + s - 60, y + 60], [x + s - 60, y + s * 0.62], [x + 60, y + s * 0.62], [x + 60, y + 60]]], 12))
    cx, cy, r = x + s * 0.5, y + s * 0.36, s * 0.12
    m.append(cut([[[round(cx + r * math.cos(a * math.pi / 12), 1), round(cy + r * math.sin(a * math.pi / 12), 1)] for a in range(25)]], 12))
    m.append(cut([bar(x + 60, y + s * 0.74, s * 0.66, 0), bar(x + 60, y + s * 0.85, s * 0.44, 0)], 15))
    return m


def email(x, y, w, h):
    m = [block(x, y, w, h)]; gap = 52 if not P else (h - 300) / 10
    m.append(cut([bar(x + 50, y + 70, w * 0.42, 0)], 22))
    m.append(cut([[[x + 30, y + 120], [x + w - 30, y + 120]]], 8))
    m.append(cut([bar(x + 50, y + 180 + i * gap, (w - 100) * (0.95, 0.88, 0.97, 0.7, 0.0, 0.92, 0.86, 0.5, 0.0, 0.4)[i], 0) for i in range(10) if i not in (4, 8)], 13))
    m.append(cut([[[x + 50, y + h - 90], [x + 50 + w * 0.36, y + h - 90]]], 34))
    return m


def strip(x, y, w, h, lines):
    st = []
    for i, s in enumerate(lines): st += fit(s, x + 60, (y + h * 0.66) if len(lines) == 1 else (y + 130 + i * 110), 64, w - 120, "l")
    return [block(x, y, w, h), cut(st, 12)]


def carousel(cx, cy, n, s, gap):
    tot = n * s + (n - 1) * gap; m = []; dg = s * 0.1
    for i in range(n):
        x = cx - tot / 2 + i * (s + gap); y = cy - s / 2
        m.append(block(x, y, s, s, 18 if s > 200 else 12))
        m.append(cut([[[x + s * 0.2, y + s * 0.2], [x + s * 0.8, y + s * 0.2], [x + s * 0.8, y + s * 0.6], [x + s * 0.2, y + s * 0.6], [x + s * 0.2, y + s * 0.2]]], 10 if s > 200 else 8))
        m.append(cut([[[x + s * 0.2 + j * dg, y + s * 0.8], [x + s * 0.2 + j * dg + 1, y + s * 0.8]] for j in range(n)], 9 if s > 200 else 6))   # the page dots
        m.append(cut([[[x + s * 0.2 + i * dg, y + s * 0.8], [x + s * 0.2 + i * dg + 1, y + s * 0.8]]], 22 if s > 200 else 14))              # this page
    return m


PS = 600 if not P else 760
p_post = pic(post(CX - PS / 2, CY - PS / 2 + 40, PS) + [caption("ONE BRIEF.|EVERY FORMAT.")])
flow(p_post, 16.0, 18.0, 1.0)
EW, EH = (600, 760) if not P else (720, 980)
p_email = pic(email(CX - EW / 2, CY - EH / 2 + (70 if not P else 110), EW, EH) + [caption("ONE BRIEF.|EVERY FORMAT.")])
flow(p_email, 20.0, 22.0, 1.0)
if not P: p_cap = pic(strip(CX - 800, CY - 100, 1600, 260, ["SPRING MENU, BAKED THIS MORNING."]) + [caption("NOT COPY-PASTED.")])
else: p_cap = pic(strip(CX - 450, CY - 170, 900, 330, ["SPRING MENU,", "BAKED THIS MORNING."]) + [caption("NOT COPY-PASTED.")])
flow(p_cap, 24.0, 26.0, 1.0)
p_car = pic((carousel(CX, CY + 40, 5, 300, 34) if not P else carousel(CX, CY + 40, 5, 178, 16)) + [caption("NOT COPY-PASTED.")])
flow(p_car, 28.0, 30.0, 1.0)

# ---- 6 one line, four languages: the letters change, the sand stays
LANG = ["SAME VOICE.", "MESMA VOZ.", "MÊME VOIX.", "MISMA VOZ."]
LB = [32.0, 33.5, 35.0, 36.5]
for i, (s, b) in enumerate(zip(LANG, LB)):
    if not P: p = pic([block(CX - 820, CY - 170, 1640, 340), cut(fit(s, CX, CY + 82, 190, 1400), 24)])
    else:
        a, c = s.split(" ")
        p = pic([block(CX - 470, CY - 330, 940, 620), cut(fit(a, CX, CY - 60, 190, 800) + fit(c, CX, CY + 200, 190, 800), 24)])
    flow(p, b - (1.4 if i == 0 else 1.0), b, 0.7)

# ---- 7 the review: three drafts, two kept, one struck and flowed out again rewritten. The finger's only scene
if not P:
    DW, DH, DG = 440, 360, 70
    DP = [(CX - DW * 1.5 - DG + i * (DW + DG), CY - DH / 2 + 50) for i in range(3)]
else:
    DW, DH, DG = 760, 330, 46
    DP = [(CX - DW / 2, CY - DH * 1.5 - DG + 90 + i * (DH + DG)) for i in range(3)]


def draft(x, y, k):
    m = [block(x, y, DW, DH)]
    rows = [(0.8, 0.62, 0.9, 0.5), (0.7, 0.9, 0.56, 0.84), (0.92, 0.5, 0.8, 0.66), (0.6, 0.86, 0.74, 0.9)][k]
    m.append(cut([bar(x + 50, y + 70, DW * 0.36, 0)], 20))
    m.append(cut([bar(x + 50, y + 140 + j * (52 if not P else (DH - 180) / 3.6), (DW - 100) * rows[j] * (0.78 if P else 1.0), 0) for j in range(4)], 13))
    return m


def tick(x, y): return cut([[[x + DW - 110, y + DH - 70], [x + DW - 86, y + DH - 46], [x + DW - 46, y + DH - 96]]], 11)


p_rev = pic(draft(*DP[0], 0) + draft(*DP[1], 1) + draft(*DP[2], 2) + [caption("DRAFTS FOR|YOUR REVIEW.")])
flow(p_rev, 37.2, 39.0, 1.0)
# the fingertip: in, a tick on the first, a tick on the second, a line through the third, out. Its marks are the only strokes in the film
segs = []
tk = lambda x, y: [[x + DW - 110, y + DH - 70], [x + DW - 86, y + DH - 46], [x + DW - 46, y + DH - 96]]
T1 = 40.0; T2 = 41.0; T3 = 42.0
L = lambda a, b: math.hypot(a[0] - b[0], a[1] - b[1])


def mark(pts, b0, b1, r, kind):
    """A stroke by the fingertip, laid along b0 to b1 by length, with the finger's keys on it."""
    tot = sum(L(pts[i], pts[i + 1]) for i in range(len(pts) - 1)); t = b0
    keys.append([round(b0 - 0.25, 4), pts[0][0] + 20, pts[0][1] - 14, 0.45]); keys.append([round(b0, 4), pts[0][0], pts[0][1], 0])
    for i in range(len(pts) - 1):
        dt = (b1 - b0) * L(pts[i], pts[i + 1]) / tot
        segs.append([round(t, 4), round(t + dt, 4), round(pts[i][0], 1), round(pts[i][1], 1), round(pts[i + 1][0], 1), round(pts[i + 1][1], 1), r, 0]); t += dt
        keys.append([round(t, 4), pts[i + 1][0], pts[i + 1][1], 0])
    keys.append([round(b1 + 0.25, 4), pts[-1][0] + 24, pts[-1][1] - 18, 0.45])
    taps.append([b0, b1, kind])


keys.append([39.0, W + 260, H + 320, 1.0])
mark(tk(*DP[0]), T1, T1 + 0.4, 10, 0)
mark(tk(*DP[1]), T2, T2 + 0.4, 10, 0)
x3, y3 = DP[2]
mark([[x3 + 30, y3 + 50], [x3 + DW - 30, y3 + DH - 50]], T3, T3 + 0.45, 12, 1)
p_rew = pic(draft(*DP[0], 0) + [tick(*DP[0])] + draft(*DP[1], 1) + [tick(*DP[1])] + draft(*DP[2], 3) + [caption("DRAFTS FOR|YOUR REVIEW.")])
flow(p_rew, 43.0, 44.6, 0.8)
outF = 43.6
keys.append([outF, W + 300, H + 360, 1.0])

# ---- 8 a month at a time: a calendar fills row by row, out of one pile
CN, CR = 7, 4
if not P:
    TW, TH, TG = 150, 104, 18
    gx = CX - (CN * TW + (CN - 1) * TG) / 2 - 150; gy = CY - (CR * TH + (CR - 1) * TG) / 2 + 40
else:
    TW, TH, TG = 112, 96, 14
    gx = CX - (CN * TW + (CN - 1) * TG) / 2; gy = H * 0.36
for k in range(CR + 1):
    m = []
    for j in range(k):
        for i in range(CN): m.append(block(gx + i * (TW + TG), gy + j * (TH + TG), TW, TH, 10))
    left = (CR - k) / CR
    if left > 0:
        side = math.sqrt(left) * 520
        if not P: m.append(block(gx + CN * (TW + TG) + 60, CY + 40 - side * 0.55, side * 0.62, side * 1.1, 60))
        else: m.append(block(CX - side * 0.55, H * 0.70, side * 1.1, side * 0.62, 60))
    m.append(caption("A MONTH|AT A TIME."))
    p = pic(m)
    if k == 0: flow(p, 44.6, 46.0, 0.8)
    else: flow(p, 46.0 + (k - 1) * 1.0, 46.0 + k * 1.0, 0.6)

# ---- 9 yours: a document, and the words in sand beside it
if not P: DX0, DY0, DW0, DH0 = W * 0.60, H * 0.20, 470, 650
else: DX0, DY0, DW0, DH0 = CX - 230, H * 0.17, 460, 620
doc = [block(DX0, DY0, DW0, DH0, 14), cut([bar(DX0 + 56, DY0 + 90, DW0 * 0.4, 0)], 22),
       cut([bar(DX0 + 56, DY0 + 170 + i * 56, (DW0 - 112) * (0.9, 0.7, 0.96, 0.6, 0.86, 0.74, 0.5, 0.0)[i], 0) for i in range(7)], 13),
       cut([[[DX0 + DW0 - 120, DY0], [DX0 + DW0 - 120, DY0 + 120], [DX0 + DW0, DY0 + 120]]], 10)]
WORDS = ["THE VOICE.", "THE PROMPTS.", "THE CODE.", "YOURS."]
wh = min(84, ((W * 0.44) if not P else (W - 200)) / width("THE PROMPTS.", 1.0))
words = []
for i, s in enumerate(WORDS):
    x0, y0, dy = (W * 0.10, H * 0.32, 150) if not P else (100, H * 0.62, 140)
    words.append(sand(text(s, x0, y0 + i * dy, wh * (1.25 if i == 3 else 1.0), "l"), 12 if i < 3 else 16))
p_yours = pic(doc + words)
flow(p_yours, 50.0, 52.0, 1.0)

clickOff = 54.0; logo = 54.35   # then a little over two seconds of the end card

table = {
    "w": W, "h": H, "bpm": BPM, "beat": BEAT, "beats": BEATS, "dur": BEATS * BEAT,
    "clickOn": clickOn, "clickOff": clickOff, "logo": logo, "outF": outF,
    "pics": pics, "morphs": morphs, "pours": pours, "taps": taps, "segs": sorted(segs), "keys": sorted(keys, key=lambda k: k[0]),
    "review": [37.2, 44.6], "rewAt": 43.0, "langs": LB,
}
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE=" + json.dumps(table, separators=(",", ":"), ensure_ascii=False) + ";")
print("dur", table["dur"], "pics", len(pics), "morphs", len(morphs))
