"""
R24 · Cairn. Original score, composed in code, timed to the film's one table (bake/table.json).

32 s at 84 bpm in A minor, resolving to C major on the summit: mountain air, not R23's taiko.
Night: wind and a low drone; every dashboard number that hits the rock is a small glassy tick; the gust is a roar.
The tilt up into the cloud: a breathy flute and an airy pad. Every stone falls with a whistle and lands on an
orchestral hit (a low boom, a string stab, a rock crunch, a crash). The weeks: a string ostinato on Am, F, C, G, a
wood tick on every sixteenth like a clock running fast, a whoosh for every day that passes, bells when the rank
climbs. The checkpoint: the music stops dead before every decision, then a stamp; GO on a major chord, NO-GO on a
cluster, VOID muted, CLOSED clean. The summit: the last three stones on the beat, a riser, the final hit opens on
C major with the flute over it; bells for the URL.
Usage: python score/compose.py  ->  assets/bgm/score.wav   (numpy only, deterministic)
"""
import math
import json
import os
import wave
import numpy as np

SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "bgm", "score.wav")
TB = json.load(open(os.path.join(HERE, "..", "bake", "table.json"), encoding="utf-8"))
T, FPS, BEAT, DUR = TB["T"], TB["fps"], TB["beat"], TB["dur"]
N = int(DUR * SR)
rng = np.random.default_rng(24)
L = np.zeros(N)
R = np.zeros(N)
tt = np.arange(N) / SR


def add(sig, start, pan=0.0, g=1.0):
    i0 = int(round(start * SR))
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


def onepole(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def lowpass(x, cutoff):
    return onepole(onepole(x, cutoff), cutoff)


def highpass(x, cutoff):
    return x - onepole(x, cutoff)


def noise(dur, a=0.002, rel=0.05):
    n = int(dur * SR)
    return rng.standard_normal(n) * env(n, a, rel)


def norm(x):
    return x / (np.max(np.abs(x)) + 1e-9)


def swish(dur, lo=600, hi=5000, rise=False):
    n = int(dur * SR)
    u = np.arange(n) / n
    shape = u ** 2.2 if rise else np.sin(np.pi * u) ** 2
    # a moving band: three static bands cross-faded along the stroke
    s = rng.standard_normal(n)
    a, b, c = lowpass(s, lo), lowpass(s, (lo + hi) / 2), lowpass(s, hi)
    m = u if rise else np.sin(np.pi * u)
    x = a * (1 - m) ** 2 + 2 * b * m * (1 - m) + c * m ** 2
    return norm(x * shape)


def taiko(f=58, dur=1.4, g=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    fr = f + 90 * np.exp(-t * 28)
    body = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 3.2)
    skin = lowpass(noise(0.06, a=0.0005, rel=0.015), 1800)
    body[: len(skin)] += 0.6 * skin
    return g * body


def shime(g=1.0):
    n = int(0.16 * SR)
    t = np.arange(n) / SR
    fr = 340 + 260 * np.exp(-t * 60)
    s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 32)
    s[: int(0.01 * SR)] += highpass(noise(0.01, a=0.0002, rel=0.003), 2000)
    return g * s


def crash(dur=2.2, g=1.0):
    return g * norm(highpass(noise(dur, a=0.001, rel=dur / 3.5), 3500))


def hat(g=1.0, open_=False):
    return g * norm(highpass(noise(0.18 if open_ else 0.05, a=0.0003, rel=0.06 if open_ else 0.012), 7000))


def kick(g=1.0):
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    fr = 48 + 120 * np.exp(-t * 40)
    return g * np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 9)


def snare(g=1.0):
    s = 0.5 * tone(190, 0.18, a=0.001, rel=0.05)
    s += 0.8 * norm(highpass(noise(0.18, a=0.0005, rel=0.06), 1500))
    return g * s


def block(f=880, g=1.0):
    return g * (tone(f, 0.12, a=0.0005, rel=0.025) + 0.5 * tone(f * 1.52, 0.12, a=0.0005, rel=0.015))


def pluck(f, dur=1.2, bright=0.5):
    # Karplus-Strong: a plucked string, a little nasal like a shamisen when bright
    n = int(dur * SR)
    p = max(2, int(SR / f))
    buf = rng.uniform(-1, 1, p)
    out = np.empty(n)
    k = 0.996
    for i in range(n):
        v = buf[i % p]
        out[i] = v
        buf[i % p] = k * (bright * v + (1 - bright) * 0.5 * (v + buf[(i + 1) % p]))
    out[: int(0.002 * SR)] *= np.linspace(0, 1, int(0.002 * SR))
    return norm(out) * env(n, 0.001, dur / 2.5)


def bell(f, dur=2.4):
    return sum(h * tone(f * k, dur, a=0.001, rel=dur / (1 + 1.2 * i)) for i, (k, h) in enumerate(((1, 1.0), (2.0, 0.45), (2.76, 0.3), (5.4, 0.12))))


def whistle(t0, t1, f0=2400, f1=260, g=1.0):
    n = int((t1 - t0) * SR)
    u = np.arange(n) / n
    fr = f0 * (f1 / f0) ** u
    s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * (0.2 + 0.8 * u)
    add(s, t0, 0.0, g)


hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
beats = lambda a, b, step=BEAT: [round(a + k * step, 4) for k in range(int(round((b - a) / step)))]

def hsh(n):   # the film's hash, so the ticks land where the numbers do
    x = math.sin(n * 127.1 + 311.7) * 43758.5453
    return x - math.floor(x)


lands, falls, stamps = TB["lands"], TB["falls"], TB["stamps"]

# ---- air: wind under everything, louder at night and in the gust; a low drone on A
w = norm(lowpass(rng.standard_normal(N), 500)) * (0.55 + 0.45 * np.sin(2 * np.pi * 0.23 * tt) ** 2)
wmask = np.clip(1 - (tt - T["weeks"][0]) / 1.0, 0.25, 1) * np.clip((T["title"] + 1.5 - tt) / 1.0, 0, 1)
L += 0.06 * w * wmask
R += 0.06 * np.roll(w, 4321) * wmask
dr = (np.sin(2 * np.pi * hz(33) * tt) + 0.35 * np.sin(2 * np.pi * hz(45) * tt * 1.003)) * np.clip(tt / 1.5, 0, 1) * np.clip((T["weeks"][0] + 1 - tt) / 1.0, 0, 1)
L += 0.06 * dr
R += 0.06 * dr

# ---- the forty numbers: a glassy tick where each one hits the rock (the same clock as the film)
for i in range(40):
    t0 = 0.12 + 2.2 * hsh(i * 1.31)
    fall = 0.55 + 0.25 * hsh(i * 5)
    th = t0 + fall
    if th < T["gust"]:
        f = 1800 + 1600 * hsh(i * 3)
        tk = tone(f, 0.09, a=0.0005, rel=0.02, harm=(1, 0.4, 0.2)); tk[:2205] += 0.4 * highpass(noise(0.05, a=0.0003, rel=0.01), 4000)
        add(tk, th, 0.8 * (hsh(i * 2.7 + 1) * 2 - 1), 0.05)
add(swish(1.3, 200, 6000, rise=False), T["gust"] - 0.25, 0.3, 0.32)
add(norm(lowpass(noise(1.4, a=0.08, rel=0.5), 900)), T["gust"] - 0.1, -0.2, 0.18)

# ---- the flute and the pad: up into the cloud
def flute(f, dur, g=1.0, vib=5.2):
    n = int(dur * SR)
    t = np.arange(n) / SR
    ph = 2 * np.pi * np.cumsum(f * (1 + 0.006 * np.sin(2 * np.pi * vib * t) * np.clip(t / 0.3, 0, 1))) / SR
    body = np.sin(ph) + 0.18 * np.sin(2 * ph) + 0.06 * np.sin(3 * ph)
    breath = lowpass(highpass(rng.standard_normal(n), 900), 4000) * 0.22
    return g * (body + breath) * env(n, 0.09, dur / 2.2)

def pad(midis, t0, dur, g=0.05, pan=0.0):
    for j, m in enumerate(midis):
        add(tone(hz(m), dur, a=0.6, rel=dur / 2, harm=(1, 0.25, 0.08), detune=0.0009), t0, -0.5 + j / max(1, len(midis) - 1), g)

pad([57, 60, 64, 69], T["first"][0], 2.6, 0.035)
F1 = [(76, 0.9), (74, 0.5), (72, 0.5), (69, 1.4)]
tf = T["first"][0] + 0.1
for m, d in F1:
    add(flute(hz(m), d * 1.4), tf, 0.2, 0.12)
    tf += d

# ---- every stone: a whistle as it falls, then the hit
def stone_hit(t0, big):
    add(taiko(44 if big else 52, 1.9 if big else 1.2), t0, 0.0, 0.62 if big else 0.45)
    add(tone(hz(33), 1.8, a=0.002, rel=0.7), t0, 0.0, 0.35 if big else 0.22)
    n = int(0.5 * SR)   # rock crunch: grainy noise, low
    crunch = lowpass(rng.standard_normal(n) * (rng.random(n) > 0.82), 1400) * env(n, 0.001, 0.12)
    add(norm(crunch), t0, 0.15, 0.3)
    add(crash(2.4 if big else 1.4), t0, -0.25, 0.12 if big else 0.07)
    for j, m in enumerate([45, 52, 57, 60, 64]):   # a string stab
        add(tone(hz(m), 0.5, a=0.004, rel=0.18, harm=(1, 0.6, 0.4, 0.25, 0.15)), t0, -0.6 + 0.3 * j, 0.05)

for k, tl in enumerate(lands):
    t0 = tl - falls[k]
    whistle(t0, tl, 2200, 300, 0.05)
    add(swish(falls[k] + 0.1, 400, 7000, rise=True), t0 - 0.05, 0.0, 0.12)
    stone_hit(tl, k in (0, 5))

# ---- the weeks: string ostinato, a clock running fast, a whoosh per day, bells as the rank climbs
CH = [[45, 57, 60, 64], [41, 57, 60, 65], [48, 55, 60, 64], [43, 55, 59, 62]]   # Am F C G
b0, b1 = T["weeks"][0], T["check"][0]
k = 0
tb = b0
while tb < b1 - 1e-6:
    ch = CH[(k // 8) % 4]
    add(pluck(hz(ch[0] - 12), 0.5, 0.25), tb, -0.1, 0.17)
    for j, m in enumerate(ch[1:]):
        add(tone(hz(m + (12 if k % 2 else 0)), BEAT / 2 * 0.9, a=0.004, rel=0.1, harm=(1, 0.5, 0.3, 0.2)), tb, -0.4 + 0.4 * j, 0.028)
    for j in range(2):
        add(block(1500 if j == 0 else 1250, 1.0), tb + j * BEAT / 4, 0.5, 0.05)
    if k % 2 == 0:
        add(kick(), tb, 0.0, 0.25)
    tb += BEAT / 2
    k += 1
d = TB["lands"][1] - 2 * ((TB["lands"][2] - TB["lands"][1]) / 2)
day = (TB["lands"][2] - TB["lands"][1]) / 2
td = d
while td < b1:
    if td >= b0:
        add(swish(0.7, 500, 6000), td - 0.2, 0.4 * math.sin(td), 0.1)
    td += day
for rk in TB["ranks"][1:]:
    for j, m in enumerate([81, 84, 88, 93]):
        add(bell(hz(m), 1.6), rk["t"] + 0.06 * j, 0.3, 0.035)
MEL = [69, 72, 76, 74, 72, 71, 69, 67, 69, 72, 74, 76]
for j, m in enumerate(MEL):
    add(flute(hz(m + 12), BEAT * 0.95), b0 + 0.5 + j * BEAT, 0.25, 0.05)

# ---- the checkpoint: a dead stop before every decision, then the stamp
for j, sp in enumerate(stamps):
    t0 = sp["t"]
    i0, i1 = int((t0 - 0.12) * SR), int(t0 * SR)
    L[i0:i1] *= np.linspace(1, 0.05, i1 - i0)
    R[i0:i1] *= np.linspace(1, 0.05, i1 - i0)
    add(taiko(60, 1.0), t0, 0.0, 0.5)
    add(snare(), t0, 0.1, 0.18)
    add(crash(1.2), t0, 0.3, 0.07)
    chord = {"GO": [57, 61, 64, 69], "NO-GO": [56, 57, 63, 64], "VOID": [57, 60], "CLOSED": [57, 64, 69]}[sp["word"]]
    g = 0.045 if sp["word"] != "VOID" else 0.03
    for q, m in enumerate(chord):
        add(tone(hz(m), 0.9, a=0.003, rel=0.35, harm=(1, 0.5, 0.3, 0.2)), t0, -0.4 + 0.25 * q, g)
    for q in range(3):   # a tense low pulse until the next decision
        add(pluck(hz(33), 0.4, 0.2), t0 + BEAT * (0.5 + q * 0.5), -0.1, 0.12)
for j, m in enumerate([76, 74, 72, 74]):
    add(flute(hz(m), 0.6), TB["line"] + j * BEAT / 2, 0.1, 0.06)

# ---- the summit: a riser into the last landing, then C major opens with the flute over it
add(swish(1.8, 300, 10000, rise=True), lands[5] - 1.8, 0.0, 0.22)
for q in range(16):
    add(shime(), lands[3] - 0.2 + q * (lands[5] - lands[3] + 0.2) / 16, 0.3 * (-1) ** q, 0.05 + 0.06 * q / 16)
tc = lands[5]
for j, m in enumerate([36, 48, 55, 60, 64, 67, 72, 76]):
    add(tone(hz(m), DUR - tc, a=0.08, rel=2.4, harm=(1, 0.3, 0.12), detune=0.0007), tc, -0.6 + 0.17 * j, 0.06)
for j, (m, dd) in enumerate([(79, 0.7), (81, 0.5), (84, 1.0), (83, 0.5), (79, 1.6)]):
    add(flute(hz(m), dd * 1.3), tc + 0.2 + sum(x[1] for x in [(79, 0.7), (81, 0.5), (84, 1.0), (83, 0.5), (79, 1.6)][:j]), 0.15, 0.1)
tu = T["title"] + 0.7
add(swish(0.6, 800, 8000), tu - 0.1, -0.3, 0.12)
for j, m in enumerate([84, 88, 91, 96, 91, 88]):
    add(bell(hz(m), 2.0), tu + 1.2 + j * 0.12, 0.4 * math.sin(j), 0.03)
add(bell(hz(72), 3.0), tu + 2.4, 0.0, 0.05)

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
