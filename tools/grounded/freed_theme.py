#!/usr/bin/env python3
"""Project Grounded: gevechtsmuziek van Dave (TRAINER_ALBERT, Cooltrainer, Victory Road + Battle Stadium):
"Freed From Desire" (Gala, 1996) als eurodance-gevechtsthema.

Bron: sound/songs/grounded_src/freed_from_desire.mid (D-klein, 120 bpm; sporen 4 piano, 5 bas, 6 orgel-riff,
7 zangmelodie, 8 synth strings, 11 saw-bas, 13 drums). De melodie komt níet uit de MIDI maar uit Jordi's
trompet-bladmuziek (Bb-trompet, genoteerd in E-klein = klinkend D-klein, een grote secunde lager): daar zijn
de herhalingen gelijk en klopt het ritme (zie MUZIEK.md, "twee bronnen"). Begeleiding/drums komen uit de MIDI.

Opbouw (132 bpm, 1 maat = 1,82 s):
  intro  4 maten (7,3 s): "na na na"-hook op trompet + vierkant, orgelstoten, opbouw met kick en snareroffel
  loop  28 maten (50,9 s):
     A 4  orgel-riff + bas + beat (instrumentaal)
     B 8  couplet ("my love has got no money")
     C 8  refrein ("freed from desire"), laatste maat een break (alleen de opmaat)
     D 8  "na na na"-hook, vol
Lead = trompet (DirectSound) + PSG-vierkant in unisono (eurodance-glans, buiten de 8-bit-mixer).
Stemverdeler: max. 10 DirectSound-noten tegelijk (hook > bas > drums > orgel > piano > strijkers).
Schrijft ook voicegroup_grounded_dave (= grounded_gm met een zacht vierkant op 80 en een plukvierkant op 81).
Gebruik: python3 tools/grounded/freed_theme.py"""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import notes_of, dedupe, thin, allocate, releases, release_ticks, Song

SRC = 'sound/songs/grounded_src/freed_from_desire.mid'
OUT = 'sound/songs/midi/mus_grounded_vs_dave.mid'
VG = 'sound/voicegroups/grounded_dave.inc'
TPB, BAR, BEAT = 240, 960, 240
BPM = 132
TRUMPET, ORGAN, PIANO, SYNTH_BASS, STRINGS, SQ_LEAD, SQ_PLUCK = 56, 17, 2, 38, 50, 80, 81

# --- melodie uit de bladmuziek (klinkend), per maat: (tel, lengte in tellen, noot) ---
D5, E5, F5, C5, Bb4 = 74, 76, 77, 72, 70
EEEEE = [(1.5, .5, E5), (2, .5, E5), (2.5, .5, E5), (3, .5, E5), (3.5, .5, E5)]       # opmaat "my love has got no"
# couplet (blad maat 8-15)
V1 = EEEEE[:4] + [(3.5, .25, E5), (3.75, .75, F5)]                                     # F overgebonden
V2 = [(0.5, .5, D5), (1.5, .5, D5), (2, .5, C5), (2.5, .5, C5), (3, .5, C5), (3.5, .25, C5), (3.75, .75, Bb4)]
V3 = EEEEE
V4 = [(0, .5, F5)] + V2
V8 = V2[:-1] + [(3.75, .25, Bb4)]                                                      # niet overbinden: refrein volgt
VERSE = [V1, V2, V3, V4, V3, V4, V1, V8]
# refrein (blad maat 25-32): "freed from desire / mind and senses purified" (blad: tweede maat helemaal E)
R1 = [(0, .75, F5), (0.75, .75, D5), (1.5, .5, D5), (2, .75, C5), (2.75, .25, C5)]
R2 = [(0, .5, E5), (0.5, .5, E5), (1, .5, E5), (1.5, .5, E5), (2, .5, E5), (2.5, .25, E5), (2.75, .75, E5), (3.5, .5, E5)]
CHORUS = [R1, R2, R1, R2, R1, R2, R1, EEEEE]
# "na na na" (blad maat 33-40)
N1 = [(0, .75, F5), (0.75, .75, D5), (1.5, .5, D5), (2, .75, C5), (2.75, .75, C5), (3.5, .5, C5)]
N2 = [(0, .75, Bb4), (0.75, .25, Bb4)] + EEEEE
N4 = [(0, .5, Bb4)] + EEEEE
N8 = [(0, .5, Bb4)]
NANA = [N1, N2, N1, N4, N1, N2, N1, N8]
INTRO_LEAD = [N1, N2, N1, N8]

# --- drums: rs_drumset; echte lengtes (de bron heeft overal 2 ticks); 28/44/70/51 vallen weg (buiten de kit/PSG/te vol) ---
DRUM_MAP = {36: (36, 120), 38: (38, 120), 39: (39, 120), 46: (46, 120), 54: (54, 60), 49: (57, 480)}


def src_tracks():
    m = mido.MidiFile(SRC)
    assert m.ticks_per_beat == TPB
    return {i: notes_of(m.tracks[i]) for i in range(4, 14)}


def take(ev, src_bar, nbars, dst_bar):
    """Noten uit maten [src_bar, src_bar+nbars) naar dst_bar verschuiven; lange noten aan het eind afkappen."""
    s0, s1, d = src_bar * BAR, (src_bar + nbars) * BAR, (dst_bar - src_bar) * BAR
    return [[s + d, min(e, s1) + d, n, v] for s, e, n, v in ev if s0 <= s < s1]


def melody(bars, dst_bar):
    out = []
    for i, bar in enumerate(bars):
        for beat, dur, n in bar:
            s = (dst_bar + i) * BAR + int(beat * BEAT)
            out.append([s, s + int(dur * BEAT), n, 112 if beat in (0, 2) else 100])
    return out


def drums(ev):
    out = []
    for s, e, n, v in ev:
        if n not in DRUM_MAP:
            continue
        n2, ln = DRUM_MAP[n]
        if n == 54 and s % 240 not in (80, 200):
            continue                                    # tamboerijn alleen op de shuffle (1/3 en 5/6 tel)
        if n == 39:
            s = round(s / 60) * 60                      # clap op 0,99 tel -> precies op 2 en 4
        if n == 38 and any(o[2] == 38 and 0 < s - o[0] < 120 for o in out):
            ln = 60                                     # snareroffel: 16e
        out.append([s, s + ln, n2, v])
    return dedupe(out)


def voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Dave (Freed From Desire). Gegenereerd door tools/grounded/freed_theme.py.'
    lines[1] = '@ 2 = piano met korte release (stoten), 80 = zacht vierkant (50%) voor de hook, 81 = plukkend vierkant (25%) voor de saw-bas.'
    lines[2] = 'voice_group grounded_dave'
    rep = {2: '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_piano1_60, 255, 250, 0, 200  @ 2',
           80: '\tvoice_square_1 60, 0, 0, 2, 0, 2, 9, 1  @ 80',
           81: '\tvoice_square_2 60, 0, 1, 0, 2, 3, 1  @ 81'}
    out = []
    for l in lines:
        k = l.rsplit('@', 1)[1].strip() if '@' in l and l.startswith('\tvoice') else None
        out.append(rep.get(int(k), l) if k and k.isdigit() else l)
    open(VG, 'w').write('\n'.join(out))


def build():
    T = src_tracks()
    parts = {k: [] for k in ('lead', 'bass', 'drums', 'organ', 'piano', 'strings', 'sq_lead', 'sq_pluck')}
    organ = thin(T[6], 2, 'bottom')                      # D4 + D5 (D6 klinkt schel)
    # intro (maat 0-3)
    parts['lead'] += melody(INTRO_LEAD, 0)
    for b in range(4):
        parts['organ'] += take(organ, 38, 1, b)
    intro_dr = drums(take(T[13], 38, 2, 0) + take(T[13], 38, 2, 2))
    parts['drums'] += [e for e in intro_dr if e[2] in (54, 46) or (e[2] == 36 and e[0] >= 2 * BAR)]
    parts['drums'] += [[3 * BAR + i * 60, 3 * BAR + i * 60 + 60, 38, 40 + i * 4] for i in range(16)]   # roffel naar de loop
    # A: riff (maat 4-7) = bron 38-41
    parts['organ'] += take(organ, 38, 4, 4)
    parts['bass'] += take(T[5], 38, 4, 4)
    parts['drums'] += drums(take(T[13], 38, 4, 4))
    # B: couplet (maat 8-15) = bron 53-60; bas = bron 55-56 (53/54 missen een noot)
    parts['lead'] += melody(VERSE, 8)
    for b in range(8, 16, 2):
        parts['bass'] += take(T[5], 55, 2, b)
    parts['organ'] += take(organ, 53, 8, 8)
    parts['sq_pluck'] += take(T[11], 53, 8, 8)
    parts['drums'] += drums(take(T[13], 53, 8, 8))
    # C: refrein (maat 16-23) = bron 70-77
    parts['lead'] += melody(CHORUS, 16)
    parts['bass'] += take(T[5], 70, 8, 16)
    strings = thin([[round(s / BEAT) * BEAT, round(e / BEAT) * BEAT, n, v] for s, e, n, v in T[8]], 1, 'top')
    parts['piano'] += take(thin(T[4], 2, 'top'), 70, 8, 16)
    parts['strings'] += take(strings, 70, 8, 16)
    parts['drums'] += drums(take(T[13], 70, 8, 16))
    # D: na na na (maat 24-31) = bron 78-85
    parts['lead'] += melody(NANA, 24)
    parts['bass'] += take(T[5], 78, 8, 24)
    parts['piano'] += take(thin(T[4], 2, 'top'), 78, 8, 24)
    parts['strings'] += take(strings, 78, 8, 24)
    parts['drums'] += drums(take(T[13], 78, 8, 24))
    parts['sq_lead'] = [list(e) for e in parts['lead']]
    # pianostoten kort houden: einde + uitklinktijd vóór de volgende stoot (anders 4 pianonoten tegelijk)
    parts['piano'] = [[s, min(e, s + 80), n, v] for s, e, n, v in parts["piano"]]
    # strijkers in stukken van 2 tellen (pulserende pad): dan valt bij een volle tel alleen dat stuk weg
    # (bron-timing op de tel afronden; elk stuk stopt een uitklinktijd eerder, zodat stukken elkaar niet overlappen)
    parts['strings'] = [[t, min(e, t + 2 * BEAT - 96), n, v] for s, e, n, v in parts['strings'] for t in range(s, e - 60, 2 * BEAT)]
    for k in parts:
        parts[k] = dedupe(parts[k])
    # stemverdeler
    voicegroup()
    rel = releases('grounded_dave')
    progs = {'lead': TRUMPET, 'bass': SYNTH_BASS, 'organ': ORGAN, 'piano': PIANO, 'strings': STRINGS}
    tail = {k: release_ticks(rel.get(p, 200), TPB, BPM) for k, p in progs.items()}
    order = ['lead', 'bass', 'drums', 'organ', 'piano', 'strings']
    res = allocate({k: parts[k] for k in order}, order, tail)
    for k in order:
        n, kept = len(parts[k]), len(res[k])
        print('  %-8s %4d noten, %3d vallen weg (%.1f%%)' % (k, n, n - kept, 100 * (n - kept) / max(n, 1)))
        parts[k] = res[k]
    end = 32 * BAR
    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.loop = (4 * BAR, end)
    song.add(parts['lead'], TRUMPET, 112, 0)
    song.add(parts['sq_lead'], SQ_LEAD, 52, 1)
    song.add(parts['bass'], SYNTH_BASS, 118, 2)
    song.add(parts['organ'], ORGAN, 78, 3, pan=54)
    song.add(parts['piano'], PIANO, 74, 4, pan=74)
    song.add(parts['strings'], STRINGS, 58, 5)
    song.add(parts['sq_pluck'], SQ_PLUCK, 40, 6)
    song.add(parts['drums'], 127, 104, 9)
    song.save(OUT, end)
    print(OUT)


if __name__ == '__main__':
    build()
