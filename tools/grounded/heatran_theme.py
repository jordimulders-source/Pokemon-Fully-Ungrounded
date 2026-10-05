#!/usr/bin/env python3
"""Project Grounded: "Battle! Heatran" v2, eigen compositie in échte stoner rock (Kyuss 'Green Machine'/'Thumb'/
'Gardenia', vroege Queens of the Stone Age, Sleep, Fu Manchu). Jordi over v1: 'geen stoner, eerder Bowser's Castle-
metal'. v2 volgt zijn beschrijving punt voor punt:
  - strofen: alleen fuzzbas + drums (groovende, melodische baslijn, losse drums met hihat/ride); in de 2e helft
    zacht de refreinriff palm-muted op de gitaar
  - refreinen: zwaar, traag, headbangend: halftempo (snare op tel 3), de refreinriff voluit in drop C met dikke
    'Big Muff'-fuzz, bas en gitaren unisono, crash/open hihat, syncopen en pauzes in de riff
  - rustig middenstuk: bas + getokkelde cleane gitaararpeggio's (dorisch, woestijn), dan opbouw terug naar de riff
  - warm, bluesy, C-mineur-pentatonisch + blue note Gb; groove boven drama
100 bpm (refreinen voelen als 50: halftempo), drop C (laagste powerchord = C2).

  maat 0-1   intro: fuzz-powerchord C zwelt aan + hoge feedback, lava-rommel op de floor tom
  maat 2-4   de refreinriff één keer voluit (statement), maat 4 = de stop (akkoord laten hangen, baspickup)
Loop (48 maten, 115 s):
  V1  5-12   strofe: bas + drums (hihat); maat 9-12 de refreinriff zacht palm-muted links
  R1 13-20   refrein: riff voluit, halftempo, crash/open hihat; maat 20 = stop
  V2 21-28   strofe 2: bas + drums (ride), palm-muted riff links en rechts, zacht
  R2 29-36   refrein 2: riff + de leadgitaar 'zingt' erboven
  M  37-44   middenstuk: bas + cleane arpeggio's, ride/sidestick; 41-44 opbouw (toms, feedback, snareroffel)
  R3 45-52   refrein 3: riff + bluesy solo met bends; maat 52 = stop -> terug naar de strofe (= maat 4 -> 5)
Gitaren: één sample = een complete fuzz-powerchord (C2+G2+C3 samen door FluidR3 + eigen Big Muff-fuzz) = 1 kanaal
per akkoord; links/rechts, de rechter +9 cent (dubbele opname). Palm-mute = eigen sample (GM 28 door dezelfde fuzz).
Fuzzbas met octaaffuzz + schoon laag (blend). Dynamiek met CC7 per spoor per sectie.
Samples: tools/grounded/heatran_samples.py. Gebruikt musiclib.py; zie MUZIEK.md. Gebruik: python3 tools/grounded/heatran_theme.py"""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks

OUT = 'sound/songs/midi/mus_grounded_vs_heatran.mid'
VG = 'grounded_heatran'
TPB, BPM = 96, 100
S = TPB // 4                   # een 16e
BAR = TPB * 4
LAY = 4                        # snare iets achter de tel (laid back)
CLEAN, MUTE, SINGLE, POWER, LEAD, BASS, DRUMS = 27, 28, 29, 30, 31, 34, 127
# eigen drumkit (drumsets/heatran.inc, vanaf noot 36)
KICK, SNARE, OHH, RIDE, FTOM, MTOM, CRASH, CRASH2, CHH, STICK, BELL = range(36, 47)
DRUM_REL = {KICK: 0, SNARE: 0, OHH: 200, RIDE: 210, FTOM: 0, MTOM: 0, CRASH: 220, CRASH2: 220, CHH: 0, STICK: 0,
            BELL: 200}
DRUM_LEN = {KICK: TPB // 2, SNARE: TPB * 3 // 4, OHH: TPB // 2 - 6, RIDE: TPB, FTOM: TPB // 2, MTOM: TPB // 2,
            CRASH: TPB * 2, CRASH2: TPB * 2, CHH: S, STICK: S, BELL: TPB // 2}

INTRO_RIFF, STOP0 = 2, 4
V1, R1, V2, R2, M, R3, END = 5, 13, 21, 29, 37, 45, 53      # secties (maat); loop = maat 5-53

N = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'Ab': 8, 'A': 9,
     'Bb': 10, 'B': 11}


def p(name):
    """'C2' -> midi-noot (C4 = 60)."""
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


# ---- de refreinriff (drop C): (16e, lengte in 16en, 'P' powerchord | 'N' losse noot, grondtoon) ---------------
# syncopen (de Eb vóór tel 3, de Gb op de 'e' van 4) en pauzes (R2: tel 4 leeg, dan een pickup)
RIFF_A = [(0, 5, 'P', 'C2'), (6, 1, 'N', 'C2'), (7, 3, 'P', 'Eb2'), (10, 2, 'P', 'F2'), (12, 1, 'N', 'C2'),
          (13, 2, 'P', 'Gb2'), (15, 1, 'N', 'F2')]
RIFF_B = [(0, 3, 'P', 'G2'), (3, 3, 'P', 'F2'), (6, 2, 'P', 'Eb2'), (8, 4, 'P', 'C2'), (14, 1, 'N', 'Eb2'),
          (15, 1, 'N', 'D2')]
RIFF_TURN = [(0, 3, 'P', 'Ab2'), (3, 1, 'N', 'Ab2'), (4, 2, 'P', 'Bb2'), (6, 2, 'N', 'Bb2'), (8, 6, 'P', 'C3'),
             (14, 1, 'N', 'Bb2'), (15, 1, 'N', 'G2')]
RIFF_STOP = [(0, 8, 'P', 'C2')]                                    # akkoord hangt 2 tellen, dan stilte
STOP_BASS = [(0, 8, 'C2'), (12, 2, 'G1'), (14, 1, 'Bb1'), (15, 1, 'B1')]   # chromatische pickup naar de strofe
CHORUS = [RIFF_A, RIFF_B, RIFF_A, RIFF_B, RIFF_A, RIFF_B, RIFF_TURN, RIFF_STOP]

# ---- strofe: de melodische fuzzbas (16e, lengte, noot) -------------------------------------------------------------
VB_A = [(0, 3, 'C2'), (3, 1, 'C2'), (4, 2, 'Eb2'), (6, 1, 'C2'), (7, 1, 'F2'), (8, 2, 'G2'), (10, 1, 'Bb2'),
        (11, 1, 'G2'), (12, 2, 'C3'), (14, 1, 'Bb2'), (15, 1, 'G2')]
VB_B = [(0, 3, 'F2'), (3, 1, 'F2'), (4, 1, 'Ab2'), (5, 1, 'F2'), (6, 2, 'Gb2'), (8, 3, 'F2'), (11, 1, 'Eb2'),
        (12, 3, 'C2'), (15, 1, 'Bb1')]
VB_C = [(0, 3, 'C2'), (3, 1, 'C2'), (4, 2, 'Eb2'), (6, 1, 'C2'), (7, 1, 'F2'), (8, 2, 'G2'), (10, 1, 'Bb2'),
        (11, 1, 'C3'), (12, 1, 'Eb3'), (13, 1, 'C3'), (14, 1, 'Bb2'), (15, 1, 'G2')]       # variant (hoger loopje)
VB_TURN = [(0, 3, 'C2'), (3, 1, 'C2'), (4, 2, 'Eb2'), (6, 2, 'F2'), (8, 2, 'Gb2'), (10, 2, 'G2'), (12, 4, 'Bb2')]
VERSE_BASS = [VB_A, VB_B, VB_A, VB_B, VB_C, VB_B, VB_A, VB_TURN]
VERSE2_BASS = [VB_C, VB_B, VB_A, VB_B, VB_C, VB_B, VB_C, VB_TURN]

# ---- middenstuk: cleane arpeggio's (8en) en de bas ------------------------------------------------------------------
ARP = [['C3', 'G3', 'Bb3', 'D4', 'Eb4', 'D4', 'Bb3', 'G3'],      # Cm9
       ['C3', 'G3', 'Bb3', 'D4', 'Eb4', 'D4', 'Bb3', 'G3'],
       ['F2', 'C3', 'A3', 'Eb4', 'G4', 'Eb4', 'A3', 'C3'],       # F9 (dorisch: de woestijn-IV)
       ['F2', 'C3', 'A3', 'Eb4', 'G4', 'Eb4', 'A3', 'C3'],
       ['Ab2', 'Eb3', 'G3', 'C4', 'Eb4', 'C4', 'G3', 'Eb3'],     # Abmaj7
       ['Bb2', 'F3', 'Bb3', 'D4', 'F4', 'D4', 'Bb3', 'F3'],      # Bb
       ['C3', 'G3', 'C4', 'Eb4', 'G4', 'Eb4', 'C4', 'G3'],       # Cm
       ['G2', 'D3', 'F3', 'B3', 'Bb3', 'B3', 'D4', 'F4']]        # G7#9 -> refrein
MID_BASS = [[(0, 12, 'C2'), (12, 2, 'Bb1'), (14, 2, 'G1')],
            [(0, 8, 'C2'), (8, 4, 'Eb2'), (12, 4, 'G2')],
            [(0, 12, 'F2'), (12, 2, 'Eb2'), (14, 2, 'C2')],
            [(0, 8, 'F2'), (8, 4, 'A2'), (12, 2, 'C3'), (14, 2, 'A2')],
            [(0, 12, 'Ab1'), (12, 4, 'Eb2')],
            [(0, 12, 'Bb1'), (12, 4, 'F2')],
            [(0, 6, 'C2'), (6, 2, 'C2'), (8, 4, 'Eb2'), (12, 4, 'G2')],
            [(0, 4, 'G1'), (4, 2, 'G1'), (6, 2, 'Bb1'), (8, 2, 'B1'), (10, 2, 'D2'), (12, 2, 'F2'), (14, 2, 'Ab2')]]

# ---- leadgitaar: (16e, lengte, noot, extra) ; 'b' = bend van 2 halve tonen eronder, 'v' = vibrato ----------------
SING = [   # R2: de 'zang'-melodie (John Garcia) op de leadgitaar, C-mineur-pentatonisch
    [(2, 2, 'G4', ''), (4, 6, 'Bb4', 'v'), (10, 2, 'G4', ''), (12, 4, 'F4', '')],
    [(0, 8, 'G4', 'bv'), (10, 2, 'Eb4', ''), (12, 4, 'C4', '')],
    [(2, 2, 'G4', ''), (4, 6, 'Bb4', 'v'), (10, 2, 'C5', ''), (12, 4, 'Bb4', '')],
    [(0, 12, 'G4', 'v')],
    [(2, 2, 'C5', ''), (4, 6, 'Eb5', 'v'), (10, 2, 'C5', ''), (12, 4, 'Bb4', '')],
    [(0, 8, 'C5', 'bv'), (8, 4, 'Bb4', ''), (12, 4, 'G4', '')],
    [(2, 2, 'F4', ''), (4, 4, 'G4', ''), (8, 4, 'Bb4', ''), (12, 4, 'C5', '')],
    [(0, 6, 'G4', 'v'), (6, 2, 'F4', ''), (8, 8, 'C4', 'v')],
]
SOLO = [
    [(0, 2, 'G4', ''), (2, 2, 'Bb4', ''), (4, 4, 'C5', 'b'), (8, 2, 'Bb4', ''), (10, 2, 'G4', ''), (12, 4, 'F4', 'v')],
    [(0, 2, 'G4', ''), (2, 1, 'F4', ''), (3, 1, 'Eb4', ''), (4, 4, 'C4', 'v'), (10, 2, 'Eb4', ''), (12, 2, 'F4', ''),
     (14, 2, 'Gb4', '')],
    [(0, 6, 'G4', 'bv'), (6, 2, 'Bb4', ''), (8, 2, 'C5', ''), (10, 2, 'Eb5', ''), (12, 4, 'C5', 'v')],
    [(0, 2, 'Bb4', ''), (2, 2, 'G4', ''), (4, 2, 'Bb4', ''), (6, 2, 'G4', ''), (8, 8, 'F4', 'v')],
    [(0, 1, 'C5', ''), (1, 1, 'Bb4', ''), (2, 1, 'G4', ''), (3, 1, 'F4', ''), (4, 1, 'G4', ''), (5, 1, 'Bb4', ''),
     (6, 1, 'C5', ''), (7, 1, 'Eb5', ''), (8, 4, 'F5', 'bv'), (12, 2, 'Eb5', ''), (14, 2, 'C5', '')],
    [(0, 1, 'Eb5', ''), (1, 1, 'C5', ''), (2, 1, 'Bb4', ''), (3, 1, 'C5', ''), (4, 1, 'Eb5', ''), (5, 1, 'C5', ''),
     (6, 1, 'Bb4', ''), (7, 1, 'G4', ''), (8, 4, 'Bb4', ''), (12, 4, 'G4', 'v')],
    [(0, 8, 'C5', 'bv'), (8, 2, 'Eb5', ''), (10, 2, 'F5', ''), (12, 4, 'G5', 'b')],
    [(0, 8, 'C5', 'v'), (8, 8, 'C5', 'v')],                     # de stop: lang uitzingen boven het hangende akkoord
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
        self.n = {k: [] for k in ('pwrL', 'pwrR', 'sglL', 'sglR', 'muteL', 'muteR', 'clean', 'bass', 'lead', 'fb',
                                  'kick', 'snare', 'hat', 'ride', 'tom', 'crash')}
        self.fx = {k: [] for k in self.n}     # (tick, 'vol'|'mod'|'bend', waarde) per spoor; 'vol' = CC7 in %

    def add(self, part, start, length, note, vel):
        self.n[part].append([int(start), int(start + length), note, vel])

    def vol(self, parts, bar, pct):
        for k in parts:
            self.fx[k].append((bar * BAR, 'vol', pct))


def riff(P, bar, pattern, vel=112, guitars=True, bass=True, right=True):
    for st, ln, kind, nm in pattern:
        s = bar * BAR + st * S
        acc = 10 if st in (0, 8) else (0 if kind == 'P' else -12)
        if guitars:
            side = ('L', 'R') if right else ('L',)
            for sd in side:
                P.add(('pwr' if kind == 'P' else 'sgl') + sd, s, ln * S, p(nm), vel + acc - (6 if sd == 'R' else 0))
        if bass:
            P.add('bass', s, ln * S, bass_note(p(nm)), 116 + (8 if st in (0, 8) else 0))


def palm_mute(P, bar, pattern, sides=('L',), vel=104):
    """De refreinriff gedempt: elke noot als korte chug, lange noten herhaald op elke 8e (zoals een echte palm-mute)."""
    for st, ln, kind, nm in pattern:
        for k in range(0, ln, 2):
            s = bar * BAR + (st + k) * S
            for sd in sides:
                P.add('mute' + sd, s, S + S // 2, p(nm) if p(nm) <= p('G2') else p(nm) - 12,
                      vel + (10 if st + k in (0, 8) else 0) - (4 if sd == 'R' else 0))


def lead(P, bar, phrase, vel=118, part='lead'):
    for st, ln, nm, fx in phrase:
        s = bar * BAR + st * S
        n = p(nm)
        if 'b' in fx:                                       # bend: begin 2 halve tonen lager, in een 16e omhoog
            P.add(part, s, ln * S, n - 2, vel)
            for k in range(1, 7):
                P.fx[part].append((s + k * S // 6, 'bend', min(8191, int(8192 * k / 6))))
        else:
            P.add(part, s, ln * S, n, vel)
        if 'v' in fx and ln >= 4:                           # vertraagd vibrato (na een 8e)
            P.fx[part].append((s + 2 * S, 'mod', 9))


def verse_drums(P, bar, i, cym='hat'):
    """Strofe: vol tempo, los en laid back: kick, snare op 2 en 4, ghost notes, hihat of ride in 8en."""
    b = bar * BAR
    kicks = (0, 7, 10) if i % 2 == 0 else (0, 3, 10, 13)
    for k in kicks:
        P.add('kick', b + k * S, DRUM_LEN[KICK], KICK, 100 if k == 0 else 88)
    for q in (4, 12):
        P.add('snare', b + q * S + LAY, DRUM_LEN[SNARE], SNARE, 108)
    for g in ((7, 14) if i % 2 else (14,)):                 # ghost notes
        P.add('snare', b + g * S + LAY, S, SNARE, 44)
    for e in range(8):
        if cym == 'hat':
            if i % 2 and e == 7:
                P.add('hat', b + e * 2 * S, DRUM_LEN[OHH], OHH, 76)        # open hihat op de laatste 'en'
            else:
                P.add('hat', b + e * 2 * S, DRUM_LEN[CHH], CHH, 84 if e % 2 == 0 else 58)
        else:
            P.add('ride', b + e * 2 * S, DRUM_LEN[RIDE] // 2, RIDE, 88 if e % 2 == 0 else 62)


def chorus_drums(P, bar, pattern, i, cym='hat'):
    """Refrein: halftempo, snare op tel 3, kick op de accenten van de riff, crash om de 2 maten, open hihat of
    ride op de tellen."""
    b = bar * BAR
    kicks = sorted({st for st, ln, kind, nm in pattern if kind == 'P'} - {8})
    for k in kicks:
        P.add('kick', b + k * S, DRUM_LEN[KICK], KICK, 124 if k == 0 else 110)
    if pattern is RIFF_STOP:
        P.add('crash', b, DRUM_LEN[CRASH2], CRASH2, 118)
        return
    P.add('snare', b + 8 * S + LAY, DRUM_LEN[SNARE], SNARE, 127)
    if i % 2 == 0:
        P.add('crash', b, DRUM_LEN[CRASH], CRASH if i % 4 == 0 else CRASH2, 120)
    for q in range(4):
        if i % 2 == 0 and q == 0:
            continue
        if cym == 'hat':
            P.add('hat', b + q * TPB, DRUM_LEN[OHH], OHH, 104 if q % 2 == 0 else 90)
        else:
            P.add('ride', b + q * TPB, DRUM_LEN[RIDE], BELL if q % 2 else RIDE, 104 if q % 2 == 0 else 96)


def fill(P, bar, start16=12):
    """Tomfill (snare + toms in 16en) naar de crash van de volgende maat; vervangt de groove vanaf start16."""
    b = bar * BAR
    for k in ('hat', 'ride', 'snare', 'kick'):
        P.n[k] = [x for x in P.n[k] if not (b + start16 * S <= x[0] < b + BAR)]
    seq = [SNARE, SNARE, MTOM, MTOM, FTOM, FTOM, FTOM, SNARE][-(16 - start16):]
    for i, nt in enumerate(seq):
        P.add('snare' if nt == SNARE else 'tom', b + (start16 + i) * S, S, nt, 96 + i * 4)


def chorus(P, bar0, cym='hat', lead_phrases=None, right=True):
    for i, pat in enumerate(CHORUS):
        b = bar0 + i
        if pat is RIFF_STOP:
            riff(P, b, pat, bass=False, right=right)
            for st, ln, nm in STOP_BASS:
                P.add('bass', b * BAR + st * S, ln * S, bass_note(p(nm)), 120)
        else:
            riff(P, b, pat, right=right)
        chorus_drums(P, b, pat, i, cym)
        if lead_phrases:
            lead(P, b, lead_phrases[i], 116)
    fill(P, bar0 + 6, 12)                                    # de turnaround rolt naar de stop


def stop_feedback(P, bar, note='C5'):
    """Na de stop: de versterker blijft huilen (feedback) zolang het akkoord hangt."""
    s = bar * BAR
    P.add('fb', s + S * 2, 6 * S, p(note), 110)
    for j in range(7):
        P.fx['fb'].append((s + S * 2 + j * S, 'vol', int(30 + 70 * j / 6)))
    P.fx['fb'] += [(s + S * 2, 'mod', 0), (s + S * 5, 'mod', 10)]


def build():
    P = Parts()
    G = ('pwrL', 'pwrR', 'sglL', 'sglR')

    # ---- intro: zwelling, dan de riff één keer als statement ----------------------------------------------------
    P.add('pwrL', 0, 2 * BAR - S, p('C2'), 112)
    P.add('pwrR', 0, 2 * BAR - S, p('C2'), 106)
    for k in range(33):                                     # powerchord zwelt in 2 maten aan
        for sd in ('pwrL', 'pwrR'):
            P.fx[sd].append((k * 2 * BAR // 32, 'vol', int(((k / 32) ** 1.6) * 100)))
    P.add('fb', BAR // 2, BAR + BAR // 2 - S, p('G4'), 110)      # hoge feedbacktoon zwelt mee
    for k in range(25):
        P.fx['fb'].append((BAR // 2 + k * (BAR + BAR // 2) // 24, 'vol', int(((k / 24) ** 1.3) * 100)))
    P.fx['fb'] += [(BAR, 'mod', 4), (BAR + BAR // 2, 'mod', 10)]
    for k in range(16):                                     # lava-rommel op de floor tom in maat 1
        P.add('tom', BAR + k * S, S, FTOM, 50 + k * 4)
    P.vol(G + ('bass',), INTRO_RIFF, 100)
    for i, pat in enumerate((RIFF_A, RIFF_B, RIFF_STOP)):
        b = INTRO_RIFF + i
        if pat is RIFF_STOP:
            riff(P, b, pat, bass=False)
            for st, ln, nm in STOP_BASS:
                P.add('bass', b * BAR + st * S, ln * S, bass_note(p(nm)), 120)
        else:
            riff(P, b, pat)
        chorus_drums(P, b, pat, i)
    stop_feedback(P, STOP0)

    # ---- V1: alleen bas + drums; daarna zacht de palm-muted refreinriff ------------------------------------------
    P.vol(('bass',), V1, 100)
    P.vol(('muteL', 'muteR'), V1, 100)
    for i in range(8):
        b = V1 + i
        for st, ln, nm in VERSE_BASS[i]:
            P.add('bass', b * BAR + st * S, ln * S, bass_note(p(nm)), 112 + (10 if st in (0, 8) else 0))
        verse_drums(P, b, i, 'hat')
        if i >= 4:
            palm_mute(P, b, CHORUS[i - 4] if i < 7 else RIFF_B, ('L',), 96)
    fill(P, R1 - 1, 12)

    # ---- R1: het refrein -----------------------------------------------------------------------------------------
    P.vol(G, R1, 100)
    P.vol(('bass',), R1, 92)
    chorus(P, R1)
    stop_feedback(P, R1 + 7)

    # ---- V2: bas + drums (ride), palm-muted riff links en rechts --------------------------------------------------
    P.vol(('bass',), V2, 100)
    for i in range(8):
        b = V2 + i
        for st, ln, nm in VERSE2_BASS[i]:
            P.add('bass', b * BAR + st * S, ln * S, bass_note(p(nm)), 112 + (10 if st in (0, 8) else 0))
        verse_drums(P, b, i, 'ride')
        pat = CHORUS[i % 6] if i < 7 else RIFF_B
        palm_mute(P, b, pat, ('L', 'R') if i >= 2 else ('L',), 92 + (6 if i >= 4 else 0))
    fill(P, R2 - 1, 8)

    # ---- R2: refrein + de leadgitaar zingt -----------------------------------------------------------------------
    P.vol(('bass',), R2, 92)
    chorus(P, R2, 'ride', SING)

    # ---- M: middenstuk, bas + cleane arpeggio's; 41-44 opbouw -----------------------------------------------------
    P.vol(('bass',), M, 100)
    P.vol(('clean',), M, 100)
    for i in range(8):
        b = M + i
        for e, nm in enumerate(ARP[i]):
            P.add('clean', b * BAR + e * 2 * S, 4 * S, p(nm), 100 + (14 if e == 0 else 0) - (0 if i < 4 else -6))
        for st, ln, nm in MID_BASS[i]:
            P.add('bass', b * BAR + st * S, ln * S, bass_note(p(nm)), 108 + (10 if st == 0 else 0))
        bb = b * BAR
        if i < 4:                                           # ruimte: ride op de tellen, sidestick op 3, zachte kick
            P.add('kick', bb, DRUM_LEN[KICK], KICK, 84)
            for q in range(4):
                P.add('ride', bb + q * TPB, DRUM_LEN[RIDE], RIDE, 70 if q else 82)
            P.add('snare', bb + 8 * S + LAY, S, STICK, 80)
        elif i < 6:                                         # de groove komt terug (ride in 8en, sidestick 2 en 4)
            for k in (0, 10):
                P.add('kick', bb + k * S, DRUM_LEN[KICK], KICK, 96)
            for e in range(8):
                P.add('ride', bb + e * 2 * S, DRUM_LEN[RIDE] // 2, RIDE, 84 if e % 2 == 0 else 64)
            for q in (4, 12):
                P.add('snare', bb + q * S + LAY, S, STICK, 92)
        else:                                               # floor tom in 8en die aanzwelt, kick op de tellen
            for e in range(8):
                P.add('tom', bb + e * 2 * S, S, FTOM, 70 + (i - 6) * 24 + e * 3)
            for q in range(4):
                P.add('kick', bb + q * TPB, DRUM_LEN[KICK], KICK, 96 + (i - 6) * 16)
    for k in range(8):                                      # snareroffel in 16en over tel 3-4 van de laatste maat
        P.add('snare', (R3 - 1) * BAR + (8 + k) * S, S, SNARE, 80 + k * 6)
    s = (M + 6) * BAR                                       # feedback zwelt aan over de laatste 2 maten
    P.add('fb', s, 2 * BAR - S, p('G4'), 110)
    for j in range(33):
        P.fx['fb'].append((s + j * 2 * BAR // 32, 'vol', int(((j / 32) ** 1.4) * 100)))
    P.fx['fb'] += [(s, 'mod', 0), (s + BAR, 'mod', 8)]
    # in de laatste maat van het middenstuk zwelt de powerchord G al mee
    P.add('pwrL', (M + 7) * BAR, BAR - S, p('G2'), 104)
    for j in range(17):
        P.fx['pwrL'].append(((M + 7) * BAR + j * BAR // 16, 'vol', int(((j / 16) ** 2) * 90)))

    # ---- R3: refrein + solo --------------------------------------------------------------------------------------
    P.vol(G, R3, 100)
    P.vol(('bass',), R3, 92)
    chorus(P, R3, 'hat', SOLO)                              # climax: beide gitaren + solo
    P.add('crash', R3 * BAR, DRUM_LEN[CRASH2], CRASH2, 116)

    for k in P.n:
        P.n[k] = dedupe(P.n[k])
    return P


def write_voicegroup():
    """grounded_gm + 27 cleane gitaar, 28 palm-mute, 29 fuzz (losse noten), 30 fuzz-powerchord, 31 fuzz-lead,
    34 fuzzbas, 127 stoner-drumkit."""
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Battle! Heatran (stoner rock). Gegenereerd door tools/grounded/heatran_theme.py.'
    lines[1] = ('@ 27 = cleane gitaar, 28 = palm-mute-powerchord, 29 = fuzz (losse noten), 30 = fuzz-powerchord '
                '(1 sample = 1 kanaal), 31 = fuzz-lead, 34 = octaaffuzzbas, 127 = drumkit.')
    lines[2] = 'voice_group %s' % VG
    repl = {
        '@ 27': '\tvoice_directsound 60, 0, DirectSoundWaveData_gm_clean_guitar, 255, 0, 255, 190  @ 27',
        '@ 28': '\tvoice_directsound 60, 0, DirectSoundWaveData_heatran_mute_power, 255, 0, 255, 120  @ 28',
        '@ 29': '\tvoice_directsound 60, 0, DirectSoundWaveData_heatran_muff_low, 255, 0, 255, 165  @ 29',
        '@ 30': '\tvoice_directsound 60, 0, DirectSoundWaveData_heatran_muff_power, 255, 0, 255, 170  @ 30',
        '@ 31': '\tvoice_directsound 60, 0, DirectSoundWaveData_heatran_fuzz_lead, 255, 0, 255, 200  @ 31',
        '@ 34': '\tvoice_directsound 60, 0, DirectSoundWaveData_heatran_octfuzz_bass, 255, 0, 255, 160  @ 34',
        '@ 127': '\tvoice_keysplit_all voicegroup_heatran_drumset  @ 127',
    }
    out = []
    for l in lines:
        tag = '@' + l.rsplit('@', 1)[1] if '@' in l and l.startswith('\t') else None
        out.append(repl.get(tag.strip() if tag else None, l))
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    kit = [   # vanaf noot 36; alles DirectSound
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_heatran_kick, 255, 0, 255, %d' % DRUM_REL[KICK],
        'voice_directsound_no_resample 60, 60, DirectSoundWaveData_heatran_snare, 255, 0, 255, %d' % DRUM_REL[SNARE],
        'voice_directsound_no_resample 60, 84, DirectSoundWaveData_heatran_open_hat, 255, 0, 255, %d' % DRUM_REL[OHH],
        'voice_directsound_no_resample 60, 44, DirectSoundWaveData_heatran_ride, 255, 0, 255, %d' % DRUM_REL[RIDE],
        'voice_directsound 60, 40, DirectSoundWaveData_heatran_floor_tom, 255, 0, 255, %d' % DRUM_REL[FTOM],
        'voice_directsound 66, 80, DirectSoundWaveData_heatran_floor_tom, 255, 0, 255, %d' % DRUM_REL[MTOM],
        'voice_directsound_no_resample 60, 36, DirectSoundWaveData_heatran_crash, 255, 0, 255, %d' % DRUM_REL[CRASH],
        'voice_directsound 57, 92, DirectSoundWaveData_heatran_crash, 255, 0, 255, %d' % DRUM_REL[CRASH2],
        'voice_directsound_no_resample 60, 76, DirectSoundWaveData_heatran_closed_hat, 255, 0, 255, %d' % DRUM_REL[CHH],
        'voice_directsound_no_resample 60, 56, DirectSoundWaveData_heatran_side_stick, 255, 0, 255, %d' % DRUM_REL[STICK],
        'voice_directsound 67, 40, DirectSoundWaveData_heatran_ride, 255, 0, 255, %d' % DRUM_REL[BELL],
    ]
    open('sound/voicegroups/drumsets/heatran.inc', 'w').write(
        '@ Project Grounded: stoner-drumkit voor Battle! Heatran (heatran_theme.py), samples uit FluidR3 (heatran_samples.py):\n'
        '@ 36 kick, 37 snare, 38 open hihat, 39 ride, 40 floor tom, 41 middentom, 42 crash (links), 43 crash (rechts, lager),\n'
        '@ 44 gesloten hihat, 45 sidestick, 46 ride hoger (bel).\n'
        'voice_group heatran_drumset, 36\n' + ''.join('\t%s\n' % k for k in kit) + '\n')


def fx_events(fx, notes):
    """bend/mod terugzetten op het begin van de volgende noot (niet bij de note-off: dan zakt de uitklinktijd)."""
    starts = sorted(set(n[0] for n in notes))
    ev = [x for x in fx if x[1] == 'vol']
    pm = [x for x in fx if x[1] != 'vol']
    for t, kind, v in pm:
        ev.append((t, kind, v))
        nxt = next((s for s in starts if s > t), None)
        if nxt is not None:
            ev.append((nxt, kind, 0))
    best = {}
    for t, kind, v in ev:
        if kind == 'vol':
            best[(t, kind)] = v                              # laatste waarde op een tick wint
        elif (t, kind) not in best or v:
            best[(t, kind)] = v if (t, kind) not in best else max(best[(t, kind)], v)
    return [(t, k, v) for (t, k), v in best.items()]


def save(P, path):
    out = mido.MidiFile(type=1, ticks_per_beat=TPB)
    cond = mido.MidiTrack()
    cond.append(mido.MetaMessage('set_tempo', tempo=int(60e6 / BPM), time=0))
    cond.append(mido.MetaMessage('marker', text='[', time=V1 * BAR))
    cond.append(mido.MetaMessage('marker', text=']', time=(END - V1) * BAR))
    out.tracks.append(cond)
    layout = [  # naam, programma, volume (100%), kanaal, pan, vaste bend
        ('pwrL', POWER, 100, 0, 22, 0),
        ('pwrR', POWER, 96, 1, 106, 3 * 128),
        ('sglL', SINGLE, 96, 2, 28, 0),
        ('sglR', SINGLE, 92, 3, 100, 3 * 128),
        ('muteL', MUTE, 64, 4, 34, 0),
        ('muteR', MUTE, 60, 5, 94, 3 * 128),
        ('clean', CLEAN, 80, 6, 76, 0),
        ('bass', BASS, 80, 7, 64, 0),
        ('lead', LEAD, 108, 8, 80, 0),
        ('fb', LEAD, 92, 10, 50, 0),
    ]
    for name, prog, vol, ch, pan, bend in layout:
        fx = fx_events(P.fx[name], P.n[name])
        if bend:
            fx = [(0, 'bend', bend)] + fx
        add_track(out, P.n[name], prog, vol, ch, pan, fx)
    drums = ('kick', 'snare', 'hat', 'ride', 'tom', 'crash')
    add_track(out, sorted(sum((P.n[k] for k in drums), [])), DRUMS, 120, 9, 64, [])
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
            ev.append((tk, 1, mido.Message('pitchwheel', channel=ch, pitch=v)))
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
    progs = {'pwrL': POWER, 'pwrR': POWER, 'sglL': SINGLE, 'sglR': SINGLE, 'muteL': MUTE, 'muteR': MUTE,
             'clean': CLEAN, 'bass': BASS, 'lead': LEAD, 'fb': LEAD}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) for k, pr in progs.items()}
    for k, nt in (('kick', KICK), ('snare', SNARE), ('hat', OHH), ('ride', RIDE), ('tom', FTOM), ('crash', CRASH)):
        tail[k] = release_ticks(DRUM_REL[nt], TPB, BPM) if DRUM_REL[nt] else 0
    for k in ('bass', 'lead', 'fb', 'muteL', 'muteR'):
        P.n[k] = detach(P.n[k], tail[k])
    # een powerchord en een losse noot op dezelfde gitaar overlappen nooit: samen één partij voor de detach
    for side in 'LR':
        both = detach(sorted(P.n['pwr' + side] + P.n['sgl' + side]), tail['pwr' + side])
        pw = {(s, n) for s, e, n, v in P.n['pwr' + side]}
        P.n['pwr' + side] = [x for x in both if (x[0], x[2]) in pw]
        P.n['sgl' + side] = [x for x in both if (x[0], x[2]) not in pw]
    order = ['lead', 'pwrL', 'sglL', 'bass', 'kick', 'snare', 'crash', 'clean', 'muteL', 'fb', 'tom', 'hat', 'ride',
             'pwrR', 'sglR', 'muteR']
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
