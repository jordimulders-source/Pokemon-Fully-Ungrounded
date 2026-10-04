#!/usr/bin/env python3
"""Project Grounded: Wally's gevechtsmuziek die met Wally meegroeit (Jordi).

Eén bron (sound/songs/grounded_src/wally_battle_oras.mid, ORAS "Battle! Wally"), vijf arrangementen met dezelfde
noten en dus dezelfde iconische melodie, steeds zwaarder:
  1 = fluitje + akoestische gitaar (bovenstem), traag en wimpy (vrij voor een nieuw vroeg gevecht)
  2 = fluit + klarinet + akoestische gitaar (vrij voor een nieuw gevecht)
  3 = Mauville: blokfluit, nylon-gitaar, plukkende bas, kick + tamboerijn
  4 = Meteor Falls: overdrive-gitaar, trompet, bas, strijkers, trombone, volle drums
  5 = Victory Road en rematches: heavy metal, distortion-gitaar en -bas, dubbele bassdrum, crashes, sneller.
Een stemverdeler houdt het aantal noten tegelijk onder de 8 kanalen van de engine (zie tools/grounded/MUZIEK.md).
De elektrische piano uit de MIDI is in ORAS een elektrische gitaar. Drumnoten 37 en 52 zijn in rs_drumset PSG-piepjes:
die worden snare (38) en crash (57). Schrijft ook voicegroup_grounded_wally (= grounded_gm met echte gitaren op 24-31).
Gebruik: python3 tools/grounded/wally_theme.py"""
import mido

SRC = 'sound/songs/grounded_src/wally_battle_oras.mid'
OUT = 'sound/songs/midi/mus_grounded_vs_wally_%d.mid'
VG = 'sound/voicegroups/grounded_wally.inc'
# sporen in de bron: 0 viool, 1 basgitaar, 2 trombone, 3 hoorn (melodie), 4 drums, 5 cello, 6 e-piano (= gitaar-riff)
NYLON, OVERDRIVE, DIST, DIST_LOW, WHISTLE, FLUTE, CLARINET, AC_BASS = 24, 29, 30, 31, 78, 73, 71, 32
# per spoor: (programma, volume[, max. noten tegelijk, 'top'/'bottom'])
ARR = {
    1: dict(tempo=0.74, tracks={3: (WHISTLE, 92, 1, 'top'), 6: (NYLON, 80, 1, 'top'), 1: (AC_BASS, 60, 1, 'bottom'),
                                4: ('drums_tiny', 56)}),
    2: dict(tempo=0.80, tracks={3: (FLUTE, 96, 1, 'top'), 6: (NYLON, 86, 2, 'top'), 2: (CLARINET, 62, 1, 'top'),
                                1: (AC_BASS, 70, 1, 'bottom'), 4: ('drums_soft', 62)}),
    3: dict(tempo=0.88, tracks={3: (73, 100), 6: (NYLON, 96), 1: (33, 84), 4: ('drums_soft', 70)}),
    4: dict(tempo=0.95, tracks={3: (56, 104), 6: (OVERDRIVE, 104), 1: (33, 100), 5: (48, 64), 2: (57, 80), 4: ('drums', 96)}),
    5: dict(tempo=1.04, tracks={3: (60, 112), 6: (DIST, 116), 1: (DIST_LOW, 104, 2, 'bottom'),
                                2: (57, 96), 4: ('drums_metal', 120)}),
}
DRUM_FIX = {37: 38, 52: 57}
# De engine mixt 8 DirectSound-kanalen (m4a.c). Meer noten tegelijk = een nieuwe noot steelt een kanaal en kapt een
# andere af ("snips"). Daarom verdeelt dit script de stemmen: max. MAX_VOICES tegelijk, met voorrang op volgorde.
MAX_VOICES = 8
PRIORITY = [3, 6, 4, 1, 2, 5, 0]          # melodie, riff, drums, bas, trombone, cello, viool
DRUM_LEN = 96                             # drumsamples zijn kort; lange drumnoten houden alleen een kanaal bezet
TAIL = 96                                 # uitklinktijd (ticks) die een kanaal na de note-off nog bezet houdt


def notes_of(t):
    tick, on, ev = 0, {}, []
    for msg in t:
        tick += msg.time
        if msg.type == 'note_on' and msg.velocity:
            on.setdefault(msg.note, []).append((tick, msg.velocity))
        elif msg.type in ('note_on', 'note_off') and on.get(msg.note):
            s, vel = on[msg.note].pop(0)
            ev.append([s, tick, msg.note, vel])
    seen, out = set(), []                  # de bron heeft dubbele noten (zelfde noot, zelfde tick): klik + kanaalroof
    for e in sorted(ev):
        if (e[0], e[2]) not in seen:
            seen.add((e[0], e[2]))
            out.append(e)
    return out


def thin(ev, maxn, keep):
    """Akkoorden uitdunnen tot maxn noten (hoogste of laagste houden)."""
    out = []
    by_start = {}
    for e in ev:
        by_start.setdefault(e[0], []).append(e)
    for s in sorted(by_start):
        grp = sorted(by_start[s], key=lambda e: -e[2] if keep == 'top' else e[2])
        active = [o for o in out if o[0] < s < o[1]]
        room = max(0, maxn - len(active))
        out += grp[:room] if room else []
        if not room:                       # oude noot afkappen voor de nieuwe (legato), anders verdwijnt de melodie
            for o in active:
                o[1] = s
            out += grp[:maxn]
    return sorted(out)


def drums_for(ev, mode, end):
    out = []
    for s, e, n, vel in ev:
        n = DRUM_FIX.get(n, n)
        if mode == 'drums_soft' and n in (38, 57, 55):
            n = 54
        if mode == 'drums_tiny':           # alleen een voorzichtige kick op de tel en wat tamboerijn
            if n == 36 and s % 384 == 0:
                vel = int(vel * 0.7)
            elif n in (38, 57, 55) and s % 768 == 384:
                n, vel = 54, int(vel * 0.6)
            else:
                continue
        out.append([s, s + DRUM_LEN, n, vel])
    if mode == 'drums_metal':              # dubbele bassdrum op elke achtste en een crash op elke maat
        have = {s for s, _, n, _ in out if n == 36}
        out += [[t, t + DRUM_LEN, 36, 96] for t in range(0, end, 192) if t not in have]
        out += [[t, t + DRUM_LEN, 57, 100] for t in range(0, end, 1536) if not any(o[0] == t and o[2] == 57 for o in out)]
    seen, res = set(), []                  # na het omzetten (snare -> tamboerijn) opnieuw ontdubbelen
    for e in sorted(out):
        if (e[0], e[2]) not in seen:
            seen.add((e[0], e[2]))
            res.append(e)
    return res


def build(v):
    src = mido.MidiFile(SRC)
    a = ARR[v]
    out = mido.MidiFile(type=1, ticks_per_beat=src.ticks_per_beat)
    cond = mido.MidiTrack()
    end = max(sum(m.time for m in t) for t in src.tracks)
    tempo = next(m.tempo for t in src.tracks for m in t if m.type == 'set_tempo')
    cond.append(mido.MetaMessage('set_tempo', tempo=int(tempo / a['tempo']), time=0))
    cond.append(mido.MetaMessage('marker', text='[', time=0))
    cond.append(mido.MetaMessage('marker', text=']', time=end))
    out.tracks.append(cond)
    parts = {}
    for ti, spec in a['tracks'].items():
        prog = spec[0]
        ev = notes_of(src.tracks[ti])
        if isinstance(prog, str):
            ev = drums_for(ev, prog, end)
        elif len(spec) > 2:
            ev = thin(ev, spec[2], spec[3])
        if v in (1, 2):                    # zachter en minder stellig
            for e in ev:
                e[3] = max(30, int(e[3] * 0.8))
        parts[ti] = ev
    # stemmen verdelen: wie lager in PRIORITY staat, valt weg als alle kanalen bezet zijn
    busy = []
    for ti in sorted(parts, key=PRIORITY.index):
        kept = []
        for e in parts[ti]:
            s, en = e[0], e[1] + TAIL
            pts = [s] + [b[0] for b in busy if s < b[0] < en]   # over de hele duur van de noot, niet alleen de start
            if all(sum(1 for b in busy if b[0] <= p < b[1]) < MAX_VOICES for p in pts):
                kept.append(e)
                busy.append((s, en))
        parts[ti] = kept
    for ti, spec in a['tracks'].items():
        prog, vol = spec[0], spec[1]
        drums = isinstance(prog, str)
        ch = 9 if drums else ti if ti != 4 else 8
        nt = mido.MidiTrack()
        nt.append(mido.Message('program_change', channel=ch, program=127 if drums else prog, time=0))
        nt.append(mido.Message('control_change', channel=ch, control=7, value=vol, time=0))
        msgs = []
        for s, e, n, vel in parts[ti]:
            msgs.append((s, 1, n, vel))
            msgs.append((e, 0, n, 0))
        msgs.sort()
        last = 0
        for t, kind, n, vel in msgs:
            nt.append(mido.Message('note_on' if kind else 'note_off', channel=ch, note=n, velocity=vel, time=t - last))
            last = t
        out.tracks.append(nt)
    out.save(OUT % v)


def voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[2] = 'voice_group grounded_wally'
    lines[0] = '@ Project Grounded: grounded_gm met echte gitaren op 24-31 (Wally). Gegenereerd door tools/grounded/wally_theme.py.'
    lines[1] = '@ 24-27 nylon, 28-29 overdrive, 30-31 distortion, 78 fluitje.'
    rep = {24: 'sc88pro_nylon_str_guitar, 255, 249, 25, 76', 25: 'sc88pro_nylon_str_guitar, 255, 249, 25, 76',
           26: 'sc88pro_nylon_str_guitar, 255, 249, 25, 76', 27: 'sc88pro_nylon_str_guitar, 255, 249, 25, 76',
           28: 'sd90_classical_overdrive_guitar, 255, 0, 255, 226', 29: 'sd90_classical_overdrive_guitar, 255, 0, 255, 226',
           30: 'sd90_classical_distortion_guitar_high, 255, 0, 255, 195', 31: 'sd90_classical_distortion_guitar_low, 255, 0, 255, 195',
           78: 'sd90_classical_whistle, 255, 127, 231, 127'}
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
