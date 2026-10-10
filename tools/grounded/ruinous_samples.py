#!/usr/bin/env python3
"""Project Grounded: eigen samples voor Battle! Treasures of Ruin (ruinous_theme.py), voorvoegsel ruinous_*.

Gemeten aan de drumstem van het origineel (Spleeter, maat 17-32): de 'snare op elke tel' is eigenlijk een grote trom
(51% van de energie in 90-130 Hz, 23% in 130-200 Hz, ring tot -12 dB na ±250 ms, een korte tik erop); tussen de
tellen (de achtste 'en') valt een lage, korte dreun (30-90 Hz, -12 dB na ±90 ms). Hoog (> 3 kHz) maar 1-2%.
Op de GBA en Jordi's speakers geeft een luid laag onder ±60 Hz 'overload': de dreun ligt hier op 72 -> 62 Hz.
  ruinous_taiko   grote trom op de tel: vel 128 -> 104 Hz, twee hogere modi, korte vel-tik + houten rand, kamergalm
  ruinous_boom    lage dreun op de 'en': 78 -> 62 Hz, kort (±0,2 s), zachte klik (anders hoor je hem niet in 8 bit)
  ruinous_ka      de rand van de taiko (ka): droge tik voor roffels en opmaten
  ruinous_impact  de inslag (maat 5 en 65): lage trom + ruisuitbarsting + metalen naklank, ±1,1 s
  ruinous_synth   het elektronische ostinato: twee ontstemde zaagtanden door een dichtklappend resonant filter (pluk),
                  C4; korte, strakke aanzet (16en = 1 kanaal)
De koto (oosterse tokkel, vanaf maat 21) is de stock-Emerald-koto (unknown_koto_high), het ruisniveau en koper stock.
Gebruik: python3 tools/grounded/ruinous_samples.py [naam ...]   (daarna: python3 tools/grounded/resample_wav.py --all)"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sample_utils import resample, write_wav

OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'
SR = 44100
RATE = 11025
RNG = np.random.default_rng(683)


def band(x, lo, hi, sr=SR):
    f = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / sr)
    f[(fr < lo) | (fr > hi)] = 0
    return np.fft.irfft(f, len(x))


def soft_lowpass(x, hi, slope=500, sr=SR):
    f = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / sr)
    m = fr > hi
    f[m] *= np.exp(-(fr[m] - hi) / slope)
    return np.fft.irfft(f, len(x))


def norm(x, peak=0.97):
    return x / (np.abs(x).max() + 1e-12) * peak


def tail_fade(x, sec):
    n = int(sec * SR); x = x.copy(); x[-n:] *= np.linspace(1, 0, n) ** 1.5
    return x


def membrane(f_hi, f_lo, sweep, decay, dur, modes):
    t = np.arange(int(dur * SR)) / SR
    f = f_lo + (f_hi - f_lo) * np.exp(-t / sweep)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.zeros_like(t)
    for ratio, amp, dec in modes:
        x += amp * np.sin(ph * ratio) * np.exp(-t / (decay * dec))
    return x


def room(x, rt=0.18, mix=0.18):
    """korte kamergalm: ruis-impulsrespons met exponentiële staart (lowpass), zodat de trom 'groot' klinkt."""
    n = int(rt * 2.5 * SR)
    t = np.arange(n) / SR
    ir = band(RNG.standard_normal(n), 80, 3500) * np.exp(-t / (rt / 3))
    ir[0] = 0
    y = np.convolve(x, ir)[:len(x)]
    return x + mix * norm(y) * np.abs(x).max()


def taiko():
    dur = 0.5
    x = membrane(128, 104, 0.025, 0.14, dur, ((1.0, 1.0, 1.0), (1.5, 0.35, 0.55), (2.05, 0.18, 0.35)))
    n = len(x); t = np.arange(n) / SR
    m = int(0.02 * SR); tt = np.arange(m) / SR
    skin = band(RNG.standard_normal(m), 300, 2500) * np.exp(-tt / 0.004)       # bachi op het vel
    wood = band(RNG.standard_normal(m), 1200, 4500) * np.exp(-tt / 0.0015)     # tik
    x = norm(x)
    x[:m] += 0.42 * norm(skin) + 0.22 * norm(wood)
    x = np.tanh(1.5 * x) / np.tanh(1.5)
    x = room(x, 0.2, 0.16)
    x = band(x, 55, 20000)
    x = soft_lowpass(x, 3500, 600)
    return norm(tail_fade(x, 0.08))


def boom():
    dur = 0.24
    x = membrane(78, 62, 0.02, 0.07, dur, ((1.0, 1.0, 1.0), (1.6, 0.25, 0.5)))
    t = np.arange(len(x)) / SR
    m = int(0.012 * SR)
    click = band(RNG.standard_normal(m), 600, 2500) * np.exp(-np.arange(m) / SR / 0.002)
    x = norm(x)
    x[:m] += 0.16 * norm(click)
    # een tweede, hogere boventoon (2x) maakt hem op kleine speakers hoorbaar zonder meer sub
    x += 0.22 * np.sin(2 * np.pi * 2 * 64 * t) * np.exp(-t / 0.04)
    x = np.tanh(1.3 * norm(x)) / np.tanh(1.3)
    x = band(x, 50, 6000)
    return norm(tail_fade(x, 0.05))


def ka():
    dur = 0.1
    n = int(dur * SR); t = np.arange(n) / SR
    crack = band(RNG.standard_normal(n), 1200, 4500) * np.exp(-t / 0.004)
    body = np.sin(2 * np.pi * 820 * t) * np.exp(-t / 0.018) + 0.5 * np.sin(2 * np.pi * 1510 * t) * np.exp(-t / 0.01)
    low = np.sin(2 * np.pi * 180 * t) * np.exp(-t / 0.025)
    x = norm(crack) + 0.6 * norm(body) + 0.35 * low
    x = soft_lowpass(x, 4200, 500)
    return norm(tail_fade(x, 0.02))


def impact():
    dur = 1.1
    lo = membrane(96, 62, 0.06, 0.32, dur, ((1.0, 1.0, 1.0), (1.47, 0.4, 0.5), (2.1, 0.2, 0.3)))
    n = len(lo); t = np.arange(n) / SR
    burst = band(RNG.standard_normal(n), 300, 5000) * np.exp(-t / 0.09)
    metal = np.zeros(n)
    for f, a, d in ((410, 1.0, 0.5), (623, 0.7, 0.4), (887, 0.5, 0.33), (1270, 0.35, 0.25), (1730, 0.25, 0.2)):
        metal += a * np.sin(2 * np.pi * f * t + RNG.uniform(0, 6.3)) * np.exp(-t / d)
    metal = band(metal * (1 + 0.3 * band(RNG.standard_normal(n), 2, 30)), 300, 5000)
    x = 0.9 * norm(lo) + 0.55 * norm(burst) + 0.28 * norm(metal)
    x = np.tanh(1.6 * norm(x)) / np.tanh(1.6)
    x = room(x, 0.35, 0.22)
    x = band(x, 50, 20000)
    x = soft_lowpass(x, 4000, 600)
    return norm(tail_fade(x, 0.25))


def synth(key=60):
    """elektronische pluk: 2 zaagtanden (+-9 cent) + een sub-blok een octaaf lager, door een Chamberlin-SVF waarvan de
    cutoff in ±0,12 s van 3,2 kHz naar 450 Hz klapt (resonantie 0,55), lichte tanh."""
    dur = 0.32
    n = int(dur * SR); t = np.arange(n) / SR
    f0 = 440.0 * 2 ** ((key - 69) / 12)
    saw = lambda f: 2 * ((f * t) % 1.0) - 1
    x = 0.5 * saw(f0 * 2 ** (9 / 1200)) + 0.5 * saw(f0 * 2 ** (-9 / 1200)) + 0.25 * np.sign(np.sin(np.pi * f0 * t))
    fc = 450 + 2750 * np.exp(-t / 0.045)
    q = 0.55
    low = band_ = 0.0
    y = np.zeros(n)
    for i in range(n):
        f = 2 * np.sin(np.pi * fc[i] / SR)
        high = x[i] - low - q * band_
        band_ += f * high
        low += f * band_
        y[i] = low
    env = np.minimum(1, t / 0.002) * np.exp(-t / 0.11)
    y = np.tanh(1.8 * norm(y) * env) / np.tanh(1.8)
    y = soft_lowpass(y, 3600, 500)
    return norm(tail_fade(y, 0.05))


SAMPLES = {   # naam: (functie, grondtoon)
    'ruinous_taiko': (taiko, 60), 'ruinous_boom': (boom, 60), 'ruinous_ka': (ka, 60),
    'ruinous_impact': (impact, 60), 'ruinous_synth': (synth, 60),
}


def main(only=None):
    global RNG
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    total = 0
    for name, (fn, key) in SAMPLES.items():
        if only and name not in only:
            continue
        RNG = np.random.default_rng(683 + sum(name.encode()))     # vaste seed per sample: los of samen = identiek
        a = norm(resample(fn(), SR, RATE))
        write_wav(OUT + name + '.wav', a, RATE, key, None)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (
                label, name)
        total += len(a) + 16
        sp = np.abs(np.fft.rfft(a)) ** 2; fr = np.fft.rfftfreq(len(a), 1 / RATE)
        print('%-16s %5d samples (%.2f s), < 60 Hz %4.1f%%, < 150 Hz %4.1f%%, > 2k %4.1f%%' % (
            name, len(a), len(a) / RATE, 100 * sp[fr < 60].sum() / sp.sum(), 100 * sp[fr < 150].sum() / sp.sum(),
            100 * sp[fr > 2000].sum() / sp.sum()))
    open(DATA, 'w').write(inc)
    print('totaal %.1f KB' % (total / 1024))


if __name__ == '__main__':
    main(sys.argv[1:] or None)
