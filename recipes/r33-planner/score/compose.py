"""
R33 · Planner. Original score, composed in code, timed to the film's one table (bake/table.json).

33.3 s at 108 bpm in F major: a marimba, a felt piano, an upright bass and a shaker over F, Dm, Bb, C, a bar each.
Every move on the desk has its sound on the beat: the form sliding in, tabs pulled out, the volvelle clicking, banners
unrolling, the accordion unfolding, a riffle of flaps, rubber stamps, a crumple and a roll, the printer chattering a
line at a time, a pencil ticking, the strip tearing and the paper plane. Then the sweep, the logo on an F major chord
with a bell, and the URL typing.
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
rng = np.random.default_rng(133)
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







# ---------------------------------------------------------------- Planner
E, LINES = TB["E"], TB["lines"]
CHORDS = [[41, 53, 57, 60], [38, 50, 53, 57], [34, 50, 53, 58], [36, 52, 55, 60]]   # F, Dm, Bb, C: a bar each
BASS = [29, 26, 34, 36]


def marimba(m, t0, g=1.0, pan=0.0):
    # a struck wooden bar: the fundamental, its tuned fourth partial, a knock on the attack
    f = hz(m)
    add(tone(f, 0.9, a=0.001, rel=0.28, harm=(1.0, 0.0, 0.0, 0.25)) + 0.12 * tone(f * 9.9, 0.9, a=0.0005, rel=0.015), t0, pan, g)


def felt(m, t0, g=1.0, dur=1.8, pan=0.0):
    add(lowpass(piano(m, dur), 1600), t0, pan, g)


def upright(m, t0, g=1.0, dur=0.7):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * hz(m) * t) + 0.35 * np.sin(4 * np.pi * hz(m) * t) + 0.12 * np.sin(6 * np.pi * hz(m) * t)) * np.exp(-t * 4.5)
    s[: int(0.006 * SR)] *= np.linspace(0, 1, int(0.006 * SR))
    add(lowpass(s, 900), t0, 0.0, g)


def shaker(t0, g=1.0, pan=0.3):
    add(norm(highpass(noise(0.07, a=0.012, rel=0.02), 5000)), t0, pan, g)


def slide(t0, dur=0.3, g=0.05, pan=0.0):
    add(swish(dur, 300, 3000), t0, pan, g)


def tap(t0, g=0.08, pan=0.0):
    add(norm(lowpass(noise(0.05, a=0.0005, rel=0.02), 1800)), t0, pan, g)
    thud(t0, g * 0.6, 120)


def click(t0, g=0.1, pan=0.0):
    # the volvelle's split pin catching: a dry wooden click
    add(block(1250, 1.0), t0, pan, g)
    add(norm(highpass(noise(0.01, a=0.0002, rel=0.003), 3000)), t0, pan, g * 0.6)


def crumple(t0, dur, g=0.1, pan=0.0):
    # paper balled up: a run of small crackles
    k = 0
    while k * 0.018 < dur:
        add(norm(highpass(noise(0.012, a=0.0003, rel=0.004), 2500 + 2500 * hsh(t0 + k))), t0 + k * 0.018 + 0.008 * hsh(k * 3.3), pan + 0.3 * (hsh(k) - 0.5), g * (0.4 + 0.6 * hsh(k * 1.7)))
        k += 1


def rip(t0, g=0.1):
    # a strip torn along its perforation
    n = int(0.32 * SR)
    am = 1 + 0.6 * np.sign(np.sin(np.arange(n) / SR * 2 * np.pi * 70))
    add(norm(highpass(noise(0.32, a=0.01, rel=0.12), 1500)) * am, t0, 0.0, g)


# ---- the band: marimba and felt piano over an upright bass and a shaker, F Dm Bb C, then F for the logo
end_band = E["sweep"][0]
for k, bt in enumerate(beats(0.0, end_band)):
    bar, beat = (k // 4) % 4, k % 4
    ch = CHORDS[bar]
    if k >= 2:
        upright(BASS[bar] + (7 if beat == 2 else 0), bt, 0.3 if beat in (0, 2) else 0.0)
    if k >= 8:
        add(kick(), bt, 0.0, 0.08 if beat in (0, 2) else 0.0)
        if beat in (1, 3):
            add(norm(lowpass(highpass(noise(0.12, a=0.004, rel=0.05), 1500), 6000)), bt, -0.2, 0.05)
    if k >= 4:
        shaker(bt + BEAT * 0.5, 0.02, 0.35)
        shaker(bt, 0.012, 0.35)
    # the marimba: a broken chord, then eighths
    pat = [ch[1] + 12, ch[2] + 12, ch[3] + 12, ch[2] + 24]
    marimba(pat[beat], bt, 0.06, -0.35 + 0.23 * beat)
    if k >= 16:
        marimba([ch[3] + 12, ch[1] + 24, ch[2] + 12, ch[3] + 24][beat], bt + BEAT * 0.5, 0.035, 0.4 - 0.2 * beat)
    if beat == 0 and k >= 4:
        for j, m in enumerate(ch[1:]):
            felt(m + 12, bt + 0.01 * j, 0.03, 2.0, -0.3 + 0.3 * j)

# ---- foley on the desk
slide(E["formIn"][0], 0.5, 0.07, -0.4)
tap(E["formIn"][1], 0.1)
for k, tb in enumerate(E["tabs"]):
    slide(tb, 0.28, 0.05, 0.3)
    tap(tb + 0.3, 0.05, 0.4)
slide(E["formOut"][0], 0.5, 0.05, -0.5)
slide(E["wheelIn"][0], 0.5, 0.06, -0.3)
tap(E["wheelIn"][1], 0.09, -0.3)
for k, c in enumerate(E["clicks"]):
    click(c, 0.12, -0.3)
    click(c + 0.09, 0.05, -0.3)
    add(swish(0.45, 500, 6000, rise=True), c + 0.12, 0.3, 0.035)    # the banner unrolls
    marimba(72 + [0, 2, 4, 7][k], c + 0.12, 0.05, 0.3)
for k in range(4):
    slide(E["toRows"][0] + 0.1 * k, 0.35, 0.03, -0.4 + 0.2 * k)
for k, rw in enumerate(E["rows"]):
    flutter(rw, 0.05, -0.3 + 0.15 * k)
for d in range(30):                                                  # the flaps lift in a wave: a riffle
    c, rw = d % 7, d // 7
    ft = E["flaps"] + (c + rw) * 0.12
    add(norm(highpass(noise(0.04, a=0.002, rel=0.015), 2200)), ft + 0.05 * hsh(d), -0.6 + 0.2 * c, 0.03)
for k, ts in enumerate(E["stamps"]):
    slide(ts - 0.45, 0.3, 0.04, 0.5)
    thud(ts, 0.3, 80)
    stamp(ts, 0.16, 0.1)
    crumple(ts + 0.3, 0.3, 0.07, 0.1)
    add(swish(0.5, 200, 1600), ts + 0.6, 0.5, 0.05)                 # the ball rolls off
    slide(ts + 0.75, 0.4, 0.05, -0.2)                                # the new card slides in
    marimba(65 + [0, 3, 7][k], ts + 1.2, 0.05, -0.2)
for k in range(4):
    flutter(E["foldUp"][0] + k * 0.22, 0.04, 0.3 - 0.2 * k)
slide(E["printerIn"][0], 0.5, 0.06, 0.0)
thud(E["printerIn"][1], 0.15, 90)
slide(E["feedIn"][0], 0.6, 0.05, 0.0)
rows = len(TB["csv"]) + 1
for k in range(rows):                                                # the printer, a line at a time
    t0 = E["feed"][0] + (E["feed"][1] - E["feed"][0]) * k / rows
    for i in range(5):
        key(t0 + i * 0.022, 0.03, -0.3 + 0.15 * i)
    add(norm(lowpass(noise(0.05, a=0.003, rel=0.02), 900)), t0, 0.0, 0.03)
n = int((E["feed"][1] - E["feed"][0]) * SR)
motor = lowpass(np.sin(2 * np.pi * 100 * np.arange(n) / SR) * 0.6 + rng.standard_normal(n) * 0.2, 400)
add(motor * env(n, 0.2, 2.0), E["feed"][0], 0.0, 0.03)
for k in range(9):
    scratch(0.09, 0.05, -0.3, E["ticks"][0] + (E["ticks"][1] - E["ticks"][0]) * (k + 0.5) / 9)
rip(E["tear"], 0.09)
for k in range(3):
    flutter(E["plane"][0] + k * 0.22, 0.05, -0.2 + 0.2 * k)
add(swish(1.4, 400, 5000), E["fly"][0], 0.6, 0.07)

# ---- every word of type set down on the desk, and picked off again
for LN in LINES:
    n = len(LN["words"])
    for k in range(n):
        tap(LN["t"] + k * 0.16 + 0.2, 0.06 if not LN.get("big") else 0.1, -0.5 + k / max(1, n - 1))
    slide(LN["out"], 0.35, 0.025, 0.3)

# ---- the sweep, the logo on F, the line and the URL typing
slide(E["sweep"][0], 0.8, 0.1, -0.5)
thud(E["sweep"][1], 0.3, 60)
for j, m in enumerate([29, 41, 48, 53, 57, 60, 65]):
    add(piano(m, 3.4), E["logo"] + 0.01 * j, -0.5 + 0.17 * j, 0.06)
add(bell(hz(77), 3.0), E["logo"] + 0.02, 0.0, 0.05)
upright(29, E["logo"], 0.4, 2.0)
for k in range(6):
    marimba([65, 69, 72, 77, 81, 84][k], E["name"] + k * BEAT * 0.5, 0.05, -0.4 + 0.16 * k)
URL = "ai.joaoqueiros.com/systems/content-calendar"
for k in range(0, len(URL), 2):
    key(E["url"] + 1.1 * k / len(URL), 0.04, 0.2)

# ---- master: a soft-clip that lifts the body and keeps the peaks round, then a fade at the very end
mix = np.stack([L, R], axis=1)
mix /= np.max(np.abs(mix))
DRIVE = 2.6
mix = np.tanh(mix * DRIVE) / np.tanh(DRIVE) * 0.58
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
