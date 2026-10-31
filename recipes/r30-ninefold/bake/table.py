"""The one table for R30 · Ninefold: every cut, wave, post, tool and impact on a 128 bpm grid, and five
colours taken from the photo for the palette. The film reads assets/table.js, the score reads bake/table.json.
Usage: python bake/table.py"""
import json, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS, BPM, DUR = 30, 128, 32.0
BEAT = 60 / BPM                                   # 0.46875 s
b = lambda x: round(x * BEAT, 4)

T = {
    "open": [0.0, b(6)],          # one glass tile spins, the photo split into colour through it
    "field": [b(6), b(17)],       # it shatters, and the camera pulls back over an endless field of glass
    "feed": [b(17), b(30)],       # a dolly zoom down a profile column; nine tiles drop in posting order
    "tools": [b(30), b(47)],      # one tool every beat and a half, each a new shape of the same field
    "device": [b(47), b(58)],     # a kaleidoscope folds the field into one tile; three words shatter on it
    "title": b(58),
    "end": DUR,
}

# ---------------- I · open
spin = b(5.5)                                     # the spin settles
shatter = b(5.5)                                  # and the tile bursts into nine
words = {"one": b(2), "nine": b(9), "zero": b(13), "order": b(19), "profile": b(29), "twelve": b(45), "browser": b(47)}

# ---------------- II · field
reveal = [b(6), b(9.5)]
pulses = [b(x) for x in range(9, 17)]             # a wave rolls out from the centre on every beat

# ---------------- III · feed
runway = [b(17), b(19)]                           # the dolly zoom down the column
topcut = b(19)                                    # hard cut to straight above
ORDER = [(2 - j % 3, 2 - j // 3) for j in range(9)]   # (col, row), post 1 bottom-right
posts = [b(20 + j) for j in range(9)]
seam = b(29)

# ---------------- IV · tools, only names the app lists
NAMES = ["Grid Maker", "Carousel", "Covers", "Palette", "Resize", "QR Code", "Icon Maker", "Captions", "Hashtags", "Bio"]
TOOLS = [{"name": n, "t": b(30 + 1.5 * j)} for j, n in enumerate(NAMES)]
twelve = b(45)

# ---------------- V · device
kal = b(47)
collapse = [b(49), b(50)]
NOES = [{"word": w, "launch": b(50 + 2 * j), "hit": b(51 + 2 * j)} for j, w in enumerate(["UPLOAD", "ACCOUNT", "WATERMARK"])]

# ---------------- VI · title
morph = [b(58), b(60.5)]
mark = b(61)
line = b(62)

img = Image.open(os.path.join(ROOT, "assets", "img", "demo-banner.jpg")).convert("RGB").resize((180, 240))
pal = img.quantize(colors=5, method=Image.Quantize.MEDIANCUT).getpalette()[:15]
PALETTE = ["#%02x%02x%02x" % tuple(c) for c in sorted([pal[i:i + 3] for i in range(0, 15, 3)], key=lambda c: sum(c))]

cuts = [T["field"][0], T["feed"][0], topcut] + [x["t"] for x in TOOLS] + [twelve, kal, collapse[1]] + [n["hit"] for n in NOES] + [T["title"]]
table = {"fps": FPS, "beat": BEAT, "bpm": BPM, "dur": DUR, "T": T, "spin": spin, "shatter": shatter, "words": words,
         "reveal": reveal, "pulses": pulses, "runway": runway, "topcut": topcut, "order": ORDER, "posts": posts,
         "seam": seam, "tools": TOOLS, "twelve": twelve, "kal": kal, "collapse": collapse, "noes": NOES, "morph": morph,
         "mark": mark, "line": line, "palette": PALETTE, "cuts": sorted(cuts)}
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE = " + json.dumps(table) + ";\n")
json.dump(table, open(os.path.join(ROOT, "bake", "table.json"), "w", encoding="utf-8"), indent=1)
print(json.dumps(T)); print("palette", PALETTE)
