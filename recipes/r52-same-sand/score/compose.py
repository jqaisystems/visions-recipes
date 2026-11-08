"""The score for R52 · Same Sand, composed in code at 96 bpm in D minor, the same family as R51 Hands Off: plucked strings, a hand drum, and the sand itself as noise.
New here is a soft pad that breathes in under every flow and lands with it, a note for each format that climbs as the formats change,
the same four notes in four registers for the four languages, and the pluck alone for the review.
Every sound is placed from the table. Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py"""
import json, math, os, re, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TB = json.loads(re.sub(r"^window\.TABLE=|;\s*$", "", open(os.path.join(ROOT, "assets", "table.js"), encoding="utf-8").read()))
SR = 48000; DUR = TB["dur"]; BEAT = TB["beat"]; N = int(SR * DUR)
B = lambda x: x * BEAT
out = np.zeros((N, 2))


def add(at, sig, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N or i < 0: return
    sig = sig[:N - i]
    out[i:i + len(sig), 0] += sig * gain * math.cos((pan + 1) * math.pi / 4) * 1.41
    out[i:i + len(sig), 1] += sig * gain * math.sin((pan + 1) * math.pi / 4) * 1.41


def midi(m): return 440 * 2 ** ((m - 69) / 12)


_c = {}
def pluck(m, dur=1.3, bright=6, damp=0.996):
    """A plucked string (Karplus-Strong), worked out one period at a time."""
    k = (m, dur, bright, damp)
    if k not in _c:
        n = int(dur * SR); p = max(2, int(round(SR / midi(m)))); g = np.random.default_rng(m); buf = np.convolve(g.uniform(-1, 1, p), np.ones(bright) / bright, "same") * 1.8; x = np.zeros(n)
        for i in range(0, n, p):
            e = min(p, n - i); x[i:i + e] = buf[:e]; buf = 0.5 * (buf + np.roll(buf, -1)) * damp
        t = np.arange(n) / SR
        _c[k] = x * np.minimum(1, t * 1200) * np.minimum(1, (dur - t) * 25)
    return _c[k]


def noise(n, seed): return np.random.default_rng(seed).normal(0, 1, n)


def band(x, lo, hi):
    """A plain FFT band-pass."""
    f = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(f * np.exp(-((np.log(np.maximum(fr, 1)) - math.log(math.sqrt(lo * hi))) / (0.5 * math.log(hi / lo))) ** 2), len(x))


SAND = band(noise(SR * 4, 1), 2400, 11000); SAND /= np.abs(SAND).max()
LOWS = band(noise(SR * 4, 2), 300, 1800); LOWS /= np.abs(LOWS).max()


def sand(dur, seed=0, low=0.3):
    """Sand moving: bright noise with a little body, full of tiny uneven grains."""
    n = int(dur * SR); i = (seed * 9973) % (SR * 3); j = (seed * 4111) % (SR * 3)
    x = np.resize(SAND[i:], n) + low * np.resize(LOWS[j:], n)
    g = np.random.default_rng(seed).uniform(0.45, 1.0, n // 240 + 2); e = np.interp(np.arange(n), np.arange(len(g)) * 240, g)
    return x * e


def drum(f=74.0, dur=0.5, drop=1.9, seed=0):
    """A hand drum: a low skin that bends, with the slap of a palm on it."""
    t = np.arange(int(dur * SR)) / SR; ph = 2 * np.pi * np.cumsum(f * (1 + drop * np.exp(-t * 46))) / SR
    return np.sin(ph) * np.exp(-t * 7.5) + 0.22 * sand(dur, seed + 300, 1.0) * np.exp(-t * 80)


def tak(seed=0):
    t = np.arange(int(0.16 * SR)) / SR
    return (np.sin(2 * np.pi * 430 * t) * 0.55 + 0.7 * band(noise(len(t), seed + 40), 700, 4000) * 3) * np.exp(-t * 42)


def click(f=2400.0):
    t = np.arange(int(0.05 * SR)) / SR; return (np.sin(2 * np.pi * f * t) * 0.5 + noise(len(t), 8) * 0.5) * np.exp(-t * 240)


def breath(notes, dur, seed=0):
    """The new voice: a soft pad that swells in over the flow and is gone the moment it lands."""
    t = np.arange(int(dur * SR)) / SR; x = np.zeros(len(t))
    for k, m in enumerate(notes):
        for q, a in ((1.0, 1.0), (1.004, 0.7), (2.0, 0.22), (0.5, 0.35)): x += a * np.sin(2 * np.pi * midi(m) * q * t + k + q * 3)
    x = x / len(notes)
    sw = np.clip(t / dur, 0, 1); env = sw ** 1.6 * np.minimum(1, (dur - t) * 30)
    air = band(noise(len(t), seed + 600), 500, 3000) * 0.25
    return (x + air) * env


# ---- the harmony, four beats a bar: Dm, Bb, F, C
CH = [(38, [57, 62, 65, 69]), (34, [58, 62, 65, 70]), (41, [57, 60, 65, 69]), (36, [55, 60, 64, 67])]
def chord(b): return CH[int(b // 4) % 4]


rev0, rev1 = TB["review"]; off = TB["clickOff"]

# ---- light on, and the pour
add(B(TB["clickOn"]), click(), 0.5, -0.2)
add(B(TB["clickOn"]) + 0.01, click(900.0), 0.5, 0.2)
for k, (p0, p1, x0, y0, tint) in enumerate(TB["pours"]):
    d = B(p1 - p0) + 0.4; x = sand(d, 5 + k, 0.9 if not tint else 0.3); t = np.arange(len(x)) / SR
    add(B(p0), x * np.minimum(1, t * 6) * (0.8 + 0.2 * np.sin(t * 7)) * np.minimum(1, (d - t) * 2.2), 0.2 if not tint else 0.16, 0.0 if not tint else -0.3)
    if tint:
        for q, m in enumerate([74, 77, 81]): add(B(p0 + q * 0.5), pluck(m, 1.8, 4, 0.998), 0.12, -0.3 + q * 0.2)
d = B(4.6 - 1.2); t = np.arange(int(d * SR)) / SR
add(B(1.2), np.sin(2 * np.pi * midi(38) * t) * np.minimum(1, t * 0.6) * np.minimum(1, (d - t) * 3), 0.16)

# ---- every flow: the sand travelling, the pad breathing in under it, and a landing exactly on the beat
FORMAT_NOTES = {16.0: 62, 20.0: 65, 24.0: 69, 28.0: 74}      # a note for each format, climbing
for k, (b0, b1, pic, travel) in enumerate(TB["morphs"]):
    d = B(b1 - b0); x = sand(d + 0.1, k + 20, 0.5); t = np.arange(len(x)) / SR; u = t / d
    env = np.sin(np.clip(u, 0, 1) * math.pi) ** 1.3 * np.minimum(1, (d + 0.1 - t) * 20)
    review = rev0 <= b0 < rev1
    add(B(b0), x * env, 0.11 * travel * (0.6 if review else 1.0), (k % 5 - 2) * 0.15)
    root, up = chord(b1)
    add(B(b0), breath([up[0] - 12, up[1] - 12, up[2] - 12], d, k), 0.1 * (0.5 if review else 1.0), 0.0)
    if not review:
        add(B(b1), drum(66, 0.6, 2.0, seed=k), 0.42)
        add(B(b1), pluck(root, 1.6, 8, 0.997), 0.3, -0.05)
    if b0 in FORMAT_NOTES: add(B(b1), pluck(FORMAT_NOTES[b0], 2.4, 5, 0.998), 0.26, 0.15)

# ---- the groove under the formats and the month: the sand as a shaker, the strings in eighths
def groove(b0, b1, busy):
    for s16 in range(int(b0 * 4), int(b1 * 4)):
        b = s16 / 4; root, up = chord(b); ib = int(b); frac = s16 % 4
        if busy or frac % 2 == 0:
            ln = 0.05 + 0.03 * (frac == 2); add(B(b), sand(ln, s16 % 37 + 90, 0.1) * np.exp(-np.arange(int(ln * SR)) / SR * 70), (0.16 if frac == 2 else 0.08), 0.3 if frac % 2 else -0.3)
        if frac == 0 and ib % 2 == 1: add(B(b), tak(ib), 0.16, 0.1)
        if frac in (0, 2): add(B(b), pluck(up[(s16 // 2) % 4], 0.5, 5, 0.99), 0.12, 0.45 * math.sin(s16 * 1.7))
        if frac == 0 and ib % 4 == 0: add(B(b), pluck(root, 1.2, 8, 0.995), 0.3, -0.05)


groove(5.0, 16.0, False)
groove(16.0, 31.0, True)

# ---- four languages: the same four notes, a register higher each time
MOTIF = [62, 65, 69, 67]
for i, b in enumerate(TB["langs"]):
    for q, m in enumerate(MOTIF): add(B(b - 1.0 + q * 0.25), pluck(m + 12 * (i - 1) if i else m - 12, 1.4, 5, 0.997), 0.2, -0.3 + q * 0.2)
    add(B(b), drum(60 + i * 4, 0.5, 2.0, seed=40 + i), 0.36)

# ---- the review: the music drops to the pluck alone, and every touch of the finger is heard
for b in range(int(rev0) + 1, int(rev1)):
    root, up = chord(b)
    if b % 2 == 0: add(B(b), pluck(root + 12, 1.8, 8), 0.24, -0.1)
    add(B(b + 0.5), pluck(up[b % 4], 0.9, 6), 0.08, 0.2)
for k, (b0, b1, kind) in enumerate(TB["taps"]):
    d = B(b1 - b0) + 0.05; x = sand(d, 70 + k, 0.4); t = np.arange(len(x)) / SR
    add(B(b0), x * np.minimum(1, t * 80) * np.minimum(1, (d - t) * 30), 0.2 if kind == 0 else 0.26, 0.2)
    if kind == 0: add(B(b1), pluck(74 + 3 * k, 1.2, 4, 0.997), 0.18, 0.25)
    else: add(B(b0), pluck(46, 1.6, 9, 0.99), 0.3, -0.1)

# ---- the month, and the end
groove(rev1, 50.0, True)
add(B(52.0), drum(52, 1.3, 2.6, seed=21), 0.6)
for m, pn in [(38, 0), (50, 0.1), (57, -0.2), (62, 0.2), (65, -0.3), (69, 0.3)]: add(B(52.0), pluck(m, 2.6, 5, 0.998), 0.2, pn)
for q, m in enumerate([69, 74, 77, 81]): add(B(52.0 + 0.5 + q * 0.33), pluck(m, 1.6, 4, 0.998), 0.12, -0.3 + q * 0.2)

# ---- light off, and one last chord on the mark
stop = int(B(off) * SR); fade = np.ones(N); fade[stop:] = 0.0; fade[stop - 200:stop] = np.linspace(1, 0, 200); out *= fade[:, None]
add(B(off), click(), 0.55)
add(B(off) + 0.01, click(900.0), 0.5)
add(B(TB["logo"]), drum(52, 1.2, 1.6, seed=9), 0.4)
for m, pn in [(38, 0), (50, -0.1), (57, 0.1), (65, -0.25), (69, 0.25), (74, 0.05)]: add(B(TB["logo"]), pluck(m, 2.9, 7, 0.999), 0.24, pn)

# ---- a small room, and the master
L = int(0.34 * SR); ir = np.random.default_rng(11).normal(0, 1, L) * np.exp(-np.arange(L) / SR * 14)
for c in (0, 1):
    wet = np.fft.irfft(np.fft.rfft(out[:, c], N + L) * np.fft.rfft(np.roll(ir, c * 7), N + L), N + L)[:N]
    out[:, c] += wet * 0.016
out = np.tanh(out * 1.05)
tail = int(0.25 * SR); out[-tail:] *= np.linspace(1, 0, tail)[:, None]
pk = np.abs(out).max(); out = out / pk * 0.76
print("score", round(N / SR, 3), "peak", pk)
os.makedirs(os.path.join(ROOT, "assets", "bgm"), exist_ok=True)
w = wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
