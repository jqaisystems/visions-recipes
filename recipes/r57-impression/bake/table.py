"""The one table for R57 · Impression, read by the film and by score/compose.py: the beat grid, the pin frame, every shape pressed
into it and when, the moulds that test the fit, the resets, the camera, the light and the words. The workflow and the paths are a demo.
Writes assets/table.js (not committed).  Usage: python bake/table.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1920, 1080
BPM = 96; BEAT = 60 / BPM; BEATS = 64

# ---------------- the frame: NX by NY steel pins, PITCH apart. Field units: 0..FW across, 0..FH down, one pin every PITCH
NX, NY, PITCH = 144, 80, 10.0
FW, FH = NX * PITCH, NY * PITCH
EXT = 60.0          # how far a pin can slide out of the plate
LEN = 78.0          # how long a pin is

# ---------------- marks, in field units. v is how far the pins there are pushed, 0 to 1. Later marks paint over earlier ones
def rect(x, y, w, h, v=1.0, r=0): return ["rect", x, y, w, h, v, r]
def frame(x, y, w, h, lw, v=1.0, r=0): return ["frame", x, y, w, h, lw, v, r]
def circ(x, y, rad, lw, v=1.0): return ["circ", x, y, rad, lw, v]          # ring, or a disc when lw is 0
def line(x0, y0, x1, y1, lw, v=1.0): return ["line", x0, y0, x1, y1, lw, v]
def arc(x, y, rx, ry, a0, a1, lw, v=1.0): return ["arc", x, y, rx, ry, a0, a1, lw, v]
def text(s, x, y, size, wt=800, v=1.0, al="c"): return ["text", s, x, y, size, wt, v, al]
def full(v): return rect(-20, -20, FW + 40, FH + 40, v)

# ---------------- the problem: one workflow as it runs now, snags and all
STEPS = [(165, 0.62), (405, 0.48), (645, 0.70), (1035, 0.55), (1275, 0.64)]
SY, SW, SH = 470, 150, 150
DELAY = (840, 470, 78)
problem = []
for i, (cx, _) in enumerate(STEPS[:-1]):                      # the handoffs: ridges between steps, with burrs on them
    nx = STEPS[i + 1][0]
    if cx == 645: problem.append(line(cx + SW / 2, SY, DELAY[0] - DELAY[2], SY, 26, 0.34)); problem.append(line(DELAY[0] + DELAY[2], SY, nx - SW / 2, SY, 26, 0.34))
    else: problem.append(line(cx + SW / 2, SY, nx - SW / 2, SY, 26, 0.34))
    for k in range(3):
        bx = cx + SW / 2 + 18 + k * 26 + (i * 7) % 11
        problem.append(rect(bx, SY - 22 + ((k + i) % 2) * 26, 12, 18, 0.46))
problem.append(arc(720, 330, 330, 150, 200, 340, 24, 0.44))   # rework: a loop from step four back to step two
problem += [line(1015, 395, 1000, 352, 24, 0.44), rect(372, 380, 30, 30, 0.44, 4)]
problem.append(circ(DELAY[0], DELAY[1], DELAY[2], 24, 0.52))   # the delay: a ring with a sunken middle, where work waits
problem.append(circ(DELAY[0], DELAY[1], DELAY[2] - 16, 0, 0.06))
for cx, v in STEPS:                                             # the steps, each a block of its own height, one with a notch
    problem.append(rect(cx - SW / 2, SY - SH / 2, SW, SH, v, 14))
problem.append(rect(STEPS[2][0] - 20, SY + 20, 40, 55, 0.3, 4))
problem.append(rect(STEPS[4][0] + 30, SY - 75, 45, 40, 0.82, 6))

LABELS = [   # the map, named: [beat in, beat out, text, anchor fx, fy, the pin's push there, which side the label sits]
    [10.6, 19.6, "STEPS", STEPS[0][0], SY - SH / 2, 0.62, -1],
    [11.6, 19.6, "HANDOFFS", 525, SY, 0.34, 1],
    [12.6, 19.6, "DELAYS", DELAY[0], DELAY[1] + DELAY[2], 0.52, 1],
    [13.6, 19.6, "REWORK", 720, 180, 0.44, -1],
]

# ---------------- the paths. Each is a mould pressed onto the front: no pin can stay further out than the mould allows.
# cap marks say how much the mould cuts off; fit=True means the mould starts as the exact negative of the problem
PATHS = [
    {"name": "PATH 1", "fit": False, "cap": [full(0.88), rect(70, 380, 470, 180, 0.30, 12)]},
    {"name": "PATH 2", "fit": True, "cap": [rect(300, 150, 830, 120, 0.86, 30), circ(DELAY[0], DELAY[1], DELAY[2] + 18, 0, 0.82)]},
    {"name": "PATH 3", "fit": True, "cap": []},
]
CHECKS = ["PRICE", "SETUP", "INTEGRATIONS", "PRIVACY", "MAINTENANCE", "REVERSIBILITY"]

# ---------------- the test, the owner and the measure
cal = []; DAYS = []
CW, CH, CG = 112, 96, 18; CX0, CY0 = 120, 120
for d in range(30):
    c, r = d % 6, d // 6
    x, y = CX0 + c * (CW + CG), CY0 + r * (CH + CG)
    cal.append(frame(x, y, CW, CH, 14, 0.24, 10)); DAYS.append((x, y))
owner = [circ(1185, 190, 66, 0, 0.95), arc(1185, 420, 118, 120, 180, 360, 0, 0.8)]   # a person: a head, a gap for the neck, shoulders
target = [circ(1185, 610, 92, 20, 0.6), circ(1185, 610, 52, 18, 0.75), circ(1185, 610, 16, 0, 0.95)]

# ---------------- the brief
brief = [frame(330, 70, 780, 660, 26, 0.5, 18), rect(400, 140, 420, 56, 0.95, 8)]
for k in range(5): brief.append(rect(400, 250 + k * 64, 640 * (0.95 if k % 3 else 0.72), 22, 0.5, 6))
brief += [circ(960, 610, 70, 18, 0.85), line(925, 612, 952, 640, 16, 0.85), line(952, 640, 1000, 585, 16, 0.85)]

SHAPES = {"problem": problem, "cal": cal, "owner": owner, "target": target, "brief": brief}
for i in range(30): SHAPES["day%d" % i] = [rect(DAYS[i][0] + 12, DAYS[i][1] + 12, CW - 24, CH - 24, 0.62, 6)]
for i, p in enumerate(PATHS): SHAPES["cap%d" % i] = p["cap"] or [full(0)]

# ---------------- events, in order. Each one acts on every pin with a weight that rises from 0 to 1 over [t0, t1] (plus the pin's own
# delay) and then stays: "back" pushes pins out to a shape and they stay there; "front" presses a mould on and pushes back whatever
# sticks out past it; "tilt" and "flat" send every pin home. delay: "x" left to right, "y" top down, "r" from the middle, "n" scattered
EV = []
def ev(kind, shape=None, t0=0, t1=1, delay="n", spread=0.0, **kw):
    EV.append(dict(kind=kind, shape=shape, t0=t0, t1=t1, delay=delay, spread=spread, **kw))

ev("back", "problem", 3.0, 4.6, "r", 1.4)
P0 = [24.0, 28.8, 33.6]
for i, b in enumerate(P0):
    # the mould comes down over a beat, holds while it's checked, lifts; where it pushed pins back they glow amber until the problem
    # is pressed back in from behind
    ev("front", "cap%d" % i, b, b + 1.0, "x", 0.5, path=i, fit=PATHS[i]["fit"], lift=(b + 3.4 if i < 2 else 40.3), restore=(b + 3.9 if i < 2 else None))  # the fit holds through the recommendation
    if i < 2: ev("back", "problem", b + 3.9, b + 4.5, "r", 0.3, restore=True)
TILT = [41.0, 44.2]            # the frame tips back, every pin slides home, the frame comes back up
ev("tilt", None, 41.6, 42.4, "y", 1.2)
ev("back", "cal", 44.6, 45.4, "x", 0.5)
DAY0, DSTEP = 45.4, 0.17
for i in range(30): ev("back", "day%d" % i, DAY0 + i * DSTEP, DAY0 + i * DSTEP + 0.2, "r", 0.05, day=i)
ev("back", "owner", 48.0, 48.6, "r", 0.3)
ev("back", "target", 48.9, 49.5, "r", 0.3)
ev("flat", None, 51.0, 51.35, "n", 0.25)
ev("back", "brief", 52.0, 53.2, "y", 0.9)

# ---------------- the words, flat, along the top
CAPS = [
    ("ONE PROBLEM.", 2.4, 5.8),
    ("TAKEN AS IT IS.", 6.0, 9.6),
    ("MAPPED BEFORE ANYTHING IS BOUGHT.", 14.2, 19.6),
    ("UP TO THREE PATHS.", 20.0, 23.6),
    ("WHERE IT DOESN'T FIT, THE PINS MOVE.", 24.0, 28.4),
    ("CHECKED, NOT GUESSED.", 28.8, 33.2),
    ("ONE RECOMMENDATION.", 37.0, 39.0),
    ("EVEN IF IT'S NO CHANGE.", 39.2, 41.4),
    ("A 30-DAY TEST.", 45.0, 47.6),
    ("AN OWNER. ONE MEASURE OF SUCCESS.", 47.8, 51.0),
    ("THE DECISION BRIEF.", 52.4, 54.8),
    ("WITHIN FIVE BUSINESS DAYS.", 55.0, 57.4),
    ("NO CODE WRITTEN. NOTHING CONNECTED.", 57.6, 60.2),
]
KINDS = [20.6, "A READY-MADE TOOL · A CONNECTED WORKFLOW · A SIMPLER PROCESS", 23.6]

# ---------------- the camera: [beat, eye x, y, z, target x, y, z, fov]. World: x right, y up, z out of the plate, the field centred
CAM = [
    [0.0, 1180, 120, 760, 40, -10, 0, 30],
    [9.0, 1060, 160, 860, 20, -10, 0, 30],
    [10.4, -980, 60, 520, -420, -40, 10, 30],
    [19.4, 980, 80, 560, 380, -40, 10, 30],
    [20.4, -1000, 340, 1300, 440, -40, 0, 30],
    [36.2, -930, 320, 1230, 440, -40, 0, 30],
    [40.6, -700, 220, 1020, 330, -40, 10, 30],
    [41.2, 1350, 520, 1500, 0, -60, 0, 30],
    [44.2, 1250, 480, 1450, 0, -60, 0, 30],
    [44.8, -760, 420, 1480, 80, -20, 0, 30],
    [50.8, -660, 380, 1440, 80, -20, 0, 30],
    [51.6, -260, -180, 1650, 0, -10, 0, 30],
    [64.0, -160, -140, 1600, 0, -10, 0, 30],
]
LIGHT = {"on": 0.6, "off": [59.6, 60.4], "key": [-0.55, 0.62, 0.56], "rim": [0.8, 0.2, -0.55]}
LOGO = 60.6

table = {
    "w": W, "h": H, "bpm": BPM, "beat": BEAT, "beats": BEATS, "dur": round(BEATS * BEAT, 4),
    "nx": NX, "ny": NY, "pitch": PITCH, "fw": FW, "fh": FH, "ext": EXT, "len": LEN,
    "shapes": SHAPES, "paths": [{"name": p["name"], "fit": p["fit"]} for p in PATHS], "checks": CHECKS, "ev": EV,
    "tilt": TILT, "labels": LABELS, "caps": CAPS, "kinds": KINDS, "cam": CAM, "light": LIGHT, "logo": LOGO,
    "label": "AI PROBLEM-TO-SOLUTION ASSESSMENT · DEMO WORKFLOW",
}
os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE=" + json.dumps(table, separators=(",", ":"), ensure_ascii=False) + ";")
print("dur", table["dur"], "events", len(EV), "pins", NX * NY)
