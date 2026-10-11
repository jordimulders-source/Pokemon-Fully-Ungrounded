#!/usr/bin/env python3
"""Project Grounded: "Battle! Treasures of Ruin" (song 683, MUS_GROUNDED_VS_RUINOUS): het gevechtsthema van Wo-Chien,
Chien-Pao, Ting-Lu en Chi-Yu (Pokémon Scarlet/Violet) in GBA-stijl, v3.

Nagebouwd op het raster van het origineel (Jordi's mp3 + Spleeter-stems, gemeten met librosa/basic-pitch):
152 bpm (onset-fase 0,070 s, maat 1 = 0,37 s), maat = 1,579 s, loop = 65 maten (102,6 s; maat 70 = maat 5).
Toonsoort: B met een frygische C (bas en ostinato B-B-.-B-B-.-C-.), wisselend groot/klein, G (lydisch, met C#)
als bVI, E en F# als IV en V, en een paar chromatische opbouwmaten.
Vorm (maten van het origineel):
  I   1-4    intro: zwevend Bmaj6-akkoord, daarna F#6/9; elektronische twinkelingen (PSG) op een los, ongemeten
             ritme (gemeten: aanzetten om de 30-100 ms, alleen F#5-Eb6); de cry valt in maat 2
  [loop]
  Q   5-12   INSLAG op maat 5; het ostinato (16en x x . x x . x . per halve maat, B met de frygische C) alleen met
             een B-F#-bourdon; trompetroep F5 (maat 6-8, de verminderde kwint) die naar F#5 stijgt (9-12); maat 9
             een rommelende trom, maat 11-12 lichte hats
  U  13-16   de trommen komen erbij (3-3-2), bas-aanloop A-Bb ... D-C# naar B
  A  17-32   de groove: grote trom op elke tel, lage dreun op elke 'en', hats, bas B-B-.-B-.-.-C-. | B-B-.-B-B-.-A-.;
             vanaf maat 21 de oosterse tokkel (koto, 16en: Jordi hoorde hier 'een oosters instrument, geen strijkers');
             akkoorden B5 B5 B5 B5 B | E-Gm B B B G B B G G Bm Bm; trompet-fanfare (F#5) in 31-32
  A2 33-36   G G F# D/A: stijgende trompetparen (F#4-A4-B4), F#5-roep
  B  37-52   tweede groove: Bm Em B5 B5 B G B5 B5 G G|Gm Bm Bm G G|Gm F# A, hoorns en koto, fanfare in 47-48
  R  53-56   roffels: taiko en snare in 16en over een verminderd B-akkoord (B D F A)
  H  57-60   B7 Em B7 A: hats in 16en, de koto speelt B7-arpeggio's
  K  61-64   opbouw: G -> Gm|E -> G#m -> G#m|F#, steeds dichtere roffels en een stijgende hoornlijn
  X  65      inslag + het Bmaj6-akkoord van de intro, de trommen vallen weg
  Q2 66-69   het ostinato alleen (zoals maat 5-12, zonder trompet); opmaat naar de inslag van maat 5 (= loopbegin)
  ]
(De vorm hierboven is die van v1; v2 en v3 houden het drumritme en de vorm, de rest is vervangen.)
v3 (Jordi over v2: 'lijkt nog nergens op, een soort glitchend systeem, geen tokkel of strijker zoals het origineel;
instrumenten isoleren'): alle melodische lagen spelen samples die uit het origineel zelf geknipt zijn
(tools/grounded/ruinous_samples.py, CUTS, gestemd op de gemeten grondtoon), getoetst per laag met een A/B (solo uit de
mixbuffer van één test-ROM tegen de stem):
  lo    het lage instrument van de intro (stem 'piano': E2 uit maat 1, B3 uit maat 5 met loop van 1,0 s), maat 1-8
  ost   de rustige maten 5-12 en 66-69: een halve maat van de stem 'other' uit maat 67 (B3 + F#4 aangehouden, de C4 op
        16e 6), per halve maat aangeslagen en naar de grondtoon getransponeerd (E-maten E4, G-maten G3)
  oth   maat 13-64: per akkoord de halve maat van de stem 'other' waar dat akkoord in het origineel klinkt (B, E, G,
        Gm, Bm, F#, D/A, Em, A; > 160 Hz), programmawissel per halve maat; akkoorden zonder eigen knipsel getransponeerd
  bass  één basnoot E2 uit de basstem, gemeten ritme en register (B1-B2, G2, F#2; opbouw tot F1)
  drums ongewijzigd sinds v1/v2 (ritme 'goed'), synthetische taiko/dreun/ka/inslag + stock-kit
Weggelaten: de hogere lijn in de stem 'piano' (maat 23-60, 0,2% van de energie; de A/B bleef onherkenbaar), trompetten,
hoorns, strijkers en PSG (v1/v2). ROM: ±135 KB samples (11025 Hz).
Gebruik: python3 tools/grounded/ruinous_theme.py [--render <map>] [-v]"""
import os, subprocess, sys
import numpy as np
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

OUT = 'sound/songs/midi/mus_grounded_vs_ruinous.mid'
VG = 'grounded_ruinous'
TPB = 96
S = TPB // 4                 # een 16e
BAR = TPB * 4
BPM = 152
MAX_V = 11                   # legendary-budget

LO, OSTP, OSTP2, PADP, INTROP, PADG, BASS, STR, DRUMS = 107, 82, 83, 84, 85, 86, 33, 48, 127
CALL, WIDE14, WIDE18 = 87, 88, 89   # v6
(TAIKO, BOOM, KA, IMPACT, CRASH, HAT, SNARE, TAIKO_LO, KICK) = range(36, 45)

N = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'Ab': 8,
     'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def p(name):
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


def pat(s):
    """'stap:lengte:noot ...' -> [(stap, lengte, noot)]"""
    out = []
    for w in s.split():
        a, b, c = w.split(':')
        out.append((int(a), int(b), p(c)))
    return out


# ---- harmonie (gemeten per halve maat: bas-grondtoon + aangehouden tonen in de stem 'other') --------------------------
# naam: (grondtoon, akkoordtonen, buurtoon van het ostinato in halve tonen boven de grondtoon)
CHORD = {
    'B5': (11, (11, 6), 1), 'B': (11, (11, 3, 6), 1), 'Bm': (11, (11, 2, 6), 1), 'B7': (11, (11, 3, 6, 9), 1),
    'Bo': (11, (11, 2, 5, 9), 1), 'E': (4, (4, 6, 11), 2), 'Em': (4, (4, 7, 11), 2), 'Gm': (7, (7, 10, 2), 2),
    'G': (7, (7, 11, 2, 6), 2), 'F#': (6, (6, 8, 1), 1), 'DA': (9, (9, 2, 6, 1), 2), 'A': (9, (9, 1, 4), 2),
    'G#m': (8, (8, 11, 3), 2), 'Bmaj': (11, (11, 4, 6, 3, 8, 9), 1), 'F#69': (6, (6, 8, 10, 1, 11, 5), 1),
    'B11': (11, (11, 4, 6, 9), 1), 'Emaj': (4, (4, 8, 11), 2), 'F#m': (6, (6, 9, 1), 1), 'C#': (1, (1, 5, 8), 2),
    'G#': (8, (8,), 1),
}
HARM = {}   # maat (1-based) -> (akkoord eerste helft, tweede helft)
for b in range(1, 70):
    HARM[b] = ('B5', 'B5')
for b, c in {1: 'Bmaj', 2: 'Bmaj', 3: 'F#69', 4: 'F#69', 21: 'B', 22: 'E', 23: 'B', 24: 'B', 25: 'B', 26: 'G',
             29: 'G', 30: 'G', 31: 'Bm', 32: 'Bm', 33: 'G', 34: 'G', 35: 'F#', 36: 'DA', 37: 'Bm', 38: 'Em', 41: 'B',
             42: 'G', 45: 'G', 46: 'G|Gm', 47: 'Bm', 48: 'Bm', 49: 'G', 50: 'G|Gm', 51: 'F#', 52: 'A',
             53: 'Bo', 54: 'Bo', 55: 'Bo', 56: 'Bo', 57: 'B7', 58: 'Em', 59: 'B7', 60: 'B11', 61: 'G', 62: 'Emaj|Em',
             63: 'F#m', 64: 'C#', 65: 'G#'}.items():
    a, _, z = c.partition('|')
    HARM[b] = (a, z or a)


def section(b):
    for name, lo, hi in (('I', 1, 4), ('Q', 5, 12), ('U', 13, 16), ('A', 17, 32), ('A2', 33, 36), ('B', 37, 52),
                         ('R', 53, 56), ('H', 57, 60), ('K', 61, 64), ('X', 65, 65), ('Q2', 66, 69)):
        if lo <= b <= hi:
            return name


INTRO = 4
END = 69


def near(pc, lo):
    """laagste toon >= lo met toonklasse pc"""
    return lo + ((pc - lo) % 12)


def voicing(ch, lo, n):
    """n akkoordtonen vanaf lo omhoog (gesloten ligging)"""
    tones = CHORD[ch][1]
    out, m = [], lo
    while len(out) < n:
        if m % 12 in tones:
            out.append(m)
        m += 1
    return out


class Parts(dict):
    def __missing__(self, k):
        self[k] = []
        return self[k]


def add(P, key, t0, st, ln, n, v):
    P[key].append([t0 + st * S, t0 + (st + ln) * S, n, v])


# ---- materiaal ---------------------------------------------------------------------------------------------------
# v4 (Jordi over v3: 'lo klopt alleen de eerste toon; oth loopt een noot en verdwijnt; oth2 als een vastslaande
# cd-speler; bas een rare remix'): geen geraden lijnen en geen herhaalde stukjes waar het origineel doorloopt.
#   intro  maat 1-4: het origineel zelf (alle stems), één sample
#   lo     maat 5-8: de frase van het lage instrument (stem 'piano'), één sample
#   ost    maat 5-12 en 66-69: het ostinato met de diepe bourdon (maat 8) / zonder (maat 67), één hele maat per aanslag
#   pad    maat 13-64: het aangehouden B3+F#4 van de grooves (stem 'other' < 450 Hz), per maat (of halve maat bij
#          een akkoordwissel) naar de grondtoon getransponeerd
#   bass   noot voor noot uit de basstem (pyin per 16e), één B1-sample
# Niet nagemaakt (niet betrouwbaar te isoleren uit 'other'): de 16e-figuur en de hogere lijn van de grooves.
SHIFT = {11: 0, 4: 5, 7: -4, 6: -5, 9: -2, 8: -3, 1: 2, 2: 3}     # transpositie per grondtoon (B = 0)
# v6 roep (stem 'vocals', maat 5-12): F6 (5:4-6:6), F5 (tot 9:4), F#5 (tot het eind van maat 12); niveau per 8e (dB, gemeten)
CALL_ENV = [-107, -105, -47, -37, -37, -37, -35, -34, -33, -34, -39, -40, -43, -40, -42, -44, -40, -37, -34, -34, -33, -32,
            -32, -33, -33, -36, -30, -30, -29, -32, -31, -33, -35, -41, -37, -35, -31, -31, -33, -33, -35, -36, -34, -32,
            -30, -26, -27, -30, -28, -30, -31, -32, -33, -31, -34, -32, -30, -33, -33, -32, -32, -33, -31, -31]
CALL_V = 64                           # CC7 bij het luidste punt (-26 dB)
WIDE_V = 100                          # pad-spoor in maat 13-20 (brede knipsels)
# (v9: CALL_V, WIDE_V en de ost-CC's gaan door mv(): MELO_DB luider)
# v8 strijkerssectie + alles van de stem 'other' in maat 21-65: het origineel zelf op zijn eigen plek, stukken van
# 2 maten (ruinous_samples.ST_PIECES), om en om op 'str' en 'str2' zodat elk stuk zijn overloop uitspeelt
ST_PIECES = [(21, 2), (23, 2), (25, 2), (27, 2), (29, 2), (31, 2), (33, 2), (35, 2), (37, 2), (39, 2), (41, 2), (43, 2), (45, 2), (47, 2), (49, 2), (51, 2), (53, 2), (55, 2), (57, 2), (59, 2), (61, 2), (63, 2), (65, 1)]
ST_PROG = {b: 40 + i for i, (b, _) in enumerate(ST_PIECES)}
PAD_OWN = {}   # v8: geen eigen padknipsels meer (maat 21-65 = ST_PIECES)
STR_VOL = 127                          # sectie: niveau t.o.v. pad/drums (gemeten in de mix)
# v9 (Jordi over de 1.0: 'heel muffled, zacht'; gemeten t.o.v. het origineel: 60-120 Hz +4,5 dB te veel = de
# lijf-dreun van taiko/dreun, de rest van het spectrum gelijk na de EQ in ruinous_samples.py): de lage plank op de
# synthetische trommen (ruinous_samples.DRUM_LOW_DB) en alles behalve trommen en bas MELO_DB luider. Strijkers en
# stem 'other' stonden al op 127/127: een tweede spoor met dezelfde stukken (str/str2 -> strb/str2b) op STR_VOL_B.
MELO_DB = 4.5
MELO = 10 ** (MELO_DB / 20)
DRUM_DB = 1.5                          # trommen (na de lage plank) iets luider: spoorvolume, taiko via velocity
DRUM = 10 ** (DRUM_DB / 20)


def dv(v):
    return max(1, min(127, round(v * DRUM)))
STR_VOL_B = round(127 * (MELO - 1))


def mv(v):
    return max(1, min(127, round(v * MELO)))
BASS_NOTES = {   # maat: stap:lengte:noot:velocity (pyin per 16e op de basstem, maat 5-69; v4)
    5: '0:1:D#2:80 1:1:D#2:87 2:7:E2:99 9:1:F2:80 10:1:E2:82 11:2:D#2:81 14:1:E2:80',
    13: '0:2:F2:80',
    14: '9:2:B1:80',
    15: '0:1:B1:80 3:2:A#1:86',
    16: '8:1:C2:80 10:1:C#2:80 11:5:D2:122',
    17: '0:2:B1:93 3:1:B1:113 4:1:C2:90 6:2:C2:119 8:1:B1:90 9:1:B1:100 11:3:B1:118 14:1:C2:92',
    18: '0:1:B1:97 1:1:B1:100 2:1:B1:80 3:2:B1:83 6:1:C2:80 8:1:B1:89 9:2:B1:96 11:2:B1:107 13:1:A2:80 14:2:A2:127',
    19: '0:1:B1:83 1:1:B1:90 3:2:B1:115 5:1:C2:80 6:1:C2:104 7:1:B1:80 8:1:B1:97 9:1:B1:107 11:3:B1:118 14:2:C2:123',
    20: '0:1:B1:110 1:1:B1:119 2:1:B1:83 3:2:B1:115 5:1:B1:80 6:1:C2:109 8:1:B1:93 9:2:B1:110 11:2:B1:113 13:1:G#1:80 14:2:A1:127',
    21: '0:1:B1:92 1:2:B1:112 3:2:B1:119 5:1:C2:80 6:2:C2:125 8:1:B1:96 9:1:B1:127 10:1:B1:83 11:2:B1:119 13:1:B1:80 14:2:C2:119',
    22: '0:1:E2:103 1:2:E2:127 3:3:E2:121 6:1:F#2:115 7:1:F#2:86 8:1:E2:125 9:2:E2:127 11:3:E2:114 14:1:F#2:126 15:1:F#2:87',
    23: '0:1:B2:127 1:2:B2:127 3:1:B1:127 4:2:B1:122 6:1:C2:122 7:1:B1:89 8:1:B1:107 9:1:B1:124 10:1:B1:82 11:1:B1:118 12:1:B1:104 13:1:G#1:89 14:1:A1:127 15:1:A#1:92',
    24: '0:1:B1:109 1:2:B1:116 3:1:B1:124 4:1:B1:100 6:2:C2:124 8:1:B1:103 9:2:B1:119 11:1:B1:121 12:1:B1:110 14:1:A1:112 15:1:A#1:84',
    25: '0:1:B1:101 1:2:B1:125 3:1:B1:115 4:2:B1:113 6:1:C2:127 7:1:C#2:86 8:1:B1:118 9:2:B1:112 11:1:B1:119 12:1:B1:106 13:1:B1:84 14:2:C2:118',
    26: '0:1:G1:94 1:2:G1:109 3:1:G1:107 4:1:G1:127 5:1:G1:113 6:1:A1:127 7:1:A1:98 8:1:G1:98 9:1:G1:106 10:1:G1:80 11:1:G1:121 12:1:G1:111 13:1:G1:94 14:1:A1:104 15:1:A1:80',
    27: '0:1:B1:102 1:2:B1:119 3:1:B1:115 4:2:B1:110 6:1:C2:127 7:1:B1:83 8:1:B1:110 9:2:B1:113 11:1:B1:107 12:1:A#1:108 13:1:G#1:100 14:1:A1:127 15:1:A1:95',
    28: '0:1:B1:113 1:2:B1:116 3:2:B1:127 6:1:C2:103 8:1:B1:114 9:1:B1:127 10:1:B1:86 11:2:B1:127 13:1:G#1:88 14:1:A1:127 15:1:A1:95',
    29: '0:1:G#1:121 1:1:G1:127 3:1:G2:103 4:1:G2:106 6:1:A1:106 7:1:A1:84 8:1:G1:100 9:1:G2:126 10:1:G#2:80 11:1:G2:89 12:1:G#1:97 13:1:G#1:98 14:2:A1:123',
    30: '0:2:G1:89 3:1:G1:97 4:1:G1:107 5:1:G1:89 6:1:A1:116 7:1:A1:84 8:1:G#1:113 9:1:G1:118 11:1:G2:94 12:1:G2:91 14:2:F#2:115',
    31: '0:1:B1:91 1:2:B1:104 3:1:B1:115 4:1:D2:104 5:1:E2:94 6:2:F#2:119 8:1:B1:122 9:2:B1:127 11:1:B1:115 12:1:D2:103 13:1:E2:91 14:1:F#2:114 15:1:F#2:82',
    32: '0:1:B1:98 1:2:B1:100 3:2:B1:116 5:1:D2:83 6:1:F#2:91 10:1:F#2:91 12:1:D#2:91 13:1:E2:95 14:1:F#2:99',
    33: '0:1:G2:85 1:1:G2:104 3:2:G2:91 5:1:F#2:83 6:2:A2:108 8:2:G2:92 10:1:G#2:80 11:2:G2:97 13:1:G#2:91 14:1:A1:124 15:1:A1:97',
    34: '0:1:G1:83 1:1:G2:91 3:1:G2:101 4:2:G2:93 6:2:A2:109 8:2:G2:96 11:2:G2:104 13:1:F#2:94 14:2:F#2:120',
    35: '0:1:F#2:95 1:1:F#2:123 2:1:F#2:84 3:1:F#2:107 4:1:F#2:88 5:1:G2:94 6:2:F#2:119 8:1:F#2:89 9:1:F#2:112 10:1:F#2:111 11:1:F#2:106 12:1:F#2:118 13:1:F#2:122 14:1:F#2:123 15:1:G2:80',
    36: '1:1:G2:116 2:1:A2:89 3:1:A2:99 4:1:G1:102 5:1:G1:97 6:2:A1:120 11:1:B1:118 12:1:A1:101 13:1:G#1:94 14:1:A1:127 15:1:A1:89',
    37: '0:1:B1:123 1:2:B1:127 3:1:B1:109 4:1:B1:118 5:1:B1:85 6:1:C2:118 7:1:C2:80 8:1:B1:124 9:2:B1:124 11:1:B1:127 12:1:B1:127 13:1:B1:91 14:2:C2:127',
    38: '0:1:E2:124 1:1:E2:127 2:1:E2:86 3:1:E2:127 4:1:E2:127 5:1:E2:103 7:1:F#2:82 8:1:E2:104 9:1:E2:127 10:1:E2:81 11:1:E1:121 12:1:B1:119 13:1:F2:100 14:1:F#2:127 15:1:F#2:88',
    39: '0:1:B1:127 1:2:B1:127 3:1:B1:109 4:1:B1:119 5:1:B1:86 6:2:C2:121 8:1:B1:122 9:2:B1:127 11:1:B1:127 12:1:B1:120 13:1:G#1:88 14:2:A1:116',
    40: '0:1:B1:123 1:1:B1:125 2:1:B1:83 3:2:B1:122 6:1:C2:117 7:1:B1:80 8:1:B1:109 9:2:B1:118 11:1:B1:127 12:1:B1:115 13:1:A#1:85 14:1:A1:127 15:1:A1:94',
    41: '0:1:B1:124 1:2:B1:127 3:1:B1:124 4:1:B1:106 5:1:B1:85 6:1:C2:124 7:1:B1:89 8:1:B1:109 9:2:B1:127 11:1:B1:127 12:1:B1:127 13:1:B1:95 14:2:C2:127',
    42: '0:1:G1:94 1:1:G1:103 3:1:G1:112 4:1:G1:119 5:1:G1:96 6:1:A2:127 7:1:A2:85 8:1:G1:113 9:1:G1:110 11:1:G1:115 12:1:G1:121 13:1:G1:95 14:1:A1:127 15:1:A1:98',
    43: '0:1:B1:127 1:2:B1:127 3:1:B1:127 4:1:B1:120 5:1:B1:86 6:1:C2:127 7:1:B1:83 8:1:B1:116 9:2:B1:106 11:1:B1:120 12:1:B1:127 13:1:G#1:104 14:1:A1:127 15:1:A1:90',
    44: '0:1:B1:107 1:1:B1:121 2:1:B1:82 3:2:B1:127 5:1:C2:80 6:2:C2:121 8:1:B1:104 9:1:B1:127 10:1:B1:80 11:1:B1:111 12:1:B1:99 13:1:G#1:92 14:1:A1:127 15:1:A1:84',
    45: '0:1:G1:88 1:1:G1:98 3:1:G2:94 4:1:G1:113 5:1:G1:94 6:1:A2:108 7:1:A2:85 8:1:G#1:114 9:1:G1:127 11:1:G1:108 12:1:G#1:113 13:1:G#1:97 14:2:A1:95',
    46: '0:3:G2:93 3:2:G2:100 5:1:G#2:92 6:2:A2:122 8:1:G2:82 9:1:G2:95 11:1:G2:107 12:1:G2:98 13:1:F#2:96 14:2:F#2:104',
    47: '0:3:B1:107 3:1:B1:104 4:1:D#2:98 5:1:E2:92 6:2:F#2:113 8:1:B2:92 9:2:B2:122 11:2:B1:122 13:1:F#2:91 14:2:F#2:102',
    48: '0:1:B2:109 1:2:B2:123 3:1:B1:127 4:1:C2:107 5:1:F#2:83 6:1:F#2:103 9:1:F2:83 10:1:F#2:100 12:1:D#2:80 13:1:E2:89 14:2:F#2:107',
    49: '1:2:G2:92 3:1:G2:98 4:2:G1:101 6:2:A1:115 8:1:G#1:99 9:1:G1:93 12:1:G1:80 14:1:A1:113 15:1:A1:85',
    50: '0:3:G2:90 3:2:G2:89 5:1:A2:82 6:1:A2:116 7:1:A2:88 8:1:G2:86 9:1:G2:95 11:2:G2:92 13:1:F#2:94 14:2:F#2:103',
    51: '0:1:F#2:85 1:1:F#2:92 2:1:F#2:117 3:2:F#2:119 5:1:F#2:94 6:2:F#2:120 9:1:F#2:90 10:1:F#2:122 11:3:F#2:101 14:2:F#2:127',
    52: '0:1:G1:98 1:1:G1:93 2:1:G1:113 3:1:A2:112 4:1:G1:97 5:1:G#1:96 6:1:G1:112 8:1:G#1:103 9:1:G1:97 10:1:A1:116 11:1:B1:103 12:1:A1:115 13:1:G#1:118 14:1:A1:127 15:1:A1:91',
    53: '2:1:E1:84 3:1:E1:80 4:1:E1:85 5:1:E1:82 6:1:A1:91 9:1:B1:88 10:2:B1:97 12:1:A1:81 13:1:B1:83 14:1:B1:94 15:1:B1:83',
    54: '0:1:C2:82 1:4:B1:91 5:1:B1:97 6:2:B1:87 8:1:B1:80 9:1:B1:100 10:1:B1:100 11:2:B1:98 13:1:B1:82 14:1:A1:82 15:1:B1:83',
    55: '0:1:B1:92 1:1:B1:95 2:1:C2:86 3:1:B2:90 4:1:B2:95 5:1:B2:83 6:1:B1:80 7:1:B1:80 8:1:B1:80 9:1:B1:80 10:1:B1:88 11:1:B1:101 14:1:B1:92 15:1:B1:89',
    56: '0:1:B1:89 1:5:B1:92 8:3:B1:80 11:1:A#1:80 12:2:A1:86 14:1:A2:101 15:1:A2:97',
    57: '0:1:B1:98 1:1:B1:118 2:1:B1:106 3:1:B1:82 4:2:E1:115 6:2:A2:101 9:1:A#1:113 10:1:B1:96 12:1:E1:110 13:1:B1:116 14:2:A2:98',
    58: '1:1:B1:125 2:2:B1:112 6:1:F#3:94 8:1:E3:105 10:2:F#3:105 13:2:F#2:117 15:1:G2:87',
    59: '1:1:B1:115 2:2:B1:106 4:2:E1:109 6:1:G1:83 7:1:A1:83 8:1:E1:107 9:1:B1:113 10:2:B1:100 12:1:E1:113',
    60: '0:1:E1:109 1:1:B1:123 2:1:B1:112 3:1:B1:85 4:1:E1:119 8:1:E1:115 9:1:B1:127 10:2:B1:118 12:1:E1:114 13:1:B1:122 14:2:B1:116',
    61: '0:1:G#1:125 1:1:G#1:111 2:1:A1:121 3:1:G#1:111 5:1:F1:80',
    62: '0:1:G#1:111 1:3:G#1:119 4:1:A#1:80 6:1:D#2:90 7:1:E2:89',
    63: '3:1:G#2:87 4:1:D2:84 5:1:E2:89',
    64: '4:1:B1:85 5:2:A1:85 10:1:F1:81 11:1:F#1:92 12:1:G1:80 13:1:A#1:80',
}


def pat4(s):
    """'stap:lengte:noot:vel ...' -> [(stap, lengte, noot, vel)]"""
    out = []
    for w in s.split():
        a, b, c, v = w.split(':')
        out.append((int(a), int(b), p(c), int(v)))
    return out


def compose():
    P, CC, EX = Parts(), Parts(), Parts()
    for b in range(1, END + 1):
        t0 = (b - 1) * BAR
        sec = section(b)
        h1, h2 = HARM[b]
        nxt = HARM.get(b + 1, ('B5', 'B5'))[0]
        # ------------------------------------------------------------------ intro en lo (frasen uit het origineel)
        if b == 1:
            add(P, 'intro', t0, 0, 64, 60, 127)
        if b == 5:
            add(P, 'lo', t0, 0, 64, 60, 127)
            add(P, 'call', t0, 4, 18, p('F6'), 127)
            add(P, 'call', t0, 22, 46, p('F5'), 127)
            add(P, 'call', t0, 68, 60, p('F#5'), 127)
            for i, db in enumerate(CALL_ENV):
                CC['call'].append((t0 + 2 * i * S, 7, max(1, min(127, round(CALL_V * MELO * 10 ** ((db + 26) / 20))))))
        # ------------------------------------------------------------------ ostinato (rustige maten) / pad (grooves)
        if 5 <= b <= 12 or b >= 66:
            add(P, 'ost', t0, 0, 16, 60, 120)
            CC['ost'].append((t0, 'prog', OSTP if b <= 12 else OSTP2))
            if b in (5, 66):            # maat 66-69 liggen in het origineel 12,7 dB onder de grooves (5-12: 7-9 dB)
                CC['ost'].append((t0, 7, mv(84 if b == 5 else 50)))
        if b in PAD_OWN:              # het eigen stuk pad van deze maat (A/B met het getransponeerde pad < 0,75)
            add(P, 'pad', t0, 0, 16, 60, 120)
            CC['pad'].append((t0, 'prog', PAD_OWN[b]))
        elif 13 <= b <= 20:            # v6: hele maat 'other' 160-5000 Hz (pad + de hoge lijn erboven)
            add(P, 'pad', t0, 0, 16, 60, 120)
            CC['pad'].append((t0, 'prog', WIDE14 if b <= 16 else WIDE18))
            if b == 13:
                CC['pad'].append((t0, 7, mv(WIDE_V)))
        elif 21 <= b <= 65:            # v8: het pad zit in de knipsels van de stem 'other' (ST_PIECES)
            pass
        elif 13 <= b <= 64:
            if b == 21:
                CC['pad'].append((t0, 7, 100))
            halves = ((0, 16, h1),) if h1 == h2 else ((0, 8, h1), (8, 8, h2))
            for h, ln, ch in halves:
                root = CHORD[ch][0]
                if root == 7:          # G/Gm: het G-pad (octaven), zonder transpositie
                    add(P, 'pad', t0, h, ln, 60, 120)
                    CC['pad'].append((t0 + h * S, 'prog', PADG))
                else:
                    add(P, 'pad', t0, h, ln, 60 + SHIFT[root], 120)
                    CC['pad'].append((t0 + h * S, 'prog', PADP))
        # ------------------------------------------------------------------ strijker (vanaf maat 21, Jordi: 'vanaf 32 s mis ik de strijker')
        for i, (b1, n1) in enumerate(ST_PIECES):   # v8: de stem 'other' zelf, 2 maten per stuk
            if b1 == b:
                trk = 'str' if i % 2 == 0 else 'str2'
                add(P, trk, t0, 0, 16 * n1 + 1, 60, 127)
                CC[trk].append((t0, 'prog', ST_PROG[b1]))
                CC[trk].append((t0, 7, STR_VOL))
                add(P, trk + 'b', t0, 0, 16 * n1 + 1, 60, 127)      # v9: zelfde stuk op een tweede spoor (coherent)
                CC[trk + 'b'].append((t0, 'prog', ST_PROG[b1]))
                CC[trk + 'b'].append((t0, 7, STR_VOL_B))
        # ------------------------------------------------------------------ bas (noot voor noot uit de stem)
        if b in BASS_NOTES:
            for st, ln, n, v in pat4(BASS_NOTES[b]):
                add(P, 'bass', t0, st, ln, n, v)
        # ------------------------------------------------------------------ drums
        # (maat 1-4: de drums van de intro zitten in het intro-sample)
        if b == 5:
            add(P, 'fx', t0, 0, 16, IMPACT, 127)
            add(P, 'fx2', t0, 0, 8, CRASH, 116)
            add(P, 'tk', t0, 0, 6, TAIKO, 127)
        if sec == 'Q':
            if b == 9:      # rommelende trom (gemeten: lage aanzetten op 16e 1-9, aflopend)
                for k in range(1, 10):
                    add(P, 'tk', t0, k, 1, TAIKO_LO, 96 - 6 * k)
            if b in (11, 12):
                for k in (0, 2, 3, 4, 6, 8, 10, 11, 12, 14):
                    add(P, 'hh', t0, k, 1, HAT, 54 if k % 4 == 0 else 40)
            if b == 12:
                for k in (12, 13, 14, 15):
                    add(P, 'sn', t0, k, 1, KA, 60 + 10 * (k - 12))
        elif sec == 'U':
            for k in (0, 3, 6, 8, 11, 14):
                add(P, 'tk', t0, k, 2, TAIKO if k in (0, 8) else TAIKO_LO, 96 + 6 * (b - 13) if k in (0, 8) else 80 + 6 * (b - 13))
            if b >= 14:
                for k in (2, 10):
                    add(P, 'bm', t0, k, 2, BOOM, 80 + 6 * (b - 14))
            if b >= 15:
                for k in range(0, 16, 2):
                    add(P, 'hh', t0, k, 1, HAT, 56 if k % 4 == 0 else 44)
            if b == 16:
                P['tk'] = [d for d in P['tk'] if not (t0 + 8 * S <= d[0] < t0 + BAR)]
                for k in range(8, 16):
                    add(P, 'tk', t0, k, 1, TAIKO if k % 2 == 0 else TAIKO_LO, 84 + 5 * (k - 8))
                    add(P, 'sn', t0, k, 1, SNARE, 50 + 8 * (k - 8))
        elif sec in ('A', 'A2', 'B'):
            fill = b % 4 == 0
            # gemeten (maat 17-43, flux per band per 16e): op elke tel slaat álles tegelijk (laag, snare-band, hoog
            # 0,8-1,0), ertussen bijna niets (hats 0,1-0,35, iets meer op 16e 6 en 14)
            for k in (0, 4, 8, 12):
                if fill and k == 12:
                    continue
                add(P, 'tk', t0, k, 2, TAIKO, 120 if k == 0 else (106 if k == 8 else 100))
                if k == 0 and b % 4 == 1:
                    continue                       # de crash neemt de snare en de dreun over (kanalen)
                add(P, 'sn', t0, k, 1, SNARE, 78 if k in (0, 8) else 70)
                if k in (0, 8):
                    add(P, 'bm', t0, k, 2, BOOM, 84)
            for k in (1, 2, 3, 6, 9, 10, 11, 14):  # op de tellen klinkt de snare al
                add(P, 'hh', t0, k, 1, HAT, 92 if k in (6, 14) else 62)
            if fill:
                for k in (12, 13, 14, 15):
                    add(P, 'tk', t0, k, 1, TAIKO if k % 2 == 0 else TAIKO_LO, 96 + 8 * (k - 12))
                    add(P, 'sn', t0, k, 1, SNARE, 62 + 10 * (k - 12))
            if b % 4 == 1:
                add(P, 'fx2', t0, 0, 8, CRASH, 104 if sec == 'A2' or b in (17, 37) else 92)
        elif sec == 'R':
            for k in range(16):
                acc = k % 4 == 0
                add(P, 'tk', t0, k, 1, TAIKO if acc else TAIKO_LO, (112 if acc else 72 + 2 * (k % 4)) + 2 * (b - 53))
                add(P, 'sn', t0, k, 1, SNARE, (86 if acc else 52) + 6 * (b - 53))
            if b == 53:
                add(P, 'fx2', t0, 0, 8, CRASH, 108)
            if b == 56:
                add(P, 'fx2', t0, 12, 4, CRASH, 96)
        elif sec == 'H':
            # gemeten (maat 57-60): snare op de tellen (0,9) en de 'en' (0,4-0,6), kick op 16e 1-2, 5, 9, 13-14
            hits = (0, 2, 4, 6, 8, 10, 12, 14) if b != 59 else (0, 2, 3, 4, 6, 7, 8, 10, 11, 12, 14)
            for k in hits:
                add(P, 'sn', t0, k, 1, SNARE, 104 if k % 4 == 0 else 70)
            for k in (1, 5, 9, 13):
                add(P, 'bm', t0, k, 2, KICK, 104)
            for k in (2, 14):
                add(P, 'tk', t0, k, 1, TAIKO_LO, 70)
            for k in range(16):
                if k not in (5, 15):
                    add(P, 'hh', t0, k, 1, HAT, 64 if k % 4 == 0 else 46)
            if b == 57:
                add(P, 'fx2', t0, 0, 8, CRASH, 104)
            if b == 60:
                P['sn'] = [d for d in P['sn'] if not (t0 + 12 * S <= d[0] < t0 + BAR)]
                for k in (12, 13, 14, 15):
                    add(P, 'sn', t0, k, 1, SNARE, 80 + 10 * (k - 12))
        elif sec == 'K':
            start = 8 if b == 61 else 0
            for k in range(16):
                if b == 61 and k < 8:
                    if k in (0, 2, 3, 4, 6):
                        add(P, 'tk', t0, k, 1, TAIKO if k in (0, 4) else TAIKO_LO, 112 if k in (0, 4) else 84)
                    continue
                acc = k % 4 == 0
                add(P, 'tk', t0, k, 1, TAIKO if acc else TAIKO_LO, min(127, (108 if acc else 74) + 5 * (b - 61)))
                add(P, 'sn', t0, k, 1, SNARE, min(127, (78 if acc else 50) + 9 * (b - 61) + 2 * (k - start) // 2))
            for k in (2, 6, 10, 14):
                add(P, 'bm', t0, k, 2, BOOM, 84 + 4 * (b - 61))
            if b == 61:
                add(P, 'fx2', t0, 0, 8, CRASH, 108)
        elif sec == 'X':
            for k in (3, 4, 9):
                add(P, 'bm', t0, k, 2, BOOM, 92 - 10 * (k // 4))
        elif sec == 'Q2' and b == 69:
            for k in (12, 13, 14, 15):
                add(P, 'tk', t0, k, 1, TAIKO_LO, 64 + 12 * (k - 12))
                add(P, 'sn', t0, k, 1, KA, 58 + 12 * (k - 12))
    return P, CC, EX


# ---- voicegroup, keysplits, drumkit -------------------------------------------------------------------------------
KIT = [   # vanaf noot 36: (regel, lengte van de sample in s; None = geloopt)
    ('voice_directsound 60, 64, DirectSoundWaveData_ruinous_taiko, 255, 0, 255, 170', 0.50),
    ('voice_directsound 60, 64, DirectSoundWaveData_ruinous_boom, 255, 0, 255, 150', 0.24),
    ('voice_directsound 60, 64, DirectSoundWaveData_ruinous_ka, 255, 0, 255, 100', 0.10),
    ('voice_directsound 60, 64, DirectSoundWaveData_ruinous_impact, 255, 0, 255, 200', 1.10),
    ('voice_directsound 60, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 170', None),
    ('voice_directsound 60, 64, DirectSoundWaveData_unknown_close_hihat, 255, 0, 255, 80', 0.08),
    ('voice_directsound 60, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 120', 0.16),
    ('voice_directsound 55, 64, DirectSoundWaveData_ruinous_taiko, 255, 0, 255, 150', 0.67),
    ('voice_directsound 60, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 120', 0.29),
]
KEYSPLITS = {}   # naam: (tabel, [(sample, sustain, release)]); v5 had hier de stock-strijkers (v6: eigen knipsel)
VOICES = {
    LO: 'voice_directsound 60, 0, DirectSoundWaveData_ruinous_lo58, 255, 0, 255, 160',
    OSTP: 'voice_directsound 60, 0, DirectSoundWaveData_ruinous_ostbar, 255, 0, 255, 140',
    OSTP2: 'voice_directsound 60, 0, DirectSoundWaveData_ruinous_ostbar2, 255, 0, 255, 140',
    INTROP: 'voice_directsound 60, 0, DirectSoundWaveData_ruinous_intro, 255, 0, 255, 160',
    BASS: 'voice_directsound 60, 0, DirectSoundWaveData_ruinous_bass, 255, 0, 255, 100',
    DRUMS: 'voice_keysplit_all voicegroup_ruinous_drumset',
    CALL: 'voice_directsound 60, 0, DirectSoundWaveData_ruinous_call, 120, 0, 255, 170',
    WIDE14: 'voice_directsound 60, 0, DirectSoundWaveData_ruinous_wide14, 255, 0, 255, 140',
    WIDE18: 'voice_directsound 60, 0, DirectSoundWaveData_ruinous_wide18, 255, 0, 255, 140',
}
for _b, _p in ST_PROG.items():
    VOICES[_p] = 'voice_directsound 60, 0, DirectSoundWaveData_ruinous_st%d, 255, 0, 255, 200' % _b
for _b, _p in PAD_OWN.items():
    VOICES[_p] = 'voice_directsound 60, 0, DirectSoundWaveData_ruinous_pad_m%d, 255, 0, 255, 140' % _b

def write_voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Battle! Treasures of Ruin. Gegenereerd door tools/grounded/ruinous_theme.py.'
    lines[1] = ('@ samples uit het origineel (ruinous_samples.py): 107 laag Aziatisch instrument (maat 5-8), '
                '82/83 ostinato (maat 8 / 67), 84/86 pad (B/G), 85 intro (maat 1-4), 87 roep, 88/89 maat 13-20, 48 strijker, '
                '33 bas; 127 = drumkit ruinous.')
    lines[2] = 'voice_group %s' % VG
    out = []
    for l in lines:
        if l.startswith('\t') and '@' in l:
            prog = int(l.rsplit('@', 1)[1])
            if prog in VOICES:
                l = '\t%s  @ %d' % (VOICES[prog], prog)
        out.append(l)
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    open('sound/voicegroups/drumsets/ruinous.inc', 'w').write(
        '@ Project Grounded: drumkit voor Battle! Treasures of Ruin (ruinous_theme.py): 36 taiko, 37 lage dreun, 38 ka,\n'
        '@ 39 inslag, 40 crash, 41 hihat, 42 orkestsnare (roffels), 43 lage taiko, 44 kick.\n'
        '@ ruinous_* = eigen samples (ruinous_samples.py).\n'
        'voice_group ruinous_drumset, 36\n' + ''.join('\t%s\n' % k for k, _ in KIT) + '\n')
    for name, (table, samples) in KEYSPLITS.items():
        open('sound/voicegroups/keysplits/%s.inc' % name, 'w').write(
            '@ Project Grounded: Battle! Treasures of Ruin, %s (samples uit het origineel; tabel keysplit_%s).\n'
            '@ Gegenereerd door tools/grounded/ruinous_theme.py.\n'
            'voice_group %s_keysplit\n' % (name, table, name) +
            ''.join('\tvoice_directsound 60, 0, DirectSoundWaveData_%s, 255, 0, %d, %d\n' % (s, su, r) for s, su, r in samples))


# ---- bouwen ---------------------------------------------------------------------------------------------------------
TRACKS = [   # (naam, programma, volume, pan)
    ('tk', DRUMS, 127, 64), ('bm', DRUMS, dv(100), 64), ('sn', DRUMS, dv(84), 70), ('hh', DRUMS, dv(40), 76),
    ('fx', DRUMS, dv(110), 64), ('fx2', DRUMS, dv(80), 58),
    ('bass', BASS, 78, 64), ('ost', OSTP, mv(84), 60), ('pad', PADP, mv(100), 64), ('lo', LO, mv(30), 64),   # balans gemeten t.o.v. de drums (stems)
    ('intro', INTROP, mv(55), 64),   # v9: 49 -> 55 (de opening zat op RMS ±600-1300: ruisvloer van de uitgang)
    ('str', 40, 100, 64),
    ('str2', 41, 100, 64),
    ('strb', 40, 100, 64),
    ('str2b', 41, 100, 64),
    ('call', CALL, 1, 58),   # even luid als het pad (gemeten in de stem 'other')   # het origineel ligt in maat 1-4 15,5 dB onder de grooves (gemeten)
]
PSG = set()
ORDER = ['intro', 'tk', 'bm', 'fx', 'bass', 'call', 'str', 'str2', 'strb', 'str2b', 'lo', 'ost', 'pad', 'fx2', 'sn', 'hh']
DRUMPARTS = ('tk', 'bm', 'sn', 'hh', 'fx', 'fx2')
# hoe lang een slag mag doorklinken (16en); de volgende slag in dezelfde partij kapt eerder
RING = {TAIKO: 4, BOOM: 2, KA: 1, IMPACT: 16, CRASH: 6, HAT: 1, SNARE: 1, TAIKO_LO: 3, KICK: 2}
FREE = (CRASH, IMPACT)


def kit_rel(n):
    return int(KIT[n - 36][0].rsplit(',', 1)[1])


def ring_gates(notes):
    notes = sorted(notes)
    starts = sorted({n[0] for n in notes if n[2] not in FREE})
    out = []
    for n in notes:
        ln = RING.get(n[2], 2) * S
        if n[2] not in FREE:
            nxt = next((x for x in starts if x > n[0]), None)
            if nxt is not None:
                r = release_ticks(kit_rel(n[2]), TPB, BPM) + 1
                ln = min(ln, max(3, nxt - n[0] - r))
        out.append([n[0], n[0] + ln, n[2], n[3]])
    return out


def tight(ev, tail):
    """tokkels/stoten: noot + uitklinktijd past tot de volgende aanslag (min. 3 ticks)."""
    ev = sorted(ev)
    starts = sorted(set(e[0] for e in ev))
    out = []
    for e in ev:
        nxt = next((t for t in starts if t > e[0]), None)
        end = e[1] if nxt is None else min(e[1], max(e[0] + 3, nxt - tail))
        out.append([e[0], end, e[2], e[3]])
    return out


def no_overlap(ev):
    ev = sorted(ev)
    for i, e in enumerate(ev):
        nxt = next((x[0] for x in ev[i + 1:] if x[2] == e[2] and x[0] >= e[0] and x is not e), None)
        if nxt is not None and nxt < e[1]:
            e[1] = max(e[0] + 1, nxt)
    return ev


def build(render_dir=None):
    write_voicegroup()
    rel = releases(VG)
    P, CC, EX = compose()
    parts = {k: dedupe(v) for k, v in P.items()}
    progs = {k: pr for k, pr, _, _ in TRACKS}
    tail = {}
    for k, pr in progs.items():
        tail[k] = 0 if (k in PSG or pr == DRUMS) else release_ticks(rel.get(pr, 200), TPB, BPM) + 2
    for k in ('lo',):
        if k in parts:
            parts[k] = detach(parts[k], tail[k])
    for k in ('bass',):
        if k in parts:
            parts[k] = tight(parts[k], tail[k])
    for k in DRUMPARTS:
        if k in parts:
            parts[k] = ring_gates(parts[k])
    for k in parts:
        parts[k] = no_overlap(parts[k])
    for k, pr in progs.items():
        if pr == DRUMS:
            continue
        assert all(n >= p('E1') for _, _, n, _ in parts.get(k, [])), '%s: noten onder E1' % k
    proxy = {}
    for k in DRUMPARTS:
        proxy[k] = []
        for i, (s0, e0, n, v) in enumerate(parts.get(k, [])):
            line, slen = KIT[n - 36]
            occ = e0 - s0 + release_ticks(kit_rel(n), TPB, BPM) + 2
            if slen is not None:
                key = int(line.split()[1].rstrip(','))
                sec = slen * (2 ** ((60 - key) / 12) if 'no_resample' not in line else 1)
                occ = min(occ, int(sec * BPM / 60 * TPB) + 1)
            proxy[k].append([s0, s0 + occ, n, v, i])
    alloc_in = {k: (proxy[k] if k in proxy else parts.get(k, [])) for k in ORDER}
    kept = allocate(alloc_in, ORDER, tail, max_voices=MAX_V)
    for k in proxy:
        idx = {e[4] for e in kept[k]}
        kept[k] = [e for i, e in enumerate(parts.get(k, [])) if i in idx]
    parts['tk'] = [[a, b, n, dv(v)] for a, b, n, v in parts.get('tk', [])]   # v9: taiko staat al op volume 127
    for k in ORDER:
        n = len(parts.get(k, []))
        weg = [e for e in parts.get(k, []) if e not in kept[k]]
        gone = sorted({e[0] // BAR + 1 for e in weg})
        if "-v" in sys.argv and weg:
            print("     ", [(e[0] // BAR + 1, (e[0] % BAR) // S, e[2]) for e in weg])
        print('  %-5s %4d noten, %3d vallen weg (%.1f%%)%s' % (k, n, len(weg), 100 * len(weg) / max(n, 1),
                                                            ' (maten %s)' % gone[:16] if gone else ''))
        parts[k] = kept[k]
    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.tempo(INTRO * BAR, BPM / 120)
    song.loop = (INTRO * BAR, END * BAR)
    for ch, (k, prog, vol, pan) in enumerate(TRACKS):
        notes = sorted(parts.get(k, []))
        song.add(notes, prog, vol, ch, pan, extra=list(EX.get(k, [])), ccs=list(CC.get(k, [])))
    song.save(OUT, END * BAR)
    print(OUT, 'intro %.2f s, loop %.1f s' % (INTRO * 4 * 60 / BPM, (END - INTRO) * 4 * 60 / BPM))
    if render_dir:
        render_gm(render_dir)


# ---- offline-render (FluidR3 GM; andere klanken dan de GBA, wel noten/vorm/tempo) ------------------------------------
GM_PROG = {'str': 48, 'bass': 33, 'ost': 89, 'pad': 89, 'lo': 107, 'intro': 89}
GM_DRUM = {TAIKO: 41, BOOM: 35, KA: 37, IMPACT: 49, CRASH: 57, HAT: 42, SNARE: 38, TAIKO_LO: 43, KICK: 36}


def render_gm(outdir, seconds=None):
    os.makedirs(outdir, exist_ok=True)
    m = mido.MidiFile(OUT)
    gm = mido.MidiFile(type=1, ticks_per_beat=m.ticks_per_beat)
    gm.tracks.append(m.tracks[0])
    free = [c for c in range(16) if c != 9]
    for i, (k, prog, vol, pan) in enumerate(TRACKS):
        drum = prog == DRUMS
        ch = 9 if drum else free.pop(0)
        t = mido.MidiTrack()
        for x in m.tracks[i + 1]:
            if x.type == 'program_change':
                x = x.copy(channel=ch, program=0 if drum else GM_PROG[k])
            elif x.type in ('note_on', 'note_off') and drum:
                x = x.copy(channel=ch, note=GM_DRUM.get(x.note, 47))
            elif hasattr(x, 'channel'):
                x = x.copy(channel=ch)
            t.append(x)
        gm.tracks.append(t)
    mid = os.path.join(outdir, 'ruinous_gm.mid')
    gm.save(mid)
    wav = os.path.join(outdir, 'ruinous_fluidr3.wav')
    subprocess.run(['fluidsynth', '-ni', '-g', '0.5', '-r', '22050', '-F', wav, '/usr/share/sounds/sf2/FluidR3_GM.sf2',
                    mid], check=True, capture_output=True)
    print('render:', wav)


if __name__ == '__main__':
    build(sys.argv[sys.argv.index('--render') + 1] if '--render' in sys.argv else None)
