"""
R21 · Kitted. Original score, composed in code, timed to the film's one table (bake/table.json).

32 s in E minor, opening to E major under the word. A work light clunks and flickers on over a fluorescent hum and a
low drone, with the odd clatter from the pile. The audit is a scanner tone gliding across the bench: a bright blip for
each tool that stays, a low buzz for each thing that does not, and every binned piece lands in the bin with a clang.
The kept tools rise on a swell; the case slides in with a thump and its lid opens on a latch. A 100 bpm groove starts
under the laser (Em, C, G, D): the beam is a filtered hiss that follows each cut, crackling, and every plug pops out.
Each tool clicks into its cutout on the beat with one note of a rising arpeggio and a shimmer as its name lights. The
prompt cards riffle in. Each bench's light clunks on, the cases open together on a chord, and every job starts with a
chime and ticks along. The playbook lands with a soft thud, the laser hisses through the word, and one wide E major
chord holds it.
Usage: python score/compose.py  ->  assets/bgm/score.wav   (numpy only, deterministic)
"""
import json
import os
import wave
import numpy as np

SR = 44100
DUR = 32.0
N = int(DUR * SR)
rng = np.random.default_rng(21)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "bgm", "score.wav")
TB = json.load(open(os.path.join(HERE, "..", "bake", "table.json"), encoding="utf-8"))
T, TOOLS, BOOK, EXTRAS, BENCHES = TB["T"], TB["tools"], TB["book"], TB["extras"], TB["benches"]

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


def highpass(x, cutoff):
    return x - lowpass(x, cutoff)


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


def click(g=1.0, f=3150):
    # a steel detent: a bright transient over a short metallic ring
    s = 0.35 * tone(f, 0.12, a=0.0005, rel=0.03, harm=(1, 0.4, 0.2))
    s[: int(0.03 * SR)] += lowpass(noise(0.03, a=0.0003, rel=0.004, cutoff=9000), 11000)
    return g * s


def knock(f=90, dur=0.35):
    return lowpass(tone(f, dur, a=0.001, rel=0.08, harm=(1, 0.5, 0.2)) + 0.5 * noise(dur, a=0.001, rel=0.02, cutoff=1500), 2000)


def clang(f=420, dur=0.9):
    # a thin steel bin struck: inharmonic partials that ring and die
    s = sum(h * tone(f * k, dur, a=0.0008, rel=dur / (1.5 + 2 * i)) for i, (k, h) in enumerate(((1, 1.0), (1.59, 0.6), (2.31, 0.45), (3.7, 0.25))))
    hit = noise(0.04, a=0.0005, rel=0.01, cutoff=7000)
    s[: len(hit)] += 0.4 * hit
    return s


def kick():
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    f = 48 + 90 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def hat(g=1.0):
    return g * highpass(noise(0.05, a=0.0005, rel=0.012), 6000)


def hiss(dur, bright=1.0):
    # the laser: a band of noise with a thin high whistle riding on it
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = highpass(lowpass(rng.standard_normal(n), 7000), 1800) * 0.6
    s += 0.25 * np.sin(2 * np.pi * (2350 + 60 * np.sin(2 * np.pi * 7 * t)) * t) * bright
    e = np.minimum(1, t / 0.03) * np.minimum(1, (dur - t) / 0.05)
    return s * np.clip(e, 0, 1)


hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
pan_x = lambda x: max(-0.9, min(0.9, x / 5))
tt = np.arange(N) / SR

# ---- the work light: a clunk, a flicker, then a fluorescent hum; a low E drone; the pile settling
add(knock(70, 0.5), T["light"][0], -0.2, 0.12)
for k, ft in enumerate([0.2, 0.32, 0.44, 0.52]):
    add(click(0.6, 2200 + 300 * k), ft, -0.2, 0.05)
hum = (np.sin(2 * np.pi * 120 * tt) + 0.5 * np.sin(2 * np.pi * 240 * tt) + 0.2 * np.sin(2 * np.pi * 360 * tt))
add(lowpass(hum, 900) * np.clip((tt - T["light"][1]) / 0.3, 0, 1) * np.clip((T["word"][1] + 1.5 - tt) / 2.0, 0, 1), 0, 0.1, 0.012)
drone = sum(a * np.sin(2 * np.pi * f * tt * (1 + d)) for f, a in ((hz(28), 1.0), (hz(40), 0.6), (hz(47), 0.25)) for d in (-0.0012, 0.0012))
add(lowpass(drone, 600) * np.minimum(1, tt / 2.0) * np.clip((T["word"][0] + 0.5 - tt) / 1.5, 0, 1), 0, 0, 0.05)
for k in range(9):                                                   # the odd clatter from the pile
    add(click(0.3, 1800 + 1400 * rng.random()), 0.9 + 2.7 * rng.random(), rng.uniform(-0.6, 0.6), 0.03)

# ---- the audit: a scanner glides across; a blip for every tool that stays, a buzz for what goes
an = int((T["audit"][1] - T["audit"][0]) * SR); at = np.arange(an) / SR
glide = 900 + 900 * at / at[-1]
add(np.sin(2 * np.pi * np.cumsum(glide) / SR) * np.sin(np.pi * at / at[-1]) ** 0.5, T["audit"][0], 0, 0.012)
add(swish(T["audit"][1] - T["audit"][0], rise=True), T["audit"][0], 0, 0.02)
KEEP = [64, 67, 71, 74, 76, 79, 83]
for j, tl in enumerate(sorted(TOOLS, key=lambda q: q["tagT"])):
    add(tone(hz(KEEP[j] + 12), 0.5, a=0.002, rel=0.12, harm=(1, 0.3)), tl["tagT"], pan_x(tl["heapPos"][0]), 0.05)
for e in EXTRAS:
    if e["label"]:
        add(lowpass(tone(hz(40), 0.22, a=0.004, rel=0.08, harm=(1, 0.8, 0.6, 0.4)), 1200), e["tagT"], pan_x(e["heapPos"][0]), 0.05)
for e in EXTRAS:                                                     # off the edge and into the bin
    add(swish(0.35), e["binT"], 0.6, 0.015)
    add(clang(300 + 220 * rng.random(), 0.8), e["binT"] + 0.85, 0.75, 0.04)

# ---- the kept tools rise and hover; the case slides in and its lid opens
add(swish(1.2, rise=True), T["hover"][0], 0, 0.035)
pn = int(2.6 * SR); pt = np.arange(pn) / SR
add(lowpass(sum(np.sin(2 * np.pi * hz(m) * pt * (1 + d)) for m in (64, 67, 71, 76) for d in (-0.002, 0.002)), 1600) * np.minimum(1, pt / 0.8) * np.exp(-np.clip(pt - 1.2, 0, None) * 2), T["hover"][0], 0, 0.02)
add(swish(0.8), T["caseIn"][0], 0.7, 0.05)
add(knock(65, 0.5), T["caseIn"][1] - 0.05, 0.2, 0.14)
add(click(1.0, 1900), T["lid"][0] + 0.1, 0, 0.06)
add(knock(110, 0.25), T["lid"][1], 0, 0.06)
hn = int((T["headIn"][1] - T["headIn"][0]) * SR); ht = np.arange(hn) / SR   # the head comes down on a servo
add(np.sin(2 * np.pi * np.cumsum(600 - 200 * ht / ht[-1]) / SR) * 0.5, T["headIn"][0], 0, 0.02)

# ---- a groove at 100 bpm from the lid to the end of onboarding: kick, hats, a bass line over Em, C, G, D
BEAT = T["beat"]
G0 = T["install"] - 8 * BEAT
CH = [[40, 64, 67, 71], [36, 64, 67, 72], [43, 62, 67, 71], [38, 62, 66, 69]]
nb = int(round((T["jobsEnd"] - G0) / BEAT))
for b in range(nb):
    t0 = G0 + b * BEAT
    ch = CH[(b // 4) % 4]
    add(kick(), t0, 0, 0.16 if b % 2 == 0 else 0.11)
    add(hat(), t0 + BEAT / 2, 0.3, 0.025)
    add(hat(0.6), t0 + BEAT * 0.75, -0.3, 0.015)
    add(lowpass(tone(hz(ch[0]), BEAT * 0.9, a=0.004, rel=0.18, harm=(1, 0.5, 0.2)), 500), t0, 0, 0.09)
    if b % 4 == 0:
        add(lowpass(sum(tone(hz(m), 4 * BEAT + 0.6, a=0.25, rel=1.0) for m in ch[1:]), 1500 if t0 < T["lights"][0] else 2600), t0, 0, 0.02 if t0 < T["lights"][0] else 0.03)

# ---- the laser: a hiss that follows each cut, crackling; every plug pops out
for c in TOOLS + [BOOK]:
    a, b = c["cutT"]
    add(hiss(b - a, 1.0 if c is TOOLS[0] else 0.7), a, pan_x(c["fit"][0]), 0.05)
    ct = a
    while ct < b:
        add(noise(0.008, a=0.0004, rel=0.003, cutoff=8000), ct, pan_x(c["fit"][0]) + rng.uniform(-0.2, 0.2), 0.03 + 0.03 * rng.random())
        ct += rng.exponential(1 / 70)
    add(tone(hz(88), 0.12, a=0.001, rel=0.03) + 0.6 * noise(0.12, a=0.001, rel=0.015, cutoff=3000), b + 0.02, pan_x(c["fit"][0]), 0.05)   # the pop
    add(lowpass(noise(0.5, a=0.02, rel=0.2), 1400), b + 0.05, pan_x(c["fit"][0]), 0.02)                                               # the puff

# ---- installed: each tool clicks in on the beat with a note of a rising arpeggio; its name lights with a shimmer
ARP = [64, 67, 71, 76, 79, 83, 88]
for j, tl in enumerate(TOOLS):
    p = pan_x(tl["fit"][0])
    add(click(1.0, 2800), tl["dropT"], p, 0.09)
    add(knock(150, 0.15), tl["dropT"], p, 0.05)
    add(tone(hz(ARP[j]), 0.9, a=0.002, rel=0.3, harm=(1, 0.4, 0.15)), tl["dropT"], p, 0.05)
    for q in range(4):
        add(tone(hz(ARP[j] + 24 + [0, 7, 12, 19][q]), 0.25, a=0.002, rel=0.07), tl["dropT"] + 0.06 + 0.05 * q, p, 0.01)

# ---- the prompt cards riffle in
for ct in TB["cardT"]:
    add(highpass(noise(0.03, a=0.0005, rel=0.008, cutoff=6000), 1500), ct + 0.26, -0.6, 0.05)
    add(click(0.25, 2400), ct + 0.28, -0.6, 0.02)

# ---- onboarding: each bench's light clunks on, the cases open together, each job starts with a chime and ticks
for b in BENCHES:
    if b["x"]:
        add(knock(75, 0.4), b["lightT"], pan_x(b["x"] / 4), 0.07)
        add(click(0.5, 2200), b["lightT"] + 0.06, pan_x(b["x"] / 4), 0.03)
add(swish(0.8), T["cases"][0], 0, 0.04)
for k in range(4):
    add(click(0.7, 1900 + 80 * k), T["lids"][0] + 0.1 + 0.015 * k, -0.6 + 0.4 * k, 0.04)
for j, m in enumerate([52, 64, 67, 71, 76]):
    add(tone(hz(m), 3.2, a=0.3, rel=1.4, harm=(1, 0.3)), T["lids"][0], -0.4 + 0.2 * j, 0.03)
for k, b in enumerate(BENCHES):
    add(bell(hz([76, 79, 83, 86, 88][k]), 1.6), b["jobT"], pan_x(b["x"] / 4), 0.04)
    for q in range(6):
        add(tone(hz([76, 79, 83, 86, 88][k] + 12), 0.08, a=0.001, rel=0.02), b["jobT"] + 0.4 * (q + 1), pan_x(b["x"] / 4), 0.012)
    add(bell(hz([88, 91, 95, 98, 100][k]), 1.2), b["jobT"] + 2.4, pan_x(b["x"] / 4), 0.025)    # done

# ---- the handover: the playbook lands; the laser hisses through the word; one wide E major chord holds it
add(swish(0.5), T["book"][0], 0.2, 0.03)
add(knock(80, 0.4), T["book"][1], 0.2, 0.1)
add(hiss(T["word"][1] - T["word"][0] - 0.3, 0.8), T["word"][0], 0, 0.045)
ct = T["word"][0]
while ct < T["word"][1] - 0.3:
    add(noise(0.008, a=0.0004, rel=0.003, cutoff=8000), ct, rng.uniform(-0.4, 0.4), 0.025 + 0.025 * rng.random())
    ct += rng.exponential(1 / 60)
add(swish(1.4, rise=True), T["word"][0] + 0.6, 0, 0.03)
for j, m in enumerate([76, 80, 83]):
    add(bell(hz(m + 12), 3.6), T["word"][1] - 0.4 + 0.16 * j, -0.3 + 0.3 * j, 0.05)
for j, m in enumerate([28, 40, 47, 52, 56, 59, 64, 68, 71]):
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
