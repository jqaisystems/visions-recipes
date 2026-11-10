"""The one table for R56 · Pressed, read by the film and by score/compose.py: the beat grid, the pin wall, every relief pressed into it
and when, the filter wave, the light and the captions. The sources, the field and the briefing are a demo.
Writes assets/table.js (not committed).  Usage: python bake/table.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1920, 1080
BPM = 100; BEAT = 60 / BPM; BEATS = 64

# ---------------- the wall: NX by NY pins, PITCH px apart, centred in the frame
NX, NY, PITCH = 256, 144, 7.2
OX, OY = (W - NX * PITCH) / 2, (H - NY * PITCH) / 2
BX, BY = 250, 22                 # where the briefing sits: its left edge, and how far it's moved down
EXT = 46.0                       # how far a pin can slide out, in px

# ---------------- marks, in screen px. Each value is how far the pins there slide out, 0 to 1
def rect(x, y, w, h, v=1.0, r=0): return ["rect", x, y, w, h, v, r]                 # filled
def frame(x, y, w, h, lw, v=1.0, r=0): return ["frame", x, y, w, h, lw, v, r]      # outline
def circ(x, y, rad, lw, v=1.0): return ["circ", x, y, rad, lw, v]                   # ring, or a disc when lw is 0
def line(x0, y0, x1, y1, lw, v=1.0): return ["line", x0, y0, x1, y1, lw, v]
def text(s, x, y, size, wt=800, v=1.0, al="left", fit=0): return ["text", s, x, y, size, wt, v, al, fit]


def page(x, y, w, h):            # a page: an outline, a heading and lines of text
    m = [frame(x, y, w, h, 12, 1.0, 10), rect(x + 34, y + 40, w * 0.5, 22, 0.9)]
    for i in range(6): m.append(rect(x + 34, y + 92 + i * 44, (w - 68) * (0.95 if i % 3 else 0.7), 12, 0.6))
    return m


def feed(x, y, w, h):            # a feed: rows of items, each a square and two lines. Plain lines, not any product's icon
    m = [frame(x, y, w, h, 10, 0.9, 6)]
    rh = (h - 40) / 4
    for i in range(4):
        yy = y + 22 + i * rh
        m += [rect(x + 24, yy, rh - 18, rh - 18, 0.9, 4), rect(x + rh + 18, yy + 6, w * 0.5, 12, 0.7), rect(x + rh + 18, yy + 30, w * 0.34, 10, 0.5)]
    return m


def site(x, y, w, h):            # a site: a window with a bar, a hero block and columns
    m = [frame(x, y, w, h, 10, 1.0, 12), rect(x, y, w, 48, 0.8, 12)]
    m += [rect(x + 30, y + 80, w - 60, h * 0.34, 0.55, 6)]
    for j in range(3): m.append(rect(x + 30 + j * (w - 60) / 3, y + 110 + h * 0.34, (w - 60) / 3 - 22, h * 0.3, 0.7, 6))
    return m


def lens(x, y, rad):             # a magnifier
    return [circ(x, y, rad, 22, 1.0), circ(x, y, rad * 0.62, 0, 0.25), line(x + rad * 0.72, y + rad * 0.72, x + rad * 1.55, y + rad * 1.55, 34, 1.0)]


def chart(x, y, w, h):           # a chart: a base line and bars
    m = [line(x, y + h, x + w, y + h, 10, 0.8)]
    hs = [0.35, 0.55, 0.42, 0.78, 0.62, 1.0]; bw = w / len(hs)
    for i, k in enumerate(hs): m.append(rect(x + i * bw + 10, y + h - h * k, bw - 22, h * k - 8, 0.95, 4))
    return m


def knowledge(x, y, w, h):       # the knowledge document: a structured page, headings and indented rows
    m = [frame(x, y, w, h, 10, 1.0, 8)]
    yy = y + 46
    for sec in range(3):
        m.append(rect(x + 40, yy, w * 0.36, 26, 1.0)); yy += 52
        for k in range(3): m.append(rect(x + 80, yy, (w - 140) * (0.9 - 0.12 * k), 12, 0.7)); yy += 30
        yy += 26
    return m


def folder(cx, cy, w, h):
    x, y = cx - w / 2, cy - h / 2
    return [rect(x, y - 40, w * 0.38, 60, 0.75, 12), rect(x, y, w, h, 0.9, 16), rect(x + 30, y + 40, w - 60, 10, 0.4)]


def glyph(cx, cy, s):            # a briefing, small: a heading bar and three lines
    return [rect(cx - s * 0.36, cy - s * 0.32, s * 0.5, s * 0.14, 1.0, 2)] + [rect(cx - s * 0.36, cy - s * 0.08 + k * s * 0.17, s * 0.72 * (1 - 0.12 * k), s * 0.08, 0.8) for k in range(3)]


# ---------------- layers: a picture and when it's pressed in. keys are [beat, weight]; delay says which way the pins follow:
# "x" left to right, "y" top to bottom, "r" from the middle out, "n" scattered. spread is in beats
layers = []


def L(name, marks, keys, delay="n", spread=1.0, filt=False, move=None, anchor=None):
    layers.append({"name": name, "marks": marks, "keys": keys, "delay": delay, "spread": spread, "filt": filt, "move": move, "anchor": anchor})


# 2 pressed in from everywhere, one after another, then all at once
SRC = {"page": (250, 290, 300, 400), "feed": (660, 250, 430, 300), "site": (1240, 260, 460, 360), "lens": (880, 700, 120), "chart": (1300, 660, 360, 300)}
L("page", page(*SRC["page"]), [[8.0, 0], [9.2, 1]], "r", 0.9, move=[[31.6, 0, 0, 1], [34.0, 160 - 400, 480 + BY - 490, 0.3]], anchor=[400, 490])
L("feed", feed(*SRC["feed"]), [[10.0, 0], [11.2, 1]], "y", 0.9, filt=True)
L("site", site(*SRC["site"]), [[12.0, 0], [13.2, 1]], "x", 0.9, filt=True)
L("lens", lens(*SRC["lens"]), [[14.0, 0], [15.0, 1]], "r", 0.7, move=[[31.9, 0, 0, 1], [34.3, 160 - 900, 650 + BY - 720, 0.42]], anchor=[900, 720])
L("chart", chart(*SRC["chart"]), [[15.6, 0], [16.6, 1]], "x", 0.7, move=[[32.2, 0, 0, 1], [34.6, 160 - 1480, 820 + BY - 810, 0.3]], anchor=[1480, 810])
# echoes of the same kinds of source, all at once, so the wall fills up
L("echo", page(1720, 300, 170, 230) + feed(60, 760, 300, 210) + site(560, 820, 380, 180) + chart(1680, 640, 200, 240) + lens(1120, 430, 70),
  [[16.8, 0], [17.6, 0.85]], "n", 1.2, filt=True)
NOISE = [[16.4, 0], [18.0, 0.95], [21.0, 0.6], [27.5, 0.6]]
# 3 what you know: one structured page pressed in softly underneath everything, and kept
L("knowledge", knowledge(560, 270, 800, 700), [[20.2, 0], [22.0, 0.34], [36.0, 0.34], [38.0, 0]], "y", 1.4)
# 4 the filter: a wave runs across the wall and flattens what doesn't matter, then what's left slides into groups
WAVE = [[28.0, -160], [31.4, W + 160]]
# 5 written up: the groups become the bullets of a short briefing, pushed up out of the wall line by line
BRIEF = [
    (text("THIS WEEK, IN BRIEF", BX - 90, 372, 100, 800), 36.4),
    (text("A NEW SAFETY STANDARD, DRAFTED", BX + 70, 500 + BY, 74, 800), 37.4),
    (text("WHY: IT COVERS TWO OF YOUR ROUTES", BX + 70, 566 + BY, 58, 600, 0.75), 38.0),
    (text("A RIVAL REWROTE ITS SERVICE PAGE", BX + 70, 670 + BY, 74, 800), 38.6),
    (text("WHY: IT NOW TARGETS YOUR REGION", BX + 70, 736 + BY, 58, 600, 0.75), 39.2),
    (text("TWO NEW TENDERS NEARBY", BX + 70, 840 + BY, 74, 800), 39.8),
    (text("WHY: BOTH CLOSE THIS MONTH", BX + 70, 906 + BY, 58, 600, 0.75), 40.4),
]
for i, (mk, b0) in enumerate(BRIEF): L("brief%d" % i, [mk], [[b0, 0], [b0 + 0.7, 1], [44.4, 1], [45.4, 0]], "x", 0.8)
for nm in ("page", "lens", "chart"): next(l for l in layers if l["name"] == nm)["keys"] += [[44.4, 1], [45.4, 0]]
# 6 on schedule: a grid of days. Daily, the briefing presses up on every day in turn; weekly, on one day only
DAYS = []
S, GAP = 170, 30; X0 = (W - (7 * S + 6 * GAP)) / 2
grid = []
for row, yc in enumerate((470, 720)):
    for d in range(7):
        x = X0 + d * (S + GAP); grid.append(frame(x, yc - S / 2, S, S, 9, 0.4, 10)); DAYS.append((x + S / 2, yc, row, d))
L("grid", grid, [[45.2, 0], [46.0, 1], [53.0, 1], [54.0, 0]], "x", 1.0)
POPS = []
for cx, cy, row, d in DAYS:
    if row == 0: b = 46.5 + d * 0.5
    elif d == 0: b = 50.5
    else: continue
    POPS.append([b, row]); L("day%d%d" % (row, d), glyph(cx, cy, S * 0.8), [[b, 0], [b + 0.22, 1], [53.0, 1], [54.0, 0]], "r", 0.15)
# 7 yours: a folder at the edge, then the light slides off the wall
L("folder", folder(960, 640, 420, 300), [[55.0, 0], [56.0, 1]], "r", 0.9)

# ---------------- captions, pressed into the band along the top, each one rising as the last sinks
CAPS = [
    ("YOUR SOURCES.", 2.0, 8.4),
    ("NEWS. SITES.", 9.0, 12.8),
    ("FEEDS. COMPETITORS.", 13.0, 19.6),
    ("BRIEFED ON YOUR FIELD.", 20.4, 24.4),
    ("IT READS THIS FIRST.", 24.6, 28.0),
    ("ONLY WHAT MATTERS.", 28.6, 32.8),
    ("WHAT CHANGED, AND WHY.", 33.0, 36.4),
    ("IN YOUR FORMAT.", 36.6, 40.8),
    ("IN YOUR VOICE.", 41.0, 45.0),
    ("DAILY OR WEEKLY.", 45.4, 49.4),
    ("ON YOUR RHYTHM.", 49.6, 53.4),
    ("THE CODE. THE PROMPTS.", 54.2, 56.0),
    ("THE KNOWLEDGE DOCUMENT.|YOURS.", 56.8, 59.8),
]
CAPY, CAPS_H, CAPW = 150, 112, 1760
for k, (s, b0, b1) in enumerate(CAPS):
    lines = s.split("|"); mk = []
    for i, l in enumerate(lines):
        if len(lines) == 1: mk.append(text(l, W / 2, CAPY + 40, CAPS_H, 800, 1.0, "c", CAPW))
        else: mk.append(text(l, W / 2, CAPY - 4 + i * 86, 78, 800, 1.0, "c", CAPW))
    # each caption is fully down before the next one rises: it starts to sink a beat before the next begins
    out = CAPS[k + 1][1] - 1.0 if k + 1 < len(CAPS) else b1
    L("cap%d" % k, mk, [[b0, 0], [b0 + 0.5, 1], [out - 0.01, 1], [out + 0.4, 0]], "x", 0.6)

# ---------------- the light: a low raking lamp. az is where it comes from (180 = the left, 270 = the top), el how low it is
LIGHT = {
    "on": 1.0, "off": [59.8, 60.9],
    "az": [[0, 196], [36.0, 204], [40.4, 206], [42.2, 302], [44.2, 214], [64, 220]],
    "el": [[0, 27], [40.4, 27], [42.2, 34], [44.2, 27], [64, 27]],
    "spot": [[1.0, -700, 380], [2.4, 760, 420], [36.0, 980, 520], [59.8, 1100, 520], [60.9, 3000, 520]],
}
CAM = [[0, 820, -2400], [64, 1100, -2300]]     # where the camera's vanishing point sits: the pins lean away from it
LOGO = 61.2

table = {
    "w": W, "h": H, "bpm": BPM, "beat": BEAT, "beats": BEATS, "dur": round(BEATS * BEAT, 4),
    "nx": NX, "ny": NY, "pitch": PITCH, "ox": OX, "oy": OY, "ext": EXT,
    "layers": layers, "noise": NOISE, "wave": WAVE, "light": LIGHT, "cam": CAM, "logo": LOGO,
    "pops": POPS, "label": "AI RESEARCH & BRIEFING SYSTEMS · DEMO BRIEFING",
}
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE=" + json.dumps(table, separators=(",", ":"), ensure_ascii=False) + ";")
print("dur", table["dur"], "layers", len(layers), "pins", NX * NY)
