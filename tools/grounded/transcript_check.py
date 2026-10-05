#!/usr/bin/env python3
"""Project Grounded: een MIDI-transcriptie controleren tegen een opname van het origineel (gemaakt voor Neo Plasma v5).

1. timing per spoor: de noten van een spoor ±48 ticks verschuiven en kijken waar de toonhoogte-specifieke aanslagen
   (spectrale flux op de harmonischen 1-4 van elke noot) in de opname het sterkst zijn. Een spoor dat anders uitkomt
   dan de rest staat verschoven in de bron (Neo Plasma: sawtooth 17 ticks te vroeg).
2. noten: harmonische salience (som van 5 harmonischen, STFT 4096, per toonhoogte gewit) op de eigen toonhoogte vs.
   de buren (±1, ±2 halve toon). Verdacht = een buur > eigen + marge die door geen andere bronnoot verklaard wordt.

Gebruik: python3 tools/grounded/transcript_check.py <bron.mid> <opname.wav> <t0> <bpm> [spoor ...]
  t0 = tijd (s) van tick 0 in de opname, bpm = gemeten tempo van de opname (niet dat van de MIDI).
Uitvoer: beste verschuiving per spoor + lijst verdachte noten (maat.16e, noot, eigen/buur in dB)."""
import sys
import numpy as np, librosa, mido
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from musiclib import notes_of

NN = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
SR = 22050


def main():
    src, wav, t0, bpm = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
    m = mido.MidiFile(src)
    tpb = m.ticks_per_beat
    trs = [int(x) for x in sys.argv[5:]] or [i for i, t in enumerate(m.tracks)
                                             if notes_of(t) and all(x.channel != 9 for x in t if x.type == 'note_on')]
    T = {i: notes_of(m.tracks[i]) for i in range(len(m.tracks))}
    t_of = lambda tk: t0 + tk / tpb * 60 / bpm
    bar = 4 * tpb
    y, _ = librosa.load(wav, sr=SR)
    # 1. timing
    S = np.log1p(100 * np.abs(librosa.stft(y, n_fft=2048, hop_length=64)))
    flux = np.maximum(0, np.diff(S, axis=1, prepend=S[:, :1]))
    fps = SR / 64
    print('timing (beste verschuiving in ticks; vergelijk de sporen onderling):')
    for i in trs:
        rows = []
        for s, e, n, v in T[i]:
            f0 = librosa.midi_to_hz(n)
            rows.append((s, sorted({int(round(h * f0 / (SR / 2048))) + d for h in (1, 2, 3, 4) for d in (-1, 0, 1)
                                    if h * f0 < 8000})))
        res = []
        for sh in range(-tpb // 8, tpb // 8 + 1, 2):
            tot = 0
            for s, bins in rows:
                k = int(round(t_of(s + sh) * fps))
                if 3 < k < flux.shape[1] - 4:
                    tot += flux[bins, k - 3:k + 4].sum(0).max() / len(bins)
            res.append((tot, sh))
        print('  spoor %2d %-22s %+4d' % (i, m.tracks[i].name[:22], max(res)[1]))
    # 2. noten
    M = np.abs(librosa.stft(y, n_fft=4096, hop_length=256))
    df, fps = SR / 4096, SR / 256
    Z = np.zeros((84, M.shape[1]))
    for n in range(24, 108):
        for h, w in ((1, 1.0), (2, .6), (3, .4), (4, .3), (5, .2)):
            fh = h * librosa.midi_to_hz(n)
            if fh < 9000:
                Z[n - 24] += w * M[int(fh * .985 / df):int(np.ceil(fh * 1.015 / df)) + 1].max(0)
    Z = 20 * np.log10(Z + 1e-6)
    Z -= np.median(Z, axis=1, keepdims=True)
    allnotes = [(s, e, n, i) for i in trs for s, e, n, v in T[i]]
    for i in trs:
        flags = []
        for s, e, n, v in T[i]:
            a = int((t_of(s) + .02) * fps)
            b = max(a + 1, int(min(t_of(e), t_of(s) + .25) * fps))
            mean = lambda k: Z[k - 24, a:b].mean() if 24 <= k < 108 and b <= Z.shape[1] else -99
            expl = {k + d for s2, e2, k, j in allnotes if s2 < e and e2 > s and (j != i or k != n)
                    for d in (0, 12, -12, 19, 24)}
            own = mean(n)
            bv, bn = max((mean(n + d), n + d) for d in (-2, -1, 1, 2))
            if bv > own + 5 and bn not in expl:
                flags.append('%d.%g %s%d (%+.0f dB: %s%d)' % (s // bar, s % bar / (tpb / 4), NN[n % 12], n // 12 - 1,
                                                              bv - own, NN[bn % 12], bn // 12 - 1))
        print('spoor %d: %d noten, %d verdacht' % (i, len(T[i]), len(flags)))
        for f in flags:
            print('   ', f)


if __name__ == '__main__':
    main()
