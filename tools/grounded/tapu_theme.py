#!/usr/bin/env python3
"""Project Grounded: "Battle! Tapu" (Pokémon Sun/Moon), transcriptie + arrangement, FASE 1 (noten en ritme).

Bron: alleen de mp3 (geen MIDI). Werkwijze fase 1: Spleeter (4 stems) + basic-pitch per stem + CQT/onset-analyse per
16e op een vast raster (174 bpm, maat 1 = 0,740 s in de mp3). Jordi: "het belangrijkste zijn de chants en de luide
tribal-drums; bijna ritualistisch". Dit is nog GEEN definitieve mix: alleen noten/ritme om per partij te beoordelen.

Gemeten aan het origineel (180 s, twee keer de loop + fade):
  tempo 174 bpm (autocorrelatie van de onsets, 128 tellen), 4/4, loop = 60 maten = 82,8 s (zelfgelijkenis, lag 82,80 s);
  het origineel begint meteen met de eerste grote slag (0,72-0,74 s = maat 1, tel 1) en springt na maat 60 terug naar
  maat 1. Toonsoort: E met b2/b5 (E-F-G-A-Bb-C-D#: 'E-locrisch/frygisch met tritonus'), bas-ostinato op E met
  Bb-A-G; het slot (maat 53-60) zakt naar G#m en een Bb-pedaal (tritonus van E).
  Vorm (maten van het origineel, ob = 1..60):
    1-4    HIT + koor-/strijkersakkoord F#4-C5-E5-C6 (tritonus F#-C), bas-loopje C# D# F G (heeltoons)
    5-8    vooral drums; maat 5 een uitgeroepen A#4 ('HAA'), maat 7-8 aanzwellende clusters
    9-12   tremolo B3+F4 (tritonus) in 16en, drums bouwen op; maat 12 bas F2 (b2) + de chant valt in op tel 4 (B3-kreet)
    13-28  groove: bas-ostinato E E E E . Bb A G, taiko-patroon (tellen 1,2,3,'3-en',4), chant op Bb4/Eb5/D5 (13-16),
           daarna losse chant-lettergrepen en kreten (17-24); elke 4e maat een variant (Bb-A-G-loopje of C-pedaal)
    29-36  overmatige akkoorden (F+ / E+ / F+ / Ab-C-Eb), hoorn-melodie A4-C#5 / C5-G#4, staccato C4-pulsen op 6 en 14
    37-48  E5-kwartnoten (37-40), E6-kwartnoten met G6 (41-46), overmatige melodie terug (46-48)
    49-52  tweede chant (E4..E5, G#4/C#5), hoge wisselfiguur A5/F#5 -> G#5/B5, bas F#2/A2
    53-60  slot: G#2/B2 (53-56) -> Bb1-pedaal (57-60), wisselfiguur A#5/C#6 -> A#5/E5 -> G5/E5, vier-op-de-vloer-kick
In de game: 3 maten 'licht' voorspel (4,14 s), dan de HIT = maat 1 van het origineel = loopbegin. De Tapu-transitie
eindigt precies op HIT_SECONDS (hieronder). Loop [ = HIT, ] = einde maat 60 (terug naar de HIT, zoals het origineel).

Voicegroup grounded_tapu (gegenereerd) = grounded_gm met alleen stock-Emerald-samples: 52 koor 'aah'
(classical_choir_voice_ahhs), 53 mannenstem (unused_unknown_male_voice, kreten), 48-50 strijkers (keysplit),
60 hoorn (keysplit), 77 shakuhachi (sd90_classical_shakuhachi, hoge wisselfiguur), 33 fingered bass, 47 pauk,
127 = drumkit drumsets/tapu.inc (taiko, ambient tom, Indiase trom, SC-55-tom, conga's, ohtsuzumi/kotsuzumi,
orkestbekken, tamboerijn, hyoushigi, kick; geen PSG).
Gebruik: python3 tools/grounded/tapu_theme.py [--render <map>] [--frag <map>]"""
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
PRE = 3                                    # maten voorspel vóór de HIT
HIT_TICK = PRE * BAR                       # = loopbegin
HIT_SECONDS = PRE * 4 * 60 / BPM           # 4,138 s nominaal ...
HIT_SECONDS_GBA = HIT_SECONDS * 1.0045     # ... 4,156 s op de GBA (die speelt 0,45% te traag, MUZIEK.md)
ORIG_HIT_SECONDS = 0.74                    # de eerste grote slag + koor in de mp3 (maat 1, tel 1)
NBARS = 60                                 # loop = maat 1-60 van het origineel
END = PRE + NBARS

CHOIR, SHOUT, STR, STR2, STR3, HORN, SHAKU, BASS, TIMP, DRUMS = 52, 53, 48, 49, 50, 60, 77, 33, 47, 127
# drumkit (drumsets/tapu.inc, vanaf 36)
TAIKO, TAIKO_LO, BIGTOM, INDIAN, TOM, CONGA_LO, CONGA_HI, OHTSU, KOTSU, CRASH, TAMB, HYOU, KICK = range(36, 49)

N = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8,
     'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def p(name):
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


def at(ob, q=0):
    """tick van 16e q in maat ob van het origineel (ob 1 = de HIT); ob <= 0 = voorspel."""
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
BC = [(0, 4, 'C2'), (4, 2, 'C3'), (6, 2, 'C2'), (8, 2, 'D2'), (10, 2, 'C3'), (12, 2, 'C2'), (14, 2, 'C3')]
BFS = [(i * 2, 2, 'F#2' if i % 2 == 0 else 'A2') for i in range(8)]
BGS = [(i * 2, 2, 'G#2' if i % 2 == 0 else 'B2') for i in range(8)]
BGS_END = BGS[:5] + [(10, 1, 'D2'), (11, 3, 'C#2'), (14, 2, 'B1')]
BBB = [(0, 2, 'A#1'), (2, 2, 'A#2'), (4, 2, 'A#1'), (6, 2, 'A#1'), (8, 2, 'A#1'), (10, 2, 'A#2'), (12, 2, 'A#1'),
       (14, 2, 'C#3')]
BBB_END = [(0, 4, 'A#1'), (4, 2, 'A#2'), (6, 2, 'A#1'), (8, 2, 'A#1'), (10, 2, 'A#2'), (12, 4, 'C#2')]
GROOVE = {13: BA, 14: BA, 15: BA, 16: BB, 17: BA, 18: BA, 19: BAC, 20: BC, 21: BA, 22: BA, 23: BAC, 24: BB,
          25: BA, 26: BA, 27: BAC, 28: BC, 29: BA, 30: BA, 31: BAC, 32: BB, 33: BA, 34: BA, 35: BAC, 36: BC,
          37: BA2, 38: BA2, 39: BA2, 40: BA2, 41: BA, 42: BA, 43: BAC, 44: BB, 45: BA, 46: BA, 47: BAC, 48: BC,
          49: BA2, 50: BA2, 51: BFS, 52: BFS, 53: BGS, 54: BGS, 55: BGS, 56: BGS_END,
          57: BBB, 58: BBB, 59: BBB, 60: BBB_END}


def bass():
    out = []
    put(out, 1, [(1, 3, 'C#2'), (4, 3, 'D#2'), (7, 2, 'C#2'), (9, 2, 'F2'), (11, 1, 'G2'), (12, 3, 'C#2'), (15, 1, 'D#2')])
    put(out, 2, [(0, 15, 'C#2'), (15, 1, 'D2')])
    put(out, 3, [(1, 2, 'C2'), (3, 7, 'F2'), (10, 6, 'E2')])
    put(out, 4, [(0, 11, 'C#2'), (11, 5, 'C2')])
    put(out, 5, [(2, 3, 'C#2'), (5, 2, 'D2'), (7, 6, 'D2'), (13, 3, 'G#1')])
    put(out, 6, [(0, 6, 'G#1'), (6, 10, 'A1')])
    put(out, 7, [(0, 2, 'B1'), (2, 8, 'C#2'), (10, 2, 'A1'), (12, 4, 'A#1')])
    put(out, 8, [(0, 4, 'C#2'), (4, 3, 'D2'), (7, 5, 'G#1'), (12, 4, 'G#1')])
    put(out, 12, [(0, 16, 'F2')])                                     # b2 onder de chant-inzet
    for ob, pat in GROOVE.items():
        put(out, ob, pat, 104)
    # voorspel: lage E-drone die aanzwelt naar de HIT (licht: één noot per maat)
    for i, v in enumerate((60, 78, 96)):
        put(out, i + 1 - PRE, [(0, 16, 'E1', v)])
    return dedupe(out)


# ---------------------------------------------------------------- chant (stem 'vocals', CQT per 16e) -------------------
CHANT = [
    # maat 1-4: koorakkoord (E5 + F#4, C6 bovenin) meteen na de HIT; maat 5 de uitgeroepen A#4 staat bij SHOUTS
    '1:1:47:E5:96 1:1:47:F#4:92',
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
SHOUTS = [   # korte kreten (mannenstem): de luidste, breedbandige vocal-onsets
    '5:0:4:A#4:120 12:12:4:B3:124 14:9:3:B3:118 17:13:3:B3:118 24:8:1:A#4:110 24:9:3:A#4:124 48:11:1:A#4:116 '
    '52:0:1:A#4:112 56:13:1:A#4:112',
]


def chant():
    out = []
    for s in CHANT:
        notes_str(out, s, 100)
    # voorspel: koor zwelt aan (lange noot E4 + B4, steeds luider) naar de HIT
    put(out, 2 - PRE, [(8, 8, ['E4', 'B4'], 56)])
    put(out, 3 - PRE, [(0, 16, ['E4', 'B4'], 80)])
    return dedupe(out)


def shouts():
    out = []
    for s in SHOUTS:
        notes_str(out, s)
    return dedupe(out)


# ---------------------------------------------------------------- strijkers / pad (stem 'other') ----------------------
def pad():
    out = []
    put(out, 1, [(1, 41, ['C5', 'C6'], 90)])                         # maat 1-3 (+ half 4): tritonusakkoord met het koor
    put(out, 7, [(0, 16, ['F4', 'F#4'], 64)])                        # aanzwellende clusters
    put(out, 8, [(0, 8, ['G#4', 'A4'], 76), (8, 8, ['G#4', 'A4'], 92)])
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
    put(out, 57, [(0, 64, ['A#3', 'F4'], 74)])
    return dedupe(out)


def tremolo():
    out = []
    for ob in range(9, 13):
        for q in range(16):
            if ob == 9 and q < 8 or ob == 12 and q >= 12:
                continue
            v = 50 + (ob - 9) * 14 + q
            put(out, ob, [(q, 1, ['B3', 'F4'], min(v, 112))])
    return dedupe(out)


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
    '57:0:2:A#5 57:2:2:A#5 57:4:2:A#5 57:6:4:E5 57:10:2:A#5 57:12:2:E5 57:14:1:E5 57:15:1:A#5',
    '58:0:1:A#5 58:1:4:E5 58:5:2:A#5 58:7:2:E5 58:9:2:E5 58:11:2:E5 58:13:2:A#5 58:15:1:E5',
    '59:0:1:D#5 59:1:5:G5 59:6:2:E5 59:8:3:E5 59:11:1:E5 59:13:1:E5 59:14:2:G5 60:0:3:E5 60:3:7:G5 60:10:2:E5',
]


def horn():
    out = []
    for s in HORN_MEL:
        notes_str(out, s, 100)
    return dedupe(out)


def hi():
    out = []
    for s in HI_MEL:
        notes_str(out, s, 96)
    for ob in range(53, 57):                                          # A#5/C#6 in achtsten
        put(out, ob, [(q * 2, 2, 'A#5' if q % 2 == 0 else 'C#6', 92) for q in range(8)])
    return dedupe(out)


# ---------------------------------------------------------------- drums (stem 'drums', onsets per band per 16e) -------
def drums():
    t, m, pc, cr, tp = [], [], [], [], []    # taiko/grote trommen, middentrommen/toms, kleine percussie, bekkens, pauk

    def hit(lst, ob, q, note, vel, ln=2):
        lst.append([at(ob, q), at(ob, q) + ln * S16, note, vel])

    # voorspel (licht): maat -2 pauk-roffel pp, maat -1 handtrommen in achtsten, maat 0 taiko-opbouw + flam naar de HIT
    for q in range(0, 16, 2):
        hit(tp, 1 - PRE, q, p('E2'), 40 + q * 2, 2)
    for q in range(0, 16):
        hit(tp, 2 - PRE, q, p('E2'), 56 + q * 2, 1)
    for q in range(0, 16, 2):
        hit(m, 2 - PRE, q, CONGA_LO if q % 4 == 0 else CONGA_HI, 56 + q * 2)
    for q in (0, 4, 8, 10, 12, 13, 14, 15):
        hit(t, 3 - PRE, q, TAIKO if q < 12 else TAIKO_LO, 80 + q * 3)
    for q in range(0, 16):
        hit(m, 3 - PRE, q, TOM if q % 2 else INDIAN, 70 + q * 3)
    hit(pc, 3 - PRE, 14, OHTSU, 110)

    # maat 1-12 (intro): per 16e uit de drumstem (onsets per band): LAAG = taiko/grote trom, KRAK = scherpe tik
    # (mid+hoog: ohtsuzumi), MID = middentrom (alleen mid: maat 9-12 op 1 en 3). Getallen = gemeten sterkte.
    LOW = {1: {0: 281, 6: 48, 8: 42, 10: 46, 12: 88, 14: 44}, 2: {0: 175, 1: 69, 7: 67, 9: 55, 14: 154, 15: 93},
           3: {4: 104, 7: 135, 8: 125, 13: 102, 14: 72}, 4: {1: 67, 5: 78, 7: 87, 8: 133, 15: 81},
           5: {2: 92, 3: 63, 6: 76, 11: 69, 13: 100, 14: 68}, 6: {0: 224, 3: 84, 5: 90, 12: 61, 13: 76, 14: 87, 15: 95},
           7: {0: 75, 1: 98, 2: 62, 8: 88, 12: 67, 13: 79}, 8: {0: 105, 1: 83, 9: 82},
           9: {0: 236, 2: 106, 3: 159, 4: 175, 8: 184, 9: 138, 12: 114, 14: 81},
           10: {0: 97, 1: 127, 6: 102, 8: 88, 9: 98, 12: 119, 15: 75},
           11: {0: 188, 3: 66, 4: 112, 8: 145, 12: 128, 14: 96}, 12: {0: 123, 4: 155, 5: 95, 8: 84, 12: 75}}
    CRACK = {1: {0: 65}, 2: {0: 81, 14: 87, 15: 22}, 3: {0: 61, 14: 56}, 4: {0: 50, 7: 62, 9: 29, 10: 61, 14: 49},
             5: {0: 68}, 6: {0: 97, 14: 88, 15: 24}, 7: {0: 66, 9: 61, 10: 50, 14: 23}, 8: {1: 61, 3: 45, 13: 36, 14: 35, 15: 26}}
    MID = {9: {0: 28, 8: 139}, 10: {0: 73, 8: 100}, 11: {0: 59, 8: 96}, 12: {0: 84, 4: 60, 8: 133}}
    vel = lambda x, top: int(min(127, 58 + 69 * min(x, top) / top))
    for ob, d in LOW.items():
        for q, x in d.items():
            hit(t, ob, q, BIGTOM if x >= 170 else (TAIKO if x >= 95 else TAIKO_LO), vel(x, 250), 3)
    for ob, d in CRACK.items():
        for q, x in d.items():
            hit(pc, ob, q, OHTSU, vel(x, 90))
    for ob, d in MID.items():
        for q, x in d.items():
            hit(m, ob, q, INDIAN, vel(x, 140))
    hit(t, 1, 0, TAIKO, 127, 4)                                        # HIT: twee lagen (grote trom + taiko)
    hit(cr, 1, 0, CRASH, 120, 8)
    for q in range(8, 16):                                            # maat 8: pauk-roffel crescendo naar maat 9
        hit(tp, 8, q, p('E2'), 70 + (q - 8) * 7, 1)
    for q in (12, 13, 14, 15):
        hit(m, 12, q, TOM, 100 + (q - 12) * 6)
    # groove maat 13-60 (gemiddeld per 16e gemeten): slagen op 1, 2, 3, '3-en', 4 (laag+mid); in maat 13-52 klinkt
    # na elke tel een zachtere tweede slag (16e 1, 5, 9, 13: 'DUM-dum'); hoog alleen zwak op 2 en 4 (hyoushigi pp)
    for ob in range(13, NBARS + 1):
        for q, n, v in ((0, TAIKO, 118), (4, BIGTOM, 108), (8, TAIKO, 120), (10, TAIKO_LO, 108), (12, BIGTOM, 112)):
            hit(t, ob, q, n, v)
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
    return {'taiko': dedupe(t), 'toms': dedupe(m), 'perc': dedupe(pc), 'cym': dedupe(cr), 'timp': dedupe(tp)}


# ---------------------------------------------------------------- sporen ----------------------------------------------
TRACKS = [   # (naam, programma, volume, pan)
    ('chant', CHOIR, 110, 64), ('shout', SHOUT, 104, 64), ('horn', HORN, 92, 56), ('hi', SHAKU, 84, 72),
    ('bass', BASS, 110, 64), ('pad', STR, 64, 64), ('pulse', STR2, 78, 60), ('trem', STR3, 70, 68),
    ('taiko', DRUMS, 120, 64), ('toms', DRUMS, 100, 58), ('perc', DRUMS, 84, 74), ('cym', DRUMS, 80, 64),
    ('timp', TIMP, 90, 64),
]
MAX_V = 11                    # legendary: 11 DirectSound-noten (1 kanaal vrij voor effecten)


def kit_releases():
    return {36 + i: int(l.split(',')[-1]) for i, l in enumerate(KIT)}


def build(render_dir=None, frag_dir=None):
    write_voicegroup()
    rel = releases(VG)
    kitrel = kit_releases()
    parts = {'chant': chant(), 'shout': shouts(), 'horn': horn(), 'hi': hi(), 'bass': bass(), 'pad': pad(),
             'pulse': pulses(), 'trem': tremolo()}
    parts.update(drums())
    melodic = {'chant': CHOIR, 'shout': SHOUT, 'horn': HORN, 'hi': SHAKU, 'bass': BASS, 'pad': STR, 'pulse': STR2,
               'trem': STR3, 'timp': TIMP}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) + 2 for k, pr in melodic.items()}
    dl = max(release_ticks(r, TPB, BPM) for r in kitrel.values())
    for k in ('taiko', 'toms', 'perc', 'cym'):
        tail[k] = dl // 2
    for k in ('chant', 'horn', 'hi', 'bass', 'pulse', 'timp', 'pad', 'trem'):
        parts[k] = detach(parts[k], tail[k])
    order = ['taiko', 'cym', 'chant', 'shout', 'bass', 'toms', 'horn', 'hi', 'timp', 'pulse', 'perc', 'pad', 'trem']
    kept = allocate({k: parts[k] for k in order}, order, tail, max_voices=MAX_V)
    print('uitklinktijd (ticks):', tail)
    for k in order:
        n = len(parts[k])
        gone = sorted({(e[0] // BAR) - PRE + 1 for e in parts[k] if e not in kept[k]})
        print('  %-6s %4d noten, %3d vallen weg (%.1f%%)%s' % (k, n, n - len(kept[k]), 100 * (n - len(kept[k])) / max(n, 1),
                                                             ' (maten origineel %s)' % gone[:12] if gone else ''))
        parts[k] = kept[k]
    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.tempo(HIT_TICK, BPM / 120)                                   # tempo op de looptick zelf
    song.loop = (HIT_TICK, END * BAR)
    for ch, (k, prog, vol, pan) in enumerate(TRACKS):
        notes = parts[k]
        song.add(notes, prog, vol, ch, pan)
    song.save(OUT, END * BAR)
    print(OUT, 'voorspel %.3f s (HIT_SECONDS; GBA %.3f s), loop %.1f s' % (HIT_SECONDS, HIT_SECONDS_GBA,
                                                                          NBARS * 4 * 60 / BPM))
    if render_dir:
        render_gm(render_dir)
    if frag_dir:
        fragments(frag_dir)


KIT = [   # vanaf noot 36; alles DirectSound (stock Emerald)
    'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 140',                 # 36 taiko
    'voice_directsound 53, 0, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 140',                 # 37 taiko laag
    'voice_directsound 60, 0, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 150',              # 38 grote trom
    'voice_directsound 60, 0, DirectSoundWaveData_unused_heart_of_asia_indian_drum, 255, 0, 255, 120',  # 39 Indiase trom
    'voice_directsound 60, 0, DirectSoundWaveData_unused_sc55_tom, 255, 0, 255, 130',               # 40 tom
    'voice_directsound 60, 44, DirectSoundWaveData_sc88pro_open_low_conga, 255, 0, 255, 80',        # 41 conga laag
    'voice_directsound_no_resample 64, 84, DirectSoundWaveData_sc88pro_mute_high_conga, 255, 0, 255, 60',  # 42 conga hoog
    'voice_directsound 60, 80, DirectSoundWaveData_ethnic_flavours_ohtsuzumi, 255, 0, 255, 110',    # 43 ohtsuzumi
    'voice_directsound 60, 48, DirectSoundWaveData_ethnic_flavours_kotsuzumi, 255, 0, 255, 110',    # 44 kotsuzumi
    'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 216',  # 45 orkestbekken
    'voice_directsound 60, 80, DirectSoundWaveData_sc88pro_tambourine, 255, 0, 255, 90',            # 46 tamboerijn
    'voice_directsound 60, 40, DirectSoundWaveData_ethnic_flavours_hyoushigi, 255, 0, 255, 90',     # 47 hyoushigi
    'voice_directsound 60, 0, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 120',      # 48 kick
]


def write_voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Battle! Tapu (fase 1). Gegenereerd door tools/grounded/tapu_theme.py.'
    lines[1] = ('@ alleen stock-samples: 52 koor, 53 mannenstem (kreten), 77 shakuhachi, 127 = drumkit tapu '
                '(taiko/trommen/conga/tsuzumi/bekken/tamboerijn/kick).')
    lines[2] = 'voice_group %s' % VG
    repl = {
        '@ 53': '\tvoice_directsound 60, 0, DirectSoundWaveData_unused_unknown_male_voice, 255, 0, 255, 150  @ 53',
        '@ 77': '\tvoice_directsound 60, 0, DirectSoundWaveData_sd90_classical_shakuhachi, 255, 0, 255, 160  @ 77',
        '@ 127': '\tvoice_keysplit_all voicegroup_tapu_drumset  @ 127',
    }
    out = []
    for l in lines:
        tag = '@' + l.rsplit('@', 1)[1] if '@' in l and l.startswith('\t') else None
        out.append(repl.get(tag.strip() if tag else None, l))
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    open('sound/voicegroups/drumsets/tapu.inc', 'w').write(
        '@ Project Grounded: drumkit voor Battle! Tapu (tapu_theme.py), alleen stock-samples: 36/37 taiko (hoog/laag),\n'
        '@ 38 grote trom (ambient tom), 39 Indiase trom, 40 tom, 41/42 conga, 43 ohtsuzumi, 44 kotsuzumi, 45 orkestbekken,\n'
        '@ 46 tamboerijn, 47 hyoushigi, 48 kick.\n'
        'voice_group tapu_drumset, 36\n' + ''.join('\t%s\n' % k for k in KIT) + '\n')


# ---- offline-render (FluidR3 GM; andere klanken dan de GBA, wel noten/vorm/tempo) ------------------------------------
GM_PROG = {'chant': 52, 'shout': 53, 'horn': 60, 'hi': 77, 'bass': 33, 'pad': 48, 'pulse': 45, 'trem': 44,
           'timp': 47}
GM_DRUM = {TAIKO: 41, TAIKO_LO: 43, BIGTOM: 35, INDIAN: 45, TOM: 47, CONGA_LO: 64, CONGA_HI: 62, OHTSU: 60,
           KOTSU: 61, CRASH: 49, TAMB: 54, HYOU: 76, KICK: 36}


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
    'b_chants': ({'chant', 'shout'}, 1, 24),
    'b2_chants': ({'chant', 'shout'}, 48, 18),
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
        st = HIT_SECONDS + (ob - 1) * sec_bar
        mp3 = os.path.join(outdir, 'fluid_%s.mp3' % name)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', '%.3f' % st, '-t', str(ln), '-i', wav, '-af',
                        'loudnorm=I=-16:TP=-1.5,afade=t=out:st=%.1f:d=1' % (ln - 1), '-ar', '44100', '-b:a', '160k', mp3], check=True)
        os.remove(wav)
        os.remove(mid)
        if src_mp3:
            ost = ORIG_HIT_SECONDS + (ob - 1) * sec_bar
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
