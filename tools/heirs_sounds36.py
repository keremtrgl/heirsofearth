"""Heirs of Earth 3.6: weapon and artifact sounds. Synthesised from sines and filtered noise like the rest; no samples.

Usage: python tools/heirs_sounds36.py   (scipy lives in the user site, so no -I)
Muskets and matchlocks, the flintlock pistol, the blunderbuss, the field cannon, torsion engines (scorpio, manuballista,
gastraphetes), the trebuchet and stone thrower, the sling, the repeating crossbow, fire lance and naft, fire arrow rockets,
the harpoon gun; and three artifact calls: the Kemet sistrum, the Pars karnay and the Inti conch.
"""
import os

import numpy as np

from heirs_music import Inst, ROOT, SR, bandpass, highpass, lowpass, write_wav

RNG = np.random.default_rng(3601)
I = Inst(RNG)


def t_axis(seconds):
    return np.arange(int(SR * seconds)) / SR


def noise(n):
    return RNG.standard_normal(n)


def place(out, x, at, gain=1.0):
    s = int(SR * at)
    e = min(len(out), s + len(x))
    out[s:e] += x[: e - s] * gain


def room(x, seconds=0.6, mix=0.18, tone=4000):
    n = int(SR * seconds)
    ir = RNG.standard_normal(n) * np.exp(-np.arange(n) / (SR * seconds / 5))
    ir = lowpass(ir, tone)
    ir /= np.sqrt(np.sum(ir ** 2))
    from scipy.signal import fftconvolve
    dry = np.concatenate([x, np.zeros(n)])
    wet = fftconvolve(x, ir)
    wet = np.concatenate([wet, np.zeros(max(0, len(dry) - len(wet)))])[: len(dry)]
    return dry * (1 - mix) + wet * mix


def save(name, x, peak=0.9):
    x = highpass(x, 30)
    x = x / (np.max(np.abs(x)) + 1e-9) * peak
    energy = np.abs(x)
    last = np.nonzero(energy > 0.003)[0]
    x = x[: (last[-1] if len(last) else len(x)) + int(SR * 0.05)]
    fade = int(SR * 0.03)
    x[-fade:] *= np.linspace(1, 0, fade)
    write_wav(os.path.join(ROOT, name + ".wav"), x)
    print(name, f"{len(x) / SR:.2f}s")


def boom(seconds, body=55, crack=1.0, dark=1800, decay=0.35):
    t = t_axis(seconds)
    blast = lowpass(noise(len(t)), dark) * np.exp(-t / decay)
    thump = np.sin(2 * np.pi * np.cumsum(body * (1 + 1.5 * np.exp(-t / 0.02))) / SR) * np.exp(-t / (decay * 0.8))
    snap = highpass(noise(len(t)), 2500) * np.exp(-t / 0.008) * crack
    return blast * 1.2 + thump * 1.0 + snap * 0.6


def powder_shot(name, seconds=1.6, pan_hiss=0.25, body=60, crack=0.8, dark=2200, decay=0.32):
    """Matchlock and flintlock: the pan flashes a moment before the charge goes."""
    out = np.zeros(int(SR * seconds))
    t = t_axis(0.09)
    hiss = bandpass(noise(len(t)), 2500, 8000) * np.clip(t / 0.01, 0, 1) * np.exp(-t / 0.05) * pan_hiss
    place(out, hiss, 0.0)
    place(out, boom(seconds - 0.06, body, crack, dark, decay), 0.06)
    save(name, room(out, 0.9, 0.22, 3500))


def flintlock():
    out = np.zeros(int(SR * 1.2))
    t = t_axis(0.03)
    click = bandpass(noise(len(t)), 3000, 9000) * np.exp(-t / 0.004)
    place(out, click, 0.0, 0.8)
    place(out, bandpass(noise(int(SR * 0.05)), 2500, 8000) * np.exp(-t_axis(0.05) / 0.02) * 0.3, 0.015)
    place(out, boom(1.1, body=85, crack=1.0, dark=2600, decay=0.22), 0.045)
    save("HE_Shot_Flintlock", room(out, 0.7, 0.2, 4000))


def blunderbuss():
    out = np.zeros(int(SR * 1.8))
    place(out, boom(1.7, body=48, crack=0.6, dark=1600, decay=0.42), 0.03)
    for k in range(10):                                                   # the shot spreading
        place(out, bandpass(noise(int(SR * 0.04)), 3000, 9000) * np.exp(-t_axis(0.04) / 0.01) * 0.25, 0.08 + k * 0.012 + RNG.uniform(0, 0.01))
    save("HE_Shot_Blunderbuss", room(out, 1.0, 0.25, 3000))


def cannon():
    out = np.zeros(int(SR * 3.0))
    place(out, boom(2.9, body=38, crack=0.5, dark=900, decay=0.7), 0.0)
    t = t_axis(2.2)
    rumble = lowpass(noise(len(t)), 220) * np.exp(-t / 0.9) * 1.4
    place(out, rumble, 0.1)
    save("HE_Shot_Cannon", room(out, 2.0, 0.3, 2000))


def torsion(name, f=180.0, wood=1.0, size=1.0):
    """Ballista and scorpio: the slider released, the sinew skein twanging, the frame knocking."""
    out = np.zeros(int(SR * 1.0))
    t = t_axis(0.5)
    twang = (np.sin(2 * np.pi * f * size * t * (1 + 0.25 * np.exp(-t / 0.03))) + 0.5 * np.sin(2 * np.pi * f * 2.03 * size * t)) * np.exp(-t / 0.09)
    knock = I.drum(140 / size, 0.06, snap=0.6, band=(600, 2500), drop=0.1, length=0.3) * wood
    whoosh = bandpass(noise(int(SR * 0.35)), 400, 2500) * np.sin(np.pi * np.clip(t_axis(0.35) / 0.35, 0, 1)) * 0.25
    place(out, knock, 0.0, 0.9)
    place(out, twang, 0.005, 0.8)
    place(out, whoosh, 0.03)
    save(name, room(out, 0.5, 0.15, 5000))


def trebuchet():
    out = np.zeros(int(SR * 2.4))
    for k in range(4):                                                    # the arm creaking as it swings
        t = t_axis(0.12)
        creak = bandpass(noise(len(t)), 300 + 90 * k, 900 + 120 * k) * (1 + np.sin(2 * np.pi * 38 * t)) * np.exp(-t / 0.05)
        place(out, creak, 0.0 + k * 0.09, 0.4)
    t = t_axis(0.8)
    whoosh = bandpass(noise(len(t)), 150, 900) * np.sin(np.pi * np.clip(t / 0.8, 0, 1)) ** 2
    place(out, whoosh, 0.2, 0.9)
    thud = I.drum(52, 0.35, snap=0.4, band=(200, 1200), drop=0.2, length=1.2)
    place(out, thud, 0.55, 1.1)                                           # the arm hits the crossbar
    rattle = I.drum(110, 0.12, snap=0.8, band=(400, 2500), drop=0.05, length=0.4)
    place(out, rattle, 0.62, 0.5)
    save("HE_Shot_Trebuchet", room(out, 1.2, 0.22, 3000))


def sling():
    out = np.zeros(int(SR * 0.9))
    for k in range(3):                                                    # two whirls and the release
        t = t_axis(0.18)
        w = bandpass(noise(len(t)), 600, 3200) * np.sin(np.pi * t / 0.18) ** 2 * (0.5 + 0.25 * k)
        place(out, w, k * 0.16)
    t = t_axis(0.25)
    snap = bandpass(noise(len(t)), 1500, 6000) * np.exp(-t / 0.012)
    zip_ = bandpass(noise(len(t)), 2000, 5000) * np.exp(-t / 0.06) * 0.4
    place(out, snap, 0.48, 0.9)
    place(out, zip_, 0.5)
    save("HE_Shot_Sling", room(out, 0.4, 0.12, 6000))


def repeater():
    out = np.zeros(int(SR * 0.7))
    for at, g in ((0.0, 0.6), (0.06, 0.4)):                              # lever clack, then the string
        place(out, I.drum(700, 0.02, snap=0.9, band=(1500, 6000), drop=0.02, length=0.12), at, g)
    t = t_axis(0.3)
    twang = np.sin(2 * np.pi * 260 * t * (1 + 0.2 * np.exp(-t / 0.02))) * np.exp(-t / 0.06)
    place(out, twang, 0.09, 0.7)
    place(out, bandpass(noise(int(SR * 0.2)), 800, 4000) * np.exp(-t_axis(0.2) / 0.05) * 0.3, 0.1)
    save("HE_Shot_Repeater", room(out, 0.35, 0.12, 6000))


def fire_jet(name, seconds=1.4, roar=1.0, pop=0.6):
    t = t_axis(seconds)
    env = np.clip(t / 0.05, 0, 1) * np.exp(-t / (seconds * 0.45))
    body = lowpass(noise(len(t)), 900) * (1 + 0.3 * np.sin(2 * np.pi * 13 * t)) * env * roar
    hiss = bandpass(noise(len(t)), 2000, 7000) * env * 0.35
    crackle = np.zeros_like(t)
    for _ in range(25):
        at = RNG.uniform(0.02, seconds * 0.7)
        place(crackle, bandpass(noise(int(SR * 0.01)), 2000, 8000) * np.exp(-t_axis(0.01) / 0.002), at, RNG.uniform(0.3, 1.0))
    out = body + hiss + crackle * 0.5
    place(out, boom(0.5, body=90, crack=0.4, dark=1500, decay=0.08), 0.0, pop)
    save(name, room(out, 0.8, 0.2, 4000))


def rockets():
    out = np.zeros(int(SR * 2.0))
    for k in range(5):                                                    # a ripple of fire arrows leaving the battery
        t = t_axis(1.0)
        f = 900 + 500 * t + RNG.uniform(-80, 80)
        whistle = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.08 * np.exp(-t / 0.5)
        hiss = bandpass(noise(len(t)), 1500, 6500) * np.clip(t / 0.02, 0, 1) * np.exp(-t / 0.35)
        place(out, hiss + whistle, k * 0.11 + RNG.uniform(0, 0.03), 0.6 + RNG.uniform(0, 0.3))
        place(out, I.drum(160, 0.03, snap=0.6, band=(800, 3000), drop=0.1, length=0.15), k * 0.11, 0.4)
    save("HE_Shot_FireArrows", room(out, 0.8, 0.2, 5000))


def harpoon():
    out = np.zeros(int(SR * 0.9))
    place(out, I.drum(120, 0.08, snap=0.8, band=(500, 3000), drop=0.15, length=0.4), 0.0, 1.0)
    t = t_axis(0.5)
    spring = np.sin(2 * np.pi * 85 * t * (1 + 0.6 * np.exp(-t / 0.02))) * np.exp(-t / 0.15) + 0.4 * np.sin(2 * np.pi * 410 * t) * np.exp(-t / 0.05)
    place(out, spring, 0.004, 0.8)
    rope = bandpass(noise(int(SR * 0.6)), 300, 1800) * np.exp(-t_axis(0.6) / 0.2) * 0.35
    place(out, rope, 0.05)
    save("HE_Shot_Harpoon", room(out, 0.4, 0.12, 5000))


def sistrum_call():
    out = np.zeros(int(SR * 2.6))
    for k, at in enumerate((0.0, 0.35, 0.7, 0.88, 1.06)):
        place(out, I.sistrum(0.7), at, 1.0 if k in (0, 3) else 0.75)
    place(out, I.drum(95, 0.2, snap=0.3, band=(900, 4000), length=0.8), 0.0, 0.5)
    place(out, I.drum(95, 0.2, snap=0.3, band=(900, 4000), length=0.8), 1.06, 0.6)
    place(out, I.bell(660, 1.6, 0.9), 1.06, 0.18)
    save("HE_Sistrum", room(out, 1.4, 0.28, 6000))


def karnay():
    """The long trumpet of Pars: two low brassy calls, the second rising."""
    a = I.brass(116.5, 1.0, bright=1.3, attack=0.12, bend=0.05)
    b = I.brass(116.5, 1.6, bright=1.4, attack=0.1, bend=0.05)
    t = t_axis(len(b) / SR)
    b2 = I.brass(155.6, 1.0, bright=1.4, attack=0.15, bend=0.02)
    out = np.zeros(int(SR * 4.0))
    place(out, a, 0.0)
    place(out, b, 1.15)
    place(out, b2, 2.0, 0.8)
    place(out, I.drum(85, 0.22, snap=0.35, band=(800, 3500), jingle=0.35), 1.15, 0.6)
    save("HE_Karnay", room(out, 1.6, 0.3, 3500))


def conch():
    """The Inti pututu: a breathy conch call that swells and falls."""
    out = np.zeros(int(SR * 3.6))
    for at, f, d in ((0.0, 233.1, 1.3), (1.4, 233.1, 0.5), (1.95, 261.6, 1.4)):
        x = I.flute(f, d, breath=0.45, vib=0.012, scoop=0.06, bright=0.9, attack=0.18)
        x += 0.5 * I.brass(f, d, bright=0.5, attack=0.2, bend=0.06)[: len(x)]
        place(out, x, at, 0.8)
    place(out, I.drum(66, 0.32, snap=0.3, band=(600, 3000), length=1.1), 1.95, 0.5)
    save("HE_Pututu", room(out, 1.8, 0.3, 3500))


if __name__ == "__main__":
    powder_shot("HE_Shot_Musket")
    powder_shot("HE_Shot_Matchlock", pan_hiss=0.45, body=70, crack=0.9, dark=2600, decay=0.26)
    flintlock()
    blunderbuss()
    cannon()
    torsion("HE_Shot_Scorpio", f=170, size=1.0)
    torsion("HE_Shot_Manuballista", f=230, size=1.2, wood=0.7)
    trebuchet()
    sling()
    repeater()
    fire_jet("HE_Shot_FireLance", 1.3, roar=1.0, pop=0.7)
    fire_jet("HE_Shot_Naft", 1.8, roar=1.3, pop=0.3)
    rockets()
    harpoon()
    sistrum_call()
    karnay()
    conch()
