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


CUTS = {}     # naam: (stem(men), t0, t1, toets, band, loop (s vanaf begin) of None)
RATES = {}    # afwijkende samplerate per knipsel (Hz)
# v4 (Jordi over v3: 'lo klopt alleen de eerste toon', 'oth loopt een noot en verdwijnt', 'oth2 als een vastslaande
# cd-speler', 'bas een rare remix'): geen geraden noten en geen herhaalde halve maten meer waar het origineel doorloopt.
#  intro: maat 1-4 van het origineel zelf, alle stems samen (= de mix), als één sample; de drums van de intro zitten erin
CUTS['ruinous_intro'] = (('other', 'piano', 'vocals', 'bass', 'drums'), at(1, 0), at(5, 0), 60, None, None)
#  lo58: het lage instrument (stem 'piano') in maat 5-8 als één frase; inhoud < 2 kHz, dus 8 kHz
CUTS['ruinous_lo58'] = ('piano', at(5, 0), at(9, 0), 60, None, None)
RATES['ruinous_lo58'] = 8000
#  ostbar: het ostinato met de diepe strijker-bourdon B2 ('bijna keelzang', Jordi) - hele maat 8 van de stem 'other'
CUTS['ruinous_ostbar'] = ('other', at(8, 0), at(9, 0) + 0.08, 60, (55, 5000), None)   # v6: tot 5 kHz (was 2,6: 'muffled')
#  ostbar2: maat 66-69 hebben die bourdon niet: hele maat 67
CUTS['ruinous_ostbar2'] = ('other', at(67, 0), at(68, 0) + 0.08, 60, (55, 2600), None)
#  pad: het aangehouden B3+F#4 van de grooves (stem 'other' < 450 Hz, zonder de lijn erboven), hele maat 19;
#  per maat aangeslagen en naar de grondtoon getransponeerd, net als het ostinato
CUTS['ruinous_pad'] = ('other', at(19, 0), at(20, 0) + 0.08, 60, (160, 450), None)
#  pad_g: in de G-maten ligt het pad in octaven (G3 + G4, gemeten maat 26-50): eigen knipsel uit maat 33
CUTS['ruinous_pad_g'] = ('other', at(33, 0), at(34, 0) + 0.08, 60, (160, 450), None)
#  pad_mNN: maten waar het pad van het origineel anders ligt (in de A/B chroma < 0,75 met het getransponeerde B/G-pad:
#  de D/A-Bm-Em-maten 36-39 en de roffels/opbouw 52-64): het eigen stuk van die maat (< 450 Hz)
PAD_OWN = (36, 37, 38, 39) + tuple(range(52, 65))
for _b in PAD_OWN:
    CUTS['ruinous_pad_m%d' % _b] = ('other', at(_b, 0), at(_b + 1, 0) + 0.08, 60, (160, 450), None)
#  het pad bevat alleen < 450 Hz: 4 kHz is genoeg (6,4 KB per maat i.p.v. 17,6 KB)
for _n in ['ruinous_pad', 'ruinous_pad_g'] + ['ruinous_pad_m%d' % _b for _b in PAD_OWN]:
    RATES[_n] = 4000
#  bass: één B1 uit de basstem (maat 19, 16e 11-13: alleen B1 + boventonen, 0,3 s) met zijn natuurlijke uitklank;
#  de noten zelf komen noot voor noot uit de basstem (pyin per 16e)
CUTS['ruinous_bass'] = ('bass', at(19, 11) - 0.005, at(19, 14), 35, (30, 3000), None)
#  v6 (Jordi over v5: 'vanaf 6 s is de hoofdmelodie te weggedrukt, te muffled, vanaf 19-20 s ook'; 'het instrument
#  vanaf 31 s is te veel blazer en te weinig strijker'):
#  wide14/wide18: maat 13-20 hadden alleen het pad (< 450 Hz); de hoge ostinatolijn (B5-C6, maat 13-16) en de B4-lijn
#  (17-20) uit de stem 'other' ontbraken (gemeten -10 tot -20 dB boven 500 Hz). Hele maat 14 / 18, 160-5000 Hz.
CUTS['ruinous_wide14'] = ('other', at(14, 0), at(15, 0) + 0.08, 60, (160, 5000), None)
CUTS['ruinous_wide18'] = ('other', at(18, 0), at(19, 0) + 0.08, 60, (160, 5000), None)
#  call: de aangehouden roep F5 -> F#5 van maat 5-12 (stem 'vocals', 300-5500 Hz) ontbrak; één F#5 uit maat 10
#  (16e 4-12), harmonisch gemaskerd, ping-pong-loop.  str: de strijker vanaf maat 21 (stem 'other', 560-4000 Hz):
#  F#5 uit maat 21 (16e 3-11), harmonisch gemaskerd (de ostinato-lekkage -12 dB, strijkruis blijft), i.p.v. de
#  stock-strijkers (aanzet 255 = koperachtig; 1-4 kHz +4..+7 dB te helder gemeten).
CUTS['ruinous_call'] = ('vocals', at(10, 4), at(10, 12), 78, (300, 5500), 'held')
#  v7 (Jordi over v6: 'je probeert strijkers met blazers na te maken; totaal anders'): vanaf maat 21 speelt een
#  strijkerssectie in akkoorden (F#5 + D#6 + F#6 + A#6 tegelijk, geen samenhangend vibrato: ensemble), geen solo-
#  lijn. Dus geen noten meer maar halve maten uit de stem 'other' (450-5000 Hz, 6 kHz), hergebruikt waar het
#  origineel zich herhaalt (keuze: ruinous_theme.SEC_MAP, gemeten met chroma per 8e + spectrum).
SEC_SRC = [40, 41, 42, 43, 64, 72, 90, 92, 97, 99]   # halve maten: 2 x (maat - 1) + 0/1
for _h in SEC_SRC:
    CUTS['ruinous_sec%d' % _h] = ('other', at(_h // 2 + 1, 8 * (_h % 2)), at(_h // 2 + 1, 8 * (_h % 2) + 8) + 0.08, 60,
                                  (450, 5000), None)
    RATES['ruinous_sec%d' % _h] = 6000
SHELF = {}   # dB (v6: strijkerknipsel)
WHOLE = tuple('ruinous_sec%d' % _h for _h in SEC_SRC) + ('ruinous_wide14', 'ruinous_wide18', 'ruinous_intro', 'ruinous_lo58', 'ruinous_ostbar', 'ruinous_ostbar2', 'ruinous_pad', 'ruinous_pad_g') + tuple(
    'ruinous_pad_m%d' % _b for _b in PAD_OWN)   # niet hertonen


def make_held(name):
    """aangehouden noot uit een stem: gestemd, harmonisch masker (deeltonen +-35 ct, de rest -12 dB: lekkage van
    andere partijen weg, strijkruis blijft zwak), aanzet 0,12 s + ping-pong-loop van het aangehouden deel."""
    stem, t0, t1, key, bnd, _ = CUTS[name]
    x = band(read_stem(stem, t0 - 0.005, t1), *bnd)
    x, cents = tune(x - np.mean(x), key)
    nom = 440.0 * 2 ** ((key - 69) / 12)
    nf, hop = 4096, 256
    win = np.hanning(nf)
    pad = np.concatenate([np.zeros(nf), x, np.zeros(nf)])
    fq = np.fft.rfftfreq(nf, 1 / SR)
    m = np.full(len(fq), 10 ** (-12 / 20))
    for h in range(1, 12):
        c = nom * h
        m[(fq > c * 2 ** (-0.35 / 12) - 6) & (fq < c * 2 ** (0.35 / 12) + 6)] = 1.0
    y = np.zeros(len(pad)); wsum = np.zeros(len(pad))
    for i in range(0, len(pad) - nf, hop):
        y[i:i + nf] += np.fft.irfft(np.fft.rfft(pad[i:i + nf] * win) * m, nf) * win
        wsum[i:i + nf] += win ** 2
    x = (y / np.maximum(wsum, 1e-6))[nf:nf + len(x)]
    if name in SHELF:                  # hoge plank boven 1,2 kHz (zwaartepunt gelijk aan de stem)
        X = np.fft.rfft(x); fq2 = np.fft.rfftfreq(len(x), 1 / SR)
        X *= 1 + (10 ** (SHELF[name] / 20) - 1) / (1 + (1200 / np.maximum(fq2, 1)) ** 2)
        x = np.fft.irfft(X, len(x))
    att, xf = int(0.12 * SR), int(0.08 * SR)
    sus = x[att:]
    w = np.linspace(0, np.pi / 2, xf)
    body = np.concatenate([sus[:-xf], sus[-xf:] * np.cos(w) + sus[::-1][:xf] * np.sin(w), sus[::-1][xf:]])
    x = np.concatenate([x[:att], body])
    x[-xf:] = x[-xf:] * np.cos(w) + x[att - xf:att] * np.sin(w)
    x = fade_in_out(x, 0.003, 0.0001)
    return norm(x), (att, len(x)), cents


def make_cut(name):
    stem, t0, t1, key, bnd, lp = CUTS[name]
    if lp == 'held':
        return make_held(name)
    stems = stem if isinstance(stem, tuple) else (stem,)
    x = sum(read_stem(s, t0, t1) for s in stems)
    if bnd:
        x = band(x, *bnd)
    x = x - np.mean(x)
    if name in WHOLE:
        cents = 0.0
    else:
        x, cents = tune(x, key)
    # maatknipsels lopen 80 ms door: de laatste 60 ms vloeien uit over de aanzet van de volgende maat (geen dip)
    x = fade_in_out(x, 0.003, 0.06 if name in WHOLE and name not in ('ruinous_intro', 'ruinous_lo58') else
                    (0.025 if lp else 0.05))
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
            rate = RATE
        else:
            src = CUTS[name][0]
            if not all(os.path.exists(STEMS + st + '.wav') for st in (src if isinstance(src, tuple) else (src,))):
                print('%s: stem ontbreekt, bestaande wav blijft' % name)
                continue
            x, lpx, cents = make_cut(name)
            key = CUTS[name][3]
            rate = RATES.get(name, RATE)
            a = norm(resample(x, SR, rate))
            lp = (int(lpx[0] * rate / SR), int(lpx[1] * rate / SR)) if lpx else None
            info = ', gestemd %+.0f ct%s' % (-cents, ', loop %.2f-%.2f s' % (lp[0] / rate, lp[1] / rate) if lp else '')
        write_wav(OUT + name + '.wav', a, rate, key, lp)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (
                label, name)
        total += len(a) + 16
        sp = np.abs(np.fft.rfft(a)) ** 2; fr = np.fft.rfftfreq(len(a), 1 / rate)
        print('%-16s %5d samples (%.2f s), < 60 Hz %4.1f%%, < 150 Hz %4.1f%%, > 2k %4.1f%%%s' % (
            name, len(a), len(a) / rate, 100 * sp[fr < 60].sum() / sp.sum(), 100 * sp[fr < 150].sum() / sp.sum(),
            100 * sp[fr > 2000].sum() / sp.sum(), info))
    open(DATA, 'w').write(inc)
    print('totaal %.1f KB' % (total / 1024))


if __name__ == '__main__':
    main(sys.argv[1:] or None)
