"""The score for R53 · Channels, composed in code at 96 bpm in D minor, the same family as R51 Hands Off and R52 Same Sand: plucked strings, a hand drum, and the sand itself as noise.
New here is the trickle: every stream is grain noise that follows the flow, so a channel can be heard opening, filling and splitting. At the fork the melody splits into two lines,
the failure is one bell over silence, and the shadow run plays the same phrase twice in unison until one copy is smoothed away.
Every sound is placed from the table. Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py"""
import json, math, os, re, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TB = json.loads(re.sub(r"^window\.TABLE=|;\s*$", "", open(os.path.join(ROOT, "assets", "table.js"), encoding="utf-8").read()))
SR = 48000; DUR = TB["dur"]; BEAT = TB["beat"]; N = int(SR * DUR)
B = lambda x: x * BEAT
out = np.zeros((N, 2))
ST = TB["streams"]


def add(at, sig, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N or i < 0: return
    sig = sig[:N - i]
    out[i:i + len(sig), 0] += sig * gain * math.cos((pan + 1) * math.pi / 4) * 1.41
    out[i:i + len(sig), 1] += sig * gain * math.sin((pan + 1) * math.pi / 4) * 1.41


def midi(m): return 440 * 2 ** ((m - 69) / 12)


_c = {}
def pluck(m, dur=1.3, bright=6, damp=0.996, det=1.0):
    """A plucked string (Karplus-Strong), worked out one period at a time."""
    k = (m, dur, bright, damp, det)
    if k not in _c:
        n = int(dur * SR); p = max(2, int(round(SR / (midi(m) * det)))); g = np.random.default_rng(m + int(det * 1000)); buf = np.convolve(g.uniform(-1, 1, p), np.ones(bright) / bright, "same") * 1.8; x = np.zeros(n)
        for i in range(0, n, p):
            e = min(p, n - i); x[i:i + e] = buf[:e]; buf = 0.5 * (buf + np.roll(buf, -1)) * damp
        t = np.arange(n) / SR
        _c[k] = x * np.minimum(1, t * 1200) * np.minimum(1, (dur - t) * 25)
    return _c[k]


def noise(n, seed): return np.random.default_rng(seed).normal(0, 1, n)


def band(x, lo, hi):
    f = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(f * np.exp(-((np.log(np.maximum(fr, 1)) - math.log(math.sqrt(lo * hi))) / (0.5 * math.log(hi / lo))) ** 2), len(x))


SAND = band(noise(SR * 4, 1), 2400, 11000); SAND /= np.abs(SAND).max()
LOWS = band(noise(SR * 4, 2), 300, 1800); LOWS /= np.abs(LOWS).max()
WATER = band(noise(SR * 6, 3), 900, 5200); WATER /= np.abs(WATER).max()


def sand(dur, seed=0, low=0.3):
    n = int(dur * SR); i = (seed * 9973) % (SR * 3); j = (seed * 4111) % (SR * 3)
    x = np.resize(SAND[i:], n) + low * np.resize(LOWS[j:], n)
    g = np.random.default_rng(seed).uniform(0.45, 1.0, n // 240 + 2); e = np.interp(np.arange(n), np.arange(len(g)) * 240, g)
    return x * e


def trickle(dur, seed=0, rate=1.0):
    """The new voice: grains running down a channel, a steady hiss full of tiny clicks, denser as more of them run."""
    n = int(dur * SR); i = (seed * 7919) % (SR * 5); x = np.resize(WATER[i:], n) * 0.5
    rng = np.random.default_rng(seed + 900); k = rng.random(n) < 0.0016 * rate
    clicks = np.convolve(k * rng.uniform(-1, 1, n), np.exp(-np.arange(60) / 9.0), "same")
    return x + clicks * 0.9


def drum(f=74.0, dur=0.5, drop=1.9, seed=0):
    t = np.arange(int(dur * SR)) / SR; ph = 2 * np.pi * np.cumsum(f * (1 + drop * np.exp(-t * 46))) / SR
    return np.sin(ph) * np.exp(-t * 7.5) + 0.22 * sand(dur, seed + 300, 1.0) * np.exp(-t * 80)


def tak(seed=0):
    t = np.arange(int(0.16 * SR)) / SR
    return (np.sin(2 * np.pi * 430 * t) * 0.55 + 0.7 * band(noise(len(t), seed + 40), 700, 4000) * 3) * np.exp(-t * 42)


def click(f=2400.0):
    t = np.arange(int(0.05 * SR)) / SR; return (np.sin(2 * np.pi * f * t) * 0.5 + noise(len(t), 8) * 0.5) * np.exp(-t * 240)


def bell(m=81, dur=4.0):
    """One bell: inharmonic partials that ring and fade."""
    t = np.arange(int(dur * SR)) / SR; f = midi(m); x = np.zeros(len(t))
    for q, a, d in ((1.0, 1.0, 1.2), (2.76, 0.5, 2.2), (5.4, 0.28, 3.5), (8.93, 0.14, 5.0), (0.5, 0.25, 0.9)): x += a * np.sin(2 * np.pi * f * q * t) * np.exp(-t * d)
    return x * np.minimum(1, t * 3000)


def breath(notes, dur, seed=0):
    t = np.arange(int(dur * SR)) / SR; x = np.zeros(len(t))
    for k, m in enumerate(notes):
        for q, a in ((1.0, 1.0), (1.004, 0.7), (2.0, 0.22), (0.5, 0.35)): x += a * np.sin(2 * np.pi * midi(m) * q * t + k + q * 3)
    x = x / len(notes); sw = np.clip(t / dur, 0, 1); env = sw ** 1.6 * np.minimum(1, (dur - t) * 30)
    return (x + band(noise(len(t), seed + 600), 500, 3000) * 0.25) * env


CH = [(38, [57, 62, 65, 69]), (34, [58, 62, 65, 70]), (41, [57, 60, 65, 69]), (36, [55, 60, 64, 67])]
def chord(b): return CH[int(b // 4) % 4]


F = ST["fail"]; FAT, CLR = F["at"], F["clear"]; ALERT = TB["alert"][2]; OPEN = ST["open"]; SH = ST["shadow"]; off = TB["clickOff"]
quiet = lambda b: FAT <= b < CLR + 0.2       # the failure: the music stops

# ---- light on
add(B(TB["clickOn"]), click(), 0.5, -0.2); add(B(TB["clickOn"]) + 0.01, click(900.0), 0.5, 0.2)
d = B(16.0 - 1.2); t = np.arange(int(d * SR)) / SR
add(B(1.2), np.sin(2 * np.pi * midi(38) * t) * np.minimum(1, t * 0.6) * np.minimum(1, (d - t) * 3), 0.13)

# ---- the work arriving in its piles, and the old furrow's trickle, stop and start
d = B(8.0 - 1.3); x = sand(d, 3, 0.4); t = np.arange(len(x)) / SR
add(B(1.3), x * np.minimum(1, t * 2) * np.minimum(1, (d - t) * 2) * (0.6 + 0.4 * np.sin(t * 5)), 0.07, -0.5)
for w0, w1 in ST["furTrickle"]:
    d = B(w1 - w0) + 3.0; x = trickle(d, int(w0 * 10), 0.5); t = np.arange(len(x)) / SR
    add(B(w0), x * (0.5 - 0.5 * np.cos(2 * np.pi * 0.9 * t / BEAT)) * np.minimum(1, (d - t) * 0.8), 0.07, 0.4)

# ---- the map: the fingertip's strokes, quick and dry, a pluck on each, and a tick to approve it
MAPN = [62, 65, 69, 67, 70, 69, 74]
k = 0
for kind, t0, t1 in TB["strokes"]:
    if kind in ("furrow", "sweep", "alert"): continue
    dd = B(t1 - t0) + 0.04; x = sand(dd, 40 + k, 0.35); tt = np.arange(len(x)) / SR
    add(B(t0), x * np.minimum(1, tt * 70) * np.minimum(1, (dd - tt) * 30), 0.14, -0.3 + 0.1 * k)
    if kind == "tick": add(B(t1), pluck(81, 1.8, 4, 0.998), 0.24, 0.2); add(B(t1), drum(66, 0.6, 2.0, 5), 0.3)
    else: add(B(t0), pluck(MAPN[k % 7], 1.1, 5, 0.997), 0.16, -0.3 + 0.1 * k)
    k += 1

# ---- the caption flows: the pad breathing in under each, as in Same Sand
for kk, (b0, b1, _) in enumerate(TB["captions"]):
    if b0 is None or quiet(b0): continue
    root, up = chord(b1); dd = B(b1 - b0)
    add(B(b0), breath([up[0] - 12, up[1] - 12, up[2] - 12], dd, kk), 0.07)
    x = sand(dd + 0.1, kk + 20, 0.5); tt = np.arange(len(x)) / SR
    add(B(b0), x * np.sin(np.clip(tt / dd, 0, 1) * math.pi) ** 1.3 * np.minimum(1, (dd + 0.1 - tt) * 20), 0.05, 0.0)

# ---- the channels open: a rush, then a steady stream, heard all the way to the light going off
d = B(off - OPEN); x = trickle(d, 77, 1.6); t = np.arange(len(x)) / SR; bt = OPEN + t / BEAT
env = np.minimum(1, t * 1.5) * (0.55 + 0.45 * np.exp(-np.maximum(0, bt - 21) * 0.6)) * np.where((bt >= FAT) & (bt < CLR), 0.45, 1.0)
add(B(OPEN), x * env, 0.10, -0.15)
add(B(OPEN), trickle(d, 78, 1.2) * env, 0.08, 0.25)
add(B(16.0), drum(52, 1.3, 2.6, seed=21), 0.5)
for m, pn in [(38, 0), (50, 0.1), (57, -0.2), (62, 0.2), (65, -0.3)]: add(B(16.0), pluck(m, 2.6, 5, 0.998), 0.18, pn)


def groove(b0, b1, busy, split=False):
    """The strings in eighths and the sand as a shaker. At the fork the melody splits into two lines, left and right."""
    for s16 in range(int(b0 * 4), int(b1 * 4)):
        b = s16 / 4; root, up = chord(b); ib = int(b); frac = s16 % 4
        if quiet(b): continue
        if busy or frac % 2 == 0:
            ln = 0.05 + 0.03 * (frac == 2); add(B(b), sand(ln, s16 % 37 + 90, 0.1) * np.exp(-np.arange(int(ln * SR)) / SR * 70), (0.14 if frac == 2 else 0.07), 0.3 if frac % 2 else -0.3)
        if frac == 0 and ib % 2 == 1: add(B(b), tak(ib), 0.15, 0.1)
        if frac in (0, 2):
            m = up[(s16 // 2) % 4]
            if split: add(B(b), pluck(m, 0.5, 5, 0.99), 0.1, -0.6); add(B(b + 0.25), pluck(up[(s16 // 2 + 2) % 4] + 12, 0.45, 4, 0.99), 0.08, 0.6)
            else: add(B(b), pluck(m, 0.5, 5, 0.99), 0.12, 0.45 * math.sin(s16 * 1.7))
        if frac == 0 and ib % 4 == 0: add(B(b), pluck(root, 1.2, 8, 0.995), 0.3, -0.05); add(B(b), drum(64, 0.5, 2.0, seed=ib), 0.32)


groove(18.0, 20.0, False)
groove(20.0, 30.0, True, split=True)

# ---- to the right person: a bright figure as the pulse lands
pa = ST["personAt"]
for q, m in enumerate([74, 77, 81, 86]): add(B(pa - 0.75 + q * 0.25), pluck(m, 1.4, 4, 0.998), 0.16, 0.5)
add(B(pa), drum(70, 0.6, 2.2, seed=31), 0.36)

# ---- when it fails: the grains back up, the music stops, one bell
dd = B(0.5); x = sand(dd, 61, 0.9); tt = np.arange(len(x)) / SR
add(B(FAT), x * np.minimum(1, tt * 40) * np.exp(-tt * 3), 0.24, 0.3)
add(B(FAT), drum(46, 1.2, 1.2, seed=62), 0.34)
add(B(ALERT), bell(81, 5.0), 0.2, 0.25)
add(B(ALERT + 0.02), bell(69, 4.0), 0.07, -0.2)
# the fingertip clears it, and everything comes back
dd = B(0.4); x = sand(dd, 63, 0.4); tt = np.arange(len(x)) / SR
add(B(CLR - 0.3), x * np.minimum(1, tt * 60) * np.minimum(1, (dd - tt) * 20), 0.2, 0.3)
add(B(CLR + 0.2), drum(58, 0.9, 2.2, seed=64), 0.44)
for m, pn in [(41, 0), (53, 0.1), (60, -0.2), (65, 0.2), (69, -0.1)]: add(B(CLR + 0.2), pluck(m, 2.2, 5, 0.998), 0.18, pn)
groove(36.0, 38.0, False)

# ---- the shadow run: one phrase twice in unison, the old way on the left and the new way on the right, landing together
PHR = [62, 65, 69, 74]
for k, a in enumerate(SH):
    for q, m in enumerate(PHR): add(B(a - 1.0 + q * 0.25), pluck(m + (0 if k < 2 else 2), 0.9, 5, 0.997), 0.13, -0.55); add(B(a - 1.0 + q * 0.25), pluck(m + (0 if k < 2 else 2), 0.9, 5, 0.997, 1.003), 0.13, 0.55)
    add(B(a), drum(60, 0.6, 2.0, seed=70 + k), 0.24, -0.4); add(B(a), drum(60.4, 0.6, 2.0, seed=74 + k), 0.24, 0.4)
groove(38.0, 43.0, False)
# the old furrow smoothed away, and the left copy goes with it
dd = B(44.6 - 43.0); x = sand(dd, 81, 0.5); tt = np.arange(len(x)) / SR
add(B(43.0), x * np.minimum(1, tt * 20) * np.minimum(1, (dd - tt) * 10) * (0.7 + 0.3 * np.sin(tt * 14)), 0.18, -0.4)
for q, m in enumerate(PHR): add(B(44.0 + q * 0.25), pluck(m + 12, 1.1, 4, 0.997), 0.15, 0.3)

# ---- yours, and the end
groove(44.0, 52.0, True)
add(B(52.0), drum(52, 1.3, 2.6, seed=91), 0.5)
for m, pn in [(38, 0), (50, 0.1), (57, -0.2), (62, 0.2), (65, -0.3), (69, 0.3)]: add(B(52.0), pluck(m, 2.6, 5, 0.998), 0.2, pn)
for q, m in enumerate([69, 74, 77, 81]): add(B(52.5 + q * 0.33), pluck(m, 1.6, 4, 0.998), 0.11, -0.3 + q * 0.2)

stop = int(B(off) * SR); fade = np.ones(N); fade[stop:] = 0.0; fade[stop - 200:stop] = np.linspace(1, 0, 200); out *= fade[:, None]
add(B(off), click(), 0.55); add(B(off) + 0.01, click(900.0), 0.5)
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
