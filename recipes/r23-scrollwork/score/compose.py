"""
R23 · Scrollwork. Original score, composed in code, timed to the film's one table (bake/table.json).

32 s at 100 bpm (0.6 s a beat) in D minor, opening to D major on the title, scored like an anime opening.
A low drone in the dark; a brush stroke hisses down the frame; the rod falls with a whistle and lands on a taiko hit
and a crash (every impact frame gets one). The spiral spins up over taiko and a tight high drum, a whoosh on every
smear frame, a riser into the pose. Plucked strings take the motif while the mark turns. The scroll flies on a
driving groove (kick, hats, a bass line on Dm, Bb, F, C), paper rustling under it, a wood block on every plate that
passes. The thumb grinds: a metal sizzle on every ride down the rod, a hit on every new site. The manga page slams
in on half beats and rolls into the title: one last hit, D major, a whoosh as the lockup wipes on, bells for the URL.
Usage: python score/compose.py  ->  assets/bgm/score.wav   (numpy only, deterministic)
"""
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
rng = np.random.default_rng(23)
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

# ---- the dark: a low drone, the brush, the rod falling
dr = (np.sin(2 * np.pi * hz(26) * tt) + 0.4 * np.sin(2 * np.pi * hz(38) * tt * 1.002)) * np.clip(tt / 1.2, 0, 1)
dr *= np.clip((T["title"] + 3 - tt) / 1.0, 0, 1)
L += 0.05 * dr
R += 0.05 * dr
add(swish(0.75, 400, 6000), 0.3, -0.2, 0.22)
add(swish(0.4, 2000, 9000), 0.62, 0.3, 0.1)
whistle(1.25, 1.8, 2600, 220, 0.06)

# ---- every impact frame: a taiko hit and a crash, the big ones with a sub boom
for d in TB["impacts"]:
    big = d["n"] >= 3
    add(taiko(52 if big else 66, 1.8 if big else 1.0), d["t"], 0.0, 0.62 if big else 0.42)
    add(crash(2.6 if big else 1.4), d["t"], 0.25, 0.16 if big else 0.08)
    if big:
        add(tone(hz(26), 1.6, a=0.002, rel=0.6), d["t"], 0.0, 0.3)

# ---- the spin: taiko on the beat, shime between, a whoosh on every smear frame, a riser into the pose
for k, b in enumerate(beats(T["spin"][0], T["pose"])):
    add(taiko(70, 0.6), b, -0.2, 0.3 if k % 2 == 0 else 0.2)
    add(shime(), b + BEAT / 2, 0.35, 0.16)
    if k % 4 == 3:
        add(shime(), b + BEAT * 0.75, -0.35, 0.12)
for f in TB["smears"]:
    t0 = f / FPS
    if T["spin"][0] <= t0 < T["pose"]:
        add(swish(0.14, 1200, 7000), t0 - 0.03, 0.4 * np.sin(f), 0.11)
add(swish(1.4, 300, 9000, rise=True), T["pose"] - 1.4, 0.0, 0.2)

# ---- the pose: plucked strings take the motif (D minor), a bass under it
MOTIF = [62, 65, 69, 67, 65, 64, 62, 57]
for k, m in enumerate(MOTIF):
    add(pluck(hz(m), 1.0, 0.62), T["pose"] + 0.15 + k * BEAT / 2, 0.3 * np.sin(k * 1.7), 0.17)
for k, b in enumerate(beats(T["pose"], T["scroll"][0])):
    add(pluck(hz(38), 0.7, 0.3), b, -0.1, 0.14)

# ---- the scroll: a driving groove, a bass line on Dm, Bb, F, C, rustling paper, a wood block per plate
CH = [[50, 53, 57], [46, 50, 53], [53, 57, 60], [48, 52, 55]]
for k, b in enumerate(beats(T["scroll"][0], T["thumb"][0])):
    add(kick(), b, 0.0, 0.42)
    if k % 2 == 1:
        add(snare(), b, 0.1, 0.13)
    add(hat(), b + BEAT / 2, 0.4, 0.05)
    add(hat(open_=k % 4 == 3), b + BEAT / 4 * 3, -0.4, 0.035)
    ch = CH[(k // 4) % 4]
    add(pluck(hz(ch[0] - 12), 0.55, 0.25), b, -0.15, 0.2)
    add(pluck(hz(ch[0] - 12), 0.4, 0.25), b + BEAT / 2, -0.15, 0.12)
    if k % 2 == 0:
        for j, m in enumerate(ch):
            add(pluck(hz(m + 12), 0.9, 0.6), b + 0.02 * j, -0.4 + 0.4 * j, 0.06)
MEL = [74, 72, 69, 72, 74, 77, 76, 74, 72, 69, 67, 69]
for k, m in enumerate(MEL):
    add(pluck(hz(m), 1.1, 0.68), T["scroll"][0] + 1.2 + k * BEAT, 0.25, 0.1)
rust = norm(highpass(rng.standard_normal(N), 1800)) * (0.5 + 0.5 * np.sin(2 * np.pi * 3.1 * tt) ** 2)
rmask = np.clip((tt - T["scroll"][0]) / 0.3, 0, 1) * np.clip((15.6 - tt) / 0.4, 0, 1)
L += 0.012 * rust * rmask
R += 0.012 * np.roll(rust, 777) * rmask
for k, s in enumerate(TB["stamps"]):
    add(block(780 + 60 * k), s, -0.4, 0.22)
    add(taiko(90, 0.4), s, 0.0, 0.18)
add(swish(1.2, 300, 8000, rise=True), T["thumb"][0] - 1.2, 0.0, 0.18)

# ---- the thumb: a metal sizzle on every ride down the rod, double-time hats, a hit on every new site
for k, s in enumerate(TB["swaps"]):
    n = int(1.15 * SR)
    u = np.arange(n) / n
    sz = norm(highpass(rng.standard_normal(n), 5200)) * (0.35 + 0.65 * (0.5 + 0.5 * np.sin(2 * np.pi * 37 * u * 1.15))) * np.sin(np.pi * u) ** 0.5
    add(sz, s + 0.04, 0.45, 0.06)
    for j in range(8):
        add(hat(), s + j * BEAT / 4, 0.4 if j % 2 else -0.4, 0.04)
    add(kick(), s, 0.0, 0.4)
    add(kick(), s + BEAT, 0.0, 0.32)
    add(snare(), s + BEAT * 1.5, 0.1, 0.12)
    ch = CH[k % 4]
    add(pluck(hz(ch[0] - 12), 1.0, 0.25), s, -0.1, 0.22)
    for j, m in enumerate(ch):
        add(pluck(hz(m + 12), 1.0, 0.6), s + 0.03 * j, -0.4 + 0.4 * j, 0.07)
    add(pluck(hz(MEL[k * 2 % len(MEL)] + 12), 0.8, 0.7), s + BEAT, 0.3, 0.07)
add(swish(1.2, 300, 9000, rise=True), T["cabinet"][0] - 1.2, 0.0, 0.2)

# ---- the cabinet: every panel slams on a half beat, then a roll into the title
for k, p in enumerate(TB["panels"]):
    add(taiko(110 - 6 * k, 0.5), p, -0.3 + 0.1 * k, 0.3)
    add(snare(), p, 0.2, 0.1)
for k in range(24):
    t0 = 25.9 + 1.7 * (1 - (1 - k / 24) ** 1.6)
    add(shime(), t0, 0.3 * (-1) ** k, 0.06 + 0.1 * k / 24)
add(swish(1.6, 300, 10000, rise=True), T["title"] - 1.6, 0.0, 0.24)

# ---- the title: D major, wide; a whoosh as the lockup wipes on; bells for the URL
tu = T["title"] + 1.5
for j, m in enumerate([26, 38, 45, 50, 54, 57, 62, 66, 69]):
    add(tone(hz(m), DUR - T["title"], a=0.04, rel=2.6, harm=(1, 0.3, 0.1), detune=0.0007), T["title"], -0.6 + 0.15 * j, 0.06)
for j, m in enumerate([62, 66, 69, 74, 78]):
    add(pluck(hz(m), 2.4, 0.6), T["title"] + 0.03 * j, -0.5 + 0.25 * j, 0.11)
add(swish(0.6, 800, 8000), tu - 0.1, -0.3, 0.14)
add(taiko(60, 1.4), tu, 0.0, 0.3)
for k, m in enumerate([78, 81, 86, 85, 81, 78, 74]):
    add(bell(hz(m + 12), 2.0), tu + 1.1 + k * 0.13, 0.4 * np.sin(k), 0.03)
add(bell(hz(74), 3.0), tu + 2.3, 0.0, 0.06)

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
