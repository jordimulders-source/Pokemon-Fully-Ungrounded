#!/usr/bin/env python3
"""Project Grounded: "Battle! Treasures of Ruin" (song 683, MUS_GROUNDED_VS_RUINOUS): het gevechtsthema van Wo-Chien,
Chien-Pao, Ting-Lu en Chi-Yu (Pokémon Scarlet/Violet) in GBA-stijl, v1.

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
Instrumenten: eigen samples (tools/grounded/ruinous_samples.py, voorvoegsel ruinous_*, ±25 KB): drumkit
drumsets/ruinous.inc (taiko, lage dreun, ka, inslag; stock crash/hihat/orkestsnare/lage taiko), 82 elektronisch
ostinato (ruinous_synth); stock: 107 koto (unknown_koto_high, klinkt een octaaf hoger: noten -12), 33 fingered bass,
48 strijkers, 60 hoorn, 56 trompet (eigen keysplits met kortere release), PSG: 80 blokgolf (ostinato een octaaf hoger,
'elektronisch'), 81 blokgolf (twinkelingen).
Laag (Jordi's speakers): niets onder C2 op DirectSound; de bas staat een octaaf hoger dan in het origineel (B2), de lage
dreun op 62-78 Hz en zachter dan de taiko.
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

STR, HORN, TPT, KOTO, SYN, BASS, SQ1, SQ2, DRUMS = 48, 60, 56, 107, 82, 33, 80, 81, 127
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
OST = (0, 1, 3, 4, 6)                         # het ostinato-ritme per halve maat (gemeten: maat 5-12 en 66-69)
# trompet (maat 6-12): de roep van de 'vocals'-stem (basic-pitch), F5 -> F#5
CALL = {6: '10:2:F5 12:2:F5', 7: '12:1:F5 13:2:F5 15:1:F5', 8: '0:4:F5 4:3:F5 7:2:F5 9:2:F5 11:4:F5',
        9: '4:2:F#5 6:2:F#5 11:1:F#5 12:2:F#5 14:2:F#5', 10: '1:2:F#5 5:1:F#5 6:2:F#5 8:2:F#5 10:1:F#5 11:2:F#5 13:3:F#5',
        11: '3:3:F#5 6:2:F#5 8:3:F#5 11:1:F#5 12:1:F#5 13:2:F#5',
        12: '0:1:F#5 1:3:F#5 4:1:F#5 5:2:F#5 7:2:F#5 9:2:F#5 11:2:F#5 13:2:F#5 15:1:F#5'}
FANFARE = '0:2:F#5 2:5:F#5 9:2:F#5 11:4:F#5'           # maat 31/47 (de herhaalde F#5-figuur)
FANFARE2 = '0:2:F#5 3:1:F#5 4:1:F#5 5:3:F#5 9:5:F#5 14:2:E5'
PAIRS = '4:1:F#4 5:2:F#4 8:1:A4 9:2:A4 12:1:B4 13:2:B4'  # maat 30/34/46/50: stijgende paren (vocals-stem)
FALL = {35: '0:2:F#5 2:2:F#5 4:6:F#5 12:2:E5 14:2:C#5', 36: '0:6:F#4 6:1:G4 7:3:G4 11:1:D5 12:1:C#5 13:3:D5',
        51: '0:2:F#5 2:2:F#5 4:6:F#5 12:2:G5 14:2:A5', 52: '0:6:F#5 6:1:E5 7:3:E5 11:1:C#5 12:1:B4 13:3:C#5'}
# koto: per akkoord een cel (a a . b b . c .) uit akkoordtonen in G4-D6; per maat wisselt de richting
KOTO_SET = {'B5': ('F#5', 'B5', 'C#6', 'B5', 'F#5', 'E5'), 'B': ('F#5', 'B5', 'D#6', 'B5', 'F#5', 'D#5'),
            'Bm': ('F#5', 'B5', 'D6', 'B5', 'F#5', 'D5'), 'B7': ('D#5', 'F#5', 'A5', 'F#5', 'D#5', 'B4'),
            'E': ('E5', 'B5', 'F#5', 'E5', 'B4', 'F#5'), 'Em': ('E5', 'G5', 'B5', 'G5', 'E5', 'B4'),
            'Gm': ('G5', 'Bb5', 'D6', 'Bb5', 'G5', 'D5'), 'G': ('D5', 'G5', 'B5', 'F#5', 'D5', 'C#6'),
            'F#': ('F#5', 'G#5', 'C#6', 'G#5', 'F#5', 'C#5'), 'DA': ('A4', 'D5', 'F#5', 'C#6', 'A5', 'F#5'),
            'A': ('A4', 'C#5', 'E5', 'C#5', 'A4', 'E5'), 'Bo': ('D5', 'F5', 'A5', 'F5', 'D5', 'B4'),
            'B11': ('E5', 'F#5', 'A5', 'F#5', 'E5', 'B4')}


TPT_BARS = set(CALL) | {30, 31, 32, 34, 35, 36, 46, 47, 48, 50, 51, 52}


def compose():
    P, CC, EX = Parts(), Parts(), Parts()
    rng = np.random.default_rng(683)
    for b in range(1, END + 1):
        t0 = (b - 1) * BAR
        sec = section(b)
        h1, h2 = HARM[b]
        nxt = HARM.get(b + 1, ('B5', 'B5'))[0]
        # ------------------------------------------------------------------ intro: zwevend akkoord + twinkelingen
        if sec == 'I':
            ch = h1
            vo = [p('B3'), p('E4'), p('F#4'), p('D#5')] if ch == 'Bmaj' else [p('C#4'), p('F#4'), p('G#4'), p('A#4')]
            for h in (0, 8):
                for n in vo:
                    add(P, 'str', t0, h, 8, n, 52 + 10 * (b % 2) if h == 0 else 60)
            # twinkelingen: los ritme (12-36 ticks), noten uit het akkoord in F#5-Eb6, aanzwellend en weer weg
            pool = [p(x) for x in (('F#5', 'G#5', 'A5', 'B5', 'D#6', 'E6') if ch == 'Bmaj' else ('F5', 'F#5', 'G#5', 'B5', 'C#6'))]
            t = t0 + int(rng.integers(0, 12))
            while t < t0 + BAR - 6:
                ln = int(rng.choice((12, 12, 18, 24, 30, 36)))
                env = 0.5 + 0.5 * np.sin(np.pi * ((t - t0) / BAR))
                P['sq2'].append([t, t + min(ln, 18), int(rng.choice(pool)), int(64 + 50 * env * rng.uniform(0.6, 1.0))])
                t += ln
            if b == 2:     # de twee zachte dreunen van het origineel (maat 2: kick op 16e 4 en 7)
                add(P, 'bm', t0, 4, 2, BOOM, 70); add(P, 'bm', t0, 7, 2, BOOM, 62)
            if b == 4:     # aanloop naar de inslag: taiko-roffel aanzwellend + strijkers B-F# ontstaan
                for k in range(8, 16):
                    add(P, 'tk', t0, k, 1, TAIKO_LO, 40 + 9 * (k - 8))
            continue
        r1, r2 = CHORD[h1][0], CHORD[h2][0]
        # ------------------------------------------------------------------ ostinato (elektronisch, de hele loop)
        if sec in ('Q', 'U', 'A', 'A2', 'B', 'R', 'H', 'K', 'Q2'):
            for h, ch in ((0, h1), (8, h2)):
                root, _, nb = CHORD[ch]
                base = near(root, p('A2'))           # A2-G#3: rond het origineel (B2/B3)
                for k in OST:
                    n = base + (nb if k == 6 else 0)
                    v = 104 if k == 0 else (92 if k == 3 else 80)
                    add(P, 'syn', t0, h + k, 1, n, v)
                    add(P, 'sq1', t0, h + k, 1, n + 12, 76 if k in (0, 3) else 60)
        # ------------------------------------------------------------------ bourdon / akkoorden (strijkers)
        if sec in ('Q', 'Q2', 'U'):
            vo = [p('B3'), p('F#4')] + ([p('E4')] if (sec == 'U' and b % 2 == 0) or (sec == 'Q2' and b % 2 == 1) else [])
            for h in (0, 8):
                for n in vo:
                    add(P, 'str', t0, h, 8, n, 66 if sec != 'U' else 74 + 3 * (b - 13))
            if b in (5, 13):
                add(P, 'str', t0, 0, 16, p('B2'), 70)
        elif sec in ('A', 'A2', 'B', 'R', 'H', 'K'):
            for h, ch in ((0, h1), (8, h2)):
                lo = p('F#3') if sec != 'R' else p('A3')
                horns = sec in ('A', 'A2', 'B') and not (sec == 'A' and b < 21)
                vo = voicing(ch, p('B3') if horns else lo, 2 if horns or sec == 'K' else 3)     # met hoorns erbij: 2 stemmen, hoger
                if b in TPT_BARS or b == 53:
                    vo = vo[1:]                    # trompet erbij: één strijkersstem (kanalen)
                for n in vo:
                    add(P, 'str', t0, h, 8, n, 84 if sec in ('A', 'B', 'A2') else 92)
        elif sec == 'X':          # gemeten: één vastgehouden G# (Ab6 bovenin), verder niets
            for n in (p('G#3'), p('G#4'), p('G#5')):
                add(P, 'str', t0, 0, 16, n, 96)
        # ------------------------------------------------------------------ hoorns: felle lange tonen
        if sec in ('A', 'A2', 'B') and not (sec == 'A' and b < 21):
            if b % 2 == 1 or h1 != h2 or HARM[b - 1] != HARM[b]:
                for h, ch in ((0, h1), (8, h2)) if h1 != h2 else ((0, h1),):
                    root = CHORD[ch][0]
                    lo = near(root, p('F#3'))
                    ln = 8 if h1 != h2 else 16
                    for n in (lo, lo + 7 if (lo + 7) % 12 in CHORD[ch][1] else lo + 12):
                        add(P, 'horn', t0, h, ln, n, 96)
        elif sec == 'U' and b >= 15:
            for n in (p('B3'), p('F#4')):
                add(P, 'horn', t0, 0, 16, n, 70 + 18 * (b - 15))
        elif sec == 'K':
            line = {61: ('G4', 'A4'), 62: ('Bb4', 'B4'), 63: ('B4', 'C#5'), 64: ('D#5', 'F#5')}[b]
            for h, nm in zip((0, 8), line):
                add(P, 'horn', t0, h, 8, p(nm), 96 + 4 * (b - 61))
                add(P, 'horn', t0, h, 8, p(nm) - 12, 88 + 4 * (b - 61))
        elif sec == 'X':
            add(P, 'horn', t0, 0, 12, p('G#4'), 104)
        # ------------------------------------------------------------------ bas
        if sec in ('A', 'A2', 'B'):
            for h, ch in ((0, h1), (8, h2)):
                root, _, nb = CHORD[ch]
                R = near(root, p('C2'))
                hi = h == 8 and ch in ('B5', 'B', 'Bm') and b % 2 == 1      # octaafsprong op de tweede helft
                steps = ((0, 1, R), (1, 1, R), (3, 2, R), (6, 2, R + nb))
                if h == 8:
                    nroot = CHORD[nxt][0]
                    tgt = near(nroot, p('C2'))
                    appr = (tgt + 1 if b % 2 == 1 else tgt - 2) if nroot == root else tgt - 1
                    if appr < p('C2'):
                        appr += 12
                    steps = ((0, 1, R + (12 if hi else 0)), (1, 1, R + (12 if hi else 0)), (3, 1, R), (4, 1, R),
                             (6, 2, appr))
                for st, ln, n in steps:
                    add(P, 'bass', t0, h + st, ln, n, 112 if st == 0 else 98)
        elif sec == 'U':
            ph = {16: '10:2:D3 12:1:D3 13:1:D3 14:1:D3 15:1:C#3'}.get(b)
            if ph:
                for st, ln, n in pat(ph):
                    add(P, 'bass', t0, st, ln, n, 104)
        elif sec == 'R':
            for st, ln, n in pat('0:2:B2 3:1:B2 4:1:B2 9:2:B2 12:1:B2 13:1:A2 14:2:Bb2'):
                add(P, 'bass', t0, st, ln, n, 106)
        elif sec == 'H':
            root = CHORD[h1][0]
            R = near(root, p('C2'))
            for st, ln, n in ((0, 2, R), (3, 1, R), (4, 2, R + 5), (6, 2, R - 2 + (12 if R - 2 < p('C2') else 0)),
                              (8, 2, R), (11, 1, R), (12, 2, R + 7), (14, 2, R + 5)):
                add(P, 'bass', t0, st, ln, n, 108 if st in (0, 8) else 96)
        elif sec == 'K':
            ph = {61: '0:2:G2 3:2:Ab2 6:2:A2 8:2:G2 11:2:Ab2 14:2:A2', 62: '0:2:G2 3:2:Ab2 6:4:Eb3 10:6:E3',
                  63: '0:3:Ab2 3:3:Eb3 6:2:E3 8:3:Ab2 11:3:Eb3 14:2:E3',
                  64: '0:3:Ab2 4:2:B2 6:2:Ab2 8:2:A2 10:2:F2 12:2:F2 14:2:F#2'}[b]
            for st, ln, n in pat(ph):
                add(P, 'bass', t0, st, ln, n, 110)
        elif sec == 'Q' and b == 5:
            add(P, 'bass', t0, 0, 6, p('E2'), 100)            # de inslag-dreun van het origineel (E2)
        # ------------------------------------------------------------------ koto (oosters, vanaf maat 21)
        if (sec in ('A', 'A2', 'B', 'H') and not (sec == 'A' and b < 21)) and b not in (31, 32, 47, 48):
            for h, ch in ((0, h1), (8, h2)):
                cell = KOTO_SET[ch]
                c = cell[:3] if (b + h // 8) % 2 == 0 else cell[3:]
                for k, n in zip(OST, (c[0], c[0], c[1], c[1], c[2])):
                    add(P, 'koto', t0, h + k, 1, p(n) - 12, 104 if k in (0, 3) else 86)   # unknown_koto_high: +12
        # ------------------------------------------------------------------ trompet
        if b in CALL:
            for st, ln, n in pat(CALL[b]):
                add(P, 'tpt', t0, st, ln, n, 96 if b < 9 else 106)
        if b in (31, 47):
            for st, ln, n in pat(FANFARE):
                add(P, 'tpt', t0, st, ln, n, 112)
        if b in (32, 48):
            for st, ln, n in pat(FANFARE2):
                add(P, 'tpt', t0, st, ln, n, 112)
        if b in (30, 34, 46, 50):
            for st, ln, n in pat(PAIRS):
                add(P, 'tpt', t0, st, ln, n, 104)
        if b in FALL:
            for st, ln, n in pat(FALL[b]):
                add(P, 'tpt', t0, st, ln, n, 108)
        # ------------------------------------------------------------------ drums
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
                add(P, 'hh', t0, k, 1, HAT, 52 if k in (6, 14) else 34)
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
    ('voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 170', None),
    ('voice_directsound_no_resample 60, 64, DirectSoundWaveData_unknown_close_hihat, 255, 0, 255, 80', 0.08),
    ('voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 120', 0.16),
    ('voice_directsound 55, 64, DirectSoundWaveData_ruinous_taiko, 255, 0, 255, 150', 0.67),
    ('voice_directsound_no_resample 60, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 120', 0.29),
]
KEYSPLITS = {   # naam: (tabel, [(sample, sustain, release)])
    'ruinous_str': ('strings', [('sc88pro_string_ensemble_%d' % k, 255, 150) for k in (60, 72, 84)]),
    'ruinous_horn': ('french_horn', [('sc88pro_french_horn_60', 224, 140), ('sc88pro_french_horn_72', 218, 140)]),
    'ruinous_tpt': ('trumpet', [('sc88pro_trumpet_%d' % k, 193, 110) for k in (60, 72, 84)]),
}
VOICES = {
    STR: 'voice_keysplit voicegroup_ruinous_str_keysplit, keysplit_strings',
    HORN: 'voice_keysplit voicegroup_ruinous_horn_keysplit, keysplit_french_horn',
    TPT: 'voice_keysplit voicegroup_ruinous_tpt_keysplit, keysplit_trumpet',
    KOTO: 'voice_directsound 60, 0, DirectSoundWaveData_unknown_koto_high, 255, 240, 0, 100',
    SYN: 'voice_directsound 60, 0, DirectSoundWaveData_ruinous_synth, 255, 0, 255, 90',
    BASS: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_fingered_bass, 255, 253, 0, 120',
    SQ1: 'voice_square_1 60, 0, 0, 1, 0, 2, 3, 1',
    SQ2: 'voice_square_2 60, 0, 0, 0, 1, 0, 1',
    DRUMS: 'voice_keysplit_all voicegroup_ruinous_drumset',
}


def write_voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Battle! Treasures of Ruin. Gegenereerd door tools/grounded/ruinous_theme.py.'
    lines[1] = ('@ eigen samples (ruinous_samples.py): 82 elektronisch ostinato, 127 = drumkit ruinous; stock: 107 koto, '
                '33 bas, 48 strijkers, 60 hoorn, 56 trompet (keysplits ruinous_*), PSG 80/81.')
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
            '@ Project Grounded: Battle! Treasures of Ruin, %s (stock-samples, kortere release; tabel keysplit_%s).\n'
            '@ Gegenereerd door tools/grounded/ruinous_theme.py.\n'
            'voice_group %s_keysplit\n' % (name, table, name) +
            ''.join('\tvoice_directsound 60, 0, DirectSoundWaveData_%s, 255, 0, %d, %d\n' % (s, su, r) for s, su, r in samples))


# ---- bouwen ---------------------------------------------------------------------------------------------------------
TRACKS = [   # (naam, programma, volume, pan)
    ('tk', DRUMS, 127, 64), ('bm', DRUMS, 100, 64), ('sn', DRUMS, 84, 70), ('hh', DRUMS, 64, 76),
    ('fx', DRUMS, 110, 64), ('fx2', DRUMS, 80, 58),
    ('bass', BASS, 100, 64), ('syn', SYN, 84, 60), ('koto', KOTO, 100, 72), ('tpt', TPT, 82, 56),
    ('horn', HORN, 76, 60), ('str', STR, 70, 68), ('sq1', SQ1, 36, 52), ('sq2', SQ2, 44, 80),
]
PSG = {'sq1', 'sq2'}
ORDER = ['tk', 'bm', 'fx', 'bass', 'syn', 'koto', 'tpt', 'fx2', 'sn', 'horn', 'str', 'hh']
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
    for k in ('str', 'horn', 'tpt'):
        if k in parts:
            parts[k] = detach(parts[k], tail[k])
    for k in ('bass', 'syn', 'koto', 'sq1', 'sq2'):
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
        lowest = p('C2') if k not in PSG else p('C2')
        assert all(n >= lowest for _, _, n, _ in parts.get(k, [])), '%s: noten onder C2' % k
        if pr in (TPT, HORN):
            assert all(n >= 48 for _, _, n, _ in parts.get(k, [])), '%s: koper onder C3' % k
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
GM_PROG = {'bass': 33, 'syn': 81, 'koto': 107, 'tpt': 56, 'horn': 60, 'str': 48, 'sq1': 80, 'sq2': 80}
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
            elif x.type in ('note_on', 'note_off') and k == 'koto':
                x = x.copy(channel=ch, note=x.note + 12)
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
