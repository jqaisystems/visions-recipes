"""R41 · Hatch: the beat grid, read by the film and by score/compose.py.
125 bpm, 72 beats. In beats: rise 0-8, log 8-12, words 12-20, observe 20-32, gate 32-36.5, tunnel 36.5-42, refusal 42-48, publish 48-58, close 58-72.
Writes bake/table.json and assets/table.js.  Usage: python bake/table.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BPM = 125; BEAT = 60 / BPM; BEATS = 72
table = {"dur": BEATS * BEAT, "beat": BEAT, "bpm": BPM, "beats": BEATS}
json.dump(table, open(os.path.join(ROOT, "bake", "table.json"), "w", encoding="utf-8"))
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE = " + json.dumps(table) + ";\n")
print("dur", table["dur"])
