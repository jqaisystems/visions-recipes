"""R18 · Loom. The one table: every source thread, the headlines that flicker past, the rules punched into the card,
every pick of the loom, and the three stories of the briefing. Seeded, so the film and the score always agree.
Writes ../assets/loom.js (window.TABLE, for the film) and loom.json (for score/compose.py).
Usage: python bake/loom.py"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
rnd = random.Random(18)

# ---- when things happen (seconds)
T = {
    "stream": [0.3, 3.6],          # the sources arrive as threads of light
    "card": 4.2,                   # the knowledge card slides into the loom
    "read": 7.3,                   # the loom reads the card, before it reads the news
    "cords": 7.6,                  # the card's cords drop to every thread
    "weave": 8.4,                  # the shed opens
    "reject": [9.0, 12.4],         # the threads the card doesn't lift fall away
    "fast": 14.0,                  # the loom runs at double time
    "full": 19.2,                  # the briefing is woven
    "resolve": [15.6, 18.4],       # its type comes through the weave
    "clock": 20.6,                 # the clock swings in
    "nine": 22.4,                  # Monday, 09:00
    "cut": 22.6,                   # the cloth is cut
    "fold": [22.9, 23.5, 24.0],    # folded twice
    "slide": [24.0, 25.0],         # to the table, before the meeting
    "clockOut": 23.9,
    "stack": [26.0, 28.0],         # every Monday
    "word": [28.3, 29.9],          # the threads gather into the word
    "end": 29.6,
}
BEAT = 0.625                       # 96 bpm: the loom is the beat

# ---- the warp: 212 sources; 9 the card lifts, in three groups of three (one group per story)
N = 212
WX = [-4.2 + 8.4 * i / (N - 1) for i in range(N)]
STORY_X = [2.8, 0.0, -2.8]         # +x reads left from the reading camera (it looks along +z)
kept = {}
for c, cx in enumerate(STORY_X):
    for off in (-0.3, 0.0, 0.3):
        i = min(range(N), key=lambda k: abs(WX[k] - (cx + off)))
        kept[i] = c
rejects = sorted(rnd.uniform(*T["reject"]) for _ in range(N - len(kept)))
rnd.shuffle(rejects)
threads, ri = [], 0
for i in range(N):
    # each thread comes in from the dark: a point on a wide shell behind and around the loom
    az = rnd.uniform(-1.2, 1.2) * math.pi * 0.5 + math.pi
    el = rnd.uniform(0.05, 0.85)
    rad = rnd.uniform(24, 40)
    start = [round(rad * math.cos(el) * math.sin(az), 3), round(2 + rad * math.sin(el), 3), round(-6 + rad * math.cos(el) * math.cos(az), 3)]
    arrive = round(T["stream"][0] + (T["stream"][1] - T["stream"][0] - 1.3) * rnd.random() ** 0.8, 3)
    th = {"x": round(WX[i], 4), "start": start, "arrive": arrive, "story": kept.get(i, -1)}
    if i not in kept:
        th["reject"] = round(rejects[ri], 3)
        ri += 1
    threads.append(th)

# ---- headlines that flicker past in the stream: made up; three matter, four are noise
HEADLINES = [
    ("Tender opens for a three-year contract", True),
    ("Five trends you can't ignore", False),
    ("A competitor cuts its entry price", True),
    ("We're thrilled to announce…", False),
    ("Draft rules on customer data", True),
    ("The same story, fourth outlet", False),
    ("Sponsored: the future is now", False),
]
headlines = []
for k, (text, signal) in enumerate(HEADLINES):
    t0 = round(0.5 + 0.42 * k, 3)
    side = -1 if k % 2 == 0 else 1
    pos = [round(side * rnd.uniform(3.2, 6.4), 3), round(rnd.uniform(5.8, 9.4), 3), round(rnd.uniform(-10, -5), 3)]
    headlines.append({"text": text, "signal": signal, "t0": t0, "t1": round(t0 + 1.7, 3), "pos": pos})

# ---- the knowledge card: what you know, punched in one hole at a time (and read before the news)
RULES = ["our market", "our clients", "competitors", "regulation", "tenders", "no press releases", "no duplicates", "always the why"]
rules = [{"label": lab, "t": round(5.0 + 0.3 * k, 3), "col": k % 4, "row": k // 4} for k, lab in enumerate(RULES)]

# ---- every pick: on the beat from the shed opening, double time after T.fast, until the briefing is woven;
#      after the cut the loom starts next week's cloth
picks, t = [], 8.6
while t <= T["full"] + 1e-6:
    picks.append(round(t, 4))
    t += BEAT if t < T["fast"] - 1e-6 else BEAT / 2
picks2, t = [], 23.2
while t <= 28.4:
    picks2.append(round(t, 4))
    t += BEAT

# ---- the briefing: three stories, each from its group of three threads (made up)
stories = [
    {"title": "A tender opens", "body": "The city opens a tender for a three-year design contract.", "why": "It fits our team, and it closes on 14 November."},
    {"title": "A rival cuts prices", "body": "A competitor lowered its entry plan by 15% this week.", "why": "Two of our renewals are due this month."},
    {"title": "New rules on data", "body": "Draft guidance on customer data is open for comment.", "why": "Our sign-up form needs a review before it lands."},
]

table = {"T": T, "beat": BEAT, "threads": threads, "headlines": headlines, "rules": rules, "picks": picks, "picks2": picks2, "stories": stories}
with open(os.path.join(HERE, "..", "assets", "loom.js"), "w", encoding="utf-8", newline="\n") as f:
    f.write("window.TABLE = " + json.dumps(table, ensure_ascii=False) + ";\n")
with open(os.path.join(HERE, "loom.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(table, f, ensure_ascii=False, indent=1)
print("threads", N, "kept", len(kept), "picks", len(picks), "+", len(picks2))
