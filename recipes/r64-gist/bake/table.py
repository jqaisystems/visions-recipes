"""The one table for R64 · Gist, read by the film and by score/compose.py: the beat grid, the board and its light, the nails landing
scattered, the wave that straightens them onto the grid, the theme sweep, the winding of BRIEF, the held last pass and the
reviewer's lamp, the wall of earlier days, the camera and the words. The board and its signals are a demo.
Writes assets/table.js (not committed).  Usage: python bake/table.py  (run bake/wind.py first)"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1920, 1080
BPM = 96; BEAT = 60 / BPM; BEATS = 64

# ---------------- the board: world units, one unit is one pixel in the wide shot; x right, y up, the nails stand out along +z
NAIL_H = 15.0               # how far each nail stands out of the board
THREAD_Z = [4.0, 13.0]      # the first pass sits low on the nails, the last one high
LIGHT = [0.62, -0.42, -0.66]   # the way the key light travels: low from the upper left, so every nail throws a long shadow

# ---------------- scattered: the nails land in eight waves, one on each beat, each well off its place and leaning
WAVES = 8
WAVE0 = 1.0
WAVE_SPREAD = 0.55
SCATTER = [230.0, 0.55]     # how far a nail lands from its place (world units), and how far it may lean (radians)
# ---------------- normalize: a ripple from the centre lifts each nail, carries it to its place on the grid and taps it home
NORM = [8.8, 12.6, 1.1]     # beat the ripple starts, beat the last nail lands, how long each nail takes (beats)
# ---------------- classify: a band of light crosses the board and every head takes its theme's colour
SWEEP = [12.8, 15.6]

# ---------------- the winding: [beat from, beat to, ease]. Pass k of n is laid at from + (to - from) * (k / n) ** (1 / ease)
WIND = [16.0, 40.0, 2.2]
LOOSE = 40.0                # the thread stops one pass short: from here its end hangs from the last nail
LAMP = [42.4, 45.6]         # the reviewer's lamp crosses the board
APPROVE = 45.8              # only then is the last pass laid
# ---------------- archive: the camera pulls back to a wall of earlier days, five across and three down; today is the last
ARCHIVE = [47.4, 55.0]
WALL = [5, 3]
PITCH = [2160, 1320]
DAYS = ["MON", "TUE", "WED", "THU", "FRI"]

# ---------------- the words, flat, along the top
CAPS = [
    ("USEFUL SIGNALS ARRIVE FROM EVERYWHERE.", 1.6, 4.8),
    ("AND SIT IN TABS UNTIL THEY'RE FORGOTTEN.", 5.0, 8.4),
    ("EVERY LINK BECOMES A RECORD.", 9.0, 12.4),
    ("GROUPED BY TOPIC AND DATE.", 12.8, 15.8),
    ("THE LATEST USEFUL ITEMS,", 25.0, 28.6),
    ("IN ONE SHORT DAILY BRIEF.", 28.8, 32.8),
    ("A PERSON DECIDES WHAT EACH ONE BECOMES.", 40.6, 43.8),
    ("NOTHING IS PUBLISHED AUTOMATICALLY.", 44.0, 47.2),
    ("KEPT BY DAY, MONTH AND TOPIC.", 48.4, 51.8),
    ("RESEARCH STARTS FROM MEMORY, NOT OLD TABS.", 52.0, 56.4),
]

# ---------------- the camera: [beat, eye x, y, z, target x, y, z, fov]. Two more cameras blend in on top: one that follows the
# thread's tip, and one that holds on the loose end
WIDE = [0, -40, 1560, 0, -10, 0, 40]
WX, WY = -(WALL[0] - 1) / 2 * PITCH[0], (WALL[1] - 1) / 2 * PITCH[1]      # the middle of the wall, today's board at the origin
CAM = [
    [0.0, -1180, -470, 390, -700, -210, 0, 40],
    [4.5, -600, -520, 440, -160, -160, 0, 44],
    [8.4, *WIDE],
    [12.6, *WIDE],
    [15.4, 0, -620, 1380, 0, -30, 0, 40],
    [16.0, 0, -620, 1380, 0, -30, 0, 40],
    [24.5, *WIDE],
    [30.0, -360, -560, 1300, 0, -20, 0, 40],
    [36.0, 260, -480, 1340, 20, -20, 0, 40],
    [40.0, *WIDE],
    [47.4, *WIDE],
    [55.0, WX, WY - 1500, 9200, WX, WY - 60, 0, 40],
    [64.0, WX, WY - 1500, 9200, WX, WY - 60, 0, 40],
]
FOLLOW = [[0, 0], [16.0, 0], [16.7, 1], [21.5, 1], [24.5, 0]]   # how much the tip-following camera has the shot
FOLLOW_OFF = [-110, -190, 330, 36]                              # where it sits from the tip, and its lens
HOLD = [[0, 0], [40.4, 0], [42.2, 1], [46.4, 1], [47.4, 0]]    # how much the loose-end camera has the shot
HOLD_OFF = [70, -120, 380, 30]
LOGO = 57.0

table = {
    "w": W, "h": H, "bpm": BPM, "beat": BEAT, "beats": BEATS, "dur": round(BEATS * BEAT, 4),
    "nailH": NAIL_H, "threadZ": THREAD_Z, "light": LIGHT,
    "waves": WAVES, "wave0": WAVE0, "waveSpread": WAVE_SPREAD, "scatter": SCATTER, "norm": NORM, "sweep": SWEEP,
    "wind": WIND, "loose": LOOSE, "lamp": LAMP, "approve": APPROVE,
    "archive": ARCHIVE, "wall": WALL, "pitch": PITCH, "days": DAYS, "wallC": [WX, WY],
    "caps": CAPS, "cam": CAM, "follow": FOLLOW, "followOff": FOLLOW_OFF, "hold": HOLD, "holdOff": HOLD_OFF, "logo": LOGO,
    "tags": ["NEWSLETTER", "RELEASE", "DOCS UPDATE", "SAVED LINK", "COMMUNITY NOTE", "SOCIAL POST"],
    "label": "AI NEWS CURATOR · DEMO BOARD",
    "endTitle": "AI News Curator", "endUrl": "ai.joaoqueiros.com/systems/ai-news-curator",
    "endLine": "RESEARCH BRIEFING WORKFLOW · THIS FILM IS CODE",
}
os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE=" + json.dumps(table, separators=(",", ":"), ensure_ascii=False) + ";")
print("dur", table["dur"])
