#!/usr/bin/env python3
"""Project Grounded: Battle! Area Zero (MUS_GROUNDED_VS_AREA_ZERO, 682) = de Area Zero Wild Battle uit het origineel.

De knippen en de frameplanning komen uit vs_areazero_samples.py (vs_areazero_plan.json). Dit script schrijft:
  - sound/voicegroups/drumsets/area_zero_vs.inc  (kit: noot 36+j = stuk j, op de eigen toonhoogte)
  - sound/voicegroups/grounded_vs_area_zero.inc  (voicegroup _grounded_vs_area_zero: programma 0 = die kit)
  - de labels in sound/direct_sound_data.inc en de includes in sound/voice_groups.inc (idempotent)
  - sound/songs/midi/mus_grounded_vs_area_zero.mid
150 bpm met 24 ticks per tel = 1 m4a-tick per frame, dus elke noot start op precies de frame uit het plan. Lus: van
het begin van stuk 1 (maat 9) tot het eind van het laatste stuk (maat 9 van de volgende doorgang).
v1 (okt 10): eerste versie op het origineel (optie A: alles geknipt, 11025 Hz, DPCM)."""
import json, os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import Song

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = 'sound/songs/midi/mus_grounded_vs_area_zero.mid'
VG = '_grounded_vs_area_zero'
REL = 255                                    # geen uitsterving: de knip eindigt zelf (crossfade in de sample)
VOL = 127                                    # spoorvolume (twee sporen, zie onder)


def main():
    plan = json.load(open(os.path.join(HERE, 'vs_areazero_plan.json')))
    pieces = plan['pieces']
    open('sound/voicegroups/drumsets/area_zero_vs.inc', 'w').write(
        '@ Project Grounded: Battle! Area Zero, het origineel in aansluitende knippen (vs_areazero_samples.py);\n'
        '@ noot 36+j = stuk j, eigen toonhoogte. Gegenereerd door tools/grounded/vs_areazero_theme.py.\n'
        'voice_group area_zero_vs, 36\n' + ''.join(
            '\tvoice_directsound 60, 0, DirectSoundWaveData_vsaz_%d, 255, 0, 255, %d\n' % (j, REL)
            for j in range(len(pieces))) + '\n')
    open('sound/voicegroups/%s.inc' % VG.lstrip('_'), 'w').write(
        '@ Project Grounded: voicegroup voor Battle! Area Zero (vs_areazero_theme.py): programma 0 = de knippenkit.\n'
        'voice_group %s\n\tvoice_keysplit_all voicegroup_area_zero_vs\n' % VG.lstrip('_'))
    dsd = 'sound/direct_sound_data.inc'
    txt = open(dsd).read()
    for j in range(len(pieces)):
        lab = 'vsaz_%d' % j
        if 'DirectSoundWaveData_%s::' % lab not in txt:
            txt = txt.rstrip('\n') + ('\n\n\t.align 2\nDirectSoundWaveData_%s::\n'
                                      '\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (lab, lab))
    open(dsd, 'w').write(txt)
    vgi = 'sound/voice_groups.inc'
    txt = open(vgi).read()
    for inc in ('drumsets/area_zero_vs.inc', '%s.inc' % VG.lstrip('_')):
        line = '.include "sound/voicegroups/%s"' % inc
        if line not in txt:
            txt = txt.rstrip('\n') + '\n' + line + '\n'
    open(vgi, 'w').write(txt)

    notes = []
    for j, pc in enumerate(pieces):
        f0 = pc['frame']
        dur = int(pc['len'] / 11025 * 59.7275) + 2          # tot de sample zelf op is
        v = max(1, min(127, int(round(127 * pc['gain']))))
        notes.append([f0, f0 + dur, 36 + j, v])
    song = Song(24, 500000)
    song.tempo(0, 150 / 120)
    song.loop = (plan['loop_start'], plan['loop_end'])
    # niveau: één stem gaf -26 LUFS (Giratina -22,7, wild -17,6) bij velocity/volume al op 127; een tweede spoor
    # met dezelfde noten (zelfde frame, coherent) = +6 dB -> -20 LUFS. Kost 1 kanaal extra (max. 4 tijdens een naad).
    song.add(notes, 0, VOL, 0, 64)
    song.add([n[:] for n in notes], 0, VOL, 1, 64)
    song.save(OUT, plan['loop_end'])
    print(OUT, '%d stukken, lus %d-%d' % (len(notes), plan['loop_start'], plan['loop_end']))


if __name__ == '__main__':
    main()
