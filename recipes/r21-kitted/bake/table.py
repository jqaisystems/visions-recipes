"""R21 · Kitted. The one table: the film's clock, every tool (its outline, its cutout, where it lies in the heap, where
it hovers and where it fits in the case), the things that get binned, the laser's cut path and timing, the prompt
cards and the five benches' jobs. Writes ../assets/table.js for the film and table.json for the score.
Usage: python bake/table.py   (standard library only, deterministic)"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
rnd = random.Random(21)

# ---- the clock (seconds of film time)
BEAT = 0.6                                  # 100 bpm
T = dict(light=[0.2, 0.6], audit=[3.8, 6.0], bin=[6.2, 7.6], hover=[6.4, 7.6], caseIn=[7.6, 8.4], lid=[8.2, 8.9],
         headIn=[8.6, 9.0], cut0=9.1, cutFirst=1.2, cutEach=0.36, headOut=[13.0, 13.4], install=13.6, beat=BEAT,
         cards=[17.5, 18.7], lights=[18.9, 19.5], cases=[19.4, 20.2], lids=[20.0, 20.7], jobs=20.8, jobsEnd=24.4,
         book=[25.0, 25.6], word=[26.0, 28.4], end=29.0)


def arc(cx, cz, r, a0, a1, n):
    return [[cx + r * math.cos(a0 + (a1 - a0) * i / n), cz + r * math.sin(a0 + (a1 - a0) * i / n)] for i in range(n + 1)]


def rrect(w, d, r, n=6):
    x, z = w / 2 - r, d / 2 - r
    return (arc(x, z, r, 0, math.pi / 2, n) + arc(-x, z, r, math.pi / 2, math.pi, n) +
            arc(-x, -z, r, math.pi, 1.5 * math.pi, n) + arc(x, -z, r, 1.5 * math.pi, 2 * math.pi, n))


def circle(r, n=48, cx=0, cz=0):
    return arc(cx, cz, r, 0, 2 * math.pi, n)[:-1]


# ---- the tools: outlines in the case's plane (x along the tool, z across), centred on 0,0
def pen():
    return arc(-1.22, 0, 0.18, math.pi / 2, 1.5 * math.pi, 10) + [[0.82, -0.18], [1.06, -0.12], [1.4, 0], [1.06, 0.12], [0.82, 0.18]]


def spanner():
    return (arc(-1.05, 0, 0.16, math.pi / 2, 1.5 * math.pi, 10) +
            [[0.5, -0.16], [0.72, -0.4], [1.3, -0.4], [0.98, 0.0], [1.3, 0.4], [0.72, 0.4], [0.5, 0.16]])


def lens():
    a0 = math.asin(0.12 / 0.55)
    return arc(-0.45, 0, 0.55, a0, 2 * math.pi - a0, 40) + arc(0.88, 0, 0.12, -math.pi / 2, math.pi / 2, 8)


def gear():
    pts, n = [], 10
    for k in range(n):
        a = 2 * math.pi * k / n
        for da, rr in ((-0.17, 0.5), (-0.1, 0.62), (0.1, 0.62), (0.17, 0.5)):
            pts.append([rr * math.cos(a + da), rr * math.sin(a + da)])
        pts += arc(0, 0, 0.5, a + 0.17, a + 2 * math.pi / n - 0.17, 3)[1:-1]
    return pts


def film():
    w, d, pts = 1.3, 0.95, []
    xs = [-0.44, -0.22, 0.0, 0.22, 0.44]
    pts.append([-w / 2, -d / 2])
    for x in xs:                                         # sprocket notches along the back edge
        pts += [[x - 0.06, -d / 2], [x - 0.06, -d / 2 + 0.1], [x + 0.06, -d / 2 + 0.1], [x + 0.06, -d / 2]]
    pts += [[w / 2, -d / 2], [w / 2, d / 2]]
    for x in reversed(xs):                               # and the front edge
        pts += [[x + 0.06, d / 2], [x + 0.06, d / 2 - 0.1], [x - 0.06, d / 2 - 0.1], [x - 0.06, d / 2]]
    pts.append([-w / 2, d / 2])
    return pts


def report():
    w, d, f = 0.8, 0.92, 0.22
    return [[-w / 2, -d / 2], [w / 2 - f, -d / 2], [w / 2, -d / 2 + f], [w / 2, d / 2], [-w / 2, d / 2]]


def page():
    w, d = 1.5, 0.9
    body = rrect(w, d, 0.08, 4)
    return body[: len(body) * 3 // 4 + 1] + [[-0.2, -d / 2], [-0.24, -d / 2 - 0.13], [-0.66, -d / 2 - 0.13], [-0.7, -d / 2]] + body[len(body) * 3 // 4 + 1:]


def ccw(p):
    s = sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(p, p[1:] + p[:1]))
    return p if s > 0 else p[::-1]


def offset(p, d):
    """Pushes a closed outline out by d (miter, capped), for the cutout and the laser's path."""
    p, out, n = ccw(p), [], len(p)
    for i in range(n):
        a, b, c = p[i - 1], p[i], p[(i + 1) % n]
        n1 = [(b[1] - a[1]), -(b[0] - a[0])]
        n2 = [(c[1] - b[1]), -(c[0] - b[0])]
        l1, l2 = math.hypot(*n1) or 1, math.hypot(*n2) or 1
        n1, n2 = [n1[0] / l1, n1[1] / l1], [n2[0] / l2, n2[1] / l2]
        m = [n1[0] + n2[0], n1[1] + n2[1]]
        lm = math.hypot(*m) or 1
        m = [m[0] / lm, m[1] / lm]
        cos = max(0.5, m[0] * n1[0] + m[1] * n1[1])
        out.append([round(b[0] - m[0] * d / cos, 4), round(b[1] - m[1] * d / cos, 4)])
    return out


def length(p):
    return sum(math.dist(a, b) for a, b in zip(p, p[1:] + p[:1]))


R4 = lambda p: [[round(x, 4), round(z, 4)] for x, z in p]
# name, the work it does (the audit tag), the skill tag engraved under its cutout, its outline, holes, its colour in the heap,
# where it fits in the case (x, z, turn), and the tool's thickness
TOOLS = [
    dict(id="pen", name="Writing", skill="house voice", shape=pen(), holes=[], heap="#ff5d5d", fit=[-1.27, -1.3, 0]),
    dict(id="spanner", name="Code", skill="review rules", shape=spanner(), holes=[], heap="#ffad3b", fit=[1.5, -1.28, 0]),
    dict(id="lens", name="Images", skill="brand looks", shape=lens(), holes=[circle(0.37, 40, -0.45, 0)], heap="#c46bff", fit=[-1.7, 0.0, 0]),
    dict(id="gear", name="Automations", skill="starter recipes", shape=gear(), holes=[circle(0.17, 24)], heap="#ffe04a", fit=[0.3, -0.05, 0]),
    dict(id="film", name="Video", skill="your formats", shape=film(), holes=[rrect(0.78, 0.48, 0.04, 3)], heap="#5c9cff", fit=[1.95, 0.08, 0]),
    dict(id="report", name="Reports", skill="weekly, monthly", shape=report(), holes=[], heap="#62f08a", fit=[-2.25, 1.3, 0]),
    dict(id="page", name="Pages", skill="templates", shape=page(), holes=[], heap="#ff6bd0", fit=[-0.85, 1.36, 0]),
]
BOOK = dict(id="book", name="Playbook", shape=rrect(1.5, 1.0, 0.06, 3), fit=[1.65, 1.32, 0])
CASE = dict(w=6.0, d=4.0, h=0.8, foam=0.3, x=0.4, z=0.3, lid=4.0, margin=0.055)

# the case's layout must leave foam between every pair of cutouts
def bbox(t):
    xs, zs = [p[0] + t["fit"][0] for p in t["shape"]], [p[1] + t["fit"][1] for p in t["shape"]]
    return min(xs), max(xs), min(zs), max(zs)


ALL = TOOLS + [BOOK]
for i, a in enumerate(ALL):
    ax0, ax1, az0, az1 = bbox(a)
    assert ax0 > -CASE["w"] / 2 + 0.15 and ax1 < CASE["w"] / 2 - 0.15 and az0 > -CASE["d"] / 2 + 0.15 and az1 < CASE["d"] / 2 - 0.15, a["id"]
    for b in ALL[i + 1:]:
        bx0, bx1, bz0, bz1 = bbox(b)
        assert ax1 + 0.14 < bx0 or bx1 + 0.14 < ax0 or az1 + 0.14 < bz0 or bz1 + 0.14 < az0, (a["id"], b["id"])

# the cut: the first outline slowly (the close-up), then the rest at speed, the playbook's slot last
t = T["cut0"]
for k, tool in enumerate(ALL):
    tool["cut"] = offset(tool["shape"], CASE["margin"])
    dur = T["cutFirst"] if k == 0 else T["cutEach"]
    tool["cutT"] = [round(t, 3), round(t + dur, 3)]
    tool["cutLen"] = round(length(tool["cut"]), 4)
    t += dur + (0.1 if k == 0 else 0.0)
    tool["shape"] = R4(tool["shape"])
    tool["holes"] = [R4(h) for h in tool.get("holes", [])]
assert t < T["headOut"][0], t

# ---- the heap on the bench: the seven tools in their own colours, mixed with duplicates and clutter
EXTRAS = [
    dict(kind="tool", of="pen", heap="#ff8a3b", label="DUPLICATE", scale=0.92),
    dict(kind="tool", of="lens", heap="#ff4fa3", label="DUPLICATE", scale=0.82),
    dict(kind="tool", of="gear", heap="#b6ff4a", label="NOT NEEDED", scale=0.74),
    dict(kind="tool", of="report", heap="#8a7dff", label="DUPLICATE", scale=0.9),
    dict(kind="keys", heap="#ffd36b", label="PERSONAL LOGINS"),
    dict(kind="note", text="pasted prompt", heap="#ffe66b", label="PASTED PROMPTS"),
    dict(kind="note", text="ask Ana", heap="#ff9ecf", label=""),
    dict(kind="note", text="v3 final", heap="#9fe8ff", label=""),
    dict(kind="note", text="which login?", heap="#c6ff9e", label=""),
    dict(kind="cable", heap="#ff6b6b", label="TANGLED"),
    dict(kind="cable", heap="#6bb8ff", label=""),
]
SHAPES = {t["id"]: t["shape"] for t in TOOLS}
for e in EXTRAS:
    if e["kind"] == "tool":
        e["shape"] = R4([[x * e["scale"], z * e["scale"]] for x, z in SHAPES[e["of"]]])
        e["holes"] = [R4([[x * e["scale"], z * e["scale"]] for x, z in h]) for h in next(t for t in TOOLS if t["id"] == e["of"])["holes"]]

# place everything in a loose pile: seeded, a few tries for each piece so the pile reads as a pile, not a stack
PILE = TOOLS + EXTRAS
placed = []
for k, it in enumerate(PILE):
    for _ in range(400):
        x, z = rnd.uniform(-3.1, 3.1), rnd.uniform(-1.3, 1.9)
        if all(math.hypot(x - a, z - b) > 0.95 for a, b in placed) or _ == 399:
            break
    placed.append((x, z))
    it["heapPos"] = [round(x, 3), round(0.02 + 0.07 * (k % 4) + (0.12 if it.get("kind") == "note" else 0), 3), round(z, 3)]
    it["heapRot"] = [round(rnd.uniform(-0.12, 0.12), 3), round(rnd.uniform(-math.pi, math.pi), 3), round(rnd.uniform(-0.12, 0.12), 3)]

# the audit: the scanning bar crosses the bench left to right; each piece is tagged as the bar reaches it
SCAN = [-4.6, 4.6]
for it in PILE:
    u = (it["heapPos"][0] - SCAN[0]) / (SCAN[1] - SCAN[0])
    it["tagT"] = round(T["audit"][0] + u * (T["audit"][1] - T["audit"][0]), 3)
# the extras slide off the right edge into the bin, nearest first
order = sorted(EXTRAS, key=lambda e: -e["heapPos"][0])
for j, e in enumerate(order):
    e["binT"] = round(T["bin"][0] + j * (T["bin"][1] - T["bin"][0] - 0.5) / (len(order) - 1), 3)
# the kept tools rise and hover in a row over the case, standing up, then drop into their cutouts on the beat
for k, tool in enumerate(TOOLS):
    tool["hover"] = [round(-4.05 + 1.35 * k, 3), 6.6, CASE["z"]]
    tool["riseT"] = round(T["hover"][0] + 0.1 * k, 3)
    tool["dropT"] = round(T["install"] + BEAT * k, 3)
assert TOOLS[-1]["dropT"] + 0.25 < T["cards"][0]

# ---- the prompt library: index cards riffle into a box beside the case
CARDS = ["Weekly report", "Client reply", "Meeting notes", "Product shot", "Social cut", "Landing page", "Brief to deck",
         "Invoice check", "Welcome email", "Proposal draft", "Blog outline", "Data cleanup", "Release notes", "FAQ answer",
         "Ad variants", "Style check", "Code review", "Job post", "Price sheet", "Board summary"]
CARDT = [round(T["cards"][0] + (T["cards"][1] - T["cards"][0] - 0.3) * (i / (len(CARDS) - 1)) ** 0.85, 3) for i in range(len(CARDS))]

# ---- onboarding: five benches in a row, each runs a real job in light
BENCHES = [dict(x=-22.0, job="report"), dict(x=-11.0, job="image"), dict(x=0.0, job="page"), dict(x=11.0, job="clip"), dict(x=22.0, job="automation")]
for k, b in enumerate(BENCHES):
    b["lightT"] = round(T["lights"][0] + 0.15 * [2, 1, 0, 1, 2][k], 3) if b["x"] else 0.2
    b["jobT"] = round(T["jobs"] + 0.32 * k, 3)

TABLE = dict(T=T, scan=SCAN, case=CASE, tools=TOOLS, book=BOOK, extras=EXTRAS, cards=CARDS, cardT=CARDT, benches=BENCHES)
with open(os.path.join(HERE, "..", "assets", "table.js"), "w", encoding="utf-8", newline="\n") as f:
    f.write("window.TABLE = " + json.dumps(TABLE, ensure_ascii=False, separators=(",", ":")) + ";\n")
slim = json.loads(json.dumps(TABLE))
for it in slim["tools"] + slim["extras"] + [slim["book"]]:
    for k in ("shape", "holes", "cut"):
        it.pop(k, None)
with open(os.path.join(HERE, "table.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(slim, f, ensure_ascii=False, indent=1)
for tool in ALL:
    print(tool["id"], "cut", tool["cutT"], "len", tool["cutLen"], "drop", tool.get("dropT"), "tag", tool.get("tagT"))
print("bin", [(e.get("of") or e["kind"], e["binT"]) for e in order])
