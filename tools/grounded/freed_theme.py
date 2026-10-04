#!/usr/bin/env python3
"""Project Grounded: gevechtsmuziek van Dave (TRAINER_ALBERT, Cooltrainer, Victory Road + Battle Stadium):
"Freed From Desire" (Gala, 1996).

Volgt de bron-MIDI 1-op-1 (sound/songs/grounded_src/freed_from_desire.mid, D-klein): één aaneengesloten stuk in de
originele volgorde, niets herschikt (Jordi, ronde 2: "geen remix"). Alleen instrumenten gemapt naar de GBA, drums
omgezet, akkoorden uitgedund en een stemverdeler.
  bronmaat 49-52  intro: de orgel-riff met bas en beat (7,5 s)
  bronmaat 53-85  loop: couplet 2 -> "want more and more" -> refrein -> "na na na" (33 maten, 61,9 s)
De loop springt van bronmaat 85 (C-akkoord, einde "na na na") terug naar 53 (D-klein, riff), net als 37 -> 38 in het
nummer. Enige ingreep: de opmaat-E's in maat 85 (die in het nummer naar de a-capella-herhaling leiden) vallen weg,
zoals maat 37 eindigt.
Melodie = spoor 7 (de zang), gedubbeld in unisono: trompet (DirectSound) + PSG-vierkant. Eén melodie tegelijk.
Saw-bas (spoor 11) = plukkend PSG-vierkant. Stemverdeler: max. 10 DirectSound-noten tegelijk
(melodie > bas > drums > orgel > piano > strijkers > pad). Schrijft ook voicegroup_grounded_dave.
Gebruik: python3 tools/grounded/freed_theme.py"""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import notes_of, dedupe, thin, allocate, releases, release_ticks, Song

SRC = 'sound/songs/grounded_src/freed_from_desire.mid'
OUT = 'sound/songs/midi/mus_grounded_vs_dave.mid'
VG = 'sound/voicegroups/grounded_dave.inc'
TPB, BAR, BEAT = 240, 960, 240
BPM = 128
FIRST, LOOP, END = 49, 53, 86            # bronmaten: intro 49-52, loop 53-85
TRUMPET, ORGAN, PIANO, SYNTH_BASS, STRINGS, SQ_LEAD, SQ_PLUCK = 56, 17, 2, 38, 50, 80, 81
# drums (rs_drumset): echte lengtes, de bron heeft overal 2 ticks. 28/70 vallen buiten de kit, 44/51 zijn PSG
# (44 = gesloten hihat onder de kick: weg, anders te vol), 49 -> crash 57. Tamboerijn alleen op de shuffle.
DRUM_MAP = {36: (36, 120), 38: (38, 120), 39: (39, 120), 46: (46, 120), 54: (54, 60), 49: (57, 480)}


def drums(ev):
    out = []
    for s, e, n, v in ev:
        if n not in DRUM_MAP or (n == 54 and s % BEAT not in (80, 200)):
            continue
        n2, ln = DRUM_MAP[n]
        if n == 39:
            s = round(s / 60) * 60                      # clap op 0,99 tel -> precies op de tel
        if n == 38 and any(o[2] == 38 and 0 < s - o[0] < 120 for o in out):
            ln = 60                                     # snareroffel: 16e
        out.append([s, s + ln, n2, v])
    return dedupe(out)


def voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Dave (Freed From Desire). Gegenereerd door tools/grounded/freed_theme.py.'
    lines[1] = '@ 2 = piano met korte release (stoten), 80 = zacht vierkant (50%) voor de melodie, 81 = plukkend vierkant (25%) voor de saw-bas.'
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
    m = mido.MidiFile(SRC)
    assert m.ticks_per_beat == TPB
    T = {i: notes_of(m.tracks[i]) for i in range(4, 14)}
    s0, s1 = FIRST * BAR, END * BAR

    def cut(ev):
        """Bronmaten FIRST..END-1, naar tick 0 geschoven; noten die over het einde lopen afkappen."""
        return [[s - s0, min(e, s1) - s0, n, v] for s, e, n, v in ev if s0 <= s < s1]

    lead = cut(T[7])
    lead = [e for e in lead if not (e[0] >= (85 - FIRST) * BAR and e[2] == 76)]   # opmaat-E's in maat 85 (zie boven)
    lead.sort()
    for a, nxt in zip(lead, lead[1:]):                    # één stem: legato-overlap van 1-2 ticks weghalen
        a[1] = min(a[1], nxt[0])
    parts = {
        'lead': lead,
        'bass': cut(T[5]),
        'drums': drums(cut(T[13])),
        'organ': cut(thin(T[6], 2, 'bottom')),            # D4 + D5 (D6 klinkt schel)
        'piano': cut(thin(T[4], 2, 'top')),
        'strings': cut(thin([[round(s / BEAT) * BEAT, round(e / BEAT) * BEAT, n, v] for s, e, n, v in T[8] + T[9]], 1, 'top')),
        'pad': cut(thin([[round(s / BEAT) * BEAT, round(e / BEAT) * BEAT, n, v] for s, e, n, v in T[10]], 1, 'top')),
        'sq_pluck': cut(T[11]),
    }
    # pianostoten kort: einde + uitklinktijd vóór de volgende stoot (anders 4 pianonoten tegelijk)
    parts['piano'] = [[s, min(e, s + 80), n, v] for s, e, n, v in parts['piano']]
    # lange pads in stukken van 2 tellen die een uitklinktijd eerder stoppen: bij een volle tel valt alleen dat stuk weg
    for k in ('strings', 'pad'):
        parts[k] = [[t, min(e, t + 2 * BEAT - 96), n, v] for s, e, n, v in parts[k] for t in range(s, e - 60, 2 * BEAT)]
    for k in parts:
        parts[k] = dedupe(parts[k])
    parts['sq_lead'] = [list(e) for e in parts['lead']]
    voicegroup()
    rel = releases('grounded_dave')
    progs = {'lead': TRUMPET, 'bass': SYNTH_BASS, 'organ': ORGAN, 'piano': PIANO, 'strings': STRINGS, 'pad': STRINGS}
    tail = {k: release_ticks(rel.get(p, 200), TPB, BPM) for k, p in progs.items()}
    order = ['lead', 'bass', 'drums', 'organ', 'piano', 'strings', 'pad']
    res = allocate({k: parts[k] for k in order}, order, tail)
    for k in order:
        n, kept = len(parts[k]), len(res[k])
        print('  %-8s %4d noten, %3d vallen weg (%.1f%%)' % (k, n, n - kept, 100 * (n - kept) / max(n, 1)))
        parts[k] = res[k]
    end = s1 - s0
    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.loop = ((LOOP - FIRST) * BAR, end)
    song.add(parts['lead'], TRUMPET, 112, 0)
    song.add(parts['sq_lead'], SQ_LEAD, 52, 1)
    song.add(parts['bass'], SYNTH_BASS, 118, 2)
    song.add(parts['organ'], ORGAN, 78, 3, pan=54)
    song.add(parts['piano'], PIANO, 74, 4, pan=74)
    song.add(parts['strings'], STRINGS, 58, 5)
    song.add(parts['pad'], STRINGS, 48, 6, pan=80)
    song.add(parts['sq_pluck'], SQ_PLUCK, 40, 7)
    song.add(parts['drums'], 127, 104, 9)
    song.save(OUT, end)
    print(OUT, '(intro %.1f s, loop %.1f s)' % ((LOOP - FIRST) * 4 * 60 / BPM, (END - LOOP) * 4 * 60 / BPM))


if __name__ == '__main__':
    build()
