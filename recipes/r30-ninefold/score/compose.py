"""
R30 · Ninefold. Original score, composed in code, timed to the film's one table (bake/table.json).

32 s at 128 bpm in D minor, opening to F major as the nine posts lock into one picture.
The open: a low drone and a spinning whirr, a sub hit for "one image", a riser, and the tile bursting on a sub and
breaking glass. The field: four on the floor, and a glass ting on every wave, climbing the D minor. The feed: a riser
down the dolly zoom, a drop on the cut, a block, a pluck and a thump for every post in posting order, then strings and a
bell as the seams flash. The tools: a sub hit and a ting on every cut, climbing in pitch over a driving groove, and a run
of glass as the whole field returns. The device: a shimmer as the kaleidoscope turns, a downward sweep as it collapses,
and for each word a rising whoosh, a sub and breaking glass on the impact. The title: nine ticks as the tiles lock, the
mark on an F major chord and a bell, bells as the URL types.
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
rng = np.random.default_rng(129)
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







# ---------------------------------------------------------------- Ninefold
spin, shatter, W, reveal, pulses = TB["spin"], TB["shatter"], TB["words"], TB["reveal"], TB["pulses"]
runway, topcut, posts, seam, tools, tw = TB["runway"], TB["topcut"], TB["posts"], TB["seam"], TB["tools"], TB["twelve"]
kal, collapse, noes, morph, mark, line = TB["kal"], TB["collapse"], TB["noes"], TB["morph"], TB["mark"], TB["line"]
DM = [38, 45, 50, 53, 57]              # D minor
FM = [41, 48, 53, 57, 60, 65]          # F major, from the profile to the mark


def pad(midis, t0, dur, g=0.04, a=0.8):
    for j, m in enumerate(midis):
        add(tone(hz(m), dur, a=a, rel=dur / 2.0, harm=(1, 0.35, 0.15), detune=0.0008), t0, -0.6 + 1.2 * j / max(1, len(midis) - 1), g)


def sub(t0, f=46, dur=1.2, g=1.0):
    # a sub hit: a sine that falls an octave, under a short click
    n = int(dur * SR)
    u = np.arange(n) / SR
    ph = np.cumsum(f * (1 + np.exp(-u * 18))) / SR
    add(np.sin(2 * np.pi * ph) * np.exp(-u * 3.2), t0, 0.0, g)
    add(norm(highpass(noise(0.01, a=0.0005, rel=0.006), 3000)), t0, 0.0, g * 0.25)


def glass(t0, g=1.0, pan=0.0, base=2600):
    # glass breaking: a spray of bright inharmonic pings over a noise burst
    for k in range(9):
        f = base * (1 + 1.7 * hsh(k * 3.3 + t0))
        add(tone(f, 0.5, a=0.001, rel=0.06 + 0.1 * hsh(k + t0), harm=(1, 0.3)), t0 + 0.012 * k, pan + 0.5 * math.sin(k * 2.1), g * 0.12)
    add(norm(highpass(noise(0.35, a=0.001, rel=0.09), 3500)), t0, pan, g * 0.5)


def ting(m, t0, g=1.0, pan=0.0):
    add(tone(hz(m), 1.2, a=0.001, rel=0.35, harm=(1, 0.0, 0.25)), t0, pan, g)
    add(tone(hz(m) * 2.76, 0.6, a=0.001, rel=0.12), t0, pan, g * 0.2)


def riser(t0, t1, lo=200, hi=8000, g=1.0):
    add(swish(t1 - t0, lo, hi, rise=True), t0, 0.0, g)


# ---- open: a low drone and a spinning whirr; one image; the tile bursts on a sub and breaking glass
pad([38, 45, 50], 0.0, T["field"][0] + 0.5, 0.05, a=0.4)
n = int(spin * SR)
u = np.arange(n) / SR
whirr = np.sin(2 * np.pi * np.cumsum(120 + 900 * np.exp(-u * 1.3)) / SR) * (0.5 + 0.5 * np.sin(2 * np.pi * np.cumsum(14 * np.exp(-u * 1.1)) / SR))
add(lowpass(whirr, 3000) * env(n, 0.3, 1.5), 0.0, 0.0, 0.03)
sub(W["one"], 44, 1.0, 0.25)
add(taiko(55, 1.0), W["one"], 0.0, 0.14)
riser(W["one"] + 0.3, shatter, 300, 6000, 0.07)
sub(shatter, 41, 1.6, 0.45)
glass(shatter, 0.8)
add(crash(1.8), shatter, 0.0, 0.05)

# ---- field: four on the floor; a glass ting on every pulse, climbing the D minor
for b in beats(T["field"][0], T["feed"][0]):
    add(kick(), b, 0.0, 0.15)
for b in beats(T["field"][0] + BEAT / 2, T["feed"][0]):
    add(hat(0.7), b, 0.35, 0.03)
for b in beats(pulses[0] + BEAT, T["feed"][0], BEAT * 2):
    add(snare(), b, -0.1, 0.07)
pad(DM, T["field"][0], T["feed"][0] - T["field"][0] + 0.4, 0.035, a=0.3)
add(swish(reveal[1] - reveal[0], 6000, 300), reveal[0], 0.0, 0.06)
tings = [62, 65, 69, 74, 72, 69, 65, 69]
for j, pb in enumerate(pulses):
    ting(tings[j % len(tings)], pb, 0.07, -0.5 + 0.14 * j)
for key_ in ("nine", "zero"):
    sub(W[key_], 44, 0.8, 0.22)
    add(taiko(52, 0.9), W[key_], 0.0, 0.12)
bass = [38, 38, 41, 43]
for j, b in enumerate(beats(T["field"][0], T["feed"][0], BEAT * 2)):
    add(tone(hz(bass[j % 4]), BEAT * 1.8, a=0.004, rel=0.3, harm=(1, 0.5, 0.25)), b, 0.0, 0.06)

# ---- feed: a riser down the dolly zoom, a drop on the cut, a tick and a rising note per post, the seams flash on F major
riser(runway[0], topcut, 150, 9000, 0.1)
n = int((topcut - runway[0]) * SR)
gl = np.cumsum(hz(50) * (1 + np.linspace(0, 1, n) ** 2)) / SR
add(np.sin(2 * np.pi * gl) * env(n, 0.5, 0.4), runway[0], 0.0, 0.03)
sub(topcut, 41, 1.4, 0.4)
glass(topcut, 0.3)
for b in beats(topcut + BEAT, T["tools"][0]):
    add(kick(), b, 0.0, 0.13)
for b in beats(topcut + BEAT / 2, T["tools"][0], BEAT / 2):
    add(hat(0.5), b, 0.3, 0.02)
pad([38, 45, 50, 53], topcut, seam - topcut, 0.03, a=0.4)
mel = [62, 65, 67, 69, 72, 74, 77, 79, 81]
for j, tp in enumerate(posts):
    add(block(1500 + 100 * j, 0.6), tp, 0.6 - 0.15 * j, 0.08)
    add(pluck(hz(mel[j]), 1.0, 0.55), tp, 0.6 - 0.15 * j, 0.06)
    add(tone(90, 0.12, a=0.001, rel=0.04, harm=(1, 0.5)), tp, 0.0, 0.08)
strings(FM, seam, T["tools"][0] - seam + 0.6, 0.07, a=0.15)
add(bell(hz(77), 2.0), seam, 0.0, 0.05)
shing(seam, 0.05)

# ---- tools: a hit on every cut, climbing in pitch, over a driving groove; a run of glass as the field returns
for b in beats(T["tools"][0], T["device"][0]):
    add(kick(), b, 0.0, 0.15)
for b in beats(T["tools"][0] + BEAT / 2, T["device"][0]):
    add(hat(0.7), b, 0.35, 0.03)
for b in beats(T["tools"][0] + BEAT, T["device"][0], BEAT * 2):
    add(snare(), b, -0.1, 0.08)
arp = [53, 57, 60, 65, 60, 57]
for j, b in enumerate(beats(T["tools"][0], T["device"][0], BEAT / 2)):
    add(pluck(hz(arp[j % 6]), 0.5, 0.45), b, 0.4 * math.sin(j), 0.035)
for j, x in enumerate(tools):
    sub(x["t"], 44 + j, 0.5, 0.16)
    ting(65 + [0, 2, 4, 5, 7, 9, 11, 12, 14, 16][j], x["t"], 0.06, -0.6 + 0.13 * j)
    add(swish(0.25, 500, 7000, rise=True), x["t"] - 0.25, 0.0, 0.04)
pad(FM, T["tools"][0], T["device"][0] - T["tools"][0], 0.03, a=0.4)
sub(tw, 41, 1.4, 0.4)
add(crash(2.0), tw, 0.0, 0.06)
for k in range(10):
    ting([77, 81, 84, 89][k % 4], tw + 0.06 * k, 0.03, -0.7 + 0.15 * k)

# ---- device: the kaleidoscope turns on a shimmer, the field collapses into one tile, three words shatter on the glass
n = int((collapse[1] - kal) * SR)
sh = np.sin(2 * np.pi * hz(86) * np.arange(n) / SR) * (0.5 + 0.5 * np.sin(2 * np.pi * 8 * np.arange(n) / SR)) * env(n, 0.3, 0.8)
add(sh, kal, 0.0, 0.012)
pad([41, 48, 53, 57], kal, T["title"] - kal + 0.5, 0.035, a=0.4)
add(swish(collapse[1] - collapse[0], 7000, 200), collapse[0], 0.0, 0.1)
sub(collapse[1], 41, 1.2, 0.35)
for b in beats(kal, collapse[1]):
    add(kick(), b, 0.0, 0.12)
for j, nn in enumerate(noes):
    add(swish(nn["hit"] - nn["launch"], 300, 6000, rise=True), nn["launch"], 0.0, 0.08)
    sub(nn["hit"], 43 - 2 * j, 1.0, 0.32)
    glass(nn["hit"], 0.7, 0.2 * (j - 1), 2400 + 300 * j)
    add(pluck(hz([65, 69, 72][j]), 1.2, 0.5), nn["hit"] + 0.08, 0.4, 0.06)
for b in beats(collapse[1] + BEAT, T["title"], BEAT * 2):
    add(hat(0.5), b, 0.3, 0.018)

# ---- title: nine tiles lock with nine ticks, the mark lands on F major and a bell, bells as the URL types
add(swish(morph[1] - morph[0], 200, 7000, rise=True), morph[0], 0.0, 0.08)
for j in range(9):
    add(block(1800 + 90 * j, 0.5), T["title"] + 0.05 * j, -0.6 + 0.15 * j, 0.05)
sub(morph[1], 41, 1.8, 0.4)
add(taiko(43, 1.8), morph[1], 0.0, 0.22)
for j, m in enumerate([29, 41, 48, 53, 57, 60, 65]):
    add(tone(hz(m), DUR - morph[1], a=0.2, rel=2.6, harm=(1, 0.3, 0.12), detune=0.0007), morph[1], -0.6 + 0.2 * j, 0.042)
add(bell(hz(77), 3.5), mark + 0.02, 0.0, 0.07)
for j, m in enumerate([41, 48, 53, 57, 60, 65]):
    add(piano(m, 3.2), mark + 0.03 + 0.02 * j, -0.5 + 0.2 * j, 0.04)
for j, m in enumerate([84, 89, 93, 96, 93, 89]):
    add(bell(hz(m), 2.0), line + 1.0 + j * 0.13, 0.4 * math.sin(j), 0.024)
add(bell(hz(72), 3.0), line + 1.9, 0.0, 0.04)

# ---- master: a soft-clip that lifts the body and keeps the peaks round, then a fade at the very end
mix = np.stack([L, R], axis=1)
mix /= np.max(np.abs(mix))
DRIVE = 2.6
mix = np.tanh(mix * DRIVE) / np.tanh(DRIVE) * 0.58   # matched to Seamless, so the two films compare at one level
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
