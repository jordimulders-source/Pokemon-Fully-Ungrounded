#!/usr/bin/env python3
"""Project Grounded: drie eigen legendary-gevechtsthema's (originele composities in GBA-stijl, geen nabouw).

Jordi: "bedenk wat themes van Pokémon die we nog niet hebben". Ze vervangen de placeholder MUS_RG_VS_LEGEND.

1. Battle! Zacian & Zamazenta (Mega Forest)            MUS_GROUNDED_VS_ZACIAN = 684
   Ridderlijk en heroïsch, Galar: B-klein, 152 bpm. Twee motieven:
     ZWAARD (Zacian):  gestippelde B4 -> F#5 -> B5 (de slag omhoog), dan rondzwaaiend omlaag; trompet + strijkers.
     SCHILD (Zamazenta): brede halve noten die stapsgewijs dalen en blijven staan; hoorns + tuba, in D-groot.
   Begeleiding: galopperende strijkers (8e + twee 16en = ruiterij), marssnare, pauken, buisklokken.
   Vorm: intro 4 (snareroffel, hoornroep, zwaardkop) | A zwaard | A2 zwaard + galop + tegenmelodie |
         B schild (D-groot, strijkers spelen het zwaardritme eronder) | K duel (zwaardkop en schildkop als vraag en
         antwoord, wordt dichter) | C = zwaard een hele toon hoger (C#-klein, 'Crowned') met de schildlijn in de
         hoorns, koor en klokken; laatste maat terug op F# (dominant) -> loop naar A.
2. Battle! Xerneas & Yveltal (Glimwood Tangle)          MUS_GROUNDED_VS_XERNEAS = 685
   Leven en dood: één melodie in twee gedaanten, 168 bpm.
     LEVEN (Xerneas): E-GROOT, melodie in de strijkers met glockenspiel, harparpeggio's in 16en, tamboerijn.
     DOOD (Yveltal): dezelfde melodie in E-KLEIN (G#->G, C#->C, D#->D behalve op de dominant B), op distortion-
     gitaar met hoorns een octaaf lager, tuba, buisklok die luidt, zware half-time drums, vleugelslagen (PSG-ruis).
   Vorm: intro 4 (bloei -> plotseling klein) | L leven | L2 leven voller | S dood (half-time) | S2 dood (vol) |
         B wisseling per twee maten (groot/klein) | C de cirkel rond: groot op trompet, met de gitaar en het koor
         van de dood eronder -> loop naar L.
3. Battle! Uxie, Mesprit & Azelf (de meren in de Spacetime Cave)   MUS_GROUNDED_VS_LAKE_TRIO = 686
   Mysterieus, F#-klein, 144 bpm, akkoorden F#m-D-E-C#m-Bm-D-G(Napolitaans)-C#. Drie motieven die op hetzelfde
   akkoordschema passen en dus samen kunnen klinken:
     KENNIS (Uxie):     kristallen achtsten 3+3+2 op akkoordtonen (methodisch, een denkpatroon); glockenspiel + PSG.
     EMOTIE (Mesprit):  zingende lijn met zuchten (lange noot, twee achtsten omlaag); hobo + strijkers.
     WILSKRACHT (Azelf): ritmische fanfare die elke maat hoger klimt (gestippeld, herhaalde noten); trompet + hoorns.
   Vorm: intro 4 (rimpelend water op de PSG-golf, paukenroffel) | A kennis | B emotie | C wilskracht |
         D de drie samen | D2 samen + vol | E break (elk motief één maat, dan C#) -> loop naar A.

Alleen Emerald-samples (geen eigen samples, dus geen ROM-kosten voor samples). Eén voicegroup voicegroup_grounded_legends3
(grounded_gm + overrides), keysplits/legends3_spicc.inc en drumsets/legends3.inc (alle drums als voice_directsound op
een vaste toets: speelt op de rate van de sample, niet op de mixersnelheid zoals _no_resample).
Klank (hoofdsessie, 10 okt): de mixer rondt elk kanaal na het volume af op 8 bit, dus zachte, zuivere DirectSound-
stemmen 'fuzzen'. Daarom: geen fluit, DS-velocities >= 76, sub-bas op de PSG-golf, DS-bas niet onder C2, lichte
zuivere figuren (Uxie, rimpelingen) op PSG.
Stemverdeler max. 11 DirectSound-noten (legendary).
  python3 tools/grounded/legends3_theme.py [--ref <map>]     (--ref: FluidR3-referentie-MIDI's met octaafcorrecties)
Zie tools/grounded/MUZIEK.md."""
import math, os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

VG = 'grounded_legends3'
MAXV = 11
TPB = 96
S = TPB // 4                  # een 16e
BAR = TPB * 4

N = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'E#': 5, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8,
     'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11, 'B#': 0}


def p(name):
    n = 12 * (int(name[-1]) + 1) + N[name[:-1]]
    return n + 12 if name[:-1] == 'B#' else n


CH = {'Bm': (11, (11, 2, 6)), 'G': (7, (7, 11, 2)), 'D': (2, (2, 6, 9)), 'A': (9, (9, 1, 4)), 'Em': (4, (4, 7, 11)),
      'F#': (6, (6, 10, 1)), 'F#m': (6, (6, 9, 1)), 'G#': (8, (8, 0, 3)), 'E': (4, (4, 8, 11)),
      'B': (11, (11, 3, 6)), 'C#m': (1, (1, 4, 8)), 'Am': (9, (9, 0, 4)), 'C': (0, (0, 4, 7)), 'C#': (1, (1, 5, 8))}

# programma's in voicegroup_grounded_legends3
GLOCK, BELL, DIST_HI, FBASS, HARP, TIMP, STR, SPICC, CHOIR, TPT, TUBA, HORN, OBOE, KIT = \
    9, 14, 30, 33, 46, 47, 48, 49, 52, 56, 58, 60, 64, 127
SQ1, SQ2, WAVE, NOISE = 80, 81, 84, 121
TROLL = 45                    # pauk met korte release (roffels; 16en op de gewone pauk bezetten 3 kanalen)
# drumkit drumsets/legends3.inc (vanaf 36)
KICK, OSN, SN, TOM_L, TOM_M, TOM_H, CRASH, CRASH2, HH, TAMB, TAIKO, OHH = range(36, 48)
DLEN = {KICK: 2 * S, OSN: 3 * S, SN: 3 * S, TOM_L: 2 * S, TOM_M: 2 * S, TOM_H: 2 * S, CRASH: TPB,
        CRASH2: TPB, HH: S, TAMB: S, TAIKO: TPB, OHH: 2 * S}


def near(pc, lo):
    return lo + ((pc - lo) % 12)


def tones(name, lo, hi):
    return [m for m in range(lo, hi + 1) if m % 12 in CH[name][1]]


class Parts(dict):
    def __missing__(self, k):
        self[k] = []
        return self[k]


def mel(pat, t0, vel, tr=0, oct=0):
    return [[t0 + st * S, t0 + (st + ln) * S, p(n) + tr + 12 * oct, vel] for st, ln, n in pat]


def drum(P, t0, steps, key, vel, part='drums'):
    for k in steps:
        P[part].append([t0 + k * S, t0 + k * S + DLEN[key], key, vel])


def roll(P, t0, st, n, key, v0, dv, part='drums'):
    """roffel in 16en (snare/toms), crescendo."""
    for k in range(n):
        P[part].append([t0 + (st + k) * S, t0 + (st + k) * S + S, key, min(127, v0 + dv * k)])


def gust(P, CC, EX, name, t0, length, key, vmax, wobble=5, seed=0, down=False):
    """vleugelslag/wind op het PSG-ruisspoor: één noot, CC7 zwelt aan en af, pitch bend (BENDR 12)."""
    P[name].append([t0, t0 + length, key, 110])
    steps = max(2, length // S)
    for k in range(steps + 1):
        x = k / steps
        CC[name].append((t0 + k * S, 7, int(8 + vmax * math.sin(math.pi * min(1.0, x)) ** 1.5)))
        semis = (-12 * x) if down else wobble * math.sin(2 * math.pi * (x * 1.5 + seed * 0.37))
        EX[name].append((t0 + k * S, mido.Message('pitchwheel', pitch=max(-8192, min(8191, int(semis / 12 * 8191))))))


def counter_line(bars, lo, hi, vel, unit=8):
    """tegenstem: per `unit` 16en een akkoordtoon in lo..hi, zo dicht mogelijk bij de vorige (niet 3x dezelfde).
    bars: [(t0, akkoord, tr)]"""
    out, prev, same = [], None, 0
    for t0, ch, tr in bars:
        for h in range(0, 16, unit):
            cand = [m + tr for m in tones(ch, lo - tr, hi - tr)]
            if prev is None:
                n = cand[len(cand) // 2]
            else:
                cand.sort(key=lambda m: (abs(m - prev), m))
                n = cand[0]
                if n == prev:
                    same += 1
                    if same >= 2 and len(cand) > 1:
                        n, same = cand[1], 0
                else:
                    same = 0
            out.append([t0 + h * S, t0 + (h + unit) * S - 8, n, vel])
            prev = n
    return out


def pad(P, key, t0, ch, lo, hi, n, vel, tr=0, half=True):
    """liggend akkoord (bovenste n akkoordtonen in lo..hi), in halve maten (lange noten in stukken)."""
    ts = [m + tr for m in tones(ch, lo, hi)][-n:]
    for h in ((0, 8) if half else (0,)):
        ln = 8 if half else 16
        P[key] += [[t0 + h * S, t0 + (h + ln) * S - 8, m, vel] for m in ts]


def gallop(P, key, t0, ch, lo, vel, tr=0):
    """ruiterij: per tel 8e + twee 16en op een akkoordtoon (grondtoon, terts, kwint, terts)."""
    ts = tones(ch, lo, lo + 14)
    for b in range(4):
        n = ts[(0, 1, 2, 1)[b] % len(ts)] + tr
        for st, ln, acc in ((0, 2, 16), (2, 1, 0), (3, 1, 4)):
            k = 4 * b + st
            P[key].append([t0 + k * S, t0 + (k + ln) * S, n, vel + acc])


def bass8(P, t0, ch, vel, tr=0, pat=(0, 0, 12, 0, 7, 0, 12, 0), lo=38):
    r = near(CH[ch][0] + tr, lo)
    for k in range(8):
        P['bass'].append([t0 + 2 * k * S, t0 + 2 * k * S + 2 * S - 6, r + pat[k], vel + (12 if k % 4 == 0 else 0)])


# =====================================================================================================================
# 1. Zacian & Zamazenta
# =====================================================================================================================
Z_PROG = {'I': ['Bm', 'Bm', 'G', 'F#'],
          'A': ['Bm', 'G', 'D', 'A', 'Bm', 'G', 'Em', 'F#'],
          'B': ['D', 'A', 'Bm', 'F#m', 'G', 'D', 'Em', 'A'],
          'K': ['Bm', 'Bm', 'G', 'G', 'Em', 'Em', 'F#', 'G#']}
Z_PROG['C'] = Z_PROG['A']
SWORD = [
    [(0, 3, 'B4'), (3, 1, 'F#5'), (4, 4, 'B5'), (8, 2, 'A5'), (10, 2, 'F#5'), (12, 2, 'D5'), (14, 2, 'F#5')],
    [(0, 6, 'G5'), (6, 2, 'F#5'), (8, 4, 'E5'), (12, 4, 'D5')],
    [(0, 3, 'A4'), (3, 1, 'F#5'), (4, 4, 'A5'), (8, 2, 'G5'), (10, 2, 'F#5'), (12, 2, 'D5'), (14, 2, 'F#5')],
    [(0, 8, 'E5'), (8, 4, 'C#5'), (12, 4, 'A4')],
    [(0, 3, 'B4'), (3, 1, 'F#5'), (4, 4, 'B5'), (8, 2, 'A5'), (10, 2, 'F#5'), (12, 2, 'D5'), (14, 2, 'F#5')],
    [(0, 6, 'B5'), (6, 2, 'A5'), (8, 4, 'G5'), (12, 4, 'B5')],
    [(0, 4, 'G5'), (4, 4, 'E5'), (8, 4, 'F#5'), (12, 4, 'G5')],
    [(0, 12, 'F#5'), (12, 2, 'E5'), (14, 2, 'C#5')],
]
SHIELD = [
    [(0, 8, 'A4'), (8, 4, 'F#4'), (12, 4, 'D4')],
    [(0, 12, 'E4'), (12, 4, 'A4')],
    [(0, 8, 'F#4'), (8, 4, 'D4'), (12, 4, 'F#4')],
    [(0, 8, 'A4'), (8, 8, 'C#5')],
    [(0, 8, 'B4'), (8, 4, 'G4'), (12, 4, 'D4')],
    [(0, 12, 'A4'), (12, 4, 'F#4')],
    [(0, 4, 'G4'), (4, 4, 'B4'), (8, 4, 'E5'), (12, 4, 'D5')],
    [(0, 16, 'C#5')],
]
DUEL_TPT = {0: [(0, 3, 'B4'), (3, 1, 'F#5'), (4, 6, 'B5')], 2: [(0, 3, 'B4'), (3, 1, 'D5'), (4, 6, 'G5')],
            4: [(0, 3, 'B4'), (3, 1, 'E5'), (4, 6, 'G5')],
            6: [(0, 3, 'C#5'), (3, 1, 'F#5'), (4, 4, 'A#5'), (8, 8, 'C#6')],
            7: [(0, 4, 'D#5'), (4, 4, 'G#5'), (8, 8, 'B#5')]}
DUEL_HORN = {1: [(0, 4, 'F#4'), (4, 4, 'D4'), (8, 8, 'B3')], 3: [(0, 4, 'D4'), (4, 4, 'B3'), (8, 8, 'G3')],
             5: [(0, 4, 'E4'), (4, 4, 'B3'), (8, 8, 'G3')], 6: [(0, 8, 'F#4'), (8, 8, 'A#4')],
             7: [(0, 8, 'G#4'), (8, 8, 'B#4')]}


def zacian():
    P, CC, EX = Parts(), Parts(), Parts()
    plan = [('I', 4), ('A', 8), ('A2', 8), ('B', 8), ('K', 8), ('C', 8)]
    tl = []
    for sec, n in plan:
        for i in range(n):
            tl.append((len(tl), sec, i))
    cbars = []
    for b, sec, i in tl:
        t0 = b * BAR
        prog = Z_PROG[sec[0]]
        ch = prog[i]
        tr = 2 if (sec == 'C' and i < 7) else 0
        r = CH[ch][0] + tr
        if sec == 'I':
            if i == 0:
                roll(P, t0, 0, 32, OSN, 72, 2)                      # snareroffel over twee maten
                P['timp'] += [[t0 + k * S, t0 + (k + 1) * S, p('B2'), 76 + k] for k in range(32)]
                P['horn'].append([t0, t0 + 8 * S - 8, p('B3'), 96])
                P['horn'].append([t0 + 8 * S, t0 + 16 * S - 8, p('F#4'), 104])
                P['pad'] += [[t0, t0 + 16 * S - 8, m, 84] for m in (p('B3'), p('F#4'))]
            if i == 1:
                P['horn'] += mel([(0, 8, 'B4'), (8, 4, 'A4'), (12, 4, 'F#4')], t0, 108)
                P['pad'] += [[t0, t0 + 16 * S - 8, m, 88] for m in (p('D4'), p('B4'))]
            if i == 2:
                P['tpt'] += mel([(0, 3, 'B4'), (3, 1, 'F#5'), (4, 8, 'B5'), (12, 2, 'A5'), (14, 2, 'G5')], t0, 120)
                P['strings'] += mel([(0, 3, 'B4'), (3, 1, 'F#5'), (4, 8, 'B5')], t0, 100)
                drum(P, t0, (0,), CRASH, 112)
                drum(P, t0, (0, 8), KICK, 116)
                P['timp'] += [[t0, t0 + 2 * S, p('G2'), 120], [t0 + 8 * S, t0 + 10 * S, p('D3'), 108]]
                pad(P, 'pad', t0, ch, p('D4'), p('B4'), 2, 90)
            if i == 3:     # F#: strijkersloop omhoog naar de B van maat 1, toms
                sc = [p(x) for x in ('F#4', 'G4', 'A4', 'B4', 'C#5', 'D5', 'E5', 'F#5', 'G5', 'A5', 'A#5', 'B5')]
                P['spicc'] += [[t0 + (4 + k) * S, t0 + (5 + k) * S, sc[k], 92 + 2 * k] for k in range(12)]
                P['tpt'] += mel([(0, 4, 'F#5'), (4, 4, 'C#5')], t0, 110)
                roll(P, t0, 8, 8, TOM_M, 96, 4)
                P['drums'][-8:] = [[s, s + DLEN[TOM_M], (TOM_H, TOM_H, TOM_M, TOM_M, TOM_L, TOM_L, SN, SN)[k], v]
                                   for k, (s, e, n, v) in enumerate(P['drums'][-8:])]
                P['timp'].append([t0, t0 + 2 * S, p('F#2') + 12, 116])
                P['bass'].append([t0, t0 + 8 * S - 6, near(6, 38), 112])
            P['wave'].append([t0, t0 + BAR - 8, near(r, 36), 60])
            continue
        # ---- melodie / motieven ----
        if sec in ('A', 'A2', 'C'):
            P['tpt'] += mel(SWORD[i], t0, 120 if sec != 'A' else 116, tr)
            if sec != 'A':
                P['strings'] += mel(SWORD[i], t0, 104, tr)
            if sec == 'C':      # de schildlijn als tegenstem (hoorns, halve noten), zie onder
                cbars.append((t0, ch, tr))
        elif sec == 'B':
            P['horn'] += mel(SHIELD[i], t0, 116)
            P['tuba'] += mel(SHIELD[i], t0, 104, oct=-1)
            if i >= 4:          # trompet geeft het schild de tweede helft glans: zwaardkop op de tel
                P['tpt'] += mel([(4, 3, 'D5'), (7, 1, 'F#5'), (8, 4, 'A5')], t0, 104) if i == 5 else []
        elif sec == 'K':
            if i in DUEL_TPT:
                P['tpt'] += mel(DUEL_TPT[i], t0, 122)
            if i in DUEL_HORN:
                P['horn'] += mel(DUEL_HORN[i], t0, 118)
        # ---- harmonie ----
        if sec == 'A':
            pad(P, 'pad', t0, ch, p('F#3'), p('D4') + 2, 2, 86, tr)
        if sec in ('A2', 'C'):
            gallop(P, 'spicc', t0, ch, p('B3'), 88, tr)
        if sec == 'B':          # strijkers spelen het zwaardritme (3+1+4) op akkoordtonen, galop eronder
            ts = tones(ch, p('D5'), p('D6'))
            P['strings'] += [[t0 + st * S, t0 + (st + ln) * S, ts[min(len(ts) - 1, j)], 98]
                             for st, ln, j in ((0, 3, 0), (3, 1, 1), (4, 4, 2), (8, 8, 1))]
            gallop(P, 'spicc', t0, ch, p('A3'), 84)
            pad(P, 'choir', t0, ch, p('F#4'), p('D5'), 1, 88)
        if sec == 'K':          # duel: spiccato 16en in de lage ligging, steeds hoger
            base = near(CH[ch][0], p('B3') if i < 4 else p('E4'))
            pat = (0, 7, 12, 7) if i < 6 else (0, 4, 7, 12)
            P['spicc'] += [[t0 + k * S, t0 + k * S + S, base + pat[k % 4], 84 + (14 if k % 4 == 0 else 0) + 2 * i]
                           for k in range(16)]
            if i >= 6:
                pad(P, 'choir', t0, ch, p('F#4'), p('D5') + 1, 2, 92)
        if sec == 'C':
            pad(P, 'choir', t0, ch, p('F#4'), p('E5'), 2, 92, tr)
            if i in (0, 4):
                P['bell'].append([t0, t0 + 6 * S, near(r, 71), 100])
        # ---- bas, tuba, pauken ----
        if sec == 'K':
            bass8(P, t0, ch, 98, 0, pat=(0, 0, 0, 0, 0, 0, 12, 12) if i < 6 else (0, 12, 0, 12, 0, 12, 0, 12))
        elif sec == 'B':
            bass8(P, t0, ch, 96, 0, pat=(0, 0, 7, 0, 12, 0, 7, 0))
        else:
            bass8(P, t0, ch, 100 if sec != 'A' else 96, tr)
        P['wave'].append([t0, t0 + BAR - 8, near(r, 36), 68])
        if sec == 'A2':
            P['tuba'] += [[t0, t0 + 8 * S - 8, near(r, 48), 100], [t0 + 8 * S, t0 + 16 * S - 8, near(r + 7, 48), 96]]
        tq = near(r, 38) + (12 if near(r, 38) < p('F2') else 0)
        P['timp'].append([t0, t0 + 2 * S, tq, 118])
        if sec != 'K' or i % 2 == 0:
            q = near(r + 7, 38)
            P['timp'].append([t0 + 8 * S, t0 + 10 * S, q + (12 if q < p('F2') else 0), 104])
        # ---- drums: mars ----
        if sec == 'K' and i < 6:       # half-time duel: kick 1, snare 3, zwaardslag (crash) bij elke trompetroep
            drum(P, t0, (0, 10), KICK, 118)
            drum(P, t0, (8,), SN, 118)
            drum(P, t0, (12, 14, 15), OSN, 92)
            if i in DUEL_TPT:
                drum(P, t0, (0,), CRASH2, 108)
        elif sec == 'K':               # opbouw naar C: roffel + toms
            drum(P, t0, (0, 4, 8, 12), KICK, 116)
            roll(P, t0, 0, 16, OSN, 70 + 10 * (i - 6), 3)
            if i == 7:
                P['timp'] += [[t0 + (8 + k) * S, t0 + (9 + k) * S, p('G#2'), 80 + 5 * k] for k in range(8)]
        else:
            kicks = (0, 8) if sec == 'A' else (0, 6, 8, 14)
            drum(P, t0, kicks, KICK, 116)
            drum(P, t0, (4, 12), SN, 114)
            if sec != 'A':          # galopperende ghost-snares op de 16en vóór de tel
                drum(P, t0, (3, 7, 11), OSN, 82)
            if sec in ('A2', 'C', 'B'):
                drum(P, t0, range(0, 16, 2), HH, 84)
            if i % 4 == 0:
                drum(P, t0, (0,), CRASH, 116 if sec == 'C' else 106)
            if i == 7:              # fill
                drum(P, t0, (12, 13), TOM_H, 104)
                drum(P, t0, (14,), TOM_L, 112)
    # C: de schildlijn als tegenstem in de hoorns (halve noten, steeds dichtbij)
    P['horn'] += counter_line(cbars, p('D4'), p('A4') + 2, 112)
    end = len(tl) * BAR
    return dict(parts=P, cc=CC, ex=EX, end=end, loop=4, bpm=152,
                order=['tpt', 'horn', 'drums', 'bell', 'bass', 'spicc', 'timp', 'choir', 'strings', 'tuba', 'pad'],
                layout=[('tpt', TPT, 100, 0, 70), ('horn', HORN, 100, 1, 56), ('tuba', TUBA, 88, 2, 60),
                        ('bass', FBASS, 104, 3, 64), ('timp', TROLL, 104, 4, 64), ('spicc', SPICC, 110, 5, 44),
                        ('strings', STR, 88, 6, 84), ('pad', STR, 80, 7, 52), ('choir', CHOIR, 84, 8, 76),
                        ('bell', BELL, 80, 10, 88), ('wave', WAVE, 56, 11, 64)],
                drums=('drums',), drumvol=118)


# =====================================================================================================================
# 2. Xerneas & Yveltal
# =====================================================================================================================
X_PROG = {'I': ['E', 'E', 'Em', 'B'],
          'L': ['E', 'A', 'E', 'B', 'C#m', 'F#m', 'B', 'E'],
          'S': ['Em', 'Am', 'Em', 'B', 'C', 'Am', 'B', 'Em'],
          'B': ['E', 'A', 'Em', 'Am', 'C#m', 'B', 'C', 'B']}
X_PROG['C'] = X_PROG['L']
LIFE = [
    [(0, 6, 'E5'), (6, 2, 'F#5'), (8, 4, 'G#5'), (12, 4, 'B5')],
    [(0, 12, 'A5'), (12, 2, 'G#5'), (14, 2, 'F#5')],
    [(0, 6, 'G#5'), (6, 2, 'A5'), (8, 4, 'B5'), (12, 4, 'E6')],
    [(0, 8, 'D#6'), (8, 8, 'B5')],
    [(0, 6, 'C#6'), (6, 2, 'B5'), (8, 4, 'A5'), (12, 4, 'G#5')],
    [(0, 4, 'F#5'), (4, 4, 'G#5'), (8, 4, 'A5'), (12, 4, 'C#6')],
    [(0, 6, 'B5'), (6, 2, 'A5'), (8, 4, 'G#5'), (12, 4, 'F#5')],
    [(0, 16, 'E5')],
]
B_FRAG = [(0, 'L'), (1, 'L'), (0, 'S'), (1, 'S'), (4, 'L'), (6, 'L'), (4, 'S'), (3, 'L')]   # B: (frase, gedaante)


def to_death(notes, ch):
    """dezelfde melodie in E-klein: G#->G, C#->C, D#->D (op de dominant B blijven D# en F# staan)."""
    out = []
    for s, e, n, v in notes:
        pc = n % 12
        if pc == 8 or pc == 1 or (pc == 3 and ch != 'B'):
            n -= 1
        out.append([s, e, n, v])
    return out


def xerneas():
    P, CC, EX = Parts(), Parts(), Parts()
    plan = [('I', 4), ('L', 8), ('L2', 8), ('S', 8), ('S2', 8), ('B', 8), ('C', 8)]
    tl = []
    for sec, n in plan:
        for i in range(n):
            tl.append((len(tl), sec, i))
    for b, sec, i in tl:
        t0 = b * BAR
        ch = X_PROG[sec[0]][i]
        r = CH[ch][0]
        mode = 'S' if sec[0] == 'S' else ('L' if sec[0] in 'LC' else ('S' if ch in ('Em', 'Am', 'C') else 'L'))
        if sec == 'B':
            mode = B_FRAG[i][1] if i != 7 else 'L'
        if sec == 'I':
            if i in (0, 1):    # bloei: harp-arpeggio omhoog, glockenspiel-sterretjes
                ts = tones('E', p('E4'), p('E6'))
                P['harp'] += [[t0 + k * S, t0 + k * S + S, ts[(k + 8 * i) % len(ts)], 84 + 2 * k] for k in range(16)]
                P['glock'] += [[t0 + 8 * S, t0 + 12 * S, p('B5') + 5 * i, 96], [t0 + 12 * S, t0 + 16 * S, p('E6'), 92]]
                pad(P, 'pad', t0, 'E', p('G#3'), p('E4') + 4, 2, 84)
                P['wave'].append([t0, t0 + BAR - 8, p('E2'), 52])
            if i == 2:         # de dood valt in: klok, pauk, koor laag, vleugelslag
                P['bell'].append([t0, t0 + 12 * S, p('E4'), 110])
                P['timp'] += [[t0, t0 + 2 * S, p('E3'), 124]]
                drum(P, t0, (0,), CRASH2, 116)
                drum(P, t0, (0,), TAIKO, 120)
                P['choir'] += [[t0, t0 + 16 * S - 8, m, 96] for m in (p('E4'), p('G4'), p('B4'))]
                P['low'] += [[t0, t0 + 16 * S - 8, p('E3'), 104]]
                gust(P, CC, EX, 'wing', t0 + 4 * S, 12 * S, 60, 90, wobble=3, seed=2)
                P['wave'].append([t0, t0 + BAR - 8, p('E2'), 70])
            if i == 3:         # B: gitaarstoot + roffel
                P['lead_d'] += mel([(0, 6, 'B4'), (8, 6, 'D#5'), (14, 2, 'F#5')], t0, 116)
                P['low'] += [[t0, t0 + 6 * S, p('B2') + 12, 104], [t0 + 8 * S, t0 + 14 * S, p('F#3'), 104]]
                roll(P, t0, 0, 16, OSN, 72, 4)
                P['timp'] += [[t0 + (8 + k) * S, t0 + (9 + k) * S, p('B2'), 80 + 5 * k] for k in range(8)]
                P['wave'].append([t0, t0 + BAR - 8, p('B2'), 70])
            continue
        # ---- melodie ----
        if sec in ('L', 'L2'):
            m = mel(LIFE[i], t0, 104 if sec == 'L' else 110)
            P['lead_l'] += m
            P['glock'] += [[s, min(e, s + 4 * S), n, 92] for s, e, n, v in m if (s - t0) % (4 * S) == 0]
        elif sec in ('S', 'S2'):
            m = to_death(mel(LIFE[i], t0, 118), ch)
            P['lead_d'] += [[s, e, n - 12, v] for s, e, n, v in m]          # gitaar een octaaf lager, duister
            P['low'] += [[s, e, n - 24, 108] for s, e, n, v in m]           # hoorns nog een octaaf lager
        elif sec == 'B':
            k, form = B_FRAG[i]
            m = mel(LIFE[k], t0, 112)
            if i == 7:
                P['lead_l'] += m
                P['lead_d'] += [[s, e, n - 12, 116] for s, e, n, v in m]
            elif form == 'L':
                P['lead_l'] += m
                P['glock'] += [[s, min(e, s + 4 * S), n, 92] for s, e, n, v in m if (s - t0) % (4 * S) == 0]
            else:
                m = to_death(m, ch)
                P['lead_d'] += [[s, e, n - 12, 118] for s, e, n, v in m]
                P['low'] += [[s, e, n - 24, 106] for s, e, n, v in m]
        elif sec == 'C':       # de cirkel rond: trompet in groot, strijkers erboven, de dood (gitaar) eronder
            m = mel(LIFE[i], t0, 122)
            P['tpt'] += [[s, e, n - 12, v] for s, e, n, v in m]
            P['lead_l'] += [[s, e, n, 108] for s, e, n, v in m]
            P['lead_d'] += [[s, e, n - 24, 108] for s, e, n, v in m] if i % 2 == 0 else []
        # ---- harmonie ----
        if mode == 'L':
            ts = tones(ch, p('E4') - 2, p('E6'))
            lo = next(k for k, m in enumerate(ts) if m >= near(r, p('E4') - 2))
            arp = ts[lo:lo + 4] + [ts[lo + 4] if lo + 4 < len(ts) else ts[-1]]
            cyc = arp + arp[-2:0:-1]
            if sec != 'C' or True:
                P['harp'] += [[t0 + k * S, t0 + k * S + S, cyc[k % len(cyc)], 86 + (12 if k % 4 == 0 else 0)]
                              for k in range(16)]
            if sec == 'L':
                pad(P, 'pad', t0, ch, p('G#3'), p('E4') + 4, 2, 86)
            elif sec != 'B':
                pad(P, 'choir', t0, ch, p('G#4'), p('E5'), 2, 86)
        else:
            if sec == 'S2' or sec == 'B':
                base = near(r, p('E3'))
                P['spicc'] += [[t0 + k * S, t0 + k * S + S, base + (0, 0, 12, 0, 7, 0, 12, 0)[k % 8] + 12,
                                86 + (14 if k % 4 == 0 else 0)] for k in range(16)]
            pad(P, 'choir', t0, ch, p('E4'), p('C5'), 2 if sec == 'S' else 1, 92)
            if i % 4 == 0:
                P['bell'].append([t0, t0 + 10 * S, near(r, 64), 106])
            if sec == 'S' and i in (1, 5):
                gust(P, CC, EX, 'wing', t0, 2 * BAR - 2 * S, 58, 96, wobble=4, seed=i)
        # ---- bas ----
        if mode == 'L':
            bass8(P, t0, ch, 98, pat=(0, 0, 7, 0, 12, 0, 7, 0), lo=40)
        else:
            if sec == 'S':       # half-time: lange grondtonen met een duw op 3-en
                rr = near(r, 40)
                P['bass'] += [[t0, t0 + 6 * S - 6, rr, 112], [t0 + 6 * S, t0 + 8 * S - 6, rr, 100],
                              [t0 + 8 * S, t0 + 14 * S - 6, rr, 108], [t0 + 14 * S, t0 + 16 * S - 6, rr + 12, 100]]
            else:
                bass8(P, t0, ch, 104, pat=(0, 0, 0, 12, 0, 0, 12, 0), lo=40)
            P['tuba'] += [[t0, t0 + 8 * S - 8, near(r, 48), 104], [t0 + 8 * S, t0 + 16 * S - 8, near(r, 48), 98]]
        P['wave'].append([t0, t0 + BAR - 8, near(r, 36), 66 if mode == 'L' else 74])
        tq = near(r, 38) + (12 if near(r, 38) < p('F2') else 0)
        P['timp'].append([t0, t0 + 2 * S, tq, 118 if mode == 'S' else 108])
        # ---- drums ----
        if mode == 'L':
            drum(P, t0, (0, 8, 10) if sec != 'L' else (0, 8), KICK, 112)
            drum(P, t0, (4, 12), SN, 106)
            drum(P, t0, range(0, 16, 2), TAMB, 88)
            if sec in ('L2', 'C'):
                drum(P, t0, range(1, 16, 2), HH, 78)
            if i % 4 == 0:
                drum(P, t0, (0,), CRASH, 108 if sec != 'C' else 118)
        elif sec == 'S':      # half-time, zwaar
            drum(P, t0, (0, 3, 10), KICK, 120)
            drum(P, t0, (8,), SN, 124)
            drum(P, t0, (0,), TAIKO, 118)
            drum(P, t0, (8,), TAIKO, 104)
            drum(P, t0, range(0, 16, 4), OHH, 74)
            if i % 4 == 0:
                drum(P, t0, (0,), CRASH2, 116)
        else:                 # S2 / B-dood: vol tempo, dubbele kicks
            drum(P, t0, (0, 2, 6, 8, 10, 14), KICK, 118)
            drum(P, t0, (4, 12), SN, 120)
            drum(P, t0, range(0, 16, 2), HH, 84)
            drum(P, t0, (0, 8), TAIKO, 112)
            if i % 4 == 0 or (sec == 'B'):
                drum(P, t0, (0,), CRASH2, 112)
        if i == 7 and sec != 'C':
            drum(P, t0, (12, 13), TOM_H, 104)
            drum(P, t0, (14,), TOM_L, 114)
        if sec == 'C' and i == 7:
            roll(P, t0, 8, 8, SN, 84, 5)
    end = len(tl) * BAR
    return dict(parts=P, cc=CC, ex=EX, end=end, loop=4, bpm=168,
                order=['lead_l', 'lead_d', 'tpt', 'drums', 'bell', 'bass', 'low', 'harp', 'timp', 'glock', 'spicc', 'tuba',
                       'choir', 'pad'],
                layout=[('lead_l', STR, 100, 0, 72), ('glock', GLOCK, 84, 1, 92), ('harp', HARP, 100, 2, 40),
                        ('lead_d', DIST_HI, 92, 3, 56), ('tpt', TPT, 100, 4, 64), ('low', HORN, 96, 5, 60),
                        ('tuba', TUBA, 86, 6, 64), ('bass', FBASS, 104, 7, 64), ('timp', TROLL, 104, 8, 64),
                        ('choir', CHOIR, 84, 10, 80), ('bell', BELL, 84, 11, 50), ('pad', STR, 78, 12, 52),
                        ('spicc', SPICC, 104, 13, 76), ('wave', WAVE, 56, 14, 64), ('wing', NOISE, 60, 15, 64)],
                drums=('drums',), drumvol=118)


# =====================================================================================================================
# 3. Uxie, Mesprit & Azelf
# =====================================================================================================================
L_PROG = ['F#m', 'D', 'E', 'C#m', 'Bm', 'D', 'G', 'C#']
MESPRIT = [
    [(0, 12, 'C#5'), (12, 2, 'B4'), (14, 2, 'A4')],
    [(0, 6, 'A4'), (6, 2, 'F#4'), (8, 4, 'A4'), (12, 4, 'D5')],
    [(0, 12, 'E5'), (12, 2, 'D5'), (14, 2, 'B4')],
    [(0, 8, 'C#5'), (8, 8, 'G#4')],
    [(0, 6, 'D5'), (6, 2, 'C#5'), (8, 4, 'B4'), (12, 4, 'F#5')],
    [(0, 12, 'F#5'), (12, 2, 'E5'), (14, 2, 'D5')],
    [(0, 8, 'B4'), (8, 4, 'D5'), (12, 4, 'G5')],
    [(0, 4, 'E#5'), (4, 4, 'G#5'), (8, 8, 'C#5')],
]
AZ_R = [(0, 3), (3, 1), (4, 3), (7, 1), (8, 4), (12, 2), (14, 2)]
AZ_N = [('F#4', 'F#4', 'A4', 'C#5', 'F#5', 'E5', 'C#5'), ('F#4', 'F#4', 'A4', 'D5', 'F#5', 'E5', 'D5'),
        ('G#4', 'G#4', 'B4', 'E5', 'G#5', 'F#5', 'E5'), ('G#4', 'G#4', 'C#5', 'E5', 'G#5'),
        ('B4', 'B4', 'D5', 'F#5', 'B5', 'A5', 'F#5'), ('A4', 'A4', 'D5', 'F#5', 'A5', 'F#5', 'E5'),
        ('B4', 'B4', 'D5', 'G5', 'B5', 'A5', 'G5'), ('C#5', 'C#5', 'E#5', 'G#5', 'C#6')]


def azelf(i):
    rh = AZ_R if len(AZ_N[i]) == 7 else AZ_R[:4] + [(8, 8)]
    return [(st, ln, n) for (st, ln), n in zip(rh, AZ_N[i])]


def uxie(P, key, t0, ch, lo, vel, part_len=2):
    """kennis: achtsten 3+3+2 op akkoordtonen (index 0,1,2, 0,1,2, 3,2) boven lo."""
    ts = tones(ch, lo, lo + 24)
    for k, j in enumerate((0, 1, 2, 0, 1, 2, 3, 2)):
        P[key].append([t0 + 2 * k * S, t0 + (2 * k + part_len) * S - 4, ts[j], vel + (16 if k in (0, 3, 6) else 0)])


def lakes():
    P, CC, EX = Parts(), Parts(), Parts()
    plan = [('I', 4), ('A', 8), ('B', 8), ('C', 8), ('D', 8), ('D2', 8), ('E', 4)]
    tl = []
    for sec, n in plan:
        for i in range(n):
            tl.append((len(tl), sec, i))
    E_PROG = ['F#m', 'D', 'G', 'C#']
    for b, sec, i in tl:
        t0 = b * BAR
        ch = E_PROG[i] if sec == 'E' else ('F#m' if sec == 'I' and i < 3 else ('C#' if sec == 'I' else L_PROG[i]))
        r = CH[ch][0]
        if sec == 'I':
            # rimpelend water: PSG-golf in 16en (zuiver, geen DS-fuzz), paukenroffel, koor zwelt
            ts = tones(ch, p('F#4'), p('F#6'))
            cyc = ts[:6] + ts[4:0:-1]
            P['ripple'] += [[t0 + k * S, t0 + k * S + S - 4, cyc[k % len(cyc)], 60 + 3 * i + (10 if k % 4 == 0 else 0)]
                            for k in range(16)]
            if i < 3:
                P['choir'] += [[t0, t0 + 16 * S - 8, m, 80 + 6 * i] for m in tones(ch, p('F#4'), p('C#5'))]
                P['timp'] += [[t0 + k * S, t0 + (k + 1) * S, p('F#2') + 12, 76 + 4 * i + k] for k in range(0, 16, 2)]
                P['bell'].append([t0, t0 + 8 * S, (p('C#5'), p('A4'), p('F#4'))[i], 96]) if i < 3 else None
            else:              # C#: koperstoot en roffel
                P['tpt'] += mel([(0, 6, 'G#4'), (8, 8, 'C#5')], t0, 116)
                P['horn'] += mel([(0, 6, 'E#4'), (8, 8, 'G#4')], t0, 110)
                roll(P, t0, 0, 16, OSN, 72, 4)
                P['timp'] += [[t0 + (8 + k) * S, t0 + (9 + k) * S, p('C#3'), 84 + 5 * k] for k in range(8)]
                drum(P, t0, (0,), CRASH2, 110)
            P['wave'].append([t0, t0 + BAR - 8, near(r, 36), 56])
            continue
        # ---- motieven ----
        if sec == 'A':
            uxie(P, 'glock', t0, ch, p('C#5'), 96)
            uxie(P, 'sq', t0, ch, p('C#5') - 12, 84)
            P['strings'] += [[t0, t0 + 16 * S - 8, near(r, p('F#5')), 92]] if i % 2 == 0 else \
                [[t0, t0 + 8 * S - 8, tones(ch, p('F#5'), p('F#6'))[1], 92], [t0 + 8 * S, t0 + 16 * S - 8,
                                                                             tones(ch, p('F#5'), p('F#6'))[0], 92]]
        elif sec == 'B':
            P['oboe'] += mel(MESPRIT[i], t0, 110)
            P['strings'] += mel(MESPRIT[i], t0, 96, oct=1)
            uxie(P, 'sq', t0, ch, p('C#4'), 64) if i >= 4 else None    # kennis echoot zacht mee (PSG)
        elif sec == 'C':
            P['tpt'] += mel(azelf(i), t0, 120)
            P['horn'] += mel(azelf(i), t0, 108, oct=-1)
        elif sec in ('D', 'D2'):
            P['horn'] += mel(azelf(i), t0, 114, oct=-1)
            P['strings'] += mel(MESPRIT[i], t0, 102, oct=1)
            P['oboe'] += mel(MESPRIT[i], t0, 108)
            uxie(P, 'sq', t0, ch, p('C#5'), 88)
            if sec == 'D2':
                P['tpt'] += mel(azelf(i), t0, 116)
                uxie(P, 'glock', t0, ch, p('C#6'), 90)
        elif sec == 'E':       # break: elk motief één maat, dan alle drie op C#
            if i == 0:
                uxie(P, 'glock', t0, ch, p('C#5'), 100)
                uxie(P, 'sq', t0, ch, p('C#4'), 88)
            elif i == 1:
                P['oboe'] += mel(MESPRIT[1], t0, 112)
                P['strings'] += mel(MESPRIT[1], t0, 100, oct=1)
            elif i == 2:
                P['tpt'] += mel(azelf(6), t0, 120)
                P['horn'] += mel(azelf(6), t0, 110, oct=-1)
            else:
                P['tpt'] += mel(azelf(7), t0, 122)
                P['horn'] += mel(azelf(7), t0, 112, oct=-1)
                P['strings'] += mel(MESPRIT[7], t0, 100, oct=1)
                uxie(P, 'sq', t0, ch, p('C#5'), 92)
        # ---- harmonie ----
        if sec in ('A', 'D'):
            pad(P, 'choir', t0, ch, p('E4'), p('C#5'), 2, 86 if sec == 'A' else 92)
        if sec == 'B':
            ts = tones(ch, p('F#3'), p('F#6'))
            lo = next(k for k, m in enumerate(ts) if m >= near(r, p('F#3')))
            cyc = ts[lo:lo + 5] + ts[lo + 3:lo:-1]
            P['harp'] += [[t0 + k * S, t0 + k * S + S, cyc[k % len(cyc)], 86 + (12 if k % 4 == 0 else 0)]
                          for k in range(16)]
            pad(P, 'choir', t0, ch, p('E4'), p('C#5'), 2, 84)
        if sec in ('C', 'D2'):
            base = near(r, p('F#3'))
            P['spicc'] += [[t0 + k * S, t0 + k * S + S, base + (0, 7, 12, 7)[k % 4], 86 + (14 if k % 4 == 0 else 0)]
                           for k in range(16)]
        if sec == 'C':
            pad(P, 'choir', t0, ch, p('E4'), p('C#5'), 1, 92)
        # ---- bas, tuba, pauken ----
        if sec == 'B':
            rr = near(r, 38)
            P['bass'] += [[t0, t0 + 6 * S - 6, rr, 100], [t0 + 6 * S, t0 + 8 * S - 6, rr + 7, 92],
                          [t0 + 8 * S, t0 + 16 * S - 6, rr, 100]]
        elif sec != 'E':
            bass8(P, t0, ch, 100, pat=(0, 0, 12, 0, 0, 7, 12, 0))
        else:
            P['bass'].append([t0, t0 + 8 * S - 6, near(r, 38), 108])
        if sec == 'C':
            P['tuba'] += [[t0, t0 + 8 * S - 8, near(r, 48), 104], [t0 + 8 * S, t0 + 16 * S - 8, near(r + 7, 48), 98]]
        P['wave'].append([t0, t0 + BAR - 8, near(r, 36), 66])
        tq = near(r, 38) + (12 if near(r, 38) < p('F2') else 0)
        P['timp'].append([t0, t0 + 2 * S, tq, 116])
        if sec in ('C', 'D'):
            q = near(r + 7, 38)
            P['timp'].append([t0 + 8 * S, t0 + 10 * S, q + (12 if q < p('F2') else 0), 104])
        # ---- drums ----
        if sec == 'A':          # mysterieus maar in beweging: toms en taiko, hats in 16en
            drum(P, t0, (0, 6, 10), TAIKO, 110)
            drum(P, t0, (4, 12), SN, 100)
            drum(P, t0, range(0, 16, 1), HH, 70)
            P['drums'] = [d if d[2] != HH or (d[0] - t0) % (4 * S) != 0 else [d[0], d[1], HH, 88]
                          for d in P['drums']]
        elif sec == 'B':        # half-time
            drum(P, t0, (0, 10), KICK, 112)
            drum(P, t0, (8,), SN, 112)
            drum(P, t0, range(0, 16, 2), HH, 78)
        elif sec == 'E':
            drum(P, t0, (0,), TAIKO, 118)
            if i == 3:
                roll(P, t0, 8, 8, TOM_H, 90, 4)
                P['drums'][-8:] = [[s, s + DLEN[TOM_M], (TOM_H, TOM_H, TOM_M, TOM_M, TOM_L, TOM_L, SN, SN)[k], v]
                                   for k, (s, e, n, v) in enumerate(P['drums'][-8:])]
        else:                   # C / D / D2: drijvend
            drum(P, t0, (0, 3, 8, 11) if sec != 'D' else (0, 8, 11), KICK, 116)
            drum(P, t0, (4, 12), SN, 114)
            drum(P, t0, range(0, 16, 2), HH, 82)
            drum(P, t0, (6, 14), TAIKO, 100)
        if sec != 'E' and i % 4 == 0:
            drum(P, t0, (0,), CRASH if sec != 'A' else CRASH2, 110)
        if sec != 'E' and i == 7:
            drum(P, t0, (12, 13), TOM_H, 102)
            drum(P, t0, (14,), TOM_L, 110)
    end = len(tl) * BAR
    return dict(parts=P, cc=CC, ex=EX, end=end, loop=4, bpm=144,
                order=['tpt', 'oboe', 'horn', 'glock', 'drums', 'bell', 'strings', 'bass', 'spicc', 'harp', 'timp', 'tuba',
                       'choir'],
                layout=[('glock', GLOCK, 92, 0, 84), ('sq', SQ1, 64, 1, 64), ('oboe', OBOE, 100, 2, 60),
                        ('strings', STR, 92, 3, 76), ('tpt', TPT, 100, 4, 68), ('horn', HORN, 100, 5, 56),
                        ('tuba', TUBA, 86, 6, 64), ('bass', FBASS, 104, 7, 64), ('timp', TROLL, 102, 8, 64),
                        ('choir', CHOIR, 84, 10, 72), ('harp', HARP, 100, 11, 44), ('spicc', SPICC, 104, 12, 84),
                        ('wave', WAVE, 56, 13, 64), ('ripple', SQ2, 60, 14, 64), ('bell', BELL, 84, 15, 64)],
                drums=('drums',), drumvol=116)


THEMES = {'zacian': zacian, 'xerneas': xerneas, 'lake_trio': lakes}
OCT_DOWN = {}      # (distortion_guitar_high klinkt op de geschreven hoogte; geen correcties nodig)


def voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm + overrides voor Battle! Zacian & Zamazenta / Xerneas & Yveltal / Uxie, Mesprit & Azelf.'
    lines[1] = '@ Gegenereerd door tools/grounded/legends3_theme.py. Alleen Emerald-samples.'
    lines[2] = 'voice_group %s' % VG
    over = {
        9: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_glockenspiel, 255, 165, 51, 150',
        14: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_tubular_bell, 255, 165, 51, 200',
        30: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_distortion_guitar_high, 255, 0, 255, 165',
        45: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 90',
        46: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_harp, 255, 242, 51, 100',
        47: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 200',
        49: 'voice_keysplit voicegroup_legends3_spicc_keysplit, keysplit_strings',
        56: 'voice_keysplit voicegroup_legends3_trumpet_keysplit, keysplit_trumpet',
        60: 'voice_keysplit voicegroup_legends3_horn_keysplit, keysplit_french_horn',
        64: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_oboe, 255, 165, 154, 140',
        80: 'voice_square_1 60, 0, 0, 1, 0, 2, 5, 1',
        81: 'voice_square_2 60, 0, 2, 0, 1, 4, 1',
        84: 'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_1, 0, 7, 15, 0',
        121: 'voice_noise_alt 60, 0, 0, 0, 0, 15, 2',
        127: 'voice_keysplit_all voicegroup_legends3_drumset',
    }
    out = []
    for l in lines:
        for k, v in over.items():
            if l.rstrip().endswith('@ %d' % k):
                l = '\t%s  @ %d' % (v, k)
        out.append(l)
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    open('sound/voicegroups/keysplits/legends3_spicc.inc', 'w').write(
        '@ Project Grounded: spiccato-strijkers (harde aanzet, kort) voor legends3_theme.py.\n'
        'voice_group legends3_spicc_keysplit\n' +
        ''.join('\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_string_ensemble_%d, 255, 0, 255, 110\n' % k
                for k in (60, 72, 84)))
    # koper met kortere uitklinktijd: 16en-opmaten (zwaardslag, Azelf-fanfare) houden zo één kanaal bezet
    open('sound/voicegroups/keysplits/legends3_trumpet.inc', 'w').write(
        '@ Project Grounded: trompet met kortere release (legends3_theme.py).\n'
        'voice_group legends3_trumpet_keysplit\n' +
        ''.join('\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_trumpet_%d, 255, 0, 193, 112\n' % k
                for k in (60, 72, 84)))
    open('sound/voicegroups/keysplits/legends3_horn.inc', 'w').write(
        '@ Project Grounded: hoorn met kortere release (legends3_theme.py).\n'
        'voice_group legends3_horn_keysplit\n'
        '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_french_horn_60, 255, 0, 224, 120\n'
        '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_french_horn_72, 255, 0, 218, 120\n')
    kit = [
        ('36 kick', 'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 200'),
        ('37 orkestsnare', 'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 200'),
        ('38 snare', 'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 200'),
        ('39 tom laag', 'voice_directsound 45, 52, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 204'),
        ('40 tom midden', 'voice_directsound 51, 64, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 204'),
        ('41 tom hoog', 'voice_directsound 57, 76, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 204'),
        ('42 orkestbekken', 'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 216'),
        ('43 crash', 'voice_directsound 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165'),
        ('44 hihat dicht', 'voice_directsound 60, 64, DirectSoundWaveData_unknown_close_hihat, 255, 127, 0, 188'),
        ('45 tamboerijn', 'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_tambourine, 255, 127, 77, 204'),
        ('46 taiko', 'voice_directsound 57, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180'),
        ('47 hihat open', 'voice_directsound 60, 64, DirectSoundWaveData_unknown_open_hihat, 255, 242, 141, 0'),
    ]
    open('sound/voicegroups/drumsets/legends3.inc', 'w').write(
        '@ Project Grounded: drumkit voor legends3_theme.py (Zacian / Xerneas / meren). Alleen stock-samples, geen PSG.\n'
        '@ ' + ', '.join(n for n, _ in kit) + '.\n'
        '@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.\n'
        'voice_group legends3_drumset, 36\n' + ''.join('\t%s\n' % v for _, v in kit))


def build(name, refdir=None):
    th = THEMES[name]()
    P, bpm = th['parts'], th['bpm']
    for k in list(P):
        P[k] = dedupe(P[k])
    # op een bekkenslag geen hihat/tamboerijn (scheelt een kanaal op de zwaarste tel)
    cr = {e[0] for e in P['drums'] if e[2] in (CRASH, CRASH2)}
    P['drums'] = [e for e in P['drums'] if not (e[2] in (HH, OHH, TAMB) and e[0] in cr)]
    progs = {k: pr for k, pr, *_ in th['layout']}
    rel = releases(VG)
    tail = {k: release_ticks(rel.get(pr, 200), TPB, bpm) + 2 for k, pr in progs.items()}
    for k, pr in progs.items():           # elke DS-partij: noot + uitklinktijd eindigt vóór de volgende aanslag
        if rel.get(pr) is not None:
            P[k] = detach(P[k], tail[k])
    for k, pr in progs.items():
        if rel.get(pr) is not None:
            low = [n for _, _, n, _ in P[k] if n < 36]
            assert not low, '%s %s: DirectSound-noten onder C2 (fuzz/dreun): %s' % (name, k, low[:5])
            if pr in (TPT, HORN, TUBA):
                bad = [n for _, _, n, _ in P[k] if n < 48]
                assert not bad, '%s %s: koper onder C3 %s' % (name, k, bad[:5])
            soft = [v for _, _, _, v in P[k] if v < 76]
            assert not soft, '%s %s: zachte DS-noten (8-bit-fuzz) %s' % (name, k, soft[:5])
        else:
            low = [n for _, _, n, _ in P[k] if n < 36 and pr != NOISE]
            assert not low, '%s %s: PSG-noten onder C2 klinken als C2' % (name, k)
    order = th['order']
    ds = {k: P[k] for k in order}
    kept = allocate(ds, order, tail, max_voices=MAXV)
    for k in order:
        n = len(ds[k])
        if n and len(kept[k]) < n:
            print('  %s %s: %d van %d noten vallen weg (%.1f%%)' % (name, k, n - len(kept[k]), n, 100 * (n - len(kept[k])) / n))
            if os.environ.get('L3_DEBUG'):
                kk = {tuple(e) for e in kept[k]}
                print('     weg op maat:', [round(e[0] / BAR, 2) for e in ds[k] if tuple(e) not in kk][:20])
                for e in [e for e in ds[k] if tuple(e) not in kk][:4]:
                    busy = {}
                    for q in order:
                        for x in kept[q]:
                            if x[0] <= e[0] < x[1] + tail.get(q, 0):
                                busy[q] = busy.get(q, 0) + 1
                    print('       %.2f bezet:' % (e[0] / BAR), busy)
        P[k] = kept[k]
    if os.environ.get('L3_OCC'):      # gemiddelde kanaalbezetting per partij per 4 maten (vóór de stemverdeler)
        for b0 in range(0, th['end'] // BAR, 4):
            row = []
            for k in order:
                t = tail.get(k, 0)
                busy = sum(sum(1 for e in ds[k] if e[0] <= x < e[1] + t) for x in range(b0 * BAR, (b0 + 4) * BAR, S))
                if busy:
                    row.append('%s %.1f' % (k, busy / 64))
            print('   maat %2d: %s' % (b0, ', '.join(row)))
    lp = th['loop'] * BAR
    for ref in (False, True):
        if ref and not refdir:
            continue
        song = Song(TPB, 500000)
        song.tempo(0, bpm / 120)
        song.loop = (lp, th['end'])
        for k, pr, vol, ch, pan in th['layout']:
            notes = P[k]
            ccs = list(th['cc'].get(k, []))
            ex = list(th['ex'].get(k, []))
            if ex:
                ccs = [(0, 20, 12)] + ccs
            song.add(notes, pr if not ref else min(pr, 126), vol, ch, pan, extra=ex, ccs=ccs)
        drums = sorted(sum((P[k] for k in th['drums']), []))
        if ref:      # GM-kit: andere toetsen
            gm = {KICK: 36, OSN: 38, SN: 40, TOM_L: 41, TOM_M: 45, TOM_H: 48, CRASH: 49, CRASH2: 57, HH: 42,
                  TAMB: 54, TAIKO: 35, OHH: 46}
            drums = [[s, e, gm[n], v] for s, e, n, v in drums]
        song.add(drums, KIT if not ref else 0, th.get('drumvol', 110), 9)
        written = {k for k, *_ in th['layout']} | set(th['drums'])
        assert not [k for k in P if P[k] and k not in written], '%s: partij niet weggeschreven %s' % (
            name, [k for k in P if P[k] and k not in written])
        out = os.path.join(refdir, 'legends3_%s_ref.mid' % name) if ref else \
            'sound/songs/midi/mus_grounded_vs_%s.mid' % name
        song.save(out, th['end'])
        if not ref:
            print(out, '| intro %.1f s | loop %.1f s | totaal %.1f s' % (
                lp / TPB * 60 / bpm, (th['end'] - lp) / TPB * 60 / bpm, th['end'] / TPB * 60 / bpm))


if __name__ == '__main__':
    ref = sys.argv[sys.argv.index('--ref') + 1] if '--ref' in sys.argv else None
    voicegroup()
    for n in THEMES:
        build(n, ref)
