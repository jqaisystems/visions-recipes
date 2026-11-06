"""The one table for R47 · Flywheel, read by the film and by score/compose.py: the beat grid, the pin batch and the day of every click.
Every pin is invented. Writes assets/table.js (not committed).  Usage: python bake/table.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BPM = 120; BEAT = 60 / BPM; BEATS = 64
PINS, DAYS = 108, 75

# the batch is cut row by row: a cutter tick for every pin
CUT, CUT_END = 14.0, 20.0
cuts = [round(CUT + (CUT_END - CUT) * i / PINS, 4) for i in range(PINS)]

# the days: slow, then a little quicker, then a blur of notches. It's the click that sets the tempo
clicks = [33.0, 35.0, 37.0, 38.0, 39.0]
iv = 1.0
while len(clicks) < 20:
    iv = max(iv * 0.87, 0.14)
    clicks.append(round(clicks[-1] + iv, 4))
left = DAYS - len(clicks); end = 52.0; gap = (end - clicks[-1]) / left
for _ in range(left):
    clicks.append(round(clicks[-1] + gap, 4))
assert len(clicks) == DAYS and abs(clicks[-1] - end) < 0.01 and gap > 0.05, gap

table = {"bpm": BPM, "beat": BEAT, "beats": BEATS, "dur": BEATS * BEAT, "pins": PINS, "days": DAYS, "cuts": cuts, "clicks": clicks,
         "drop": 1.0, "strat": 4.0, "batch": 12.0, "cut": CUT, "approve": 22.0, "stamp": 24.0, "wheel": 27.0, "breath": 31.5, "day1": 33.0,
         "seasons": 41.0, "pull": 52.0, "melt": 57.0, "logo": 60.0}
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE=" + json.dumps(table, separators=(",", ":")) + ";\n")
print("days", len(clicks), "gap", round(gap, 3), "last slow", clicks[19], "dur", table["dur"])
