"""
R18 · Loom. Original score, composed in code, timed to the film's one table (bake/loom.json).

32 s, A minor into C, warm and wooden. A low drone and soft plucks as the sources arrive as threads; static for the
headlines that flicker past. The card slides in on brass, a clack and a rising note for every rule punched, a shimmer
as it is read, a rain of plucks as the cords drop. Then the loom is the beat, 96 bpm: a wooden thunk for every beat-up,
a swish for every pass of the shuttle, a hook clack on the off-beat, over Am, F, C, G; muffled drops for the threads
that fall away, nine notes for the nine that matter, a bell for each story as the type comes through. The clock ticks
to 09:00 and strikes; the cloth is cut and folded; every Monday lands with a soft thud; one wide chord holds the word.
Usage: python score/compose.py  ->  assets/bgm/score.wav   (numpy only, deterministic)
"""
import json
import os
import wave
import numpy as np

SR = 44100
DUR = 32.0
N = int(DUR * SR)
rng = np.random.default_rng(18)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "bgm", "score.wav")
TABLE = json.load(open(os.path.join(HERE, "..", "bake", "loom.json"), encoding="utf-8"))
T, THREADS, HEADLINES, RULES, PICKS, PICKS2 = (TABLE[k] for k in ("T", "threads", "headlines", "rules", "picks", "picks2"))
BEAT = TABLE["beat"]

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


def pad(midis, dur, a=1.2, rel=1.6, cutoff=1800):
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = sum(np.sin(2 * np.pi * hz(m) * t * (1 + d)) for m in midis for d in (-0.0018, 0.0018))
    e = np.minimum(1, t / a) * np.minimum(1, (dur - t) / rel)
    return lowpass(sig * np.clip(e, 0, 1), cutoff)


def pluck(f, dur=1.0, rel=0.25):
    return tone(f, dur, a=0.002, rel=rel, harm=(1, 0.45, 0.18, 0.06))


def bell(f, dur=2.6):
    return sum(h * tone(f * k, dur, a=0.001, rel=dur / (1 + 1.2 * i)) for i, (k, h) in enumerate(((1, 1.0), (2.0, 0.45), (2.76, 0.3), (5.4, 0.12))))


def thunk(dur=0.3):
    # the beater: a wooden knock, a low body and a short burst of filtered noise
    return lowpass(tone(70, dur, a=0.001, rel=0.06, harm=(1, 0.6, 0.3)) + 0.6 * noise(dur, a=0.001, rel=0.02, cutoff=1800), 2200)


def swish(dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = lowpass(rng.standard_normal(n), 3200) * np.sin(np.pi * t / dur) ** 2
    return s / (np.max(np.abs(s)) + 1e-9)


def clack():
    return lowpass(noise(0.05, a=0.0005, rel=0.008, cutoff=6000) + tone(1800, 0.05, a=0.0005, rel=0.01), 7000)


hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
PENTA = [69, 72, 74, 76, 79, 81, 84]          # A minor pentatonic

# ---- the drone: low A and E under the stream and the card
n = int(9.0 * SR); tt = np.arange(n) / SR
drone = lowpass(sum(a * np.sin(2 * np.pi * f * tt * (1 + d)) for f, a in ((hz(33), 1.0), (hz(45), 0.6), (hz(52), 0.3)) for d in (-0.001, 0.001)), 800)
add(drone * np.minimum(1, tt / 1.2) * np.minimum(1, (9.0 - tt) / 0.8), 0, 0, 0.06)
add(pad([57, 64, 69, 72], 4.6, a=1.5, rel=1.4), 0.2, 0, 0.03)

# ---- the sources arrive: a soft pluck for some threads as each reaches the beam, panned by where it lands
for k, th in enumerate(THREADS[::3]):
    m = PENTA[int(rng.integers(len(PENTA)))] + (12 if rng.random() > 0.75 else 0)
    add(pluck(hz(m), 0.6, 0.12), th["arrive"] + 0.9, th["x"] / 5, 0.016)
add(swish(3.4), 0.3, -0.2, 0.025)
# headlines flicker past: a little static each
for h in HEADLINES:
    add(lowpass(noise(0.35, a=0.01, rel=0.12), 5000) * (0.5 + 0.5 * np.sign(np.sin(np.arange(int(0.35 * SR)) / SR * 2 * np.pi * 23))), h["t0"], np.sign(h["pos"][0]) * 0.5, 0.012)

# ---- the card: a brass slide, a clack and a rising note per rule, a shimmer as it is read, a rain as the cords drop
add(swish(0.8), T["card"] - 0.05, 0.6, 0.05)
add(tone(hz(45), 0.6, a=0.002, rel=0.16, harm=(1, 0.5, 0.2)), T["card"] + 0.75, 0, 0.12)
for k, rl in enumerate(RULES):
    add(clack(), rl["t"], -0.5 + 0.3 * rl["col"], 0.16)
    add(bell(hz([69, 72, 74, 76, 79, 81, 84, 86][k]), 1.4), rl["t"] + 0.01, -0.5 + 0.3 * rl["col"], 0.035)
for k in range(24):
    add(tone(hz(PENTA[k % 7] + 12), 0.3, a=0.002, rel=0.06), T["read"] + 0.6 * k / 24, -0.6 + 1.2 * k / 24, 0.012)
for k in range(30):
    add(pluck(hz(PENTA[int(rng.integers(7))]), 0.5, 0.08), T["cords"] + 0.9 * rng.random(), rng.uniform(-0.8, 0.8), 0.012)

# ---- the loom is the beat: Am, F, C, G, a bar each; a thunk per beat-up, a swish per pass, a clack on the off-beat
CH = [[45, 57, 64, 69, 72], [41, 57, 65, 69, 72], [48, 60, 64, 67, 72], [43, 59, 62, 67, 71]]
BAR = 4 * BEAT
t0, k = T["weave"], 0
while t0 < T["full"] + 0.4:
    ch = CH[k % 4]
    add(pad(ch[1:], BAR + 0.8, a=0.4, rel=0.9, cutoff=2000), t0, 0, 0.04)
    for b in range(4):
        add(lowpass(tone(hz(ch[0] - 12 if b % 2 == 0 else ch[0]), 0.45, a=0.004, rel=0.16, harm=(1, 0.3)), 500), t0 + b * BEAT, 0, 0.11)
    t0 += BAR; k += 1
for j, p in enumerate(PICKS + PICKS2):
    g = 0.7 if p > T["cut"] else 1.0
    fast = T["fast"] < p <= T["full"] + 0.01
    add(thunk(), p, 0.1, 0.22 * g)
    add(swish(0.24 if fast else 0.4), p - (0.28 if fast else 0.44), 0.7 if j % 2 else -0.7, 0.035 * g)
    add(clack(), p + (BEAT / 4 if fast else BEAT / 2), -0.3, 0.05 * g)
# the threads that fall away: a muffled drop for some of them
for th in THREADS[1::5]:
    if "reject" in th:
        add(lowpass(tone(hz(33 + int(rng.integers(0, 5))), 0.5, a=0.004, rel=0.14, harm=(1, 0.4)), 400), th["reject"] + 0.6, th["x"] / 5, 0.05)
        add(noise(0.4, a=0.02, rel=0.1, cutoff=900), th["reject"] + 0.45, th["x"] / 5, 0.012)
# nine that matter
for k, m in enumerate([69, 72, 76, 79, 81, 84, 88, 91, 93]):
    add(bell(hz(m), 1.8), 12.7 + 0.06 * k, -0.6 + 0.15 * k, 0.03)
# the type comes through: a bell for the headline and each story
for k, tb in enumerate([15.8, 16.5, 17.2, 17.9]):
    add(bell(hz([76, 81, 84, 88][k]), 2.4), tb, -0.4 + 0.27 * k, 0.05)

# ---- the clock: ticks to 09:00, then it strikes
for k in range(8):
    add(clack() * 0.7, T["clock"] + 0.6 + 0.25 * k, 0, 0.06)
for j, m in enumerate([69, 64, 72, 57]):
    add(bell(hz(m + 12), 3.4), T["nine"] + 0.02 + 0.03 * j, -0.2 + 0.13 * j, 0.09)
add(tone(hz(45), 2.6, a=0.005, rel=1.0, harm=(1, 0.5, 0.2)), T["nine"], 0, 0.12)
add(pad([57, 64, 69, 72, 76], 3.6, a=0.4, rel=1.6), T["nine"], 0, 0.045)
# cut, fold, fold, carried to the table
add(swish(0.35), T["cut"], -0.5, 0.06)
add(tone(2400, 0.2, a=0.001, rel=0.05), T["cut"] + 0.05, 0, 0.02)
for tf in T["fold"][:2]:
    add(swish(0.55), tf, 0.2, 0.05)
add(swish(1.0), T["slide"][0], 0.4, 0.04)
add(thunk(0.4), T["slide"][1] - 0.05, 0.3, 0.12)
# the loom starts next week's cloth: a softer pulse over C, G
for k in range(3):
    add(pad([[60, 64, 67, 72], [59, 62, 67, 71], [57, 64, 69, 72]][k], BAR + 0.6, a=0.4, rel=0.9), PICKS2[0] + k * BAR, 0, 0.035)

# ---- every Monday: a soft thud for each briefing on the stack, faster and higher as it rises
for k in range(52):
    tk = T["stack"][0] + (T["stack"][1] - T["stack"][0]) * (k / 52) ** 1.25 + 0.3
    add(lowpass(tone(hz(45 + (k // 13) * 2), 0.18, a=0.002, rel=0.04, harm=(1, 0.5)), 900), tk, 0.2, 0.05)
    if k % 4 == 0:
        add(pluck(hz(PENTA[(k // 4) % 7] + 12), 0.5, 0.1), tk, -0.3 + 0.6 * (k % 8) / 8, 0.025)

# ---- the threads gather into the word, and one wide chord in C holds it
for k in range(40):
    add(tone(hz(PENTA[k % 7] + 12), 0.45, a=0.002, rel=0.1), T["word"][0] + 1.5 * k / 40, -0.8 + 1.6 * ((k * 5) % 11) / 10, 0.02)
add(swish(1.6), T["word"][0] + 0.1, 0, 0.04)
for j, m in enumerate([72, 76, 79]):
    add(bell(hz(m + 12), 3.6), T["word"][1] - 0.5 + 0.16 * j, -0.3 + 0.3 * j, 0.05)
for j, m in enumerate([36, 48, 55, 60, 64, 67, 71, 74, 79]):
    add(tone(hz(m), DUR - T["word"][1] + 0.5, a=0.04, rel=2.0, harm=(1, 0.3, 0.1), detune=0.0007), T["word"][1] - 0.5, -0.6 + 0.15 * j, 0.09)

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
