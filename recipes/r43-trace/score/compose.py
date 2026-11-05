"""R43 · Trace: the sound and the picture, composed as one signal.
The left channel is the beam's x and the right channel its y. Every scene below is a set of strokes; the beam redraws the
scene over and over, and how fast it redraws is the note you hear. A kick is the whole picture being thrown about, a snare is
the picture frazzling, and a small quiet picture is a quiet sound. Nothing is added to the audio that the beam doesn't draw.
Plot assets/bgm/score.wav on an XY scope and you get the film's images.
Writes assets/bgm/score.wav and assets/beam.js (neither committed).  Usage: python score/compose.py"""
import base64, json, os, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TB = json.load(open(os.path.join(ROOT, "bake", "table.json"), encoding="utf-8"))
SR = TB["sr"]; BEAT = TB["beat"]; BEATS = TB["beats"]; N = int(round(TB["dur"] * SR)); ASPECT = TB["aspect"]
GAIN = 0.125    # the scope's gain knob: world units to WAV level. The film divides it back out.
rng = np.random.default_rng(41)


def cl(x, a=0.0, b=1.0): return max(a, min(b, x))
def r(t, a, b): return cl((t - a) / (b - a))
def eo(u): return 1 - (1 - u) ** 3
def eio(u): return 4 * u ** 3 if u < 0.5 else 1 - (-2 * u + 2) ** 3 / 2
def eb(u): return 1 + 2.7 * (u - 1) ** 3 + 1.7 * (u - 1) ** 2


# ---------------- a single-stroke font, drawn by hand. x 0 to .7, y 0 to 1
F = {
    "A": "0,0 .35,1 .7,0|.13,.38 .57,.38", "B": "0,0 0,1 .45,1 .62,.88 .62,.64 .45,.52 0,.52|.45,.52 .68,.4 .68,.13 .48,0 0,0", "C": ".68,.82 .5,1 .2,1 0,.78 0,.22 .2,0 .5,0 .68,.18",
    "D": "0,0 0,1 .4,1 .68,.75 .68,.25 .4,0 0,0", "E": ".68,1 0,1 0,0 .68,0|0,.52 .5,.52", "F": ".68,1 0,1 0,0|0,.52 .5,.52", "G": ".68,.82 .5,1 .2,1 0,.78 0,.22 .2,0 .5,0 .68,.2 .68,.46 .38,.46",
    "H": "0,0 0,1|.68,0 .68,1|0,.52 .68,.52", "I": ".14,1 .14,0", "J": ".6,1 .6,.2 .42,0 .18,0 0,.2", "K": "0,0 0,1|.68,1 0,.42|.22,.58 .7,0", "L": "0,1 0,0 .62,0",
    "M": "0,0 0,1 .38,.35 .76,1 .76,0", "N": "0,0 0,1 .68,0 .68,1", "O": ".2,0 0,.22 0,.78 .2,1 .5,1 .7,.78 .7,.22 .5,0 .2,0", "P": "0,0 0,1 .46,1 .66,.84 .66,.6 .46,.44 0,.44",
    "Q": ".2,0 0,.22 0,.78 .2,1 .5,1 .7,.78 .7,.22 .5,0 .2,0|.42,.24 .72,-.06", "R": "0,0 0,1 .46,1 .66,.84 .66,.6 .46,.44 0,.44|.36,.44 .7,0", "S": ".66,.84 .48,1 .2,1 .02,.84 .02,.64 .2,.52 .5,.48 .68,.34 .68,.16 .5,0 .2,0 0,.16",
    "T": "0,1 .7,1|.35,1 .35,0", "U": "0,1 0,.22 .2,0 .5,0 .7,.22 .7,1", "V": "0,1 .35,0 .7,1", "W": "0,1 .2,0 .4,.7 .6,0 .8,1", "X": "-.05,-.08 .73,1.08|-.05,1.08 .73,-.08", "Y": "0,1 .35,.48 .7,1|.35,.48 .35,0", "Z": "0,1 .68,1 0,0 .68,0",
    "0": ".2,0 0,.22 0,.78 .2,1 .46,1 .66,.78 .66,.22 .46,0 .2,0|.08,.2 .58,.8", "1": ".1,.8 .32,1 .32,0|.08,0 .56,0", "2": "0,.8 .18,1 .46,1 .64,.8 .64,.58 0,0 .68,0", "3": "0,.86 .2,1 .46,1 .64,.84 .64,.64 .4,.52 .66,.38 .66,.16 .46,0 .2,0 0,.14",
    "4": ".52,0 .52,1 0,.3 .7,.3", "5": ".62,1 .06,1 .02,.54 .42,.6 .64,.42 .64,.18 .44,0 .18,0 0,.14", "6": ".6,.92 .4,1 .2,.96 0,.7 0,.2 .2,0 .46,0 .64,.18 .64,.38 .46,.54 .2,.54 0,.36", "7": "0,1 .66,1 .24,0",
    "8": ".32,.54 .1,.66 .06,.84 .2,1 .46,1 .6,.84 .56,.66 .32,.54 .04,.38 0,.16 .18,0 .48,0 .66,.16 .6,.38 .32,.54", "9": ".06,.08 .26,0 .46,.04 .66,.3 .66,.8 .46,1 .2,1 .02,.82 .02,.62 .2,.46 .46,.46 .66,.64",
    "a": ".58,.62 .58,0|.58,.46 .42,.62 .18,.62 0,.44 0,.18 .18,0 .42,0 .58,.16", "c": ".56,.5 .42,.62 .16,.62 0,.46 0,.16 .16,0 .42,0 .56,.12", "e": "0,.32 .58,.32 .58,.44 .42,.62 .16,.62 0,.46 0,.16 .16,0 .44,0 .56,.1",
    "i": ".1,.62 .1,0|.03,.96 .17,.96 .17,.82 .03,.82 .03,.96", "j": ".2,.62 .2,-.14 .06,-.26|.13,.96 .27,.96 .27,.82 .13,.82 .13,.96", "m": "0,0 0,.62|0,.46 .14,.62 .28,.62 .36,.46 .36,0|.36,.46 .5,.62 .64,.62 .72,.46 .72,0", "o": ".16,0 0,.16 0,.46 .16,.62 .42,.62 .58,.46 .58,.16 .42,0 .16,0",
    "q": ".58,.62 .58,-.28|.58,.46 .42,.62 .16,.62 0,.46 0,.16 .16,0 .42,0 .58,.16", "r": "0,0 0,.62|0,.42 .16,.6 .4,.62", "s": ".52,.52 .38,.62 .14,.62 .02,.5 .02,.4 .14,.32 .42,.28 .56,.18 .56,.1 .42,0 .14,0 0,.1", "u": "0,.62 0,.16 .16,0 .42,0 .58,.16|.58,.62 .58,0",
    ":": ".06,.74 .2,.74 .2,.6 .06,.6 .06,.74|.06,.38 .2,.38 .2,.24 .06,.24 .06,.38", ".": ".04,0 .18,0 .18,.14 .04,.14 .04,0", "?": ".02,.8 .2,1 .46,1 .64,.82 .64,.62 .32,.4 .32,.24|.32,.04 .32,0", "-": ".08,.45 .52,.45", "'": ".14,1 .1,.72", "·": ".1,.5 .17,.5", '"': ".1,1 .1,.72|.3,1 .3,.72",
}
GL = {c: [np.array([[float(v) for v in p.split(",")] for p in st.split()]) for st in s.split("|")] for c, s in F.items()}
WID = {c: max(p[:, 0].max() for p in g) for c, g in GL.items()}


def width(s, h, track=0.2):
    return sum((WID.get(c, 0.32) + track) * h for c in s) - track * h


def T(s, x, y, h, a="c", n=None, track=0.2):
    """Strokes for a line of text."""
    w = width(s, h, track); x0 = x - (w / 2 if a == "c" else (w if a == "r" else 0)); out = []
    for k, c in enumerate(s if n is None else s[:n]):
        if c in GL:
            for st in GL[c]: out.append(st * h + [x0, y])
        x0 += (WID.get(c, 0.32) + track) * h
    return out


def fit(s, x, y, wd, a="c", maxh=0.5, track=0.2):
    return T(s, x, y, min(maxh, wd / width(s, 1.0, track)), a, track=track)


def xf(strokes, s=1.0, sy=None, dx=0.0, dy=0.0, rot=0.0):
    sy = s if sy is None else sy; c, n = np.cos(rot), np.sin(rot); out = []
    for p in strokes:
        q = p * [s, sy]; out.append(np.c_[q[:, 0] * c - q[:, 1] * n + dx, q[:, 0] * n + q[:, 1] * c + dy])
    return out


def dense(strokes, n=14):
    out = []
    for p in strokes:
        d = np.r_[0, np.cumsum(np.hypot(*np.diff(p, axis=0).T))]; u = np.linspace(0, d[-1] + 1e-9, max(2, n))
        out.append(np.c_[np.interp(u, d, p[:, 0]), np.interp(u, d, p[:, 1])])
    return out


def proj(p3, ry=0.0, rx=0.0, rz=0.0, cam=3.2, f=2.6, dz=0.0):
    p = np.asarray(p3, float); x, y, z = p[:, 0], p[:, 1], p[:, 2]
    x, z = x * np.cos(ry) + z * np.sin(ry), -x * np.sin(ry) + z * np.cos(ry)
    y, z = y * np.cos(rx) - z * np.sin(rx), y * np.sin(rx) + z * np.cos(rx)
    x, y = x * np.cos(rz) - y * np.sin(rz), x * np.sin(rz) + y * np.cos(rz)
    k = f / np.maximum(0.25, cam + z + dz)
    return np.c_[x * k, y * k]


def text3(strokes, **kw):
    return [proj(np.c_[p, np.zeros(len(p))], **kw) for p in dense(strokes, 8)]


def box(x, y, z, w, h, d):
    a = np.array([[x, y, z], [x + w, y, z], [x + w, y + h, z], [x, y + h, z], [x, y, z], [x, y, z + d], [x + w, y, z + d], [x + w, y, z], [x + w, y + h, z], [x + w, y + h, z + d], [x + w, y, z + d], [x + w, y + h, z + d], [x, y + h, z + d], [x, y, z + d], [x, y + h, z + d], [x, y + h, z]])
    return a


def circ(rad, n=64, z=0.0, cx=0.0, cy=0.0, frm=0.0, to=6.2832):
    u = np.linspace(frm, to, n); return np.c_[cx + rad * np.cos(u), cy + rad * np.sin(u), np.full(n, z)]


# ---------------- the scenes. Each is f(b) -> strokes, in world units (x -1.78 to 1.78, y -1 to 1)
LISS = [(1, 1), (1, 2), (2, 3), (3, 4), (3, 5), (5, 6)]
def s_dot(b):
    R = 0.0 if b < 1 else 0.8 * eb(r(b, 1, 1.6))
    a, c = LISS[min(len(LISS) - 1, max(0, int((b - 1) // 1)))]
    u = np.linspace(0, 6.2832, 700); ph = (b * 0.7) % 6.2832
    return [np.c_[R * 1.45 * np.sin(a * u + ph), R * np.sin(c * u)]]


def s_sphere(b):
    u = np.linspace(0, 1, 700); th = u * 3.1416; ph = u * 6.2832 * 11
    p = np.c_[np.sin(th) * np.cos(ph), np.cos(th), np.sin(th) * np.sin(ph)]
    k = 1.15 + 0.12 * np.cos(2 * 3.1416 * (b % 1))
    return [proj(p * k, ry=b * 0.9, rx=0.5 + 0.3 * np.sin(b * 0.7), rz=b * 0.2)]


ROWS = [("09:41", "PROMPT", "USE LAST YEAR'S MARGINS"), ("09:42", "TOOL.READ", "CONTRACTS/RENEWAL.PDF"), ("09:44", "OUTPUT", "THEY ASKED FOR 10 OFF")]
def row(i, b, b0, y, h=0.16):
    tm, ev, pay = ROWS[i]; n = 5 + len(ev) + len(pay)
    typed = int(r(b, b0, b0 + 1.6) * (n + 1))
    out = T(tm, -1.68, y, h, "l", n=typed) + T(ev, -0.72, y, h, "l", n=max(0, typed - 5))
    py = y - 0.24
    pt = dense(T(pay, -1.68, py, 0.13, "l", n=max(0, typed - 5 - len(ev))), 7)
    melt = eio(r(b, b0 + 2.6, b0 + 3.4))
    for p in pt:
        wave_y = py + 0.065 + 0.09 * np.sin(p[:, 0] * 26 + b * 6.283 * 0.5 + i) * (0.5 + 0.5 * np.sin(p[:, 0] * 3 + b * 2))
        out.append(np.c_[p[:, 0], p[:, 1] * (1 - melt) + wave_y * melt])
    return out


def s_rows(b):
    out = []
    out += T("DEMO DATA", 1.68, 0.86, 0.075, "r")
    for i, (b0, y) in enumerate(((8, 0.52), (11, -0.02), (14, -0.56))):
        if b >= b0: out += row(i, b, b0, y)
    return out


def s_big(a, c=None, top=0.22, h=None):
    def f(b):
        hit = np.exp(-(b % 1) * 7)
        out = fit(a, 0, top if c else -0.17, 3.15, maxh=0.52) + (fit(c, 0, -0.5, 3.15, maxh=0.52) if c else [])
        return text3(xf(out, 1 + 0.03 * hit), ry=0.22 * np.sin(b * 0.9), rx=0.08 * np.cos(b * 1.3), cam=2.6, f=2.6)
    return f


def s_dash(b):
    rot = -0.55 + (b - 24) * 0.11; rx = 0.32
    out = []
    H = [0.9, 0.7, 0.45, 1.15, 0.6]
    for i, h0 in enumerate(H):
        h = h0 * eb(r(b, 24.2 + i * 0.3, 24.9 + i * 0.3)) * (1 + 0.1 * np.sin(b * 3.14 + i)) + 1e-3
        out.append(proj(box(-1.6 + i * 0.42, -0.72, -0.14, 0.3, h, 0.28), ry=rot, rx=rx))
    ring = eo(r(b, 25.6, 27)); use = 0.64
    out.append(proj(circ(0.62, 40, 0.0, 0.92, 0.1), ry=rot, rx=rx))
    out.append(proj(circ(0.5, 40, 0.0, 0.92, 0.1, 1.57, 1.57 - 6.283 * use * ring), ry=rot, rx=rx))
    out += T("DEMO DATA", -1.68, 0.86, 0.075, "l")
    num = str(int(round(86 * eo(r(b, 26, 28)))))
    out += [proj(np.c_[p, np.full(len(p), 0.0)], ry=rot, rx=rx) for p in dense(T(num, 0.92, -0.08, 0.36), 7)]
    return out


def gate(ang, push=0.0, b=0.0, rot=0.0):
    out = []; W, H = 0.8, 0.82
    fr = np.array([[-W, -H, 0], [W, -H, 0], [W, H, 0], [-W, H, 0], [-W, -H, 0]])
    out.append(proj(fr, ry=rot, dz=-push))
    for side in (-1, 1):
        c, s = np.cos(ang), np.sin(ang)
        def door(x, y):   # hinged at the outer edge
            dx = x - side * W; return [side * W + dx * c, y, side * dx * s * 1.0]
        pts = []
        for k, xx in enumerate(np.linspace(0.0, 1.0, 5)):
            x = side * W * (1 - xx); pts += ([door(x, -H), door(x, H)] if k % 2 == 0 else [door(x, H), door(x, -H)])
        out.append(proj(np.array(pts), ry=rot, dz=-push))
        pts = []
        for k, yy in enumerate(np.linspace(-H, H, 5)):
            pts += ([door(side * W, yy), door(0, yy)] if k % 2 == 0 else [door(0, yy), door(side * W, yy)])
        out.append(proj(np.array(pts), ry=rot, dz=-push))
    return out


def s_gate(b):
    return gate(0.0, 0.0, b, rot=0.34 * np.sin((b - 34) * 0.55))


def s_gate_q(b):
    return xf(gate(0.0, 0.0, b, rot=0.0), 0.72, dy=0.26) + fit("APPROVE?", 0, -0.86, 2.0, maxh=0.34)


def s_gate_shut(b):
    k = 1 - eio(r(b, 40, 40.5))
    return xf(s_gate_q(39.9), max(k, 0.0))


def s_open(b):
    u = eo(r(b, 41, 42.2)); return gate(u * 1.9, 2.6 * eio(r(b, 41.1, 42.4)), b, rot=0.0)


def s_tunnel(b, mid=None):
    out = []; tw = b * 1.5
    pts = []
    for k in range(9):
        z = ((k - (b * 2.2) % 1) * 0.7)
        sq = np.array([[-1, -0.6], [1, -0.6], [1, 0.6], [-1, 0.6], [-1, -0.6]]) * 1.05
        a = tw + k * 0.11; c, s = np.cos(a), np.sin(a)
        for x, y in sq: pts.append([x * c - y * s, x * s + y * c, z])
    out.append(proj(np.array(pts), cam=0.7, f=1.15))
    return out + (mid or [])


def s_tunnel_ro(b):
    return s_tunnel(b, fit("READ-ONLY", 0, -0.12, 2.6, maxh=0.34) if b > 44 else None)


def s_full(b):
    return fit("FULL", 0, 0.14, 2.3, maxh=0.46) + fit("ACCESS", 0, -0.42, 2.3, maxh=0.46)


def s_x(b):
    k = 1 + 0.5 * np.exp(-(b - 48) * 6); q = 0.85 * k
    return fit("FULL", 0, 0.14, 2.3, maxh=0.46) + fit("ACCESS", 0, -0.42, 2.3, maxh=0.46) + [np.array([[-q * 1.5, -q], [q * 1.5, q]]), np.array([[q * 1.5, -q], [-q * 1.5, q]])]


def s_sieve(b):
    out = []
    for k in range(9):
        out.append(proj(np.array([[-2.2 + k * 0.55, -0.62, -1.2], [-2.2 + k * 0.55, -0.62, 1.8]]), cam=2.4, f=2.0))
        out.append(proj(np.array([[-2.2, -0.62, -1.2 + k * 0.38], [2.2, -0.62, -1.2 + k * 0.38]]), cam=2.4, f=2.0))
    for s, at in (("CREDENTIALS", 50.4), ("RAW LOGS", 52), ("LOCAL PATHS", 53.6)):
        d = b - at
        if d < 0 or d > 1.7: continue
        y = 1.1 - 2.2 * eio(cl(d / 1.1)) ** 1.5 - 0.5 * r(d, 1.1, 1.7)
        pts = dense(fit(s, 0, 0, 3.0, maxh=0.4), 9)
        for p in pts:
            q = p + [0, y]; below = np.clip(-0.5 - q[:, 1], 0, None); m = np.clip(below * 3.5, 0, 1)
            yy = q[:, 1] * (1 - m) + (-0.82 + 0.1 * np.sin(q[:, 0] * 20 + b * 4)) * m
            out.append(np.c_[q[:, 0], yy])
    return out


def s_keep(b):
    out = []
    for i, (s, y) in enumerate((("SOURCE CODE", 0.42), ("SAFETY DOCS", -0.1), ("PUBLIC DEMO", -0.62))):
        at = 55.2 + i * 0.7
        if b < at: continue
        out += xf(T(s, -0.3, y, 0.25), 1 + 0.2 * np.exp(-(b - at) * 8), dy=0)
        tk = r(b, at + 0.3, at + 0.55)
        if tk > 0: out.append(np.array([[1.1, y + 0.1], [1.1 + 0.1 * cl(tk * 2), y + 0.1 - 0.12 * cl(tk * 2)], [1.2 + 0.26 * cl(tk * 2 - 1), y - 0.02 + 0.3 * cl(tk * 2 - 1)]]))
    return out or [np.zeros((2, 2))]


def s_off(b):
    base = s_big("CHECKED BEFORE", "IT'S PUBLIC.")(59.9)
    sy = 1 - eio(r(b, 60, 60.45)); sx = 1 - eio(r(b, 60.5, 61))
    return xf(base, sx * 1.15, max(sy, 0.004))


def s_end(b):
    k = 1 - eio(r(b, 67.6, 68)); u = eo(r(b, 62.5, 63.2)); n = int(r(b, 63, 64) * 20)
    out = fit("CODEX CONTROL CENTER", 0, -0.14, 2.3 * u + 1e-3, maxh=0.2)
    out += T("AI.JOAOQUEIROS.COM", 0, -0.5, 0.15, n=n)
    if b > 64: out += T("OPEN SOURCE · MIT", 0, -0.78, 0.095, n=int(r(b, 64, 64.8) * 17))
    return xf(out, k)


# (from beat, scene, rate multiple, arpeggio on?)   each morphs out of the last over about half a beat
SCORE = [
    (0, s_dot, None, 0), (6, s_sphere, 2, 0), (8, s_rows, 0.5, 0),
    (18, s_big("SEES THE SHAPE"), 1, 0), (20, s_big("NOT THE WORDS"), 1, 0), (22, s_big("METADATA", "ONLY."), 1, 0),
    (24, s_dash, 1, 1), (30.5, s_big("NO API KEY", "TO OBSERVE."), 1, 0),
    (34, s_gate, 2, 0), (38, s_gate_q, 1, 0), (40, s_gate_shut, 2, 0),
    (41, s_open, 2, 1), (42.4, s_tunnel, 2, 1), (44, s_big("READ-ONLY"), 1, 0), (46, s_full, 1, 0), (48, s_x, 1, 0),
    (50, s_sieve, 1, 0), (55, s_keep, 1, 0), (58, s_big("CHECKED BEFORE", "IT'S PUBLIC."), 1, 0),
    (60, s_off, 2, 0), (62.2, s_end, 1, 0),
]
ROOT_HZ = [41.2, 32.7, 55.0, 61.74]    # E, C, A, B
ARP = [1, 1, 1.5, 1, 2, 1, 1.5, 2]


def sample(strokes, n):
    if not strokes: return np.zeros((n, 2))
    strokes = [p for p in strokes if len(p)]
    if not strokes: return np.zeros((n, 2))
    W = []
    for k, p in enumerate(strokes):
        if k: W.append(np.hypot(*(p[0] - strokes[k - 1][-1])) * 0.012 + 1e-5)    # pen up: the beam jumps almost at once
        W.extend(np.hypot(*np.diff(p, axis=0).T) + 1e-5)
    Q = np.concatenate(strokes); W.append(np.hypot(*(Q[-1] - Q[0])) * 0.012 + 1e-5)
    Q = np.r_[Q, Q[:1]]; u = np.r_[0, np.cumsum(W)]; v = (np.arange(n) + 0.5) / n * u[-1]
    return np.c_[np.interp(v, u, Q[:, 0]), np.interp(v, u, Q[:, 1])]


def scene_at(b):
    idx = 0
    for k, s in enumerate(SCORE):
        if b >= s[0]: idx = k
    return idx


xy = np.zeros((N, 2)); pos = 0; low = 1e9
while pos < N:
    b = pos / SR / BEAT; k = scene_at(b); _, fn, mul, arp = SCORE[k]
    root = ROOT_HZ[int(b // 4) % 4]
    if mul is None: f = 82.4 / LISS[min(len(LISS) - 1, max(0, int((b - 1) // 1)))][0]
    else: f = root * mul * (ARP[int(b * 2) % 8] if arp else 1)
    n = max(32, int(round(SR / f))); low = min(low, n)
    A = sample(fn(b), n)
    if k > 0 and b < SCORE[k][0] + 0.5 and fn is not s_off:   # morph out of the last scene
        m = eio((b - SCORE[k][0]) / 0.5); last = SCORE[k - 1][1]
        A = (1 - m) * sample(last(SCORE[k][0] - 1e-3), n) + m * A
    e = min(N, pos + n); xy[pos:e] = A[:e - pos]; pos = e

# ---------------- the drums, which are the picture being thrown about
t = np.arange(N) / SR
def kick(at, amp, d=0.09):
    i = int(at * SR); m = int(0.28 * SR); x = np.arange(m) / SR
    s = np.sin(2 * np.pi * (46 * x + 80 * (1 - np.exp(-x * 34)) / 34)) * np.exp(-x / d) * amp
    e = min(N, i + m); xy[i:e, 0] += s[:e - i]; xy[i:e, 1] += s[:e - i] * 0.7
def noise(at, amp, d):
    i = int(at * SR); m = int(d * 4 * SR); x = np.arange(m) / SR; s = rng.normal(size=(m, 2)) * (np.exp(-x / d) * amp)[:, None]
    e = min(N, i + m); xy[i:e] += s[:e - i]
pump = np.ones(N)
for bt in range(BEATS):
    on = 4 <= bt < 8 or 12 <= bt < 40 or 42 <= bt < 60
    if on:
        i = int(bt * BEAT * SR); m = int(0.36 * SR); e = min(N, i + m); x = np.arange(e - i) / SR
        pump[i:e] = np.minimum(pump[i:e], 1 - 0.09 * np.exp(-x / 0.08))
xy *= pump[:, None]
for bt in range(BEATS):
    on = 4 <= bt < 8 or 12 <= bt < 40 or 42 <= bt < 60
    if on: kick(bt * BEAT, 0.05)
    if on and bt >= 12 and bt % 2 == 1: noise(bt * BEAT, 0.012, 0.05)
    if on and bt >= 18:
        noise((bt + 0.5) * BEAT, 0.004, 0.012)
for at, a in ((41, 0.55), (48, 0.6), (46, 0.16), (6, 0.16), (8, 0.16), (18, 0.14), (24, 0.16), (34, 0.16), (50, 0.16), (58, 0.16)): kick(at * BEAT, a, 0.14)
i0, i1 = int(48 * BEAT * SR), int(50 * BEAT * SR)    # the refusal: a harsh buzz, so the X shakes
xy[i0:i1, 0] += 0.035 * np.sign(np.sin(2 * np.pi * 73.4 * t[i0:i1])) * np.exp(-(t[i0:i1] - t[i0]) * 1.1)
xy[i0:i1, 1] += 0.035 * np.sign(np.sin(2 * np.pi * 110 * t[i0:i1])) * np.exp(-(t[i0:i1] - t[i0]) * 1.1)
# round the corners a little, which also softens the buzz
for c in (0, 1): xy[:, c] = np.convolve(xy[:, c], [0.2, 0.6, 0.2], mode="same")

L = np.clip(xy[:, 0] / ASPECT * GAIN, -1, 1); R = np.clip(xy[:, 1] / ASPECT * GAIN, -1, 1)
pcm = (np.c_[L, R] * 32767).astype(np.int16)
os.makedirs(os.path.join(ROOT, "assets", "bgm"), exist_ok=True)
with wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
open(os.path.join(ROOT, "assets", "beam.js"), "w", encoding="ascii").write('window.BEAM = {gain:%f, b64:"%s"};\n' % (GAIN, base64.b64encode(pcm.tobytes()).decode("ascii")))
print("samples", N, "fewest samples in one redraw", low, "peak", float(np.abs(np.c_[L, R]).max()))
