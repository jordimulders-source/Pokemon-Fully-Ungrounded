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

LO, OSTP, BASS, DRUMS = 107, 82, 33, 127
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
# v3: noten van de laag 'lo' per 16e: 'stap:lengte:noot' (dominante toon per 16e in de stem 'piano'; B1/A1 een octaaf
# hoger). De halve-maat-lagen (ost, oth) dragen hun eigen noten (geknipt uit het origineel).
LO_NOTES = {
    1: '1:7:E2 8:1:B2 9:7:B3', 2: '0:1:B3 1:1:E4 2:1:B3 3:2:B2 7:2:D#4 13:3:B3',
    3: '1:7:F#2 8:3:B2 11:3:A2 14:2:B2', 4: '0:1:F#3 1:1:F#4 2:2:A#4 4:2:G#4',
    5: '0:15:B3 15:1:B2', 6: '0:2:B3', 7: '8:5:B3', 8: '0:1:B3 1:3:F#4',
    # (v3: de hogere lijn vanaf maat 23 in de stem 'piano' bleef in de A/B onherkenbaar (chroma 0-0,4 per maat) en
    # draagt maar 0,2% van de energie: weggelaten - liever weinig lagen die kloppen)
}
# transpositie van het ostinato-knipsel (B3 = 59) per grondtoon (gemeten: B, E omhoog, G omlaag)
SHIFT = {11: 0, 4: 5, 7: -4, 6: -5, 9: -2, 8: -3, 1: 2, 2: 3}
# akkoord -> (halve-maat-sample uit 'other', transpositie); zonder eigen knipsel: het dichtstbijzijnde getransponeerd
OTH_OF = {'B5': ('B', 0), 'B': ('B', 0), 'B7': ('B', 0), 'B11': ('B', 0), 'Bo': ('Bm', 0), 'Bm': ('Bm', 0),
          'E': ('E', 0), 'Emaj': ('E', 0), 'Em': ('Em', 0), 'G': ('G', 0), 'Gm': ('Gm', 0), 'F#': ('Fs', 0),
          'F#m': ('Fs', 0), 'DA': ('DA', 0), 'A': ('A', 0), 'G#m': ('Bm', -3), 'C#': ('Fs', -5), 'G#': ('Bm', -3)}
OTH_TAGS = ('B', 'E', 'G', 'Gm', 'Bm', 'Fs', 'DA', 'Em', 'A')
OTH_PROG = {t: 84 + i for i, t in enumerate(OTH_TAGS)}


def compose():
    P, CC, EX = Parts(), Parts(), Parts()
    for b in range(1, END + 1):
        t0 = (b - 1) * BAR
        sec = section(b)
        h1, h2 = HARM[b]
        nxt = HARM.get(b + 1, ('B5', 'B5'))[0]
        # ------------------------------------------------------------------ lo (het lage Aziatische instrument)
        if b in LO_NOTES:
            for st, ln, n in pat(LO_NOTES[b]):
                if n < p('C2'):
                    n += 12
                add(P, 'lo', t0, st, ln, n, 116 if ln >= 2 else 108)
        # ------------------------------------------------------------------ 'other': pad + figuur (halve maten)
        if 5 <= b <= 12 or b >= 66:            # rustige maten: het ostinato-pad uit maat 67
            for h, ch in ((0, h1), (8, h2)):
                add(P, 'ost', t0, h, 8, 59 + SHIFT[CHORD[ch][0]], 112)
        elif 13 <= b <= 64:                    # de halve maat van het origineel met hetzelfde akkoord
            for h, ch in ((0, h1), (8, h2)):
                tag, sh = OTH_OF[ch]
                add(P, 'oth', t0, h, 8, 60 + sh, 112)
                CC['oth'].append((t0 + h * S, 'prog', OTH_PROG[tag]))
        # ------------------------------------------------------------------ bas
        if sec in ('A', 'A2', 'B'):
            for h, ch in ((0, h1), (8, h2)):
                root, _, nb = CHORD[ch]
                R = near(root, p('A1'))                  # register van het origineel (B1, E2, G2, F#2)
                hi = h == 8 and root == 11 and b % 2 == 1  # B2-sprong op de tweede helft (gemeten in oneven maten)
                steps = ((0, 1, R), (1, 1, R), (3, 2, R), (6, 2, R + nb))
                if h == 8:
                    nroot = CHORD[nxt][0]
                    tgt = near(nroot, p('A1'))
                    appr = (tgt + 1 if b % 2 == 1 else tgt - 2) if nroot == root else tgt - 1
                    steps = ((0, 1, R + (12 if hi else 0)), (1, 1, R + (12 if hi else 0)), (3, 1, R), (4, 1, R),
                             (6, 2, appr))
                for st, ln, n in steps:
                    add(P, 'bass', t0, h + st, ln, n, 116 if st == 0 else 104)
        elif sec == 'U' and b == 16:
            for st, ln, n in pat('10:2:D2 12:1:D2 13:1:D2 14:1:D2 15:1:C#2'):
                add(P, 'bass', t0, st, ln, n, 108)
        elif sec == 'R':
            for st, ln, n in pat('0:2:B1 3:1:B1 4:1:B1 9:2:B2 12:1:B1 13:1:A1 14:2:Bb1'):
                add(P, 'bass', t0, st, ln, n, 110)
        elif sec == 'H':
            root = CHORD[h1][0]
            R = near(root, p('A1'))
            for st, ln, n in ((0, 2, R), (3, 1, R), (4, 2, R + 5), (6, 2, R + 10), (8, 2, R), (11, 1, R),
                              (12, 2, R + 7), (14, 2, R + 5)):
                add(P, 'bass', t0, st, ln, n, 112 if st in (0, 8) else 102)
        elif sec == 'K':
            ph = {61: '0:2:G1 3:2:Ab1 6:2:A1 8:2:G1 11:2:Ab1 14:2:A1', 62: '0:2:G1 3:2:Ab1 6:4:Eb2 10:6:E2',
                  63: '0:3:Ab1 3:3:Eb2 6:2:E2 8:3:Ab1 11:3:Eb2 14:2:E2',
                  64: '0:3:Ab1 4:2:B1 6:2:Ab1 8:2:A1 10:2:F1 12:2:F1 14:2:F#1'}[b]
            for st, ln, n in pat(ph):
                add(P, 'bass', t0, st, ln, n, 112)
        elif sec == 'Q' and b == 5:
            add(P, 'bass', t0, 0, 6, p('E2'), 108)            # de inslag-dreun van het origineel (E2)
        # ------------------------------------------------------------------ drums
        if b == 2:     # de twee zachte dreunen van het origineel (maat 2: kick op 16e 4 en 7)
            add(P, 'bm', t0, 4, 2, BOOM, 70); add(P, 'bm', t0, 7, 2, BOOM, 62)
        if b == 4:     # aanloop naar de inslag: taiko-roffel aanzwellend
            for k in range(8, 16):
                add(P, 'tk', t0, k, 1, TAIKO_LO, 70 + 6 * (k - 8))
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
KEYSPLITS = {   # naam: (tabel, [(sample, sustain, release)])
    'ruinous_lo': ('ruinous_lo', [('ruinous_lo_e2', 255, 150), ('ruinous_lo_b3', 255, 150)]),
}
VOICES = {
    LO: 'voice_keysplit voicegroup_ruinous_lo_keysplit, keysplit_ruinous_lo',
    OSTP: 'voice_directsound 60, 0, DirectSoundWaveData_ruinous_ostbar, 255, 0, 255, 140',
    BASS: 'voice_directsound 60, 0, DirectSoundWaveData_ruinous_bass, 255, 0, 255, 100',
    DRUMS: 'voice_keysplit_all voicegroup_ruinous_drumset',
}
for _t, _p in OTH_PROG.items():
    VOICES[_p] = 'voice_directsound 60, 0, DirectSoundWaveData_ruinous_oth_%s, 255, 0, 255, 140' % _t


def write_voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Battle! Treasures of Ruin. Gegenereerd door tools/grounded/ruinous_theme.py.'
    lines[1] = ('@ samples uit het origineel (ruinous_samples.py): 107 laag Aziatisch instrument (keysplit ruinous_lo), '
                '82 ostinato-pad (maat 67), 84-92 stem other per akkoord, 33 bas; 127 = drumkit ruinous.')
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
    ('tk', DRUMS, 127, 64), ('bm', DRUMS, 100, 64), ('sn', DRUMS, 84, 70), ('hh', DRUMS, 40, 76),
    ('fx', DRUMS, 110, 64), ('fx2', DRUMS, 80, 58),
    ('bass', BASS, 104, 64), ('ost', OSTP, 100, 60), ('oth', 84, 100, 64), ('lo', LO, 110, 64),
]
PSG = set()
ORDER = ['tk', 'bm', 'fx', 'bass', 'lo', 'ost', 'oth', 'fx2', 'sn', 'hh']
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
GM_PROG = {'bass': 33, 'ost': 89, 'oth': 89, 'lo': 107}
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
