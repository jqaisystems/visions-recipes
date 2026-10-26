"""
R20 · Cartographer. Original score, composed in code, timed to the film's one table (bake/table.json).

32 s in D minor, opening to D major as the route is ruled. A lamp hums on over a low drone and a breath of fog. The
survey ring sends a sonar ping on every turn of its beam while the relief rises as a patter of tiny taps that thickens
with the land. Each opportunity lands as a pluck over a pulse at 90 bpm (Dm, Bb, F, C); its three rings settle with a
soft shimmer, and each pin knocked flat is a muted thud. The ranked pins lift off as a rising line, one note per rank.
The dividers take a brass step on every stride; each phase opens on its own chord (D, G, A), the compass needle ticks
and settles with a bell. The relief settles with a low fall, the paper rolls with a long crackling swish, the ribbon is
tied, and the route writes the word over one wide D major chord.
Usage: python score/compose.py  ->  assets/bgm/score.wav   (numpy only, deterministic)
"""
import json
import os
import wave
import numpy as np

SR = 44100
DUR = 32.0
N = int(DUR * SR)
rng = np.random.default_rng(20)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "bgm", "score.wav")
TB = json.load(open(os.path.join(HERE, "..", "bake", "table.json"), encoding="utf-8"))
T, PINS, STRIDES = TB["T"], TB["pins"], TB["strides"]

L = np.zeros(N)
R = np.zeros(N)


def add(sig, start, pan=0.0, g=1.0):
    i0 = int(start * SR)
    if i0 >= N or i0 < 0:
        return
    sig = np.asarray(sig, dtype=float)[: N - i0] * g
    L[i0:i0 + len(sig)] += sig * np.sqrt(0.5 * (1 - pan))
    R[i0:i0 + len(sig)] += sig * np.sqrt(0.5 * (1 + pan))


def env(n, a, rel):
    e = np.ones(n)
    na = max(1, int(a * SR))
    e[:na] = np.linspace(0, 1, na)
    e[na:] = np.exp(-np.arange(n - na) / (rel * SR))
    k = min(n, int(0.01 * SR))
    e[-k:] *= np.linspace(1, 0, k)
    return e


def tone(f, dur, a=0.005, rel=0.3, harm=(1.0,), detune=0.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    return sum(h * np.sin(2 * np.pi * f * (k + 1) * t * (1 + detune * k)) for k, h in enumerate(harm)) * env(n, a, rel)


def lowpass(x, cutoff):
    # one-pole low-pass; cutoff may be a number or an array (a moving filter)
    cut = np.broadcast_to(np.asarray(cutoff, dtype=float), x.shape)
    a = np.exp(-2 * np.pi * cut / SR)
    y = np.zeros_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a[i]) * v + a[i] * acc
        y[i] = acc
    return y


def noise(dur, a=0.002, rel=0.05, cutoff=0):
    n = int(dur * SR)
    s = rng.standard_normal(n)
    if cutoff:
        s = lowpass(s, cutoff)
        s /= np.max(np.abs(s)) + 1e-9
    return s * env(n, a, rel)


def swish(dur, rise=False):
    n = int(dur * SR)
    t = np.arange(n) / SR
    shape = (t / dur) ** 2.2 if rise else np.sin(np.pi * t / dur) ** 2
    s = lowpass(rng.standard_normal(n), 2600 + 2400 * (t / dur if rise else 0)) * shape
    return s / (np.max(np.abs(s)) + 1e-9)


def bell(f, dur=2.6):
    return sum(h * tone(f * k, dur, a=0.001, rel=dur / (1 + 1.2 * i)) for i, (k, h) in enumerate(((1, 1.0), (2.0, 0.45), (2.76, 0.3), (5.4, 0.12))))


def click(g=1.0):
    # a brass detent: a bright transient over a short metallic ring
    s = 0.35 * tone(3150, 0.12, a=0.0005, rel=0.03, harm=(1, 0.4, 0.2))
    s[: int(0.03 * SR)] += lowpass(noise(0.03, a=0.0003, rel=0.004, cutoff=9000), 11000)
    return g * s


def knock(f=90, dur=0.35):
    return lowpass(tone(f, dur, a=0.001, rel=0.08, harm=(1, 0.5, 0.2)) + 0.5 * noise(dur, a=0.001, rel=0.02, cutoff=1500), 2000)


hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
pan_x = lambda x: max(-0.9, min(0.9, x / 7))
tt = np.arange(N) / SR

# ---- the lamp hums on; a low D drone; a breath of fog until the audit clears it
add(lowpass(np.sin(2 * np.pi * 100 * tt) + 0.4 * np.sin(2 * np.pi * 200 * tt), 400) * np.clip((tt - T["lamp"][0]) / 1.2, 0, 1) * np.exp(-np.clip(tt - 1.6, 0, None) * 0.9), 0, -0.3, 0.02)
add(click(0.9), T["lamp"][0], -0.4, 0.08)
drone = sum(a * np.sin(2 * np.pi * f * tt * (1 + d)) for f, a in ((hz(38), 1.0), (hz(50), 0.55), (hz(57), 0.25)) for d in (-0.0012, 0.0012))
add(lowpass(drone, 650) * np.minimum(1, tt / 2.0) * np.clip((T["roll"][1] + 1.0 - tt) / 1.4, 0, 1), 0, 0, 0.06)
fn = int((T["audit"][1] + 0.5) * SR); ft = np.arange(fn) / SR
add(lowpass(rng.standard_normal(fn), 900) * np.minimum(1, ft / 1.5) * np.clip((T["audit"][1] + 0.5 - ft) / 1.2, 0, 1), 0, 0, 0.022)
pn = int(T["audit"][1] * SR); pt = np.arange(pn) / SR
pad = sum(np.sin(2 * np.pi * hz(m) * pt * (1 + d)) for m in (62, 65, 69) for d in (-0.002, 0.002))
add(lowpass(pad, 300 + 2200 * np.clip((pt - T["audit"][0]) / (T["audit"][1] - T["audit"][0]), 0, 1) ** 1.4) * np.minimum(1, pt / 2.0) * np.minimum(1, (T["audit"][1] - pt) / 0.8), 0, 0, 0.03)

# ---- the survey: a ping on every turn of the beam, the land rising as a patter of taps
turn = (T["audit"][1] - T["audit"][0]) / TB["sweepTurns"]
for k in range(TB["sweepTurns"]):
    t0 = T["audit"][0] + k * turn
    add(bell(hz(81), 2.4), t0, 0.0, 0.06)
    add(bell(hz(93), 1.2), t0, 0.0, 0.03)
    add(tone(hz(69), 1.8, a=0.002, rel=0.9, harm=(1, 0.2)), t0 + 0.32, 0.3, 0.03)       # the echo
add(swish(T["audit"][1] - T["audit"][0], rise=True), T["audit"][0], 0, 0.03)
rt = T["audit"][0]
while rt < T["audit"][1] + 0.3:
    u = min(1.0, (rt - T["audit"][0]) / (T["audit"][1] - T["audit"][0]))
    add(tone(1800 + 2600 * rng.random(), 0.04, a=0.0004, rel=0.008), rt, rng.uniform(-0.8, 0.8), 0.006 + 0.004 * rng.random())
    rt += rng.exponential(1 / (6 + 70 * np.sin(np.pi * u) ** 1.5))
add(knock(70, 0.6), T["audit"][1] - 0.05, 0, 0.1)
add(tone(hz(38), 1.6, a=0.004, rel=0.5, harm=(1, 0.4)), T["audit"][1] - 0.05, 0, 0.08)

# ---- the opportunities: a pulse at 90 bpm over Dm, Bb, F, C; each pin lands as a pluck, its rings shimmer
BEAT = 60 / 90
CH = [[38, 62, 65, 69], [34, 62, 65, 70], [41, 60, 65, 69], [36, 60, 64, 67]]
t0, k = T["pins"] - 0.3, 0
while t0 < T["dividers"] - 0.2:
    ch = CH[k % 4]
    add(lowpass(sum(tone(hz(m), 4 * BEAT + 0.8, a=0.3, rel=1.2) for m in ch[1:]), 1700), t0, 0, 0.02)
    for b in range(4):
        add(lowpass(tone(hz(ch[0]), 0.4, a=0.004, rel=0.14, harm=(1, 0.3)), 420), t0 + b * BEAT, 0, 0.09)
        add(click(0.22), t0 + b * BEAT + BEAT / 2, -0.4, 0.04)
    t0 += 4 * BEAT; k += 1
SCALE = [62, 65, 67, 69, 72, 74, 77, 79, 81, 84, 86, 89]
for j, p in enumerate(sorted(PINS, key=lambda q: q["drop"])):
    add(tone(hz(SCALE[j]), 0.7, a=0.002, rel=0.2, harm=(1, 0.45, 0.15)), p["drop"], pan_x(p["x"]), 0.045)
    add(knock(140, 0.18), p["drop"], pan_x(p["x"]), 0.04)
    for q in range(3):                                                    # payoff, cost, risk settle
        add(tone(hz(SCALE[j] + 24 + [0, 4, 7][q]), 0.3, a=0.002, rel=0.08), p["drop"] + 0.08 + 0.1 * q, pan_x(p["x"]), 0.008)
for p in PINS:
    if not p["rank"]:
        add(knock(85, 0.45), p["knock"] + 0.18, pan_x(p["x"]), 0.14)
        add(knock(120, 0.2), p["knock"] + 0.38, pan_x(p["x"]), 0.06)     # the bounce
        add(tone(hz(45), 0.8, a=0.005, rel=0.25, harm=(1, 0.3)), p["knock"] + 0.18, pan_x(p["x"]), 0.04)

# ---- ranked: a rising line, one note per rank as each pin lifts off; a tick as each tag swings in
for p in sorted([q for q in PINS if q["rank"]], key=lambda q: q["rank"]):
    pan = -0.6 + 0.17 * p["rank"]
    add(swish(0.6), p["rankT"], pan, 0.02)
    add(bell(hz([62, 65, 69, 72, 74, 77, 81, 84][p["rank"] - 1]), 1.4), p["rankT"] + 0.95, pan, 0.04)
    add(click(0.5), T["tags"] + 0.15 * (p["rank"] - 1), pan, 0.04)

# ---- the route: a brass step on every stride; each phase opens on its chord (D, G, A); the compass settles
add(swish(0.5), T["dividers"], 0.2, 0.04)
for st in STRIDES:
    add(click(0.7), st[1] - 0.01, 0.2, 0.06)
    add(lowpass(tone(hz(50), 0.25, a=0.002, rel=0.06), 600), st[1] - 0.01, 0, 0.05)
PCH = [[50, 62, 66, 69, 74], [43, 59, 62, 67, 71], [45, 61, 64, 69, 73]]
for k, (a, b) in enumerate(T["legs"]):
    add(lowpass(sum(tone(hz(m), b - a + 1.4, a=0.08, rel=1.1) for m in PCH[k][1:]), 2400), a - 0.05, -0.3 + 0.3 * k, 0.035)
    add(tone(hz(PCH[k][0]), b - a + 1.2, a=0.02, rel=0.9, harm=(1, 0.4)), a - 0.05, 0, 0.09)
    add(bell(hz(PCH[k][-1] + 12), 2.0), b, 0, 0.04)
cs = T["compass"][0]
for k in range(7):
    add(tone(3600 - 120 * k, 0.05, a=0.0005, rel=0.012), cs + 0.09 * k * (1 + 0.25 * k), -0.5, 0.02 * (1 - k / 8))
add(bell(hz(86), 2.2), T["compass"][1] - 0.05, -0.4, 0.05)

# ---- the roadmap: the land settles, the paper rolls with a crackle, the ribbon is tied
add(swish(T["sink"][1] - T["sink"][0] + 0.4), T["sink"][0], 0, 0.05)
add(tone(hz(38), 2.0, a=0.05, rel=0.8, harm=(1, 0.5)), T["sink"][0], 0, 0.07)
add(swish(T["roll"][1] - T["roll"][0]), T["roll"][0], 0, 0.06)
ct = T["roll"][0]
while ct < T["roll"][1]:
    add(noise(0.012, a=0.0005, rel=0.004, cutoff=6000), ct, rng.uniform(-0.5, 0.5), 0.02 + 0.03 * rng.random())
    ct += rng.exponential(1 / 55)
add(knock(95, 0.3), T["roll"][1], 0.1, 0.08)
add(swish(0.4), T["tie"][0], -0.3, 0.05)
add(click(1.0), T["tie"][0] + 0.25, -0.3, 0.07)
add(knock(70, 0.4), T["tie"][1] - 0.1, -0.3, 0.08)

# ---- the route writes the word; one wide D major chord holds it
for k in range(40):
    add(tone(hz([74, 78, 81, 85, 86, 90][k % 6] + 12), 0.4, a=0.002, rel=0.09), T["word"][0] + 1.4 * k / 40, -0.8 + 1.6 * ((k * 5) % 11) / 10, 0.016)
add(swish(1.6, rise=True), T["word"][0] - 0.3, 0, 0.035)
for j, m in enumerate([74, 78, 81]):
    add(bell(hz(m + 12), 3.6), T["word"][1] - 0.4 + 0.16 * j, -0.3 + 0.3 * j, 0.05)
for j, m in enumerate([38, 50, 57, 62, 66, 69, 73, 76, 81]):
    add(tone(hz(m), DUR - T["word"][1] + 0.4, a=0.04, rel=2.0, harm=(1, 0.3, 0.1), detune=0.0007), T["word"][1] - 0.4, -0.6 + 0.15 * j, 0.085)

# ---- master: a soft-clip that lifts the body and keeps the peaks round, then a fade at the very end
mix = np.stack([L, R], axis=1)
mix /= np.max(np.abs(mix))
DRIVE = 2.4
mix = np.tanh(mix * DRIVE) / np.tanh(DRIVE) * 0.84
fade = int(0.8 * SR)
mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
data = (mix * 32767).astype("<i2").tobytes()
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with wave.open(OUT, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data)
print("wrote", os.path.normpath(OUT), DUR, "s")
