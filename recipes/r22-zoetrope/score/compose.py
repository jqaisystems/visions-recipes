"""
R22 · Zoetrope. Original score, composed in code, timed to the film's one table (bake/table.json).

32 s in D minor, opening to D major on the title. The machines spin under everything: a whirr whose pitch is the
rate the slots pass (thirty a second when locked) and a flutter at each turn of the drum. A lamp clicks on. The strobe
stutters in: one xenon tick for every frame it fires on, closer and closer, until it locks with a hard flash and
becomes a steady 30 Hz clatter like a projector. The lock is the beat: 150 bpm, one beat per turn of the twelve
frames. The horse gallops on it, four hooves a stride, over a low pulse and Dm, Bb, F, C. The dive rises into a flash
and almost silence: inside the loop the hooves are far off, under water. Another flash and the cabinet: a music box
for the mirror drum, wing beats for the disc, a paper riffle for the flip book. Out of phase, the clatter slips off
the beat, the strobe stops and everything winds down like a stopped tape, then one flash slams it back. The last
flash opens on D major and the music box plays the title out.
Usage: python score/compose.py  ->  assets/bgm/score.wav   (numpy only, deterministic)
"""
import json
import os
import wave
import numpy as np

SR = 44100
DUR = 32.0
N = int(DUR * SR)
rng = np.random.default_rng(22)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "bgm", "score.wav")
TB = json.load(open(os.path.join(HERE, "..", "bake", "table.json"), encoding="utf-8"))
T, FPS = TB["T"], TB["fps"]
FLASH = TB["flash"]
OMEGA = np.array(TB["omega"])

L = np.zeros(N)
R = np.zeros(N)
tt = np.arange(N) / SR


def add(sig, start, pan=0.0, g=1.0):
    i0 = int(start * SR)
    if i0 >= N or i0 < 0:
        return
    sig = np.asarray(sig, dtype=float)[: N - i0] * g
    L[i0:i0 + len(sig)] += sig * np.sqrt(0.5 * (1 - pan))
    R[i0:i0 + len(sig)] += sig * np.sqrt(0.5 * (1 + pan))


def env(n, a, rel):
    e = np.ones(n)
    na = max(1, int(a * SR))
    e[:na] = np.linspace(0, 1, na)
    e[na:] = np.exp(-np.arange(n - na) / (rel * SR))
    k = min(n, int(0.01 * SR))
    e[-k:] *= np.linspace(1, 0, k)
    return e


def tone(f, dur, a=0.005, rel=0.3, harm=(1.0,), detune=0.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    return sum(h * np.sin(2 * np.pi * f * (k + 1) * t * (1 + detune * k)) for k, h in enumerate(harm)) * env(n, a, rel)


def lowpass(x, cutoff):
    # one-pole low-pass; cutoff may be a number or an array (a moving filter)
    cut = np.broadcast_to(np.asarray(cutoff, dtype=float), x.shape)
    a = np.exp(-2 * np.pi * cut / SR)
    y = np.zeros_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a[i]) * v + a[i] * acc
        y[i] = acc
    return y


def highpass(x, cutoff):
    return x - lowpass(x, cutoff)


def noise(dur, a=0.002, rel=0.05, cutoff=0):
    n = int(dur * SR)
    s = rng.standard_normal(n)
    if cutoff:
        s = lowpass(s, cutoff)
        s /= np.max(np.abs(s)) + 1e-9
    return s * env(n, a, rel)


def swish(dur, rise=False):
    n = int(dur * SR)
    t = np.arange(n) / SR
    shape = (t / dur) ** 2.2 if rise else np.sin(np.pi * t / dur) ** 2
    s = lowpass(rng.standard_normal(n), 2200 + 3000 * (t / dur if rise else 0)) * shape
    return s / (np.max(np.abs(s)) + 1e-9)


def bell(f, dur=2.6):
    return sum(h * tone(f * k, dur, a=0.001, rel=dur / (1 + 1.2 * i)) for i, (k, h) in enumerate(((1, 1.0), (2.0, 0.45), (2.76, 0.3), (5.4, 0.12))))


def musicbox(f, dur=1.4):
    # a steel comb tooth: bright, slightly inharmonic, quick to fade
    return sum(h * tone(f * k, dur, a=0.0008, rel=dur / (2 + 3 * i)) for i, (k, h) in enumerate(((1, 1.0), (3.01, 0.32), (5.98, 0.12), (8.9, 0.05))))


def tick(g=1.0):
    # a xenon strobe firing: a dry crack and a short high ring
    s = 0.3 * tone(3600, 0.05, a=0.0003, rel=0.012)
    s[: int(0.012 * SR)] += highpass(noise(0.012, a=0.0002, rel=0.003), 2500)
    return g * s


def thud(f=60, dur=0.4):
    n = int(dur * SR)
    t = np.arange(n) / SR
    fr = f + 70 * np.exp(-t * 35)
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 11) + 0.25 * lowpass(noise(dur, a=0.001, rel=0.02), 900)


def hoof(g=1.0):
    s = 0.6 * thud(95, 0.18)
    hit = lowpass(noise(0.09, a=0.0008, rel=0.02, cutoff=2200), 1800)
    s[: len(hit)] += hit
    return g * s


def boom(dur=2.4):
    n = int(dur * SR)
    t = np.arange(n) / SR
    fr = 34 + 60 * np.exp(-t * 6)
    s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 1.6)
    return s + 0.5 * lowpass(noise(dur, a=0.001, rel=0.25), 2400)


hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
BEAT = 0.4                     # one turn of twelve frames at thirty a second
omega = np.interp(tt * FPS, np.arange(len(OMEGA)), OMEGA)
spinning = np.ones(N)
spinning[(tt >= T["video"][0]) & (tt < T["video"][1])] = 0.15     # inside the loop the machines are far away
lock_on = np.zeros(N)
for a, b in [(T["lock"], T["video"][0]), (T["cabinet"], T["drift"][0]), (T["relock"], DUR)]:
    lock_on[(tt >= a) & (tt < b)] = 1
slowdown = np.clip((T["relock"] - tt) / (T["relock"] - T["dark"][0]), 0, 1) * ((tt >= T["dark"][0]) & (tt < T["relock"]))

# ---- the machines: a whirr at the rate the slots pass, a flutter at each turn
rate = 30 * omega
ph = 2 * np.pi * np.cumsum(rate) / SR
whirr = 0.5 * np.sin(ph) + 0.3 * np.sin(2 * ph + 0.3) + 0.18 * np.sin(3 * ph) + 0.1 * np.sin(5 * ph)
air = lowpass(rng.standard_normal(N), 900) * 2.2
flutter = 0.6 + 0.4 * np.sin(ph / 12)
lampup = np.clip(tt / 0.6, 0, 1)
w = (0.55 * whirr + 0.35 * air) * flutter * lampup * spinning * (1 - 0.6 * np.clip((tt - T["end"]) / 1.5, 0, 1))
L += 0.07 * w
R += 0.07 * w

# ---- the lamp clicks on; a low D drone with a mains hum
add(tone(2200, 0.06, a=0.0005, rel=0.01), 0.05, -0.3, 0.12)
add(noise(0.03, a=0.0003, rel=0.005, cutoff=6000), 0.05, -0.3, 0.07)
drone = (np.sin(2 * np.pi * hz(38) * tt) + 0.4 * np.sin(2 * np.pi * hz(50) * tt * 1.0007)) * np.clip(tt / 2, 0, 1)
drone *= 1 - 0.7 * ((tt >= T["video"][0]) & (tt < T["video"][1])) - 0.9 * (tt >= T["end"])
L += 0.05 * drone
R += 0.05 * drone

# ---- the strobe: a tick on every frame it fires; locked, the ticks become a projector clatter
for f in FLASH:
    t = f / FPS
    locked = lock_on[min(N - 1, int(t * SR))] > 0
    if t >= T["end"]: break
    g = 0.035 if locked else 0.12
    add(tick(g), t, -0.4 if locked else rng.uniform(-0.5, 0.5))
# out of phase: the ticks slip between the beats
for k, t in enumerate(np.arange(T["drift"][0], T["drift"][1], 1 / 24)):
    add(tick(0.06), t, rng.uniform(-0.6, 0.6))

# ---- the hard flashes: every lock and every cut
for t in [T["lock"], T["video"][0], T["cabinet"], T["relock"], T["end"]]:
    add(boom(2.6), t, 0, 0.32)
    add(highpass(noise(0.25, a=0.0005, rel=0.06), 3000), t, 0, 0.12)
add(swish(2.2, rise=True), T["lock"] - 2.2, 0, 0.06)
add(swish(1.0, rise=True), T["dive"][1] - 1.0, 0, 0.09)
add(swish(0.6, rise=True), T["cabinet"] - 0.6, 0, 0.05)
add(swish(0.6, rise=True), T["end"] - 0.6, 0, 0.06)

# ---- the beat: a low pulse on every turn while locked, with Dm, Bb, F, C in bars of four turns
CHORDS = [[50, 57, 62, 65], [46, 53, 58, 62], [41, 48, 53, 57], [48, 55, 60, 64]]
def pulse_span(a, b, g=1.0):
    k = 0
    t = a
    while t < b - 0.05:
        add(thud(52, 0.42), t, 0, 0.16 * g)
        if k % 2 == 1:
            add(highpass(noise(0.05, a=0.0005, rel=0.015), 6500), t, 0.3, 0.025 * g)
        if k % 4 == 0:
            ch = CHORDS[(k // 4) % 4]
            for j, m in enumerate(ch):
                add(tone(hz(m), min(1.7, b - t + 0.6), a=0.08, rel=0.9, harm=(1, 0.35, 0.12), detune=0.0006), t, -0.5 + 0.33 * j, 0.03 * g)
        k += 1
        t += BEAT
pulse_span(T["lock"], T["dive"][0] + 0.4)
pulse_span(T["cabinet"], T["drift"][0])
pulse_span(T["relock"], T["end"])

# ---- the horse: four hooves a stride, on the beat; inside the loop they are far away
for a, b, g in [(T["lock"], T["video"][0], 1.0), (T["video"][0], T["video"][1], 0.35)]:
    t = a
    while t < b - 0.05:
        for q, off in enumerate([0.0, 0.07, 0.16, 0.24]):
            add(hoof(0.11 * g * (1 if q != 2 else 1.3)), t + off, -0.2 + 0.13 * q)
        t += BEAT
# inside the loop: a muffled hum under the hooves
add(lowpass(tone(hz(38), 2.8, a=0.3, rel=2.0, harm=(1, 0.5)), 600), T["video"][0], 0, 0.06)

# ---- the cabinet: a music box for the mirror drum, wing beats for the disc, a riffle for the flip book
BOX = [74, 77, 81, 86, 84, 81, 77, 79, 74, 77, 81, 84, 86, 84, 81, 77]
for k, t in enumerate(np.arange(13.2, 15.4, BEAT / 2)):
    add(musicbox(hz(BOX[k % len(BOX)]), 1.2), t, 0.25 * np.sin(k), 0.05)
for k, t in enumerate(np.arange(15.4, 17.2, BEAT)):
    for off in (0.0, 0.2):
        add(swish(0.16), t + off, 0.4 * np.sin(k + off), 0.07)
for k, t in enumerate(np.arange(17.4, 19.2, 1 / 30)):
    add(highpass(noise(0.012, a=0.0003, rel=0.004, cutoff=7000), 1400), t, 0.5, 0.05 * (0.6 + 0.4 * np.sin(k * 0.3)))
# the wide shot: the music box returns over the whole cabinet
for k, t in enumerate(np.arange(19.2, 20.4, BEAT / 2)):
    add(musicbox(hz(BOX[(k + 3) % len(BOX)]), 1.2), t, 0, 0.04)

# ---- out of phase: the chord bends down like a stopped tape as the machines slow, then one flash slams it back
seg = (tt >= T["drift"][0]) & (tt < T["relock"])
bend = 1 - 0.35 * slowdown ** 0.5
for j, m in enumerate([50, 57, 62, 65]):
    p = 2 * np.pi * np.cumsum(hz(m) * bend) / SR
    s = (np.sin(p) + 0.3 * np.sin(2 * p)) * seg * np.clip((tt - T["drift"][0]) / 0.4, 0, 1) * np.clip((T["relock"] - tt) / 0.05, 0, 1)
    L += 0.022 * s * (1 - 0.15 * j)
    R += 0.022 * s * (0.55 + 0.15 * j)

# ---- the title: D major, wide, and the music box plays it out
for j, m in enumerate([26, 38, 45, 50, 54, 57, 62, 66, 69]):
    add(tone(hz(m), DUR - T["end"], a=0.05, rel=2.4, harm=(1, 0.3, 0.1), detune=0.0007), T["end"], -0.6 + 0.15 * j, 0.07)
for j, m in enumerate([74, 78, 81]):
    add(bell(hz(m + 12), 3.4), T["end"] + 0.5 + 0.16 * j, -0.3 + 0.3 * j, 0.04)
OUTRO = [86, 85, 81, 78, 81, 85, 86, 90, 88, 86]
for k, m in enumerate(OUTRO):
    add(musicbox(hz(m), 1.8), T["end"] + 1.2 + k * BEAT, 0.3 * np.sin(k), 0.045 * (1 - k / 14))

# ---- master: a soft-clip that lifts the body and keeps the peaks round, then a fade at the very end
mix = np.stack([L, R], axis=1)
mix /= np.max(np.abs(mix))
DRIVE = 2.4
mix = np.tanh(mix * DRIVE) / np.tanh(DRIVE) * 0.84
fade = int(0.8 * SR)
mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
data = (mix * 32767).astype("<i2").tobytes()
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with wave.open(OUT, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data)
print("wrote", os.path.normpath(OUT), DUR, "s")
