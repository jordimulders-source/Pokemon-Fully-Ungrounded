#!/usr/bin/env python3
"""Project Grounded: Wally's gevechtsmuziek die met Wally meegroeit (Jordi).

Eén bron (sound/songs/grounded_src/wally_battle_oras.mid, ORAS "Battle! Wally"), drie arrangementen met dezelfde
noten en dus dezelfde iconische melodie:
  1 = Mauville (kneuzerig): blokfluit op de melodie, Wally's eerste gitaar (nylon) speelt de riff, plukkende bas,
      alleen kick + tamboerijn, iets trager.
  2 = Meteor Falls: overdrive-gitaar, trompet op de melodie, bas, strijkers zacht, vollere drums.
  3 = Victory Road en rematches: het eindresultaat met distortion-gitaar, strijkers, trombone, hoorn, cello, volle drums.
De elektrische piano uit de MIDI is in ORAS een elektrische gitaar. Drumnoten 37 en 52 zijn in rs_drumset PSG-piepjes:
die worden snare (38) en crash (57). Schrijft ook voicegroup_grounded_wally (= grounded_gm met echte gitaren op 24-31).
Gebruik: python3 tools/grounded/wally_theme.py"""
import mido

SRC = 'sound/songs/grounded_src/wally_battle_oras.mid'
OUT = 'sound/songs/midi/mus_grounded_vs_wally_%d.mid'
VG = 'sound/voicegroups/grounded_wally.inc'
# sporen in de bron: 0 viool, 1 basgitaar, 2 trombone, 3 hoorn (melodie), 4 drums, 5 cello, 6 e-piano (= gitaar-riff)
NYLON, OVERDRIVE, DIST = 24, 29, 30
ARR = {
    1: dict(tempo=0.88, tracks={3: (73, 100), 6: (NYLON, 96), 1: (33, 84), 4: ('drums_soft', 70)}),
    2: dict(tempo=0.95, tracks={3: (56, 104), 6: (OVERDRIVE, 104), 1: (33, 100), 5: (48, 64), 2: (57, 80), 4: ('drums', 96)}),
    3: dict(tempo=1.0, tracks={3: (60, 112), 6: (DIST, 112), 1: (33, 110), 5: (48, 92), 0: (40, 96), 2: (57, 100), 4: ('drums', 116)}),
}
DRUM_FIX = {37: 38, 52: 57}


def build(v):
    src = mido.MidiFile(SRC)
    a = ARR[v]
    out = mido.MidiFile(type=1, ticks_per_beat=src.ticks_per_beat)
    cond = mido.MidiTrack()
    end = 0
    for t in src.tracks:
        tick = 0
        for msg in t:
            tick += msg.time
        end = max(end, tick)
    tempo = next(m.tempo for t in src.tracks for m in t if m.type == 'set_tempo')
    cond.append(mido.MetaMessage('set_tempo', tempo=int(tempo / a['tempo']), time=0))
    cond.append(mido.MetaMessage('marker', text='[', time=0))
    cond.append(mido.MetaMessage('marker', text=']', time=end))
    out.tracks.append(cond)
    for ti, (prog, vol) in a['tracks'].items():
        t = src.tracks[ti]
        nt = mido.MidiTrack()
        drums = prog in ('drums', 'drums_soft')
        ch = 9 if drums else ti if ti != 4 else 8
        nt.append(mido.Message('program_change', channel=ch, program=127 if drums else prog, time=0))
        nt.append(mido.Message('control_change', channel=ch, control=7, value=vol, time=0))
        pending = 0
        for msg in t:
            pending += msg.time
            if msg.is_meta or msg.type not in ('note_on', 'note_off'):
                continue
            note = msg.note
            if drums:
                note = DRUM_FIX.get(note, note)
                if prog == 'drums_soft':          # kneuzerig: alleen kick en tamboerijn i.p.v. snare/crash
                    if note in (38, 57, 55):
                        note = 54
            vel = msg.velocity if msg.type == 'note_on' else 0
            if v == 1 and vel:
                vel = max(30, int(vel * 0.8))
            nt.append(mido.Message('note_on' if vel else 'note_off', channel=ch, note=note, velocity=vel, time=pending))
            pending = 0
        out.tracks.append(nt)
    out.save(OUT % v)


def voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[2] = 'voice_group grounded_wally'
    lines[0] = '@ Project Grounded: grounded_gm met echte gitaren op 24-31 (Wally). Gegenereerd door tools/grounded/wally_theme.py.'
    lines[1] = '@ 24-27 nylon, 28-29 overdrive, 30-31 distortion.'
    rep = {24: 'sc88pro_nylon_str_guitar, 255, 249, 25, 76', 25: 'sc88pro_nylon_str_guitar, 255, 249, 25, 76',
           26: 'sc88pro_nylon_str_guitar, 255, 249, 25, 76', 27: 'sc88pro_nylon_str_guitar, 255, 249, 25, 76',
           28: 'sd90_classical_overdrive_guitar, 255, 0, 255, 226', 29: 'sd90_classical_overdrive_guitar, 255, 0, 255, 226',
           30: 'sd90_classical_distortion_guitar_high, 255, 0, 255, 195', 31: 'sd90_classical_distortion_guitar_low, 255, 0, 255, 195'}
    out = []
    for l in lines:
        if l.rstrip().endswith(tuple('@ %d' % k for k in rep)):
            k = int(l.rsplit('@', 1)[1])
            l = '\tvoice_directsound 60, 0, DirectSoundWaveData_%s  @ %d' % (rep[k], k)
        out.append(l)
    open(VG, 'w').write('\n'.join(out))


if __name__ == '__main__':
    voicegroup()
    for v in ARR:
        build(v)
        print(OUT % v)
