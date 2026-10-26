"""
R19 · Phoropter. Original score, composed in code, timed to the film's one table (bake/table.json).

32 s, D minor resolving to D major the moment the right lens locks. A low drone under a soft pad whose filter is
closed while the chart is out of focus and opens as it sharpens. The phoropter swings in with a whoosh and settles
with a soft knock; every detent of the lens wheel is a crisp brass click. The options run over a pulse at 84 bpm
(Dm, Bb, F, C): each lens is a two-note call, "one... two", and the gauge needles land with small ticks. A bright tick
for every check that holds, a muted knock for every one that does not, a hiss as lens 1 fogs, whooshes as the lenses
leave. A reverse swell carries lens 2 home; the lock is a heavy click and a D major bell chord as the chart snaps
sharp. A tick for every day of the test, a bell for every check-in, paper in flight, a thud on the desk, the stamp,
and one wide chord under the word.
Usage: python score/compose.py  ->  assets/bgm/score.wav   (numpy only, deterministic)
"""
import json
import os
import wave
import numpy as np

SR = 44100
DUR = 32.0
N = int(DUR * SR)
rng = np.random.default_rng(19)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "bgm", "score.wav")
TB = json.load(open(os.path.join(HERE, "..", "bake", "table.json"), encoding="utf-8"))
T, OPT, WHEEL, DAYS, CHECKIN = TB["T"], TB["options"], TB["wheel"], TB["days"], TB["checkin"]

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
    # one-pole low-pass; cutoff may be a number or an array (a moving filter)
    cut = np.broadcast_to(np.asarray(cutoff, dtype=float), x.shape)
    a = np.exp(-2 * np.pi * cut / SR)
    y = np.zeros_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a[i]) * v + a[i] * acc
        y[i] = acc
    return y


def noise(dur, a=0.002, rel=0.05, cutoff=0):
    n = int(dur * SR)
    s = rng.standard_normal(n)
    if cutoff:
        s = lowpass(s, cutoff)
        s /= np.max(np.abs(s)) + 1e-9
    return s * env(n, a, rel)


def swish(dur, rise=False):
    n = int(dur * SR)
    t = np.arange(n) / SR
    shape = (t / dur) ** 2.2 if rise else np.sin(np.pi * t / dur) ** 2
    s = lowpass(rng.standard_normal(n), 2600 + 2400 * (t / dur if rise else 0)) * shape
    return s / (np.max(np.abs(s)) + 1e-9)


def bell(f, dur=2.6):
    return sum(h * tone(f * k, dur, a=0.001, rel=dur / (1 + 1.2 * i)) for i, (k, h) in enumerate(((1, 1.0), (2.0, 0.45), (2.76, 0.3), (5.4, 0.12))))


def click(g=1.0):
    # a brass detent: a bright transient over a short metallic ring
    s = 0.35 * tone(3150, 0.12, a=0.0005, rel=0.03, harm=(1, 0.4, 0.2))
    s[: int(0.03 * SR)] += lowpass(noise(0.03, a=0.0003, rel=0.004, cutoff=9000), 11000)
    return g * s


def knock(f=90, dur=0.35):
    return lowpass(tone(f, dur, a=0.001, rel=0.08, harm=(1, 0.5, 0.2)) + 0.5 * noise(dur, a=0.001, rel=0.02, cutoff=1500), 2000)


hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)

# ---- the drone and the "out of focus" pad: its filter opens as the chart sharpens
n = int(DUR * SR); tt = np.arange(n) / SR
drone = sum(a * np.sin(2 * np.pi * f * tt * (1 + d)) for f, a in ((hz(38), 1.0), (hz(50), 0.55), (hz(57), 0.25)) for d in (-0.0012, 0.0012))
add(lowpass(drone, 700) * np.minimum(1, tt / 1.5) * (1 - 0.5 * np.clip((tt - 8.6) / 1.0, 0, 1)) * np.clip((T["lift"] + 1.5 - tt) / 1.5, 0, 1), 0, 0, 0.06)
pn = int(9.0 * SR); pt = np.arange(pn) / SR
padsig = sum(np.sin(2 * np.pi * hz(m) * pt * (1 + d)) for m in (62, 65, 69, 72) for d in (-0.002, 0.002))
cut = 380 + 2600 * np.clip((pt - T["sharpen"][0]) / (T["sharpen"][1] - T["sharpen"][0]), 0, 1) ** 1.5
add(lowpass(padsig, cut) * np.minimum(1, pt / 1.6) * np.minimum(1, (9.0 - pt) / 1.0), 0.2, 0, 0.035)

# ---- the phoropter swings in and settles
add(swish(1.1), T["swing"] - 0.1, 0.5, 0.07)
add(knock(70, 0.5), T["swing"] + 0.55, 0.2, 0.12)
add(tone(hz(38), 1.2, a=0.004, rel=0.35, harm=(1, 0.4)), T["swing"] + 0.55, 0, 0.08)

# ---- every detent of the wheel is a click
for k, (tw, dw) in enumerate(WHEEL[1:]):
    add(click(1.0 if k < 8 else 1.4), tw, 0.35, 0.09)
# the chart sharpens: a rising line of plucks, row by row; the ring around the bottleneck shimmers on
for k, m in enumerate([62, 65, 69, 72, 74, 77, 81]):
    add(tone(hz(m), 0.9, a=0.003, rel=0.22, harm=(1, 0.35, 0.1)), T["sharpen"][0] + 0.25 + 0.27 * k, -0.5 + 0.17 * k, 0.03)
for k in range(18):
    add(tone(hz([81, 84, 86, 89][k % 4] + 12), 0.4, a=0.002, rel=0.08), T["ring"][0] + 0.7 * k / 18, -0.4 + 0.8 * k / 18, 0.012)

# ---- the options: a pulse at 84 bpm over Dm, Bb, F, C; each lens is a call, "one... two"
BEAT = 60 / 84
CH = [[38, 62, 65, 69], [34, 62, 65, 70], [41, 60, 65, 69], [36, 60, 64, 67]]
t0, k = T["opt"][0] - 0.4, 0
while t0 < T["out"]:
    ch = CH[k % 4]
    add(lowpass(sum(tone(hz(m), 4 * BEAT + 0.8, a=0.3, rel=1.2) for m in ch[1:]), 1800), t0, 0, 0.022)
    for b in range(4):
        add(lowpass(tone(hz(ch[0]), 0.4, a=0.004, rel=0.14, harm=(1, 0.3)), 420), t0 + b * BEAT, 0, 0.1)
        add(click(0.25), t0 + b * BEAT + BEAT / 2, -0.4, 0.05)
    t0 += 4 * BEAT; k += 1
for j, to in enumerate(T["opt"]):
    add(bell(hz(69 + [0, 2, 4][j]), 1.6), to + 0.18, -0.3, 0.05)          # "one"
    add(bell(hz(74 + [0, 2, 4][j]), 1.8), to + 0.62, 0.3, 0.045)          # "two"
    add(swish(0.4), to - 0.2, 0.4, 0.03)
    for g in range(5):                                                     # the needles land
        add(tone(4200 + 300 * g, 0.05, a=0.0005, rel=0.012), to + 0.45 + 0.05 * g, -0.6 + 0.3 * g, 0.012)

# ---- the lenses leave the wheel; the checks land
for k in range(3):
    add(swish(0.9), T["out"] + 0.12 * k, -0.6 + 0.6 * k, 0.04)
for k, o in enumerate(OPT):
    for j, (tc, ok) in enumerate(zip(o["checkT"], o["checks"])):
        pan = -0.6 + 0.6 * k
        if ok:
            add(tone(hz([81, 84, 86, 88, 93][j]), 0.35, a=0.002, rel=0.08, harm=(1, 0.3)), tc, pan, 0.03)
        else:
            add(knock(110, 0.25), tc, pan, 0.08)
# lens 1 fogs (a hiss) and swings away; lens 3 slides out
add(noise(0.9, a=0.25, rel=0.3, cutoff=5000), T["fog"], -0.6, 0.025)
add(swish(0.8), T["fog"] + 0.4, -0.7, 0.05)
add(tone(hz(45), 1.0, a=0.01, rel=0.3, harm=(1, 0.4)), T["fog"] + 0.5, -0.5, 0.06)
add(swish(0.6), T["out3"], 0.7, 0.05)

# ---- lens 2 comes home: a reverse swell, then the lock and D major as the chart snaps sharp
add(swish(T["lock"] - T["back"], rise=True), T["back"], 0.2, 0.06)
sw_n = int((T["lock"] - T["back"]) * SR); sw_t = np.arange(sw_n) / SR
add(sum(np.sin(2 * np.pi * hz(m) * sw_t) for m in (57, 62, 66, 69)) * (sw_t / sw_t[-1]) ** 3, T["back"], 0, 0.02)
add(click(2.2), T["lock"], 0.3, 0.12)
add(knock(80, 0.5), T["lock"], 0.2, 0.12)
for j, m in enumerate([62, 66, 69, 74, 78]):
    add(bell(hz(m + 12), 3.2), T["lock"] + 0.03 + 0.04 * j, -0.4 + 0.2 * j, 0.06)
add(tone(hz(38), 3.0, a=0.005, rel=1.2, harm=(1, 0.5, 0.2)), T["lock"], 0, 0.11)
add(lowpass(sum(tone(hz(m), 4.2, a=0.6, rel=1.4) for m in (62, 66, 69, 73)), 2200), T["lock"] + 0.1, 0, 0.03)

# ---- thirty days: a tick each, a bell for every weekly check-in
for d, td in enumerate(DAYS):
    add(tone(hz(86 + (d % 3) * 2), 0.12, a=0.001, rel=0.03), td, -0.6 + 1.2 * d / 29, 0.018)
    if d + 1 in CHECKIN:
        add(bell(hz([74, 78, 81, 86][CHECKIN.index(d + 1)]), 1.4), td, 0, 0.035)

# ---- the brief: paper in flight, a thud on the desk, the stamp
add(swish(1.3), T["lift"], -0.2, 0.05)
add(knock(95, 0.3), T["land"], 0.1, 0.1)
add(knock(60, 0.45), T["stamp"], 0.2, 0.18)
add(click(0.8), T["stamp"], 0.2, 0.08)
add(tone(hz(50), 1.4, a=0.004, rel=0.5, harm=(1, 0.4)), T["stamp"], 0, 0.07)

# ---- the rings gather into the word; one wide D major chord holds it
for k in range(36):
    add(tone(hz([74, 78, 81, 85, 86, 90][k % 6] + 12), 0.4, a=0.002, rel=0.09), T["word"][0] + 1.3 * k / 36, -0.8 + 1.6 * ((k * 5) % 11) / 10, 0.018)
add(swish(1.5, rise=True), T["word"][0] - 0.2, 0, 0.035)
for j, m in enumerate([74, 78, 81]):
    add(bell(hz(m + 12), 3.6), T["word"][1] - 0.4 + 0.16 * j, -0.3 + 0.3 * j, 0.05)
for j, m in enumerate([38, 50, 57, 62, 66, 69, 73, 76, 81]):
    add(tone(hz(m), DUR - T["word"][1] + 0.4, a=0.04, rel=2.0, harm=(1, 0.3, 0.1), detune=0.0007), T["word"][1] - 0.4, -0.6 + 0.15 * j, 0.085)

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
