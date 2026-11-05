"""R43 · Trace: the beat grid and the beam's colour, read by the film and by score/compose.py.
120 bpm, 68 beats. Sections in beats: dot 0-8, log 8-24, observe 24-34, approve 34-50, publish 50-60, close 60-68.
Writes bake/table.json and assets/table.js.  Usage: python bake/table.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BPM = 120; BEAT = 60 / BPM; BEATS = 68
TEAL = [0.0, 0.86, 0.78]; AQUA = [0.30, 1.0, 0.86]; AMBER = [1.0, 0.62, 0.14]; RED = [1.0, 0.17, 0.08]; BONE = [0.86, 1.0, 0.95]
table = {
    "dur": BEATS * BEAT, "beat": BEAT, "bpm": BPM, "beats": BEATS, "sr": 48000, "aspect": 16 / 9,
    # the beam's colour from each beat on. A real scope has one colour; this one is keyed by time and is not in the audio.
    "colour": [[0, TEAL], [24, AQUA], [34, AMBER], [41, AQUA], [46, AMBER], [48, RED], [50, TEAL], [60, BONE], [62, AQUA]],
    "logo": [62.2, 67.7],
}
json.dump(table, open(os.path.join(ROOT, "bake", "table.json"), "w", encoding="utf-8"))
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE = " + json.dumps(table) + ";\n")
print("dur", table["dur"])
