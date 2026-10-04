#!/usr/bin/env python3
"""Project Grounded: Battle! Regigigas, een bombastische remix van het Regi-thema (mus_vs_regi) met Slow Start (Jordi).

- Intro (maat 0-19 van het Regi-thema): begint op 55% tempo en versnelt per maat tot 100% (maat 8). Regigigas wordt
  laag voor laag wakker: eerst orgel + bas, dan pauken en toms, dan de robot-arpeggio's (PSG, zoals in het
  origineel), vanaf maat 8 het hele orkest (trompet, hoorn, koor, tuba, taiko, crash).
- Loop (maat 20-39): het koraal op koper + koor boven de bas-ostinato. In maat 30-33 zakt hij nog één keer in
  (tempo omlaag, drums weg, zachter: "bijkomen") en komt met een paukenroffel terug op vol gas (maat 34).
Gebruikt tools/grounded/musiclib.py (stemverdeler, ontdubbelen) en voicegroup_grounded_gm. Zie tools/grounded/MUZIEK.md.
Gebruik: python3 tools/grounded/regigigas_theme.py"""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import notes_of, dedupe, thin, detach, allocate, releases, release_ticks, Song

SRC = 'sound/songs/midi/mus_vs_regi.mid'
OUT = 'sound/songs/midi/mus_grounded_vs_regigigas.mid'
VG = 'grounded_gm'
TPB_OUT = 96
BAR = TPB_OUT * 4
TRUMPET, HORN, TUBA, CHOIR, ORGAN, TIMPANI, TAIKO, BASS, SQ1, SQ2 = 56, 60, 58, 52, 19, 47, 116, 33, 80, 81
DRUMS = 127

# tempo per maat (factor van het origineel, 160 bpm)
SLOW_START = [0.55, 0.60, 0.66, 0.72, 0.79, 0.86, 0.93, 1.0]
DIP = {30: [0.9], 31: [0.76], 32: [0.62], 33: [0.68, 0.78, 0.89, 1.0]}   # maat -> factor per tel (1 = hele maat)
DIP_BARS = (31, 32)        # hier vallen drums, taiko en arpeggio's weg
INTRO_END, LOOP_START, LOOP_END = 20, 20, 40
DRUM_MAP = {38: 38, 47: 43, 48: 45, 57: 57}   # rs_drumset: snare, toms, crash


def scaled(track, f):
    ev = notes_of(track)
    return [[s * f, e * f, n, v] for s, e, n, v in ev]


def bar_of(t):
    return t // BAR


def build():
    src = mido.MidiFile(SRC)
    f = TPB_OUT // src.ticks_per_beat
    T = {i: scaled(src.tracks[i], f) for i in range(1, 9)}
    end = LOOP_END * BAR
    parts = {}

    # koraal / melodie
    parts['trumpet'] = [e for e in thin(T[1], 1, 'top') if bar_of(e[0]) >= 8]
    parts['organ'] = [e for e in thin(T[1], 2, 'top') if bar_of(e[0]) < 8]          # intro: chromatisch motief op orgel
    parts['horn'] = [e for e in thin(T[2], 1, 'top') if bar_of(e[0]) >= 8]
    parts['choir'] = [list(e) for e in thin(T[2], 1, 'top') if bar_of(e[0]) >= LOOP_START]
    parts['stabs'] = [[s, s + 24, n, 110] for s, e, n, v in T[6]]                  # G#-steken van de intro op trompet
    # bas: ostinato + een lange tuba-grondtoon per maat
    parts['bass'] = [[s, e, n + 12 if n < 31 else n, v] for s, e, n, v in thin(T[3], 1, 'bottom')]   # niet onder G1
    roots = {}
    for s, e, n, v in parts['bass']:
        roots.setdefault(bar_of(s), n)
    parts['tuba'] = [[b * BAR, (b + 1) * BAR - 12, roots[b] + 12, 100] for b in sorted(roots) if b >= 8]
    # slagwerk
    parts['timpani'] = [[s, min(e, s + 48), 48, v] for s, e, n, v in T[8]]
    drums = [[s, min(e, s + 96), DRUM_MAP.get(n, 38), v] for s, e, n, v in T[7] if bar_of(s) >= 2]
    drums += [[b * BAR, b * BAR + 192, 57, 120] for b in (8, 20, 34)]                # crashes op de grote inzetten
    parts['drums'] = dedupe(drums)
    parts['taiko'] = [[b * BAR + o, b * BAR + o + 96, 48, 115] for b in range(8, LOOP_END) for o in (0, 192)]
    # robot-arpeggio's (PSG, tellen niet mee voor de 10 kanalen)
    parts['arp1'] = [e for e in T[4] if bar_of(e[0]) >= 4]
    parts['arp2'] = [e for e in T[5] if bar_of(e[0]) >= 8]

    # bijkomen: drums/taiko/arpeggio's weg, alles zachter; maat 33 een paukenroffel die aanzwelt
    for k in ('drums', 'taiko', 'arp1', 'arp2', 'stabs'):
        parts[k] = [e for e in parts[k] if bar_of(e[0]) not in DIP_BARS + (33,) or k == 'stabs']
    for k in parts:
        for e in parts[k]:
            if bar_of(e[0]) in (30, 31, 32):
                e[3] = int(e[3] * (0.85 if bar_of(e[0]) == 30 else 0.65))
    parts['timpani'] = [e for e in parts['timpani'] if bar_of(e[0]) != 33]
    parts['timpani'] += [[33 * BAR + i * 24, 33 * BAR + i * 24 + 24, 48, 50 + i * 4] for i in range(16)]
    parts['drums'] += [[33 * BAR + i * 24, 33 * BAR + i * 24 + 24, 38, 40 + i * 4] for i in range(8, 16)]

    # Slow Start: de intro laag voor laag
    for k, first in (('bass', 0), ('organ', 0), ('timpani', 2), ('drums', 2), ('stabs', 4)):
        parts[k] = [e for e in parts[k] if bar_of(e[0]) >= first]

    # stemmen verdelen (DirectSound; PSG-arpeggio's tellen niet mee)
    rel = releases(VG)
    progs = {'trumpet': TRUMPET, 'organ': ORGAN, 'horn': HORN, 'choir': CHOIR, 'stabs': TRUMPET, 'bass': BASS,
             'tuba': TUBA, 'timpani': TIMPANI, 'taiko': TAIKO}
    ds = {k: v for k, v in parts.items() if k not in ('arp1', 'arp2')}
    order = ['trumpet', 'organ', 'bass', 'drums', 'horn', 'choir', 'tuba', 'timpani', 'stabs', 'taiko']
    tail = {k: release_ticks(rel.get(p, 200), TPB_OUT, 160) for k, p in progs.items()}
    for k in ('trumpet', 'horn', 'choir', 'tuba', 'bass', 'organ'):
        ds[k] = detach(ds[k], tail[k])
    kept = allocate(ds, order, tail=tail, drum_len=None, drum_parts=('drums',), max_voices=10)
    for k in order:
        if len(kept[k]) < len(ds[k]) * 0.97:
            print('  %s: %d van %d noten vallen weg (te vol)' % (k, len(ds[k]) - len(kept[k]), len(ds[k])))
    parts.update(kept)

    song = Song(TPB_OUT, 375000)
    for b, fac in enumerate(SLOW_START):
        song.tempo(b * BAR, fac)
    song.tempo(LOOP_START * BAR, 1.0)
    for b, facs in DIP.items():
        for i, fac in enumerate(facs):
            song.tempo(b * BAR + i * (BAR // len(facs)), fac)
    song.tempo(34 * BAR, 1.0)
    song.loop = (LOOP_START * BAR, end)
    layout = [('trumpet', TRUMPET, 110, 0, 64), ('organ', ORGAN, 96, 1, 64), ('horn', HORN, 100, 2, 52),
              ('choir', CHOIR, 84, 3, 76), ('stabs', TRUMPET, 96, 4, 70), ('bass', BASS, 104, 5, 64),
              ('tuba', TUBA, 92, 6, 60), ('timpani', TIMPANI, 104, 7, 64), ('taiko', TAIKO, 92, 8, 64),
              ('drums', DRUMS, 104, 9, 64), ('arp1', SQ1, 44, 10, 44), ('arp2', SQ2, 36, 11, 84)]
    for k, prog, vol, ch, pan in layout:
        song.add([e for e in parts[k] if e[0] < end], prog, vol, ch, pan)
    song.save(OUT, end)
    print(OUT)


if __name__ == '__main__':
    build()
