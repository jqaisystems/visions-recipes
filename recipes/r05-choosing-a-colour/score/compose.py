"""
Original score for R05 · Choosing a Colour (How to Choose Brand Colours), composed in code. MIT, like the rest of
this project.

D major, slow and liquid. Every colour at once is a wide, wavering pad full of water drops. As the adjectives
arrive the drops thin out and the harmony narrows; the competitor scan is a soft blip for each dot, the same
note again and again, with one higher note left for the gap. The primary pools on a low swell, its code ticks in,
and each swatch locks with a chime that climbs the chord. The tests get light plucks, and the title resolves on D
with a bell.

Picture timings come from the T table in index.html (mirrored below).
Usage: py -3.13 score/compose.py  ->  assets/bgm/score.wav   (numpy only, deterministic)
"""
import os
import wave
import numpy as np

SR = 44100
TOTAL = 26.0
N = int(TOTAL * SR)
rng = np.random.default_rng(5)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "bgm", "score.wav")

# ---- picture timings (index.html T table)
OPEN = (0.5, 2.6, 37)
S1, WORDS, DRAIN = 4.2, (4.7, 0.35), (5.6, 7.8)
S2, DOTS, GAP, DOTS_OUT = 8.2, (8.6, 0.09, 12), 10.6, 12.0
S3, POOL, CODE = 12.2, (12.4, 15.0), (14.0, 14.8, 7)
S4, BANDS, LABELS = 16.2, (16.3, 18.8), (17.6, 0.25, 4)
S5, FADE, TESTS = 20.2, (20.0, 20.7), (20.5, 0.18, 5)
MARK, TITLE, URL = 23.3, 23.6, (24.4, 25.2, 22)

L = np.zeros(N)
R = np.zeros(N)
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


def paper(dur, g=1.0, lo=500, hi=6500, grains=900):
    """Paper texture: dense tiny grains of band-limited noise, the crackle of a sheet being handled."""
    n = int(dur * SR)
    out = np.zeros(n)
    for _ in range(int(grains * dur)):
        gl = int(rng.uniform(0.002, 0.012) * SR)
        i = int(rng.uniform(0, 1) * max(1, n - gl))
        out[i:i + gl] += rng.standard_normal(gl) * np.hanning(gl) * rng.uniform(0.2, 1.0)
    return lp(hp(out, lo), hi) * g




def piano(m, g=1.0, dur=1.8, bright=1.0):
    """A soft felt piano note: slightly stretched partials, a quick hammer, a long gentle decay."""
    n = int(dur * SR); t = t_of(n); f = hz(m)
    x = np.zeros(n)
    for h in range(1, 8):
        fh = f * h * (1 + 0.0004 * h * h)
        if fh > SR / 2.2:
            break
        x += np.sin(2 * np.pi * fh * t) * (0.6 ** (h - 1)) * bright ** (h - 1) * np.exp(-t * (1.6 + 0.9 * h))
    hammer = lp(rng.standard_normal(n), 2500) * np.exp(-t / 0.004) * 0.05
    return (x + hammer) * adsr(n, a=0.002, d=10, s=1, rel=0.3) * g * 0.6


def pencil(speed, g=1.0):
    """Graphite on paper. `speed` is the line's speed per sample (0..1): it sets loudness and brightness, and a
    rough grain texture rides on top so it never sounds like plain hiss."""
    n = len(speed)
    out = []
    for _ in range(2):
        x = hp(rng.standard_normal(n), 900)
        grain = lp(np.abs(rng.standard_normal(n)), 60) * 2.2              # the paper's tooth
        cut = 1800 + 5200 * speed
        out.append(lp_var(x * (0.55 + 0.45 * grain), cut, block=128) * speed ** 0.8 * g)
    return out




def drop(m, g=1.0):
    """A water drop: a sine that bends upward fast, with a tiny splash."""
    n = int(0.25 * SR); t = t_of(n)
    f = hz(m) * (1 + 0.9 * (1 - np.exp(-t / 0.018)))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.05)
    splash = hp(rng.standard_normal(n), 3000) * np.exp(-t / 0.006) * 0.08
    return (x + splash) * adsr(n, a=0.001, d=10, s=1, rel=0.05) * g


def liquid_pad(midis, dur, g=1.0, cutoff=1200, wob=0.18, a=0.8, rel=1.2):
    """A pad whose pitch wavers slowly, like light through water. wob in semitones."""
    n = int(dur * SR); t = t_of(n)
    out = []
    for side, det in enumerate((-0.07, 0.07)):
        x = np.zeros(n)
        for k, m in enumerate(midis):
            lfo = wob * np.sin(2 * np.pi * (0.21 + 0.05 * k + 0.03 * side) * t + k)
            f = hz(m + det) * 2 ** (lfo / 12)
            ph = 2 * np.pi * np.cumsum(f) / SR
            x += sum(np.sin(ph * h) / h for h in range(1, 7))
        out.append(lp(x, cutoff, poles=2) * adsr(n, a=a, d=10, s=1, rel=rel) * g / len(midis))
    return out


def chime(m, g=1.0):
    return bell(m, g, dur=2.2) + piano(m + 12, g * 0.35, dur=2.2)


D_ADD9 = [38, 50, 57, 62, 64, 66]
B_MIN9 = [35, 50, 54, 57, 61]
G_MAJ7 = [43, 50, 55, 59, 62, 66]
A_SUS = [45, 52, 57, 62, 64]
D_END = [38, 50, 54, 57, 62, 66, 69]
D_SCALE = [62, 64, 66, 69, 71, 74, 76, 78, 81]

# ---- 0-4.2: every colour at once. A wide wavering pad, water drops everywhere, the line types softly
add_st(*liquid_pad(D_ADD9 + [69, 71], 5.2, g=0.42, cutoff=1700, wob=0.35, a=1.0), 0.0)
add(sub(38, 5.0, g=0.13), 0.0)
add_st(*whoosh(4.6, 2.4, g=0.03, f0=300, f1=2400), 0.0)
tt = 0.15
while tt < S1 + 0.6:
    add(drop(rng.choice(D_SCALE) + 12, rng.uniform(0.05, 0.11)), tt, pan=rng.uniform(-0.7, 0.7))
    tt += rng.exponential(0.11)
for k in range(0, OPEN[2], 2):
    add(tick(0.035, f=rng.uniform(2000, 2800)), OPEN[0] + k * (OPEN[1] - OPEN[0]) / OPEN[2], pan=0.1)

# ---- 4.2-8.2: 01 personality. Three words, three notes; the drops thin out as the colours drain
add_st(*liquid_pad([50, 57, 62, 66], 4.6, g=0.38, cutoff=1300, wob=0.12, a=0.6), S1 - 0.2)
add(sub(38, 4.4, g=0.12), S1 - 0.2)
for i, m in enumerate((66, 69, 74)):
    add(piano(m, 0.26, dur=2.4), WORDS[0] + i * WORDS[1] + 0.1, pan=-0.3 + 0.3 * i)
tt = S1
while tt < DRAIN[1]:
    u = (tt - S1) / (DRAIN[1] - S1)
    add(drop(rng.choice(D_SCALE) + 12, 0.07 * (1 - u) + 0.02), tt, pan=rng.uniform(-0.6, 0.6))
    tt += rng.exponential(0.12 + 0.5 * u)
add_st(*whoosh(DRAIN[1] - DRAIN[0], 1.2, g=0.035, f0=2400, f1=600), DRAIN[0])

# ---- 8.2-12.2: 02 competitors. The same note for nearly every dot; the gap gets a different one
add_st(*liquid_pad(B_MIN9, 4.6, g=0.36, cutoff=1100, wob=0.08, a=0.5), S2 - 0.2)
add(sub(35, 4.4, g=0.13), S2 - 0.2)
for i in range(DOTS[2]):
    m = 69 if i not in (9, 10) else (71 if i == 9 else 66)      # the green and the red stray a little
    add(piano(m, 0.12, dur=0.8, bright=0.7), DOTS[0] + i * DOTS[1], pan=float(np.sin(i)) * 0.5)
add(chime(76, 0.16), GAP, pan=-0.4)
add_st(*whoosh(0.8, 0.5, g=0.03, f0=600, f1=2600), DOTS_OUT - 0.3)

# ---- 12.2-16.2: 03 primary. The ink settles into one pool on a low swell; the code ticks in
add_st(*liquid_pad(G_MAJ7, 4.6, g=0.42, cutoff=1200, wob=0.05, a=1.2), S3 - 0.3)
add(sub(43, 4.4, g=0.16), S3 - 0.2)
add_st(*whoosh(POOL[1] - POOL[0] + 0.4, 1.8, g=0.04, f0=200, f1=1400), POOL[0])
add(piano(62, 0.22, dur=3.0), POOL[0] + 0.2, pan=-0.2)
add(piano(74, 0.2, dur=3.0), POOL[1] - 0.4, pan=-0.3)
for k in range(CODE[2]):
    add(tick(0.05, f=2600 + 120 * k), CODE[0] + k * (CODE[1] - CODE[0]) / CODE[2], pan=0.3)

# ---- 16.2-20.2: 04 supporting. The swatches pour down; one chime per swatch, climbing the chord
add_st(*liquid_pad(A_SUS, 4.4, g=0.42, cutoff=1400, wob=0.04, a=0.6), S4 - 0.2)
add(sub(45, 4.2, g=0.15), S4 - 0.2)
add_st(*whoosh(BANDS[1] - BANDS[0], 1.4, g=0.035, f0=500, f1=3000), BANDS[0])
for i, m in enumerate((69, 73, 76, 81)):
    add(chime(m, 0.17), LABELS[0] + i * LABELS[1], pan=-0.6 + 0.4 * i)

# ---- 20.2-23: 05 test. The page turns light; one pluck per layout
add_st(*whoosh(0.9, 0.5, g=0.035, f0=800, f1=4000), FADE[0])
add_st(*pad([50, 57, 62, 66, 69], 3.4, g=0.38, cutoff=1500, a=0.5, rel=0.8), S5 - 0.2)
for i, m in enumerate((74, 78, 81, 78, 86)):
    add(piano(m, 0.16, dur=1.4), TESTS[0] + i * TESTS[1] + 0.05, pan=-0.6 + 0.3 * i)

# ---- lockup: resolve on D, a bell for the mark, two notes for the title, ticks for the URL
add_st(*liquid_pad(D_END, TOTAL - MARK + 0.4, g=0.5, cutoff=1500, wob=0.03, a=1.0, rel=1.8), MARK - 0.4)
add(sub(38, TOTAL - MARK, g=0.18), MARK - 0.3)
add(bell(74, 0.22, dur=3.2), MARK, pan=-0.1)
add(piano(66, 0.24, dur=2.6), TITLE + 0.1, pan=-0.2)
add(piano(69, 0.22, dur=2.6), TITLE + 0.45, pan=0.2)
for k in range(0, URL[2], 2):
    add(tick(0.04, f=rng.uniform(2200, 3000)), URL[0] + k * (URL[1] - URL[0]) / URL[2], pan=rng.uniform(-0.2, 0.2))
add(drop(86, 0.12), URL[1] + 0.2, pan=0.2)

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
