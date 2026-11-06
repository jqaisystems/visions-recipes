"""The one table for R48 · Reflow, read by the film and by score/compose.py: the beat grid and every event that makes a sound.
The site in the film says only YOUR BRAND and is a demo. Writes assets/table.js (not committed).  Usage: python bake/table.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BPM = 112; BEAT = 60 / BPM; BEATS = 60
SITES = 9

table = {
    "bpm": BPM, "beat": BEAT, "beats": BEATS, "dur": BEATS * BEAT, "sites": SITES,
    "drops": [1.1, 2.1, 3.1],                 # the three lumps of brand land
    "row": 5.0,                               # they melt into the row
    "stamp": 6.0, "stampGap": 0.3,            # the mould stamps one grey site per gap
    "hit": 9.1, "topple": 0.22,               # one lump hits the first, and each falls after the last
    "wire": 12.0, "draw": 13.0, "drawEnd": 17.0,   # the slab, then the coils draw the page
    "blobs": [17.5, 18.0, 18.5],              # colour lands on the nav, the hero and the cards
    "breath": 25.0, "slam1": 26.5, "slam2": 29.5, "release": 33.25,   # the squeeze
    "press": 37.25,                           # the cursor presses the button
    "turn": 41.0, "turnEnd": 43.0, "pipes": 42.6,   # round the back
    "fold": 48.0, "shut": 51.0, "slide": 52.4, "logo": 55.5,
}
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE=" + json.dumps(table, separators=(",", ":")) + ";\n")
print("dur", table["dur"])
