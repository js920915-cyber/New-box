"""Temporary score for the brand film, synthesized from scratch (no samples, no licensing).

Usage: python3 scripts/score.py public/audio/score.wav
120 BPM, D minor. Section times follow src/BrandFilm.tsx; visual cuts sit on the beat grid.
Meant as a guide track; replace with a licensed music cue in the final edit if preferred.
"""
import sys
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

SR = 48000
DUR = 55.0
N = int(SR * DUR)
rng = np.random.default_rng(7)
t_all = np.arange(N) / SR

L = np.zeros(N)
R = np.zeros(N)
send = np.zeros((N, 2))  # reverb bus


def idx(t):
    return int(round(t * SR))


def place(sig, t0, gain=1.0, pan=0.0, verb=0.0):
    """Add a mono or stereo signal at t0 seconds."""
    i0 = idx(t0)
    if sig.ndim == 1:
        sig = np.stack([sig * np.sqrt(0.5 * (1 - pan)), sig * np.sqrt(0.5 * (1 + pan))], axis=1) * np.sqrt(2)
    n = min(len(sig), N - i0)
    if n <= 0:
        return
    L[i0:i0 + n] += sig[:n, 0] * gain
    R[i0:i0 + n] += sig[:n, 1] * gain
    if verb:
        send[i0:i0 + n] += sig[:n] * gain * verb


def lp(x, fc, order=2):
    return sosfilt(butter(order, fc, 'low', fs=SR, output='sos'), x)


def hp(x, fc, order=2):
    return sosfilt(butter(order, fc, 'high', fs=SR, output='sos'), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], 'band', fs=SR, output='sos'), x)


def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)


def note(name):
    names = {'C': -9, 'C#': -8, 'D': -7, 'Eb': -6, 'E': -5, 'F': -4, 'F#': -3, 'G': -2, 'Ab': -1, 'A': 0, 'Bb': 1, 'B': 2}
    n, o = name[:-1], int(name[-1])
    return 440.0 * 2 ** ((names[n] + 12 * (o - 4)) / 12)


def saw(f, n, phase=0.0):
    t = np.arange(n) / SR
    return 2 * ((f * t + phase) % 1) - 1


# ---------------- drums ----------------

def kick(gain=1.0, t0=0.0, punch=1.0):
    n = idx(0.5)
    t = np.arange(n) / SR
    f = 46 + 110 * np.exp(-t / 0.035) * punch
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t / 0.3)
    click = hp(rng.standard_normal(n), 3000) * np.exp(-t / 0.004) * 0.25
    place(np.tanh((s + click) * 1.6), t0, gain * 0.9)


def clap(gain=1.0, t0=0.0):
    n = idx(0.4)
    t = np.arange(n) / SR
    noise = bp(rng.standard_normal(n), 900, 5200)
    e = np.exp(-t / 0.12) * (1 + 0.6 * (np.exp(-((t - 0.012) % 0.011) / 0.003)) * (t < 0.035))
    tone = np.sin(2 * np.pi * 185 * t) * np.exp(-t / 0.05) * 0.4
    place((noise * e * 0.6 + tone), t0, gain * 0.5, verb=0.35)


def hat(gain=1.0, t0=0.0, open_=False, pan=0.25):
    n = idx(0.3 if open_ else 0.08)
    t = np.arange(n) / SR
    s = hp(rng.standard_normal(n), 7500, 4) * np.exp(-t / (0.12 if open_ else 0.022))
    place(s, t0, gain * 0.16, pan=pan)


def tom(f0, gain=1.0, t0=0.0):
    n = idx(0.4)
    t = np.arange(n) / SR
    f = f0 * (1 + 0.6 * np.exp(-t / 0.05))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.18)
    place(s, t0, gain * 0.45, verb=0.2)


def impact(t0, gain=1.0, length=4.0):
    n = idx(length)
    t = np.arange(n) / SR
    f = 30 + 70 * np.exp(-t / 0.12)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 1.2)
    crash = lp(hp(rng.standard_normal(n), 400), 9000) * np.exp(-t / 0.9) * 0.35
    place(np.tanh(boom * 1.4) + crash, t0, gain, verb=0.6)


def whoosh(t0, length, gain=1.0, lo=300, hi=6000, pan=0.0):
    n = idx(length)
    x = rng.standard_normal(n)
    # time-varying band: sweep up then down, swell envelope
    out = np.zeros(n)
    blocks = 64
    edges = np.linspace(0, n, blocks + 1).astype(int)
    zi = None
    for b in range(blocks):
        u = (b + 0.5) / blocks
        c = lo * (hi / lo) ** np.sin(np.pi * u)
        sos = butter(2, [c * 0.6, min(c * 1.6, SR / 2 - 100)], 'band', fs=SR, output='sos')
        seg, zi = sosfilt(sos, x[edges[b]:edges[b + 1]], zi=zi if zi is not None else np.zeros((sos.shape[0], 2)))
        out[edges[b]:edges[b + 1]] = seg
    e = np.sin(np.pi * np.linspace(0, 1, n)) ** 2
    place(out * e, t0, gain * 0.5, pan=pan, verb=0.3)


def riser(t0, length, gain=1.0, f0=200, f1=8000, tone=True):
    n = idx(length)
    u = np.linspace(0, 1, n)
    x = rng.standard_normal(n)
    out = np.zeros(n)
    blocks = 80
    edges = np.linspace(0, n, blocks + 1).astype(int)
    zi = None
    for b in range(blocks):
        c = f0 * (f1 / f0) ** ((b + 0.5) / blocks)
        sos = butter(2, min(c, SR / 2 - 200), 'low', fs=SR, output='sos')
        seg, zi = sosfilt(sos, x[edges[b]:edges[b + 1]], zi=zi if zi is not None else np.zeros((sos.shape[0], 2)))
        out[edges[b]:edges[b + 1]] = seg
    s = out * u ** 2 * 0.6
    if tone:
        f = 110 * 2 ** (u * 2)
        s += np.sin(2 * np.pi * np.cumsum(f) / SR) * u ** 3 * 0.25
    place(s, t0, gain, verb=0.4)


def beep(t0, f=1760, gain=1.0, pan=0.0):
    n = idx(0.12)
    t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)) * env(n, 0.002, 0.03)
    place(s, t0, gain * 0.18, pan=pan, verb=0.3)


# ---------------- tonal layers ----------------

def pad(chord, t0, length, gain=1.0, cutoff=1400, attack=0.6, release=0.8, bright=0.0):
    n = idx(length + release)
    t = np.arange(n) / SR
    out = np.zeros((n, 2))
    for k, nm in enumerate(chord):
        f = note(nm)
        for d, side in ((-0.09, 0), (0.0, None), (0.08, 1)):
            v = saw(f * 2 ** (d / 12), n, phase=rng.random())
            if side is None:
                out[:, 0] += v * 0.6
                out[:, 1] += v * 0.6
            else:
                out[:, side] += v
    out[:, 0] = lp(out[:, 0], cutoff * (1 + bright), 2)
    out[:, 1] = lp(out[:, 1], cutoff * (1 + bright), 2)
    e = np.minimum(1, t / attack) * np.where(t > length, np.exp(-(t - length) / (release / 3)), 1)
    out *= e[:, None] / max(1, len(chord))
    place(out, t0, gain * 0.22, verb=0.5)


def bass_note(nm, t0, length, gain=1.0, cutoff=380):
    n = idx(length + 0.05)
    t = np.arange(n) / SR
    f = note(nm)
    s = saw(f, n) * 0.7 + np.sin(2 * np.pi * f / 2 * t) * 0.6
    s = lp(s, cutoff, 2) * env(n, 0.004, length * 0.55)
    place(np.tanh(s * 1.5), t0, gain * 0.45)


def drone(t0, length, gain=1.0):
    n = idx(length)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * note('D1') * t) + 0.5 * np.sin(2 * np.pi * note('D2') * t + 0.3) + 0.15 * np.sin(2 * np.pi * note('A2') * t)
    s *= 0.8 + 0.2 * np.sin(2 * np.pi * 0.25 * t)
    e = np.minimum(1, t / 2.0) * np.minimum(1, (length - t) / 1.0)
    place(np.tanh(s * e * 1.2), t0, gain * 0.5)


def shimmer(t0, length, gain=1.0):
    n = idx(length)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for k, nm in enumerate(['D6', 'A6', 'F6', 'E7']):
        s += np.sin(2 * np.pi * note(nm) * t + k) * (0.5 + 0.5 * np.sin(2 * np.pi * (0.3 + 0.17 * k) * t + k))
    e = np.minimum(1, t / 1.5) * np.minimum(1, (length - t) / 1.0)
    st = np.stack([s * e, np.roll(s, 2400) * e], axis=1)
    place(st, t0, gain * 0.03, verb=0.8)


def arp(chord, t0, length, gain=1.0, step=0.125):
    k = 0
    tt = t0
    seq = chord + chord[1:-1][::-1]
    while tt < t0 + length - 1e-6:
        nm = seq[k % len(seq)]
        n = idx(0.25)
        t = np.arange(n) / SR
        f = note(nm)
        s = (saw(f, n) * 0.5 + np.sin(2 * np.pi * f * t)) * env(n, 0.003, 0.09)
        place(lp(s, 3500), tt, gain * 0.12, pan=0.35 if k % 2 else -0.35, verb=0.4)
        k += 1
        tt += step


BEAT = 0.5
PROG = [['D3', 'F3', 'A3', 'E4'], ['Bb2', 'D3', 'F3', 'A3'], ['F2', 'A3', 'C4', 'E4'], ['C3', 'E3', 'G3', 'D4']]
ROOT = ['D2', 'Bb1', 'F2', 'C2']


def bar_chord(t):
    return int(((t - 21.0) // 2) % 4)


# ---------------- arrangement ----------------

# S1 universe: drone, shimmer, slow swell
drone(0.0, 19.2, gain=0.75)
drone(18.75, 2.3, gain=0.35)
shimmer(0.3, 10.0, gain=1.0)
pad(['D3', 'A3', 'E4'], 0.6, 4.6, gain=0.6, cutoff=700, attack=2.5, release=1.5)
riser(2.8, 2.25, gain=0.5, f0=150, f1=5000, tone=False)

# S2 destination: atmosphere whoosh, pulses build
whoosh(5.0, 1.8, gain=1.1, lo=200, hi=5000)
pad(['D3', 'F3', 'A3', 'C4'], 5.0, 5.0, gain=0.7, cutoff=900, attack=1.0)
for b in np.arange(5.0, 10.0, BEAT):
    k = (b - 5.0) / 5.0
    if b < 7.0 and (b - 5.0) % 1.0 != 0:
        continue
    kick(0.35 + 0.35 * k, b, punch=0.6)
riser(8.4, 1.6, gain=0.6, f0=300, f1=9000)

# S3 center: rhythm grows
for b in np.arange(10.0, 15.0, BEAT):
    kick(0.7, b)
    hat(0.8, b + BEAT / 2)
    bass_note('D2', b, 0.22, gain=0.6)
    bass_note('D2', b + 0.25, 0.2, gain=0.4)
pad(['D3', 'F3', 'A3', 'E4'], 10.0, 5.0, gain=0.7, cutoff=1100)
whoosh(12.55, 0.8, gain=0.8, lo=600, hi=7000)  # through the door
beep(10.4, 1320, 0.6)

# S4 question: groove, hits on cuts, then the beat stops in slow motion
for c in (15.0, 16.5, 18.0):
    impact(c, gain=0.35, length=1.2)
    whoosh(c - 0.25, 0.4, gain=0.6, lo=800, hi=8000)
for b in np.arange(15.0, 18.75, BEAT):
    kick(0.85, b)
    hat(0.9, b + BEAT / 2)
    if int(round((b - 15.0) / BEAT)) % 2 == 1:
        clap(0.8, b)
    bass_note('D2', b, 0.22, gain=0.7)
    bass_note('F2' if (b // 1) % 2 else 'D2', b + 0.25, 0.2, gain=0.45)
pad(['D3', 'F3', 'A3', 'C4'], 15.0, 3.7, gain=0.7, cutoff=1300)
# slow motion: everything drops out, a low heartbeat and a reverse swell into the drop
pad(['D3', 'A3', 'D4'], 18.75, 2.25, gain=0.35, cutoff=500, attack=0.3, release=0.4)
for hb in (19.1, 19.45, 20.1, 20.45):
    tom(55, 0.6 if hb in (19.1, 20.1) else 0.35, hb)
riser(19.7, 1.3, gain=0.9, f0=200, f1=12000)

# S5 assessment: the drop
impact(21.0, gain=0.9, length=2.5)
for c in (21.0, 23.0, 24.5, 26.5, 28.5):
    beep(c + 0.05, 1760, 1.0, pan=0.3)
    beep(c + 0.16, 2350, 0.7, pan=0.3)
for b in np.arange(21.0, 41.0, BEAT):
    i = int(round((b - 21.0) / BEAT))
    ch = bar_chord(b)
    kick(1.0, b)
    if i % 2 == 1:
        clap(1.0, b)
    for s16 in range(4):
        hat(0.7 if s16 % 2 else 0.45, b + s16 * BEAT / 4, pan=0.3 if s16 % 2 else -0.2)
    bass_note(ROOT[ch], b, 0.2, gain=0.85, cutoff=420)
    bass_note(ROOT[ch], b + 0.25, 0.18, gain=0.6, cutoff=500)
    if i % 8 == 7:
        kick(0.6, b + 0.375)
for k, t0 in enumerate(np.arange(21.0, 41.0, 2.0)):
    pad(PROG[k % 4], t0, 2.0, gain=0.75, cutoff=1500 if t0 < 31 else 2000, attack=0.05, release=0.3)

# S6 training: impacts on cuts, stabs
for c in (31.0, 33.5, 36.0, 38.5):
    impact(c, gain=0.4, length=1.0)
    whoosh(c - 0.3, 0.45, gain=0.5, lo=900, hi=9000)
for b in np.arange(31.0, 41.0, 1.0):
    ch = bar_chord(b)
    pad(PROG[ch], b + 0.75, 0.12, gain=0.9, cutoff=3000, attack=0.005, release=0.15)
for c in (34.95, 35.3, 35.6):
    tom(80, 0.8, c)

# S7 back to movement: brighter, emotional lift
for b in np.arange(41.0, 49.0, BEAT):
    i = int(round((b - 41.0) / BEAT))
    kick(1.0, b)
    if i % 2 == 1:
        clap(1.1, b)
    hat(0.9, b + BEAT / 2, open_=True)
    hat(0.5, b + BEAT / 4)
    hat(0.5, b + 3 * BEAT / 4)
LIFT = [['Bb2', 'D3', 'F3', 'C4'], ['F2', 'A3', 'C4', 'G4'], ['C3', 'E3', 'G3', 'D4'], ['D3', 'F3', 'A3', 'E4']]
LROOT = ['Bb1', 'F2', 'C2', 'D2']
for k, t0 in enumerate(np.arange(41.0, 49.0, 2.0)):
    pad(LIFT[k], t0, 2.0, gain=1.05, cutoff=2400, attack=0.08, release=0.4, bright=0.3)
    arp([n.replace('2', '4').replace('3', '5') for n in LIFT[k]], t0, 2.0, gain=1.0)
    for b in np.arange(t0, t0 + 2.0, 0.25):
        bass_note(LROOT[k], b, 0.2, gain=0.8)
for c in (43.5, 46.0):
    impact(c, gain=0.35, length=1.0)
riser(47.0, 2.0, gain=0.9, f0=300, f1=14000)
shimmer(44.0, 5.0, gain=1.3)

# S8 brand: breath, then the final hit and a long tail
pad(['D3', 'A3', 'E4'], 49.0, 2.1, gain=0.6, cutoff=900, attack=0.5, release=0.3)
riser(50.2, 0.9, gain=0.7, f0=500, f1=12000, tone=False)
impact(51.1, gain=1.2, length=3.9)
kick(1.0, 51.1)
pad(['D2', 'A2', 'D3', 'F3', 'A3', 'E4'], 51.1, 2.6, gain=1.1, cutoff=1800, attack=0.02, release=1.3)
shimmer(51.1, 3.9, gain=1.5)

# ---------------- mix ----------------
ir_n = idx(2.6)
ir_t = np.arange(ir_n) / SR
ir = np.stack([rng.standard_normal(ir_n), rng.standard_normal(ir_n)], axis=1) * np.exp(-ir_t / 0.55)[:, None]
ir[:, 0] = lp(ir[:, 0], 6000)
ir[:, 1] = lp(ir[:, 1], 6000)
ir /= np.sqrt((ir ** 2).sum(axis=0))
wet = np.stack([fftconvolve(send[:, 0], ir[:, 0])[:N], fftconvolve(send[:, 1], ir[:, 1])[:N]], axis=1)

mix = np.stack([L, R], axis=1) + wet * 0.9
mix[:, 0] = hp(mix[:, 0], 25)
mix[:, 1] = hp(mix[:, 1], 25)
fade = np.minimum(1, t_all / 0.4) * np.clip((DUR - t_all) / 1.6, 0, 1)
mix *= fade[:, None]
mix /= np.max(np.abs(mix)) + 1e-9
mix = np.tanh(mix * 1.25) / np.tanh(1.25) * 0.89
out = sys.argv[1] if len(sys.argv) > 1 else 'public/audio/score.wav'
wavfile.write(out, SR, (mix * 32767).astype(np.int16))
print(out, f'{DUR}s', 'peak', float(np.max(np.abs(mix))))
