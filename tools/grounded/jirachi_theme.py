#!/usr/bin/env python3
"""Project Grounded: Battle! Jirachi, een eigen compositie (Jordi: "heel hoopvol, licht en vrolijk, wat past bij een
wishmaker"). Een legendary-gevecht met drive, maar als een sterrenhemel: celesta, speeldoos, glockenspiel, harp,
fluit, pizzicato en lange strijkers, zachte koortjes, triangel en een windgong (vallende sterren), warme bas.

152 bpm, D-groot (climax in E-groot). 1 tel = 23,7 frames, 1 maat = 1,58 s.
Hook = het 'wens'-motief: een sprong omhoog naar een voorhoudingsnoot die een stap omlaag oplost (A4 -> G5 -> F#5).

Intro = de transitie (B_TRANSITION_JIRACHI, src/battle_transition.c): de muziek begint met een opmaat van 4 tellen.
Gemeten in de emulator (gMPlayInfo_BGM.clock tegen de helderheid van het beeld): de transitie begint ±25 frames na de
muziek, dus transitieframe t valt op muziektel 1 + t / 23,7.
  tel 0            : het beeld dimt -> zachte koor/strijkers
  tel 1 (t = 0)    : de ster verschijnt -> windgong + dalende celesta (het spoor van fonkelingen)
  tel 3 (t = 44)   : de ster duikt terug -> harpglissando omhoog
  tel 4 (t = 68)   : de wens, alles wordt goudwit = maat 1 tel 0 -> bekken, triangel, belakkoord, pauk
  maat 1-4         : speeldoos speelt het wensmotief (het gevechtsscherm komt op; de cry van Jirachi valt in maat 2-3)
  maat 5-6         : opbouw: pizzicato, stijgende strijkers, roffel, pauken, harpglissando + windgong
Loop (56 maten, ±85 s; v2 = v1 tot de opbouw, daarna een euforische trance-climax op verzoek van Jordi):
  A  (0-7)   thema op fluit + glockenspiel, pizzicato, harp-arpeggio's, huppelende bas
  A' (8-15)  thema op strijkers + fluit een octaaf hoger, hogere afsluiting
  B  (16-19) avontuur: hoorn met een heldhaftig tegenthema, spiccato-strijkers, celesta-antwoorden, pauken
  opbouw (20-23, 42,6 s) Bm-G-Em-A, tempo 152 -> 168: supersaw 'filter' gaat open, roffel versnelt, riser, adem
  drop 1 (24-31, 48,7 s) trance 168 bpm: wensmotief op supersaw-lead, gated supersaw, off-beat bas, 4/4-kick, clap
  breakdown (32-35, 60,1 s) G-Gm-D-A, alleen pad + lead (+ speeldoos), mini-opbouw
  drop 2 (36-43, 65,8 s) groter (glockenspiel op de lead, koor), laatste maat ritardando naar 152 + glissando
  D  (44-51, 77,3 s) het thema in E-groot een octaaf hoger (fluit + strijkers + glockenspiel), hoorn, koor, bekkens
  E  (52-55) C-D-G-A: het wensmotief stijgt in sequens, roffel + harpglissando terug naar A
Voicegroup grounded_jirachi = grounded_gm + eigen samples (gm_samples.py: jirachi_celesta, jirachi_music_box,
jirachi_chimes; jirachi_samples.py: supersaws, sawbas, trancekick) + eigen drumkit (drumsets/jirachi.inc, alles DirectSound). Zie tools/grounded/MUZIEK.md.
Gebruik: python3 tools/grounded/jirachi_theme.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

OUT = 'sound/songs/midi/mus_grounded_vs_jirachi.mid'
VG = 'grounded_jirachi'
TPB, BPM = 96, 152
S16 = TPB // 4
E8 = TPB // 2
BAR = TPB * 4
PICK = 4 * TPB                      # opmaat (de transitie), gemeten: de flits valt op muziektel 4
MAX_VOICES = 11                     # legendary

CELESTA, GLOCK, MBOX, PIZZ, HARP, TIMP, STR, CHOIR, HORN, FLUTE, BASS, DRUMS = 8, 9, 10, 45, 46, 47, 48, 52, 60, 73, 33, 127
SPARK, SHAKER = 81, 120            # PSG
# trance-climax (v2): eigen samples uit jirachi_samples.py
SAW_DARK, SAW_MID, SAW_BRIGHT, SAW_LEAD, SAW_PLUCK, SAW_BASS = 88, 89, 90, 91, 92, 39
SUB, RISER, HATS = 84, 121, 122    # PSG: golf (sub), ruis (riser, open/dichte hihats)
BPM_TR = 168                       # tempo van de climax
TKICK, CLAP, TSNARE = 43, 44, 45
# eigen drumkit (drumsets/jirachi.inc, vanaf noot 36)
KICK, ROLL, SNARE, CRASH, TRI, CHIMES, JINGLE = 36, 37, 38, 39, 40, 41, 42

INTRO_BARS = 6                      # maat 1-6
LOOP_BAR = INTRO_BARS + 1           # songmaat 7 = loopmaat 0
LOOP_LEN = 56
A0, A1, B0, BUILD0, DROP1, BREAK0, DROP2, D0, E0 = 0, 8, 16, 20, 24, 32, 36, 44, 52
SECTIONS = [('A', A0), ('A2', A1), ('B', B0), ('BUILD', BUILD0), ('DROP1', DROP1), ('BREAK', BREAK0),
            ('DROP2', DROP2), ('D', D0), ('E', E0)]


def section(lb):
    name, st = [x for x in SECTIONS if x[1] <= lb][-1]
    return name, lb - st

N = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'Ab': 8,
     'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def p(name):
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


def t(sb):
    """begin van songmaat sb (1 = na de opmaat)."""
    return PICK + (sb - 1) * BAR


def lt(lb):
    """begin van loopmaat lb."""
    return t(LOOP_BAR + lb)


LOOP_START, LOOP_END = lt(0), lt(LOOP_LEN)

QUAL = {'': (0, 4, 7), 'm': (0, 3, 7), '7': (0, 4, 7, 10), 'm7': (0, 3, 7, 10)}


def chord(name):
    root = name[:2] if len(name) > 1 and name[1] in '#b' else name[:1]
    return N[root], QUAL[name[len(root):]]


# akkoorden per maat (één of twee per maat)
INTRO = ['D', 'Bm', 'G', 'A', 'G', 'A']
LOOP = (['D', 'Bm', 'G', 'A', 'D', 'B7', ('Em', 'Gm'), ('D', 'A')] +                    # A
        ['D', 'Bm', 'G', 'A', 'D', 'G', ('Em7', 'A7'), 'D'] +                          # A'
        ['Bm', 'G', 'D', 'A'] +                                                        # B (eerste helft)
        ['Bm', 'G', 'Em', 'A'] +                                                       # opbouw (152 -> 168 bpm)
        ['D', 'Bm', 'G', 'A', 'D', 'Bm', 'G', 'A'] +                                   # drop 1 (trance, 168 bpm)
        ['G', 'Gm', 'D', 'A'] +                                                        # breakdown (pad + lead)
        ['D', 'Bm', 'G', 'A', 'D', 'Bm', 'G', 'B7'] +                                  # drop 2 (ritardando -> E)
        ['E', 'C#m', 'A', 'B', 'E', 'A', ('F#m7', 'B7'), 'E'] +                        # D (A' in E)
        ['C', 'D', 'G', 'A'])                                                          # E
assert len(LOOP) == LOOP_LEN


def chords_at(seq, bar_start, b):
    c = seq[b]
    halves = c if isinstance(c, tuple) else (c, c)
    return [(bar_start, halves[0]), (bar_start + 2 * TPB, halves[1])]


def tones(name, lo, hi):
    """akkoordtonen tussen lo en hi (oplopend)."""
    r, q = chord(name)
    return [n for n in range(lo, hi + 1) if (n - r) % 12 in q]


def bass_note(name):
    return 38 + (chord(name)[0] - 2) % 12          # D2..C#3


def mel(pattern, start, vel=110, shift=0):
    return [[start + st * S16, start + (st + ln) * S16, p(n) + shift, vel] for st, ln, n in pattern]


# --- melodieën (16e-stappen per maat) ------------------------------------------------------------------------------
THEME = [   # A (D-groot); het wensmotief = sprong omhoog naar een voorhouding die oplost
    [(0, 4, 'A4'), (4, 6, 'G5'), (10, 2, 'F#5'), (12, 2, 'E5'), (14, 2, 'F#5')],     # D
    [(0, 6, 'D5'), (6, 2, 'B4'), (8, 4, 'C#5'), (12, 4, 'D5')],                     # Bm
    [(0, 4, 'B4'), (4, 6, 'A5'), (10, 2, 'G5'), (12, 2, 'F#5'), (14, 2, 'G5')],     # G
    [(0, 6, 'E5'), (6, 2, 'F#5'), (8, 8, 'E5')],                                    # A
    [(0, 4, 'A4'), (4, 6, 'G5'), (10, 2, 'F#5'), (12, 2, 'A5'), (14, 2, 'B5')],     # D
    [(0, 6, 'B5'), (6, 2, 'A5'), (8, 4, 'F#5'), (12, 4, 'D#5')],                    # B7
    [(0, 4, 'E5'), (4, 4, 'G5'), (8, 6, 'Bb5'), (14, 2, 'A5')],                     # Em | Gm
    [(0, 8, 'F#5'), (8, 4, 'E5'), (12, 4, 'C#5')],                                  # D | A
]
THEME2_END = [   # A' maat 4-7: hoger, eindigt op de grondtoon
    [(0, 4, 'A4'), (4, 6, 'G5'), (10, 2, 'F#5'), (12, 2, 'A5'), (14, 2, 'D6')],     # D
    [(0, 8, 'D6'), (8, 4, 'B5'), (12, 4, 'G5')],                                    # G
    [(0, 4, 'E5'), (4, 4, 'G5'), (8, 4, 'B5'), (12, 4, 'C#6')],                     # Em7 | A7
    [(0, 12, 'D6'), (12, 4, 'A5')],                                                 # D
]
HEROIC = [   # B: hoorn
    [(0, 4, 'F#4'), (4, 2, 'B4'), (6, 2, 'C#5'), (8, 6, 'D5'), (14, 2, 'C#5')],     # Bm
    [(0, 4, 'B4'), (4, 4, 'G4'), (8, 8, 'D5')],                                     # G
    [(0, 4, 'A4'), (4, 2, 'D5'), (6, 2, 'E5'), (8, 6, 'F#5'), (14, 2, 'E5')],       # D
    [(0, 4, 'E5'), (4, 4, 'C#5'), (8, 8, 'A4')],                                    # A
    [(0, 4, 'F#4'), (4, 2, 'B4'), (6, 2, 'C#5'), (8, 6, 'D5'), (14, 2, 'E5')],      # Bm
    [(0, 4, 'D5'), (4, 2, 'E5'), (6, 2, 'F#5'), (8, 8, 'G5')],                      # G
    [(0, 6, 'G5'), (6, 2, 'F#5'), (8, 4, 'E5'), (12, 4, 'B4')],                     # Em
    [(0, 8, 'A#4'), (8, 4, 'C#5'), (12, 4, 'E5')],                                  # F#7
]
WISH = [   # C: het wensmotief vergroot, met de octaafsprong
    [(0, 4, 'D5'), (4, 12, 'D6')],                                                  # G
    [(0, 8, 'Bb5'), (8, 4, 'A5'), (12, 4, 'G5')],                                   # Gm
    [(0, 12, 'F#5'), (12, 4, 'A5')],                                                # D
    [(0, 8, 'A5'), (8, 4, 'F#5'), (12, 4, 'D#5')],                                  # B7
    [(0, 4, 'B4'), (4, 12, 'G5')],                                                  # Em
    [(0, 8, 'Bb5'), (8, 4, 'A5'), (12, 4, 'G5')],                                   # Gm
    [(0, 8, 'F#5'), (8, 8, 'A5')],                                                  # D
    [(0, 8, 'A5'), (8, 4, 'F#5'), (12, 4, 'D#5')],                                  # F#m7 | B7
]
RISE = [   # E: het motief in sequens omhoog
    [(0, 4, 'G4'), (4, 6, 'F5'), (10, 2, 'E5'), (12, 4, 'C5')],                     # C
    [(0, 4, 'A4'), (4, 6, 'G5'), (10, 2, 'F#5'), (12, 4, 'D5')],                    # D
    [(0, 4, 'B4'), (4, 6, 'A5'), (10, 2, 'G5'), (12, 4, 'D5')],                     # G
    [(0, 8, 'E5'), (8, 4, 'C#5'), (12, 4, 'E5')],                                   # A
]

BUILD_MEL = [   # opbouw maat 2-3: het wensmotief op de supersaw-lead, tel 4 van de laatste maat stil (de adem vóór de drop)
    [(0, 4, 'B4'), (4, 6, 'G5'), (10, 2, 'F#5'), (12, 4, 'E5')],                    # Em
    [(0, 4, 'C#5'), (4, 4, 'E5'), (8, 4, 'A5')],                                    # A
]
BREAK_MEL = WISH[:3] + [[(0, 8, 'E5'), (8, 4, 'C#5')]]                              # breakdown: G Gm D A
DROP_END = [(0, 6, 'F#5'), (6, 2, 'D#5'), (8, 4, 'F#5'), (12, 4, 'A5')]             # drop 2, laatste maat (B7 -> E)

PARTS = ('flute', 'glock', 'strmel', 'horn', 'mbox', 'celesta', 'harp', 'pizz', 'strings', 'choir', 'bass', 'timp',
         'drums', 'perc', 'spark', 'shaker',
         'tlead', 'tsaw', 'tbass', 'tpluck', 'tdrums', 'sub')


def trance(P, lb, s, sec, k, halves, gliss):
    """De euforische climax: opbouw (152 -> 168 bpm, 'filter' gaat open, roffel versnelt, riser), drop 1, breakdown
    (alleen pad + lead + speeldoos), drop 2 (groter: glockenspiel op de lead, koor in twee stemmen) en een ritardando
    terug naar 152 bpm en het thema in E (sectie D)."""
    name = halves[0][1]
    r = bass_note(name)
    pad = tones(name, 62, 76)[:3]
    last = sec == 'BUILD' and k == 3 or sec == 'BREAK' and k == 3      # tel 4 stil: de adem vóór de drop
    end = s + (3 * TPB if last else BAR)
    if sec == 'BUILD':
        if k < 2:                                                       # het heldhaftige tegenthema loopt door
            P['horn'] += mel(HEROIC[4 + k], s, 120)
        else:
            P['tlead'] += mel(BUILD_MEL[k - 2], s, 92 + 8 * (k - 2))
        if k == 0:
            P['perc'] += [[s, s + 2 * TPB, CRASH, 100]]
            P['timp'] += [[s, s + TPB, r + 12 if r < 45 else r, 108]]
        # supersaw-akkoord, filter gaat per maat verder open (dark -> mid -> bright; CC7 loopt mee op)
        P['tsaw'] += [[s, end - 8, n, 70 + 2 * k] for n in pad]
        # pluck-arpeggio: 16en, elke maat een register hoger
        tn = tones(name, 62 + 5 * k, 90)
        P['tpluck'] += [[s + i * S16, s + i * S16 + 8, tn[min((0, 1, 2, 1, 2, 3, 2, 3)[i % 8] + (i // 8), len(tn) - 1)], 52 + 6 * k + i]
                        for i in range(12 if last else 16)]
        # bas: achtsten, de laatste maat 16en
        step = S16 if k == 3 else E8
        P['tbass'] += [[s + i * step, s + i * step + step - 8, r, 82 + 6 * k] for i in range((3 * TPB) // step if last else BAR // step)]
        # kick in kwarten; roffel versnelt: kwarten -> achtsten -> 16en -> 32en
        P['tdrums'] += [[s + i * TPB, s + i * TPB + E8, TKICK, 100 + 4 * k] for i in range(3 if last else 4)]
        if k < 3:
            step = (TPB, E8, S16)[k]
            P['tdrums'] += [[s + i * step, s + i * step + step // 2 + 4, TSNARE, 56 + 10 * k + i * (12 // (BAR // step) + 1)]
                            for i in range(BAR // step)]
        else:
            P['tdrums'] += [[s + i * S16, s + i * S16 + 10, TSNARE, 78 + i] for i in range(8)]
            P['tdrums'] += [[s + 2 * TPB + i * 12, s + 2 * TPB + i * 12 + 8, TSNARE, 88 + i * 2] for i in range(8)]
        if k >= 2:                                                      # stijgende strijkers (zoals de intro)
            rise = ['F#4', 'G4', 'A4', 'B4', 'C#5', 'D5', 'E5', 'F#5', 'G5', 'A5', 'B5', 'C#6', 'D6', 'E6']
            P['strmel'] += [[s + i * E8, s + i * E8 + E8, p(n), 66 + i * 2] for i, n in enumerate(rise[(k - 2) * 8:(k - 2) * 8 + 8])
                            if not (last and i >= 6)]
            P['choir'] += [[s, end - 8, tones(name, 66, 78)[0], 70 + 6 * (k - 2)]]
        # PSG-riser (ruis), vier maten lang omhoog, ook door de stille tel heen
        P['shaker'] += [[s + i * TPB, s + i * TPB + TPB, 48 + 2 * (4 * k + i), 50 + 4 * (4 * k + i)] for i in range(4)]
        return
    if sec == 'BREAK':
        P['tsaw'] += [[s, end - 8, n, 84] for n in pad]
        P['tlead'] += mel(BREAK_MEL[k], s, 100)
        P['mbox'] += mel(BREAK_MEL[k], s, 92, 12)
        P['choir'] += [[s, end - 8, tones(name, 66, 78)[0], 80]]
        if k == 0:
            P['perc'] += [[s, s + 2 * TPB, CRASH, 90]]
            P['tbass'] += [[s, s + TPB, r, 100]]
        if k == 3:                                                      # mini-opbouw naar drop 2
            P['tdrums'] += [[s + i * TPB, s + i * TPB + E8, TKICK, 100 + 6 * i] for i in range(3)]
            P['tdrums'] += [[s + i * S16, s + i * S16 + 10, TSNARE, 70 + 3 * i] for i in range(12)]
            P['shaker'] += [[s + i * TPB, s + i * TPB + TPB, 60 + 4 * i, 70 + 10 * i] for i in range(4)]
        return
    # ---- drops ----
    big = sec == 'DROP2'
    fill = big and k == 7                                               # laatste maat: ritardando + fill naar E
    m = DROP_END if fill else THEME[k % 4]
    P['tlead'] += mel(m, s, 112 if big else 104)
    if big:
        P['glock'] += mel(m, s, 88, 12)
    for hs, nm in halves:
        tn = tones(nm, 62, 76)[:3]
        rr = bass_note(nm)
        for i in range(4):                                              # gated supersaw-akkoorden (achtsten)
            if fill and hs + i * E8 >= s + 2 * TPB:
                break
            P['tsaw'] += [[hs + i * E8, hs + i * E8 + 22, n, 92] for n in tn]
        P['tbass'] += [[hs + i * TPB + E8, hs + i * TPB + E8 + 22, rr, 110] for i in range(2)]   # off-beat bas
        P['sub'] += [[hs + i * TPB + E8, hs + i * TPB + E8 + 26, rr, 100] for i in range(2)]
        top = tones(nm, 66, 78)
        ln = BAR if halves[0][1] == halves[1][1] else 2 * TPB
        if hs == s or halves[0][1] != halves[1][1]:
            P['choir'] += [[hs, hs + ln - 8, top[0], 84 if big else 76]]
            if big:
                P['choir'] += [[hs, hs + ln - 8, top[1], 72]]
    # pluck-arpeggio in 16en (de tweede helft een octaaf hoger), met een delay-echo op het PSG-vierkant
    tn = tones(name, 74, 93)
    P['tpluck'] += [[s + i * S16, s + i * S16 + 8, tn[min((0, 1, 2, 1)[i % 4] + (3 if i % 8 >= 4 else 0), len(tn) - 1)], 74]
                    for i in range(8 if fill else 16)]
    # drums: four on the floor, clap op 2 en 4, crash elke 4 maten (drop 2: elke 2)
    P['tdrums'] += [[s + i * TPB, s + i * TPB + E8, TKICK, 127] for i in range(4)]
    P['tdrums'] += [[s + i * TPB, s + i * TPB + E8 + S16, CLAP, 100] for i in (1, 3)]
    if k % (2 if big else 4) == 0:
        P['perc'] += [[s, s + 2 * TPB, CRASH, 108 if k == 0 else 92]]
    # hihats op het PSG-ruiskanaal: open op de off-beat, dicht op de andere 16en
    for i in range(16):
        if i % 4 == 0:
            continue
        P['shaker'] += [[s + i * S16, s + i * S16 + (16 if i % 4 == 2 else 3), 84 if i % 4 == 2 else 92, 100 if i % 4 == 2 else 56]]
    if fill:                                                            # roffel + harpglissando (E-pentatonisch)
        P['tdrums'] += [[s + 2 * TPB + i * S16, s + 2 * TPB + i * S16 + 10, TSNARE, 80 + 4 * i] for i in range(8)]
        gliss(s + 3 * TPB, p('B4'), p('B6'), 8, 12, 104, tonic=4)


def build():
    P = {k: [] for k in PARTS}

    def gliss(start, lo, hi, n, step, vel, part='harp', tonic=2):
        ns = [x for x in range(lo, hi + 1) if (x - tonic) % 12 in (0, 2, 4, 7, 9)]   # pentatonisch (D: D E F# A B)
        idx = [round(i * (len(ns) - 1) / (n - 1)) for i in range(n)]
        P[part] += [[start + i * step, start + i * step + step, ns[j], vel - 12 + i * 3] for i, j in enumerate(idx)]

    def harp_arp(start, name, vel, sixteenths=False, ln=None):
        tn = tones(name, 50, 81)                    # D3..A5
        pat = [0, 2, 4, 5, 6, 5, 4, 2] if not sixteenths else [0, 1, 2, 3, 4, 5, 6, 7, 8, 7, 6, 5, 4, 3, 2, 1]
        step = S16 if sixteenths else E8
        for i, k in enumerate(pat[: (2 * TPB) // step]):
            n = tn[min(k, len(tn) - 1)]
            P['harp'].append([start + i * step, start + i * step + (ln or S16), n, vel])

    def pizz_off(start, name, vel):                 # naslagen op de achtsten 'en'
        tn = tones(name, 62, 76)                    # D4..E5
        for b in range(2):
            s = start + b * TPB + E8
            P['pizz'] += [[s, s + 12, n, vel] for n in tn[:2]]

    def bass_bounce(start, name, vel):
        r = bass_note(name)
        P['bass'] += [[start, start + 3 * S16 - 4, r, vel], [start + 4 * S16, start + 6 * S16 - 4, r + 7, vel - 10],
                      [start + 6 * S16, start + 8 * S16 - 4, r + 12, vel - 6]]

    def shaker(start, n16=16, loud=(2, 6, 10, 14)):
        P['shaker'] += [[start + i * S16, start + i * S16 + 6, 84, 80 if i in loud else 40] for i in range(n16)]

    # ===== opmaat = transitie =====
    P['strings'] += [[0, TPB * 4 - 8, n, 50] for n in (p('A3'), p('D4'))]       # het beeld dimt
    P['choir'] += [[0, TPB * 4 - 8, p('F#4'), 56]]
    P['perc'] += [[TPB, 3 * TPB, CHIMES, 112]]                                   # de ster verschijnt
    P['celesta'] += [[TPB + i * E8, TPB + i * E8 + E8, p(n), 96 - i * 6] for i, n in enumerate(('A6', 'F#6', 'E6', 'D6'))]
    gliss(3 * TPB, p('D4'), p('D6'), 7, 12, 96)                                 # de ster duikt terug
    P['perc'] += [[3 * TPB, 4 * TPB, CHIMES, 80]]
    P['celesta'] += [[3 * TPB + 72, 4 * TPB, p('A6'), 84]]                       # de glinstering (SE_SHINY)
    # ===== maat 1: de wens =====
    s = t(1)
    P['perc'] += [[s, s + 2 * TPB, CRASH, 92], [s, s + 2 * TPB, TRI, 100]]
    P['glock'] += [[s, s + 2 * TPB, p('D6'), 104]]
    P['timp'] += [[s, s + TPB, p('D3'), 110]]
    # maat 1-4: speeldoos met het wensmotief, zachte pad + koor, harp vanaf maat 2
    for b in range(1, 5):
        s, name = t(b), INTRO[b - 1]
        P['mbox'] += mel(THEME[b - 1], s, 112, 12)
        tn = tones(name, 62, 74)
        P['strings'] += [[s, s + BAR - 8, n, 56 + b * 6] for n in tn[:2]]
        P['choir'] += [[s, s + BAR - 8, tones(name, 66, 78)[0], 60 + b * 6]]
        if b >= 2:
            harp_arp(s, name, 64 + b * 4)
            harp_arp(s + 2 * TPB, name, 64 + b * 4)
            P['bass'] += [[s, s + BAR - 8, bass_note(name), 84]]
        if b >= 3:
            P['perc'] += [[s, s + TPB, TRI, 70]]
            P['timp'] += [[s, s + TPB, bass_note(name) + 12 if bass_note(name) < 45 else bass_note(name), 84]]
    # maat 5-6: opbouw
    for b in (5, 6):
        s, name = t(b), INTRO[b - 1]
        pizz_off(s, name, 80 + (b - 5) * 16)
        pizz_off(s + 2 * TPB, name, 86 + (b - 5) * 16)
        P['bass'] += [[s + i * E8, s + i * E8 + E8 - 6, bass_note(name), 92 + i * 3] for i in range(8)]
        P['drums'] += [[s + i * TPB, s + i * TPB + S16, KICK, 92 + (b - 5) * 16] for i in range(4)]
        P['timp'] += [[s + i * TPB, s + i * TPB + E8, bass_note(name) + 12 if bass_note(name) < 45 else bass_note(name),
                       84 + (b - 5) * 20 + i * 4] for i in (0, 2)]
        P['choir'] += [[s, s + BAR - 8, tones(name, 66, 78)[0], 84 + (b - 5) * 10]]
    rise = ['D4', 'E4', 'F#4', 'G4', 'A4', 'B4', 'C#5', 'D5', 'E5', 'F#5', 'G5', 'A5', 'B5', 'C#6', 'D6', 'E6']
    P['strmel'] += [[t(5) + i * E8, t(5) + i * E8 + E8, p(n), 80 + i * 2] for i, n in enumerate(rise)]
    P['drums'] += [[t(5) + i * E8, t(5) + i * E8 + S16, ROLL, 40 + i * 4] for i in range(8)]
    P['drums'] += [[t(6) + i * S16, t(6) + i * S16 + S16, ROLL, 60 + i * 3] for i in range(12)]
    shaker(t(6), 12)
    gliss(t(6) + 3 * TPB, p('A4'), p('A6'), 8, 12, 104)
    P['perc'] += [[t(6) + 3 * TPB, LOOP_START, CHIMES, 96]]

    # ===== de loop =====
    for lb in range(LOOP_LEN):
        s = lt(lb)
        halves = chords_at(LOOP, s, lb)
        main = halves[0][1]
        sec, k = section(lb)
        if sec in ('BUILD', 'DROP1', 'BREAK', 'DROP2'):
            trance(P, lb, s, sec, k, halves, gliss)
            continue
        # ---- melodie ----
        if sec == 'A':
            P['flute'] += mel(THEME[k], s, 116)
            P['glock'] += mel(THEME[k], s, 84, 12)
        elif sec == 'A2':
            m = THEME[k] if k < 4 else THEME2_END[k - 4]
            P['strmel'] += mel(m, s, 112)
            P['flute'] += mel(m, s, 100, 12 if k < 4 else 0)
        elif sec == 'B':
            P['horn'] += mel(HEROIC[k], s, 120)
            if k >= 4:
                P['flute'] += mel(HEROIC[k], s, 84, 12)                           # piccolo-verdubbeling
            # celesta-antwoorden op de lange noten (2e helft van de maat)
            tn = tones(halves[1][1], p('D6'), p('D7'))
            P['celesta'] += [[s + 2 * TPB + i * S16, s + 2 * TPB + i * S16 + S16, tn[min(i, len(tn) - 1) if k % 2 == 0
                              else max(len(tn) - 1 - i, 0)], 72 + i * 4] for i in range(4)]
        elif sec == 'D':
            m = THEME[k] if k < 4 else THEME2_END[k - 4]
            P['flute'] += mel(m, s, 108, 2 + (12 if k < 4 else 0))
            P['strmel'] += mel(m, s, 100, 2)
            P['glock'] += mel(m, s, 80, 14 if k < 4 else 2)
        else:
            P['horn'] += mel(RISE[k], s, 120)
            P['flute'] += mel(RISE[k], s, 104, 12)

        # ---- begeleiding ----
        for hs, name in halves:
            if sec in ('A', 'A2', 'D'):
                harp_arp(hs, name, 72)
                bass_bounce(hs, name, 104)
                if sec == 'A':
                    pizz_off(hs, name, 76)
            elif sec == 'B':
                r = bass_note(name)
                P['bass'] += [[hs + i * E8, hs + i * E8 + E8 - 8, r + (12 if i == 3 else 0), 104] for i in range(4)]
                tn = tones(name, 62, 76)
                P['strings'] += [[hs + i * E8, hs + i * E8 + 14, tn[(0, 1, 2, 1)[i]], 92] for i in range(4)]   # spiccato
            else:  # E
                r = bass_note(name)
                P['bass'] += [[hs + i * TPB, hs + i * TPB + TPB - 10, r + (0, 7)[i], 108] for i in range(2)]
                tn = tones(name, 62, 79)
                P['pizz'] += [[hs + i * E8, hs + i * E8 + 12, tn[i % len(tn)], 84] for i in range(4)]
        # pads: koor (1 stem; 2 in C) en hoorn-tegenstem in D
        if sec in ('A', 'A2', 'D', 'E'):
            for hs, name in halves:
                if hs != s and halves[0][1] == halves[1][1]:
                    continue
                ln = BAR if halves[0][1] == halves[1][1] else 2 * TPB
                top = tones(name, 66, 78)
                P['choir'] += [[hs, hs + ln - 8, top[0], 72]]
                if sec == 'D':
                    P['horn'] += [[hs, hs + ln - 8, tones(name, 57, 67)[-1], 92]]
        # timpani
        if sec in ('B', 'D') or (sec == 'E' and k == 3):
            r = bass_note(main)
            P['timp'] += [[s, s + TPB, r + 12 if r < 45 else r, 108]]
            if sec == 'B' and k % 2 == 1:
                P['timp'] += [[s + 3 * TPB + E8, s + 4 * TPB, r + 12 if r < 45 else r, 96]]

        # ---- drums ----
        if sec in ('A', 'A2', 'D'):
            P['drums'] += [[s + x, s + x + S16, KICK, 116] for x in (0, 3 * E8, 2 * TPB)]
            P['drums'] += [[s + x, s + x + E8, SNARE, 96] for x in (TPB, 3 * TPB)]
            shaker(s)
            if k in (0, 4) or (sec == 'D' and k % 2 == 0):
                P['perc'] += [[s, s + 2 * TPB, CRASH, 104 if k == 0 else 88]]
            elif k % 2 == 0:
                P['perc'] += [[s, s + TPB, TRI, 84]]
            if sec != 'A':
                P['perc'] += [[s + i * TPB + E8, s + i * TPB + E8 + S16, JINGLE, 70] for i in range(4)]
        elif sec == 'B':
            P['drums'] += [[s + x, s + x + S16, KICK, 118] for x in (0, 3 * E8, 2 * TPB, 2 * TPB + 3 * S16)]
            P['drums'] += [[s + x, s + x + E8, SNARE, 100] for x in (TPB, 3 * TPB)]
            P['drums'] += [[s + 3 * TPB - S16, s + 3 * TPB, ROLL, 60]]
            shaker(s, loud=(0, 4, 8, 12))
            if k in (0, 4):
                P['perc'] += [[s, s + 2 * TPB, CRASH, 100]]
        else:  # E: four on the floor, roffel naar de loop
            P['drums'] += [[s + i * TPB, s + i * TPB + S16, KICK, 118] for i in range(4)]
            shaker(s, loud=(0, 4, 8, 12))
            if k < 3:
                P['drums'] += [[s + x, s + x + E8, SNARE, 98] for x in (TPB, 3 * TPB)]
            if k == 0:
                P['perc'] += [[s, s + 2 * TPB, CRASH, 104]]
            if k == 3:                                                            # = maat 6 van de intro
                P['drums'] += [[s + i * S16, s + i * S16 + S16, ROLL, 60 + i * 3] for i in range(12)]
                gliss(s + 3 * TPB, p('A4'), p('A6'), 8, 12, 104)
                P['perc'] += [[s + 3 * TPB, LOOP_END, CHIMES, 96]]

    # PSG: zachte fonkel-echo van de harp (vierkant), 3 16en later, alleen in A/A'/D
    P['spark'] = [[a + 3 * S16, b + 3 * S16, n + 12, 50] for a, b, n, v in P['harp']
                  if lt(A0) <= a < lt(B0) or lt(D0) <= a < lt(E0)]
    # en in de drops: delay-echo van de pluck (3 16en later)
    P['spark'] += [[a + 3 * S16, b + 3 * S16, n, 40] for a, b, n, v in P['tpluck'] if lt(DROP1) <= a < lt(D0) - 3 * S16
                   and not lt(BREAK0) - 3 * S16 <= a < lt(DROP2)]

    # niets over de loopgrenzen laten lopen
    for k in P:
        out = []
        for a, b, n, v in P[k]:
            for g in (LOOP_START, LOOP_END):
                if a < g < b:
                    b = g
            if a < LOOP_END:
                out.append([a, b, n, v])
        P[k] = dedupe(out)

    write_voicegroup()
    rel = releases(VG)
    progs = {'flute': FLUTE, 'glock': GLOCK, 'strmel': STR, 'horn': HORN, 'mbox': MBOX, 'celesta': CELESTA,
             'harp': HARP, 'pizz': PIZZ, 'strings': STR, 'choir': CHOIR, 'bass': BASS, 'timp': TIMP}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) for k, pr in progs.items()}
    # trance-partijen: uitklinktijd bij het hoogste tempo (meer ticks per frame = veilige kant)
    tprogs = {'tlead': SAW_LEAD, 'tsaw': SAW_BRIGHT, 'tbass': SAW_BASS, 'tpluck': SAW_PLUCK}
    tail.update({k: release_ticks(rel.get(pr, 200), TPB, BPM_TR) for k, pr in tprogs.items()})
    tail['drums'] = tail['perc'] = tail['tdrums'] = 0
    for k in ('flute', 'strmel', 'horn', 'choir', 'bass', 'tlead'):
        P[k] = detach(P[k], tail[k])
    # lange koornoten in stukken van 2 tellen (zacht pulserend), zodat een vol moment er maar één stukje kost
    P['choir'] = [[a, min(b, a + 2 * TPB - tail['choir']), n, v] for a0, b, n, v in P['choir']
                  for a in range(a0, b, 2 * TPB) if b - a > tail['choir'] + 12]
    # drumnoten: de lint telt de nootlengte (max. 2 tellen)
    for k in ('drums', 'perc', 'tdrums'):
        P[k] = [[a, min(b, a + 2 * TPB), n, v] for a, b, n, v in P[k]]
    order = ['flute', 'tlead', 'horn', 'mbox', 'strmel', 'bass', 'drums', 'tdrums', 'tbass', 'glock', 'perc', 'harp',
             'timp', 'celesta', 'tsaw', 'tpluck', 'pizz', 'choir', 'strings']
    ds = {k: P[k] for k in order}
    kept = allocate(ds, order, tail, max_voices=MAX_VOICES)
    for k in order:
        n = len(ds[k])
        if n and len(kept[k]) < n:
            print('  %-8s %3d van %4d noten vallen weg (%.1f%%)' % (k, n - len(kept[k]), n, 100 * (n - len(kept[k])) / n))
        P[k] = kept[k]

    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    # opbouw: per tel sneller (152 -> 168, eerst langzaam, dan steeds harder); drop 2 maat 8: ritardando terug
    for i in range(16):
        song.tempo(lt(BUILD0) + i * TPB, (BPM + (BPM_TR - BPM) * ((i + 1) / 16) ** 1.6) / 120)
    for i, b in enumerate((164, 160, 157, 154)):
        song.tempo(lt(D0 - 1) + 2 * TPB + i * E8, b / 120)
    song.tempo(lt(D0), BPM / 120)
    song.loop = (LOOP_START, LOOP_END)
    # sporen die in de climax een ander instrument/volume krijgen: (tick, 'prog'/7, waarde), terug bij sectie D
    tb, d = lt(BUILD0), lt(D0)
    ramp = [(tb + i * TPB, 7, 38 + 2 * i) for i in range(16)]                    # het 'filter' gaat open
    ccs = {
        'flute': [(tb, 'prog', SAW_LEAD), (tb, 7, 92), (d, 'prog', FLUTE), (d, 7, 108)],
        'celesta': [(tb, 'prog', SAW_PLUCK), (tb, 7, 66), (d, 'prog', CELESTA), (d, 7, 84)],
        'strings': [(tb, 'prog', SAW_DARK), (lt(BUILD0 + 1), 'prog', SAW_MID), (lt(BUILD0 + 3), 'prog', SAW_BRIGHT)]
                   + ramp + [(lt(DROP1), 7, 70), (lt(BREAK0), 7, 66), (lt(DROP2), 7, 74),
                             (d, 'prog', STR), (d, 7, 72)],
        'bass': [(tb, 'prog', SAW_BASS), (tb, 7, 100), (d, 'prog', BASS), (d, 7, 112)],
        'shaker': [(tb, 'prog', RISER), (tb, 7, 28), (lt(DROP1), 'prog', HATS), (lt(DROP1), 7, 34),
                   (lt(BREAK0), 'prog', RISER), (lt(BREAK0), 7, 28), (lt(DROP2), 'prog', HATS), (lt(DROP2), 7, 34),
                   (d, 'prog', SHAKER), (d, 7, 30)],
    }
    # trance-partijen op de sporen van instrumenten die dan zwijgen
    P['flute'] = sorted(P['flute'] + P['tlead'])
    P['celesta'] = sorted(P['celesta'] + P['tpluck'])
    P['strings'] = sorted(P['strings'] + P['tsaw'])
    P['bass'] = sorted(P['bass'] + P['tbass'])
    layout = [('flute', FLUTE, 108, 0, 64), ('glock', GLOCK, 72, 1, 80), ('strmel', STR, 100, 2, 56),
              ('horn', HORN, 104, 3, 52), ('mbox', MBOX, 110, 4, 72), ('celesta', CELESTA, 84, 5, 88),
              ('harp', HARP, 84, 6, 40), ('pizz', PIZZ, 76, 7, 76), ('strings', STR, 72, 8, 60),
              ('choir', CHOIR, 66, 10, 64), ('bass', BASS, 112, 11, 64), ('timp', TIMP, 96, 12, 64),
              ('spark', SPARK, 24, 13, 96), ('shaker', SHAKER, 30, 14, 70), ('sub', SUB, 56, 15, 64)]
    for k, prog, vol, ch, pan in layout:
        song.add(P[k], prog, vol, ch, pan, ccs=ccs.get(k, ()))
    song.add(sorted(P['drums'] + P['perc'] + P['tdrums']), DRUMS, 100, 9)
    written = {k for k, *_ in layout} | {'drums', 'perc', 'tdrums', 'tlead', 'tpluck', 'tsaw', 'tbass'}
    assert not [k for k in P if P[k] and k not in written], 'partij niet weggeschreven'
    song.save(OUT, LOOP_END)
    tm = sorted(song.tempo_map)

    def sec_at(tick):
        out, last, bpm = 0.0, 0, BPM
        for tk, f in tm:
            if tk >= tick:
                break
            out += (tk - last) / TPB * 60 / bpm
            last, bpm = tk, f * 120
        return out + (tick - last) / TPB * 60 / bpm
    print(OUT, '%d sporen, intro %.1f s, loop %.1f s' % (len(layout) + 1, sec_at(LOOP_START), sec_at(LOOP_END) - sec_at(LOOP_START)))
    for nm, st in SECTIONS:
        print('  %-6s loopmaat %2d  %5.1f s' % (nm, st, sec_at(lt(st))))
    print('  einde          %5.1f s' % sec_at(LOOP_END))


def write_voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm + celesta, speeldoos, windgong en een eigen drumkit voor Battle! Jirachi.'
    lines[1] = '@ Gegenereerd door tools/grounded/jirachi_theme.py.'
    lines[2] = 'voice_group %s' % VG
    rep = {
        '@ 8': '\tvoice_directsound 60, 0, DirectSoundWaveData_jirachi_celesta, 255, 248, 0, 180  @ 8',
        '@ 9': '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_glockenspiel, 255, 165, 51, 170  @ 9',
        '@ 10': '\tvoice_directsound 60, 0, DirectSoundWaveData_jirachi_music_box, 255, 248, 0, 190  @ 10',
        '@ 33': '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_fretless_bass, 255, 253, 0, 149  @ 33',
        '@ 39': '\tvoice_directsound 60, 0, DirectSoundWaveData_jirachi_sawbass, 255, 0, 255, 120  @ 39',
        '@ 84': '\tvoice_programmable_wave_alt 60, 0, ProgrammableWaveData_1, 0, 7, 15, 0  @ 84',
        '@ 88': '\tvoice_directsound 60, 0, DirectSoundWaveData_jirachi_supersaw_dark, 255, 0, 255, 110  @ 88',
        '@ 89': '\tvoice_directsound 60, 0, DirectSoundWaveData_jirachi_supersaw_mid, 255, 0, 255, 110  @ 89',
        '@ 90': '\tvoice_directsound 60, 0, DirectSoundWaveData_jirachi_supersaw_bright, 255, 0, 255, 110  @ 90',
        '@ 91': '\tvoice_directsound 60, 0, DirectSoundWaveData_jirachi_supersaw_lead, 255, 0, 255, 190  @ 91',
        '@ 92': '\tvoice_directsound 60, 0, DirectSoundWaveData_jirachi_supersaw_mid, 255, 224, 0, 110  @ 92',
        '@ 121': '\tvoice_noise_alt 60, 0, 0, 3, 0, 15, 2  @ 121',
        '@ 122': '\tvoice_noise_alt 60, 0, 0, 0, 0, 15, 1  @ 122',
        '@ 45': '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_pizzicato_strings, 255, 226, 0, 99  @ 45',
        '@ 46': '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_harp, 255, 242, 51, 170  @ 46',
        '@ 47': '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 190  @ 47',
        '@ 81': '\tvoice_square_2 60, 0, 3, 0, 1, 4, 1  @ 81',
        '@ 120': '\tvoice_noise_alt 60, 0, 0, 0, 1, 0, 0  @ 120',
        '@ 127': '\tvoice_keysplit_all voicegroup_jirachi_drumset  @ 127',
    }
    out = []
    for l in lines:
        tag = l.rstrip().rsplit('  ', 1)[-1] if '@' in l else None
        out.append(rep.get(tag, l))
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    kit = [
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 0',          # 36 kick
        'voice_directsound 72, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 100',              # 37 roffel
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 160',        # 38 snare
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165',     # 39 crash
        'voice_directsound_no_resample 64, 80, DirectSoundWaveData_sd90_open_triangle, 255, 242, 103, 188',     # 40 triangel
        'voice_directsound 96, 50, DirectSoundWaveData_jirachi_chimes, 255, 252, 0, 200',                       # 41 windgong
        'voice_directsound_no_resample 64, 84, DirectSoundWaveData_sc88pro_jingle_bell, 255, 0, 255, 120',      # 42 belletjes
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_jirachi_kick, 255, 0, 255, 0',               # 43 trancekick
        'voice_directsound_no_resample 60, 60, DirectSoundWaveData_sc88pro_tr909_hand_clap, 255, 0, 255, 0',    # 44 clap
        'voice_directsound_no_resample 60, 68, DirectSoundWaveData_unknown_synth_snare, 255, 0, 255, 60',       # 45 roffelsnare
    ]
    open('sound/voicegroups/drumsets/jirachi.inc', 'w').write(
        '@ Project Grounded: drumkit voor Battle! Jirachi (jirachi_theme.py), alles DirectSound: 36 kick, 37 roffel,\n'
        '@ 38 snare, 39 crash, 40 triangel, 41 windgong (jirachi_chimes), 42 belletjes, 43 trancekick (jirachi_kick),\n'
        '@ 44 clap (909), 45 snare voor de roffel in de opbouw.\n'
        'voice_group jirachi_drumset, 36\n' + ''.join('\t%s\n' % k for k in kit) + '\n')


if __name__ == '__main__':
    build()
