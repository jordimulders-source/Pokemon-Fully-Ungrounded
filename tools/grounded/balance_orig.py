#!/usr/bin/env python3
"""Project Grounded: mixbalans van een GBA-arrangement meten tegen een OPNAME van het origineel (mp3/wav), i.p.v.
tegen een FluidR3-render van de bron-MIDI (balance.py). Gemaakt voor Neo Plasma v4.

Het origineel bestaat niet uit losse sporen, dus:
1. per instrumentgroep een GBA-solo-opname (andere sporen op volume 0, zie balance.record) + de volle mix;
2. de volle GBA-mix wordt op het origineel uitgelijnd (kruiscorrelatie van de aanslagcurves);
3. het mel-vermogensspectrogram van het origineel wordt benaderd als niet-negatieve som van de groepen (NNLS):
   origineel ≈ Σ w_g · GBA_g. sqrt(w_g) is dan de factor waarmee groep g luider/zachter moet om het origineel zo goed
   mogelijk na te doen (ook per sectie, met --secties);
4. het spectrum van de totale mix per octaafband (GBA vs. origineel, beide op dezelfde totale energie).
Uitkomst: per groep dB t.o.v. het gemiddelde + voorstel voor het spoorvolume (CC7).

Gebruik (vanuit de hoofdmap, test-ROM met het nummer als debugscript 1 via testrom.py):
  PYTHONPATH=tools/grounded/maptools python3 tools/grounded/balance_orig.py <origineel.wav> <t0> <omgezet.mid> \\
      <test.gba> <intro.bin> <groepen.json> [seconden] [--secties s0,s1,...]
t0 = tijd (s) in het origineel waarop tick 0 van het GBA-nummer valt (ongeveer; de uitlijning zoekt ±1 s).
groepen.json: {"lead": {"out": [1, 2]}, ...} (MIDI-spoornummers, zoals in balance.py)."""
import json, sys
import numpy as np
import librosa, mido
from scipy.optimize import nnls
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from balance import record

SR, HOP = 22050, 512
BANDS = [31, 63, 125, 250, 500, 1000, 2000, 4000, 8000]


def mel(y):
    return librosa.feature.melspectrogram(y=y, sr=SR, n_fft=2048, hop_length=HOP, n_mels=64, fmin=30, fmax=10000)


def align(ref, x, approx):
    """Verschuiving (s) van x t.o.v. ref, rond `approx` (±1 s): ref[t + d] ≈ x[t]. Op chroma (harmonie), niet op
    aanslagen: met een kick op elke tel is een verschuiving van precies één tel anders even goed."""
    ch = lambda y: librosa.feature.chroma_stft(y=y, sr=SR, hop_length=HOP)
    a, b = ch(ref), ch(x)
    a /= np.linalg.norm(a, axis=0) + 1e-9
    b /= np.linalg.norm(b, axis=0) + 1e-9
    fps = SR / HOP
    n = min(b.shape[1], int(60 * fps))
    best = max(range(max(0, int((approx - 1) * fps)), int((approx + 1) * fps)),
               key=lambda d: (a[:, d:d + n] * b[:, :n]).sum() if d + n <= a.shape[1] else -1)
    return best / fps


def octaves(y):
    S = np.abs(librosa.stft(y, n_fft=4096, hop_length=1024)) ** 2
    f = librosa.fft_frequencies(sr=SR, n_fft=4096)
    p = np.array([S[(f >= lo) & (f < hi)].sum() for lo, hi in zip(BANDS, BANDS[1:] + [11000])])
    return 10 * np.log10(p / p.sum())


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    orig, t0, out, rom, state, gfile = args[:6]
    sec = float(args[6]) if len(args) > 6 else 60
    secs = next((a.split('=')[1] for a in sys.argv if a.startswith('--secties=')), None)
    groups = json.load(open(gfile))
    om = mido.MidiFile(out)
    nt = len(om.tracks)
    full = librosa.resample(record(rom, state, [], sec), orig_sr=32768, target_sr=SR)
    ref_all, _ = librosa.load(orig, sr=SR)
    d = align(ref_all, full, float(t0))
    ref = ref_all[int(d * SR):int(d * SR) + len(full)]
    print('uitlijning: GBA-opname begint op %.2f s in het origineel' % d)
    solo = {}
    for k, g in groups.items():
        y = librosa.resample(record(rom, state, [i - 1 for i in range(1, nt) if i not in g['out']], sec),
                             orig_sr=32768, target_sr=SR)
        solo[k] = mel(y[:len(ref)])
    R = mel(ref)
    n = min(R.shape[1], *[m.shape[1] for m in solo.values()])
    keys = list(groups)
    cuts = [0] + [int(float(s) * SR / HOP) for s in secs.split(',')] + [n] if secs else [0, n]
    rows = []
    loud = max(solo[k].sum() for k in keys)
    for a, b in zip(cuts, cuts[1:]):
        # groepen die in deze sectie (bijna) niet spelen, doen niet mee (hun gewicht zegt niets)
        on = [i for i, k in enumerate(keys) if solo[k][:, a:b].sum() > 1e-3 * loud * (b - a) / n]
        A = np.stack([solo[keys[i]][:, a:b].ravel() for i in on], 1)
        w, _ = nnls(A, R[:, a:b].ravel())
        row = np.full(len(keys), np.nan)
        row[on] = 10 * np.log10(np.maximum(w, 1e-9))
        rows.append(row)
    rows = np.array(rows)
    mean = np.nanmedian(rows[rows > -80])
    print('NNLS-gewicht per groep (dB t.o.v. de mediaan; + = in de GBA-versie te zacht)')
    hdr = '%-10s' % 'groep' + ''.join('%9s' % ('%.0f-%.0fs' % (cuts[i] * HOP / SR, cuts[i + 1] * HOP / SR))
                                       for i in range(len(cuts) - 1))
    print(hdr + '   voorstel CC7 (hele stuk)')
    for j, k in enumerate(keys):
        col = rows[:, j][~np.isnan(rows[:, j])]
        corr = (np.median(col) - mean) / 2 if len(col) else 0.0
        vols = []
        for i in groups[k]['out']:
            v = next((x.value for x in om.tracks[i] if x.type == 'control_change' and x.control == 7), 127)
            vols.append('%d:%d->%d' % (i, v, max(1, min(127, round(v * 10 ** (corr / 20))))))
        print('%-10s' % k + ''.join('%9s' % ('-' if np.isnan(r[j]) else '%+.1f' % (r[j] - mean)) for r in rows)
              + '   ' + ', '.join(vols))
    go, ro = octaves(full[:len(ref)]), octaves(ref)
    print('\noctaafband (Hz)  ' + ''.join('%7d' % b for b in BANDS))
    print('origineel  dB    ' + ''.join('%7.1f' % x for x in ro))
    print('GBA        dB    ' + ''.join('%7.1f' % x for x in go))
    print('GBA - orig       ' + ''.join('%+7.1f' % x for x in go - ro))
    print('per sectie (GBA - orig per band, dB; zelfde totale energie):')
    for a, b in zip(cuts, cuts[1:]):
        sa, sb = a * HOP, b * HOP
        d = octaves(full[sa:sb]) - octaves(ref[sa:sb])
        print('  %5.0f-%-5.0fs    ' % (sa / SR, sb / SR) + ''.join('%+7.1f' % x for x in d))


if __name__ == '__main__':
    main()
