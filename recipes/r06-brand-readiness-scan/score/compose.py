"""
Original score for R06 · Brand Readiness Scan (the Brand Readiness Check), composed in code. MIT, like the rest of
this project.

A minor turning to C major, calm and precise. A low scanner drone wakes with the teal line and a filtered sweep
follows it across the card. Each of the eight checks gets a clean two-note blip as its feature lights and a soft
tick when it is ticked off, climbing an A minor pentatonic; a few checks carry their own small sound (anchor
clicks for the vector files, a lift for the last). The band scale steps the harmony up four times, and the
headline resolves on C with a bell.

Picture timings come from the T table in index.html (mirrored below).
Usage: py -3.13 score/compose.py  ->  assets/bgm/score.wav   (numpy only, deterministic)
"""
import os
import wave
import numpy as np

SR = 44100
TOTAL = 26.0
N = int(TOTAL * SR)
rng = np.random.default_rng(6)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "bgm", "score.wav")

# ---- picture timings (index.html T table)
WAKE, OUTLINE, SWEEP, LIST = (0.3, 1.4), (0.8, 2.0), (2.2, 5.6), (4.8, 5.6)
CHECKS = (6.4, 1.55, 8)
BANDS, BANDS_IN, DIM = (19.0, 21.4), (18.7, 19.2), (21.6, 22.4)
MARK, TITLE, SUB, URL = 22.3, 22.6, 23.4, (24.0, 25.0, 37)

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


def drone(m, dur, g=1.0, open_t=1.0):
    """The scanner: a low hum whose filter opens as it wakes, with a slow beating fifth."""
    n = int(dur * SR); t = t_of(n)
    x = saw(hz(m), n, harmonics=10) + 0.6 * saw(hz(m + 7) * 1.002, n, harmonics=8)
    cut = 180 + 900 * np.minimum(t / open_t, 1) ** 2
    return lp_var(lp_var(x, cut), cut) * adsr(n, a=0.4, d=10, s=1, rel=1.0) * g


def scan_sweep(dur, g=1.0, f0=600, f1=5200):
    """The line crossing the card: filtered noise whose brightness follows the line."""
    n = int(dur * SR); t = t_of(n); u = t / dur
    e = np.sin(np.pi * u) ** 0.8
    out = []
    for _ in range(2):
        out.append(lp(hp(rng.standard_normal(n), 400), f0 + (f1 - f0) * (0.5 - 0.5 * np.cos(np.pi * u)), poles=2) * e * g)
    return out


def blip2(m, g=1.0):
    """A feature found: two quick clean notes, the second a fifth up."""
    a = np.zeros(int(0.5 * SR))
    for k, (mm, dt) in enumerate(((m, 0.0), (m + 7, 0.07))):
        n = int(0.4 * SR); t = t_of(n)
        x = np.sin(2 * np.pi * hz(mm) * t) * np.exp(-t / 0.09) * adsr(n, a=0.002, d=10, s=1, rel=0.05)
        i = int(dt * SR); a[i:i + n] += x[: len(a) - i]
    return a * g


A_MIN9 = [33, 45, 52, 55, 59, 64]
F_MAJ7 = [41, 48, 53, 57, 60, 64]
G_ADD9 = [43, 50, 55, 57, 59, 62]
C_END = [36, 48, 52, 55, 60, 64, 67]
PENT = [69, 72, 74, 76, 79, 81, 84, 86]          # A minor pentatonic, one note per check

# ---- 0-6.4: the scanner wakes and crosses the card
dr = drone(33, 6.8, 0.12, open_t=2.0)
add_st(dr, dr, 0.2, width=0.4)
dr = drone(33, BANDS[1] - CHECKS[0] + 0.6, 0.06, open_t=0.5)
add_st(dr, dr, CHECKS[0] - 0.4, width=0.4)          # the scanner keeps humming under the checks
add_st(*pad(A_MIN9, 6.8, g=0.32, cutoff=900, a=1.6, rel=1.2), 0.4)
add(bell(81, 0.12, dur=2.0), WAKE[0] + 0.3, pan=-0.5)
add_st(*scan_sweep(SWEEP[1] - SWEEP[0] + 0.3, g=0.05), SWEEP[0] - 0.1)
add(thock(0.12), SWEEP[1])
add(piano(64, 0.18, dur=2.0), LIST[0] + 0.3, pan=0.4)

# ---- 6.4-19: eight checks. A blip as each feature lights, a tick as it is ticked off
chords = [(A_MIN9, 33), (F_MAJ7, 41), (G_ADD9, 43), (A_MIN9, 45)]
seg = CHECKS[1] * 2
for k in range(4):
    ch, root = chords[k]
    add_st(*pad(ch, seg + 0.8, g=0.44, cutoff=1100 + 120 * k, a=0.5, rel=0.8), CHECKS[0] - 0.2 + k * seg)
    add(sub(root + 12 if root < 36 else root, seg + 0.6, g=0.12), CHECKS[0] - 0.2 + k * seg)
for i in range(CHECKS[2]):
    t0 = CHECKS[0] + i * CHECKS[1]
    add(blip2(PENT[i], 0.13), t0 + 0.4, pan=-0.3 + 0.08 * i)
    add(tick(0.06, f=3200), t0 + CHECKS[1] * 0.45 + CHECKS[1] - 0.02, pan=0.5)   # the list ticks as the check ends
    add_st(*scan_sweep(0.45, g=0.022, f0=900, f1=3400), t0)                      # the scanner moving to the feature
# check 5 (files): little clicks as the anchor points appear
for k in range(12):
    add(tick(0.03, f=4200), CHECKS[0] + 4 * CHECKS[1] + 0.25 + k * 0.045, pan=-0.4 + 0.07 * k)
# check 8 (pride): a lift
add_st(*whoosh(1.2, 0.6, g=0.04, f0=400, f1=3600), CHECKS[0] + 7 * CHECKS[1] + 0.1)

# ---- 18.7-21.6: the band scale, four steps up
add_st(*pad([45, 52, 57, 60, 64], BANDS[1] - BANDS_IN[0] + 0.6, g=0.34, cutoff=1300, a=0.4, rel=0.6), BANDS_IN[0])
for k, (m, ch) in enumerate(((57, [45, 57, 60, 64]), (60, [48, 60, 64, 67]), (64, [52, 59, 64, 67]), (67, [55, 62, 67, 71]))):
    tb = BANDS[0] + (k / 4) * (BANDS[1] - BANDS[0]) + 0.15
    add(piano(m + 12, 0.22, dur=1.6), tb, pan=-0.45 + 0.3 * k)
    add_st(*pad(ch, 0.9, g=0.34, cutoff=1500, a=0.08, rel=0.5), tb)

# ---- lockup: resolve on C, a bell for the mark, the headline, ticks for the URL
add_st(*pad(C_END, TOTAL - DIM[0] + 0.2, g=0.52, cutoff=1500, a=1.0, rel=1.8), DIM[0] - 0.2)
add(sub(36, TOTAL - DIM[0], g=0.18), DIM[0])
add(bell(79, 0.22, dur=3.2), MARK, pan=-0.1)
add(piano(64, 0.24, dur=2.6), TITLE + 0.1, pan=-0.2)
add(piano(67, 0.22, dur=2.6), TITLE + 0.45, pan=0.2)
add(piano(72, 0.18, dur=2.4), SUB, pan=0.0)
for k in range(0, URL[2], 2):
    add(tick(0.035, f=rng.uniform(2200, 3000)), URL[0] + k * (URL[1] - URL[0]) / URL[2], pan=rng.uniform(-0.2, 0.2))

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
