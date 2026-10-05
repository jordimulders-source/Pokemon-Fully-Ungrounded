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
Loop (52 maten, ±81 s). v3: de reguliere delen weer precies als v1 (geen versnelling), en in plaats van v1's
half-time-deel C een trance-tussenstuk (Jordi: "een tussenstuk waar de 'wahhhh'-vocalen veel langer uitgerekt
worden met een hoge bpm eronder, daarna switch je weer terug naar het reguliere stuk"):
  A  (0-7)   thema op fluit + glockenspiel, pizzicato, harp-arpeggio's, huppelende bas
  A' (8-15)  thema op strijkers + fluit een octaaf hoger, hogere afsluiting
  B  (16-23) avontuur: hoorn met een heldhaftig tegenthema, spiccato-strijkers, celesta-antwoorden, pauken;
             maat 22-23 = de overgang erin (v4: G-A, opwaarts): PSG-riser, PSG-lead-arpeggio + loopje omhoog,
             vocal-opmaat A-C#-E-A, roffel op tel 3-4 van maat 23
  v4 (Jordi: v3 'te donker, mysterieus, spookachtig' -> euforische, uplifting trance): het tussenstuk in D-groot,
             D-A-Bm-G (I-V-vi-IV) en G-A-F#m-Bm (IV-V-iii-vi), slot Asus4-A -> E-groot; de vocals als korte stoten
             (3+3+2) in stijgende akkoordtonen met een terts eronder, in fase 2 gated achtsten; PSG-blokgolf-arpeggio's
             in 16en omhoog (glinster omlaag op elke 4e maat) + delay-echo op vierkant 1; roffels in maat 7, 14, 15.
             Onderstaande beschrijving van I is die van v3.
  I  (24-39, 48,9 s) het tussenstuk, abrupt naar 164 bpm (Bm-G-D-A, vocal trance): de 'aaah'-vocal (jirachi_vox)
             zingt het wensmotief in augmentatie (A4 -> G5 -> F#5 -> E5 over 8 maten, noten van 2-6 maten, glijtonen
             via pitch bend, vibrato dat langzaam opkomt, aanzwellen via CC7) boven four-on-the-floor, off-beat
             zaagtandbas, PSG-hihats en een 'sidechain'-pompende supersaw-pad (tweede vocallaag een octaaf lager);
             vanaf maat 32 een eigen tweede vocalstem,
             gated supersaw in achtsten en pluck-arpeggio's; maat 39 (B7): beat valt weg, roffel, de vocals glijden
             naar E-groot (A5 -> G#5, D#5 -> E5)
  D  (40-47, 73,0 s) switch terug naar 152 bpm: het thema in E-groot een octaaf hoger (fluit + strijkers + glockenspiel)
  E  (48-51) C-D-G-A: het wensmotief stijgt in sequens, roffel + harpglissando terug naar A
Voicegroup grounded_jirachi = grounded_gm + eigen samples (gm_samples.py: jirachi_celesta, jirachi_music_box,
jirachi_chimes; jirachi_samples.py: supersaws, sawbas, trancekick, vox) + eigen drumkit (drumsets/jirachi.inc, alles DirectSound). Zie tools/grounded/MUZIEK.md.
Gebruik: python3 tools/grounded/jirachi_theme.py"""
import os, sys
import mido
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
VOX = 85                           # v3: de 'aaah'-vocal (jirachi_vox)
LEAD, ECHO = 82, 80                # v4: PSG-blokgolf-lead (vierkant 2) en zijn delay-echo (vierkant 1)
SUB, RISER, HATS = 84, 121, 122    # PSG: golf (sub), ruis (riser, open/dichte hihats)
BPM_TR = 164                       # tempo van het tussenstuk
TKICK, CLAP, TSNARE = 43, 44, 45
# eigen drumkit (drumsets/jirachi.inc, vanaf noot 36)
KICK, ROLL, SNARE, CRASH, TRI, CHIMES, JINGLE = 36, 37, 38, 39, 40, 41, 42

INTRO_BARS = 6                      # maat 1-6
LOOP_BAR = INTRO_BARS + 1           # songmaat 7 = loopmaat 0
LOOP_LEN = 52
A0, A1, B0, I0, D0, E0 = 0, 8, 16, 24, 40, 48
SECTIONS = [('A', A0), ('A2', A1), ('B', B0), ('I', I0), ('D', D0), ('E', E0)]


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

QUAL = {'': (0, 4, 7), 'm': (0, 3, 7), '7': (0, 4, 7, 10), 'm7': (0, 3, 7, 10), 'sus4': (0, 5, 7)}


def chord(name):
    root = name[:2] if len(name) > 1 and name[1] in '#b' else name[:1]
    return N[root], QUAL[name[len(root):]]


# akkoorden per maat (één of twee per maat)
INTRO = ['D', 'Bm', 'G', 'A', 'G', 'A']
LOOP = (['D', 'Bm', 'G', 'A', 'D', 'B7', ('Em', 'Gm'), ('D', 'A')] +                    # A
        ['D', 'Bm', 'G', 'A', 'D', 'G', ('Em7', 'A7'), 'D'] +                          # A'
        ['Bm', 'G', 'D', 'A', 'Bm', 'G', 'G', 'A'] +                                   # B (= v1; v4: maat 22-23 IV-V omhoog)
        ['D', 'A', 'Bm', 'G', 'D', 'A', 'Bm', 'G'] +                                   # tussenstuk, 164 bpm: I-V-vi-IV
        ['G', 'A', 'F#m', 'Bm', 'G', 'A', 'Bm', ('Asus4', 'A')] +                      # IV-V-iii-vi, A -> E-groot
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
    [(0, 4, 'B4'), (4, 4, 'D5'), (8, 8, 'G5')],                                     # G  (v4: de overgang, opwaarts)
    [(0, 6, 'E5'), (6, 2, 'F#5'), (8, 4, 'G5'), (12, 4, 'A5')],                     # A
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

PARTS = ('flute', 'glock', 'strmel', 'horn', 'mbox', 'celesta', 'harp', 'pizz', 'strings', 'choir', 'bass', 'timp',
         'drums', 'perc', 'spark', 'shaker',
         'vox', 'vox2', 'tsaw', 'tbass', 'tpluck', 'tdrums', 'sub', 'lead', 'echo')


# --- v4: het trance-tussenstuk (loopmaat 24-39), euforisch in D-groot --------------------------------------------------
# Jordi over v3: 'te donker, mysterieus, spookachtig; ik wil euforische, uplifting trance'. Dus: I-V-vi-IV (D-A-Bm-G),
# daarna IV-V-iii-vi (G-A-F#m-Bm), geen mineur-dominant of chromatiek; de 'aah'-vocals als korte stoten op de tellen in
# stijgende akkoordtonen (tweede stem een diatonische terts lager), in fase 2 gated in achtsten; heldere PSG-blokgolf-
# arpeggio's in 16en die omhoog dansen (met een dalende glinster aan het eind van elke 4 maten) + een PSG-delay-echo.
DMAJ = [0, 2, 4, 6, 7, 9, 11]                       # D-groot (toonklassen t.o.v. C)
STAB = [(0, 1.25), (1.5, 1.25), (3, 0.75)]          # trance-stootritme 3+3+2 achtsten (in tellen)


def third_below(n):
    """de diatonische terts onder n in D-groot."""
    sc = [x for x in range(n - 6, n) if (x % 12) in DMAJ]
    return sc[-2]


def vox_bar(k, chords):
    """(begin in tellen, lengte, lead, tweede stem) voor maat k van het tussenstuk."""
    name = chords[0][1]
    out = []
    if k == 15:                                     # Asus4 -> A: stoot, dan stijgende achtsten naar E-groot
        for st, ln, a, b in ((0, 1.25, 'D6', 'A5'), (1.5, 0.5, 'C#6', 'A5'), (2, 0.4, 'A5', 'E5'),
                             (2.5, 0.4, 'B5', 'E5'), (3, 0.4, 'C#6', 'A5'), (3.5, 0.45, 'E6', 'B5')):
            out.append((st, ln, p(a), p(b)))
        return out
    if k < 8:
        tn = tones(name, 69, 88) if k < 4 else tones(name, 74, 93)      # tweede helft een octaaf hoger
        for i, (st, ln) in enumerate(STAB):
            out.append((st, ln, tn[i], third_below(tn[i])))
    else:                                           # fase 2: gated achtsten die per halve maat omhoog lopen
        for i in range(8):
            nm = chords[0 if i < 4 else 1][1]
            tn = tones(nm, 74, 93)
            n = tn[min((0, 1, 2, 3, 1, 2, 3, 4)[i], len(tn) - 1)]
            out.append((i * 0.5, 0.25, n, third_below(n)))
    return out


def vocals(P, cc):
    """Korte 'aah'-stoten (geen glijtonen meer), volume per fase via CC7 (opbouw)."""
    for k in range(16):
        s = lt(I0 + k)
        ch = chords_at(LOOP, s, I0 + k)
        for st, ln, a, b in vox_bar(k, ch):
            x, y = s + int(st * TPB), s + int((st + ln) * TPB)
            P['vox'].append([x, y, a, 118 if st == 0 else 108])
            P['vox2'].append([x, y, b, 104 if st == 0 else 96])
        v = 96 if k < 4 else 108 if k < 8 else 118
        if k in (0, 4, 8):
            cc['vox'].append((s, 7, v))
            cc['vox2'].append((s, 7, v - 8))
    # opmaat in maat 23 (de overgang): stijgende stoten A4 C#5 E5 A5 op tel 3-4
    s = lt(I0 - 1)
    P['vox'] += [[s + 2 * TPB + i * E8, s + 2 * TPB + i * E8 + 40, p(n), 100 + 6 * i]
                 for i, n in enumerate(('A4', 'C#5', 'E5', 'A5'))]
    cc['vox'].append((s, 7, 96))


def lead_bar(P, s, k, chords):
    """PSG-blokgolf: arpeggio's die omhoog dansen (vallende ster omgekeerd), dalende glinster op elke 4e maat."""
    if k == 15:                                     # loopje omhoog naar E-groot (geen G/G#)
        run = ['E4', 'F#4', 'A4', 'B4', 'C#5', 'D5', 'E5', 'F#5', 'A5', 'B5', 'C#6', 'D6', 'E6', 'F#6', 'A6', 'B6']
        P['lead'] += [[s + i * S16, s + i * S16 + S16 - 2, p(n), 80 + 2 * i] for i, n in enumerate(run)]
        return
    step = E8 if k < 4 else S16
    for i in range(BAR // step):
        tk = s + i * step
        nm = chords[0 if tk < chords[1][0] else 1][1]
        tn = tones(nm, 67 if k < 8 else 62, 93)
        if k % 4 == 3 and tk >= s + 3 * TPB:        # glinster: dalend vanaf de top
            j = len(tn) - 1 - (i - 3 * TPB // step)
        elif step == E8:
            j = i
        else:
            j = (i % 8) + (0 if i < 8 else 2 if k < 8 else 3)
        P['lead'].append([tk, tk + step - 3, tn[max(0, min(j, len(tn) - 1))], 92 if k >= 8 else 84])


def interlude(P, s, k, chords, gliss):
    """Eén maat van het tussenstuk (k = 0..15, 164 bpm): four-on-the-floor, clap op 2 en 4 (vanaf maat 4), open hihat
    op de off-beat, off-beat zaagtandbas + PSG-sub, heldere supersaw (fase 1 aangehouden en gepompt, fase 2 gated
    in achtsten), pluck-arpeggio's, PSG-lead-arpeggio's; roffels in maat 7, 14 en 15."""
    name = chords[0][1]
    r = bass_note(name)
    big, last = k >= 8, k == 15
    nb = 2 if last else 4                                               # maat 39: de beat valt op tel 3 weg
    P['tdrums'] += [[s + i * TPB, s + i * TPB + E8, TKICK, 98 if big else 92] for i in range(nb)]
    if k >= 4:
        P['tdrums'] += [[s + i * TPB, s + i * TPB + E8 + S16, CLAP, 94 if big else 84] for i in (1, 3) if i < nb]
    if k in (0, 8):
        P['perc'] += [[s, s + 2 * TPB, CRASH, 110]]
    elif k in (4, 12):
        P['perc'] += [[s, s + 2 * TPB, CRASH, 88]]
    if k == 7:                                                          # roffel naar fase 2
        P['tdrums'] += [[s + 2 * TPB + i * S16, s + 2 * TPB + i * S16 + 10, TSNARE, 66 + 4 * i] for i in range(8)]
    if k == 14:                                                         # opbouw: snare in achtsten, aanzwellend
        P['tdrums'] += [[s + i * E8, s + i * E8 + 10, TSNARE, 60 + 3 * i] for i in range(8)]
    if last:                                                            # 16en, dan 32en + harpglissando naar E
        P['tdrums'] += [[s + i * S16, s + i * S16 + 10, TSNARE, 76 + 2 * i] for i in range(8)]
        P['tdrums'] += [[s + 2 * TPB + i * 12, s + 2 * TPB + i * 12 + 8, TSNARE, 92 + 2 * i] for i in range(16)]
        gliss(s + 3 * TPB, p('B4'), p('B6'), 8, 12, 104, tonic=4)
    for i in range(4 * nb):                                             # hihats: open op de off-beat, dicht op de rest
        if i % 4:
            P['shaker'] += [[s + i * S16, s + i * S16 + (16 if i % 4 == 2 else 3), 84 if i % 4 == 2 else 92,
                             100 if i % 4 == 2 else 56]]
    P['tbass'] += [[s + i * TPB + E8, s + i * TPB + E8 + 22, r, 96 if big else 90] for i in range(nb)]
    P['sub'] += [[s + i * TPB + E8, s + i * TPB + E8 + 26, r, 88] for i in range(nb)]
    if not big:                                                         # heldere ligging (F#4..A5), geen lage pad
        P['tsaw'] += [[s, s + BAR - 8, n, 58] for n in tones(name, 66, 81)[:3]]
    else:
        for i in range(2 * nb):
            nm = chords[0 if i < 4 else 1][1]
            P['tsaw'] += [[s + i * E8, s + i * E8 + 22, n, 70] for n in tones(nm, 66, 81)[:3]]
        if last:                                                        # A-groot aangehouden onder de stijgende stoten
            P['tsaw'] += [[s + 2 * TPB, s + BAR - 8, n, 72] for n in tones('A', 66, 81)[:3]]
    if k >= 4:                                                          # pluck in 16en (fase 2 een octaaf breder)
        tn = tones(name, 74, 93)
        pat = (0, 1, 2, 1) if not big else (0, 1, 2, 3)
        P['tpluck'] += [[s + i * S16, s + i * S16 + 8, tn[min(pat[i % 4] + (3 if big and i % 8 >= 4 else 0), len(tn) - 1)],
                         66 if big else 54] for i in range(4 * nb)]
    lead_bar(P, s, k, chords)


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
        if sec == 'I':
            interlude(P, s, k, halves, gliss)
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
            P['celesta'] += [[s + 2 * TPB + i * S16, s + 2 * TPB + i * S16 + S16, tn[min(i, len(tn) - 1) if k % 2 == 0 or k == 7
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
            if k < 6:
                shaker(s, loud=(0, 4, 8, 12))
            else:                                                                 # de overgang erin: PSG-riser
                P['shaker'] += [[s + i * TPB, s + i * TPB + TPB, 50 + 3 * (4 * (k - 6) + i), 54 + 6 * (4 * (k - 6) + i)]
                                for i in range(4)]
            if k == 7:                                                            # roffel naar het tussenstuk
                P['tdrums'] += [[s + 2 * TPB + i * S16, s + 2 * TPB + i * S16 + 10, TSNARE, 64 + 4 * i] for i in range(8)]
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
    # v4, de overgang (maat 22-23): PSG-lead-arpeggio omhoog (G in achtsten, dan een loopje in 16en op A)
    s = lt(B0 + 6)
    P['lead'] += [[s + i * E8, s + i * E8 + E8 - 3, n, 72 + 2 * i] for i, n in enumerate(tones('G', 67, 93)[:8])]
    run = ['E4', 'F#4', 'A4', 'B4', 'C#5', 'D5', 'E5', 'F#5', 'A5', 'B5', 'C#6', 'D6', 'E6', 'F#6', 'A6', 'C#7']
    P['lead'] += [[s + BAR + i * S16, s + BAR + i * S16 + S16 - 2, p(n), 76 + 2 * i] for i, n in enumerate(run)]
    # de lead op het vierkant van de fonkel-echo (dat zwijgt in B en het tussenstuk); delay-echo (3 16en later,
    # zachter) op vierkant 1 via het speeldoosspoor (de speeldoos speelt alleen in de intro)
    P['echo'] = [[a + 3 * S16, b + 3 * S16, n, 70] for a, b, n, v in P['lead'] if lt(I0 + 4) <= a < lt(D0) - 3 * S16]
    P['spark'] += P['lead']
    P['mbox'] += P['echo']
    vcc = {'vox': [], 'vox2': []}
    vocals(P, vcc)

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
    tprogs = {'vox': VOX, 'vox2': VOX, 'tsaw': SAW_BRIGHT, 'tbass': SAW_BASS, 'tpluck': SAW_PLUCK}
    tail.update({k: release_ticks(rel.get(pr, 200), TPB, BPM_TR) for k, pr in tprogs.items()})
    tail['drums'] = tail['perc'] = tail['tdrums'] = 0
    for k in ('flute', 'strmel', 'horn', 'choir', 'bass', 'vox', 'vox2', 'tbass'):
        P[k] = detach(P[k], tail[k])
    # lange koornoten in stukken van 2 tellen (zacht pulserend), zodat een vol moment er maar één stukje kost
    P['choir'] = [[a, min(b, a + 2 * TPB - tail['choir']), n, v] for a0, b, n, v in P['choir']
                  for a in range(a0, b, 2 * TPB) if b - a > tail['choir'] + 12]
    # drumnoten: de lint telt de nootlengte (max. 2 tellen)
    for k in ('drums', 'perc', 'tdrums'):
        P[k] = [[a, min(b, a + 2 * TPB), n, v] for a, b, n, v in P[k]]
    order = ['vox', 'vox2', 'flute', 'horn', 'mbox', 'strmel', 'bass', 'drums', 'tdrums', 'tbass', 'glock', 'perc', 'harp',
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
    # het tussenstuk: abrupt naar 164 bpm, en bij D abrupt terug (geen versnelling van de reguliere delen)
    song.tempo(lt(I0), BPM_TR / 120)
    song.tempo(lt(D0), BPM / 120)
    song.loop = (LOOP_START, LOOP_END)
    # sporen die in het tussenstuk een ander instrument/volume krijgen: (tick, 'prog'/7, waarde), terug bij sectie D
    ti, d = lt(I0), lt(D0)
    pump = [(ti + i * TPB + o, 7, v) for i in range(32) for o, v in ((0, 26), (10, 38), (22, 50), (40, 58))]
    ccs = {
        'strmel': [(lt(I0 - 1), 'prog', VOX)] + vcc['vox'] + [(d, 'prog', STR), (d, 7, 100)],
        'horn': [(lt(I0), 'prog', VOX)] + vcc['vox2'] + [(d, 'prog', HORN), (d, 7, 104)],
        'celesta': [(ti, 'prog', SAW_PLUCK), (ti, 7, 66), (d, 'prog', CELESTA), (d, 7, 84)],
        'strings': [(ti, 'prog', SAW_MID)] + pump + [(lt(I0 + 8), 'prog', SAW_BRIGHT), (lt(I0 + 8), 7, 60),
                                                    (d, 'prog', STR), (d, 7, 72)],
        'bass': [(ti, 'prog', SAW_BASS), (ti, 7, 100), (d, 'prog', BASS), (d, 7, 112)],
        'spark': [(lt(B0 + 6), 'prog', LEAD), (lt(B0 + 6), 7, 70), (ti, 7, 76), (d, 'prog', SPARK), (d, 7, 24)],
        'mbox': [(ti, 'prog', ECHO), (ti, 7, 44), (d, 'prog', MBOX), (d, 7, 110)],
        'shaker': [(lt(B0 + 6), 'prog', RISER), (lt(B0 + 6), 7, 26), (ti, 'prog', HATS), (ti, 7, 34),
                   (d, 'prog', SHAKER), (d, 7, 30)],
    }
    # v4: korte vocal-stoten, geen glijtonen of vibrato meer (alleen zeker weten dat bend/MOD op 0 staan)
    extra = {tr: [(lt(I0 - 1), mido.Message('pitchwheel', pitch=0)), (lt(I0 - 1), mido.Message('control_change', control=1, value=0))]
             for tr in ('strmel', 'horn')}
    # trance-partijen op de sporen van instrumenten die dan zwijgen
    P['strmel'] = sorted(P['strmel'] + P['vox'])
    P['horn'] = sorted(P['horn'] + P['vox2'])
    P['celesta'] = sorted(P['celesta'] + P['tpluck'])
    P['strings'] = sorted(P['strings'] + P['tsaw'])
    P['bass'] = sorted(P['bass'] + P['tbass'])
    layout = [('flute', FLUTE, 108, 0, 64), ('glock', GLOCK, 72, 1, 80), ('strmel', STR, 100, 2, 56),
              ('horn', HORN, 104, 3, 52), ('mbox', MBOX, 110, 4, 72), ('celesta', CELESTA, 84, 5, 88),
              ('harp', HARP, 84, 6, 40), ('pizz', PIZZ, 76, 7, 76), ('strings', STR, 72, 8, 60),
              ('choir', CHOIR, 66, 10, 64), ('bass', BASS, 112, 11, 64), ('timp', TIMP, 96, 12, 64),
              ('spark', SPARK, 24, 13, 96), ('shaker', SHAKER, 30, 14, 70), ('sub', SUB, 40, 15, 64)]
    for k, prog, vol, ch, pan in layout:
        song.add(P[k], prog, vol, ch, pan, extra=extra.get(k, ()), ccs=ccs.get(k, ()))
    song.add(sorted(P['drums'] + P['perc'] + P['tdrums']), DRUMS, 100, 9)
    written = {k for k, *_ in layout} | {'drums', 'perc', 'tdrums', 'vox', 'vox2', 'tpluck', 'tsaw', 'tbass', 'lead', 'echo'}
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
        '@ 85': '\tvoice_directsound 60, 0, DirectSoundWaveData_jirachi_vox, 255, 0, 255, 150  @ 85',
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
        '@ 82': '\tvoice_square_2 60, 0, 1, 0, 2, 10, 1  @ 82',          # v4: PSG-lead (25%, helder)
        '@ 80': '\tvoice_square_1 60, 0, 0, 1, 0, 2, 7, 1  @ 80',        # v4: delay-echo van de lead
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
