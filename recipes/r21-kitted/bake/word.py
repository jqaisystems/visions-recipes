"""Writes the word "equipped" as outline paths to ../assets/word.js, in a box 1000 units wide centred on 0,0 (y down),
for the ending: the laser engraves these outlines into the foam of the lid. Uses the film's own Inter.
Usage: python word.py   (needs fonttools and brotli)"""
import json
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import DecomposingRecordingPen

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "assets", "fonts", "inter-600.woff2")
WORD, WIDTH = "equipped", 1000

font = TTFont(FONT)
cmap, gs = font.getBestCmap(), font.getGlyphSet()
upm = font["head"].unitsPerEm
names = [cmap[ord(ch)] for ch in WORD]
adv = [font["hmtx"][n][0] for n in names]
scale = WIDTH / sum(adv)
x0, base = -WIDTH / 2, 0.25 * upm * scale     # the x-height sits about on the centre line
contours, x = [], 0
for n, a in zip(names, adv):
    rec = DecomposingRecordingPen(gs)
    gs[n].draw(rec)
    pen = SVGPathPen(gs)
    rec.replay(TransformPen(pen, (scale, 0, 0, -scale, x0 + x * scale, base)))
    for part in pen.getCommands().split("M")[1:]:
        contours.append("M" + part.strip())
    x += a
with open(os.path.join(HERE, "..", "assets", "word.js"), "w", encoding="utf-8", newline="\n") as f:
    f.write("window.WORD = " + json.dumps({"text": WORD, "contours": contours}) + ";\n")
print("contours:", len(contours))
