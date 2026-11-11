"""The score for R58 · Casting, composed in code from assets/table.js: a new family for season 10, dry and wooden, a small room.
Each lamp is a heavy relay clack and then its own filament hum, and the hums are tuned so the lamps make a chord as they light:
D, A and F sharp, and the fourth adds E. Blocks sliding are soft wooden knocks, a handoff is a plucked note running along the wall,
the collapse is a box of blocks settling, and when the lamps go out the room drops to one hum. Needs NumPy.
Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py"""
import json, os, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.loads(open(os.path.join(ROOT, "assets", "table.js"), encoding="utf-8").read()[len("window.TABLE="):-1])
SR = 48000; BEAT = T["beat"]; DUR = T["dur"]; N = int(DUR * SR)
out = np.zeros((N, 2)); t = np.arange(N) / SR
rng = np.random.default_rng(58)
sec = lambda b: b * BEAT
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
PAN = [-0.55, -0.15, 0.25, 0.6]
NOTE = [50, 57, 54, 52]          # each lamp's hum: D, A, F sharp, E


def put(x, at, pan=0.0, g=1.0):
    i = int(at * SR)
    if i >= N or i + len(x) <= 0: return
    a, b = max(0, i), min(N, i + len(x)); seg = x[a - i:b - i] * g
    out[a:b, 0] += seg * np.sqrt(0.5 * (1 - pan)); out[a:b, 1] += seg * np.sqrt(0.5 * (1 + pan))


def lowpass(x, c):
    y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)): acc += c * (x[i] - acc); y[i] = acc
    return y


def clack(at, pan, g=1.0):       # a heavy relay: a hard click, a body thump, a little rattle
    n = int(0.25 * SR); tt = np.arange(n) / SR
    click = rng.standard_normal(n) * np.exp(-tt / 0.004)
    body = np.sin(2 * np.pi * (90 + 160 * np.exp(-tt / 0.01)) * tt) * np.exp(-tt / 0.05)
    rattle = rng.standard_normal(n) * np.exp(-((tt - 0.022) / 0.006) ** 2) * 0.4
    put(lowpass(click, 0.5) * 0.9 + body * 0.8 + rattle, at, pan, g)


KNOCKS = []
for k in range(16):              # wooden knocks: a short tuned body with a woody click
    f = rng.uniform(380, 1300); n = int(0.09 * SR); tt = np.arange(n) / SR
    x = (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 2.3 * tt) * np.exp(-tt / 0.006)) * np.exp(-tt / rng.uniform(0.012, 0.03))
    KNOCKS.append(x * 0.5)


def knocks(t0, t1, count, g=1.0, shape=None):
    u = rng.random(int(count))
    if shape is not None: u = shape(u)
    for v in u: put(KNOCKS[rng.integers(len(KNOCKS))], t0 + v * (t1 - t0), rng.uniform(-0.8, 0.8), g * rng.uniform(0.35, 1.0))


def pluck(m, at, g=1.0, pan=0.0, d=0.9):   # a plucked string, Karplus-Strong
    p = int(SR / hz(m)); n = int(d * 2.5 * SR); buf = rng.uniform(-1, 1, p); y = np.zeros(n)
    for i in range(n): y[i] = buf[i % p]; buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
    put(y * np.exp(-np.arange(n) / SR / d), at, pan, g)


def bell(m, at, g=1.0, d=2.0, pan=0.0):
    n = int(d * 3 * SR); tt = np.arange(n) / SR; f = hz(m)
    x = np.sin(2 * np.pi * f * tt) * np.exp(-tt / d) + 0.25 * np.sin(2 * np.pi * f * 3.0 * tt) * np.exp(-tt / (d * 0.2))
    put(x * np.minimum(1, tt / 0.004), at, pan, g)


def keyv(K, b):
    xs = np.array([k[0] for k in K]); ys = np.array([k[1] for k in K]); return np.interp(b, xs, ys)


# ---------------- the lamps: a clack each time one switches on or off, and a hum that follows its level
bt = t / BEAT
for i, K in enumerate(T["lamps"]):
    lv = keyv(K, bt); f = hz(NOTE[i])
    hum = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t + 0.3) + 0.12 * np.sin(2 * np.pi * 3 * f * t)) \
        * (1 + 0.15 * np.sin(2 * np.pi * 100 * t))   # the filament's buzz at the mains
    out[:, 0] += hum * lv * 0.045 * np.sqrt(0.5 * (1 - PAN[i])); out[:, 1] += hum * lv * 0.045 * np.sqrt(0.5 * (1 + PAN[i]))
    for a, c in zip(K, K[1:]):
        if c[0] - a[0] < 0.06 and abs(c[1] - a[1]) > 0.5: clack(sec(c[0]), PAN[i], 0.55 if c[1] > a[1] else 0.35)

# ---------------- the lattice turning, then settling square: a slow wooden creak that stops on the first lamp
T0, T1 = sec(T["turn"][0]), sec(T["turn"][1])
n = int((T1 - T0) * SR); cr = lowpass(rng.standard_normal(n), 0.02) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.7 * np.arange(n) / SR)) * np.linspace(1, 0.2, n)
put(cr * 2.2, T0, 0.0, 0.5); knocks(T0, T1, 40, 0.3, lambda u: u ** 0.6)
# ---------------- the shared memory: a low struck chord under the proof shots, one per lamp's word
for k, b in enumerate([14.2, 17.8, 21.4]): bell([50, 57, 54][k], sec(b), 0.22, 2.6, PAN[k])
# ---------------- the handoffs: a plucked run along the wall from one word to the next
for b0, b1, i, j in T["beam"]:
    t0, t1 = sec(b0), sec(b1)
    for k, m in enumerate([62, 66, 69, 74]): pluck(m + (2 if j == 2 else 0), t0 + (t1 - t0) * k / 4, 0.16, PAN[i] + (PAN[j] - PAN[i]) * k / 3)
for k, b in enumerate(T["hand"]): pluck([57, 62, 66][k], sec(b), 0.2, PAN[k])
# ---------------- the human signs off: one soft low note and a tick of wood
bell(50, sec(T["human"]["in"][1]), 0.2, 2.0, 0.25); knocks(sec(T["human"]["in"][1]) + 0.3, sec(T["human"]["in"][1]) + 0.35, 2, 0.6)
# ---------------- the fourth lamp swings in, and the lattice rebuilds itself: a long scatter of knocks
RB = T["rebuild"]; knocks(sec(RB[0]), sec(RB[1]), 520, 0.5, lambda u: u ** 1.1)
n = int(sec(T["swing"][1] - T["swing"][0]) * SR); put(lowpass(rng.standard_normal(n), 0.04) * np.sin(np.pi * np.arange(n) / n) * 1.5, sec(T["swing"][0]), PAN[3], 0.4)
bell(52, sec(RB[1]) + 0.1, 0.24, 2.4, PAN[3]); bell(64, sec(RB[1]) + 0.12, 0.1, 1.8, PAN[3])
# ---------------- the collapse into one block: a box of blocks settling, then one plain thump. And back out
CL = T["collapse"]; knocks(sec(CL[0]), sec(CL[1]), 700, 0.55, lambda u: u ** 0.7)
n = int(0.6 * SR); tt = np.arange(n) / SR; put(np.sin(2 * np.pi * np.cumsum(50 + 60 * np.exp(-tt / 0.03)) / SR) * np.exp(-tt / 0.18), sec(CL[1]), 0.0, 0.8)
EX = T["expand"]; knocks(sec(EX[0]), sec(EX[1]), 600, 0.5, lambda u: u ** 1.3)
# ---------------- the finale: the full chord under the last image, then the mark
for k, m in enumerate([50, 57, 54, 52, 62]): bell(m, sec(EX[1]) + 0.05 * k, 0.18, 3.0, PAN[k % 4])
bell(62, sec(T["logo"]) + 0.1, 0.28, 3.0); bell(69, sec(T["logo"]) + 0.12, 0.12, 2.4); bell(74, sec(T["logo"]) + 0.14, 0.08, 2.0)
# ---------------- a small tap under each line of words
for s, b0, b1 in T["caps"]: put(KNOCKS[2], sec(b0), 0.0, 0.25)

# ---------------- master: a small dry room, then the level
ir_n = int(0.5 * SR); ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR / 0.11); ir /= np.sqrt(np.sum(ir ** 2))
for ch in range(2):
    f = np.fft.rfft(out[:, ch], N + ir_n); out[:, ch] += 0.12 * np.fft.irfft(f * np.fft.rfft(ir, N + ir_n))[:N]
out *= np.clip((DUR - t) / 0.4, 0, 1)[:, None]
out *= 10 ** (-1.5 / 20) / np.max(np.abs(out))
pcm = (np.clip(out, -1, 1) * 32767).astype("<i2")
os.makedirs(os.path.join(ROOT, "assets", "bgm"), exist_ok=True)
with wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("score", round(DUR, 2), "s, peak -1.5 dBFS")
