#!/usr/bin/env python3
"""Project Grounded: Battle! Pokémon Tower, een gevechtsremix van Lavender Town (FRLG MUS_RG_LAVENDER).

Jordi: "Hadden we al een battle theme voor alle gevechten in Pokemon Tower waar we Lavender Town geremixed hebben?"
MUS_GROUNDED_VS_POKE_TOWER = 687. Speelt bij elk gevecht in MAPSEC_POKEMON_TOWER (wild en trainers, ook Agatha).

Remixregel (MUZIEK.md): het origineel 1-op-1 (vorm, volgorde, noten van melodie/arpeggio/tegenlijnen), alleen
instrumenten wisselen en lagen toevoegen. Tempo 128 -> 160 bpm (de toonhoogtes en de 40-maats-vorm blijven).
  origineel (mus_rg_lavender.mid, tpb 24 -> hier 96: tick x 4)        remix
  intro 4 maten: alleen het arpeggio C-G-B-F#                         maat 1 chromatische 16en-val (strijkers +
                                                                     vierkant) + snareroffel, maat 2 tritonus-stoten
                                                                     (hoorn E4 + strijkers A#4 + bas), maat 3-4 het
                                                                     arpeggio met galopbas en drums
  A1  maat 0-7   melodie (orgel)                                      orgel (origineel instrument), half-time drums,
                                                                     galopbas
  A2  maat 8-15  melodie een octaaf hoger                             strijkers, drums vol (backbeat)
  B1  maat 16-19 melodie rust                                         hoorn-riff B-G-F# in 3+3+2, taiko/hyoushigi,
                                                                     atarigane-bel (zoals het origineel), tomroffel
  A3  maat 20-27 melodie (accordeon)                                  koor 'aah' (de geesten), drums vol
  A4  maat 28-35 melodie (accordeon)                                  trompet + strijkers unisono, 16en-hihats
  B2  maat 36-39 melodie rust                                         koor zakt chromatisch (E5-D#5-D5-C#5),
                                                                     half-time, tomroffel terug naar A1
Altijd: het arpeggio (origineel spoor 7) op PSG-vierkant 2, de 'jammerlijn' (spoor 5, melodie met chromatische
glijders) een octaaf hoger op PSG-vierkant 1, de chromatische fluitlijn (spoor 4) op de PSG-golf, hihats op PSG-ruis.
Alleen Emerald/FRLG-samples (geen eigen samples, geen ROM-kosten voor samples): orgel2, strijkers, koor, trompet,
hoorn, fingered bass; eigen kit drumsets/tower.inc (kick, snare, crash, toms, en de Japanse percussie van het
origineel: taiko, kotsuzumi, atarigane, hyoushigi).
Stemverdeler max. 10 DirectSound-noten (gewone trainer).
  python3 tools/grounded/tower_theme.py
Zie tools/grounded/MUZIEK.md."""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import notes_of, dedupe, detach, allocate, releases, release_ticks, Song

VG = 'grounded_tower'
OUT = 'sound/songs/midi/mus_grounded_vs_poke_tower.mid'
SRC = 'sound/songs/midi/mus_rg_lavender.mid'
MAXV = 10
TPB = 96
S = TPB // 4
BAR = TPB * 4
BPM = 160
INTRO = 4
LOOP_BARS = 40
SCALE = 4                     # origineel tpb 24 -> 96; de intro van het origineel is ook 4 maten, dus tick x 4 past

# programma's in voicegroup_grounded_tower
FBASS, ORGAN, STR, CHOIR, TPT, HORN = 33, 17, 48, 52, 56, 60
SQ1, SQ2, WAVE, NOISE, KIT = 80, 81, 84, 121, 127
NOISE_HAT = 84
# drumkit drumsets/tower.inc (vanaf 36)
KICK, SN, CRASH, TOM_L, TOM_M, TOM_H, TAIKO, KOTSU, BELL, HYOU = range(36, 46)
DLEN = {KICK: 2 * S, SN: 2 * S, CRASH: 4 * S, TOM_L: 2 * S, TOM_M: 2 * S, TOM_H: 2 * S, TAIKO: 4 * S,
        KOTSU: 2 * S, BELL: 4 * S, HYOU: S}

NN = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}


def p(name):
    return 12 * (int(name[-1]) + 1) + NN[name[:-1]]


def bt(b):
    """tick van loopmaat b (0 = eerste melodiemaat)."""
    return (INTRO + b) * BAR


def section(b):
    for name, lo, hi in (('A1', 0, 8), ('A2', 8, 16), ('B1', 16, 20), ('A3', 20, 28), ('A4', 28, 36),
                         ('B2', 36, 40)):
        if lo <= b < hi:
            return name
    return 'I'


def loopbar(tick):
    return tick // BAR - INTRO


class Parts(dict):
    def __missing__(self, k):
        self[k] = []
        return self[k]


def orig():
    m = mido.MidiFile(SRC)
    assert m.ticks_per_beat * SCALE == TPB
    return {i: [[s * SCALE, e * SCALE, n, v] for s, e, n, v in notes_of(t)] for i, t in enumerate(m.tracks)}


def drum(P, t0, steps, key, vel, part='drums'):
    for k in steps:
        P[part].append([t0 + k * S, t0 + k * S + DLEN[key], key, vel])


def roll(P, t0, st, n, key, v0, dv, part='drums'):
    for k in range(n):
        P[part].append([t0 + (st + k) * S, t0 + (st + k + 1) * S, key, min(127, v0 + dv * k)])


# grondtonen per maat (origineel spoor 3: E | D | C | E C B E, maat 15/31: E G F# B)
ROOT = {0: [p('E2')] * 4, 1: [p('D2')] * 4, 2: [p('C2')] * 4, 3: [p('E2'), p('C2'), p('B1'), p('E2')]}
ROOT_TURN = [p('E2'), p('G2'), p('F#2'), p('B2')]


def roots(b):
    if b in (15, 31):
        return ROOT_TURN
    return ROOT[b % 4]


def bass_bar(P, t0, rs, style, nxt):
    """galop (8e + twee 16en per tel), half (achtsten) of 332 (3+3+2, B-delen). nxt = eerste grondtoon van de
    volgende maat: de laatste 16e is een chromatische nadering van bovenaf."""
    if style == '332':
        for k in (0, 3, 6, 8, 11, 14):
            P['bass'].append([t0 + k * S, t0 + (k + 2) * S, rs[k // 4], 116 if k in (0, 8) else 100])
        return
    for beat in range(4):
        r = rs[beat]
        steps = ((0, 2, 116), (2, 1, 96), (3, 1, 100)) if style == 'gallop' else ((0, 2, 112), (2, 2, 98))
        for st, ln, v in steps:
            k = 4 * beat + st
            n = r
            if beat == 3 and k == 15 and nxt is not None and nxt != r:
                n = nxt + 1                    # glijdt van bovenaf de volgende grondtoon in (E -> D#-D)
            P['bass'].append([t0 + k * S, t0 + (k + ln) * S, n, v + (8 if beat in (0, 2) and st == 0 else 0)])


def build_parts():
    O = orig()
    P = Parts()
    CC = Parts()
    loop0 = bt(0)
    end = bt(LOOP_BARS)

    # ---- melodie (origineel spoor 1) per sectie op een ander instrument ----
    for s, e, n, v in O[1]:
        if s < loop0:
            continue
        sec = section(loopbar(s))
        vel = 112 if e - s > S else 96
        if sec == 'A1':
            P['organ'].append([s, e, n, vel])
        elif sec == 'A2':
            P['strings'].append([s, e, n, vel])
        elif sec == 'A3':
            P['choir'].append([s, e, n, vel])
        elif sec == 'A4':
            P['tpt'].append([s, e, n, vel])
            P['strings'].append([s, e, n, vel - 8])
    # ---- jammerlijn (origineel spoor 5) op vierkant 1: een octaaf hoger, in A2 twee ----
    for s, e, n, v in O[5]:
        sec = section(loopbar(s))
        P['sq1'].append([s, e, n + (24 if sec == 'A2' else 12), 100 if e - s > S else 80])
    # ---- chromatische fluitlijn (spoor 4) op de golf, arpeggio (spoor 7) op vierkant 2 ----
    P['wave'] = [[s, e, n, 100] for s, e, n, v in O[4]]
    P['arp'] = [[s, e, n, 76 if (s // (2 * S)) % 4 == 0 else 60] for s, e, n, v in O[7] if s >= 2 * BAR]

    # ---- intro ----
    for k in range(16):                       # maat 1: chromatische val E6 -> C#5 in 16en
        n = p('E6') - k
        P['strings'].append([k * S, (k + 1) * S, n, 92 + k])
        P['sq1'].append([k * S, (k + 1) * S, n - 12, 90])
    roll(P, 0, 0, 16, SN, 76, 3)
    t1 = BAR                                  # maat 2: tritonus-stoten E + A#
    for k, ln in ((0, 2), (3, 2), (6, 2), (8, 6)):
        P['horn'].append([t1 + k * S, t1 + (k + ln) * S, p('E4'), 120])
        P['strings'].append([t1 + k * S, t1 + (k + ln) * S, p('A#4'), 116])
        P['bass'].append([t1 + k * S, t1 + (k + ln) * S, p('E2'), 124])
        drum(P, t1, (k,), KICK, 124)
    drum(P, t1, (0,), CRASH, 120)
    drum(P, t1, (12, 13), TOM_H, 108)
    drum(P, t1, (14,), TOM_M, 112)
    drum(P, t1, (15,), TOM_L, 116)
    for i in (2, 3):                          # maat 3-4: arpeggio + galopbas + drums
        t0 = i * BAR
        bass_bar(P, t0, [p('E2')] * 4, 'gallop', p('E2'))
        drum(P, t0, (0, 10) if i == 2 else (0,), KICK, 120)
        drum(P, t0, (8,), SN, 112)
        drum(P, t0, (0,), TAIKO, 112)
        for k in range(0, 16, 2):
            P['hat'].append([t0 + k * S, t0 + k * S + 6, NOISE_HAT, 64 if k % 4 == 0 else 44])
    roll(P, 3 * BAR, 12, 4, SN, 96, 8)

    # ---- loop ----
    bells = [s for s, e, n, v in O[6]]
    for b in range(LOOP_BARS):
        t0 = bt(b)
        sec = section(b)
        nxt = roots((b + 1) % LOOP_BARS)[0]
        # bas
        if sec == 'B1' and b != 19:
            bass_bar(P, t0, roots(b), '332', nxt)
        else:
            bass_bar(P, t0, roots(b), 'gallop', nxt)
        # hoorn-riff in B1 (B-G-F# in 3+3+2, laatste maat het E-G-F#-B-figuur van het origineel)
        if sec == 'B1':
            if b < 19:
                up = 12 if b == 18 else 0
                for k, ln, nm in ((0, 3, 'B4'), (3, 3, 'G4'), (6, 2, 'F#4'), (8, 3, 'B4'), (11, 3, 'G4'),
                                  (14, 2, 'F#4')):
                    P['horn'].append([t0 + k * S, t0 + (k + ln) * S, p(nm) + up, 118 if k in (0, 8) else 108])
            else:
                for k, nm in ((0, 'E5'), (4, 'G5'), (8, 'F#5'), (12, 'B5')):
                    P['horn'].append([t0 + k * S, t0 + (k + 4) * S, p(nm), 118])
        # koor zakt chromatisch in B2 (in halve maten, laatste maat alleen de eerste helft)
        if sec == 'B2':
            n = p('E5') - (b - 36)
            for h in ((0, 1) if b < 39 else (0,)):
                P['choir'].append([t0 + h * 8 * S, t0 + (h + 1) * 8 * S - 6, n, 108])
        # drums
        if sec in ('A1', 'B2'):                   # half-time: kick 1 en 3-en, snare op 3
            drum(P, t0, (0, 10), KICK, 112)
            drum(P, t0, (8,), SN, 116)
            if b % 4 == 0:
                drum(P, t0, (0,), TAIKO, 110)
            hats = range(0, 16, 2)
        elif sec == 'B1':                         # Japanse percussie: taiko + hyoushigi, geen backbeat
            drum(P, t0, (0, 6, 10), TAIKO, 104)
            drum(P, t0, (4, 12), HYOU, 112)
            drum(P, t0, (14,), KOTSU, 104)
            hats = ()
        else:                                     # vol: kick 1, 2-en, 3; snare 2 en 4
            drum(P, t0, (0, 6, 8) if sec != 'A4' else (0, 6, 8, 14), KICK, 112)
            drum(P, t0, (4, 12), SN, 118)
            if b % 2 == 1 and sec != 'A4':
                drum(P, t0, (15,), SN, 84)
            hats = range(0, 16, 1) if sec == 'A4' else range(0, 16, 2)
        for k in hats:
            P['hat'].append([t0 + k * S, t0 + k * S + 6, NOISE_HAT, 64 if k % 4 == 0 else (44 if k % 2 == 0 else 34)])
        if b in (0, 8, 20, 28, 36):
            drum(P, t0, (0,), CRASH, 118)
        # fills aan het eind van elke frase
        if b in (7, 27):
            drum(P, t0, (12, 13), TOM_H, 108)
            drum(P, t0, (14,), TOM_M, 112)
            drum(P, t0, (15,), TOM_L, 116)
        if b in (15, 35):
            roll(P, t0, 8, 8, SN, 86, 5)
        if b == 19:
            for k, key in zip(range(8, 16), (TOM_H, TOM_H, TOM_M, TOM_M, TOM_L, TOM_L, SN, SN)):
                P['drums'].append([t0 + k * S, t0 + (k + 1) * S, key, 100 + 3 * (k - 8)])
        if b == 39:
            for k, key in zip(range(8, 16), (TOM_H, TOM_M, TOM_H, TOM_M, TOM_L, TOM_L, SN, SN)):
                P['drums'].append([t0 + k * S, t0 + (k + 1) * S, key, 100 + 3 * (k - 8)])
    # atarigane-bel van het origineel (spoor 6, maat 16-39 op tel 3)
    for s in bells:
        if s >= loop0:
            P['drums'].append([s, s + DLEN[BELL], BELL, 100])
    # geen drumnoten dubbel op één tick met dezelfde toets; op een crash geen hihat
    cr = {e[0] for e in P['drums'] if e[2] == CRASH}
    P['hat'] = [e for e in P['hat'] if e[0] not in cr]
    # een tomroffel/snareroffel vervangt de groove op dezelfde 16en
    fill = {(e[0]) for e in P['drums'] if e[2] in (TOM_H, TOM_M, TOM_L) or (e[2] == SN and e[1] - e[0] == S)}
    P['drums'] = [e for e in P['drums'] if not (e[0] in fill and e[2] in (KICK, TAIKO)
                                                and loopbar(e[0]) in (7, 15, 19, 27, 35, 39))]
    return P, CC, end


LAYOUT = [  # (partij, programma, volume, kanaal, pan)
    ('organ', ORGAN, 124, 0, 64),
    ('strings', STR, 104, 1, 72),
    ('choir', CHOIR, 104, 2, 56),
    ('tpt', TPT, 96, 3, 60),
    ('horn', HORN, 104, 4, 66),
    ('bass', FBASS, 88, 5, 64),
    ('sq1', SQ1, 46, 6, 52),
    ('arp', SQ2, 44, 7, 80),
    ('wave', WAVE, 48, 8, 64),
    ('hat', NOISE, 40, 10, 64),
]
ORDER = ['organ', 'strings', 'tpt', 'choir', 'drums', 'bass', 'horn']


def voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm + overrides voor Battle! Pokémon Tower (Lavender Town-remix).'
    lines[1] = '@ Gegenereerd door tools/grounded/tower_theme.py. Alleen stock-samples.'
    lines[2] = 'voice_group %s' % VG
    over = {
        17: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_organ2, 255, 127, 180, 150',
        33: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_fingered_bass, 255, 253, 0, 149',
        52: 'voice_directsound 60, 0, DirectSoundWaveData_classical_choir_voice_ahhs, 160, 0, 255, 165',
        80: 'voice_square_1 60, 0, 0, 2, 0, 1, 9, 1',
        81: 'voice_square_2 60, 0, 1, 0, 2, 5, 1',
        84: 'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_3, 0, 7, 15, 2',
        121: 'voice_noise_alt 60, 0, 0, 0, 1, 0, 0',
        127: 'voice_keysplit_all voicegroup_tower_drumset',
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
        ('38 crash', 'voice_directsound 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165'),
        ('39 tom laag', 'voice_directsound 45, 52, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180'),
        ('40 tom midden', 'voice_directsound 51, 64, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180'),
        ('41 tom hoog', 'voice_directsound 57, 76, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180'),
        ('42 taiko', 'voice_directsound 63, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180'),
        ('43 kotsuzumi', 'voice_directsound 64, 84, DirectSoundWaveData_ethnic_flavours_kotsuzumi, 255, 0, 255, 160'),
        ('44 atarigane', 'voice_directsound 60, 40, DirectSoundWaveData_ethnic_flavours_atarigane, 255, 0, 255, 180'),
        ('45 hyoushigi', 'voice_directsound 60, 88, DirectSoundWaveData_ethnic_flavours_hyoushigi, 255, 0, 255, 150'),
    ]
    open('sound/voicegroups/drumsets/tower.inc', 'w').write(
        '@ Project Grounded: drumkit voor tower_theme.py (Battle! Pokémon Tower). Alleen stock-samples, geen PSG.\n'
        '@ ' + ', '.join(n for n, _ in kit) + '.\n'
        '@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.\n'
        'voice_group tower_drumset, 36\n' + ''.join('\t%s\n' % v for _, v in kit))


def build():
    P, CC, end = build_parts()
    for k in list(P):
        P[k] = dedupe(P[k])
    progs = {k: pr for k, pr, *_ in LAYOUT}
    rel = releases(VG)
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) + 2 for k, pr in progs.items()}
    tail['drums'] = release_ticks(180, TPB, BPM) + 2
    for k, pr in progs.items():
        if rel.get(pr) is not None:
            P[k] = detach(P[k], tail[k])
            low = [n for _, _, n, _ in P[k] if n < 28]
            assert not low, '%s: DirectSound-noten onder E1 %s' % (k, low[:5])
            if pr in (TPT, HORN):
                bad = [n for _, _, n, _ in P[k] if n < 48]
                assert not bad, '%s: koper onder C3 %s' % (k, bad[:5])
            soft = [v for _, _, _, v in P[k] if v < 76]
            assert not soft, '%s: zachte DS-noten (8-bit-fuzz) %s' % (k, soft[:5])
    ds = {k: P[k] for k in ORDER}
    kept = allocate(ds, ORDER, tail, max_voices=MAXV)
    for k in ORDER:
        n = len(ds[k])
        if n and len(kept[k]) < n:
            lost = [e for e in ds[k] if e not in kept[k]]
            print('  %s: %d van %d noten vallen weg (%.1f%%), maten %s' % (
                k, len(lost), n, 100 * len(lost) / n, sorted({loopbar(e[0]) for e in lost})[:12]))
        P[k] = kept[k]
    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.loop = (bt(0), end)
    for k, pr, vol, ch, pan in LAYOUT:
        song.add(P[k], pr, vol, ch, pan, ccs=CC.get(k, []))
    song.add(sorted(P['drums']), KIT, 112, 9)
    written = {k for k, *_ in LAYOUT} | {'drums'}
    assert not [k for k in P if P[k] and k not in written]
    song.save(OUT, end)
    print(OUT, '| intro %.1f s | loop %.1f s | totaal %.1f s' % (
        bt(0) / TPB * 60 / BPM, (end - bt(0)) / TPB * 60 / BPM, end / TPB * 60 / BPM))


if __name__ == '__main__':
    voicegroup()
    build()
