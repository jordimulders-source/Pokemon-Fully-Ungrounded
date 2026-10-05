#!/usr/bin/env python3
"""Project Grounded: "Battle! SickBlik" (TRAINER_OWEN, Cooltrainer op Victory Road B2F en in het Battle Stadium =
Jordi zelf). Eigen compositie: extreem funky, smerige slap bass ('stank face'), à la Vulfpeck 'Dean Town', Victor
Wooten, Marcus Miller, Louis Cole, Jamiroquai. De bas is de ster en draagt de hook.

108 bpm, E-dorisch (Em7 - A7-vamp) met blue notes (Bb, de b5) en chromatische tussennoten.
  maat 0-1   intro: bas solo, de 'stank face'-lick; in maat 1 een hihat en een snarepickup
Loop (maat 2-33, 32 maten = 71 s):
  A1  2-9    groove: slap bass (thumb op de lage noten, pops op de octaven, ghost/dead notes, hammer-ons,
             slides), funkdrums (16e-hihat, ghost notes op de snare), wah-chanks + scratches op de gitaar;
             vanaf maat 6 clavinet en hoornstoten
  H1 10-17   de hook: een 'Dean Town'-achtige unisono-riff (bas + hoorns twee octaven hoger + gedempte gitaar
             een octaaf hoger), drums vol, crash om de 2 maten; maat 17 eindigt met een stop en een basfill
  B  18-23   breakdown: alleen bas + drums (bassolo: double thumbing in sextolen, dead notes in 32en, double-stop-
             pops, blues-loopjes); 22 = stop-time (hits van de band, de bas vult de gaten), 23 = opbouw
  A2 24-29   groove met talkbox-lead (melodie), Rhodes-akkoorden, hoornstoten, wah-chanks
  H2 30-33   de hook met handclap en clavinet erbij; de laatste maat eindigt met dezelfde octaafloop als de intro
             (maat 1), dus de terugsprong naar maat 2 is naadloos
Articulaties van de bas = aparte programma's met eigen samples (tools/grounded/sickblik_samples.py): thumb, pop,
dode thumb, dode pop. Hammer-on = dezelfde noot klinkt door en de pitch bend springt (geen nieuwe aanslag); slide =
noot begint 2 halve tonen lager en buigt omhoog. De baslijn is één snaar: elke noot stopt als de volgende begint.
Gebruikt musiclib.py; zie MUZIEK.md. Gebruik: python3 tools/grounded/sickblik_theme.py"""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, allocate, releases, release_ticks

OUT = 'sound/songs/midi/mus_grounded_vs_sickblik.mid'
VG = 'grounded_sickblik'
TPB, BPM = 96, 108
S = TPB // 4                   # een 16e
BAR = TPB * 4

# programma's in de voicegroup (zie write_voicegroup)
RH_M9, RH_13, CLAV, GW_9, GW_M9, GSCR, GMUTE = 4, 5, 7, 26, 27, 28, 29
THUMB, POP, DEADT, DEADP = 34, 35, 36, 37
HORNS, HORNS_HI, TALK, DRUMS = 61, 62, 85, 127
REL = {RH_M9: 200, RH_13: 200, CLAV: 140, GW_9: 150, GW_M9: 150, GSCR: 120, GMUTE: 140, THUMB: 150, POP: 150,
       DEADT: 100, DEADP: 100, HORNS: 160, HORNS_HI: 160, TALK: 185}

# eigen drumkit (drumsets/sickblik.inc, vanaf noot 36)
KICK, SNARE, CHH, OHH, PHH, CRASH, CLAP, STICK, TOMH, TOML = range(36, 46)
DRUM_REL = {KICK: 0, SNARE: 0, CHH: 0, OHH: 190, PHH: 0, CRASH: 220, CLAP: 0, STICK: 0, TOMH: 0, TOML: 0}
DRUM_LEN = {KICK: TPB // 2, SNARE: TPB // 2, CHH: S - 4, OHH: TPB // 2 - 8, PHH: S, CRASH: TPB * 2, CLAP: TPB // 3,
            STICK: S, TOMH: S + S // 2, TOML: TPB // 2}

INTRO, A1, H1, BRK, STOPT, BUILD, A2, H2, END = 0, 2, 10, 18, 22, 23, 24, 30, 34

N = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
     'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def p(name):
    """'E1' -> midi-noot (C4 = 60, E1 = 28 = laagste noot die mag)."""
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


# ---- de bas: (16e (mag een breuk zijn), lengte in 16en, noot, articulatie) ------------------------------------------
# T = thumb (slap), P = pop, X = dode thumb (ghost), Y = dode pop, H = hammer-on (de vorige noot klinkt door en buigt
# naar deze toon), een 's' erachter = slide (begint 2 halve tonen lager)
INTRO0 = [(0, 2, 'E1', 'T'), (2, 1, 'E1', 'X'), (3, 1, 'E2', 'P'), (4, 1, 'E1', 'X'), (5, 1, 'E1', 'T'),
          (6, 1, 'G1', 'Ts'), (7, 1, 'E1', 'X'), (8, 1, 'A1', 'T'), (9, 1, 'B1', 'H'), (10, 1, 'A2', 'P'),
          (11, 1, 'E1', 'X'), (12, 1, 'D2', 'T'), (13, 1, 'D3', 'P'), (14, 1, 'Bb1', 'T'), (15, 1, 'B1', 'T')]
OCT_RUN = [(10, 1, 'G1', 'T'), (11, 1, 'G2', 'P'), (12, 1, 'A1', 'T'), (13, 1, 'A2', 'P'), (14, 1, 'Bb1', 'T'),
           (15, 1, 'B1', 'T')]                     # octaafloop naar de E: eind van de intro én van de loop
INTRO1 = [(0, 1, 'E1', 'T'), (1, 1, 'E1', 'X'), (2, 1, 'E1', 'X'), (3, 1, 'E2', 'P'), (4, 1, 'E1', 'T'),
          (5, 1, 'G2', 'P'), (6, 1, 'A1', 'T'), (7, 1, 'B1', 'H'), (8, 2, 'D3', 'P')] + OCT_RUN

GA_E = [(0, 2, 'E1', 'T'), (2, 1, 'E1', 'X'), (3, 1, 'E2', 'P'), (4, 1, 'E1', 'X'), (5, 1, 'E1', 'T'),
        (6, 1, 'G1', 'T'), (7, 1, 'G2', 'P'), (8, 1, 'E1', 'X'), (9, 1, 'A1', 'T'), (10, 1, 'B1', 'H'),
        (11, 1, 'D3', 'P'), (12, 1, 'E1', 'T'), (13, 1, 'E1', 'Y'), (14, 1, 'E2', 'P'), (15, 1, 'G#1', 'T')]
GA_A_HEAD = [(0, 2, 'A1', 'T'), (2, 1, 'A1', 'X'), (3, 1, 'A2', 'P'), (4, 1, 'A1', 'X'), (5, 1, 'G1', 'T'),
             (6, 1, 'A1', 'T'), (7, 1, 'G2', 'P')]
GA_A = GA_A_HEAD + [(8, 1, 'A1', 'X'), (9, 1, 'C#2', 'T'), (10, 1, 'D2', 'H'), (11, 1, 'D3', 'P'),
                    (12, 1, 'G1', 'T'), (13, 1, 'G2', 'P'), (14, 1, 'F#1', 'T'), (15, 1, 'F1', 'T')]
GA_E2 = [(0, 1, 'E1', 'T'), (1, 1, 'E1', 'X'), (2, 1, 'E1', 'X'), (3, 1, 'E2', 'P'), (4, 0.5, 'E1', 'X'),
         (4.5, 0.5, 'E1', 'X'), (5, 1, 'E1', 'T'), (6, 1, 'D2', 'T'), (7, 1, 'E2', 'P'), (8, 1, 'E1', 'X'),
         (9, 1, 'G1', 'T'), (10, 1, 'A1', 'H'), (11, 1, 'G2', 'P'), (12, 1, 'E1', 'T'), (13, 1, 'D3', 'P'),
         (14, 1, 'E1', 'X'), (15, 1, 'G#1', 'T')]
GA_A2 = GA_A_HEAD + [(8, 1, 'A1', 'X'), (9, 1, 'A1', 'T'), (10, 1, 'A2', 'P'), (11, 1, 'C3', 'P'),
                     (12, 1, 'C#3', 'P'), (13, 1, 'E2', 'T'), (14, 1, 'Bb1', 'T'), (15, 1, 'B1', 'T')]
GA_PICK = GA_A_HEAD + [(8, 1, 'A1', 'X')] + [(9, 1, 'A1', 'T')] + OCT_RUN          # naar de hook

# ---- de hook (unisono): (16e, lengte, noot in de basligging) --------------------------------------------------------
HOOK_A = [(0, 2, 'E2'), (2, 1, 'E2'), (3, 1, 'G2'), (5, 1, 'A2'), (6, 1, 'Bb2'), (7, 2, 'B2'), (10, 1, 'D3'),
          (11, 1, 'E3'), (12, 1, 'D3'), (13, 1, 'B2'), (14, 1, 'A2'), (15, 1, 'G2')]
HOOK_B = [(0, 2, 'A2'), (2, 1, 'G2'), (3, 1, 'E2'), (5, 1, 'G2'), (7, 1, 'E2'), (8, 1, 'D2'), (9, 2, 'E2'),
          (12, 1, 'G2'), (13, 1, 'F#2'), (14, 1, 'F2'), (15, 1, 'D#2')]
HOOK_C_RUN = [(0, 1, 'E2'), (1, 1, 'G2'), (2, 1, 'A2'), (3, 1, 'Bb2'), (4, 1, 'B2'), (5, 1, 'D3'), (6, 1, 'E3'),
              (7, 1, 'G3'), (8, 2, 'E3')]       # bluesladder omhoog, dan de hit
HOOK_C = HOOK_C_RUN + [(11, 1, 'D3'), (13, 1, 'Bb2'), (14, 1, 'A2'), (15, 1, 'G2')]

# bas in de hook: de eerste E van A een octaaf lager (E1, thumb) met een ghost erachter = meer gewicht
def hook_bass(pat, low_start=True):
    out = []
    for st, ln, nm in pat:
        if low_start and st == 0 and nm == 'E2' and ln >= 2:
            out += [(0, 1, 'E1', 'T'), (1, 1, 'E1', 'X')]
            continue
        out.append((st, ln, nm, 'P' if p(nm) >= p('D3') else 'T'))
    return out


# breakdown: de bassolo
SOLO1 = [(0, 1, 'E1', 'T'), (1, 1, 'E1', 'X'), (2, 1, 'E2', 'P'), (3, 1, 'E1', 'X'), (4, 1, 'E1', 'T'),
         (5, 1, 'E2', 'P'), (6, 1, 'D2', 'T'), (7, 1, 'D3', 'P'), (8, 1, 'E1', 'X'), (9, 1, 'E1', 'X'),
         (10, 1, 'G1', 'T'), (11, 1, 'A1', 'H'), (12, 1, 'G2', 'P'), (13, 1, 'E1', 'X'), (14, 1, 'E2', 'P'),
         (15, 1, 'E1', 'Y')]
_t = 2 / 3                                           # 16e-triool (sextolen per tel): double thumbing
SOLO2 = [(0, _t, 'E1', 'T'), (_t, _t, 'E1', 'X'), (2 * _t, _t, 'E2', 'P'), (2, _t, 'G1', 'T'),
         (2 + _t, _t, 'G1', 'X'), (2 + 2 * _t, _t, 'G2', 'P'),
         (4, _t, 'A1', 'T'), (4 + _t, _t, 'A1', 'X'), (4 + 2 * _t, _t, 'A2', 'P'), (6, _t, 'Bb1', 'T'),
         (6 + _t, _t, 'Bb1', 'X'), (6 + 2 * _t, _t, 'Bb2', 'P'),
         (8, 2, 'B1', 'T'), (10, 1, 'B2', 'P'), (11, 1, 'B1', 'X'), (12, 1, 'D2', 'T'), (13, 1, 'D3', 'P'),
         (14, 1, 'E2', 'T'), (15, 1, 'E3', 'P')]
SOLO3 = [(0, 1, 'E1', 'T'), (1, 1, 'E1', 'X'), (2, 1, 'E1', 'X'), (3, 2, 'G2', 'P'), (3, 2, 'D3', 'P'),   # double stop
         (6, 1, 'E1', 'T'), (7, 1, 'E1', 'X'), (8, 1, 'B1', 'Ts'), (9, 1, 'B2', 'P'), (10, 1, 'E1', 'X'),
         (11, 2, 'A2', 'P'), (11, 2, 'E3', 'P'), (13, 1, 'E1', 'T'), (14, 1, 'E1', 'X'), (15, 1, 'G1', 'T')]
SOLO4 = ([(k / 2, 0.5, 'E1', 'X' if k % 2 == 0 else 'Y') for k in range(8)] +     # 'mitrailleur' in 32en
         [(4, 1, 'E1', 'T'), (5, 1, 'E2', 'P'), (6, 1, 'E1', 'X'), (7, 1, 'E1', 'X'),
          (8, 1, 'E1', 'T'), (9, 1, 'G1', 'T'), (10, 1, 'A1', 'T'), (11, 1, 'Bb1', 'T'), (12, 1, 'B1', 'T'),
          (13, 1, 'D2', 'T'), (14, 1, 'E2', 'P'), (15, 1, 'G2', 'P')])
STOP_BASS = [(0, 1, 'E1', 'T'), (2, 1, 'E1', 'T'), (3, 1, 'E2', 'P'), (4, 1, 'G1', 'T'), (5, 1, 'G2', 'P'),
             (7, 1, 'E1', 'T'), (9, 1, 'A1', 'T'), (10, 1, 'A2', 'P'), (11, 1, 'Bb1', 'T'), (12, 1, 'Bb2', 'P'),
             (13, 1, 'B1', 'T'), (14, 1, 'B2', 'P'), (15, 1, 'D3', 'P')]

# talkbox-melodie in A2 (16e, lengte, noot, fx): s = slide erin, v = vibrato
TALKBOX = [
    [(2, 2, 'B4', ''), (4, 1, 'D5', ''), (5, 3, 'E5', 's'), (10, 2, 'D5', ''), (12, 4, 'B4', 'v')],
    [(0, 2, 'A4', ''), (2, 2, 'G4', ''), (4, 4, 'A4', 'v'), (10, 1, 'G4', ''), (11, 1, 'E4', ''), (12, 4, 'G4', 's')],
    [(2, 2, 'B4', ''), (4, 1, 'D5', ''), (5, 3, 'E5', 's'), (8, 2, 'G5', ''), (10, 2, 'E5', ''), (12, 2, 'D5', ''),
     (14, 2, 'B4', '')],
    [(0, 6, 'C#5', 'sv'), (6, 2, 'B4', ''), (8, 8, 'A4', 'v')],
    [(2, 2, 'E5', ''), (4, 2, 'G5', ''), (6, 2, 'E5', ''), (8, 2, 'D5', ''), (10, 2, 'B4', ''), (12, 4, 'D5', 's')],
    [(0, 4, 'E5', 'v'), (4, 2, 'D5', ''), (6, 2, 'B4', ''), (8, 4, 'A4', '')],
]

# hoornstoten (16e, lengte, noot) per maat: Em en A7
HORN_E = [(10, 1, 'B4'), (11, 1, 'D5'), (13, 2, 'E5')]
HORN_A = [(3, 1, 'C#5'), (6, 2, 'D5'), (14, 1, 'B4'), (15, 1, 'D5')]
# clavinet (16e, noot), 16e-lengte
CLAV_E = [(1, 'B3'), (2, 'D4'), (4, 'E4'), (6, 'D4'), (7, 'E4'), (9, 'G4'), (10, 'E4'), (12, 'D4'), (14, 'B3'),
          (15, 'D4')]
CLAV_A = [(1, 'C#4'), (2, 'E4'), (4, 'G4'), (6, 'E4'), (7, 'G4'), (9, 'A4'), (10, 'G4'), (12, 'E4'), (14, 'C#4'),
          (15, 'E4')]
GTR_CHORDS = (2, 6, 10, 13)            # wah-chanks; de andere 16en (behalve waar de snare zit) scratches


class Parts:
    def __init__(self):
        self.n = {k: [] for k in ('thumb', 'pop', 'deadT', 'deadP', 'gtrW', 'gtrS', 'gtrM', 'clav', 'rhodes',
                                  'hornLo', 'hornHi', 'talk', 'kick', 'snare', 'hat', 'ohat', 'crash', 'clap', 'tom')}
        self.fx = {k: [] for k in self.n}     # (tick, 'bend'|'mod'|'vol', waarde)
        self.prog = {}                        # (spoor, start, noot) -> programma (sporen die wisselen)

    def add(self, part, start, length, note, vel, prog=None):
        s = int(round(start))
        self.n[part].append([s, int(round(start + length)), note, vel])
        if prog is not None:
            self.prog[(part, s, note)] = prog


ART = {'T': 'thumb', 'P': 'pop', 'X': 'deadT', 'Y': 'deadP'}
VEL = {'T': 118, 'P': 116, 'X': 92, 'Y': 84}


def bass_line(P, bar, pat, accent=(0, 8)):
    """Eén snaar: voeg de noten toe; H = hammer-on (vorige noot langer + bend), s = slide."""
    b = bar * BAR
    last = None
    for st, ln, nm, art in sorted(pat, key=lambda x: x[0]):
        s, n = b + st * S, p(nm)
        if art == 'H':
            if last is None:
                continue
            part, note = last
            note[1] = int(round(s + ln * S))
            step = n - note[2]
            P.fx[part].append((s, 'bend', 8191 if step >= 2 else int(4096 * step)))
            continue
        kind = art[0]
        part = ART[kind]
        vel = VEL[kind] + (8 if st in accent and kind in 'TP' else 0)
        if kind in 'XY':
            P.add(part, s, max(6, min(ln * S, S // 2)), n, vel)
        else:
            P.add(part, s, ln * S, n, vel)
        note = P.n[part][-1]
        if 's' in art[1:]:
            for k, v in enumerate((-8192, -5461, -2731, 0)):
                P.fx[part].append((s + k * 3, 'bend', v))
        last = (part, note)


def line(P, part, bar, pat, shift, vel, prog_fn=None, length_scale=1.0):
    for st, ln, nm in pat:
        n = p(nm) + shift
        pr = prog_fn(n) if prog_fn else None
        P.add(part, bar * BAR + st * S, max(S // 2, ln * S * length_scale), n, vel + (8 if st in (0, 8) else 0), pr)


def horns(P, bar, pat, shift=0, vel=112, stab=True):
    """Hoorns: trompet + tenorsax een octaaf lager in één sample; vanaf C5 de hoge sample (minder transponeren)."""
    for st, ln, nm in pat:
        n = p(nm) + shift
        part = 'hornHi' if n >= 72 else 'hornLo'
        L = ln * S - (6 if stab else 2)
        P.add(part, bar * BAR + st * S, max(10, L), n, vel + (8 if st in (0, 8) else 0))


def groove_drums(P, bar, i, open_hat=True, hats=True):
    b = bar * BAR
    kicks = (0, 3, 10) if i % 2 == 0 else (0, 7, 10, 13)
    for k in kicks:
        P.add('kick', b + k * S, DRUM_LEN[KICK], KICK, 118 if k == 0 else 104)
    for q in (4, 12):
        P.add('snare', b + q * S + 2, DRUM_LEN[SNARE], SNARE, 116)
    ghosts = (7, 9, 15) if i % 2 == 0 else (6, 9, 11, 14)
    for g in ghosts:
        P.add('snare', b + g * S + 2, S // 2, SNARE, 40 + (g % 3) * 4)
    if hats:
        for k in range(16):
            if open_hat and i % 2 == 1 and k == 14:
                P.add('ohat', b + k * S, DRUM_LEN[OHH], OHH, 84)
            elif open_hat and i % 2 == 1 and k == 15:
                continue
            else:
                P.add('hat', b + k * S, DRUM_LEN[CHH], CHH, 92 if k % 4 == 0 else (80 if k % 2 == 0 else 58))


def hook_drums(P, bar, i, pat, clap=False):
    """Hook: kick op de accenten van de riff, snare 2 en 4 (+ clap in H2), 16e-hihat, crash om de 2 maten."""
    b = bar * BAR
    acc = {st for st, ln, nm in pat if ln >= 2 or st in (0, 3, 7, 11)}
    for k in sorted(acc | {0}):
        if k not in (4, 12):
            P.add('kick', b + k * S, DRUM_LEN[KICK], KICK, 120 if k == 0 else 108)
    for q in (4, 12):
        P.add('snare', b + q * S, DRUM_LEN[SNARE], SNARE, 122)
        if clap:
            P.add('clap', b + q * S, DRUM_LEN[CLAP], CLAP, 104)
    for g in (9, 14):
        P.add('snare', b + g * S, S // 2, SNARE, 46)
    if i % 2 == 0:
        P.add('crash', b, DRUM_LEN[CRASH], CRASH, 112)
    for k in range(0, 16, 2 if clap else 1):                # H2: hihat in 8en (ruimte voor clap + clavinet)
        if i % 2 == 0 and k == 0:
            continue
        P.add('hat', b + k * S, DRUM_LEN[CHH], CHH, 96 if k % 4 == 0 else (82 if k % 2 == 0 else 62))


def fill(P, bar, start16=12, toms=True):
    """Snare/tom-fill in 16en tot het eind van de maat (vervangt de groove vanaf start16)."""
    b = bar * BAR
    for k in ('hat', 'ohat', 'snare', 'kick', 'clap'):
        P.n[k] = [x for x in P.n[k] if not (b + start16 * S <= x[0] < b + BAR)]
    seq = ([SNARE, SNARE, TOMH, TOMH, TOML, TOML, SNARE, SNARE] if toms else [SNARE] * 8)[-(16 - start16):]
    for j, nt in enumerate(seq):
        part = 'snare' if nt == SNARE else 'tom'
        P.add(part, b + (start16 + j) * S, DRUM_LEN[nt] if part == 'tom' else S, nt, 84 + j * 6)


def guitar(P, bar, chord, vel=104):
    """Wah-chanks op GTR_CHORDS, scratches op de overige oneven 16en (niet onder de snare)."""
    b = bar * BAR
    prog, root = (GW_M9, p('E3')) if chord == 'E' else (GW_9, p('A3'))   # A9 = de E9-greep een kwart hoger
    for k in range(16):
        if k in GTR_CHORDS:
            P.add('gtrW', b + k * S, S, root, vel + (6 if k == 2 else 0), prog)
        elif k % 2 == 1 and k not in (5, 13):
            P.add('gtrS', b + k * S, S // 2, p('E3'), 66 + (k % 4) * 3)


def clav(P, bar, chord, vel=100):
    for st, nm in (CLAV_E if chord == 'E' else CLAV_A):
        P.add('clav', bar * BAR + st * S, S - 4, p(nm), vel + (10 if st in (2, 10) else 0))


def rhodes(P, bar, chord, vel=96):
    b = bar * BAR
    prog, n = (RH_M9, p('E3')) if chord == 'E' else (RH_13, p('A3'))
    P.add('rhodes', b, 5 * S, n, vel + 8, prog)
    P.add('rhodes', b + 7 * S, 3 * S, n, vel, prog)
    P.add('rhodes', b + 12 * S, 2 * S, n, vel - 6, prog)


def talkbox(P, bar, phrase, vel=112):
    for st, ln, nm, fx in phrase:
        s = bar * BAR + st * S
        P.add('talk', s, ln * S - 3, p(nm), vel + (6 if st in (0, 8) else 0))
        if 's' in fx:
            for k, v in enumerate((-8192, -6144, -4096, -2048, 0)):
                P.fx['talk'].append((s + k * 3, 'bend', v))
        if 'v' in fx and ln >= 4:
            P.fx['talk'].append((s + 2 * S, 'mod', 12))


def build():
    P = Parts()
    EA = ('E', 'A')

    # ---- intro: bas solo; maat 1 hihat in 8en + snarepickup ------------------------------------------------------
    bass_line(P, 0, INTRO0)
    bass_line(P, 1, INTRO1)
    for e in range(8):
        P.add('hat', BAR + e * 2 * S, DRUM_LEN[CHH], CHH, 70 if e % 2 else 84)
    P.add('kick', BAR + 8 * S, DRUM_LEN[KICK], KICK, 100)
    fill(P, 1, 12, toms=False)

    # ---- A1: groove; vanaf maat 6 clavinet en hoornstoten ---------------------------------------------------------
    pats = [GA_E, GA_A, GA_E2, GA_A2, GA_E, GA_A, GA_E2, GA_PICK]
    for i, pat in enumerate(pats):
        b = A1 + i
        bass_line(P, b, pat)
        groove_drums(P, b, i)
        guitar(P, b, EA[i % 2])
        if i >= 4:
            clav(P, b, EA[i % 2])
            horns(P, b, HORN_E if i % 2 == 0 else HORN_A)
    P.add('crash', A1 * BAR, DRUM_LEN[CRASH], CRASH, 108)
    fill(P, H1 - 1, 12)

    # ---- H1: de hook -------------------------------------------------------------------------------------------
    hook_pats = [HOOK_A, HOOK_B, HOOK_A, HOOK_C, HOOK_A, HOOK_B, HOOK_A, HOOK_C_RUN]
    for i, pat in enumerate(hook_pats):
        b = H1 + i
        bass_line(P, b, hook_bass(pat))
        horns(P, b, pat, 24, 114, stab=False)
        line(P, 'gtrM', b, pat, 12, 108)
        hook_drums(P, b, i, pat)
    # maat 17: na de hit op tel 3 een stop; de bas vult (sextolen) naar de breakdown
    b = H1 + 7
    bass_line(P, b, [(10, _t, 'E1', 'T'), (10 + _t, _t, 'E1', 'X'), (10 + 2 * _t, _t, 'E2', 'P'),
                     (12, _t, 'G1', 'T'), (12 + _t, _t, 'G1', 'X'), (12 + 2 * _t, _t, 'G2', 'P'),
                     (14, 1, 'Bb1', 'T'), (15, 1, 'B1', 'T')])
    for k in ('hat', 'snare', 'kick'):
        P.n[k] = [x for x in P.n[k] if not (b * BAR + 9 * S <= x[0] < (b + 1) * BAR)]
    P.add('crash', b * BAR + 8 * S, DRUM_LEN[CRASH], CRASH, 118)
    P.add('kick', b * BAR + 8 * S, DRUM_LEN[KICK], KICK, 124)

    # ---- breakdown: bas + drums ----------------------------------------------------------------------------------
    for i, pat in enumerate((SOLO1, SOLO2, SOLO3, SOLO4)):
        b = BRK + i
        bass_line(P, b, pat)
        bb = b * BAR
        for k in (0, 10) if i % 2 == 0 else (0, 6, 10):
            P.add('kick', bb + k * S, DRUM_LEN[KICK], KICK, 112)
        for q in (4, 12):
            P.add('snare', bb + q * S + 2, DRUM_LEN[SNARE], SNARE, 110)
        for g in (3, 7, 9, 14):
            P.add('snare', bb + g * S + 2, S // 2, SNARE, 38 + (g % 2) * 6)
        for e in range(8):
            P.add('hat', bb + e * 2 * S, DRUM_LEN[CHH], CHH, 84 if e % 2 == 0 else 64)
        P.add('hat', bb + 4 * S, DRUM_LEN[PHH], PHH, 70)
    P.add('crash', BRK * BAR, DRUM_LEN[CRASH], CRASH, 104)
    # stop-time: hits op 1 en de '&' van 2, de bas vult de gaten
    bb = STOPT * BAR
    bass_line(P, STOPT, STOP_BASS, accent=(0, 7))
    for st in (0, 7):
        P.add('kick', bb + st * S, DRUM_LEN[KICK], KICK, 124)
        P.add('crash' if st == 0 else 'snare', bb + st * S, DRUM_LEN[CRASH] if st == 0 else DRUM_LEN[SNARE],
              CRASH if st == 0 else SNARE, 120)
        horns(P, STOPT, [(st, 2, 'E5' if st == 0 else 'G5')], 0, 120)
        P.add('gtrW', bb + st * S, S, p('E3'), 116, GW_9)
    for e in range(4):                                     # alleen de pedaalhihat op de tellen
        P.add('hat', bb + e * TPB, DRUM_LEN[PHH], PHH, 76)
    # opbouw: groove op E, snareroffel, hoorns zwellen aan
    bass_line(P, BUILD, GA_E2[:-1] + [(15, 1, 'B1', 'T')])
    groove_drums(P, BUILD, 0, open_hat=False)
    guitar(P, BUILD, 'E', 92)
    fill(P, BUILD, 8, toms=False)
    horns(P, BUILD, [(8, 7, 'B4')], 0, 90, stab=False)
    s = BUILD * BAR + 8 * S
    for j in range(8):
        P.fx['hornLo'].append((s + j * S, 'vol', 45 + j * 8))
    P.fx['hornLo'].append((A2 * BAR, 'vol', 100))

    # ---- A2: groove + talkbox + Rhodes + hoorns ------------------------------------------------------------------
    pats = [GA_E, GA_A, GA_E2, GA_A2, GA_E2, GA_PICK]
    for i, pat in enumerate(pats):
        b = A2 + i
        bass_line(P, b, pat)
        groove_drums(P, b, i)
        guitar(P, b, EA[i % 2], 96)
        rhodes(P, b, EA[i % 2])
        talkbox(P, b, TALKBOX[i])
        if i in (1, 3):
            horns(P, b, HORN_A[2:])                        # alleen het pickupje (de talkbox zingt)
    P.add('crash', A2 * BAR, DRUM_LEN[CRASH], CRASH, 116)
    fill(P, H2 - 1, 12)

    # ---- H2: de hook met clap en clavinet; de laatste maat = octaafloop zoals de intro ----------------------------
    hook2 = [HOOK_A, HOOK_B, HOOK_A, HOOK_C_RUN]
    for i, pat in enumerate(hook2):
        b = H2 + i
        last = i == len(hook2) - 1
        bass_line(P, b, hook_bass(pat) + (OCT_RUN if last else []))
        horns(P, b, pat, 24, 116, stab=False)
        line(P, 'gtrM', b, pat, 12, 110)
        line(P, 'clav', b, pat, 24, 100, length_scale=0.7)
        hook_drums(P, b, i, pat, clap=True)
    b = END - 1
    for k in ('hat', 'snare', 'kick', 'clap'):
        P.n[k] = [x for x in P.n[k] if not (b * BAR + 9 * S <= x[0] < (b + 1) * BAR)]
    P.add('kick', b * BAR + 8 * S, DRUM_LEN[KICK], KICK, 124)
    P.add('crash', b * BAR + 8 * S, DRUM_LEN[CRASH], CRASH, 116)
    fill(P, b, 12, toms=False)                             # dezelfde snarepickup als in de intro (maat 1)

    for k in P.n:
        P.n[k] = dedupe(P.n[k])
    return P


def one_string(P, tails):
    """De bas is één snaar: elke noot (alle articulaties samen) stopt als de volgende begint, maar klinkt minstens
    de helft van de afstand (slap = kort, de ruimte is de funk). Double stops (zelfde start) blijven samen."""
    allb = sorted([(x[0], k, x) for k in ('thumb', 'pop', 'deadT', 'deadP') for x in P.n[k]], key=lambda y: y[0])
    starts = sorted(set(s for s, _, _ in allb))
    for s, k, x in allb:
        nxt = next((t for t in starts if t > s), None)
        if nxt is None:
            continue
        gap = nxt - s
        x[1] = min(x[1], max(s + gap // 2, nxt - tails[k]), nxt)


def write_voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Battle! SickBlik (slap-funk). Gegenereerd door tools/grounded/sickblik_theme.py.'
    lines[1] = ('@ 4/5 = Rhodes Em9/A13, 7 = clavinet, 26/27 = wah-chank A9/Em9, 28 = scratch, 29 = gedempte gitaar, '
                '34-37 = slap bass (thumb, pop, dode thumb, dode pop), 61/62 = hoorns, 85 = talkbox, 127 = drumkit.')
    lines[2] = 'voice_group %s' % VG
    ds = lambda smp, prog: '\tvoice_directsound 60, 0, DirectSoundWaveData_%s, 255, 0, 255, %d  @ %d' % (smp, REL[prog], prog)
    repl = {
        '@ 4': ds('sb_rhodes_m9', RH_M9), '@ 5': ds('sb_rhodes_13', RH_13), '@ 7': ds('sb_clav', CLAV),
        '@ 26': ds('sb_gtr_wah_9', GW_9), '@ 27': ds('sb_gtr_wah_m9', GW_M9), '@ 28': ds('sb_gtr_scratch', GSCR),
        '@ 29': ds('sb_gtr_mute', GMUTE), '@ 34': ds('sb_slap_thumb', THUMB), '@ 35': ds('sb_slap_pop', POP),
        '@ 36': ds('sb_dead_thumb', DEADT), '@ 37': ds('sb_dead_pop', DEADP), '@ 61': ds('sb_horns', HORNS),
        '@ 62': ds('sb_horns_hi', HORNS_HI), '@ 85': ds('sb_talkbox', TALK),
        '@ 127': '\tvoice_keysplit_all voicegroup_sickblik_drumset  @ 127',
    }
    out = []
    for l in lines:
        tag = ('@' + l.rsplit('@', 1)[1]).strip() if '@' in l and l.startswith('\t') else None
        out.append(repl.get(tag, l))
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    kit = [   # vanaf noot 36; alles DirectSound (FluidR3-kit uit heatran_samples.py + sb_pedal_hat/sb_clap)
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_heatran_kick, 255, 0, 255, %d' % DRUM_REL[KICK],
        'voice_directsound_no_resample 60, 60, DirectSoundWaveData_heatran_snare, 255, 0, 255, %d' % DRUM_REL[SNARE],
        'voice_directsound_no_resample 60, 84, DirectSoundWaveData_sb_closed_hat, 255, 0, 255, %d' % DRUM_REL[CHH],  # kopie van Heatran v2's closed hat (Heatran v3 gebruikt hem niet meer)
        'voice_directsound_no_resample 60, 84, DirectSoundWaveData_heatran_open_hat, 255, 0, 255, %d' % DRUM_REL[OHH],
        'voice_directsound_no_resample 60, 80, DirectSoundWaveData_sb_pedal_hat, 255, 0, 255, %d' % DRUM_REL[PHH],
        'voice_directsound_no_resample 60, 40, DirectSoundWaveData_heatran_crash, 255, 0, 255, %d' % DRUM_REL[CRASH],
        'voice_directsound_no_resample 60, 52, DirectSoundWaveData_sb_clap, 255, 0, 255, %d' % DRUM_REL[CLAP],
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_heatran_side_stick, 255, 0, 255, %d' % DRUM_REL[STICK],
        'voice_directsound 67, 76, DirectSoundWaveData_heatran_floor_tom, 255, 0, 255, %d' % DRUM_REL[TOMH],
        'voice_directsound 62, 52, DirectSoundWaveData_heatran_floor_tom, 255, 0, 255, %d' % DRUM_REL[TOML],
    ]
    open('sound/voicegroups/drumsets/sickblik.inc', 'w').write(
        '@ Project Grounded: funkkit voor Battle! SickBlik (sickblik_theme.py): 36 kick, 37 snare (ghost notes = zacht),\n'
        '@ 38 gesloten hihat, 39 open hihat, 40 pedaalhihat, 41 crash, 42 handclap, 43 sidestick, 44/45 tom hoog/laag.\n'
        'voice_group sickblik_drumset, 36\n' + ''.join('\t%s\n' % k for k in kit) + '\n')


def fx_events(fx, notes):
    """bend/mod: terugzetten op 0 bij de volgende noot die zelf geen bend/mod op die tick heeft."""
    ev = {}
    for t, kind, v in fx:
        ev[(t, kind)] = v
    out = dict(ev)
    for kind in ('bend', 'mod'):
        cur = 0
        times = sorted(set([t for (t, k) in ev if k == kind] + [n[0] for n in notes]))
        for t in times:
            if (t, kind) in ev:
                cur = ev[(t, kind)]
            elif cur != 0:
                out[(t, kind)] = 0
                cur = 0
    return [(t, k, v) for (t, k), v in out.items()]


def add_track(out, notes, prog, vol, ch, pan, fx, progs=None, init=()):
    t = mido.MidiTrack()
    t.append(mido.Message('program_change', channel=ch, program=prog, time=0))
    t.append(mido.Message('control_change', channel=ch, control=7, value=vol, time=0))
    t.append(mido.Message('control_change', channel=ch, control=10, value=pan, time=0))
    for c, v in init:
        t.append(mido.Message('control_change', channel=ch, control=c, value=v, time=0))
    ev = []
    for tk, kind, v in fx:
        if kind == 'vol':
            ev.append((tk, 1, mido.Message('control_change', channel=ch, control=7, value=max(0, min(127, v * vol // 100)))))
        elif kind == 'mod':
            ev.append((tk, 1, mido.Message('control_change', channel=ch, control=1, value=v)))
        elif kind == 'bend':
            ev.append((tk, 1, mido.Message('pitchwheel', channel=ch, pitch=max(-8192, min(8191, v)))))
    cur = prog
    for s, e, n, v in sorted(notes):
        ev.append((e, 0, mido.Message('note_off', channel=ch, note=n, velocity=0)))
        pr = (progs or {}).get((s, n), prog)
        if pr != cur:
            ev.append((s, 1, mido.Message('program_change', channel=ch, program=pr)))
            cur = pr
        ev.append((s, 2, mido.Message('note_on', channel=ch, note=n, velocity=max(1, min(127, int(v))))))
    last = 0
    for tk, _, m in sorted(ev, key=lambda x: (x[0], x[1])):
        t.append(m.copy(time=tk - last))
        last = tk
    out.tracks.append(t)


LAYOUT = [  # naam, programma, volume, kanaal, pan
    ('thumb', THUMB, 104, 0, 64), ('pop', POP, 92, 1, 64), ('deadT', DEADT, 110, 2, 64), ('deadP', DEADP, 80, 3, 64),
    ('gtrW', GW_M9, 80, 4, 34), ('gtrS', GSCR, 58, 5, 34), ('gtrM', GMUTE, 72, 6, 40),
    ('clav', CLAV, 66, 7, 96), ('rhodes', RH_M9, 56, 8, 28), ('hornLo', HORNS, 84, 10, 76),
    ('hornHi', HORNS_HI, 84, 11, 76), ('talk', TALK, 100, 12, 88),
]
# stemverdeler: van hoog naar laag (de bas is de ster)
ORDER = ['thumb', 'pop', 'deadT', 'kick', 'snare', 'hornHi', 'hornLo', 'talk', 'gtrM', 'deadP', 'crash', 'clap',
         'clav', 'gtrW', 'hat', 'ohat', 'rhodes', 'tom', 'gtrS']
DRUM_PARTS = ('kick', 'snare', 'hat', 'ohat', 'crash', 'clap', 'tom')


def save(P, path):
    out = mido.MidiFile(type=1, ticks_per_beat=TPB)
    cond = mido.MidiTrack()
    cond.append(mido.MetaMessage('set_tempo', tempo=int(60e6 / BPM), time=0))
    cond.append(mido.MetaMessage('marker', text='[', time=A1 * BAR))
    cond.append(mido.MetaMessage('marker', text=']', time=(END - A1) * BAR))
    out.tracks.append(cond)
    for name, prog, vol, ch, pan in LAYOUT:
        progs = {(s, n): pr for (k, s, n), pr in P.prog.items() if k == name}
        init = [(20, 2)] if name in ('thumb', 'pop', 'talk') else []          # BENDR = 2 halve tonen
        add_track(out, P.n[name], prog, vol, ch, pan, fx_events(P.fx[name], P.n[name]), progs, init)
    add_track(out, sorted(sum((P.n[k] for k in DRUM_PARTS), [])), DRUMS, 118, 9, 64, [])
    written = {k for k, *_ in LAYOUT} | set(DRUM_PARTS)
    assert not [k for k in P.n if P.n[k] and k not in written], 'partij niet weggeschreven'
    assert all(x[1] <= END * BAR for k in P.n for x in P.n[k]), 'noot loopt over het loopeinde'
    assert all(x[1] <= A1 * BAR or x[0] >= A1 * BAR for k in P.n for x in P.n[k]), 'noot loopt over het loopbegin'
    out.save(path)


def main():
    P = build()
    write_voicegroup()
    prog_of = {name: prog for name, prog, *_ in LAYOUT}
    tail = {k: release_ticks(REL[pr], TPB, BPM) for k, pr in prog_of.items()}
    one_string(P, tail)
    for k, nt in (('kick', KICK), ('snare', SNARE), ('hat', CHH), ('ohat', OHH), ('crash', CRASH), ('clap', CLAP),
                  ('tom', TOML)):
        tail[k] = release_ticks(DRUM_REL[nt], TPB, BPM) if DRUM_REL[nt] else 0
    order = ORDER
    kept = allocate({k: P.n[k] for k in order}, order, tail)
    print('uitklinktijd (ticks):', {k: v for k, v in tail.items() if v})
    for k in order:
        n = len(P.n[k])
        print('  %-7s %4d noten, %3d vallen weg (%.1f%%)' % (k, n, n - len(kept[k]), 100 * (n - len(kept[k])) / max(n, 1)))
        P.n[k] = kept[k]
    save(P, OUT)
    spb = 4 * 60 / BPM
    print(OUT, '%.1f s intro, %.1f s loop' % (A1 * spb, (END - A1) * spb))
    for nm, a, b in (('intro', INTRO, A1), ('A1', A1, H1), ('H1', H1, BRK), ('B', BRK, A2), ('A2', A2, H2),
                     ('H2', H2, END)):
        print('  %-5s maat %2d-%2d  %6.1f - %6.1f s' % (nm, a, b - 1, a * spb, b * spb))


if __name__ == '__main__':
    main()
