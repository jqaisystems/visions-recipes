"""
Original score for R08 · Boiling Line (the Music page), composed in code. MIT, like the rest of this project.

In the spirit of the page's calm tracks: soft piano over an ocean wash, C major, unhurried. A pen scratches
whenever a line is being drawn, at the speed of the drawing. Slow waves of filtered noise swell and break. When
the piano is sketched it starts to play, and its melody is the same NOTES table the drawn keys press on. The
sunset brings warm pads, and the title gets a last soft chord and a tick per letter of the URL.

Picture timings come from the T table and NOTES in index.html (mirrored below).
Usage: py -3.13 score/compose.py  ->  assets/bgm/score.wav   (numpy only, deterministic)
"""
import os
import wave
import numpy as np

SR = 44100
TOTAL = 26.0
N = int(TOTAL * SR)
rng = np.random.default_rng(8)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "bgm", "score.wav")

# ---- picture timings (index.html T table and NOTES)
DRAWS = [(0.4, 1.8), (1.4, 2.6), (2.4, 3.4), (4.0, 4.8), (4.45, 5.25), (4.9, 5.7), (5.35, 6.15), (5.8, 6.6),
         (5.6, 6.6), (9.8, 12.4)]                       # every pen stroke window: horizon, sun, rays, waves, shore, piano
SUNSET, WASH, SEA = (16.0, 21.0), (16.4, 19.6), (17.2, 20.4)
TITLE, SUB, URL = 21.4, 22.2, (22.8, 23.8, 29)
WHITE = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83]   # the 14 drawn white keys, C4 to B5
NOTES = [(12.7, 4), (13.1, 6), (13.5, 7), (13.9, 9), (14.5, 8), (14.9, 7), (15.3, 6), (15.9, 4),
         (16.4, 7), (16.8, 9), (17.2, 11), (17.8, 9), (18.6, 7), (19.4, 4), (20.4, 7)]

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




def ocean(dur, g=1.0, period=6.5):
    """Waves: filtered noise that swells and breaks on a slow cycle, a little different in each ear."""
    n = int(dur * SR); t = t_of(n)
    out = []
    for side in range(2):
        ph = (t / period + 0.17 * side) % 1.0
        swell = np.where(ph < 0.7, (ph / 0.7) ** 2, np.exp(-(ph - 0.7) / 0.09))
        x = lp(hp(rng.standard_normal(n), 120), 900 + 2600 * swell, poles=2)
        out.append(x * (0.25 + 0.75 * swell) * adsr(n, a=1.5, d=10, s=1, rel=1.5) * g)
    return out


# ---- the pen: a scratch while any stroke is drawing
t = np.arange(N) / SR
speed = np.zeros(N)
for a, b in DRAWS:
    u = np.clip((t - a) / (b - a), 0, 1)
    speed = np.maximum(speed, np.where((t > a) & (t < b), np.sin(np.pi * u) ** 0.7, 0))
speed = lp(speed * (0.75 + 0.25 * np.sin(t * 37) ** 2), 25)
add_st(*pencil(speed, g=0.09), 0.0)

# ---- the sea, from the first waves to the end
add_st(*ocean(TOTAL - 3.6, g=0.05), 3.6)

# ---- harmony: a quiet bed, warming at the sunset
C_MAJ9 = [36, 48, 55, 59, 62, 64]; A_MIN9 = [33, 45, 52, 55, 59, 60]; F_MAJ9 = [29, 41, 48, 52, 55, 57]; G_SUS = [31, 43, 50, 55, 57, 60]
plan = [(0.0, C_MAJ9, 6.4), (6.2, A_MIN9, 6.2), (12.2, F_MAJ9, 4.2), (16.2, G_SUS, 3.8), (19.8, C_MAJ9, TOTAL - 19.8)]
for t0, ch, dur in plan:
    warm = 1.25 if t0 >= SUNSET[0] else 1.0
    add_st(*pad(ch, dur + 0.6, g=0.3 * warm, cutoff=900 + 300 * (warm - 1) * 4, a=1.2, rel=1.2), t0)
    add(sub(ch[0] + 12, dur + 0.4, g=0.08), t0)

# a few opening notes while the sun is drawn, before the piano exists
for m, tt in ((64, 2.2), (67, 3.3), (72, 7.4), (71, 8.6)):
    add(piano(m, 0.16, dur=2.6, bright=0.6), tt, pan=-0.2)

# ---- the drawn piano plays: the same notes its keys press
for tn, k in NOTES:
    add(piano(WHITE[k], 0.27, dur=2.4, bright=0.75), tn, pan=-0.35 + 0.05 * k)
    add(piano(WHITE[k] - 12, 0.08, dur=2.0, bright=0.5), tn + 0.01, pan=-0.3)

# ---- sunset and title
add_st(*whoosh(4.0, 2.4, g=0.025, f0=300, f1=1800), SUNSET[0] + 0.4)
add(bell(79, 0.14, dur=3.2), TITLE + 0.1, pan=-0.2)
for m, dt in ((60, 0.0), (64, 0.08), (67, 0.16), (72, 0.26)):
    add(piano(m, 0.17, dur=3.4, bright=0.6), SUB + dt, pan=-0.1 + 0.06 * (m - 60) / 4)
for k in range(0, URL[2], 2):
    add(tick(0.03, f=rng.uniform(2200, 3000)), URL[0] + k * (URL[1] - URL[0]) / URL[2], pan=rng.uniform(-0.2, 0.2))

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
