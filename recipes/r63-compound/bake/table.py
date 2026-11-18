"""The one table for R63 · Compound, read by the film and by score/compose.py: the beat grid, the board and its light, the ring of
nails going in, the light that approves them, the four windings and how fast each lays its passes, the camera and the words. The
board is a demo.  Writes assets/table.js (not committed).  Usage: python bake/table.py  (run bake/wind.py first)"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1920, 1080
BPM = 96; BEAT = 60 / BPM; BEATS = 64

# ---------------- the board: world units, about a pixel each in the wide shot; x right, y up, the nails stand out along +z
NAIL_H = 15.0                  # how far each nail stands out of the board
THREAD_Z = [3.0, 13.0]         # the first pass sits low on the nails, the last one high
LIGHT = [0.55, -0.45, -0.70]   # the way the key light travels: low from the upper left, so every nail throws a long shadow

# ---------------- the nails go in round the ring, clockwise from the top, a mallet on every beat
LAND = [1.2, 8.2]
# ---------------- the approval: one light runs round the ring and every nail ticks
APPROVE = [9.0, 12.0]

# ---------------- the windings. The bone thread's first three passes are a day each, timed by hand; then pass j of n lands at
# 19 + 17 * ((j - 3) / (n - 3)) ** (1 / ease), slow at first and then a rush. The colour threads follow, one after another.
TIE = 13.8                                      # the bone thread ties on
DAYS = [[14.0, 0], [16.0, 1], [17.5, 2], [19.0, 3]]
WIND = [[19.0, 36.0, 2.4], [36.5, 40.5, 1.5], [40.8, 44.2, 1.5], [44.5, 48.0, 1.5]]   # [from, to, ease] for each thread
TALPHA = [1.25, 1.65, 1.65, 1.65]              # each thread's brightness, relative to the bone thread
THICK = [[0, 16.0], [19.5, 16.0], [24.0, 1.0]]    # the first passes are drawn thick enough to follow; the thread thins as it rushes
TIEOFF = 48.4

# ---------------- the words, flat, along the top
CAPS = [
    ("A BATCH OF ON-BRAND PINS.", 1.6, 4.8),
    ("DESIGNED ONCE.", 5.0, 8.4),
    ("YOU APPROVE THE BATCH,", 9.0, 11.2),
    ("NOT EACH POST.", 11.4, 13.4),
    ("ONE PIN, EVERY DAY.", 14.4, 18.0),
    ("NOBODY TOUCHING A SCHEDULER.", 18.4, 22.4),
    ("PINS KEEP SURFACING", 24.6, 28.2),
    ("FOR MONTHS.", 28.4, 31.4),
    ("IT COMPOUNDS.", 32.2, 36.0),
    ("IN YOUR BRAND,", 37.0, 40.8),
    ("ON YOUR ACCOUNTS.", 41.2, 45.0),
    ("YOU OWN THE SYSTEM.", 48.8, 52.4),
    ("AND THE AUDIENCE.", 52.6, 56.4),
]

# ---------------- the camera: [beat, eye x, y, z, target x, y, z, fov]. One more camera blends in on top: it follows the thread's tip
WIDE = [0, 78, 1655, 0, 78, 0, 40]
CAM = [
    [0.0, -300, 170, 300, 70, 430, 0, 40],
    [3.6, -170, -160, 560, 210, 280, 0, 42],
    [8.4, *WIDE],
    [12.6, *WIDE],
    [14.2, -60, -1080, 900, 0, 40, 0, 40],
    [19.4, 110, -980, 980, 0, 50, 0, 40],
    [23.0, 0, 130, 900, 0, 130, 0, 40],
    [34.0, *WIDE],
    [38.5, 230, -330, 1560, 0, 70, 0, 40],
    [43.0, -240, -290, 1580, 0, 70, 0, 40],
    [47.6, *WIDE],
    [49.4, -560, -420, 250, -40, -60, 0, 36],
    [53.0, 330, -460, 300, 140, 60, 0, 36],
    [56.2, *WIDE],
    [64.0, *WIDE],
]
FOLLOW = [[0, 0], [64, 0]]   # how much the tip-following camera has the shot (not used in this cut)
FOLLOW_OFF = [-120, -200, 300, 36]                               # where it sits from the tip, and its lens
LOGO = 57.0

table = {
    "w": W, "h": H, "bpm": BPM, "beat": BEAT, "beats": BEATS, "dur": round(BEATS * BEAT, 4),
    "nailH": NAIL_H, "threadZ": THREAD_Z, "light": LIGHT, "land": LAND, "approve": APPROVE,
    "tie": TIE, "days": DAYS, "wind": WIND, "talpha": TALPHA, "thick": THICK, "tieoff": TIEOFF,
    "caps": CAPS, "cam": CAM, "follow": FOLLOW, "followOff": FOLLOW_OFF, "logo": LOGO,
    "label": "PINTEREST GROWTH AUTOMATION · DEMO BOARD",
}
os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE=" + json.dumps(table, separators=(",", ":"), ensure_ascii=False) + ";")
print("dur", table["dur"])
