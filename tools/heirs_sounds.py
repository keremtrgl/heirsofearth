"""Synthesises the signature sounds of Heirs of Earth into HeirsOfEarth/Sounds/HeirsOfEarth/*.wav.

Usage: python tools/heirs_sounds.py  (scipy lives in the user site, so no -I)
horn  - a deep war horn (Nordheim storm horn, declarations of war)
bugle - a short brass call (Roman eagle, Hellenic aegis)
gong  - a large bronze gong (Tianxia dragon seal)
drum  - a field drum roll ending in two heavy beats (Albion war drum)
Everything is generated from sine partials and filtered noise: no samples, no third-party audio.
"""
import os
import wave

import numpy as np
from scipy.signal import butter, lfilter

SR = 44100
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "HeirsOfEarth", "Sounds", "HeirsOfEarth")
RNG = np.random.default_rng(7)


def t_axis(seconds):
    return np.arange(int(SR * seconds)) / SR


def lowpass(x, hz, order=2):
    b, a = butter(order, hz / (SR / 2), "low")
    return lfilter(b, a, x)


def bandpass(x, lo, hi, order=2):
    b, a = butter(order, [lo / (SR / 2), hi / (SR / 2)], "band")
    return lfilter(b, a, x)


def envelope(n, attack, release, total):
    t = np.arange(n) / SR
    env = np.minimum(1.0, t / max(attack, 1e-4))
    tail = total - release
    env *= np.where(t > tail, np.clip(1 - (t - tail) / release, 0, 1), 1.0)
    return env


def reverb(x, seconds=1.2, mix=0.25, tone=3500):
    n = int(SR * seconds)
    ir = RNG.standard_normal(n) * np.exp(-np.arange(n) / (SR * seconds / 5))
    ir = lowpass(ir, tone)
    ir /= np.sqrt(np.sum(ir ** 2))
    wet = np.convolve(x, ir)
    wet = np.concatenate([wet, np.zeros(max(0, len(x) + n - len(wet)))])[: len(x) + n]
    dry = np.concatenate([x, np.zeros(n)])
    return dry * (1 - mix) + wet * mix


def brass(freq, seconds, attack=0.08, release=0.12, bright=1.0, vibrato=0.0, bend=0.0):
    """A brass note: harmonics whose brightness follows the loudness, a small pitch bend into the note and a breath."""
    t = t_axis(seconds)
    env = envelope(len(t), attack, release, seconds)
    f = freq * (1 - bend * np.exp(-t / 0.06)) * (1 + vibrato * np.sin(2 * np.pi * 5.0 * t) * np.clip((t - 0.4) / 0.4, 0, 1))
    phase = 2 * np.pi * np.cumsum(f) / SR
    out = np.zeros_like(t)
    for h in range(1, 16):
        if freq * h > 9000:
            break
        amp = (1.0 / h ** 0.9) * env ** (1 + (h - 1) * 0.35 / bright)
        out += amp * np.sin(h * phase + RNG.uniform(0, 0.3))
    breath = lowpass(RNG.standard_normal(len(t)), 2400) * 0.03 * env
    return (out + breath) * env


def save(name, x, peak=0.85):
    x = x / (np.max(np.abs(x)) + 1e-9) * peak
    fade = int(SR * 0.02)
    x[-fade:] *= np.linspace(1, 0, fade)
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name + ".wav")
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())
    print(name, f"{len(x) / SR:.2f}s")


def horn():
    a = brass(98.0, 1.1, attack=0.22, release=0.18, bright=0.6, bend=0.06)
    b = brass(146.8, 1.7, attack=0.12, release=0.7, bright=0.7, vibrato=0.006, bend=0.04)
    gap = np.zeros(int(SR * 0.06))
    x = np.concatenate([a, gap, b])
    x = lowpass(x, 3200)
    save("HE_Horn", reverb(x, 1.6, 0.3, 2600))


def bugle():
    notes = [(392.0, 0.16), (523.3, 0.16), (659.3, 0.16), (784.0, 0.75)]
    parts = []
    for f, d in notes:
        parts.append(brass(f, d, attack=0.025, release=0.05 if d < 0.5 else 0.3, bright=1.4, vibrato=0.004 if d > 0.5 else 0, bend=0.03))
        parts.append(np.zeros(int(SR * 0.025)))
    x = lowpass(np.concatenate(parts), 6500)
    save("HE_Bugle", reverb(x, 1.3, 0.28, 4500))


def gong():
    seconds = 5.0
    t = t_axis(seconds)
    f0 = 92.0
    ratios = [1.0, 1.52, 2.0, 2.27, 2.74, 3.3, 4.1, 5.2, 6.4, 7.9]
    decays = [3.2, 2.6, 2.3, 2.0, 1.7, 1.4, 1.1, 0.8, 0.6, 0.45]
    out = np.zeros_like(t)
    for r, d in zip(ratios, decays):
        bloom = np.clip(t / (0.05 + 0.08 * r), 0, 1) ** 1.5
        for detune in (-0.0018, 0.0018):
            f = f0 * r * (1 + detune) * (1 + 0.012 * (1 - np.exp(-t / 0.6)))
            out += (1 / r ** 0.6) * bloom * np.exp(-t / d) * np.sin(2 * np.pi * np.cumsum(f) / SR + RNG.uniform(0, 6))
    hit = lowpass(RNG.standard_normal(len(t)), 900) * np.exp(-t / 0.03) * 2.0
    shimmer = bandpass(RNG.standard_normal(len(t)), 2500, 7000) * np.exp(-t / 1.4) * np.clip(t / 0.4, 0, 1) * 0.08
    x = out + hit + shimmer
    save("HE_Gong", reverb(x, 2.0, 0.22, 5000))


def drum():
    seconds = 2.3
    n = int(SR * seconds)
    x = np.zeros(n)

    def stroke(at, amp, body=190.0, snare=1.0, decay=0.09):
        m = int(SR * 0.4)
        t = np.arange(m) / SR
        tone = np.sin(2 * np.pi * body * t * (1 - 0.15 * (1 - np.exp(-t / 0.02)))) * np.exp(-t / decay)
        rattle = bandpass(RNG.standard_normal(m), 1500, 4800) * np.exp(-t / (decay * 1.4)) * snare
        s = int(SR * at)
        e = min(n, s + m)
        x[s:e] += amp * (tone * 1.0 + rattle * 0.5)[: e - s]

    at = 0.0
    k = 0
    while at < 1.25:
        crescendo = 0.25 + 0.6 * (at / 1.25)
        stroke(at, crescendo * (1.0 if k % 2 == 0 else 0.82) * RNG.uniform(0.9, 1.1))
        at += 0.042
        k += 1
    for at, amp in ((1.38, 1.6), (1.75, 1.9)):
        stroke(at, amp, body=120.0, snare=0.6, decay=0.16)
        m = int(SR * 0.5)
        t = np.arange(m) / SR
        s = int(SR * at)
        e = min(n, s + m)
        x[s:e] += amp * 1.4 * (np.sin(2 * np.pi * 58 * t) * np.exp(-t / 0.22))[: e - s]
    save("HE_Drum", reverb(x, 1.2, 0.2, 5000))


if __name__ == "__main__":
    horn()
    bugle()
    gong()
    drum()
