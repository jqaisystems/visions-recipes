"""The one table for R54 alternative · Register, read by the film and by score/compose.py: the beat grid, every scene, every slam,
every plate locking into register, and the words. The sources, the field and the briefing are a demo.
Writes assets/table.js (not committed).  Usage: python bake/table.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1920, 1080
BPM = 120; BEAT = 60 / BPM; BEATS = 74

# ---------------- the scenes, in beats
SC = {
    "dive": [0, 8],        # out of one dot: the camera pulls back from a single cyan dot to the words, and the plates lock
    "flood": [8, 20],      # everything at once: sources slam in on the beat, then the plates drift apart and the noise rises
    "key": [20, 28],       # the key plate: black only, the knowledge document drawn line by line
    "sweep": [28, 38],     # colour back, a roller wipes the noise away, what matters locks into register
    "press": [38, 53],     # a whip down to the press: the web runs and stops on the briefing
    "deal": [53, 63],      # on schedule: sheets dealt onto the days
    "yours": [63, 72],     # the folder, the plates fanned apart, an ink flood
}
LOGO = 69.4

# kinetic words: [beat in, beat out, text, plate mix c,m,y,k, where]
WORDS = [
    [1.0, 7.6, "YOUR", [0, 0, 0, 1], "dive1"], [1.0, 7.6, "SOURCES.", [1, 0.85, 0, 0], "dive2"],
    [8.0, 10.0, "NEWS.", [0, 0, 0, 1], "slam"], [10.0, 12.0, "SITES.", [0, 0, 0, 1], "slam"],
    [12.0, 14.0, "FEEDS.", [0, 0, 0, 1], "slam"], [14.0, 19.6, "COMPETITORS.", [0, 0, 0, 1], "slam"],
    [20.6, 24.0, "BRIEFED ON|YOUR FIELD.", [0, 0, 0, 1], "left"], [24.0, 27.8, "IT READS|THIS FIRST.", [0, 0, 0, 1], "left"],
    [28.6, 34.6, "ONLY WHAT|MATTERS.", [0, 0, 0, 1], "top"], [34.6, 37.8, "WHAT CHANGED,|AND WHY.", [0, 0, 0, 1], "top"],
    [43.5, 47.8, "IN YOUR FORMAT.", [0, 1, 0.1, 0], "band"], [47.8, 52.6, "IN YOUR VOICE.", [0, 1, 0.1, 0], "band"],
    [53.2, 57.8, "DAILY", [0, 0, 0, 1], "deal"], [57.8, 59.8, "OR WEEKLY.", [0, 0, 0, 1], "deal"], [59.8, 62.8, "ON YOUR RHYTHM.", [0, 0, 0, 1], "deal"],
    [63.2, 65.2, "THE CODE.|THE PROMPTS.", [0, 0, 0, 1], "yours"], [65.2, 68.0, "THE KNOWLEDGE|DOCUMENT. YOURS.", [0, 0, 0, 1], "yours"],
]
SLAMS = [8, 9, 10, 11, 12, 13, 14, 15]                 # tiles and words landing in the flood
LOCKS = [6.0, 33.0, 34.0, 35.0, 42.0]                  # plates snapping into register
WHOOSH = [20.0, 38.0, 53.0, 67.0]                      # whips and collapses
SWEEP = [29.0, 32.0]                                   # the roller crossing the sheet
PRESS = {"run": [38.4, 42.0], "pages": 7}              # the web running, slowing to a stop on the briefing
DEALS = [54.0, 54.5, 55.0, 55.5, 56.0, 56.5, 57.0]     # daily: a sheet onto each day
WEEKLY = 58.5                                          # weekly: one sheet, heavier
FAN = [67.0, 67.8]; FLOOD = [68.0, 69.0]
BRIEF = {
    "head": "THIS WEEK, IN BRIEF",
    "items": [["A NEW SAFETY STANDARD, DRAFTED", "WHY: IT COVERS TWO OF YOUR ROUTES"],
              ["A RIVAL REWROTE ITS SERVICE PAGE", "WHY: IT NOW TARGETS YOUR REGION"],
              ["TWO NEW TENDERS NEARBY", "WHY: BOTH CLOSE THIS MONTH"]],
    "lines": [43.0, 44.0, 45.0, 46.0],                 # masthead, then each item typesets on the beat
}

table = {
    "w": W, "h": H, "bpm": BPM, "beat": BEAT, "beats": BEATS, "dur": BEATS * BEAT, "logo": LOGO,
    "sc": SC, "words": WORDS, "slams": SLAMS, "locks": LOCKS, "whoosh": WHOOSH, "sweep": SWEEP, "press": PRESS,
    "deals": DEALS, "weekly": WEEKLY, "fan": FAN, "flood": FLOOD, "brief": BRIEF,
    "label": "AI RESEARCH & BRIEFING SYSTEMS · DEMO BRIEFING",
}
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE=" + json.dumps(table, separators=(",", ":"), ensure_ascii=False) + ";")
print("dur", table["dur"], "words", len(WORDS))
