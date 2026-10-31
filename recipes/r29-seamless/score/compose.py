"""
R29 · Seamless. Original score, composed in code, timed to the film's one table (bake/table.json).

32 s at 112 bpm in E minor, opening to G major as the tiles melt seamless on the profile.
The pour: a held E minor, a pitched glide as the drop falls, a bloop, a low bloom and smaller drops for the rings, a
shimmer as the photo surfaces. The cut: a pen line as the seams draw on, then for each seam a rising stretch and a
glassy pluck on the beat it snaps, and a run of clicks as the numbers rise. Posted: a wooden tick, a drop and a plucked
note for every tile in posting order, then a riser and a G major bloom as the seams melt. Twelve tools: a filtered
sweep on each morph, drops for the covers, bells for the palette, a squash on each resize, a grid of clicks for the QR.
On your device: a rubbery glide as the upload pulls the drop, a snap back with a wobble, a pluck for each "No".
The title: drops as the liquid gathers, the mark on a warm G major chord and a bell, bells as the URL types.
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
rng = np.random.default_rng(29)
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







# ---------------------------------------------------------------- Seamless
fall, surface, draw, seams, numbers = TB["fall"], TB["surface"], TB["draw"], TB["seams"], TB["numbers"]
posts, melt, tools, resize = TB["posts"], TB["melt"], TB["tools"], TB["resize"]
tray, pull, snap, labels = TB["tray"], TB["pull"], TB["snap"], TB["labels"]
gather, mark, line = TB["gather"], TB["mark"], TB["line"]
EM = [40, 47, 52, 55, 59]              # E minor, the pour and the cut
GM = [43, 50, 55, 59, 62, 67]          # G major, from the melt to the mark


def pad(midis, t0, dur, g=0.04, a=0.8):
    for j, m in enumerate(midis):
        add(tone(hz(m), dur, a=a, rel=dur / 2.0, harm=(1, 0.35, 0.15), detune=0.0008), t0, -0.6 + 1.2 * j / max(1, len(midis) - 1), g)


def drop(t0, f0=1400, f1=380, dur=0.16, g=1.0, pan=0.0):
    # a liquid drop: a sine that bends down fast, the "bloop"
    n = int(dur * SR)
    u = np.linspace(0, 1, n)
    ph = np.cumsum(f1 + (f0 - f1) * np.exp(-u * 9)) / SR
    add(np.sin(2 * np.pi * ph) * env(n, 0.001, dur * 0.4), t0, pan, g)


def glass(m, t0, g=1.0, pan=0.0):
    # a glassy pluck as a seam snaps: a bright pluck over two inharmonic partials
    add(pluck(hz(m), 1.4, 0.75), t0, pan, g)
    add(tone(hz(m) * 2.76, 0.9, a=0.001, rel=0.25), t0, pan, g * 0.25)
    add(tone(hz(m) * 5.4, 0.5, a=0.001, rel=0.12), t0, pan, g * 0.12)


def tick(t0, f=1500, g=1.0, pan=0.0):
    # a soft wooden tick as a tile lands
    add(tone(f, 0.08, a=0.0005, rel=0.02, harm=(1, 0.4)), t0, pan, g)
    add(norm(lowpass(noise(0.02, a=0.0005, rel=0.01), 3000)), t0, pan, g * 0.25)


def sweep(t0, dur=0.5, g=1.0, pan=0.0):
    # a quick filtered sweep for each tool morph
    add(swish(dur, 400, 7000, rise=True), t0 - dur * 0.7, pan, g)
    drop(t0, 900, 300, 0.2, g * 0.5, pan)


# ---- the pour: a held E minor, the drop falls on a pitched glide and lands, a low bloom, rings, the photo surfaces
pad([40, 47, 52], 0.0, T["cut"][0] + 0.8, 0.05, a=1.0)
n = int((fall[1] - fall[0]) * SR)
u = np.linspace(0, 1, n)
gl = np.cumsum(hz(83) * (1 - 0.5 * u ** 2)) / SR
add(np.sin(2 * np.pi * gl) * env(n, 0.2, 0.6) * u, fall[0], 0.0, 0.02)
add(swish(fall[1] - fall[0], 300, 3000, rise=True), fall[0], 0.0, 0.05)
drop(fall[1], 1800, 300, 0.25, 0.3)
add(taiko(41, 1.8), fall[1], 0.0, 0.22)
thud(fall[1], 0.25, 50)
for j in range(5):
    drop(fall[1] + 0.32 * (j + 1), 1500 - 180 * j, 420, 0.12, 0.08 * (0.8 ** j), 0.5 * math.sin(j * 2.1))
add(bell(hz(76), 2.5), fall[1] + 0.02, 0.0, 0.04)
strings([52, 59, 64, 67], surface[0], T["cut"][0] - surface[0] + 1.0, 0.05, a=1.2)
n = int((surface[1] - surface[0]) * SR)
sh = np.sin(2 * np.pi * hz(88) * np.arange(n) / SR) * (0.5 + 0.5 * np.sin(2 * np.pi * 6 * np.arange(n) / SR)) * env(n, 0.8, 0.6)
add(sh, surface[0], 0.0, 0.01)

# ---- the cut: a pen line for each seam, then a stretch and a glassy snap per seam on its beat, numbers on a run
pad(EM, T["cut"][0], T["post"][0] - T["cut"][0] + 0.6, 0.035, a=0.6)
for b in beats(T["cut"][0], T["post"][0]):
    add(kick(), b, 0.0, 0.11)
for b in beats(seams[0]["snap"] + BEAT / 2, T["post"][0]):
    add(hat(0.6), b, 0.3, 0.022)
add(norm(lowpass(highpass(noise(draw[1] - draw[0], a=0.05, rel=0.2), 2000), 7000)), draw[0], 0.0, 0.04)
for j, s in enumerate(seams):
    n = int(BEAT * SR)
    u = np.linspace(0, 1, n)
    gl = np.cumsum(hz(52 + 3 * j) * (1 + 1.5 * u ** 2)) / SR
    add(np.sin(2 * np.pi * gl) * u ** 1.5 * np.exp(-0 * u), s["snap"] - BEAT, -0.5 + 0.33 * j, 0.025)
    glass([71, 74, 78, 83][j], s["snap"], 0.11, -0.5 + 0.33 * j)
    drop(s["snap"] + 0.01, 2200, 600, 0.1, 0.12, -0.5 + 0.33 * j)
for j in range(9):
    add(block(1400 + 120 * j, 0.5), numbers[0] + j * 0.12, -0.6 + 0.15 * j, 0.03)

# ---- posted: a tick per tile in posting order, a plucked line, then the seams melt on a G major bloom
for b in beats(T["post"][0], T["tools"][0]):
    add(kick(), b, 0.0, 0.12)
for b in beats(T["post"][0] + BEAT / 2, T["tools"][0]):
    add(hat(0.6), b, 0.3, 0.024)
add(swish(0.5, 300, 5000, rise=True), T["post"][0], 0.0, 0.07)
mel = [64, 67, 71, 74, 71, 67, 69, 71, 74]
for j, tp in enumerate(posts):
    tick(tp, 1300 + 90 * j, 0.18, 0.6 - 0.15 * j)
    drop(tp, 1200, 380, 0.11, 0.1, 0.6 - 0.15 * j)
    add(pluck(hz(mel[j]), 0.9, 0.5), tp, 0.6 - 0.15 * j, 0.05)
pad([40, 47, 52, 55], T["post"][0], melt[0] - T["post"][0] + 0.3, 0.03, a=0.5)
add(swish(melt[1] - melt[0] + 0.2, 200, 5000, rise=True), melt[0] - 0.1, 0.0, 0.08)
strings(GM, melt[1], T["device"][0] - melt[1] + 0.6, 0.05, a=0.4)
add(taiko(43, 1.6), melt[1], 0.0, 0.22)
add(bell(hz(79), 2.2), melt[1] + 0.02, 0.0, 0.04)

# ---- twelve tools: a sweep on every morph, a squash on each resize, a little grid of clicks for the QR
for b in beats(T["tools"][0], T["device"][0]):
    add(kick(), b, 0.0, 0.12)
for b in beats(T["tools"][0] + BEAT / 2, T["device"][0]):
    add(hat(0.6), b, 0.3, 0.025)
arp = [55, 59, 62, 67, 62, 59]
for j, b in enumerate(beats(T["tools"][0], T["device"][0], BEAT / 2)):
    add(pluck(hz(arp[j % 6]), 0.6, 0.45), b, 0.4 * math.sin(j), 0.035)
for j, x in enumerate(tools[1:]):
    sweep(x["t"], 0.45, 0.07, -0.4 + 0.16 * j)
for j in range(5):
    drop(tools[1]["t"] + 0.08 * j, 1500 + 200 * j, 500, 0.1, 0.06, -0.6 + 0.3 * j)
for j in range(5):
    add(bell(hz([67, 71, 74, 79, 83][j]), 1.0), tools[2]["t"] + 0.07 * j, -0.6 + 0.3 * j, 0.02)
for j, tr_ in enumerate(resize[1:]):
    add(swish(0.3, 2000 - 600 * j, 300), tr_ - 0.3, 0.0, 0.05)
    thud(tr_, 0.12, 70 - 8 * j)
for j in range(16):
    add(block(1800 + 500 * hsh(j * 3.1), 0.3), tools[4]["t"] + 0.35 + j * 0.04, 0.7 * math.sin(j * 1.7), 0.02)

# ---- on your device: the tray, the drop stretched on a rising rubber glide, a snap back and a wobble
pad([40, 47, 52, 55, 59], T["device"][0], T["title"] - T["device"][0] + 0.6, 0.035, a=0.5)
add(swish(tray[1] - tray[0], 400, 4000), tray[0], 0.0, 0.05)
for b in beats(T["device"][0], pull[0]):
    add(kick(), b, 0.0, 0.08)
n = int((pull[1] - pull[0]) * SR)
u = np.linspace(0, 1, n)
gl = np.cumsum(hz(40) * (1 + 2.5 * u ** 2) * (1 + 0.02 * np.sin(2 * np.pi * 7 * u * (pull[1] - pull[0])))) / SR
add((np.sin(2 * np.pi * gl) + 0.3 * np.sin(4 * np.pi * gl)) * env(n, 0.4, 2.0) * u, pull[0], 0.2, 0.07)
add(swish(pull[1] - pull[0], 200, 3500, rise=True), pull[0], 0.3, 0.05)
n = int(1.4 * SR)
u = np.arange(n) / SR
wob = np.sin(2 * np.pi * (hz(52) + 40 * np.exp(-u * 5.5) * np.cos(u * 17)) * u) * np.exp(-u * 3)
add(wob, snap, 0.0, 0.08)
drop(snap, 2400, 260, 0.3, 0.3)
thud(snap, 0.3, 48)
add(taiko(45, 1.4), snap, 0.0, 0.22)
for j, tl_ in enumerate(labels):
    add(pluck(hz([64, 67, 71][j]), 1.0, 0.5), tl_, 0.3, 0.06)
    tick(tl_, 1800, 0.08, 0.3)
for b in beats(snap, T["title"]):
    add(kick(), b, 0.0, 0.1)
for b in beats(snap + BEAT / 2, T["title"]):
    add(hat(0.6), b, 0.3, 0.022)

# ---- the title: the liquid gathers on a riser, the mark lands on a warm G major chord and a bell, bells as the URL types
add(swish(gather[1] - gather[0] + 0.2, 200, 7000, rise=True), gather[0], 0.0, 0.1)
for j in range(9):
    drop(gather[0] + 0.12 * j, 1600 - 60 * j, 420, 0.1, 0.06, -0.6 + 0.15 * j)
add(taiko(43, 1.8), gather[1], 0.0, 0.26)
thud(gather[1], 0.3, 49)
for j, m in enumerate([31, 43, 50, 55, 59, 62, 67]):
    add(tone(hz(m), DUR - gather[1], a=0.25, rel=2.6, harm=(1, 0.3, 0.12), detune=0.0007), gather[1], -0.6 + 0.2 * j, 0.042)
add(bell(hz(79), 3.5), mark + 0.02, 0.0, 0.07)
for j, m in enumerate([43, 50, 55, 59, 62, 67]):
    add(piano(m, 3.2), mark + 0.03 + 0.02 * j, -0.5 + 0.2 * j, 0.04)
for j, m in enumerate([83, 86, 91, 95, 91, 86]):
    add(bell(hz(m), 2.0), line + 1.0 + j * 0.13, 0.4 * math.sin(j), 0.024)
add(bell(hz(74), 3.0), line + 1.9, 0.0, 0.04)

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
