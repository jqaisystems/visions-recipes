"""
R35 · Pop-Up. Original score, composed in code, timed to the film's one table (bake/table.json).

33.4 s at 88 bpm in G major, in the morning: a soft piano bed, pizzicato strings and a celesta over a sub bass, a kick
and a shaker, Gmaj7, Em7, Cmaj7, D6sus, a bar each. Every paper move has its sound on the beat: the form and the call
notes sliding in, every page turning, a snap and a rising pluck for every card that stands up, a music box for the
section tabs, the pull tab, the fan of swatches, the pencil's scratch as it strikes, writes and ticks, the stamp, the
book closing and the envelope. Then a black sheet slides over, the logo lands on a G major chord with a bell, and the
URL types.
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






# ---------------------------------------------------------------- Pop-Up
E, LINES = TB["E"], TB["lines"]
# G major in the morning, a bar each: Gmaj7, Em7, Cmaj7, D6sus
CHORDS = [[55, 59, 62, 66], [52, 55, 59, 62], [48, 52, 55, 59], [50, 55, 57, 59]]
BASS = [43, 40, 36, 38]


def celesta(m, t0, g=1.0, pan=0.0, dur=1.6):
    # a celesta: a bright sine with a short metallic partial, quick to fade
    f = hz(m)
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 4.0 * f * t) * np.exp(-t * 18)
         + 0.2 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 6)) * np.exp(-t * 3.2)
    s[: int(0.002 * SR)] *= np.linspace(0, 1, int(0.002 * SR))
    add(s, t0, pan, g)


def musicbox(m, t0, g=1.0, pan=0.0):
    f = hz(m)
    n = int(1.4 * SR)
    t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * 5.4 * f * t) * np.exp(-t * 30)) * np.exp(-t * 4.5)
    add(highpass(s, 300), t0, pan, g)


def sub(m, t0, g=1.0, dur=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * hz(m) * t) * np.minimum(1, t * 60) * np.exp(-t * 2.4)
    add(s, t0, 0.0, g)


def shaker(t0, g=1.0, pan=0.0):
    n = int(0.09 * SR)
    u = np.arange(n) / n
    add(norm(highpass(rng.standard_normal(n), 5000)) * np.sin(np.pi * u) ** 2, t0, pan, g)


def page(t0, dur=0.6, g=0.07, pan=0.0):
    # a page turning: a soft swoosh that lifts, and a light slap as it lands
    add(swish(dur, 300, 4200, rise=True), t0, pan, g)
    add(norm(lowpass(noise(0.05, a=0.001, rel=0.02), 2500)), t0 + dur * 0.92, -pan, g * 0.7)


def popup(t0, m, g=0.05, pan=0.0):
    # a card standing up: a little paper snap and a rising pluck
    add(norm(highpass(noise(0.02, a=0.0003, rel=0.008), 2500)), t0, pan, g * 0.9)
    add(pluck(hz(m), 0.6, 0.6), t0 + 0.01, pan, g * 0.8)
    add(pluck(hz(m + 7), 0.5, 0.5), t0 + 0.06, pan, g * 0.4)


def slide(t0, dur=0.3, g=0.05, pan=0.0):
    add(swish(dur, 300, 3000), t0, pan, g)


def tap(t0, g=0.08, pan=0.0):
    add(norm(lowpass(noise(0.05, a=0.0005, rel=0.02), 1800)), t0, pan, g)
    thud(t0, g * 0.6, 120)


# ---- the band: celesta and pizzicato over a sub and a shaker, Gmaj7 Em7 Cmaj7 D6sus, then G for the logo
end_band = E["cloth"][0] + BEAT
for k, bt in enumerate(beats(0.0, end_band)):
    bar, beat = (k // 4) % 4, k % 4
    ch = CHORDS[bar]
    if beat == 0:
        for j, m in enumerate(ch):
            add(piano(m, BEAT * 4), bt + 0.015 * j, -0.3 + 0.2 * j, 0.02)
    if k >= 4:
        pizz([ch[0] + 12, ch[2] + 12, ch[1] + 12, ch[3] + 12][beat], 0.05, 0.3 - 0.2 * (beat % 2), bt)
    if k >= 8 and beat in (0, 2):
        sub(BASS[bar] + (7 if beat == 2 else 0), bt, 0.3, BEAT * 1.6)
    if k >= 8:
        add(kick(), bt, 0.0, 0.06 if beat == 0 else 0.0)
        shaker(bt + BEAT * 0.5, 0.025, 0.4)
        shaker(bt, 0.015, -0.4)
    if k >= 16:
        # the celesta answers in the right hand, an eighth off the beat
        celesta([ch[3] + 12, ch[2] + 12, ch[3] + 14, ch[1] + 24][beat], bt + BEAT * 0.5, 0.025, 0.35)
# a little room under everything
air = lowpass(highpass(rng.standard_normal(N), 2500), 7000) * 0.006
add(air * env(N, 1.0, 1.5), 0.0, 0.0, 1.0)

# ---- intake
slide(E["form"][0], 0.6, 0.07, -0.5)
tap(E["form"][1] - 0.1, 0.07, -0.3)
slide(E["notes"][0], 0.4, 0.05, -0.3)
tap(E["notes"][1] - 0.05, 0.06, -0.2)
add(swish(1.2, 400, 2600), E["feed"][0], 0.0, 0.06)
thud(E["feed"][1], 0.12, 90)
# ---- the book: every leaf turned, every card stood up
for k in range(5):
    a, b2 = E["leaf%d" % k]
    page(a, b2 - a, 0.08 if k else 0.1, 0.3)
    if k == 0:
        thud(b2, 0.2, 70)   # the cover lands
for j in range(2):
    a, b2 = E["strip%d" % j]
    add(swish(b2 - a, 600, 3000), a, -0.2, 0.05)
    for i, tc in enumerate(E["chips%d" % j]):
        popup(tc + 0.3, 79 + [0, 2, 4][i] - 5 * j, 0.05, 0.2 + 0.1 * i)
for j, tt in enumerate(E["tabs"]):
    musicbox(74 + [0, 2, 4, 7, 9, 11, 12][j], tt, 0.035, 0.6)
for j, tp in enumerate(E["per"]):
    popup(tp, 67 + 4 * j, 0.07, -0.4 + 0.4 * j)
slide(E["tone"][0], E["tone"][1] - E["tone"][0], 0.05, -0.4)
key(E["tone"][1], 0.08, -0.4)
for j, tw in enumerate(E["toneW"]):
    popup(tw, 76 + 2 * j, 0.05, -0.4)
for j, ts in enumerate(E["sky"]):
    popup(ts, 62 + 5 * j, 0.07, 0.4)
popup(E["gap"][0], 83, 0.05, 0.3)
celesta(86, E["gap"][0] + 0.1, 0.04, 0.3)
add(swish(E["fan"][1] - E["fan"][0], 800, 5000, rise=True), E["fan"][0], -0.4, 0.04)
for j in range(5):
    add(norm(highpass(noise(0.015, a=0.0002, rel=0.006), 3000)), E["fan"][0] + j * 0.18, -0.5 + 0.1 * j, 0.04)
popup(E["spec"], 74, 0.06, -0.2)
for j, tr in enumerate(E["rows"]):
    popup(tr, 67 + [0, 2, 4, 7, 9][j], 0.05, 0.4)
add(swish(0.6, 400, 2400, rise=True), E["flap"][0], 0.3, 0.05)
for j, tq in enumerate(E["qt"]):
    popup(tq, 71 + 5 * j, 0.06, 0.3)
    musicbox(83 + 2 * j, tq + 0.15, 0.03, 0.3)
# ---- the human edit: the pencil, a scratch for the strike, writing, ticks, and the stamp
scratch(E["strike"][1] - E["strike"][0], 0.07, -0.3, E["strike"][0])
x = E["write"][0]
while x < E["write"][1]:
    scratch(0.07, 0.03 + 0.02 * hsh(x), -0.3, x)
    x += 0.11
for tt in E["ticks"]:
    scratch(0.08, 0.05, -0.3, tt)
    scratch(0.1, 0.05, -0.3, tt + 0.1)
stamp(E["stamp"], 0.16, 0.2)
celesta(91, E["stamp"] + 0.05, 0.04, 0.2)
# ---- export: the book closes, folds flat, goes in the envelope
page(E["close"][0], E["close"][1] - E["close"][0], 0.09, -0.3)
thud(E["close"][1], 0.25, 65)
add(swish(E["flat"][1] - E["flat"][0], 2400, 300), E["flat"][0], 0.0, 0.05)
slide(E["env"][0], 0.5, 0.06, 0.5)
add(swish(0.4, 600, 2400), E["env"][0] + 0.5, 0.0, 0.05)
tap(E["env"][1] - 0.1, 0.07, 0.1)

# ---- every word of type set down, and lifted off again
for LN in LINES:
    n = len(LN["words"])
    for k in range(n):
        tap(LN["t"] + k * 0.16 + 0.2, 0.05, -0.5 + k / max(1, n - 1))
    slide(LN["out"], 0.35, 0.025, 0.3)

# ---- the black sheet, the logo on G, the URL typing
add(swish(0.8, 300, 2400), E["cloth"][0], -0.3, 0.07)
thud(E["cloth"][1], 0.25, 60)
for j, m in enumerate([43, 55, 59, 62, 66, 69, 74]):
    add(piano(m, 3.4), E["logo"] + 0.01 * j, -0.5 + 0.17 * j, 0.055)
add(bell(hz(79), 3.0), E["logo"] + 0.02, 0.0, 0.05)
sub(43, E["logo"], 0.4, 2.4)
for k in range(5):
    celesta([79, 83, 86, 90, 91][k], E["name"] + k * BEAT * 0.5, 0.04, -0.4 + 0.2 * k)
URL = "ai.joaoqueiros.com/systems/ai-brief-generator"
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
