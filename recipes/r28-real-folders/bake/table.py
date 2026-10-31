"""The one table for R28 Real Folders: the clock of every scene on a 108 bpm grid, the shutters, the flood of captures
and the folder each one is filed in, the search and its matches, the markup and the solid-pixel redaction, the
client-ready backdrop and the screen recording. The film reads assets/table.js, the score reads bake/table.json.
Usage: python bake/table.py  (or --vertical <project> for the 9:16 cut's table)"""
import json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERT = "--vertical" in sys.argv
OUTDIR = sys.argv[sys.argv.index("--vertical") + 1] if VERT else ROOT
FPS, BPM, DUR = 30, 108, 32.0
BEAT = 60 / BPM                                   # 0.5556 s
q = lambda b: round(b * BEAT, 4)                  # beat number to seconds
hsh = lambda n: (math.sin(n * 127.1 + 311.7) * 43758.5453) % 1.0

T = {
    "shutter": [0.0, q(7)],        # a desktop, the capture overlay, the loupe, a selection, the first shutter
    "flood": [q(7), q(16)],        # captures on the beat, then a city of folders rises and every card is filed
    "search": [q(16), q(27)],      # "invoice" types, a scan crosses the city, the words lift, the matches rise
    "mark": [q(27), q(38)],        # one card: an arrow, a box, step badges, an email snapped into solid pixels
    "ready": [q(38), q(49)],       # the backdrop floods into the gradient; then the card becomes a screen recording
    "title": q(49),
    "end": DUR,
}

# ---------------- I · the shutter
overlay = q(1)                                    # the scrim and crosshair drop in
drag = [q(2.5), q(4.5)]                           # the selection drags out
shot0 = q(5)                                      # the first shutter
lift = [q(5), q(6.5)]                             # the selection lifts off as a card

# ---------------- II · a flood of captures, filed into folders
PROJECTS = ["Bug Reports", "Invoices", "Site QA", "Pitch Deck", "Lumen Rebrand", "Onboarding",
            "Moodboard", "Receipts", "Wireframes", "Press Kit", "Client Notes", "Tutorials"]
GX, GY = 4, 3                                     # the city: four folders across, three deep
folders = []
for k, name in enumerate(PROJECTS):
    gx, gy = k % GX, k // GX
    folders.append({"name": name, "gx": gx * 1.55, "gy": gy * 1.35, "h": round(0.34 + 0.22 * hsh(k * 2.1), 3),
                    "rise": round(q(12) + 0.06 * (gx + gy) + 0.05 * hsh(k), 4)})
NC = 36
shots = [round(q(7) + (q(11.5) - q(7)) * math.sqrt(k / NC), 4) for k in range(NC)]   # faster and faster
tilt = [q(11.25), q(12.75)]                       # the camera tilts into the isometric city
file_ = [q(13), q(15.5)]                          # every card flies into its folder
WORDS = ["brief", "palette", "hero", "header", "logo", "footer", "pricing", "draft", "review", "notes", "menu", "grid",
         "login", "error", "chart", "slide", "quote", "terms", "photo", "layout", "button", "cover", "sketch", "order"]
MATCH = {3: 1, 11: 7, 17: 10, 26: 4}               # the four cards with "invoice" in them, and the folder each is in
cards = []
for k in range(NC):
    f = MATCH[k] if k in MATCH else int(hsh(k * 3.7) * len(PROJECTS))
    cards.append({"t": shots[k], "x": round(140 + hsh(k * 1.3) * 1640, 1), "y": round(150 + hsh(k * 2.9) * 700, 1),
                  "rot": round((hsh(k * 4.1) - 0.5) * 16, 2), "f": f, "kind": 4 if k in MATCH else int(hsh(k * 5.3) * 4),
                  "match": k in MATCH, "words": (["invoice"] if k in MATCH else []) + [WORDS[(k * 7 + j * 5) % len(WORDS)] for j in range(2)],
                  "file": round(file_[0] + (file_[1] - file_[0] - 0.5) * hsh(k * 6.1), 4)})

# ---------------- III · found by its words
QUERY = "invoice"
type_ = [q(17), q(18.5)]
scan = [q(18.75), q(21.5)]                        # the scan crosses the city, back to front
rise = [q(21.75 + 0.5 * j) for j in range(len(MATCH))]   # each match rises out of its folder, on the half beat
dive = [q(25.25), q(27)]                          # into the first match

# ---------------- IV · marked up and redacted
arrow = [q(28.5), q(29.5)]
box = [q(30), q(31)]
badges = [q(29.5), q(31)]
redact = [q(32.5), q(35)]                         # the email snaps into solid pixels, square by square
mark_out = [q(37), q(38)]

# ---------------- V · client-ready, then a screen recording
flood_bg = [q(38.5), q(40)]                       # the backdrop floods into the gradient
face = [q(38.5), q(40.5)]                         # the card turns to face the camera
rec = [q(43), q(48.5)]                            # REC, a timer, and a strip of frames unrolling
frames = [round(q(43.5) + k * BEAT * 0.5, 4) for k in range(9)]

# ---------------- VI · title
sel = [q(49.5), q(50.75)]                         # the overlay selects the empty centre
shot1 = q(51)                                     # the last shutter: the logo
line = q(52)

impacts = [shot0, shot1]
table = {"fps": FPS, "beat": BEAT, "bpm": BPM, "dur": DUR, "T": T, "overlay": overlay, "drag": drag, "shot0": shot0,
         "lift": lift, "folders": folders, "shots": shots, "tilt": tilt, "file": file_, "cards": cards, "matches": sorted(MATCH), "query": QUERY,
         "type": type_, "scan": scan, "rise": rise, "dive": dive, "arrow": arrow, "box": box, "badges": badges,
         "redact": redact, "mark_out": mark_out, "flood_bg": flood_bg, "face": face, "rec": rec, "frames": frames,
         "sel": sel, "shot1": shot1, "line": line, "impacts": impacts, "vert": VERT}
os.makedirs(os.path.join(OUTDIR, "assets"), exist_ok=True)
open(os.path.join(OUTDIR, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE = " + json.dumps(table, ensure_ascii=False) + ";\n")
if not VERT:
    json.dump(table, open(os.path.join(ROOT, "bake", "table.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(json.dumps(T)); print("shots", shots[0], shots[-1], "rise", rise, "shot1", shot1)
