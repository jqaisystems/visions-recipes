"""
Original score for R03 · Signal from Noise (AI News Curator), composed in code. MIT, like the rest of this project.

D minor turning to F major, 90 BPM. Noise first: hiss and a rustle of metallic grains over a dark Dm9 bed while
the opening line types. The field switches on with a deep thunk and a magnetic hum, and the grains sweep into
line as the harmony opens to F. Six poles land with six struck tones. The brief gets a calm Bbmaj7 to F pad and a
soft pop for each row; the review gate is a scan with a tick per row. The archive settles, and the lockup
resolves on F with a bell. Every sound ends in a release.

Picture timings come from the T table in index.html (mirrored below).
Usage: py -3.13 score/compose.py  ->  assets/bgm/score.wav   (numpy only, deterministic)
"""
import os
import wave
import numpy as np

SR = 44100
TOTAL = 26.0
N = int(TOTAL * SR)
rng = np.random.default_rng(23)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "bgm", "score.wav")

# ---- picture timings (index.html T table)
BEAT = 60 / 90
OPEN = (0.6, 1.9, 18)
NORMALIZE = (4.0, 7.4)
CLASSIFY = (9.0, 12.2)
THEMES = (10.2, 6, 0.22)
PICK = (13.4, 13.9)
CARD = 13.8
FLY = (14.0, 0.2, 0.8)          # first row starts, stagger, flight time
GATE = (18.9, 20.1)
ROW0, ROWG = 416, 50
FOOT = (20.2, 20.9, 35)
ARCHIVE = (21.2, 22.6)
RECEDE = 21.0
LOGO = 22.2
WORDS = (22.5, 4, 0.14)
SUB = 23.7
URL = (24.0, 25.0, 42)

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



def paper(dur, g=1.0, lo=500, hi=6500, grains=900):
    """Paper texture: dense tiny grains of band-limited noise, the crackle of a sheet being handled."""
    n = int(dur * SR)
    out = np.zeros(n)
    for _ in range(int(grains * dur)):
        gl = int(rng.uniform(0.002, 0.012) * SR)
        i = int(rng.uniform(0, 1) * max(1, n - gl))
        out[i:i + gl] += rng.standard_normal(gl) * np.hanning(gl) * rng.uniform(0.2, 1.0)
    return lp(hp(out, lo), hi) * g


def crease(g=1.0):
    """A fold being pressed flat: a crackle swelling into a soft thump."""
    n = int(0.55 * SR); t = t_of(n)
    env = np.minimum(t / 0.35, 1.0) ** 1.5 * np.exp(-np.maximum(t - 0.35, 0) / 0.05)
    crk = paper(0.55, 1.0, lo=900, hi=7000, grains=1400) * env
    thump = np.sin(2 * np.pi * 95 * t) * np.exp(-np.maximum(t - 0.36, 0) / 0.06) * (t > 0.36)
    return (crk * 0.9 + thump * 0.6) * g


def roller(dur, g=1.0):
    """A printer head rolling down the sheet: a filtered hum with a fast mechanical tick."""
    n = int(dur * SR); t = t_of(n)
    hum = lp(rng.standard_normal(n), 1200, poles=2) * 0.6 + 0.25 * np.sin(2 * np.pi * 220 * t)
    ticks = (np.sin(2 * np.pi * 28 * t) > 0.92).astype(float)
    ticks = lp(ticks * rng.standard_normal(n), 5000) * 0.9
    env = np.minimum(t / 0.06, 1) * np.clip((dur - t) / 0.08, 0, 1)
    return (hum + ticks) * env * g


def slide(dur, g=1.0):
    """Card sliding across a surface: a soft swell of low paper noise."""
    n = int(dur * SR); t = t_of(n); u = t / dur
    env = np.sin(np.pi * u) ** 1.3
    return lp(paper(dur, 1.0, lo=200, hi=2600, grains=700), 3000) * env * g




def grains(dur, density, g=1.0, f_lo=2500, f_hi=9000, dens_curve=None, seed_pan=0.6):
    """Iron filings: tiny inharmonic metallic pings, scattered in time. density = grains per second (or a curve)."""
    n = int(dur * SR)
    out = [np.zeros(n), np.zeros(n)]
    t = 0.0
    while t < dur:
        u = t / dur
        d = density if dens_curve is None else dens_curve(u)
        t += rng.exponential(1.0 / max(d, 1e-3))
        if t >= dur:
            break
        gl = int(rng.uniform(0.006, 0.03) * SR)
        i = int(t * SR)
        if i + gl >= n:
            break
        f = rng.uniform(f_lo, f_hi)
        tt = t_of(gl)
        x = (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 2.76 * tt)) * np.exp(-tt / (gl / SR / 4))
        a = rng.uniform(0.2, 1.0)
        p = rng.uniform(-seed_pan, seed_pan)
        out[0][i:i + gl] += x * a * np.sqrt(0.5 * (1 - p))
        out[1][i:i + gl] += x * a * np.sqrt(0.5 * (1 + p))
    return [o * g for o in out]


def hum(dur, g=1.0, f=55.0, open_t=1.0):
    """Magnetic hum: a mains-like tone with odd harmonics whose filter opens as the field turns on."""
    n = int(dur * SR); t = t_of(n)
    x = sum(np.sin(2 * np.pi * f * h * t + h) / h for h in (1, 2, 3, 5, 7))
    cut = 160 + 1400 * np.minimum(t / open_t, 1) ** 2
    return lp_var(x, cut) * adsr(n, a=0.3, d=10, s=1, rel=0.8) * g


def hiss(dur, g=1.0, f=5000):
    n = int(dur * SR)
    return [lp(hp(rng.standard_normal(n), 2500), f) * adsr(n, a=0.4, d=10, s=1, rel=0.6) * g for _ in range(2)]


def strike(m, g=1.0):
    """A pole landing: a soft low thump with a struck metal partial on top."""
    n = int(1.6 * SR); t = t_of(n)
    thump = np.sin(2 * np.pi * np.cumsum(70 + 80 * np.exp(-t / 0.03)) / SR) * np.exp(-t / 0.12)
    return thump * 0.6 * g + bell(m, 0.5 * g, dur=1.6)


D_MIN9 = [38, 50, 53, 57, 60, 64]
F_MAJ9 = [41, 53, 57, 60, 64, 67]
BB_MAJ7 = [46, 58, 62, 65, 69]
C_ADD9 = [48, 55, 60, 62, 64]
ARP = {"F": [65, 69, 72, 76], "Bb": [65, 70, 74, 77], "Dm": [62, 65, 69, 72]}

# ---- 0-4 noise: hiss, scattered filings, a dark bed, the opening line typing
add_st(*pad(D_MIN9, 5.0, g=0.42, cutoff=800, a=1.2, rel=1.2), 0.0)
add(sub(38, 5.0, g=0.16), 0.0)
add_st(*hiss(5.0, 0.05), 0.0)
add_st(*grains(4.6, 34, g=0.05), 0.0)
for k in range(OPEN[2]):
    add(tick(0.06, f=rng.uniform(1700, 2500)), OPEN[0] + k * (OPEN[1] - OPEN[0]) / OPEN[2], pan=rng.uniform(-0.2, 0.2))

# ---- 4.0-7.4 normalize: thunk, the field hums on, the filings sweep into line, the harmony opens to F
add(boom(0.35), NORMALIZE[0])
add(thock(0.45), NORMALIZE[0])
add(hum(8.6, 0.09, open_t=2.5), NORMALIZE[0])
nd = NORMALIZE[1] - NORMALIZE[0] + 0.6
add_st(*grains(nd, 0, g=0.06, dens_curve=lambda u: 30 + 520 * np.sin(np.pi * min(1, u * 1.15)) ** 2), NORMALIZE[0] + 0.1)
add_st(*whoosh(nd, nd * 0.45, g=0.07, f0=500, f1=4200), NORMALIZE[0])
add_st(*pad(F_MAJ9, 5.6, g=0.5, cutoff=1500, a=1.0, rel=1.0), 5.2)
add(sub(41, 5.4, g=0.16), 5.2)
for k, tb in enumerate(np.arange(5.6, 9.0, BEAT)):
    add(pluck(ARP["F"][k % 4], 0.08, d=0.2, bright=2400), tb, pan=-0.3 + 0.6 * (k % 4) / 3)

# ---- 9.0-12.2 classify: the field splits into six poles; a struck tone for each theme
cd = CLASSIFY[1] - CLASSIFY[0]
add_st(*grains(cd, 0, g=0.055, dens_curve=lambda u: 40 + 420 * np.sin(np.pi * u) ** 2), CLASSIFY[0])
add_st(*whoosh(cd, cd * 0.4, g=0.06, f0=400, f1=3600), CLASSIFY[0])
add_st(*pad(D_MIN9[1:] + [41], 5.2, g=0.46, cutoff=1400, a=0.6, rel=1.0), CLASSIFY[0] - 0.2)
for i, m in enumerate((62, 65, 69, 72, 74, 77)):
    add(strike(m, 0.3), THEMES[0] + i * THEMES[2], pan=[-0.5, 0, 0.5, -0.5, 0, 0.5][i])

# ---- 13.4-18.9 the brief: six glints, a row lands every 0.2 s, a calm pad
for i in range(6):
    add(tick(0.12, f=5200 + 300 * i), PICK[0] + i * 0.05, pan=[-0.5, 0, 0.5, -0.5, 0, 0.5][i])
add_st(*whoosh(0.9, 0.5, g=0.06, f0=600, f1=3000), CARD - 0.2)
add_st(*pad(BB_MAJ7, 3.0, g=0.5, cutoff=1500, a=0.6, rel=0.8), 13.6)
add_st(*pad(F_MAJ9, 4.0, g=0.5, cutoff=1500, a=0.8, rel=0.9), 16.2)
add(sub(46, 2.8, g=0.15), 13.6)
add(sub(41, 4.0, g=0.15), 16.2)
for i in range(6):
    land = FLY[0] + i * FLY[1] + FLY[2]
    add(blip(72 + [0, 2, 4, 7, 9, 12][i], 0.16), land - 0.02, pan=0.15)
    add(thock(0.12), land)
tb, k = 15.4, 0
while tb < GATE[0] - 0.1:
    chord = "Bb" if tb < 16.2 else "F"
    add(pluck(ARP[chord][k % 4], 0.06, d=0.18, bright=2200), tb, pan=-0.35 + 0.7 * (k % 4) / 3)
    k += 1
    tb += BEAT / 2

# ---- 18.9-20.9 review: the gate scans down the card, a tick as it passes each row, the footnote types
add(zap(GATE[1] - GATE[0], 0.1), GATE[0])
add_st(*pad(C_ADD9, 2.4, g=0.42, cutoff=1300, a=0.4, rel=0.6), GATE[0] - 0.1)
for i in range(6):
    p = (i * ROWG + 35 + 15) / (6 * ROWG + 12)
    add(blip(84, 0.1), GATE[0] + p * (GATE[1] - GATE[0]), pan=0.2)
for k in range(0, FOOT[2], 2):
    add(tick(0.05, f=rng.uniform(2000, 2800)), FOOT[0] + k * (FOOT[1] - FOOT[0]) / FOOT[2], pan=0.1)

# ---- 21-26 archive and lockup: the field settles into rows, resolve on F, the line, the URL, a bell
add_st(*whoosh(ARCHIVE[1] - ARCHIVE[0] + 0.4, 0.6, g=0.07, f0=300, f1=2600), ARCHIVE[0] - 0.2)
add_st(*grains(1.6, 0, g=0.045, dens_curve=lambda u: 300 * (1 - u) ** 2 + 10), ARCHIVE[0])
add_st(*pad(F_MAJ9, TOTAL - RECEDE, g=0.58, cutoff=1600, a=0.5, rel=1.6), RECEDE)
add(sub(41, TOTAL - RECEDE, g=0.2), RECEDE)
add(bell(72, 0.3, dur=3.2), LOGO, pan=-0.2)
for i in range(WORDS[1]):
    add(pluck([65, 69, 72, 76][i], 0.08, d=0.2, bright=2400), WORDS[0] + i * WORDS[2])
add(thock(0.18), SUB)
for k in range(0, URL[2], 2):
    add(tick(0.05, f=rng.uniform(2200, 3000)), URL[0] + k * (URL[1] - URL[0]) / URL[2], pan=rng.uniform(-0.2, 0.2))
add(bell(84, 0.16, dur=3.0), URL[1] + 0.1, pan=0.1)

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
