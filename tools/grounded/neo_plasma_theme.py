#!/usr/bin/env python3
"""Project Grounded: gevechtsmuziek van Neo Team Plasma (Battle Stadium): "Battle! Neo Team Plasma"
(Pokémon Black 2/White 2), MIDI van Byabbington (onlinesequencer).

Volgt de bron (sound/songs/grounded_src/b2w2_neo_plasma.mid, 176 bpm, 138 maten) 1-op-1: zelfde noten, volgorde en
structuur, loop over het hele nummer (zoals de vorige versie). Alleen de instrumenten zijn gemapt, drums omgezet,
akkoorden uitgedund en een stemverdeler (max. 10 DirectSound-noten tegelijk).

v1 (prepare_auto) gaf Jordi 'een puur synth-deuntje': de automatische mapping zette de elektrische gitaar (GM 27) en
de sawtooth (81) samen op één PSG-vierkant, de sine (80) op een tweede PSG-vierkant en de steel drums (114) op een
crashbekken; het kerkorgel (19) werd het dunne organ2. Nu krijgt elk bronspoor een eigen, echt instrument
(voicegroup_grounded_neo_plasma, een kopie van grounded_gm):

  bronspoor (GM-programma)        rol                                   GBA
  2013 Drum Kit (kanaal 10)       crash/splash                          rs_drumset 57/55
  909 Drum Kit                    kick (kwarten)                        rs_drumset 36
  Electric Drum Kit (118)         snare (achtste off-beats), hihats     rs_drumset 38/42/46
  Slap Bass (36)                  bas in octaven                        sc88pro_slap_bass (onderstem; octaaf erbij als er plaats is)
  8-Bit Sawtooth (81)             lead in octaven + bas-loopjes         lead: DirectSound-blokgolf (sc88pro_square_wave) + zacht PSG-vierkant
                                                                        op de bovenste octaaf; noten < C3: sc88pro_synth_bass
  Electric Guitar (27)            riff/powerchords                      < D3: sd90 distortion guitar (laag), anders sd90 overdrive guitar
  Church Organ (Classic) (19)     orgelakkoorden (16e)                  sc88pro_church_organ3_high (3 stemmen)
  8-Bit Sine (80)                 zachte lead + chromatische glissando's PSG golf (sinus, ProgrammableWaveData_1), zacht
  Steel Drums (114)               melodie                               sd90_classical_detuned_ep1_high, percussief (geen sample voor steel drums)
  8-Bit Triangle (80)             4 lange noten                         PSG golf (driehoek, ProgrammableWaveData_2), zacht
Gebruik: python3 tools/grounded/neo_plasma_theme.py"""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import notes_of, dedupe, thin, detach, allocate, releases, release_ticks, Song

SRC = 'sound/songs/grounded_src/b2w2_neo_plasma.mid'
OUT = 'sound/songs/midi/mus_grounded_vs_neo_plasma.mid'
VG = 'sound/voicegroups/grounded_neo_plasma.inc'
TPB, BAR, BEAT = 384, 1536, 384
BPM = 176
END = 138 * BAR

# programma's in voicegroup_grounded_neo_plasma
ORGAN, GTR_HI, GTR_LO, SLAP, SYNTH_BASS, LEAD, LEAD_PSG, SINE, TRI, STEEL, DRUMS = 19, 29, 31, 36, 38, 81, 80, 82, 83, 114, 127
VOICES = {
    ORGAN:      'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_church_organ3_high, 255, 76, 154, 120',
    GTR_HI:     'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_overdrive_guitar, 255, 0, 255, 130',
    GTR_LO:     'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_distortion_guitar_low, 255, 0, 255, 130',
    SLAP:       'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_slap_bass, 255, 235, 128, 99',
    SYNTH_BASS: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_synth_bass, 255, 252, 0, 115',
    LEAD:       'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_square_wave, 255, 0, 255, 120',
    LEAD_PSG:   'voice_square_1 60, 0, 0, 2, 0, 2, 9, 1',
    SINE:       'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_1, 0, 7, 15, 1',
    TRI:        'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_2, 0, 7, 15, 1',
    STEEL:      'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_detuned_ep1_high, 255, 225, 0, 170',
}
# drums (rs_drumset, eerste noot 36): (noot, lengte in ticks). De bron heeft overal 16e (96); echte lengtes.
# 37 (side stick) is PSG in rs_drumset -> snare iets zachter; 44 (pedaal-hihat, PSG) -> gesloten hihat;
# 49 -> crash 57; 55 (splash) = trinity-crash in de kit; 78 (cuíca, 2 noten) valt buiten de kit: weg.
DRUM_MAP = {36: (36, 192, 1.0), 37: (38, 192, 0.85), 38: (38, 192, 1.0), 42: (42, 96, 0.8), 44: (42, 96, 0.8),
            46: (46, 192, 0.9), 49: (57, 768, 1.0), 55: (55, 384, 0.9), 57: (57, 768, 1.0)}


def voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Neo Team Plasma (BW2). Gegenereerd door tools/grounded/neo_plasma_theme.py.'
    lines[1] = '@ Echte samples per bronspoor: 19 kerkorgel, 29/31 gitaar, 36 slap, 38 synthbas, 81 blokgolf-lead, 114 steel drums (EP).'
    lines[2] = 'voice_group grounded_neo_plasma'
    out = []
    for l in lines:
        k = l.rsplit('@', 1)[1].strip() if '@' in l and l.startswith('\tvoice') else None
        if k and k.isdigit() and int(k) in VOICES:
            l = '\t%s  @ %s' % (VOICES[int(k)], k)
        out.append(l)
    open(VG, 'w').write('\n'.join(out))


def groups(ev):
    g = {}
    for e in ev:
        g.setdefault(e[0], []).append(list(e))
    return [sorted(g[s], key=lambda e: e[2]) for s in sorted(g)]


def drums(ev):
    out, dropped = [], 0
    for s, e, n, v in ev:
        if n not in DRUM_MAP:
            dropped += 1
            continue
        n2, ln, f = DRUM_MAP[n]
        out.append([s, s + ln, n2, int(v * f)])
    out = dedupe(out)
    # een nieuwe slag op dezelfde drumnoot kapt de vorige af (anders twee kanalen voor één bekken)
    by = {}
    for e in out:
        by.setdefault(e[2], []).append(e)
    for lst in by.values():
        for a, b in zip(lst, lst[1:]):
            a[1] = min(a[1], b[0])
    return sorted(out), dropped


def build():
    m = mido.MidiFile(SRC)
    assert m.ticks_per_beat == TPB
    T = {i: notes_of(m.tracks[i]) for i in range(10)}
    clip = lambda ev: [[s, min(e, END), n, v] for s, e, n, v in ev if s < END]
    dr, drum_drop = drums(T[0] + T[1] + T[2])
    main = [e for e in dr if e[2] in (36, 38)]
    cym = [e for e in dr if e[2] not in (36, 38)]

    # slap bas: onderstem = bas, bovenste octaaf apart (lage prioriteit)
    bass, bass_oct = [], []
    for g in groups(T[3]):
        bass.append(g[0])
        bass_oct += g[1:2] if len(g) > 1 else []
    # sawtooth: noten < C3 = bas-loopjes (synthbas); de rest: bovenste noot op PSG, de tweede (of de enige) op DS
    saw_lo = [e for e in T[4] if e[2] < 48]
    lead, lead_psg = [], []
    for g in groups([e for e in T[4] if e[2] >= 48]):
        lead_psg.append(g[-1])
        lead.append(g[-2] if len(g) > 1 else list(g[-1]))
    saw_lo = thin(saw_lo, 1, 'top')         # octaven D#1+D#2: de bovenste (onder E1 dreunt het)
    # gitaar: onderste en bovenste noot van elk akkoord (octaaf/powerchord-omlijsting)
    gtr = []
    for g in groups(T[5]):
        gtr += [g[0]] + ([g[-1]] if g[-1][2] != g[0][2] else [])
    organ = thin(T[6], 3, 'top')
    parts = {'lead': lead, 'drums': main, 'bass': bass, 'guitar': gtr, 'organ': organ, 'steel': T[8],
             'cym': cym, 'saw_lo': saw_lo, 'bass_oct': bass_oct}
    parts = {k: dedupe(clip(v)) for k, v in parts.items()}
    psg = {'lead_psg': dedupe(clip(lead_psg)), 'sine': dedupe(clip(T[7])), 'tri': dedupe(clip(T[9]))}

    voicegroup()
    rel = releases('grounded_neo_plasma')
    progs = {'lead': LEAD, 'bass': SLAP, 'bass_oct': SLAP, 'guitar': GTR_HI, 'organ': ORGAN, 'steel': STEEL,
             'saw_lo': SYNTH_BASS}
    tail = {k: release_ticks(rel[p], TPB, BPM) for k, p in progs.items()}
    tail.update(drums=0, cym=0)
    for k in progs:                                   # legato/16e: vorige noot een uitklinktijd eerder los
        parts[k] = detach(parts[k], tail[k])
    order = ['lead', 'drums', 'bass', 'guitar', 'organ', 'steel', 'cym', 'saw_lo', 'bass_oct']
    res = allocate(parts, order, tail)
    print('drumnoten buiten de kit (weg): %d' % drum_drop)
    for k in order:
        n, kept = len(parts[k]), len(res[k])
        print('  %-9s %4d noten, %3d vallen weg (%.1f%%)' % (k, n, n - kept, 100 * (n - kept) / max(n, 1)))
    p = res
    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.loop = (0, END)
    tracks = [
        (p['lead'], LEAD, 114, 0, 64),
        (psg['lead_psg'], LEAD_PSG, 44, 1, 64),
        ([e for e in p['guitar'] if e[2] >= 50], GTR_HI, 116, 2, 44),
        ([e for e in p['guitar'] if e[2] < 50], GTR_LO, 120, 3, 44),
        (p['organ'], ORGAN, 106, 4, 84),
        (p['bass'], SLAP, 127, 5, 64),
        (p['bass_oct'], SLAP, 96, 6, 64),
        (p['saw_lo'], SYNTH_BASS, 114, 7, 64),
        (p['steel'], STEEL, 124, 8, 76),
        (psg['sine'], SINE, 48, 10, 64),
        (psg['tri'], TRI, 44, 11, 64),
        (sorted(p['drums'] + p['cym']), DRUMS, 127, 9, None),
    ]
    written = 0
    for notes, prog, vol, ch, pan in tracks:
        if notes:
            song.add(notes, prog, vol, ch, pan)
            written += len(notes)
    assert written == sum(len(p[k]) for k in order) + sum(len(v) for v in psg.values()), 'niet elke partij staat in de MIDI'
    song.save(OUT, END)
    print(OUT, '(%d sporen, %.1f s per ronde)' % (len(song.tracks), END / TPB * 60 / BPM))


if __name__ == '__main__':
    build()
