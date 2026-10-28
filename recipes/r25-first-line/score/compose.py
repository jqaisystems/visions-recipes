"""
R25 · First Line. Original score, composed in code, timed to the film's one table (bake/table.json).

32 s at 96 bpm in D minor, resolving to F major as the trails fly out over Porto at dawn.
The brief: a night room, a low D, the lamp clicks, the pencil scratches one line and lands on a hit.
The roughs: a plucked twelve-string line on Dm, Bb, F, C (a nod to Porto), a pencil scratch on every rough, a
paper-flutter rhythm under the flip book. Ink and paint: each stroke draws with a rising swish and a plucked note, the
lift is a riser, the ink wipe a brush swish, and at the colour wipe the piano and strings arrive; the lock is the big
hit. The system: a groove, and an orchestral hit and stamp on every panel. Worldwide: a rising chord as the trails fly
out, F major opens, the figures land as stamps. The title: F major, bells as the URL types.
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
rng = np.random.default_rng(25)
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


# ---------------------------------------------------------------- First Line
lamp, line, roughs, flips, strokes, lift, wipes, lock, panels, trails, figures = (
    TB[k] for k in ("lamp", "line", "roughs", "flips", "strokes", "lift", "wipes", "lock", "panels", "trails", "figures"))
TU = T["title"] + 0.6   # the lockup wipes on; the URL types at TU + 1.2


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


DM, BB, FM, CM, GM, AM = [50, 57, 62, 65], [46, 58, 62, 65], [41, 57, 60, 65], [48, 55, 60, 64], [43, 58, 62, 67], [45, 57, 61, 64]

# ---- the night room: a low D, a hum, the river far off; the lamp clicks on
room = norm(lowpass(rng.standard_normal(N), 380)) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.17 * tt) ** 2)
rmask = np.clip(1 - (tt - T["sketch"][0]) / 2.0, 0.3, 1) * np.clip((T["world"][0] + 0.5 - tt) / 0.5, 0, 1)
L += 0.05 * room * rmask
R += 0.05 * np.roll(room, 5555) * rmask
dr = (np.sin(2 * np.pi * hz(38) * tt) + 0.3 * np.sin(2 * np.pi * hz(50) * tt * 1.002)) * np.clip(tt / 1.2, 0, 1) * np.clip((T["ink"][0] + 2 - tt) / 1.5, 0, 1)
L += 0.07 * dr
R += 0.07 * dr
add(norm(highpass(noise(0.03, a=0.0002, rel=0.004), 2500)), lamp, -0.4, 0.3)
add(norm(lowpass(noise(0.08, a=0.0003, rel=0.02), 900)), lamp + 0.004, -0.4, 0.15)
add(tone(hz(57), 1.6, a=0.004, rel=0.6, harm=(1, 0.4)), lamp + 0.05, -0.3, 0.03)   # the bulb's warm ring
add(piano(74, 2.4), lamp + BEAT * 2, 0.2, 0.05)

# ---- one line: the pencil scratch, then the hit as it lands
scratch(line[1] - line[0], 0.22, 0.1, line[0])
add(swish(0.6, 400, 6000, rise=True), line[1] - 0.6, 0.0, 0.12)
hit(line[1], 0.9, DM)

# ---- the roughs: twelve-string on Dm Bb F C in eighths, a kick on the beat, a scratch on every rough
b0, b1 = T["sketch"][0], T["ink"][0]
add(swish(0.55, 300, 8000), wipes[0]["t"] - 0.15, -0.3, 0.16)
PROG = [DM, BB, FM, CM]
ARP = [0, 2, 3, 2, 1, 2, 3, 2]
k = 0
tb = b0
while tb < b1 + 4 * BEAT - 1e-6:   # it carries on under the strokes, quieter
    ch = PROG[(k // 8) % 4]
    g = 0.11 if tb < b1 else 0.07
    if k % 8 == 0:
        twelve(ch[0] - 12, 2.2, g * 1.2, -0.1, tb)
    twelve(ch[ARP[k % 8]] + 12, 0.9, g * 0.8, 0.35 * (-1) ** k, tb)
    if k % 2 == 0 and tb < b1:
        add(kick(), tb, 0.0, 0.2)
    if k % 4 == 2 and tb < b1:
        add(hat(), tb, 0.4, 0.05)
    tb += BEAT / 2
    k += 1
for i, tr in enumerate(roughs):
    scratch(0.18 + 0.08 * (i % 3), 0.13, 0.6 * math.sin(i * 2.1), tr)
for i, tf in enumerate(flips):
    flutter(tf, 0.18, 0.5 * (-1) ** i)

# ---- ink and paint: each stroke draws itself with a swish and a note, the lift rises, the wipes swish
for j, (s0, s1) in enumerate(strokes):
    add(swish(s1 - s0, 500, 7000, rise=True), s0, -0.45 + 0.3 * j, 0.1)
    scratch(s1 - s0, 0.08, -0.45 + 0.3 * j, s0)
    twelve([62, 65, 69, 74][j], 1.8, 0.1, -0.45 + 0.3 * j, s0)
add(swish(lift[1] - lift[0] + 0.3, 200, 9000, rise=True), lift[0], 0.0, 0.2)
for q in range(8):
    add(shime(), lift[0] + q * (lift[1] - lift[0]) / 8, 0.3 * (-1) ** q, 0.04 + 0.04 * q / 8)
add(swish(0.6, 300, 6000), wipes[1]["t"] - 0.1, 0.4, 0.18)
add(piano(62, 1.8), wipes[1]["t"], -0.2, 0.06)
tc = wipes[2]["t"]
add(swish(0.7, 400, 10000), tc - 0.15, -0.4, 0.2)
for j, m in enumerate([46, 58, 62, 65, 70]):   # the colour arrives on Bb: a piano chord and the strings swell
    add(piano(m, 2.4), tc + 0.01 * j, -0.5 + 0.25 * j, 0.06)
strings([58, 62, 65, 70], tc, lock - tc + 1.2, 0.05, a=0.35)
add(swish(1.0, 300, 9000, rise=True), lock - 1.0, 0.0, 0.16)
hit(lock, 1.3, AM)
strings([45, 57, 61, 64, 69], lock, T["system"][0] - lock + 0.3, 0.06, a=0.08)
for j, m in enumerate([81, 85, 88]):
    add(bell(hz(m), 1.6), lock + 0.35 + 0.08 * j, 0.3, 0.03)

# ---- the system: a groove on Dm Gm Bb A, a hit and a stamp on every panel
s0, s1 = T["system"][0], T["world"][0]
SPROG = [DM, GM, BB, AM]
k = 0
tb = s0
while tb < s1 - 1e-6:
    ch = SPROG[int((tb - s0 + 1e-6) / (BEAT * 2)) % 4]   # a chord every two beats
    if k % 2 == 0:
        add(kick(), tb, 0.0, 0.26)
        add(pluck(hz(ch[0] - 12), 0.5, 0.25), tb, -0.1, 0.16)
    if k % 4 == 2:
        add(snare(), tb, 0.1, 0.13)
    add(hat(), tb + BEAT / 4, 0.45, 0.04)
    add(piano(ch[1 + k % 3] + 12, 0.8), tb, 0.3 * (-1) ** k, 0.035)
    tb += BEAT / 2
    k += 1
strings([62, 65, 69], s0, s1 - s0, 0.03, a=1.0)
for j, p in enumerate(panels):
    tp = p["t"]
    hit(tp, 0.95 if j in (0, 5) else 0.7, SPROG[j % 4])
    stamp(tp)
    add(swish(0.3, 800, 8000), tp - 0.3, -0.3, 0.07)

# ---- worldwide: the window opens, a rising chord as the trails fly out, F major, the figures stamp
tw = T["world"][0]
hit(tw, 1.1, FM)
add(swish(1.4, 200, 9000), tw - 0.2, 0.0, 0.2)
for j, m in enumerate([41, 53, 57, 60, 65, 69, 72]):   # the chord climbs in from the bass as the trails go
    add(tone(hz(m), DUR - trails - 0.15 * j, a=0.25, rel=2.6, harm=(1, 0.3, 0.12), detune=0.0007), trails + 0.15 * j, -0.6 + 0.2 * j, 0.05)
strings([53, 57, 60, 65, 69], trails, T["title"] - trails + 2.0, 0.07, a=0.6)
add(swish(2.2, 300, 12000, rise=True), trails - 0.2, 0.0, 0.16)
for j, m in enumerate([72, 74, 77, 76, 72]):
    twelve(m, 1.4, 0.07, 0.25, trails + 0.3 + j * BEAT * 0.75)
for j, fg in enumerate(figures):
    add(taiko(56, 0.9), fg["t"], 0.0, 0.32)
    stamp(fg["t"] - 0.02, 0.12, 0.2)
    add(bell(hz([77, 81, 84][j]), 1.4), fg["t"], -0.3 + 0.3 * j, 0.03)

# ---- the title: F major settles, the lockup wipes with a swish, bells as the URL types
add(swish(0.8, 600, 9000), TU - 0.15, -0.3, 0.12)
for j, m in enumerate([41, 53, 60, 65, 69, 72]):
    add(piano(m, 3.2), TU + 0.02 * j, -0.5 + 0.2 * j, 0.05)
for j, m in enumerate([84, 88, 91, 96, 91, 89]):
    add(bell(hz(m), 2.0), TU + 1.2 + j * 0.12, 0.4 * math.sin(j), 0.03)
add(bell(hz(77), 3.0), TU + 2.3, 0.0, 0.05)

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
