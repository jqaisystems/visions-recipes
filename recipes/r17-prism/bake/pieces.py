"""R17 · Prism. The one table: every piece of content the brief becomes, the phrases the voice blocks, and the month.
Writes ../assets/pieces.js for the film and pieces.json for the score, so every sound lands on what you see.
Usage: python pieces.py   (standard library only, seeded)"""
import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
rng = random.Random(17)

# the spectrum: one ray per colour, from the prism's right face to its piece (the yellow one splits for the languages)
RAYS = [
    dict(colour="#ff4a3d", land=12.3),
    dict(colour="#ff9a2e", land=13.4),
    dict(colour="#ffd84a", land=14.4, split=(7.6, 7.2, 0.0)),
    dict(colour="#46e07e", land=15.9),
    dict(colour="#3ea6ff", land=17.0),
    dict(colour="#a46bff", land=18.0),
]

# every finished piece: which ray it comes from, its format, its text, when it lands, when a person approves it, its day
PIECES = [
    dict(id="post", ray=0, pos=(13.2, 10.6, -0.4), label="POST · SQUARE", w=2.6, h=2.6, approve=19.9, day=3,
         title="We're opening in Porto.", body=["A new studio, a new light.", "Doors open in March."]),
    dict(id="thread", ray=1, pos=(16.9, 10.6, 0.4), label="THREAD · 1 OF 3", w=2.9, h=2.5, approve=20.35, day=6,
         title="", body=["1/ We're opening a studio in Porto. Here's why.", "2/ The city taught us to design slowly.", "3/ Come and see the work in March."]),
    dict(id="en", ray=2, pos=(12.0, 7.0, 0.6), label="NEWSLETTER · EN", w=2.0, h=2.5, approve=20.8, day=9,
         title="Dear friends,", body=["We have news: a new", "studio in Porto, opening", "in March. Come and see."]),
    dict(id="pt", ray=2, pos=(14.4, 7.0, 0.0), label="NEWSLETTER · PT", w=2.0, h=2.5, approve=21.1, day=10,
         title="Caros amigos,", body=["Temos novidades: um", "novo estúdio no Porto,", "abre em março. Venham ver."]),
    dict(id="fr", ray=2, pos=(16.8, 7.0, -0.6), label="NEWSLETTER · FR", w=2.0, h=2.5, approve=21.4, day=11,
         title="Chers amis,", body=["Une nouvelle : un nouveau", "studio à Porto, ouvert", "en mars. Venez voir."]),
    dict(id="blog", ray=3, pos=(18.3, 3.8, -0.4), label="BLOG · DRAFT", w=3.0, h=2.1, approve=21.85, day=14,
         title="Why we chose Porto", body=["Light off the river, streets that climb, and", "a pace that leaves room to think. We came", "for a month and decided to stay."]),
    dict(id="caption", ray=4, pos=(14.3, 3.3, 0.4), label="CAPTION", w=2.8, h=1.2, rewrite=22.3, approve=23.75, day=17,
         title="New light, new city.", title2="Porto, we're here.", body=["#porto #studio"], body2=["Doors open in March."]),
    dict(id="short", ray=5, pos=(12.4, 2.6, 0.0), label="SHORT · 9:16", w=1.35, h=2.4, approve=22.75, day=20,
         title="New studio.", body=["Porto · 0:15"]),
]

# the voice is built first, from the writing you are happy with; these lines lift off the pages as light
PAGES = [
    dict(pos=(-3.6, 7.9, 2.2), rot=(0.0, 18.0, -4.0), lift=1.0, label="EXAMPLE 01 / 08", lines=["Good work takes the time", "it needs. We still draw", "every idea by hand first."]),
    dict(pos=(3.4, 8.6, 1.0), rot=(0.0, -20.0, 5.0), lift=1.35, label="EXAMPLE 04 / 08", lines=["We say less, and mean it.", "No hype, no noise: just", "the work and why it matters."]),
    dict(pos=(2.2, 4.9, 3.8), rot=(0.0, -8.0, 3.0), lift=1.7, label="EXAMPLE 06 / 08", lines=["Write like you talk to", "one person you respect."]),
    dict(pos=(4.6, 6.6, 2.0), rot=(0.0, -16.0, -3.0), lift=2.05, label="EXAMPLE 08 / 08", lines=["Short sentences. Real", "names. Plain words."]),
]

# stock phrases the voice spec blocks: they fly in, hit the glass and break
CLICHES = [
    dict(text="In today's fast-paced world", start=(9.0, 9.4, 3.0), hit=4.7),
    dict(text="game-changer", start=(-9.0, 8.4, 2.4), hit=5.5),
    dict(text="unlock your potential", start=(9.5, 5.2, 2.0), hit=6.3),
    dict(text="Let's dive in", start=(-9.5, 5.8, 3.2), hit=7.1),
]

# the month: 30 days on a 7 by 5 grid (the 1st falls on the third column); every day has a piece
FIRST_COL = 2
DAYS = []
used = {p["day"]: p for p in PIECES}
for day in range(1, 31):
    cell = FIRST_COL + day - 1
    if day in used:
        p = used[day]
        DAYS.append(dict(day=day, col=cell % 7, row=cell // 7, ray=p["ray"], piece=p["id"], pop=None))
    else:
        DAYS.append(dict(day=day, col=cell % 7, row=cell // 7, ray=rng.randrange(6), piece=None, pop=None))
others = [d for d in DAYS if d["piece"] is None]
rng.shuffle(others)
for k, d in enumerate(others):
    d["pop"] = round(25.05 + 1.3 * k / len(others), 3)
for k, p in enumerate(PIECES):
    p["fly"] = round(24.3 + 0.11 * k, 3)
    # a piece lands when its ray reaches it; the three languages land one after another off the split
    p["land"] = RAYS[p["ray"]]["land"] if p["ray"] != 2 else round(14.8 + 0.3 * ["en", "pt", "fr"].index(p["id"]), 2)

T = dict(lift=(1.0, 3.4), cut=(2.5, 2.9, 3.3), voice=0.8, guard=4.2, brief=8.0, fire=8.6, enter=9.05, fan=(9.2, 10.6),
         formats=12.0, review=19.2, month=24.2, beads=(26.6, 28.3), end=28.7)

TABLE = dict(T=T, rays=RAYS, pieces=PIECES, pages=PAGES, cliches=CLICHES, days=DAYS)
with open(os.path.join(HERE, "..", "assets", "pieces.js"), "w", encoding="utf-8", newline="\n") as f:
    f.write("window.TABLE = " + json.dumps(TABLE, ensure_ascii=False) + ";\n")
with open(os.path.join(HERE, "pieces.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(TABLE, f, ensure_ascii=False, indent=1)
print("pieces:", len(PIECES), "days:", len(DAYS), "cliches:", len(CLICHES))
