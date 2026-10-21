"""
Original score for R02 · Paper Terminal (JQ AI Skills), composed in code. MIT, like the rest of this project.

F major, 96 BPM, warm and tactile where Token Rain was cold: soft plucks over an Fmaj9 bed while the prompt is
typed again; a printer roll as SKILL.md prints; four paper creases as the sheet folds; a stamp; a slide onto
the shelf; a building pulse through Dm and C on the pull-back; a chime for each skill that gets called; the
lockup resolves on F with a bell. Every sound ends in a release.

Picture timings come from the T table in index.html (mirrored below).
Usage: py -3.13 score/compose.py  ->  assets/bgm/score.wav   (numpy only, deterministic)
"""
import os
import wave
import numpy as np

SR = 44100
TOTAL = 26.0
N = int(TOTAL * SR)
rng = np.random.default_rng(22)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "bgm", "score.wav")

# ---- picture timings (index.html T table)
BEAT = 60 / 96
PAPER_IN = 0.15
GHOSTS = (0.3, 0.6)
TYPE = (0.9, 3.4)
PROMPT_LEN = 215
SCROLL = 3.9
CMD = (4.5, 5.2, 27)
ENTER = 5.35
PRINT = (5.5, 6.5)
FOLDS = [(7.6, 8.25), (8.25, 8.9), (8.9, 9.55)]
STAMP = 9.7
FLIGHT = (10.1, 12.5)
LAND = 12.5
PULL = (12.7, 16.5)
CALLS = [16.7, 17.35, 18.0, 18.65, 19.3]
RECEDE = 19.8
LOGO = 20.4
WORDS = (20.7, 6, 0.12)
SUB = 21.9
URL = (22.3, 23.3, 37)

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


F_MAJ9 = [41, 53, 57, 60, 64, 67]
BB_MAJ7 = [46, 58, 62, 65, 69]
D_MIN7 = [50, 57, 60, 65, 69]
C_ADD9 = [48, 55, 60, 62, 64]
ARP = {"F": [65, 69, 72, 76], "Bb": [65, 70, 74, 77], "Dm": [62, 65, 69, 72], "C": [64, 67, 72, 74]}

# ---- 0-6.5 the terminal: Fmaj9 bed, sparse plucks, the same prompt typed again
add_st(*pad(F_MAJ9, 7.2, g=0.5, cutoff=1300, a=0.9, rel=1.0), 0.0)
add(sub(41, 7.0, g=0.18), 0.0)
add(slide(0.7, 0.16), PAPER_IN)
for k, tb in enumerate(np.arange(0.6, 6.4, BEAT * 2)):
    add(pluck(ARP["F"][k % 4], 0.12, d=0.22, bright=2200), tb, pan=-0.3 + 0.6 * (k % 4) / 3)
for tg in GHOSTS:
    add(tick(0.09, f=1800), tg)
for k in range(0, PROMPT_LEN, 3):
    add(tick(0.07, f=rng.uniform(1700, 2600)), TYPE[0] + k * (TYPE[1] - TYPE[0]) / PROMPT_LEN, pan=rng.uniform(-0.2, 0.2))
add(slide(0.5, 0.08), SCROLL)
for k in range(CMD[2]):
    add(tick(0.08, f=rng.uniform(2000, 2800)), CMD[0] + k * (CMD[1] - CMD[0]) / CMD[2], pan=0.1)
add(thock(0.45), ENTER)
add(roller(PRINT[1] - PRINT[0], 0.22), PRINT[0])

# ---- 6.5-9.6 the folds: Bbmaj7, one crease per fold, pitched up each time
add_st(*pad(BB_MAJ7, 3.6, g=0.5, cutoff=1500, a=0.6, rel=0.6), 6.4)
for (a, b), m in zip(FOLDS, (69, 72, 76)):
    add_st(crease(0.42), crease(0.42), a + (b - a) * 0.5 - 0.36, width=0.5)
    add(bell(m, 0.16, dur=1.4), (a + b) / 2, pan=0.2)

# ---- 9.7 stamp, then the slide onto the shelf and the card set down
add(thock(0.6), STAMP)
add(boom(0.22), STAMP)
add(tick(0.2, f=3200), STAMP + 0.01)
add_st(slide(FLIGHT[1] - FLIGHT[0], 0.22), slide(FLIGHT[1] - FLIGHT[0], 0.22), FLIGHT[0], width=0.7)
add(thock(0.35), LAND)
add(bell(77, 0.22, dur=1.8), LAND + 0.02, pan=0.4)

# ---- 12.7-16.5 the pull-back: Dm7 then C, a pulse that builds, the shelf filling in
add_st(*pad(D_MIN7, 2.4, g=0.5, cutoff=1700, a=0.4, rel=0.4), PULL[0] - 0.3)
add_st(*pad(C_ADD9, 4.8, g=0.55, cutoff=2000, a=0.4, rel=0.5), PULL[0] + 1.9)
add_st(*whoosh(PULL[1] - PULL[0], (PULL[1] - PULL[0]) * 0.55, g=0.12, f0=300, f1=3200), PULL[0])
tb, k = PULL[0], 0
while tb < RECEDE - 0.1:
    u = min(1.0, (tb - PULL[0]) / (PULL[1] - PULL[0]))
    chord = "Dm" if tb < PULL[0] + 1.9 else "C"
    add(pluck(ARP[chord][k % 4], 0.08 + 0.08 * u, d=0.18, bright=2600), tb, pan=-0.35 + 0.7 * (k % 4) / 3)
    if tb > PULL[0] + 1.9:
        add(bass((36 if chord == "C" else 38) + (12 if k % 4 == 2 else 0), BEAT * 0.45, g=0.12 + 0.1 * u), tb)
    k += 1
    tb += BEAT / 2
for ct, m in zip(CALLS, (79, 81, 84, 86, 88)):
    add(blip(m, 0.2), ct + 0.05, pan=0.3)
    add(tick(0.08, f=4200), ct + 0.05)

# ---- 19.8-26 lockup: resolve on F, the line arrives, the URL types, a bell rings out
add_st(*pad(F_MAJ9, TOTAL - RECEDE, g=0.6, cutoff=1600, a=0.35, rel=1.6), RECEDE)
add(sub(41, TOTAL - RECEDE, g=0.2), RECEDE)
add(bell(72, 0.3, dur=3.2), LOGO, pan=-0.2)
for i in range(WORDS[1]):
    add(pluck([65, 69, 72, 76, 77, 81][i], 0.07, d=0.2, bright=2400), WORDS[0] + i * WORDS[2])
add(thock(0.18), SUB)
for k in range(URL[2]):
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
