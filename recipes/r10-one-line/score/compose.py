"""
Original score for Product Films · One Line, composed in code.

120 BPM, 20 bars (40.0 s), A minor. One progression runs under the whole take without restarting;
sections only change density, never the harmony. Every sound ends in a release and every riser
falls away instead of stopping dead (lessons from the productfilms-reel score fix, 2026-10-17).
  0-4      spark: pad fades in, two head pulses, the curve as a rising arpeggio, a lift into 4.0
  4-12     type + data: half-time groove, one rising note per chart bar, count-up ticks
  12-18    product: whoosh up to the card, UI blips, scan zap, price roll, render riser, chime
  18-29    edit + formats: full groove, a tick on every cut, keyframe blips, wave wobble, frame hits
  29-34.5  reveal + mark: drums out, whoosh on the pull-back, three bells, riser into the hit
  34.5-40  signature: one hit, Am9 rings out, chip, URL typing, rule shimmer

Picture timings live in index.html; keep the constants below in sync with them.
Usage: py -3.13 score/compose.py  ->  assets/bgm/score.wav   (numpy only, deterministic)
"""
import os
import wave
import numpy as np

SR = 44100
BEAT = 0.5          # 120 BPM
BAR = 4 * BEAT
TOTAL = 40.0
N = int(TOTAL * SR)
rng = np.random.default_rng(7)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "bgm", "score.wav")

# ---- picture timings (index.html)
PULSES = [0.5, 1.0]                       # head rings
CURVE = (1.5, 3.0)                        # SEG curve
TITLE = [2.1, 2.35]                       # "One" "line."
BASE = 4.0                                # the curve lands on the baseline
STAIR = (8.6, 11.2)                       # SEG stair, power1.inOut
COUNT = (9.4, 11.6)                       # 0 -> 1,200, power2.out
TOCARD = (12.0, 13.0)
UI_POPS = [13.8, 13.9, 14.0, 14.2, 14.3, 14.5]   # label, toggle, headline, sub, price, button
SCAN = (15.4, 15.95)
PRICE = 16.0
PROG = (16.4, 17.4)                       # the line fills the button; "Rendered" at 17.4
DROP = 18.0
BLOCKS = [17.9 + i * 0.09 + 0.3 for i in range(6)]
CUTS = [19.0, 20.0, 21.0, 22.0, 23.0]
KF_X = [6470, 6610, 6790, 6990, 7150, 7330, 7480, 7690, 7860, 7960]
KF = [18.0 + (x - 10 - 6400) / 1600 * 6.0 for x in KF_X]
WAVE = (24.0, 25.4)
FRAMES = [25.4 + 3.8 * d / 6539 for d in (2000, 4166, 6139)]
LAUNCH = 29.0                             # camera starts the pull-back; drums out
REVEAL = [30.2, 30.55, 30.9]
MARK = (32.6, 34.4)
FINAL = 34.5
CHIP = 35.9
URL = (36.2, 37.0, 41)                    # typed on, 41 characters
RULE = (36.8, 37.6)
NOTE = 37.4

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


# ---- harmony: one progression for the whole take (bar = 2 s). VI-VII-i into the signature.
AM = (45, [57, 60, 64, 69]); F = (41, [53, 57, 60, 65]); C = (36, [52, 55, 60, 64]); G = (43, [55, 59, 62, 67])
PROGRESSION = [AM, F, C, G] * 3 + [AM, F, C, F, G]       # bars 0-16; bar 16 runs 32.0 to 34.5
AM9 = (33, [45, 57, 64, 67, 71, 72])


def chord_at(t):
    return PROGRESSION[min(int(t // BAR), len(PROGRESSION) - 1)]


def pad_gain(t):
    if t < 4: return 0.5
    if t < 18: return 0.38
    if t < LAUNCH: return 0.42
    return 0.62


for k, (root, ch) in enumerate(PROGRESSION):
    t0 = k * BAR
    dur = (FINAL - t0 if k == len(PROGRESSION) - 1 else BAR) + 0.9   # overlap: bars crossfade
    bright = 2300 if t0 >= LAUNCH - 1 else 1400
    add_st(*pad(ch, dur, cutoff=bright, a=1.4 if k == 0 else 0.45), t0, g=pad_gain(t0))


# ---- rhythm section: beat-by-beat density, harmony from chord_at()
def section(t):
    if t < BASE: return None
    if t < 14.0: return "half"
    if 17.4 <= t < DROP: return "fill"
    if t < DROP: return "mid"
    if t < LAUNCH: return "full"
    return None


tb = BASE
while tb < LAUNCH - 1e-6:
    mode = section(tb)
    b = int(round(tb / BEAT)) % 4
    root, ch = chord_at(tb)
    in_wave = WAVE[0] <= tb < WAVE[1]
    if mode == "half":
        if b in (0, 2): add(kick(0.78), tb)
        add(hat(0.17), tb + BEAT / 2, pan=0.25)
    elif mode == "mid":
        add(kick(0.85), tb)
        if b in (1, 3): add(clap(0.45), tb)
        add(hat(0.19), tb + BEAT / 2, pan=0.25)
    elif mode == "full":
        add(kick(0.92), tb)
        if b in (1, 3): add(clap(0.55), tb)
        add(hat(0.2), tb + BEAT / 2, pan=0.25)
        add(hat(0.1), tb + BEAT / 4, pan=-0.3); add(hat(0.08), tb + 3 * BEAT / 4, pan=-0.3)
        for s in range(4):
            tone = ch[1:][s % 3] + 12 + (12 if s == 3 else 0)
            add(pluck(tone, 0.12, d=0.09), tb + s * BEAT / 4, pan=0.4 if s % 2 else -0.4)
    if mode in ("half", "mid", "full") and not in_wave:
        add(bass(root, BEAT * 0.46, 0.42), tb)
        add(bass(root + (12 if mode == "full" else 0), BEAT * 0.4, 0.28), tb + BEAT / 2)
    tb += BEAT

# ---- 0-4 spark
for p in PULSES:
    add(blip(81, 0.28), p); add(sub(45, 0.5, 0.35), p)
arp = [69, 72, 76, 81, 84, 88]
for i, m in enumerate(arp):
    add(pluck(m, 0.2, d=0.2, bright=2600 + 500 * i), CURVE[0] + i * 0.25, pan=-0.35 + 0.14 * i)
for i, tt in enumerate(TITLE):
    add(thock(0.35), tt + 0.15)
add_st(*sweep(1.0, 0.32), BASE - 1.0)

# ---- 4-12 type + data
for i in range(9):                           # light eighth-note shimmer while the letters rise
    root, ch = chord_at(BASE + i * BEAT)
    add(pluck(ch[(i % 3) + 1] + 12, 0.07, d=0.08, bright=2400), BASE + i * BEAT + BEAT / 2, pan=(-0.45, 0.45)[i % 2])


def stair_times():
    pts = [(3990, 3000), (4000, 3000), (4000, 2860), (4170, 2860), (4170, 2760), (4340, 2760), (4340, 2640),
           (4510, 2640), (4510, 2500), (4680, 2500), (4680, 2340), (4810, 2340)]
    cum = np.concatenate([[0], np.cumsum([np.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])])])
    out = []
    for i in range(5):
        j = next(k for k, p in enumerate(pts) if p[0] == 4000 + 170 * i)
        p = cum[j] / cum[-1]
        u = np.sqrt(p / 2) if p < 0.5 else 1 - np.sqrt((1 - p) / 2)    # invert power1.inOut
        out.append(STAIR[0] + (STAIR[1] - STAIR[0]) * u)
    return out


for i, tt in enumerate(stair_times()):        # each bar springs up on a rising note
    m = [69, 72, 74, 76, 79][i]
    add(pluck(m, 0.24, d=0.18, bright=3600), tt, pan=-0.3 + 0.15 * i)
    add(bell(m + 12, 0.1, dur=1.2), tt, pan=-0.3 + 0.15 * i)
for k in range(1, 13):                        # a tick for every hundred the counter passes
    u = 1 - np.sqrt(1 - k / 12)
    add(tick(0.1, f=2000 + 60 * k), COUNT[0] + (COUNT[1] - COUNT[0]) * u, pan=0.2)
add(blip(88, 0.16), COUNT[1])

# ---- 12-18 product
add_st(*whoosh(1.3, 0.75, 0.3, f1=4200), TOCARD[0] - 0.1)
for i, tt in enumerate(UI_POPS):
    root, ch = chord_at(tt)
    add(blip(ch[i % 4] + 12, 0.14), tt, pan=-0.3 + 0.12 * i)
add(tick(0.3, f=3000), SCAN[0])
add(zap(SCAN[1] - SCAN[0] + 0.15, 0.26), SCAN[0])
add(tick(0.25, f=2600), PRICE); add(tick(0.2, f=3100), PRICE + 0.07)
add(pluck(76, 0.18, d=0.16), PRICE + 0.05)
add(riser_tone(69, 81, PROG[1] - PROG[0] + 0.05, 0.1), PROG[0])
tt = PROG[0]
while tt < PROG[1] - 1e-6:                    # progress ticks speed up as the bar fills
    add(tick(0.09, f=2200 + 1400 * (tt - PROG[0])), tt, pan=0.15)
    tt += 0.125 if tt < PROG[0] + 0.5 else 0.0625
for m in (69, 76, 81): add(bell(m + 12, 0.16), PROG[1], pan=(m - 76) / 20)
for i in range(4):                            # fill into the drop
    add(snare(0.18 + 0.1 * i), 17.5 + i * 0.125)

# ---- 18-29 edit + formats
add(kick(1.0), DROP); add_st(*crash(0.22), DROP)
for i, tt in enumerate(BLOCKS): add(thock(0.18), tt, pan=-0.4 + 0.16 * i)
for c in CUTS: add(tick(0.24, f=2800), c); add(thock(0.15), c)
for i, tt in enumerate(KF):
    root, ch = chord_at(tt)
    add(blip(ch[(i % 3) + 1] + 24, 0.08), tt, pan=(-0.5, 0.5)[i % 2])
root, _ = chord_at(WAVE[0])
add(wobble(root, WAVE[1] - WAVE[0] + 0.1, rate=4.0, g=0.42), WAVE[0])
for i, tt in enumerate(FRAMES):
    root, ch = chord_at(tt)
    add(thock(0.35), tt); add(pluck(ch[3] + 12, 0.2, d=0.2), tt, pan=(-0.3, 0, 0.3)[i])

# ---- 29-34.5 reveal + mark (no drums: the pull-back breathes)
add(kick(0.95), LAUNCH); add_st(*crash(0.25, dur=3.0), LAUNCH)
add_st(*whoosh(2.4, 1.0, 0.42), LAUNCH)
add(sub(41, FINAL - LAUNCH, 0.32), LAUNCH)
for m, tt in zip((77, 81, 84), REVEAL):
    add(bell(m, 0.3, dur=2.6), tt, pan=(m - 81) / 14)
add_st(*sweep(FINAL - MARK[0], 0.5, fade=0.12), MARK[0])
add(riser_tone(55, 67, FINAL - MARK[0], 0.07), MARK[0])
tt, k = 33.0, 0
while tt < FINAL - 1e-6:                      # snare roll: eighths, then sixteenths
    add(snare(0.08 + 0.22 * (tt - 33.0) / 1.5), tt, pan=0.1)
    tt += 0.25 if tt < 33.75 else 0.125

# ---- 34.5-40 signature
add(kick(1.0), FINAL); add(boom(0.85), FINAL); add(clap(0.5), FINAL)
add_st(*crash(0.3, dur=3.4), FINAL)
add_st(*pad(AM9[1], TOTAL - FINAL, cutoff=2000, a=0.05, rel=3.0), FINAL, g=0.85)
add(sub(AM9[0] + 12, TOTAL - FINAL, 0.3), FINAL)
for k, m in enumerate((69, 72, 76, 81)):
    add(pluck(m, 0.14, d=0.22), FINAL + 0.5 + k * BEAT / 2, pan=(-0.3, 0.3)[k % 2])
add(bell(88, 0.16), CHIP, pan=0.2)
for i in range(URL[2]):
    add(tick(0.045, f=1800 + int(rng.integers(0, 600))), URL[0] + (URL[1] - URL[0]) * i / URL[2], pan=float(rng.uniform(-0.3, 0.3)))
add_st(*sweep(RULE[1] - RULE[0], 0.1, f0=3000, f1=9000, fade=0.4), RULE[0])
add(bell(93, 0.1, dur=2.0), NOTE, pan=-0.2)

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
mix /= np.max(np.abs(mix)) / PEAK   # PEAK sets the level: about -12 LUFS in the WAV, played at 0.65 (as productfilms-reel)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with wave.open(OUT, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix.T * 32767).astype("<i2").tobytes())
print("wrote", os.path.normpath(OUT), round(TOTAL, 2), "s")
