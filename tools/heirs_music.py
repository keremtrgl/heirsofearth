"""Heirs of Earth 3.6: the music of the nine nations, and their short signature calls (stings).

Usage: python tools/heirs_music.py [nation ...]   (scipy lives in the user site, so no -I; ffmpeg encodes the .ogg files)

Every piece is synthesised here from sine partials, filtered noise and simple physical models: no samples, no recordings,
no third-party audio. Each nation has its own mode, tempo, instruments and drum pattern; the melody is composed from a seeded
motif with variations, in the form intro - A - B - A' - outro. Output: HeirsOfEarth/Sounds/HeirsOfEarth/Music/HE_Music_<Nation>.ogg
and HeirsOfEarth/Sounds/HeirsOfEarth/HE_Sting_<Nation>.wav.
"""
import os
import subprocess
import sys
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, lfilter

SR = 44100
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "HeirsOfEarth", "Sounds", "HeirsOfEarth")
TMP = os.environ.get("TEMP", ".")


def lowpass(x, hz, order=2):
    b, a = butter(order, min(hz, SR / 2 - 100) / (SR / 2), "low")
    return lfilter(b, a, x)


def highpass(x, hz, order=2):
    b, a = butter(order, hz / (SR / 2), "high")
    return lfilter(b, a, x)


def bandpass(x, lo, hi, order=2):
    b, a = butter(order, [lo / (SR / 2), min(hi, SR / 2 - 100) / (SR / 2)], "band")
    return lfilter(b, a, x)


def ts(seconds):
    return np.arange(int(SR * seconds)) / SR


def adsr(n, a, d, s, r, total):
    t = np.arange(n) / SR
    env = np.where(t < a, t / max(a, 1e-4), s + (1 - s) * np.exp(-(t - a) / max(d, 1e-4)))
    tail = total - r
    env = env * np.where(t > tail, np.clip(1 - (t - tail) / max(r, 1e-4), 0, 1), 1.0)
    return env


# ------------------------------------------------------------------ instruments (mono arrays)
class Inst:
    def __init__(self, rng):
        self.rng = rng

    def noise(self, n):
        return self.rng.standard_normal(n)

    def pluck(self, f, dur, bright=1.0, decay=1.4, inharm=0.0004, ring=1.0, metal=0.0):
        """A plucked or struck string: decaying partials, higher ones dying faster, a little pick noise."""
        length = dur + decay * ring
        t = ts(length)
        out = np.zeros_like(t)
        for h in range(1, 14):
            fh = f * h * np.sqrt(1 + inharm * h * h) * (1 + metal * 0.003 * h)
            if fh > 11000:
                break
            amp = (1 / h ** (1.5 - 0.45 * bright)) * (0.6 + 0.4 * np.sin(np.pi * h * 0.18) ** 2)
            out += amp * np.exp(-t * (1 + 0.55 * h * (1.3 - 0.3 * bright)) / decay) * np.sin(2 * np.pi * fh * t + self.rng.uniform(0, 6))
        pick = lowpass(self.noise(len(t)), 2500 + 3000 * bright) * np.exp(-t / 0.006) * 0.25
        env = np.clip(t / 0.003, 0, 1) * np.where(t > length - 0.05, np.clip((length - t) / 0.05, 0, 1), 1)
        return (out + pick) * env

    def flute(self, f, dur, breath=0.15, vib=0.006, scoop=0.0, reed=0.0, bright=0.3, attack=0.06):
        """Flutes and reeds: a sine with a few harmonics (odd ones for reeds), breath noise around the note and a late vibrato."""
        length = dur + 0.12
        t = ts(length)
        env = adsr(len(t), attack, 0.3, 0.85, 0.12, length)
        vibrato = 1 + vib * np.sin(2 * np.pi * 5.2 * t + self.rng.uniform(0, 6)) * np.clip((t - 0.25) / 0.35, 0, 1)
        fm = f * vibrato * (1 - scoop * np.exp(-t / 0.08))
        ph = 2 * np.pi * np.cumsum(fm) / SR
        tone = np.sin(ph) + bright * 0.35 * np.sin(2 * ph) + bright * 0.15 * np.sin(3 * ph)
        if reed:
            tone += reed * (0.55 * np.sin(3 * ph) + 0.3 * np.sin(5 * ph) + 0.15 * np.sin(7 * ph))
        air = bandpass(self.noise(len(t)), max(200, f * 0.8), min(9000, f * 4.5)) * breath * (0.6 + 0.4 * env)
        chiff = bandpass(self.noise(len(t)), 1500, 6000) * np.exp(-t / 0.03) * breath * 0.8
        return (tone * env + air * env + chiff) * 0.8

    def bowed(self, f, dur, bright=0.6, vib=0.005, attack=0.18):
        length = dur + 0.25
        t = ts(length)
        env = adsr(len(t), attack, 0.6, 0.9, 0.25, length)
        fm = f * (1 + vib * np.sin(2 * np.pi * 4.8 * t + self.rng.uniform(0, 6)) * np.clip((t - 0.3) / 0.4, 0, 1))
        ph = 2 * np.pi * np.cumsum(fm) / SR
        tone = np.zeros_like(t)
        for h in range(1, 16):
            if f * h > 8000:
                break
            tone += (1 / h) * np.sin(h * ph) * env ** (1 + (h - 1) * 0.3 / bright)
        rosin = bandpass(self.noise(len(t)), 1500, 5000) * 0.02
        return lowpass(tone + rosin, 1800 + 2500 * bright) * env

    def brass(self, f, dur, bright=1.0, vib=0.004, attack=0.07, bend=0.03):
        length = dur + 0.15
        t = ts(length)
        env = adsr(len(t), attack, 0.4, 0.8, 0.15, length)
        fm = f * (1 - bend * np.exp(-t / 0.05)) * (1 + vib * np.sin(2 * np.pi * 5.0 * t) * np.clip((t - 0.35) / 0.4, 0, 1))
        ph = 2 * np.pi * np.cumsum(fm) / SR
        out = np.zeros_like(t)
        for h in range(1, 14):
            if f * h > 7000:
                break
            out += (1 / h ** 0.95) * env ** (1 + (h - 1) * 0.4 / bright) * np.sin(h * ph)
        return lowpass(out, 5500) * env

    def organ(self, f, dur, attack=0.8):
        """A soft sustained drone (tanpura, bagpipe chanter, harmonium-like reed)."""
        length = dur + 0.6
        t = ts(length)
        env = adsr(len(t), attack, 1.0, 1.0, 0.6, length)
        swell = 1 + 0.08 * np.sin(2 * np.pi * 0.17 * t + self.rng.uniform(0, 6))
        ph = 2 * np.pi * f * t
        tone = np.sin(ph) + 0.5 * np.sin(2 * ph + 0.3) + 0.3 * np.sin(3 * ph + 1.1) + 0.12 * np.sin(4 * ph) + 0.08 * np.sin(5 * ph)
        tone += 0.4 * np.sin(2 * np.pi * f * 1.003 * t)                                   # beating, like a real drone
        return lowpass(tone, 2200) * env * swell

    def drum(self, body, decay, snap=0.3, band=(1500, 5000), drop=0.25, length=0.9, jingle=0.0):
        t = ts(length)
        f = body * (1 + drop * np.exp(-t / 0.025))
        tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / decay)
        skin = bandpass(self.noise(len(t)), band[0], band[1]) * np.exp(-t / (decay * 0.35)) * snap
        out = tone + skin
        if jingle:
            j = bandpass(self.noise(len(t)), 5000, 11000) * jingle
            j *= np.exp(-t / 0.18) * (1 + 0.6 * np.sin(2 * np.pi * 28 * t))
            out += j
        return out * np.clip(t / 0.001, 0, 1)

    def bell(self, f, dur=2.5, decay=1.8):
        t = ts(dur)
        out = np.zeros_like(t)
        for r, a, d in ((1.0, 1.0, 1.0), (2.0, 0.6, 0.7), (2.76, 0.45, 0.5), (5.4, 0.25, 0.3), (8.93, 0.12, 0.2)):
            out += a * np.exp(-t / (decay * d)) * np.sin(2 * np.pi * f * r * t + self.rng.uniform(0, 6))
        return out * np.clip(t / 0.002, 0, 1)

    def gong(self, f=110, dur=4.0):
        t = ts(dur)
        out = np.zeros_like(t)
        for r, d in zip((1.0, 1.52, 2.0, 2.27, 2.74, 3.3, 4.1), (2.8, 2.3, 2.0, 1.7, 1.4, 1.1, 0.8)):
            bloom = np.clip(t / (0.05 + 0.08 * r), 0, 1) ** 1.5
            out += (1 / r ** 0.6) * bloom * np.exp(-t / d) * np.sin(2 * np.pi * np.cumsum(f * r * (1 + 0.01 * (1 - np.exp(-t / 0.6)))) / SR)
        return out + lowpass(self.noise(len(t)), 800) * np.exp(-t / 0.03)

    def sistrum(self, dur=0.6):
        t = ts(dur)
        shake = np.zeros_like(t)
        for k in range(5):
            s = int(SR * (0.0 + k * 0.045))
            m = len(t) - s
            tt = np.arange(m) / SR
            shake[s:] += bandpass(self.noise(m), 4000, 10000) * np.exp(-tt / 0.05) * (1 - k * 0.15)
            for fr in (3150, 4420, 5900):
                shake[s:] += 0.25 * np.exp(-tt / 0.12) * np.sin(2 * np.pi * fr * tt)
        return shake


# ------------------------------------------------------------------ composition
def freq_of(tonic, scale, degree):
    octave, idx = divmod(degree, len(scale))
    return tonic * 2 ** ((scale[idx] + 12 * octave) / 12)


def motif(rng, cells, beats, low, high, start, end=None):
    """One phrase: rhythm cells filling the bars, degrees moving mostly by step, ending on a strong degree."""
    notes = []
    pos = 0.0
    deg = start
    while pos < beats - 1e-6:
        cell = cells[rng.integers(len(cells))]
        for d in cell:
            if pos >= beats - 1e-6:
                break
            d = min(d, beats - pos)
            notes.append([pos, d, deg])
            pos += d
            r = rng.random()
            step = rng.choice([-1, 1]) if r < 0.58 else rng.choice([-2, 2]) if r < 0.82 else 0 if r < 0.92 else rng.choice([-4, -3, 3, 4])
            deg = int(np.clip(deg + step, low, high))
    if end is not None and notes:
        notes[-1][2] = end
        if len(notes) > 1 and abs(notes[-2][2] - end) > 2:
            notes[-2][2] = end + (1 if notes[-2][2] > end else -1)
    return notes


def theme(rng, p, start, cadence):
    """An eight-bar theme: a, a (varied), b, cadence."""
    bar = p["beats"]
    a = motif(rng, p["cells"], 2 * bar, p["low"], p["high"], start)
    a2 = [[n[0], n[1], n[2] + (1 if i == len(a) - 1 else 0)] for i, n in enumerate(a)]
    b = motif(rng, p["cells"], 2 * bar, p["low"], p["high"], start + 2)
    c = motif(rng, p["cells_end"], 2 * bar, p["low"], p["high"], start + 1, end=cadence)
    out = []
    for k, part in enumerate((a, a2, b, c)):
        out += [[n[0] + k * 2 * bar, n[1], n[2]] for n in part]
    return out


class Mix:
    def __init__(self, seconds):
        self.L = np.zeros(int(SR * seconds) + SR * 6)
        self.R = np.zeros_like(self.L)

    def put(self, x, at, gain=1.0, pan=0.0):
        s = int(SR * max(0.0, at))
        e = min(len(self.L), s + len(x))
        if e <= s:
            return
        gl, gr = np.cos((pan + 1) * np.pi / 4) * gain, np.sin((pan + 1) * np.pi / 4) * gain
        self.L[s:e] += x[: e - s] * gl
        self.R[s:e] += x[: e - s] * gr


def reverb(L, R, rng, seconds=2.4, mix=0.28, tone=4500):
    n = int(SR * seconds)
    outs = []
    for ch in (L, R):
        ir = rng.standard_normal(n) * np.exp(-np.arange(n) / (SR * seconds / 6.5))
        ir[: int(SR * 0.012)] = 0
        ir = lowpass(ir, tone)
        ir /= np.sqrt(np.sum(ir ** 2))
        wet = fftconvolve(ch, ir)[: len(ch)]
        outs.append(ch * (1 - mix) + wet * mix * 0.9)
    return outs


def finish(L, R, peak=0.80):
    L, R = highpass(L, 35), highpass(R, 35)
    m = max(np.max(np.abs(L)), np.max(np.abs(R))) + 1e-9
    L, R = L / m * peak, R / m * peak
    # trim trailing silence, then a short fade
    energy = np.maximum(np.abs(L), np.abs(R))
    last = np.nonzero(energy > 0.002)[0]
    end = min(len(L), (last[-1] if len(last) else len(L)) + int(SR * 0.3))
    L, R = L[:end], R[:end]
    fade = int(SR * 0.4)
    L[-fade:] *= np.linspace(1, 0, fade)
    R[-fade:] *= np.linspace(1, 0, fade)
    return L, R


def write_wav(path, L, R=None):
    data = np.stack([L, R], 1) if R is not None else L[:, None]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, "wb") as w:
        w.setnchannels(data.shape[1])
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(data, -1, 1) * 32767).astype("<i2").tobytes())


# ------------------------------------------------------------------ the nine nations
# Each: tonic, scale (semitones), tempo, beats per bar, rhythm cells, chord roots per bar (A and B sections),
# melody / second melody / accompaniment instruments, drone degrees, drum pattern [(beat, drum, gain)], motif for the sting.
NATIONS = {
    "Roma": dict(tonic=146.83, scale=[0, 2, 3, 5, 7, 9, 10], bpm=84, beats=4, low=0, high=9, start=4, cadence=0,
                 cells=[[1, 1, 2], [2, 1, 1], [1.5, 0.5, 1, 1], [1, 1, 1, 1]], cells_end=[[2, 2], [1, 1, 2], [3, 1]],
                 chordsA=[0, 3, 4, 0], chordsB=[5, 3, 4, 4], melody="brass", melody2="lyre", accomp="lyre", drone=[0, 4],
                 drums=[(0, "frame", 1.0), (2, "frame", 0.7), (3, "tap", 0.5)], sting=[(4, .5), (4, .25), (4, .25), (7, 1.5), (5, .5), (4, 2)]),
    "Yamato": dict(tonic=146.83, scale=[0, 1, 5, 7, 8], bpm=64, beats=4, low=0, high=8, start=3, cadence=0,
                   cells=[[2, 1, 1], [3, 1], [1, 1, 2], [4]], cells_end=[[2, 2], [4]],
                   chordsA=[0, 0, 2, 0], chordsB=[3, 2, 0, 0], melody="shakuhachi", melody2="koto", accomp="koto", drone=[0, 3],
                   drums=[(0, "taiko", 1.0), (2.5, "taiko_rim", 0.5)], sting=[(3, 1), (4, .5), (3, .5), (1, 1), (0, 2.5)]),
    "Nord": dict(tonic=110.0, scale=[0, 2, 3, 5, 7, 8, 10], bpm=72, beats=3, low=0, high=8, start=4, cadence=0,
                 cells=[[2, 1], [1, 1, 1], [3], [1.5, 0.5, 1]], cells_end=[[3], [2, 1]],
                 chordsA=[0, 6, 5, 0], chordsB=[2, 6, 3, 4], melody="fiddle", melody2="horn", accomp="lyre", drone=[0, 4],
                 drums=[(0, "frame_deep", 1.0), (1.5, "frame_deep", 0.55)], sting=[(0, 1), (4, 1.5), (3, .5), (4, 2.5)]),
    "Hellas": dict(tonic=164.81, scale=[0, 1, 3, 5, 7, 8, 10], bpm=92, beats=4, low=0, high=9, start=4, cadence=0,
                   cells=[[1, 1, 1, 1], [1, 0.5, 0.5, 2], [2, 1, 1], [0.5, 0.5, 1, 2]], cells_end=[[2, 2], [1, 1, 2]],
                   chordsA=[0, 1, 0, 6], chordsB=[3, 2, 1, 0], melody="aulos", melody2="lyre", accomp="kithara", drone=[0, 4],
                   drums=[(0, "frame", 0.9), (1.5, "tap", 0.5), (2, "frame", 0.6), (3, "tap", 0.5)], sting=[(0, .5), (2, .5), (4, .5), (5, 1), (4, 2)]),
    "Tianxia": dict(tonic=196.0, scale=[0, 2, 4, 7, 9], bpm=70, beats=4, low=0, high=8, start=2, cadence=0,
                    cells=[[2, 1, 1], [1, 1, 2], [1.5, 0.5, 2], [1, 1, 1, 1]], cells_end=[[2, 2], [4]],
                    chordsA=[0, 3, 4, 0], chordsB=[1, 3, 2, 0], melody="dizi", melody2="guzheng", accomp="guzheng", drone=[0, 3],
                    drums=[(0, "drum_low", 0.8), (3, "woodblock", 0.4)], gong=True, sting=[(4, .5), (3, .5), (2, 1), (1, .5), (0, 2.5)]),
    "Albion": dict(tonic=196.0, scale=[0, 2, 4, 5, 7, 9, 11], bpm=104, beats=4, low=0, high=10, start=4, cadence=0,
                   cells=[[1, 1, 1, 1], [1.5, 0.5, 1, 1], [2, 1, 1], [0.5, 0.5, 1, 2]], cells_end=[[2, 2], [1, 1, 2]],
                   chordsA=[0, 3, 4, 0], chordsB=[5, 3, 1, 4], melody="fife", melody2="fiddle", accomp="lute", drone=[0],
                   drums=[(0, "bass", 1.0), (1, "snare", 0.55), (1.5, "snare", 0.35), (2, "bass", 0.8), (3, "snare", 0.55), (3.5, "snare", 0.35)],
                   sting=[(0, .5), (2, .5), (4, .5), (7, 1), (4, .5), (7, 2)]),
    "Kemet": dict(tonic=164.81, scale=[0, 1, 4, 5, 7, 8, 10], bpm=80, beats=4, low=0, high=9, start=4, cadence=0,
                  cells=[[1, 1, 2], [2, 1, 1], [1, 0.5, 0.5, 2], [3, 1]], cells_end=[[2, 2], [3, 1]],
                  chordsA=[0, 1, 0, 3], chordsB=[4, 3, 1, 0], melody="ney", melody2="harp", accomp="harp", drone=[0, 4],
                  drums=[(0, "frame", 1.0), (1.5, "tap", 0.5), (2.5, "frame", 0.6)], sistrum=[1, 3], sting=[(4, .5), (5, .5), (4, .5), (2, .5), (1, 1), (0, 2)]),
    "Pars": dict(tonic=146.83, scale=[0, 1, 3, 5, 7, 8, 10], bpm=88, beats=3, low=0, high=9, start=3, cadence=0,
                 cells=[[1, 1, 1], [2, 1], [0.5, 0.5, 1, 1], [1.5, 0.5, 1]], cells_end=[[3], [2, 1]],
                 chordsA=[0, 6, 0, 3], chordsB=[2, 3, 1, 0], melody="ney", melody2="santur", accomp="santur", drone=[0, 4],
                 drums=[(0, "daf", 1.0), (1, "tap", 0.45), (2, "daf", 0.6)], sting=[(3, .5), (4, .5), (3, .5), (1, .5), (2, 1), (0, 2)]),
    "Inti": dict(tonic=220.0, scale=[0, 3, 5, 7, 10], bpm=96, beats=4, low=0, high=8, start=2, cadence=0,
                 cells=[[1, 1, 2], [1.5, 0.5, 1, 1], [1, 1, 1, 1], [0.5, 0.5, 1, 2]], cells_end=[[2, 2], [1, 1, 2]],
                 chordsA=[0, 2, 3, 0], chordsB=[1, 2, 4, 0], melody="siku", melody2="charango", accomp="charango", drone=[0],
                 drums=[(0, "bombo", 1.0), (1.5, "bombo", 0.5), (2, "bombo", 0.75), (3, "tap", 0.4)], sting=[(4, .5), (3, .5), (2, 1), (4, .5), (0, 2.5)]),
}


def play(inst, kind, f, dur):
    if kind == "lyre":
        return inst.pluck(f, dur, bright=0.8, decay=1.6)
    if kind == "kithara":
        return inst.pluck(f, dur, bright=0.9, decay=1.9)
    if kind == "harp":
        return inst.pluck(f, dur, bright=0.7, decay=2.0)
    if kind == "koto":
        return inst.pluck(f, dur, bright=1.1, decay=1.3, inharm=0.0008)
    if kind == "guzheng":
        return inst.pluck(f, dur, bright=1.2, decay=1.5, inharm=0.0008)
    if kind == "santur":
        return inst.pluck(f, dur, bright=1.5, decay=1.1, metal=1.0, inharm=0.001)
    if kind == "lute":
        return inst.pluck(f, dur, bright=0.9, decay=1.0)
    if kind == "charango":
        return inst.pluck(f, dur, bright=1.3, decay=0.7)
    if kind == "brass":
        return inst.brass(f, dur, bright=0.9)
    if kind == "horn":
        return inst.brass(f, dur, bright=0.6, attack=0.12)
    if kind == "fiddle":
        return inst.bowed(f, dur, bright=0.7)
    if kind == "shakuhachi":
        return inst.flute(f, dur, breath=0.32, vib=0.008, scoop=0.03, bright=0.2, attack=0.12)
    if kind == "dizi":
        return inst.flute(f, dur, breath=0.14, vib=0.007, bright=0.8)
    if kind == "ney":
        return inst.flute(f, dur, breath=0.3, vib=0.006, scoop=0.015, bright=0.25, attack=0.1)
    if kind == "aulos":
        return inst.flute(f, dur, breath=0.08, vib=0.004, reed=0.7, bright=0.5, attack=0.04)
    if kind == "fife":
        return inst.flute(f, dur, breath=0.08, vib=0.003, bright=0.9, attack=0.03)
    if kind == "siku":
        a = inst.flute(f, dur, breath=0.38, vib=0.004, bright=0.25, attack=0.05)
        b = inst.flute(f * 1.004, dur, breath=0.3, vib=0.003, bright=0.2, attack=0.07)
        return a * 0.6 + b * 0.4
    raise KeyError(kind)


def hit(inst, kind):
    return {
        "frame": lambda: inst.drum(95, 0.18, snap=0.35, band=(900, 4000)),
        "frame_deep": lambda: inst.drum(70, 0.3, snap=0.25, band=(500, 2500)),
        "tap": lambda: inst.drum(240, 0.05, snap=0.5, band=(2000, 6000), drop=0.1, length=0.3),
        "taiko": lambda: inst.drum(62, 0.55, snap=0.2, band=(300, 1500), drop=0.35, length=1.6),
        "taiko_rim": lambda: inst.drum(420, 0.04, snap=0.7, band=(2500, 7000), drop=0.05, length=0.25),
        "drum_low": lambda: inst.drum(80, 0.35, snap=0.25, band=(400, 2000), length=1.2),
        "woodblock": lambda: inst.drum(820, 0.03, snap=0.2, band=(1500, 4000), drop=0.02, length=0.2),
        "bass": lambda: inst.drum(58, 0.28, snap=0.15, band=(300, 1200), length=1.0),
        "snare": lambda: inst.drum(190, 0.09, snap=1.1, band=(1500, 5000), drop=0.1, length=0.5),
        "daf": lambda: inst.drum(85, 0.22, snap=0.35, band=(800, 3500), jingle=0.35),
        "bombo": lambda: inst.drum(66, 0.32, snap=0.3, band=(600, 3000), length=1.1),
    }[kind]()


def compose(name, p, seed):
    rng = np.random.default_rng(seed)
    inst = Inst(rng)
    beat = 60.0 / p["bpm"]
    bar = p["beats"]
    intro, outro = 2, 3
    sections = [("A", p["melody"]), ("B", p["melody2"]), ("A", p["melody"]), ("B2", p["melody"])]
    bars_total = intro + 8 * len(sections) + outro
    mix = Mix(bars_total * bar * beat + 4)
    tonic, scale = p["tonic"], p["scale"]
    n = len(scale)

    themeA = theme(rng, p, p["start"], p["cadence"])
    themeB = theme(rng, p, p["start"] + 2, 4 if p["cadence"] == 0 else 0)

    # drone through the whole piece, in long overlapping notes
    for k in range(0, bars_total, 4):
        dur = 4 * bar * beat + 0.8
        for i, d in enumerate(p["drone"]):
            x = inst.organ(freq_of(tonic / 2, scale, d), dur, attack=1.2)
            mix.put(x, k * bar * beat, gain=0.11 if i == 0 else 0.07, pan=-0.5 if i == 0 else 0.5)

    def chords_for(section):
        return p["chordsB"] if section.startswith("B") else p["chordsA"]

    def accomp(bar_index, root, gain=0.32, final=False):
        start = bar_index * bar * beat
        tones = [root, root + 2, root + 4, root + 7] if n >= 7 else [root, root + 1, root + 2, root + 3]
        pattern = [0, 2, 1, 2] if bar == 4 else [0, 1, 2]
        for b in range(bar):
            if final and b > 0:
                break
            d = tones[pattern[b % len(pattern)]]
            f = freq_of(tonic, scale, d) / (2 if d > n else 1)
            mix.put(play(inst, p["accomp"], f, beat * (bar if final else 0.95)), start + b * beat, gain=gain * (1.0 if b == 0 else 0.75), pan=-0.35)
        mix.put(play(inst, p["accomp"], freq_of(tonic / 2, scale, root), beat * bar), start, gain=gain * 0.8, pan=-0.2)

    def drums(bar_index, gain=0.5):
        start = bar_index * bar * beat
        for b, kind, g in p["drums"]:
            mix.put(hit(inst, kind), start + b * beat + rng.normal(0, 0.004), gain=gain * g * rng.uniform(0.9, 1.05), pan=0.25)
        for b in p.get("sistrum", []):
            mix.put(inst.sistrum(), start + b * beat, gain=gain * 0.35, pan=0.45)

    # intro: drone, drum and accompaniment
    for k in range(intro):
        accomp(k, p["chordsA"][k % 4], gain=0.28)
        drums(k, gain=0.35 + 0.1 * k)
    if p.get("gong"):
        mix.put(inst.gong(98), 0, gain=0.35, pan=0.1)

    bar_at = intro
    for si, (section, kind) in enumerate(sections):
        th = themeB if section.startswith("B") else themeA
        octave = n if (section == "B2" and kind in ("ney", "shakuhachi", "dizi", "siku", "fife", "aulos")) else 0
        if kind in ("horn",):
            octave = -n
        chords = chords_for(section)
        for k in range(8):
            accomp(bar_at + k, chords[(k // 2) % 4])
            drums(bar_at + k, gain=0.5 if section != "B" else 0.42)
        for pos, d, deg in th:
            t0 = (bar_at * bar + pos) * beat + rng.normal(0, 0.006)
            dd = deg + (0 if section != "B2" else (1 if rng.random() < 0.15 else 0))
            f = freq_of(tonic, scale, dd + octave)
            gain = 0.62 if kind in ("brass", "horn", "fiddle", "aulos") else 0.7
            if kind in ("lyre", "koto", "guzheng", "santur", "harp", "charango", "kithara", "lute"):
                gain = 0.85
                if d >= 1.5 and kind == "santur":                                   # santur tremolo on long notes
                    for r in range(int(d * 4)):
                        mix.put(play(inst, kind, f, beat * 0.25), t0 + r * beat * 0.25, gain=gain * (0.75 if r else 1), pan=0.05)
                    continue
            mix.put(play(inst, kind, f, d * beat * 0.97), t0, gain=gain, pan=0.05)
        if p.get("gong") and si % 2 == 1:
            mix.put(inst.gong(98), (bar_at + 8) * bar * beat - 0.05, gain=0.3, pan=0.1)
        bar_at += 8

    # outro: the theme's opening, slower, over the drone, then the last chord
    for k in range(outro):
        accomp(bar_at + k, p["chordsA"][0] if k == outro - 1 else p["chordsA"][k], gain=0.26, final=k == outro - 1)
        if k < outro - 1:
            drums(bar_at + k, gain=0.32 - 0.1 * k)
    for pos, d, deg in [n_ for n_ in themeA if n_[0] < bar * 2]:
        t0 = (bar_at * bar + pos * 1.25) * beat
        mix.put(play(inst, p["melody"], freq_of(tonic, scale, deg), d * beat * 1.2), t0, gain=0.5, pan=0.05)
    mix.put(play(inst, p["melody"], freq_of(tonic, scale, 0), bar * beat * 1.5), (bar_at + outro - 1) * bar * beat, gain=0.55, pan=0.05)

    L, R = reverb(mix.L, mix.R, rng, seconds=2.6, mix=0.3)
    return finish(L, R, peak=0.78)


def sting(name, p, seed):
    """Two or three seconds: the nation's call over its drone, with a drum stroke."""
    rng = np.random.default_rng(seed + 99)
    inst = Inst(rng)
    beat = 60.0 / (p["bpm"] * 1.6)
    total = sum(d for _, d in p["sting"]) * beat + 1.6
    mix = Mix(total)
    tonic, scale = p["tonic"], p["scale"]
    for d in p["drone"]:
        mix.put(inst.organ(freq_of(tonic / 2, scale, d), total - 1.5, attack=0.25), 0, gain=0.14, pan=0.0)
    first_drum = p["drums"][0][1]
    mix.put(hit(inst, first_drum), 0, gain=0.6)
    at = 0.05
    kind = p["melody"] if p["melody"] not in ("fiddle",) else "horn"
    for deg, d in p["sting"]:
        mix.put(play(inst, kind, freq_of(tonic, scale, deg), d * beat * 0.97), at, gain=0.8)
        at += d * beat
    mix.put(hit(inst, first_drum), at - p["sting"][-1][1] * beat, gain=0.45)
    if p.get("gong"):
        mix.put(inst.gong(98, 3.0), at - p["sting"][-1][1] * beat, gain=0.35)
    if p.get("sistrum"):
        mix.put(inst.sistrum(), 0.02, gain=0.3)
    L, R = reverb(mix.L, mix.R, rng, seconds=1.3, mix=0.24)
    L, R = finish(L, R, peak=0.85)
    mono = (L + R) * 0.5
    return mono / (np.max(np.abs(mono)) + 1e-9) * 0.85


def encode_ogg(wav, ogg):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-c:a", "libvorbis", "-q:a", "3", ogg], check=True)
    os.remove(wav)


if __name__ == "__main__":
    only = sys.argv[1:]
    for i, (name, p) in enumerate(NATIONS.items()):
        if only and name not in only:
            continue
        seed = 3600 + i * 17
        L, R = compose(name, p, seed)
        wav = os.path.join(TMP, f"HE_Music_{name}.wav")
        write_wav(wav, L, R)
        ogg = os.path.join(ROOT, "Music", f"HE_Music_{name}.ogg")
        os.makedirs(os.path.dirname(ogg), exist_ok=True)
        encode_ogg(wav, ogg)
        s = sting(name, p, seed)
        write_wav(os.path.join(ROOT, f"HE_Sting_{name}.wav"), s)
        print(f"{name}: music {len(L) / SR:.0f}s ({os.path.getsize(ogg) // 1024} KB), sting {len(s) / SR:.1f}s")
