"""The one table for R29 Seamless: the clock of every scene on a 112 bpm grid, the pour, the seams and the beat each
one snaps on, the posting order, the tool morphs, the upload that springs back, the title, and five colours taken from
the photo for the palette. The film reads assets/table.js, the score reads bake/table.json.
Usage: python bake/table.py  (or --vertical <project> for the 9:16 cut's table)"""
import json, os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERT = "--vertical" in sys.argv
OUTDIR = sys.argv[sys.argv.index("--vertical") + 1] if VERT else ROOT
FPS, BPM, DUR = 30, 112, 32.0
BEAT = 60 / BPM                                   # 0.5357 s
q = lambda b: round(b * BEAT, 4)

T = {
    "pour": [0.0, q(9)],          # a drop falls into a pool, the photo surfaces as it settles
    "cut": [q(9), q(20)],         # seams draw a 3x3 grid, stretch into necks and snap on the beat
    "post": [q(20), q(30)],       # the tiles hop into a profile grid in posting order, then melt seamless
    "tools": [q(30), q(43)],      # the liquid morphs through five tools
    "device": [q(43), q(50)],     # an upload tries to pull a drop out of the browser; it springs back
    "title": q(50),
    "end": DUR,
}

# ---------------- I · the pour
fall = [q(1), q(3)]                               # the drop falls and hits the pool
surface = [q(4.5), q(8)]                          # the photo surfaces as the ripples die

# ---------------- II · the cut: four seams, each drawn, stretched and snapped on its own beat
draw = [q(10), q(12)]
SEAMS = [{"axis": "x", "i": 1, "snap": q(13)}, {"axis": "x", "i": 2, "snap": q(14)},
         {"axis": "z", "i": 1, "snap": q(15)}, {"axis": "z", "i": 2, "snap": q(16)}]
numbers = [q(17), q(19.5)]

# ---------------- III · posted: post 1 is the bottom-right tile, then leftwards and upwards
ORDER = [(2 - j % 3, 2 - j // 3) for j in range(9)]   # (col, row), row 0 at the top
posts = [q(21 + j) for j in range(9)]
melt = [q(29.25), q(30)]

# ---------------- IV · five tools, each a shape the liquid takes on the beat
TOOLS = [{"name": "Carousel", "t": q(30)}, {"name": "Covers", "t": q(32.5)}, {"name": "Palette", "t": q(35)},
         {"name": "Resize", "t": q(37.5)}, {"name": "QR Code", "t": q(40)}, {"name": "Grid Maker", "t": q(42)}]
resize = [q(38), q(38.75), q(39.5)]               # 1:1, 4:5, 9:16

# ---------------- V · on your device
tray = [q(43), q(44)]
pull = [q(45), q(47)]                             # stretched up to the window's edge
snap = q(47)                                      # and back
labels = [q(45), q(46.5), q(48)]

# ---------------- VI · title
gather = [q(50), q(52)]
mark = q(53)
line = q(54)

# five colours from the photo, for the palette (median cut, sorted dark to light)
img = Image.open(os.path.join(ROOT, "assets", "img", "demo-banner.jpg")).convert("RGB").resize((180, 240))
pal = img.quantize(colors=5, method=Image.Quantize.MEDIANCUT).getpalette()[:15]
PALETTE = sorted([pal[i:i + 3] for i in range(0, 15, 3)], key=lambda c: sum(c))
PALETTE = ["#%02x%02x%02x" % tuple(c) for c in PALETTE]

impacts = [fall[1]] + [s["snap"] for s in SEAMS] + posts + [snap, mark]
table = {"fps": FPS, "beat": BEAT, "bpm": BPM, "dur": DUR, "T": T, "fall": fall, "surface": surface, "draw": draw,
         "seams": SEAMS, "numbers": numbers, "order": ORDER, "posts": posts, "melt": melt, "tools": TOOLS,
         "resize": resize, "tray": tray, "pull": pull, "snap": snap, "labels": labels, "gather": gather, "mark": mark,
         "line": line, "palette": PALETTE, "impacts": impacts, "vert": VERT}
os.makedirs(os.path.join(OUTDIR, "assets"), exist_ok=True)
open(os.path.join(OUTDIR, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE = " + json.dumps(table) + ";\n")
if not VERT:
    json.dump(table, open(os.path.join(ROOT, "bake", "table.json"), "w", encoding="utf-8"), indent=1)
print(json.dumps(T)); print("palette", PALETTE)
