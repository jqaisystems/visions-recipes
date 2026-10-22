"""
Original score for R09 · Aurora in ASCII (the Recipes library), composed in code. MIT, like the rest of this project.

A night at a terminal, A minor. Every typed character is a soft key click and the command runs with a thock and
a low boot tone. While the cells switch on, a fine digital crackle follows them. A slow analog-style pad
(two detuned saws through a lowpass) rises with the aurora, and a shimmering arpeggio climbs as it brightens.
When the cells shrink, a low hum swells and the arpeggio's filter opens to its smoothest, then both settle as
the cells grow back. The title's cells crackle on, a bell chord lands on "Recipes", and the subtitle and url
type in with the same clicks.

Picture timings come from the T table in index.html (mirrored below).
Usage: py -3.13 score/compose.py  ->  assets/bgm/score.wav   (numpy only, deterministic)
"""
import os
import wave
import numpy as np

SR = 44100
TOTAL = 26.0
N = int(TOTAL * SR)
rng = np.random.default_rng(9)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "bgm", "score.wav")

# ---- picture timings (index.html T table)
CMD, SUBT, URLT = "render aurora --ascii", "films, prompts and source", "visions.joaoqueiros.com/recipes"
TYPE, ENTER = (0.8, 2.6), 2.9
REVEAL = (3.3, 3.0)
RISE, BRIGHT, SHRINK = (3.6, 10.0), (10.0, 15.0), (15.0, 17.0, 19.0)
DIM, TITLE = (19.2, 21.0), (19.6, 2.0)
SUB, URL = (22.0, 23.0), (22.8, 24.0)

L = np.zeros(N)
R = np.zeros(N)
TAIL = int(0.012 * SR)
PEAK = 0.87
TAIL = int(0.012 * SR)
PEAK = 0.87


def t_of(n):
    return np.arange(n) / SR


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def add(sig, start, pan=0.0, g=1.0):
    """Place a mono signal. Every signal gets a 12 ms tail fade so nothing is cut while sounding."""
    sig = np.asarray(sig, dtype=float) * g
    if len(sig) > TAIL:
        sig = sig.copy()
        sig[-TAIL:] *= np.linspace(1, 0, TAIL)
    i = int(round(start * SR))
    if i < 0:
        sig, i = sig[-i:], 0
    if i >= N:
        return
    sig = sig[: N - i]
    L[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 - pan))
    R[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 + pan))


def add_st(l, r, start, g=1.0, width=0.9):
    add(l, start, pan=-width, g=g)
    add(r, start, pan=width, g=g)


def adsr(n, a=0.005, d=0.1, s=0.0, rel=0.05):
    t = t_of(n)
    e = np.clip(t / a, 0, 1) * (s + (1 - s) * np.exp(-np.maximum(t - a, 0) / max(d, 1e-4)))
    return e * np.clip((n / SR - t) / rel, 0, 1)


def lp_var(x, cut, block=256):
    """One-pole lowpass whose cutoff (Hz, per sample) may move; evaluated per block."""
    cut = np.broadcast_to(np.asarray(cut, dtype=float), x.shape)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(0, len(x), block):
        seg = x[i:i + block]
        a = np.exp(-2 * np.pi * cut[i] / SR)
        k = np.arange(len(seg))
        ys = (1 - a) * np.convolve(seg, a ** k)[:len(seg)] + acc * a * (a ** k)
        y[i:i + len(seg)] = ys
        acc = ys[-1]
    return y


def lp(x, f, poles=1):
    for _ in range(poles):
        x = lp_var(x, f)
    return x


def hp(x, f):
    return x - lp_var(x, f)


def saw(freq, n, harmonics=12):
    t = t_of(n)
    out = np.zeros(n)
    for h in range(1, harmonics + 1):
        if freq * h > SR / 2.2:
            break
        out += np.sin(2 * np.pi * freq * h * t) / h
    return out * (2 / np.pi)


def glide(f0, f1, n, shape=1.0):
    u = np.linspace(0, 1, n) ** shape
    return np.sin(2 * np.pi * np.cumsum(f0 * (f1 / f0) ** u) / SR)


def tick(g=1.0, f=2400):
    n = int(0.04 * SR); t = t_of(n)
    return np.sin(2 * np.pi * f * t) * adsr(n, a=0.0005, d=0.006, rel=0.01) * g


def thock(g=1.0):
    n = int(0.22 * SR); t = t_of(n)
    x = np.sin(2 * np.pi * 170 * t) * np.exp(-t / 0.045) + 0.3 * lp(rng.standard_normal(n), 1500) * np.exp(-t / 0.02)
    return x * adsr(n, a=0.001, d=10, s=1, rel=0.06) * g


def bell(m, g=1.0, dur=2.4):
    n = int(dur * SR); t = t_of(n); f = hz(m)
    x = np.zeros(n)
    for ratio, amp, dec in ((1, 1, 1.2), (2.0, 0.45, 0.7), (3.01, 0.25, 0.45), (4.18, 0.14, 0.3), (5.43, 0.08, 0.2)):
        x += amp * np.sin(2 * np.pi * f * ratio * t) * np.exp(-t / dec)
    return x * adsr(n, a=0.003, d=10, s=1, rel=0.4) * g * 0.5


def pad(midis, dur, g=1.0, cutoff=1400, a=0.45, rel=0.9):
    n = int(dur * SR)
    out = []
    for det in (-0.08, 0.08):
        x = np.zeros(n)
        for m in midis:
            x += saw(hz(m + det), n, harmonics=9)
        out.append(lp(x, cutoff, poles=2) * adsr(n, a=a, d=10, s=1, rel=rel) * g / len(midis))
    return out


def bass(m, dur, g=1.0):
    n = int(dur * SR)
    x = saw(hz(m), n, harmonics=10) + 0.7 * np.sin(2 * np.pi * hz(m - 12) * t_of(n))
    return lp(x, 480) * adsr(n, a=0.004, d=0.2, s=0.4, rel=0.04) * g


def sub(m, dur, g=1.0):
    n = int(dur * SR)
    return np.sin(2 * np.pi * hz(m) * t_of(n)) * adsr(n, a=dur * 0.5, d=10, s=1, rel=dur * 0.4) * g

def whoosh(dur, peak, g=1.0, f0=400, f1=5000):
    """Air moving past the camera: a bell-shaped swell whose brightness follows its level."""
    n = int(dur * SR); t = t_of(n)
    e = np.where(t < peak, (t / peak) ** 2, np.exp(-((t - peak) / (0.38 * (dur - peak))) ** 2))
    e *= np.clip((dur - t) / 0.1, 0, 1)
    out = []
    for _ in range(2):
        x = rng.standard_normal(n)
        out.append(lp(hp(x, 180), f0 + (f1 - f0) * e, poles=2) * e * g)
    return out



def lin(t, a, b):
    return np.clip((np.asarray(t, dtype=float) - a) / (b - a), 0, 1)


def ease(x):
    return x * x * (3 - 2 * x)


def cell_scale(t):
    """The grid's cell scale, as in index.html: 1, down to 0.25 at the middle of the shrink, back to 1."""
    a, m, b = SHRINK
    t = np.asarray(t, dtype=float)
    u = np.where(t < m, ease(lin(t, a, m)), 1 - ease(lin(t, m, b)))
    return np.where((t <= a) | (t >= b), 1.0, 1 - 0.75 * u)


def char_times(text, a, b):
    """When each character of a typed line appears (the painter rounds the typed count)."""
    n = len(text)
    return [(a + (k - 0.5) / n * (b - a), ch) for k, ch in enumerate(text, 1)]


def key(g=1.0):
    """A soft keyboard click: a short bright noise snap over a small low knock."""
    n = int(0.06 * SR); t = t_of(n)
    snap = hp(lp(rng.standard_normal(n), rng.uniform(3500, 5200)), 900) * np.exp(-t / 0.004)
    knock = np.sin(2 * np.pi * rng.uniform(180, 230) * t) * np.exp(-t / 0.018) * 0.5
    return (snap + knock) * adsr(n, a=0.0003, d=10, s=1, rel=0.01) * g


def blip(g=1.0):
    """One cell switching on: a few milliseconds of a high sine, like a CRT pixel catching."""
    n = int(rng.uniform(0.003, 0.009) * SR); t = t_of(n)
    return np.sin(2 * np.pi * rng.uniform(1800, 6200) * t) * np.hanning(n) * g


def pluck(m, g=1.0, cut=2000, dur=0.9):
    n = int(dur * SR); t = t_of(n)
    x = saw(hz(m), n, harmonics=10) + 0.4 * saw(hz(m) * 1.004, n, harmonics=10)
    return lp(x, cut, poles=2) * adsr(n, a=0.004, d=0.22, s=0.0, rel=0.1) * g


# ---- the terminal: one click per typed character, then the command runs
for tt, ch in char_times(CMD, *TYPE):
    add(key(0.42 if ch != " " else 0.25), tt, pan=rng.uniform(-0.15, 0.15))
add(thock(0.9), ENTER)
n = int(1.4 * SR); tb = t_of(n)
add(glide(110, 220, n, 0.6) * np.exp(-tb / 0.5) * adsr(n, a=0.02, d=10, s=1, rel=0.3), ENTER + 0.05, g=0.22)

# ---- cells switching on: a crackle that follows the reveal, and again for the title's cells
for start, span, rate, g in ((REVEAL[0], REVEAL[1] + 0.4, 85, 0.16), (TITLE[0], TITLE[1] + 0.3, 45, 0.13)):
    for _ in range(int(rate * span)):
        u = rng.uniform(0, 1)
        add(blip(g * (0.4 + 0.6 * np.sin(np.pi * u))), start + u * span, pan=rng.uniform(-0.8, 0.8))

# ---- harmony: Am, Fmaj7, Dm9 through the shrink, Am(add9) under the title
CHORDS = [(3.4, 10.4, [57, 60, 64, 69], 45), (9.8, 15.6, [53, 57, 60, 64], 41),
          (15.0, 19.9, [50, 57, 60, 64, 65], 38), (19.3, 26.0, [57, 64, 69, 71, 72], 45)]
for i, (a, b, notes, root) in enumerate(CHORDS):
    l, r = pad(notes, b - a, g=0.32 if i else 0.26, cutoff=900 + 300 * i, a=1.8 if i == 0 else 0.7, rel=1.2)
    add_st(l, r, a)
    add(sub(root - 12, b - a, g=0.32), a)

# ---- the arpeggio: shimmers in with the aurora, climbs as it brightens, opens wide while the cells are tiny
ARP_STEP = 0.15
PATTERN = [0, 1, 2, 3, 4, 3, 2, 1]
t = 5.4
k = 0
while t < 19.6:
    chord = next(c for c in reversed(CHORDS) if c[0] <= t + 0.3)
    tones = sorted(set(chord[2] + [m + 12 for m in chord[2]]))[:5]
    m = tones[PATTERN[k % len(PATTERN)] % len(tones)] + 12
    rise = float(ease(lin(t, RISE[0], RISE[1])))
    bright = float(ease(lin(t, BRIGHT[0], BRIGHT[0] + 2)))
    small = float(1 - cell_scale(t)) / 0.75
    g = (0.05 + 0.13 * rise + 0.06 * bright + 0.05 * small) * (1 - float(lin(t, 18.6, 19.6)))
    cut = 1100 + 1500 * rise + 1000 * bright + 2500 * small
    pan = 0.45 * np.sin(k * 0.9)
    x = pluck(m, g, cut)
    add(x, t, pan=pan)
    add(x, t + 0.3, pan=-pan, g=0.4)                 # ping-pong echoes
    add(x, t + 0.6, pan=pan, g=0.18)
    t += ARP_STEP
    k += 1

# ---- the shrink: a low hum swells as the cells get small, and a soft air sweep on the way back
a, mid, b = SHRINK
n = int((b - a + 0.6) * SR); th = t_of(n) + a
env = (1 - cell_scale(th)) / 0.75
hum = lp(saw(hz(33), n, harmonics=14) + 0.5 * saw(hz(45.07), n, harmonics=10), 150 + 650 * env, poles=2) * env ** 1.3
add(hum, a, g=0.5)
l, r = whoosh(2.6, 1.6, g=0.16, f0=300, f1=3800)
add_st(l, r, mid - 0.2, width=0.6)

# ---- title: a bell chord as "Recipes" settles, then the subtitle and url type in
for i, m in enumerate([69, 72, 76, 81]):
    add(bell(m, 0.36, dur=4.0), TITLE[0] + TITLE[1] + 0.05 * i, pan=-0.3 + 0.2 * i)
for line, (a, b), g in ((SUBT, SUB, 0.3), (URLT, URL, 0.24)):
    for tt, ch in char_times(line, a, b):
        add(key(g if ch != " " else g * 0.6), tt, pan=rng.uniform(-0.2, 0.2))

# ---- master: small room, gentle saturation, fade
mix = np.stack([L, R])


def fft_convolve(x, h):
    n = len(x) + len(h) - 1
    m = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(h, m), m)[:n]


ir_n = int(1.3 * SR)
ir = lp(rng.standard_normal(ir_n) * np.exp(-t_of(ir_n) / 0.4), 4500)
ir /= np.sqrt(np.sum(ir ** 2))
mix = mix + 0.2 * np.stack([fft_convolve(mix[0], ir)[:N], fft_convolve(mix[1], -ir)[:N]])
fade = np.ones(N)
fn = int(1.6 * SR)
fade[-fn:] = np.linspace(1, 0, fn) ** 2
mix = np.tanh(mix * fade * 1.1) / np.tanh(1.1)
mix /= np.max(np.abs(mix)) / PEAK   # PEAK sets the level: the WAV is mastered hot; the <audio> data-volume sets the final level

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with wave.open(OUT, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix.T * 32767).astype("<i2").tobytes())
print("wrote", os.path.normpath(OUT), round(TOTAL, 2), "s")
