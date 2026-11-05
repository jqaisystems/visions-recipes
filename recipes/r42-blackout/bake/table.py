"""R42 · Blackout: the one baked table the film and the score read.
100 bpm, 56 beats. Sections in beats: log 0-10, soak 10-20, observe 20-28, approve 28-40, wash 40-50, close 50-56.
Everything in the log is fictional demo data.  Writes bake/table.json and assets/table.js.  Usage: python bake/table.py"""
import json, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BPM = 100; BEAT = 60 / BPM
rng = random.Random(41)
P = "/home/demo/clients/harbour-cafe"
TEMPLATES = [
    ("prompt", '"rewrite the pricing page, use last year\'s margins"'),
    ("prompt", '"why did the renewal fall through in march?"'),
    ("prompt", '"draft the apology to the landlord, keep it short"'),
    ("tool.read", P + "/contracts/renewal-draft.pdf"),
    ("tool.read", P + "/finance/margins-2026.xlsx"),
    ("tool.read", P + "/notes/call-with-owner.md"),
    ("output", '"the renewal is 4,200 a month, they asked for 10% off"'),
    ("output", '"the landlord raised the deposit twice this year"'),
    ("tool.shell", "export API_TOKEN=demo-0000-0000-0000-0000"),
    ("tool.shell", "cat " + P + "/.env | grep PAYKEY_DEMO"),
    ("tool.edit", P + "/site/pricing.html  +42 -17"),
    ("tool.edit", P + "/site/menu.json  +8 -3"),
    ("session.start", "workspace " + P + "/brand-refresh"),
]
N = 90
lines, sec = [], 9 * 3600 + 41 * 60
for i in range(N):
    ev, pay = TEMPLATES[0] if i == 0 else rng.choice(TEMPLATES)
    sec += rng.randint(1, 9)
    lines.append([f"{sec // 3600:02d}:{sec % 3600 // 60:02d}:{sec % 60:02d}", ev, pay])
ROWS = 21
vis = lines[-ROWS:]
types = []
for _, ev, _p in vis:
    if ev not in types: types.append(ev)
order = list(range(ROWS)); rng.shuffle(order)
bursts = []   # the bars land in six bursts, on the half beat
for k in range(6):
    bursts.append({"b": 10 + k * 0.5, "rows": order[k * ROWS // 6:(k + 1) * ROWS // 6]})

table = {
    "dur": round(56 * BEAT, 4), "beat": round(BEAT, 6), "bpm": BPM, "lines": lines, "rows": ROWS, "types": types, "bursts": bursts,
    "big": [["EVERY", 6], ["SESSION", 7], ["LEAVES", 8], ["A TRAIL", 9]],
    "tasks": ["Structure review", "Documentation gaps", "Security review"],
    "private": ["CREDENTIALS", "RAW SESSIONS", "LOGS", "LOCAL PATHS", "DATABASES"],
    "keep": ["source code", "fake fixtures", "safety docs", "public demo"],
    "workspaces": ["workspace · a1f3", "workspace · 7c02", "workspace · e94b"],
    "name": "Codex Control Center", "url": "ai.joaoqueiros.com", "status": "OPEN SOURCE · MIT",
}
json.dump(table, open(os.path.join(ROOT, "bake", "table.json"), "w", encoding="utf-8"), ensure_ascii=False)
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE = " + json.dumps(table, ensure_ascii=False) + ";\n")
print("dur", table["dur"], "types", types)
