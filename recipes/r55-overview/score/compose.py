"""The score for Overview, composed in code from assets/table.js: metal for a field of steel pins, and a camera in flight.
Pins rising are a wash of tiny ticks, as dense as the pins moving. The flight runs on a press-like pulse; every word that rises slams,
and the camera's dashes between them are air. The noise is a clatter, the crane up one long rising sweep that lands on an open chord,
the briefing a tune on struck metal, one note per line, and brass rings like brass. Needs NumPy.
Writes assets/bgm/score.wav (not committed).  Usage: python score/compose.py"""
import json, os, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.loads(open(os.path.join(ROOT, "assets", "table.js"), encoding="utf-8").read()[len("window.TABLE="):-1])
SR = 48000; BEAT = T["beat"]; DUR = T["dur"]; N = int(DUR * SR)
out = np.zeros((N, 2))
rng = np.random.default_rng(55)
sec = lambda b: b * BEAT
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
t = np.arange(N) / SR


def put(x, t0, pan=0.0, g=1.0):
    i = int(t0 * SR)
    if i >= N or i + len(x) <= 0: return
    a, b = max(0, i), min(N, i + len(x)); seg = x[a - i:b - i] * g
    out[a:b, 0] += seg * np.sqrt(0.5 * (1 - pan)); out[a:b, 1] += seg * np.sqrt(0.5 * (1 + pan))


def lp(x, k):              # a one-pole low-pass, k from 0 (closed) to 1 (open), per sample or fixed
    y = np.zeros_like(x); acc = 0.0; kk = np.broadcast_to(k, x.shape)
    for i in range(len(x)): acc += kk[i] * (x[i] - acc); y[i] = acc
    return y


TICKS = []
for k in range(24):        # pin ticks: a click of metal, each tuned a little differently
    f = rng.uniform(2600, 7200); n = int(0.03 * SR); tt = np.arange(n) / SR
    TICKS.append((np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.51 * tt)) * np.exp(-tt / rng.uniform(0.003, 0.008)) * 0.5)


def ticks(t0, t1, count, g=1.0, shape=None, pan=(-0.9, 0.9)):
    if count <= 0 or t1 <= t0: return
    u = rng.random(int(count))
    if shape is not None: u = shape(u)
    for v in u: put(TICKS[rng.integers(len(TICKS))], t0 + v * (t1 - t0), rng.uniform(*pan), g * rng.uniform(0.4, 1.0))


def bell(m, t0, g=1.0, d=1.6, pan=0.0, brass=False):   # struck metal; brass is warmer, with a slower, rounder attack and more body
    n = int(d * 3 * SR); tt = np.arange(n) / SR; f = hz(m)
    if brass:
        x = sum(a * np.sin(2 * np.pi * f * h * tt) * np.exp(-tt / (d * dd)) for a, h, dd in ((1, 1, 1), (0.5, 2, 0.6), (0.3, 3, 0.4), (0.18, 4.2, 0.25)))
        x *= np.minimum(1, tt / 0.012)
    else:
        x = np.sin(2 * np.pi * f * tt) * np.exp(-tt / d) + 0.35 * np.sin(2 * np.pi * f * 4.0 * tt) * np.exp(-tt / (d * 0.18)) \
            + 0.12 * np.sin(2 * np.pi * f * 9.9 * tt) * np.exp(-tt / (d * 0.06))
        x *= np.minimum(1, tt / 0.002)
    put(x, t0, pan, g)


def thud(t0, g=1.0, f0=46):   # the press: a pitched-down knock with a click on top
    n = int(0.6 * SR); tt = np.arange(n) / SR; f = f0 + 80 * np.exp(-tt / 0.025)
    put(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.18), t0, 0.0, g); put(TICKS[3], t0, 0.0, g * 0.5)


def slam(t0, g=1.0, pan=0.0):  # a word rising: the press, a clang of steel and a burst of pins
    thud(t0, g * 0.9, 42)
    n = int(0.5 * SR); tt = np.arange(n) / SR
    cl = sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt / d) for f, d in ((523, 0.25), (1187, 0.12), (1903, 0.07), (2711, 0.05)))
    put(cl * 0.18, t0, pan, g); ticks(t0, t0 + 0.35, 60, g * 0.55, lambda u: u ** 2)


def air(t0, t1, g=1.0, p0=-0.7, p1=0.7, rise=True):   # the camera moving: filtered noise, opening as it speeds up
    n = int((t1 - t0) * SR)
    if n <= 0: return
    u = np.linspace(0, 1, n); x = rng.standard_normal(n)
    shape = np.sin(np.pi * u) ** 1.5; k = 0.02 + 0.22 * (u if rise else 1 - u) * shape
    y = lp(x, k) * shape
    pan = p0 + (p1 - p0) * u
    i = int(t0 * SR); a, b = max(0, i), min(N, i + n)
    out[a:b, 0] += y[a - i:b - i] * np.sqrt(0.5 * (1 - pan[a - i:b - i])) * g
    out[a:b, 1] += y[a - i:b - i] * np.sqrt(0.5 * (1 + pan[a - i:b - i])) * g


L = {l["name"]: l for l in T["layers"]}
k0 = lambda nm: L[nm]["keys"][0][0]

# ---------------- the room: the lamp's drone, on with the light and off with it
on, off0, off1 = sec(T["light"]["on"]), sec(T["light"]["off"][0]), sec(T["light"]["off"][1])
lamp = np.clip((t - on) / 0.6, 0, 1) * np.clip((off1 - t) / (off1 - off0), 0, 1)
drone = 0.5 * np.sin(2 * np.pi * hz(40) * t) + 0.3 * np.sin(2 * np.pi * hz(47) * t + 0.4 * np.sin(2 * np.pi * 0.11 * t)) + 0.12 * np.sin(2 * np.pi * hz(52) * t)
quiet = 1 - 0.6 * np.clip((t - sec(24.2)) / 0.5, 0, 1) * np.clip((sec(28.4) - t) / 0.5, 0, 1)
out[:, 0] += drone * lamp * quiet * 0.05; out[:, 1] += drone * lamp * quiet * 0.05
n = int(0.12 * SR); sw = rng.standard_normal(n) * np.exp(-np.arange(n) / SR / 0.012)
put(np.convolve(sw, np.ones(6) / 6, "same"), on, 0.0, 0.7); thud(on, 0.45)
put(np.convolve(sw, np.ones(6) / 6, "same"), off1 - 0.05, 0.0, 0.5)

# ---------------- pins rising: every relief raised or let go is a wash of ticks, as dense as how much of the field it moves
SIZE = {"c_": 260, "s_": 300, "e": 220, "knowledge": 420, "k_": 220, "f": 180, "brief": 200, "grid": 380, "day": 60, "folder": 360}
for l in T["layers"]:
    nm = next(k for k in SIZE if l["name"].startswith(k)); K = l["keys"]
    for a, b in zip(K, K[1:]):
        dw = abs(b[1] - a[1])
        if dw < 0.05: continue
        ticks(sec(a[0]), sec(b[0] + l["spread"]), SIZE[nm] * dw, 0.45 if b[1] > a[1] else 0.3, lambda u: u ** 1.4)
    if l.get("move"):
        M = l["move"]; ticks(sec(M[0][0]), sec(M[-1][0]), 200, 0.35)

# ---------------- the flight: a pulse like a press, eighths of ticks, every word a slam and every dash between them air
for b in np.arange(3.0, 15.0, 1.0):
    thud(sec(b), 0.55 if b % 2 == 0 else 0.42)
    put(TICKS[7], sec(b + 0.5), 0.25, 0.4); put(TICKS[12], sec(b + 0.75), -0.25, 0.22)
for nm in ("c_sources", "c_fly0", "c_fly1", "c_fly2", "c_fly3"): slam(sec(k0(nm)) + 0.02, 0.9)
for a, b, p in ((1.0, 3.6, 0.0), (6.0, 7.9, -0.6), (8.0, 9.9, 0.6), (10.0, 11.9, -0.6), (12.0, 14.0, 0.6)):
    air(sec(a), sec(b), 0.35, -p, p)
for nm in ("s_page", "s_feed", "s_site", "s_lens", "s_chart"): bell(76, sec(k0(nm)) + 0.1, 0.06, 0.5, rng.uniform(-0.6, 0.6))

# ---------------- everything at once: a clatter on the sixteenths, the echoes slamming in, and the press doubling up
NZ = T["noise"]; amp = lambda b: np.interp(b, [k[0] for k in NZ], [k[1] for k in NZ])
for s in np.arange(14.0, 24.0, 0.25):
    a = amp(s) * (1 - np.clip((s - 20.2) / 4.0, 0, 1))
    if a > 0.05: ticks(sec(s), sec(s + 0.25), 80 * a, 0.5)
for k in range(8): slam(sec(k0("e%d" % k)) + 0.02, 0.45, rng.uniform(-0.7, 0.7))
for b in np.arange(15.0, 20.0, 0.5): thud(sec(b), 0.5 if b % 1 == 0 else 0.3)
slam(sec(k0("c_down")) + 0.02, 0.8); slam(sec(k0("c_noise")) + 0.02, 0.85)
air(sec(14.2), sec(16.8), 0.45, 0.8, -0.6)

# ---------------- from above: one long rising sweep as the camera cranes up and the noise settles, landing on an open chord
n = int((sec(24.6) - sec(20.2)) * SR); u = np.linspace(0, 1, n)
riser = lp(rng.standard_normal(n), 0.01 + 0.3 * u ** 2) * u ** 1.5 * 0.9
gl = np.sin(2 * np.pi * np.cumsum(hz(45) * 2 ** (u * 2)) / SR) * u ** 2 * 0.25
put(riser + gl, sec(20.2), 0.0, 1.0)
for m, p in ((40, 0), (47, -0.3), (52, 0.3), (59, -0.5), (64, 0.5)): bell(m, sec(24.6), 0.16, 3.2, p)
slam(sec(k0("c_above")) + 0.02, 0.5)
# the knowledge document: a quiet clock while it rises
for b in np.arange(24.6, 28.4, 0.5): put(TICKS[7], sec(b), -0.3 if b % 1 == 0 else 0.3, 0.3 if b % 1 == 0 else 0.18)

# ---------------- the filter: the sources pop up, everything that doesn't matter drops in one falling sweep, and the rest turns brass
for k in range(8):
    nm = next((n_ for n_ in L if n_.startswith(("k_", "f")) and abs(L[n_]["keys"][0][0] - (28.4 + k * 0.18)) < 1e-6), None)
    if nm: bell(84 - k, sec(k0(nm)) + 0.04, 0.07, 0.4, rng.uniform(-0.7, 0.7))
n = int(sec(1.4) * SR); u = np.linspace(0, 1, n)
put(lp(rng.standard_normal(n), 0.25 * (1 - u) + 0.01) * np.sin(np.pi * u) * 0.6, sec(31.1), 0.0, 1.0)
ticks(sec(31.2), sec(32.6), 420, 0.5, lambda u: u ** 0.8)
for i, m in enumerate((57, 64, 69, 73)): bell(m, sec(31.6) + i * 0.03, 0.14, 2.4, -0.4 + i * 0.27, brass=True)
air(sec(33.0), sec(35.0), 0.25, -0.5, -0.2, rise=False)

# ---------------- written up: the dive down, then a tune on struck metal, one note per line, on a softer pulse
air(sec(35.0), sec(36.9), 0.5, 0.3, -0.3)
NOTES = [57, 64, 60, 67, 64, 69, 64]
for i, m in enumerate(NOTES): bell(m + 12, sec(k0("brief%d" % i)) + 0.06, 0.26 if i % 2 == 0 else 0.18, 1.4, -0.3 + 0.1 * i)
for b in np.arange(36.0, 45.0, 1.0): thud(sec(b), 0.28); put(TICKS[11], sec(b + 0.5), 0.2, 0.2)
slam(sec(k0("c_format")) + 0.02, 0.4); slam(sec(k0("c_voice")) + 0.02, 0.45)
for i, m in enumerate((76, 79, 83, 88)): bell(m, sec(40.6 + i * 0.4), 0.09, 1.0, -0.6 + i * 0.4)

# ---------------- on schedule: a pulse and a note for each day, rising through the week, then one brass hit for weekly
for i, (b, row) in enumerate(T["pops"]):
    if row == 0: thud(sec(b), 0.5); bell([64, 67, 69, 71, 72, 74, 76][i], sec(b) + 0.02, 0.15, 0.7)
    else: thud(sec(b), 0.95, 38); bell(52, sec(b), 0.2, 2.4, 0.0, True); bell(64, sec(b), 0.12, 2.0, 0.0, True)
slam(sec(k0("c_daily")) + 0.02, 0.45); slam(sec(k0("c_rhythm")) + 0.02, 0.45)

# ---------------- yours: the brass folder, two captions, then the long pull out to the whole field and the light going off
bell(52, sec(55.6), 0.2, 2.6, 0.0, True); bell(59, sec(55.6), 0.12, 2.4, 0.0, True)
slam(sec(k0("c_code")) + 0.02, 0.4); slam(sec(k0("c_yours")) + 0.02, 0.45)
n = int((sec(63.6) - sec(61.4)) * SR); u = np.linspace(0, 1, n)
put(lp(rng.standard_normal(n), 0.01 + 0.2 * u) * u ** 2 * np.clip((1 - u) * 6, 0, 1) * 0.7, sec(61.4), 0.0, 1.0)
for m, p in ((40, 0), (52, -0.2), (59, 0.2), (64, 0)): bell(m, sec(T["logo"]) + 0.08, 0.22 if m < 60 else 0.12, 3.0, p, m == 52)

# ---------------- master: a touch of room, then the level
ir_n = int(0.9 * SR); ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR / 0.22); ir /= np.sqrt(np.sum(ir ** 2))
for ch in range(2):
    f = np.fft.rfft(out[:, ch], N + ir_n); out[:, ch] += 0.16 * np.fft.irfft(f * np.fft.rfft(ir, N + ir_n))[:N]
out *= np.clip((DUR - t) / 0.4, 0, 1)[:, None]
out *= 10 ** (-1.5 / 20) / np.max(np.abs(out))
pcm = (np.clip(out, -1, 1) * 32767).astype("<i2")
os.makedirs(os.path.join(ROOT, "assets", "bgm"), exist_ok=True)
with wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("score", round(DUR, 2), "s, peak -1.5 dBFS")
