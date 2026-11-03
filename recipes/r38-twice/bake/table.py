"""R38 · Twice: the one baked table the film and the score read.
88 bpm. Sections in beats: open 0-7, rehearse 7-16, twice 16-26, sides 26-34, debrief 34-42, loop 42-46, title 46-49,
mark 49-52. Frame coordinates are in the 1600x900 frames of bake/prep.py (see frames.json).
Writes bake/table.json and assets/table.js.  Usage: python bake/table.py"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FR = json.load(open(os.path.join(ROOT, "bake", "frames.json"), encoding="utf-8"))
BPM = 88; BEAT = 60 / BPM
b = lambda x: round(x * BEAT, 4)
SEC = {"open": (0, 7), "rehearse": (7, 16), "twice": (16, 26), "sides": (26, 34), "debrief": (34, 42), "loop": (42, 46)}
T = {k: [b(a), b(z)] for k, (a, z) in SEC.items()}
T["title"] = b(46); T["mark"] = b(49)
DUR = b(52)
sh = FR["shots"]

# two speakers, as envelopes (beats): who is talking during the live section; never real speech
def env(spans, t):
    v = 0.0
    for a, z in spans:
        a, z = b(a), b(z)
        if a - 0.15 < t < z + 0.3: v = max(v, min(1, (t - a + 0.15) / 0.15) * min(1, (z + 0.3 - t) / 0.3) * (0.75 + 0.25 * math.sin(t * 19) * math.sin(t * 7.3)))
    return max(0.0, v)
THEM = [(26.3, 28.2), (29.4, 30.0), (31.6, 33.6)]
YOU = [(28.4, 29.3), (30.2, 31.4)]
ENV = [[round(env(THEM, i / 30), 3), round(env(YOU, i / 30), 3)] for i in range(int(DUR * 30) + 1)]

table = {
    "dur": DUR, "beat": round(BEAT, 6), "bpm": BPM, "n": FR["n"], "fw": FR["w"], "fh": FR["h"], "shots": sh, "T": T,
    # the window the screens sit in, on paper
    "R": [200, 108, 1520, 855],
    # I · the prep form plays, a slit sweeps and the brief writes out of it
    "sweep": [b(1.5), b(4.5)],
    # II · the role-play: a scan brings it in, the client's question is cut out of time and held
    "scanIn": [b(7), b(8.5)], "hold": b(10.5), "holdK": sh["roleplay"][0],
    "bubbleR": [32, 306, 1228, 110],            # the client's question in the role-play frame
    "feedbackY": 436,
    # III · twice: two windows, the same objection on the same beat, then the slit sweeps and it all goes live
    "split": [b(16), b(17)], "both": b(18), "sweep2": [b(21), b(23)], "help": b(23.5),
    "liveBubbleR": [44, 368, 592, 64],            # "We cannot send financial data to an external provider."
    "helpR": [1032, 406, 528, 156],
    "liveK": [sh["live"][0], sh["live"][0] + 3.2],  # before and after the objection lands
    # IV · two sides
    "env": ENV, "meter": [1432, 784], "talk": [44, 56], "trans": b(31.5), "transLabel": "ES → EN · translated on your machine", "arabicR": [44, 472, 478, 134],
    # V · the call as one image, folded into the debrief
    "strip": [b(34), b(36.2)], "fold": [b(36.4), b(37.6)], "unfold": [b(37.8), b(39)],
    "dbItems": [[b(39.4), [405, 150, 187, 58], "8 / 10 · how it went"], [b(40.2), [420, 728, 360, 30], "the gating step, named"],
                [b(40.9), [420, 822, 330, 30], "the decision, kept"]],
    "email": b(41.4),
    # VI · the loop
    "gate": [b(42), b(45.2)], "next": b(45),
    "titleType": [b(46.2), b(48)], "line": b(49.5),
    "cuts": [b(7), b(16), b(26), b(34), b(42), b(46)],
    "lines": [
        [b(0.8), b(6.8), "Every big <em>conversation</em>,"],
        [b(7.4), b(15.8), "<em>rehearsed</em> out loud,"],
        [b(17.2), b(25.8), "before it <em>happens</em>."],
        [b(26.6), b(33.8), "Audio stays on your <em>computer</em>."],
        [b(34.6), b(41.8), "Then an honest <em>debrief</em>,"],
        [b(42.4), b(45.8), "and the prep for the <em>next</em> one."],
    ],
    "rail": [[0, "PREPARE"], [b(7), "REHEARSE"], [b(16), "LIVE"], [b(34), "DEBRIEF"], [b(42), "PREPARE"]],
    "name": "Klatea", "claim": "Every big conversation, rehearsed before it happens.",
    "url": "klatea.joaoqueiros.com", "beta": "Free Windows beta",
}
json.dump(table, open(os.path.join(ROOT, "bake", "table.json"), "w", encoding="utf-8"), ensure_ascii=False)
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE = " + json.dumps(table, ensure_ascii=False) + ";\n")
print("dur", DUR, "beat", round(BEAT, 4), {k: v for k, v in T.items()})
