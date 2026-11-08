"""The score for R54 alternative · Register, composed in code from assets/table.js: a printing press at 120 bpm.
The press is the kick, paper is the hats, every slam is a hit and every plate locking into register is a clack of metal.
Whips are air, the roller is a rumble that crosses the stereo field, the noise is static, and each line of the briefing is a stamp and a bell.
Needs NumPy. Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py"""
import json, os, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.loads(open(os.path.join(ROOT, "assets", "table.js"), encoding="utf-8").read()[len("window.TABLE="):-1])
SR = 48000; BEAT = T["beat"]; DUR = T["dur"]; N = int(DUR * SR)
out = np.zeros((N, 2)); rng = np.random.default_rng(54)
sec = lambda b: b * BEAT
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
tt = lambda d: np.arange(int(d * SR)) / SR


def put(x, t, pan=0.0, g=1.0):
    i = int(round(t * SR))
    if i >= N or i + len(x) <= 0: return
    a, b = max(0, i), min(N, i + len(x)); seg = x[a - i:b - i] * g
    out[a:b, 0] += seg * np.sqrt(0.5 * (1 - pan)); out[a:b, 1] += seg * np.sqrt(0.5 * (1 + pan))


def lp(x, k):   # a one-pole low-pass, k from 0 to 1 (per-sample array or constant)
    y = np.zeros_like(x); acc = 0.0; k = np.broadcast_to(k, x.shape)
    for i in range(len(x)): acc += k[i] * (x[i] - acc); y[i] = acc
    return y


# ---------------- the instruments
t = tt(0.5); KICK = np.sin(2 * np.pi * np.cumsum(48 + 110 * np.exp(-t / 0.035)) / SR) * np.exp(-t / 0.2) * 0.9
t = tt(0.06); HAT = lp(rng.standard_normal(len(t)), 0.9) * np.exp(-t / 0.012); HAT -= lp(HAT, 0.2); HAT *= 0.35
t = tt(0.25); SNAP = (lp(rng.standard_normal(len(t)), 0.6) * np.exp(-t / 0.05) * 0.6 + np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05) * 0.4)
t = tt(1.4); BOOM = np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-t / 0.08)) / SR) * np.exp(-t / 0.5)
t = tt(0.5)
CLACK = sum(np.sin(2 * np.pi * f * t) * np.exp(-t / d) for f, d in ((1760, 0.09), (2830, 0.05), (4410, 0.03), (6020, 0.02))) * 0.25
CLACK[:int(0.004 * SR)] += rng.standard_normal(int(0.004 * SR)) * 0.6
t = tt(0.08); FLICK = lp(rng.standard_normal(len(t)), 0.5) * np.exp(-t / 0.02) * 0.6


def bell(m, at, g=1.0, d=1.2, pan=0.0):
    t = tt(d * 3); f = hz(m)
    x = np.sin(2 * np.pi * f * t) * np.exp(-t / d) + 0.4 * np.sin(2 * np.pi * f * 3.0 * t) * np.exp(-t / (d * 0.25)) + 0.15 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t / (d * 0.08))
    put(x * np.minimum(1, t / 0.002), at, pan, g)


def bass(m, at, d, g=0.5):
    t = tt(d); f = hz(m); x = np.sign(np.sin(2 * np.pi * f * t)) * 0.5 + np.sin(2 * np.pi * f * t)
    x = lp(x, 0.06 + 0.25 * np.exp(-t / 0.06)) * np.minimum(1, t / 0.004) * np.exp(-t / 0.35)
    put(x, at, 0.0, g)


def air(t0, t1, up=True, g=0.5, pan0=0.0, pan1=0.0):   # a whoosh: noise through a filter that opens or closes
    n = int((t1 - t0) * SR); u = np.arange(n) / n; k = (0.02 + 0.5 * (u if up else 1 - u) ** 2)
    x = lp(rng.standard_normal(n), k) * np.sin(np.pi * u) ** 1.5
    for i, pn in enumerate((pan0, pan1)): pass
    L = x * np.sqrt(0.5 * (1 - np.linspace(pan0, pan1, n))); R = x * np.sqrt(0.5 * (1 + np.linspace(pan0, pan1, n)))
    i = int(t0 * SR); e = min(N, i + n); out[i:e, 0] += L[:e - i] * g; out[i:e, 1] += R[:e - i] * g


SC = T["sc"]
# ---------------- 1 the dive: a rising tone out of one dot, and the plates lock with a clack
t = tt(sec(6)); f = 110 * 2 ** (t / sec(6) * 2)
put(np.sin(2 * np.pi * np.cumsum(f) / SR) * (t / sec(6)) ** 2 * 0.25, 0.0)
air(sec(0.0), sec(5.8), True, 0.35, -0.4, 0.4)
put(CLACK, sec(T["locks"][0]), 0.0, 1.0); put(BOOM, sec(T["locks"][0]), 0.0, 0.5)
for b in (1.0,): put(SNAP, sec(b), 0.0, 0.6)

# ---------------- the groove: press, paper, bass. D minor, a bar of i, VI, III, VII
PROG = [38, 34, 41, 36]
def groove(b0, b1, kick=True, hats=True, bassline=True, g=1.0):
    for b in np.arange(b0, b1, 0.5):
        bar = int(b // 4) % 4; step = b % 4
        if kick and step in (0, 1, 2, 3): put(KICK, sec(b), 0.0, 0.8 * g)
        if hats: put(HAT, sec(b + 0.25), 0.35, 0.5 * g); put(HAT, sec(b), -0.35, 0.25 * g)
        if bassline: bass(PROG[bar] + (12 if step in (1.5, 3.5) else 0), sec(b), sec(0.45), 0.42 * g)
        if kick and step in (1, 3): put(SNAP, sec(b), 0.1, 0.45 * g)

groove(8, 20, g=1.0)
for b in T["slams"]: put(BOOM, sec(b), 0.0, 0.55); put(SNAP, sec(b), 0.0, 0.5); put(CLACK, sec(b), (b % 2) - 0.5, 0.25)
# the noise: static rising, until the collapse
n = int(sec(4.5) * SR); s = rng.standard_normal(n) * (np.arange(n) / n) ** 2; s = s * (rng.random(n) < 0.08)
put(s * 0.5, sec(15.5), 0.0)
air(sec(19.4), sec(20.2), False, 0.8)
put(BOOM, sec(20.0), 0.0, 0.7)

# ---------------- 2 the key plate: the groove drops away; a soft pulse, and a pen tick for each line of the document
for b in np.arange(20, 28, 1.0): put(KICK, sec(b), 0.0, 0.25)
for sc_ in range(3):
    t0 = 21.0 + sc_ * 1.6; put(SNAP, sec(t0), -0.2, 0.25)
    for k in range(4): put(FLICK, sec(t0 + 0.3 + k * 0.25), 0.3, 0.6)
bell(62, sec(20.6), 0.18, 2.0); bell(69, sec(24.0), 0.16, 2.0)

# ---------------- 3 the sweep: colour back, static, the roller crosses left to right, then three locks
groove(28, 38, kick=True, hats=True, bassline=True, g=0.85)
n = int(sec(4.2) * SR); s = rng.standard_normal(n) * (rng.random(n) < 0.08); put(s * 0.45 * np.linspace(1, 0.4, n), sec(28), 0.0)
sw = T["sweep"]; n = int(sec(sw[1] - sw[0]) * SR); rum = lp(rng.standard_normal(n), 0.03) * 3.0 * np.sin(np.pi * np.arange(n) / n) ** 0.5
pan = np.linspace(-0.95, 0.95, n); i = int(sec(sw[0]) * SR); out[i:i + n, 0] += rum * np.sqrt(0.5 * (1 - pan)) * 0.6; out[i:i + n, 1] += rum * np.sqrt(0.5 * (1 + pan)) * 0.6
for j, b in enumerate(T["locks"][1:4]): put(CLACK, sec(b), -0.5 + j * 0.5, 1.0); bell([62, 65, 69][j], sec(b), 0.22, 0.8, -0.5 + j * 0.5)

# ---------------- 4 the press: a whip down, the web runs fast and slows to a stop, then each line prints
air(sec(37.6), sec(38.6), True, 0.9, 0.0, 0.0)
P = T["press"]["run"]; n = int(sec(P[1] - P[0]) * SR); u = np.arange(n) / n
rate = 26 * (1 - u) ** 2 + 2
ph = np.cumsum(rate) / SR; clk = np.zeros(n); clk[np.where(np.diff(np.floor(ph)) > 0)[0]] = 1.0
web = np.convolve(clk, FLICK, "same") + lp(rng.standard_normal(n), 0.15) * 0.25 * (1 - u)
put(web * 0.7, sec(P[0]), 0.0)
put(CLACK, sec(T["locks"][4]), 0.0, 1.0); put(BOOM, sec(T["locks"][4]), 0.0, 0.6)
L = T["brief"]["lines"]
for k, b in enumerate(L): put(KICK, sec(b), 0.0, 0.7); put(SNAP, sec(b), 0.0, 0.5); bell([62, 69, 72, 74][k], sec(b) + 0.02, 0.25, 1.0, -0.3 + k * 0.2)
groove(46, 53, g=0.9)

# ---------------- 5 on schedule: a flick for each sheet dealt, a thump for the weekly
air(sec(52.7), sec(53.6), False, 0.6)
groove(54, 63, kick=True, hats=True, bassline=True, g=0.8)
for k, b in enumerate(T["deals"]): put(FLICK, sec(b), -0.8 + k * 0.27, 1.0); bell(74 + [0, 2, 3, 5, 7, 5, 3][k], sec(b), 0.08, 0.5, -0.8 + k * 0.27)
put(BOOM, sec(T["weekly"]), 0.0, 0.9); put(CLACK, sec(T["weekly"]), 0.0, 0.6)

# ---------------- 6 yours: the folder lands, the plates fan apart, the ink floods, and the mark
put(SNAP, sec(63.0), 0.0, 0.6); bell(62, sec(63.2), 0.2, 1.5)
air(sec(T["fan"][0] - 0.2), sec(T["fan"][1] + 0.3), True, 0.7, -0.9, 0.9)
for k in range(4): put(CLACK, sec(T["fan"][0]) + k * 0.05, -0.9 + k * 0.6, 0.4)
fl = T["flood"]; t = tt(sec(fl[1] - fl[0]) + 0.4); put(lp(rng.standard_normal(len(t)), 0.02) * 4 * np.minimum(1, t / sec(fl[1] - fl[0])) * np.exp(-np.maximum(0, t - sec(fl[1] - fl[0])) / 0.1), sec(fl[0]), 0.0, 0.5)
put(BOOM, sec(T["logo"]), 0.0, 0.8)
for m in (50, 57, 62, 65, 69): bell(m, sec(T["logo"]) + 0.02, 0.16, 2.6)

# ---------------- master: room, then the level
ir_n = int(0.7 * SR); ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR / 0.16); ir /= np.sqrt(np.sum(ir ** 2))
for ch in range(2):
    f = np.fft.rfft(out[:, ch], N + ir_n); out[:, ch] += 0.12 * np.fft.irfft(f * np.fft.rfft(ir, N + ir_n))[:N]
out = np.tanh(out * 1.4) / 1.4                     # a soft clip, so the hits sit together
tm = np.arange(N) / SR; out *= np.clip((DUR - tm) / 0.4, 0, 1)[:, None]
out *= 10 ** (-5.5 / 20) / np.max(np.abs(out))
pcm = (np.clip(out, -1, 1) * 32767).astype("<i2")
os.makedirs(os.path.join(ROOT, "assets", "bgm"), exist_ok=True)
with wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("score", round(DUR, 2), "s, peak -5.5 dBFS")
