#!/usr/bin/env python3
"""Project Grounded: Battle! Area Zero (MUS_GROUNDED_VS_AREA_ZERO, 682) = de Area Zero Wild Battle (Scarlet/Violet)
zelf, in aansluitende knippen (vs_areazero_theme.py speelt ze af).

Waarom knippen en niet naspelen (gemeten, okt 10): de battle is doorgecomponeerd. Van de 69 maten van de lus zijn er
54 uniek (chroma per 8e >= 0.85), per stem 'other' 69/69 en vocals 69/69; een bibliotheek van herbruikbare maten (zoals
Area Zero v10) of een getrouwe naspeling past niet in 250 KB. Jordi/coördinator kozen optie A: de hele lus, 11025 Hz,
DPCM (sound/compressed_samples.mk).

Tijd: 149 bpm-raster (maat 1.6108 s, maat 1 op 1.332 s). Lus = 69 maten, periode 111.14094 s (kruiscorrelatie
van de golfvorm, gelijk op 60/90/115/140/170 s). Doorgang 1 wijkt hier en daar af (golfvorm-correlatie met doorgang 2
maar 0.70-0.84), doorgang 2 en 3 zijn gelijk (0.98-0.99). Dus:
  stuk 0      = intro + doorgang 1 tot maat 9 (alleen de eerste keer),
  stukken 1.. = één doorlopend stuk bron vanaf maat 9 van doorgang 2 tot maat 9 van doorgang 3, in stukken van 8 maten.
Elke noot start op een hele frame (m4a op 150 bpm = 1 tick per frame); de bron wordt met factor K = P*fps/L herbemonsterd
(L = hele frames per lus; K - 1 = 2e-5, 0,3 cent), zodat lus, stukgrenzen en naden precies op frames vallen. Naden: de
stukken overlappen 40 ms met een lineaire crossfade (zelfde bron = som is het origineel); de lusnaad (doorgang 3 ->
doorgang 2) is daarmee ook sample-exact op 1-2% verschil tussen de doorgangen na.
Bron: <scratchpad>/az/stems/areazero_wild_battle/*.wav (som van de Spleeter-stems = de mix; niet in de repo).
Gebruik: python3 tools/grounded/vs_areazero_samples.py"""
import json, os, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sample_utils import write_wav

OUT = 'sound/direct_sound_samples/grounded'
STEMS = '/tmp/claude-0/-home-user-projectgrounded/ffd47e46-6a2e-5021-9ef2-b627d7dbd889/scratchpad/az/stems/areazero_wild_battle/'
PLAN = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vs_areazero_plan.json')
RATE = 11025
FPS = 16777216 / 280896                     # GBA-frames per seconde
P = 111.14094                               # lusperiode (s)
BAR0, BAR = 1.332, 4 * 0.40270
PIECE_BARS = 8
OV = 0.010                                  # overlap/crossfade tussen stukken (s)
# Een nieuwe noot begint op sample 0, de lopende knip staat dan op een gebroken sample-positie (de mixer interpoleert):
# in de crossfade gaf dat -10 dB fout (offline nagebouwd). Daarom liggen alle stukgrenzen op frame-afstanden waarbij het
# aantal samples (frames * 11025/59.7275) bijna geheel is (rest < 0,04 sample), en is de lus 6639 frames.
R = RATE / FPS


def _frac(d):
    q = (d * R) % 1
    return min(q, 1 - q)
# weergaveketen (11025 Hz-sample -> mixer 21 kHz -> uitgang) dempt het hoog; omgekeerd als voorversterking (Hz, dB),
# nagemeten in de opname (zie MUZIEK.md)
EQ = [(0, 0.0), (1000, 0.0), (2000, 2.0), (3000, 4.0), (4000, 6.0), (5000, 8.0), (5600, 8.0)]   # v1b: 2-8 kHz was 1,3 dB te weinig
# v2 (Jordi over de 1.0: 'de area zero themes klinken ingame heel muffled en zacht, alsof ze niet in de game horen'):
# gemeten in de game RMS 2005 (mus_vs_wild 3339) en 72% van de energie onder 150 Hz (vs_wild 41%): de sub-bas van het
# origineel draagt het niveau, maar op de GBA-speaker hoor je die nauwelijks. Daarom een lage plank (-LOW_DB onder
# 90 Hz, glijdend tot 180 Hz) en een transparante piekbegrenzer op de hele mix (LIMIT_DB onder de hoogste piek;
# gemeten: >1 dB reductie in 0,4% van de tijd), zodat dezelfde piek meer niveau draagt; plus een derde spoor.
LOW_DB = 3.0
LIMIT_DB = 2.0


def _mix():
    x = None
    for s in ('vocals', 'other', 'bass', 'drums', 'piano'):
        w = wave.open(STEMS + s + '.wav')
        sr = w.getframerate()
        y = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float)
        y = y.reshape(-1, w.getnchannels()).mean(1) / 32768
        x = y if x is None else x + y
    return x, sr


def limit_gain(x, sr, db, look=0.005, rel=0.08, hop=32):
    """v2: piekbegrenzer met vooruitkijken (alleen numpy): versterking per sample zodat |x| <= hoogste piek - db dB;
    de reductie begint `look` s vóór de piek en herstelt in `rel` s."""
    ceil = np.abs(x).max() * 10 ** (-db / 20)
    nb = len(x) // hop + 1
    a = np.zeros(nb * hop); a[:len(x)] = np.abs(x)
    gb = np.minimum(1.0, ceil / np.maximum(a.reshape(nb, hop).max(1), 1e-9))
    n = max(1, int(look * sr / hop))
    pad = np.concatenate([np.ones(n), gb, np.ones(n)])
    gb = np.lib.stride_tricks.sliding_window_view(pad, 2 * n + 1).min(1)
    ar = np.exp(-hop / (rel * sr))
    out = np.empty(nb); v = 1.0
    for i in range(nb):
        v = min(gb[i], ar * v + (1 - ar))
        out[i] = v
    out = np.convolve(np.concatenate([np.full(n, out[0]), out, np.full(n, out[-1])]), np.ones(n) / n, 'same')[n:-n]
    return np.interp(np.arange(len(x)) / hop, np.arange(nb), out)


def _master(x, sr):
    """v2: EQ (weergaveketen + lage plank) op de hele mix, daarna de piekbegrenzer."""
    X = np.fft.rfft(x)
    fr = np.fft.rfftfreq(len(x), 1 / sr)
    X *= 10 ** (np.interp(fr, [p[0] for p in EQ], [p[1] for p in EQ]) / 20)
    X *= 10 ** (-LOW_DB * np.clip((180 - fr) / 90, 0, 1) / 20)
    x = np.fft.irfft(X, len(x))
    return x * limit_gain(x, sr, LIMIT_DB)


def _render(x, sr, t0, t1, k):
    """bron-tijd t0..t1 (s), gelezen met factor k, naar RATE; anti-alias (de EQ zit sinds v2 in _master)."""
    a, b = int(t0 * sr) - 64, int(t1 * sr) + 64
    seg = x[max(0, a):b]
    X = np.fft.rfft(seg)
    fr = np.fft.rfftfreq(len(seg), 1 / sr)
    X[fr > 0.45 * RATE] = 0
    seg = np.fft.irfft(X, len(seg))
    n = int(round((t1 - t0) / k * RATE))
    tt = t0 + np.arange(n) * k / RATE                     # bron-tijd per uitvoersample
    return np.interp(tt * sr - max(0, a), np.arange(len(seg)), seg)


def main():
    x, sr = _mix()
    x = _master(x, sr)
    L = 6639                                              # frames per lus (6638,97 gemeten; rest 0,03 sample)
    K = P * FPS / L                                       # bron-s per lied-s
    t9 = BAR0 + 8 * BAR                                   # maat 9 (doorgang 1)
    A0 = int(round(t9 / K * FPS))                         # lusbegin (frame), naar de dichtstbijzijnde goede afstand
    A = min(range(A0 - 12, A0 + 13), key=lambda a: (_frac(a) > 0.04, abs(a - A0)))
    t9 = A / FPS * K                                      # exact op de frame
    pieces = [(0, A, 0.0)]                                # (startframe, eindframe, bronverschuiving)
    step = int(round(PIECE_BARS * BAR / K * FPS))
    good = [d for d in range(step - 40, step + 41) if _frac(d) < 0.04]
    n = int((L - 2 * BAR / K * FPS) // step)              # aantal stukken van ±8 maten, rest >= 2 maten
    best = None
    import itertools
    for combo in itertools.combinations_with_replacement(good, n):
        rest = L - sum(combo)
        sc = (_frac(rest), sum(abs(d - step) for d in combo))
        if rest > 0 and (best is None or sc < best[0]):
            best = (sc, combo)
    bounds = [A]
    for d in best[1]:
        bounds.append(bounds[-1] + d)
    bounds.append(A + L)
    print('afstanden (frames, rest in samples):', [(b - a, round(_frac(b - a), 3)) for a, b in zip(bounds, bounds[1:])],
          'lusbegin', A, round(_frac(A), 3))
    pieces += [(bounds[i], bounds[i + 1], P) for i in range(len(bounds) - 1)]
    out, total = [], 0
    for j, (f0, f1, sh) in enumerate(pieces):
        t0 = f0 / FPS * K + sh
        t1 = f1 / FPS * K + sh + OV * K
        y = _render(x, sr, t0, t1, K)
        n = int(round(OV * RATE))
        if j > 0:
            y[:n] *= np.linspace(0, 1, n)                  # lineaire crossfade: zelfde bron -> som = origineel
        y[-n:] *= np.linspace(1, 0, n)
        pk = float(np.abs(y).max())
        write_wav(os.path.join(OUT, 'vsaz_%d.wav' % j), y / pk * 0.95, RATE, 60, None)
        out.append({'frame': f0, 'end': f1, 'len': len(y), 'peak': pk})
        total += len(y)
        print('vsaz_%d: frames %d-%d, bron %.3f-%.3f s, %.2f s, piek %.3f' % (j, f0, f1, t0, t1, len(y) / RATE, pk))
    top = max(o['peak'] for o in out)
    for o in out:
        o['gain'] = round(o['peak'] / top, 4)
    json.dump({'loop_start': A, 'loop_end': A + L, 'K': K, 'pieces': out}, open(PLAN, 'w'), indent=1)
    print('lus: frames %d-%d (%d frames = %.4f s, K-1 = %.2e); %d samples = %.0f KB ongecomprimeerd'
          % (A, A + L, L, L / FPS, K - 1, total, total / 1024))


if __name__ == '__main__':
    main()
