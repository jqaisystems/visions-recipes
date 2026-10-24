"""
R14 · Orrery. Original score, composed in code, timed to the film's table T (index.html).

32 s, D major with a Lydian lift. A clockwork escapement ticks on the beat (120 BPM) under everything. The brief types
and becomes a comet that strikes the sun; each ring wakes on a chime from one harmonic series; sources land as soft
pings; the writer's ribbon shimmers; the reviewer scans, buzzes once at the rejected piece, rises gold for the
escalation and chimes on the person's approval; the conjunction swells as every ring clicks into place and the beam
hits; the word lands on D add9. A quiet pad and soft plucks run under the whole film. Every sound has a release.
Usage: python score/compose.py  ->  assets/bgm/score.wav   (numpy only, deterministic)
"""
import os
import wave
import numpy as np

SR = 44100
DUR = 32.0
N = int(DUR * SR)
rng = np.random.default_rng(14)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "bgm", "score.wav")

# ---- the film's timing table (index.html T)
T = dict(type=(0.4, 1.9), ignite=2.2, hit=3.3, wake=(3.4, 4.2, 5.0), research=7.0, thread=(7.0, 8.8), frags=(7.6, 11.2),
         write=12.0, stream=(12.0, 13.8), ribbon=(12.8, 16.4), review=17.0, tiles=(17.0, 18.4), scan=(18.4, 19.4),
         red=19.3, back=(19.5, 20.4), fixed=(21.0, 21.7), gold=19.6, rise=(19.8, 20.3), click=20.85, down=(21.2, 21.7),
         merge=(21.9, 22.4), conj=22.0, beam=25.0, beads=(25.3, 27.6), end=27.8)
NF = 48

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


def S(*parts):
    out = np.zeros(max(len(x) for x in parts))
    for x in parts:
        out[: len(x)] += x
    return out


def sweep(f0, f1, dur, a=0.3, rel=0.2):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(np.geomspace(f0, f1, n)) / SR) * np.minimum(1, tt / a) * np.minimum(1, (dur - tt) / rel)


hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)

# ---- the clockwork: an escapement, tick and tock on the beat, louder once the orrery is alive
t = 0.0
k = 0
while t < T["beam"]:
    g = 0.10 if t < T["hit"] else 0.2
    f = 3400 if k % 2 == 0 else 2700
    add(S(noise(0.025, rel=0.006, cutoff=6000) * 0.6, tone(f, 0.04, rel=0.008) * 0.3), t, -0.2 if k % 2 == 0 else 0.2, g)
    t += 0.5
    k += 1

# ---- the brief: key ticks, Enter, the comet and its strike on the sun
for i in range(20):
    add(S(noise(0.03, rel=0.008) * 0.5, tone(2600 + 300 * (i % 3), 0.03, rel=0.006) * 0.25), T["type"][0] + 1.5 * i / 19, -0.2, 0.3)
add(S(tone(140, 0.25, rel=0.07, harm=(1, 0.3)), noise(0.08, rel=0.02, cutoff=900) * 0.6), T["ignite"], 0, 0.5)
add(S(noise(T["hit"] - T["ignite"], a=0.6, rel=0.05, cutoff=3000), sweep(300, 1400, T["hit"] - T["ignite"], a=0.5, rel=0.05) * 0.3), T["ignite"], -0.5, 0.28)
add(S(tone(hz(26), 2.5, rel=0.7, harm=(1, 0.5)), noise(0.4, rel=0.12, cutoff=500)), T["hit"], 0, 0.6)
for j, m in enumerate([50, 57, 62, 66, 69]):
    add(tone(hz(m), 3.0, a=0.01, rel=1.0, harm=(1, 0.3, 0.1)), T["hit"], -0.4 + 0.2 * j, 0.12)

# ---- the agents wake: one chime each, from one harmonic series on D, and a brass swing
f0 = hz(38)
for i, tw in enumerate(T["wake"]):
    add(noise(0.6, a=0.2, rel=0.12, cutoff=1200), tw, -0.4 + 0.4 * i, 0.15)
    add(tone(f0 * (6 + 2 * i), 1.8, rel=0.6, harm=(1, 0.4, 0.15)), tw + 0.5, -0.4 + 0.4 * i, 0.3)

# ---- research: a thread from the sun, then each source lands with a soft ping
add(sweep(400, 900, T["thread"][1] - T["thread"][0], a=0.4, rel=0.4) * 0.5, T["thread"][0], -0.3, 0.1)
PENTA = [74, 76, 78, 81, 83, 86, 88, 90]
for kk in range(NF):
    ta = T["frags"][0] + 1.0 + (T["frags"][1] - T["frags"][0] - 1.0) * kk / (NF - 1)
    add(tone(hz(PENTA[(kk * 5) % 8]), 0.35, rel=0.1, harm=(1, 0.2)), ta, -0.6 + 1.2 * ((kk * 7) % 11) / 10, 0.07)

# ---- write: the stream on, then the ribbon's shimmer
add(sweep(500, 1100, T["stream"][1] - T["stream"][0], a=0.4, rel=0.4) * 0.5, T["stream"][0], 0, 0.1)
n = int((T["ribbon"][1] - T["ribbon"][0]) * SR); tt = np.arange(n) / SR
sh = sum(np.sin(2 * np.pi * hz(m) * tt + 2 * np.sin(2 * np.pi * 5.5 * tt)) for m in (81, 85, 88)) / 3
add(sh * np.minimum(1, tt / 0.6) * np.minimum(1, (tt[-1] - tt) / 0.8), T["ribbon"][0], 0.2, 0.06)

# ---- review: tiles arrive, a scan, one rejected (buzz), one escalated (gold rise), a click and an approval
for j in range(6):
    add(tone(hz(69 + 2 * j), 0.3, rel=0.08, harm=(1, 0.3)), T["tiles"][0] + 0.3 + (T["tiles"][1] - T["tiles"][0] - 0.3) * j / 5, -0.5 + 0.2 * j, 0.12)
add(noise(T["scan"][1] - T["scan"][0], a=0.3, rel=0.25, cutoff=2400), T["scan"][0], 0.3, 0.15)
n = int(0.35 * SR); tt = np.arange(n) / SR
buzz = np.sign(np.sin(2 * np.pi * 92 * tt)) * env(n, 0.005, 0.12)
add(lowpass(buzz, 900), T["red"], 0.2, 0.25)
add(noise(0.6, a=0.15, rel=0.15, cutoff=1500), T["back"][0], -0.3, 0.12)
add(sweep(hz(74), hz(86), T["rise"][1] - T["rise"][0] + 0.3, a=0.1, rel=0.25) * 0.6, T["gold"], 0.3, 0.2)
add(S(noise(0.02, rel=0.005), tone(3200, 0.02, rel=0.004) * 0.3), T["click"] - 0.02, 0.3, 0.35)
add(tone(hz(81), 0.7, rel=0.25, harm=(1, 0.3)), T["click"] + 0.1, 0.3, 0.3)
add(tone(hz(86), 0.8, rel=0.28, harm=(1, 0.3)), T["click"] + 0.22, 0.3, 0.26)
add(tone(hz(78), 0.6, rel=0.2, harm=(1, 0.3)), T["fixed"][1], -0.2, 0.2)

# ---- the conjunction: a long swell, every ring clicks into place, then the beam hits
dur = T["beam"] - T["conj"] + 0.2
add(S(sweep(hz(38), hz(62), dur, a=2.2, rel=0.08) * 0.6, noise(dur, a=2.4, rel=0.06, cutoff=3500) * 0.5), T["conj"], 0, 0.25)
for i in range(3):
    tc = T["conj"] + 1.7 + 0.45 * (2 - i)
    add(S(noise(0.05, rel=0.012, cutoff=5000), tone(hz(86 - 5 * i), 0.5, rel=0.15, harm=(1, 0.4))), tc, -0.5 + 0.5 * i, 0.3)
add(S(tone(hz(26), 3.5, rel=1.0, harm=(1, 0.5, 0.2)), noise(0.6, rel=0.18, cutoff=800)), T["beam"], 0, 0.75)
for j, m in enumerate([38, 50, 57, 62, 66, 69, 74]):
    add(tone(hz(m), 2.5, a=0.004, rel=0.9, harm=(1, 0.3)), T["beam"], -0.6 + 0.2 * j, 0.1)

# ---- the beads: a falling shimmer of plucks, then the word lands on D add9
for kk in range(24):
    add(tone(hz([86, 83, 81, 78, 76, 74][kk % 6] + (12 if kk % 4 == 0 else 0)), 0.5, rel=0.15, harm=(1, 0.2)), T["beads"][0] + 0.09 * kk, -0.6 + 1.2 * (kk % 7) / 6, 0.06)
for j, m in enumerate([38, 50, 57, 62, 64, 66, 69]):
    add(tone(hz(m), 4.4, a=0.004, rel=1.6, harm=(1, 0.35, 0.12), detune=0.0007), T["beads"][1], -0.5 + 0.17 * j, 0.15)

# ---- the bed: a quiet pad and soft plucks under the whole film (Dmaj9, Bm9, Gmaj7#11, A sus), resolving to D
PROG = [[50, 57, 61, 64, 66], [47, 54, 57, 61, 62], [43, 50, 54, 59, 61], [45, 52, 57, 59, 64]]
BAR = 2.0
t0, kk = T["hit"], 0
while t0 < T["beads"][1] - 0.05:
    chord = PROG[kk % 4]
    d = min(BAR, T["beads"][1] - t0) + 0.9
    for j, m in enumerate(chord):
        n = int(d * SR); tt = np.arange(n) / SR
        pad = sum(h * np.sin(2 * np.pi * hz(m) * (q + 1) * tt * (1 + 0.0015 * q)) for q, h in enumerate((1, 0.35, 0.15)))
        add(pad * np.minimum(1, tt / 0.7) * np.minimum(1, (d - tt) / 0.9), t0, -0.5 + 0.25 * j, 0.03)
    for s in range(8):
        ts = t0 + s * BAR / 8
        if ts >= T["beam"] - 0.2:
            continue
        pl = lowpass(tone(hz(chord[[0, 2, 1, 3, 2, 4, 3, 2][s]] + 12), 0.45, a=0.003, rel=0.16, harm=(1, 0.4, 0.15)), 3600)
        add(pl, ts, -0.35 + 0.1 * s, 0.04)
    t0 += BAR
    kk += 1

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
