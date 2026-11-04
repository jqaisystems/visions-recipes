"""The score for R40 · One Take, composed in code at 128 bpm and timed to bake/table.json: a fall and a bounce;
  a tight track of kick, clap and bass through the twelve worlds, each with its own sound and a whoosh on each dive; a riser,
  one beat of silence and a sub drop on the pull-back; a press and five cards; the days riffling and a slam on FRIDAY; a
  chord on the logo. Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py"""
import json, os, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TB = json.load(open(os.path.join(ROOT, "bake", "table.json"), encoding="utf-8"))
SR = 48000; DUR = TB["dur"]; BEAT = TB["beat"]; N = int(SR * DUR)
rng = np.random.default_rng(83)


def env(n, a, d):
    e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    return e * np.exp(-np.arange(n) / SR / d)


def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); s = 0.0
    for i in range(len(x)):
        s = (1 - a) * x[i] + a * s; y[i] = s
    return y


def hp(x, fc): return x - lp(x, fc)


def add(out, at, sig, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N or i + len(sig) <= 0: return
    if i < 0: sig = sig[-i:]; i = 0
    sig = sig[:N - i]
    out[i:i + len(sig), 0] += sig * gain * (1 - max(0, pan))
    out[i:i + len(sig), 1] += sig * gain * (1 + min(0, pan))


def mtof(m): return 440 * 2 ** ((m - 69) / 12)


def pluck(f, d=0.5, bright=1.0):
    n = int(SR * d); x = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f * m * x) * np.exp(-x * (6 + 8 * m / bright)) for m, a in [(1, 1), (2, 0.5), (3, 0.25), (4, 0.12)])
    return s * env(n, 0.002, d)


def bell(f, d=2.0):
    n = int(SR * d); x = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f * m * x) * np.exp(-x * (1.2 + 1.6 * m)) for m, a in [(1, 1), (2.76, 0.32), (5.4, 0.12)])
    return s * env(n, 0.003, 9)


def pad(freqs, d):
    n = int(SR * d); x = np.arange(n) / SR; s = np.zeros(n)
    for f in freqs:
        for det in (-0.12, 0.0, 0.1):
            s += np.sin(2 * np.pi * f * (1 + det / 100) * x + rng.uniform(0, 6)) * 0.33
    a = min(0.5, d / 3); e = np.minimum(1, np.minimum(x / a, (d - x) / a))
    return s * np.clip(e, 0, 1) / len(freqs)


def kick(d=0.4):
    n = int(SR * d); x = np.arange(n) / SR
    return np.sin(2 * np.pi * (46 * x + 90 * (1 - np.exp(-x * 28)) / 28)) * env(n, 0.001, 0.13)


def snare(d=0.25):
    n = int(SR * d)
    return hp(rng.standard_normal(n), 900) * env(n, 0.001, 0.07) * 0.6 + np.sin(2 * np.pi * 190 * np.arange(n) / SR) * env(n, 0.001, 0.04) * 0.3


def hat(d=0.06):
    n = int(SR * d)
    return hp(rng.standard_normal(n), 6000) * env(n, 0.0005, 0.018)


def impact(d=2.6):
    n = int(SR * d); x = np.arange(n) / SR
    boom = np.sin(2 * np.pi * (38 * x + 120 * (1 - np.exp(-x * 9)) / 9)) * env(n, 0.002, 0.7)
    crack = hp(rng.standard_normal(n), 1500) * env(n, 0.0005, 0.05) * 0.5
    ring = sum(np.sin(2 * np.pi * f * x) * np.exp(-x * 1.4) for f in (293.7, 440.0, 587.3)) * 0.12 * env(n, 0.01, 9)
    return boom + crack + ring


def swell(d, fc=900):
    n = int(SR * d); y = lp(rng.standard_normal(n), fc) * np.sin(np.linspace(0, np.pi, n)) ** 2
    return y / (np.abs(y).max() + 1e-9)


out = np.zeros((N, 2), np.float32)
WS = TB["worlds"]
b = lambda x: x * BEAT
bar = 4 * BEAT


def whoosh(d, up=True, fc=4200):
    n = int(SR * d); x = np.linspace(0, 1, n)
    y = hp(lp(rng.standard_normal(n), fc), 500) * (x ** 3 if up else (1 - x) ** 3)
    return y / (np.abs(y).max() + 1e-9)


def pop_(f=520, d=0.14):
    n = int(SR * d); x = np.arange(n) / SR
    return np.sin(2 * np.pi * (f * x + 900 * (1 - np.exp(-x * 40)) / 40)) * np.exp(-x * 30)


def tick(f=3200, d=0.03):
    n = int(SR * d); x = np.arange(n) / SR
    return np.sin(2 * np.pi * f * x) * np.exp(-x * 200)


def thud(d=0.3):
    n = int(SR * d); x = np.arange(n) / SR
    return np.sin(2 * np.pi * 70 * x) * np.exp(-x * 22) + lp(rng.standard_normal(n), 900) * np.exp(-x * 34) * 0.5


def noiseh(d=0.1, fc=3000):
    n = int(SR * d); return hp(rng.standard_normal(n), fc) * env(n, 0.001, d / 3)


def clap():
    n = int(SR * 0.2); x = np.arange(n) / SR
    e = sum(np.exp(-np.maximum(x - o, 0) * 90) * (x >= o) for o in (0, 0.011, 0.023))
    return hp(rng.standard_normal(n), 1400) * e * 0.5


def bass(f, d):
    n = int(SR * d); x = np.arange(n) / SR
    s = np.tanh(2.2 * np.sin(2 * np.pi * f * x))
    return lp(s, 500) * env(n, 0.004, d * 0.7)


def sub(d=2.6):
    n = int(SR * d); x = np.arange(n) / SR
    return np.sin(2 * np.pi * (34 * x + 110 * (1 - np.exp(-x * 7)) / 7)) * np.exp(-x * 1.5)


ROOTS = [33, 29, 36, 31]  # A, F, C, G
CH = [[57, 60, 64], [53, 57, 60], [55, 60, 64], [55, 59, 62]]

# I · the dot: a fall, a bounce, the burst, the 12
add(out, 0, whoosh(BEAT, True, 2600), 0.14)
add(out, b(1), thud(), 0.6); add(out, b(1), pop_(330), 0.2)
add(out, b(2), thud(), 0.5); add(out, b(2), noiseh(0.4, 1800), 0.2)
for i in range(11): add(out, b(2) + i * 0.012, pluck(mtof(69 + [0, 3, 5, 7, 10, 12, 15, 17, 19, 22, 24][i]), 0.4), 0.05, pan=np.sin(i * 1.7) * 0.7)
add(out, b(3), kick(0.5), 0.6); add(out, b(3), noiseh(0.2, 2400), 0.16)
add(out, b(3.4), pad([mtof(45), mtof(52)], b(2.6)), 0.09)

# the track: it runs from the first world to the drop, then again from the wall's fold to the logo
def groove(a, z, build=True):
    i = 0; at = a
    while at < z - 0.01:
        p = (at - a) / max(z - a, 1e-9); g = 0.7 + 0.3 * p if build else 1.0
        add(out, at, kick(0.32), 0.52 * g)
        add(out, at + BEAT / 2, hat(), 0.08 * g, pan=0.3)
        if i % 2 == 1: add(out, at, clap(), 0.2 * g, pan=-0.05)
        if i % 4 == 0:
            k = (i // 4) % 4
            add(out, at, pad([mtof(m) for m in CH[k]], bar + 0.1), 0.07)
            for s in (0, 0.5, 0.75, 1.5, 2, 2.5, 3, 3.5): add(out, at + s * BEAT, bass(mtof(ROOTS[k]), BEAT * 0.45), 0.2 * g)
        at += BEAT; i += 1


groove(b(6), b(32))
groove(b(36.9), b(50), False)
groove(b(52), b(62), False)

# II · a dive before each world, and each world's own sound
ends = [w["b"] for w in WS]
for w in [6] + ends[1:]:
    d = 0.5 if w >= 31 else 0.42
    add(out, b(w) - d, whoosh(d + 0.02), 0.2)
sg = {
    0: lambda t: (add(out, t + b(1.55), thud(), 0.4), add(out, t + b(1.7), noiseh(0.1, 3400), 0.14), add(out, t + b(1.7), pop_(240), 0.22)),
    1: lambda t: [add(out, t + b(s), pop_(f), 0.18, pan=p) for s, f, p in [(0, 620, -0.3), (0.45, 760, 0.3), (0.9, 700, -0.3), (1.35, 880, 0)]],
    2: lambda t: (add(out, t, bell(mtof(76), 1.2), 0.08), add(out, t, bass(mtof(40), 0.4), 0.14)),
    3: lambda t: [add(out, t + b(0.7 + i * 0.08), tick(2400 + i * 170), 0.1) for i in range(8)],
    4: lambda t: [add(out, t + b(i * 0.25), noiseh(0.05, 2400), 0.1, pan=np.sin(i)) for i in range(6)],
    5: lambda t: [add(out, t + 0.03 * i, noiseh(0.03, 3600), 0.09, pan=0.3 * np.sin(i)) for i in range(16)],
    6: lambda t: [add(out, t + b(s + 0.25), thud(0.2), 0.3, pan=p) for s, p in [(0.25, -0.6), (0.1, -0.3), (0.45, 0), (0.35, 0.3), (0.2, 0.6)]],
    7: lambda t: [add(out, t + 0.04 * i, tick(3000), 0.12, pan=0.5 * np.sin(i * 0.7)) for i in range(16)],
    8: lambda t: ([add(out, t + 0.025 * i, tick(1500 + 40 * i, 0.02), 0.09) for i in range(17)], add(out, t + b(0.95), thud(), 0.7), add(out, t + b(0.95), noiseh(0.1, 2000), 0.2)),
    9: lambda t: add(out, t, swell(b(1.1), 2800), 0.14, pan=-0.2),
    10: lambda t: [add(out, t + 0.05 * i, pluck(mtof(76 + i * 2), 0.3), 0.08, pan=0.5 * np.sin(i)) for i in range(6)],
    11: lambda t: add(out, t, whoosh(BEAT, True, 6000), 0.14),
}
for i, w in enumerate(WS): sg[i](b(w["b"]))

# III · the riser into the silence; one beat of nothing at beat 32; the sub drop on the pull-back at 33
add(out, b(28), whoosh(b(4), True, 7000), 0.2)
sil0, sil1 = int(b(32) * SR), int(b(33) * SR)
out[sil0:sil1] *= 0.0
add(out, b(33), sub(), 0.5); add(out, b(33), noiseh(0.5, 900), 0.22)
add(out, b(33), whoosh(b(2), False, 3400), 0.2)
for i, f in enumerate([57, 64, 69, 72, 76]): add(out, b(33) + i * 0.02, bell(mtof(f), 2.6), 0.05)
for i in range(12): add(out, b(35 + i * 0.1 + 0.8), tick(1400 + i * 110, 0.05), 0.2, pan=(i - 5.5) / 8); add(out, b(35 + i * 0.1 + 0.8), thud(0.12), 0.14)
for j, ts in enumerate((37, 37.5, 38, 38.5)): add(out, b(ts), kick(0.28), 0.42); add(out, b(ts), noiseh(0.08, 3000), 0.12)

# IV · the press, the rings, five cards
add(out, b(41.5), thud(), 0.7); add(out, b(41.5), bell(mtof(81), 1.4), 0.1); add(out, b(41.5), whoosh(0.4, False), 0.14)
for j in range(5):
    add(out, b(42 + j), noiseh(0.12, 2600), 0.2, pan=(j - 2) * 0.3)
    add(out, b(42 + j) + 0.26, pluck(mtof([69, 72, 76, 79, 84][j]), 0.5), 0.13, pan=(j - 2) * 0.3)

# V · the days riffle, FRIDAY slams, three panels arrive
for j in range(4): add(out, b(50 + j * 0.5), noiseh(0.07, 2600), 0.24); add(out, b(50 + j * 0.5), kick(0.2), 0.3)
add(out, b(52), sub(1.8), 0.45); add(out, b(52), impact(), 0.16); add(out, b(52), bell(mtof(81), 2.2), 0.1)
for j in range(3): add(out, b(55 + j), whoosh(0.3, False, 3000), 0.14, pan=(j - 1) * 0.5); add(out, b(55 + j), bell(mtof([76, 79, 84][j]), 1.2), 0.08, pan=(j - 1) * 0.5)

# VI · back to the dot, one bounce, the chord
add(out, b(62), whoosh(b(0.9), True, 3000), 0.14)
add(out, b(63.4), thud(), 0.6); add(out, b(64.2), thud(), 0.5); add(out, b(64.4), whoosh(b(1), True, 2400), 0.14)
add(out, b(65.2), kick(0.6), 0.34)
for m, d in [(45, 0), (52, 0.03), (57, 0.06), (60, 0.09), (64, 0.12), (69, 0.15)]: add(out, b(65.2) + d, bell(mtof(m + 12), 3.4), 0.1)
add(out, b(65.2), pad([mtof(m) for m in [33, 45, 52, 57, 60]], DUR - b(65.2)), 0.1)

g = np.ones(N); t = np.arange(N) / SR
g *= np.where(t > DUR - 1.2, np.clip((DUR - t) / 1.2, 0, 1), 1)
out *= g[:, None]
out = out / max(np.abs(out).max(), 1e-9) * 0.89
os.makedirs(os.path.join(ROOT, "assets", "bgm"), exist_ok=True)
with wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
print("score:", round(DUR, 2), "s")
