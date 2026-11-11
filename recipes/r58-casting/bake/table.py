"""The one table for R58 · Casting, read by the film and by score/compose.py: the beat grid, the room, the lamps and when they
light, the lattice's turns, rebuilds and collapse, the human who signs off, the camera and the words. The system is a demo.
Writes assets/table.js (not committed).  Usage: python bake/table.py  (run bake/carve.py first)"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1920, 1080
BPM = 96; BEAT = 60 / BPM; BEATS = 64

# ---------------- the room. World units: one block is S across; x right, y up, z towards the walls; the lattice is centred
S = 10.0
RW = 1600.0           # from the lattice to each wall
FLOOR = -520.0
# the walls are faces of an octagon, each square on to one lamp: 0° (RESEARCH), 45° (DRAFT), 90° (REVIEW), 135° (PUBLISH)

# ---------------- the lamps: [beat on, beat off] spans and a level, keyed. Each lamp is one warm white, a little different.
# key lists are [beat, level] pairs, eased between
LAMP_COL = [[1.0, 0.86, 0.70], [1.0, 0.80, 0.62], [0.98, 0.90, 0.78], [1.0, 0.84, 0.66]]
ON = [6.4, 8.4, 10.4]
HAND = [25.0, 27.0, 29.0]           # the handoffs: each lamp in turn at full, the others low
def lamp_keys(i):
    k = [[0, 0]]
    if i < 3:
        on = ON[i]; k += [[on - 0.01, 0], [on, 1.0], [24.0, 1.0], [24.6, 0.28]]
        for j, h in enumerate(HAND):
            if j == i: k += [[h - 0.3, 0.28], [h, 1.0], [h + 1.7, 1.0], [h + 2.0, 0.4 if i < 2 else 1.0]]
        if i == 2: k += [[30.0, 1.0], [30.6, 0.7], [33.4, 0.7]]
        else: k += [[30.0, 0.4], [33.4, 0.4]]
        k += [[34.0, 1.0]]
    else:
        k += [[35.0 - 0.01, 0], [35.0, 1.0]]
    if i == 0: k += [[43.4, 1.0], [52.0, 1.0]]
    else: k += [[43.4 + 0.25 * i, 1.0], [43.45 + 0.25 * i, 0], [51.6 + 0.2 * i, 0], [51.65 + 0.2 * i, 1.0]]
    k += [[57.6, 1.0], [58.3, 0]]
    return k
LAMPS = [lamp_keys(i) for i in range(4)]
SWING = [35.0, 36.4, 160.0]          # the fourth lamp swings in from 160° to 135° as it comes on

# ---------------- the lattice
TURN = [0.0, 6.4, 1.15]              # it turns, and settles square to the lamps the moment the first one lights (radians at beat 0)
REBUILD = [36.6, 40.4]               # three lamps' lattice becomes four lamps' lattice, block by block
COLLAPSE = [44.4, 46.6]              # every block slides into one plain cube
EXPAND = [51.6, 53.8]                # and back out to the four-lamp lattice
SHARED = [14.0, 24.0]                # the blocks more than one shadow needs glow warm

# ---------------- the human who signs off: a head and shoulders, in REVIEW's light, beside the word
HUMAN = {"in": [30.2, 31.4], "out": [33.6, 34.4], "x0": -1400.0, "x1": -470.0, "z": 920.0, "y": -300.0}

# ---------------- the words, flat, along the top
CAPS = [
    ("ONE SYSTEM.", 1.6, 5.8),
    ("EVERY AGENT HAS ONE ROLE.", 7.0, 13.6),
    ("ONE SHARED MEMORY.", 14.6, 23.6),
    ("EACH HANDS ITS WORK ON.", 24.6, 29.8),
    ("A HUMAN SIGNS OFF.", 30.6, 34.2),
    ("A NEW AGENT.", 35.0, 37.0),
    ("ADD ONE IN HOURS, NOT WEEKS.", 37.4, 43.0),
    ("IF ONE PROMPT IS ENOUGH,", 44.6, 47.8),
    ("I'LL SAY SO.", 48.0, 51.2),
    ("YOU OWN ALL OF IT.", 53.8, 57.6),
]
RUNS = [25.0, "ON A SCHEDULE · ON A TRIGGER · ON REQUEST", 29.8]
BEAM = [[25.9, 26.9, 0, 1], [27.9, 28.9, 1, 2]]    # the handoff light running along the walls, from one word to the next

# ---------------- the camera: [beat, eye x, y, z, target x, y, z, fov]
def along(deg, dist, y=0.0):   # a point back along a lamp's line, on the lamp's side of the lattice
    a = math.radians(deg); return [-math.cos(a) * dist, y, -math.sin(a) * dist]
MID = 67.5
w0 = along(MID, 3000, 1000)
CAM = [
    [0.0, *along(MID, 1300, 260), 0, -20, 0, 34],
    [5.6, *along(MID, 1700, 420), 0, -20, 0, 38],
    [6.6, *along(MID - 25, 2600, 900), 420, -60, 520, 44],
    [13.0, *w0, 560, -40, 600, 46],
    [14.0, *along(0, 5600, 30), 0, 0, 0, 22],
    [16.8, *along(0, 5200, 30), 0, 0, 0, 22],
    [17.6, *along(45, 5600, 30), 0, 0, 0, 22],
    [20.4, *along(45, 5200, 30), 0, 0, 0, 22],
    [21.2, *along(90, 5600, 30), 0, 0, 0, 22],
    [23.8, *along(90, 5200, 30), 0, 0, 0, 22],
    [24.8, *w0, 560, -40, 600, 46],
    [29.6, *along(MID, 2900, 980), 560, -40, 600, 46],
    [30.4, -1500, 260, -500, -260, -230, 1500, 40],
    [34.2, -1420, 250, -420, -260, -230, 1500, 40],
    [35.0, *along(MID + 20, 3100, 1000), 300, -40, 760, 48],
    [42.8, *along(MID + 20, 3000, 980), 300, -40, 760, 48],
    [43.8, *along(8, 3000, 260), 500, -20, 0, 26],
    [51.0, *along(8, 2800, 250), 500, -20, 0, 26],
    [52.0, *along(MID, 3100, 1000), 400, -40, 700, 48],
    [64.0, *along(MID, 2900, 960), 400, -40, 700, 48],
]
LOGO = 58.4

table = {
    "w": W, "h": H, "bpm": BPM, "beat": BEAT, "beats": BEATS, "dur": round(BEATS * BEAT, 4),
    "s": S, "rw": RW, "floor": FLOOR, "lampCol": LAMP_COL, "lamps": LAMPS, "swing": SWING, "turn": TURN,
    "rebuild": REBUILD, "collapse": COLLAPSE, "expand": EXPAND, "shared": SHARED, "human": HUMAN,
    "caps": CAPS, "runs": RUNS, "beam": BEAM, "hand": HAND, "on": ON, "cam": CAM, "logo": LOGO,
    "label": "AI AGENT ARCHITECTURE · DEMO SYSTEM",
}
os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE=" + json.dumps(table, separators=(",", ":"), ensure_ascii=False) + ";")
print("dur", table["dur"])
