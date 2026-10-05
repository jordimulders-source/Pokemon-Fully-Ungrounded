#!/usr/bin/env python3
"""Project Grounded: "Battle! Heatran" v5, eigen compositie: Kyuss' 'Odyssey' (...And the Circus Leaves Town) op een
Game Boy Advance, alsof Kyuss de originele Ruby/Sapphire-baasmuziek van Heatran inspeelde.

Jordi (v5): bouw het op 'Odyssey': (1) intro/strofe = slow sludge (~75 bpm), lome, zware lopende bas- en gitaarriff;
(2) tempowissel naar een snelle, opzwepende desert pump (~135 bpm); (3) afwisselen tussen de snikhete trage stukken en
de agressieve snelle stukken. Klank: GBA/Gen 3-soundfont, geen studio: crunchy low-bitrate gitaren in C-standard,
doffe gecomprimeerde synthbas die de gitaar volgt, doffe Gen 3-drums (doffe snare, blikkerige crash).

Instrumenten (voicegroup grounded_heatran):
  28/29/30  slaggitaar palm-mute / riffnoot / powerchord: eigen Gen 3-achtige samples per riffnoot in C-standard
            (heatran_samples.py: FluidR3 distortion, hard gecomprimeerd, 13.379 Hz, 8 bit, korte loop)
  31        leadgitaar = sd90_classical_distortion_guitar_high (de echte Gen 3-gitaar, Frontier Brain/FRLG)
  27        feedback   = sd90_classical_overdrive_guitar
  34        bas        = sc88pro_synth_bass (de doffe Gen 3-synthbas), speelt exact de gitaarriff
  81        PSG-blokgolf: verdubbelt het motief in het tweede snelle deel (kost geen DirectSound-kanaal)
  127       drumset heatran: alleen Gen 3-samples (rnd_kick, rnd_snare, hihats, orchestra crash, trinity crash,
            sc55-toms), geen PSG-drums
Het Heatran-motief: C - Eb - F - Gb - F - Eb - C (bluesy b5), snel in de pump, traag en kreunend in de sludge.

  maat 0-1   intro (76 bpm): powerchord zwelt aan + feedback, toms rommelen; maat 1 de dalende riff (G-Gb-F-Eb)
Loop:
  A   2-9    SLUDGE 1 (76, swing): de lome riff; eerst alleen gitaar links + bas + drums, vanaf 6 beide gitaren
  ->  10-11  opbouwende versnelling per tel 76 -> 130 (chugs, snareroffel 8en -> 16en)
  B   12-28  DESERT PUMP 1 (136): beukende riff; vanaf 20 het motief op de leadgitaar; 28 = de stop (abrupt)
  C   29-36  SLUDGE 2 (76): de riff met het motief traag en kreunend (bends); tom-fill in maat 36
  D   37-52  DESERT PUMP 2 (136): tom-groove + motief (lead + PSG), climax 45-48, riff 49-51, maat 52 vertraagt
             tel voor tel (136 -> 80) met de dalende riff naar de sludge van A
Gebruikt musiclib.py; zie MUZIEK.md. Gebruik: python3 tools/grounded/heatran_samples.py; python3 tools/grounded/heatran_theme.py"""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks

OUT = 'sound/songs/midi/mus_grounded_vs_heatran.mid'
VG = 'grounded_heatran'
TPB = 96
SLOW, FAST = 76, 136
S = TPB // 4                   # een 16e
E = TPB // 2                   # een 8e
BAR = TPB * 4
SWING = 8                      # sludge: de 'en' van elke tel 8 ticks later (lome shuffle)
LAY = 3                        # snare iets achter de tel
FB, MUTE, NOTE, POWER, LEAD, BASS, PSG, DRUMS = 27, 28, 29, 30, 31, 34, 81, 127
R_BEND = 3 * 128               # rechter gitaar ±9 cent hoger (dubbele opname)
# drumkit (drumsets/heatran.inc, vanaf noot 36)
KICK, SNARE, HAT, OHAT, CRASH, FTOM, MTOM, HTOM, CRASH2 = range(36, 45)
REL = {POWER: 160, NOTE: 160, MUTE: 120, LEAD: 180, FB: 200}   # release per eigen gitaarinstrument

INTRO_DESC, A, ACC, B, STOP_B, C, D, CLIMAX, RIFF_D, RIT, END = 1, 2, 10, 12, 28, 29, 37, 45, 49, 52, 53

N = {'C': 0, 'Db': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'Gb': 6, 'G': 7, 'Ab': 8, 'A': 9, 'Bb': 10, 'B': 11}


def p(name):
    """'C2' -> midi-noot (C4 = 60)."""
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


# ---- tempo ---------------------------------------------------------------------------------------------------------
TEMPO = [(0, SLOW)]
ACC_BPM = (76, 80, 86, 94, 102, 112, 122, 130)               # versnelling per tel (maat 10-11)
for i, bpm in enumerate(ACC_BPM):
    TEMPO.append((ACC * BAR + i * TPB, bpm))
TEMPO += [(B * BAR, FAST), (C * BAR, SLOW), (D * BAR, FAST)]
for i, bpm in enumerate((124, 108, 92, 80)):                 # ritardando in de laatste maat
    TEMPO.append((RIT * BAR + i * TPB, bpm))
TEMPO.insert(1, (A * BAR, SLOW))                              # loopbegin weer traag (direct na het label)


def bpm_at(tick):
    return [b for t, b in TEMPO if t <= tick][-1]


def secs(tick):
    s, pts = 0.0, TEMPO + [(10 ** 9, 0)]
    for (t0, b), (t1, _) in zip(pts, pts[1:]):
        if tick <= t0:
            break
        s += (min(tick, t1) - t0) / TPB * 60 / b
    return s


def slow(bar):
    return bpm_at(bar * BAR) <= 80


def pos(bar, j):
    """16e-positie j in maat bar; in de sludge swingt de 'en' van elke tel."""
    return bar * BAR + j * S + (SWING if slow(bar) and j % 4 == 2 else 0)


# ---- riffs: (16e, lengte in 16en, soort, noot[, 's' = erin glijden]) ---------------------------------------------
# 'P' = powerchord (1 sample), 'N' = riffnoot (+ octaaf), 'M' = palm-mute-chug
# SLUDGE (Odyssey-langzaam): hangende C, loom loopje naar de b5, terug naar de C
S1 = [(0, 4, 'P', 'C2'), (4, 2, 'N', 'C2'), (6, 2, 'N', 'Eb2'), (8, 3, 'P', 'F2', 's'), (11, 1, 'N', 'Gb2'),
      (12, 4, 'P', 'F2')]
S2 = [(0, 3, 'P', 'Eb2'), (3, 3, 'N', 'C2'), (6, 2, 'N', 'Eb2'), (8, 8, 'P', 'C2')]
S4 = [(0, 4, 'P', 'G2'), (4, 4, 'P', 'Gb2'), (8, 4, 'P', 'F2'), (12, 2, 'N', 'Eb2'), (14, 2, 'N', 'C2')]
SLUDGE = [S1, S2, S1, S4] * 2
DESC = [(0, 4, 'P', 'G2'), (4, 4, 'P', 'Gb2'), (8, 4, 'P', 'F2'), (12, 4, 'P', 'Eb2')]
# DESERT PUMP (Odyssey-snel): beukende C-stoot + chugs, dan Eb/F/Gb erachteraan
F1 = [(0, 2, 'P', 'C2'), (2, 2, 'M', 'C2'), (4, 2, 'M', 'C2'), (6, 2, 'M', 'C2'), (8, 2, 'P', 'Eb2'),
      (10, 2, 'N', 'C2'), (12, 2, 'P', 'F2'), (14, 2, 'P', 'Gb2')]
F2 = [(0, 2, 'P', 'C2'), (2, 2, 'M', 'C2'), (4, 2, 'M', 'C2'), (6, 2, 'M', 'C2'), (8, 4, 'P', 'G2'),
      (12, 2, 'P', 'F2'), (14, 2, 'N', 'Eb2')]
F4 = [(0, 4, 'P', 'Eb2'), (4, 4, 'P', 'F2'), (8, 4, 'P', 'Gb2'), (12, 4, 'P', 'G2')]
PUMP = [F1, F2, F1, F4]
X1 = [(0, 2, 'P', 'C2'), (2, 2, 'M', 'C2'), (4, 2, 'P', 'C2'), (6, 2, 'M', 'C2'), (8, 4, 'P', 'Eb2'), (12, 4, 'P', 'F2')]
X2 = [(0, 2, 'P', 'C2'), (2, 2, 'M', 'C2'), (4, 2, 'P', 'C2'), (6, 2, 'M', 'C2'), (8, 4, 'P', 'Gb2'), (12, 4, 'P', 'G2')]
ACCEL = [[(k, 2, 'M', 'C2') for k in range(0, 16, 2)],
         [(k, 2, 'M', 'C2') for k in range(0, 8, 2)] + [(8, 2, 'P', 'Eb2'), (10, 2, 'P', 'F2'), (12, 2, 'P', 'Gb2'),
                                                        (14, 2, 'P', 'G2')]]
STOP = [(0, 8, 'P', 'C2')]

# ---- het Heatran-motief (lead): (16e, lengte, noot, fx) 'b' = bend van 2 halve tonen eronder, 'v' = vibrato -------
MOTIF = [
    [(0, 4, 'C4', ''), (4, 2, 'Eb4', ''), (6, 2, 'F4', ''), (8, 4, 'Gb4', 'v'), (12, 2, 'F4', ''), (14, 2, 'Eb4', '')],
    [(0, 10, 'C4', 'v'), (10, 2, 'Bb3', ''), (12, 4, 'C4', '')],
    [(0, 4, 'Eb4', ''), (4, 2, 'F4', ''), (6, 2, 'G4', ''), (8, 4, 'Bb4', 'b'), (12, 2, 'G4', ''), (14, 2, 'F4', '')],
    [(0, 6, 'Gb4', 'v'), (6, 2, 'F4', ''), (8, 4, 'Eb4', ''), (12, 4, 'C4', '')],
    [(0, 4, 'C4', ''), (4, 2, 'Eb4', ''), (6, 2, 'F4', ''), (8, 4, 'Gb4', 'v'), (12, 2, 'F4', ''), (14, 2, 'Eb4', '')],
    [(0, 10, 'C4', 'v'), (10, 2, 'Eb4', ''), (12, 4, 'F4', '')],
    [(0, 4, 'G4', 'b'), (4, 4, 'Bb4', ''), (8, 4, 'C5', 'bv'), (12, 4, 'Bb4', '')],
    [(0, 8, 'G4', 'v'), (8, 4, 'Gb4', ''), (12, 4, 'F4', '')],
]
# traag en kreunend in de sludge: langere bends op de lange noten
MOAN = [
    [(0, 4, 'C4', 'b'), (4, 2, 'Eb4', ''), (6, 2, 'F4', ''), (8, 6, 'Gb4', 'bv'), (14, 2, 'F4', '')],
    [(0, 12, 'Eb4', 'bv'), (12, 4, 'C4', '')],
    [(0, 4, 'Eb4', ''), (4, 2, 'F4', ''), (6, 2, 'G4', ''), (8, 8, 'Bb4', 'bv')],
    [(0, 6, 'Gb4', 'v'), (6, 2, 'F4', ''), (8, 8, 'C4', 'bv')],
    [(0, 4, 'C4', 'b'), (4, 2, 'Eb4', ''), (6, 2, 'F4', ''), (8, 6, 'Gb4', 'bv'), (14, 2, 'F4', '')],
    [(0, 10, 'Eb4', 'v'), (10, 2, 'F4', ''), (12, 4, 'G4', 'b')],
    [(0, 8, 'C5', 'bv'), (8, 4, 'Bb4', ''), (12, 4, 'G4', '')],
    [(0, 16, 'C4', 'bv')],
]
CLIMB = [
    [(0, 16, 'C5', 'bv')],
    [(0, 8, 'Bb4', 'v'), (8, 8, 'G4', 'v')],
    [(0, 12, 'C5', 'v'), (12, 4, 'Eb5', '')],
    [(0, 8, 'Bb4', 'bv'), (8, 4, 'G4', ''), (12, 4, 'Gb4', '')],
]


class Parts:
    def __init__(self):
        self.n = {k: [] for k in ('pwrL', 'pwrR', 'ntL', 'ntR', 'muteL', 'muteR', 'bass', 'lead', 'psg', 'fb',
                                  'kick', 'snare', 'cym', 'tom')}
        self.fx = {k: [] for k in list(self.n) + ['drums']}   # (tick, 'vol'|'mod'|'bend', waarde); 'vol' = CC7 in %

    def add(self, part, start, end, note, vel):
        self.n[part].append([int(start), int(end), note, vel])

    def vol(self, parts, bar, pct):
        for k in parts:
            self.fx[k].append((bar * BAR, 'vol', pct))


def slide(P, part, s):
    """In de noot glijden: begint 2 halve tonen lager, in een 8e omhoog (pitchwheel; bereik 2 halve tonen)."""
    for k in range(0, 7):
        P.fx[part].append((s + k * E // 6, 'bend', min(8191, int(8192 * (k / 6 - 1)))))


def riff(P, bar, pattern, guitars=('L', 'R'), bass=True, vel=116):
    """Gitaren en bas spelen exact dezelfde noten."""
    for st, ln, kind, nm, *fx in pattern:
        s, e = pos(bar, st), pos(bar, st + ln)
        acc = 8 if st in (0, 8) else 0
        for sd in guitars:
            part = {'P': 'pwr', 'N': 'nt', 'M': 'mute'}[kind] + sd
            v = vel + acc - (6 if sd == 'R' else 0) - (10 if kind == 'M' else 0)
            P.add(part, s, e, p(nm), v)
            if fx and 's' in fx[0]:
                slide(P, part, s)
        if bass:
            P.add('bass', s, e if kind != 'M' else s + min(e - s, S + S // 2), p(nm), 112 + acc - (14 if kind == 'M' else 0))
            if fx and 's' in fx[0]:
                slide(P, 'bass', s)


def lead(P, bar, phrase, vel=112, part='lead'):
    for st, ln, nm, fx in phrase:
        s, e = pos(bar, st), pos(bar, st + ln)
        P.add(part, s, e, p(nm) - (2 if 'b' in fx else 0), vel)
        if part == 'lead':
            if 'b' in fx:                                       # bend: begint 2 halve tonen lager, in een 8e omhoog
                for k in range(1, 7):
                    P.fx[part].append((s + k * E // 6, 'bend', min(8191, int(8192 * k / 6))))
            if 'v' in fx and ln >= 4:                           # vertraagd vibrato
                P.fx[part].append((s + E, 'mod', 7))


def psg_double(P, bar, phrase):
    """Het motief unisono op de PSG-blokgolf (de Gen 3-'battle-lead'); zonder bends: de bend-noot op zijn doeltoon."""
    for st, ln, nm, fx in phrase:
        P.add('psg', pos(bar, st), pos(bar, st + ln) - 2, p(nm), 100)


def dlen(bar, kind):
    """Drumnoten zo lang als het sample echt klinkt (rnd_kick 0,09 s, rnd_snare 0,16 s): voor de stemverdeler."""
    q = TPB * bpm_at(bar * BAR) / 60                           # ticks per seconde
    return {KICK: max(6, int(0.10 * q)), SNARE: max(8, int(0.17 * q)), HAT: max(6, int(0.08 * q)),
            OHAT: E, CRASH: 2 * TPB, CRASH2: TPB, FTOM: E, MTOM: E, HTOM: E}[kind]


def drum(P, bar, j, kind, vel, part=None, off=0):
    s = pos(bar, j) + off
    part = part or {KICK: 'kick', SNARE: 'snare', FTOM: 'tom', MTOM: 'tom', HTOM: 'tom'}.get(kind, 'cym')
    P.add(part, s, s + dlen(bar, kind), kind, vel)


def sludge_drums(P, bar, crash=False, heavy=False):
    """Loom en zwaar: kick op 1, de 'a' van 1 en de 'en' van 3; doffe snare op 2 en 4; hihat in (swing-)8en."""
    for j, v in ((0, 124), (3, 100), (10, 112)):
        drum(P, bar, j, KICK, v)
    for j in (4, 12):
        drum(P, bar, j, SNARE, 120, off=LAY)
    if crash:
        drum(P, bar, 0, CRASH, 110)
    for j in range(0, 16, 2):
        if crash and j == 0:
            continue
        if heavy and j % 4 == 2:
            drum(P, bar, j, OHAT, 78)                           # snikheet: open hihat op de 'en'
        else:
            drum(P, bar, j, HAT, 82 if j % 4 == 0 else 66)


def pump_drums(P, bar, crash=False, open_hat=False):
    """Beukend: kick 1, de 'en' van 2, 3 en de 'en' van 3; snare 2 en 4; hihat 8en."""
    for j, v in ((0, 127), (6, 112), (8, 122), (10, 108)):
        drum(P, bar, j, KICK, v)
    for j in (4, 12):
        drum(P, bar, j, SNARE, 124)
    if crash:
        drum(P, bar, 0, CRASH, 114)
    for j in range(0, 16, 2):
        if crash and j == 0:
            continue
        if open_hat and j == 14:
            drum(P, bar, j, OHAT, 86)
        else:
            drum(P, bar, j, HAT, 88 if j % 4 == 0 else 72)


def tom_groove(P, bar, crash=False):
    """Odyssey-snel: floor tom in 8en (stuwend), kick 1 en 3, snare 2 en 4."""
    for j in (0, 8):
        drum(P, bar, j, KICK, 124)
    for j in (4, 12):
        drum(P, bar, j, SNARE, 124)
    for j in range(0, 16, 2):
        if j not in (4, 12):
            drum(P, bar, j, FTOM, 104 if j % 4 == 0 else 90)
    if crash:
        drum(P, bar, 0, CRASH, 114)


def fill(P, bar, start, toms=True):
    """16en vanaf 16e 'start' tot het eind van de maat: hoge -> lage toms (of snare), crescendo."""
    for j in range(start, 16):
        k = (j - start) / max(1, 15 - start)
        kind = (HTOM if k < 0.34 else MTOM if k < 0.67 else FTOM) if toms else SNARE
        drum(P, bar, j, kind, int(96 + 28 * k))


def clear_drums(P, bar, start):
    lo, hi = pos(bar, start), (bar + 1) * BAR
    for k in ('kick', 'snare', 'cym', 'tom'):
        P.n[k] = [x for x in P.n[k] if not (lo <= x[0] < hi)]


def feedback(P, start, end, note, top=100, mod_after=None):
    """De versterker huilt: lange noot die aanzwelt (CC7) en pas laat gaat trillen."""
    P.add('fb', start, end, p(note), 110)
    steps, ln = 20, end - start
    for j in range(steps + 1):
        P.fx['fb'].append((start + j * ln * 3 // 4 // steps, 'vol', int(top * (0.15 + 0.85 * (j / steps) ** 1.5))))
    P.fx['fb'] += [(start, 'mod', 0), (start + (mod_after if mod_after is not None else ln // 2), 'mod', 8)]


def build():
    P = Parts()
    G = ('pwrL', 'pwrR', 'ntL', 'ntR', 'muteL', 'muteR')

    # ---- intro: zwelling (de cry van Heatran valt hier), dan de dalende riff ----------------------------------------
    P.add('pwrL', 0, BAR - S, p('C2'), 116)
    P.add('pwrR', 0, BAR - S, p('C2'), 110)
    P.add('bass', 0, BAR - S, p('C2'), 100)
    for k in range(17):                                        # powerchord zwelt in een maat aan
        for sd in ('pwrL', 'pwrR', 'bass'):
            P.fx[sd].append((k * BAR // 16, 'vol', int(10 + 90 * (k / 16) ** 1.6)))
    feedback(P, BAR // 4, BAR - S, 'G4', 80, BAR // 4)
    for k in range(8):                                         # lava-rommel: floor tom in 8en
        P.add('tom', BAR // 2 + k * E // 2, BAR // 2 + k * E // 2 + S, FTOM, 70 + k * 6)
    P.vol(G + ('bass',), INTRO_DESC, 100)
    riff(P, INTRO_DESC, DESC)
    for j in (0, 4, 8, 12):
        drum(P, INTRO_DESC, j, KICK, 124)
        drum(P, INTRO_DESC, j, CRASH2 if j == 0 else FTOM, 108)
    drum(P, INTRO_DESC, 12, SNARE, 110)
    fill(P, INTRO_DESC, 13, toms=False)

    # ---- A: sludge 1 -------------------------------------------------------------------------------------------------
    P.vol(G + ('bass',), A, 100)
    P.fx['drums'].append((A * BAR, 'vol', 100))
    P.vol(('fb',), A, 100)
    for i, pat in enumerate(SLUDGE):
        b = A + i
        riff(P, b, pat, guitars=('L',) if i < 4 else ('L', 'R'))
        sludge_drums(P, b, crash=i in (0, 4), heavy=i >= 4)
    feedback(P, (A + 4) * BAR + 2 * S, (A + 6) * BAR - S, 'C5', 80, BAR)

    # ---- versnelling naar de pump --------------------------------------------------------------------------------------
    for i, pat in enumerate(ACCEL):
        b = ACC + i
        riff(P, b, pat)
        for j in range(0, 16, 4):
            drum(P, b, j, KICK, 116 + 2 * j // 4)
        if i == 0:
            for j in range(0, 16, 2):
                drum(P, b, j, SNARE, 84 + 2 * j)
        else:
            for j in range(16):
                drum(P, b, j, SNARE, 96 + 2 * j)
    feedback(P, ACC * BAR, (ACC + 2) * BAR - S, 'G4', 96, BAR)

    # ---- B: desert pump 1, vanaf 20 het motief, 28 = de stop -------------------------------------------------------
    for i in range(STOP_B - B):
        b = B + i
        riff(P, b, PUMP[i % 4])
        pump_drums(P, b, crash=i % 4 == 0, open_hat=i >= 8)
        if i >= 8:
            lead(P, b, MOTIF[i - 8])
    clear_drums(P, STOP_B - 1, 12)
    fill(P, STOP_B - 1, 12, toms=False)
    riff(P, STOP_B, STOP)
    drum(P, STOP_B, 0, KICK, 127)
    drum(P, STOP_B, 0, CRASH, 120)

    # ---- C: sludge 2, het motief traag en kreunend ------------------------------------------------------------------
    for i, pat in enumerate(SLUDGE):
        b = C + i
        riff(P, b, pat)
        sludge_drums(P, b, crash=i % 2 == 0, heavy=True)
        lead(P, b, MOAN[i])
    clear_drums(P, D - 1, 8)
    fill(P, D - 1, 8)

    # ---- D: desert pump 2 -------------------------------------------------------------------------------------------
    for i in range(CLIMAX - D):                                 # tom-groove + motief (lead + PSG)
        b = D + i
        riff(P, b, PUMP[i % 4])
        tom_groove(P, b, crash=i % 4 == 0)
        lead(P, b, MOTIF[i])
        psg_double(P, b, MOTIF[i])
    clear_drums(P, CLIMAX - 1, 12)
    fill(P, CLIMAX - 1, 12)
    for i in range(RIFF_D - CLIMAX):                            # climax: hoge lead, crash op elke maat
        b = CLIMAX + i
        riff(P, b, (X1, X2)[i % 2])
        pump_drums(P, b, crash=True, open_hat=True)
        lead(P, b, CLIMB[i])
        psg_double(P, b, CLIMB[i])
    for i in range(RIT - RIFF_D):                               # de riff voluit
        b = RIFF_D + i
        riff(P, b, PUMP[i])
        pump_drums(P, b, crash=True)
    riff(P, RIT, DESC)                                          # ritardando: de dalende riff terug naar A
    for j in (0, 4, 8, 12):
        drum(P, RIT, j, KICK, 124)
        drum(P, RIT, j, CRASH2 if j == 0 else FTOM, 108)
    drum(P, RIT, 12, SNARE, 110)
    fill(P, RIT, 13, toms=False)
    feedback(P, RIT * BAR, END * BAR - S, 'G4', 92, 2 * TPB)

    for k in P.n:
        P.n[k] = dedupe(P.n[k])
    return P


def write_voicegroup():
    """grounded_gm + eigen gitaren (27, 28-31), synthbas (34), PSG-lead (81) en 127 = de drumkit."""
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = ("@ Project Grounded: grounded_gm voor Battle! Heatran v5 (Kyuss' Odyssey op de GBA). "
                'Gegenereerd door tools/grounded/heatran_theme.py.')
    lines[1] = ('@ 27 = feedback (sd90 overdrive), 28/29/30 = palm-mute/riffnoot/powerchord (keysplit_heatran, '
                'één sample per riffnoot), 31 = lead (sd90 distortion), 34 = synthbas, 127 = drumkit.')
    lines[2] = 'voice_group %s' % VG
    repl = {
        '@ 27': '\tvoice_directsound 60, 0, DirectSoundWaveData_sd90_classical_overdrive_guitar, 255, 0, 255, %d  @ 27' % REL[FB],
        '@ 28': '\tvoice_keysplit voicegroup_heatran_mute_keysplit, keysplit_heatran  @ 28',
        '@ 29': '\tvoice_keysplit voicegroup_heatran_note_keysplit, keysplit_heatran  @ 29',
        '@ 30': '\tvoice_keysplit voicegroup_heatran_power_keysplit, keysplit_heatran  @ 30',
        '@ 31': '\tvoice_directsound 60, 0, DirectSoundWaveData_sd90_classical_distortion_guitar_high, 255, 0, 255, %d  @ 31' % REL[LEAD],
        '@ 34': '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_synth_bass, 255, 250, 200, 140  @ 34',
        '@ 127': '\tvoice_keysplit_all voicegroup_heatran_drumset  @ 127',
    }
    out = []
    for l in lines:
        tag = '@' + l.rsplit('@', 1)[1] if '@' in l and l.startswith('\t') else None
        out.append(repl.get(tag.strip() if tag else None, l))
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))

    # keysplit_heatran: index 0-6 = C2 Eb2 F2 Gb2 G2 Bb2 C3 (sound/keysplit_tables.inc)
    keys = (36, 39, 41, 42, 43, 46, 48)
    kinds = {'power': ('pw', POWER, 'powerchord (grondtoon+kwint+octaaf)'), 'note': ('nt', NOTE, 'riffnoot (+octaaf)'),
             'mute': ('pm', MUTE, 'palm-mute')}
    for kind, (pre, prog, desc) in kinds.items():
        body = ''.join('\tvoice_directsound %d, 0, DirectSoundWaveData_heatran_gb_%s_%d, 255, 0, 255, %d\n'
                       % (k, pre, k, REL[prog]) for k in keys)
        open('sound/voicegroups/keysplits/heatran_%s.inc' % kind, 'w').write(
            '@ Project Grounded: Battle! Heatran v5, %s; Gen 3-achtige sample per riffnoot (heatran_samples.py),\n'
            '@ tabel keysplit_heatran (sound/keysplit_tables.inc). Gegenereerd door tools/grounded/heatran_theme.py.\n'
            'voice_group heatran_%s_keysplit\n%s' % (desc, kind, body))
    kit = [   # vanaf noot 36; alleen Gen 3-samples, alles DirectSound (geen PSG-drums)
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 242',
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 242',
        'voice_directsound_no_resample 60, 79, DirectSoundWaveData_unknown_close_hihat, 255, 127, 0, 188',
        'voice_directsound_no_resample 60, 79, DirectSoundWaveData_unknown_open_hihat, 255, 242, 141, 0',
        'voice_directsound_no_resample 30, 54, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 216',
        'voice_directsound 48, 44, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 204',
        'voice_directsound 54, 64, DirectSoundWaveData_unused_sc55_tom, 255, 216, 77, 204',
        'voice_directsound 60, 79, DirectSoundWaveData_unused_sc55_tom, 255, 204, 77, 204',
        'voice_directsound_no_resample 60, 14, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165',
    ]
    open('sound/voicegroups/drumsets/heatran.inc', 'w').write(
        '@ Project Grounded: drumkit voor Battle! Heatran v5 (heatran_theme.py): de Gen 3-drums uit rs_drumset zonder\n'
        '@ PSG-noten: 36 kick, 37 snare (dof), 38 hihat, 39 open hihat, 40 crash, 41-43 toms laag/midden/hoog,\n'
        '@ 44 trinity-crash (blikkerig).\n'
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


LAYOUT = [  # naam, programma, volume, kanaal, pan, vaste bend
    ('pwrL', POWER, 92, 0, 30, 0),
    ('pwrR', POWER, 86, 1, 98, R_BEND),
    ('ntL', NOTE, 92, 2, 30, 0),
    ('ntR', NOTE, 86, 3, 98, R_BEND),
    ('muteL', MUTE, 96, 4, 34, 0),
    ('muteR', MUTE, 90, 5, 94, R_BEND),
    ('bass', BASS, 112, 6, 64, 0),
    ('lead', LEAD, 100, 7, 70, 0),
    ('psg', PSG, 40, 8, 58, 0),
    ('fb', FB, 70, 10, 54, 0),
]
DRUM_VOL = 112


def save(P, path):
    out = mido.MidiFile(type=1, ticks_per_beat=TPB)
    cond = mido.MidiTrack()
    ev = [(t, mido.MetaMessage('set_tempo', tempo=int(round(60e6 / b)), time=0)) for t, b in TEMPO]
    ev += [(A * BAR, mido.MetaMessage('marker', text='[', time=0)), (END * BAR, mido.MetaMessage('marker', text=']', time=0))]
    last = 0
    for t, m in sorted(ev, key=lambda x: (x[0], x[1].type != 'marker')):   # op het loopbegin: eerst het label
        cond.append(m.copy(time=t - last))
        last = t
    out.tracks.append(cond)
    for name, prog, vol, ch, pan, bend in LAYOUT:
        fx = fx_events(P.fx[name], P.n[name], bend)
        if bend:
            fx = [(0, 'bend', bend)] + [x for x in fx if not (x[0] == 0 and x[1] == 'bend')]
        if any(x[1] == 'vol' for x in P.fx[name]):              # CC7 op het loopbegin opnieuw zetten
            fx.append((A * BAR, 'vol', 100))
        add_track(out, P.n[name], prog, vol, ch, pan, fx)
    drums = ('kick', 'snare', 'cym', 'tom')
    add_track(out, sorted(sum((P.n[k] for k in drums), [])), DRUMS, DRUM_VOL, 9, 64, P.fx['drums'])
    written = {k for k, *_ in LAYOUT} | set(drums)
    assert not [k for k in P.n if P.n[k] and k not in written], 'partij niet weggeschreven'
    out.save(path)


def add_track(out, notes, prog, vol, ch, pan, fx):
    t = mido.MidiTrack()
    t.append(mido.Message('program_change', channel=ch, program=prog, time=0))
    t.append(mido.Message('control_change', channel=ch, control=7, value=vol, time=0))
    t.append(mido.Message('control_change', channel=ch, control=10, value=pan, time=0))
    t.append(mido.Message('control_change', channel=ch, control=20, value=2, time=0))   # BENDR 2 halve tonen
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


def one_string(P, sd):
    """Powerchords, riffnoten en chugs van één gitaar zijn één partij: elke noot stopt waar de volgende begint."""
    names = ('pwr' + sd, 'nt' + sd, 'mute' + sd)
    both = sorted(x + [k] for k in names for x in P.n[k])
    for i, x in enumerate(both[:-1]):
        nxt = both[i + 1][0]
        if nxt > x[0]:
            x[1] = min(x[1], nxt)
    for k in names:
        P.n[k] = [x[:4] for x in both if x[4] == k]


def main():
    P = build()
    write_voicegroup()
    rel = releases(VG)
    progs = {'pwrL': POWER, 'pwrR': POWER, 'ntL': NOTE, 'ntR': NOTE, 'muteL': MUTE, 'muteR': MUTE, 'bass': BASS,
             'lead': LEAD, 'fb': FB}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, FAST) for k, pr in progs.items()}   # snel tempo = meeste ticks
    tail['kick'] = tail['snare'] = tail['tom'] = tail['cym'] = 0   # drums: de noot zelf = de echte lengte
    for sd in ('L', 'R'):
        one_string(P, sd)
    for k in progs:
        P.n[k] = detach(P.n[k], tail[k])
    for sd in ('L', 'R'):                                    # ook tussen de soorten: release eerder los
        names = ('pwr' + sd, 'nt' + sd, 'mute' + sd)
        allx = sorted(x for k in names for x in P.n[k])
        starts = sorted(set(x[0] for x in allx))
        for x in allx:
            nxt = next((t for t in starts if t > x[0]), None)
            if nxt is not None:
                x[1] = min(x[1], max(x[0] + 6, nxt - tail['pwr' + sd]))
    # zelfde toonhoogte mag in één spoor niet overlappen (de note-off van de eerste zou de tweede afkappen)
    for k in P.n:
        ns = sorted(P.n[k])
        for i, x in enumerate(ns):
            nxt = next((y[0] for y in ns[i + 1:] if y[2] == x[2] and y[0] >= x[0]), None)
            if nxt is not None and nxt < x[1]:
                x[1] = max(x[0] + 6, nxt - 1)
        P.n[k] = ns
    order = ['bass', 'pwrL', 'ntL', 'muteL', 'kick', 'snare', 'lead', 'cym', 'pwrR', 'ntR', 'muteR', 'tom', 'fb']
    kept = allocate({k: P.n[k] for k in order}, order, tail, max_voices=11)
    print('tail (ticks bij %d bpm):' % FAST, tail)
    for k in order:
        n = len(P.n[k])
        print('  %-6s %4d noten, %3d vallen weg (%.1f%%)' % (k, n, n - len(kept[k]), 100 * (n - len(kept[k])) / max(n, 1)))
        P.n[k] = kept[k]
    save(P, OUT)
    print(OUT, '%.1f s intro, %.1f s loop' % (secs(A * BAR), secs(END * BAR) - secs(A * BAR)))
    for nm, a, b in (('intro', 0, A), ('A', A, ACC), ('accel', ACC, B), ('B', B, C), ('C', C, D), ('D', D, CLIMAX),
                     ('climax', CLIMAX, RIFF_D), ('riff+rit', RIFF_D, END)):
        print('  %-8s maat %2d-%2d  %6.1f - %6.1f s' % (nm, a, b - 1, secs(a * BAR), secs(b * BAR)))


if __name__ == '__main__':
    main()
