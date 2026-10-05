#!/usr/bin/env python3
"""Project Grounded: "Battle! Heatran" v7, eigen compositie: Kyuss ('Odyssey', 'Green Machine', 'Gardenia') op een
Game Boy Advance. Geen Kyuss-noten: eigen riffs, gemeten stijl.

Geschiedenis: v1-v5 klonken als surf/ska-punk/'Bowser's Castle' (te huppelig, te vrolijk), v6 (gemeten aan Jordi's
mp3's, 76/94 bpm, lange aangehouden akkoorden, één riff) was "veel te saai, statisch en eentonig". v7 zit ertussen
(Jordi's recept, ronde 7): dreigende intro met een fuzzriff vol slides/bends -> felle drumfill -> snelle stompende
desert-rock-riff op 130 bpm (zijn keuze) -> afwisseling tussen slopende zware stukken (74) en snelle beukstukken
(130), meerdere riffs, palm-mutes, vette slides en bends, crash-accenten, stops en tomfills.

Gemeten aan de referenties (Spleeter-stems, scratchpad heatran7/riffs.py; zie MUZIEK.md 'Heatran v7'):
  drums: sterke aanslagen 65-68 % óp de tel, 22 % op de 'en', 9-12 % op de 'a', 0 % op de 'e' (Green Machine,
         Odyssey 95) -> stompend = kick/snare op de tel, alleen 16e-opstapjes op de 'a'
  bas:   2,0-2,5 sterke aanslagen per tel, gelijk verdeeld over de 16en (16e-riffs), slides 19-41 per minuut
         (Green Machine; Odyssey snel deel 127 bpm: 19/min), bends 60-100/min
Wat het níet-ska houdt op 130 bpm: kick op de tel mét de riff, snare zwaar op 2 en 4, palm-mutes op de tel en de 16en
(nooit alleen op de 'en' na een stille tel), alleen C-klein pentatonisch/blues/frygisch, geen open hihat, geen
chromatische loopjes, recht 16e-raster. stoner_checks() controleert dat, plus 'niet saai' (zie onder).

Instrumenten (voicegroup grounded_heatran):
  28   palm-mute: eigen chug-sample per riffnoot (keysplit_heatran, heatran_st_pm_*, v7)
  30   open powerchord per riffnoot (keysplit_heatran, heatran_st_pw_*, v6-samples: Gen 3-'bitcrushed' fuzz)
       slaggitaar links speelt de riff (open + palm-mute per noot via programmawissel), rechts een 'muur' (herhaalde
       aanslagen op één akkoord = één open noot, +9 cent: dubbele opname)
  31   fuzzlead (keysplit_heatran_lead): bends en pentatonische licks in de sludge, de beukmaten en de reprise
  27   feedback = sd90_classical_overdrive_guitar (de echte Gen 3-gitaar), zwelt aan in intro/fills
  34   bas = sc88pro_synth_bass (doffe Gen 3-synthbas), verdubbelt de riff exact (ook de slides)
  127  drumset heatran: Gen 3-drums zonder PSG (rnd_kick, rnd_snare, gesloten hihat, crashes, sc55-toms)
Slides/bends: BENDR 12 op alle melodische sporen (683 stappen per halve toon); een slide = bend-ramp aan het eind van
de noot naar de volgende toon (of erin vanaf onder), een bend = noot die een (halve) toon omhoog buigt en blijft.
Vorm (intro eenmalig, daarna de loop):
  0      74  zwelling: C-powerchord glijdt 5 halve tonen omhoog erin, feedback, floor tom (de cry valt hier)
  1-4    74  INTRO: dreigende slide-riff (eerst één gitaar, dan beide + drums), eindigt met een stop
  5     130  FELLE DRUMFILL (alleen drums + huilende feedback)
  A 6-13  130 RIFF A 'stomp' (Green Machine-achtig): palm-mute-16en op C, open accenten met slides; tomfill erna
  B 14-21 130 RIFF B 'groove' (Gardenia-achtig): F-pedaal, grote slides; eindigt met een stop
  C 22-27 74  RIFF C 'sludge': slopend, halftime, chugs + kreunende lead; tomfill erna
  D 28-31 130 RIFF D 'beuk': stop-time-klappen met crash, toms in de gaten, lead-schreeuwen; tomfill erna
  A2 32-39 130 RIFF A + lead-climax (pentatonische licks met bends); eindigt met een stop
  E 40-41 74  RIFF E 'Regi-dreiging': C C C Db in kwarten + crashes, dan een stop
  F 42   130  dezelfde drumfill als maat 5, terug naar A
Gebruikt musiclib.py; zie MUZIEK.md. Gebruik: python3 tools/grounded/heatran_samples.py; python3 tools/grounded/heatran_theme.py"""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks

OUT = 'sound/songs/midi/mus_grounded_vs_heatran.mid'
VG = 'grounded_heatran'
TPB = 96
SLOW, FAST = 74, 130
S = TPB // 4                   # een 16e
E = TPB // 2                   # een 8e
BAR = TPB * 4
FB, PM, POWER, LEAD, BASS, DRUMS = 27, 28, 30, 31, 34, 127
BENDR = 12
BU = 8192 // BENDR             # bend-stappen per halve toon
R_BEND = 61                    # rechter gitaar ±9 cent hoger (dubbele opname)
KICK, SNARE, HAT, OHAT, CRASH, FTOM, MTOM, HTOM, CRASH2 = range(36, 45)    # drumsets/heatran.inc
REL = {POWER: 150, PM: 100, LEAD: 190, FB: 200, BASS: 120}
PM_LEN = 14                    # palm-mute: noot 14 ticks (de sample dooft zelf; release 100 = ±10 ticks)

INTRO0, INTRO, FILL0, A, B, C, D, A2, EE, FILL, END = 0, 1, 5, 6, 14, 22, 28, 32, 40, 42, 43
LOOP = A
SLOW_BARS = set(range(0, FILL0)) | set(range(C, D)) | set(range(EE, FILL))
SECTIONS = [('zwelling', INTRO0, INTRO), ('intro', INTRO, FILL0), ('fill', FILL0, A), ('A stomp', A, B),
            ('B groove', B, C), ('C sludge', C, D), ('D beuk', D, A2), ('A2 climax', A2, EE), ('E dreiging', EE, FILL),
            ('fill', FILL, END)]
FAMILY = {'zwelling': 'Z', 'intro': 'I', 'fill': 'F', 'A stomp': 'A', 'B groove': 'B', 'C sludge': 'C', 'D beuk': 'D',
          'A2 climax': 'A', 'E dreiging': 'E'}

N = {'C': 0, 'Db': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'Gb': 6, 'G': 7, 'Ab': 8, 'A': 9, 'Bb': 10, 'B': 11}


def p(name):
    """'C2' -> midi-noot (C4 = 60)."""
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


# ---- tempo: abrupte wissels op de maatstreep (zoals Odyssey) -------------------------------------------------------
TEMPO = []
for bar in range(END):
    bpm = SLOW if bar in SLOW_BARS else FAST
    if not TEMPO or TEMPO[-1][1] != bpm or bar == LOOP:       # loopbegin: tempo op de looptick zelf
        TEMPO.append((bar * BAR, bpm))


def bpm_at(tick):
    return [b for t, b in TEMPO if t <= tick][-1]


def secs(tick):
    s, pts = 0.0, TEMPO + [(10 ** 9, 0)]
    for (t0, b), (t1, _) in zip(pts, pts[1:]):
        if tick <= t0:
            break
        s += (min(tick, t1) - t0) / TPB * 60 / b
    return s


def pos(bar, j):
    """16e-positie j in maat bar: recht raster, geen swing (swing = huppel)."""
    return bar * BAR + j * S


# ---- riffs: (16e, lengte in 16en, noot, 'o' open | 'm' palm-mute, fx) ------------------------------------------------
# fx: ('s', d) = slide aan het eind naar d halve tonen (naar de volgende noot), ('i', d) = erin glijden vanaf d,
#     ('b', d) = buigen naar +d en vasthouden. Gitaar links, bas en (als muur) gitaar rechts spelen dit exact.
def m(j, n):
    return (j, 1, n, 'm', None)


# INTRO (74): dreigend, traag, vol slides
I1 = [(0, 4, 'C2', 'o', ('i', -3)), m(4, 'C2'), m(5, 'C2'), (6, 2, 'Eb2', 'o', ('s', 2)), (8, 3, 'F2', 'o', ('b', 1)),
      m(11, 'Eb2'), (12, 4, 'C2', 'o', ('s', -2))]
I2 = [(0, 4, 'C2', 'o', None), m(4, 'C2'), m(5, 'C2'), (6, 2, 'Gb2', 'o', ('s', -1)), (8, 2, 'F2', 'o', None),
      (10, 2, 'Eb2', 'o', ('s', -3)), m(12, 'C2'), m(13, 'C2'), (14, 2, 'Db2', 'o', ('s', -1))]
I4 = [(0, 4, 'C2', 'o', None), m(4, 'C2'), m(5, 'C2'), (6, 2, 'Gb2', 'o', ('b', 1)), (8, 2, 'F2', 'o', None),
      (10, 2, 'Eb2', 'o', ('s', -3)), (12, 2, 'C2', 'o', None)]                         # 14-16: stop
# RIFF A (130) 'stomp': palm-mute-16en op C, open accenten met slides
A1 = [(0, 2, 'C2', 'o', None), m(2, 'C2'), m(3, 'C2'), m(4, 'C2'), m(5, 'C2'), (6, 2, 'Eb2', 'o', ('s', 2)),
      (8, 2, 'F2', 'o', None), m(10, 'C2'), m(11, 'C2'), (12, 2, 'G2', 'o', ('b', 1)), (14, 2, 'F2', 'o', ('s', -5))]
A2_ = [(0, 2, 'C2', 'o', None), m(2, 'C2'), m(3, 'C2'), (4, 2, 'Bb2', 'o', ('s', -3)), (6, 2, 'G2', 'o', None),
       m(8, 'C2'), m(9, 'C2'), m(10, 'C2'), m(11, 'C2'), (12, 1, 'Eb2', 'o', None), (13, 1, 'F2', 'o', None),
       (14, 2, 'Gb2', 'o', ('b', 1))]
A4 = [(0, 2, 'C2', 'o', None), m(2, 'C2'), m(3, 'C2'), (4, 2, 'Eb2', 'o', None), (6, 2, 'F2', 'o', ('s', 2)),
      (8, 2, 'G2', 'o', None), (10, 2, 'Bb2', 'o', ('b', 2)), (12, 4, 'C3', 'o', ('s', -12))]     # octaaf-duik
A4S = [(0, 2, 'C2', 'o', None), m(2, 'C2'), m(3, 'C2'), (4, 2, 'Eb2', 'o', None), (6, 2, 'F2', 'o', ('s', 2)),
       (8, 2, 'G2', 'o', None), (10, 2, 'Bb2', 'o', ('b', 2)), (12, 2, 'C3', 'o', None)]           # 14-16: stop
RIFF_A = [A1, A2_, A1, A4]
# RIFF B (130) 'groove': F-pedaal, grote slides, terug naar C
B1 = [(0, 3, 'F2', 'o', ('i', -2)), m(3, 'F2'), m(4, 'F2'), m(5, 'F2'), (6, 2, 'Ab2', 'o', ('s', 2)),
      (8, 2, 'Bb2', 'o', None), m(10, 'F2'), m(11, 'F2'), (12, 2, 'Eb2', 'o', ('s', -3)), m(14, 'C2'), m(15, 'C2')]
B2 = [(0, 3, 'C2', 'o', ('i', -2)), m(3, 'C2'), m(4, 'C2'), m(5, 'C2'), (6, 2, 'Eb2', 'o', None),
      (8, 2, 'G2', 'o', ('b', 1)), (10, 2, 'F2', 'o', None), (12, 2, 'Eb2', 'o', ('s', -3)), m(14, 'C2'), m(15, 'C2')]
B4 = [(0, 3, 'C2', 'o', ('i', -2)), m(3, 'C2'), m(4, 'C2'), m(5, 'C2'), (6, 2, 'Gb2', 'o', ('s', 1)),
      (8, 2, 'G2', 'o', None), (10, 2, 'Bb2', 'o', ('s', 2)), (12, 4, 'C3', 'o', ('s', -7))]
BSTOP = [(0, 2, 'C2', 'o', None), (4, 2, 'Db2', 'o', None), (8, 2, 'C2', 'o', ('s', -5))]     # stop: 10-16 stil
RIFF_B = [B1, B2, B1, B4, B1, B2, B1, BSTOP]
# RIFF C (74) 'sludge': slopend, halftime, chugs, kreunende bends
C1 = [(0, 4, 'C2', 'o', ('b', 1)), m(4, 'C2'), m(5, 'C2'), m(6, 'C2'), m(7, 'C2'), (8, 3, 'Gb2', 'o', ('s', -1)),
      m(11, 'F2'), (12, 4, 'Eb2', 'o', ('s', -3))]
C2_ = [(0, 4, 'C2', 'o', None), m(4, 'C2'), m(5, 'C2'), (6, 2, 'Ab2', 'o', ('s', -1)), (8, 4, 'G2', 'o', ('b', 1)),
       (12, 2, 'F2', 'o', None), (14, 2, 'Eb2', 'o', ('s', -3))]
CEND = [(0, 4, 'C2', 'o', None), m(4, 'C2'), m(5, 'C2'), m(6, 'C2'), m(7, 'C2'), (8, 4, 'Gb2', 'o', ('b', 1))]  # + tomfill
RIFF_C = [C1, C2_, C1, C2_, C1, CEND]
# RIFF D (130) 'beuk': stop-time-klappen op de tel, palm-mute-16en als aanloop
D1 = [(0, 2, 'C2', 'o', None), (4, 2, 'C2', 'o', None), (8, 2, 'C2', 'o', None), (10, 2, 'C2', 'o', None),
      m(12, 'C2'), m(13, 'C2'), m(14, 'C2'), m(15, 'C2')]
D2 = [(0, 2, 'Eb2', 'o', None), (4, 2, 'F2', 'o', None), (8, 2, 'Gb2', 'o', ('b', 1)), (10, 2, 'F2', 'o', None),
      m(12, 'Bb2'), m(13, 'Bb2'), (14, 2, 'C3', 'o', ('s', -12))]
D4 = [(0, 2, 'Eb2', 'o', None), (4, 2, 'F2', 'o', None), (8, 2, 'Gb2', 'o', ('b', 1)), (10, 2, 'F2', 'o', None),
      (12, 4, 'C3', 'o', ('s', -12))]                                                           # + tomfill
RIFF_D = [D1, D2, D1, D4]
# RIFF E (74) 'Regi-dreiging': C C C Db in kwarten, dan een stop
E1 = [(0, 4, 'C2', 'o', None), (4, 4, 'C2', 'o', None), (8, 4, 'C2', 'o', None), (12, 4, 'Db2', 'o', ('s', -1))]
E2 = [(0, 2, 'C2', 'o', None), m(2, 'C2'), m(3, 'C2'), (4, 4, 'Gb2', 'o', ('b', 1)), (8, 2, 'F2', 'o', None),
      (10, 2, 'Eb2', 'o', ('s', -3)), (12, 2, 'C2', 'o', None)]                         # 14-16: stop
RIFF_E = [E1, E2]

# ---- lead: (16e, lengte, noot, fx) fx: 'i' = erin glijden vanaf 2 halve tonen lager, 'u1'/'u2' = (halve) toon
# omhoog buigen, 'v' = vibrato. Alleen C-klein pentatonisch + blue note.
MOAN = [    # sludge, maat C+1 .. C+5
    [(0, 4, 'C4', 'i'), (4, 2, 'Eb4', ''), (6, 2, 'F4', ''), (8, 8, 'F4', 'u2v')],
    [(0, 6, 'G4', 'v'), (6, 2, 'Bb4', ''), (8, 4, 'G4', 'u1'), (12, 4, 'F4', '')],
    [(0, 4, 'Eb4', 'u2'), (4, 4, 'C4', ''), (8, 8, 'C4', 'iv')],
    [(0, 4, 'G4', 'i'), (4, 2, 'Bb4', ''), (6, 2, 'C5', ''), (8, 8, 'C5', 'u1v')],
    [(0, 4, 'Bb4', 'u2'), (4, 4, 'G4', ''), (8, 4, 'F4', 'u1'), (12, 4, 'Eb4', '')],
]
SCREAM = [  # beuk, maat D .. D+3: schreeuwen op de tel
    [(0, 4, 'C5', 'u1'), (8, 4, 'G4', 'u1v')],
    [(0, 4, 'Bb4', 'u2'), (8, 4, 'G4', 'iv')],
    [(0, 4, 'C5', 'u1'), (8, 4, 'Bb4', 'v')],
    [(0, 4, 'Eb5', 'i'), (4, 4, 'C5', 'u1v')],
]
CLIMAX = [  # reprise A2, maat A2 .. A2+7
    [(0, 2, 'C5', ''), (2, 2, 'Bb4', ''), (4, 4, 'G4', 'u1'), (8, 2, 'F4', ''), (10, 2, 'G4', ''), (12, 4, 'Bb4', 'u2')],
    [(0, 8, 'C5', 'iv'), (8, 2, 'Bb4', ''), (10, 2, 'G4', ''), (12, 4, 'F4', 'v')],
    [(0, 2, 'Eb4', ''), (2, 2, 'F4', ''), (4, 2, 'G4', ''), (6, 2, 'Bb4', ''), (8, 8, 'C5', 'u1v')],
    [(0, 4, 'Bb4', 'u2'), (4, 4, 'G4', ''), (8, 4, 'F4', 'u1'), (12, 4, 'Eb4', '')],
    [(0, 2, 'C5', ''), (2, 2, 'Bb4', ''), (4, 4, 'G4', 'u1'), (8, 2, 'F4', ''), (10, 2, 'G4', ''), (12, 4, 'Bb4', 'u2')],
    [(0, 8, 'Eb5', 'iv'), (8, 2, 'C5', ''), (10, 2, 'Bb4', ''), (12, 4, 'C5', 'u1')],
    [(0, 2, 'G4', ''), (2, 2, 'Bb4', ''), (4, 2, 'C5', ''), (6, 2, 'Eb5', ''), (8, 8, 'F5', 'u1v')],
    [(0, 4, 'Eb5', 'u2'), (4, 4, 'C5', ''), (8, 4, 'Bb4', 'v'), (12, 2, 'C5', '')],            # 14-16: stop
]


class Parts:
    def __init__(self):
        self.n = {k: [] for k in ('gtrL', 'gtrR', 'bass', 'lead', 'fb', 'kick', 'snare', 'hat', 'cym', 'tom')}
        self.fx = {k: [] for k in list(self.n) + ['drums']}   # (tick, 'vol'|'mod'|'bend', waarde); 'vol' = CC7 in %
        self.slides = []                                      # (tick, soort) voor de controles
        self.written = {}

    def add(self, part, start, end, note, vel, prog=None):
        self.n[part].append([int(start), int(end), note, vel] + ([prog] if prog is not None else []))


def vel_of(j, kind, base=0):
    """Accent óp de tel (stompend); alles naast de tel zachter dan de zachtste tel-aanslag (anti-ska)."""
    if j % 4 == 0:
        return 124 + base if kind == 'o' else 114 + base
    return (104 if kind == 'o' else 96 if j % 2 == 0 else 90) + base


def ramp(t0, t1, v0, v1, steps=6):
    t1 = max(t1, t0 + steps)
    return [(t0 + (t1 - t0) * k // steps, 'bend', int(round(v0 + (v1 - v0) * k / steps))) for k in range(steps + 1)]


def riff(P, bar, pattern, guitars=('L', 'R'), base=0):
    """Gitaar links + bas exact de riff; rechts een muur (herhaalde aanslagen op één akkoord = één open noot).
    Slides/bends als bend-events, dezelfde op alle drie de sporen."""
    wall, bends, prev_fx = [], [], True
    for st, ln, nm, kind, fx in pattern:
        s, e = pos(bar, st), pos(bar, st + ln)
        v = vel_of(st, kind, base)
        if kind == 'm':
            e = s + PM_LEN
        if 'L' in guitars:
            P.add('gtrL', s, e, p(nm), v, PM if kind == 'm' else POWER)
        P.add('bass', s, s + 12 if kind == 'm' else e, p(nm), v)
        if wall and wall[-1][2] == p(nm) and wall[-1][1] >= s - S and not fx and not prev_fx:
            wall[-1][1] = pos(bar, st + ln)
        else:
            wall.append([s, pos(bar, st + ln), p(nm), v - 6, POWER])
        prev_fx = fx is not None
        if fx:
            k, d = fx
            ln_t = ln * S
            if k == 's':                                      # slide naar de volgende noot, in de laatste 16e(n)
                L = min(ln_t, S if bpm_at(s) <= 80 else 2 * S)
                bends += ramp(e - L, e - 4, 0, d * BU)
            elif k == 'i':                                    # erin glijden
                bends += ramp(s, s + min(ln_t // 2, S), d * BU, 0)
            elif k == 'b':                                    # buigen en vasthouden
                bends += ramp(s + min(S, ln_t // 3), s + min(2 * S, 2 * ln_t // 3), 0, d * BU)
            P.slides.append((s, k))
    if 'R' in guitars:
        for x in wall:
            P.add('gtrR', *x)
    for sd in ('gtrL', 'gtrR', 'bass'):
        if sd != 'gtrR' or 'R' in guitars:
            P.fx[sd] += bends


def lead(P, bar, phrase, vel=104):
    for st, ln, nm, fx in phrase:
        s, e = pos(bar, st), pos(bar, st + ln)
        P.add('lead', s, e, p(nm), vel + (8 if st % 4 == 0 else 0))
        if 'i' in fx:
            P.fx['lead'] += ramp(s, s + min(S, (e - s) // 2), -2 * BU, 0)
        for d in (1, 2):
            if 'u%d' % d in fx:
                P.fx['lead'] += ramp(s + min(S, (e - s) // 3), s + min(2 * S, 2 * (e - s) // 3), 0, d * BU)
        if 'v' in fx and ln >= 4:
            P.fx['lead'].append((s + min(TPB, (e - s) // 2), 'mod', 10))
            P.fx['lead'].append((s, 'mod', 0))


# ---- drums ---------------------------------------------------------------------------------------------------------
def dlen(bar, kind):
    """Drumnoten zo lang als het sample echt klinkt (rnd_kick 0,09 s, rnd_snare 0,16 s): voor de stemverdeler."""
    q = TPB * (SLOW if bar in SLOW_BARS else FAST) / 60
    return {KICK: max(6, int(0.10 * q)), SNARE: max(8, int(0.17 * q)), HAT: max(6, int(0.08 * q)),
            OHAT: E, CRASH: 2 * TPB, CRASH2: TPB, FTOM: E, MTOM: E, HTOM: E}[kind]


def drum(P, bar, j, kind, vel):
    s = pos(bar, j)
    part = {KICK: 'kick', SNARE: 'snare', HAT: 'hat', OHAT: 'hat', FTOM: 'tom', MTOM: 'tom', HTOM: 'tom'}.get(kind, 'cym')
    P.add(part, s, s + dlen(bar, kind), kind, vel)


def hats(P, bar, skip=()):
    """Gesloten hihat in rechte 8en, accent op de tel (referentie: hihat-accent 69-81 % op de tel)."""
    for j in range(0, 16, 2):
        if j not in skip:
            drum(P, bar, j, HAT, 100 if j % 4 == 0 else 64)


def riff_kicks(P, bar, pattern, extra=()):
    """Kick óp de tel (1 en 3) en mee met de open accenten van de riff op de 'en' (stompend, geen huppel)."""
    js = {0, 8} | set(extra)
    js |= {st for st, ln, nm, kind, fx in pattern if kind == 'o' and st % 2 == 0 and st not in (4, 12)}
    for j in sorted(js):
        drum(P, bar, j, KICK, 127 if j % 4 == 0 else 108)


def stomp_drums(P, bar, pattern, crash=False, fill=None, stop_at=None):
    """Snel deel: kick met de riff, zware snare op 2 en 4, 8e-hihats; fill = tomfill vanaf die 16e."""
    end = stop_at if stop_at is not None else (fill if fill is not None else 16)
    riff_kicks(P, bar, [x for x in pattern if x[0] < end])
    for j in (4, 12):
        if j < end:
            drum(P, bar, j, SNARE, 127)
    if crash:
        drum(P, bar, 0, CRASH, 116)
    hats(P, bar, skip=tuple(j for j in range(16) if (crash and j == 0) or j >= end))
    if fill is not None:
        tomfill(P, bar, fill, 16)
    if stop_at is not None:
        drum(P, bar, stop_at - 2, CRASH2, 116)
        drum(P, bar, stop_at - 2, KICK, 127)


def tomfill(P, bar, j0, j1):
    """16e-tomfill hoog -> laag, aanzwellend, kick onder de laatste klappen."""
    toms = [SNARE, HTOM, HTOM, MTOM, MTOM, FTOM, FTOM, FTOM]
    n = j1 - j0
    for k, j in enumerate(range(j0, j1)):
        kind = toms[min(len(toms) - 1, k * len(toms) // n)]
        drum(P, bar, j, kind, 100 + 26 * k // max(1, n - 1))
    drum(P, bar, j1 - 2, KICK, 120)


def sludge_drums(P, bar, pattern, crash=True, fill=None):
    """Traag (74) halftime: kick 1 en mee met de chugs, loodzware snare op 3, crash op 1, hihat 8en."""
    end = fill if fill is not None else 16
    js = {0} | {st for st, ln, nm, kind, fx in pattern if st in (4, 6) and st < end}
    for j in sorted(js):
        drum(P, bar, j, KICK, 127 if j % 4 == 0 else 108)
    if end > 8:
        drum(P, bar, 8, SNARE, 127)
        drum(P, bar, 8, KICK, 120)
    if crash:
        drum(P, bar, 0, CRASH, 112)
    hats(P, bar, skip=tuple(j for j in range(16) if (crash and j == 0) or j >= end))
    if fill is not None:
        tomfill(P, bar, fill, 16)


def beuk_drums(P, bar, pattern, fill=None):
    """Beuk: crash + kick op elke open klap, snare op 2 en 4, toms in de gaten."""
    end = fill if fill is not None else 16
    for st, ln, nm, kind, fx in pattern:
        if kind == 'o' and st < end:
            drum(P, bar, st, KICK, 127 if st % 4 == 0 else 110)
            if st % 4 == 0:
                drum(P, bar, st, CRASH if st == 0 else CRASH2, 116 if st == 0 else 104)
        elif kind == 'm' and st < end and st % 2 == 0:
            drum(P, bar, st, KICK, 104)
    for j in (4, 12):
        if j < end:
            drum(P, bar, j, SNARE, 127)
    for j, t in ((2, HTOM), (6, MTOM)):
        drum(P, bar, j, t, 96)
    if fill is not None:
        tomfill(P, bar, fill, 16)


def big_fill(P, bar):
    """De felle drumfill (maat 5 en 42): snare-16en die aanzwellen, dan toms hoog -> laag, crash op de volgende 1."""
    for j in range(0, 6):
        drum(P, bar, j, SNARE, 92 + 6 * j)
    drum(P, bar, 0, CRASH2, 110)
    drum(P, bar, 0, KICK, 127)
    for j, t in zip(range(6, 16), (HTOM, HTOM, HTOM, MTOM, MTOM, MTOM, FTOM, FTOM, FTOM, FTOM)):
        drum(P, bar, j, t, 104 + 2 * (j - 6))
    for j in (8, 12, 14):
        drum(P, bar, j, KICK, 124)


def dread_drums(P, bar, stop_at=None):
    """E: kick + floor tom op elke kwart (de Regi-pauken) en een crash erop."""
    for j in (0, 4, 8, 12):
        if stop_at is None or j < stop_at - 2:
            drum(P, bar, j, KICK, 127)
            drum(P, bar, j, FTOM, 112)
            drum(P, bar, j, CRASH if j == 0 else CRASH2, 116 if j == 0 else 100)
    if stop_at is not None:
        drum(P, bar, 8, SNARE, 127)
        drum(P, bar, stop_at - 2, KICK, 127)
        drum(P, bar, stop_at - 2, CRASH, 118)


def feedback(P, start, end, note, top=100, mod_after=None):
    """De versterker huilt: lange noot die aanzwelt (CC7) en pas laat gaat trillen."""
    P.add('fb', start, end, p(note), 110)
    steps, ln = 16, end - start
    for j in range(steps + 1):
        P.fx['fb'].append((start + j * ln * 3 // 4 // steps, 'vol', int(top * (0.15 + 0.85 * (j / steps) ** 1.5))))
    P.fx['fb'] += [(start, 'mod', 0), (start + (mod_after if mod_after is not None else ln // 2), 'mod', 8)]


def build():
    P = Parts()

    # ---- zwelling: C-powerchord glijdt erin (5 halve tonen omhoog), feedback, floor tom (de cry valt hier) --------
    for sd in ('gtrL', 'gtrR', 'bass'):
        P.add(sd, 0, BAR - S, p('C2'), 116, POWER if sd != 'bass' else None)
        P.fx[sd] += ramp(0, 2 * TPB, -5 * BU, 0, 16)
        for k in range(17):
            P.fx[sd].append((k * BAR // 16, 'vol', int(12 + 88 * (k / 16) ** 1.4)))
        P.fx[sd].append((INTRO * BAR, 'vol', 100))
    feedback(P, BAR // 4, BAR, 'G4', 70, BAR // 4)
    for k in range(8):
        drum(P, 0, 8 + k, FTOM, 64 + k * 7)

    # ---- intro: dreigende slide-riff, eerst één gitaar, dan beide + drums; stop -----------------------------------
    for i, pat in enumerate([I1, I2, I1, I4]):
        b = INTRO + i
        riff(P, b, pat, guitars=('L',) if i < 2 else ('L', 'R'))
        if i < 2:
            drum(P, b, 0, CRASH, 110)
            drum(P, b, 0, KICK, 127)
            drum(P, b, 8, SNARE, 124)
            drum(P, b, 8, KICK, 118)
            if i == 1:
                for j, t in ((12, HTOM), (13, HTOM), (14, MTOM), (15, FTOM)):
                    drum(P, b, j, t, 100 + 6 * (j - 12))
        else:
            sludge_drums(P, b, pat, crash=True)
            if i == 3:                                        # stop op de laatste 8e
                P.n['hat'] = [x for x in P.n['hat'] if not (pos(b, 14) <= x[0] < pos(b + 1, 0))]
                drum(P, b, 12, CRASH2, 118)
                drum(P, b, 12, KICK, 127)
    feedback(P, (INTRO + 2) * BAR, (INTRO + 3) * BAR + 3 * TPB, 'C5', 64, BAR)

    # ---- de felle drumfill + versnelling (maat 5, en dezelfde als maat 42 aan het eind van de loop) ---------------
    for b in (FILL0, FILL):
        big_fill(P, b)
        feedback(P, b * BAR, (b + 1) * BAR - S, 'G4', 84, TPB)

    # ---- A: stomp ---------------------------------------------------------------------------------------------------
    for i in range(8):
        b = A + i
        pat = RIFF_A[i % 4]
        riff(P, b, pat, guitars=('L', 'R'))
        stomp_drums(P, b, pat, crash=i % 2 == 0, fill=12 if i == 7 else None)

    # ---- B: groove, stop aan het eind -------------------------------------------------------------------------------
    for i in range(8):
        b = B + i
        pat = RIFF_B[i]
        riff(P, b, pat)
        if pat is BSTOP:
            for st, ln, nm, kind, fx in pat:
                drum(P, b, st, KICK, 127)
                drum(P, b, st, CRASH if st == 0 else CRASH2, 118 if st == 0 else 106)
            drum(P, b, 4, SNARE, 127)
            drum(P, b, 8, SNARE, 127)
        else:
            stomp_drums(P, b, pat, crash=i % 2 == 0)

    # ---- C: sludge + kreunende lead, tomfill naar D ---------------------------------------------------------------------
    for i in range(6):
        b = C + i
        pat = RIFF_C[i]
        riff(P, b, pat)
        sludge_drums(P, b, pat, crash=True, fill=8 if pat is CEND else None)
        if 1 <= i <= 5:
            lead(P, b, MOAN[i - 1])
    feedback(P, (C + 5) * BAR + 2 * TPB, (C + 6) * BAR - S, 'G4', 90, TPB // 2)

    # ---- D: beuk, met schreeuwende lead; tomfill naar A2 --------------------------------------------------------------
    for i in range(4):
        b = D + i
        pat = RIFF_D[i]
        riff(P, b, pat)
        beuk_drums(P, b, pat, fill=12 if pat is D4 else None)
        lead(P, b, SCREAM[i], vel=108)

    # ---- A2: riff A + lead-climax, stop aan het eind ----------------------------------------------------------------------
    for i in range(8):
        b = A2 + i
        pat = A4S if i == 7 else RIFF_A[i % 4]
        riff(P, b, pat)
        stomp_drums(P, b, pat, crash=i % 2 == 0 or i >= 6, stop_at=14 if i == 7 else None)
        lead(P, b, CLIMAX[i], vel=106)

    # ---- E: Regi-dreiging (74), stop, dan de fill ----------------------------------------------------------------------------
    riff(P, EE, E1)
    dread_drums(P, EE)
    riff(P, EE + 1, E2)
    dread_drums(P, EE + 1, stop_at=14)
    feedback(P, EE * BAR, (EE + 1) * BAR + 3 * TPB, 'C5', 72, BAR)

    for k in P.n:
        P.n[k] = dedupe(P.n[k])
    P.written = {k: [list(x) for x in v] for k, v in P.n.items()}
    return P


# ---- controles: anti-ska/anti-Bowser's Castle (blijven) + 'niet saai' (nieuw in v7) ---------------------------------
SCALE = {0, 1, 3, 5, 6, 7, 8, 10}          # C-klein blues/frygisch: C Db Eb F Gb G Ab Bb (geen E = grote terts)
MEL = ('gtrL', 'gtrR', 'bass', 'lead', 'fb')


def section_of(tick):
    bar = tick // BAR
    return next(nm for nm, a, b in SECTIONS if a <= bar < b)


def stoner_checks(P):
    """Faalt (AssertionError) als het nummer weer richting ska/surf/Bowser's Castle schuift (v1-v5) of weer saai en
    statisch wordt (v6). Geeft de meetwaarden terug."""
    W = P.written
    fails, rep = [], {}
    # ===== anti-ska / anti-vrolijk =====
    # 1. toonladder: alleen C-klein pentatonisch/blues/frygisch, geen grote terts (E)
    for k in ('gtrL', 'bass', 'lead', 'fb'):
        bad = sorted({n[2] % 12 for n in W[k]} - SCALE)
        if bad:
            fails.append('%s: toonklassen buiten C-klein blues/frygisch: %s' % (k, bad))
    # 2. lead: geen grote terts omhoog; 3. geen chromatische Mario-loopjes (4+ noten in halve tonen dezelfde kant op)
    for k in ('gtrL', 'bass', 'lead'):
        ns = sorted(W[k])
        line = [min(n[2] for n in ns if n[0] == s) for s in sorted(set(n[0] for n in ns))]
        st = [b - a for a, b in zip(line, line[1:]) if b != a]
        if k == 'lead' and any(x == 4 for x in st):
            fails.append('lead: sprong van een grote terts omhoog (vrolijk)')
        runs = sum(1 for x, y, z in zip(st, st[1:], st[2:]) if abs(x) == 1 and x == y == z)
        if runs:
            fails.append('%s: %d chromatische loopjes van 4+ noten' % (k, runs))
    # 4. recht 16e-raster (geen swing/huppel)
    for k in P.n:
        if k != 'fb' and any(n[0] % S for n in W[k]):
            fails.append('%s: noten naast het rechte 16e-raster (swing/huppel)' % k)
    # 5. hihat: geen open hihat, accent op de tel
    if any(n[2] == OHAT for n in W['hat']):
        fails.append('open hihat (ska/disco)')
    on = [n[3] for n in W['hat'] if n[0] % TPB == 0]
    off = [n[3] for n in W['hat'] if n[0] % TPB]
    if off and on and max(off) >= min(on):
        fails.append('hihat op de en even hard als op de tel (off-beat-accent)')
    # 6. geen skank (aanslag naast de tel terwijl de tel stil was) en het accent óp de tel
    for k in ('gtrL', 'bass', 'lead'):
        ns = sorted(W[k])
        sounding = lambda t: any(n[0] <= t < n[1] for n in ns)
        offb = [n for n in ns if n[0] % TPB]
        skank = [n for n in offb if not sounding(n[0] - n[0] % TPB)]
        if skank:
            fails.append('%s: %d off-beat-stoten na een stille tel (ska/skank), bijv. maat %d' % (
                k, len(skank), skank[0][0] // BAR))
        if k != 'lead' and offb and max(n[3] for n in offb) >= min(n[3] for n in ns if n[0] % TPB == 0):
            fails.append('%s: off-beat even hard als op de tel' % k)
        rep[k + ' naast de tel'] = len(offb) / len(ns)
    # 7. stompend: kick vooral op de tel, zware snare op 2 en 4 in de snelle riffmaten
    kk = W['kick']
    rep['kick op de tel'] = sum(1 for n in kk if n[0] % TPB == 0) / len(kk)
    if rep['kick op de tel'] < 0.5:
        fails.append('kick: maar %.0f%% op de tel' % (100 * rep['kick op de tel']))
    sn = W['snare']
    fast_riff_bars = [b for nm, a, e in SECTIONS if FAMILY[nm] in 'AB' for b in range(a, e)]
    miss = [b for b in fast_riff_bars if not all(any(n[0] == pos(b, j) and n[3] >= 120 for n in sn) for j in (4,))]
    if miss:
        fails.append('snelle riffmaten zonder zware snare op 2: %s' % miss)
    rep['snare op 2/4 (snel)'] = sum(1 for n in sn if n[0] // BAR in fast_riff_bars and n[0] % (2 * TPB) == TPB) / max(
        1, sum(1 for n in sn if n[0] // BAR in fast_riff_bars))
    # 8. bas = exact de gitaarriff
    g = {(n[0], n[2]) for n in W['gtrL']}
    bs = {(n[0], n[2]) for n in W['bass']}
    if g - bs:
        fails.append('bas verdubbelt de gitaar niet op %d aanslagen' % len(g - bs))
    # 9. tempo: traag 66-80 (slopend), snel 124-136 (Jordi: ±130)
    for t, b in TEMPO:
        if not (66 <= b <= 80 or 124 <= b <= 136):
            fails.append('tempo %d bpm buiten 66-80 / 124-136' % b)

    # ===== niet saai (v6: 'te saai, statisch, eentonig') =====
    loop = [(nm, a, b) for nm, a, b in SECTIONS if a >= LOOP]
    loop_s = secs(END * BAR) - secs(LOOP * BAR)
    # 10. minstens 3 verschillende riffs: secties waarvan geen enkele maat (toonhoogte + ritme) in een eerdere zit
    def bars_of(a, b):
        out = set()
        for bar in range(a, b):
            pat = tuple(sorted((n[0] - bar * BAR, n[2], n[4]) for n in W['gtrL'] if bar * BAR <= n[0] < (bar + 1) * BAR))
            if pat:
                out.add(pat)
        return out
    seen, riffs = set(), []
    for nm, a, b in loop:
        pats = bars_of(a, b)
        if pats and not (pats & seen):
            riffs.append(nm)
        seen |= pats
    rep['verschillende riffs in de loop'] = len(riffs)
    rep['verschillende maatpatronen in de loop'] = len(seen)
    if len(riffs) < 3:
        fails.append('maar %d verschillende riffs in de loop (%s)' % (len(riffs), riffs))
    # 11. minstens 2 tempowissels per loop (incl. de terugsprong)
    tl = [b for t, b in TEMPO if t >= LOOP * BAR]
    changes = sum(1 for x, y in zip(tl, tl[1:] + tl[:1]) if x != y)
    rep['tempowissels per loop'] = changes
    if changes < 2:
        fails.append('maar %d tempowissels per loop' % changes)
    # 12. stop of fill vóór elke riffwissel: in de laatste tel alle melodische sporen >= een 8e stil, of >= 3 tom/
    #     snare-klappen op de 16en
    bounds = [a for nm, a, b in SECTIONS if a > 0] + [END]
    for t in bounds:
        if t == END or FAMILY[section_of(t * BAR)] != FAMILY[section_of(t * BAR - 1)]:
            w0, w1 = t * BAR - TPB, t * BAR
            silent = max((sum(1 for j in range(w0, w1, S) if all(not (n[0] <= j < n[1]) for k in MEL for n in W[k]))), 0)
            hits = len({n[0] for n in W['tom'] + W['snare'] if w0 <= n[0] < w1})
            if silent < 2 and hits < 3:
                fails.append('geen stop of fill vóór maat %d' % t)
    # 13. palm-mute: aandeel palm-muted onder de snelle aanslagen (8en/16en) van de gitaar
    gl = sorted(W['gtrL'])
    starts = sorted(set(n[0] for n in gl))
    nxt = {s: b for s, b in zip(starts, starts[1:])}
    quick = [n for n in gl if n[0] >= LOOP * BAR and nxt.get(n[0], 10 ** 9) - n[0] <= E]
    pmq = sum(1 for n in quick if n[4] == PM) / max(1, len(quick))
    pm_all = sum(1 for n in gl if n[4] == PM) / len(gl)
    rep['palm-mute onder de 8en/16en'] = pmq
    rep['palm-mute van alle aanslagen'] = pm_all
    if pmq < 0.4 or pm_all < 0.25:
        fails.append('te weinig palm-mutes (%.0f%% van de 8en/16en, %.0f%% totaal)' % (100 * pmq, 100 * pm_all))
    # 14. slides en bends (referentie-bas: 19-41 slides/min)
    sl = [t for t, k in P.slides if t >= LOOP * BAR]
    rep['slides/bends per minuut (gitaar)'] = 60 * len(sl) / loop_s
    if 60 * len(sl) / loop_s < 15:
        fails.append('te weinig slides/bends: %.0f per minuut' % (60 * len(sl) / loop_s))
    # 15. geen lange aangehouden akkoorden (v6): aandeel gitaartijd in noten > 2 tellen, en gemiddelde afstand
    long_t = sum(n[1] - n[0] for n in gl if n[1] - n[0] > 2 * TPB and n[0] >= LOOP * BAR)
    all_t = sum(n[1] - n[0] for n in gl if n[0] >= LOOP * BAR)
    rep['aandeel lange akkoorden'] = long_t / all_t
    if long_t / all_t > 0.10:
        fails.append('%.0f%% van de gitaartijd in akkoorden > 2 tellen (statisch)' % (100 * long_t / all_t))
    ioi = [b - a for a, b in zip(starts, starts[1:]) if a >= LOOP * BAR]
    rep['gem. afstand gitaaraanslagen (tel)'] = sum(ioi) / len(ioi) / TPB
    if sum(ioi) / len(ioi) > 0.75 * TPB:
        fails.append('gitaar te weinig actief (gem. %.2f tel tussen aanslagen)' % (sum(ioi) / len(ioi) / TPB))
    # 16. wilde drums: crash op elke sectiestart, gem. >= 1 crash per 2 maten, >= 3 tomfills per loop
    cy = W['cym']
    for nm, a, b in loop:
        if FAMILY[nm] != 'F' and not any(n[0] == a * BAR for n in cy):
            fails.append('geen crash op de start van %s' % nm)
    ncr = sum(1 for n in cy if n[0] >= LOOP * BAR)
    rep['crashes per maat'] = ncr / (END - LOOP)
    if ncr < (END - LOOP) / 2:
        fails.append('te weinig crash-accenten (%d in %d maten)' % (ncr, END - LOOP))
    fills = 0
    for bar in range(LOOP, END):
        for beat in range(4):
            w0 = pos(bar, 4 * beat)
            if len({n[0] for n in W['tom'] if w0 <= n[0] < w0 + TPB}) >= 3:
                fills += 1
                break
    rep['tomfills per loop'] = fills
    if fills < 3:
        fails.append('maar %d tomfills per loop' % fills)
    assert not fails, 'stoner_checks:\n  ' + '\n  '.join(fails)
    return rep


def write_voicegroup():
    """grounded_gm + feedback (27), palm-mute (28), powerchord (30), lead (31), synthbas (34), drumkit (127)."""
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = ("@ Project Grounded: grounded_gm voor Battle! Heatran v7 (Kyuss op de GBA). "
                'Gegenereerd door tools/grounded/heatran_theme.py.')
    lines[1] = ('@ 27 = feedback (sd90 overdrive), 28 = palm-mute (keysplit_heatran), 30 = powerchord (keysplit_heatran, '
                'één sample per riffnoot), 31 = fuzzlead (keysplit_heatran_lead), 34 = synthbas, 127 = drumkit.')
    lines[2] = 'voice_group %s' % VG
    repl = {
        '@ 27': '\tvoice_directsound 60, 0, DirectSoundWaveData_sd90_classical_overdrive_guitar, 255, 0, 255, %d  @ 27' % REL[FB],
        '@ 28': '\tvoice_keysplit voicegroup_heatran_pm_keysplit, keysplit_heatran  @ 28',
        '@ 30': '\tvoice_keysplit voicegroup_heatran_power_keysplit, keysplit_heatran  @ 30',
        '@ 31': '\tvoice_keysplit voicegroup_heatran_lead_keysplit, keysplit_heatran_lead  @ 31',
        '@ 34': '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_synth_bass, 255, 0, 255, %d  @ 34' % REL[BASS],
        '@ 127': '\tvoice_keysplit_all voicegroup_heatran_drumset  @ 127',
    }
    out = []
    for l in lines:
        tag = '@' + l.rsplit('@', 1)[1] if '@' in l and l.startswith('\t') else None
        out.append(repl.get(tag.strip() if tag else None, l))
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))

    keys = (36, 37, 39, 41, 42, 43, 44, 46, 48)               # keysplit_heatran (sound/keysplit_tables.inc)
    body = ''.join('\tvoice_directsound %d, 0, DirectSoundWaveData_heatran_st_pw_%d, 255, 0, 255, %d\n'
                   % (k, k, REL[POWER]) for k in keys)
    open('sound/voicegroups/keysplits/heatran_power.inc', 'w').write(
        '@ Project Grounded: Battle! Heatran v6/v7, powerchord (grondtoon+kwint+octaaf) per riffnoot (heatran_samples.py),\n'
        '@ tabel keysplit_heatran (sound/keysplit_tables.inc). Gegenereerd door tools/grounded/heatran_theme.py.\n'
        'voice_group heatran_power_keysplit\n' + body)
    body = ''.join('\tvoice_directsound %d, 0, DirectSoundWaveData_heatran_st_pm_%d, 255, 0, 255, %d\n'
                   % (k, k, REL[PM]) for k in keys)
    open('sound/voicegroups/keysplits/heatran_pm.inc', 'w').write(
        '@ Project Grounded: Battle! Heatran v7, palm-mute-chug (grondtoon+kwint) per riffnoot (heatran_samples.py),\n'
        '@ tabel keysplit_heatran (sound/keysplit_tables.inc). Gegenereerd door tools/grounded/heatran_theme.py.\n'
        'voice_group heatran_pm_keysplit\n' + body)
    body = ''.join('\tvoice_directsound %d, 0, DirectSoundWaveData_heatran_st_lead_%d, 255, 0, 255, %d\n'
                   % (k, k, REL[LEAD]) for k in (60, 67))
    open('sound/voicegroups/keysplits/heatran_lead.inc', 'w').write(
        '@ Project Grounded: Battle! Heatran v6/v7, fuzzlead C4/G4 (heatran_samples.py), tabel keysplit_heatran_lead.\n'
        '@ Gegenereerd door tools/grounded/heatran_theme.py.\n'
        'voice_group heatran_lead_keysplit\n' + body)
    kit = [   # vanaf noot 36; alleen Gen 3-samples, alles DirectSound (geen PSG-drums)
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 242',
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 242',
        'voice_directsound_no_resample 60, 70, DirectSoundWaveData_unknown_close_hihat, 255, 127, 0, 188',
        'voice_directsound_no_resample 60, 70, DirectSoundWaveData_unknown_open_hihat, 255, 242, 141, 0',
        'voice_directsound_no_resample 30, 54, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 216',
        'voice_directsound 48, 44, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 204',
        'voice_directsound 54, 64, DirectSoundWaveData_unused_sc55_tom, 255, 216, 77, 204',
        'voice_directsound 60, 79, DirectSoundWaveData_unused_sc55_tom, 255, 204, 77, 204',
        'voice_directsound_no_resample 60, 14, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165',
    ]
    open('sound/voicegroups/drumsets/heatran.inc', 'w').write(
        '@ Project Grounded: drumkit voor Battle! Heatran v6/v7 (heatran_theme.py): de Gen 3-drums uit rs_drumset zonder\n'
        '@ PSG-noten: 36 kick, 37 snare (dof), 38 hihat, 39 open hihat (ongebruikt), 40 crash, 41-43 toms\n'
        '@ laag/midden/hoog, 44 trinity-crash (blikkerig).\n'
        'voice_group heatran_drumset, 36\n' + ''.join('\t%s\n' % k for k in kit) + '\n')
    inc = open('sound/voice_groups.inc').read()
    line = '.include "sound/voicegroups/keysplits/heatran_pm.inc"\n'
    if line not in inc:
        anchor = '.include "sound/voicegroups/keysplits/heatran_power.inc"\n'
        assert anchor in inc
        open('sound/voice_groups.inc', 'w').write(inc.replace(anchor, anchor + line))


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


LAYOUT = [  # naam, programma, volume, kanaal, pan, vaste bend
    ('gtrL', POWER, 100, 0, 34, 0),
    ('gtrR', POWER, 90, 1, 94, R_BEND),
    ('bass', BASS, 100, 2, 64, 0),
    ('lead', LEAD, 84, 3, 70, 0),
    ('fb', FB, 64, 4, 54, 0),
]
DRUM_VOL = 112
DRUM_PARTS = ('kick', 'snare', 'hat', 'cym', 'tom')


def add_track(out, notes, prog, vol, ch, pan, fx):
    t = mido.MidiTrack()
    t.append(mido.Message('program_change', channel=ch, program=prog, time=0))
    t.append(mido.Message('control_change', channel=ch, control=7, value=vol, time=0))
    t.append(mido.Message('control_change', channel=ch, control=10, value=pan, time=0))
    t.append(mido.Message('control_change', channel=ch, control=20, value=BENDR, time=0))   # BENDR 12 halve tonen
    ev = []
    for tk, kind, v in fx:     # volgorde op één tick: note-off, controllers, programma, note-on
        if kind == 'vol':
            ev.append((tk, 1, mido.Message('control_change', channel=ch, control=7, value=max(0, min(127, v * vol // 100)))))
        elif kind == 'mod':
            ev.append((tk, 1, mido.Message('control_change', channel=ch, control=1, value=v)))
        elif kind == 'bend':
            ev.append((tk, 1, mido.Message('pitchwheel', channel=ch, pitch=max(-8192, min(8191, v)))))
    cur = prog
    for n in sorted(notes):
        s, e, nt, v = n[:4]
        pr = n[4] if len(n) > 4 else prog
        if pr != cur:                                          # programmawissel per noot (open <-> palm-mute)
            ev.append((s, 2, mido.Message('program_change', channel=ch, program=pr)))
            cur = pr
        ev.append((e, 0, mido.Message('note_off', channel=ch, note=nt, velocity=0)))
        ev.append((s, 3, mido.Message('note_on', channel=ch, note=nt, velocity=max(1, min(127, int(v))))))
    last = 0
    for tk, _, msg in sorted(ev, key=lambda x: (x[0], x[1])):
        t.append(msg.copy(time=tk - last))
        last = tk
    out.tracks.append(t)


def save(P, path):
    out = mido.MidiFile(type=1, ticks_per_beat=TPB)
    cond = mido.MidiTrack()
    ev = [(t, mido.MetaMessage('set_tempo', tempo=int(round(60e6 / b)), time=0)) for t, b in TEMPO]
    ev += [(LOOP * BAR, mido.MetaMessage('marker', text='[', time=0)), (END * BAR, mido.MetaMessage('marker', text=']', time=0))]
    last = 0
    for t, msg in sorted(ev, key=lambda x: (x[0], x[1].type != 'marker')):   # op het loopbegin: eerst het label
        cond.append(msg.copy(time=t - last))
        last = t
    out.tracks.append(cond)
    for name, prog, vol, ch, pan, bend in LAYOUT:
        fx = fx_events(P.fx[name], P.n[name], bend)
        if bend:
            fx = [(0, 'bend', bend)] + [x for x in fx if not (x[0] == 0 and x[1] == 'bend')]
        if any(x[1] == 'vol' for x in P.fx[name]):              # CC7 op het loopbegin opnieuw zetten
            fx = [x for x in fx if not (x[0] == LOOP * BAR and x[1] == 'vol')] + [(LOOP * BAR, 'vol', 100)]
        fx = [x for x in fx if not (x[0] == LOOP * BAR and x[1] in ('bend', 'mod'))]
        fx += [(LOOP * BAR, 'bend', bend), (LOOP * BAR, 'mod', 0)]   # bend/vibrato op het loopbegin terug
        # programma op het loopbegin vastzetten (de loop eindigt misschien op een palm-mute)
        add_track(out, P.n[name], prog, vol, ch, pan, fx)
        if name in ('gtrL', 'gtrR'):
            tr = out.tracks[-1]
            first = next((n for n in sorted(P.n[name]) if n[0] >= LOOP * BAR), None)
            if first is not None and len(first) > 4:
                # het eerste loopnoot-programma staat al op de looptick als de noot ervóór een ander programma had;
                # zo niet, dan alsnog expliciet zetten
                tick, has = 0, False
                for msg in tr:
                    tick += msg.time
                    if tick == LOOP * BAR and msg.type == 'program_change':
                        has = True
                if not has:
                    insert_at(tr, LOOP * BAR, mido.Message('program_change', channel=ch, program=first[4]))
    add_track(out, sorted(sum((P.n[k] for k in DRUM_PARTS), [])), DRUMS, DRUM_VOL, 9, 64, P.fx['drums'])
    written = {k for k, *_ in LAYOUT} | set(DRUM_PARTS)
    assert not [k for k in P.n if P.n[k] and k not in written], 'partij niet weggeschreven'
    out.save(path)


def insert_at(track, at, msg):
    """msg op tick at invoegen, vóór de eerste note_on op die tick."""
    tick, i = 0, 0
    while i < len(track):
        nt = tick + track[i].time
        if nt > at or (nt == at and track[i].type == 'note_on' and track[i].velocity):
            break
        tick = nt
        i += 1
    if i < len(track):
        nxt = track[i]
        track.insert(i, msg.copy(time=at - tick))
        track[i + 1] = nxt.copy(time=nxt.time - (at - tick))
    else:
        track.insert(i - 1 if track[-1].type == 'end_of_track' else i, msg.copy(time=at - tick))


def fit_legato(ns, tail):
    """Gitaar/bas: elke noot eindigt `tail` ticks vóór de volgende aanslag in het spoor (de release vult het gat:
    klinkt legato, kost geen tweede kanaal). Programma (5e veld) blijft staan."""
    ns = sorted(ns)
    starts = sorted(set(n[0] for n in ns))
    out = []
    for n in ns:
        nxt = next((t for t in starts if t > n[0]), None)
        e = n[1] if nxt is None else min(n[1], max(n[0] + 6, nxt - tail))
        out.append([n[0], e] + list(n[2:]))
    return out


def main():
    P = build()
    rep = stoner_checks(P)
    write_voicegroup()
    rel = releases(VG)
    tail = {'gtrL': release_ticks(REL[POWER], TPB, FAST) + 2, 'gtrR': release_ticks(REL[POWER], TPB, FAST) + 2,
            'bass': release_ticks(REL[BASS], TPB, FAST) + 2, 'lead': release_ticks(REL[LEAD], TPB, FAST) + 2,
            'fb': release_ticks(REL[FB], TPB, FAST) + 2}
    for k in DRUM_PARTS:
        tail[k] = 0                                            # drums: de noot zelf = de echte lengte
    for k in ('gtrL', 'gtrR', 'bass'):
        P.n[k] = fit_legato(P.n[k], tail[k])
    for k in ('lead', 'fb'):
        P.n[k] = detach(P.n[k], tail[k])
    # zelfde toonhoogte mag in één spoor niet overlappen (de note-off van de eerste zou de tweede afkappen)
    for k in P.n:
        ns = sorted(P.n[k])
        for i, x in enumerate(ns):
            nxt = next((y[0] for y in ns[i + 1:] if y[2] == x[2] and y[0] >= x[0]), None)
            if nxt is not None and nxt < x[1]:
                x[1] = max(x[0] + 6, nxt - 1)
        P.n[k] = ns
    # palm-mutes kort laten klinken met hun eigen (korte) release: tail per noot
    pm_tail = release_ticks(REL[PM], TPB, FAST) + 2
    occ = {k: [list(n) for n in P.n[k]] for k in P.n}
    for k in ('gtrL', 'gtrR'):                                 # stemverdeler rekent per noot met de juiste release
        occ[k] = [[n[0], n[1] - tail[k] + pm_tail] + list(n[2:]) if len(n) > 4 and n[4] == PM else n for n in occ[k]]
    order = ['bass', 'gtrL', 'kick', 'snare', 'lead', 'cym', 'tom', 'hat', 'gtrR', 'fb']
    kept = allocate({k: occ[k] for k in order}, order, tail, max_voices=11)
    print('tail (ticks bij %d bpm):' % FAST, {k: v for k, v in tail.items() if v}, 'palm-mute', pm_tail)
    for k in order:
        n = len(P.n[k])
        keep = {(x[0], x[2]) for x in kept[k]}
        P.n[k] = [x for x in P.n[k] if (x[0], x[2]) in keep]
        print('  %-6s %4d noten, %3d vallen weg (%.1f%%)' % (k, n, n - len(P.n[k]), 100 * (n - len(P.n[k])) / max(n, 1)))
    save(P, OUT)
    print(OUT, '%.1f s intro, %.1f s loop (totaal %.1f s)' % (secs(LOOP * BAR), secs(END * BAR) - secs(LOOP * BAR), secs(END * BAR)))
    for nm, a, b in SECTIONS:
        print('  %-11s maat %2d-%2d  %3d bpm  %6.1f - %6.1f s' % (nm, a, b - 1, bpm_at(a * BAR), secs(a * BAR), secs(b * BAR)))
    print('stoner_checks OK:')
    for k, v in rep.items():
        print('  %-38s %.2f' % (k, v))


if __name__ == '__main__':
    main()
