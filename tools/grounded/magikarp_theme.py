#!/usr/bin/env python3
"""Project Grounded: "Battle! Magikarp", een eigen compositie. Een vis die op het droge ligt te spartelen en zichzelf
héél serieus neemt (Splash: er gebeurt niets).

150 bpm, Bes-groot (B-deel G-klein), oom-pah met tuba + fagot, kazoo als zanger, glijtonen (pitch bend) en een
fluitje als slide whistle. Spartelende maten: af en toe een 5/8 of 7/8, en één 'verkeerde' extra tel van 3/8.
  intro  I1 fanfare (F7), I2 'TA-DAA!' + het fluitje zakt in elkaar, I3 5/8 geflap        (±4 s)
Loop (±49 s):
  A   (8 maten) de hook op kazoo (v2: een octaaf lager, F3-D5; v1 was 'te hoog, tot het irritante aan toe'): twee keer 'flip-flop' omhoog, dan een plop omlaag (boing); maat 4 = 5/8;
      maat 8: heldhaftige klim ... en de kazoo duikt een octaaf omlaag (plons)
  A'  idem, xylofoon een octaaf boven de kazoo erbij (zachter), pizzicato-plinks, kleine snare; eindigt op D7 (naar G-klein)
  B   (8 maten) quasi-dramatisch in G-klein: trompetfanfare, pauken, roffels ... B5 = de punchline: Magikarp's
      eigen cry als DJ-scratch op de maat ('Ma-' 'Ma-' 'MAGIKARP', tel 1, 1-en, 2; eigen spoor) + een bubbeltje,
      treurtrompet 'wah wah wah waaah'; tweede poging nog pompeuzer, fluitje omhoog ... en dan een lege 3/8-maat
      met alleen een vibraslap (er gebeurt niets)
  C   (8 maten) spartelen: xylofoon flapt heen en weer, kazoo antwoordt met boings, maten van 8/5/8/7/8/5/8;
      laatste maat = de fanfare van de intro, terug naar A
Voicegroup grounded_magikarp (gegenereerd) = grounded_gm met eigen samples (gm_samples.py): 70 fagot (FluidR3),
84 kazoo (gesynthetiseerde zoempuls), 78 fluitje (slide whistle), 45 pizzicato, 47 pauken met korte release,
127 eigen drumkit (drumsets/magikarp.inc): kick, snare, woodblock hoog/laag (FluidR3), boing (synth), plons
(bubbels), vibraslap (FluidR3), crash; 44/45 cry-scratch en cry (magikarp_samples.py, uit de echte Gen 3-cry). Alles DirectSound; de shaker is PSG-ruis (kost geen kanaal).
v3: kazoo 3,7 dB zachter (volume 67), en de cry-scratch vaker: A8 stotterend 'Ma-Ma-Ma-Ma-' onder de duik, C1 als
antwoord op de xylofoon (gewoon en een kwart hoger), C8 de hele cry achterstevoren tot de terugsprong.
Zie tools/grounded/MUZIEK.md. Gebruik: python3 tools/grounded/magikarp_theme.py"""
import math, os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

OUT = 'sound/songs/midi/mus_grounded_vs_magikarp.mid'
VG = 'grounded_magikarp'
TPB, BPM = 48, 150
E = TPB // 2                   # een achtste
S16 = TPB // 4
XYLO, PIZZ, TIMP, TRUMPET, TUBA, BASSOON, WHISTLE, KAZOO, SHAKER, DRUMS = 13, 45, 47, 56, 58, 70, 78, 84, 120, 127
KICK, SNARE, WB_HI, WB_LO, BOING, PLONS, VIBRA, CRASH, CRY_SCRATCH, CRY, CRY_HI, CRY_STUT, CRY_REV = range(36, 49)
DRUM_LEN = {KICK: 20, SNARE: 22, WB_HI: 8, WB_LO: 8, BOING: 88, PLONS: 36, VIBRA: 120, CRASH: 96,
            CRY_SCRATCH: 23, CRY: 108,          # cry: 0,19 s / 0,90 s bij 150 bpm (8,33 ms per tick)
            CRY_HI: 17, CRY_STUT: 10, CRY_REV: 108}   # v3: scratch een kwart hoger, 'Ma' 0,08 s, cry achterstevoren
KAZOO_SHIFT = -12             # v2 (Jordi: 'het eerste deuntje te hoog, tot het irritante aan toe'): kazoo een octaaf lager
BENDR = {'kazoo': 12, 'whistle': 12, 'tpt': 2}
CRY_VOL = 60                   # v3: mee omlaag met de kazoo (blijft net onder de lead)
KAZOO_VOL = 67                 # v3 (Jordi: 'hoofdtoon iets te luid'): 100 -> 67 = -3,5 dB t.o.v. de rest

N = {'C': 0, 'C#': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'Ab': 8, 'A': 9, 'Bb': 10, 'B': 11}


def p(name):
    """'Bb4' -> midi-noot (C4 = 60)."""
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


CH = {'Bb': [10, 2, 5], 'F7': [5, 9, 0, 3], 'Cm': [0, 3, 7], 'Gm': [7, 10, 2], 'Eb': [3, 7, 10],
      'D7': [2, 6, 9, 0], 'D': [2, 6, 9]}

# (naam, lengte in achtsten, akkoord; 'X>Y' = wissel op de 5e achtste)
INTRO = [('I1', 8, 'F7'), ('I2', 8, 'Bb'), ('I3', 5, 'F7')]
A = [('A1', 8, 'Bb'), ('A2', 8, 'F7'), ('A3', 8, 'Cm'), ('A4', 5, 'F7'),
     ('A5', 8, 'Bb'), ('A6', 8, 'Gm'), ('A7', 8, 'Eb'), ('A8', 8, 'F7>Bb')]
A2_ = [(n + "'", l, c) for n, l, c in A[:-1]] + [("A8'", 8, 'D7')]
B = [('B1', 8, 'Gm'), ('B2', 8, 'Eb>D'), ('B3', 8, 'Gm'), ('B4', 8, 'Eb>D'),
     ('B5', 8, 'D'), ('B6', 8, 'D'), ('B7', 8, 'Gm'), ('B8', 8, 'D'), ('GAP', 3, 'D')]
C = [('C1', 8, 'Bb'), ('C2', 5, 'F7'), ('C3', 8, 'Cm'), ('C4', 7, 'F7'),
     ('C5', 8, 'Bb'), ('C6', 5, 'Eb'), ('C7', 8, 'F7'), ('C8', 8, 'F7')]
BARS = INTRO + A + A2_ + B + C
START, t = {}, 0
for name, ln, ch in BARS:
    START[name] = t
    t += ln * E
END = t
LOOP = START['A1']
LEN = {n: l for n, l, c in BARS}


def chord_at(name, e8):
    ch = next(c for n, l, c in BARS if n == name)
    if '>' in ch:
        a, b = ch.split('>')
        return a if e8 < 4 else b
    return ch


# ---- melodieën: (achtste, lengte in achtsten, noot, effect) ----------------------------------------------------------
# effecten: scoop (van onderen in de noot glijden), droop (aan het eind omlaag vallen), dive (octaaf omlaag duiken),
#           vib (vibrato), rise (fluitje: octaaf omhoog), fall (fluitje: octaaf omlaag), wiggle (fluitje: spartelen)
HOOK = {
    'A1': [(0, 1, 'F5'), (1, 1, 'F5'), (2, 2, 'Bb5', 'scoop'), (4, 1, 'A5'), (5, 1, 'G5'), (6, 1, 'F5'), (7, 1, 'D5')],
    'A2': [(0, 1, 'Eb5'), (1, 1, 'D5'), (2, 1, 'C5'), (3, 3, 'F4', 'droop')],
    'A3': [(0, 1, 'G5'), (1, 1, 'G5'), (2, 2, 'C6', 'scoop'), (4, 1, 'Bb5'), (5, 1, 'A5'), (6, 1, 'G5'), (7, 1, 'Eb5')],
    'A4': [(0, 1, 'D5'), (1, 1, 'C5'), (2, 1, 'A4'), (3, 2, 'F4', 'droop')],
    'A5': [(0, 1, 'F5'), (1, 1, 'F5'), (2, 2, 'Bb5', 'scoop'), (4, 1, 'A5'), (5, 1, 'G5'), (6, 1, 'F5'), (7, 1, 'D5')],
    'A6': [(0, 1, 'Bb5'), (1, 1, 'A5'), (2, 1, 'G5'), (3, 1, 'D5'), (4, 2, 'G5', 'scoop'), (6, 1, 'F5'), (7, 1, 'Eb5')],
    'A7': [(0, 1, 'Eb5'), (1, 1, 'G5'), (2, 1, 'Bb5'), (3, 1, 'C6'), (4, 4, 'D6', 'vib')],
    'A8': [(0, 1, 'C6'), (1, 1, 'A5'), (2, 1, 'F5'), (3, 1, 'Eb5'), (4, 3, 'D5', 'dive')],
}
HOOK["A8'"] = [(0, 1, 'C6'), (1, 1, 'A5'), (2, 1, 'F#5'), (3, 1, 'D5'), (4, 2, 'D5', 'scoop'), (6, 2, 'D4', 'droop')]
FANFARE = [(0, 1, 'F4'), (1, 1, 'F4'), (2, 1, 'F4'), (3, 1, 'A4'), (4, 1, 'C5'), (5, 1, 'Eb5'), (6, 2, 'F5')]
DRAMA = {   # B: trompet (G-klein), zelfernstig
    'B1': [(0, 3, 'G4'), (3, 1, 'G4'), (4, 4, 'D5')],
    'B2': [(0, 3, 'Eb5'), (3, 1, 'D5'), (4, 1, 'C5'), (5, 1, 'Bb4'), (6, 2, 'A4')],
    'B3': [(0, 3, 'G4'), (3, 1, 'Bb4'), (4, 4, 'D5')],
    'B4': [(0, 2, 'Eb5'), (2, 2, 'F5'), (4, 4, 'F#5', 'vib')],
    'B6': [(0, 1.5, 'C4', 'droop'), (1.5, 1.5, 'B3', 'droop'), (3, 1.5, 'Bb3', 'droop'), (4.5, 3.5, 'A3', 'vib')],
    'B7': [(0, 1, 'D5'), (1, 1, 'D5'), (2, 1, 'D5'), (3, 1, 'G5'), (4, 4, 'Bb5')],
    'B8': [(0, 1, 'A5'), (1, 1, 'A5'), (2, 1, 'A5'), (3, 1, 'C6'), (4, 3, 'D6', 'vib')],
}
ANSWER = {  # C: kazoo antwoordt op het geflap
    'C2': [(0, 1, 'C5'), (1, 1, 'Eb5'), (2, 3, 'A5', 'droop')],
    'C4': [(0, 1, 'F5'), (1, 1, 'Eb5'), (2, 1, 'D5'), (3, 1, 'C5'), (4, 3, 'F4', 'droop')],
    'C6': [(0, 1, 'G5'), (1, 1, 'Bb5'), (2, 3, 'Eb6', 'scoop')],
}
FLAP = {    # C: xylofoon flapt heen en weer (zestienden)
    'C1': ['F5', 'D5', 'F5', 'D5', 'Bb5', None, None, None, 'A5', 'F5', 'A5', 'F5', 'C6', None, None, None],
    'C3': ['G5', 'Eb5', 'G5', 'Eb5', 'C6', None, None, None, 'Bb5', 'G5', 'Bb5', 'G5', 'D6', None, None, None],
    'C5': ['Bb5', 'F5', 'Bb5', 'F5', 'D6', None, None, None, 'C6', 'A5', 'C6', 'A5', 'F6', None, 'Eb6', None],
    'C7': ['F4', 'A4', 'C5', 'Eb5', 'F5', 'A5', 'C6', 'Eb6', 'F6', None, 'Eb6', None, 'C6', None, 'A5', None],
}
GM_SCALE = [7, 9, 10, 0, 2, 3, 6]          # G harmonisch klein


def third_below(n, scale):
    for d in range(1, 6):
        if (n - d) % 12 in scale:
            lo = n - d
            break
    for d in range(1, 6):
        if (lo - d) % 12 in scale:
            return lo - d
    return n - 3


def build():
    parts = {k: [] for k in ('kazoo', 'xylo', 'tpt', 'tpt2', 'tuba', 'bassoon', 'pizz', 'timp', 'whistle', 'drums',
                             'shaker', 'cry')}
    fx = {k: [] for k in BENDR}            # (start, eind, effect) per spoor met pitch bend

    def note(part, bar, e8, ln8, nm, vel, eff=None, stacc=True):
        s = START[bar] + int(round(e8 * E))
        ln = int(round(ln8 * E))
        dur = int(E * 0.7) if (stacc and ln8 <= 1) else ln - 4
        n = p(nm) if isinstance(nm, str) else nm
        parts[part].append([s, s + dur, n, vel])
        if eff:
            fx[part].append((s, s + dur, eff))

    def drum(bar, e8, n, vel):
        s = START[bar] + int(round(e8 * E))
        parts['drums'].append([s, s + DRUM_LEN[n], n, vel])

    def mel(part, bar, pat, vel, shift=0):
        for x in pat:
            e8, ln8, nm = x[:3]
            accent = 8 if e8 in (0, 2, 4) else 0
            note(part, bar, e8, ln8, p(nm) + shift, vel + accent, x[3] if len(x) > 3 and part in BENDR else None)

    def roll(part, bar, e8_from, e8_to, n, v0, v1, step=0.5):
        k, cnt = e8_from, int((e8_to - e8_from) / step)
        for i in range(cnt):
            v = v0 + (v1 - v0) * i / max(1, cnt - 1)
            if part == 'drums':
                drum(bar, k, n, int(v))
            else:
                note(part, bar, k, step, n, int(v))
            k += step

    # ---- bas: oom-pah (tuba + fagot), ritme volgt de maatlengte ----------------------------------------------------
    def oompah(bar, ln, vel=112):
        for e8 in ((0, 4) if ln == 8 else (0, 3) if ln == 5 else (0, 4)):
            ch = CH[chord_at(bar, e8)]
            root = bass_note(ch[0])
            nt = root if e8 == 0 or '>' in next(c for n, l, c in BARS if n == bar) else fifth(root, ch)
            note('tuba', bar, e8, 1.5, nt, vel)
            drum(bar, e8, KICK, 100)
        pah = {8: (2, 6), 5: (2, 4), 7: (2, 5, 6)}[ln]
        for e8 in pah:
            ch = CH[chord_at(bar, e8)]
            note('bassoon', bar, e8, 1, top(ch[1], 50, 62), vel - 14)

    def spartel(bar, ln, vel=86):          # woodblock: onregelmatig geflap in zestienden
        pat = {8: (1, 3, 4, 9, 11, 12, 13), 5: (1, 2, 3, 6, 7, 8), 7: (1, 3, 4, 7, 9, 10, 11)}[ln]
        for i, k in enumerate(pat):
            drum(bar, k / 2, WB_HI if i % 3 != 2 else WB_LO, vel - (10 if i % 2 else 0))

    def shaker(bar, ln, vel=60):
        for k in range(ln):
            s = START[bar] + k * E
            parts['shaker'].append([s, s + 4, 76, vel if k % 2 else vel - 22])

    # ---- intro ---------------------------------------------------------------------------------------------------
    def fanfare(bar):
        mel('tpt', bar, FANFARE, 108)
        mel('tpt2', bar, FANFARE, 96, shift=-12)
        roll('timp', bar, 0, 6, p('F2'), 60, 112)
        roll('drums', bar, 4, 8, SNARE, 50, 104)
        note('tuba', bar, 0, 1, p('F2'), 112)
        note('tuba', bar, 6, 2, p('F2'), 116, stacc=False)
        drum(bar, 0, KICK, 104)
    fanfare('I1')
    # I2: TA-DAA! ... en het fluitje zakt in elkaar
    note('tpt', 'I2', 0, 3, 'Bb5', 120, stacc=False)
    note('tpt2', 'I2', 0, 3, 'D5', 108, stacc=False)
    note('tuba', 'I2', 0, 3, 'Bb1', 120, stacc=False)
    note('timp', 'I2', 0, 1, 'Bb2', 120)
    drum('I2', 0, CRASH, 110)
    drum('I2', 0, KICK, 112)
    note('whistle', 'I2', 3, 3.5, 'Bb5', 104, 'fall', stacc=False)   # v2: Bb5 i.p.v. Bb6 (minder schel)
    drum('I2', 7, PLONS, 110)
    # I3 (5/8): geflap
    drum('I3', 0, BOING, 112)
    spartel('I3', 5, 92)
    for e8, nm in ((0, 'F3'), (1.5, 'C3'), (2, 'F3'), (3, 'A3'), (3.5, 'C4')):
        note('bassoon', 'I3', e8, 0.5, nm, 104)
    note('tuba', 'I3', 0, 1, 'F2', 110)

    # ---- A en A' -------------------------------------------------------------------------------------------------
    for prime in ('', "'"):
        for name, ln, ch in A:
            bar = name + prime
            key = name if not (prime and name == 'A8') else "A8'"
            mel('kazoo', bar, HOOK[key], 104, shift=KAZOO_SHIFT)
            oompah(bar, ln)
            spartel(bar, ln, 80 if not prime else 72)
            shaker(bar, ln)
            if prime:                                               # xylofoon een octaaf boven de kazoo, snare op 2 en 4
                for x in HOOK[key]:
                    note('xylo', bar, x[0], min(x[1], 1), p(x[2]) + KAZOO_SHIFT + 12, 80)
                for e8 in ((2, 6) if ln == 8 else (2,)):
                    drum(bar, e8, SNARE, 70)
                for e8 in ((3, 7) if ln == 8 else (4,)):            # pizzicato-plinks op de achteraan-tel
                    tones = CH[chord_at(bar, e8)]
                    note('pizz', bar, e8, 1, top(tones[2 if len(tones) > 2 else 0], 67, 79), 84)
        b1 = 'A1' + prime
        drum(b1, 0, CRASH, 104 if not prime else 92)
        for nm in ('A2', 'A4'):                                     # de plop: boing op de vallende noot
            drum(nm + prime, 3, BOING, 100)
        for e8, nm in ((6, 'F3'), (6.5, 'C3'), (7, 'F2')):         # fagot: blub-blub-blub na de plop
            note('bassoon', 'A2' + prime, e8, 0.5, nm, 100)
        if prime:
            note('whistle', "A4'", 3, 2, 'C6', 96, 'wiggle', stacc=False)
        else:
            drum('A8', 7, PLONS, 112)                               # na de duik: plons
    note('whistle', "A8'", 4, 2, 'D6', 96, 'rise', stacc=False)

    # ---- B: het drama ----------------------------------------------------------------------------------------------
    for bar in ('B1', 'B2', 'B3', 'B4', 'B7', 'B8'):
        mel('tpt', bar, DRAMA[bar], 112)
        if bar in ('B3', 'B4', 'B7', 'B8'):
            parts['tpt2'] += [[s, e, third_below(n, GM_SCALE), v - 14] for s, e, n, v in
                              mel_notes(bar, DRAMA[bar], 112)]
        for e8 in (0, 4):                                           # tuba: zware halve noten, fagot: achtsten
            ch = CH[chord_at(bar, e8)]
            note('tuba', bar, e8, 3, bass_note(ch[0]), 116, stacc=False)
        for e8 in range(8):
            ch = CH[chord_at(bar, e8)]
            note('bassoon', bar, e8, 1, top(ch[0], 43, 55), 88 if e8 % 2 else 100)
        for e8 in (0, 3, 4):
            drum(bar, e8, KICK, 108)
        for e8 in (2, 6):
            drum(bar, e8, SNARE, 96)
        shaker(bar, 8, 52)
    for bar in ('B1', 'B3', 'B7'):
        roll('timp', bar, 4, 8, p('G2'), 64, 108)
    for bar in ('B4', 'B8'):
        roll('timp', bar, 0, 8, p('D2'), 56, 118)
        roll('drums', bar, 6, 8, SNARE, 70, 112, step=0.25)
    for bar in ('B1', 'B7'):
        drum(bar, 0, CRASH, 112)
    # B5: de punchline van de heldenfanfare: Magikarp's eigen cry als DJ-scratch, 'Ma- Ma- MAGIKARP!' (tel 1, 1-en,
    # 2), dan alleen een klein bubbeltje (Splash: er gebeurt niets)
    for e8, n in ((0, CRY_SCRATCH), (1, CRY_SCRATCH), (2, CRY)):
        s = START['B5'] + e8 * E
        parts['cry'].append([s, s + DRUM_LEN[n], n, 127])
    drum('B5', 7, PLONS, 72)
    # v3 (Jordi: 'de scratch is gelukt, mag vaker'): nog drie scratches, steeds op de maat en net onder de lead.
    # A8 (einde van de eerste A): terwijl de kazoo een octaaf omlaag duikt, blijft de plaat haken: 'Ma-Ma-Ma-Ma-'
    for k in range(4):
        s = START['A8'] + 5 * E + k * S16
        parts['cry'].append([s, s + DRUM_LEN[CRY_STUT], CRY_STUT, 104 + 6 * k])
    # C1: de xylofoon flapt, Magikarp antwoordt in de gaten: 'Ma-?' (2-en) ... 'MA-?!' (4-en, een kwart hoger)
    for e8, n, v in ((3, CRY_SCRATCH, 110), (7, CRY_HI, 120)):
        s = START['C1'] + e8 * E
        parts['cry'].append([s, s + DRUM_LEN[n], n, v])
    # C8: onder de fanfare de hele cry achterstevoren, die precies op de terugsprong (A1, crash) eindigt
    s = END - 2 - DRUM_LEN[CRY_REV]                                # 2 ticks marge: niet over de loopsprong heen
    parts['cry'].append([s, END - 2, CRY_REV, 120])
    # B6: wah wah wah waaah (treurtrompet, tuba eronder)
    mel('tpt', 'B6', DRAMA['B6'], 110)
    for x in DRAMA['B6']:
        note('tuba', 'B6', x[0], x[1], p(x[2]) - 24, 100, stacc=False)
    drum('B6', 4.5, BOING, 96)
    # B8 -> GAP: fluitje omhoog ... en dan niets (3/8 met alleen een vibraslap)
    note('whistle', 'B8', 4, 4, 'D6', 100, 'rise', stacc=False)
    drum('GAP', 0, VIBRA, 116)

    # ---- C: spartelen ----------------------------------------------------------------------------------------------
    for name, ln, ch in C[:-1]:
        if name in FLAP:
            for k, nm in enumerate(FLAP[name]):
                if nm:
                    note('xylo', name, k / 2, 0.5, nm, 100 if k % 4 == 0 else 86)
        if name in ANSWER:
            mel('kazoo', name, ANSWER[name], 104, shift=KAZOO_SHIFT)
            drum(name, 0, BOING, 104)
        spartel(name, ln, 84)
        shaker(name, ln)
        for e8 in ((0, 4) if ln == 8 else (0, 3) if ln == 5 else (0, 4)):   # tuba kort, pizzicato erachteraan
            tones = CH[chord_at(name, e8)]
            note('tuba', name, e8, 1, bass_note(tones[0]), 108)
            drum(name, e8, KICK, 96)
            for o, e in ((tones[1], e8 + 1), (tones[2 if len(tones) > 2 else 0], e8 + 2)):
                if e < ln:
                    note('pizz', name, e, 1, top(o, 55, 67), 92)
    drum('C1', 0, CRASH, 96)
    note('whistle', 'C3', 4, 4, 'D6', 88, 'wiggle', stacc=False)
    note('whistle', 'C7', 0, 4, 'F5', 92, 'rise', stacc=False)   # v2: F5 i.p.v. F6
    fanfare('C8')

    for k in parts:
        parts[k] = dedupe(parts[k])
    return parts, fx


def mel_notes(bar, pat, vel):
    out = []
    for x in pat:
        e8, ln8, nm = x[:3]
        s = START[bar] + int(round(e8 * E))
        dur = int(E * 0.7) if ln8 <= 1 else int(round(ln8 * E)) - 4
        out.append([s, s + dur, p(nm), vel + (8 if e8 in (0, 2, 4) else 0)])
    return out


def bass_note(pc):
    """Grondtoon tussen Bb1 (34) en A2 (45)."""
    n = 24 + pc
    while n < 34:
        n += 12
    return n


def fifth(root, ch):
    f = root + 7
    return f if f <= 45 else f - 12


def top(pc, lo, hi):
    n = pc
    while n < lo:
        n += 12
    return n if n < hi else n - 12


def bend_events(part, notes, effects):
    """Pitch bend / vibrato per noot. Waarde in halve tonen (BENDR = bereik); terugzetten bij de volgende noot."""
    rng = BENDR[part]
    ev = [(0, mido.Message('control_change', control=20, value=rng)),     # BENDR
          (0, mido.Message('control_change', control=21, value=44)),      # LFOS: snel, kazoo-achtig
          (0, mido.Message('pitchwheel', pitch=0)),
          (0, mido.Message('control_change', control=1, value=0))]

    def pw(t, semis):
        u = max(-64, min(63, int(round(semis / rng * 64))))
        ev.append((int(t), mido.Message('pitchwheel', pitch=u * 128)))

    starts = sorted(set(n[0] for n in notes))
    for s, e, kind in sorted(effects):
        nxt = next((x for x in starts if x > s), e + TPB)
        d = e - s
        if kind == 'scoop':
            for i in range(5):
                pw(s + 2 * i, -2 + 0.5 * i)
        elif kind in ('droop', 'dive', 'fall'):
            depth = {'droop': -3, 'dive': -12, 'fall': -12}[kind]
            t0 = s + (d // 2 if kind == 'droop' else d // 6)
            steps = max(2, (e - t0) // 2)
            for i in range(steps + 1):
                f = i / steps
                pw(t0 + 2 * i, depth * (f ** 1.4 if kind == 'droop' else f))
        elif kind == 'rise':
            steps = max(2, d // 2)
            for i in range(steps + 1):
                f = i / steps
                pw(s + 2 * i, -12 * (1 - f) ** 1.3)
        elif kind == 'wiggle':
            steps = max(2, d // 2)
            for i in range(steps + 1):
                f = i / steps
                pw(s + 2 * i, -5 + 5 * math.sin(f * math.pi * 5) - 2 * f)
        elif kind == 'vib':
            ev.append((s + d // 3, mido.Message('control_change', control=1, value=28 if part != 'tpt' else 40)))
            ev.append((nxt, mido.Message('control_change', control=1, value=0)))
        if kind != 'vib':
            ev.append((min(nxt, e + 30), mido.Message('pitchwheel', pitch=0)))
    return sorted(ev, key=lambda x: x[0])


def write_voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Battle! Magikarp. Gegenereerd door tools/grounded/magikarp_theme.py.'
    lines[1] = ('@ 45 pizzicato, 47 pauken (korte release), 70 fagot, 78 fluitje (slide whistle), 84 kazoo, '
                '127 Magikarp-drumkit.')
    lines[2] = 'voice_group %s' % VG
    repl = {
        '@ 45': '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_pizzicato_strings, 255, 216, 0, 140  @ 45',
        '@ 47': '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 180  @ 47',
        '@ 70': '\tvoice_directsound 60, 0, DirectSoundWaveData_magikarp_bassoon, 255, 0, 255, 120  @ 70',
        '@ 78': '\tvoice_directsound 60, 0, DirectSoundWaveData_sd90_classical_whistle, 255, 0, 255, 120  @ 78',
        '@ 84': '\tvoice_directsound 60, 0, DirectSoundWaveData_magikarp_kazoo, 250, 0, 255, 120  @ 84',
        '@ 127': '\tvoice_keysplit_all voicegroup_magikarp_drumset  @ 127',
    }
    out = []
    for l in lines:
        tag = '@' + l.rsplit('@', 1)[1] if '@' in l and l.startswith('\t') else None
        out.append(repl.get(tag.strip() if tag else None, l))
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    kit = [   # vanaf noot 36; alles DirectSound (geen PSG-piepjes)
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 0',          # 36 kick
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 0',         # 37 snare
        'voice_directsound 76, 74, DirectSoundWaveData_magikarp_woodblock, 255, 0, 255, 0',                    # 38 woodblock hoog
        'voice_directsound 69, 54, DirectSoundWaveData_magikarp_woodblock, 255, 0, 255, 0',                    # 39 woodblock laag
        'voice_directsound 60, 64, DirectSoundWaveData_magikarp_boing, 255, 0, 255, 0',                        # 40 boing
        'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_bubbles, 255, 0, 255, 0',                       # 41 plons
        'voice_directsound 60, 64, DirectSoundWaveData_magikarp_vibraslap, 255, 0, 255, 0',                    # 42 vibraslap
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165',    # 43 crash
        'voice_directsound 60, 64, DirectSoundWaveData_magikarp_cry_scratch, 255, 0, 255, 0',                  # 44 cry-scratch
        'voice_directsound 60, 64, DirectSoundWaveData_magikarp_cry, 255, 0, 255, 0',                          # 45 cry
        'voice_directsound 65, 64, DirectSoundWaveData_magikarp_cry_scratch, 255, 0, 255, 0',                  # 46 cry-scratch hoog
        'voice_directsound 60, 64, DirectSoundWaveData_magikarp_cry_stutter, 255, 0, 255, 0',                  # 47 'Ma' (stotter)
        'voice_directsound 60, 64, DirectSoundWaveData_magikarp_cry_rev, 255, 0, 255, 0',                      # 48 cry achterstevoren
    ]
    open('sound/voicegroups/drumsets/magikarp.inc', 'w').write(
        '@ Project Grounded: drumkit voor Battle! Magikarp (magikarp_theme.py): 36 kick, 37 snare, 38/39 woodblock,\n'
        '@ 40 boing (springveer), 41 plons (bubbels), 42 vibraslap, 43 crash, 44 cry-scratch, 45 cry, 46 cry-scratch hoog,\n'
        '@ 47 stotter-scratch, 48 cry achterstevoren (magikarp_samples.py).\n'
        'voice_group magikarp_drumset, 36\n' + ''.join('\t%s\n' % k for k in kit) + '\n')


def main():
    parts, fx = build()
    write_voicegroup()
    rel = releases(VG)
    progs = {'kazoo': KAZOO, 'xylo': XYLO, 'tpt': TRUMPET, 'tpt2': TRUMPET, 'tuba': TUBA, 'bassoon': BASSOON,
             'pizz': PIZZ, 'timp': TIMP, 'whistle': WHISTLE}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) for k, pr in progs.items()}
    tail['drums'] = tail['cry'] = 0
    for k in ('kazoo', 'tpt', 'tpt2', 'tuba'):
        parts[k] = detach(parts[k], tail[k])
    order = ['cry', 'kazoo', 'tpt', 'drums', 'whistle', 'xylo', 'tuba', 'bassoon', 'tpt2', 'pizz', 'timp']
    ds = {k: parts[k] for k in order}
    kept = allocate(ds, order, tail)
    print('tail (ticks):', tail)
    for k in order:
        n = len(ds[k])
        print('  %-8s %4d noten, %3d vallen weg (%.1f%%)' % (k, n, n - len(kept[k]), 100 * (n - len(kept[k])) / max(n, 1)))
        parts[k] = kept[k]

    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.loop = (LOOP, END)
    layout = [('kazoo', KAZOO, KAZOO_VOL, 0, 64), ('xylo', XYLO, 84, 1, 84), ('tpt', TRUMPET, 104, 2, 54),
              ('tpt2', TRUMPET, 88, 3, 74), ('tuba', TUBA, 112, 4, 64), ('bassoon', BASSOON, 96, 5, 44),
              ('pizz', PIZZ, 84, 6, 92), ('timp', TIMP, 96, 7, 64), ('whistle', WHISTLE, 76, 8, 70),
              ('shaker', SHAKER, 40, 10, 80)]
    for k, prog, vol, ch, pan in layout:
        extra = bend_events(k, parts[k], fx[k]) if k in fx else ()
        song.add(parts[k], prog, vol, ch, pan, extra)
    song.add(parts['drums'], DRUMS, 104, 9)
    song.add(parts['cry'], DRUMS, CRY_VOL, 11, 64)               # eigen spoor: volume los van de drums
    written = {k for k, *_ in layout} | {'drums', 'cry'}
    assert not [k for k in parts if parts[k] and k not in written], 'partij niet weggeschreven'
    song.save(OUT, END)
    print(OUT, '%.1f s intro, %.1f s loop' % (LOOP / TPB * 60 / BPM, (END - LOOP) / TPB * 60 / BPM))


if __name__ == '__main__':
    main()
