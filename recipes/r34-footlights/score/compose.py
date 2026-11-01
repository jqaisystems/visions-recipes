"""
R34 · Footlights. Original score, composed in code, timed to the film's one table (bake/table.json).

33.1 s at 96 bpm in D major, at night: a warm electric piano over a sub bass and brushes, Dmaj7, Bm7, Gmaj7, A6, a
bar each, with a soft vinyl hiss. Every move on stage has its sound on the beat: the lamp flickering on, curtain rings
on the rail, the phone rising, flaps and PIN tiles turning over, a bell when the PIN matches, the cable unrolling,
Wi-Fi pings, the pulley and a fast flutter of frames, slider and button clicks, the meeting tile lighting on a chord,
the footlights coming on, the blind's ratchet. Then the curtains close, the front-cloth drops, the logo lands on a D
major chord with a bell, and the URL types.
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
rng = np.random.default_rng(134)
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






# ---------------------------------------------------------------- Footlights
E, LINES = TB["E"], TB["lines"]
# D major at night, a bar each: Dmaj7, Bm7, Gmaj7, A6
CHORDS = [[50, 54, 57, 61], [47, 50, 54, 57], [43, 47, 50, 54], [45, 49, 52, 54]]
BASS = [38, 35, 31, 33]


def epiano(m, t0, g=1.0, dur=1.8, pan=0.0):
    # a warm electric piano: a sine with a bell partial on the attack, and a slow tremolo
    f = hz(m)
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 3)
         + 0.18 * np.sin(2 * np.pi * 7.02 * f * t) * np.exp(-t * 14)) * np.exp(-t * 1.3) * (1 + 0.18 * np.sin(2 * np.pi * 4.6 * t))
    s[: int(0.003 * SR)] *= np.linspace(0, 1, int(0.003 * SR))
    k = min(n, int(0.03 * SR))
    s[-k:] *= np.linspace(1, 0, k)
    add(lowpass(s, 3200), t0, pan, g)


def sub(m, t0, g=1.0, dur=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * hz(m) * t) * np.minimum(1, t * 60) * np.exp(-t * 2.2)
    add(s, t0, 0.0, g)


def brush(t0, g=1.0, pan=0.0, dur=0.22):
    # a brush swept across a snare: filtered noise that swells and falls
    n = int(dur * SR)
    u = np.arange(n) / n
    add(norm(highpass(lowpass(rng.standard_normal(n), 7000), 1500)) * np.sin(np.pi * u) ** 1.5, t0, pan, g)


def slide(t0, dur=0.3, g=0.05, pan=0.0):
    add(swish(dur, 300, 3000), t0, pan, g)


def tap(t0, g=0.08, pan=0.0):
    add(norm(lowpass(noise(0.05, a=0.0005, rel=0.02), 1800)), t0, pan, g)
    thud(t0, g * 0.6, 120)


def flip(t0, g=0.06, pan=0.0):
    # a small tile turned over: a tick and a paper slap
    add(norm(highpass(noise(0.012, a=0.0002, rel=0.004), 3500)), t0, pan, g)
    add(norm(highpass(noise(0.04, a=0.0005, rel=0.012), 1400)), t0 + 0.06, pan, g * 0.7)


def rings(t0, dur, g=0.06, pan=0.0):
    # curtain rings running along a rail: a train of small metal clicks
    k = 0
    while k * 0.035 < dur:
        add(tone(2400 + 600 * hsh(t0 + k), 0.05, a=0.0005, rel=0.02, harm=(1, 0.4)), t0 + k * 0.035 + 0.01 * hsh(k * 1.3), pan, g * (0.5 + 0.5 * hsh(k * 2.1)))
        k += 1


def hum(t0, dur, g=0.03):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * 100 * t) + 0.4 * np.sin(2 * np.pi * 200 * t)) * env(n, 0.3, 0.6)
    add(lowpass(s, 600), t0, 0.0, g)


def rattle(t0, dur, g=0.06):
    # a roller blind coming down: a ratchet slowing as it goes
    k, x = 0, 0.0
    while x < dur:
        add(norm(highpass(noise(0.01, a=0.0002, rel=0.004), 2500)), t0 + x, 0.2, g)
        x += 0.03 + 0.04 * (x / dur)
        k += 1


# ---- the band: electric piano over a sub bass and brushes, Dmaj7 Bm7 Gmaj7 A6, then D for the logo
end_band = E["close"][0] + BEAT * 2
for k, bt in enumerate(beats(0.0, end_band)):
    bar, beat = (k // 4) % 4, k % 4
    ch = CHORDS[bar]
    if beat == 0:
        for j, m in enumerate(ch[1:]):
            epiano(m + 12, bt + 0.012 * j, 0.035, BEAT * 4.2, -0.3 + 0.3 * j)
    if k >= 4 and beat in (0, 2):
        sub(BASS[bar] + (7 if beat == 2 else 0), bt, 0.32 if k >= 8 else 0.18, BEAT * 1.6)
    if k >= 8:
        add(kick(), bt, 0.0, 0.07 if beat == 0 else 0.0)
        brush(bt + BEAT * 0.5, 0.03, 0.3)
        if beat in (1, 3):
            brush(bt, 0.05, -0.2, 0.3)
    if k >= 16:
        # a little melody in the right hand, an eighth off the beat
        mel = [ch[3] + 12, ch[2] + 12, ch[3] + 14, ch[1] + 24][beat]
        epiano(mel, bt + BEAT * 0.5, 0.025, BEAT * 1.2, 0.35)
# vinyl hiss under everything, a little crackle
hiss = lowpass(highpass(rng.standard_normal(N), 3000), 9000) * 0.012
add(hiss * env(N, 1.0, 1.5), 0.0, 0.0, 1.0)
for i in range(int(DUR * 7)):
    add(norm(highpass(noise(0.004, a=0.0001, rel=0.002), 2000)), rng.random() * DUR, rng.random() - 0.5, 0.01 * rng.random())

# ---- the stage
hum(E["lamp"][0], 1.5, 0.02)
for x in (0.0, 0.18, 0.4):
    add(norm(highpass(noise(0.01, a=0.0002, rel=0.004), 3000)), E["lamp"][0] + x * 1.2, -0.6, 0.04)   # the lamp's flicker
rings(E["curtain"][0], E["curtain"][1] - E["curtain"][0], 0.05, 0.0)
add(swish(1.2, 200, 2400), E["curtain"][0], 0.0, 0.07)
add(swish(0.9, 300, 3000, rise=True), E["phoneUp"][0], -0.4, 0.07)
thud(E["phoneUp"][1] - 0.15, 0.25, 80)
for k, tf in enumerate(E["flaps"]):
    flip(tf, 0.09, -0.4)
    epiano(74 + [0, 4][k], tf + 0.12, 0.04, 1.0, -0.4)
add(swish(0.5, 2000, 9000, rise=True), E["beam"][0], -0.2, 0.03)
slide(E["panelIn"][0], 0.5, 0.06, 0.4)
for k, tp in enumerate(E["pinPhone"]):
    flip(tp, 0.06, -0.4)
for k, tp in enumerate(E["pinPC"]):
    flip(tp, 0.06, 0.4)
add(bell(hz(81), 1.6), E["match"], 0.0, 0.05)
add(bell(hz(88), 1.6), E["match"] + 0.08, 0.1, 0.03)
add(swish(0.5, 3000, 300), E["screenOff"][0], -0.4, 0.04)
key(E["usbBtn"], 0.08, 0.4)
k = 0
while k * 0.05 < E["cable"][1] - E["cable"][0]:   # the cable unrolling: a soft tick of a coil
    add(norm(lowpass(noise(0.02, a=0.0005, rel=0.008), 2200)), E["cable"][0] + k * 0.05, -0.4 + 0.6 * k * 0.05 / (E["cable"][1] - E["cable"][0]), 0.03)
    k += 1
thud(E["cable"][1], 0.15, 110)
for k, tw in enumerate(E["wifi"]):
    add(tone(hz(86 + 2 * k), 0.5, a=0.002, rel=0.3, harm=(1, 0.3)), tw, -0.3, 0.025)
# the feed: the pulley's wheels, and a fast flutter of frames ticking past
for k in range(2):
    add(norm(lowpass(noise(0.06, a=0.001, rel=0.02), 900)), E["pulley"][0] + 0.25 * k, -0.2 + 0.4 * k, 0.08)
run_end = E["close"][0]
x = E["run"]
while x < run_end:
    add(norm(highpass(noise(0.008, a=0.0002, rel=0.003), 4000)), x, 0.1, 0.012)
    x += 70 / 210
flip(E["fps"], 0.08, 0.3)
for a, b in (E["zoom"], E["expo"]):
    key(a, 0.05, 0.4)
    add(swish(b - a, 400, 2400, rise=True), a, 0.4, 0.03)
    key(b, 0.05, 0.4)
for ts in E["switch"]:
    key(ts, 0.09, 0.4)
    add(swish(0.25, 1200, 6000), ts + 0.02, 0.3, 0.04)
key(E["start"], 0.1, 0.3)
slide(E["panelOut"][0], 0.5, 0.06, 0.4)
for j, m in enumerate([62, 66, 69, 73, 74]):
    epiano(m + 12, E["tile"] + 0.06 * j, 0.04, 2.0, -0.3 + 0.15 * j)
add(bell(hz(86), 2.0), E["tile"], 0.3, 0.04)
for k, tf in enumerate(E["foot"]):
    add(norm(lowpass(noise(0.03, a=0.0005, rel=0.01), 1500)), tf, -0.6 + 0.24 * k, 0.07)
    add(tone(hz(62 + [0, 4, 7, 11, 12, 16][k] + 12), 0.8, a=0.002, rel=0.5, harm=(1, 0.3, 0.1)), tf + 0.15, -0.6 + 0.24 * k, 0.03)
hum(E["foot"][0], E["close"][0] - E["foot"][0], 0.015)
rattle(E["blind"][0], E["blind"][1] - E["blind"][0], 0.05)
thud(E["blind"][1], 0.1, 140)
for k, tg in enumerate(E["tags"]):
    flip(tg, 0.08, -0.2 + 0.2 * k)

# ---- every word of type set down, and lifted off again
for LN in LINES:
    n = len(LN["words"])
    for k in range(n):
        tap(LN["t"] + k * 0.16 + 0.2, 0.06, -0.5 + k / max(1, n - 1))
    slide(LN["out"], 0.35, 0.025, 0.3)

# ---- the curtains close, the front-cloth drops, the logo on D, the URL typing
rings(E["close"][0], E["close"][1] - E["close"][0], 0.05, 0.0)
add(swish(1.1, 200, 2400), E["close"][0], 0.0, 0.07)
add(swish(0.8, 3000, 200), E["cloth"][0], 0.0, 0.08)
thud(E["cloth"][1], 0.3, 60)
for j, m in enumerate([38, 50, 57, 62, 66, 69, 73]):
    add(piano(m, 3.4), E["logo"] + 0.01 * j, -0.5 + 0.17 * j, 0.055)
add(bell(hz(78), 3.0), E["logo"] + 0.02, 0.0, 0.05)
sub(38, E["logo"], 0.4, 2.4)
for k in range(5):
    epiano([74, 78, 81, 85, 86][k], E["name"] + k * BEAT * 0.5, 0.04, 1.4, -0.4 + 0.2 * k)
URL = "ai.joaoqueiros.com/systems/phone-webcam-bridge"
for k in range(0, len(URL), 2):
    key(E["url"] + 1.1 * k / len(URL), 0.04, 0.2)

# ---- master: a soft-clip that lifts the body and keeps the peaks round, then a fade at the very end
mix = np.stack([L, R], axis=1)
mix /= np.max(np.abs(mix))
DRIVE = 2.4
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
