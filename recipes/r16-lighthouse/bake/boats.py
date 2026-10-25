"""R16 · Lighthouse. Writes the film's one table: the beam's path and every prospect (boat), with the moment the beam
first finds it, the moment it is scored and the score itself. The film reads ../assets/boats.js and the score reads
boats.json, so picture and sound always agree. Seeded, so it writes the same table every time.
Usage: python bake/boats.py"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
DUR = 32.0
HOT = 85   # a score at or above this is a hot lead

# The beam: [film t, azimuth in degrees (0 = straight out to sea, + to the right), reach in world units].
# Ignite, sweep the sea (source), visit three boats (enrich), sweep again (score), hold on the best one (draft).
BEAM = [
    [0.0, -66, 60], [3.2, -66, 60], [8.8, 66, 70],
    [9.5, 34, 50], [10.9, 34, 50], [11.5, 4, 58], [12.6, 4, 58], [13.2, -32, 46], [14.2, -32, 46],
    [14.9, -64, 62], [18.6, 64, 62], [20.0, -32, 46], [24.8, -32, 46], [26.8, -78, 70], [DUR, -84, 70],
]
SOURCE, SCORE = (3.2, 8.8), (14.9, 18.6)

# The three boats the beam stops on, then three more hot leads. Made up: no real people or companies.
SPECIAL = [
    dict(key="A", phi=-32, d=46, score=96, kind="Design studio · 24 people", signal="Hiring a designer"),
    dict(key="B", phi=4, d=58, score=91, kind="Architecture practice · 18 people", signal="Opened a second office"),
    dict(key="C", phi=34, d=50, score=88, kind="Brand agency · 40 people", signal="Posted about a rebrand"),
]
EXTRA_HOT = [93, 89, 86]
N = 44


def e_io(u):   # GSAP power2.inOut
    return 2 * u * u if u < 0.5 else 1 - (-2 * u + 2) ** 2 / 2


def beam_at(t):
    i = 0
    while i < len(BEAM) - 2 and t >= BEAM[i + 1][0]:
        i += 1
    a, b = BEAM[i], BEAM[i + 1]
    u = e_io(min(1.0, max(0.0, (t - a[0]) / (b[0] - a[0]))))
    return a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u


def first_pass(phi, window):
    t = window[0]
    while t <= window[1]:
        if abs(beam_at(t)[0] - phi) < 1.5:
            return round(t, 3)
        t += 1 / 120
    return None


rng = random.Random(16)
boats = [dict(b) for b in SPECIAL]
while len(boats) < N:
    phi, d = rng.uniform(-62, 62), rng.uniform(34, 95)
    x, z = math.sin(math.radians(phi)) * d, -math.cos(math.radians(phi)) * d
    if all(math.hypot(x - math.sin(math.radians(o["phi"])) * o["d"], z + math.cos(math.radians(o["phi"])) * o["d"]) > 6.5 for o in boats):
        boats.append(dict(phi=round(phi, 2), d=round(d, 2)))
for i, b in enumerate(boats[3:]):
    b["score"] = EXTRA_HOT[i] if i < len(EXTRA_HOT) else rng.randint(12, 78)
for b in boats:
    b["found"] = first_pass(b["phi"], SOURCE)
    b["scored"] = first_pass(b["phi"], SCORE)
    b["hot"] = b["score"] >= HOT
    b["yaw"] = round(rng.uniform(0, 360), 1)
    b["bob"] = round(rng.uniform(0, 6.28), 2)
assert all(b["found"] and b["scored"] for b in boats), "every boat must be passed by both sweeps"

# Hot leads moor at the quay, best score in the middle.
hot = sorted([b for b in boats if b["hot"]], key=lambda b: -b["score"])
order = [2, 3, 1, 4, 0, 5]
for slot, b in zip(order, hot):
    b["slot"] = slot

table = dict(beam=BEAM, hot=HOT, boats=boats)
with open(os.path.join(HERE, "..", "assets", "boats.js"), "w", encoding="utf-8") as f:
    f.write("window.BOATS = " + json.dumps(table) + ";\n")
with open(os.path.join(HERE, "boats.json"), "w", encoding="utf-8") as f:
    json.dump(table, f, indent=1)
print(len(boats), "boats,", len(hot), "hot; found", min(b["found"] for b in boats), "to", max(b["found"] for b in boats))
