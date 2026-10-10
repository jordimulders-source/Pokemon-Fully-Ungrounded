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


def crystal(rate=16000, key=84, dur=1.3):
    f0 = 440 * 2 ** ((key - 69) / 12)
    t = np.arange(int(rate * dur)) / rate
    x = np.zeros_like(t)
    # (verhouding, sterkte, uitsterftijd s): grondtoon draagt, octaaf + licht onharmonische glans sterven snel
    # v5 (Jordi: 'de piepjes missen de helft'): in het origineel klinkt elke belnoot ±1 maat door (wolk van tonen);
    # grondtoon sterft nu in 1,3 s i.p.v. 0,45 s
    # v6 (Jordi: 'vanaf 4 s een echo die te lang blijft'): gemeten uitsterving in het origineel -6 dB na 0,25 s,
    # -11..-15 dB na 0,5 s, -20 dB na 0,75 s -> grondtoon 0,3 s
    for r, a, d in ((1.0, 1.0, 0.3), (2.0, 0.30, 0.15), (3.01, 0.12, 0.07), (4.18, 0.05, 0.04)):
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


def _read(src, t0, t1, dc=441):
    w = wave.open(src)
    sr = w.getframerate()
    w.setpos(int(t0 * sr))
    raw = np.frombuffer(w.readframes(int((t1 - t0) * sr)), np.int16).astype(float)
    x = raw.reshape(-1, w.getnchannels()).mean(1) / 32768
    return x - np.convolve(x, np.ones(dc) / dc, 'same'), sr        # gelijkstroom/brom < 50 Hz eruit (bas: dc groter)


# v8 (Jordi: 'op 22 s / 47 s te muffled'): gemeten weergaveketen (16 kHz-sample -> mixer 21 kHz -> GBA-uitgang, mGBA-
# opname) t.o.v. het origineel: -2 dB bij 2 kHz, -3,4 bij 4 kHz, -5,6 bij 6 kHz, -6,6 bij 7 kHz. De knippen krijgen het
# omgekeerde als voorversterking (Hz, dB), zodat de opname weer even helder is als het origineel.
EQ = [(0, 0.0), (1000, 0.0), (2000, 2.0), (3000, 2.5), (4000, 3.4), (5000, 4.6), (6000, 5.6), (7000, 6.6), (8000, 6.6)]


def _to_rate(x, sr, rate, eq=False):
    X = np.fft.rfft(x)
    if eq:
        fr = np.fft.rfftfreq(len(x), 1 / sr)
        X *= 10 ** (np.interp(fr, [p[0] for p in EQ], [p[1] for p in EQ]) / 20)
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
    x = _to_rate(x, sr, rate, eq=True)
    loop = None
    if dur > take + 0.05:                                         # langer dan de knip: aanhouding loopen
        x, loop, c = _loop(x, rate, int(0.8 * rate), 1.0, 1.15, 0.4)
    else:
        x[-int(0.03 * rate):] *= np.linspace(1, 0, int(0.03 * rate))
    x[:int(0.01 * rate)] *= np.linspace(0, 1, int(0.01 * rate))
    pk = np.abs(x).max()
    print('az_choir_%02d: m%d.%02d, %.2f s geknipt, loop %s, piek %.3f' % (i, bar, pos, len(x) / rate, loop, pk))
    return x / pk * 0.95, loop, pk


# v5 (Jordi: 'de aria klinkt nog niet overal even vloeiend; doe het zoals bij het koor'): de aria in hele frasen uit
# de vocals-stem (eigen aanzet, glijders en uitklink), elk een kitnoot op de eigen toonhoogte: (maat, 16e, lengte in 16en).
# m36 en m39 zitten niet in de vocals-stem (Spleeter: 'other'); die blijven noten op az_voice.
ARIA_PHRASES = [(24, 11, 44), (27, 13, 15), (29, 3, 54), (32, 13, 51), (37, 4, 28)]


def aria(j, bar, pos, ln, src=VOCALS, rate=RATE):
    t = BAR1 + (bar - 1) * 2 + pos * 0.125
    x, sr = _read(src, t - 0.03, t + ln * 0.125)
    x = _to_rate(x, sr, rate, eq=True)
    x[:int(0.01 * rate)] *= np.linspace(0, 1, int(0.01 * rate))
    x[-int(0.08 * rate):] *= np.linspace(1, 0, int(0.08 * rate))
    pk = np.abs(x).max()
    print('az_aria_%d: m%d.%02d, %.2f s' % (j, bar, pos, len(x) / rate))
    return x / pk * 0.95, pk


# v7 (Jordi: 'vanaf 8 s doen de piepjes hun eigen ding'): de hoge belletjeswolk (Ab6 C#7 Eb7 met wisselnoten en echo)
# is niet noot voor noot na te spelen; in de intro (m5-7) en de pauzes klinken in de 'other'-stem alleen de belletjes,
# dus die stukken komen als één geheel uit het origineel.
# v8 (Jordi: 'op 13 s lijkt de distorted melodie perfect te starten maar hij kapt meteen af; op 22 s veel te muffled'):
# de 'distorted melodie' is de aanzwellende, vervormde Eb-akkoordklank (Eb2 Bb2 Eb3 G3 F4 + ruis) die in het origineel
# van m7.75 tot m10.75 doorklinkt; de knip stopte op m8.4 en de PSG-bas/strijkers vulden dat niet (geen Eb2 in de
# opname). Ook de glans op 22 s (B-deel, 'other' 25-45% boven 2 kHz, wij 1%) zit in die stem. Nu de hele
# begeleiding m5-15 uit 'other' + 'bass' in drie aansluitende stukken (maat, 16e, lengte in 16en); het thema speelt
# stuk 1 en 2 nog eens op m16 en m20 (golfvorm-correlatie m12/m20 0.84, m13/m21 0.86; m8/m16 0.52, zelfde akkoorden).
OTHER = VOCALS.replace('vocals.wav', 'other.wav')
BASS = VOCALS.replace('vocals.wav', 'bass.wav')
# Ook onder de aria (m24-39; Jordi: 'de melodie op 47 s is te muffled'): 'other' daar 7 dB onder de stem en 29% boven
# 2 kHz, onze strijkers even luid als de stem en 1%. Stuk 4 en 5 = m24-31, het thema herhaalt ze op m32 en m36.
# Daar ook de 'drums'-stem erbij: die heeft naast de slagen de Eb2/Eb3-bromtoon (orgelpunt; zonder viel de chroma-
# correlatie van m25-27 van 0.88 naar 0.55-0.75).
BELL_RIPS = [(5, 0, 48), (8, 0, 64), (12, 0, 64), (24, 0, 64), (28, 0, 64)]
DRUMS = VOCALS.replace('vocals.wav', 'drums.wav')
RIP_DRUMS_FROM = 24                            # vanaf deze maat zit de drums-stem in de knip
SEAM = 0.015                                   # overlap tussen de stukken: lineaire crossfade (som = origineel)


def bellrip(j, bar, pos, ln, rate=RATE):
    t = BAR1 + (bar - 1) * 2 + pos * 0.125 - 0.03
    t1 = t + ln * 0.125 + SEAM
    xo, sr = _read(OTHER, t, t1, dc=4410)
    xb, _ = _read(BASS, t, t1, dc=4410)
    if bar >= RIP_DRUMS_FROM:
        xb = xb + _read(DRUMS, t, t1, dc=4410)[0]
    x = _to_rate(xo + xb, sr, rate, eq=True)
    n = int(SEAM * rate)
    x[:n] *= np.linspace(0, 1, n)
    x[-n:] *= np.linspace(1, 0, n)
    pk = np.abs(x).max()
    print('az_bells_%d: m%d.%02d, %.2f s, piek %.3f' % (j, bar, pos, len(x) / rate, pk))
    return x / pk * 0.95, pk


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
    ag = []
    for j, (bar, pos, ln) in enumerate(ARIA_PHRASES):
        y, pk = aria(j, bar, pos, ln, src)
        write_wav(os.path.join(OUT, 'az_aria_%d.wav' % j), y, RATE, 60, None)
        ag.append(pk)
    bg = []
    for j, (bar, pos, ln) in enumerate(BELL_RIPS):
        y, pk = bellrip(j, bar, pos, ln)
        write_wav(os.path.join(OUT, 'az_bells_%d.wav' % j), y, RATE, 60, None)
        bg.append(pk)
    # v8: één schaal voor alle knippen (piek / grootste piek van koor, aria en begeleiding): velocity lineair = de
    # verhoudingen van het origineel (Jordi: 'vanaf 8 s wordt alles naar de achtergrond gedrongen')
    top = max(bg + ag + gains)
    for name, g in (('bells', bg), ('aria', ag), ('choir', gains)):
        open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'areazero_%s_gain.txt' % name), 'w').write(
            ' '.join('%.4f' % (x / top) for x in g) + '\n')


if __name__ == '__main__':
    main()
