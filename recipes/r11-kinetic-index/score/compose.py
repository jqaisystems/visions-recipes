"""
R11 · Kinetic Index. Original score, composed in code (first made for the --blog page intro on visions.joaoqueiros.com).

10 s, F major, 100 BPM. Built on the One Line instrument set (every sound has a release, risers fall away).
  0-1.6     the prompt types: one key tick per character, Enter lands on a soft thock
  1.6-3.0   the river of titles pours out: page-turn air and a soft arpeggio
  2.6-7.2   three searches type out (a tick per letter); each lands on the beat with a chime as the matches light up
  7.2-8.9   the river tilts away and rushes: air and a riser
  9.0       "Field notes for imagined worlds.": one hit, the chord rings out
Picture timings live in index.html; keep the constants below in sync with them.
Usage: python score/compose.py  ->  assets/bgm/score.wav   (numpy only, deterministic)
"""
import os
import wave
import numpy as np

SR = 44100
BEAT = 0.6
TOTAL = 10.0
N = int(TOTAL * SR)
rng = np.random.default_rng(23)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "bgm", "score.wav")

# ---- picture timings (index.html)
PROMPT_LEN, TYPE = 41, (0.25, 1.45)   # "/index visions --searchable --field-notes"
ENTER = 1.6
Q = [("colour", 2.6, 3.0), ("motion", 4.3, 4.8), ("light", 6.1, 6.6)]   # same words as Q in index.html
DEL = 0.22
TILT = (7.2, 8.9)
TITLE, SUB = 9.0, 9.45
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


# ---- instruments
def kick(g=1.0):
    n = int(0.5 * SR); t = t_of(n)
    f = 46 + 110 * np.exp(-t / 0.03)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.17)
    click = lp(rng.standard_normal(n), 3500) * np.exp(-t / 0.004) * 0.25
    return (body + click) * adsr(n, a=0.001, d=10, s=1, rel=0.12) * g * 0.7


def snare(g=1.0):
    n = int(0.3 * SR); t = t_of(n)
    body = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05)
    x = rng.standard_normal(n)
    noise = lp(hp(x, 1400), 7000) * np.exp(-t / 0.11)
    return (0.6 * body + 0.8 * noise) * adsr(n, a=0.001, d=10, s=1, rel=0.08) * g


def clap(g=1.0):
    n = int(0.32 * SR); x = rng.standard_normal(n)
    x = lp(hp(x, 900), 5200)
    e = np.zeros(n)
    for off in (0.0, 0.011, 0.023):
        i = int(off * SR); e[i:] += np.exp(-t_of(n - i) / 0.055)
    return x * e * 0.5 * adsr(n, a=0.001, d=10, s=1, rel=0.08) * g


def hat(g=1.0, d=0.02):
    n = int(0.09 * SR); x = rng.standard_normal(n)
    return hp(x, 7500) * adsr(n, a=0.001, d=d, rel=0.02) * g


def crash(g=1.0, dur=2.4):
    n = int(dur * SR)
    out = []
    for _ in range(2):
        x = hp(rng.standard_normal(n), 5200)
        out.append(lp(x, 11000) * adsr(n, a=0.002, d=0.9, rel=0.5) * g)
    return out


def tick(g=1.0, f=2400):
    n = int(0.04 * SR); t = t_of(n)
    return np.sin(2 * np.pi * f * t) * adsr(n, a=0.0005, d=0.006, rel=0.01) * g


def thock(g=1.0):
    n = int(0.22 * SR); t = t_of(n)
    x = np.sin(2 * np.pi * 170 * t) * np.exp(-t / 0.045) + 0.3 * lp(rng.standard_normal(n), 1500) * np.exp(-t / 0.02)
    return x * adsr(n, a=0.001, d=10, s=1, rel=0.06) * g


def blip(m, g=1.0):
    """Short glassy UI pop with a tiny upward bend."""
    n = int(0.22 * SR); t = t_of(n)
    f = hz(m) * (1 + 0.04 * (1 - np.exp(-t / 0.01)))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.25 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    return x * adsr(n, a=0.002, d=0.06, rel=0.08) * g


def pluck(m, g=1.0, d=0.14, bright=3200):
    n = int(0.7 * SR)
    return lp(saw(hz(m), n, harmonics=14), bright) * adsr(n, a=0.002, d=d, rel=0.15) * g


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


def wobble(m, dur, rate, g=1.0):
    """Bass with a filter that opens and closes on the beat: the line shivering into a waveform."""
    n = int(dur * SR); t = t_of(n)
    x = saw(hz(m), n, harmonics=14) + 0.6 * np.sin(2 * np.pi * hz(m - 12) * t)
    cut = 220 + 1300 * (0.5 - 0.5 * np.cos(2 * np.pi * rate * t))
    return lp_var(lp_var(x, cut, block=128), cut, block=128) * adsr(n, a=0.02, d=10, s=1, rel=0.12) * g


def sweep(dur, g=1.0, f0=300, f1=6500, fade=0.15):
    """Noise riser: opens up and gets louder, then falls away over the last `fade` s."""
    n = int(dur * SR); t = t_of(n)
    u = t / dur
    e = u ** 2 * np.clip((dur - t) / fade, 0, 1) ** 0.5
    out = []
    for _ in range(2):
        out.append(lp(rng.standard_normal(n), f0 + (f1 - f0) * u ** 2, poles=2) * e * g)
    return out


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


def zap(dur, g=1.0):
    """The scan line moving down the card: a falling, bright-to-dark sweep."""
    n = int(dur * SR); t = t_of(n); u = t / dur
    tone = glide(2200, 520, n, shape=0.7) * 0.35
    noise = lp(rng.standard_normal(n), 6000 - 5200 * u, poles=2)
    return (tone + noise) * np.sin(np.pi * u) ** 0.7 * g


def riser_tone(m0, m1, dur, g=1.0, fade=0.1):
    n = int(dur * SR); t = t_of(n)
    x = glide(hz(m0), hz(m1), n, shape=1.6)
    x = x + 0.3 * np.sign(x) * np.abs(x) ** 3
    return x * (t / dur) ** 1.5 * np.clip((dur - t) / fade, 0, 1) * g


def boom(g=1.0):
    n = int(3.0 * SR); t = t_of(n)
    f = 36 + 60 * np.exp(-t / 0.08)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.9) * adsr(n, a=0.001, d=10, s=1, rel=0.6) * g


F = (41, [57, 60, 65, 69]); DM = (38, [57, 62, 65, 69]); BB = (34, [58, 62, 65, 70]); C = (36, [55, 60, 64, 67])
PROG = [(3.0, 4.8, *F), (4.8, 6.6, *DM), (6.6, 7.8, *BB), (7.8, TITLE, *C)]
FADD9 = [29, 41, 53, 60, 65, 67, 69, 72]

def page(g=1.0):
    """A page turning: a short airy swish."""
    n = int(0.28 * SR); t = t_of(n); u = t / 0.28
    out = []
    for _ in range(2):
        x = lp(hp(rng.standard_normal(n), 900), 3500 + 3000 * np.sin(np.pi * u), poles=2)
        out.append(x * np.sin(np.pi * u) ** 1.5 * g)
    return out

# ---- the prompt
for i in range(1, PROMPT_LEN + 1):
    add(tick(0.2, f=1700 + int(rng.integers(0, 900))), TYPE[0] + (TYPE[1] - TYPE[0]) * (i - 0.5) / PROMPT_LEN, pan=float(rng.uniform(-0.35, 0.35)))
add(thock(0.5), ENTER); add(sub(41, 0.6, 0.3), ENTER)

# ---- the river pours out: page-turn air and a soft arpeggio
for k in range(6):
    add_st(*page(0.10 + 0.02 * k), ENTER + 0.08 + 0.21 * k)
add_st(*pad([53, 60, 65, 69], 3.0 - ENTER + 0.5, cutoff=1100, a=0.5, rel=0.4), ENTER, g=0.24)
tb, s = ENTER + 0.3, 0
while tb < 2.95:
    add(pluck([65, 69, 72, 77][s % 4], 0.05 + 0.015 * s, d=0.1, bright=2800), tb, pan=(-0.35, 0.35)[s % 2])
    tb += BEAT / 4; s += 1

# ---- the searches: a groove from the first landing, a tick per letter, a chime when the matches light up
for a, b, root, ch in PROG[:3]:
    add_st(*pad(ch, b - a + 0.6, cutoff=1700, a=0.1, rel=0.5), a, g=0.3)
tb = 3.0
while tb < TILT[0] - 1e-6:
    root = [r_ for a_, b_, r_, h_ in PROG if a_ <= tb < b_][0]
    beat = int(round((tb - 3.0) / BEAT))
    add(kick(0.62 if beat % 2 == 0 else 0.4), tb)
    if beat % 2: add(clap(0.22), tb)
    add(hat(0.1), tb + BEAT / 2, pan=0.25)
    add(bass(root, BEAT * 0.4, 0.34), tb); add(bass(root + 12, BEAT * 0.2, 0.16), tb + BEAT / 2)
    tb += BEAT
for i, (q, t0, land) in enumerate(Q):
    if i:
        for k in range(len(Q[i - 1][0])):
            add(tick(0.07, f=1300), t0 - DEL + DEL * k / len(Q[i - 1][0]), pan=-0.2)
    for k in range(len(q)):
        add(tick(0.17, f=1900 + int(rng.integers(0, 800))), t0 + (land - 0.06 - t0) * (k + 0.5) / len(q), pan=float(rng.uniform(-0.3, 0.3)))
    root, ch = [(r_, h_) for a_, b_, r_, h_ in PROG if a_ <= land < b_][0]
    for j, m in enumerate(ch[1:]):
        add(bell(m + 12, 0.07, dur=1.2), land + 0.03 * j, pan=-0.35 + 0.35 * j)
    add(blip(ch[3] + 24, 0.07), land + 0.18)

# ---- the river tilts away and rushes
add_st(*whoosh(TITLE - TILT[0] + 0.1, 1.3, 0.26, f0=400, f1=5200), TILT[0])
a, b, root, ch = PROG[3]
add_st(*pad(ch + [ch[0] + 12], TITLE - 6.6 + 0.6, cutoff=2400, a=0.6, rel=0.6), 6.6, g=0.3)
add(sub(root, TITLE - 7.8, 0.22), 7.8)
add(riser_tone(48, 60, TITLE - 7.6, 0.07, fade=0.08), 7.6)
for k in range(10):
    add_st(*page(0.05 + 0.02 * k), 7.4 + 0.15 * k)
add_st(*sweep(TITLE - 8.0, 0.2, fade=0.1), 8.0)

# ---- "Field notes for imagined worlds."
add(boom(0.7), TITLE); add(kick(0.9), TITLE)
add_st(*pad(FADD9, TOTAL - TITLE + 0.5, cutoff=2200, a=0.03, rel=1.0), TITLE, g=0.7)
for i, m in enumerate([77, 81, 84, 89]):
    add(bell(m, 0.1, dur=1.4), TITLE + 0.1 + 0.07 * i, pan=-0.3 + 0.2 * i)
add(pluck(84, 0.1, d=0.2), SUB)
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
fn = int(0.6 * SR)
fade[-fn:] = np.linspace(1, 0, fn) ** 2
mix = np.tanh(mix * fade * 1.1) / np.tanh(1.1)
mix /= np.max(np.abs(mix)) / PEAK   # PEAK sets the level: about -12 LUFS in the WAV, played at 0.65 (as productfilms-reel)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with wave.open(OUT, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix.T * 32767).astype("<i2").tobytes())
print("wrote", os.path.normpath(OUT), round(TOTAL, 2), "s")
