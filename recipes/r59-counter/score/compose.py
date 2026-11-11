"""The score for R59 · Counter, composed in code from assets/table.js: a tight electronic groove at 120 bpm in D minor, built
around the one camera move. Every dive is a rising sweep that lands on an impact; every counter opening is a small pop; the scenes
play their own parts on the grid: keystrokes, dial ratchets, a snare for every cliché struck out, plucked notes as the network grows,
card flicks, and the chain's arrows. The drums drop out for the close and a chord brings in the mark.
Needs NumPy. Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py"""
import json, os, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.loads(open(os.path.join(ROOT, "assets", "table.js"), encoding="utf-8").read()[len("window.TABLE="):-1])
SR = 48000; BEAT = T["beat"]; DUR = T["dur"]; N = int(DUR * SR)
out = np.zeros((N, 2)); t = np.arange(N) / SR
rng = np.random.default_rng(591)
sec = lambda b: b * BEAT
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
A = [a - (T["lead"] if k else 0) for k, a in enumerate(T["arrive"])]; DV = T["dives"]   # each scene's own clock starts LEAD beats before it lands


def put(x, at, pan=0.0, g=1.0):
    i = int(round(at * SR))
    if i >= N or i + len(x) <= 0: return
    a, b = max(0, i), min(N, i + len(x)); seg = x[a - i:b - i] * g
    out[a:b, 0] += seg * np.sqrt(0.5 * (1 - pan)); out[a:b, 1] += seg * np.sqrt(0.5 * (1 + pan))


def lp(x, c):
    y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)): acc += c * (x[i] - acc); y[i] = acc
    return y


def env(n, a, d):
    tt = np.arange(n) / SR; return np.minimum(1, tt / max(a, 1e-4)) * np.exp(-tt / d)


def kick(at, g=1.0):
    n = int(0.42 * SR); tt = np.arange(n) / SR; f = 46 + 110 * np.exp(-tt / 0.035)
    put(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.16) + rng.standard_normal(n) * np.exp(-tt / 0.002) * 0.25, at, 0, g)


def hat(at, g=1.0, d=0.03):
    n = int(0.12 * SR); x = rng.standard_normal(n); x = x - lp(x, 0.35); put(x * env(n, 0.0005, d), at, 0.25, g)


def clap(at, g=1.0, pan=0.0):
    n = int(0.3 * SR); tt = np.arange(n) / SR; x = rng.standard_normal(n); x = x - lp(x, 0.08)
    e = sum(np.exp(-np.maximum(0, tt - o) / 0.008) * (tt >= o) for o in (0, 0.011, 0.022)) * 0.5 + np.exp(-tt / 0.09) * (tt >= 0.03)
    put(x * e * 0.8, at, pan, g)


def bass(m, at, dur, g=1.0):
    n = int(dur * SR); tt = np.arange(n) / SR; f = hz(m); ph = 2 * np.pi * f * tt
    x = np.sin(ph) + 0.3 * np.sin(2 * ph) + 0.12 * np.tanh(3 * np.sin(ph)); put(x * np.minimum(1, tt / 0.004) * np.exp(-tt / (dur * 0.9)), at, 0, g)


def pluck(m, at, g=1.0, pan=0.0, d=0.5):
    p = max(2, int(SR / hz(m))); n = int(d * 2.5 * SR); buf = rng.uniform(-1, 1, p); y = np.zeros(n)
    for i in range(n): y[i] = buf[i % p]; buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.995
    put(y * np.exp(-np.arange(n) / SR / d), at, pan, g)


def pad(ms, at, dur, g=1.0):
    n = int(dur * SR); tt = np.arange(n) / SR; x = np.zeros(n)
    for k, m in enumerate(ms):
        f = hz(m)
        for dt in (-0.12, 0.12): x += np.sin(2 * np.pi * f * (1 + dt / 100) * tt + k) + 0.25 * np.sin(2 * np.pi * 2 * f * tt)
    e = np.minimum(1, tt / 0.25) * np.minimum(1, (dur - tt) / 0.3); put(lp(x, 0.08) * e / len(ms), at, 0, g)


def click(at, g=1.0, f=3200, pan=0.0):
    n = int(0.04 * SR); tt = np.arange(n) / SR; put(np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.004) + rng.standard_normal(n) * np.exp(-tt / 0.001) * 0.4, at, pan, g)


def riser(t0, t1, g=1.0):
    n = int((t1 - t0) * SR); u = np.arange(n) / n; x = rng.standard_normal(n)
    y = np.zeros(n); acc = 0.0; c = 0.01 + 0.5 * u ** 2
    for i in range(n): acc += c[i] * (x[i] - acc); y[i] = acc
    tone = np.sin(2 * np.pi * np.cumsum(hz(50 + 24 * u ** 1.5)) / SR) * 0.3
    put((y * 1.6 + tone) * u ** 1.8, t0, 0, g)


def impact(at, g=1.0):
    n = int(1.6 * SR); tt = np.arange(n) / SR
    boom = np.sin(2 * np.pi * np.cumsum(38 + 70 * np.exp(-tt / 0.06)) / SR) * np.exp(-tt / 0.5)
    crash = rng.standard_normal(n); crash = (crash - lp(crash, 0.25)) * np.exp(-tt / 0.45) * 0.35
    put(boom + crash, at, 0, g)


def pop(at, m=86, g=1.0):
    n = int(0.25 * SR); tt = np.arange(n) / SR; f = hz(m) * (0.5 + 0.5 * np.minimum(1, tt / 0.05))
    put(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.07), at, 0, g)


# ---------------- the groove: kick on the beat, hats on the offbeat, claps on 2 and 4, bass and pad in D minor (Dm, Bb, F, C)
PROG = [[50, 53, 57], [46, 50, 53], [53, 57, 60], [48, 52, 55]]
G0, G1 = T["arrive"][1], T["close"][0][0]                  # the groove starts at the first landing and stops for the close
dives = [(sec(a), sec(b)) for a, b in DV]
in_dive = lambda s: any(a <= s < b for a, b in dives)
b = G0
while b < G1:
    s = sec(b); bar = int((b - G0) // 4) % 4; pos = (b - G0) % 4
    duck = 0.35 if in_dive(s) else 1.0
    kick(s, 0.9 * duck); hat(s + BEAT / 2, 0.22 * duck)
    if pos in (1, 3) and b >= T["arrive"][2]: clap(s, 0.45 * duck)
    root = PROG[bar][0] - 12
    for q in range(2): bass(root + (7 if (pos == 3 and q == 1) else 0), s + q * BEAT / 2, BEAT / 2 * 0.9, 0.42 * duck)
    if pos == 0: pad([m + 12 for m in PROG[bar]], s, 4 * BEAT, 0.16)
    b += 1
# ---------------- scene 0: a low pad under the typing, and every keystroke
pad([62, 65, 69], 0.0, sec(T["arrive"][1]), 0.12)
for i, ch in enumerate(T["prompt"]):
    if ch != " ": click(sec(T["type0"] + i * T["typeStep"]), 0.35, rng.uniform(2400, 4200), rng.uniform(-0.3, 0.3))
# ---------------- the dives and the landings, and the pop as each counter opens
for (d0, d1), o in zip(DV, T["open"]):
    riser(sec(d0) - 0.2, sec(d1), 0.5); impact(sec(d1), 0.75); pop(sec(o), 86, 0.25)
# ---------------- scene 1: the dials ratchet as they turn
for i, K in enumerate(T["knobs"]):
    for a, c in zip(K, K[1:]):
        if a[1] != c[1]:
            for q in range(10): click(sec(A[1] + a[0] + (c[0] - a[0]) * q / 10), 0.16, 5200, -0.3 + 0.3 * i)
# ---------------- scene 2: a snare and a zap for every cliché struck out
for i in range(len(T["cliches"])):
    s = sec(A[2] + T["strike0"] + i * 0.5); clap(s, 0.6, -0.4 if i % 2 == 0 else 0.4)
    n = int(0.15 * SR); tt = np.arange(n) / SR; put(np.sign(np.sin(2 * np.pi * (900 - 2500 * tt) * tt)) * np.exp(-tt / 0.04) * 0.15, s, 0, 1)
# ---------------- scene 3: plucked notes as the network grows
PENTA = [62, 65, 67, 69, 72, 74, 77]
for i in range(3): pluck(PENTA[i * 2] + 12, sec(A[3] + T["node0"] + i * 0.75 + 0.5), 0.3, [-0.5, 0.5, 0.2][i], 0.7)
for i in range(18): pluck(PENTA[int(rng.integers(len(PENTA)))] + 12, sec(A[3] + T["node0"] + 1 + i * 0.3), 0.12, rng.uniform(-0.7, 0.7), 0.3)
# ---------------- scene 4: a card flick for every card dealt, and the flips
for i in range(20):
    s = sec(A[4] + T["deal0"] + i * T["dealStep"] + 0.3); n = int(0.06 * SR); x = rng.standard_normal(n); put((x - lp(x, 0.2)) * env(n, 0.001, 0.015), s, (i % 5 - 2) / 3, 0.35)
    col, row = i % 5, i // 5; click(sec(A[4] + T["flip0"] + col * 0.15 + row * 0.12 + 0.25), 0.12, 1800, (col - 2) / 3)
# ---------------- scene 5: the chain's arrows, and the rewrite typed
for i, c in enumerate(T["chain"]):
    pluck([57, 62, 69][i] + 12, sec(A[5] + c - 0.2), 0.3, -0.5 + 0.5 * i, 0.6)
for q in range(24): click(sec(A[5] + T["chain"][2] + q / 28), 0.12, rng.uniform(2600, 4000))
# ---------------- the close: a hit under each line, then the chord for the mark
for b0, s in T["close"]:
    impact(sec(b0), 0.35); pluck(74, sec(b0), 0.25, 0, 0.8)
pad([50, 57, 62, 65, 69], sec(T["logo"]), DUR - sec(T["logo"]), 0.3)
for k, m in enumerate([62, 69, 74, 77]): pluck(m, sec(T["logo"]) + 0.05 * k, 0.22, -0.3 + 0.2 * k, 1.4)

# ---------------- master: a short room, glue, and the level
ir_n = int(0.6 * SR); ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR / 0.14); ir /= np.sqrt(np.sum(ir ** 2))
for ch in range(2):
    f = np.fft.rfft(out[:, ch], N + ir_n); out[:, ch] += 0.1 * np.fft.irfft(f * np.fft.rfft(ir, N + ir_n))[:N]
out = np.tanh(out / np.max(np.abs(out)) * 1.6) / np.tanh(1.6)
out *= np.clip((DUR - t) / 0.5, 0, 1)[:, None]
out *= 10 ** (-1.5 / 20) / np.max(np.abs(out))
pcm = (np.clip(out, -1, 1) * 32767).astype("<i2")
os.makedirs(os.path.join(ROOT, "assets", "bgm"), exist_ok=True)
with wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("score", round(DUR, 2), "s, peak -1.5 dBFS")
