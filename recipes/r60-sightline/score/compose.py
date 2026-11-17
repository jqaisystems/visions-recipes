"""The score for R60 · Sightline, composed in code from assets/table.js, in season 10's dry, wooden family. The lamp rolls on its rail
with a soft rumble that follows its speed. The shadow is a hiss while it's noise, and as the lamp nears a station the hiss narrows
onto one note and lands as a struck tone with a wooden snap: each sweep plays three notes. Each rebuild is a scatter of wooden
knocks running across the lattice. At the last stop nothing reads, so the hiss holds and doesn't resolve. Then one full chord.
Needs NumPy.  Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py"""
import json, os, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.loads(open(os.path.join(ROOT, "assets", "table.js"), encoding="utf-8").read()[len("window.TABLE="):-1])
SR = 48000; BEAT = T["beat"]; DUR = T["dur"]; N = int(DUR * SR)
out = np.zeros((N, 2)); t = np.arange(N) / SR; bt = t / BEAT
rng = np.random.default_rng(60)
sec = lambda b: b * BEAT
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
NOTES = [62, 65, 69, 69, 67, 62, 62, 66, 69]      # one for each word that lands: D F A, then A G D, then D F sharp A


def put(x, at, pan=0.0, g=1.0):
    i = int(at * SR)
    if i >= N or i + len(x) <= 0: return
    a, b = max(0, i), min(N, i + len(x)); seg = x[a - i:b - i] * g
    out[a:b, 0] += seg * np.sqrt(0.5 * (1 - pan)); out[a:b, 1] += seg * np.sqrt(0.5 * (1 + pan))


def band(x, lo, hi):               # a soft band-pass, done in one go across the whole signal
    f = np.fft.rfftfreq(len(x), 1 / SR); X = np.fft.rfft(x)
    g = 1 / np.sqrt(1 + (lo / np.maximum(f, 1e-6)) ** 4) / np.sqrt(1 + (f / hi) ** 4)
    return np.fft.irfft(X * g, len(x))


def keyv(K, b): return np.interp(b, [k[0] for k in K], [k[1] for k in K])
def sm(u): u = np.clip(u, 0, 1); return u * u * (3 - 2 * u)


def lamp_deg(b):
    a = np.full_like(b, T["start"], dtype=float)
    for b0, b1, a0, a1 in T["moves"]:
        u = np.clip((b - b0) / (b1 - b0), 0, 1); a = np.where(b > b0, a0 + (a1 - a0) * (1 - (1 - u ** 1.5) ** 3), a)
    return a


def knock_bank(n, lo, hi):          # wooden knocks: a short tuned body with a woody click
    B = []
    for k in range(n):
        f = rng.uniform(lo, hi); m = int(0.09 * SR); tt = np.arange(m) / SR
        B.append((np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 2.3 * tt) * np.exp(-tt / 0.006)) * np.exp(-tt / rng.uniform(0.012, 0.03)) * 0.5)
    return B
KNOCKS = knock_bank(16, 380, 1300); TICKS = knock_bank(6, 1500, 2300)


def clack(at, pan, g=1.0):          # a heavy relay: a hard click, a body thump, a little rattle
    n = int(0.25 * SR); tt = np.arange(n) / SR
    click = band(rng.standard_normal(n) * np.exp(-tt / 0.004), 200, 5000)
    body = np.sin(2 * np.pi * (90 + 160 * np.exp(-tt / 0.01)) * tt) * np.exp(-tt / 0.05)
    put(click * 0.9 + body * 0.8 + rng.standard_normal(n) * np.exp(-((tt - 0.022) / 0.006) ** 2) * 0.4, at, pan, g)


def bell(m, at, g=1.0, d=2.0, pan=0.0):
    n = int(d * 3 * SR); tt = np.arange(n) / SR; f = hz(m)
    x = np.sin(2 * np.pi * f * tt) * np.exp(-tt / d) + 0.25 * np.sin(2 * np.pi * f * 3.0 * tt) * np.exp(-tt / (d * 0.2))
    put(x * np.minimum(1, tt / 0.004), at, pan, g)


def thump(at, g=1.0, f0=48):
    n = int(0.6 * SR); tt = np.arange(n) / SR
    put(np.sin(2 * np.pi * np.cumsum(f0 + 60 * np.exp(-tt / 0.03)) / SR) * np.exp(-tt / 0.16), at, 0.0, g)


# ---------------- what the picture is doing, sample by sample
deg = lamp_deg(bt); level = keyv(T["lamp"], bt)
speed = np.abs(np.gradient(deg, 1 / SR)); speed = speed / speed.max()
busy = np.zeros(N)                                   # 1 while a rebuild is under way: the shadow is churning even though the lamp is still
for b0, b1, _ in T["rebuild"]: busy = np.maximum(busy, sm((bt - b0) / 0.5) * (1 - sm((bt - b1 + 0.6) / 0.6)))
sharp = np.zeros(N)                                  # 1 when a word is on the wall
for s in T["stations"]: sharp = np.maximum(sharp, np.exp(-((deg - s) / 2.2) ** 2))
sharp *= 1 - busy
pan = np.clip((deg - 45) / 110, -0.8, 0.8)           # everything follows the lamp across the room

# ---------------- the lamp: a relay clack as it comes on, and a filament hum under the whole film
clack(sec(1.6), -0.5, 0.6)
hum = (np.sin(2 * np.pi * hz(38) * t) + 0.35 * np.sin(2 * np.pi * hz(50) * t + 0.3) + 0.1 * np.sin(2 * np.pi * hz(57) * t)) * (1 + 0.15 * np.sin(2 * np.pi * 100 * t))
out += (hum * level * 0.05)[:, None] * np.sqrt(0.5)

# ---------------- the rail: a soft rumble and a whirr that follow the lamp's speed
roll = band(rng.standard_normal(N), 40, 320) * speed ** 0.7 * 0.9
whirr = np.sin(2 * np.pi * np.cumsum(70 + 150 * speed) / SR) * speed ** 1.2 * 0.10
rr = (roll + whirr) * level
out[:, 0] += rr * np.sqrt(0.5 * (1 - pan)); out[:, 1] += rr * np.sqrt(0.5 * (1 + pan))

# ---------------- the shadow: a hiss while it's noise, narrowing onto the note of the word it's about to become
hiss = band(rng.standard_normal(N), 1800, 7000) * (1 - sharp) ** 1.5 * (0.45 + 0.55 * np.maximum(speed, busy)) * level * 0.085
out[:, 0] += hiss * np.sqrt(0.5 * (1 - pan)); out[:, 1] += hiss * np.sqrt(0.5 * (1 + pan))
slow = band(rng.standard_normal(N), 0.5, 14); slow /= np.abs(slow).max()
lands = T["lands"]
for k, (lb, st, lat, word) in enumerate(lands):
    f = hz(NOTES[k]); nxt = lands[k + 1][0] if k + 1 < len(lands) else 1e9
    own = (bt > lb - 3.2) & (bt < nxt - 3.2) if k else (bt < nxt - 3.2)          # this note owns the time up to its landing and the hold after
    gather = np.where(bt < lb, sharp ** 0.6 * (1 - sharp ** 6), 0.0) * own       # the hiss narrowed onto the note, just before it lands
    held = np.where(bt >= lb, sharp ** 8, 0.0) * own                              # and the clear tone while the word holds
    tone = slow * np.sin(2 * np.pi * f * t) * gather * 0.5 + (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)) * held * 0.035 * (1 + 0.2 * np.sin(2 * np.pi * 4.5 * t))
    tone *= level
    out[:, 0] += tone * np.sqrt(0.5 * (1 - pan)); out[:, 1] += tone * np.sqrt(0.5 * (1 + pan))
    p = float(np.interp(lb, bt, pan))
    bell(NOTES[k], sec(lb), 0.30, 1.6, p); bell(NOTES[k] - 12, sec(lb), 0.14, 2.2, p)   # the word lands: a struck note,
    put(KNOCKS[k % 16], sec(lb), p, 0.9); thump(sec(lb), 0.35)                          # a wooden snap and a small thump

# ---------------- the rebuilds: knocks running across the lattice as the blocks slide, over a low creak
for b0, b1, _ in T["rebuild"]:
    t0, t1 = sec(b0), sec(b1)
    for v in rng.random(560): put(KNOCKS[rng.integers(16)], t0 + v * (t1 - t0 - 0.2), -0.6 + 1.2 * v + rng.uniform(-0.2, 0.2), 0.5 * rng.uniform(0.3, 1.0))
    n = int((t1 - t0) * SR); put(band(rng.standard_normal(n), 30, 160) * np.sin(np.pi * np.arange(n) / n) ** 2 * 2.0, t0, 0.0, 0.5)

# ---------------- the roadmap: a small tick each time the lamp crosses a mark on the wall's line (every 7.5 degrees)
i0 = int(sec(T["timeline"][0]) * SR); q = np.floor(deg[i0:] / 7.5 + 0.5)
for i in np.nonzero(np.diff(q) > 0)[0]:
    if 0 < deg[i0 + i] < 94: put(TICKS[int(q[i + 1]) % 6], (i0 + i) / SR, float(pan[i0 + i]), 0.35)

# ---------------- the last stop: nothing reads. A dull thump where a note would be, and two low notes that don't agree
stop_b = T["moves"][-1][1]
thump(sec(stop_b), 0.5, 40); put(KNOCKS[5] * 0.6, sec(stop_b), 0.6, 0.7)
n = int(sec(T["markGlow"][0] - stop_b) * SR); tt = np.arange(n) / SR; env = np.minimum(1, tt / 0.8) * np.minimum(1, (n / SR - tt) / 0.6)
put((np.sin(2 * np.pi * hz(50) * tt) + 0.8 * np.sin(2 * np.pi * hz(56) * tt)) * env * (1 + 0.3 * np.sin(2 * np.pi * 0.9 * tt)), sec(stop_b), 0.5, 0.035)

# ---------------- the direction: the three marks light together, one full chord. Then the mark
g0 = sec(T["markGlow"][0])
for k, m in enumerate([50, 57, 62, 66, 69]): bell(m, g0 + 0.06 * k, 0.2, 3.0, [-0.5, 0.0, 0.5, -0.25, 0.25][k])
bell(62, sec(T["logo"]) + 0.1, 0.28, 3.0); bell(69, sec(T["logo"]) + 0.12, 0.12, 2.4); bell(74, sec(T["logo"]) + 0.14, 0.08, 2.0)
# ---------------- a small tap under each line of words
for s, b0, b1 in T["caps"]: put(KNOCKS[2], sec(b0), 0.0, 0.22)

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
