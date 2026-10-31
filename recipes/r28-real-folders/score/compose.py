"""
R28 · Real Folders. Original score, composed in code, timed to the film's one table (bake/table.json).

32 s at 108 bpm in A minor, opening to C major as the search finds its matches.
The shutter: a held A minor, a swish as the capture overlay drops in, a riser while the selection drags out, and one
dry double click of a shutter. The flood: a shutter click on every capture, so they become a rhythm as the flood
speeds up, over a kick and a plucked arpeggio; a low swish and a thud as the camera tilts, a soft wooden thock as each
folder rises and each card is filed. Found: a key for each letter, a shimmer as the scan crosses the city, a blip for
the words, a rising chime for each match. Marked up: a marker stroke for the arrow and the box, a pop per badge, and
short bit-crushed blips as the pixels snap in. Client-ready: a warm C major and a ring as the gradient floods in, then
a recording beep, a tick per second and a soft click per frame. The title: a riser as the overlay drags out, and the
last shutter on a C major chord, with bells as the URL types.
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
rng = np.random.default_rng(28)
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






# ---------------------------------------------------------------- Real Folders
overlay, drag, shot0, lift = TB["overlay"], TB["drag"], TB["shot0"], TB["lift"]
shots, tilt, file_, cards, folders = TB["shots"], TB["tilt"], TB["file"], TB["cards"], TB["folders"]
typ, scan, rise, dive = TB["type"], TB["scan"], TB["rise"], TB["dive"]
arrow, box, badges, redact = TB["arrow"], TB["box"], TB["badges"], TB["redact"]
flood_bg, face, rec, frames = TB["flood_bg"], TB["face"], TB["rec"], TB["frames"]
sel, shot1, line = TB["sel"], TB["shot1"], TB["line"]
AM = [45, 52, 57, 60, 64]              # A minor, the desk and the flood
CM = [48, 55, 60, 64, 67, 72]          # C major, from the matches to the logo


def pad(midis, t0, dur, g=0.04, a=0.8):
    for j, m in enumerate(midis):
        add(tone(hz(m), dur, a=a, rel=dur / 2.0, harm=(1, 0.35, 0.15), detune=0.0008), t0, -0.6 + 1.2 * j / max(1, len(midis) - 1), g)


def shutter(t0, g=1.0, pan=0.0):
    # the capture: two dry clicks a breath apart and a small body thump
    for k, (d, f) in enumerate(((0.0, 2600), (0.042, 1900))):
        add(norm(highpass(noise(0.012, a=0.0005, rel=0.008), 2500)), t0 + d, pan, g * (1.0 - 0.35 * k))
        add(tone(f, 0.05, a=0.0005, rel=0.015, harm=(1, 0.4)), t0 + d, pan, g * 0.35)
    add(tone(130, 0.12, a=0.001, rel=0.05, harm=(1, 0.5)), t0, pan, g * 0.5)


def thock(t0, g=1.0, f=180, pan=0.0):
    # a card filed: a soft wooden knock
    add(tone(f, 0.18, a=0.001, rel=0.06, harm=(1, 0.6, 0.2)), t0, pan, g)
    add(norm(lowpass(noise(0.03, a=0.001, rel=0.02), 1500)), t0, pan, g * 0.3)


def crush(f, dur=0.06, bits=3, hold=6):
    # a bit-crushed blip: a square wave, quantised and sampled-and-held
    n = int(dur * SR)
    x = np.sign(np.sin(2 * np.pi * f * np.arange(n) / SR)) * env(n, 0.001, dur * 0.6)
    q = 2 ** bits
    x = np.round(x * q) / q
    return np.repeat(x[::hold], hold)[:n]


# ---- the shutter: a held A minor, the overlay drops in, the selection drags out on a riser, one capture
pad([45, 52, 57], 0.0, T["flood"][0] + 0.6, 0.05, a=0.5)
add(swish(0.4, 300, 5000), overlay - 0.05, 0.0, 0.08)
add(tone(hz(81), 0.5, a=0.003, rel=0.2, harm=(1, 0.3)), overlay, 0.2, 0.03)
for j in range(6):
    add(block(2200 + 300 * hsh(j), 0.25), overlay + 0.12 * j + 0.1, -0.5 + 0.2 * j, 0.012)
add(swish(drag[1] - drag[0] + 0.2, 200, 6000, rise=True), drag[0], 0.0, 0.08)
n = int((drag[1] - drag[0]) * SR)
gl = np.cumsum(hz(57) * (1 + np.linspace(0, 1, n) ** 2)) / SR
add(np.sin(2 * np.pi * gl) * env(n, 0.3, 0.2), drag[0], 0.0, 0.02)
shutter(shot0, 0.3)
add(taiko(55, 1.2), shot0, 0.0, 0.18)
add(bell(hz(76), 1.8), shot0 + 0.02, 0.0, 0.04)
add(swish(lift[1] - lift[0], 400, 7000), lift[0] + 0.1, 0.0, 0.08)

# ---- the flood: a shutter on every capture, a groove underneath, the tilt, the city rising, every card filed
for j, ts in enumerate(shots[1:]):
    shutter(ts, 0.12 + 0.05 * hsh(j), 0.7 * math.sin(j * 1.9))
for b in beats(T["flood"][0], T["search"][0]):
    add(kick(), b, 0.0, 0.12)
for b in beats(T["flood"][0] + BEAT / 2, tilt[0]):
    add(hat(0.6), b, 0.3, 0.025)
arp = [57, 60, 64, 69, 64, 60]
for j, b in enumerate(beats(T["flood"][0], tilt[0], BEAT / 2)):
    add(pluck(hz(arp[j % 6]), 0.6, 0.4), b, 0.4 * math.sin(j), 0.04)
pad(AM, T["flood"][0], T["search"][0] - T["flood"][0] + 0.8, 0.035, a=0.6)
add(swish(tilt[1] - tilt[0] + 0.2, 150, 4000), tilt[0], 0.0, 0.13)
thud(tilt[1], 0.3, 55)
for F in folders:
    thock(F["rise"], 0.08, 110 + 40 * hsh(F["gx"] * 3 + F["gy"]), 0.6 * math.sin(F["rise"] * 9))
for j, C in enumerate(sorted(cards, key=lambda c: c["file"])):
    thock(C["file"] + 0.5, 0.06, 220 + 80 * hsh(j * 1.7), 0.7 * math.sin(j * 2.3))
for b in beats(tilt[1], T["search"][0], BEAT / 2):
    add(hat(0.5), b, -0.3, 0.02)

# ---- found: a key per letter, a scan that shimmers, a blip for each word, a rising chime for each match
pad([53, 57, 60, 64], T["search"][0], dive[0] - T["search"][0] + 0.6, 0.035, a=0.6)
for j in range(7):
    key(typ[0] + (typ[1] - typ[0]) * j / 7, 0.08, 0.5 * math.sin(j * 1.7))
for b in beats(T["search"][0], dive[0]):
    add(kick(), b, 0.0, 0.09)
n = int((scan[1] - scan[0]) * SR)
sh = np.sin(2 * np.pi * hz(88) * np.arange(n) / SR) * (0.5 + 0.5 * np.sin(2 * np.pi * 9 * np.arange(n) / SR)) * env(n, 0.2, 0.4)
add(sh, scan[0], 0.0, 0.012)
add(swish(scan[1] - scan[0], 800, 9000), scan[0], 0.0, 0.05)
for j in range(14):
    tw = scan[0] + (scan[1] - scan[0]) * (j + 0.5) / 14
    add(block(1700 + 600 * hsh(j * 2.2), 0.3), tw, 0.8 * math.sin(j * 1.3), 0.015)
for j, tr_ in enumerate(rise):
    for k, m in enumerate((72, 76, 79)):
        add(bell(hz(m + [0, 4, 7, 12][j]), 1.4), tr_ + 0.05 * k, -0.4 + 0.3 * j, 0.03)
    add(tone(hz(CM[j + 1]), 0.6, a=0.002, rel=0.2, harm=(1, 0.5)), tr_, 0.0, 0.04)
pad(CM[:4], rise[0], dive[0] - rise[0] + 0.5, 0.03, a=0.4)
add(swish(dive[1] - dive[0], 300, 10000, rise=True), dive[0], 0.0, 0.15)

# ---- marked up and redacted: a marker stroke, a pop per badge, bit-crushed blips as the pixels snap in
add(taiko(48, 1.4), T["mark"][0], 0.0, 0.22)
pad([50, 57, 60, 65], T["mark"][0], T["ready"][0] - T["mark"][0] + 0.6, 0.035, a=0.5)
for b in beats(T["mark"][0], T["ready"][0]):
    add(kick(), b, 0.0, 0.11)
for b in beats(T["mark"][0] + BEAT / 2, T["ready"][0]):
    add(hat(0.6), b, 0.3, 0.022)
add(norm(lowpass(highpass(noise(arrow[1] - arrow[0], a=0.02, rel=0.08), 1500), 6000)), arrow[0], -0.3, 0.05)
add(norm(lowpass(highpass(noise(box[1] - box[0], a=0.02, rel=0.08), 1200), 5000)), box[0], 0.3, 0.05)
for j, tb in enumerate(badges):
    add(block(1200 + 300 * j, 0.8), tb, -0.3 + 0.6 * j, 0.06)
    add(pluck(hz([69, 72][j]), 0.6, 0.5), tb, -0.3 + 0.6 * j, 0.05)
cols = 29
for i in range(cols):
    tc = redact[0] + 0.25 + i / cols * (redact[1] - redact[0] - 0.9)
    add(crush(hz(84 - (i % 5) * 3), 0.05, 3, 5), tc, -0.6 + 1.2 * i / cols, 0.03)
add(crush(hz(57), 0.22, 2, 9), redact[1] - 0.6, 0.0, 0.05)

# ---- client-ready: the gradient floods in on a warm C major, then a recording ticks along
add(taiko(48, 1.6), flood_bg[0], 0.0, 0.25)
shing(flood_bg[0] + 0.05, 0.04)
add(swish(flood_bg[1] - flood_bg[0], 300, 6000, rise=True), flood_bg[0], 0.0, 0.08)
strings([48, 55, 60, 64, 67], flood_bg[0], T["title"] - flood_bg[0] + 0.5, 0.07, a=0.7)
for b in beats(flood_bg[0], T["title"]):
    add(kick(), b, 0.0, 0.13)
for b in beats(flood_bg[0] + BEAT / 2, T["title"]):
    add(hat(0.6), b, 0.3, 0.026)
arp2 = [60, 64, 67, 72, 67, 64]
for j, b in enumerate(beats(face[1], T["title"], BEAT / 2)):
    add(pluck(hz(arp2[j % 6]), 0.6, 0.45), b, 0.4 * math.sin(j), 0.04)
add(tone(1000, 0.12, a=0.002, rel=0.04), rec[0], 0.4, 0.05)
add(tone(1000, 0.12, a=0.002, rel=0.04), rec[0] + 0.16, 0.4, 0.05)
for s in range(1, int(rec[1] - rec[0]) + 1):
    add(block(2400, 0.5), rec[0] + s, 0.5, 0.02)
for j, tf in enumerate(frames):
    shutter(tf, 0.05, -0.6 + 1.2 * j / len(frames))

# ---- the title: the city folds away, the overlay drags out on a riser, the last shutter fires on C major
add(swish(0.5, 6000, 200), T["title"], 0.0, 0.1)
add(swish(sel[1] - sel[0] + 0.15, 200, 7000, rise=True), sel[0], 0.0, 0.09)
n = int((shot1 - sel[0]) * SR)
gl = np.cumsum(hz(60) * (1 + np.linspace(0, 1, n) ** 2)) / SR
add(np.sin(2 * np.pi * gl) * env(n, 0.3, 0.1), sel[0], 0.0, 0.02)
shutter(shot1, 0.35)
thud(shot1, 0.35, 55)
add(taiko(44, 1.6), shot1, 0.0, 0.3)
for j, m in enumerate([36, 48, 55, 60, 64, 67]):
    add(tone(hz(m), DUR - shot1, a=0.2, rel=2.4, harm=(1, 0.3, 0.12), detune=0.0007), shot1, -0.6 + 0.24 * j, 0.045)
add(bell(hz(72), 3.5), shot1 + 0.02, 0.0, 0.07)
for j, m in enumerate([48, 55, 60, 64, 67, 72]):
    add(piano(m, 3.2), shot1 + 0.03 + 0.02 * j, -0.5 + 0.2 * j, 0.045)
for j, m in enumerate([84, 88, 91, 96, 91, 88]):
    add(bell(hz(m), 2.0), line + 0.5 + j * 0.12, 0.4 * math.sin(j), 0.026)
add(bell(hz(79), 3.0), line + 1.4, 0.0, 0.045)

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
