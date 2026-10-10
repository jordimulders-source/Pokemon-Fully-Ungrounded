#!/usr/bin/env python3
"""Project Grounded: eigen sample voor Area Zero (areazero_theme.py).

az_crystal: het 'kristal'-belletje van Area Zero (sinus + zwakke boventonen, snelle aanzet, lange uitsterving).
Gesynthetiseerd (geen FluidR3 nodig), grondtoon C6, 16 kHz (resample_wav.py: grondtoon >= C6 -> 16000 Hz), geen loop
(sterft vanzelf uit). Stock-glockenspiel/unknown_bell klinken een kwarttoon vals op toets 60 (gemeten: 1361 Hz en
1227 Hz), dus voor een arpeggio dat precies moet kloppen niet bruikbaar.
v3 (Jordi: 'de YEEEEHOOOOO HO-koorroepen en de onnatuurlijke aria vanaf ±46 s heb je nog niet goed nagemaakt'):
alle vocalen komen uit het origineel zelf (Spleeter-vocals-stem), 11025 Hz:
  az_voice / az_voice_lo: de aria-stem, één aangehouden toon (m26 F5, 50,25-51,35 s; m30 Bb4, 58,3-59,9 s), met de
     eigen vibrato; loop = geheel aantal vibratoperiodes, gecrossfaded; gestemd op precies F5 / Bb4 (de stem zingt
     daar ±0,5 halve toon hoger dan de noot).
  az_choir_NN: de koorroepen m8-24, per akkoord de echte aanzet + klinker van het origineel ('YEEE', 'HOOO'), op de eigen
     toonhoogte (kit-regel = eigen toonhoogte), lange akkoorden met een loop in de aanhouding.
Bron: <scratchpad>/az/stems/areazero/vocals.wav (niet in de repo; ontbreekt hij, dan blijft de bestaande wav staan).
Gebruik: python3 tools/grounded/areazero_samples.py [vocals.wav]"""
import os, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sample_utils import write_wav

OUT = 'sound/direct_sound_samples/grounded'


def crystal(rate=16000, key=84, dur=0.9):
    f0 = 440 * 2 ** ((key - 69) / 12)
    t = np.arange(int(rate * dur)) / rate
    x = np.zeros_like(t)
    # (verhouding, sterkte, uitsterftijd s): grondtoon draagt, octaaf + licht onharmonische glans sterven snel
    for r, a, d in ((1.0, 1.0, 0.45), (2.0, 0.30, 0.18), (3.01, 0.12, 0.09), (4.18, 0.05, 0.05)):
        x += a * np.sin(2 * np.pi * f0 * r * t) * np.exp(-t / d)
    att = np.minimum(1, t / 0.004)                     # 4 ms aanzet: tik zonder klik
    x *= att
    x[-int(rate * 0.05):] *= np.linspace(1, 0, int(rate * 0.05))
    return x / np.abs(x).max() * 0.95


VOCALS = '/tmp/claude-0/-home-user-projectgrounded/ffd47e46-6a2e-5021-9ef2-b627d7dbd889/scratchpad/az/stems/areazero/vocals.wav'
# v4 (Jordi: 'koor loopt de hele tijd i.p.v. dat de toon doorklinkt; aria hapert; vocals iets te muffled'): langere
# stukken (aria m34 F5 66,2-68,1 s), loops van >= 1 s met een gelijk-vermogen-crossfade, 16 kHz (uitgezonderd in
# resample_wav.py --all).
RATE = 16000
VOICES = [('az_voice', 66.20, 68.10, 77, 600, 820), ('az_voice_lo', 58.30, 60.10, 70, 420, 520)]
BAR1 = 0.185                               # maat 1 in het origineel (s)
# koorroepen: (maat, zestiende, lengte in zestienden) = theme CHOIR_EVENTS; sample = aanzet + max. 1,0 s
CHOIR_EVENTS = [(8, 4, 12), (9, 0, 24), (12, 0, 32), (14, 0, 16), (15, 0, 12), (15, 12, 4), (16, 0, 28), (17, 12, 4),
                (18, 0, 4), (18, 4, 4), (20, 0, 32), (22, 0, 16), (23, 0, 8), (23, 8, 8), (24, 0, 8), (24, 8, 8)]


def _read(src, t0, t1):
    w = wave.open(src)
    sr = w.getframerate()
    w.setpos(int(t0 * sr))
    raw = np.frombuffer(w.readframes(int((t1 - t0) * sr)), np.int16).astype(float)
    x = raw.reshape(-1, w.getnchannels()).mean(1) / 32768
    return x - np.convolve(x, np.ones(441) / 441, 'same'), sr      # gelijkstroom/brom < 50 Hz eruit


def _to_rate(x, sr, rate):
    X = np.fft.rfft(x)
    X[int(len(X) * 0.9 * rate / sr):] = 0                         # anti-alias
    x = np.fft.irfft(X, len(x))
    return np.interp(np.arange(int(len(x) * rate / sr)) * sr / rate, np.arange(len(x)), x)


def _pitch(x, sr, lo=600, hi=820):
    """gemiddelde grondtoon (Hz) via autocorrelatie per 40 ms-venster, mediaan in centen."""
    n, out = int(sr * 0.04), []
    for i in range(0, len(x) - n, n // 2):
        w = x[i:i + n] * np.hanning(n)
        ac = np.correlate(w, w, 'full')[n - 1:]
        a, b = int(sr / hi), int(sr / lo)
        k = a + int(np.argmax(ac[a:b]))
        if 0 < k < len(ac) - 1:                    # parabolische interpolatie
            y0, y1, y2 = ac[k - 1], ac[k], ac[k + 1]
            k = k + 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2 + 1e-12)
        out.append(12 * np.log2(sr / k / 440) + 69)
    return 440 * 2 ** ((np.median(out) - 69) / 12)


def _loop(x, rate, s0, lmin, lmax, fade_frac=0.3):
    """beste loop vanaf s0 (lengte lmin..lmax s), einde gecrossfaded (gelijk vermogen) met wat vóór s0 staat."""
    best, L = -2, 0
    for cand in range(int(lmin * rate), min(len(x) - s0 - 1, int(lmax * rate))):
        a, b = x[s0:s0 + 400], x[s0 + cand:s0 + cand + 400]
        if len(b) < 400:
            break
        c = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)
        if c > best:
            best, L = c, cand
    e = s0 + L
    fade = min(int(L * fade_frac), s0)
    y = x[:e].copy()
    t = np.linspace(0, np.pi / 2, fade)
    y[e - fade:e] = y[e - fade:e] * np.cos(t) + x[s0 - fade:s0] * np.sin(t)
    return y, (s0, e), best


def voice(name, t0, t1, key, lo, hi, src=VOCALS, rate=RATE):
    x, sr = _read(src, t0, t1)
    f = _pitch(x, sr, lo, hi)
    target = 440 * 2 ** ((key - 69) / 12)
    r = target / f                                                 # lees met stap r: r < 1 = omlaag
    x = np.interp(np.arange(int(len(x) / r)) * r, np.arange(len(x)), x)
    x = _to_rate(x, sr, rate)
    y, loop, c = _loop(x, rate, int(0.40 * rate), 1.0, min(1.45, len(x) / rate - 0.42), 0.35)
    y[:int(0.03 * rate)] *= np.linspace(0, 1, int(0.03 * rate))   # zachte aanzet (de voicegroup doet de rest)
    print('%s: gemeten %.1f Hz (%+.2f halve toon t.o.v. de noot), loop %d-%d (%.3f s, aansluiting %.3f)'
          % (name, f, 12 * np.log2(f / target), loop[0], loop[1], (loop[1] - loop[0]) / rate, c))
    return y / np.abs(y).max() * 0.95, loop


def choir(i, bar, pos, ln, src=VOCALS, rate=RATE):
    t = BAR1 + (bar - 1) * 2 + pos * 0.125
    dur = ln * 0.125
    take = min(dur, 2.0)                                          # v4: tot 2 s echt, daarna een loop van >= 1 s
    x, sr = _read(src, t - 0.02, t + take)
    x = _to_rate(x, sr, rate)
    loop = None
    if dur > take + 0.05:                                         # langer dan de knip: aanhouding loopen
        x, loop, c = _loop(x, rate, int(0.8 * rate), 1.0, 1.15, 0.4)
    else:
        x[-int(0.03 * rate):] *= np.linspace(1, 0, int(0.03 * rate))
    x[:int(0.01 * rate)] *= np.linspace(0, 1, int(0.01 * rate))
    pk = np.abs(x).max()
    print('az_choir_%02d: m%d.%02d, %.2f s geknipt, loop %s, piek %.3f' % (i, bar, pos, len(x) / rate, loop, pk))
    return x / pk * 0.95, loop, pk


def main():
    os.makedirs(OUT, exist_ok=True)
    write_wav(os.path.join(OUT, 'az_crystal.wav'), crystal(), 16000, 84, None)
    print('az_crystal.wav')
    src = sys.argv[1] if len(sys.argv) > 1 else VOCALS
    if not os.path.exists(src):
        print('vocals-stem niet gevonden: de stem-samples blijven zoals ze zijn')
        return
    for name, t0, t1, key, lo, hi in VOICES:
        y, loop = voice(name, t0, t1, key, lo, hi, src)
        write_wav(os.path.join(OUT, name + '.wav'), y, RATE, key, loop)
    gains = []
    for i, (bar, pos, ln) in enumerate(CHOIR_EVENTS):
        y, loop, pk = choir(i, bar, pos, ln, src)
        write_wav(os.path.join(OUT, 'az_choir_%02d.wav' % i), y, RATE, 60, loop)
        gains.append(pk)
    # relatieve luidheid per roep (genormaliseerde samples; het thema zet de velocity hiernaar)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'areazero_choir_gain.txt'), 'w').write(
        ' '.join('%.4f' % (g / max(gains)) for g in gains) + '\n')


if __name__ == '__main__':
    main()
