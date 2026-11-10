"""The one table for Overview, read by the film and by score/compose.py: the beat grid, the pin field, every relief raised out of it
and when, the noise, the camera (baked per frame), the light and the captions. The sources, the field and the briefing are a demo.
Writes assets/table.js (not committed).  Usage: python bake/table.py"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1920, 1080, 30
BPM = 112; BEAT = 60 / BPM; BEATS = 68
DUR = round(BEATS * BEAT, 4)

# ---------------- the field: NX by NZ steel pins, one unit apart. x runs across, z runs away from the first camera
NX, NZ = 192, 320
EXT = 7.0                         # how far a pin can rise, in pin spacings

# ---------------- marks, in pin units on the field (x, z). Each value is how far the pins there rise, 0 to 1
def rect(x, z, w, h, v=1.0, r=0.0): return ["rect", x, z, w, h, v, r]
def frame(x, z, w, h, lw, v=1.0, r=0.0): return ["frame", x, z, w, h, lw, v, r]
def circ(x, z, rad, lw, v=1.0): return ["circ", x, z, rad, lw, v]
def line(x0, z0, x1, z1, lw, v=1.0): return ["line", x0, z0, x1, z1, lw, v]
def text(s, x, z, size, wt=800, v=1.0, al="c", fit=0.0): return ["text", s, x, z, size, wt, v, al, fit]


def page(cx, cz, s):              # a page: an outline, a heading and lines
    w, h = s * 0.78, s; x, z = cx - w / 2, cz - h / 2
    m = [frame(x, z, w, h, s * 0.07, 1.0, s * 0.05), rect(x + w * 0.12, z + h * 0.12, w * 0.5, h * 0.08, 0.9)]
    for i in range(5): m.append(rect(x + w * 0.12, z + h * (0.32 + i * 0.12), w * (0.76 if i % 3 else 0.55), h * 0.04, 0.6))
    return m


def feed(cx, cz, s):              # a feed: rows of items, each a square and two lines. Plain lines, no product's icon
    w, h = s * 1.3, s; x, z = cx - w / 2, cz - h / 2; m = [frame(x, z, w, h, s * 0.06, 0.9, s * 0.04)]
    rh = (h - s * 0.12) / 3
    for i in range(3):
        zz = z + s * 0.08 + i * rh
        m += [rect(x + s * 0.08, zz, rh * 0.75, rh * 0.75, 0.9, 1), rect(x + s * 0.12 + rh, zz + rh * 0.1, w * 0.5, rh * 0.2, 0.7), rect(x + s * 0.12 + rh, zz + rh * 0.48, w * 0.32, rh * 0.15, 0.5)]
    return m


def site(cx, cz, s):              # a site: a window, a bar, a hero block and columns
    w, h = s * 1.4, s; x, z = cx - w / 2, cz - h / 2
    m = [frame(x, z, w, h, s * 0.06, 1.0, s * 0.05), rect(x, z, w, h * 0.13, 0.8, s * 0.05), rect(x + w * 0.07, z + h * 0.22, w * 0.86, h * 0.3, 0.55, 1)]
    for j in range(3): m.append(rect(x + w * 0.07 + j * w * 0.29, z + h * 0.6, w * 0.26, h * 0.28, 0.7, 1))
    return m


def lens(cx, cz, s):              # a magnifier
    rad = s * 0.36
    return [circ(cx - s * 0.1, cz - s * 0.1, rad, s * 0.09, 1.0), circ(cx - s * 0.1, cz - s * 0.1, rad * 0.6, 0, 0.25),
            line(cx - s * 0.1 + rad * 0.72, cz - s * 0.1 + rad * 0.72, cx + s * 0.42, cz + s * 0.42, s * 0.13, 1.0)]


def chart(cx, cz, s):             # a chart: a base line and bars
    w, h = s * 1.2, s; x, z = cx - w / 2, cz - h / 2
    m = [line(x, z + h, x + w, z + h, s * 0.05, 0.8)]
    hs = [0.35, 0.55, 0.42, 0.78, 0.62, 1.0]; bw = w / len(hs)
    for i, k in enumerate(hs): m.append(rect(x + i * bw + bw * 0.15, z + h - h * k, bw * 0.7, h * k - s * 0.04, 0.95, 0.5))
    return m


def knowledge(cx, cz, w, h):      # the knowledge document: a structured page, headings and indented rows
    x, z = cx - w / 2, cz - h / 2; m = [frame(x, z, w, h, 1.6, 1.0, 2)]
    zz = z + 5
    for sec in range(3):
        m.append(rect(x + 6, zz, w * 0.3, 3.2, 1.0)); zz += 6.5
        for k in range(3): m.append(rect(x + 11, zz, (w - 22) * (0.9 - 0.14 * k), 1.6, 0.7)); zz += 3.6
        zz += 2.4
    return m


def folder(cx, cz, w, h):
    x, z = cx - w / 2, cz - h / 2
    return [rect(x, z - 7, w * 0.38, 10, 0.7, 2), rect(x, z, w, h, 0.85, 3), rect(x + 5, z + 6, w - 10, 1.4, 0.35)]


def glyph(cx, cz, s):             # a briefing, small: a heading bar and three lines
    return [rect(cx - s * 0.36, cz - s * 0.32, s * 0.5, s * 0.14, 1.0, 0.5)] + [rect(cx - s * 0.36, cz - s * 0.08 + k * s * 0.17, s * 0.72 * (1 - 0.12 * k), s * 0.08, 0.8) for k in range(3)]


ICON = {"page": page, "feed": feed, "site": site, "lens": lens, "chart": chart}

# ---------------- layers: a picture and when it rises. keys are [beat, weight]. delay says which way the pins follow:
# "x" left to right, "z" far to near, "r" from the middle out, "n" scattered. spread is in beats.
# brass: [[beat, amount]], how much of the layer's pins turn brass. quiet: the noise is held down under it, so it reads clean
layers = []


def L(name, marks, keys, delay="n", spread=1.0, move=None, anchor=None, brass=None, quiet=False, kind="src"):
    layers.append({"name": name, "marks": marks, "keys": keys, "delay": delay, "spread": spread, "move": move, "anchor": anchor,
                   "brass": brass, "quiet": quiet, "kind": kind})


RINGS = []                        # a ripple through the field: [beat, x, z, height]


def cap(name, s, x, z, size, b0, b1, fit=176.0, delay="x", spread=0.5, ring=0.0):
    L(name, [text(s, x, z, size, 800, 1.0, "c", fit)], [[b0, 0], [b0 + 0.4, 1], [b1 - 0.4, 1], [b1, 0]], delay, spread, quiet=True, kind="cap")
    if ring: RINGS.append([b0 + 0.25, x, z - size * 0.35, ring])


# 1 ground level: the camera rises off the pins and flies over the sources as they rise ahead of it
cap("c_sources", "YOUR SOURCES.", 96, 284, 15, 2.4, 6.6, ring=0.5)
FLY = [("NEWS.", 238, 6.9, 8.9, "page", 38, 218), ("SITES.", 202, 8.9, 10.9, "feed", 156, 184),
       ("FEEDS.", 166, 10.9, 12.9, "site", 36, 146), ("COMPETITORS.", 130, 12.9, 15.2, "lens", 158, 112)]
for k, (s, z, b0, b1, ic, ix, iz) in enumerate(FLY):
    cap("c_fly%d" % k, s, 96, z, 17 if len(s) < 8 else 14, b0, b1, delay="z", spread=0.35, ring=0.7)
    L("s_" + ic, ICON[ic](ix, iz, 30), [[b0 - 0.2, 0], [b0 + 0.6, 1], [19.6, 1], [20.6, 0]], "r", 0.6)
L("s_chart", chart(40, 96, 30), [[14.2, 0], [15.0, 1], [19.6, 1], [20.6, 0]], "r", 0.6)
# 2 everything at once: the sources come up again all around, and the field turns to noise
ECHO = [("page", 160, 110, 26), ("site", 36, 40, 24), ("feed", 160, 36, 22), ("chart", 40, 112, 22), ("lens", 118, 118, 22),
        ("page", 14, 78, 18), ("feed", 180, 82, 14), ("site", 96, 34, 20)]
for k, (ic, x, z, s) in enumerate(ECHO):
    b = 15.4 + k * 0.25; L("e%d" % k, ICON[ic](x, z, s), [[b, 0], [b + 0.35, 0.85], [19.6, 0.85], [20.8, 0]], "r", 0.3)
    RINGS.append([b + 0.2, x, z, 0.35])
cap("c_down", "FROM DOWN HERE,", 96, 72, 13, 15.6, 18.0, fit=150, spread=0.4)
cap("c_noise", "IT'S ALL NOISE.", 96, 72, 14, 18.0, 20.4, fit=150, spread=0.4)
RINGS.append([1.3, 96, 336, 0.5])   # the light coming on: one breath through the field
NOISE = [[0.0, 0.0], [1.0, 0.16], [4.0, 0.12], [14.4, 0.16], [16.4, 0.95], [20.0, 0.95], [24.0, 0.0]]
# 3 from above: the camera cranes straight up, and the noise settles from the middle out
FLAT = {"b": [20.2, 24.2], "x": 96, "z": 70, "r": 230}
cap("c_above", "FROM ABOVE,", 96, 34, 18, 21.0, 24.6, fit=150, delay="r", spread=0.6)
L("knowledge", knowledge(96, 84, 118, 68), [[24.4, 0], [25.8, 0.42], [28.4, 0.42], [29.0, 0.16], [35.0, 0.16], [35.8, 0]], "z", 1.2, kind="doc")
cap("c_field", "BRIEFED ON YOUR FIELD.", 96, 36, 12, 24.8, 28.6, fit=176, ring=0.3)
# 4 the filter: the sources come up around it, everything that doesn't matter drops, and what's left turns brass
SRC4 = [("page", 28, 70, 20, True), ("feed", 166, 46, 17, False), ("lens", 160, 98, 20, True), ("site", 36, 108, 15, False),
        ("chart", 132, 74, 17, True), ("feed", 60, 42, 13, False), ("site", 158, 120, 13, False), ("page", 90, 116, 13, False)]
KEEP = {"page": (20, 52), "lens": (20, 76), "chart": (20, 100)}    # where each kept source goes: the bullets of the briefing
for k, (ic, x, z, s, keep) in enumerate(SRC4):
    b = 28.4 + k * 0.18
    if keep:
        kx, kz = KEEP[ic]
        L("k_" + ic, ICON[ic](x, z, s), [[b, 0], [b + 0.4, 1], [44.8, 1], [45.8, 0]], "r", 0.4,
          move=[[33.0, 0, 0, 1], [35.0, kx - x, kz - z, 12.0 / s]], anchor=[x, z], brass=[[31.4, 0], [32.4, 1]])
    else:
        L("f%d" % k, ICON[ic](x, z, s), [[b, 0], [b + 0.4, 0.9], [31.2, 0.9], [32.4, 0]], "x", 0.9)
    RINGS.append([b + 0.2, x, z, 0.25])
cap("c_matters", "ONLY WHAT MATTERS.", 96, 32, 13, 28.8, 32.4, fit=176)
cap("c_why", "WHAT CHANGED, AND WHY.", 96, 32, 12, 32.4, 35.4, fit=176)
# 5 written up: the briefing rises out of the field line by line, next to its brass bullets
BX = 32
BRIEF = [("THIS WEEK, IN BRIEF", 96, 32, 12, 800, 1.0, 38.0, "c"),
         ("SUPPLIER PRICES ROSE", BX, 52, 10.5, 800, 1.0, 38.6, "left"), ("WHY: TWO OF YOUR LINES", BX, 62, 8, 700, 0.72, 39.1, "left"),
         ("A NEW GRANT OPENS", BX, 76, 10.5, 800, 1.0, 39.6, "left"), ("WHY: YOUR SECTOR, YOUR SIZE", BX, 86, 8, 700, 0.72, 40.1, "left"),
         ("A RIVAL IS HIRING", BX, 100, 10.5, 800, 1.0, 40.6, "left"), ("WHY: IN YOUR REGION", BX, 110, 8, 700, 0.72, 41.1, "left")]
for i, (s, x, z, size, wt, v, b0, al) in enumerate(BRIEF):
    L("brief%d" % i, [text(s, x, z, size, wt, v, al, 156)], [[b0, 0], [b0 + 0.6, 1], [44.8, 1], [45.8, 0]], "x", 0.7, quiet=True, kind="brief")
cap("c_format", "IN YOUR FORMAT.", 104, 82, 14, 35.6, 37.9, fit=140, ring=0.3)
cap("c_voice", "IN YOUR VOICE.", 96, 128, 11, 42.0, 45.4, fit=170)
# 6 on schedule: a grid of days. Daily, the briefing rises on every day in turn; weekly, once, taller and in brass
S, GAP = 20, 4; X0 = (NX - (7 * S + 6 * GAP)) / 2
grid = []; DAYS = []
for row, zc in enumerate((62, 90)):
    for d in range(7):
        x = X0 + d * (S + GAP); grid.append(frame(x, zc - S / 2, S, S, 1.3, 0.35, 1.5)); DAYS.append((x + S / 2, zc, row, d))
L("grid", grid, [[45.6, 0], [46.6, 1], [54.2, 1], [55.0, 0]], "x", 1.0, kind="doc")
POPS = []
for cx, cz, row, d in DAYS:
    if row == 0: b = 47.4 + d * 0.5
    elif d == 0: b = 51.4
    else: continue
    POPS.append([b, row])
    L("day%d%d" % (row, d), glyph(cx, cz, S * 0.82), [[b, 0], [b + 0.2, 0.75 if row == 0 else 1.0], [54.2, 0.75 if row == 0 else 1.0], [55.0, 0]], "r", 0.12,
      brass=[[0, 0]] if row == 0 else [[0, 1]])
    RINGS.append([b + 0.15, cx, cz, 0.22 if row == 0 else 0.5])
cap("c_daily", "DAILY OR WEEKLY.", 96, 40, 13, 46.2, 51.0, fit=176)
cap("c_rhythm", "ON YOUR RHYTHM.", 96, 40, 13, 51.2, 55.0, fit=176)
# 7 yours: a brass folder, then the camera pulls all the way out and the light goes off
L("folder", folder(96, 92, 64, 40), [[55.4, 0], [56.2, 1], [61.6, 1], [62.6, 0]], "r", 0.6, brass=[[0, 1]], kind="doc")
RINGS.append([55.8, 96, 92, 0.5])
cap("c_code", "THE CODE. THE PROMPTS.", 96, 50, 12, 56.0, 59.0, fit=176)
cap("c_yours", "THE KNOWLEDGE DOCUMENT. YOURS.", 96, 50, 9.6, 59.0, 62.4, fit=184)

# ---------------- the camera: [beat, x, y, z, yaw, pitch, roll, fov, ease]. yaw 0 looks along -z; pitch -90 looks straight down
# ease is how fast it moves through the key, 1 = smooth flow, 0 = it settles there
def aim(b, cx, cz, width, yaw=0.0, pitch=-40.0, roll=0.0, fov=40.0, ease=0.4, frac=0.82, dz=0.0):
    """a camera key that frames a thing width pins wide, centred on (cx, cz), from yaw and pitch"""
    th = math.tan(math.radians(fov) / 2); D = width / (frac * 2 * th * W / H)
    Y, P = math.radians(yaw), math.radians(pitch); f = [math.sin(Y) * math.cos(P), math.sin(P), -math.cos(Y) * math.cos(P)]
    T = [cx, EXT * 0.5, cz + dz]
    return [b] + [round(T[k] - f[k] * D, 3) for k in range(3)] + [yaw, pitch, roll, fov, ease]


def tw(name):                     # how wide a caption is, roughly: 0.66 em a letter, never wider than its fit
    m = next(l for l in layers if l["name"] == name)["marks"][0]; return min(len(m[1]) * m[4] * 0.66, m[8] or 1e9)


def at(name):
    m = next(l for l in layers if l["name"] == name)["marks"][0]; return m[2], m[3] - m[4] * 0.36


CAM = [
    [0.0, 96, 2.0, 344, 0, -2, 0, 34, 0],
    [1.0, 96, 2.2, 341, 0, -3, 0, 34, 0.5],
    aim(3.6, *at("c_sources"), tw("c_sources"), 0, -34, 0, 38, 0.5),
    aim(6.0, *at("c_sources"), tw("c_sources") * 0.92, 0, -38, 0, 38, 0.2),
    aim(7.9, *at("c_fly0"), tw("c_fly0") * 1.25, 0, -42, -3, 40, 0.3),
    aim(9.9, *at("c_fly1"), tw("c_fly1") * 1.25, 0, -42, 3, 40, 0.3),
    aim(11.9, *at("c_fly2"), tw("c_fly2") * 1.25, 0, -42, -3, 40, 0.3),
    aim(14.0, *at("c_fly3"), tw("c_fly3") * 1.05, 0, -40, 0, 40, 0.4),
    aim(16.8, *at("c_down"), tw("c_down") * 1.05, 5, -40, 3, 44, 0.5),
    aim(19.2, *at("c_noise"), tw("c_noise") * 1.05, -4, -40, -3, 44, 0.4),
    aim(22.6, *at("c_above"), 150, 0, -72, 0, 42, 0.8, dz=22),
    [24.6, 96, 150, 72, 0, -90, 0, 40, 0.3],
    [28.0, 96, 152, 72, 0, -90, 0, 40, 0.4],
    [35.5, 96, 140, 72, 0, -90, 0, 40, 0.3],
    aim(37.0, 104, 77, 150, -6, -46, 0, 40, 0.5),
    aim(39.4, 92, 48, 160, -4, -48, 0, 40, 0.5),
    aim(41.8, 96, 74, 186, 0, -52, 0, 40, 0.4, frac=0.88),
    aim(44.8, 96, 86, 196, 0, -56, 0, 40, 0.3, frac=0.9),
    aim(47.2, 96, 62, 178, 0, -58, 0, 40, 0.5),
    aim(50.8, 96, 66, 182, 4, -42, 0, 40, 0.5),
    aim(54.6, 96, 66, 184, 0, -40, 0, 40, 0.3),
    aim(57.4, 96, 70, 170, 0, -52, 0, 40, 0.4),
    aim(60.6, 96, 68, 186, 0, -60, 0, 40, 0.3),
    [62.0, 96, 160, 80, 0, -88, 0, 40, 0.8],
    [63.6, 96, 520, 160, 0, -90, 0, 40, 0],
]


def herm(K, b, col):
    if b <= K[0][0]: return K[0][col]
    if b >= K[-1][0]: return K[-1][col]
    i = 0
    while K[i + 1][0] < b: i += 1
    a, c = K[i], K[i + 1]; dt = c[0] - a[0]; u = (b - a[0]) / dt

    def tan(j):
        if j <= 0 or j >= len(K) - 1: return 0.0
        return K[j][-1] * (K[j + 1][col] - K[j - 1][col]) / (K[j + 1][0] - K[j - 1][0])
    m0, m1 = tan(i) * dt, tan(i + 1) * dt
    u2, u3 = u * u, u * u * u
    return (2 * u3 - 3 * u2 + 1) * a[col] + (u3 - 2 * u2 + u) * m0 + (-2 * u3 + 3 * u2) * c[col] + (u3 - u2) * m1


def cam_at(b):
    x, y, z, yaw, pit, rol, fov = (herm(CAM, b, c) for c in range(1, 8))
    Y, P, R = math.radians(yaw), math.radians(pit), math.radians(rol)
    fwd = [math.sin(Y) * math.cos(P), math.sin(P), -math.cos(Y) * math.cos(P)]
    rt = [math.cos(Y), 0.0, math.sin(Y)]
    up = [rt[1] * fwd[2] - rt[2] * fwd[1], rt[2] * fwd[0] - rt[0] * fwd[2], rt[0] * fwd[1] - rt[1] * fwd[0]]
    cr, sr = math.cos(R), math.sin(R)
    rt2 = [rt[k] * cr + up[k] * sr for k in range(3)]; up2 = [up[k] * cr - rt[k] * sr for k in range(3)]
    return [x, y, z], fwd, rt2, up2, math.tan(math.radians(fov) / 2)


def project(b, p):
    pos, f, r, u, th = cam_at(b); d = [p[k] - pos[k] for k in range(3)]
    cz = sum(d[k] * f[k] for k in range(3))
    if cz <= 0.1: return None
    sx = sum(d[k] * r[k] for k in range(3)) / (cz * th * W / H); sy = sum(d[k] * u[k] for k in range(3)) / (cz * th)
    return ((sx * 0.5 + 0.5) * W, (0.5 - sy * 0.5) * H)


NF = int(round(DUR * FPS)); CAMF = []
for f in range(NF):
    b = f / FPS / BEAT; pos, fw, rt, up, th = cam_at(b)
    # focus: where the middle of the frame meets the field
    t = (pos[1] - EXT * 0.4) / max(-fw[1], 0.05)
    CAMF.append([round(v, 4) for v in pos + fw + rt + up + [th, min(t, 900.0)]])

# ---------------- the light: a low raking lamp. az is where it shines from, around the field (180 = from the left, 270 = from the far end),
# el its height. pool is a soft pool of light on the field [beat, x, z, radius]
LIGHT = {
    "on": 1.0, "off": [62.6, 63.5],
    "az": [[0, 215], [4, 168], [20, 160], [28, 154], [37, 150], [40.2, 150], [42.4, 192], [45, 156], [68, 160]],
    "el": [[0, 5], [3, 16], [14, 22], [20, 18], [26, 30], [44, 30], [48, 26], [68, 30]],
    "pool": [[0, 96, 300, 60], [14, 96, 140, 70], [20, 96, 90, 80], [26, 96, 72, 90], [36, 80, 82, 75], [46, 96, 78, 90], [56, 96, 72, 80], [64, 96, 160, 260]],
}
LOGO = 63.6

table = {
    "w": W, "h": H, "fps": FPS, "bpm": BPM, "beat": BEAT, "beats": BEATS, "dur": DUR,
    "nx": NX, "nz": NZ, "ext": EXT, "layers": layers, "noise": NOISE, "flat": FLAT, "rings": RINGS,
    "cam": CAMF, "light": LIGHT, "logo": LOGO, "pops": POPS, "label": "AI RESEARCH & BRIEFING SYSTEMS · DEMO BRIEFING",
}
open(os.path.join(ROOT, "assets", "table.js"), "w", encoding="utf-8").write("window.TABLE=" + json.dumps(table, separators=(",", ":"), ensure_ascii=False) + ";")

if __name__ == "__main__":
    import sys
    print("dur", DUR, "frames", NF, "layers", len(layers), "pins", NX * NZ)
    if "-v" in sys.argv:   # where each caption sits on screen at its middle: a rough box, the text 0.6 em wide a letter
        for l in layers:
            if l["kind"] != "cap" and l["kind"] != "brief": continue
            m = l["marks"][0]; s, x, z, size, al, fit = m[1], m[2], m[3], m[4], m[7], m[8]
            w = min(len(s) * size * 0.66, fit or 1e9); x0 = x - w / 2 if al == "c" else x; b = (l["keys"][1][0] + l["keys"][-2][0]) / 2
            pts = [project(b, (xx, EXT * 0.8, zz)) for xx in (x0, x0 + w) for zz in (z - size * 0.72, z)]
            if None in pts: print("%-14s b%5.1f behind the camera" % (l["name"], b)); continue
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            print("%-14s b%5.1f x %5d..%5d  y %5d..%5d  h %4d" % (l["name"], b, min(xs), max(xs), min(ys), max(ys), max(ys) - min(ys)))
