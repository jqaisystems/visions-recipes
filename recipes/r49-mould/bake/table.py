"""The one table for R49 · Mould, read by the film and by score/compose.py: the beat grid and every event that makes a sound.
The pictures in the film are demos. Writes assets/table.js (not committed).  Usage: python bake/table.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BPM = 104; BEAT = 60 / BPM; BEATS = 57

table = {
    "bpm": BPM, "beat": BEAT, "beats": BEATS, "dur": BEATS * BEAT,
    "drops": [0.8, 1.4, 2.0, 2.6, 3.2, 3.8],   # six mismatched pictures land
    "gather": 5.6, "morph": 6.4, "lumpEnd": 23.0,   # they're squashed into one lump
    "rod": 12.0, "plates": [12.5, 13.5, 14.5, 15.5],   # the screw, then the four plates
    "pressStart": 19.6, "pressHit": 21.0,      # one slow press
    "seals": 23.3,                             # a thumb marks the first set
    "fly": 26.0,                               # the approved six go up on the wall
    "slams": [27, 28, 29, 30, 31, 32, 33, 34, 35], "bursts": [1, 2, 2, 3, 4, 5, 6, 7, 9],   # the run
    "retract": 35.5,
    "stop": 38.4, "stamp": 40.0, "replace": 41.0,   # the pink one, the silence and the stamp
    "sink": 43.4, "moves": 43.5, "yours": 48.0, "slide": 49.5, "logo": 52.5,
}
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE=" + json.dumps(table, separators=(",", ":")) + ";")
print("dur", table["dur"])
