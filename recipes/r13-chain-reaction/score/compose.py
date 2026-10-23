"""
R13 · Chain Reaction. Original score, composed in code from the machine's own run.

34 s. The physics bake (bake/bake.mjs) writes every impact to bake/events.json in physics time. The film plays the
physics on its own clock (slow motion through the dominoes, a 2 s freeze at the bell), so this script runs the same
time remap as index.html and places every impact at its film time. Impacts in the slow motion play lower and longer,
like slowed tape. Under it, a 120 BPM pulse in D minor that goes muffled in the slow motion and drops out in the
freeze, where the bell's partials hang and a reverse swell rises into the thaw. Then the bell rings out, a riser
carries the pull-back, an arpeggio follows the beads and F add9 lands on the word. Every sound has a release.
Usage: python score/compose.py  ->  assets/bgm/score.wav   (numpy only, deterministic)
"""
import json
import os
import wave
import numpy as np

SR = 44100
DUR = 34.0
N = int(DUR * SR)
rng = np.random.default_rng(13)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "bgm", "score.wav")
EV = json.load(open(os.path.join(HERE, "..", "bake", "events.json"), encoding="utf-8"))
M, EVENTS = EV["marks"], EV["events"]
P_END = 19.0 - 0.05

# ---- the film's clock drives the physics clock: the same remap as physAt() in index.html
cl = lambda v, a=0.0, b=1.0: min(b, max(a, v))
rr = lambda t, a, b: cl((t - a) / (b - a))
ss = lambda u: u * u * (3 - 2 * u)
SLOW = (M["domino"] - 0.2, M["relay"] + 0.3)
FREEZE_P, HOLD = M["bell"] + 0.09, 2.0
FT, PT, RATE = [], [], []
p, frozen_at, i = 0.0, None, 0
while True:
    t = i / 240
    if t > DUR + 1e-9:
        break
    in_slow = ss(rr(p, SLOW[0] - 0.25, SLOW[0])) * (1 - ss(rr(p, SLOW[1], SLOW[1] + 0.25)))
    rate = 1 + (0.3 - 1) * in_slow
    if frozen_at is None:
        rate *= 1 + (0.12 - 1) * ss(rr(p, FREEZE_P - 0.35, FREEZE_P))
        if p >= FREEZE_P:
            frozen_at = t
    if frozen_at is not None:
        s = t - frozen_at
        rate = 0.0 if s < HOLD else 0.12 + (1 - 0.12) * ss(rr(s, HOLD, HOLD + 0.6))
    FT.append(t); PT.append(p); RATE.append(rate)
    p = min(P_END, p + rate / 240)
    i += 1
# the film samples its remap every 8th step (30 per second); sample the same way so sound and picture agree exactly
FT, PT, RATE = np.array(FT)[::8], np.array(PT)[::8], np.array(RATE)[::8]


def film_at(phys):
    k = int(np.searchsorted(PT, phys - 1e-6))
    return float(FT[min(k, len(FT) - 1)])


def rate_at(t):
    return float(RATE[min(len(RATE) - 1, int(round(t * 30)))])


F = {k: film_at(v) for k, v in M.items()}
F_FREEZE = film_at(FREEZE_P)
F_THAW = F_FREEZE + HOLD
T_PB = (F["out"] + 2.0, F["out"] + 4.5)
T_BEAD = (T_PB[1] - 0.5, T_PB[1] + 2.2)
T_END = T_BEAD[1] + 0.2
print("film marks", {k: round(v, 2) for k, v in F.items()}, "freeze", round(F_FREEZE, 2))

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


hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
xpan = lambda x: float(np.clip((x - 2500) / 2600, -0.7, 0.7))

# ---- the trigger: one key tick per character, Enter, and the ball condensing out of light
for k in range(19):
    add(S(noise(0.03, rel=0.008) * 0.5, tone(2600 + 300 * (k % 3), 0.03, rel=0.006) * 0.25), 0.35 + 1.4 * k / 18, -0.3, 0.3)
add(S(tone(140, 0.25, rel=0.07, harm=(1, 0.3)), noise(0.08, rel=0.02, cutoff=900) * 0.6), 2.25, 0, 0.55)
n = int(1.2 * SR); tt = np.arange(n) / SR
add(np.sin(2 * np.pi * np.cumsum(np.linspace(hz(62), hz(86), n)) / SR) * np.minimum(1, tt / 0.9) * np.exp(-np.maximum(0, tt - 1.0) / 0.08), 1.25, 0, 0.12)
add(tone(hz(86), 1.2, rel=0.4, harm=(1, 0.5, 0.2)), 2.4, 0, 0.28)

# ---- the machine, impact by impact, at film time; in slow motion the sound is pitched down and stretched
PENTA = [62, 65, 67, 69, 72, 74, 77, 79, 81, 84]
last, dom = {}, 0
for e in EVENTS:
    pair = "-".join(sorted([e["a"], e["b"]]))
    ph, v = e["t"], e["v"]
    if ph < M["drop"] or ph > 18.0:
        continue
    if ph - last.get(pair, -1) < 0.04:
        continue
    last[pair] = ph
    t = film_at(ph)
    sl = rate_at(t)
    pf = max(0.45, sl ** 0.6)           # pitch factor: lower in the slow motion
    st = 1 / max(0.35, sl ** 0.5)       # decay stretch
    g = float(np.clip(v / 6, 0.15, 1.0))
    if pair in ("ball-track", "ball2-track"):
        if v > 1.5:
            add(noise(0.06 * st, rel=0.02 * st, cutoff=700), t, 0, 0.16 * g)
    elif pair in ("ball-tray", "stop-tray"):
        add(S(tone(180 * pf, 0.4, rel=0.09 * st, harm=(1, 0.5, 0.2)), noise(0.05, rel=0.015, cutoff=1400) * 0.4), t, -0.3, 0.5 * g)
    elif pair == "domino-domino":
        add(S(tone((520 + 60 * dom) * pf, 0.5, rel=0.05 * st, harm=(1, 0.6, 0.3)), noise(0.05, rel=0.012 * st, cutoff=3000) * 0.5), t, -0.2 + 0.05 * dom, 0.55)
        add(tone(hz(57) * pf, 0.9, rel=0.25 * st, harm=(1, 0.3)), t, 0, 0.18)   # a low thump under each slab
        dom += 1
    elif pair in ("ball-domino", "domino-floor"):
        add(S(tone(420 * pf, 0.4, rel=0.04 * st, harm=(1, 0.5)), noise(0.04, rel=0.01, cutoff=2400) * 0.4), t, 0, 0.32 * g)
    elif pair == "ball2-peg":
        add(tone(hz(PENTA[int(np.clip(v * 2, 0, len(PENTA) - 1))]), 0.7, rel=0.22, harm=(1, 0.25, 0.08)), t, 0.1, 0.42)
    elif pair == "ball2-funnel":
        add(tone(220, 0.25, rel=0.06, harm=(1, 0.4)), t, 0.15, 0.35 * g)
    elif pair == "ball2-gate":
        add(S(tone(98, 0.5, rel=0.12, harm=(1, 0.5, 0.25)), noise(0.06, rel=0.02, cutoff=1200) * 0.4), t, 0.3, 0.6)
    elif pair in ("ball2-floor", "ball2-stop"):
        add(tone(160, 0.25, rel=0.06, harm=(1, 0.3)), t, 0.5, 0.3 * g)

# ---- the human tick, then the gate lifts
add(S(noise(0.02, rel=0.005), tone(3200, 0.02, rel=0.004) * 0.3), F["open"] - 0.62, 0.3, 0.35)   # the click
add(tone(hz(81), 0.6, rel=0.2, harm=(1, 0.3)), F["open"] - 0.5, 0.3, 0.38)
add(tone(hz(86), 0.7, rel=0.25, harm=(1, 0.3)), F["open"] - 0.38, 0.3, 0.32)
add(noise(0.6, a=0.15, rel=0.15, cutoff=1800), F["open"], 0.3, 0.2)

# ---- the bell: a strike, the partials frozen in the air, a reverse swell, then the full ring on the thaw
f0 = hz(77)
BELL = ((1, 1.0, 1.6), (2.0, 0.5, 1.0), (2.76, 0.35, 0.7), (5.4, 0.2, 0.35), (8.9, 0.1, 0.18))
n = int(0.4 * SR); tt = np.arange(n) / SR
add(sum(a * np.sin(2 * np.pi * f0 * k * tt) for k, a, d in BELL) * env(n, 0.002, 0.12), F["bell"], 0.4, 0.4)
n = int(HOLD * SR); tt = np.arange(n) / SR
frozen = sum(a * np.sin(2 * np.pi * f0 * k * tt + 3 * np.sin(2 * np.pi * 0.35 * tt * k)) for k, a, d in BELL)
add(frozen * np.minimum(1, tt / 0.25) * np.minimum(1, (HOLD - tt) / 0.3) * 0.5, F_FREEZE, 0.2, 0.3)
n = int(1.4 * SR); tt = np.arange(n) / SR
swell = rng.standard_normal(n) * (tt / tt[-1]) ** 3
add(lowpass(swell, 2500) / 3 + np.sin(2 * np.pi * hz(65) * tt) * (tt / tt[-1]) ** 2 * 0.4, F_THAW - 1.4, 0, 0.35)
n = int(3.6 * SR); tt = np.arange(n) / SR
ring = sum(a * np.sin(2 * np.pi * f0 * k * tt) * np.exp(-tt / d) for k, a, d in BELL)
ring[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))
add(ring, F_THAW, 0.4, 0.55)
add(S(tone(hz(38), 1.6, rel=0.5, harm=(1, 0.4)), noise(0.25, rel=0.07, cutoff=600) * 0.8), F_THAW, 0, 0.5)   # the impact lands

# ---- the report: a swish, then a confirmation chime
add(noise(0.5, a=0.1, rel=0.12, cutoff=2600), F["out"] + 0.15, 0.4, 0.25)
add(S(tone(hz(79), 0.8, rel=0.28, harm=(1, 0.3)), tone(hz(84), 0.8, rel=0.28) * 0.6), F["out"] + 0.9, 0.4, 0.3)

# ---- the pulse: 120 BPM eighths in D minor; muffled in the slow motion, silent in the freeze
BEAT = 0.5
ROOTS = [(0.0, 38), (F["tray"] - 0.3, 34), (F["pegs"] - 0.3, 31), (F["open"] - 0.6, 33), (F_THAW, 34), (T_PB[0], 36)]
t = 2.4
while t < T_BEAD[0]:
    root = [m for (t0, m) in ROOTS if t >= t0][-1]
    sl = rate_at(t)
    if not (F_FREEZE - 0.05 < t < F_THAW):
        b = tone(hz(root), 0.24, a=0.004, rel=0.07, harm=(1, 0.55, 0.25))
        b = lowpass(b, 300 + 2600 * sl ** 1.5)
        add(b, t, 0, 0.22 * (0.6 + 0.4 * sl))
        if int(round(t / BEAT * 2)) % 4 == 0:   # a soft kick on the beat
            n = int(0.25 * SR); tt = np.arange(n) / SR
            add(np.sin(2 * np.pi * np.cumsum(np.linspace(120, 45, n)) / SR) * np.exp(-tt / 0.07), t, 0, 0.3 * (0.5 + 0.5 * sl))
    t += BEAT / 2

# ---- the pull-back: air and a riser that falls away into the beads
n = int((T_PB[1] - T_PB[0] + 0.6) * SR); tt = np.arange(n) / SR
add(np.sin(2 * np.pi * np.cumsum(np.linspace(hz(50), hz(74), n)) / SR) * np.minimum(1, tt / 1.5) * np.exp(-np.maximum(0, tt - (T_PB[1] - T_PB[0])) / 0.2), T_PB[0], 0, 0.16)
add(noise(T_PB[1] - T_PB[0] + 0.6, a=1.6, rel=0.35, cutoff=3000), T_PB[0], 0, 0.12)

# ---- the beads fly into the word: a rising arpeggio, then F add9 lands
for k, m in enumerate([65, 69, 72, 77, 79, 81, 84, 89]):
    add(tone(hz(m), 1.0, rel=0.35, harm=(1, 0.3, 0.1)), T_BEAD[0] + 0.28 * k, -0.6 + 0.17 * k, 0.2)
for k, m in enumerate([41, 53, 57, 60, 65, 67, 69]):
    add(tone(hz(m), 5.0, a=0.004, rel=1.6, harm=(1, 0.35, 0.12), detune=0.0007), T_BEAD[1], -0.5 + 0.17 * k, 0.16)
add(noise(0.3, rel=0.08, cutoff=900), T_BEAD[1], 0, 0.3)

# ---- the music bed: a quiet pad and a soft plucked arpeggio under the whole film, so it never feels bare.
# Dm, Bb, F, C, one chord per bar (2 s at 120 BPM), on the same grid as the pulse; it resolves to F for the word.
PROG = [[50, 53, 57, 62], [46, 50, 53, 58], [41, 48, 53, 57], [48, 52, 55, 60]]
BAR = 2.0
t0, k = 0.6, 0
while t0 < T_BEAD[1] - 0.05:
    chord = PROG[k % 4]
    dur = min(BAR, T_BEAD[1] - t0) + 0.9
    for j, m in enumerate(chord):   # pad: slow attack, overlapping release, gently detuned
        n = int(dur * SR); tt = np.arange(n) / SR
        pad = sum(h * np.sin(2 * np.pi * hz(m) * (q + 1) * tt * (1 + 0.0015 * q)) for q, h in enumerate((1, 0.35, 0.15)))
        e = np.minimum(1, tt / 0.7) * np.minimum(1, (dur - tt) / 0.9)
        add(pad * e, t0, -0.5 + 0.33 * j, 0.035)
    # the arpeggio: chord tones an octave up on eighths, muffled in the slow motion, silent in the freeze
    for s in range(8):
        ts = t0 + s * BAR / 8
        if ts >= T_BEAD[0] or F_FREEZE - 0.1 < ts < F_THAW:
            continue
        sl = rate_at(ts)
        note = chord[[0, 2, 1, 3, 2, 1, 3, 2][s]] + 12
        pl = tone(hz(note), 0.45, a=0.003, rel=0.16, harm=(1, 0.4, 0.15))
        pl = lowpass(pl, 900 + 3200 * sl ** 1.5)
        add(pl, ts, -0.35 + 0.1 * s, 0.05 * (0.55 + 0.45 * sl))
    t0 += BAR
    k += 1
# the bed lands on F with the word
for j, m in enumerate([41, 48, 53, 57, 60]):
    n = int(4.5 * SR); tt = np.arange(n) / SR
    pad = sum(h * np.sin(2 * np.pi * hz(m) * (q + 1) * tt) for q, h in enumerate((1, 0.35, 0.15)))
    add(pad * np.minimum(1, tt / 0.4) * np.exp(-tt / 2.2), T_BEAD[1], -0.4 + 0.2 * j, 0.04)

# ---- master: peak-normalise, then a soft fade at the very end
mix = np.stack([L, R], axis=1)
mix /= np.max(np.abs(mix))
DRIVE = 2.6                                           # a soft-clip master: lifts the body, keeps the peaks round
mix = np.tanh(mix * DRIVE) / np.tanh(DRIVE) * 0.84
fade = int(0.6 * SR)
mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
data = (mix * 32767).astype("<i2").tobytes()
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with wave.open(OUT, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data)
print("wrote", os.path.normpath(OUT), DUR, "s")
