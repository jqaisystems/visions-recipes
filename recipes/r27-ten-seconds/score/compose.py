"""
R27 · Ten Seconds. Original score, composed in code, timed to the film's one table (bake/table.json).

32 s at 96 bpm in D minor, opening to F major on the wall of pages.
Record: a low drone, a breath, then tape chatter that speeds up as ninety seconds race past, over a soft pulse and a
plucked ostinato. Keep: a long swell as the camera pulls back, a ratchet while the window weighs the take, a low bell
and a thud as it locks, scattered plucks falling away as the rest peels off. Your machine: two tones a little apart
that glide into one as the clone locks on, wind for the cloud, and a soft scrape as it erases itself. It speaks: the
music thins to a pad under the cloned voice, with a key for each letter as the line types. Everywhere: a tick for
each name, a pop as the voice lands on the page, a pluck for each branch, rising through F major as the pages land,
a thunk for each flag and a chime when it is re-rendered. The title: one low chord on the bar, a bell on the lockup,
bells as the URL types.
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
rng = np.random.default_rng(27)
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


def twelve(m, dur=1.4, g=1.0, pan=0.0, t0=0.0):
    # a twelve-string course: the note and its octave, the octave a hair late and a hair sharp
    add(pluck(hz(m), dur, 0.45), t0, pan, g)
    add(pluck(hz(m + 12) * 1.002, dur * 0.8, 0.6), t0 + 0.012, -pan, g * 0.55)


def piano(m, dur=1.6, g=1.0):
    f = hz(m)
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = sum(h * np.sin(2 * np.pi * f * k * t * (1 + 0.0004 * k * k)) * np.exp(-t * (1.6 + 1.1 * k)) for k, h in
            enumerate((1.0, 0.55, 0.3, 0.18, 0.1, 0.05), start=1))
    s[: int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))
    k = min(n, int(0.02 * SR))
    s[-k:] *= np.linspace(1, 0, k)
    return g * s


def strings(midis, t0, dur, g=0.05, a=0.5):
    for j, m in enumerate(midis):
        n = int(dur * SR)
        t = np.arange(n) / SR
        sig = 0
        for dt in (-0.0025, 0.0, 0.0031):   # a small section: three detuned saws, softened
            ph = 2 * np.pi * np.cumsum(hz(m) * (1 + dt + 0.003 * np.sin(2 * np.pi * 5.1 * t + j))) / SR
            sig = sig + sum(np.sin(ph * h) / h for h in range(1, 7))
        sig = lowpass(sig, 2600) * env(n, a, dur / 2.2)
        add(sig, t0, -0.6 + 1.2 * j / max(1, len(midis) - 1), g / 3)


def scratch(dur, g=1.0, pan=0.0, t0=0.0):
    # graphite on paper: grainy band-limited noise with a stroke-shaped envelope and a rough tooth
    n = int(dur * SR)
    u = np.arange(n) / n
    grain = rng.standard_normal(n) * (0.4 + 0.6 * (rng.random(n) > 0.7))
    x = highpass(lowpass(grain, 6500), 1800) * (np.sin(np.pi * u) ** 0.6) * (0.7 + 0.3 * np.sin(2 * np.pi * 23 * u * dur))
    add(norm(x), t0, pan, g)


def flutter(t0, g=1.0, pan=0.0):
    # a page flipping: a soft whoosh and a papery slap at the end
    add(swish(0.22, 900, 7000), t0, pan, g)
    add(norm(highpass(noise(0.05, a=0.0005, rel=0.012), 1200)), t0 + 0.17, pan, g * 0.8)


def hit(t0, big=1.0, chord=(50, 57, 62, 65)):
    add(taiko(46, 1.6), t0, 0.0, 0.5 * big)
    add(kick(), t0, 0.0, 0.3 * big)
    add(crash(1.6 * big), t0, -0.25, 0.08 * big)
    for j, m in enumerate(chord):
        add(tone(hz(m), 0.55, a=0.004, rel=0.2, harm=(1, 0.6, 0.4, 0.25, 0.15)), t0, -0.6 + 0.4 * j, 0.05 * big)


def stamp(t0, g=0.14, pan=0.3):
    add(norm(lowpass(noise(0.09, a=0.0004, rel=0.03), 2400)), t0 + 0.02, pan, g)



def pizz(m, g=1.0, pan=0.0, t0=0.0, dur=0.4):
    add(pluck(hz(m), dur, 0.3), t0, pan, g)


def key(t0, g=1.0, pan=0.0):
    # a typewriter key: a sharp click and a little body
    add(norm(highpass(noise(0.018, a=0.0002, rel=0.004), 3000)), t0, pan, g)
    add(tone(1900 + 400 * hsh(t0 * 7), 0.03, a=0.0003, rel=0.008), t0, pan, g * 0.3)


def thud(t0, g=1.0, f=70):
    n = int(0.3 * SR)
    t = np.arange(n) / SR
    add(np.sin(2 * np.pi * np.cumsum(f + 60 * np.exp(-t * 40)) / SR) * np.exp(-t * 14), t0, 0.0, g)


def shing(t0, g=1.0):
    # a gold line slicing the frame: a bright metallic ring
    for k, (f, h) in enumerate(((2637, 1.0), (3520, 0.6), (5274, 0.35), (7040, 0.2))):
        add(tone(f, 1.6, a=0.001, rel=0.5 / (1 + k), harm=(1,)), t0, 0.3 - 0.2 * k, g * h)
    add(norm(highpass(noise(0.4, a=0.001, rel=0.12), 5000)), t0, 0.2, g * 0.6)




# ---------------------------------------------------------------- Ten Seconds
breath, write, pull, scan, lock, peel, dive = (TB[k] for k in ("breath", "write", "pull", "scan", "lock", "peel", "dive"))
frame, clone, cloud, erase = (TB[k] for k in ("frame", "clone", "cloud", "erase"))
voice, CLIP, typ = TB["voice"], 3.6, TB["type"]
names_at, into_page, pullout, b1, b2, b3, qc, flags = (TB[k] for k in ("names_at", "into_page", "pullout", "b1", "b2", "b3", "qc", "flags"))
retract, bar_t, mark_t = TB["retract"], TB["bar"], TB["mark"]
TU = mark_t + 1.0   # the URL types
FM = [53, 57, 60, 65, 69, 72, 77]      # F major, for the wall
LETTERS = 49                           # the spoken line's letters, typed in one stretch


def pad(midis, t0, dur, g=0.04, a=0.8):
    for j, m in enumerate(midis):
        add(tone(hz(m), dur, a=a, rel=dur / 2.0, harm=(1, 0.35, 0.15), detune=0.0008), t0, -0.6 + 1.2 * j / max(1, len(midis) - 1), g)


def breathe(t0, dur, g=1.0):
    n = int(dur * SR)
    u = np.arange(n) / n
    x = lowpass(rng.standard_normal(n), 900) * np.sin(np.pi * u) ** 1.5
    add(norm(x), t0, 0.0, g)


# ---- record: a drone, the hairline, a breath, then ninety seconds of tape racing past
pad([38, 45, 50], 0.0, T["keep"][0] + 1.0, 0.05, a=0.4)
add(swish(0.55, 300, 4000, rise=True), 0.0, 0.0, 0.07)
add(tone(hz(74), 0.6, a=0.004, rel=0.25, harm=(1, 0.3)), 0.5, 0.0, 0.03)
breathe(breath[0], breath[1] - breath[0] + 0.35, 0.09)
w0, w1 = write
k = 0
while True:
    u = (k / 140) ** (1 / 1.35)              # clicks on the head's schedule: faster and faster
    tc = w0 + u * (w1 - w0)
    if tc > w1:
        break
    key(tc, 0.05 + 0.04 * hsh(k), 0.5 * math.sin(k))
    k += 1
add(swish(w1 - w0, 300, 9000, rise=True), w0, 0.0, 0.1)
for b in beats(w0, T["keep"][0]):
    add(kick(), b, 0.0, 0.12)
arp = [62, 65, 69, 74, 69, 65]
for j, b in enumerate(beats(w0, pull[0] + 0.01, BEAT / 2)):
    add(pluck(hz(arp[j % 6]), 0.6, 0.35), b, 0.4 * math.sin(j), 0.045)

# ---- keep: pull back, weigh, lock, peel, dive
add(swish(pull[1] - pull[0] + 0.3, 200, 3000), pull[0], 0.0, 0.12)
pad([50, 57, 62, 65], pull[0], dive[1] - pull[0] + 0.5, 0.035, a=0.6)
for j, b in enumerate(beats(scan[0], scan[1], BEAT / 4)):
    add(block(1400 + 400 * hsh(j), 0.6), b, -0.6 + 1.2 * (j % 8) / 7, 0.05)
for b in beats(pull[0], dive[1]):
    add(kick(), b, 0.0, 0.1)
thud(lock, 0.35, 62)
add(bell(hz(74), 2.6), lock, 0.0, 0.07)
add(bell(hz(81), 2.0), lock + 0.04, 0.2, 0.03)
for j in range(14):
    tp = peel[0] + (peel[1] - peel[0] + 0.4) * hsh(j * 3.1)
    add(pluck(hz([74, 72, 69, 65, 62, 60, 57][j % 7]), 0.5, 0.3), tp, 0.8 * math.sin(j * 2.3), 0.03)
    add(swish(0.2, 1200, 7000), tp, 0.8 * math.sin(j * 2.3), 0.025)
add(swish(dive[1] - dive[0], 300, 10000, rise=True), dive[0], 0.0, 0.14)

# ---- your machine: the frame, two tones becoming one, a cloud that never arrives
add(taiko(50, 1.4), frame[0], 0.0, 0.25)
pad([50, 57, 62, 65, 69], frame[0], T["speak"][0] - frame[0] + 0.6, 0.04, a=0.5)
scratch(frame[1] - frame[0], 0.03, -0.3, frame[0])
n = int((clone[1] - clone[0] + 1.6) * SR)
tc_ = np.arange(n) / SR
glide = 1 + 0.035 * np.clip(1 - tc_ / (clone[1] - clone[0]), 0, 1) ** 2
for j, m in enumerate((62, 69)):
    f = hz(m)
    pa, pb = 2 * np.pi * f * tc_, 2 * np.pi * np.cumsum(f * glide) / SR
    add((np.sin(pa) + 0.3 * np.sin(2 * pa) + np.sin(pb) + 0.3 * np.sin(2 * pb)) * env(n, 0.3, 1.2), clone[0], -0.3 + 0.6 * j, 0.03)
add(bell(hz(74), 2.4), clone[1], 0.0, 0.06)
for j, m in enumerate([50, 57, 62, 65, 69]):
    add(piano(m, 2.4), clone[1] + 0.015 * j, -0.5 + 0.25 * j, 0.04)
for b in beats(clone[1], T["speak"][0]):
    add(kick(), b, 0.0, 0.09)
nw = int((erase[1] - cloud[0]) * SR)
wind = lowpass(highpass(rng.standard_normal(nw), 300), 1800) * np.sin(np.pi * np.arange(nw) / nw) ** 2
add(norm(wind), cloud[0], 0.7, 0.07)
scratch(erase[1] - erase[0], 0.04, 0.6, erase[0])
add(swish(0.6, 400, 6000), T["speak"][0] - 0.1, 0.0, 0.08)

# ---- it speaks: a key for each letter, then the music thins to a pad under the voice
for j in range(LETTERS):
    key(typ[0] + (typ[1] - typ[0]) * j / LETTERS, 0.07, 0.5 * math.sin(j * 1.7))
pad([50, 57, 65], T["speak"][0], T["every"][0] - T["speak"][0] + 0.6, 0.03, a=0.6)
add(tone(hz(38), voice + CLIP + 0.6 - T["speak"][0], a=0.6, rel=2.0), T["speak"][0], 0.0, 0.05)
add(bell(hz(77), 2.4), voice + CLIP + 0.1, 0.0, 0.05)
add(pluck(hz(65), 1.2, 0.4), voice + CLIP + 0.1, 0.0, 0.05)

# ---- everywhere: names, the page, the branches, the wall, the quality check
for j, tn in enumerate(names_at):
    add(block(1800 + 180 * j, 0.6), tn, 0.3, 0.06)
add(swish(into_page[1] - into_page[0], 400, 5000), into_page[0], 0.0, 0.09)
add(tone(hz(77), 0.4, a=0.002, rel=0.12, harm=(1, 0.5)), into_page[1], 0.0, 0.06)
add(taiko(53, 1.4), into_page[1], 0.0, 0.25)
strings([53, 60, 65, 69, 72], pullout[0], retract[0] - pullout[0] + 0.6, 0.07, a=0.8)
for b in beats(into_page[1], retract[0]):
    add(kick(), b, 0.0, 0.13)
for b in beats(into_page[1] + BEAT / 2, retract[0]):
    add(hat(0.6), b, 0.3, 0.025)
for j in range(3):
    add(pluck(hz(53 + 7 * j), 1.0, 0.4), b1[0] + 0.2 * j, -0.5 + 0.5 * j, 0.06)
for j in range(12):
    add(pluck(hz(FM[j % 7] + 12 * (j // 7)), 0.7, 0.45), b2[0] + (b2[1] - b2[0]) * j / 12, 0.8 * math.sin(j), 0.04)
leaves = sorted(lf["t"] for b in TB["tree"] for kd in b["kids"] for lf in kd["leaves"])
for j, tl_ in enumerate(leaves):
    add(block(2600 + 900 * (j / len(leaves)), 0.4), tl_, 0.9 * math.sin(j * 1.3), 0.012)
    if j % 6 == 0:
        add(pluck(hz(FM[(j // 6) % 7] + 12), 0.5, 0.5), tl_, 0.9 * math.sin(j * 1.3), 0.035)
add(tone(hz(57), qc[1] - qc[0] + 0.4, a=0.1, rel=0.4, harm=(1, 0.5, 0.3)), qc[0] - 0.2, -0.4, 0.02)
for f in flags:
    thud(f["t"], 0.2, 80)
    add(block(700, 1.0), f["t"], 0.2, 0.05)
    add(bell(hz(84), 1.2), f["t"] + BEAT, 0.3, 0.035)
    add(bell(hz(88), 1.0), f["t"] + BEAT + 0.07, 0.3, 0.025)

# ---- the title: everything pulls back into one bar, one chord, the lockup, bells as the URL types
add(swish(retract[1] - retract[0], 300, 8000), retract[0], 0.0, 0.12)
thud(bar_t, 0.35, 55)
add(taiko(44, 1.6), bar_t, 0.0, 0.3)
for j, m in enumerate([41, 53, 60, 65, 69]):
    add(tone(hz(m), DUR - bar_t, a=0.2, rel=2.4, harm=(1, 0.3, 0.12), detune=0.0007), bar_t, -0.6 + 0.3 * j, 0.045)
add(bell(hz(65), 3.5), mark_t + 0.02, 0.0, 0.07)
for j, m in enumerate([41, 53, 60, 65, 69, 72]):
    add(piano(m, 3.2), mark_t + 0.03 + 0.02 * j, -0.5 + 0.2 * j, 0.045)
for j, m in enumerate([84, 89, 93, 96, 93, 89]):
    add(bell(hz(m), 2.0), TU + j * 0.12, 0.4 * math.sin(j), 0.026)
add(bell(hz(77), 3.0), TU + 1.1, 0.0, 0.045)

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
