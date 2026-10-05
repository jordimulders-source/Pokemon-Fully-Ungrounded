#!/usr/bin/env python3
"""Project Grounded: "Battle! Heatran" v3, eigen compositie in desert/stoner rock & heavy psych (Kyuss 'Welcome to
Sky Valley'/'Gardenia', Fu Manchu, Truckfighters, Sleep, Electric Wizard).

Jordi over v2: 'klinkt te veel als surf rock, ska-punk of upbeat 60s rock'. Gemeten oorzaken in v2 (zie MUZIEK.md):
  - ritme: 100 bpm met een riff vol korte 16e-stoten (powerchords gem. 0,78 tel, losse noten 0,07 tel na detach),
    een drukke melodische 16e-baslijn (2,9 aanslagen/s, 70% <= een 8e), kick 60% naast de tel, ghost notes,
    hihat in 8en met een open hihat op de laatste 'en' = upbeat rock/ska;
  - rock-'n-roll-wendingen: chromatische opstapjes (G-Bb-B -> C, Eb-D, Gb-F-Eb): 21% chromatische stappen in de riff;
  - klank: 'Big Muff' met middenboost 150-700 Hz (= 60s-fuzz-honk), fuzzlead met 46% energie > 2 kHz, schone
    middenstukgitaar (GM 27) = twang.
v3 volgt de briefing strikt:
  - C standard / drop C, extreem laag; fuzz = schone gitaar door eigen 'Big Muff' (middenscoop) + 'SVT/Sunn + kast'
    (heatran_samples.py): donker, wollig, geen treble;
  - 84 bpm; refreinen halftempo (snare op 3 = 42 bpm-gevoel), strofen trage zware groove; bekkens alleen óp de tellen
    (kwarten, open en gruizig), geen 8e-hihat, geen off-beats, geen ghost notes;
  - riffs: lange aangehouden powerchords, C-mineur-pentatonisch + b5 (Gb), b6 (Ab) als doomkleur, slides i.p.v.
    chromatische opstapjes; bas (SVT-fuzz) verdubbelt de riff unisono;
  - vorm (Jordi): strofen alleen bas + drums, later de refreinriff palm-muted (lange gedempte 8e-chugs); refreinen
    zwaar en headbangend; hard/zacht; rustig middenstuk met bas en getokkel (warme, donkere gitaar), dan opbouw.

  maat 0-1   intro: fuzz-powerchord C zwelt aan + feedback, floor tom rommelt in 8en
  maat 2-4   de refreinriff als statement (2 maten), maat 4 = de stop (akkoord hangt, feedback, baspickup)
Loop (48 maten, 137 s):
  V1  5-12   strofe: bas + drums (halfopen hihat in kwarten); 9-12 de refreinriff palm-muted, zacht links
  R1 13-20   refrein: riff voluit, halftempo, crash/china om de 2 maten, open hihat op de tellen; 20 = stop
  V2 21-28   strofe 2: bas (variant met octaafsprong) + drums (ride in kwarten); palm-mute links en rechts
  R2 29-36   refrein 2: riff + de leadgitaar 'zingt' erboven (lange noten, bends)
  M  37-44   middenstuk: bas + getokkelde warme gitaar, ride zacht; 41-44 opbouw (floor tom, feedback, roffel)
  R3 45-52   refrein 3: riff + bluesy solo; 52 = stop -> terug naar de strofe (= maat 4 -> 5)
Samples: tools/grounded/heatran_samples.py. Gebruikt musiclib.py; zie MUZIEK.md. Gebruik: python3 tools/grounded/heatran_theme.py"""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks

OUT = 'sound/songs/midi/mus_grounded_vs_heatran.mid'
VG = 'grounded_heatran'
TPB, BPM = 96, 84
S = TPB // 4                   # een 16e
E = TPB // 2                   # een 8e
BAR = TPB * 4
LAY = 3                        # snare iets achter de tel (lome groove)
CLEAN, MUTE, POWER, LEAD, BASS, DRUMS = 27, 28, 30, 31, 34, 127
R_BEND = 3 * 128               # rechter gitaar ±9 cent hoger (dubbele opname)
# eigen drumkit (drumsets/heatran.inc, vanaf noot 36)
KICK, SNARE, OHH, RIDE, FTOM, MTOM, CRASH, CHINA, STICK, BELL, HHALF = range(36, 47)
DRUM_REL = {KICK: 0, SNARE: 0, OHH: 215, RIDE: 215, FTOM: 0, MTOM: 0, CRASH: 225, CHINA: 220, STICK: 0, BELL: 200,
            HHALF: 0}
DRUM_LEN = {KICK: TPB // 2, SNARE: TPB, OHH: TPB, RIDE: TPB, FTOM: TPB // 2, MTOM: TPB // 2, CRASH: TPB * 3,
            CHINA: TPB * 2, STICK: S, BELL: TPB // 2, HHALF: TPB // 3}

INTRO_RIFF, STOP0 = 2, 4
V1, R1, V2, R2, M, R3, END = 5, 13, 21, 29, 37, 45, 53      # secties (maat); loop = maat 5-53

N = {'C': 0, 'Db': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'Gb': 6, 'G': 7, 'Ab': 8, 'A': 9, 'Bb': 10, 'B': 11}


def p(name):
    """'C2' -> midi-noot (C4 = 60)."""
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


# ---- de refreinriff (drop C): (16e, lengte in 16en, soort, grondtoon) ------------------------------------------
# 'P' = aangehouden powerchord, 'S' = powerchord die erin glijdt (slide van 2 halve tonen eronder), 'M' = één
# gedempte chug (palm-mute) tussen twee akkoorden. Lange, doorklinkende akkoorden; geen chromatische opstapjes.
RIFF_A1 = [(0, 6, 'P', 'C2'), (6, 2, 'M', 'C2'), (8, 4, 'P', 'Eb2'), (12, 4, 'S', 'F2')]
RIFF_A2 = [(0, 2, 'P', 'Gb2'), (2, 2, 'P', 'F2'), (4, 4, 'P', 'Eb2'), (8, 8, 'P', 'C2')]
RIFF_B1 = [(0, 6, 'P', 'C2'), (6, 2, 'M', 'C2'), (8, 4, 'P', 'G2'), (12, 4, 'S', 'Bb2')]
RIFF_B2 = [(0, 6, 'P', 'Ab2'), (6, 2, 'P', 'G2'), (8, 8, 'P', 'F2')]
RIFF_TURN = [(0, 8, 'P', 'Ab2'), (8, 8, 'S', 'Bb2')]
RIFF_STOP = [(0, 8, 'P', 'C2')]                                    # akkoord hangt 2 tellen, dan stilte
STOP_BASS = [(0, 8, 'C2'), (12, 2, 'G1'), (14, 2, 'Bb1')]          # pentatonische pickup naar de strofe
CHORUS = [RIFF_A1, RIFF_A2, RIFF_A1, RIFF_A2, RIFF_B1, RIFF_B2, RIFF_TURN, RIFF_STOP]

# ---- strofe: de fuzzbas-groove (16e, lengte, noot); trage, aangehouden noten ------------------------------------
VB_1 = [(0, 6, 'C2'), (6, 2, 'C2'), (8, 2, 'Eb2'), (10, 2, 'F2'), (12, 4, 'G2')]
VB_2 = [(0, 3, 'F2'), (3, 1, 'Gb2'), (4, 4, 'F2'), (8, 4, 'Eb2'), (12, 4, 'C2')]
VB_3 = [(0, 6, 'C2'), (6, 2, 'C3'), (8, 2, 'Bb2'), (10, 2, 'G2'), (12, 4, 'F2')]      # Kyuss-octaafsprong
VB_4 = [(0, 4, 'Eb2'), (4, 2, 'F2'), (6, 2, 'Eb2'), (8, 6, 'C2'), (14, 2, 'Bb1')]
VB_T = [(0, 8, 'G1'), (8, 8, 'Bb1')]                                # naar het refrein
VERSE_BASS = [VB_1, VB_2, VB_1, VB_4, VB_1, VB_2, VB_1, VB_T]
VERSE2_BASS = [VB_1, VB_2, VB_3, VB_4, VB_1, VB_2, VB_3, VB_T]

# ---- middenstuk: getokkelde warme gitaar (8en, laten doorklinken) en de bas -----------------------------------
ARP = [['C3', 'G3', 'Bb3', 'D4', 'Eb4', 'D4', 'Bb3', 'G3'],      # Cm9
       ['C3', 'G3', 'Bb3', 'D4', 'Eb4', 'D4', 'Bb3', 'G3'],
       ['F2', 'C3', 'A3', 'Eb4', 'G4', 'Eb4', 'A3', 'C3'],       # F9 (dorisch: de woestijn-IV)
       ['F2', 'C3', 'A3', 'Eb4', 'G4', 'Eb4', 'A3', 'C3'],
       ['Ab2', 'Eb3', 'G3', 'C4', 'Eb4', 'C4', 'G3', 'Eb3'],     # Abmaj7
       ['Bb2', 'F3', 'Bb3', 'D4', 'F4', 'D4', 'Bb3', 'F3'],      # Bb
       ['C3', 'G3', 'C4', 'Eb4', 'G4', 'Eb4', 'C4', 'G3'],       # Cm
       ['G2', 'D3', 'F3', 'Bb3', 'D4', 'Bb3', 'F3', 'D3']]       # Gm7 -> refrein
MID_BASS = [[(0, 16, 'C2')], [(0, 12, 'C2'), (12, 4, 'Bb1')],
            [(0, 16, 'F2')], [(0, 12, 'F2'), (12, 4, 'Eb2')],
            [(0, 16, 'Ab1')], [(0, 16, 'Bb1')],
            [(0, 16, 'C2')], [(0, 8, 'G1'), (8, 8, 'Bb1')]]

# ---- leadgitaar: (16e, lengte, noot, extra) ; 'b' = bend van 2 halve tonen eronder, 'v' = vibrato ----------------
SING = [   # R2: de 'zang'-melodie (John Garcia) op de leadgitaar, C-mineur-pentatonisch, lange noten
    [(4, 4, 'G4', ''), (8, 8, 'Bb4', 'v')],
    [(0, 8, 'G4', 'bv'), (10, 2, 'Eb4', ''), (12, 4, 'C4', 'v')],
    [(4, 4, 'G4', ''), (8, 6, 'Bb4', 'v'), (14, 2, 'C5', '')],
    [(0, 12, 'G4', 'v')],
    [(4, 4, 'C5', ''), (8, 8, 'Eb5', 'v')],
    [(0, 8, 'C5', 'bv'), (8, 4, 'Bb4', ''), (12, 4, 'G4', 'v')],
    [(0, 8, 'F4', 'v'), (8, 8, 'G4', 'bv')],
    [(0, 12, 'C4', 'v')],
]
SOLO = [
    [(0, 4, 'G4', ''), (4, 4, 'C5', 'b'), (8, 2, 'Bb4', ''), (10, 2, 'G4', ''), (12, 4, 'F4', 'v')],
    [(0, 4, 'G4', 'b'), (4, 2, 'F4', ''), (6, 2, 'Eb4', ''), (8, 8, 'C4', 'v')],
    [(0, 6, 'G4', 'bv'), (6, 2, 'Bb4', ''), (8, 2, 'C5', ''), (10, 2, 'Eb5', ''), (12, 4, 'C5', 'v')],
    [(0, 2, 'Bb4', ''), (2, 2, 'G4', ''), (4, 2, 'Gb4', ''), (6, 2, 'F4', ''), (8, 8, 'Eb4', 'v')],
    [(0, 2, 'C5', ''), (2, 2, 'Eb5', ''), (4, 4, 'F5', 'bv'), (8, 2, 'Eb5', ''), (10, 2, 'C5', ''), (12, 4, 'Bb4', '')],
    [(0, 8, 'C5', 'bv'), (8, 2, 'Bb4', ''), (10, 2, 'G4', ''), (12, 4, 'Gb4', 'v')],
    [(0, 8, 'F4', 'bv'), (8, 8, 'G4', 'bv')],
    [(0, 12, 'C5', 'v')],                                     # de stop: lang uitzingen boven het hangende akkoord
]


def bass_note(n):
    """Bas: zelfde toonklasse als de riff, in E1-Eb3 (nooit onder E1 = 28)."""
    while n > 51:
        n -= 12
    while n < 28:
        n += 12
    return n


class Parts:
    def __init__(self):
        self.n = {k: [] for k in ('pwrL', 'pwrR', 'muteL', 'muteR', 'clean', 'bass', 'lead', 'fb',
                                  'kick', 'snare', 'cym', 'tom')}
        self.fx = {k: [] for k in list(self.n) + ['drums']}   # (tick, 'vol'|'mod'|'bend', waarde); 'vol' = CC7 in %

    def add(self, part, start, length, note, vel):
        self.n[part].append([int(start), int(start + length), note, vel])

    def vol(self, parts, bar, pct):
        for k in parts:
            self.fx[k].append((bar * BAR, 'vol', pct))


def slide(P, part, s, cents=2):
    """In de noot glijden: begint `cents` halve tonen lager, in een 8e omhoog (pitchwheel; bereik 2 halve tonen)."""
    for k in range(0, 7):
        P.fx[part].append((s + k * E // 6, 'bend', min(8191, int(8192 * (k / 6 - 1)))))


def riff(P, bar, pattern, vel=112, guitars=True, bass=True, right=True):
    for st, ln, kind, nm in pattern:
        s = bar * BAR + st * S
        acc = 8 if st in (0, 8) else 0
        if guitars:
            for sd in (('L', 'R') if right else ('L',)):
                if kind == 'M':
                    P.add('mute' + sd, s, ln * S, p(nm), 116 - (4 if sd == 'R' else 0))
                else:
                    P.add('pwr' + sd, s, ln * S, p(nm), vel + acc - (6 if sd == 'R' else 0))
                    if kind == 'S':
                        slide(P, 'pwr' + sd, s)
        if bass:
            P.add('bass', s, ln * S, bass_note(p(nm)), 114 + (8 if st in (0, 8) else 0))


def palm_mute(P, bar, pattern, sides=('L',), vel=104):
    """De refreinriff gedempt: elke akkoordnoot als gedempte chugs op elke 8e, zolang de noot duurt."""
    for st, ln, kind, nm in pattern:
        for k in range(0, ln, 2):
            s = bar * BAR + (st + k) * S
            for sd in sides:
                P.add('mute' + sd, s, E, p(nm), vel + (10 if st + k in (0, 8) else 0) - (4 if sd == 'R' else 0))


def lead(P, bar, phrase, vel=118, part='lead'):
    for st, ln, nm, fx in phrase:
        s = bar * BAR + st * S
        P.add(part, s, ln * S, p(nm) - (2 if 'b' in fx else 0), vel)
        if 'b' in fx:                                       # bend: begint 2 halve tonen lager, in een 8e omhoog
            for k in range(1, 7):
                P.fx[part].append((s + k * E // 6, 'bend', min(8191, int(8192 * k / 6))))
        if 'v' in fx and ln >= 4:                           # vertraagd vibrato (na een 8e)
            P.fx[part].append((s + E, 'mod', 8))


def verse_drums(P, bar, i, cym='hat'):
    """Strofe: trage zware groove. Kick op 1 (+ één 8e-duw), snare op 2 en 4, bekken alleen op de tellen."""
    b = bar * BAR
    kicks = (0, 6, 8) if i % 2 == 0 else (0, 8, 10)
    for k in kicks:
        P.add('kick', b + k * S, DRUM_LEN[KICK], KICK, 118 if k == 0 else 104)
    for q in (4, 12):
        P.add('snare', b + q * S + LAY, DRUM_LEN[SNARE], SNARE, 112)
    for q in range(4):
        if i == 0 and q == 0:
            continue                                         # crash op 1 van de strofe
        if cym == 'hat':
            if i % 4 == 3 and q == 3:
                P.add('cym', b + q * TPB, DRUM_LEN[OHH], OHH, 90)            # open hihat óp tel 4
            else:
                P.add('cym', b + q * TPB, DRUM_LEN[HHALF], HHALF, 82 if q % 2 == 0 else 70)
        else:
            P.add('cym', b + q * TPB, DRUM_LEN[RIDE], BELL if q == 0 else RIDE, 84 if q % 2 == 0 else 72)
    if i == 0:
        P.add('cym', b, DRUM_LEN[CRASH], CRASH, 108)


def chorus_drums(P, bar, pattern, i, cym='hat'):
    """Refrein: halftempo, snare op tel 3, kick op de akkoorden van de riff, crash/china om de 2 maten, open hihat
    of ride op de tellen (gruizig, lang)."""
    b = bar * BAR
    kicks = sorted({st for st, ln, kind, nm in pattern if kind != 'M'} - {8})
    for k in kicks:
        P.add('kick', b + k * S, DRUM_LEN[KICK], KICK, 127 if k == 0 else 114)
    if pattern is RIFF_STOP:
        P.add('cym', b, DRUM_LEN[CHINA], CHINA, 116)
        return
    P.add('snare', b + 8 * S + LAY, DRUM_LEN[SNARE], SNARE, 127)
    if i % 2 == 0:
        P.add('cym', b, DRUM_LEN[CRASH], CRASH if i % 4 == 0 else CHINA, 108)
    for q in range(4):
        if i % 2 == 0 and q == 0:
            continue
        if cym == 'hat':
            P.add('cym', b + q * TPB, DRUM_LEN[OHH], OHH, 84 if q % 2 == 0 else 72)
        else:
            P.add('cym', b + q * TPB, DRUM_LEN[RIDE], RIDE, 86 if q % 2 == 0 else 76)


def fill(P, bar, start16=8, step=2):
    """Trage tomfill (snare + floor tom in 8en) naar de crash van de volgende maat; vervangt de groove."""
    b = bar * BAR
    for k in ('cym', 'snare', 'kick'):
        P.n[k] = [x for x in P.n[k] if not (b + start16 * S <= x[0] < b + BAR)]
    seq = list(range(start16, 16, step))
    for j, st in enumerate(seq):
        nt = (SNARE, FTOM, MTOM, FTOM)[j % 4] if j < len(seq) - 1 else SNARE
        P.add('snare' if nt == SNARE else 'tom', b + st * S, E, nt, 98 + j * 5)
        if nt != SNARE:
            P.add('kick', b + st * S, DRUM_LEN[KICK], KICK, 100)


def chorus(P, bar0, cym='hat', lead_phrases=None):
    for i, pat in enumerate(CHORUS):
        b = bar0 + i
        if pat is RIFF_STOP:
            riff(P, b, pat, bass=False)
            for st, ln, nm in STOP_BASS:
                P.add('bass', b * BAR + st * S, ln * S, bass_note(p(nm)), 120)
        else:
            riff(P, b, pat)
        chorus_drums(P, b, pat, i, cym)
        if lead_phrases:
            lead(P, b, lead_phrases[i], 116)
    fill(P, bar0 + 6, 8)                                     # de turnaround rolt naar de stop


def stop_feedback(P, bar, note='C5'):
    """Na de stop: de versterker blijft huilen (feedback) zolang het akkoord hangt."""
    s = bar * BAR
    P.add('fb', s + S * 2, 10 * S, p(note), 110)
    for j in range(9):
        P.fx['fb'].append((s + S * 2 + j * S, 'vol', int(30 + 70 * j / 8)))
    P.fx['fb'] += [(s + S * 2, 'mod', 0), (s + S * 6, 'mod', 10)]


def verse(P, bar0, bass_bars, cym, mute_from, sides_from):
    for i in range(8):
        b = bar0 + i
        for st, ln, nm in bass_bars[i]:
            P.add('bass', b * BAR + st * S, ln * S, bass_note(p(nm)), 112 + (10 if st in (0, 8) else 0))
        verse_drums(P, b, i, cym)
        if i >= mute_from and i < 7:
            pat = CHORUS[(i - mute_from) % 6]
            palm_mute(P, b, pat, ('L', 'R') if i >= sides_from else ('L',), 96 + (6 if i >= 4 else 0))
        elif i == 7:
            palm_mute(P, b, RIFF_TURN, ('L', 'R') if i >= sides_from else ('L',), 104)
    fill(P, bar0 + 7, 8)


def build():
    P = Parts()
    G = ('pwrL', 'pwrR')

    # ---- intro: zwelling, dan de riff één keer als statement ----------------------------------------------------
    P.add('pwrL', 0, 2 * BAR - S, p('C2'), 112)
    P.add('pwrR', 0, 2 * BAR - S, p('C2'), 106)
    for k in range(33):                                     # powerchord zwelt in 2 maten aan
        for sd in G:
            P.fx[sd].append((k * 2 * BAR // 32, 'vol', int(((k / 32) ** 1.6) * 100)))
    P.add('fb', BAR // 2, BAR + BAR // 2 - S, p('G4'), 110)      # hoge feedbacktoon zwelt mee
    for k in range(25):
        P.fx['fb'].append((BAR // 2 + k * (BAR + BAR // 2) // 24, 'vol', int(((k / 24) ** 1.3) * 100)))
    P.fx['fb'] += [(BAR, 'mod', 4), (BAR + BAR // 2, 'mod', 10)]
    for k in range(8):                                      # lava-rommel: floor tom in 8en die aanzwelt
        P.add('tom', BAR + k * E, E, FTOM, 60 + k * 8)
    P.vol(G + ('bass',), INTRO_RIFF, 100)
    for i, pat in enumerate((RIFF_A1, RIFF_A2, RIFF_STOP)):
        b = INTRO_RIFF + i
        if pat is RIFF_STOP:
            riff(P, b, pat, bass=False)
            for st, ln, nm in STOP_BASS:
                P.add('bass', b * BAR + st * S, ln * S, bass_note(p(nm)), 120)
        else:
            riff(P, b, pat)
        chorus_drums(P, b, pat, i)
    stop_feedback(P, STOP0)

    # ---- V1: alleen bas + drums; vanaf maat 9 zacht de palm-muted refreinriff links ------------------------------
    P.vol(('bass',), V1, 100)
    P.vol(('muteL', 'muteR'), V1, 92)
    P.fx['drums'].append((V1 * BAR, 'vol', 86))
    verse(P, V1, VERSE_BASS, 'hat', 4, 99)

    # ---- R1: het refrein -----------------------------------------------------------------------------------------
    P.vol(G, R1, 100)
    P.vol(('bass',), R1, 94)
    P.vol(('muteL', 'muteR'), R1, 100)
    P.fx['drums'].append((R1 * BAR, 'vol', 100))
    chorus(P, R1)
    stop_feedback(P, R1 + 7)

    # ---- V2: bas (octaafsprong) + drums (ride), palm-muted riff links en rechts -------------------------------------
    P.vol(('bass',), V2, 100)
    P.vol(('muteL', 'muteR'), V2, 96)
    P.fx['drums'].append((V2 * BAR, 'vol', 88))
    verse(P, V2, VERSE2_BASS, 'ride', 2, 4)

    # ---- R2: refrein + de leadgitaar zingt -----------------------------------------------------------------------
    P.vol(('bass',), R2, 94)
    P.vol(('muteL', 'muteR'), R2, 100)
    P.fx['drums'].append((R2 * BAR, 'vol', 100))
    chorus(P, R2, 'ride', SING)

    # ---- M: middenstuk, bas + getokkelde warme gitaar; 41-44 opbouw -----------------------------------------------
    P.vol(('bass',), M, 78)
    P.vol(('clean',), M, 100)
    P.fx['drums'].append((M * BAR, 'vol', 62))
    for i in range(8):
        b = M + i
        for e, nm in enumerate(ARP[i]):
            P.add('clean', b * BAR + e * E, 3 * E, p(nm), 104 + (12 if e == 0 else 0) + (6 if i >= 4 else 0))
        for st, ln, nm in MID_BASS[i]:
            P.add('bass', b * BAR + st * S, ln * S, bass_note(p(nm)), 108 + (10 if st == 0 else 0))
        bb = b * BAR
        if i == 4:
            P.vol(('bass',), b, 88)
            P.fx['drums'].append((bb, 'vol', 76))
        if i == 6:
            P.vol(('bass',), b, 96)
            P.fx['drums'].append((bb, 'vol', 90))
        if i < 4:                                           # ruimte: ride zacht op de tellen, kick op 1
            P.add('kick', bb, DRUM_LEN[KICK], KICK, 92)
            for q in range(4):
                P.add('cym', bb + q * TPB, DRUM_LEN[RIDE], RIDE, 64 if q else 76)
        elif i < 6:                                         # hartslag: floor tom op 1 en 3, sidestick op 2 en 4
            for q in range(4):
                P.add('cym', bb + q * TPB, DRUM_LEN[RIDE], RIDE, 72 if q else 84)
                if q % 2 == 0:
                    P.add('tom', bb + q * TPB, DRUM_LEN[FTOM], FTOM, 92)
                    P.add('kick', bb + q * TPB, DRUM_LEN[KICK], KICK, 96)
                else:
                    P.add('snare', bb + q * TPB + LAY, S, STICK, 92)
        else:                                               # floor tom in 8en die aanzwelt, kick op de tellen
            for e in range(8):
                P.add('tom', bb + e * E, E, FTOM, 80 + (i - 6) * 22 + e * 3)
            for q in range(4):
                P.add('kick', bb + q * TPB, DRUM_LEN[KICK], KICK, 100 + (i - 6) * 14)
    for k in range(4):                                      # snareroffel in 16en over tel 4 van de laatste maat
        P.add('snare', (R3 - 1) * BAR + (12 + k) * S, S, SNARE, 96 + k * 8)
    s = (M + 6) * BAR                                       # feedback zwelt aan over de laatste 2 maten
    P.add('fb', s, 2 * BAR - S, p('G4'), 110)
    for j in range(33):
        P.fx['fb'].append((s + j * 2 * BAR // 32, 'vol', int(((j / 32) ** 1.4) * 100)))
    P.fx['fb'] += [(s, 'mod', 0), (s + BAR, 'mod', 8)]
    P.add('pwrL', (M + 7) * BAR, BAR - S, p('G2'), 104)      # de powerchord G zwelt al mee
    for j in range(17):
        P.fx['pwrL'].append(((M + 7) * BAR + j * BAR // 16, 'vol', int(((j / 16) ** 2) * 90)))

    # ---- R3: refrein + solo --------------------------------------------------------------------------------------
    P.vol(G, R3, 100)
    P.vol(('bass',), R3, 94)
    P.fx['drums'].append((R3 * BAR, 'vol', 100))
    chorus(P, R3, 'hat', SOLO)
    P.fx['drums'].append((END * BAR - BAR, 'vol', 100))
    # de stop aan het eind van de loop = de stop van de intro (maat 4): naadloos terug naar de strofe

    for k in P.n:
        P.n[k] = dedupe(P.n[k])
    return P


def write_voicegroup():
    """grounded_gm + 27 warme schone gitaar, 28 palm-mute, 30 fuzz-powerchord, 31 fuzz-lead,
    34 SVT-fuzzbas, 127 stoner-drumkit."""
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Battle! Heatran (stoner rock). Gegenereerd door tools/grounded/heatran_theme.py.'
    lines[1] = ('@ 27 = warme schone gitaar, 28 = palm-mute-powerchord, 30 = fuzz-powerchord '
                '(1 sample = 1 kanaal), 31 = fuzz-lead, 34 = SVT-fuzzbas, 127 = drumkit.')
    lines[2] = 'voice_group %s' % VG
    repl = {
        '@ 27': '\tvoice_directsound 48, 0, DirectSoundWaveData_heatran_warm_clean, 255, 0, 255, 200  @ 27',
        '@ 28': '\tvoice_directsound 60, 0, DirectSoundWaveData_heatran_doom_mute, 255, 0, 255, 140  @ 28',
        '@ 30': '\tvoice_directsound 60, 0, DirectSoundWaveData_heatran_doom_power, 255, 0, 255, 185  @ 30',
        '@ 31': '\tvoice_directsound 60, 0, DirectSoundWaveData_heatran_doom_lead, 255, 0, 255, 200  @ 31',
        '@ 34': '\tvoice_directsound 60, 0, DirectSoundWaveData_heatran_svt_bass, 255, 0, 255, 170  @ 34',
        '@ 127': '\tvoice_keysplit_all voicegroup_heatran_drumset  @ 127',
    }
    out = []
    for l in lines:
        tag = '@' + l.rsplit('@', 1)[1] if '@' in l and l.startswith('\t') else None
        out.append(repl.get(tag.strip() if tag else None, l))
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    kit = [   # vanaf noot 36; alles DirectSound
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_heatran_kick, 255, 0, 255, %d' % DRUM_REL[KICK],
        'voice_directsound_no_resample 60, 62, DirectSoundWaveData_heatran_snare, 255, 0, 255, %d' % DRUM_REL[SNARE],
        'voice_directsound_no_resample 60, 80, DirectSoundWaveData_heatran_open_hat, 255, 0, 255, %d' % DRUM_REL[OHH],
        'voice_directsound_no_resample 60, 44, DirectSoundWaveData_heatran_ride, 255, 0, 255, %d' % DRUM_REL[RIDE],
        'voice_directsound 60, 40, DirectSoundWaveData_heatran_floor_tom, 255, 0, 255, %d' % DRUM_REL[FTOM],
        'voice_directsound 65, 76, DirectSoundWaveData_heatran_floor_tom, 255, 0, 255, %d' % DRUM_REL[MTOM],
        'voice_directsound_no_resample 60, 36, DirectSoundWaveData_heatran_crash, 255, 0, 255, %d' % DRUM_REL[CRASH],
        'voice_directsound_no_resample 60, 92, DirectSoundWaveData_heatran_china, 255, 0, 255, %d' % DRUM_REL[CHINA],
        'voice_directsound_no_resample 60, 56, DirectSoundWaveData_heatran_side_stick, 255, 0, 255, %d' % DRUM_REL[STICK],
        'voice_directsound 66, 40, DirectSoundWaveData_heatran_ride, 255, 0, 255, %d' % DRUM_REL[BELL],
        'voice_directsound_no_resample 60, 70, DirectSoundWaveData_heatran_open_hat, 255, 0, 255, %d' % DRUM_REL[HHALF],
    ]
    open('sound/voicegroups/drumsets/heatran.inc', 'w').write(
        '@ Project Grounded: stoner-drumkit voor Battle! Heatran (heatran_theme.py), FluidR3 Power-kit (heatran_samples.py):\n'
        '@ 36 kick, 37 snare, 38 open hihat, 39 ride, 40 floor tom, 41 middentom, 42 crash, 43 china,\n'
        '@ 44 sidestick, 45 ride hoger (bel), 46 halfopen hihat (kort, open-hihatsample afgekapt).\n'
        'voice_group heatran_drumset, 36\n' + ''.join('\t%s\n' % k for k in kit) + '\n')


def fx_events(fx, notes, base=0):
    """bend/mod terugzetten op het begin van de volgende noot (niet bij de note-off: dan zakt de uitklinktijd).
    base = vaste bend van het spoor (rechter gitaar); bends komen erbovenop."""
    starts = sorted(set(n[0] for n in notes))
    ev = [x for x in fx if x[1] == 'vol']
    pm = [x for x in fx if x[1] != 'vol']
    pm_ticks = {(t, k) for t, k, v in pm}
    for t, kind, v in pm:
        ev.append((t, kind, v + (base if kind == 'bend' else 0)))
        nxt = next((s for s in starts if s > t), None)
        if nxt is not None and (nxt, kind) not in pm_ticks:
            ev.append((nxt, kind, base if kind == 'bend' else 0))
    best = {}
    for t, kind, v in ev:
        if kind == 'vol' or (t, kind) not in best or (t, kind) in pm_ticks:
            if (t, kind) in pm_ticks and (t, kind) in best and kind != 'vol':
                if v == (base if kind == 'bend' else 0):
                    continue                                 # een reset wint niet van een eigen waarde
            best[(t, kind)] = v
    return [(t, k, v) for (t, k), v in best.items()]


def save(P, path):
    out = mido.MidiFile(type=1, ticks_per_beat=TPB)
    cond = mido.MidiTrack()
    cond.append(mido.MetaMessage('set_tempo', tempo=int(60e6 / BPM), time=0))
    cond.append(mido.MetaMessage('marker', text='[', time=V1 * BAR))
    cond.append(mido.MetaMessage('marker', text=']', time=(END - V1) * BAR))
    out.tracks.append(cond)
    layout = [  # naam, programma, volume (100%), kanaal, pan, vaste bend
        ('pwrL', POWER, 100, 0, 24, 0),
        ('pwrR', POWER, 96, 1, 104, R_BEND),
        ('muteL', MUTE, 84, 4, 34, 0),
        ('muteR', MUTE, 80, 5, 94, R_BEND),
        ('clean', CLEAN, 66, 6, 76, 0),
        ('bass', BASS, 84, 7, 64, 0),
        ('lead', LEAD, 100, 8, 74, 0),
        ('fb', LEAD, 84, 10, 50, 0),
    ]
    for name, prog, vol, ch, pan, bend in layout:
        fx = fx_events(P.fx[name], P.n[name], bend)
        if bend:
            fx = [(0, 'bend', bend)] + [x for x in fx if not (x[0] == 0 and x[1] == 'bend')]
        add_track(out, P.n[name], prog, vol, ch, pan, fx)
    drums = ('kick', 'snare', 'cym', 'tom')
    add_track(out, sorted(sum((P.n[k] for k in drums), [])), DRUMS, 118, 9, 64, P.fx['drums'])
    written = {k for k, *_ in layout} | set(drums)
    assert not [k for k in P.n if P.n[k] and k not in written], 'partij niet weggeschreven'
    out.save(path)


def add_track(out, notes, prog, vol, ch, pan, fx):
    t = mido.MidiTrack()
    t.append(mido.Message('program_change', channel=ch, program=prog, time=0))
    t.append(mido.Message('control_change', channel=ch, control=7, value=vol, time=0))
    t.append(mido.Message('control_change', channel=ch, control=10, value=pan, time=0))
    ev = []
    for tk, kind, v in fx:     # volgorde op één tick: note-off, controllers, note-on
        if kind == 'vol':
            ev.append((tk, 1, mido.Message('control_change', channel=ch, control=7, value=max(0, min(127, v * vol // 100)))))
        elif kind == 'mod':
            ev.append((tk, 1, mido.Message('control_change', channel=ch, control=1, value=v)))
        elif kind == 'bend':
            ev.append((tk, 1, mido.Message('pitchwheel', channel=ch, pitch=max(-8192, min(8191, v)))))
    for s, e, n, v in notes:
        ev.append((e, 0, mido.Message('note_off', channel=ch, note=n, velocity=0)))
        ev.append((s, 2, mido.Message('note_on', channel=ch, note=n, velocity=max(1, min(127, int(v))))))
    last = 0
    for tk, _, m in sorted(ev, key=lambda x: (x[0], x[1])):
        t.append(m.copy(time=tk - last))
        last = tk
    out.tracks.append(t)


def main():
    P = build()
    write_voicegroup()
    rel = releases(VG)
    progs = {'pwrL': POWER, 'pwrR': POWER, 'muteL': MUTE, 'muteR': MUTE, 'clean': CLEAN, 'bass': BASS,
             'lead': LEAD, 'fb': LEAD}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) for k, pr in progs.items()}
    tail['kick'] = tail['snare'] = tail['tom'] = 0
    tail['cym'] = release_ticks(DRUM_REL[CRASH], TPB, BPM)
    for k in ('bass', 'lead', 'fb', 'muteL', 'muteR', 'pwrL', 'pwrR'):         # de getokkelde gitaar mag doorklinken
        P.n[k] = detach(P.n[k], tail[k])
    # zelfde toonhoogte mag in één spoor niet overlappen (de note-off van de eerste zou de tweede afkappen)
    for k in P.n:
        ns = sorted(P.n[k])
        for i, x in enumerate(ns):
            nxt = next((y[0] for y in ns[i + 1:] if y[2] == x[2] and y[0] >= x[0]), None)
            if nxt is not None and nxt < x[1]:
                x[1] = max(x[0] + 6, nxt - 1)
        P.n[k] = ns
    order = ['lead', 'pwrL', 'bass', 'kick', 'snare', 'clean', 'muteL', 'cym', 'fb', 'tom', 'pwrR', 'muteR']
    kept = allocate({k: P.n[k] for k in order}, order, tail, max_voices=11)
    print('tail (ticks):', tail)
    for k in order:
        n = len(P.n[k])
        print('  %-6s %4d noten, %3d vallen weg (%.1f%%)' % (k, n, n - len(kept[k]), 100 * (n - len(kept[k])) / max(n, 1)))
        P.n[k] = kept[k]
    save(P, OUT)
    spb = 4 * 60 / BPM
    print(OUT, '%.1f s intro, %.1f s loop' % (V1 * spb, (END - V1) * spb))
    for nm, a, b in (('intro', 0, V1), ('V1', V1, R1), ('R1', R1, V2), ('V2', V2, R2), ('R2', R2, M), ('M', M, R3),
                     ('R3', R3, END)):
        print('  %-5s maat %2d-%2d  %6.1f - %6.1f s' % (nm, a, b - 1, a * spb, b * spb))


if __name__ == '__main__':
    main()
