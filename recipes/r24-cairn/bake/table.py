"""The one table for R24 Cairn: the clock of every scene, the beat grid (84 bpm), the moments each stone lands, the
checkpoint stamps, the impact frames and the smear frames. The film reads assets/table.js, the score reads
bake/table.json. Usage: python bake/table.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS, BPM, DUR = 30, 84, 32.0
BEAT = 60 / BPM                                   # 0.714 s
q = lambda b: round(b * BEAT, 4)                  # beat number to seconds

T = {
    "open": [0.0, q(5)],          # a ridge at night in fog; forty numbers hail down and blow away, three stay
    "gust": q(3.5),
    "first": [q(5), q(13)],       # the camera tilts up into the cloud; the first stone falls and lands
    "weeks": [q(13), q(25)],      # time-lapse: the sun swings over, a stone lands at week 4 and at week 8
    "check": [q(25), q(34)],      # the real checkpoint's decisions slam in as lettering
    "summit": [q(34), q(39)],     # the last stones drop on the beat; the sun breaks; the camera cranes up
    "title": q(39),
    "end": DUR,
}
# stone k lands at lands[k]; the stones are the mark's six, bottom first
lands = [q(7), q(18), q(23), q(34.5), q(35.5), q(36.5)]
falls = [0.62, 0.5, 0.5, 0.42, 0.38, 0.38]        # seconds in the air before each landing
ranks = [{"t": lands[0] + 0.9, "pos": 18, "label": "START"}, {"t": lands[1] + 0.25, "pos": 9, "label": "WEEK 4"},
         {"t": lands[2] + 0.25, "pos": 3, "label": "WEEK 8"}]
# the checkpoint: four real decisions from CP-03, one on each beat pair
stamps = [{"t": q(26 + 2 * k), "word": w, "note": n} for k, (w, n) in enumerate([
    ("GO", "buyer searches"), ("NO-GO", "film batch 2"), ("VOID", "email sign-up read"), ("CLOSED", "indexing watches")])]
line = q(32.5)
NUMBERS = ["CTR 2.1%", "+12%", "Bounce 61%", "Score 87", "1,204 keywords", "Health 92", "+340 links", "Avg pos 23.4",
           "Sessions 3,118", "Visibility 4.2%", "Speed 71", "-8%", "Errors 214", "Load 2.8s", "Pages 695", "Words 1,880",
           "Mobile 64", "Dwell 0:42", "Imp. 18.3k", "Tags 41", "+0.4", "Rank 31", "Alt 77%", "H1 x3", "LCP 3.1s", "CLS 0.19",
           "Links 9,410", "Uptime 99.2", "Refs 58", "Crawl 12k", "-23", "Anchors 61%", "Redirects 38", "TTFB 0.9s",
           "Images 402", "Volume 2.4k", "KD 47", "+5 pts", "Grade B", "Trust 33"]
assert len(NUMBERS) == 40
THREE = ["01  INDEXED", "02  BUYER SEARCHES", "03  ENQUIRIES"]

impacts = [{"t": lands[0], "n": 3}, {"t": lands[1], "n": 2}, {"t": lands[2], "n": 2}]
impacts += [{"t": s["t"], "n": 2} for s in stamps]
impacts += [{"t": lands[3], "n": 2}, {"t": lands[4], "n": 2}, {"t": lands[5], "n": 3}]
impacts.sort(key=lambda d: d["t"])

# smear frames: the last two frames of every fall, and the frame of the gust
smears = sorted(set([round(d["t"] * FPS) - j for d in impacts if d["t"] in lands for j in (1, 2)] + [round(T["gust"] * FPS)]))

table = {"fps": FPS, "beat": BEAT, "bpm": BPM, "dur": DUR, "T": T, "lands": lands, "falls": falls, "ranks": ranks,
         "stamps": stamps, "line": line, "numbers": NUMBERS, "three": THREE, "impacts": impacts, "smears": smears}
open(os.path.join(ROOT, "assets", "table.js"), "w").write("window.TABLE = " + json.dumps(table) + ";\n")
json.dump(table, open(os.path.join(ROOT, "bake", "table.json"), "w"), indent=1)
print(json.dumps(T), lands, [s["t"] for s in stamps])
