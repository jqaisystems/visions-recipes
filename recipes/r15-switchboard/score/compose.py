"""
R15 · Switchboard. Original score, composed in code, timed to the film's PATCHES and T (index.html).

32 s, F major, 120 BPM with a swing feel: a 1940s rhythm section reimagined (walking bass, brushed hats, soft piano
stabs). Two old telephone rings open it; every patch is a lift, a brass click as each plug lands, a zip of light down
the wire and a small chime for its card. The urgent request thins the band to the bass, pulses an alarm and rings a
bell when a person picks up; the rush adds horn stabs on every patch; the lamps turning green climb a run; the neon
sign hums and crackles into the last chord. Every sound has a release.
Usage: python score/compose.py  ->  assets/bgm/score.wav   (numpy only, deterministic)
"""
import os
import wave
import numpy as np

SR = 44100
DUR = 32.0
N = int(DUR * SR)
rng = np.random.default_rng(15)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "bgm", "score.wav")

# ---- the film's table (index.html PATCHES, T)
PATCHES = [("INBOX", "SUPPORT", 3.4, 1.0, True), ("FORMS", "CRM", 9.0, 1.0, True), ("CHAT", "SALES", 10.5, 1.0, True),
           ("CALENDAR", "OPS", 12.0, 1.0, True), ("MAIL", "BILLING", 13.2, 1.0, True), ("ALERTS", "ON CALL", 16.4, 1.8, True),
           ("WEBHOOKS", "PRODUCT", 20.0, 0.7, False), ("SURVEYS", "SUCCESS", 20.5, 0.7, False), ("TICKETS", "ARCHIVE", 21.0, 0.7, False),
           ("INVOICES", "FINANCE", 21.5, 0.7, False), ("LEADS", "MARKETING", 22.0, 0.7, False), ("SHEETS", "LEGAL", 22.5, 0.7, False)]
T = dict(route=3.4, enrich=9.0, decide=15.0, connect=20.0, green=(23.6, 24.6), pull=(24.2, 26.6), neon=26.0, end=28.4)
NEON_CONTOURS = 13


def tm(p):
    _, _, t0, s, _ = p
    return dict(blink=t0 - 1.1 * s, aFly=(t0, t0 + 0.45 * s), bFly=(t0 + 0.25 * s, t0 + 0.7 * s), pulse=(t0 + 0.75 * s, t0 + 1.25 * s), lit=t0 + 1.25 * s, card=t0 + 1.3 * s)


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


def phone_ring(dur=0.9):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    bell = sum(a * np.sin(2 * np.pi * f * tt) for f, a in ((1180, 1.0), (1720, 0.6), (2640, 0.3)))
    return bell * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 20 * tt))) * env(n, 0.005, 0.5)


def click(g=1.0):
    return S(noise(0.03, rel=0.006, cutoff=7000) * 0.8, tone(2400, 0.12, rel=0.03, harm=(1, 0.5, 0.3)) * 0.4, tone(180, 0.08, rel=0.02) * 0.5) * g


# ---- the room and the first rings
add(noise(3.0, a=1.0, rel=1.0, cutoff=500), 0, 0, 0.04)
add(phone_ring(), 0.6, -0.4, 0.22)
add(phone_ring(), 1.8, -0.4, 0.22)

# ---- the band: F6, D7, Gm7, C7, one chord per bar (2 s at 120 BPM), from the first patch to the green wave
BEAT = 0.5
CHORDS = [(41, [57, 60, 62, 65]), (38, [54, 57, 60, 62]), (43, [58, 62, 65, 67]), (36, [52, 55, 58, 62])]
WALK = [[0, 4, 7, 9], [0, 3, 6, 9], [0, 3, 7, 10], [0, 4, 7, 10]]
t, beat = T["route"] - 0.6, 0
while t < T["green"][1]:
    bar = int(beat // 4) % 4
    root, chord = CHORDS[bar]
    in_alarm = T["decide"] < t < 18.6
    # walking bass on every beat
    add(lowpass(tone(hz(root + WALK[bar][beat % 4]), 0.45, a=0.004, rel=0.18, harm=(1, 0.45, 0.2)), 700), t, 0, 0.32)
    if not in_alarm:
        # brushed hats: a swung pair of eighths
        add(noise(0.08, a=0.01, rel=0.03, cutoff=8000), t, 0.35, 0.05)
        add(noise(0.06, a=0.008, rel=0.025, cutoff=8000), t + BEAT * 2 / 3, 0.35, 0.035)
        # piano stabs on 2 and 4
        if beat % 2 == 1:
            for j, m in enumerate(chord):
                add(lowpass(tone(hz(m), 0.35, a=0.003, rel=0.12, harm=(1, 0.3, 0.1)), 2400), t, -0.3 + 0.15 * j, 0.045)
    t += BEAT
    beat += 1

# ---- every patch: lift, click, click, the zip of light down the wire, a chime for its card; horn stabs in the rush
for i, p in enumerate(PATCHES):
    m = tm(p)
    pan = -0.5 + (i % 6) * 0.2
    add(noise(m["aFly"][1] - m["aFly"][0], a=0.15, rel=0.08, cutoff=2000), m["aFly"][0], pan, 0.08)
    add(click(), m["aFly"][1], pan, 0.4)
    add(click(0.8), m["bFly"][1], -pan, 0.4)
    n = int((m["pulse"][1] - m["pulse"][0]) * SR); tt = np.arange(n) / SR
    zip_ = np.sin(2 * np.pi * np.cumsum(np.geomspace(500, 1800, n)) / SR) * np.minimum(1, tt / 0.05) * np.exp(-tt / 0.3)
    add(zip_, m["pulse"][0], 0, 0.07)
    if p[4]:
        add(S(tone(hz(84), 0.5, rel=0.18, harm=(1, 0.3)), tone(hz(88), 0.5, rel=0.18) * 0.6), m["card"], 0.3, 0.16)
    if not p[4]:
        n = int(0.32 * SR); tt = np.arange(n) / SR
        horn = sum(np.sign(np.sin(2 * np.pi * hz(mm) * tt)) * 0.3 for mm in (65, 69, 72))
        add(lowpass(horn * env(n, 0.02, 0.12), 1600), m["lit"], pan, 0.09)

# ---- the urgent one: an alarm pulse while the AI layer decides, a bell when the person picks up
for k in range(int((18.3 - 15.6) / 0.25)):
    add(lowpass(np.sign(np.sin(2 * np.pi * 220 * np.arange(int(0.12 * SR)) / SR)) * env(int(0.12 * SR), 0.005, 0.04), 1400), 15.6 + k * 0.25, 0.4, 0.05)
add(phone_ring(1.1), tm(PATCHES[5])["lit"], 0.5, 0.2)

# ---- the lamps go green: a climbing run, one note per lamp
RUN = [65, 69, 72, 76, 77, 81, 84, 88]
for k in range(24):
    add(tone(hz(RUN[k % 8] + (12 if k >= 16 else 0)), 0.4, rel=0.14, harm=(1, 0.25)), T["green"][0] + k * 0.042, -0.6 + 1.2 * (k % 6) / 5, 0.07)

# ---- the neon: a hum, crackles on each letter's flicker, then the last chord F6/9
n = int((DUR - T["neon"]) * SR); tt = np.arange(n) / SR
hum = sum(a * np.sin(2 * np.pi * f * tt) for f, a in ((60, 1.0), (120, 0.6), (180, 0.3), (240, 0.15)))
add(lowpass(hum, 600) * np.minimum(1, tt / 1.2) * np.minimum(1, (tt[-1] - tt) / 1.0), T["neon"], 0, 0.07)
for ci in range(NEON_CONTOURS):
    add(noise(0.12, rel=0.03, cutoff=6000), T["neon"] + ci * 0.11, -0.5 + ci / NEON_CONTOURS, 0.08)
for j, m in enumerate([41, 53, 57, 62, 64, 67, 69]):
    add(tone(hz(m), 4.5, a=0.004, rel=1.6, harm=(1, 0.35, 0.12), detune=0.0007), T["end"], -0.5 + 0.17 * j, 0.15)
add(noise(0.3, rel=0.08, cutoff=900), T["end"], 0, 0.25)

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
