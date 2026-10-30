"""
R26 · The Gate. Original score, composed in code, timed to the film's one table (bake/table.json).

32 s at 112 bpm in E minor, resolving to G major when the gate opens.
The flood: a stamp, then a vortex of paper and typewriter clicks that speeds up with the storm, over a pizzicato
ostinato; the kill switch cuts everything dead and lands a hit with a metal shing, then paper rains down.
Find: a clockwork pulse, a swish as the map draws, a falling note and a thud for every pin, a shimmer for each shop.
Score: a ratchet as the needle sweeps, and a stamp per card in its own pitch (hot high, skip a dull thud).
Draft and check: typewriter keys as the drafts type, a hum under the scan line, a low thunk and a scratch for every
flag, a bell for every repair. The gate: a string swell as it draws, a lock clunk on a rising chord for each lock, a dead
stop, the click, G major opens with a low bell, a metronome tock for every throttled step, a riser through the gate.
The title: G major, a reply chime, bells as the URL types.
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
rng = np.random.default_rng(26)
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


# ---------------------------------------------------------------- The Gate
stamp_t, storm, kill, streets, pins, shops, cards, fold_t, split, drafts, scan, flags, gate_draw, locks, stop_t, approve, gate_open, sends, reply, mark_t = (
    TB[k] for k in ("stamp", "storm", "kill", "streets", "pins", "shops", "cards", "fold", "split", "drafts", "scan", "flags",
                    "gate_draw", "locks", "stop", "approve", "gate_open", "sends", "reply", "mark"))
TU = mark_t + 1.0   # the URL types


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


EM, CM, GM, DMJ, AMN = [52, 55, 59, 64], [48, 55, 60, 64], [43, 55, 59, 62], [50, 54, 57, 62], [45, 52, 57, 60]

# ---- the flood: a stamp, then the vortex speeds up over a pizzicato ostinato
thud(stamp_t, 0.5, 60)
add(norm(lowpass(noise(0.06, a=0.0004, rel=0.02), 1500)), stamp_t, 0.0, 0.3)
pizz(64, 0.14, 0.0, stamp_t)
STORM = 340
for i in range(1, STORM):
    born = storm[0] + (storm[1] - storm[0]) * math.sqrt(i / STORM)
    if born < kill - 0.02 and i % 2 == 0:
        key(born, 0.035 + 0.04 * (born - storm[0]) / (kill - storm[0]), 0.8 * math.sin(i * 2.39996))
add(swish(kill - storm[0], 200, 9000, rise=True), storm[0], 0.0, 0.22)
OST = [64, 67, 71, 67, 64, 71, 76, 71]
tb, k = stamp_t + BEAT, 0
while tb < kill - 1e-6:
    pizz(OST[k % 8] - 12, 0.12, 0.3 * (-1) ** k, tb)
    if k % 2 == 0:
        pizz(40, 0.14, -0.1, tb, 0.6)
    tb += BEAT / 2
    k += 1
# the kill switch: everything stops dead, then the hit
i0 = int((kill - 0.07) * SR)
i1 = int(kill * SR)
L[i0:i1] *= np.linspace(1, 0.02, i1 - i0)
R[i0:i1] *= np.linspace(1, 0.02, i1 - i0)
L[i1:int((kill + 0.01) * SR)] *= 0.02
R[i1:int((kill + 0.01) * SR)] *= 0.02
add(taiko(42, 2.0), kill, 0.0, 0.65)
add(kick(), kill, 0.0, 0.35)
add(crash(2.4), kill, -0.2, 0.12)
shing(kill, 0.06)
for j, m in enumerate([40, 52, 55, 59, 64]):
    add(tone(hz(m), 0.6, a=0.003, rel=0.25, harm=(1, 0.6, 0.4, 0.25, 0.15)), kill, -0.6 + 0.3 * j, 0.05)
add(swish(1.0, 300, 4000), kill + 0.15, 0.0, 0.12)   # the drained envelopes fall
for j in range(14):
    add(norm(lowpass(noise(0.05, a=0.001, rel=0.02), 2500)), kill + 0.4 + j * 0.07 + 0.03 * hsh(j), 0.6 * math.sin(j * 1.7), 0.05 * (1 - j / 14))

# ---- the groove from find to the gate: a clockwork pulse, a kick, a bass on the progression
g0, g1 = T["find"][0], gate_draw[0]
PROG = [EM, CM, GM, DMJ]
tb, k = g0, 0
while tb < g1 - 1e-6:
    ch = PROG[(k // 8) % 4] if tb < T["draft"][0] else [AMN, EM, CM, DMJ][(k // 8) % 4]
    add(block(1500 if k % 2 == 0 else 1250), tb, 0.5, 0.035)
    add(block(1700), tb + BEAT / 4, 0.5, 0.02)
    if k % 2 == 0:
        add(kick(), tb, 0.0, 0.2)
        add(pluck(hz(ch[0] - 12), 0.45, 0.25), tb, -0.1, 0.13)
    if k % 4 == 2:
        add(snare(), tb, 0.1, 0.07)
    pizz(ch[1 + k % 3] + 12, 0.06, 0.35 * (-1) ** k, tb, 0.3)
    tb += BEAT / 2
    k += 1
strings([52, 59, 64], g0, g1 - g0, 0.025, a=1.2)

# ---- find: the map draws, the pins fall and land, the shops shimmer
add(swish(streets[1] - streets[0], 400, 8000, rise=True), streets[0], -0.2, 0.12)
PENT = [76, 79, 81, 83, 86, 88]
for j, tp in enumerate(pins):
    whistle(tp - 0.28, tp, 2600, 900, 0.025)
    thud(tp, 0.28, 90)
    add(bell(hz(PENT[j]), 1.0), tp, -0.5 + 0.2 * j, 0.025)
for j, ts in enumerate(shops):
    for q in range(4):
        add(tone(hz(PENT[j] + 12 + [0, 3, 7, 12][q]), 0.25, a=0.002, rel=0.08), ts + q * 0.04, 0.4 - 0.2 * j, 0.012)

# ---- score: a ratchet as the needle sweeps, a stamp per card in its lane's pitch
LANE_NOTE = {"HOT": 83, "WARM": 79, "COLD": 71, "SKIP": None}
for c in cards:
    add(swish(0.3, 600, 7000), c["t"] - 0.3, -0.5, 0.06)
    for q in range(8):
        add(block(2200 + 100 * q, 1.0), c["t"] + q * 0.026, 0.1, 0.018)
    ts = c["t"] + 0.2
    thud(ts, 0.22, 80)
    add(norm(lowpass(noise(0.07, a=0.0004, rel=0.025), 2400)), ts, 0.3, 0.1)
    if LANE_NOTE[c["lane"]]:
        add(bell(hz(LANE_NOTE[c["lane"]]), 1.2), ts, 0.3, 0.03)
    add(swish(0.32, 500, 5000), c["t"] + 0.3, 0.5, 0.05)
add(swish(0.4, 300, 3000), fold_t, 0.6, 0.1)
thud(fold_t + 0.33, 0.15, 60)

# ---- draft and check: the split, typewriter keys, the scan hum, flags and repairs
add(swish(0.5, 300, 9000), split - 0.4, 0.0, 0.14)
for j, td in enumerate(drafts):
    pizz([64, 67, 71][j], 0.12, -0.5 + 0.5 * j, td)
    ty = td + 0.2
    for q in range(int((1.5) / 0.055)):   # the copy types in, about eighteen keys a second
        key(ty + q * 0.055 + 0.01 * hsh(q + j * 40), 0.04, -0.5 + 0.5 * j)
n = int((scan[1] - scan[0]) * SR)
u = np.arange(n) / n
hum = sum(np.sin(2 * np.pi * hz(76 + d) * (1 + 0.0 * u) * np.arange(n) / SR) for d in (0, 7)) * np.sin(np.pi * u) ** 0.5
add(hum, scan[0], 0.0, 0.015)
for fl in flags:
    tf = fl["t"]
    thud(tf, 0.25, 55)
    add(norm(highpass(rng.standard_normal(int(0.2 * SR)) * (rng.random(int(0.2 * SR)) > 0.6), 2000)) * env(int(0.2 * SR), 0.002, 0.08), tf, 0.2, 0.08)
    add(tone(hz(46), 0.3, a=0.002, rel=0.12, harm=(1, 0.8, 0.6, 0.4)), tf, 0.0, 0.05)
    tr = tf + BEAT
    add(bell(hz(88), 1.2), tr + 0.1, -0.2, 0.03)
    for q in range(8):
        key(tr + 0.1 + q * 0.056, 0.035, 0.2)
add(swish(0.6, 300, 6000), T["gate"][0] - 0.9, -0.3, 0.1)
thud(T["gate"][0] - 0.15, 0.2, 65)

# ---- the gate: a swell as it draws, a clunk and a rising chord per lock, a dead stop, Approve, G major
strings([40, 52, 59, 64], gate_draw[0], gate_draw[1] - gate_draw[0] + 0.6, 0.06, a=2.5)
for q in range(24):
    add(tone(hz(88 + [0, 3, 7, 10][q % 4]), 0.3, a=0.002, rel=0.1), gate_draw[0] + q * (gate_draw[1] - gate_draw[0]) / 24, 0.6 * math.sin(q), 0.008 + 0.01 * q / 24)
LOCKN = [52, 55, 59, 62]
for j, lk in enumerate(locks):
    tl = lk["t"]
    thud(tl, 0.3, 75)
    add(norm(lowpass(noise(0.04, a=0.0003, rel=0.012), 3000)), tl + 0.01, 0.2, 0.12)
    add(block(900, 1.0), tl + 0.06, 0.2, 0.06)
    for q, m in enumerate(LOCKN[: j + 1]):
        add(tone(hz(m + 12), BEAT * 0.95, a=0.01, rel=0.3, harm=(1, 0.5, 0.25)), tl, -0.4 + 0.25 * q, 0.03)
    add(pluck(hz(LOCKN[j] - 12), 0.6, 0.25), tl, -0.1, 0.14)
add(swish(stop_t - locks[3]["t"], 300, 5000, rise=True), locks[3]["t"] + 0.1, 0.4, 0.06)
# the dead stop: silence from the stop to the click
i0, i1 = int((stop_t - 0.05) * SR), int(stop_t * SR)
L[i0:i1] *= np.linspace(1, 0.0, i1 - i0)
R[i0:i1] *= np.linspace(1, 0.0, i1 - i0)
L[i1:int(approve * SR)] *= 0.0
R[i1:int(approve * SR)] *= 0.0
# Approve: a click, a low bell, and G major opens
add(norm(highpass(noise(0.012, a=0.0002, rel=0.003), 2500)), approve, 0.3, 0.35)
add(tone(1200, 0.04, a=0.0005, rel=0.01), approve, 0.3, 0.1)
add(taiko(48, 2.0), approve + 0.02, 0.0, 0.55)
add(bell(hz(43), 4.0), approve + 0.02, 0.0, 0.12)
add(crash(2.6), approve + 0.02, -0.2, 0.1)
for j, m in enumerate([43, 55, 59, 62, 67, 71]):
    add(piano(m, 3.0), approve + 0.02 + 0.015 * j, -0.5 + 0.2 * j, 0.06)
strings([55, 59, 62, 67, 71], approve, T["title"] - approve + 2.0, 0.08, a=0.3)
for j, ts in enumerate(sends):
    add(block(800, 1.0), ts, -0.3, 0.12)
    add(block(1200, 1.0), ts + 0.005, -0.3, 0.04)
    add(swish(0.32, 400, 6000), ts - 0.02, 0.0, 0.06)
    add(kick(), ts, 0.0, 0.12)
add(swish(T["title"] - sends[2] + 0.2, 200, 12000, rise=True), sends[2], 0.0, 0.2)

# ---- the title: G major settles, the reply chimes, the mark lands, bells as the URL types
tt = T["title"]
add(taiko(52, 1.4), tt, 0.0, 0.3)
for j, m in enumerate([43, 55, 59, 62, 67]):
    add(tone(hz(m), DUR - tt, a=0.15, rel=2.4, harm=(1, 0.3, 0.12), detune=0.0007), tt, -0.6 + 0.3 * j, 0.045)
add(swish(0.55, 600, 7000), reply - 0.05, 0.5, 0.08)
add(bell(hz(79), 1.5), reply + 0.5, 0.3, 0.04)
add(bell(hz(83), 1.5), reply + 0.62, 0.3, 0.035)
add(swish(0.5, 400, 9000, rise=True), mark_t - 0.5, 0.0, 0.1)
add(bell(hz(67), 3.5), mark_t + 0.05, 0.0, 0.07)
for j, m in enumerate([43, 55, 62, 67, 71, 74]):
    add(piano(m, 3.2), mark_t + 0.05 + 0.02 * j, -0.5 + 0.2 * j, 0.045)
for j, m in enumerate([86, 91, 95, 98, 95, 91]):
    add(bell(hz(m), 2.0), TU + j * 0.12, 0.4 * math.sin(j), 0.028)
add(bell(hz(79), 3.0), TU + 1.1, 0.0, 0.045)

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
