"""The one table for R59 · Counter, read by the film and by score/compose.py. The film is one unbroken zoom: each scene sits
inside the counter of a letter (the hole in an O, a dial's knob, a full stop) of the scene before, and the camera spirals down
through it. This table holds the beat grid, when each scene arrives and when the camera dives, the turn of each dive, and every
event the music hits: keystrokes, knob moves, strikes, nodes, cards and arrows. The library is a demo.
Writes assets/table.js (not committed).  Usage: python bake/table.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1920, 1080
BPM = 120; BEAT = 60 / BPM; BEATS = 84

# ---------------- the scenes. Each dive: [beat it starts, beat it lands], and how far the next scene is turned inside its counter
DIVES = [[8.5, 11.5], [21.0, 24.0], [33.0, 36.0], [45.0, 48.0], [57.0, 60.0], [68.0, 70.5]]
TURN = [0.0, 1.5708, -1.5708, 0.0, 3.1416, -1.5708]
OPEN = [d[0] - 1.5 for d in DIVES]           # each counter opens onto the next scene's colour a beat and a half before the dive
ARRIVE = [0.0] + [d[1] for d in DIVES]       # when each scene fills the frame
LEAD = 1.5                                   # each scene starts this many beats before it lands, so the dive shows it turning in

# ---------------- scene 0: the prompt, typed
PROMPT = "WRITE IT IN OUR VOICE."
TYPE0, TYPE_STEP = 0.75, 0.25                # first keystroke, and one key every quarter beat
# ---------------- scene 1: the voice spec, three dials. Each knob: [beat (scene time), position 0..1]
KNOBS = [
    [[0.0, 0.5], [3.0, 0.5], [4.0, 0.12], [8.0, 0.12]],     # TONE: plain
    [[0.0, 0.5], [4.0, 0.5], [5.0, 0.3], [8.0, 0.3]],       # RHYTHM: short
    [[0.0, 0.5], [5.0, 0.5], [6.0, 0.08], [8.0, 0.08]],     # VOCABULARY: ours
]
# ---------------- scene 2: the anti-patterns, struck out one per beat
CLICHES = ["IN TODAY'S FAST-PACED WORLD", "A TRUE GAME-CHANGER", "UNLOCK YOUR POTENTIAL", "LET'S DIVE IN",
           "SEAMLESS SYNERGY", "ELEVATE YOUR BRAND", "NOT JUST A TOOL, A JOURNEY", "IN CONCLUSION"]
CL_IN, STRIKE0 = 0.5, 3.0                    # they fly in from this beat, and the strikes start here, one a half beat
# ---------------- scene 3: domain knowledge, a network that grows
NODES = ["THE VOCABULARY", "HOW THE FIELD THINKS", "WHAT EXPERT READS LIKE"]
NODE0 = 1.5
# ---------------- scene 4: the prompt library, twenty cards dealt
KINDS = ["POSTS", "REPORTS", "EMAILS", "BRIEFS", "SUMMARIES"]
DEAL0, DEAL_STEP = 0.5, 0.25
FLIP0 = 6.5
# ---------------- scene 5: a chain, draft then critique then rewrite
CHAIN = [1.0, 3.0, 5.0]                      # when each column takes the sentence
# ---------------- scene 6: the close
CLOSE = [[72.0, "NOT A MAGIC PROMPT."], [74.5, "A LIBRARY YOU OWN."]]
LOGO = 77.5

table = {
    "w": W, "h": H, "bpm": BPM, "beat": BEAT, "beats": BEATS, "dur": round(BEATS * BEAT, 4),
    "dives": DIVES, "turn": TURN, "open": OPEN, "arrive": ARRIVE, "lead": LEAD,
    "prompt": PROMPT, "type0": TYPE0, "typeStep": TYPE_STEP, "knobs": KNOBS,
    "cliches": CLICHES, "clIn": CL_IN, "strike0": STRIKE0, "nodes": NODES, "node0": NODE0,
    "kinds": KINDS, "deal0": DEAL0, "dealStep": DEAL_STEP, "flip0": FLIP0, "chain": CHAIN,
    "close": CLOSE, "logo": LOGO, "label": "PROMPT ENGINEERING · DEMO LIBRARY",
}
os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE=" + json.dumps(table, separators=(",", ":"), ensure_ascii=False) + ";")
print("dur", table["dur"])
