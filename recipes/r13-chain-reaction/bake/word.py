"""Writes the word "automation" as outline paths in world coordinates to ../assets/word.js, for the pull-back:
the ball's path re-forms into these contours. Uses the film's own Libre Baskerville.
Usage: python word.py   (needs fonttools and brotli)"""
import json, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import DecomposingRecordingPen

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "assets", "fonts", "libre-baskerville-400.woff2")
WORD = "automation"
CENTER = (2525, 1110)       # the middle of the machine, in world px
WIDTH = 3000                # the word's width, in world px

font = TTFont(FONT)
cmap, gs = font.getBestCmap(), font.getGlyphSet()
upm = font["head"].unitsPerEm
names = [cmap[ord(ch)] for ch in WORD]
adv = [font["hmtx"][n][0] for n in names]
scale = WIDTH / sum(adv)
x0 = CENTER[0] - WIDTH / 2
base = CENTER[1] + 0.25 * upm * scale          # the x-height sits about on the centre line

contours, x = [], 0
for n, a in zip(names, adv):
    rec = DecomposingRecordingPen(gs)
    gs[n].draw(rec)
    pen = SVGPathPen(gs)
    rec.replay(TransformPen(pen, (scale, 0, 0, -scale, x0 + x * scale, base)))
    d = pen.getCommands()
    # one path per contour, so the film can sample and fade each one on its own
    for part in d.split("M")[1:]:
        contours.append("M" + part.strip())
    x += a
out = os.path.join(HERE, "..", "assets", "word.js")
with open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write("window.WORD = " + json.dumps({"text": WORD, "contours": contours}) + ";\n")
print("contours:", len(contours), "scale:", round(scale, 4))
