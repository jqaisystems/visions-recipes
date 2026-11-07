"""The one table for R51 · Hands Off, read by the film and by score/compose.py: the beat grid, and every stroke that moves the sand, with or without a finger.
The workflow and the script in the film are demos. Writes assets/table.js (not committed).  Usage: python bake/table.py"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1920, 1080
PORTRAIT = H > W
BPM = 100; BEAT = 60 / BPM; BEATS = 56

# ---------------- a single-stroke font, drawn by hand. x 0 to .7, y 0 to 1
F = {
    "A": "0,0 .35,1 .7,0|.13,.38 .57,.38", "B": "0,0 0,1 .45,1 .62,.88 .62,.64 .45,.52 0,.52|.45,.52 .68,.4 .68,.13 .48,0 0,0", "C": ".68,.82 .5,1 .2,1 0,.78 0,.22 .2,0 .5,0 .68,.18",
    "D": "0,0 0,1 .4,1 .68,.75 .68,.25 .4,0 0,0", "E": ".68,1 0,1 0,0 .68,0|0,.52 .5,.52", "F": ".68,1 0,1 0,0|0,.52 .5,.52", "G": ".68,.82 .5,1 .2,1 0,.78 0,.22 .2,0 .5,0 .68,.2 .68,.46 .38,.46",
    "H": "0,0 0,1|.68,0 .68,1|0,.52 .68,.52", "I": ".14,1 .14,0", "J": ".6,1 .6,.2 .42,0 .18,0 0,.2", "K": "0,0 0,1|.68,1 0,.42|.22,.58 .7,0", "L": "0,1 0,0 .62,0",
    "M": "0,0 0,1 .38,.35 .76,1 .76,0", "N": "0,0 0,1 .68,0 .68,1", "O": ".2,0 0,.22 0,.78 .2,1 .5,1 .7,.78 .7,.22 .5,0 .2,0", "P": "0,0 0,1 .46,1 .66,.84 .66,.6 .46,.44 0,.44",
    "R": "0,0 0,1 .46,1 .66,.84 .66,.6 .46,.44 0,.44|.36,.44 .7,0", "S": ".66,.84 .48,1 .2,1 .02,.84 .02,.64 .2,.52 .5,.48 .68,.34 .68,.16 .5,0 .2,0 0,.16",
    "T": "0,1 .7,1|.35,1 .35,0", "U": "0,1 0,.22 .2,0 .5,0 .7,.22 .7,1", "V": "0,1 .35,0 .7,1", "W": "0,1 .2,0 .4,.7 .6,0 .8,1", "Y": "0,1 .35,.48 .7,1|.35,.48 .35,0",
    "a": ".58,.62 .58,0|.58,.46 .42,.62 .18,.62 0,.44 0,.18 .18,0 .42,0 .58,.16", "b": "0,1 0,0|0,.46 .16,.62 .42,.62 .58,.46 .58,.16 .42,0 .16,0 0,.16", "d": ".58,1 .58,0|.58,.46 .42,.62 .16,.62 0,.46 0,.16 .16,0 .42,0 .58,.16",
    "e": "0,.32 .58,.32 .58,.44 .42,.62 .16,.62 0,.46 0,.16 .16,0 .44,0 .56,.1", "f": ".44,1 .26,1 .16,.88 .16,0|0,.62 .38,.62", "g": ".58,.62 .58,-.14 .42,-.3 .14,-.3|.58,.46 .42,.62 .16,.62 0,.46 0,.16 .16,0 .42,0 .58,.16",
    "i": ".1,.62 .1,0|.1,.94 .1,.86", "l": ".1,1 .1,0", "n": "0,0 0,.62|0,.44 .16,.62 .42,.62 .56,.46 .56,0", "o": ".16,0 0,.16 0,.46 .16,.62 .42,.62 .58,.46 .58,.16 .42,0 .16,0",
    "r": "0,0 0,.62|0,.42 .16,.6 .4,.62", "s": ".52,.52 .38,.62 .14,.62 .02,.5 .02,.4 .14,.32 .42,.28 .56,.18 .56,.1 .42,0 .14,0 0,.1", "t": ".16,.92 .16,.14 .28,0 .44,0|0,.62 .38,.62",
    "u": "0,.62 0,.16 .16,0 .42,0 .58,.16|.58,.62 .58,0", "w": "0,.62 .16,0 .32,.46 .48,0 .64,.62", "x": "0,.62 .54,0|0,0 .54,.62",
    "(": ".26,1.08 .08,.8 .04,.4 .08,.02 .26,-.26", ")": ".04,1.08 .22,.8 .26,.4 .22,.02 .04,-.26", "=": ".04,.46 .52,.46|.04,.24 .52,.24", ":": ".1,.56 .1,.5|.1,.1 .1,.04",
    ".": ".06,.05 .06,0", "?": ".02,.8 .2,1 .46,1 .64,.82 .64,.62 .32,.4 .32,.24|.32,.04 .32,0", ",": ".08,.08 .02,-.14",
}
GL = {c: [[tuple(float(v) for v in p.split(",")) for p in st.split()] for st in s.split("|")] for c, s in F.items()}
WID = {c: max(q[0] for st in g for q in st) for c, g in GL.items()}


def width(s, h, track=0.26):
    return sum((WID.get(c, 0.34) + track) * h for c in s) - track * h


def text(s, cx, y, h, align="c", track=0.26):
    """Strokes for a line of text. y is the baseline, in pixels from the top."""
    wd = width(s, h, track); x = cx - (wd / 2 if align == "c" else 0); out = []
    for c in s:
        for st in GL.get(c, []): out.append([(x + a * h, y - b * h) for a, b in st])
        x += (WID.get(c, 0.34) + track) * h
    return out


def fit(s, cx, y, h, wd):
    return text(s, cx, y, min(h, h * wd / width(s, h)))


def rect(x, y, w, h):
    return [[(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]]


def arc(cx, cy, r, a0, a1, n=20):
    return [[(cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]]


segs, keys, hiss = [], [], []


def L(a, b): return math.hypot(a[0] - b[0], a[1] - b[1])


def draw(strokes, b0, b1, r, kind=0, finger=True, loud=1.0):
    """Lays strokes along the time from b0 to b1, by length, with a little time for the hops. Every mark in the film comes through here."""
    lens = [sum(L(s[i], s[i + 1]) for i in range(len(s) - 1)) for s in strokes]
    hops = [L(strokes[i][-1], strokes[i + 1][0]) * 0.3 for i in range(len(strokes) - 1)] + [0]
    total = max(1.0, sum(lens) + sum(hops)); t = b0; k = (b1 - b0) / total
    for s, ln, hop in zip(strokes, lens, hops):
        if finger: keys.append([t, s[0][0], s[0][1], 0])
        for i in range(len(s) - 1):
            dt = L(s[i], s[i + 1]) * k
            if dt > 0: segs.append([round(t, 4), round(t + dt, 4), round(s[i][0], 1), round(s[i][1], 1), round(s[i + 1][0], 1), round(s[i + 1][1], 1), r, kind])
            t += dt
            if finger: keys.append([round(t, 4), s[i + 1][0], s[i + 1][1], 0])
        t += hop * k
    hiss.append([b0, b1, round(loud * min(1.0, 0.45 + total / (b1 - b0) / 5200), 3), kind])


def wipe(cx, cy, w, h, b0, b1, r=None, finger=True, loud=1.0):
    """Sand swept back over an area, in a zigzag."""
    r = r or max(16, h * 0.3); rows = max(2, int(h / (r * 1.3)) + 1); x0, x1 = cx - w / 2 - r * 0.2, cx + w / 2 + r * 0.2; p = []
    for i in range(rows):
        y = cy - h / 2 + r * 0.5 + (h - r) * i / max(1, rows - 1)
        p += [(x0, y), (x1, y)] if i % 2 == 0 else [(x1, y), (x0, y)]
    draw([p], b0, b1, round(r, 1), 1, finger, loud)


def task(cx, cy, s):
    """The same task, every time: read a sheet, copy it across to another sheet."""
    w, h, gap = 300 * s, 400 * s, 250 * s
    if PORTRAIT: w, h, gap = 250 * s, 330 * s, 180 * s
    ax, bx, y = cx - gap / 2 - w, cx + gap / 2, cy - h / 2; out = []
    out += rect(ax, y, w, h)
    for i in range(3): out.append([(ax + w * 0.16, y + h * (0.26 + i * 0.22)), (ax + w * (0.84 - 0.16 * (i == 2)), y + h * (0.26 + i * 0.22))])
    m0, m1 = (ax + w + gap * 0.16, cy), (bx - gap * 0.16, cy)
    out.append([m0, (cx, cy - h * 0.06), m1]); out.append([(m1[0] - gap * 0.2, m1[1] - gap * 0.18), m1, (m1[0] - gap * 0.24, m1[1] + gap * 0.14)])
    out += rect(bx, y, w, h)
    for i in range(3): out.append([(bx + w * 0.16, y + h * (0.26 + i * 0.22)), (bx + w * (0.84 - 0.16 * (i == 2)), y + h * (0.26 + i * 0.22))])
    return out


CX, CY = W / 2, H * 0.57
TW = (720 if PORTRAIT else 1000); TH = (480 if PORTRAIT else 520)    # the area the big task sits in
TS = 1.0 if not PORTRAIT else 0.98
CAPY = 190 if not PORTRAIT else 410                                   # where the captions sit
CW = W - 200
CH = 76 if not PORTRAIT else 72

# ---- light on
clickOn = 1.0; pour0, pour1 = 1.15, 5.0

# ---- the same task, by hand
keys.append([4.6, W + 120, H + 140, 1])
draw(fit("THE SAME TASK.", CX, CAPY, CH, CW), 5.0, 6.4, 8.5)
draw(task(CX, CY, TS), 6.6, 10.4, 8.5)
wipe(CX, CY, TW, TH, 10.5, 11.1, 92, loud=1.2)
draw(fit("AGAIN.", CX, CAPY + 100, CH * 0.8, CW), 11.2, 11.8, 8)
draw(task(CX, CY + 40, TS * 0.9), 11.8, 13.4, 8)
wipe(CX, CY + 40, TW, TH, 13.45, 13.9, 92, loud=1.2)
wipe(CX, CAPY + 72, 620, 84, 13.85, 13.98, 40)
draw(fit("AND AGAIN.", CX, CAPY + 100, CH * 0.8, CW), 14.0, 14.45, 8)   # scrawled over the last one, faster each time
draw(task(CX, CY + 40, TS * 0.9), 14.45, 15.3, 8)
wipe(CX, H / 2, W + 200, H + 200, 15.4, 16.1, 190, loud=1.5)

# ---- plain English
if PORTRAIT:
    draw(fit("IF YOU CAN", CX, H * 0.46, 112, CW), 16.3, 17.3, 11); draw(fit("DESCRIBE IT...", CX, H * 0.46 + 170, 112, CW), 17.3, 18.7, 11)
else:
    draw(fit("IF YOU CAN", CX, H * 0.44, 130, CW), 16.3, 17.3, 12); draw(fit("DESCRIBE IT...", CX, H * 0.44 + 200, 130, CW), 17.3, 18.7, 12)
wipe(CX, H / 2, W + 200, H + 200, 18.9, 19.5, 190, loud=1.5)

# ---- the map: boxes, handoffs pressed in deep
if PORTRAIT:
    BX = [(W * 0.22, H * 0.36), (W * 0.74, H * 0.47), (W * 0.26, H * 0.60), (W * 0.74, H * 0.72)]; BW, BH = 300, 170
else:
    BX = [(W * 0.15, H * 0.42), (W * 0.40, H * 0.72), (W * 0.62, H * 0.42), (W * 0.85, H * 0.72)]; BW, BH = 300, 180
m = []
for x, y in BX: m += rect(x - BW / 2, y - BH / 2, BW, BH)
draw(m, 19.6, 21.1, 9)
hand = []
for (a, c) in zip(BX, BX[1:]):
    p0 = (a[0] + (BW / 2 if c[0] > a[0] else -BW / 2), a[1]); p1 = (c[0], c[1] - BH / 2) if c[1] > a[1] else (c[0], c[1] + BH / 2)
    if c[1] < a[1]: p0 = (a[0] + BW / 2, a[1])
    hand.append([p0, (p1[0], p0[1]), p1])
draw(hand, 21.1, 22.0, 7)
for i, s in enumerate(hand):
    b = 22.0 + i * 0.16; x, y = s[-1]
    draw([[(x, y), (x + 1, y)]], b, b + 0.12, 23, 0)
draw(fit("MAPPED BEFORE ANY CODE.", CX, CAPY, CH * 0.92, CW), 22.5, 23.9, 8)
wipe(CX, H / 2, W + 200, H + 200, 24.0, 24.5, 190, loud=1.5)

# ---- the code, by hand, faster than a hand should go. A demo: no real system
CODE = ["for row in inbox:", "    note = read(row)", "    send(draft(note))", "log(run)"]
if PORTRAIT:
    draw(fit("CUSTOM PYTHON.", CX, 360, CH, CW), 24.6, 25.3, 8); draw(fit("NOT A TEMPLATE.", CX, 480, CH, CW), 25.3, 26.0, 8)
    cx0, cy0, ch, dy = 120, 720, 54, 130
else:
    draw(fit("CUSTOM PYTHON. NOT A TEMPLATE.", CX, CAPY, CH * 0.8, CW), 24.6, 26.0, 8)
    cx0, cy0, ch, dy = 500, 440, 72, 128
st = []
for i, l in enumerate(CODE):
    st += text(l.strip(), cx0 + (len(l) - len(l.strip())) * ch * 0.62, cy0 + i * dy, ch, "l")
draw(st, 26.1, 29.3, 6.5)

# ---- hands off. One last dot, and the finger leaves
dot = (cx0 + width("log(run)", ch) + 60, cy0 + 3 * dy)
draw([[dot, (dot[0] + 1, dot[1])]], 29.5, 29.75, 22)
keys.append([30.5, dot[0] + 1, dot[1], 0])
keys.append([30.9, dot[0] + 40, dot[1] - 10, 0.5])
keys.append([31.6, W + 500, H + 620, 1.0])
lift = 30.5; offF = 31.6; alone = 33.0

# ---- alone: the sweep nobody made, and the same task running by itself
wipe(CX, H / 2, W + 200, H + 200, alone, alone + 0.6, 190, False, 1.5)
draw(task(CX, CY - 40, TS), alone + 0.6, alone + 1.6, 8.5, 0, False)
wipe(CX, CY - 40, TW, TH, alone + 1.6, alone + 1.85, 92, False)
draw(task(CX, CY - 40, TS), alone + 1.85, alone + 2.6, 8.5, 0, False)
wipe(CX, CY - 40, TW, TH, alone + 2.6, alone + 2.8, 92, False)
draw(task(CX, CY - 40, TS), alone + 2.8, alone + 3.3, 8.5, 0, False)
wipe(CX, H / 2, W + 200, H + 200, alone + 3.3, alone + 3.7, 190, False, 1.5)

# ---- a wall of them, each on its own loop, and it keeps running under the night
night0, night1 = 41.5, 46.0
wall0 = alone + 3.8
wallEnd = 46.4
nx, ny = (4, 7) if PORTRAIT else (8, 4)
top = (300 if not PORTRAIT else 560); bot = H - (40 if not PORTRAIT else 170)
TLW, TLH = (W - 80) / nx, (bot - top) / ny
ts = TLW / (1010 if not PORTRAIT else 860)
land = 43.0     # the moment the whole wall is complete, all at once, on a downbeat
for iy in range(ny):
    for ix in range(nx):
        cx, cy = 40 + TLW * (ix + 0.5), top + TLH * (iy + 0.5); off = (ix + iy) * 0.11
        T = wall0
        while T < land - 0.01:
            f = min(1.0, (T - wall0) / (land - wall0 - 1.0)); loop = 1.0 - 0.5 * f   # each one speeds up to twice a beat
            loop = min(loop, land - T) if land - T - loop < 0.3 else loop
            b = T + off * max(0.0, 1.0 - f * 1.25); e = T + loop
            last = e >= land - 0.01
            draw(task(cx, cy, ts), b, (land if last else b + (e - b) * 0.76), max(3.2, 8.5 * ts), 0, False, 0.0)
            if not last: wipe(cx, cy, TLW * 0.94, TLH * 0.9, b + (e - b) * 0.78, e - 0.005, TLH * 0.3, False, 0.0)
            T = e
for iy in range(ny):
    for ix in range(nx):
        cx, cy = 40 + TLW * (ix + 0.5), top + TLH * (iy + 0.5)
        b = land + 1.0 + ix * 0.1 + iy * 0.06
        while b < 46.2:
            wipe(cx, cy, TLW * 0.94, TLH * 0.9, b, b + 0.14, TLH * 0.3, False, 0.0)
            draw(task(cx, cy, ts), b + 0.15, b + 0.62, max(3.2, 8.5 * ts), 0, False, 0.0)
            b += 1.5
hiss.append([wall0, wallEnd, 0.5, 9])

# ---- a sun goes down, a moon comes up, and nothing stops
def sky(b0, b1, bits, moon=False):
    """A disc that really moves: the sand closes behind it and opens in front, every step. The moon has its bite."""
    n = 110; rad = 50
    pos = lambda u: (-90 + (W + 180) * u, (150 if not PORTRAIT else 320) - math.sin(u * math.pi) * (82 if not PORTRAIT else 150))
    for i in range(n + 1):
        t0 = b0 + (b1 - b0) * i / n; dt = (b1 - b0) / n; p = pos(i / n)
        if i: q = pos((i - 1) / n); segs.append([round(t0, 5), round(t0 + dt * 0.2, 5), round(q[0], 1), round(q[1], 1), round(q[0], 1), round(q[1], 1), rad + 9, 1])
        segs.append([round(t0 + dt * 0.3, 5), round(t0 + dt * 0.5, 5), round(p[0], 1), round(p[1], 1), round(p[0], 1), round(p[1], 1), rad, 0])
        if moon: segs.append([round(t0 + dt * 0.6, 5), round(t0 + dt * 0.8, 5), round(p[0] + 26, 1), round(p[1] - 12, 1), round(p[0] + 26, 1), round(p[1] - 12, 1), rad - 5, 2])


skyY = (118 if not PORTRAIT else 300)
wipe(CX, top * 0.5, W + 200, top + 60, alone + 3.7, wall0 + 0.4, 90, False, 0.0)
sky(wall0 + 0.5, 44.2, 0)
if PORTRAIT:
    draw(fit("ON YOUR", CX, 470, CH, CW), night0, night0 + 0.9, 8, 0, False); draw(fit("SCHEDULE.", CX, 470 + 0, CH, CW), night0 + 0.9, night0 + 1.9, 8, 0, False)
else:
    draw(fit("ON YOUR SCHEDULE.", CX, 255, 74, CW), night0, night0 + 1.8, 8, 0, False)
sky(43.6, 46.6, 0, True)

# ---- morning, and it's all yours: the table clears itself, and the sand is laid back down as a folder
clear = []
n = 7
for i in range(n):
    y = H * (i + 0.5) / n
    clear.append([(-120, y), (W + 120, y)] if i % 2 == 0 else [(W + 120, y), (-120, y)])
clearAt = 46.6
draw(clear, clearAt, clearAt + 1.0, 158, 0, False, 1.6)
if PORTRAIT:
    fx, fy, fw, fh = W / 2 - 220, H * 0.52, 440, 320
    t0, t1 = H * 0.27, H * 0.32
    lines = [("EVERY FILE.", W / 2, 470), ("EVERY PROMPT.", W / 2, 590), ("YOURS.", W / 2, 1400)]
else:
    fx, fy, fw, fh = W * 0.63, H * 0.33, 470, 340
    lines = [("EVERY FILE.", W * 0.31, H * 0.40), ("EVERY PROMPT.", W * 0.31, H * 0.56), ("YOURS.", W * 0.31, H * 0.74)]
rows = []
dy = 26; y = fy; i = 0
while y < fy + fh:
    x0, x1 = fx, fx + fw
    if y < fy + 44: x1 = fx + fw * 0.42
    rows.append([(x0, y), (x1, y)] if i % 2 == 0 else [(x1, y), (x0, y)]); y += dy; i += 1
draw(rows, clearAt + 1.1, clearAt + 2.5, 19, 2, False, 0.9)
cap = min(92, ((W - 160) if PORTRAIT else W * 0.46) / width("EVERY PROMPT.", 1.0))
for k, (t, x, y) in enumerate(lines):
    draw(text(t, x, y, cap if k < 2 else cap * 1.3), clearAt + 1.5 + k * 0.85, clearAt + 2.3 + k * 0.85, 8.5 if k < 2 else 11, 2, False, 0.8)

clickOff = 51.0; logo = 51.35
segs.sort(key=lambda s: s[0]); keys.sort(key=lambda k: k[0])

table = {
    "w": W, "h": H, "bpm": BPM, "beat": BEAT, "beats": BEATS, "dur": BEATS * BEAT,
    "clickOn": clickOn, "pour": [pour0, pour1], "lift": lift, "offF": offF, "alone": alone, "wall0": wall0, "land": land,
    "night": [night0, night1], "morning": [clearAt - 0.4, clearAt + 0.8], "clickOff": clickOff, "logo": logo,
    "segs": segs, "keys": keys, "hiss": hiss,
}
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE=" + json.dumps(table, separators=(",", ":")) + ";")
print("dur", table["dur"], "segs", len(segs), "keys", len(keys))
