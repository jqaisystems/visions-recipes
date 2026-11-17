"""The score for R61 · Stacked, composed in code from assets/table.js, in season 10's dry, wooden family. Three lamps click on over a
heap of blocks, each with its own low filament hum, and the heap rattles once as it stirs. Then the lattice is built row by row on a
grid of dotted sixteenths: every row locks with a tuned wooden knock, a step higher each time, so the build is a rising scale, and
the hums swell as the words complete. The rebuilds are scatters of knocks that land on a struck chord, each of the team steps in on
a soft pluck, and one full chord brings in the mark. The stack is a demo.
Needs NumPy.  Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py"""
import json, os, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.loads(open(os.path.join(ROOT, "assets", "table.js"), encoding="utf-8").read()[len("window.TABLE="):-1])
SR = 48000; BEAT = T["beat"]; DUR = T["dur"]; N = int(DUR * SR)
out = np.zeros((N, 2)); t = np.arange(N) / SR; bt = t / BEAT
rng = np.random.default_rng(61)
sec = lambda b: b * BEAT
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
PAN = [-0.6, 0.0, 0.6]                       # seen from the lamps' side, the 0° wall is on the left and the 90° wall on the right
SCALE = [50, 52, 54, 55, 57, 59, 61]          # D major, from D3: the rows climb it


def put(x, at, pan=0.0, g=1.0):
    i = int(at * SR)
    if i >= N or i + len(x) <= 0: return
    a, b = max(0, i), min(N, i + len(x)); seg = x[a - i:b - i] * g
    out[a:b, 0] += seg * np.sqrt(0.5 * (1 - pan)); out[a:b, 1] += seg * np.sqrt(0.5 * (1 + pan))


def band(x, lo, hi):
    f = np.fft.rfftfreq(len(x), 1 / SR); X = np.fft.rfft(x)
    g = 1 / np.sqrt(1 + (lo / np.maximum(f, 1e-6)) ** 4) / np.sqrt(1 + (f / hi) ** 4)
    return np.fft.irfft(X * g, len(x))


def keyv(K, b): return np.interp(b, [k[0] for k in K], [k[1] for k in K])
def sm(u): u = np.clip(u, 0, 1); return u * u * (3 - 2 * u)


def wood(f, d=0.05, g=1.0):                   # a tuned wooden bar: the body, a woody overtone and a click
    n = int(max(0.12, d * 6) * SR); tt = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * tt) * np.exp(-tt / d) + 0.45 * np.sin(2 * np.pi * f * 3.93 * tt) * np.exp(-tt / (d * 0.18))
    x += band(rng.standard_normal(n), 1500, 6000) * np.exp(-tt / 0.0025) * 0.35
    return x * np.minimum(1, tt / 0.0008) * g


def knock(at, pan=0.0, g=1.0, lo=380, hi=1300): put(wood(rng.uniform(lo, hi), rng.uniform(0.012, 0.03)), at, pan, g * 0.5)


def clack(at, pan, g=1.0):                    # a heavy lamp switch: a hard click, a body thump, a little rattle
    n = int(0.25 * SR); tt = np.arange(n) / SR
    click = band(rng.standard_normal(n) * np.exp(-tt / 0.004), 200, 5000)
    body = np.sin(2 * np.pi * (90 + 160 * np.exp(-tt / 0.01)) * tt) * np.exp(-tt / 0.05)
    put(click * 0.9 + body * 0.8 + rng.standard_normal(n) * np.exp(-((tt - 0.022) / 0.006) ** 2) * 0.4, at, pan, g)


def bell(m, at, g=1.0, d=2.0, pan=0.0):
    n = int(d * 3 * SR); tt = np.arange(n) / SR; f = hz(m)
    x = np.sin(2 * np.pi * f * tt) * np.exp(-tt / d) + 0.25 * np.sin(2 * np.pi * f * 3.0 * tt) * np.exp(-tt / (d * 0.2))
    put(x * np.minimum(1, tt / 0.004), at, pan, g)


def pluck(m, at, g=1.0, pan=0.0):             # a soft plucked string, Karplus-Strong
    f = hz(m); p = int(SR / f); n = int(2.2 * SR); y = np.zeros(n); y[:p] = band(rng.standard_normal(p * 4), 80, 3000)[:p]
    for i in range(p, n): y[i] = 0.996 * 0.5 * (y[i - p] + y[i - p - 1])
    put(y / (np.abs(y).max() + 1e-9), at, pan, g)


def thump(at, g=1.0, f0=46):
    n = int(0.6 * SR); tt = np.arange(n) / SR
    put(np.sin(2 * np.pi * np.cumsum(f0 + 60 * np.exp(-tt / 0.03)) / SR) * np.exp(-tt / 0.16), at, 0.0, g)


def rattle(at, dur, n, g=1.0):                # a box of blocks shaken once
    for k in range(n): knock(at + dur * rng.beta(1.6, 2.4), rng.uniform(-0.5, 0.5), g * rng.uniform(0.3, 1.0), 260, 900)


# ---------------- the lamps: a switch as each comes on, and a filament hum each, swelling as the words complete
built = np.zeros(N)
for k, b0 in enumerate(T["rows"]): built = np.maximum(built, (bt >= b0 + T["lift"]) * (k + 1) / len(T["rows"]))
for i, on in enumerate(T["on"]):
    clack(sec(on), PAN[i], 0.55)
    lev = keyv(T["lamps"][i], bt); m = [38, 45, 50][i]
    hum = sum(a * np.sin(2 * np.pi * hz(m) * h * t + i) for h, a in ((1, 1.0), (2, 0.35), (3, 0.12)))
    hum *= lev * (0.22 + 0.78 * sm(built)) * (1 + 0.08 * np.sin(2 * np.pi * (0.31 + 0.07 * i) * t))
    out[:, 0] += hum * 0.045 * np.sqrt(0.5 * (1 - PAN[i])); out[:, 1] += hum * 0.045 * np.sqrt(0.5 * (1 + PAN[i]))

# ---------------- the heap: a rattle in the dark, and a stir just before it lifts
rattle(sec(0.15), 0.5, 22, 0.55)
rattle(sec(T["assemble"][0] - 1.1), 0.7, 28, 0.7)

# ---------------- the assembly: the blocks lift with a rising air, and every row locks on its own step of the scale
air = band(rng.standard_normal(N), 300, 2400)
lift_env = sm((bt - T["rows"][0] + 0.5) / 2.0) * (1 - sm((bt - T["rows"][-1] - T["lift"]) / 0.8))
out[:, 0] += air * lift_env * 0.035; out[:, 1] += np.roll(air, 977) * lift_env * 0.035
for k, b0 in enumerate(T["rows"]):
    land = sec(b0 + T["lift"]); m = SCALE[k % 7] + 12 * (k // 7)
    put(wood(hz(m), 0.09, 1.0), land, (k % 3 - 1) * 0.35, 0.55)
    put(wood(hz(m + 12), 0.04, 1.0), land + 0.002, -(k % 3 - 1) * 0.35, 0.18)
    for q in range(5): knock(land + rng.uniform(-0.012, 0.02), rng.uniform(-0.7, 0.7), 0.35)
done = T["rows"][-1] + T["lift"]
thump(sec(done), 0.9)
for m, p in ((62, -0.6), (66, 0.0), (69, 0.6), (74, 0.0)): bell(m, sec(done) + 0.01, 0.16, 2.6, p)

# ---------------- the rebuilds: knocks in a wave across the room, landing on a struck chord
for (b0, b1, deg), chord in zip(T["rebuild"], ([55, 59, 62, 67], [50, 57, 62, 66, 69])):
    for k in range(70):
        u = rng.uniform(0, 1); knock(sec(b0 + 0.3 + u * (b1 - b0 - 0.6)), (u - 0.5) * 1.4 * (1 if deg < 45 else -1), 0.55)
    thump(sec(b1), 0.6)
    for j, m in enumerate(chord): bell(m, sec(b1) + 0.008 * j, 0.14, 2.4, (j / (len(chord) - 1) - 0.5) * 1.2)

# ---------------- the team: one soft pluck as each steps into the light
for (li, b0, b1), m in zip(T["team"], (69, 74, 78)): pluck(m, sec(b0 + 0.7), 0.3, PAN[li])

# ---------------- the close: the lamps go out and one full chord brings in the mark
for i in range(3): clack(sec(61.0 + 0.2 * i), PAN[i], 0.35)
for j, m in enumerate((38, 50, 57, 62, 66, 69, 74)): bell(m, sec(T["logo"]) + 0.012 * j, 0.15, 3.2, (j / 6 - 0.5) * 1.2)

# ---------------- a small dry room, then the level
n = int(0.5 * SR); tt = np.arange(n) / SR; ir = rng.standard_normal(n) * np.exp(-tt / 0.11)
ir = band(ir, 200, 6000); ir /= np.sqrt((ir ** 2).sum())
L = 1 << int(np.ceil(np.log2(N + n)))
for c in range(2):
    wet = np.fft.irfft(np.fft.rfft(out[:, c], L) * np.fft.rfft(np.roll(ir, 37 * c), L), L)[:N]
    out[:, c] += wet * 0.22
fade = np.minimum(1, (DUR - t) / 0.6); out *= fade[:, None]
out *= 10 ** (-1.5 / 20) / np.abs(out).max()
os.makedirs(os.path.join(ROOT, "assets", "bgm"), exist_ok=True)
with wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype("<i2").tobytes())
print("score %.1f s, peak -1.5 dBFS" % DUR)
