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
v3 (Jordi: 'het moet klinken als het origineel'): de melodische samples komen uit het origineel zelf (CUTS hieronder:
stem, tijd, grondtoon, loop); v1 (zaagtand-synth, stock-koto) en v2 (FluidR3-koto/shamisen, sinus-ostinato) zijn weg.
Gebruik: python3 tools/grounded/ruinous_samples.py [naam ...]   (daarna: python3 tools/grounded/resample_wav.py --all)"""
import os, sys, wave
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


# ---- v3: melodische samples uit het origineel zelf (Spleeter-stems), Jordi: 'het moet klinken als het origineel' ----
# Bron: <scratchpad>/az/stems/ruinous/<stem>.wav (44,1 kHz stereo, niet in de repo; ontbreekt hij, dan blijven de
# bestaande wav's staan). Maat m begint in het origineel op 0,366 + (m-1) x 1,5789 s (152 bpm, gemeten raster).
STEMS = '/tmp/claude-0/-home-user-projectgrounded/ffd47e46-6a2e-5021-9ef2-b627d7dbd889/scratchpad/az/stems/ruinous/'
S16 = 60 / 152 / 4
T0 = 0.070 + 3 * S16


def at(b, k):
    return T0 + ((b - 1) * 16 + k) * S16


def read_stem(stem, t0, t1):
    w = wave.open(STEMS + stem + '.wav')
    sr = w.getframerate()
    assert sr == SR
    w.setpos(int(t0 * sr))
    x = np.frombuffer(w.readframes(int((t1 - t0) * sr)), np.int16).astype(float)
    return x.reshape(-1, w.getnchannels()).mean(1) / 32768


def f0_of(x, key, sr=SR):
    """echte grondtoon rond de verwachte noot: per harmonische h1-h4 de FFT-piek (8x zero-padding) binnen +-60 cent,
    gewogen gemiddelde in cent (hogere harmonischen geven in een kort venster een preciezere toonhoogte)."""
    nom = 440.0 * 2 ** ((key - 69) / 12)
    seg = x[len(x) // 6:]
    X = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), 8 * len(seg))); fr = np.fft.rfftfreq(8 * len(seg), 1 / sr)
    cs, ws = [], []
    for h in (1, 2, 3, 4):
        sel = (fr > nom * h * 2 ** (-0.6 / 12)) & (fr < nom * h * 2 ** (0.6 / 12))
        i = np.argmax(X * sel)
        cs.append(1200 * np.log2(fr[i] / h / nom)); ws.append(X[i] * h)
    return nom * 2 ** (np.average(cs, weights=ws) / 1200)


def tune(x, key, sr=SR):
    """zuiver stemmen: resample zodat de gemeten grondtoon precies op de noot ligt; geeft (x, afwijking in cent)."""
    ratio = f0_of(x, key, sr) / (440.0 * 2 ** ((key - 69) / 12))
    n = int(len(x) * ratio)
    return np.interp(np.arange(n) / ratio, np.arange(len(x)), x), 1200 * np.log2(ratio)


def xloop(x, start, end, fade):
    """loop start..end (samples), crossfade van `fade` samples met wat vóór het loopbegin staat."""
    x = x[:end].copy()
    w = np.linspace(0, 1, fade)
    x[end - fade:end] = x[end - fade:end] * (1 - w) + x[start - fade:start] * w
    return x, (start, end)


def fade_in_out(x, a=0.004, b=0.04):
    x = x.copy(); na, nb = int(a * SR), int(b * SR)
    x[:na] *= np.linspace(0, 1, na); x[-nb:] *= np.linspace(1, 0, nb)
    return x


CUTS = {}     # naam: (stem, t0, t1, toets, band, loop (s vanaf begin) of None)
#  lo_e2: het lage Aziatische instrument van de intro, E2 (maat 1, 16e 1-7: alleen E2 met zijn eigen boventonen)
CUTS['ruinous_lo_e2'] = ('piano', at(1, 1) - 0.01, at(1, 8), 40, None, None)
#  lo_b3: hetzelfde instrument, B3 aangehouden (maat 5, de hele maat; de stem 'piano' heeft daar niets anders)
CUTS['ruinous_lo_b3'] = ('piano', at(5, 0) + 0.02, at(6, 0) - 0.02, 59, None, (0.45, 1.45))
#  ostbar: het ostinato (B3 + F#4 aangehouden, de frygische C4 op 16e 6), een halve maat uit de rustige maat 67
CUTS['ruinous_ostbar'] = ('other', at(67, 0), at(67, 8), 59, (90, 2600), None)
#  oth_*: de hele stem 'other' (pad B3+F#4, de 16e-figuur B4+F#5-E-C#, de hogere lijn) als halve maat per akkoord,
#  geknipt waar dat akkoord in het origineel klinkt; 30 ms langer dan een halve maat (overlap met de volgende aanslag)
OTH = {'B': (18, 0), 'E': (22, 0), 'G': (29, 0), 'Gm': (46, 8), 'Bm': (31, 0), 'Fs': (35, 0), 'DA': (36, 0),
       'Em': (38, 0), 'A': (52, 0)}
for _t, (_b, _k) in OTH.items():
    CUTS['ruinous_oth_' + _t] = ('other', at(_b, _k), at(_b, _k + 8) + 0.03, 60, (160, 5000), None)  # >160 Hz: geen baslek
#  bass: één basnoot E2 (maat 22, 16e 3-5: alleen E2 + boventonen; de B1 van maat 17 had een D2 erdoor) met zijn
#  natuurlijke uitklank
CUTS['ruinous_bass'] = ('bass', at(22, 3) - 0.005, at(22, 6) - 0.01, 40, (30, 3000), None)
WHOLE = ('ruinous_ostbar',) + tuple('ruinous_oth_' + t for t in OTH)      # meerdere tonen in één sample: niet hertonen, lengte = halve maat


def make_cut(name):
    stem, t0, t1, key, bnd, lp = CUTS[name]
    x = read_stem(stem, t0, t1)
    if bnd:
        x = band(x, *bnd)
    x = x - np.mean(x)
    if name in WHOLE:
        cents = 0.0
    else:
        x, cents = tune(x, key)
    x = fade_in_out(x, 0.003, 0.025 if (lp or name in WHOLE) else 0.05)
    loop = None
    if lp:
        a, z = int(lp[0] * SR), int(min(lp[1] * SR, len(x)))
        x, loop = xloop(x, a, z, int(0.25 * SR))
    return norm(x), loop, cents


SAMPLES = {   # naam: (functie, grondtoon) - synthetische drums (ongewijzigd sinds v1)
    'ruinous_taiko': (taiko, 60), 'ruinous_boom': (boom, 60), 'ruinous_ka': (ka, 60),
    'ruinous_impact': (impact, 60),
}


def main(only=None):
    global RNG
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    total = 0
    todo = [(n, 'synth') for n in SAMPLES] + [(n, 'cut') for n in CUTS]
    for name, kind in todo:
        if only and name not in only:
            continue
        if kind == 'synth':
            RNG = np.random.default_rng(683 + sum(name.encode()))     # vaste seed per sample: los of samen = identiek
            fn, key = SAMPLES[name]
            a, lp, info = norm(resample(fn(), SR, RATE)), None, ''
        else:
            if not os.path.exists(STEMS + CUTS[name][0] + '.wav'):
                print('%s: stem ontbreekt, bestaande wav blijft' % name)
                continue
            x, lpx, cents = make_cut(name)
            key = CUTS[name][3]
            a = norm(resample(x, SR, RATE))
            lp = (int(lpx[0] * RATE / SR), int(lpx[1] * RATE / SR)) if lpx else None
            info = ', gestemd %+.0f ct%s' % (-cents, ', loop %.2f-%.2f s' % (lp[0] / RATE, lp[1] / RATE) if lp else '')
        write_wav(OUT + name + '.wav', a, RATE, key, lp)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (
                label, name)
        total += len(a) + 16
        sp = np.abs(np.fft.rfft(a)) ** 2; fr = np.fft.rfftfreq(len(a), 1 / RATE)
        print('%-16s %5d samples (%.2f s), < 60 Hz %4.1f%%, < 150 Hz %4.1f%%, > 2k %4.1f%%%s' % (
            name, len(a), len(a) / RATE, 100 * sp[fr < 60].sum() / sp.sum(), 100 * sp[fr < 150].sum() / sp.sum(),
            100 * sp[fr > 2000].sum() / sp.sum(), info))
    open(DATA, 'w').write(inc)
    print('totaal %.1f KB' % (total / 1024))


if __name__ == '__main__':
    main(sys.argv[1:] or None)
