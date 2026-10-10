#!/usr/bin/env python3
"""Project Grounded: Battle! Dialga/Palkia (Diamond/Pearl) op de GBA, uit Jordi's MIDI (DialgaPalkiaMIDIBeta.mid).

Jordi: "Arceus en Dialga/Palkia themes wil ik eigenlijk nog wel namaken, ik denk dat dat niet al te moeilijk zal
zijn, omdat beide redelijk simplistische instrumenten gebruiken. Maar moeten kijken of dat lukt voor niet te hoge
files."  MUS_GROUNDED_VS_DIALGA_PALKIA = 678 (Dialga, Palkia en hun Origin-vormen, Spear Pillar).

De noten komen 1-op-1 uit de MIDI (staat op origin/master, niet in de werkbranch; pad als argument of
DP_MIDI=...). 180 bpm, tpb 96, 9 eenstemmige sporen. Alleen stock-samples (Emerald/FRLG), geen eigen samples.
Opruimen (geen hercompositie):
  - vorm: intro maat 0-5, loop maat 6 -> 115,5. Alles na maat 48,5 staat een halve maat verschoven (de MIDI
    heeft daar een 2/4-maat); het einde (115,5) sluit naadloos aan op maat 6 (bas C-E-pedaal, arpeggio, drums en
    pauken lopen door).
  - spoor 7 speelt overal 12 ticks (1/32) te laat (een 'humanize'-vertraging); terug op de tel. Waar het dan
    unisono met spoor 2/3 meespeelt, krijgt de verdubbeling de laagste prioriteit in de stemverdeler.
  - spoor 4 = spoor 6 een octaaf lager en 12 ticks later (echo): beide op de PSG-vierkanten, op de tel.
  - 'fp'-houdnoten (accent 47 ticks + dezelfde noot op velocity 40) worden één noot; andere v40-noten -> v84.
  - programma's van de MIDI per sectie (strijkers/hoorn/trompet/orgel/EP), behalve de rare: spoor 1 'sopraansax'
    vanaf maat 48 (bas) blijft synth-bas, spoor 3 'fretless bass' (maat 32-43, akkoordnoten G3) = strijkers,
    spoor 9 'synth strings' (maat 68-87, paukenpartij) = pauken, de losse 'piano'-noot van spoor 2 = strijkers.
  - koper niet onder C3: trompetnoten onder C3 (spoor 5, maat 107-113) op strijkers.
  - drum 66 (timbale met pitchbend-sweep, maat 89) valt weg; crashes op de sectiestarts (de MIDI heeft er één).
Stemverdeler max. 11 DirectSound-noten (legendary), PSG telt niet mee.
  python3 tools/grounded/dialga_theme.py <dp.mid>
Zie tools/grounded/MUZIEK.md."""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import notes_of, dedupe, detach, releases, release_ticks, Song

VG = 'grounded_dialga'
OUT = 'sound/songs/midi/mus_grounded_vs_dialga_palkia.mid'
MAXV = 11
TPB = 96
BAR = TPB * 4
BPM = 180
LOOP0 = 6 * BAR
END = 115 * BAR + BAR // 2

# programma's in voicegroup_grounded_dialga
SYNBASS, STR, HORN, TPT, ORGAN, EP, TIMP = 39, 48, 60, 56, 18, 4, 47
SQ1, SQ2, NOISE, KIT = 80, 81, 121, 127
# eigen drumkit drumsets/dialga.inc
KICK, SN, CLAP, TOM_L, TOM_M, TOM_H, CRASH = range(36, 43)
DRUM_MAP = {36: KICK, 40: SN, 39: CLAP, 41: TOM_L, 43: TOM_M, 48: TOM_H, 57: CRASH}
HATS = {42: (84, 70), 44: (84, 56)}      # gesloten / pedaal-hihat -> PSG-ruis (toets, velocity)
GM2INST = {39: SYNBASS, 64: SYNBASS, 38: SYNBASS, 48: STR, 1: STR, 35: STR, 60: HORN, 56: TPT, 18: ORGAN,
           2: EP, 47: TIMP, 51: TIMP}
# prioriteit per bronspoor (hoog eerst): melodie (3, 7), tegenstem/akkoord (2, 5), bas, drums, pauken
PRIO = [3, 7, 5, 2, 'drums', 1, 9, 'dbl']


def load(path):
    m = mido.MidiFile(path)
    assert m.ticks_per_beat == TPB
    out = {}
    for i, t in enumerate(m.tracks):
        tick, prog, ev = 0, None, []
        on = {}
        for x in t:
            tick += x.time
            if x.type == 'program_change':
                prog = x.program
            elif x.type == 'note_on' and x.velocity:
                on.setdefault(x.note, []).append((tick, x.velocity, prog))
            elif x.type in ('note_on', 'note_off') and on.get(x.note):
                s, v, p = on[x.note].pop(0)
                ev.append([s, tick, x.note, v, p])
        seen, ded = set(), []
        for e in sorted(ev):
            if (e[0], e[2]) not in seen:
                seen.add((e[0], e[2])); ded.append(e)
        out[i] = ded
    return out


def fp_merge(ev):
    """accent + houdnoot (zelfde toon, v40, sluit aan) -> één noot."""
    ev = sorted(ev)
    out = []
    for e in ev:
        prev = out[-1] if out else None
        if prev and e[3] <= 48 and e[2] == prev[2] and 0 <= e[0] - prev[1] <= 4:
            prev[1] = e[1]
            continue
        out.append(list(e))
    for e in out:
        if e[3] < 80:
            e[3] = 84
    return out


def build_parts(src):
    S = load(src)
    notes = []          # [s, e, n, v, inst, prio]
    # spoor 7: 12 ticks terug op de tel
    t7 = []
    for s, e, n, v, p in S[7]:
        if s % 48 == 12:
            s, e = s - 12, e - 12
        t7.append([s, e, n, v, p])
    S[7] = t7
    others = {(s, n) for tr in (2, 3) for s, e, n, v, p in S[tr]}
    for tr in (1, 2, 3, 5, 7, 9):
        for s, e, n, v, p in fp_merge(S[tr]):
            inst = GM2INST[p]
            if tr == 3 and p == 35:
                inst = STR
            if inst == TPT and n < 48:
                inst = STR
            if inst == TIMP:
                v = max(v, 100)
            prio = tr
            if tr == 7 and (s, n) in others:
                prio = 'dbl'
            notes.append([s, e, n, v, inst, prio])
    # drums
    drums, hats = [], []
    for s, e, n, v, p in S[8]:
        if n in HATS:
            key, vel = HATS[n]
            hats.append([s, s + 12, key, vel if v >= 100 else vel - 14])
        elif n in DRUM_MAP:
            drums.append([s, e, DRUM_MAP[n], min(127, v + 10)])
    for b in (12 * BAR, 48 * BAR + BAR // 2, 95 * BAR + BAR // 2, LOOP0):
        if not any(d[0] == b and d[2] == CRASH for d in drums):
            drums.append([b, b + BAR // 2, CRASH, 112])
    # PSG-vierkanten: arpeggio (6) en de octaaf-echo (4), op de tel
    sq1 = [[s, e, n, 100 if v >= 100 else 84] for s, e, n, v, p in S[6]]
    sq2 = []
    for s, e, n, v, p in S[4]:
        if s % 48 == 12:
            s, e = s - 12, e - 12
        sq2.append([s, e, n, 96 if v >= 100 else 80])
    return notes, dedupe(drums), dedupe(hats), dedupe(sq1), dedupe(sq2)


def voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm + overrides voor Battle! Dialga/Palkia (Diamond/Pearl).'
    lines[1] = '@ Gegenereerd door tools/grounded/dialga_theme.py. Alleen stock-samples.'
    lines[2] = 'voice_group %s' % VG
    over = {
        4: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_detuned_ep1_high, 255, 204, 77, 200',
        18: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_organ2, 255, 0, 255, 150',
        39: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_synth_bass, 255, 252, 0, 115',
        47: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 200',
        80: 'voice_square_1 60, 0, 0, 2, 0, 2, 5, 1',
        81: 'voice_square_2 60, 0, 2, 0, 2, 5, 1',
        121: 'voice_noise_alt 60, 0, 0, 0, 1, 0, 0',
        127: 'voice_keysplit_all voicegroup_dialga_drumset',
    }
    out = []
    for l in lines:
        for k, v in over.items():
            if l.rstrip().endswith('@ %d' % k):
                l = '\t%s  @ %d' % (v, k)
        out.append(l)
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    kit = [
        ('36 kick', 'voice_directsound 67, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 180'),
        ('37 snare', 'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 180'),
        ('38 clap', 'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_tr909_hand_clap, 255, 0, 255, 170'),
        ('39 tom laag', 'voice_directsound 45, 52, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180'),
        ('40 tom midden', 'voice_directsound 51, 64, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180'),
        ('41 tom hoog', 'voice_directsound 57, 76, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180'),
        ('42 crash', 'voice_directsound 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165'),
    ]
    open('sound/voicegroups/drumsets/dialga.inc', 'w').write(
        '@ Project Grounded: drumkit voor dialga_theme.py (Battle! Dialga/Palkia). Alleen stock-samples, geen PSG.\n'
        '@ ' + ', '.join(n for n, _ in kit) + '.\n'
        '@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.\n'
        'voice_group dialga_drumset, 36\n' + ''.join('\t%s\n' % v for _, v in kit))


LAYOUT = [  # (instrument, volume, kanaal, pan); volumes gemeten met balance.py tegen een FluidR3-render van de bron
    (STR, 88, 0, 64),
    (HORN, 92, 1, 56),
    (TPT, 84, 2, 72),
    (ORGAN, 88, 3, 64),
    (EP, 84, 4, 72),
    (SYNBASS, 127, 5, 64),
    (TIMP, 68, 6, 60),
]


def build(src):
    notes, drums, hats, sq1, sq2 = build_parts(src)
    rel = releases(VG)
    tail = {i: release_ticks(rel.get(i, 200), TPB, BPM) + 2 for i, *_ in LAYOUT}
    dtail = release_ticks(180, TPB, BPM) + 2
    # legato per bronspoor (zelfde spoor: vorige noot een uitklinktijd eerder los)
    by_tr = {}
    for e in notes:
        by_tr.setdefault(e[5] if e[5] != 'dbl' else 7, []).append(e)
    for tr, ev in by_tr.items():
        ev.sort()
        starts = sorted({e[0] for e in ev})
        for e in ev:
            nxt = next((t for t in starts if t > e[0]), None)
            if nxt is not None:
                e[1] = min(e[1], max(e[0] + 6, nxt - tail[e[4]]))
    for e in notes:
        assert e[2] >= 28, e
        if e[4] in (TPT, HORN):
            assert e[2] >= 48, e
    # stemverdeler over de hele nootduur incl. uitklinktijd, op prioriteit
    busy, kept, lost = [], [], {}
    items = [(PRIO.index(e[5]), e[0], 'n', e) for e in notes] + [(PRIO.index('drums'), d[0], 'd', d) for d in drums]
    items.sort(key=lambda x: (x[0], x[1]))
    for pr, s, kind, e in items:
        en = e[1] + (tail[e[4]] if kind == 'n' else dtail)
        pts = [s] + [b[0] for b in busy if s < b[0] < en]
        if all(sum(1 for b in busy if b[0] <= p < b[1]) < MAXV for p in pts):
            kept.append((kind, e)); busy.append((s, en))
        else:
            lost.setdefault(PRIO[pr], []).append(e)
    total = {}
    for e in notes:
        total[e[5]] = total.get(e[5], 0) + 1
    total['drums'] = len(drums)
    for k in PRIO:
        if k in lost:
            print('  %s: %d van %d noten vallen weg (%.1f%%), maten %s' % (
                k, len(lost[k]), total[k], 100 * len(lost[k]) / total[k], sorted({e[0] // BAR for e in lost[k]})[:12]))
    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.loop = (LOOP0, END)
    for inst, vol, ch, pan in LAYOUT:
        ev = sorted([e[:4] for kind, e in kept if kind == 'n' and e[4] == inst])
        song.add(dedupe(ev), inst, vol, ch, pan)
    song.add(sorted(e[:4] for kind, e in kept if kind == 'd'), KIT, 88, 9)
    song.add(sq1, SQ1, 54, 10, 44)
    song.add(sq2, SQ2, 46, 11, 84)
    song.add(hats, NOISE, 28, 12, 64)
    song.save(OUT, END)
    print(OUT, '| intro %.1f s | loop %.1f s | totaal %.1f s' % (
        LOOP0 / TPB * 60 / BPM, (END - LOOP0) / TPB * 60 / BPM, END / TPB * 60 / BPM))


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('DP_MIDI', 'DialgaPalkiaMIDIBeta.mid')
    voicegroup()
    build(src)
