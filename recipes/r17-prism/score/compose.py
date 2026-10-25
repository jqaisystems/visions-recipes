"""
R17 · Prism. Original score, composed in code, timed to the film's one table (bake/pieces.json).

32 s, D major, bright and glassy. A glass drone under the pages; a soft rain of pings as the lines lift off as light;
a tink as each edge of the prism draws and a long glass ring for each cut. Stock phrases arrive on a dull whoosh and
break with a thud, a crack and falling shards. The brief: a rising rush into the glass, then the spectrum opens a
six-note chord, one note per colour, and a light pulse carries the formats; each piece lands on its own note with soft
typing. Review: a click and a two-note chime per approval, a rewind for the rewrite. The month ticks in, the lights
rise in a shimmer, and one wide chord holds the word. Every sound has a release.
Usage: python score/compose.py  ->  assets/bgm/score.wav   (numpy only, deterministic)
"""
import json
import os
import wave
import numpy as np

SR = 44100
DUR = 32.0
N = int(DUR * SR)
rng = np.random.default_rng(17)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "bgm", "score.wav")
TABLE = json.load(open(os.path.join(HERE, "..", "bake", "pieces.json"), encoding="utf-8"))
T, RAYS, PIECES, PAGES, CLICHES, DAYS = (TABLE[k] for k in ("T", "rays", "pieces", "pages", "cliches", "days"))

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


def glass(f, dur=2.4, g=1.0):
    # a struck glass: a few inharmonic partials, the high ones dying first
    return sum(h * tone(f * k, dur, a=0.001, rel=dur / (1 + 0.9 * i)) for i, (k, h) in enumerate(((1, 1.0), (2.32, 0.5), (4.25, 0.25), (6.63, 0.12)))) * g


def pluck(f, dur=1.2):
    return tone(f, dur, a=0.002, rel=0.28, harm=(1, 0.35, 0.12))


def sweep(dur, f0, f1, cutoff=3000):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = lowpass(rng.standard_normal(n), cutoff) * (t / dur) ** 2
    return s / (np.max(np.abs(s)) + 1e-9) * np.minimum(1, (dur - t) / 0.03)


hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
SPEC = [62, 66, 69, 73, 76, 81]           # one note per colour, red (low) to violet (high): D, F#, A, C#, E, A
PENTA = [74, 76, 78, 81, 83, 86, 88]

# ---- the glass drone: from the first frame to the brief, a soft D with a fifth above
n = int(9.2 * SR); tt = np.arange(n) / SR
drone = lowpass(sum(a * np.sin(2 * np.pi * f * tt * (1 + d)) for f, a in ((hz(38), 1.0), (hz(50), 0.6), (hz(57), 0.3)) for d in (-0.001, 0.001)), 900)
add(drone * np.minimum(1, tt / 1.2) * np.minimum(1, (9.2 - tt) / 1.0), 0, 0, 0.05)
add(pad([62, 69, 74, 76], 4.4, a=1.4, rel=1.4), 0.2, 0, 0.03)

# ---- the lines lift off as light: a soft rain of pings, densest where the most lines lift
for k in range(150):
    pg = PAGES[k % len(PAGES)]
    tk = pg["lift"] + 0.95 * rng.random() + 0.4 * rng.random()
    m = PENTA[int(rng.integers(len(PENTA)))] + (12 if rng.random() > 0.8 else 0)
    add(tone(hz(m), 0.5, a=0.002, rel=0.08), tk, pg["pos"][0] / 6, 0.012)
for pg in PAGES:
    add(noise(0.9, a=0.25, rel=0.3, cutoff=2500), pg["lift"], pg["pos"][0] / 6, 0.02)

# ---- the prism: a tink as each edge draws, a long glass ring and a scrape for each cut
for k in range(9):
    add(tone(hz(86 + (k % 3) * 2), 0.4, a=0.001, rel=0.07), 1.75 + 0.13 * k, -0.4 + 0.1 * k, 0.02)
for j, tc in enumerate(T["cut"]):
    add(glass(hz([74, 78, 81][j]), 3.2), tc, [-0.4, 0.4, 0][j], 0.06)
    add(noise(0.4, a=0.02, rel=0.1, cutoff=7000), tc, [-0.4, 0.4, 0][j], 0.025)

# ---- stock phrases: a dull whoosh in, a thud, a crack, shards falling
for c in CLICHES:
    pan = 0.6 if c["start"][0] > 0 else -0.6
    add(sweep(1.6, 0, 0, 900), c["hit"] - 1.6, pan, 0.07)
    add(tone(62, 0.5, a=0.002, rel=0.12, harm=(1, 0.5)), c["hit"], pan * 0.5, 0.2)
    add(noise(0.18, a=0.001, rel=0.04, cutoff=3500), c["hit"], pan * 0.5, 0.12)
    for k in range(9):
        add(lowpass(tone(900 + 1400 * rng.random(), 0.12, a=0.001, rel=0.025, harm=(1, 0.4)), 4000), c["hit"] + 0.25 + 0.9 * rng.random(), pan + 0.3 * (rng.random() - 0.5), 0.018)

# ---- the brief: a chime as the card draws, a rush into the glass, a bright ping as it enters
add(glass(hz(81), 1.6), T["brief"], -0.5, 0.04)
add(sweep(T["enter"] - T["fire"] + 0.05, 0, 0, 5000), T["fire"], -0.4, 0.09)
add(glass(hz(93), 2.0), T["enter"], 0, 0.05)
add(tone(hz(38), 1.4, a=0.005, rel=0.5, harm=(1, 0.4)), T["enter"], 0, 0.2)

# ---- the spectrum: one note per colour, opening into a chord
for i, m in enumerate(SPEC):
    f0 = T["fan"][0] + 0.14 * i
    add(tone(hz(m), 3.2, a=0.01, rel=1.3, harm=(1, 0.3, 0.1)), f0, -0.6 + 0.24 * i, 0.06)
    add(glass(hz(m + 12), 1.6), f0, -0.6 + 0.24 * i, 0.025)

# ---- a light pulse carries the formats and the review: D, Bm, G, A, two bars each at 100 bpm
BEAT = 0.6
CH = [[50, 62, 66, 69, 73], [47, 62, 66, 71, 74], [43, 62, 67, 71, 74], [45, 61, 64, 69, 76]]
t0, k = 10.8, 0
while t0 < T["month"]:
    seg = min(4 * BEAT * 2, T["month"] + 0.4 - t0)
    ch = CH[k % 4]
    add(pad(ch[1:], seg + 0.8, a=0.5, rel=1.0, cutoff=2200), t0, 0, 0.045)
    for b in range(int(seg / BEAT + 0.5)):
        tb = t0 + b * BEAT
        add(lowpass(tone(hz(ch[0] - 12 if b % 2 == 0 else ch[0]), 0.4, a=0.004, rel=0.14, harm=(1, 0.3)), 600), tb, 0, 0.11)
        add(noise(0.03, rel=0.008, cutoff=9000), tb + BEAT / 2, 0.25, 0.018)
    t0 += 4 * BEAT * 2; k += 1

# ---- each piece lands on its colour's note, and types itself in
for p in PIECES:
    m = SPEC[p["ray"]] + (0 if p["id"] not in ("pt", "fr") else (3 if p["id"] == "pt" else 5))
    pan = 0.3 + 0.1 * (p["ray"] - 2.5)
    add(pluck(hz(m + 12)), p["land"], pan, 0.09)
    add(glass(hz(m + 24), 1.2), p["land"], pan, 0.02)
    for j in range(8):
        add(noise(0.016, rel=0.004, cutoff=5000), p["land"] + 0.08 + 0.08 * j + 0.015 * (j % 3), pan, 0.022)

# ---- review: a click and two notes up for each approval; a rewind for the rewrite
for p in PIECES:
    add(tone(2200, 0.03, a=0.001, rel=0.006, harm=(1, 0.5)), p["approve"] - 0.02, 0.35, 0.06)
    add(tone(hz(81), 0.6, a=0.002, rel=0.18, harm=(1, 0.2)), p["approve"], 0.35, 0.05)
    add(tone(hz(86), 0.8, a=0.002, rel=0.24, harm=(1, 0.2)), p["approve"] + 0.08, 0.35, 0.05)
    if p.get("rewrite"):
        rw = p["rewrite"]
        add(tone(2200, 0.03, a=0.001, rel=0.006, harm=(1, 0.5)), rw - 0.02, 0.3, 0.06)
        n = int(0.5 * SR); tt = np.arange(n) / SR
        rev = (tone(hz(74), 0.5, a=0.002, rel=0.2, harm=(1, 0.3)) + 0.5 * tone(hz(81), 0.5, a=0.002, rel=0.2))[::-1]
        add(rev, rw + 0.1, 0.3, 0.08)
        add(pluck(hz(SPEC[p["ray"]] + 12)), rw + 0.6, 0.3, 0.08)

# ---- the month: pieces fly in and every other day ticks into place, rising
for p in PIECES:
    add(sweep(0.8, 0, 0, 2500), p["fly"], 0.2, 0.02)
pops = sorted(d["pop"] for d in DAYS if d["pop"])
for j, tp in enumerate(pops):
    add(tone(hz(PENTA[j % len(PENTA)] + (12 if j > 14 else 0)), 0.3, a=0.001, rel=0.06), tp, -0.6 + 1.2 * j / len(pops), 0.03)
add(pad([50, 62, 66, 69, 74], 3.0, a=0.8, rel=1.4), T["month"], 0, 0.05)

# ---- the lights rise into the word, and one wide chord holds it
for k in range(48):
    tk = T["beads"][0] + 1.7 * k / 48
    add(tone(hz(PENTA[k % len(PENTA)] + 12), 0.5, a=0.002, rel=0.12), tk, -0.8 + 1.6 * ((k * 7) % 13) / 12, 0.02)
add(sweep(1.6, 0, 0, 6000), T["beads"][0] + 0.2, 0, 0.04)
for j, m in enumerate([62, 73, 81]):
    add(glass(hz(m + 12), 3.4), T["beads"][1] - 0.4 + 0.16 * j, -0.3 + 0.3 * j, 0.06)
for j, m in enumerate([38, 50, 57, 62, 66, 69, 73, 76, 81]):
    add(tone(hz(m), DUR - T["beads"][1] + 0.4, a=0.04, rel=2.0, harm=(1, 0.3, 0.1), detune=0.0007), T["beads"][1] - 0.4, -0.6 + 0.15 * j, 0.09)

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
