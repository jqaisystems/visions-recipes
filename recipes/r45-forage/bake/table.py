"""R45 · Forage: the one table, read by the film and by score/compose.py.
108 bpm, 62 beats. In beats: spore 0-4, search 4-14, words 14-21, scores 21-25.5, contraction 25.5-31, judgement 31-39,
email 39-46, never twice 46-53, close 53-62. Every business, score and email here is fictional.
The network's survivors are chosen here; the agents do the rest.
Writes bake/table.json and assets/table.js.  Usage: python bake/table.py"""
import json, math, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BPM = 108; BEAT = 60 / BPM; BEATS = 62
SW, SH = 1280, 720
rng = random.Random(44)

# 500 fictional businesses, spread with a minimum distance so the dish looks foraged and not random
nodes = []
d = 30.0
while len(nodes) < 500:
    for _ in range(4000):
        x, y = rng.uniform(26, SW - 26), rng.uniform(26, SH - 26)
        if all((x - a) ** 2 + (y - b) ** 2 > d * d for a, b, *_ in nodes):
            nodes.append([round(x, 1), round(y, 1), 0, 0])
            if len(nodes) == 500: break
    d *= 0.95

# 30 survivors, spread out across the dish
cand = list(range(500)); rng.shuffle(cand)
surv = []
for i in cand:
    x, y = nodes[i][:2]
    if 110 < x < SW - 110 and 90 < y < SH - 90 and all(math.hypot(x - nodes[j][0], y - nodes[j][1]) > 92 for j in surv):
        surv.append(i)
    if len(surv) == 30: break
assert len(surv) == 30
for i, n in enumerate(nodes):
    if i in surv: n[2] = rng.randint(62, 96); n[3] = 1
    else: n[2] = min(59, int(abs(rng.gauss(26, 16))))
# the order they stop feeding: lowest first, all gone in two beats
gone = {i: 25.5 + 2.0 * (nodes[i][2] / 60) ** 1.2 + rng.uniform(0, 0.15) for i in range(500) if i not in surv}

# the arteries: a minimum spanning tree over the survivors, each edge a wandering line
inT = {surv[0]}; edges = []
while len(inT) < 30:
    a, b = min(((a, b) for a in inT for b in surv if b not in inT), key=lambda e: math.hypot(nodes[e[0]][0] - nodes[e[1]][0], nodes[e[0]][1] - nodes[e[1]][1]))
    edges.append([a, b]); inT.add(b)


def wander(a, b):
    ax, ay, bx, by = nodes[a][0], nodes[a][1], nodes[b][0], nodes[b][1]
    pts = [[ax, ay], [bx, by]]
    amp = math.hypot(bx - ax, by - ay) * 0.14
    for _ in range(3):
        q = [pts[0]]
        for p, r in zip(pts, pts[1:]):
            nx, ny = -(r[1] - p[1]), r[0] - p[0]; L = math.hypot(nx, ny) or 1
            k = rng.uniform(-amp, amp) / L
            q += [[(p[0] + r[0]) / 2 + nx * k, (p[1] + r[1]) / 2 + ny * k], r]
        pts = q; amp *= 0.5
    return [[round(x, 1), round(y, 1)] for x, y in pts]


arteries = [{"a": a, "b": b, "pts": wander(a, b)} for a, b in edges]
deg = {i: 0 for i in surv}
for a, b in edges: deg[a] += 1; deg[b] += 1
leaves = [i for i in surv if deg[i] == 1]
# the hero: the leaf nearest the left-centre, so the film's card sits to its right
hero = min(leaves, key=lambda i: math.hypot(nodes[i][0] - 470, nodes[i][1] - 360))
nodes[hero][2] = 87
heroEdge = next(k for k, e in enumerate(arteries) if hero in (e["a"], e["b"]))
if arteries[heroEdge]["a"] == hero:
    arteries[heroEdge]["pts"].reverse(); arteries[heroEdge]["a"], arteries[heroEdge]["b"] = arteries[heroEdge]["b"], arteries[heroEdge]["a"]
# the one that's rejected: another leaf, near the hero so both fit in the same shot
others = [i for i in leaves if i != hero]
rej = min(others, key=lambda i: math.hypot(nodes[i][0] - nodes[hero][0], nodes[i][1] - nodes[hero][1]))
rejEdge = next(k for k, e in enumerate(arteries) if rej in (e["a"], e["b"]))
# contacted: the hero and five more, which repel from beat 46
contacted = [hero] + rng.sample([i for i in surv if i not in (hero, rej)], 5)
# a fresh search: new fictional businesses, for the network to spread to
fresh = [[round(rng.uniform(40, SW - 40), 1), round(rng.uniform(40, SH - 40), 1)] for _ in range(70)]
fresh = [f for f in fresh if all(math.hypot(f[0] - nodes[c][0], f[1] - nodes[c][1]) > 70 for c in contacted)]

table = {
    "dur": round(BEATS * BEAT, 4), "beat": round(BEAT, 6), "bpm": BPM, "beats": BEATS, "sw": SW, "sh": SH,
    "nodes": nodes, "surv": surv, "gone": {str(k): round(v, 3) for k, v in gone.items()}, "arteries": arteries,
    "hero": hero, "heroEdge": heroEdge, "rej": rej, "rejEdge": rejEdge, "contacted": contacted, "fresh": fresh,
}
json.dump(table, open(os.path.join(ROOT, "bake", "table.json"), "w", encoding="utf-8"))
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE = " + json.dumps(table) + ";\n")
print("dur", table["dur"], "hero", nodes[hero][:2], "rej", nodes[rej][:2], "fresh", len(fresh))
