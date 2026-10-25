"""
R16 · Lighthouse. Original score, composed in code, timed to the film's one table (bake/boats.json) and T (index.html).

32 s, A minor, slow and wide: a night pad over the sea's wash. A filament hum and a foghorn open it; every boat the
beam finds answers with a soft sonar ping; the three cards chime; every score ticks up and the hot leads ring a warm
bell; the draft types itself, the lever ratchets and clunks, the message flies with a rush and lands on a chord; the
harbour lights rise in a shimmer and harbour bells ring into the last chord. Every sound has a release.
Usage: python score/compose.py  ->  assets/bgm/score.wav   (numpy only, deterministic)
"""
import json
import os
import wave
import numpy as np

SR = 44100
DUR = 32.0
N = int(DUR * SR)
rng = np.random.default_rng(16)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "bgm", "score.wav")
TABLE = json.load(open(os.path.join(HERE, "..", "bake", "boats.json"), encoding="utf-8"))
BOATS = TABLE["boats"]

# ---- the film's T (index.html)
T = dict(ignite=0.9, source=3.4, enrich=9.3, score=14.6, hot=18.9, draft=20.2, pull=23.0, sent=23.45, hit=24.15, beads=(25.9, 27.9), end=28.4)
CARDS = [9.6, 11.6, 13.3]

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
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.zeros_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def noise(dur, a=0.002, rel=0.05, cutoff=0):
    n = int(dur * SR)
    s = rng.standard_normal(n)
    if cutoff:
        s = lowpass(s, cutoff)
        s /= np.max(np.abs(s)) + 1e-9
    return s * env(n, a, rel)


def pad(midis, dur, a=1.2, rel=1.6):
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = sum(np.sin(2 * np.pi * hz(m) * t * (1 + d)) for m in midis for d in (-0.0016, 0.0016))
    e = np.minimum(1, t / a) * np.minimum(1, (dur - t) / rel)
    return lowpass(sig * np.clip(e, 0, 1), 1500)


def bell(f, dur=2.4, g=1.0):
    return sum(h * tone(f * k, dur, a=0.002, rel=dur / (1 + 0.6 * i)) for i, (k, h) in enumerate(((1, 1.0), (2.76, 0.45), (5.4, 0.22), (8.93, 0.1)))) * g


hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)

# ---- the sea: a slow wash the whole way through
n = N; tt = np.arange(n) / SR
wash = lowpass(rng.standard_normal(n), 420)
wash /= np.max(np.abs(wash))
add(wash * (0.55 + 0.45 * np.sin(2 * np.pi * tt / 7.5) ** 2) * np.minimum(1, tt / 1.5) * np.minimum(1, (DUR - tt) / 1.5), 0, 0, 0.06)

# ---- the lamp: a filament hum rising to the ignition, a soft crackle, then the foghorn
n = int(1.6 * SR); tt = np.arange(n) / SR
hum = sum(a * np.sin(2 * np.pi * f * tt) for f, a in ((100, 1.0), (200, 0.5), (300, 0.2)))
add(lowpass(hum, 700) * np.minimum(1, tt / 0.8) * np.exp(-np.maximum(0, tt - 1.0) * 3), 0.0, 0, 0.05)
for k in range(6):
    add(noise(0.05, rel=0.012, cutoff=5000), T["ignite"] + 0.07 * k + 0.02 * (k % 2), 0.2, 0.06)
add(tone(55, 0.6, a=0.002, rel=0.25, harm=(1, 0.5)), T["ignite"], 0, 0.18)
n = int(2.6 * SR); tt = np.arange(n) / SR
vib = 1 + 0.004 * np.sin(2 * np.pi * 5 * tt)
horn = sum(a * np.sign(np.sin(2 * np.pi * f * vib * tt)) for f, a in ((73.4, 1.0), (98.0, 0.7)))
add(lowpass(horn, 380) * np.minimum(1, tt / 0.35) * np.minimum(1, (2.6 - tt) / 0.9), 1.3, -0.1, 0.12)

# ---- the night pad: Am(add9), Fmaj7, C(add9), G6, four seconds each, from the first sweep to the harbour
CH = [[57, 64, 71, 72], [53, 60, 64, 69], [48, 55, 62, 64], [55, 59, 64, 67]]
t0, k = 2.6, 0
while t0 < T["end"]:
    seg = min(4.2, T["end"] + 0.2 - t0)
    g = 0.05 if t0 < T["source"] else (0.035 if T["draft"] <= t0 < T["sent"] else 0.06)
    add(pad(CH[k % 4], seg + 0.8, a=1.0, rel=1.2), t0, 0, g)
    add(lowpass(tone(hz(CH[k % 4][0] - 12), seg + 0.6, a=0.6, rel=1.8), 400), t0, 0, 0.09)
    t0 += 4.0; k += 1
# a slow pulse under the scoring and the glide
for b in np.arange(T["score"], 25.6, 0.5):
    add(lowpass(tone(hz(45), 0.35, a=0.01, rel=0.12), 300), b, 0, 0.05 if b < T["draft"] else 0.03)

# ---- every boat the beam finds: a soft sonar ping, pitched by where it sits
PENTA = [69, 72, 74, 76, 79, 81, 84]
for b in BOATS:
    m = PENTA[int((b["phi"] + 64) / 128 * len(PENTA)) % len(PENTA)]
    p = tone(hz(m + 12), 0.9, a=0.004, rel=0.22, harm=(1, 0.12))
    add(p, b["found"], b["phi"] / 70, 0.05)
    add(p, b["found"] + 0.18, -b["phi"] / 70, 0.018)

# ---- enrichment: a glass chime and a few soft ticks for each card
for c in CARDS:
    add(bell(hz(88), 1.6), c, 0.3, 0.05)
    for k in range(4):
        add(noise(0.02, rel=0.005, cutoff=6000), c + 0.12 + 0.06 * k, 0.3, 0.035)

# ---- scores: digits tick up as the beam passes; a warm bell for every hot lead
for b in BOATS:
    pan = b["phi"] / 70
    for k in range(5):
        add(noise(0.012, rel=0.004, cutoff=7000), b["scored"] + 0.1 * k, pan, 0.012 + 0.004 * b["hot"])
    if b["hot"]:
        add(bell(hz(76 if b["score"] > 90 else 72), 2.6), b["scored"] + 0.6, pan, 0.06)
add(pad([45, 52, 57, 64], 2.0, a=0.6, rel=1.2), T["hot"], 0, 0.05)

# ---- the draft types itself, the lever ratchets and clunks, the message flies and lands
for k, tk in enumerate(np.arange(T["draft"] + 0.6, 22.3, 1 / 14)):
    add(noise(0.018, rel=0.004, cutoff=4500), tk + 0.012 * ((k * 7) % 3), 0.35, 0.03)
for k in range(7):
    add(tone(1800, 0.03, a=0.001, rel=0.006, harm=(1, 0.5)), T["pull"] + 0.065 * k, 0.4, 0.05)
add(tone(70, 0.4, a=0.002, rel=0.12, harm=(1, 0.6)), T["sent"], 0.3, 0.2)
add(noise(0.12, rel=0.04, cutoff=1200), T["sent"], 0.3, 0.1)
n = int((T["hit"] - T["sent"]) * SR); tt = np.arange(n) / SR
whoosh = lowpass(rng.standard_normal(n), 2500) * np.sin(np.pi * tt / tt[-1]) ** 2
add(whoosh, T["sent"] + 0.05, -0.2, 0.12)
for j, m in enumerate([57, 64, 69, 71, 76]):
    add(tone(hz(m), 3.0, a=0.01, rel=1.2, harm=(1, 0.3)), T["hit"], -0.4 + 0.2 * j, 0.05)

# ---- the harbour lights rise in a shimmer, harbour bells, the last chord
for k in range(40):
    tk = T["beads"][0] + 1.9 * k / 40
    add(tone(hz(PENTA[k % len(PENTA)] + 12 + (12 if k > 28 else 0)), 0.6, a=0.002, rel=0.15), tk, -0.7 + 1.4 * ((k * 5) % 11) / 10, 0.02)
for j, m in enumerate([69, 64, 76]):
    add(bell(hz(m), 3.4), T["beads"][1] + 0.18 * j, -0.3 + 0.3 * j, 0.07)
for j, m in enumerate([45, 57, 64, 67, 71, 72, 76]):
    add(tone(hz(m), DUR - T["end"], a=0.02, rel=1.8, harm=(1, 0.3, 0.1), detune=0.0007), T["end"], -0.5 + 0.17 * j, 0.11)

# ---- master: a soft-clip that lifts the body and keeps the peaks round, then a fade at the very end
mix = np.stack([L, R], axis=1)
mix /= np.max(np.abs(mix))
DRIVE = 2.6
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
