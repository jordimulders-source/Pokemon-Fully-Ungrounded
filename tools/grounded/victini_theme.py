#!/usr/bin/env python3
"""Project Grounded: Battle! Victini, een eigen compositie (Jordi: "een episch overwinnings anime stijl theme, dat de
good guy na episodes lang struggle aan het overwinnen is, dat je er adrenaline van krijgt").

Anime-climax-rock: koperfanfare met grote sprongen, spiccato-strijkers in zestienden, distortion-powerchords, drumfills;
een 'nog even struggle'-deel in B-mineur dat doorbreekt naar de climax een hele toon hoger (E-groot).
Victini = de overwinnings-Pokémon: het 'V-motief' daalt en springt weer omhoog, zoals een V (A5-F#5-D5-A4, D5-F#5-A5).

172 bpm, D-groot (climax E-groot). 1 tel = 20,8 frames, 1 maat = 1,40 s.
Intro (maat 0) = de transitie (B_TRANSITION_VICTINI, src/battle_transition.c). Zoals bij Jirachi gemeten begint een
route-transitie ±25 frames na de muziek. Transitieframe t -> muziekframe 25 + t:
  t = 0  (25)  vuur aan de onderrand          -> pauken- en snareroffel (tel 0-2 op 174 bpm)
  t = 6  (31)  de V vliegt omhoog              -> strijkers-rip omhoog (tel 1-2,5)
  t = 32 (57)  inslag, de V wit-heet          -> tel 3: koperstoot + crash + pauk (tel 2-4 op 224 bpm: 16 frames/tel)
  t = 48 (73)  alles vliegt in brand (explosie) -> maat 1 tel 0: tutti D-groot, de fanfare begint (vanaf hier 172 bpm)
  maat 1-2: V-fanfare (trompet + hoorn in octaven), maat 3: ademmaat op A (de cry van Victini, ±2,5 s na de transitie)
Loop (maat 4-45, 42 maten = 58,6 s):
  A  (4-11)   het heldenthema: trompet + hoorn in tertsen, powerchord-achtsten, spiccato-zestienden, rockbeat
  B  (12-19)  'royal road' (G-A-F#m-Bm): de strijkers zingen, de trompet antwoordt, snareopbouw
  A2 (20-27)  het thema met koor en PSG-glans; de laatste maat kantelt naar F#7
  C  (28-35)  de struggle in B-mineur: het thema in mineur laag in de hoorns, galopperende palm-mutes, half-time,
              pauken; opbouw G-A-B (bVI-bVII-I) en één tel stilte
  D  (36-43)  DOORBRAAK: het thema +2 (E-groot), four-on-the-floor, koor, crashes, bas in octaven
  T  (44-45)  C-D-koperstoten (bVI-bVII van E), dan maat 45 = maat 3 (A, opbouw) -> terug naar A in D (naadloos)
v2 (Jordi: euforischer/triomfantelijker): open heldenthema met octaafsprongen, hoorn in decimen, key change
E -> F midden in D (maat 3 = scharnier B -> C7), T = F-G-A-stoten; stijgende PSG-arpeggio's, buitelende bellen op de
PSG-golf, 32sten-risers, snare-roffels naar elke drop, octaafbas in achtsten.
Gebruikt tools/grounded/musiclib.py; voicegroup_grounded_victini = grounded_gm + eigen powerchords
(victini_samples.py), spiccato-strijkers en een eigen kit (drumsets/victini.inc, alles DirectSound).
Zie tools/grounded/MUZIEK.md. Gebruik: python3 tools/grounded/victini_theme.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

OUT = 'sound/songs/midi/mus_grounded_vs_victini.mid'
VG = 'grounded_victini'
TPB, BPM = 96, 172
S16 = TPB // 4
BAR = TPB * 4
MAXV = 11                                 # legendary: 11 DirectSound-noten
# programma's
TRUMPET, HORN, STRINGS, SPICC, POWER, MUTE, BASS, CHOIR, TIMPANI, KIT = 56, 60, 48, 49, 29, 28, 33, 52, 47, 127
SQ_LEAD, SQ_ARP, BELL, NOISE = 80, 81, 82, 121   # PSG (kost geen DirectSound-kanalen); 82 = golf-'bel'
# kit (drumsets/victini.inc)
KICK, SNARE, ROLL, CLAP, CRASH, BIGCRASH, HAT = 36, 37, 38, 39, 40, 41, 42
TOMS = (43, 44, 45, 46)                    # laag -> hoog
A0, B0, A2, C0, D0, T0, END = 4, 12, 20, 28, 36, 44, 46

N = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'Ab': 8,
     'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def p(name):
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


QUAL = {'': (0, 4, 7), 'm': (0, 3, 7), '7': (0, 4, 7, 10), 'sus': (0, 5, 7)}


def chord(name, shift=0):
    root = name[:2] if len(name) > 1 and name[1] in '#b' else name[:1]
    return (N[root] + shift) % 12, QUAL[name[len(root):]]


# akkoorden per maat: [(16e-stap, akkoord)]
PROG = {1: [(0, 'D')], 2: [(0, 'G'), (8, 'A')], 3: [(0, 'A')]}
THEME_CH = [[(0, 'D')], [(0, 'G')], [(0, 'Bm')], [(0, 'A')], [(0, 'D')], [(0, 'G')], [(0, 'Em'), (8, 'A')], [(0, 'D')]]
for i, c in enumerate(THEME_CH):
    PROG[A0 + i] = c
    PROG[A2 + i] = c
PROG[A2 + 7] = [(0, 'F#7')]
for i, c in enumerate(['G', 'A', 'F#m', 'Bm', 'G', 'A', 'Bm', 'A']):
    PROG[B0 + i] = [(0, c)]
for i, c in enumerate([[(0, 'Bm')], [(0, 'G')], [(0, 'Em')], [(0, 'F#')], [(0, 'Bm')], [(0, 'G')],
                       [(0, 'G'), (8, 'A')], [(0, 'Bsus'), (8, 'B')]]):
    PROG[C0 + i] = c
SHIFT = {}                                     # climax: hele toon hoger, halverwege nog een halve (key change)
for i, c in enumerate(THEME_CH):
    PROG[D0 + i] = c
    SHIFT[D0 + i] = 2 if i < 4 else 3
PROG[D0 + 3] = [(0, 'B'), (8, 'C7')]          # V van E -> V van F (de key change)
SHIFT[D0 + 3] = 0
PROG[T0] = [(0, 'G'), (8, 'A')]                # F -> G -> A: stijgende hele tonen terug naar A (V van D)
PROG[T0 + 1] = [(0, 'A')]


def chords_in(bar):
    """[(start16, eind16, (grondtoon-pc, intervallen))]"""
    cs = PROG[bar]
    out = []
    for k, (st, name) in enumerate(cs):
        en = cs[k + 1][0] if k + 1 < len(cs) else 16
        out.append((st, en, chord(name, SHIFT.get(bar, 0))))
    return out


def reg(pc, lo):
    """pc in het octaaf vanaf noot lo (lo .. lo+11)."""
    return lo + (pc - lo) % 12


# --- melodieën: [(16e-stap, lengte in 16en, noot)] per maat --------------------------------------------------------
FANFARE = [  # V-motief: daalt en springt weer omhoog
    [(0, 2, 'A5'), (2, 2, 'F#5'), (4, 2, 'D5'), (6, 2, 'A4'), (8, 2, 'D5'), (10, 2, 'F#5'), (12, 4, 'A5')],
    [(0, 4, 'B5'), (4, 2, 'A5'), (6, 2, 'G5'), (8, 7, 'A5')],
]
THEME = [   # v2: open, stijgende heldenintervallen (kwart + kwint = octaaf, octaafsprongen), top D6
    [(0, 2, 'A4'), (2, 2, 'D5'), (4, 8, 'A5'), (12, 2, 'B5'), (14, 2, 'C#6')],
    [(0, 6, 'D6'), (6, 2, 'B5'), (8, 2, 'G5'), (10, 2, 'A5'), (12, 4, 'B5')],
    [(0, 2, 'B4'), (2, 2, 'F#5'), (4, 6, 'B5'), (10, 2, 'A5'), (12, 2, 'F#5'), (14, 2, 'A5')],
    [(0, 4, 'C#6'), (4, 2, 'B5'), (6, 2, 'A5'), (8, 4, 'E5'), (12, 2, 'C#5'), (14, 2, 'A4')],
    [(0, 2, 'D5'), (2, 6, 'D6'), (8, 2, 'C#6'), (10, 2, 'B5'), (12, 4, 'A5')],
    [(0, 2, 'B4'), (2, 2, 'D5'), (4, 2, 'G5'), (6, 6, 'B5'), (12, 2, 'A5'), (14, 2, 'B5')],
    [(0, 2, 'E5'), (2, 2, 'G5'), (4, 4, 'B5'), (8, 2, 'A5'), (10, 2, 'B5'), (12, 4, 'C#6')],
    [(0, 12, 'D6')],
]
# D, maat 3: de key change (E -> F): eerste helft het thema in E, dan een dalende aanloop over C7 die op F5 oplost
KEYCHANGE_BAR = [(0, 4, 'D#6'), (4, 2, 'C#6'), (6, 2, 'B5'), (8, 2, 'C6'), (10, 2, 'A#5'), (12, 2, 'G5'), (14, 2, 'E5')]
THEME_TURN = [(0, 4, 'C#6'), (4, 4, 'A#5'), (8, 7, 'F#5')]          # A2 maat 8: kantelt naar F#7 (-> B-mineur)
THEME_TURN_HORN = [(0, 4, 'A#5'), (4, 4, 'F#5'), (8, 7, 'C#5')]
STR_MEL = [   # B: de strijkers zingen (royal road)
    [(0, 6, 'D5'), (6, 2, 'E5'), (8, 4, 'G5'), (12, 4, 'B5')],
    [(0, 6, 'A5'), (6, 2, 'G5'), (8, 8, 'E5')],
    [(0, 6, 'C#5'), (6, 2, 'D5'), (8, 4, 'F#5'), (12, 4, 'A5')],
    [(0, 6, 'F#5'), (6, 2, 'E5'), (8, 8, 'D5')],
    [(0, 6, 'D5'), (6, 2, 'E5'), (8, 4, 'G5'), (12, 4, 'D6')],
    [(0, 6, 'C#6'), (6, 2, 'B5'), (8, 4, 'A5'), (12, 4, 'E5')],
    [(0, 4, 'F#5'), (4, 4, 'B5'), (8, 4, 'D6'), (12, 4, 'C#6')],
    [(0, 8, 'A5')],
]
B_ANSWER = {1: [(10, 2, 'C#5'), (12, 2, 'E5'), (14, 2, 'A5')], 3: [(10, 2, 'B4'), (12, 2, 'D5'), (14, 2, 'F#5')],
            7: [(8, 4, 'E5'), (12, 2, 'C#5'), (14, 2, 'B4')]}
STRUGGLE_HORN = [   # het thema in mineur, laag en zwaar
    [(0, 4, 'B3'), (4, 2, 'F#4'), (6, 6, 'B4'), (12, 2, 'A4'), (14, 2, 'F#4')],
    [(0, 6, 'G4'), (6, 2, 'F#4'), (8, 2, 'E4'), (10, 2, 'D4'), (12, 4, 'E4')],
    [(0, 4, 'E4'), (4, 2, 'B3'), (6, 6, 'G4'), (12, 2, 'F#4'), (14, 2, 'E4')],
    [(0, 8, 'F#4'), (8, 4, 'A#4'), (12, 4, 'C#5')],
]
STRUGGLE_TP = [     # de trompet vecht terug (hoorn een terts eronder)
    [(0, 4, 'F#5'), (4, 2, 'B4'), (6, 6, 'B5'), (12, 2, 'A5'), (14, 2, 'F#5')],
    [(0, 6, 'G5'), (6, 2, 'F#5'), (8, 2, 'E5'), (10, 2, 'D5'), (12, 4, 'E5')],
    [(0, 4, 'D5'), (4, 4, 'B4'), (8, 4, 'E5'), (12, 4, 'C#5')],
    [(0, 2, 'F#4'), (2, 2, 'B4'), (4, 2, 'D#5'), (6, 2, 'F#5'), (8, 4, 'B5')],    # stopt op tel 4: stilte
]
STABS = [(0, 3), (3, 3), (6, 2)]                    # koperstoten 'V-ritme' (3+3+2)

SCALE_D = [2, 4, 6, 7, 9, 11, 1]


def third_below(n, scale=SCALE_D):
    pcs = [m for m in range(n - 12, n) if m % 12 in scale]
    if n % 12 not in scale:
        return n - 4
    return pcs[-2]


def mel(pattern, bar, vel, shift=0, gap=3):
    """lengte - gap ticks (articulatie)"""
    return [[bar * BAR + st * S16, bar * BAR + (st + ln) * S16 - gap, p(n) + shift, vel] for st, ln, n in pattern]


def build():
    parts = {k: [] for k in ('lead', 'horn', 'strmel', 'spicc', 'power', 'mute', 'bass', 'choir', 'timp', 'drums',
                             'sqlead', 'sqarp', 'bells', 'hats')}

    def drum(bar, step, note, vel, ln=1):
        t = bar * BAR + step * S16
        parts['drums'].append([t, t + ln * S16, note, vel])

    def hats(bar, steps, vel_on=72, vel_off=42):
        for i in steps:
            t = bar * BAR + i * S16
            parts['hats'].append([t, t + S16 // 2, 84, vel_on if i % 2 == 0 else vel_off])

    def tomfill(bar, start=12, vel=100):
        for k, i in enumerate(range(start, 16)):
            drum(bar, i, TOMS[::-1][min(k, 3)] if start >= 12 else TOMS[::-1][(k // 2) % 4], vel + k * 4)

    def spicc(bar, lo=50, steps=range(16), vel=86, pattern=(0, 7, 12, 7)):
        for st, en, (pc, iv) in chords_in(bar):
            r = reg(pc, lo)
            for i in steps:
                if st <= i < en:
                    t = bar * BAR + i * S16
                    parts['spicc'].append([t, t + S16 - 6, r + pattern[i % 4], vel + (10 if i % 4 == 0 else 0)])

    def power(bar, rhythm, vel=104, prog='power', ln=None):
        """rhythm: [(16e-stap, lengte in 16en)]"""
        for st, en, (pc, iv) in chords_in(bar):
            r = reg(pc, 40)
            for s, l in rhythm:
                if st <= s < en:
                    t = bar * BAR + s * S16
                    parts[prog].append([t, t + (ln or l * S16 - 8), r, vel + (8 if s % 4 == 0 else 0)])

    def bass(bar, steps=range(0, 16, 2), octave=False, vel=108):
        """octave: 'anime-opening'-octaafbas, elke achtste om en om grondtoon/octaaf (v2)."""
        for st, en, (pc, iv) in chords_in(bar):
            r = reg(pc, 28)
            for i in steps:
                if st <= i < en:
                    t = bar * BAR + i * S16
                    up = octave and i % 4 == 2
                    parts['bass'].append([t, t + 2 * S16 - 10, r + (12 if up else 0), vel - (6 if up else 0)])

    def choir(bar, vel=84):
        for st, en, (pc, iv) in chords_in(bar):
            top = reg((pc + iv[1]) % 12, 67)          # de terts, G4..F#5: stralend
            for h in range(st, en, 8):
                parts['choir'].append([bar * BAR + h * S16, bar * BAR + min(h + 8, en) * S16, top, vel])

    def arp(bar, vel=60, lo=62):
        """v2: snelle stijgende chiptune-arpeggio's: per halve maat 8 zestienden omhoog over twee octaven."""
        for st, en, (pc, iv) in chords_in(bar):
            r = reg(pc, lo)
            run = [r + o + x for o in (0, 12, 24) for x in (0, iv[1], iv[2])]
            for i in range(st, en):
                t = bar * BAR + i * S16
                parts['sqarp'].append([t, t + S16 - 4, run[i % 8], vel + (8 if i % 8 == 0 else 0)])

    def riser(bar, start=8, vel=56):
        """stijgende 32sten (chiptune-riser) naar een drop."""
        (pc, iv) = chords_in(bar)[-1][2]
        run = [reg(pc, 60) + o + x for o in (0, 12, 24, 36) for x in (0, iv[1], iv[2])]
        parts['sqarp'] = [a for a in parts['sqarp'] if a[0] < bar * BAR + start * S16 or a[0] >= (bar + 1) * BAR]
        for k in range((16 - start) * 2):
            t = bar * BAR + start * S16 + k * S16 // 2
            parts['sqarp'].append([t, t + S16 // 2 - 2, run[min(k, len(run) - 1)], vel + k])

    def bells(bar, pat, shift=0, vel=64):
        """v2: hoge bellen (PSG-golf) die over de melodie buitelen: in elke lange melodienoot een dalend-stijgend
        zestiendenfiguurtje op akkoordtonen, een octaaf boven de melodie."""
        for stn, ln, n in pat:
            if ln < 6:
                continue
            for i in range(stn + 2, stn + ln):
                pc, iv = [c for c in chords_in(bar) if c[0] <= i < c[1]][0][2]
                tones = sorted(reg((pc + x) % 12, 74) for x in iv[:3])
                fig = [tones[2], tones[1], tones[0], tones[1], tones[2], tones[0] + 12]
                t = bar * BAR + i * S16
                parts['bells'].append([t, t + S16 - 3, fig[(i - stn - 2) % 6], vel])

    def roll(bar, start=8, vel=64, step=6):
        """snare-roll naar een drop: zestienden, de laatste tel in 32sten, crescendo."""
        for i in range(start, 16):
            if i < 12:
                drum(bar, i, SNARE, vel + (i - start) * step)
            else:
                for h in (0, S16 // 2):
                    t = bar * BAR + i * S16 + h
                    parts['drums'].append([t, t + S16 // 2, ROLL, min(127, vel + (i - start) * step + (h > 0) * 3)])

    def timp(bar, step, vel=110, ln=4):
        pc = chords_in(bar)[0][2][0]
        for st, en, (cpc, iv) in chords_in(bar):
            if st <= step < en:
                pc = cpc
        t = bar * BAR + step * S16
        parts['timp'].append([t, t + ln * S16, reg(pc, 38), vel])

    # ---------------- maat 0: de transitie (tel 0-2 op 174 bpm, tel 2-4 op 224 bpm) ----------------
    for i in range(0, 12, 2):                                                  # paukenroffel op D, crescendo
        parts['timp'].append([i * S16, i * S16 + 2 * S16, p('D2'), 70 + i * 4])
    for i in range(0, 12):                                                     # snareroffel
        drum(0, i, ROLL, 40 + i * 5)
    rip = ['A3', 'D4', 'F#4', 'A4', 'D5', 'F#5', 'A5', 'D6']                   # de V vliegt omhoog
    for k, n in enumerate(rip):
        t = (4 + k) * S16
        parts['spicc'].append([t, t + S16 - 4, p(n), 80 + k * 4])
    parts['strmel'].append([0, 4 * S16, p('D4'), 70])                          # aanzwellende strijkers
    t = 12 * S16                                                                # tel 3: inslag
    parts['lead'].append([t, t + S16 - 2, p('A5'), 120])
    parts['horn'].append([t, t + S16 - 2, p('A4'), 116])
    parts['power'].append([t, t + S16, reg(2, 40), 120])
    drum(0, 12, CRASH, 116, 4)
    drum(0, 12, KICK, 120)
    parts['timp'].append([t, t + S16, p('A2'), 124])
    for k, n in enumerate(('D5', 'E5', 'F#5')):                                 # da-da-da ->
        t = (13 + k) * S16
        parts['lead'].append([t, t + S16 - 3, p(n), 104 + k * 6])
        drum(0, 13 + k, SNARE, 90 + k * 12)

    # ---------------- maat 1-2: de V-fanfare (explosie) ----------------
    for b in (1, 2):
        parts['lead'] += mel(FANFARE[b - 1], b, 122)
        parts['horn'] += mel(FANFARE[b - 1], b, 112, shift=-12)
        power(b, [(0, 6), (6, 2), (8, 6), (14, 2)], 110)
        bass(b)
        hats(b, range(0, 16, 2))
        drum(b, 0, BIGCRASH if b == 1 else CRASH, 124, 8)
        for s in (0, 6, 8):
            drum(b, s, KICK, 122)
        drum(b, 4, SNARE, 112)
        drum(b, 12, SNARE, 112)
        timp(b, 0, 124)
        timp(b, 8, 110)
    for i in range(12, 16):
        drum(2, i, SNARE, 90 + (i - 12) * 8)

    # ---------------- de opbouwmaat op A (maat 3 = maat 45: naadloze loop) ----------------
    def turn(b):
        spicc(b, vel=74)
        power(b, [(i, 2) for i in range(0, 16, 2)], 92)
        bass(b, octave=True)
        for s in (0, 4, 8, 12):
            drum(b, s, KICK, 104 + s)
        roll(b, 8, 60, 8)                                   # v2: snare-roll in 16en/32sten + riser naar de drop
        riser(b, 8, 50)
        for i in range(8, 16, 2):
            timp(b, i, 80 + (i - 8) * 5, 2)
        hats(b, range(0, 8))
    turn(3)

    # ---------------- de loop ----------------
    def rock(b, fill=False, crash=False):
        for s in (0, 6, 8, 10):
            drum(b, s, KICK, 120)
        for s in (4, 12):
            if not (fill and s == 12):
                drum(b, s, SNARE, 114)
        if crash:
            drum(b, 0, CRASH, 112, 8)
        if fill:
            tomfill(b)
        hats(b, range(0, 12 if fill else 16))

    def theme_bar(k, b, shift=0, choir_on=False, sq=False):
        pat = THEME[k]
        parts['lead'] += mel(pat, b, 118, shift)
        if shift:                                            # climax: hoorn een octaaf onder (unisono-kracht)
            parts['horn'] += mel(pat, b, 106, shift - 12)
        else:
            parts['horn'] += [[s, e, third_below(n) - 12, 100] for s, e, n, v in mel(pat, b, 0)]   # v2: decimen = open
        if sq:
            parts['sqlead'] += mel(pat, b, 70, shift)

    # A en A2: het heldenthema
    for sec in (A0, A2):
        for k in range(8):
            b = sec + k
            last = k == 7
            if sec == A2 and last:
                parts['lead'] += mel(THEME_TURN, b, 118)
                parts['horn'] += mel(THEME_TURN_HORN, b, 98, -12)
                parts['sqlead'] += mel(THEME_TURN, b, 70)
            else:
                theme_bar(k, b, choir_on=sec == A2, sq=sec == A2)
                if sec == A2:
                    bells(b, THEME[k], vel=60)
            spicc(b)
            power(b, [(i, 2) for i in range(0, 16, 2)], 98)
            bass(b, octave=True)
            rock(b, fill=last and sec == A2, crash=k % 4 == 0)
            if last and sec == A0:                                   # snare-roll naar B
                parts['drums'] = [d for d in parts['drums'] if not (d[2] == SNARE and d[0] >= b * BAR + 8 * S16)]
                roll(b, 8, 70)
            if k % 4 == 0:
                timp(b, 0, 118)
            if sec == A2:
                choir(b, 80)
                arp(b, 46)
            else:
                arp(b, 34)
            if last:
                riser(b, 8, 48)

    # B: royal road, de strijkers zingen
    for k in range(8):
        b = B0 + k
        parts['strmel'] += mel(STR_MEL[k], b, 112, gap=6)
        if k in B_ANSWER:
            parts['lead'] += mel(B_ANSWER[k], b, 108)
        spicc(b, steps=range(0, 16, 2), vel=78)
        power(b, [(0, 6), (6, 2), (8, 6), (14, 2)], 96)
        bass(b, steps=(0, 3, 6, 8, 11, 14))
        arp(b, 50)
        for s in (0, 8):
            drum(b, s, KICK, 116)
        drum(b, 4, SNARE, 104)
        drum(b, 12, SNARE, 104)
        if k == 0 or k == 4:
            drum(b, 0, CRASH, 104, 8)
            timp(b, 0, 112)
        hats(b, range(0, 16, 2), 64)
        if k == 7:                                                               # snareopbouw naar A2
            parts['drums'] = [d for d in parts['drums'] if not (d[2] == SNARE and d[0] >= b * BAR + 8 * S16)]
            roll(b, 8, 66, 7)
            riser(b, 8, 50)

    # C: de struggle (B-mineur), half-time, galop
    gallop = [(0, 2), (2, 1), (3, 1), (4, 2), (6, 1), (7, 1), (8, 2), (10, 1), (11, 1), (12, 2), (14, 1), (15, 1)]
    for k in range(8):
        b = C0 + k
        stop = k == 7
        if k < 4:
            parts['horn'] += mel(STRUGGLE_HORN[k], b, 118)
        else:
            parts['lead'] += mel(STRUGGLE_TP[k - 4], b, 120)
            if stop:
                parts['horn'] += mel(STRUGGLE_TP[k - 4], b, 108, -12)
            else:
                parts['horn'] += [[s, e, third_below(n), 100] for s, e, n, v in mel(STRUGGLE_TP[k - 4], b, 0)]
        steps = range(12) if stop else range(16)
        spicc(b, lo=47, steps=steps, vel=82, pattern=(0, 12, 7, 12))
        if k >= 6:
            power(b, [(i, 2) for i in range(0, 12 if stop else 16, 2)], 104)
        else:
            power(b, [g for g in gallop if g[0] < 16], 96, prog='mute')
        bass(b, steps=[i for i in range(0, 16, 2) if not (stop and i >= 12)])
        if k < 6:
            drum(b, 0, KICK, 120)
            drum(b, 6, KICK, 104)
            drum(b, 10, KICK, 110)
            drum(b, 8, SNARE, 118)
            timp(b, 0, 116)
            timp(b, 8, 100)
            hats(b, range(0, 16, 2), 60)
            if k in (0, 4):
                drum(b, 0, CRASH, 104, 8)
            if k == 3:
                tomfill(b, 12, 96)
        elif k == 6:                                              # G-A: opbouw, snare in achtsten
            for s in (0, 4, 8, 12):
                drum(b, s, KICK, 118)
            for i in range(0, 16, 2):
                drum(b, i, SNARE, 80 + i * 2)
            drum(b, 0, CRASH, 110, 8)
            for i in range(0, 16, 4):
                timp(b, i, 96 + i * 2, 2)
            hats(b, range(16), 70)
        else:                                                      # B: zestienden, en dan één tel stilte
            for s in (0, 4, 8):
                drum(b, s, KICK, 122)
            for i in range(12):
                drum(b, i, SNARE, 84 + i * 3)
            for i in range(0, 12, 2):
                timp(b, i, 96 + i * 2, 2)
            drum(b, 0, CRASH, 112, 8)
            hats(b, range(12), 76)
        if k >= 4:
            choir(b, 78 if k < 7 else 90)
        if stop:
            parts['choir'] = [c for c in parts['choir'] if not (b * BAR + 12 * S16 <= c[0])]
            parts['choir'] = [[s, min(e, b * BAR + 12 * S16 - 6), n, v] for s, e, n, v in parts['choir']]

    # D: DOORBRAAK, het thema in E-groot; maat 3 = de key change, maat 4-7 in F-groot (v2)
    for k in range(8):
        b = D0 + k
        sh = SHIFT[b]
        if k == 3:
            parts['lead'] += mel(KEYCHANGE_BAR, b, 120)
            parts['horn'] += mel(KEYCHANGE_BAR, b, 106, -12)
            parts['sqlead'] += mel(KEYCHANGE_BAR, b, 70)
        else:
            theme_bar(k, b, shift=sh, sq=True)
            bells(b, THEME[k], shift=sh, vel=68)
        spicc(b, lo=52)
        power(b, [(i, 2) for i in range(0, 16, 2)], 106 + (4 if k >= 4 else 0))
        bass(b, octave=True, vel=112)
        choir(b, 92 if k < 4 else 100)
        arp(b, 52 if k < 4 else 58)
        for s in (0, 4, 8, 12):
            drum(b, s, KICK, 124)
        for s in (4, 12):
            if not (k in (3, 7) and s == 12):
                drum(b, s, SNARE, 118)
        if k % 2 == 0 or k == 3:
            if k != 3:
                drum(b, 0, BIGCRASH if k in (0, 4) else CRASH, 120 if k in (0, 4) else 108, 8)
            timp(b, 0, 124)
        if k in (3, 7):                                            # snare-roll + riser naar de key change / T
            roll(b, 8, 76, 6)
            riser(b, 8, 56)
            hats(b, range(8), 80)
        else:
            drum(b, 14, SNARE, 84)
            hats(b, range(16), 80)

    # T: F -> G -> A: stijgende koperstoten, dan de opbouwmaat
    b = T0
    for half, top, low in ((0, ('B5', 'B5', 'D6'), ('G5', 'G5', 'B5')), (8, ('C#6', 'C#6', 'E6'), ('A5', 'A5', 'C#6'))):
        for (s, l), n, h in zip(STABS, top, low):
            t = b * BAR + (half + s) * S16
            parts['lead'].append([t, t + l * S16 - 10, p(n), 122])
            parts['horn'].append([t, t + l * S16 - 10, p(h), 108])
            parts['sqlead'].append([t, t + l * S16 - 10, p(n), 70])
            drum(b, half + s, KICK, 124)
            drum(b, half + s, SNARE if s else CRASH, 112, 1 if s else 8)
        power(b, [(half + s, l) for s, l in STABS], 112)
        bass(b, steps=[half + s for s, l in STABS])
        timp(b, half, 122)
    choir(b, 90)
    turn(T0 + 1)

    for k in parts:
        parts[k] = dedupe(parts[k])
    write_voicegroup()

    rel = releases(VG)
    progs = {'lead': TRUMPET, 'horn': HORN, 'strmel': STRINGS, 'spicc': SPICC, 'power': POWER, 'mute': MUTE,
             'bass': BASS, 'choir': CHOIR, 'timp': TIMPANI}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, 174) + 2 for k, pr in progs.items()}   # lint rekent met de eerste tempo (174)
    tail['drums'] = 8
    for k in ('lead', 'horn', 'strmel', 'spicc', 'power', 'mute', 'bass', 'choir'):
        parts[k] = detach(parts[k], tail[k])
    order = ['lead', 'drums', 'strmel', 'bass', 'horn', 'power', 'mute', 'spicc', 'choir', 'timp']
    ds = {k: parts[k] for k in order}
    kept = allocate(ds, order, tail, max_voices=MAXV)
    for k in order:
        n = len(ds[k])
        lost = n - len(kept[k])
        print('  %-6s %4d noten, %3d weg (%.1f%%)' % (k, n, lost, 100.0 * lost / max(n, 1)))
        parts[k] = kept[k]

    song = Song(TPB, 500000)
    song.tempo(0, 174 / 120)
    song.tempo(2 * TPB, 224 / 120)
    song.tempo(BAR, BPM / 120)
    song.loop = (A0 * BAR, END * BAR)
    layout = [('lead', TRUMPET, 112, 0, 64), ('horn', HORN, 92, 1, 52), ('strmel', STRINGS, 100, 2, 76),
              ('spicc', SPICC, 70, 3, 84), ('power', POWER, 72, 4, 44), ('mute', MUTE, 78, 5, 44),
              ('bass', BASS, 104, 6, 64), ('choir', CHOIR, 72, 7, 64), ('timp', TIMPANI, 96, 8, 64),
              ('sqlead', SQ_LEAD, 36, 10, 70), ('sqarp', SQ_ARP, 30, 11, 88), ('hats', NOISE, 40, 12, 72),
              ('bells', BELL, 50, 13, 40)]
    for k, prog, vol, ch, pan in layout:
        song.add(parts[k], prog, vol, ch, pan)
    song.add(parts['drums'], KIT, 110, 9)
    written = {k for k, *_ in layout} | {'drums'}
    assert not [k for k in parts if parts[k] and k not in written], 'partij niet weggeschreven'
    song.save(OUT, END * BAR)
    intro = 2 * 60 / 174 + 2 * 60 / 224 + 3 * 4 * 60 / BPM
    print(OUT, '%.1f s intro, %.1f s loop' % (intro, (END - A0) * 4 * 60 / BPM))


def write_voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Battle! Victini. Gegenereerd door tools/grounded/victini_theme.py.'
    lines[1] = ('@ 28 palm-mute-powerchord, 29 distortion-powerchord (victini_samples.py), 49 spiccato, '
                '80/81 PSG-lead/arpeggio, 82 golf-bellen, 121 PSG-hihat, 127 kit (drumsets/victini.inc).')
    lines[2] = 'voice_group %s' % VG
    repl = {
        '@ 28': '\tvoice_directsound 60, 0, DirectSoundWaveData_victini_mute, 255, 0, 255, 140  @ 28',
        '@ 29': '\tvoice_directsound 60, 0, DirectSoundWaveData_victini_power, 255, 0, 255, 160  @ 29',
        '@ 47': '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 200  @ 47',
        '@ 49': '\tvoice_keysplit voicegroup_victini_spicc_keysplit, keysplit_strings  @ 49',
        '@ 80': '\tvoice_square_1 60, 0, 0, 1, 0, 0, 12, 1  @ 80',
        '@ 81': '\tvoice_square_2 60, 0, 2, 0, 1, 6, 1  @ 81',
        '@ 82': '\tvoice_programmable_wave_alt 60, 0, ProgrammableWaveData_5, 0, 2, 6, 1  @ 82',
        '@ 121': '\tvoice_noise_alt 60, 0, 0, 0, 1, 0, 0  @ 121',
        '@ 127': '\tvoice_keysplit_all voicegroup_victini_drumset  @ 127',
    }
    out = []
    for l in lines:
        tag = '@' + l.rsplit('@', 1)[1] if '@' in l and l.startswith('\t') else None
        out.append(repl.get(tag.strip() if tag else None, l))
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    open('sound/voicegroups/keysplits/victini_spicc.inc', 'w').write(
        '@ Project Grounded: spiccato-strijkers (harde aanzet, kort) voor Battle! Victini (victini_theme.py).\n'
        'voice_group victini_spicc_keysplit\n'
        + ''.join('\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_string_ensemble_%d, 255, 210, 0, 130\n' % k
                  for k in (60, 72, 84)) + '\n')
    kit = [   # vanaf noot 36; alles DirectSound (geen PSG-piepjes)
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 160',              # 36 kick
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 170',             # 37 snare
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 160',       # 38 roffel
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_tr909_hand_clap, 255, 0, 255, 140',       # 39 clap
        'voice_directsound_no_resample 60, 50, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 190',          # 40 crash
        'voice_directsound_no_resample 60, 78, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 200',  # 41 grote crash
        'voice_directsound_no_resample 60, 79, DirectSoundWaveData_unknown_close_hihat, 255, 127, 0, 150',           # 42 hihat
        'voice_directsound 45, 40, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180',                         # 43 tom laag
        'voice_directsound 50, 52, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180',                         # 44 tom
        'voice_directsound 55, 76, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180',                         # 45 tom
        'voice_directsound 60, 88, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180',                         # 46 tom hoog
    ]
    open('sound/voicegroups/drumsets/victini.inc', 'w').write(
        '@ Project Grounded: kit voor Battle! Victini (victini_theme.py): 36 kick, 37 snare, 38 roffelsnare, 39 clap,\n'
        '@ 40 crash, 41 grote crash, 42 hihat, 43-46 toms laag -> hoog. Alles DirectSound.\n'
        'voice_group victini_drumset, 36\n' + ''.join('\t%s\n' % k for k in kit) + '\n')


if __name__ == '__main__':
    build()
