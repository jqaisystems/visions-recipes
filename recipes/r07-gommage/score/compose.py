"""
Original score for R07 · Gommage (Imagined Worlds, the Stills collection), composed in code. MIT, like the rest of
this project.

An autumn waltz in 3/4 at 78 BPM, D minor turning to F major. A felt piano keeps the waltz (bass on one, soft
chords on two and three) under a sparse melody; string-like pads swell with the dissolve. A breathy wind rises as
the picture comes apart, and a rustle of leaves follows how many leaves are in the air. As they settle into the
new picture the harmony opens to F, and the title lands on a bell.

Picture timings come from the T table in index.html (mirrored below).
Usage: py -3.13 score/compose.py  ->  assets/bgm/score.wav   (numpy only, deterministic)
"""
import os
import wave
import numpy as np

SR = 44100
TOTAL = 26.0
N = int(TOTAL * SR)
rng = np.random.default_rng(7)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "bgm", "score.wav")

# ---- picture timings (index.html T table)
OUT_FRONT = (3.0, 8.6)        # leaves leave image A
LAND = (14.6, 20.6)           # leaves settle into image B
KICKER, TITLE, URL = 21.4, 21.7, (22.6, 23.6, 30)
BAR0, BEAT = 0.3, 60 / 78     # the waltz: bar k starts at BAR0 + 3 * BEAT * k

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


def rustle(env, g=1.0):
    """Leaves in the air: dense dry grains whose amount follows env (0..1 per sample)."""
    out = []
    for _ in range(2):
        x = np.zeros(N)
        tt = 0.0
        while tt < TOTAL:
            e = env[min(N - 1, int(tt * SR))]
            tt += rng.exponential(1.0 / (8 + 900 * e))
            if e < 0.01:
                continue
            gl = int(rng.uniform(0.003, 0.014) * SR); i = int(tt * SR)
            if i + gl >= N:
                break
            x[i:i + gl] += rng.standard_normal(gl) * np.hanning(gl) * rng.uniform(0.2, 1.0)
        out.append(lp(hp(x, 1500), 7500) * env * g)
    return out


def bar(k):
    return BAR0 + 3 * BEAT * k


# chords: (bass, voicing)
DM = (38, [53, 57, 62]); BB = (34, [53, 58, 62]); A7 = (33, [52, 55, 61]); GM = (31, [50, 55, 58])
C = (36, [52, 55, 60]); F = (29, [53, 57, 60]); FMAJ9 = (29, [52, 57, 60, 67])
PLAN = [DM, DM, BB, A7, GM, DM, BB, C, F, FMAJ9, FMAJ9]
# a sparse melody: (bar, beat, midi, length in beats)
MEL = [(0, 0, 69, 3), (1, 0, 67, 1.5), (1, 1.5, 65, 1.5), (2, 0, 65, 2), (2, 2, 62, 1), (3, 0, 64, 3),
       (4, 0, 62, 1.5), (4, 1.5, 65, 1.5), (5, 0, 69, 3), (6, 0, 70, 2), (6, 2, 69, 1), (7, 0, 67, 3),
       (8, 0, 69, 1.5), (8, 1.5, 72, 1.5), (9, 0, 76, 3), (10, 0, 72, 3)]

# ---- the waltz: bass on one, soft chords on two and three
for k, (b, v) in enumerate(PLAN):
    t0 = bar(k)
    if t0 > TOTAL - 1.2:
        break
    soft = 0.75 if 3 <= k <= 6 else 1.0          # the storm thins the accompaniment
    add(piano(b + 12, 0.22 * soft, dur=2.2, bright=0.7), t0, pan=-0.25)
    for beat in (1, 2):
        for j, m in enumerate(v):
            add(piano(m, 0.075 * soft, dur=1.2, bright=0.6), t0 + beat * BEAT + 0.008 * j, pan=0.15 + 0.05 * j)
for (k, beat, m, ln) in MEL:
    add(piano(m + 12, 0.2, dur=max(1.4, ln * BEAT + 0.8)), bar(k) + beat * BEAT, pan=0.05)

# ---- strings: pads that follow the chords and swell with the dissolve and the landing
for k, (b, v) in enumerate(PLAN):
    t0 = bar(k)
    if t0 > TOTAL - 1.0:
        break
    g = 0.26 + (0.12 if 1 <= k <= 3 else 0) + (0.14 if 6 <= k <= 8 else 0)
    add_st(*liquid_pad([b + 12] + v, min(3 * BEAT + 0.6, TOTAL - t0), g=g, cutoff=1300, wob=0.06, a=0.5, rel=0.6), t0 - 0.05)
    add(sub(b + 12 if b < 36 else b, min(3 * BEAT, TOTAL - t0), g=0.09), t0)

# ---- wind and leaves, from the same fronts as the picture
t = np.arange(N) / SR
born = np.clip((t - OUT_FRONT[0]) / (OUT_FRONT[1] - OUT_FRONT[0]), 0, 1)
landed = np.clip((t - LAND[0]) / (LAND[1] - LAND[0]), 0, 1)
air = np.clip(born - landed, 0, 1)
gust = np.exp(-((t - 6.2) / 2.6) ** 2) + 0.5 * np.exp(-((t - 17.0) / 2.4) ** 2)
add_st(*rustle(lp(air * (0.35 + 0.65 * gust), 4), g=0.07), 0.0)
add_st(*whoosh(9.0, 3.6, g=0.05, f0=250, f1=2600), OUT_FRONT[0] - 0.5)
add_st(*whoosh(7.5, 3.2, g=0.035, f0=300, f1=2200), LAND[0] - 1.5)

# ---- lockup: the title lands on a bell; ticks for the URL; the last F rings out
add(bell(77, 0.2, dur=3.4), TITLE + 0.1, pan=-0.2)
add(bell(81, 0.12, dur=3.0), TITLE + 0.5, pan=0.2)
for k in range(0, URL[2], 2):
    add(tick(0.03, f=rng.uniform(2200, 3000)), URL[0] + k * (URL[1] - URL[0]) / URL[2], pan=rng.uniform(-0.2, 0.2))
add_st(*liquid_pad([41, 53, 57, 60, 64, 69], TOTAL - 22.5, g=0.34, cutoff=1400, wob=0.03, a=1.2, rel=1.6), 22.5)

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
