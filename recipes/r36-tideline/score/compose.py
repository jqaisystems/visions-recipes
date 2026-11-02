"""The soundtrack for R36 · Tideline: the strongest minute of the Tidesstunes track itself (assets/img/music.wav, cut
by bake/prep.py at the same moment as the picture), with a few sound marks made in code, timed to bake/table.json:
a swell on each slit, a tick on the window's lock, a stutter and a filter drop on the datamosh, a soft bright line
on the link, three bell notes for the phones, a low wash under the tunnel, and a bell on the mark.
Writes assets/bgm/score.wav (not committed). Without music.wav it writes the marks over a quiet piano bed.
Usage: python score/compose.py"""
import json, os, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TB = json.load(open(os.path.join(ROOT, "bake", "table.json"), encoding="utf-8"))
SR = 48000
DUR = TB["dur"]
N = int(SR * DUR)
rng = np.random.default_rng(36)
t = np.arange(N) / SR


def read_wav(p):
    with wave.open(p) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        return x.reshape(-1, w.getnchannels())


def env(n, a, d):
    e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    return e * np.exp(-np.arange(n) / SR / d)


def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); s = 0.0
    for i in range(len(x)):
        s = (1 - a) * x[i] + a * s; y[i] = s
    return y


def add(out, at, sig, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N: return
    sig = sig[:N - i]
    out[i:i + len(sig), 0] += sig * gain * (1 - max(0, pan))
    out[i:i + len(sig), 1] += sig * gain * (1 + min(0, pan))


def bell(f, d=2.4):
    n = int(SR * d); x = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f * m * x) * np.exp(-x * (1.2 + 1.6 * m)) for m, a in [(1, 1), (2.76, 0.4), (5.4, 0.18), (8.9, 0.07)])
    return s * env(n, 0.003, 9)


def swell(d):
    n = int(SR * d); x = rng.standard_normal(n).astype(np.float32)
    y = lp(x, 900) * np.sin(np.linspace(0, np.pi, n)) ** 2
    return y / (np.abs(y).max() + 1e-9)


out = np.zeros((N, 2), np.float32)
mpath = os.path.join(ROOT, "assets", "img", "music.wav")
if os.path.exists(mpath):
    m = read_wav(mpath)
    if m.shape[1] == 1: m = np.repeat(m, 2, 1)
    m = m[:N]
    m = np.pad(m, ((0, N - len(m)), (0, 0)))
else:
    m = np.zeros((N, 2), np.float32)
    for k, f in enumerate([220, 277.2, 329.6, 415.3] * 10):
        add(m, k * TB["beat"], bell(f, 3) * 0.12, pan=0.3 * np.sin(k))

# the music: in on the first frame, a filter drop and a stutter on the hold, out under the mark
g = np.ones(N)
g[:int(0.6 * SR)] = np.linspace(0, 1, int(0.6 * SR))
f0, f1 = TB["mosh"]
c0, c1 = TB["T"]["mark"], DUR
g *= np.where(t > c1 - 2.2, np.clip((c1 - t) / 2.2, 0, 1), 1)
mm = m.copy()
seg = (t >= f0) & (t < TB["T"]["phones"][0])
if seg.any():
    i0, i1 = np.where(seg)[0][[0, -1]]
    low = np.stack([lp(m[i0:i1 + 1, c], 520) for c in range(2)], 1)
    w = np.sin(np.linspace(0, np.pi, i1 + 1 - i0))[:, None] ** 0.5
    mm[i0:i1 + 1] = m[i0:i1 + 1] * (1 - w) + low * w
    # the stutter: one grain held at the freeze, repeated, as the picture holds
    fz = int(TB["freeze"] * SR); gl_ = int(0.09 * SR)
    grain = m[fz:fz + gl_] * np.hanning(gl_)[:, None]
    for k in range(6):
        a = fz + k * gl_
        mm[a:a + gl_] = mm[a:a + gl_] * 0.3 + grain * (0.9 - k * 0.1)
out += mm * g[:, None] * 0.82

# the marks
for a, d in [(TB["sweep"][0], TB["sweep"][1] - TB["sweep"][0]), (TB["unfold"][0], TB["unfold"][1] - TB["unfold"][0])]:
    add(out, a, swell(d), 0.07, pan=-0.2)
tick = np.sin(2 * np.pi * 2400 * np.arange(int(0.05 * SR)) / SR) * env(int(0.05 * SR), 0.001, 0.012)
add(out, TB["slide"][1] - 0.05, tick, 0.22)
add(out, TB["slide"][1] - 0.05, bell(659.3, 1.8), 0.06)
add(out, TB["fall"][0], swell(TB["fall"][1] - TB["fall"][0]), 0.06, pan=0.2)
add(out, TB["linkLine"][0], bell(1318.5, 1.4), 0.07)
for k, (at, f) in enumerate(zip(TB["phones"], [523.25, 659.25, 783.99])):
    add(out, at, bell(f), 0.11, pan=(k - 1) * 0.5)
wash = swell(TB["tunnel"][1] - TB["tunnel"][0] + 0.6)
sub = np.sin(2 * np.pi * 55 * np.arange(len(wash)) / SR) * np.sin(np.linspace(0, np.pi, len(wash)))
add(out, TB["tunnel"][0], wash * 0.09 + sub * 0.05)
for f, d in [(392, 0), (493.9, 0.04), (587.3, 0.08), (784, 0.12)]:
    add(out, c0 + d, bell(f, 3.2), 0.07)

peak = np.abs(out).max()
out = out / max(peak, 1e-9) * 0.89
os.makedirs(os.path.join(ROOT, "assets", "bgm"), exist_ok=True)
with wave.open(os.path.join(ROOT, "assets", "bgm", "score.wav"), "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
print("score:", round(DUR, 2), "s")
