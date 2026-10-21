"""
Original score for R01 · Token Rain (Prompt Engineering), composed in code. MIT, like the rest of this project.

D minor, free time with a 120 BPM pulse under the dive. One arc: a quiet Dm9 bed while the prompt types and the
draft streams; the scan rises; the clichés crackle as they burn; the rain hisses and a pulse builds through
Bb and C; three chimes climb at Draft, Critique and Rewrite; the landing resolves on F major; the lockup
rings out on Bbmaj9. Every sound ends in a release; nothing is cut while sounding.

Picture timings come from index.html: the T table is mirrored below, and the per-word times are read from
score/timings.json (dumped from the live page's window.TR_INFO).
Usage: py -3.13 score/compose.py  ->  assets/bgm/score.wav   (numpy only, deterministic)
"""
import json
import os
import wave
import numpy as np

SR = 44100
TOTAL = 26.0
N = int(TOTAL * SR)
rng = np.random.default_rng(21)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "bgm", "score.wav")

# ---- picture timings (index.html T table)
RULE = 0.1
FIELD = 0.3
TYPE = (0.6, 1.9)
PROMPT_LEN = 39
ENTER = 2.0
SCAN = (5.0, 6.9)
CAM = (9.4, 16.0)
Y_END, GATES = -48.0, (-14.0, -26.0, -38.0)
LINE_IN = 16.5
RULE_FORM = (21.0, 21.7)
LOGO = 21.3
TITLE = 22.0
URL = (22.5, 23.5, 46)
with open(os.path.join(HERE, "timings.json"), encoding="utf-8") as fh:
    WORDS = json.load(fh)["words"]


def gate_time(gy):
    """When the stream's centre (Y_END * smoothstep(p)) passes gate gy + 1, as the HUD counts it."""
    target = (gy + 1) / Y_END
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if mid * mid * (3 - 2 * mid) < target:
            lo = mid
        else:
            hi = mid
    return CAM[0] + lo * (CAM[1] - CAM[0])


GATE_T = [gate_time(g) for g in GATES]

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




def crackle(dur, density, g=1.0, f_lo=2500):
    """Glyphs burning into tokens: a shower of tiny bright grains that thins out."""
    n = int(dur * SR)
    out = np.zeros(n)
    count = int(density * dur)
    for _ in range(count):
        gl = int(rng.uniform(0.002, 0.008) * SR)
        i = int(rng.uniform(0, 1) ** 1.6 * (n - gl))
        grain = hp(rng.standard_normal(gl), f_lo) * np.hanning(gl) * rng.uniform(0.3, 1.0)
        out[i:i + gl] += grain
    return out * g


# ---- bed: Dm9 while the draft exists
add_st(*pad([50, 57, 60, 64, 65], 9.9, g=0.55, cutoff=900, a=1.4, rel=1.2), 0.0)
add(sub(38, 9.8, g=0.22), 0.0)

# ---- 0-4.4 prompt + stream
add_st(*sweep(0.8, g=0.10, f0=1500, f1=7000, fade=0.25), RULE)
add(thock(0.22), FIELD, pan=-0.2)
for k in range(PROMPT_LEN):
    tk = TYPE[0] + k * (TYPE[1] - TYPE[0]) / PROMPT_LEN
    add(tick(0.10, f=rng.uniform(1900, 2700)), tk, pan=rng.uniform(-0.25, 0.25))
add(thock(0.5), ENTER)
add(blip(81, 0.16), ENTER + 0.02, pan=0.2)
SCALE = [62, 65, 67, 69, 72, 74, 77, 79]
for k, w in enumerate(WORDS):
    add(blip(SCALE[k % len(SCALE)] + 12 * (k // 16), 0.09), w["show"], pan=-0.4 + 0.8 * k / len(WORDS))

# ---- 5.0-6.9 the scan, with a ping on each flagged phrase
add(zap(0.35, 0.22), SCAN[0] - 0.05)
add(riser_tone(74, 86, SCAN[1] - SCAN[0], g=0.07, fade=0.25), SCAN[0])
first_flag = {}
for w in WORDS:
    if w["f"] and w["f"] not in first_flag:
        first_flag[w["f"]] = w["flag"]
for k, tf in enumerate(sorted(first_flag.values())):
    add(blip(86 + (k % 3) * 3, 0.22), tf, pan=-0.5 + k / 6)
    add(tick(0.14, f=5200), tf)

# ---- 7.4-9.2 the burn: flagged phrases crackle bright, the rest of the draft dissolves softer
for w in WORDS:
    add_st(crackle(0.45, 260, g=0.16 if w["f"] else 0.07), crackle(0.45, 260, g=0.16 if w["f"] else 0.07), w["burn"], width=0.6)
add_st(*sweep(1.8, g=0.10, f0=600, f1=3000, fade=0.6), 7.4)

# ---- 9.4-16 the chain: rain hiss, a pulse that builds through Bb and C, a chime per gate
add_st(*sweep(CAM[1] - CAM[0] + 0.2, g=0.30, f0=900, f1=9000, fade=0.45), CAM[0])
add_st(*pad([46, 58, 62, 65, 69], 3.4, g=0.5, cutoff=1500, a=0.6, rel=0.5), CAM[0])
add_st(*pad([48, 60, 64, 67, 69], 3.6, g=0.55, cutoff=2100, a=0.3, rel=0.5), CAM[0] + 3.2)
STEP = 0.25
k = 0
tb = CAM[0]
while tb < CAM[1] - 0.2:
    u = (tb - CAM[0]) / (CAM[1] - CAM[0])
    root = 34 if tb < CAM[0] + 3.2 else 36
    add(bass(root + (12 if k % 4 == 2 else 0), 0.22, g=0.18 + 0.32 * u), tb)
    if tb >= CAM[0] + 3.2:
        add(hat(0.05 + 0.10 * u), tb + STEP / 2, pan=0.3)
    k += 1
    tb += STEP
for gt, m in zip(GATE_T, (74, 77, 81)):
    add(bell(m, 0.42, dur=2.2), gt, pan=0.15)
    add_st(*whoosh(1.2, 0.55, g=0.16), gt - 0.55)

# ---- 16 landing: resolve on F major, then hold
LAND = CAM[1]
add(boom(0.55), LAND)
add_st(*crash(0.10, dur=2.6), LAND)
add_st(*pad([53, 57, 60, 64, 67], RULE_FORM[0] - LAND + 0.4, g=0.6, cutoff=1800, a=0.08, rel=0.6), LAND)
add(sub(41, RULE_FORM[0] - LAND + 0.2, g=0.22), LAND)
add(bell(77, 0.30, dur=3.0), LINE_IN, pan=-0.2)

# ---- 21-26 lockup: the rule draws, the logo and title land, the URL types, Bbmaj9 rings out
add_st(*sweep(RULE_FORM[1] - RULE_FORM[0], g=0.14, f0=2000, f1=9000, fade=0.2), RULE_FORM[0])
add_st(*pad([46, 58, 62, 65, 69, 72], TOTAL - RULE_FORM[0], g=0.6, cutoff=1600, a=0.5, rel=1.6), RULE_FORM[0])
add(sub(34, TOTAL - RULE_FORM[0], g=0.2), RULE_FORM[0])
add(bell(81, 0.32, dur=3.2), LOGO + 0.4, pan=0.2)
add(thock(0.28), TITLE + 0.05)
for k in range(URL[2]):
    add(tick(0.06, f=rng.uniform(2200, 3000)), URL[0] + k * (URL[1] - URL[0]) / URL[2], pan=rng.uniform(-0.2, 0.2))
add(bell(86, 0.18, dur=3.0), URL[1] + 0.1, pan=-0.1)

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
