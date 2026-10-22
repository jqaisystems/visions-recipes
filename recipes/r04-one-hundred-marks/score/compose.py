"""
Original score for R04 · One Hundred Marks, One Line (Marks, the book), composed in code. MIT, like the rest of
this project.

G major, unhurried. A pencil on paper is the lead instrument: its scratch follows the line's speed, frame by
frame. Each mark the line lands on gets one soft piano note, climbing a G major arpeggio as the pace quickens, so
the fast middle becomes a shimmer. Under it, warm pads move G, Em9, Cmaj9, D. The line opens into the JQ mark on
a G major chord, a bell for "Marks", two notes for the line under it and a tick per letter of the URL.

Picture timings come from the T table in index.html (mirrored below, including the chain's tempo curve).
Usage: py -3.13 score/compose.py  ->  assets/bgm/score.wav   (numpy only, deterministic)
"""
import json
import os
import wave
import numpy as np

SR = 44100
TOTAL = 26.0
N = int(TOTAL * SR)
rng = np.random.default_rng(4)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "bgm", "score.wav")

# ---- picture timings (index.html T table)
DRAW = (0.4, 2.5)
FIRST = (2.7, 4.4)
CHAIN = (6.0, 19.4)
END = (19.6, 21.4)
FILL = (21.1, 22.1)
WORD, SUBLINE, URL = 22.2, 23.0, (23.6, 24.6, 21)
# how many outlines the line flows through: read from the same assets/outlines.js the film uses
with open(os.path.join(HERE, "..", "assets", "outlines.js"), encoding="utf-8") as f:
    MARKS = len(json.loads(f.read().split("window.OUTLINES = ", 1)[1].strip().rstrip(";"))["marks"])
MOVE = 0.72                 # each step moves for 72% of its time, then rests

# the chain's tempo, exactly as the painter computes it
steps = MARKS - 1
raw = np.array([0.06 + 0.5 * (1 - u / 0.8) ** 2.4 if u < 0.8 else 0.06 + 0.28 * ((u - 0.8) / 0.2) ** 2
                for u in np.arange(steps) / (steps - 1)])
raw = raw / raw.sum() * (CHAIN[1] - CHAIN[0])
starts = CHAIN[0] + np.concatenate([[0], np.cumsum(raw)[:-1]])

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


# ---- the line's speed over the whole film, from the same timings as the picture
speed = np.zeros(N)
tt = t_of(N)


def bump(a, b, peak):
    """A move from a to b with a cosine ease: speed is a sine hump."""
    i0, i1 = int(a * SR), int(b * SR)
    u = np.linspace(0, 1, i1 - i0, endpoint=False)
    speed[i0:i1] = np.maximum(speed[i0:i1], peak * np.sin(np.pi * u))


bump(*DRAW, 0.55)
bump(*FIRST, 0.7)
for s, d in zip(starts, raw):
    bump(s, s + d * MOVE, min(1.0, 0.16 / (d * MOVE)) ** 0.6)
bump(*END, 0.55)
speed = lp(speed, 30)

G_MAJ9 = [43, 55, 59, 62, 66, 69]
E_MIN9 = [40, 55, 59, 62, 66]
C_MAJ9 = [36, 55, 59, 62, 64]
D_SUS = [38, 54, 57, 62, 64]
G_END = [43, 55, 59, 62, 67, 71]
ARP = [67, 71, 74, 79, 83, 86, 91]                     # G major, climbing

# ---- 0-6: the page. A quiet G bed, the pencil draws, the first note when the bird closes
add_st(*pad(G_MAJ9, 7.2, g=0.36, cutoff=900, a=1.6, rel=1.6), 0.0)
add(sub(43, 7.0, g=0.12), 0.0)
add_st(*pencil(speed, g=0.16), 0.0)
add(piano(62, 0.32, dur=2.4), DRAW[0] + 0.05, pan=-0.2)
add(piano(67, 0.36, dur=2.6), FIRST[1] - 0.05, pan=0.1)
add(piano(71, 0.22, dur=2.4), FIRST[1] + 0.35, pan=0.25)
add(thock(0.08), FIRST[1] - 0.05)

# ---- 6-19.4: one hundred marks. One note per landing, climbing as the pace quickens; pads move underneath
chords = [(G_MAJ9, 43), (E_MIN9, 40), (C_MAJ9, 36), (D_SUS, 38)]
seg = (CHAIN[1] - CHAIN[0]) / 4
for k, (ch, root) in enumerate(chords):
    add_st(*pad(ch, seg + 0.9, g=0.4, cutoff=1100 + 200 * k, a=0.7, rel=0.9), CHAIN[0] - 0.3 + k * seg)
    add(sub(root, seg + 0.6, g=0.13), CHAIN[0] - 0.2 + k * seg)
for i, (s, d) in enumerate(zip(starts, raw)):
    land = s + d * MOVE
    pace = min(1.0, 0.16 / d)                          # 0.3 slow .. 1 fastest
    deg = int(round(pace * 4)) + (i % 3)               # faster = higher on the arpeggio
    m = ARP[min(deg, len(ARP) - 1)]
    g = 0.2 * (1.1 - 0.55 * pace)                      # dense notes play softer
    add(piano(m, g, dur=0.9 + 0.9 * (1 - pace), bright=0.8), land - 0.01, pan=float(np.sin(i * 1.7)) * 0.45)
    add(tick(0.03 * (1.1 - 0.6 * pace), f=2600 + 900 * pace), land, pan=float(np.cos(i * 1.3)) * 0.3)
add_st(*whoosh(4.0, 2.8, g=0.035, f0=500, f1=3800), 11.2)

# ---- 19.4-22: the last mark opens into the JQ mark; the line lands on a G chord and fills in
add_st(*pad(G_END, TOTAL - END[0] + 0.2, g=0.5, cutoff=1500, a=1.4, rel=1.8), END[0] - 0.2)
add(sub(43, TOTAL - END[0], g=0.17), END[0])
for m, dt, p in ((55, 0.0, -0.3), (59, 0.06, -0.1), (62, 0.12, 0.1), (67, 0.2, 0.3)):
    add(piano(m, 0.3, dur=3.6), END[1] - 0.05 + dt, pan=p)
add(bell(79, 0.14, dur=3.0), FILL[0] + 0.5, pan=0.2)

# ---- lockup: a bell for "Marks", two notes for the line under it, a tick per URL letter
add(bell(74, 0.22, dur=3.2), WORD, pan=-0.15)
add(piano(71, 0.22, dur=2.0), SUBLINE, pan=-0.1)
add(piano(74, 0.2, dur=2.4), SUBLINE + 0.22, pan=0.1)
for k in range(URL[2]):
    add(tick(0.04, f=rng.uniform(2200, 3000)), URL[0] + k * (URL[1] - URL[0]) / URL[2], pan=rng.uniform(-0.2, 0.2))
add(piano(79, 0.16, dur=2.6), URL[1] + 0.15, pan=0.15)

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
