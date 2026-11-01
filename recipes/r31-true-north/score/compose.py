"""
R31 · True North. Original score, composed in code, timed to the film's one table (bake/table.json).

33 s at 116 bpm in E minor, opening to G major on the lockup.
The open: a low pad, the needle's bezel clicking as it spins down, the prompt typing, a bell for the coral spark. The
globe: a rush out as the camera pulls back, glassy plucks as the tiles arrive, then a whip and a ratchet into every
brake with a sub, a kick and a struck glass, climbing; a rush for the dive. The zoom: a hit on every push, a glass
climbing per still, the needle's sweep ticking, over a groove. The tunnel: a rush and a driving pulse with C under the
E minor. --motion: a soft drop and a struck glass as each ring opens. The title: a riser as the light gathers, the
lockup on G major with a bell, the URL typing.
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
rng = np.random.default_rng(131)
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







# ---------------------------------------------------------------- True North
EM = [40, 47, 52, 55, 59]              # E minor
GM = [31, 43, 50, 55, 59, 62, 67]      # G major, on the lockup
brakes, dive, steps, rings = TB["brakes"], TB["dive"], TB["drosteSteps"], TB["rings"]
gather, mark, line = TB["gather"], TB["mark"], TB["line"]


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


def ring(m, t0, g=1.0, pan=0.0):
    # struck glass: one clean partial and its inharmonic ring
    add(tone(hz(m), 2.6, a=0.001, rel=1.2, harm=(1, 0.0, 0.08)), t0, pan, g)
    add(tone(hz(m) * 2.32, 1.2, a=0.001, rel=0.4), t0, pan, g * 0.18)


def tick(t0, g=1.0, pan=0.0, f=3200):
    add(norm(highpass(noise(0.012, a=0.0004, rel=0.006), f)), t0, pan, g)
    add(tone(f / 6, 0.03, a=0.0005, rel=0.012), t0, pan, g * 0.3)


def type_run(t0, t1, chars, g=0.05, pan=-0.3):
    if chars <= 0 or t1 <= t0:
        return
    step = (t1 - t0) / chars
    for k in range(0, chars, 2):
        tick(t0 + k * step + 0.004 * hsh(k + t0), g * (0.7 + 0.3 * hsh(k * 1.3 + t0)), pan + 0.2 * math.sin(k), 2600 + 1400 * hsh(k + 9 * t0))


def ratchet(t0, t1, n, g=0.03, pan=0.0):
    # a compass bezel turning: clicks that slow down into the stop
    for k in range(n):
        u = 1 - (1 - k / n) ** 2
        tick(t0 + (t1 - t0) * u, g * (0.6 + 0.4 * k / n), pan, 1500 + 900 * hsh(k * 2.1 + t0))


# ---- I · open: a low E minor pad, the needle's bezel spinning down, the prompt typing, the coral spark
pad([28, 40, 47, 52], 0.0, TB["pull"][0] + 1.0, 0.03, 1.0)
ratchet(BEAT * 0.8, BEAT * 5, 34, 0.035, 0.3)
type_run(TB["typing"][0], TB["typing"][1], len(TB["prompt"]) // 2, 0.035, -0.35)
add(bell(hz(88), 2.4), BEAT * 3, 0.3, 0.05)

# ---- II · the globe: a rush out, the build of tiles, a whip and a lock on every brake, rising
add(swish(TB["pull"][1] - TB["pull"][0], 150, 6000, rise=True), TB["pull"][0], 0.0, 0.06)
sub(TB["pull"][0], 41, 1.6, 0.35)
add(taiko(52, 1.4), TB["pull"][0], 0.0, 0.16)
add(crash(2.4), TB["pull"][0], 0.0, 0.035)
for k in range(16):                                                                  # the tiles arriving, glassy
    tt0 = TB["build"][0] + (TB["build"][1] - TB["build"][0]) * hsh(k * 3.3)
    add(pluck(hz([64, 67, 71, 74, 76, 79][k % 6] + 12), 0.5, 0.7), tt0, 0.7 * math.sin(k * 1.9), 0.012)
pad(EM, TB["pull"][0] + 0.4, dive[1] - TB["pull"][0], 0.03, 1.2)
MOVES = [[BEAT * 7, BEAT * 10], [BEAT * 11.2, BEAT * 13], [BEAT * 14.2, BEAT * 16]]
for j, (m0, m1) in enumerate(MOVES):
    add(swish(m1 - m0, 300, 7000), m0, 0.5 - 0.5 * j, 0.06)
    ratchet(m0 + (m1 - m0) * 0.35, m1, 14, 0.03, -0.3 + 0.3 * j)
    t0 = brakes[j]["t"]
    sub(t0, 44 - 2 * j, 1.0, 0.32)
    add(kick(), t0, 0.0, 0.16)
    ring([76, 79, 83][j], t0 + 0.01, 0.08, 0.4)
for bt in beats(BEAT * 10, dive[0]):                                                 # a pulse under the brakes
    add(kick(), bt, 0.0, 0.08)
    add(hat(0.5), bt + BEAT * 0.5, 0.3, 0.018)
add(swish(dive[1] - dive[0], 120, 12000, rise=True), dive[0], 0.0, 0.1)             # the dive

# ---- III · droste: a hit on every push, a tick climbing per still, a groove
CL = [64, 66, 67, 69, 71, 72, 74, 76]
for j, s in enumerate(steps):
    sub(s, 44, 0.8, 0.26 if j else 0.4)
    add(taiko(58, 1.0), s, 0.0, 0.1)
    ring(CL[j] + 12, s + 0.02, 0.05, 0.5 * math.sin(j * 1.7))
    ratchet(s + BEAT * 0.15, s + BEAT * 0.15 + 0.55, 10, 0.022, 0.4 * math.cos(j))   # the needle sweeping in the next
    if j == 0:
        add(crash(2.4), s, 0.0, 0.05)
for k, bt in enumerate(beats(steps[0], TB["T"]["tunnel"][0], BEAT * 0.5)):
    if k % 2 == 0:
        add(kick(), bt, 0.0, 0.13)
    else:
        add(hat(0.6), bt, 0.25, 0.022)
    if k % 4 == 2:
        add(snare(0.7), bt, -0.1, 0.04)
    add(pluck(hz([40, 47, 52, 55][(k // 2) % 4] + (12 if k % 2 else 0)), 0.35, 0.3), bt, 0.0, 0.03)
pad([40, 47, 52, 55, 59], steps[0], TB["T"]["tunnel"][0] - steps[0] + 0.5, 0.025, 0.4)

# ---- IV · tunnel: a filtered rush and a driving pulse that brakes
t0, t1 = TB["T"]["tunnel"][0], TB["T"]["motion"][0]
sub(t0, 38, 2.0, 0.42)
add(crash(3.0), t0, 0.0, 0.06)
add(swish(t1 - t0, 200, 9000), t0, 0.0, 0.09)
for k, bt in enumerate(beats(t0, t1 - BEAT, BEAT * 0.5)):
    add(kick(), bt, 0.0, 0.12 if k % 2 == 0 else 0.0)
    add(hat(0.7), bt + BEAT * 0.25, 0.3, 0.02)
    if k % 4 == 2:
        add(snare(0.7), bt, -0.1, 0.045)
    add(pluck(hz([52, 59, 64, 67, 64, 59][k % 6] + 12), 0.4, 0.5), bt, 0.5 * math.sin(k), 0.022)
pad([36, 48, 55, 59, 64], t0, t1 - t0 + 0.5, 0.03, 0.5)                              # C under the E minor, lifting

# ---- V · --motion: a soft drop, a struck glass as each ring opens
pad([43, 50, 55, 59, 62], t1, TB["T"]["title"] - t1 + 0.8, 0.035, 0.6)
for j, rt in enumerate(rings):
    ring([79, 83, 86][j], rt, 0.07, -0.5 + 0.5 * j)
    add(swish(0.4, 600, 5000), rt, -0.5 + 0.5 * j, 0.03)
for k, bt in enumerate(beats(rings[0], TB["T"]["title"], BEAT * 0.5)):
    add(pluck(hz([67, 71, 74, 79, 74, 71][k % 6]), 0.9, 0.4), bt, 0.6 * math.sin(k * 1.3), 0.022)

# ---- VI · title: a riser as the light gathers, the lockup on G major and a bell, the URL typing
add(swish(mark - gather[0], 200, 8000, rise=True), gather[0], 0.0, 0.08)
ratchet(gather[0], mark - 0.2, 26, 0.03, 0.0)
sub(mark, 31, 1.8, 0.42)
add(taiko(43, 1.8), mark, 0.0, 0.2)
for j, m in enumerate(GM):
    add(tone(hz(m), DUR - mark, a=0.2, rel=2.6, harm=(1, 0.3, 0.12), detune=0.0007), mark, -0.6 + 0.2 * j, 0.04)
add(bell(hz(83), 3.5), mark + 0.02, 0.0, 0.07)
for j, m in enumerate([43, 50, 55, 59, 62, 67]):
    add(piano(m, 3.2), mark + 0.03 + 0.02 * j, -0.5 + 0.2 * j, 0.04)
type_run(TB["tunnelLines"][1] + 0.45, TB["tunnelLines"][1] + 1.25, len("visions.joaoqueiros.com/stills"), 0.03, 0.0)   # the site, typed
type_run(TB["motionLine"] + 0.45, TB["motionLine"] + 1.25, len("visions.joaoqueiros.com/motion"), 0.03, 0.0)
type_run(line + 0.6, line + 1.5, len("ai.joaoqueiros.com/atlastudio"), 0.03, 0.2)
add(bell(hz(79), 3.0), line + 1.6, 0.0, 0.04)

# ---- master: a soft-clip that lifts the body and keeps the peaks round, then a fade at the very end
mix = np.stack([L, R], axis=1)
mix /= np.max(np.abs(mix))
DRIVE = 2.6
mix = np.tanh(mix * DRIVE) / np.tanh(DRIVE) * 0.58   # the level Seamless and Ninefold use
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
