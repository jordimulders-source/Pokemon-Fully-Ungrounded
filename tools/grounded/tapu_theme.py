#!/usr/bin/env python3
"""Project Grounded: "Battle! Tapu" (Pokémon Sun/Moon), transcriptie + arrangement, v2.

Bron: alleen de mp3 (geen MIDI). Spleeter (4 stems) + basic-pitch per stem + CQT/onset-analyse per 16e op een vast
raster (174 bpm, maat 1 = 0,740 s in de mp3). Jordi: "het belangrijkste zijn de chants en de luide tribal-drums;
bijna ritualistisch"; v2-feedback: "1-5 s een herhalend chant-thema (slimme vervanging mag), op 6 s een HOO met een
harde drumslag, dan beginnen de drums, 11-17 s die TUDUDU" en "het gaat om jouw interpretatie".

Gemeten aan het origineel (180 s, twee keer de loop + fade):
  tempo 174 bpm, 4/4, loop = 60 maten = 82,8 s, maat 61 = maat 1. Toonsoort: E met b2/b5; bas-ostinato E/Bb-A-G.
  Vorm (maten van het origineel, ob = 1..60; tijd in de mp3 = 0,74 + (ob - 1) * 1,379 s):
    1-4    openingsslag + akkoord F#4-C5-E5-C6, het herhalende chant-thema (elke halve maat dezelfde figuur:
           B4/E5 op de slag, E4-F4 heen en weer, lage mannenstem F#3 op 16e 4 en 7; vocal-stem, CQT per 16e)
    5      de HIT (6,26 s): 'HOO' (koor zwelt van F#3 naar A#3) + harde slag = einde van de gevechtsintro
    5-8    de drums beginnen (gemeten per 16e per band)
    9-12   het motief 'TU-DU-DU-DUUUU - TU-DU-DU-DU' (11,8-17,3 s): taiko's op 16e 0, 2, 3, 4 (lang) | 8, 9, 12, 14,
           onder een tremolo B3+F4 (tritonus) in 16en
    13-28  groove: bas-ostinato, taiko-patroon (tellen 1,2,3,'3-en',4), chant op Bb4/Eb5/D5, kreten
    29-36  overmatige akkoorden, hoorn-melodie; 37-48 E5-/E6-figuren, korte E6-tikjes op de tellen (41-48, het 'fluitje')
    49-52  tweede chant, hoge wisselfiguur; 53-60 slot: G#2/B2 -> Bb1-pedaal, vier-op-de-vloer
In de game begint het nummer bij maat 1 (geen eigen voorspel meer); de Tapu-transitie eindigt op de HIT
(HIT_SECONDS_GBA = 5,542 s = TAPU_HIT_FRAME 333 in src/battle_transition.c). Loop = maat 1-60 (terug naar de chant).

v3 (Jordi over v2: 'HOO wimpy, weg', 'de TUDUDU is een synth en compleet onhoorbaar', 'baslijn klopt niet', 'niet
energiek, drums niet hard genoeg'): geen HOO meer (de slag op de HIT blijft), synth-lead in maat 9-12 (synth()), synthbas
op tapu_synth (hergemeten per 16e), harder slagwerk + kick, PSG-hats en PSG-puls (geen DS-kanalen).
Voicegroup grounded_tapu (gegenereerd) = grounded_gm met: 52 chant 'aa' (tapu_vox_a), 38 synthbas + 81 synth-lead
(tapu_synth), 80 PSG-blokgolf, 120 PSG-ruis (hats),
54 lage 'hu' (tapu_vox_hu) (eigen formant-samples, tools/grounded/tapu_samples.py), 48-50 strijkers (keysplit),
60 hoorn (keysplit), 73 fluit (de E6-tikjes), 77 shakuhachi, 33 fingered bass, 47 pauk, 127 = drumkit
drumsets/tapu.inc (odaiko/taiko/ka/bekken eigen samples; Indiase trom, tom, conga's, kotsuzumi, hyoushigi, kick stock).
Gebruik: python3 tools/grounded/tapu_samples.py (eenmalig) en python3 tools/grounded/tapu_theme.py [--render <map>]"""
import os, subprocess, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

OUT = 'sound/songs/midi/mus_grounded_vs_tapu.mid'
VG = 'grounded_tapu'
TPB = 48
S16 = TPB // 4
BAR = TPB * 4
BPM = 174
PRE = 0                                    # v2: geen eigen voorspel meer; de game begint bij maat 1 van het origineel
HIT_OB = 5                                 # de HIT ('HOO!' + eerste grote slag) = maat 5 van het origineel (6,26 s)
HIT_TICK = (HIT_OB - 1) * BAR
HIT_SECONDS = (HIT_OB - 1) * 4 * 60 / BPM  # 5,517 s nominaal ...
HIT_SECONDS_GBA = HIT_SECONDS * 1.0045     # ... 5,542 s op de GBA (die speelt 0,45% te traag) -> TAPU_HIT_FRAME 333
ORIG_BAR1 = 0.74                           # maat 1, tel 1 in de mp3 (openingsslag + akkoord; chant 0,9-5,8 s)
NBARS = 60                                 # loop = maat 1-60 van het origineel (terug naar de chant, zoals het origineel)
END = PRE + NBARS

CHOIR, CHLO, STR, STR2, HORN, SHAKU, FLUTE, BASS, TIMP, DRUMS = 52, 54, 48, 49, 60, 77, 73, 38, 47, 127
SYN, PSQ, HAT = 81, 80, 120              # v3: synth-lead (tapu_synth), PSG-blokgolf (16en-puls/verdubbeling), PSG-ruis (hats)
# drumkit (drumsets/tapu.inc, vanaf 36): TAIKO/TAIKO_LO/BIGTOM/KA = eigen samples (tapu_samples.py)
TAIKO, TAIKO_LO, BIGTOM, INDIAN, TOM, CONGA_LO, CONGA_HI, KA, KOTSU, CRASH, TAMB, HYOU, KICK, IMPACT = range(36, 50)
OHTSU = KA
RING = {BIGTOM: 8, TAIKO: 4, TAIKO_LO: 5, CRASH: 14, KA: 1, INDIAN: 2, TOM: 2, CONGA_LO: 1, CONGA_HI: 1, KOTSU: 2,
        TAMB: 2, HYOU: 1, KICK: 2, IMPACT: 24}           # hoe lang een slag maximaal doorklinkt (16en); korter als dezelfde partij opnieuw slaat

N = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8,
     'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def p(name):
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


def at(ob, q=0):
    """tick van 16e q in maat ob van het origineel (ob 1 = begin van het nummer, ob 5 = de HIT)."""
    return (PRE + ob - 1) * BAR + q * S16


def put(out, ob, pat, vel=100):
    """pat: [(16e, lengte in 16en, noot of [noten], velocity?)]"""
    for item in pat:
        q, ln, nt = item[:3]
        v = item[3] if len(item) > 3 else vel
        for n in (nt if isinstance(nt, (list, tuple)) else [nt]):
            out.append([at(ob, q), at(ob, q) + ln * S16, p(n) if isinstance(n, str) else n, v])


def notes_str(out, s, vel=None):
    """'ob:q:len:NOOT[:vel] ...' -> noten (transcriptietabellen)."""
    for tok in s.split():
        f = tok.split(':')
        ob, q, ln, nt = int(f[0]), int(f[1]), int(f[2]), f[3]
        v = int(f[4]) if len(f) > 4 else (vel or 100)
        out.append([at(ob, q), at(ob, q) + ln * S16, p(nt), v])


# ---------------------------------------------------------------- bas (stem 'bass', basic-pitch, per 16e) -------------
BA = [(0, 2, 'E2'), (2, 2, 'E2'), (4, 2, 'E2'), (6, 4, 'E2'), (10, 2, 'A#2'), (12, 2, 'A2'), (14, 2, 'G2')]
BA2 = [(0, 2, 'E2'), (2, 2, 'G2'), (4, 2, 'E2'), (6, 2, 'G2'), (8, 2, 'E2'), (10, 2, 'A#2'), (12, 2, 'A2'), (14, 2, 'G2')]
BAC = [(0, 2, 'E2'), (2, 2, 'E2'), (4, 2, 'E2'), (6, 2, 'E2'), (8, 2, 'E2'), (10, 2, 'D#2'), (12, 2, 'D2'), (14, 2, 'C2')]
BB = [(0, 2, 'A#2'), (2, 2, 'A2'), (4, 2, 'G2'), (6, 2, 'A#2'), (8, 2, 'A2'), (10, 2, 'G2'), (12, 2, 'A#2'), (14, 2, 'G2')]
BC = [(0, 2, 'C2'), (2, 1, 'C#2'), (3, 4, 'C2'), (7, 1, 'C#2'), (8, 1, 'D2'), (9, 3, 'C2'), (12, 1, 'C#2'), (13, 1, 'B1'),
      (14, 2, 'C2')]                                    # v3: C2-pedaal met wiebel (basstem), geen C3-sprongen
BFS = [(i * 2, 2, 'F#2' if i % 2 == 0 else 'A2') for i in range(8)]
BGS = [(0, 2, 'G#2'), (2, 2, 'B1'), (4, 2, 'G#2'), (6, 2, 'B1'), (8, 2, 'G#2'), (10, 2, 'B1'), (12, 1, 'C#2'),
       (13, 1, 'A#1'), (14, 2, 'B1')]                   # v3: G#2 tegen de lage B1 (basstem), niet B2
BGS_END = BGS[:5] + [(10, 1, 'D2'), (11, 3, 'C#2'), (14, 2, 'B1')]
BBB = [(0, 2, 'A#1'), (2, 2, 'A#1'), (4, 2, 'A#1'), (6, 2, 'A#1'), (8, 2, 'A#1'), (10, 1, 'B1'), (11, 1, 'C2'),
       (12, 1, 'D2'), (13, 1, 'A#1'), (14, 2, 'C2')]     # v3: A#1-pedaal + wiebel B1-C2-D2 (basstem)
BBB_END = [(0, 2, 'A#1'), (2, 2, 'A#1'), (4, 2, 'A#1'), (6, 2, 'A#1'), (8, 2, 'A#1'), (10, 1, 'B1'), (11, 1, 'C2'),
           (12, 1, 'C#2'), (13, 1, 'A#1'), (14, 2, 'B1')]
GROOVE = {13: BA, 14: BA, 15: BA, 16: BB, 17: BA, 18: BA, 19: BAC, 20: BC, 21: BA, 22: BA, 23: BAC, 24: BB,
          25: BA, 26: BA, 27: BAC, 28: BC, 29: BA, 30: BA, 31: BAC, 32: BB, 33: BA, 34: BA, 35: BAC, 36: BC,
          37: BA2, 38: BA2, 39: BA2, 40: BA2, 41: BA, 42: BA, 43: BAC, 44: BB, 45: BA, 46: BA, 47: BAC, 48: BC,
          49: BA2, 50: BA2, 51: BFS, 52: BFS, 53: BGS, 54: BGS, 55: BGS, 56: BGS_END,
          57: BBB, 58: BBB, 59: BBB, 60: BBB_END}
# v3: maten waar de basstem per 16e (harmonische som) afwijkt van het vaste riff (vergelijking v2: 25-62% gelijk)
GROOVE.update({
    14: [(0, 2, 'E2'), (2, 2, 'E2'), (4, 2, 'E2'), (6, 1, 'E2'), (7, 1, 'F2'), (8, 2, 'E2'), (10, 2, 'A#2'), (12, 1, 'B1'),
         (13, 1, 'A1'), (14, 2, 'B1')],
    15: [(0, 2, 'E2'), (2, 2, 'E2'), (4, 1, 'E2'), (5, 2, 'D#2'), (7, 1, 'E2'), (8, 1, 'C2'), (9, 1, 'B1'), (10, 1, 'A#1'),
         (11, 2, 'B1'), (13, 1, 'A1'), (14, 2, 'G2')],
    16: [(0, 2, 'A#1'), (2, 2, 'E2'), (4, 2, 'G2'), (6, 1, 'C2'), (7, 1, 'C#2'), (8, 2, 'A#1'), (10, 2, 'G2'), (12, 1, 'B1'),
         (13, 1, 'A#1'), (14, 2, 'B1')],
    27: [(0, 2, 'E2'), (2, 2, 'E2'), (4, 2, 'E2'), (6, 1, 'C2'), (7, 1, 'C#2'), (8, 1, 'D#2'), (9, 1, 'E2'), (10, 2, 'D2'),
         (12, 1, 'A#1'), (13, 1, 'A1'), (14, 1, 'A#1'), (15, 1, 'B1')],
    28: [(0, 1, 'B1'), (1, 1, 'C#2'), (2, 1, 'D2'), (3, 1, 'B1'), (4, 2, 'C2'), (6, 1, 'C2'), (7, 2, 'D2'), (9, 1, 'D3'),
         (10, 1, 'D#2'), (11, 1, 'C2'), (12, 1, 'A1'), (13, 2, 'F2'), (15, 1, 'F#2')],
    29: [(0, 2, 'E2'), (2, 2, 'E2'), (4, 2, 'E2'), (6, 1, 'F2'), (7, 1, 'C#2'), (8, 1, 'E2'), (9, 1, 'F#2'), (10, 1, 'D2'),
         (11, 1, 'F#2'), (12, 1, 'G2'), (13, 1, 'F#2'), (14, 2, 'G2')],
})


def bass():
    # v4 (Jordi: 'het begin wordt gedomineerd door een baslijn die helemaal niet bestaat in het origineel'): in de
    # basstem is maat 1-11 alleen de lage romp van de taiko's (C#2/D2 per slag, pyin-stemhebbendheid 1-40%, geen
    # aangehouden toon); de eerste echte bastoon is de F2 van maat 12 (aangehouden, 40-67%), dan de groove (maat 13).
    out = []
    put(out, 12, [(0, 16, 'F2')])                                     # b2 onder de chant-inzet
    for ob, pat in GROOVE.items():
        put(out, ob, pat, 104)
    return dedupe(out)


# ---------------------------------------------------------------- chant (stem 'vocals', CQT per 16e) -------------------
CHANT = [
    # maat 1-4: het herhalende chant-thema staat in chant_theme() (v2)
    # maat 13-16: chant Bb4/Eb5 (D5 als doorgang) in achtsten
    '13:0:2:A#4 13:2:2:D#5 13:4:2:A#4 13:6:2:D#5 13:8:1:D5 13:9:2:D#5 13:12:2:A#4 13:14:2:D#5',
    '14:0:2:A#4 14:2:2:D#5 14:5:1:D#5 14:6:2:A#4 14:14:2:A#4',
    '15:1:2:B4 15:3:1:D#5 15:4:2:D5 15:6:1:E5 15:7:2:D5 15:9:1:E5 15:10:2:D5 15:12:2:D#5 15:14:1:D5 15:15:1:D#5',
    '16:0:1:D5:84 16:3:2:D#5:76 16:8:2:E4:70',
    # maat 17-24: losse lettergrepen (zachter), de kreten staan bij SHOUTS
    '17:2:1:A#4:100 17:4:4:E4:80 17:10:1:F4:76',
    '18:10:3:F4:70 18:15:1:A#4:70',
    '19:0:1:A#4:80 19:2:3:D5:74 19:8:4:D#5:84',
    '20:0:2:D#5:70',
    '21:12:3:B4:76 21:15:1:A#4:76',
    '22:1:2:A#4:80 22:7:1:D#5:92 22:8:2:E5:74 22:11:2:D#5:76 22:15:1:E5:70',
    '23:2:2:D5:70 23:14:1:D#5:90 23:15:1:E5:70',
    '24:0:2:E5:70',
    # maat 49-56: tweede chant
    '49:0:1:E4 49:1:1:A4 49:3:1:A#4 49:5:1:B4 49:6:1:A#4 49:7:2:D#5 49:9:1:E5 49:10:2:D#5 49:13:1:E5 49:14:2:D#5',
    '50:1:2:B4 50:5:2:D#5 50:8:2:E5 50:10:1:D#5 50:12:2:C#5 50:14:1:E5 50:15:1:B4',
    '51:1:1:C#5 51:2:1:F#4 51:6:1:C#5 51:10:1:G#4 51:11:1:B4 51:12:1:D#5 51:13:1:F#4',
    '52:1:1:G#4:84 52:8:1:D#5:84',
    '53:6:2:F#4:84 53:9:4:C#5:74',
    '54:2:2:C#5:84 54:4:1:D#5:76 54:5:1:E5:76 54:12:1:D#5:76',
    '55:11:1:C#5:80 55:12:3:D#5:80',
    '56:8:2:D#5:90 56:14:8:F#4:110',
    # maat 60: opmaat terug naar de HIT
    '60:12:1:E4:90 60:13:1:D#4:96 60:14:1:E4:90 60:15:1:B3:96',
]


def chant_theme():
    """Maat 1-4 (0,74-6,26 s in het origineel): het herhalende chant-thema, gemeten met CQT per 16e op de vocal-stem.
    Het koor herhaalt elke halve maat dezelfde figuur: bovenstem B4/E5 op de slag, dan E4-F4-heen-en-weer, en een lage
    mannenstem (F#3) ertussen op 16e 4 en 7. Op de GBA als losse lettergrepen: bovenstem 'ha' (tapu_vox_a), lage 'hu'
    (tapu_vox_hu). Maat 1 begint met een lange roep op E5 (met het openingsakkoord); maat 4 eindigt een halve maat
    eerder (adem) zodat de HOO op maat 5 vrij staat."""
    hi, lo = [], []
    fig_hi = [(0, 1, 'B4', 112), (1, 1, 'E5', 100), (2, 1, 'E4', 94), (3, 1, 'F4', 100), (5, 1, 'F4', 96),
              (6, 2, 'E4', 100)]
    fig_lo = [(4, 1, 'F#3', 118), (7, 1, 'F#3', 108)]
    for ob in range(1, 5):
        for h in (0, 8):
            if ob == 1 and h == 0:
                put(hi, 1, [(0, 7, 'E5', 108)])
                put(lo, 1, [(4, 1, 'F#3', 104), (7, 1, 'F#3', 104)])
                continue
            if ob == 4 and h == 8:
                put(hi, 4, [(8, 1, 'B4', 116), (9, 1, 'E5', 108), (10, 2, 'E4', 104)])
                continue
            put(hi, ob, [(h + q, ln, n, v) for q, ln, n, v in fig_hi])
            put(lo, ob, [(h + q, ln, n, v) for q, ln, n, v in fig_lo])
    return hi, lo


INTRO_CHANT = 0.42   # v4: chant maat 1-4 -7,5 dB (gemeten: chant -2,3 / drums -6,7 dB t.o.v. de mix; origineel -7,0 / -4,1)


def chant():
    out = []
    for s in CHANT:
        notes_str(out, s, 100)
    out += [[a, b, n, int(v * INTRO_CHANT)] for a, b, n, v in chant_theme()[0]]
    return dedupe(out)


def legato(notes):
    """elke noot tot de volgende aanslag (geen detach: dat maakte van 16en losse stipjes); dezelfde toonhoogte nooit
    overlappend."""
    notes = sorted(notes)
    out = []
    for i, n in enumerate(notes):
        nxt = notes[i + 1][0] if i + 1 < len(notes) else None
        e = n[1] if nxt is None or nxt - n[1] > 2 * S16 else nxt
        out.append([n[0], max(n[0] + 2, e), n[2], n[3]])
    return out


def chant_lo():
    return dedupe([[a, b, n, int(v * INTRO_CHANT)] for a, b, n, v in chant_theme()[1]])


# ---------------------------------------------------------------- strijkers / pad (stem 'other') ----------------------
def pad():
    out = []
    put(out, 1, [(0, 40, ['C5', 'C6'], 50)])                         # maat 1-3 (+ half 4): tritonusakkoord (v4 zachter)
    put(out, 7, [(0, 16, ['F4', 'F#4'], 40)])                        # aanzwellende clusters (v4 zachter: drums voorop)
    put(out, 8, [(0, 8, ['G#4', 'A4'], 46), (8, 8, ['G#4', 'A4'], 56)])
    groove_pad = {16: ['G4', 'A#4'], 20: ['A#4', 'D5'], 24: ['G4', 'C5'], 28: ['C5', 'D#5']}
    for ob in range(13, 29):
        put(out, ob, [(0, 16, groove_pad.get(ob, ['E4', 'B4']), 62)])
    aug = {29: ['F4', 'A4', 'C#5'], 31: ['E4', 'G#4', 'C5'], 33: ['F4', 'A4', 'C#5'], 35: ['G#4', 'C5', 'D#5']}
    for ob, ch in aug.items():
        put(out, ob, [(0, 32, ch, 70)])
    for ob in range(37, 41):
        put(out, ob, [(0, 16, ['E4', 'C5'], 64)])
    third = {41: ('A4', 'F4'), 42: ('F4', 'C#5'), 43: ('D#4', 'B4'), 44: ('B4', 'B4'), 45: ('A4', 'A4'),
             46: ('F4', 'A4'), 47: ('D#4', 'F#4'), 48: ('F#4', 'G4')}
    for ob, (a, b) in third.items():
        put(out, ob, [(0, 8, ['E4', 'C5', a], 64), (8, 8, ['E4', 'C5', b], 64)])
    put(out, 49, [(0, 32, ['F#4', 'A4', 'C#5'], 66)])
    put(out, 51, [(0, 16, ['F#4', 'G#4', 'C5'], 66)])
    put(out, 52, [(0, 16, ['G#4', 'B4', 'E5'], 66)])
    put(out, 53, [(0, 64, ['A#4', 'C#5'], 70)])
    # v4: maat 57-60 = de aangehouden tritonus-textuur uit de stem 'other' (A#4/E5, in 59-60 met G5), zie hi()
    put(out, 57, [(0, 32, ['A#4', 'E5'], 74)])
    put(out, 59, [(0, 32, ['A#4', 'E5', 'G5'], 74)])
    return dedupe(out)


# ---------------------------------------------------------------- synth (v3) -------------------------------------------
# Jordi (v2): 'de TUDUDU van 11 seconden is compleet onhoorbaar. Dat is volgens mij juist een synth' + zijn neurie
# (tapu_hum_synth.ogg, 5,9 s = precies maat 9-12). Gemeten: in de stem 'other' (basic-pitch + harmonische som per 16e)
# komt in maat 9-12 een brede synth binnen die stap voor stap stijgt: E3 (maat 9 16e 0), B3 (9:8), E4 (10:4), F4 (10:8),
# daarna een trillende B3/F4 met E4<->F4-gewiebel tot maat 12. De neurie heeft dezelfde vorm (pyin, op 174 bpm gelegd):
# vier lange tonen per halve maat ('TU-DU-DU-DUUUU': G2 D3 E3 F#3, eerste sprong ook een kwint), dan 16en-trillers rond
# een toon ('TUDUDUDU'). Hier: de stijging op de gemeten toonhoogtes, de trillers/staart uit de neurie (+11 halve tonen:
# zijn F#3 = de F4 van het origineel, G3 = F#4, E3 = D#4). Elders in het nummer komt deze lead niet terug (maat 13-60:
# 'other' bevat daar de boventonen van de synthbas, zie bass()); bij de herhaling van de loop klinkt hij opnieuw.
# v4 (Jordi: 'de synth doet vanaf 13 seconden heel raar, afzwakken, wegvallen, die moet doorgetrokken worden, luister
# naar mijn neurie'): v3 kortte elke noot met detach() in (uitklinktijd 16 ticks > een 16e: de trillers werden halve
# stipjes) en had gaten (11:2-11:6, 12:3-12:5). Nu één doorlopende, legato lijn (elke noot tot de volgende aanslag, geen
# rust) op de tonen van de neurie (basic-pitch op de neurie, maat 9 = 0,31 s): G2 . D3 . | E3 . F#3 G3-F#3-G3-F#3 |
# (F3) E3 F#3 . . . | E3 D#3 G#2 . E3 G3 F#3 . G3 F#3; in de ligging van de stem (+9 voor de eerste twee, dan +11).
# v5 (Jordi over v4: 'alles behalve de synth klopt; klinkt wat gehaast, kloppen de noten, is synth het juiste
# instrument?'): opnieuw getranscribeerd uit de stem 'other' (drie methodes per 16e: piek-tracking, pyin per band,
# basic-pitch; tabel in de rapportmap). Het is GEEN melodielijn maar een akkoord dat zich opbouwt en dan blijft liggen:
# E3 + E4 (octaaf) op 9:0, B3 erbij op 9:8, E4 opnieuw aangezet op 10:0 (basic-pitch: nieuwe aanzet, Jordi's 3e toon),
# E4 schuift naar F4 op 10:8, E3 valt weg op 11:8, en B3 + F4 (tritonus) liggen tot 13:0 (40 zestienden). De bovenstem
# (wat je neuriet) = E3 . B3 . E4 . F4 - - - - -, elke stap een halve maat op de taikoslagen (9:0 9:8 10:0 10:8).
# De neurie heeft dezelfde vorm en hetzelfde ritme (stappen +7 +2 +2 i.p.v. +7 +5 +1: kleinere sprongen, gewoon
# neuriën), en zijn 'TUDUDU'-gewiebel op 10:8-11:0 is de zweving van de synth (ensemble, 2,5-9 Hz), geen triller;
# de 'woeps' omhoog op 11:0 en 12:0 = de synth die daar opnieuw aanzet en helderder wordt (filter open).
# v4 maakte van dat gewiebel en die woepsen 16 losse 16en-noten (F#4/F4-trillers, D#4, G3) in een eenstemmige lijn
# die elke vorige toon afkapte, plus een PSG-16en-puls: dat was het 'gehaast'. Klank: synth-brass (tapu_brass).
SYN_LINE = ('9:0:40:E3:110 9:0:16:E4:84 9:8:24:B3:112 10:0:8:E4:118 10:8:8:F4:124 '
            '11:0:15:B3:116 11:0:15:F4:124 12:0:13:B3:118 12:0:13:F4:127')
SYN_BRIGHT = 82        # tapu_brass_hi: vanaf 11:0 (filter open), terug naar 81 op 9:0


def synth():
    out = []
    notes_str(out, SYN_LINE)
    return sorted(dedupe(out))


def synth_ccs():
    """programmawissels: de heldere synth-brass voor de aanzetten van 11:0 en 12:0, de donkere vanaf 9:0."""
    return [(at(9, 0), 'prog', SYN), (at(11, 0), 'prog', SYN_BRIGHT)]


def synth_psg():
    """PSG-blokgolf (kost geen DS-kanaal): maat 17-20 en 25-28 de bovenlaag van de synthbas (stem 'other': het
    basriff een octaaf hoger). v5: de 16en-puls van maat 9-12 is weg (de synth daar pulseert niet)."""
    out = []
    for ob in list(range(17, 21)) + list(range(25, 29)):
        put(out, ob, [(q, ln, p(n) + 12, 92) for q, ln, n in GROOVE[ob]])
    return dedupe(out)


def hats():
    """PSG-ruis: de stem 'drums' heeft vanaf maat 17 een hoge 16en-laag (3-10 kHz), in maat 13-16 alleen zwak."""
    out = []
    for ob in range(13, NBARS + 1):
        for q in range(16):
            if ob < 17 and q % 2:
                continue
            v = 96 if q % 4 == 0 else (78 if q % 2 == 0 else 62)
            if ob < 17:
                v -= 16
            out.append([at(ob, q), at(ob, q) + 1, 84, v])
    return out


def pulses():
    out = []
    for ob in range(29, 49):
        put(out, ob, [(5, 2, 'C4', 96), (13, 2, 'C4', 96)])
    for ob in (53, 54):
        put(out, ob, [(0, 3, 'C4', 96), (9, 3, 'C4', 96), (6, 2, 'F4', 80), (14, 2, 'F4', 80)]
            + [(q, 2, 'D#5', 78) for q in (0, 4, 8, 12)])
    for ob in (55, 56):
        put(out, ob, [(12, 3, 'C4', 96)] + [(q, 2, 'D#5', 74) for q in (0, 4, 8)])
    for ob in range(57, 61):
        put(out, ob, [(1, 2, 'A#3', 90), (5, 2, 'A#3', 90), (0, 2, 'F4', 80), (9, 2, 'D#4', 86), (12, 2, 'D#4', 92)])
    return dedupe(out)


# ---------------------------------------------------------------- melodie (stem 'other', basic-pitch) -----------------
HORN_MEL = [
    '29:9:5:A4 30:4:4:A4 30:8:3:C#5 30:11:1:C#5 30:12:1:E5 30:13:3:C#5',
    '31:0:2:C5 31:2:6:G#4 31:8:6:G#4 31:14:2:G#4 32:3:8:G#4 32:12:4:E4',
    '33:7:2:A4 33:9:4:F4 33:14:2:A4 34:0:2:A4 34:2:4:F4 34:6:2:A4 34:8:1:C#5 34:9:4:C#5 34:13:3:C#5',
    '35:0:3:C5 35:3:5:C5 35:8:8:D#5 36:0:6:D#5 36:6:7:D#5 36:13:3:D#5',
    '37:0:4:E5 37:4:4:E5 37:8:4:E5 37:12:4:E5 38:0:2:E5 38:2:6:G5 38:8:2:E5 38:10:6:G5',
    '39:0:4:E5 39:4:4:E5 39:8:4:E5 39:12:4:E5 40:0:2:E5 40:2:1:E5 40:3:5:E5 40:8:3:E5 40:11:5:E5',
    '43:0:2:C5 43:6:2:C5 46:8:6:C#5 47:0:5:C5 47:8:2:D#5 47:10:4:D#5 47:14:2:D#5 48:4:7:D#5 48:12:2:G#5',
]
HI_MEL = [   # hoge partij: E6-kwarten (41-48) en de wisselfiguur (49-60)
    '41:2:2:E5 41:4:4:E6 41:8:8:E6 42:0:2:E6 42:2:2:G6 42:4:4:E6 42:8:2:E6 42:10:2:G6 42:12:4:E6',
    '43:0:4:E6 44:5:2:E5 44:12:4:E6 45:0:4:E6 45:4:4:E6 45:8:2:E6 45:10:2:E5 45:12:4:E6',
    '46:2:2:G6 46:8:2:E6 46:10:2:G6 47:0:4:E6 47:4:4:E6 47:8:4:E6 47:12:4:E6 48:0:4:E6',
    '49:0:2:A5 49:2:2:F#5 49:4:2:A5 49:6:2:F#5 49:8:3:A5 49:11:2:F#5 49:13:3:C#6',
    '50:0:1:C#6 50:1:4:A5 50:5:3:A5 50:8:3:A5 50:11:1:A5 50:12:1:C#6 50:13:3:A5',
    '51:1:3:G#5 51:4:2:B5 51:6:3:G#5 51:9:3:G#5 51:12:4:B5 52:0:6:G#5 52:6:2:B5 52:8:3:B5 52:11:5:G#5',
]
# v4 (Jordi over v3: 'het fluitje vanaf 1:06 is wat te hoog. en wat dat fluitje vanaf 1:18 gaat doen snap ik ook
# niet'): maat 49-56 een octaaf lager (de stem 'other' heeft de wisselfiguur ook op A4/F#4); maat 57-60 was geen melodie
# maar basic-pitch op een aangehouden tritonus-pad (A#4/E5/A#5, energie per 16e vlak 30-36 dB): weg uit de
# shakuhachi, als akkoord in pad().
HI_OCT = -12


def horn():
    out = []
    for s in HORN_MEL:
        notes_str(out, s, 100)
    put(out, 5, [(0, 3, ['E3', 'B3'], 127)])                          # v4: koperstoot op de HIT
    return dedupe(out)


PIPS = HI_MEL[:3]     # maat 41-48: hoge E6-'fluitjes'
HI_MEL = HI_MEL[3:]


def pips():
    """Maat 41-48 (het 'fluitje' vanaf 20 s in e2): basic-pitch op de stem 'other' vindt E6 (soms G6) als korte tikjes
    van ±1 zestiende op de tellen (lengte 0,8-1,9 zestiende, velocity ±50), geen aangehouden kwartnoten zoals in v1
    (shakuhachi, 4 zestienden: 'gaat helemaal fout'). v2: zelfde tijdstippen, 1 zestiende, staccato fluit (stock
    sc88pro_flute, release 127), zachter."""
    out = []
    for s in PIPS:
        for tok in s.split():
            f = tok.split(':')
            ob, q, nt = int(f[0]), int(f[1]), f[3]
            if p(nt) >= p('E6'):
                out.append([at(ob, q), at(ob, q) + S16, p(nt), 92 if nt == 'G6' else 100])
    return dedupe(out)


def hi():
    out = []
    for s in HI_MEL:
        notes_str(out, s, 96)
    for ob in range(53, 57):                                          # A#5/C#6 in achtsten
        put(out, ob, [(q * 2, 2, 'A#5' if q % 2 == 0 else 'C#6', 92) for q in range(8)])
    return dedupe([[a, b, n + HI_OCT, v] for a, b, n, v in out])


# ---------------------------------------------------------------- drums (stem 'drums', onsets per band per 16e) -------
def ring_gates(notes):
    """Drumnoten zo lang laten klinken als de slag echt doorklinkt (RING), maar niet langer dan tot de volgende slag
    in dezelfde partij: v1 kapte elke slag na 2-3 zestienden af (release 140) = tikjes i.p.v. trommen."""
    notes = sorted(notes)
    starts = sorted({n[0] for n in notes})
    out = []
    for n in notes:
        nxt = next((x for x in starts if x > n[0]), None)
        ln = RING.get(n[2], 2) * S16
        if nxt is not None and n[2] not in (CRASH,):
            ln = min(ln, max(S16, nxt - n[0]))
        out.append([n[0], n[0] + ln, n[2], n[3]])
    return out


def drums():
    t, m, pc, cr, tp = [], [], [], [], []    # taiko/grote trommen, middentrommen/toms, kleine percussie, bekkens, pauk

    def hit(lst, ob, q, note, vel, ln=2):
        lst.append([at(ob, q), at(ob, q) + ln * S16, note, vel])

    # per 16e uit de drumstem (onsets per band): LAAG = taiko/grote trom, KRAK = scherpe tik (mid+hoog: 'ka'),
    # MID = middentrom (alleen mid). Getallen = gemeten sterkte.
    LOW = {1: {0: 281, 6: 48, 8: 42, 10: 46, 12: 88, 14: 44}, 2: {0: 175, 1: 69, 7: 67, 9: 55, 14: 154, 15: 93},
           3: {4: 104, 7: 135, 8: 125, 13: 102, 14: 72}, 4: {1: 67, 5: 78, 7: 87, 8: 133, 15: 81},
           5: {2: 92, 3: 63, 6: 76, 11: 69, 13: 100, 14: 68}, 6: {0: 224, 3: 84, 5: 90, 12: 61, 13: 76, 14: 87, 15: 95},
           7: {0: 75, 1: 98, 2: 62, 8: 88, 12: 67, 13: 79}, 8: {0: 105, 1: 83, 9: 82}}
    CRACK = {1: {0: 65}, 2: {0: 81, 14: 87, 15: 22}, 3: {0: 61, 14: 56}, 4: {0: 50, 7: 62, 9: 29, 10: 61, 14: 49},
             5: {0: 68}, 6: {0: 97, 14: 88, 15: 24}, 7: {0: 66, 9: 61, 10: 50, 14: 23}, 8: {1: 61, 3: 45, 13: 36, 14: 35, 15: 26}}
    vel = lambda x, top, lo=58, span=69: int(min(127, lo + span * min(x, top) / top))
    # maat 1-4 (chant, Jordi: 'eerst de roep, dan de eerste grote slag'): de gemeten slagen, maar zacht (hand-trom-
    # ostinato onder de chant); de openingsslag op maat 1 is een doffe boem, niet de HIT
    # v4 (Jordi: 'drums heb je wel als een soort van tikken, maar die zijn te zacht'): in het origineel zijn de drums
    # in maat 1-4 even luid als in de groove (drumstem 39-43 dB per halve maat, de chant 23-33 dB): volle trommen
    for ob in range(1, 5):
        for q, x in LOW[ob].items():
            hit(t, ob, q, BIGTOM if x >= 170 else (TAIKO if x >= 70 else TAIKO_LO), vel(x, 200, 96, 31))
        for q, x in CRACK[ob].items():
            hit(pc, ob, q, KA, vel(x, 90, 84, 40))
        for q, x in LOW[ob].items():                                  # kick onder de zware slagen
            if x >= 85:
                hit(m, ob, q, KICK, 116)
    t = [n for n in t if n[0] != at(1, 0)]
    hit(t, 1, 0, BIGTOM, 127)
    hit(m, 1, 0, TAIKO, 116)
    for i, q in enumerate((8, 9, 10, 11)):                           # korte roffel, dan 4 zestienden stilte vóór de HIT
        hit(m, 4, q, TAIKO, 96 + 10 * i)                             # (contrast: de klap zit al op de top van de mixer)
    t = [n for n in t if not at(4, 12) <= n[0] < at(5, 0)]
    m = [n for n in m if not at(4, 12) <= n[0] < at(5, 0)]
    pc = [n for n in pc if not at(4, 12) <= n[0] < at(5, 0)]
    # maat 5 = de HIT (v3 zonder 'HOO'): de eerste grote slag: odaiko + taiko + ka + bekken + kick
    # v4 (Jordi: 'de klap op 6 mag ook harder ... meer impact, of meerdere instrumenten tegelijkertijd'): odaiko + eigen
    # impact-sample (lage odaiko + sub-val + orkesthit, 2x) + taiko + bekken, met pauk en hoornstoot
    pc = [n for n in pc if n[0] != at(5, 0)]
    # het impact-sample op twee sporen tegelijk (taiko 127 + toms 108, zelfde fase = +5 dB): in v4-test 1 was de klap
    # met één impact op het bekkenspoor even luid als een groove-slag (44 dB per 16e)
    hit(t, 5, 0, BIGTOM, 127)
    imp = []                                                          # eigen partij in de stemverdeler (lange release),
    hit(imp, 5, 0, IMPACT, 127)                                       # daarna op de sporen taiko en toms

    hit(m, 5, 0, TAIKO, 127)
    hit(cr, 5, 0, CRASH, 127)
    hit(tp, 5, 0, p('E2'), 127, 4)
    # maat 5-8: 'dan beginnen de drums' (gemeten, volle sterkte)
    for ob in range(5, 9):
        for q, x in LOW[ob].items():
            if ob == 5 and q == 0:
                continue
            # v4 (Jordi: 'tussen 7 en 11 moeten de drums domineren'): harder, kleinere dynamiek
            hit(t, ob, q, BIGTOM if x >= 150 else (TAIKO if x >= 70 else TAIKO_LO), vel(x, 200, 100, 27))
        for q, x in CRACK[ob].items():
            if not (ob == 5 and q == 0):
                hit(pc, ob, q, KA, vel(x, 90, 92, 35))
        if ob >= 6:                                                   # kick onder de zware slagen (punch)
            for q, x in LOW[ob].items():
                if x >= 85:
                    hit(m, ob, q, KICK, 120)
    for q in range(8, 16):                                            # maat 8: pauk-roffel crescendo naar maat 9
        hit(tp, 8, q, p('E2'), 84 + (q - 8) * 6, 1)
    # maat 9-12 (v3): het 'TUDUDU' is de synth (Jordi), geen taikomotief meer. Drumstem per 16e (flux per band):
    # laag sterk op 16e 9 ('3-en') en 12 (4), middel op 8 (3), tel 1 matig -> 1 . . . | 3 3-en . 4
    for ob in range(9, 13):
        for q, n, v in ((0, BIGTOM if ob == 9 else TAIKO, 127 if ob == 9 else 112), (8, TAIKO, 120), (9, BIGTOM, 127),
                        (12, BIGTOM, 124)):
            if ob == 12 and q >= 12:
                continue
            hit(t, ob, q, n, v)
        hit(pc, ob, 8, KA, 108)
        hit(m, ob, 8, INDIAN, 100)
    hit(t, 11, 7, TAIKO, 112)
    for i, q in enumerate((12, 13, 14, 15)):                         # fill naar de groove
        hit(m, 12, q, TOM, 104 + 6 * i)
        hit(t, 12, q, TAIKO, 100 + 7 * i)
    # groove maat 13-60 (gemiddeld per 16e gemeten): slagen op 1, 2, 3, '3-en', 4 (laag+mid); in maat 13-52 klinkt
    # na elke tel een zachtere tweede slag (16e 1, 5, 9, 13: 'DUM-dum'); hoog alleen zwak op 2 en 4 (hyoushigi pp)
    for ob in range(13, NBARS + 1):
        for q, n, v in ((0, TAIKO, 127), (4, BIGTOM, 122), (8, TAIKO, 127), (10, TAIKO_LO, 116), (12, BIGTOM, 124)):
            hit(t, ob, q, n, v)                                       # v3: harder (Jordi: 'drums niet hard genoeg')
        if ob < 53:
            for q in (0, 8):                                          # v3: kick onder 1 en 3 (punch in het laag)
                hit(t, ob, q, KICK, 116)
        hit(m, ob, 10, INDIAN, 84)
        if ob < 53:
            for q, v in ((1, 74), (5, 90), (9, 80), (13, 80)):
                hit(m, ob, q, CONGA_LO, v)
        for q in (4, 12):
            hit(pc, ob, q, HYOU, 58)
        if ob >= 53:                                                  # slot: vier op de vloer
            for q in (0, 4, 8, 12):
                hit(t, ob, q, KICK, 120)
        if ob % 4 == 0:                                               # elke 4e maat een tomfill
            for q, v in ((13, 100), (14, 108), (15, 116)):
                hit(m, ob, q, TOM, v)
    for ob in (13, 29, 37, 49, 53, 57):
        hit(cr, ob, 0, CRASH, 116, 8)
    return {'taiko': ring_gates(dedupe(t)), 'toms': ring_gates(dedupe(m)), 'perc': ring_gates(dedupe(pc)),
            'cym': ring_gates(dedupe(cr)), 'timp': dedupe(tp), 'imp_t': ring_gates(imp), 'imp_m': ring_gates(list(imp))}


# ---------------------------------------------------------------- sporen ----------------------------------------------
TRACKS = [   # (naam, programma, volume, pan)
    ('chant', CHOIR, 74, 60), ('chlo', CHLO, 88, 68), ('syn', SYN, 120, 64), ('horn', HORN, 92, 56),
    ('hi', SHAKU, 84, 72), ('pips', FLUTE, 64, 76), ('bass', BASS, 108, 64), ('pad', STR, 52, 64),
    ('pulse', STR2, 74, 60), ('synp', PSQ, 70, 64), ('hat', HAT, 60, 72),
    ('taiko', DRUMS, 127, 64), ('toms', DRUMS, 108, 58), ('perc', DRUMS, 96, 70), ('cym', DRUMS, 84, 64),
    ('timp', TIMP, 90, 64),
]
MAX_V = 11                    # legendary: 11 DirectSound-noten (1 kanaal vrij voor effecten)


def kit_releases():
    return {36 + i: int(l.split(',')[-1]) for i, l in enumerate(KIT)}


def build(render_dir=None, frag_dir=None):
    write_voicegroup()
    rel = releases(VG)
    kitrel = kit_releases()
    parts = {'chant': chant(), 'chlo': chant_lo(), 'syn': synth(), 'horn': horn(), 'hi': hi(), 'pips': pips(),
             'bass': bass(), 'pad': pad(), 'pulse': pulses()}
    parts.update(drums())
    melodic = {'chant': CHOIR, 'chlo': CHLO, 'syn': SYN, 'horn': HORN, 'hi': SHAKU, 'pips': FLUTE, 'bass': BASS,
               'pad': STR, 'pulse': STR2, 'timp': TIMP}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) + 2 for k, pr in melodic.items()}
    for k in ('taiko', 'toms', 'perc', 'cym', 'imp_t', 'imp_m'):      # per partij de langste release van zijn kitnoten
        tail[k] = max(release_ticks(kitrel[n[2]], TPB, BPM) for n in parts[k]) + 2
    for k in ('chlo', 'horn', 'hi', 'pips', 'bass', 'pulse', 'timp', 'pad'):   # v4: syn niet (legato, doorgetrokken)
        parts[k] = detach(parts[k], tail[k])
    parts['chant'] = legato(parts['chant'])                           # gezongen: noten lopen in elkaar over
    order = ['imp_t', 'imp_m', 'taiko', 'syn', 'bass', 'cym', 'chant', 'chlo', 'toms', 'perc', 'horn', 'hi', 'pips', 'timp', 'pulse',
             'pad']
    kept = allocate({k: parts[k] for k in order}, order, tail, max_voices=MAX_V)
    print('uitklinktijd (ticks):', tail)
    for k in order:
        n = len(parts[k])
        gone = sorted({(e[0] // BAR) - PRE + 1 for e in parts[k] if e not in kept[k]})
        print('  %-6s %4d noten, %3d vallen weg (%.1f%%)%s' % (k, n, n - len(kept[k]), 100 * (n - len(kept[k])) / max(n, 1),
                                                             ' (maten origineel %s)' % gone[:12] if gone else ''))
        parts[k] = kept[k]
    parts['taiko'] = sorted(parts['taiko'] + parts.pop('imp_t'))
    parts['toms'] = sorted(parts['toms'] + parts.pop('imp_m'))
    parts['synp'] = detach(synth_psg(), 2)                            # PSG: buiten de stemverdeler (geen DS-kanaal)
    parts['hat'] = hats()
    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.loop = (0, END * BAR)                                        # terug naar maat 1 (chant), zoals het origineel
    for ch, (k, prog, vol, pan) in enumerate(TRACKS):
        notes = parts[k]
        song.add(notes, prog, vol, ch, pan, ccs=synth_ccs() if k == 'syn' else ())
    song.save(OUT, END * BAR)
    print(OUT, 'HIT op %.3f s (GBA %.3f s = TAPU_HIT_FRAME %d), loop %.1f s' % (
        HIT_SECONDS, HIT_SECONDS_GBA, round(HIT_SECONDS_GBA * 60), NBARS * 4 * 60 / BPM))
    if render_dir:
        render_gm(render_dir)
    if frag_dir:
        fragments(frag_dir)


KIT = [   # vanaf noot 36; eigen samples (tapu_samples.py) + stock Emerald; een slag klinkt door tot RING/de volgende
    'voice_directsound 60, 0, DirectSoundWaveData_tapu_taiko, 255, 0, 255, 190',                    # 36 taiko
    'voice_directsound 56, 0, DirectSoundWaveData_tapu_taiko, 255, 0, 255, 190',                    # 37 taiko laag
    'voice_directsound 60, 0, DirectSoundWaveData_tapu_odaiko, 255, 0, 255, 205',                   # 38 odaiko (grote trom)
    'voice_directsound 60, 0, DirectSoundWaveData_unused_heart_of_asia_indian_drum, 255, 0, 255, 140',  # 39 Indiase trom
    'voice_directsound 60, 0, DirectSoundWaveData_unused_sc55_tom, 255, 0, 255, 150',               # 40 tom
    'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_open_low_conga, 255, 0, 255, 80',         # 41 conga laag
    'voice_directsound_no_resample 64, 0, DirectSoundWaveData_sc88pro_mute_high_conga, 255, 0, 255, 60',  # 42 conga hoog
    'voice_directsound 60, 0, DirectSoundWaveData_tapu_ka, 255, 0, 255, 150',                       # 43 ka (rand)
    'voice_directsound 60, 0, DirectSoundWaveData_ethnic_flavours_kotsuzumi, 255, 0, 255, 110',     # 44 kotsuzumi
    'voice_directsound 60, 0, DirectSoundWaveData_tapu_crash, 255, 0, 255, 225',                    # 45 bekken
    'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_tambourine, 255, 0, 255, 90',             # 46 tamboerijn
    'voice_directsound 60, 0, DirectSoundWaveData_ethnic_flavours_hyoushigi, 255, 0, 255, 90',      # 47 hyoushigi
    'voice_directsound 60, 0, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 120',      # 48 kick
    'voice_directsound 60, 0, DirectSoundWaveData_tapu_impact, 255, 0, 255, 230',                   # 49 v4: HIT-impact
]


def write_voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Battle! Tapu (v2). Gegenereerd door tools/grounded/tapu_theme.py.'
    lines[1] = ('@ 52 chant-ha / 53 HOO-kreet / 54 lage hu (eigen formant-samples, tapu_samples.py), 77 shakuhachi, '
                '127 = drumkit tapu (odaiko/taiko/ka/bekken eigen samples).')
    lines[2] = 'voice_group %s' % VG
    repl = {
        '@ 52': '\tvoice_directsound 60, 0, DirectSoundWaveData_tapu_vox_a, 255, 0, 255, 90  @ 52',
        '@ 38': '\tvoice_directsound 60, 0, DirectSoundWaveData_tapu_synth, 255, 0, 255, 120  @ 38',
        '@ 80': '\tvoice_square_1 60, 0, 0, 2, 0, 2, 9, 1  @ 80',
        '@ 81': '\tvoice_directsound 60, 0, DirectSoundWaveData_tapu_brass, 255, 0, 255, 200  @ 81',
        '@ 82': '\tvoice_directsound 60, 0, DirectSoundWaveData_tapu_brass_hi, 255, 0, 255, 200  @ 82',
        '@ 54': '\tvoice_directsound 60, 0, DirectSoundWaveData_tapu_vox_hu, 255, 0, 255, 150  @ 54',
        '@ 77': '\tvoice_directsound 60, 0, DirectSoundWaveData_sd90_classical_shakuhachi, 255, 0, 255, 160  @ 77',
        '@ 127': '\tvoice_keysplit_all voicegroup_tapu_drumset  @ 127',
    }
    out = []
    for l in lines:
        tag = '@' + l.rsplit('@', 1)[1] if '@' in l and l.startswith('\t') else None
        out.append(repl.get(tag.strip() if tag else None, l))
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    open('sound/voicegroups/drumsets/tapu.inc', 'w').write(
        '@ Project Grounded: drumkit voor Battle! Tapu v2 (tapu_theme.py): 36/37 taiko (hoog/laag), 38 odaiko, 43 ka,\n'
        '@ 45 bekken (eigen samples, tapu_samples.py); 39 Indiase trom, 40 tom, 41/42 conga, 44 kotsuzumi, 46 tamboerijn,\n'
        '@ 47 hyoushigi, 48 kick (stock).\n'
        'voice_group tapu_drumset, 36\n' + ''.join('\t%s\n' % k for k in KIT) + '\n')


# ---- offline-render (FluidR3 GM; andere klanken dan de GBA, wel noten/vorm/tempo) ------------------------------------
GM_PROG = {'chant': 52, 'chlo': 53, 'syn': 62, 'horn': 60, 'hi': 77, 'pips': 72, 'bass': 38, 'pad': 48, 'pulse': 45,
           'synp': 80, 'hat': 122, 'timp': 47}
GM_DRUM = {TAIKO: 41, TAIKO_LO: 43, BIGTOM: 35, INDIAN: 45, TOM: 47, CONGA_LO: 64, CONGA_HI: 62, OHTSU: 60,
           KOTSU: 61, CRASH: 49, TAMB: 54, HYOU: 76, KICK: 36, IMPACT: 35}


def gm_midi(path, only=None):
    """GM-versie van de MIDI (voor FluidR3); only = set van spoornamen (solo)."""
    m = mido.MidiFile(OUT)
    gm = mido.MidiFile(type=1, ticks_per_beat=m.ticks_per_beat)
    gm.tracks.append(m.tracks[0])
    free = [c for c in range(16) if c != 9]
    for i, (k, prog, vol, pan) in enumerate(TRACKS):
        if only and k not in only:
            continue
        drum = prog == DRUMS
        ch = 9 if drum else free.pop(0)
        t = mido.MidiTrack()
        for x in m.tracks[i + 1]:
            if x.type == 'program_change':
                x = x.copy(channel=ch, program=0 if drum else GM_PROG[k])
            elif x.type in ('note_on', 'note_off'):
                x = x.copy(channel=ch, note=GM_DRUM.get(x.note, 47)) if drum else x.copy(channel=ch)
            elif hasattr(x, 'channel'):
                x = x.copy(channel=ch)
            t.append(x)
        gm.tracks.append(t)
    gm.save(path)


def fluid(mid, wav):
    subprocess.run(['fluidsynth', '-ni', '-g', '0.5', '-r', '44100', '-F', wav, '/usr/share/sounds/sf2/FluidR3_GM.sf2',
                    mid], check=True, capture_output=True)


def render_gm(outdir):
    os.makedirs(outdir, exist_ok=True)
    mid = os.path.join(outdir, 'tapu_gm.mid')
    gm_midi(mid)
    wav = os.path.join(outdir, 'tapu_fluidr3.wav')
    fluid(mid, wav)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-b:a', '160k', wav[:-4] + '.mp3'], check=True)
    os.remove(wav)
    print('render:', wav[:-4] + '.mp3')


FRAGS = {   # naam: (sporen, beginmaat origineel, lengte s)
    'a_melodie': ({'horn', 'hi', 'pad'}, 29, 24),
    'b_chants': ({'chant', 'chlo'}, 1, 24),
    'b2_chants': ({'chant', 'chlo'}, 48, 18),
    'f_synth': ({'syn', 'synp'}, 1, 25),
    'c_bas': ({'bass'}, 13, 22),
    'd_drums': ({'taiko', 'toms', 'perc', 'cym', 'timp'}, 1, 24),
    'e_alles': (None, 1, 24),
    'e2_alles': (None, 29, 24),
}


def fragments(outdir, src_mp3=None):
    os.makedirs(outdir, exist_ok=True)
    sec_bar = 4 * 60 / BPM
    for name, (only, ob, ln) in FRAGS.items():
        mid = os.path.join(outdir, 'tmp_%s.mid' % name)
        gm_midi(mid, only)
        wav = mid[:-4] + '.wav'
        fluid(mid, wav)
        st = (ob - 1) * sec_bar
        mp3 = os.path.join(outdir, 'fluid_%s.mp3' % name)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', '%.3f' % st, '-t', str(ln), '-i', wav, '-af',
                        'loudnorm=I=-16:TP=-1.5,afade=t=out:st=%.1f:d=1' % (ln - 1), '-ar', '44100', '-b:a', '160k', mp3], check=True)
        os.remove(wav)
        os.remove(mid)
        if src_mp3:
            ost = ORIG_BAR1 + (ob - 1) * sec_bar
            om = os.path.join(outdir, 'orig_%s.mp3' % name)
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', '%.3f' % max(0, ost - 0.05), '-t', str(ln),
                            '-i', src_mp3, '-af', 'loudnorm=I=-16:TP=-1.5,afade=t=out:st=%.1f:d=1' % (ln - 1), '-ar', '44100', '-b:a', '160k', om], check=True)
        print('fragment', name, 'vanaf maat %d (%.2f s in de MIDI)' % (ob, st))


if __name__ == '__main__':
    rd = sys.argv[sys.argv.index('--render') + 1] if '--render' in sys.argv else None
    fd = sys.argv[sys.argv.index('--frag') + 1] if '--frag' in sys.argv else None
    src = sys.argv[sys.argv.index('--orig') + 1] if '--orig' in sys.argv else None
    build(rd, None)
    if fd:
        fragments(fd, src)
