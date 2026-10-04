#!/usr/bin/env python3
"""Project Grounded: drie varianten van het legendary beasts-thema (MUS_C_VS_LEGEND_BEAST), à la HGSS (Jordi):
grotendeels hetzelfde nummer, met per beest één kenmerkende laag bovenop het ongewijzigde origineel.

- Suicune: heldere, galmende klokken op de melodie (zuiverheid, rust, regen) + glockenspiel-druppels op de arpeggio's.
- Entei:   elektrische gitaar: overdrive-lead op de melodie + distortion-power-chords op de baslijn (vuur, vulkaan).
- Raikou:  scherpe, zoemende synths: een smalle blokgolf (12,5%) op de melodie, snelle 'zaps' op de arpeggio's en
           zachte ruis-knetters (elektriciteit, snelheid, onweer). PSG: kost geen DirectSound-kanalen.
De drie originele sporen worden 1-op-1 gekopieerd; voicegroup_grounded_beasts = voicegroup_dummy (die het origineel
gebruikt) + de extra instrumenten op 98-105. Zie tools/grounded/MUZIEK.md.
Gebruik: python3 tools/grounded/beasts_theme.py"""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import notes_of, thin, detach, allocate, releases, release_ticks, ds_occupancy

SRC = 'sound/songs/midi/mus_c_vs_legend_beast.mid'
OUT = 'sound/songs/midi/mus_grounded_vs_%s.mid'
VG = 'grounded_beasts'
TPB = 24
BPM = 60e6 / 322580
BELL, GLOCK, OVERDRIVE, DIST_HI, DIST_LO, BUZZ, ZAP, CRACKLE = 98, 99, 100, 101, 102, 103, 104, 105
EXTRA = {
    BELL: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_tubular_bell, 255, 216, 90, 242',
    GLOCK: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_glockenspiel, 255, 165, 51, 170',   # korte druppels
    OVERDRIVE: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_overdrive_guitar, 255, 0, 255, 170',
    DIST_HI: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_distortion_guitar_high, 255, 0, 255, 160',
    DIST_LO: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_distortion_guitar_low, 255, 0, 255, 160',
    BUZZ: 'voice_square_1 60, 0, 0, 0, 0, 0, 15, 1',          # duty 12,5%: scherp en zoemend
    ZAP: 'voice_square_2 60, 0, 1, 0, 1, 4, 0',               # duty 25%, kort: elektrische zaps
    CRACKLE: 'voice_noise_alt 60, 0, 0, 0, 1, 0, 0',          # ruis-knetter
}


def voicegroup():
    src = [l for l in open('sound/voicegroups/dummy.inc').read().split('\n') if l.strip().startswith('voice_')
           and not l.strip().startswith('voice_group')]
    assert len(src) == BELL, 'dummy heeft %d stemmen' % len(src)
    out = ['@ Project Grounded: voicegroup_dummy + extra instrumenten voor de beasts-varianten. Gegenereerd door',
           '@ tools/grounded/beasts_theme.py.', 'voice_group %s' % VG] + src
    out += ['\t%s  @ %d' % (EXTRA[p], p) for p in sorted(EXTRA)]
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out) + '\n')


def note_track(notes, prog, vol, ch, pan=64):
    t = mido.MidiTrack()
    t.append(mido.Message('program_change', channel=ch, program=prog, time=0))
    t.append(mido.Message('control_change', channel=ch, control=7, value=vol, time=0))
    t.append(mido.Message('control_change', channel=ch, control=10, value=pan, time=0))
    msgs = sorted([(s, 1, n, v) for s, e, n, v in notes] + [(e, 0, n, 0) for s, e, n, v in notes])
    last = 0
    for tk, kind, n, v in msgs:
        t.append(mido.Message('note_on' if kind else 'note_off', channel=ch, note=n,
                              velocity=max(1, min(127, int(v))) if kind else 0, time=tk - last))
        last = tk
    return t


def build(beast):
    src = mido.MidiFile(SRC)
    T = {i: notes_of(src.tracks[i]) for i in (1, 2, 3)}
    melody = [e for e in T[1] if e[2] >= 72 and e[1] - e[0] >= TPB // 2]      # melodienoten (vanaf C5, >= 8e)
    arps = [e for e in T[2] if e[2] >= 84]                                     # de hoge fonkelende arpeggio's
    bass = T[3]
    layers = []                                                                # (naam, noten, programma, volume, pan, DS?)
    if beast == 'suicune':
        layers.append(('bells', [[s, min(e, s + 2 * TPB), n, 127] for s, e, n, v in melody], BELL, 127, 64, True))
        layers.append(('glock', [[s, s + TPB // 2, n - 12, 100] for s, e, n, v in arps], GLOCK, 96, 88, True))
    elif beast == 'entei':
        layers.append(('lead', [[s, e, n - 12, 112] for s, e, n, v in melody], OVERDRIVE, 104, 72, True))
        chords, seen = [], set()
        for s, e, n, v in bass:                       # één power chord per tel (grondtoon + kwint), strak
            beat = s // TPB
            if beat in seen:
                continue
            seen.add(beat)
            r = n + 12 if n < 40 else n
            chords += [[s, s + TPB // 2, r, 110], [s, s + TPB // 2, r + 7, 102]]
        layers.append(('power', chords, DIST_LO, 96, 52, True))
    elif beast == 'raikou':
        layers.append(('buzz', [[s, e, n, 112] for s, e, n, v in melody], BUZZ, 72, 64, False))
        layers.append(('zap', [[s, s + TPB // 4, n - 12, 100] for s, e, n, v in arps], ZAP, 40, 90, False))
        end = max(e for s, e, n, v in bass)
        layers.append(('crackle', [[t, t + 4, 72 + (t // TPB) % 5, 60] for t in range(0, end, TPB * 2)
                                   if (t // TPB) % 8 in (3, 6)], CRACKLE, 30, 40, False))
    # DirectSound-lagen: stemverdeling met het origineel als vaste bezetting
    rel = releases(VG)
    preset = []
    for i in (1, 2, 3):
        preset += ds_occupancy(src.tracks[i], rel, TPB, BPM)
    ds = {k: notes for k, notes, prog, vol, pan, isds in layers if isds}
    tail = {k: release_ticks(rel.get(prog, 200), TPB, BPM) for k, notes, prog, vol, pan, isds in layers if isds}
    for k in ds:
        ds[k] = detach(ds[k], tail[k])
    kept = allocate(ds, list(ds), tail, preset=preset, max_voices=11)   # legendary: 11 (1 vrij voor effecten)
    for k in ds:
        if len(kept[k]) < len(ds[k]) * 0.97:
            print('  %s/%s: %d van %d noten vallen weg (te vol)' % (beast, k, len(ds[k]) - len(kept[k]), len(ds[k])))
    out = mido.MidiFile(type=1, ticks_per_beat=TPB)
    for t in src.tracks:
        out.tracks.append(t.copy() if hasattr(t, 'copy') else mido.MidiTrack(t))
    for ch, (k, notes, prog, vol, pan, isds) in enumerate(layers, start=4):
        out.tracks.append(note_track(kept.get(k, notes) if isds else notes, prog, vol, ch, pan))
    out.save(OUT % beast)
    print(OUT % beast)


if __name__ == '__main__':
    voicegroup()
    for b in ('suicune', 'entei', 'raikou'):
        build(b)
