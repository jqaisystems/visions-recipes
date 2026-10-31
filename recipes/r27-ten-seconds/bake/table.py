"""The one table for R27 Ten Seconds: the clock of every scene on a 96 bpm grid, the ninety-second take and its
strongest ten seconds, the clone's real loudness envelope and word times, the spoken line baked to glyph outlines,
the sample leads and their branch tree, and the quality flags. The film reads assets/table.js, the score reads
bake/table.json. Usage: python bake/table.py  (needs fontTools and brotli for the woff2 font)"""
import json, math, os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# python bake/table.py --vertical <project>  writes the 9:16 cut's table: the same clock, the line and the wall laid out
# for portrait, and the flags on the same beats as the score
VERT = "--vertical" in sys.argv
OUTDIR = sys.argv[sys.argv.index("--vertical") + 1] if VERT else ROOT
CX = 540 if VERT else 960
FPS, BPM, DUR = 30, 96, 32.0
BEAT = 60 / BPM                                   # 0.625 s
q = lambda b: round(b * BEAT, 4)                  # beat number to seconds
hsh = lambda n: (math.sin(n * 127.1 + 311.7) * 43758.5453) % 1.0

T = {
    "rec": [0.0, q(6)],            # a hairline breathes, then ninety seconds of voice race past
    "keep": [q(6), q(14)],         # the whole take, a window finds the strongest ten seconds, the rest peels away
    "machine": [q(14), q(22)],     # a frame draws on: your machine; the clone locks on; a cloud never touches it
    "speak": [q(22), q(32)],       # the line types itself, the clone speaks it, each word melts into the ribbon
    "every": [q(32), q(43)],       # Hi {name}; one page, then a wall of them, one ribbon branching to every lead
    "title": q(43),
    "end": DUR,
}

# ---------------- I · the take: ninety seconds of speech-like loudness at 20 samples a second
SR = 20
take = []
for i in range(90 * SR):
    s = i / SR
    phrase = 0.5 + 0.5 * math.sin(s * 0.9 + 1.3 * math.sin(s * 0.23))          # phrases rise and fall
    gap = 0.15 if (s % 7.3) > 6.4 else 1.0                                        # breaths between phrases
    syl = abs(math.sin(s * math.pi * 4.6 + 2.0 * math.sin(s * 1.7)))             # about four syllables a second
    strong = 1.0 + 0.55 * math.exp(-((s - 57.0) / 6.5) ** 2)                      # the take warms up mid-way
    v = (0.25 + 0.75 * phrase) * gap * (0.35 + 0.65 * syl) * strong * (0.8 + 0.4 * hsh(i * 0.37))
    take.append(v)
m = max(take); take = [round(min(1.0, v / m * 1.08), 3) for v in take]
take[0] = take[-1] = 0.0
# the strongest ten seconds, found the honest way: the window with the highest mean loudness
W10 = 10 * SR
best, bi = -1, 0
for i in range(0, len(take) - W10, 2):
    v = sum(take[i:i + W10]) / W10
    if v > best: best, bi = v, i
bi = round(bi / SR) * SR                          # on a whole second, so the window edges are chunk edges
best_s = bi / SR
breath = [q(1), q(1.5)]
write = [q(1.5), q(5.5)]           # the take writes itself, the timer runs 00:00 to 01:30
pull = [q(6), q(8)]                # the camera pulls back over the whole take
scan = [q(8), q(11)]               # the window weighs the take
lock = q(11)                       # it locks on the best ten
peel = [q(11.5), q(13)]            # everything outside drains and peels away
dive = [q(12.5), q(14)]            # the camera dives into the ten seconds

# ---------------- III · your machine
frame = [q(14), q(15.5)]
clone = [q(16), q(17.5)]           # the clone slides over the voice and locks
cloud = [q(18), q(19.5)]           # a cloud drifts in and stops short
erase = [q(19.5), q(21)]           # it erases itself line by line

# ---------------- IV · it speaks: the clone line from the public Tembr demo, its envelope at 30 fps
ENV = [0.0, 0.0, 0.067, 0.162, 0.739, 0.734, 0.602, 0.553, 0.541, 0.299, 0.537, 0.712, 0.6, 0.395, 0.35, 0.226, 0.456, 1, 0.948, 0.904, 0.625, 0.503, 0.275, 0.142, 0.191, 0.24, 0.207, 0.178, 0.103, 0.061, 0.038, 0.04, 0.023, 0.19, 0.19, 0.087, 0.545, 0.885, 0.868, 0.927, 0.872, 0.793, 0.422, 0.827, 0.779, 0.654, 0.446, 0.135, 0.249, 0.325, 0.515, 0.873, 0.639, 0.347, 0.403, 0.393, 0.344, 0.378, 0.314, 0.293, 0.159, 0.056, 0.025, 0.037, 0.059, 0.068, 0.058, 0.062, 0.069, 0.091, 0.041, 0.014, 0.071, 0.662, 0.882, 0.84, 0.692, 0.753, 0.764, 0.722, 0.809, 0.911, 0.815, 0.802, 0.81, 0.755, 0.53, 0.378, 0.664, 0.763, 0.761, 0.75, 0.707, 0.739, 0.711, 0.662, 0.437, 0.538, 0.519, 0.456, 0.351, 0.731, 0.519, 0.36, 0.32, 0.244, 0.153, 0.067]
WORDS = [["I", 0.07], ["am", 0.21], ["his", 0.31], ["voice,", 0.45], ["cloned", 1.09], ["by", 1.39], ["Tembr,", 1.55],
         ["running", 2.25], ["on", 2.57], ["his", 2.79], ["own", 2.93], ["machine.", 3.07]]
CLIP = 3.6
type_ = [q(22.5), q(24)]           # the line types itself
voice = q(24)                      # the clone speaks (assets/audio/clone-line.wav)
words = [{"w": w, "t": round(voice + a, 4), "a": a, "b": (WORDS[k + 1][1] if k + 1 < len(WORDS) else CLIP)} for k, (w, a) in enumerate(WORDS)]

# the line baked to glyph outlines (Archivo 800), two rows centred, in frame pixels
font = TTFont(os.path.join(ROOT, "assets", "fonts", "archivo-800-latin.woff2"))
gs, cmap, hmtx, upm = font.getGlyphSet(), font.getBestCmap(), font["hmtx"], font["head"].unitsPerEm
SIZE = 104 if VERT else 112
ROWS = [(0, 4, 620), (4, 7, 740), (7, 10, 860), (10, 12, 980)] if VERT else [(0, 7, 350), (7, 12, 490)]   # word ranges and baselines
def glyph(ch, x, y):
    name, s = cmap[ord(ch)], SIZE / upm
    rec = RecordingPen()
    gs[name].draw(TransformPen(rec, (s, 0, 0, -s, x, y)))
    subs, cur = [], []
    for op in rec.value:
        if op[0] == "moveTo" and cur: subs.append(cur); cur = []
        cur.append(op)
    if cur: subs.append(cur)
    def render(ops, pen):
        r = RecordingPen(); r.value = ops; r.replay(pen)
    full, best, outer = SVGPathPen(gs, ntos=lambda v: ("%.1f" % v).rstrip("0").rstrip(".")), -1, ""
    render(rec.value, full)
    for sp in subs:
        bp = BoundsPen(gs); render(sp, bp)
        if bp.bounds:
            a = (bp.bounds[2] - bp.bounds[0]) * (bp.bounds[3] - bp.bounds[1])
            if a > best:
                pp = SVGPathPen(gs, ntos=lambda v: ("%.1f" % v).rstrip("0").rstrip(".")); render(sp, pp); best, outer = a, pp.getCommands()
    return full.getCommands(), outer, hmtx[name][0] * s
space = hmtx[cmap[ord(" ")]][0] * SIZE / upm
letters = []
for a, b, base in ROWS:
    width = sum(sum(hmtx[cmap[ord(c)]][0] * SIZE / upm for c in WORDS[k][0]) for k in range(a, b)) + space * (b - a - 1)
    x = CX - width / 2
    for k in range(a, b):
        w = WORDS[k][0]
        for j, ch in enumerate(w):
            d, outer, adv = glyph(ch, x, base)
            letters.append({"word": k, "i": j, "n": len(w), "d": d, "outer": outer, "x0": round(x, 1), "x1": round(x + adv, 1)})
            x += adv
        x += space

# ---------------- V · everywhere: sample leads, one hero page, a wall of pages, a branch tree
FIRST = ["Maya", "Tomás", "Inês", "Priya", "Leo", "Ana", "Sam", "Noor", "Jonas", "Clara", "Ravi", "Elena", "Omar", "Lucía",
         "Finn", "Aiko", "Marta", "Kofi", "Sofia", "Hugo", "Lena", "Diego", "Yara", "Ben"]
PLACE = ["Bakery", "Dental", "Studio", "Florist", "Cycles", "Books", "Coffee", "Yoga", "Optics", "Framing", "Tailor", "Garden"]
STREET = ["Northside", "Harbour", "Elm Row", "Old Mill", "Riverside", "Hillcrest", "Market St", "Southgate"]
COLS, ROWS_W, PW, PH = (8, 15, 340, 230) if VERT else (12, 10, 340, 230)
HERO = (3, 7) if VERT else (5, 4)
HALF = COLS * PW / 2                                    # the wall's half width: the scan runs past it
leads = []
for r_ in range(ROWS_W):
    for c in range(COLS):
        k = r_ * COLS + c
        nm = FIRST[(k * 7 + 3) % len(FIRST)] if (c, r_) != HERO else "Maya"
        biz = (STREET[(k * 5) % len(STREET)] + " " + PLACE[(k * 11 + 2) % len(PLACE)]) if (c, r_) != HERO else "Northside Bakery"
        leads.append({"c": c, "r": r_, "x": (c - (COLS - 1) / 2) * PW, "y": (r_ - (ROWS_W - 1) / 2) * PH, "name": nm, "biz": biz})
hero = HERO[1] * COLS + HERO[0]
hx, hy = leads[hero]["x"], leads[hero]["y"]
# three branches by angle around the hero, each split in four, each sub-hub feeding its leaves
others = [k for k in range(len(leads)) if k != hero]
ang = lambda k: math.atan2(leads[k]["y"] - hy, leads[k]["x"] - hx)
others.sort(key=ang)
def centroid(ks, pull):
    cx = sum(leads[k]["x"] for k in ks) / len(ks); cy = sum(leads[k]["y"] for k in ks) / len(ks)
    return [round(hx + (cx - hx) * pull, 1), round(hy + (cy - hy) * pull, 1)]
tree = []
n1 = len(others)
groups = [others[i * n1 // 3:(i + 1) * n1 // 3] for i in range(3)]
switch = q(32)
names_at = [q(32.25 + 0.375 * k) for k in range(6)]      # the {name} slot flicks through sample names, lands on Maya
into_page = [q(34.5), q(35.75)]                          # the voice flows into Maya's page
pullout = [q(35.75), q(39)]                            # the camera pulls back to the wall
b1, b2, b3 = [q(36), q(37)], [q(36.75), q(37.75)], [q(37.5), q(40)]
for gi, g in enumerate(groups):
    h1 = centroid(g, 0.45)
    subs = [g[i * len(g) // 4:(i + 1) * len(g) // 4] for i in range(4)]
    kids = []
    for si, sg in enumerate(subs):
        h2 = centroid(sg, 0.85)
        leaves = []
        for k in sg:
            d = math.hypot(leads[k]["x"] - hx, leads[k]["y"] - hy)
            leaves.append({"k": k, "t": round(b3[0] + (b3[1] - b3[0] - 0.4) * min(1, d / 2100) + 0.12 * hsh(k), 4)})
        kids.append({"p": h2, "leaves": leaves})
    tree.append({"p": h1, "kids": kids})
qc = [q(40), q(41.5)]                                  # one scan across the wall
FLAGS = ["LONG PAUSE", "REPEATED WORD", "MANGLED ENDING"]
FLAG_T = [25.3549, 25.5826, 25.279]                    # the main cut's flags, so both cuts share one score
flags = []
if VERT:
    for j, (row, ft) in enumerate(zip((3, 7, 11), FLAG_T)):
        xr = -(HALF + 60) + (ft - qc[0]) / (qc[1] - qc[0]) * 2 * (HALF + 60)
        k = min((k for k in others if leads[k]["r"] == row), key=lambda k: abs(leads[k]["x"] - xr))
        flags.append({"k": k, "kind": j, "word": FLAGS[j], "t": round(qc[0] + (leads[k]["x"] + HALF + 60) / (2 * (HALF + 60)) * (qc[1] - qc[0]), 4)})
else:
    for j, k in enumerate([others[17], others[60], others[96]]):
        flags.append({"k": k, "kind": j, "word": FLAGS[j], "t": round(qc[0] + (leads[k]["x"] + HALF + 60) / (2 * (HALF + 60)) * (qc[1] - qc[0]), 4)})
retract = [q(43), q(44.5)]
bar = q(44.5)
mark = q(45)

table = {"fps": FPS, "beat": BEAT, "bpm": BPM, "dur": DUR, "T": T,
         "take": take, "sr": SR, "best": best_s, "breath": breath, "write": write, "pull": pull, "scan": scan, "lock": lock,
         "peel": peel, "dive": dive, "frame": frame, "clone": clone, "cloud": cloud, "erase": erase,
         "env": ENV, "clip": CLIP, "type": type_, "voice": voice, "words": words, "letters": letters,
         "leads": leads, "hero": hero, "tree": tree, "switch": switch, "names_at": names_at, "into_page": into_page,
         "pullout": pullout, "b1": b1, "b2": b2, "b3": b3, "qc": qc, "flags": flags, "retract": retract, "bar": bar, "mark": mark, "half": HALF}
open(os.path.join(OUTDIR, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE = " + json.dumps(table, ensure_ascii=False) + ";\n")
slim = {k: v for k, v in table.items() if k not in ("letters", "take", "env")}
if not VERT: json.dump(slim, open(os.path.join(ROOT, "bake", "table.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(json.dumps(T)); print("best ten seconds start", best_s, "letters", len(letters), "flags", [(f["word"], f["t"]) for f in flags])
