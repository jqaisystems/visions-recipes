"""R39 · Echo (season 6, ink feedback): the one baked table the film and the score read.
112 bpm. Sections in beats: open 0-8, prep 8-17, rehearse 17-25, twice 25-34, duet 34-43, debrief 43-52, loop 52-56,
mark 56-63. The ink simulation restarts from paper at three anchors (open, rehearse, duet) so any frame can be
rebuilt from its anchor, deterministically.
Writes bake/table.json and assets/table.js.  Usage: python bake/table.py"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BPM = 112; BEAT = 60 / BPM
b = lambda x: round(x * BEAT, 4)
SEC = {"open": (0, 8), "prep": (8, 17), "rehearse": (17, 25), "twice": (25, 34), "duet": (34, 43), "debrief": (43, 52), "loop": (52, 56)}
T = {k: [b(a), b(z)] for k, (a, z) in SEC.items()}
T["mark"] = b(56)
DUR = b(63)

# two speakers in the duet (beats); never real speech
def env(spans, t):
    v = 0.0
    for a, z in spans:
        a, z = b(a), b(z)
        if a - 0.12 < t < z + 0.25:
            v = max(v, min(1, (t - a + 0.12) / 0.12) * min(1, (z + 0.25 - t) / 0.25) * (0.7 + 0.3 * math.sin(t * 21) * math.sin(t * 6.1)))
    return max(0.0, v)
THEM = [(34.3, 36.6), (38.2, 39.0), (40.2, 42.6)]
YOU = [(36.8, 38.0), (39.1, 40.0)]
ENV = [[round(env(THEM, i / 30), 3), round(env(YOU, i / 30), 3)] for i in range(int(DUR * 30) + 1)]

# the brief's words for a demo discovery call, one per beat
WORDS = ["two-week pilot", "invoice reconciliation", "success criteria", "security review", "audit trail",
         "talking points", "likely objections", "discovery questions"]

table = {
    "dur": DUR, "beat": round(BEAT, 6), "bpm": BPM, "T": T,
    "anchors": [0.0, b(17), b(34)],
    "ridges": [[0.25, b(8.6)], [b(52.2), b(56)]],
    "words": [[b(9 + j), w] for j, w in enumerate(WORDS)],
    # the client's question in rehearsal, the client's objection live: word by word, then the impact
    "question": [[b(18), "how"], [b(18.5), "the export"], [b(19), "is"], [b(19.5), "anonymized,"]],
    "qSmall": "where it is processed, who can access it",
    "qImpact": b(21), "qC": [700, 520],
    "objection": [[b(26), "We cannot send"], [b(27), "financial data"], [b(28), "to an external provider."]],
    "oImpact": b(29), "oC": [1220, 520],
    "settle": b(32.4), "help": b(30.5),
    "env": ENV, "talk": [44, 56],
    "trans": b(40), "arabic": "ما هو الجدول الزمني للمشروع؟", "english": "What is the timeline for the project?",
    "pull": [b(43), b(45.5)],
    "db": [[b(45.5), "score"], [b(46.6), "Two-week pilot on one entity"], [b(47.4), "Security review is their gating step"], [b(48.3), "follow-up email · drafted"]],
    "cuts": [b(8), b(17), b(25), b(34), b(43), b(52), b(56)],
    "lines": [
        [b(1.2), b(7.8), "Every big <em>conversation</em>,"],
        [b(9.0), b(16.8), "researched before the <em>call</em>,"],
        [b(17.6), b(24.8), "<em>rehearsed</em> out loud,"],
        [b(29.2), b(33.8), "so the hard moment happens <em>twice</em>."],
        [b(34.6), b(42.8), "Both sides, transcribed on your <em>computer</em>."],
        [b(43.6), b(51.8), "Then an honest <em>debrief</em>,"],
        [b(52.4), b(55.8), "and the prep for the <em>next</em> one."],
    ],
    "rail": [[0, "PREPARE"], [b(17), "REHEARSE"], [b(25), "LIVE"], [b(43), "DEBRIEF"], [b(52), "PREPARE"]],
    "hud": [[0, "a conversation, as ink"], [b(8), "the brief"], [b(17), "mock session"], [b(25), "the real call"],
            [b(34), "both sides · transcribed locally"], [b(43), "after the call"], [b(52), "the next one"]],
    "line": b(57.4),
    "claim": "Every big conversation, <em>rehearsed</em> before it happens.",
    "url": "klatea.joaoqueiros.com", "beta": "Free Windows beta",
}
json.dump(table, open(os.path.join(ROOT, "bake", "table.json"), "w", encoding="utf-8"), ensure_ascii=False)
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE = " + json.dumps(table, ensure_ascii=False) + ";\n")
print("dur", DUR, "beat", round(BEAT, 4), T)
