"""The one table for R61 · Stacked, read by the film and by score/compose.py: the beat grid, the room, the three lamps, the heap and
the assembly, the two rebuilds, the team stepping into the light, the camera and the words. The stack is a demo.
Writes assets/table.js (not committed).  Usage: python bake/table.py  (run bake/carve.py first)"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1920, 1080
BPM = 104; BEAT = 60 / BPM; BEATS = 68

# ---------------- the room. World units: one block is S across; x right, y up, z towards the walls; the lattice is centred
S = 10.0
RW = 1600.0                 # from the lattice to each wall
FLOOR = -520.0
ANG = [0.0, 45.0, 90.0]     # each lamp's direction across the floor, and the wall square on to it
BEAM = 640.0                # half the width of each beam: narrow enough that the team can stand in one beam and no other

# ---------------- the lamps: [beat, level] keys, eased between. Each lamp is one warm white, a little different
LAMP_COL = [[1.0, 0.86, 0.70], [1.0, 0.80, 0.62], [0.98, 0.90, 0.78]]
ON = [0.8, 1.3, 1.8]
def lamp_keys(i):
    return [[0, 0], [ON[i] - 0.01, 0], [ON[i], 1.0], [61.0, 1.0], [61.7, 0.0]]
LAMPS = [lamp_keys(i) for i in range(3)]
AMB = [[0, 0], [0.4, 0.0], [1.4, 0.16], [61.0, 0.16], [61.7, 0]]

# ---------------- the heap and the assembly: every block lies in a loose pile on the floor, then the lattice is built one row at a
# time from the floor up, so every shadow writes itself from the bottom
HEAP = {"r": 720.0, "h": 330.0}
ASSEMBLE = [9.0, 19.0]      # the first row lifts at the first beat, and the last row has landed by the second
LIFT = 1.7                  # beats each block takes to fly from the heap to its place
HH = 22                     # the lattice's rows (bake/carve.py's H)
ROW_STEP = 0.375            # a dotted sixteenth between rows, so the build plays as a rising scale
ROWS = [ASSEMBLE[0] + k * ROW_STEP for k in range(HH)]   # when each row lifts, bottom row first; each row locks LIFT beats later

# ---------------- the rebuilds: every block slides from where it was to where the next lattice needs it. [beat from, beat to, the
# bearing the wave runs across]
REBUILD = [[27.0, 31.0, 0.0], [46.0, 50.0, 90.0]]
SLIDE = 1.3

# ---------------- the team: three flat heads and shoulders, each standing in one lamp's beam only, beside that lamp's word.
# [lamp, beat in, beat out]
TEAM = [[0, 35.4, 44.2], [1, 36.6, 44.5], [2, 37.8, 44.8]]
TEAM_SCALE = [1.3, 1.2, 1.36]
TEAM_ALONG, TEAM_SIDE = 1450.0, 480.0      # how far towards its wall, and how far to the side of the word

# ---------------- the words, flat, along the top
CAPS = [
    ("SCATTERED ACROSS PERSONAL ACCOUNTS", 2.4, 5.6),
    ("AND PASTED PROMPTS.", 5.8, 8.6),
    ("THE RIGHT TOOLS FOR THE WORK.", 19.6, 26.4),
    ("SET UP FOR THE WAY YOUR TEAM WORKS.", 31.2, 34.8),
    ("HANDS-ON. REAL TASKS.", 38.4, 41.4),
    ("NOT A SLIDESHOW.", 41.6, 44.4),
    ("YOUR ACCOUNTS. YOUR KEYS.", 50.4, 54.2),
    ("YOURS TO KEEP.", 54.4, 60.4),
]

# ---------------- the camera: [beat, eye x, y, z, target x, y, z, fov]
def along(deg, dist, y=0.0):   # a point back along a lamp's line, on the lamps' side of the lattice
    a = math.radians(deg); return [-math.cos(a) * dist, y, -math.sin(a) * dist]
WIDE = [*along(45, 3000, 1250), 480, -80, 480, 44]     # high enough that the lattice sits below the words
CAM = [
    [0.0, *along(45, 1500, -300), 120, -430, 120, 42],
    [5.0, *along(45, 1700, -240), 160, -400, 160, 44],
    [9.0, *along(45, 2300, 200), 300, -240, 300, 46],
    [14.5, *along(45, 2800, 900), 420, -120, 420, 45],
    [19.0, *WIDE],
    [20.0, *WIDE],
    [21.0, *along(0, 5400, 30), 0, 0, 0, 22],
    [22.4, *along(0, 5200, 30), 0, 0, 0, 22],
    [23.2, *along(45, 5400, 30), 0, 0, 0, 22],
    [24.6, *along(45, 5200, 30), 0, 0, 0, 22],
    [25.4, *along(90, 5400, 30), 0, 0, 0, 22],
    [26.4, *along(90, 5200, 30), 0, 0, 0, 22],
    [27.2, *WIDE],
    [34.6, *along(45, 2950, 1220), 480, -80, 480, 44],
    [35.6, *along(45, 3050, 1150), 560, -170, 560, 48],
    [45.0, *along(45, 2950, 1120), 560, -170, 560, 48],
    [46.0, *WIDE],
    [52.0, *along(45, 2850, 1180), 500, -70, 500, 43],
    [61.0, *along(45, 2750, 1150), 500, -70, 500, 42],
    [68.0, *along(45, 2700, 1140), 500, -70, 500, 42],
]
LOGO = 61.2

table = {
    "w": W, "h": H, "bpm": BPM, "beat": BEAT, "beats": BEATS, "dur": round(BEATS * BEAT, 4),
    "s": S, "rw": RW, "floor": FLOOR, "ang": ANG, "beam": BEAM, "lampCol": LAMP_COL, "lamps": LAMPS, "on": ON, "amb": AMB,
    "heap": HEAP, "assemble": ASSEMBLE, "lift": LIFT, "rows": ROWS, "rebuild": REBUILD, "slide": SLIDE,
    "team": TEAM, "teamScale": TEAM_SCALE, "teamAlong": TEAM_ALONG, "teamSide": TEAM_SIDE,
    "caps": CAPS, "cam": CAM, "logo": LOGO,
    "label": "AI STACK SETUP & ENABLEMENT · DEMO STACK",
}
os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE=" + json.dumps(table, separators=(",", ":"), ensure_ascii=False) + ";")
print("dur", table["dur"])
