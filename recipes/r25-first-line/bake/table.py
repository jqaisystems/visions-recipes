"""The one table for R25 First Line: the clock of every scene, the beat grid (96 bpm), the line, the page flips, the
strokes drawing, the wipes from pencil to ink to colour, the panels, the figures, the impact frames and the smear
frames. The film reads assets/table.js, the score reads bake/table.json. Usage: python bake/table.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS, BPM, DUR = 30, 96, 32.0
BEAT = 60 / BPM                                   # 0.625 s
q = lambda b: round(b * BEAT, 4)                  # beat number to seconds

T = {
    "brief": [0.0, q(7)],         # night, a desk by the window over the Douro, a blank sheet, one pencil line
    "sketch": [q(7), q(18)],      # the world in blue pencil; roughs pile up; a flip book of roughs
    "ink": [q(18), q(29)],        # the four strokes draw themselves, lift off, pencil to ink to colour, the mark locks
    "system": [q(29), q(40)],     # manga panels of the applications slam in on the beat
    "world": [q(40), q(45)],      # out of the window over Porto at dawn; the strokes fly out as trails; the figures
    "title": q(45),
    "end": DUR,
}
lamp = q(1)                                       # the lamp clicks on
line = [q(3.5), q(5.5)]                           # the pencil draws the first line
roughs = [round(q(8) + k * BEAT * 2 / 3, 4) for k in range(9)]        # rough marks land on the sheet, in triplets
flips = [round(q(14) + k * BEAT / 2, 4) for k in range(8)]             # the flip book: eight pages on the half beat
strokes = [[q(18 + k / 2), q(18 + k / 2) + 1.0] for k in range(4)]     # each of the four strokes draws itself, on the half beat
lift = [q(22), q(23)]                         # the strokes lift off the paper and stand up as the mark
wipes = [{"t": q(7), "to": "pencil"}, {"t": q(23.5), "to": "ink"}, {"t": q(25), "to": "colour"}]  # each wipe takes half a second
lock = q(26)                                      # the mark locks front-on
panels = [{"t": q(29 + 1.5 * k), "word": w, "obj": o} for k, (w, o) in enumerate([
    ("LOGO", "card"), ("COLOUR", "box"), ("TYPE", "sign"), ("PACKAGING", "bag"), ("LABELS", "bottle"), ("SOCIAL", "phone")])]
trails = q(41)                                    # the four strokes fly out of the window as trails
figures = [{"t": q(41.5 + k), "big": b, "small": s} for k, (b, s) in enumerate([
    ("1,200+", "BRANDS"), ("40+", "COUNTRIES"), ("2014", "SINCE")])]

impacts = [{"t": line[1], "n": 2}, {"t": lock, "n": 3}, {"t": panels[0]["t"], "n": 2}, {"t": panels[5]["t"], "n": 2},
           {"t": T["world"][0], "n": 2}]
impacts.sort(key=lambda d: d["t"])
# smear frames: the two frames of the lift, and the first frame of every page flip
smears = sorted(set([round(lift[0] * FPS) + j for j in (8, 9)] + [round(f * FPS) + 1 for f in flips]))

table = {"fps": FPS, "beat": BEAT, "bpm": BPM, "dur": DUR, "T": T, "lamp": lamp, "line": line, "roughs": roughs,
         "flips": flips, "strokes": strokes, "lift": lift, "wipes": wipes, "lock": lock, "panels": panels,
         "trails": trails, "figures": figures, "impacts": impacts, "smears": smears}
open(os.path.join(ROOT, "assets", "table.js"), "w").write("window.TABLE = " + json.dumps(table) + ";\n")
json.dump(table, open(os.path.join(ROOT, "bake", "table.json"), "w"), indent=1)
print(json.dumps(T)); print("panels", [p["t"] for p in panels], "lock", lock, "wipes", [w["t"] for w in wipes])
