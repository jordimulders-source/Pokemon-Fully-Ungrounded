#!/usr/bin/env python3
"""Project Grounded: Battle! Wild Pokémon (Route 119+), het wildthema op de landroutes vanaf Route 119.

Jordi (11 okt): "een nieuw gevechtsthema op alle land routes vanaf route 119. Deze moet grande klinken,
avontuurlijk. Gebruik de route 119 theme als inspiratie."

MUS_GROUNDED_VS_WILD_ROUTE119 = 711. Bron: sound/songs/midi/mus_route119.mid (136 bpm, A-groot, tpb 24, triolen-
gevoel). De melodieën komen noot voor noot uit het origineel (tick x 4 -> tpb 96, echo-noten op velocity 32 eruit):
  - het Route 119-motief (spoor 2, hoorn, maat -9..-2 van de intro: C#5 . E4-E4-E4 C#5 | E5 D5 C#5 E5 | D5 A4 |
    F-G-A G-A-B over A | G6 | D/F# | F-G, de Hoenn-chromatiek);
  - de tweede melodie (spoor 3, tuba/trompet, loopmaat 0-15, met de klim C6-C#6-D6 over E-F-F#7-G7);
  - het tweede deel (spoor 2, loopmaat 16-31: de loop E-F#-G#-A-B, het motief een halve toon lager in Ab, terug naar
    A met Hoenn-akkoorden C/Db/G6) en de tegenstem van spoor 2 onder de tweede melodie.
Akkoorden per halve maat uit de bas (spoor 8/9) + de zwaarste toonklassen van alle sporen. Alle begeleiding is nieuw
(MUZIEK.md: anti-kermis, geen tegenlijnen boven de melodie):
  - 176 bpm, het triolengevoel van het origineel blijft (galop: grondtoon op 1 en 'a' van elke tel), fingered bass in
    galop met chromatische opmaat, golf-sub;
  - koper: trompet-lead (stock trumpet-keysplit) met hoorns in tertsen/sexten eronder, hoorn-lead in B1; brede
    strijkers (stock string ensemble) een octaaf boven of onder de melodie + liggende strijkers;
  - pauken op 1 en 3 met roffels naar elke sectie, rock-kick/snare op 1/3 en 2/4, snareroffels in triolen,
    bekkens op de frasebegins, buisklokken op de climax (Ab-deel en de terugkeer van het motief);
  - PSG: alleen een zachte blokgolf-arpeggio in triolen ónder de melodie (B2, C2) en de golf-sub.
Vorm: intro 4 maten (E-pedaal, motiefkop op de dominant, F-G, E7 + de loop omhoog) | A motief (8) | B1 tweede melodie,
hoorn, half-time (8) | B2 trompet + strijkers, klim (8) | C1 loop + Ab-deel, strijkers zingen (7) | C2 tutti, motief
terug (9) -> loop naar A.
Eén voicegroup voicegroup_grounded_route119_battle (grounded_gm + overrides) en drumsets/route119_battle.inc,
alleen stock-Emerald-samples. Stemverdeler max. 10 DirectSound-noten.
  python3 tools/grounded/route119_battle_theme.py [--ref <map>]
Zie tools/grounded/MUZIEK.md."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import notes_of, dedupe, detach, allocate, releases, release_ticks, Song
import mido

SRC = 'sound/songs/midi/mus_route119.mid'
VG = 'grounded_route119_battle'
OUT = 'sound/songs/midi/mus_grounded_vs_wild_route119.mid'
MAXV = 10
BPM = 176
TPB = 96
S = TPB // 4          # 16e
T3 = TPB // 3         # triool-8e
BAR = TPB * 4
SC = 4                # tpb 24 -> 96
L0 = 912              # loopbegin van het origineel (tick, tpb 24)
SBAR = 96             # maat in het origineel

CH = {'A': (9, (9, 1, 4)), 'G6': (7, (7, 11, 2, 4)), 'D/F#': (6, (2, 6, 9)), 'F': (5, (5, 9, 0)),
      'G': (7, (7, 11, 2)), 'D': (2, (2, 6, 9)), 'Bm': (11, (11, 2, 6)), 'F#m': (6, (6, 9, 1)), 'E': (4, (4, 8, 11)),
      'E7': (4, (4, 8, 11, 2)), 'F#7': (6, (6, 10, 1, 4)), 'G7': (7, (7, 11, 2, 5)), 'Ab': (8, (8, 0, 3)),
      'Gb6': (6, (6, 10, 1, 3)), 'Gb': (6, (6, 10, 1)), 'Db': (1, (1, 5, 8)), 'Ebm7': (3, (3, 6, 10, 1)),
      'Ab7': (8, (8, 0, 3, 6)), 'Em/B': (11, (4, 7, 11)), 'C': (0, (0, 4, 7)), 'A/E': (4, (9, 1, 4))}

# programma's in voicegroup_grounded_route119_battle
BELL, FBASS, TROLL, TIMP, STR, TPT, HORN, KIT = 14, 33, 45, 47, 48, 56, 60, 127
SQ1, SQ2, WAVE = 80, 81, 84
# drumkit drumsets/route119_battle.inc (vanaf 36)
KICK, SNARE, CRASH, TOM_L, TOM_M, TOM_H, OSN, OCYM, TAIKO = range(36, 45)
# kanaalbezetting = lengte van de sample (gemeten, 176 bpm: 1 tick = 3,55 ms) of de uitklinktijd, niet ingekort
DLEN = {KICK: 60, SNARE: 2 * S, CRASH: 150, TOM_L: TPB, TOM_M: TPB, TOM_H: TPB, OSN: 2 * S, OCYM: 2 * TPB, TAIKO: 120}

# ---------------------------------------------------------------------------------------------------------------------
# vorm: (sectie, bronmaat (loopmaat van het origineel) of None, akkoord(en) per maat)
# ---------------------------------------------------------------------------------------------------------------------
INTRO = ['E', 'E', ('F', 'G'), 'E7']
A_PROG = ['A', 'G6', 'D/F#', ('F', 'G'), 'A', 'G6', 'D/F#', ('F', 'G')]
B_PROG = ['D', 'Bm', 'A', 'F#m', 'E', 'D', 'E', ('D', 'A'),
          'D', 'Bm', 'A', 'F#m', 'E', 'D', ('E', 'F'), ('F#7', 'G7')]
C_PROG = ['E7', 'Ab', 'Gb6', 'Db', ('Gb', 'Ebm7'), 'Ab', ('Gb', 'Ab7'),
          'A', 'G6', 'D/F#', ('Em/B', 'C'), 'Db', ('G6', 'A/E'), 'D/F#', ('F', 'G'), 'D']


def timeline():
    tl = [('I', i, None, c) for i, c in enumerate(INTRO)]
    tl += [('A', i, -9 + i, c) for i, c in enumerate(A_PROG)]
    tl += [('B1' if i < 8 else 'B2', i, i, c) for i, c in enumerate(B_PROG)]
    tl += [('C1' if i < 7 else 'C2', i, 16 + i, c) for i, c in enumerate(C_PROG)]
    return tl


def halves(c):
    return c if isinstance(c, tuple) else (c, c)


def tones(ch, lo, hi):
    return [m for m in range(lo, hi + 1) if m % 12 in CH[ch][1]]


def near(pc, lo):
    return lo + ((pc - lo) % 12)


class Parts(dict):
    def __missing__(self, k):
        self[k] = []
        return self[k]


# ---------------------------------------------------------------------------------------------------------------------
# bron
# ---------------------------------------------------------------------------------------------------------------------
_src = mido.MidiFile(SRC)


def src_notes(track, r0, r1, t0, pre=0):
    """noten van spoor `track` die beginnen in loopmaat [r0, r1) (+ `pre` bronticks opmaat ervoor), zonder echo's
    (velocity 32), naar tpb 96 en verschoven naar uitvoertick t0 (= begin van maat r0)."""
    a, b = L0 + r0 * SBAR, L0 + r1 * SBAR
    out = []
    for s, e, n, v in notes_of(_src.tracks[track]):
        if v <= 40 or not (a - pre <= s < b):
            continue
        out.append([t0 + (s - a) * SC, t0 + (min(e, b) - a) * SC, n, v])
    return out


def harmonize(notes, chord_at, lo=50, hi=72, gap=3):
    """hoorns onder de melodie: hoogste akkoordtoon minstens `gap` halve tonen eronder (tertsen/sexten)."""
    out = []
    for s, e, m, v in notes:
        if e - s < T3:                    # snelle noten (de E4-triolen, loopjes) niet harmoniseren
            continue
        cand = [n for n in tones(chord_at(s), lo, hi) if n <= m - gap]
        if cand:
            out.append([s, e, cand[-1], 104])
    return out


def drum(P, t0, offs, key, vel):
    for o in offs:
        P['drums'].append([t0 + o, t0 + o + DLEN[key], key, vel])


def troll3(P, t0, start, n, key, v0, dv, step=T3):
    for k in range(n):
        P['drums'].append([t0 + start + k * step, t0 + start + (k + 1) * step, key, min(127, v0 + dv * k)])


def bass_bar(P, t0, chs, nxt, vel, mode='gallop'):
    """galop: per tel grondtoon op de tel (2 triolen) + op de 'a' (laatste triool); octaaf op tel 2 en 4."""
    for h, ch in enumerate(chs):
        r = near(CH[ch][0], 33)                     # A1..G#2
        for k in range(2):
            tb = t0 + h * 2 * TPB + k * TPB
            last = h == 1 and k == 1
            if mode == 'half':
                if k == 0:
                    P['bass'].append([tb, tb + TPB + T3, r, vel + 8])
                else:
                    P['bass'].append([tb + 2 * T3, tb + TPB, r + 12, vel])
                continue
            P['bass'].append([tb, tb + 2 * T3 - 4, r, vel + (8 if k == 0 else 0)])
            n = r + 12 if k == 1 else r
            if last and nxt:
                nr = near(CH[nxt][0], 33)
                if nr != r:
                    n = nr - 1 if nr - 1 >= 33 else nr + 1          # chromatische opmaat
            P['bass'].append([tb + 2 * T3, tb + TPB, n, vel])


def timp_bar(P, t0, chs, vel, mode='ost'):
    for h, ch in enumerate(chs):
        hi = near(CH[ch][0], 41)
        lo = hi - 5
        tb = t0 + h * 2 * TPB
        if mode == 'ost':                   # grondtoon op 1/3, kwint eronder op de 'a' van tel 2/4
            P['timp'].append([tb, tb + TPB, hi, vel + 10])
            P['timp'].append([tb + TPB + 2 * T3, tb + 2 * TPB, lo, vel])
        elif mode == 'gallop':
            P['timp'].append([tb, tb + 2 * T3, hi, vel + 10])
            P['timp'].append([tb + 2 * T3, tb + TPB, hi, vel])
            P['timp'].append([tb + TPB, tb + TPB + 2 * T3, lo, vel + 4])
            P['timp'].append([tb + TPB + 2 * T3, tb + 2 * TPB, lo, vel])
        elif mode == 'hit' and h == 0:
            P['timp'].append([tb, tb + TPB, hi, vel + 10])


def timp_roll(P, t0, ch, start, n, v0, dv, step=T3):
    hi = near(CH[ch][0], 41)
    for k in range(n):
        P['troll'].append([t0 + start + k * step, t0 + start + (k + 1) * step, hi, min(127, v0 + dv * k)])


def pad(P, t0, chs, lo, hi, vel, part='strings2'):
    """liggende strijkers: één toon per halve maat (het sample is al een ensemble), zo dicht mogelijk bij de vorige."""
    for h, ch in enumerate(chs):
        cand = tones(ch, lo, hi)
        prev = P[part][-1][2] if P[part] else cand[len(cand) // 2]
        n = min(cand, key=lambda m: (abs(m - prev), m))
        P[part].append([t0 + h * 2 * TPB, t0 + (h + 1) * 2 * TPB, n, vel])


def arp_bar(P, t0, chs, lo, vel):
    """zachte blokgolf-arpeggio in triolen, onder de melodie."""
    for h, ch in enumerate(chs):
        ts = tones(ch, lo, lo + 14)[:4]
        pat = (0, 1, 2, 3, 2, 1)
        for k in range(6):
            s = t0 + h * 2 * TPB + k * T3
            P['sq'].append([s, s + T3, ts[pat[k] % len(ts)], vel])


def wave_bar(P, t0, chs):
    for h, ch in enumerate(chs):
        r = near(CH[ch][0], 36)
        P['wave'].append([t0 + h * 2 * TPB, t0 + (h + 1) * 2 * TPB, r, 100])


def compose():
    P = Parts()
    tl = timeline()
    halfs = []
    for _, _, _, c in tl:
        halfs += list(halves(c))

    def chord_at(t):
        return halfs[min(len(halfs) - 1, t // (2 * TPB))]

    start = {}
    for bi, (sec, i, r, c) in enumerate(tl):
        start.setdefault(sec, bi * BAR)
    # ---------------- melodieën uit de bron ----------------
    tA, tB1, tB2, tC1, tC2 = start['A'], start['B1'], start['B2'], start['C1'], start['C2']
    motif = src_notes(2, -9, -1, tA)                                   # Route 119-motief
    mel_b1 = src_notes(3, 0, 8, tB1, pre=12)                           # tweede melodie (met de E5-opmaat)
    mel_b2 = src_notes(3, 8, 16, tB2)
    cnt_b = src_notes(2, 0, 8, tB1) + src_notes(2, 8, 16, tB2)        # tegenstem van spoor 2 (vel 72)
    mel_c1 = src_notes(2, 16, 23, tC1)                                 # loop omhoog + Ab-deel
    mel_c2 = src_notes(2, 23, 32, tC2)                                 # motief terug, Hoenn-akkoorden
    # A: trompet + hoorns eronder + strijkers een octaaf hoger
    P['tpt'] += [[s, e, n, 112] for s, e, n, v in motif]
    P['horn'] += harmonize(motif, chord_at)
    P['strings'] += [[s, e, n + 12, 100] for s, e, n, v in motif if e - s >= T3]
    # B1: hoorn-lead (half-time), strijkers spelen de tegenstem van het origineel
    P['horn'] += [[s, e, n, 112] for s, e, n, v in mel_b1]
    P['strings'] += [[s, e, n, 96] for s, e, n, v in cnt_b if s < tB2]
    # B2: trompet-lead, strijkers een octaaf lager, hoorns harmoniseren
    P['tpt'] += [[s, e, n, 114] for s, e, n, v in mel_b2]
    P['strings'] += [[s, e, n - 12, 104] for s, e, n, v in mel_b2 if e - s >= T3]
    P['horn'] += harmonize(mel_b2, chord_at, lo=55, hi=74)
    # C1: de strijkers zingen (een octaaf hoger), hoorns op de melodie
    P['strings'] += [[s, e, n + 12, 108] for s, e, n, v in mel_c1 if e - s >= T3]
    P['sqrun'] += [[s, e, n, 90] for s, e, n, v in mel_c1 if e - s < T3]
    P['horn'] += [[s, e, n, 104] for s, e, n, v in mel_c1 if e - s >= T3]
    # C2: tutti
    P['tpt'] += [[s, e, n, 118] for s, e, n, v in mel_c2]
    P['_lead'] = motif + mel_b1 + mel_b2 + [[s, e, n + 12, v] for s, e, n, v in mel_c1] + mel_c2
    P['horn'] += harmonize(mel_c2, chord_at)
    P['strings'] += [[s, e, n + 12, 108] for s, e, n, v in mel_c2 if e - s >= T3]

    for bi, (sec, i, r, c) in enumerate(tl):
        t0 = bi * BAR
        chs = halves(c)
        nxt = halves(tl[bi + 1][3])[0] if bi + 1 < len(tl) else halves(A_PROG[0])[0]
        last = (bi + 1 == len(tl)) or tl[bi + 1][0] != sec
        # ---------------- intro ----------------
        if sec == 'I':
            if i == 0:
                P['strings2'] += [[t0, t0 + BAR, 52, 96]]
                timp_roll(P, t0, 'E', 0, 12, 80, 2)
            if i == 1:
                P['strings2'] += [[t0, t0 + BAR, 59, 100]]
                # motiefkop op de dominant: B4 . E4-E4-E4 B4 (koper in octaven)
                head = [(0, 32, 71), (32, 36, 64), (40, 44, 64), (48, 52, 64), (64, 88, 71)]
                for s, e, n in head:
                    P['tpt'].append([t0 + s * SC, t0 + e * SC, n, 110])
                    P['horn'].append([t0 + s * SC, t0 + e * SC, n - 12, 104])
                timp_bar(P, t0, chs, 96, 'ost')
            if i == 2:
                for h, (ch, top) in enumerate(((('F'), 77), ('G', 79))):
                    tb = t0 + h * 2 * TPB
                    P['tpt'].append([tb, tb + 2 * TPB - S, top, 112])
                    P['horn'].append([tb, tb + 2 * TPB - S, top - 8 if ch == 'F' else top - 7, 106])
                    P['strings2'].append([tb, tb + 2 * TPB, near(CH[ch][0], 53), 100])
                timp_bar(P, t0, chs, 100, 'ost')
            if i == 3:
                # E7-stoot, dan de loop Eb4-E-F#-G#-A-B (spoor 2, loopmaat 16) naar het motief
                P['tpt'].append([t0, t0 + TPB, 68, 114])
                P['horn'].append([t0, t0 + TPB, 62, 106])
                run = src_notes(2, 16, 17, t0)
                P['tpt'] += [[s, e, n, 110] for s, e, n, v in run]
                P['sqrun'] += [[s, e, n, 90] for s, e, n, v in run]          # loopje dubbelen op PSG (0 kanalen)
                timp_bar(P, t0, chs, 104, 'hit')
                timp_roll(P, t0, 'E', TPB + T3, 5, 90, 5)
                troll3(P, t0, 2 * TPB, 6, SNARE, 84, 6)
            if i >= 1:
                bass_bar(P, t0, chs, nxt if i == 3 else None, 104, 'half' if i < 3 else 'gallop')
            wave_bar(P, t0, chs)
            if i == 2:
                drum(P, t0, (0,), CRASH, 104)
                drum(P, t0, (0, 2 * TPB), TAIKO, 110)
            if i == 1:
                drum(P, t0, (0, 2 * TPB), TAIKO, 104)
            if i == 3:
                drum(P, t0, (0,), TAIKO, 114)
            continue
        # ---------------- strijkerspad ----------------
        if sec in ('A', 'C2'):
            pad(P, t0, chs, 50, 62, 96)
        elif sec == 'B1':
            pad(P, t0, chs, 50, 62, 92)
        elif sec in ('B2', 'C1'):
            pad(P, t0, chs, 52, 64, 96)
        # ---------------- bas, sub, PSG ----------------
        bass_bar(P, t0, chs, nxt, 106, 'half' if sec == 'B1' else 'gallop')
        wave_bar(P, t0, chs)
        if sec in ('B2', 'C2'):
            arp_bar(P, t0, chs, 52, 80)
        # ---------------- pauken ----------------
        if last:
            timp_bar(P, t0, chs, 104, 'hit')
            timp_roll(P, t0, chs[-1], 2 * TPB, 6, 90, 5)
        elif sec == 'B1':
            timp_bar(P, t0, chs, 96, 'hit')
        elif sec == 'C2' or (sec == 'B2' and i >= 14):
            timp_bar(P, t0, chs, 102, 'gallop')
        else:
            timp_bar(P, t0, chs, 100, 'ost')
        # ---------------- klokken ----------------
        if (sec == 'C1' and i == 1) or (sec == 'C2' and i in (7, 11)) or (sec == 'A' and i == 0):
            P['bell'].append([t0, t0 + 2 * TPB, near(CH[chs[0]][0], 64), 106])
        # ---------------- drums ----------------
        first = i == 0 or (sec == 'B2' and i == 8) or (sec == 'C2' and i == 7)
        if first or (sec in ('A', 'C2') and i in (4, 11)) or (sec == 'B2' and i in (14, 15)):
            drum(P, t0, (0,), CRASH, 114)
        if sec == 'C1' and i in (1, 4):
            drum(P, t0, (0,), OCYM, 110)
        if sec == 'B1':
            drum(P, t0, (0,), KICK, 112)
            drum(P, t0, (2 * TPB + 2 * T3,), KICK, 100)
            drum(P, t0, (2 * TPB,), SNARE, 104)
            if not last:
                continue
        if sec == 'C1' and i == 0:                  # E7-overgangsmaat: stoot, dan tomroffel in triolen
            drum(P, t0, (0,), TAIKO, 116)
            for k, key in enumerate((TOM_H, TOM_H, TOM_M, TOM_M, TOM_L, TOM_L)):
                drum(P, t0, (2 * TPB + k * T3,), key, 100 + 3 * k)
            P['tpt'].append([t0, t0 + TPB, 68, 114])
            P['horn'].append([t0, t0 + TPB, 62, 106])
            continue
        if sec != 'B1':
            drum(P, t0, (0, 2 * TPB), KICK, 114)
            drum(P, t0, (TPB + 2 * T3, 3 * TPB + 2 * T3), KICK, 98)           # galop-kick op de 'a'
            drum(P, t0, (TPB,) if last else (TPB, 3 * TPB), SNARE, 108)
            if i % 4 == 3 and not last:
                drum(P, t0, (3 * TPB + T3, 3 * TPB + 2 * T3), SNARE, 92)
        if last:
            troll3(P, t0, 2 * TPB, 6, SNARE, 88, 6)
    end = len(tl) * BAR
    return P, end, start


LAYOUT = [  # (partij, programma, volume, kanaal, pan)
    ('tpt', TPT, 104, 0, 64), ('horn', HORN, 96, 1, 54), ('strings', STR, 92, 2, 76), ('strings2', STR, 78, 3, 48),
    ('bass', FBASS, 104, 4, 64), ('timp', TIMP, 104, 5, 64), ('troll', TROLL, 96, 6, 64), ('bell', BELL, 78, 7, 72),
    ('sq', SQ1, 40, 8, 40), ('sqrun', SQ2, 44, 11, 88), ('wave', WAVE, 52, 10, 64),
]
ORDER = ['tpt', 'drums', 'horn', 'strings', 'bass', 'bell', 'timp', 'troll', 'strings2']
DRUMVOL = 108


def voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm + overrides voor het Route 119+-wildthema (MUS_GROUNDED_VS_WILD_ROUTE119).'
    lines[1] = '@ Gegenereerd door tools/grounded/route119_battle_theme.py. Alleen Emerald-samples (Hoenn-koper/-strijkers/-pauken).'
    lines[2] = 'voice_group %s' % VG
    over = {
        14: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_tubular_bell, 255, 216, 90, 200',
        33: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_fingered_bass, 255, 253, 0, 149',
        45: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 90',
        47: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 170',
        48: 'voice_keysplit voicegroup_strings_keysplit, keysplit_strings',
        56: 'voice_keysplit voicegroup_trumpet_keysplit, keysplit_trumpet',
        60: 'voice_keysplit voicegroup_french_horn_keysplit, keysplit_french_horn',
        80: 'voice_square_1 60, 0, 0, 2, 0, 1, 7, 1',
        81: 'voice_square_2 60, 0, 2, 0, 1, 7, 1',
        84: 'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_1, 0, 7, 15, 0',
        127: 'voice_keysplit_all voicegroup_route119_battle_drumset',
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
        ('39 tom laag', 'voice_directsound 45, 52, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 190'),
        ('40 tom midden', 'voice_directsound 51, 64, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 190'),
        ('41 tom hoog', 'voice_directsound 57, 76, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 190'),
        ('42 orkestsnare', 'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 200'),
        ('43 orkestbekken', 'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 216'),
        ('44 taiko', 'voice_directsound 57, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180'),
    ]
    open('sound/voicegroups/drumsets/route119_battle.inc', 'w').write(
        '@ Project Grounded: drumkit voor route119_battle_theme.py (Route 119+-wildthema). Alleen stock-samples, geen PSG.\n'
        '@ ' + ', '.join(n for n, _ in kit) + '.\n'
        '@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.\n'
        'voice_group route119_battle_drumset, 36\n' + ''.join('\t%s\n' % v for _, v in kit))


def anti_kermis(P):
    """MUZIEK.md: geen begeleiding (PSG, pad, bas) boven de klinkende melodienoot; geen hoempa-bas."""
    lead = sorted(P.pop('_lead'))

    def top(s):
        mel = [m[2] for m in lead if m[0] <= s < m[1]]
        return max(mel) if mel else 999
    n0 = len(P['sq'])
    P['sq'] = [e for e in P['sq'] if e[2] < top(e[0]) - 2]       # arpeggio blijft altijd onder de melodie
    if n0 > len(P['sq']):
        print('  sq: %d arpeggionoten onder de melodie weggelaten' % (n0 - len(P['sq'])))
    bad = 0
    for part in ('sq', 'strings2', 'bass', 'wave'):
        for s, e, n, v in P[part]:
            mel = [m for m in lead if m[0] <= s < m[1]]
            if mel and n > max(m[2] for m in mel):
                bad += 1
                print('  anti-kermis: %s noot %d op maat %.2f boven de melodie %d' % (part, n, s / BAR, max(m[2] for m in mel)))
    assert bad == 0, 'anti-kermis: %d begeleidingsnoten boven de melodie' % bad


def build(refdir=None):
    P, end, start = compose()
    for k in list(P):
        P[k] = sorted(dedupe([e for e in P[k] if e[0] < end]))
        for e in P[k]:
            e[1] = min(e[1], end)
    anti_kermis(P)
    cr = {e[0] for e in P['drums'] if e[2] in (CRASH, OCYM)}
    P['drums'] = [e for e in P['drums'] if not (e[2] == SNARE and e[0] in cr and e[3] < 95)]
    progs = {k: pr for k, pr, *_ in LAYOUT}
    rel = releases(VG)
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) + 2 for k, pr in progs.items()}
    for k, pr in progs.items():
        if rel.get(pr) is not None:
            P[k] = detach(P[k], tail[k])
    for k, pr in progs.items():
        if rel.get(pr) is not None:
            low = [n for _, _, n, _ in P[k] if n < 28]
            assert not low, '%s: DirectSound-noten onder E1: %s' % (k, low[:5])
            if pr in (TPT, HORN):
                bad = [n for _, _, n, _ in P[k] if n < 48]
                assert not bad, '%s: koper onder C3 %s' % (k, bad[:5])
            soft = [v for _, _, _, v in P[k] if v < 76]
            assert not soft, '%s: zachte DS-noten (8-bit-fuzz) %s' % (k, soft[:5])
        else:
            low = [n for _, _, n, _ in P[k] if n < 36]
            assert not low, '%s: PSG-noten onder C2' % k
    ds = {k: P[k] for k in ORDER}
    kept = allocate(ds, ORDER[:-1], tail, max_voices=MAXV)
    # liggende strijkers als laatste: kan een halve maat niet op de tel beginnen, dan een 8e/tel later (in plaats
    # van de hele halve maat weg te laten)
    busy = [(e[0], e[1] + tail.get(k, 0)) for k in ORDER[:-1] for e in kept[k]]
    pk = ORDER[-1]
    kept[pk] = []
    for s, e, n, v in ds[pk]:
        for off in (0, TPB // 2, TPB, 3 * TPB // 2):
            c = [s + off, e, n, v]
            if c[1] - c[0] < TPB // 2:
                break
            if allocate({'p': [c]}, ['p'], {'p': tail[pk]}, max_voices=MAXV, preset=busy)['p']:
                kept[pk].append(c)
                busy.append((c[0], c[1] + tail[pk]))
                if off:
                    print('  %s: maat %.2f een %d ticks later' % (pk, s / BAR, off))
                break
    for k in ORDER:
        n = len(ds[k])
        if n and len(kept[k]) < n:
            print('  %s: %d van %d noten vallen weg (%.1f%%)' % (k, n - len(kept[k]), n, 100 * (n - len(kept[k])) / n))
            if os.environ.get('R119_DEBUG'):
                kk = {tuple(e) for e in kept[k]}
                print('     weg op maat:', [round(e[0] / BAR, 2) for e in ds[k] if tuple(e) not in kk][:24])
        P[k] = kept[k]
    lp = start['A']
    for ref in (False, True):
        if ref and not refdir:
            continue
        song = Song(TPB, 500000)
        song.tempo(0, BPM / 120)
        song.loop = (lp, end)
        for k, pr, vol, ch, pan in LAYOUT:
            song.add(P[k], pr if not ref else (pr if pr < 80 else 80), vol, ch, pan)
        drums = sorted(P['drums'])
        if ref:
            gm = {KICK: 36, SNARE: 38, CRASH: 49, TOM_L: 41, TOM_M: 45, TOM_H: 48, OSN: 38, OCYM: 57, TAIKO: 35}
            drums = [[s, e, gm[n], v] for s, e, n, v in drums]
        song.add(drums, KIT if not ref else 0, DRUMVOL, 9)
        written = {k for k, *_ in LAYOUT} | {'drums'}
        assert not [k for k in P if P[k] and k not in written], [k for k in P if P[k] and k not in written]
        out = os.path.join(refdir, 'route119_battle_ref.mid') if ref else OUT
        song.save(out, end)
        if not ref:
            print(out, '| intro %.1f s | loop %.1f s | totaal %.1f s' % (
                lp / TPB * 60 / BPM, (end - lp) / TPB * 60 / BPM, end / TPB * 60 / BPM))


if __name__ == '__main__':
    ref = sys.argv[sys.argv.index('--ref') + 1] if '--ref' in sys.argv else None
    voicegroup()
    build(ref)
