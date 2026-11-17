"""The one table for R60 · Sightline, read by the film and by score/compose.py: the beat grid, the room, where the lamp is on its
rail at every beat, the stations where its shadow reads, the two rebuilds, the marks left on the wall, the camera and the words.
The roadmap is a demo.  Writes assets/table.js (not committed).  Usage: python bake/table.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1920, 1080
BPM = 100; BEAT = 60 / BPM; BEATS = 68

# ---------------- the room. World units: one block is S across; x right, y up; the lattice is centred. Bearings are degrees round it.
S = 10.0
RW = 1600.0                 # from the lattice to the curved wall
FLOOR = -520.0
WALL = [-70.0, 164.0]       # the wall runs between these bearings
RAIL = 1250.0               # the lamp's rail: an arc on the floor on the far side of the lattice from the wall
STATIONS = [0.0, 45.0, 90.0]

# ---------------- the lamp: its angle is the direction its light travels. Spans are [beat from, beat to, degrees from, degrees to],
# eased so it leaves quickly and comes in slowly, and it holds between them
START, STOP = -38.0, 128.0
MOVES = [
    [2.0, 8.0, START, 0.0],       # the tangle, then WHERE
    [9.8, 12.2, 0.0, 45.0],       # DOES
    [13.6, 16.0, 45.0, 90.0],     # AI FIT?
    [25.4, 27.8, 90.0, 45.0],     # (rebuilt at 90: AUDIT) then RANK
    [30.2, 32.6, 45.0, 0.0],      # PLAN
    [41.6, 44.0, 0.0, 45.0],      # (rebuilt at 0: FIRST) then SECOND
    [45.8, 48.2, 45.0, 90.0],     # THIRD
    [50.2, 53.0, 90.0, STOP],     # and on to an angle where nothing reads
]
# each time a word lands: [beat, station, lattice, word]
LANDS = [[8.0, 0, "a", "WHERE"], [12.2, 1, "a", "DOES"], [16.0, 2, "a", "AI FIT?"],
         [22.0, 2, "b", "AUDIT"], [27.8, 1, "b", "RANK"], [32.6, 0, "b", "PLAN"],
         [39.0, 0, "c", "FIRST"], [44.0, 1, "c", "SECOND"], [48.2, 2, "c", "THIRD"]]
LAMP = [[0, 0], [1.59, 0], [1.6, 1.0], [58.0, 1.0], [58.9, 0.45], [62.4, 0.45], [62.9, 0]]     # its level
AMB = [[0, 0], [0.3, 0.0], [1.4, 0.55], [1.6, 0.2], [58.0, 0.2], [58.9, 0.26], [62.4, 0.26], [62.9, 0]]   # the room's own light
SHUTTER = 1.5               # the shadow is exposed over this many frames, so it smears while the lamp moves and is sharp when it stops

# ---------------- the rebuilds: every block slides from where it was to where the next lattice needs it. [beat from, beat to, the
# bearing the wave runs across (the lamp's own, so the word on the wall changes from one end to the other)]
REBUILD = [[18.4, 22.0, 90.0], [35.4, 39.0, 0.0]]
SLIDE = 1.3                 # beats each block takes

# ---------------- the marks: the third lattice's words stay on the wall where they landed. [beat on, beat full] and the level it keeps
MARKS = [[39.3, 40.5], [44.3, 45.5], [48.5, 49.7]]
MARK_KEEP, MARK_GLOW = 0.62, [58.4, 59.6]
TIMELINE = [39.3, 58.4]     # the line under them is drawn as far as the lamp has got, from this beat; and it glows at the end

# ---------------- the words, flat, along the top
CAPS = [
    ("FROM MOST ANGLES, A TANGLE.", 2.6, 6.6),
    ("WHERE DOES AI FIT IN YOUR BUSINESS?", 16.3, 19.6),
    ("WHERE THE HOURS ACTUALLY GO.", 22.2, 25.5),
    ("SCORED BY PAYOFF, RISK AND COST.", 27.9, 30.4),
    ("A PHASED PLAN YOU CAN EXECUTE.", 32.8, 36.0),
    ("WHAT TO BUILD FIRST,", 39.2, 42.6),
    ("SECOND", 44.1, 46.4),
    ("AND THIRD.", 48.3, 50.6),
    ("SOMETIMES THE ANSWER IS:", 53.2, 55.4),
    ("DON'T BUILD IT.", 55.4, 58.2),
    ("NO CODE. JUST DIRECTION.", 59.0, 62.2),
]
RUNS = [42.8, "A PHASED PLAN · 3 TO 12 MONTHS", 50.6]

# ---------------- the camera: [beat, follow, eye bearing, eye distance, eye height, target bearing, target distance, target height, fov]
# with follow at 1 the bearings are measured from the lamp's angle, so 180 is over the lamp's shoulder; at 0 they're fixed in the room
OS = [1, 180, 2500, 1050, 0, 935, -20, 22]          # over the lamp's shoulder: the lattice below, its shadow above
CAM = [
    [0.0, 0, 172, 2000, 380, -20, 0, -10, 34],
    [1.5, 0, 178, 2300, 520, -20, 100, -20, 35],
    [3.2, 0, 192, 3300, 1150, -12, 500, -60, 36],
    [5.6, 0, 188, 3200, 1100, -10, 500, -60, 36],
    [7.0, *OS],
    [17.8, *OS],
    [19.0, 1, 134, 2900, 650, 6, 800, -20, 32],       # the first rebuild, from the side: the blocks and the word together
    [22.8, 1, 138, 2850, 640, 6, 800, -20, 32],
    [24.4, 1, 186, 2600, 1080, 0, 935, -20, 22],
    [34.6, 1, 186, 2600, 1080, 0, 935, -20, 22],
    [36.0, 1, 226, 2900, 650, -6, 800, -20, 32],      # the second rebuild, from the other side
    [39.8, 1, 222, 2850, 640, -6, 800, -20, 32],
    [41.3, 0, 225, 3300, 820, 45, 900, 30, 33],       # the whole wall: the roadmap
    [50.2, 0, 224, 3300, 820, 45, 900, 30, 33],
    [53.0, 0, 262, 3300, 820, 96, 1000, 20, 28],      # towards the angle where nothing reads
    [57.8, 0, 263, 3250, 820, 96, 1000, 20, 28],
    [59.2, 0, 225, 3300, 820, 45, 900, 30, 33],
    [68.0, 0, 225, 3200, 800, 45, 900, 30, 32],
]
LOGO = 62.4

table = {
    "w": W, "h": H, "bpm": BPM, "beat": BEAT, "beats": BEATS, "dur": round(BEATS * BEAT, 4),
    "s": S, "rw": RW, "floor": FLOOR, "wall": WALL, "rail": RAIL, "stations": STATIONS, "start": START, "stop": STOP,
    "moves": MOVES, "lands": LANDS, "lamp": LAMP, "amb": AMB, "shutter": SHUTTER, "rebuild": REBUILD, "slide": SLIDE,
    "marks": MARKS, "markKeep": MARK_KEEP, "markGlow": MARK_GLOW, "timeline": TIMELINE,
    "caps": CAPS, "runs": RUNS, "cam": CAM, "logo": LOGO,
    "label": "AI CONSULTING & ROADMAPPING · DEMO ROADMAP",
}
os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE=" + json.dumps(table, separators=(",", ":"), ensure_ascii=False) + ";")
print("dur", table["dur"])
