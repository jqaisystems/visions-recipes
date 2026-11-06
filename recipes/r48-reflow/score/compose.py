"""The score for R48 · Reflow, composed in code at 112 bpm in F major and bouncy: pizzicato strings, a tuba, hand claps and a slide whistle that climbs
as the page gets narrower, with a wet squelch on each column change. The grey sites get only woodblocks: the band arrives with the colour. One held
breath before the walls. Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py"""
import json, math, os, re, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TB = json.loads(re.sub(r"^window\.TABLE=|;\s*$", "", open(os.path.join(ROOT, "assets", "table.js"), encoding="utf-8").read()))
SR = 48000; DUR = TB["dur"]; BEAT = TB["beat"]; N = int(SR * DUR); rng = np.random.default_rng(48)
B = lambda x: x * BEAT
out = np.zeros((N, 2))


def add(at, sig, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N or i < 0: return
    sig = sig[:N - i]
    out[i:i + len(sig), 0] += sig * gain * math.cos((pan + 1) * math.pi / 4) * 1.41
    out[i:i + len(sig), 1] += sig * gain * math.sin((pan + 1) * math.pi / 4) * 1.41


def midi(m): return 440 * 2 ** ((m - 69) / 12)


_c = {}
def pizz(m, dur=0.5):
    """A plucked string: a little Karplus-Strong, so each note has a real pluck."""
    k = (m, dur)
    if k not in _c:
        n = int(dur * SR); p = max(2, int(SR / midi(m))); buf = np.random.default_rng(m).uniform(-1, 1, p); x = np.zeros(n)
        for i in range(n):
            x[i] = buf[i % p]; buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.992
        _c[k] = x * np.minimum(1, (dur - np.arange(n) / SR) * 30)
    return _c[k]


def tuba(m, dur=0.42):
    t = np.arange(int(dur * SR)) / SR; f = midi(m) * (1 + 0.03 * np.exp(-t * 30))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) + 0.55 * np.sin(2 * ph) + 0.3 * np.sin(3 * ph) + 0.14 * np.sin(4 * ph)
    return x * np.minimum(1, t * 70) * np.minimum(1, (dur - t) * 22) * (0.8 + 0.2 * np.exp(-t * 8))


def clap(seed=0):
    g = np.random.default_rng(seed); n = int(0.14 * SR); t = np.arange(n) / SR; x = g.normal(0, 1, n)
    x = x - np.convolve(x, np.ones(8) / 8, "same")
    e = np.exp(-t * 34) + 0.6 * np.exp(-np.maximum(t - 0.012, 0) * 60) * (t > 0.012) + 0.5 * np.exp(-np.maximum(t - 0.024, 0) * 60) * (t > 0.024)
    return x * e


def block(f=1250.0, dec=46.0, dur=0.09):
    t = np.arange(int(dur * SR)) / SR
    return (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.42 * t)) * np.exp(-t * dec) * np.minimum(1, t * 3000)


def squelch(dur=0.42, f0=240.0, f1=70.0, seed=0):
    t = np.arange(int(dur * SR)) / SR; g = np.random.default_rng(seed)
    f = f0 * (f1 / f0) ** (t / dur) * (1 + 0.16 * np.sin(2 * np.pi * 27 * t))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR)
    n = g.normal(0, 1, len(t)); w = 40; n = np.convolve(n, np.ones(w) / w, "same") * 2.2
    return (x + 0.55 * n) * np.exp(-t * 7 / dur * 0.6) * np.minimum(1, t * 300) * np.minimum(1, (dur - t) * 60)


def thud(f=62.0, dur=0.7, drop=2.2):
    t = np.arange(int(dur * SR)) / SR
    p = 2 * np.pi * np.cumsum(f * (1 + drop * np.exp(-t * 34))) / SR
    return np.sin(p) * np.exp(-t * 6.0) * np.minimum(1, t * 800)


def whistle(f0, f1, dur, seed=0):
    """A slide whistle: a breathy sine that glides, with a little vibrato."""
    t = np.arange(int(dur * SR)) / SR; g = np.random.default_rng(seed)
    f = f0 * (f1 / f0) ** (np.minimum(t / dur, 1) ** 0.8) * (1 + 0.006 * np.sin(2 * np.pi * 6 * t))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR); n = g.normal(0, 1, len(t)); n = np.convolve(n, np.ones(6) / 6, "same")
    return (x + 0.05 * n) * np.minimum(1, t * 40) * np.minimum(1, (dur - t) * 30)


def boing(f=120.0, dur=0.9):
    t = np.arange(int(dur * SR)) / SR
    f2 = f * (1 + 0.5 * np.sin(2 * np.pi * 11 * t) * np.exp(-t * 5))
    return np.sin(2 * np.pi * np.cumsum(f2) / SR) * np.exp(-t * 4.2) * np.minimum(1, t * 300)


CH = {"F": [41, 53, 60, 65, 69, 72, 77], "Dm": [38, 50, 57, 62, 65, 69, 74], "Bb": [46, 53, 58, 62, 65, 70, 74], "C": [36, 48, 55, 60, 64, 67, 72]}
PROG = ["F", "Dm", "Bb", "C"]
def chord_at(b): return PROG[int(b // 4) % 4]


def band(b0, b1, claps=True, pz=True, level=1.0):
    """Oom-pah: tuba on one and three, pizzicato on the offbeats, claps on two and four."""
    for b in np.arange(math.ceil(b0), b1, 1.0):
        ch = CH[chord_at(b)]
        if b % 2 == 0: add(B(b), tuba(ch[0] + (12 if b % 4 == 2 else 12), 0.36), 0.3 * level); add(B(b), thud(58, 0.2, 1.6), 0.26 * level)
        elif claps: add(B(b), clap(int(b)), 0.16 * level, 0.1)
        if pz:
            k = int(b)
            add(B(b + 0.5), pizz(ch[2 + k % 3] + 12), 0.2 * level, -0.25)
            if k % 2 == 1: add(B(b + 0.75), pizz(ch[3 + (k // 2) % 3] + 12), 0.15 * level, 0.3)


# ---- 1. the brand: three lumps, three notes
for i, b in enumerate(TB["drops"]):
    n = int(0.22 * SR); add(B(b) - 0.22, whistle(1500 - i * 90, 500, 0.22, i), 0.05)
    add(B(b), thud(60 + i * 4), 0.85); add(B(b), squelch(0.4, 180 + i * 20, 62, 1 + i), 0.3)
    add(B(b), pizz([53, 57, 60][i], 0.7), 0.42, [-0.4, 0, 0.4][i])
band(TB["drops"][2] + 0.9, TB["row"], claps=False, level=0.7)
# ---- 2. not a template: everything colourless and mechanical. A tick and a low note per site
add(B(TB["row"]), squelch(0.5, 200, 80, 9), 0.26)
for i in range(TB["sites"]):
    b = TB["stamp"] + i * TB["stampGap"]
    add(B(b + 0.12), block(980, 50), 0.26, -0.5 + i * 0.12); add(B(b + 0.12), thud(72, 0.18, 1.4), 0.3)
# the dominoes: a run of clicks that speeds up, then a flop
add(B(TB["hit"]), thud(55, 0.7, 2.4), 0.8); add(B(TB["hit"]), squelch(0.34, 190, 70, 11), 0.3)
for i in range(TB["sites"]):
    u = (i + 1) / TB["sites"]; b = TB["hit"] + i * TB["topple"] * (1 - 0.2 * u)
    add(B(b + 0.34), block(1200 + 120 * i, 48), 0.32, -0.6 + 1.2 * u)
add(B(TB["hit"] + TB["sites"] * TB["topple"] + 0.3), thud(50, 0.5, 2.0), 0.5)
# ---- 3. the wire: the slab, then a rising pluck as each coil draws
add(B(TB["wire"]), squelch(0.55, 120, 240, 14), 0.3)
for k, b in enumerate(np.arange(TB["draw"], TB["drawEnd"], 0.25)):
    ch = CH[chord_at(b)]; add(B(b), pizz(ch[1 + k % 6] + 12, 0.35), 0.13 + 0.008 * k, 0.5 * math.sin(k * 0.8))
for b in np.arange(TB["draw"], TB["drawEnd"], 2.0): add(B(b), tuba(CH[chord_at(b)][0] + 12, 0.5), 0.2)
# ---- 4. the colour lands, and the band with it
for i, b in enumerate(TB["blobs"]):
    add(B(b), thud(66, 0.34, 2.0), 0.5); add(B(b), squelch(0.5, 150, 420, 20 + i), 0.24, [-0.3, 0, 0.3][i])
    add(B(b), pizz([65, 69, 72][i] + 12, 0.6), 0.34, [-0.3, 0, 0.3][i])
band(TB["blobs"][2] + 0.5, TB["breath"] - 0.3)
# ---- 5. the squeeze
n1 = TB["slam1"] - 0.5; add(B(n1), whistle(420, 620, B(0.5), 30), 0.1)
for j, (b, m) in enumerate(((TB["slam1"], (41, 53, 60, 65, 72)), (TB["slam2"], (46, 58, 65, 70, 77)))):
    add(B(b), thud(46, 1.2, 3.2), 1.2); add(B(b), squelch(0.65, 170, 46, 31 + j), 0.5)
    for m2 in m: add(B(b), pizz(m2 + 12, 0.8), 0.2)
    add(B(b), tuba(m[0] + 12, 0.8), 0.34)
    add(B(b + 0.1), squelch(0.28, 320, 120, 33 + j), 0.22, -0.5); add(B(b + 0.22), squelch(0.28, 360, 130, 35 + j), 0.22, 0.5)
    add(B(b), whistle(620 + j * 340, 960 + j * 480, B(1.1), 37 + j), 0.13)
band(TB["slam1"] + 1.5, TB["release"] - 0.5, level=0.95)
for b in np.arange(TB["slam2"] + 1, TB["release"] - 0.5, 0.5): add(B(b), block(2100, 90, 0.04), 0.08, 0.3)
add(B(TB["release"] - 0.5), whistle(1450, 2100, B(0.5), 40), 0.13)
add(B(TB["release"]), whistle(2100, 260, B(1.2), 41), 0.14)
add(B(TB["release"] + 0.2), boing(112, 1.1), 0.58); add(B(TB["release"] + 0.15), squelch(0.5, 110, 330, 42), 0.3)
# ---- 6. the real thing: a tiny band, a click, and a pop
band(TB["release"] + 1.75, TB["press"] - 0.2, claps=False, level=0.62)
add(B(TB["press"]), block(2600, 110, 0.05), 0.42); add(B(TB["press"]), squelch(0.25, 300, 720, 43), 0.3)
for j, m in enumerate((72, 77, 81, 84)): add(B(TB["press"] + 0.25 + j * 0.25), pizz(m, 0.5), 0.3, -0.3 + j * 0.2)
band(TB["press"] + 1.25, TB["turn"])
# ---- 7. the plumbing: a tuba glide round the back, then gurgles along the pipes
n = int(B(TB["turnEnd"] - TB["turn"]) * SR); t = np.arange(n) / SR
gl = np.sin(2 * np.pi * np.cumsum(midi(41) * 1.35 ** (t / t[-1])) / SR); add(B(TB["turn"]), (gl + 0.4 * np.sign(gl) * 0.25) * np.sin(np.linspace(0, np.pi, n)) ** 0.6, 0.3)
add(B(TB["turnEnd"]), thud(55, 0.5, 2.0), 0.6)
for b in np.arange(TB["pipes"], TB["fold"], 0.25):
    add(B(b), squelch(0.16, 170 + 110 * ((b * 4) % 3), 420 + 130 * ((b * 8) % 3), int(b * 7)), 0.14, 0.7 * math.sin(b * 2.3))
band(TB["turnEnd"] + 0.5, TB["fold"], claps=False, pz=False, level=0.95)
for b in np.arange(TB["turnEnd"] + 0.5, TB["fold"], 1.0): add(B(b + 0.5), pizz(CH[chord_at(b)][2 + int(b) % 3], 0.5), 0.2, -0.2)
# ---- 8. yours: the page goes in, the flap shuts, and the last chord
add(B(TB["fold"]), whistle(900, 300, B(1.4), 50), 0.08); add(B(TB["fold"]), squelch(0.6, 240, 90, 51), 0.26)
band(TB["fold"] + 1.5, TB["shut"] - 0.3, level=0.85)
add(B(TB["shut"]), thud(48, 1.1, 2.8), 1.1); add(B(TB["shut"]), squelch(0.5, 150, 56, 52), 0.42)
band(TB["shut"] + 0.5, TB["logo"] - 0.9, level=0.95)
n = int(B(1.0) * SR); add(B(TB["logo"] - 1.0), np.sin(2 * np.pi * np.cumsum(np.linspace(48, 36, n)) / SR) * np.linspace(0, 1, n) ** 2, 0.26)
add(B(TB["logo"]), thud(44, 1.0, 2.6), 0.9)
add(B(TB["logo"]), tuba(41, 2.2), 0.36)
for j, m in enumerate((53, 60, 65, 69, 72, 77, 81)): add(B(TB["logo"]) + j * 0.035, pizz(m, 1.8), 0.28, -0.45 + j * 0.15)

# a small room
ir = np.zeros(int(0.32 * SR))
for k, (ms, g) in enumerate(((13, 0.3), (23, 0.24), (37, 0.2), (53, 0.13), (79, 0.09), (113, 0.05), (167, 0.03))):
    ir[int(ms * SR / 1000)] = g
for ch in range(2):
    wet = np.convolve(out[:, ch], np.roll(ir, ch * 31))[:N]
    out[:, ch] += wet * 0.5
# the breath: nothing but a held room tone until the walls
i0, i1, i2 = int(B(TB["breath"] - 0.25) * SR), int(B(TB["breath"]) * SR), int(B(TB["slam1"] - 0.52) * SR)
env = np.ones(N); env[i0:i1] = np.linspace(1, 0.02, i1 - i0); env[i1:i2] = 0.02; out *= env[:, None]
i3 = int(B(TB["beats"] - 0.8) * SR); out[i3:] *= np.linspace(1, 0, N - i3)[:, None] ** 2
out = np.tanh(out * 0.95)
pk = np.max(np.abs(out)); out = out / pk * 0.72
os.makedirs(os.path.join(ROOT, "assets", "bgm"), exist_ok=True)
w = wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
print("score", round(DUR, 3), "peak", float(pk))
