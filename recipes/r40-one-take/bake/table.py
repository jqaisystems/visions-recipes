"""R40 · One Take: the one baked table the film and the score read.
128 bpm, 72 beats. Sections in beats: dot 0-6, worlds 6-32, drop 32-40, new 40-50, friday 50-62, mark 62-72.
Writes bake/table.json and assets/table.js.  Usage: python bake/table.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BPM = 128; BEAT = 60 / BPM
b = lambda x: round(x * BEAT, 4)

# the twelve places, from the case study's own list with no product names, and each one's length in beats
WORLDS = [["email", 3], ["chat", 3], ["weekly video", 3], ["shared page", 3], ["drive folder", 2], ["files", 2],
          ["feedback", 2], ["time log", 2], ["invoice", 2], ["handover notes", 2], ["commits", 1], ["uploads", 1]]
at = 6; W = []
for name, d in WORLDS:
    W.append({"name": name, "b": at, "d": d}); at += d
assert at == 32

table = {
    "dur": b(72), "beat": round(BEAT, 6), "bpm": BPM, "worlds": W,
    "cards": ["kickoff brief", "asset request list", "first-week plan", "risk list", "tracking sheet"],
    "days": ["MON", "TUE", "WED", "THU"],
    "panes": [
        {"label": "client a · email", "text": "Week 2: kickoff done, drafts due Friday."},
        {"label": "client b · shared page", "text": "Status, files and next step, in one page."},
        {"label": "client c · short video", "text": "The same record, as a short script."},
    ],
    "claim": "A portal that updates itself.", "url": "ai.joaoqueiros.com", "status": "IN DEVELOPMENT",
}
json.dump(table, open(os.path.join(ROOT, "bake", "table.json"), "w", encoding="utf-8"), ensure_ascii=False)
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE = " + json.dumps(table, ensure_ascii=False) + ";\n")
print("dur", table["dur"], "beat", BEAT)
