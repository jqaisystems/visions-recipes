"""The score for R38 alternative · Echo, composed in code at 112 bpm and timed to bake/table.json:
  a ticking pen and a low hum under the ridgelines; from the brief on, a pulse (soft kick, brushed snare, closed hat)
  on D minor, B flat, F, C; a rising pluck and a slam for each of the brief's words; the client's question hitting
  word by word, then one deep impact with a ringing tail; the live objection, then the same impact doubled with its
  own echo; two filtered voice-like synths for the duet (never speech); a click for each debrief line; the
  ridgelines again; a resolving chord on the lockup.
Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py"""
import json, os, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TB = json.load(open(os.path.join(ROOT, "bake", "table.json"), encoding="utf-8"))
SR = 48000; DUR = TB["dur"]; BEAT = TB["beat"]; N = int(SR * DUR); T = TB["T"]
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
CH = [[62, 65, 69], [58, 62, 65], [65, 69, 72], [60, 64, 67]]     # Dm, Bb, F, C
BASS = [38, 34, 41, 36]
bar = 4 * BEAT

# I · the ridgelines: a pen ticking as each ridge is laid, a low hum
for a, z in TB["ridges"]:
    t = a
    while t < z:
        add(out, t, hp(rng.standard_normal(int(0.012 * SR)), 3000) * env(int(0.012 * SR), 0.0005, 0.004), 0.08, pan=0.3 * np.sin(t * 3))
        t += 3 / 30
    add(out, a, pad([mtof(38), mtof(45)], z - a + 0.4), 0.09)

# the harmony and the pulse, from the brief to the lockup (quieter under the duet, out under the impacts' tails)
k = 0; at = T["prep"][0]
while at < T["mark"]:
    ch = CH[(k // 2) % 4]
    if k % 2 == 0:
        add(out, at, pad([mtof(m - 12) for m in ch], 2 * bar + 0.2), 0.05)
        add(out, at, pad([mtof(BASS[(k // 2) % 4])], 2 * bar + 0.1), 0.07)
    k += 1; at += bar
at = T["prep"][0]; i = 0
while at < T["mark"] - 0.01:
    quiet = T["duet"][0] <= at < T["debrief"][0]
    g = 0.55 if quiet else 1.0
    if not (TB["qImpact"] <= at < TB["qImpact"] + 1.2 or TB["oImpact"] <= at < TB["oImpact"] + 1.4):
        if i % 2 == 0: add(out, at, kick(), 0.42 * g)
        if i % 4 == 2: add(out, at, snare(), 0.16 * g, pan=0.1)
        add(out, at + BEAT / 2, hat(), 0.07 * g, pan=0.4)
        add(out, at, hat(), 0.04 * g, pan=-0.4)
    at += BEAT; i += 1

# II · the brief: a slam and a rising pluck per word
PENT = [62, 65, 67, 69, 72, 74, 77, 79]
for j, (ts, w) in enumerate(TB["words"]):
    add(out, ts, kick(0.3), 0.3)
    add(out, ts, hp(rng.standard_normal(int(0.15 * SR)), 2500) * env(int(0.15 * SR), 0.001, 0.04), 0.12, pan=0.5 * np.sin(j * 1.3))
    add(out, ts + 0.01, pluck(mtof(PENT[j]), 0.6), 0.1, pan=0.5 * np.sin(j * 1.3))

# III · the question, word by word, then the impact
for j, (ts, w) in enumerate(TB["question"]):
    add(out, ts, pluck(mtof([74, 72, 69, 65][j]), 0.8, 0.6), 0.11)
    add(out, ts, kick(0.25), 0.22)
add(out, TB["qImpact"] - 0.6, swell(0.6, 2200), 0.08)
add(out, TB["qImpact"], impact(), 0.5)
add(out, TB["qImpact"], bell(mtof(74), 3.0), 0.06)

# IV · the objection, live, then the same impact with its own echo
for j, (ts, w) in enumerate(TB["objection"]):
    add(out, ts, pluck(mtof([74, 72, 69][j]), 0.8, 0.6), 0.11)
    add(out, ts, kick(0.25), 0.25)
add(out, TB["oImpact"] - 0.6, swell(0.6, 2200), 0.09)
add(out, TB["oImpact"], impact(), 0.5, pan=0.15)
add(out, TB["oImpact"] + 0.012, impact(), 0.3, pan=-0.35)
add(out, TB["oImpact"], bell(mtof(74), 3.0), 0.06, pan=-0.4)
add(out, TB["oImpact"] + 0.02, bell(mtof(86), 3.0), 0.04, pan=0.4)
add(out, TB["help"], bell(mtof(81), 1.4), 0.04)
add(out, TB["settle"], swell(1.0, 1200), 0.06)

# V · the duet: two voice-like synths, shaped by the table's envelopes, never speech
s0, s1 = T["duet"][0], T["debrief"][0] + 0.3
n = int((s1 - s0) * SR)
ENV = np.array(TB["env"])
tt = np.arange(n) / SR + s0
for side, pan, fc, f0 in [(0, -0.5, 1100, 196), (1, 0.5, 1500, 247)]:
    e = np.interp(tt, np.arange(len(ENV)) / 30, ENV[:, side])
    syl = 0.5 + 0.5 * np.sin(2 * np.pi * 4.6 * tt + side) * np.sin(2 * np.pi * 1.9 * tt)
    ph = 2 * np.pi * np.cumsum(f0 * (1 + 0.03 * np.sin(2 * np.pi * 0.8 * tt + side))) / SR
    voice = lp(np.sign(np.sin(ph)) * 0.5 + 0.4 * rng.standard_normal(n), fc)
    add(out, s0, voice * e * syl, 0.1, pan=pan)
add(out, TB["trans"], bell(mtof(81), 1.4), 0.05, pan=0.3)
add(out, TB["trans"] + 0.8, swell(0.7, 3000), 0.04)

# VI · the debrief: the pull, then a click for each line
add(out, TB["pull"][0], swell(TB["pull"][1] - TB["pull"][0], 700), 0.08)
for j, (ts, txt) in enumerate(TB["db"]):
    add(out, ts, hp(rng.standard_normal(int(0.01 * SR)), 4000) * env(int(0.01 * SR), 0.0005, 0.004), 0.25)
    add(out, ts + 0.01, pluck(mtof([74, 77, 81, 86][j]), 0.7), 0.08)

# VII · the lockup: a resolving chord
add(out, T["mark"] - 0.5, swell(0.5, 1800), 0.06)
for m, d in [(50, 0), (57, 0.03), (62, 0.06), (65, 0.09), (69, 0.12), (74, 0.15)]:
    add(out, T["mark"] + d, bell(mtof(m), 3.4), 0.08)
add(out, T["mark"], kick(0.6), 0.45)
add(out, T["mark"], pad([mtof(m) for m in [38, 45, 50, 53, 57]], DUR - T["mark"]), 0.08)

g = np.ones(N); fi = int(0.25 * SR); g[:fi] = np.linspace(0, 1, fi)
t = np.arange(N) / SR
g *= np.where(t > DUR - 1.4, np.clip((DUR - t) / 1.4, 0, 1), 1)
out *= g[:, None]
out = out / max(np.abs(out).max(), 1e-9) * 0.89
os.makedirs(os.path.join(ROOT, "assets", "bgm"), exist_ok=True)
with wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
print("score:", round(DUR, 2), "s")
