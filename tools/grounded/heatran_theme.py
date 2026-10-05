#!/usr/bin/env python3
"""Project Grounded: "Battle! Heatran" v6, eigen compositie from scratch: Kyuss ('Odyssey', 'Green Machine') op een
Game Boy Advance, met de dreiging van het R/S Regi-gevechtsthema. Geen Kyuss-noten: eigen riffs, gemeten stijl.

Jordi (v5-feedback): 'Stop met pop-punk, ska, funk en vrolijke videogame-melodietjes' (v1-v5 klonken als surf/ska/
Mario Kart Super Circuit 'Bowser's Castle'). Daarom is v6 eerst gemeten aan zijn audioreferenties (Spleeter-stems,
librosa, basic-pitch; zie MUZIEK.md 'Heatran v6') en controleert dit script de uitkomst (stoner_checks, faalt hard):
  referentie             Odyssey traag | Odyssey/Green Machine snel   v5 (fout)
  tempo                  77 bpm        | 90-96 bpm (8e-puls 180-191/min)   76 | 136 (8e-puls 272/min)
  gitaar sustain P20/P90 0,38          | 0,55-0,63 (muur van fuzz)        0,27-0,45 (staccato)
  gitaar < 250 / > 2 kHz 72 / 0 %      | 49-72 / 1-21 %                   12-19 / 18-27 %
  hihat                  8en, accent op de tel 69-81 %, ±3,1 aanslagen/s    4,3/s, de helft op de 'en'
  toonsoort              C-klein (Krumhansl 0,69-0,79), G-frygisch (GM)     'C-groot' in de sludge
  bas                    pedaaltoon 56-78 % van de duur, halve-toonstappen 0-11 %   v5-riff 15-29 %
Dus: traag = 76 bpm halftime-sludge, snel = 94 bpm 'trein' (8en die doorklinken, accenten óp de tel), C-klein
blues/frygisch (C Db Eb F Gb G Ab Bb; nooit E/A/B/D), lange aangehouden powerchords, bas = exact de gitaarriff.

Instrumenten (voicegroup grounded_heatran):
  30   slaggitaar: powerchord-sample per riffnoot (keysplit_heatran, heatran_samples.py: FluidR3 distortion door een
       fuzz + basversterker, 13.379 Hz, 8 bit); links + rechts (+9 cent, dubbele opname)
  31   lead: eigen fuzzlead (keysplit_heatran_lead, C4/G4), laag en donker, alleen lange noten met bends
  27   feedback = sd90_classical_overdrive_guitar (de echte Gen 3-gitaar), zwelt aan
  34   bas = sc88pro_synth_bass (de doffe Gen 3-synthbas), speelt exact de gitaarriff
  127  drumset heatran: Gen 3-drums zonder PSG (rnd_kick, rnd_snare = doffe snare, gesloten hihat, orchestra crash,
       sc55-toms, trinity crash)
Vorm (intro op de transitie, naadloze loop):
  0      76  zwelling: lage C + feedback, floor tom rommelt (de cry valt hier, geen drop)
  1      76  'dreigmaat' C C C Db in kwarten (de Regi-pauken C-C-C-B, als powerchords)
  A 2-9  76  SLUDGE 1: halftime, loom, eerst één gitaar, vanaf maat 6 beide + feedback
  10     94  opbouw: C houdt aan, floor tom in 8en
  B 11-26 94 TREIN 1: 8en op de C-pedaal met aangehouden wendingen; 19-26 het Heatran-motief (Regi-'zucht':
             lange noot, kleine secunde omhoog) op de lead
  C 27-34 76 SLUDGE 2: zwaarder riff + kreunende lead (hele noten, bends) + feedback
  35     94  opbouw
  D 36-47 94 TREIN 2: 36-39 op de F-pedaal (Gb erboven, frygisch), 40-47 C-trein + climax-lead
  48     76  de dreigmaat (= maat 1), terug naar A
Gebruikt musiclib.py; zie MUZIEK.md. Gebruik: python3 tools/grounded/heatran_samples.py; python3 tools/grounded/heatran_theme.py"""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks

OUT = 'sound/songs/midi/mus_grounded_vs_heatran.mid'
VG = 'grounded_heatran'
TPB = 96
SLOW, FAST = 76, 94
S = TPB // 4                   # een 16e
E = TPB // 2                   # een 8e
BAR = TPB * 4
FB, POWER, LEAD, BASS, DRUMS = 27, 30, 31, 34, 127
R_BEND = 3 * 128               # rechter gitaar ±9 cent hoger (dubbele opname; BENDR 2)
KICK, SNARE, HAT, OHAT, CRASH, FTOM, MTOM, HTOM, CRASH2 = range(36, 45)    # drumsets/heatran.inc
REL = {POWER: 150, LEAD: 190, FB: 200}

DREAD0, A, BUILD1, B, B_LEAD, C, BUILD2, D, D_LEAD, DREAD, END = 1, 2, 10, 11, 19, 27, 35, 36, 40, 48, 49
SLOW_BARS = set(range(0, BUILD1)) | set(range(C, BUILD2)) | {DREAD}
SECTIONS = [('intro', 0, A), ('A sludge', A, BUILD1), ('opbouw', BUILD1, B), ('B trein', B, C), ('C sludge', C, BUILD2),
            ('opbouw', BUILD2, D), ('D trein', D, DREAD), ('dreig', DREAD, END)]

N = {'C': 0, 'Db': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'Gb': 6, 'G': 7, 'Ab': 8, 'A': 9, 'Bb': 10, 'B': 11}


def p(name):
    """'C2' -> midi-noot (C4 = 60)."""
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


# ---- tempo: abrupte wissels op de maatstreep (zoals Odyssey) -------------------------------------------------------
TEMPO = []
for bar in range(END):
    bpm = SLOW if bar in SLOW_BARS else FAST
    if not TEMPO or TEMPO[-1][1] != bpm or bar == A:          # loopbegin: tempo op de looptick zelf
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


# ---- riffs: (16e, lengte in 16en, noot) = powerchord; gitaren en bas spelen exact hetzelfde ---------------------
def chug(note, start, stop):
    """Doorklinkende 8en op één akkoord (de trein): elke noot duurt tot de volgende, accent komt uit riff()."""
    return [(j, 2, note) for j in range(start, stop, 2)]


# SLUDGE (76, halftime): loodzwaar, lange powerchords, trage chugs; de b2 (Db) en de b5 (Gb) als dreiging
SL1 = [(0, 6, 'C2'), (6, 2, 'C2'), (8, 2, 'C2'), (10, 6, 'Eb2')]
SL2 = [(0, 6, 'C2'), (6, 2, 'C2'), (8, 6, 'Gb2'), (14, 2, 'F2')]
SL4 = [(0, 8, 'C2'), (8, 4, 'Ab2'), (12, 4, 'G2')]
SLUDGE1 = [SL1, SL2, SL1, SL4]
# sludge 2: zwaarder, trage kwart-chugs op C, de tritonus en de b2 aangehouden
SX1 = [(0, 4, 'C2'), (4, 4, 'C2'), (8, 4, 'Eb2'), (12, 4, 'Db2')]
SX2 = [(0, 8, 'C2'), (8, 8, 'Gb2')]
SX4 = [(0, 4, 'C2'), (4, 4, 'C2'), (8, 4, 'Ab2'), (12, 4, 'G2')]
SLUDGE2 = [SX1, SX2, SX1, SX4]
# TREIN (94): 8en op de C-pedaal, dan een aangehouden wending
TR1 = chug('C2', 0, 12) + [(12, 4, 'Eb2')]
TR2 = chug('C2', 0, 12) + [(12, 4, 'Gb2')]
TR4 = [(0, 8, 'Ab2'), (8, 8, 'G2')]
TRAIN = [TR1, TR2, TR1, TR4]
TB1 = chug('C2', 0, 8) + [(8, 8, 'Gb2')]
TB2 = chug('C2', 0, 8) + [(8, 4, 'F2'), (12, 4, 'Eb2')]
TB4 = [(0, 8, 'Db2'), (8, 8, 'C2')]
TRAIN_B = [TB1, TB2, TB1, TB4]
# trein op de F-pedaal (Green Machine-achtig frygisch: de kleine secunde erboven)
TF1 = chug('F2', 0, 12) + [(12, 4, 'Gb2')]
TF2 = chug('F2', 0, 12) + [(12, 4, 'Eb2')]
TF4 = [(0, 8, 'Db2'), (8, 8, 'C2')]
TRAIN_F = [TF1, TF2, TF1, TF4]
DREAD_BAR = [(0, 4, 'C2'), (4, 4, 'C2'), (8, 4, 'C2'), (12, 4, 'Db2')]     # Regi-pauken C-C-C-B
HOLD = [(0, 16, 'C2')]

# ---- lead: (16e, lengte, noot, fx) 'b' = erin buigen vanaf 2 halve tonen lager, 'v' = vibrato ------------------
MAGMA = [   # trein 1, maat 19-26: lange noot + kleine secunde omhoog (de Regi-zucht), dalend in reeksen
    [(0, 12, 'G4', 'v'), (12, 4, 'Ab4', '')],
    [(0, 16, 'G4', 'bv')],
    [(0, 8, 'C4', ''), (8, 8, 'Db4', 'v')],
    [(0, 16, 'C4', 'bv')],
    [(0, 12, 'Bb4', 'bv'), (12, 4, 'C5', '')],
    [(0, 8, 'Db5', 'v'), (8, 8, 'C5', 'v')],
    [(0, 8, 'Bb4', ''), (8, 8, 'G4', 'v')],
    [(0, 8, 'Gb4', 'bv'), (8, 8, 'Eb4', 'v')],
]
MOAN = [    # sludge 2: hele noten die kreunen
    [(0, 16, 'C4', 'bv')],
    [(0, 16, 'Db4', 'v')],
    [(0, 16, 'C4', 'v')],
    [(0, 16, 'G4', 'bv')],
    [(0, 8, 'Ab4', 'v'), (8, 8, 'G4', 'v')],
    [(0, 16, 'Eb4', 'bv')],
    [(0, 8, 'F4', 'v'), (8, 8, 'Gb4', 'bv')],
    [(0, 16, 'C4', 'bv')],
]
CLIMAX = [  # trein 2, maat 40-47
    [(0, 12, 'C5', 'bv'), (12, 4, 'Db5', '')],
    [(0, 16, 'C5', 'v')],
    [(0, 12, 'Bb4', 'bv'), (12, 4, 'C5', '')],
    [(0, 16, 'Ab4', 'v')],
    [(0, 16, 'Gb4', 'bv')],
    [(0, 8, 'Eb4', 'v'), (8, 8, 'F4', 'v')],
    [(0, 16, 'G4', 'bv')],
    [(0, 16, 'C4', 'bv')],
]


class Parts:
    def __init__(self):
        self.n = {k: [] for k in ('gtrL', 'gtrR', 'bass', 'lead', 'fb', 'kick', 'snare', 'hat', 'cym', 'tom')}
        self.fx = {k: [] for k in list(self.n) + ['drums']}   # (tick, 'vol'|'mod'|'bend', waarde); 'vol' = CC7 in %
        self.written = {}                                     # riffnoten zoals geschreven (vóór detach): voor de controles

    def add(self, part, start, end, note, vel):
        self.n[part].append([int(start), int(end), note, vel])


def riff(P, bar, pattern, guitars=('L', 'R'), vel=112):
    """Linkergitaar en bas exact dezelfde noten; accent óp de tel (Kyuss), de 8en ertussen zachter.
    De rechtergitaar is de 'muur': dezelfde akkoorden, maar herhaalde aanslagen op één akkoord worden één lange noot
    (doorklinkende fuzz zoals bij Kyuss; gemeten sustain van de gitaarstem 0,55-0,63) en kost maar één kanaal."""
    wall = []
    for st, ln, nm in pattern:
        s, e = pos(bar, st), pos(bar, st + ln)
        v = vel + (8 if st % 16 == 0 else 4 if st % 4 == 0 else -6)
        if 'L' in guitars:
            P.add('gtrL', s, e, p(nm), v)
        P.add('bass', s, e, p(nm), v)
        if wall and wall[-1][2] == p(nm) and wall[-1][1] == s:
            wall[-1][1] = e
        else:
            wall.append([s, e, p(nm), v - 5])
    if 'R' in guitars:
        for x in wall:
            P.add('gtrR', *x)


def lead(P, bar, phrase, vel=104):
    for st, ln, nm, fx in phrase:
        s, e = pos(bar, st), pos(bar, st + ln)
        P.add('lead', s, e, p(nm), vel + (6 if st == 0 else 0))
        if 'b' in fx:                                         # in de noot buigen: 2 halve tonen lager, in een 8e omhoog
            for k in range(0, 7):
                P.fx['lead'].append((s + k * E // 6, 'bend', min(8191, int(8192 * (k / 6 - 1)))))
        if 'v' in fx and ln >= 8:                             # vertraagd vibrato
            P.fx['lead'].append((s + TPB, 'mod', 8))


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
    """Gesloten hihat in rechte 8en, accent op de tel (referentie: 69-81 % van de hihat-energie op de tel)."""
    for j in range(0, 16, 2):
        if j not in skip:
            drum(P, bar, j, HAT, 96 if j % 4 == 0 else 62)


def sludge_drums(P, bar, crash=False):
    """Halftime: kick 1 en de 'en' van 2, doffe snare op 3, kick op de 'en' van 4 naar de volgende maat."""
    for j, v in ((0, 127), (6, 108), (14, 100)):
        drum(P, bar, j, KICK, v)
    drum(P, bar, 8, SNARE, 124)
    if crash:
        drum(P, bar, 0, CRASH, 112)
    hats(P, bar, skip=(0,) if crash else ())


def train_drums(P, bar, crash=False):
    """De stompende trein: kick 1, kick 'en' van 1, snare 2; kick 3, kick 'en' van 3, snare 4; hihat 8en."""
    for j, v in ((0, 127), (2, 104), (8, 122), (10, 104)):
        drum(P, bar, j, KICK, v)
    for j in (4, 12):
        drum(P, bar, j, SNARE, 124)
    if crash:
        drum(P, bar, 0, CRASH, 114)
    hats(P, bar, skip=(0,) if crash else ())


def build_drums(P, bar):
    """Opbouw naar de trein: kick op de tel, floor tom in 8en die aanzwelt, op tel 4 twee snares."""
    for j in (0, 4, 8, 12):
        drum(P, bar, j, KICK, 120)
    for j in range(0, 12, 2):
        drum(P, bar, j, FTOM, 84 + 4 * j)
    drum(P, bar, 0, CRASH2, 104)
    drum(P, bar, 12, SNARE, 116)
    drum(P, bar, 14, SNARE, 124)


def dread_drums(P, bar):
    """De dreigmaat: kick + floor tom op elke kwart (de Regi-pauken), crash op 1, tom-roffel in 8en op tel 4."""
    for j in (0, 4, 8):
        drum(P, bar, j, KICK, 124)
        drum(P, bar, j, FTOM, 112)
    drum(P, bar, 0, CRASH2, 108)
    drum(P, bar, 12, KICK, 124)
    drum(P, bar, 12, MTOM, 110)
    drum(P, bar, 14, FTOM, 120)


def feedback(P, start, end, note, top=100, mod_after=None):
    """De versterker huilt: lange noot die aanzwelt (CC7) en pas laat gaat trillen."""
    P.add('fb', start, end, p(note), 110)
    steps, ln = 20, end - start
    for j in range(steps + 1):
        P.fx['fb'].append((start + j * ln * 3 // 4 // steps, 'vol', int(top * (0.15 + 0.85 * (j / steps) ** 1.5))))
    P.fx['fb'] += [(start, 'mod', 0), (start + (mod_after if mod_after is not None else ln // 2), 'mod', 8)]


def build():
    P = Parts()

    # ---- intro: zwelling (de cry van Heatran valt hier), dan de dreigmaat -----------------------------------------
    P.add('gtrL', 0, BAR, p('C2'), 116)
    P.add('gtrR', 0, BAR, p('C2'), 110)
    P.add('bass', 0, BAR, p('C2'), 116)
    for k in range(17):                                        # powerchord zwelt in een maat aan
        for sd in ('gtrL', 'gtrR', 'bass'):
            P.fx[sd].append((k * BAR // 16, 'vol', int(10 + 90 * (k / 16) ** 1.6)))
    feedback(P, BAR // 4, BAR, 'G4', 80, BAR // 4)
    for k in range(8):                                         # lava-rommel: floor tom in 8en
        drum(P, 0, 8 + k, FTOM, 64 + k * 6)
    for sd in ('gtrL', 'gtrR', 'bass'):
        P.fx[sd].append((DREAD0 * BAR, 'vol', 100))
    riff(P, DREAD0, DREAD_BAR)
    dread_drums(P, DREAD0)

    # ---- A: sludge 1 -------------------------------------------------------------------------------------------------
    P.fx['drums'].append((A * BAR, 'vol', 100))
    for i in range(8):
        b = A + i
        riff(P, b, SLUDGE1[i % 4], guitars=('L',) if i < 4 else ('L', 'R'))
        sludge_drums(P, b, crash=i % 2 == 0)
    feedback(P, (A + 4) * BAR, (A + 7) * BAR, 'C5', 76, BAR)

    # ---- opbouw 1 -> trein 1 -----------------------------------------------------------------------------------------
    riff(P, BUILD1, HOLD)
    build_drums(P, BUILD1)
    feedback(P, BUILD1 * BAR, (BUILD1 + 1) * BAR, 'G4', 90, TPB)
    for i in range(C - B):
        b = B + i
        riff(P, b, (TRAIN if b < B_LEAD else TRAIN_B)[i % 4])
        train_drums(P, b, crash=i % 4 == 0)
        if b >= B_LEAD:
            lead(P, b, MAGMA[b - B_LEAD])

    # ---- C: sludge 2 + kreunende lead -------------------------------------------------------------------------------
    for i in range(BUILD2 - C):
        b = C + i
        riff(P, b, SLUDGE2[i % 4])
        sludge_drums(P, b, crash=True)
        lead(P, b, MOAN[i])
    feedback(P, (C + 2) * BAR, (C + 4) * BAR, 'G4', 70, BAR)

    # ---- opbouw 2 -> trein 2 + climax --------------------------------------------------------------------------------
    riff(P, BUILD2, HOLD)
    build_drums(P, BUILD2)
    feedback(P, BUILD2 * BAR, (BUILD2 + 1) * BAR, 'C5', 90, TPB)
    for i in range(DREAD - D):
        b = D + i
        riff(P, b, (TRAIN_F if b < D_LEAD else TRAIN)[i % 4])
        train_drums(P, b, crash=i % 4 == 0 or b >= D_LEAD + 4)
        if b >= D_LEAD:
            lead(P, b, CLIMAX[b - D_LEAD])

    # ---- de dreigmaat (= maat 1) en terug naar A ---------------------------------------------------------------------
    riff(P, DREAD, DREAD_BAR)
    dread_drums(P, DREAD)

    for k in P.n:
        P.n[k] = dedupe(P.n[k])
    P.written = {k: [list(x) for x in v] for k, v in P.n.items()}
    return P


# ---- anti-ska / anti-Bowser's Castle: harde controles, afgeleid van de referentiemetingen ----------------------------
SCALE = {0, 1, 3, 5, 6, 7, 8, 10}          # C-klein blues/frygisch: C Db Eb F Gb G Ab Bb (geen E = grote terts)


def section_of(tick):
    bar = tick // BAR
    return next(nm for nm, a, b in SECTIONS if a <= bar < b)


def stoner_checks(P):
    """Faalt (AssertionError) als het nummer weer richting ska/surf/Bowser's Castle schuift. Geeft de meetwaarden terug."""
    W = P.written
    fails, rep = [], {}
    mel = {k: sorted(W[k]) for k in ('gtrL', 'bass', 'lead', 'fb')}
    # 1. toonladder: geen grote terts (E), geen A/B/D (majeur-/dorisch-kleur)
    for k, ns in mel.items():
        bad = sorted({n[2] % 12 for n in ns} - SCALE)
        if bad:
            fails.append('%s: toonklassen buiten C-klein blues/frygisch: %s' % (k, bad))
    # 2. geen grote terts omhoog (vrolijk arpeggio) en 3. geen chromatische loopjes, weinig halve-toonstappen
    for k in ('gtrL', 'bass', 'lead'):
        line = [n[2] for n in mel[k]]
        st = [b - a for a, b in zip(line, line[1:]) if b != a]
        if k == 'lead' and any(x == 4 for x in st):
            fails.append('lead: sprong van een grote terts omhoog')
        runs = sum(1 for x, y in zip(st, st[1:]) if abs(x) == 1 and x == y)
        if runs:
            fails.append('%s: %d chromatische loopjes (3 noten in halve tonen dezelfde kant op)' % (k, runs))
        allsteps = [b - a for a, b in zip(line, line[1:])]
        semi = sum(1 for x in allsteps if abs(x) == 1) / max(1, len(allsteps))
        rep[k + ' halve-toonstap'] = semi
        if k != 'lead' and semi > 0.12:                         # referentie-bas 0-11 %
            fails.append('%s: %.0f%% halve-toonstappen (referentie <= 11%%)' % (k, 100 * semi))
    # 4. tempo per sectie en geen swing
    for t, b in TEMPO:
        if not (70 <= b <= 80 or 88 <= b <= 98):
            fails.append('tempo %d bpm buiten 70-80 (traag) / 88-98 (snel; referentie 90-96)' % b)
    for k in P.n:
        if any(n[0] % S for n in W[k] if k not in ('fb',)):
            fails.append('%s: noten naast het rechte 16e-raster (swing/huppel)' % k)
    # 5. hihats: niet sneller dan de referentie, geen open hihat, accent op de tel
    for nm, a, b in SECTIONS:
        hs = [n for n in W['hat'] if a * BAR <= n[0] < b * BAR]
        if not hs:
            continue
        sec = secs(b * BAR) - secs(a * BAR)
        rate = len(hs) / sec
        rep['hihat/s ' + nm] = rate
        if rate > 3.3:                                          # referentie 3,0-3,2/s
            fails.append('%s: %.1f hihats/s (referentie <= 3,2)' % (nm, rate))
        if any(n[2] == OHAT for n in hs):
            fails.append('%s: open hihat' % nm)
        on = [n[3] for n in hs if n[0] % TPB == 0]
        off = [n[3] for n in hs if n[0] % TPB]
        if off and on and max(off) >= min(on):
            fails.append('%s: hihat op de en even hard als op de tel (off-beat-accent)' % nm)
    # 6. geen staccato: elke riffnoot klinkt tot de volgende aanslag (of >= 1 tel); gemiddelde nootlengte per sectie
    for nm, a, b in SECTIONS:
        for k in ('gtrL', 'bass'):
            ns = [n for n in W[k] if a * BAR <= n[0] < b * BAR]
            if not ns:
                continue
            starts = sorted(set(n[0] for n in W[k]))
            short = [n for n in ns if n[1] - n[0] < TPB and (n[1] < next((t for t in starts if t > n[0]), 10 ** 9))]
            if short:
                fails.append('%s %s: %d staccato-noten (korter dan een tel en stil vóór de volgende)' % (nm, k, len(short)))
            mean = sum(n[1] - n[0] for n in ns) / len(ns) / TPB
            rep['nootlengte %s %s' % (k, nm)] = mean
            if mean < (0.95 if bpm_at(a * BAR) <= 80 and nm != 'intro' else 0.5):
                fails.append('%s %s: gemiddelde nootlengte %.2f tel te kort' % (nm, k, mean))
    # 7. naast de tel: geen 'skank' (aanslag op de en/16e terwijl de tel ervoor stil was), accent op de tel
    for k in ('gtrL', 'bass'):
        ns = sorted(W[k])
        sounding = lambda t: any(n[0] <= t < n[1] for n in ns)
        off = [n for n in ns if n[0] % TPB]
        skank = [n for n in off if not sounding(n[0] - n[0] % TPB)]
        if skank:
            fails.append('%s: %d off-beat-stoten na een stille tel (ska/skank)' % (k, len(skank)))
        share = len(off) / len(ns)
        rep[k + ' naast de tel'] = share
        if share > 0.5:
            fails.append('%s: %.0f%% van de aanslagen naast de tel' % (k, 100 * share))
        if off and max(n[3] for n in off) >= min(n[3] for n in ns if n[0] % TPB == 0):
            fails.append('%s: off-beat even hard als op de tel' % k)
    # 8. geen wandelende 8e-bas: in de trein blijft de bas op de pedaal (referentie: pedaaltoon 56-78 % van de duur)
    for nm, a, b in SECTIONS:
        ns = sorted(n for n in W['bass'] if a * BAR <= n[0] < b * BAR)
        if len(ns) < 8:
            continue
        rep_share = sum(1 for x, y in zip(ns, ns[1:]) if x[2] == y[2]) / (len(ns) - 1)
        dur = {}
        for n in ns:
            dur[n[2]] = dur.get(n[2], 0) + n[1] - n[0]
        ped = max(dur.values()) / sum(dur.values())
        rep['bas pedaal %s' % nm] = ped
        if ped < 0.4:
            fails.append('%s: pedaaltoon maar %.0f%% van de duur (wandelende bas?)' % (nm, 100 * ped))
        if bpm_at(a * BAR) > 80 and rep_share < 0.5:
            fails.append('%s: bas verandert bij %.0f%% van de aanslagen van toon (walking bass)' % (nm, 100 * (1 - rep_share)))
    # 9. lead: lange noten, weinig noten (geen felle melodie in korte noten)
    ld = W['lead']
    if ld:
        lens = [(n[1] - n[0]) / TPB for n in ld]
        rep['lead nootlengte'] = sum(lens) / len(lens)
        if sum(lens) / len(lens) < 1.5 or sum(1 for x in lens if x < 1) > 0.2 * len(lens):
            fails.append('lead: te korte noten (gem. %.2f tel)' % (sum(lens) / len(lens)))
    # 10. bas = exact de gitaarriff
    g = {(n[0], n[2]) for n in W['gtrL']}
    bs = {(n[0], n[2]) for n in W['bass']}
    if g - bs:
        fails.append('bas verdubbelt de gitaar niet op %d aanslagen' % len(g - bs))
    # 11. kick vooral op de tel
    kk = W['kick']
    rep['kick op de tel'] = sum(1 for n in kk if n[0] % TPB == 0) / len(kk)
    if rep['kick op de tel'] < 0.5:
        fails.append('kick: maar %.0f%% op de tel' % (100 * rep['kick op de tel']))
    assert not fails, 'stoner_checks:\n  ' + '\n  '.join(fails)
    return rep


def write_voicegroup():
    """grounded_gm + feedback (27), powerchord-keysplit (30), lead-keysplit (31), synthbas (34), drumkit (127)."""
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = ("@ Project Grounded: grounded_gm voor Battle! Heatran v6 (Kyuss op de GBA). "
                'Gegenereerd door tools/grounded/heatran_theme.py.')
    lines[1] = ('@ 27 = feedback (sd90 overdrive), 30 = powerchord (keysplit_heatran, één sample per riffnoot), '
                '31 = fuzzlead (keysplit_heatran_lead), 34 = synthbas, 127 = drumkit.')
    lines[2] = 'voice_group %s' % VG
    repl = {
        '@ 27': '\tvoice_directsound 60, 0, DirectSoundWaveData_sd90_classical_overdrive_guitar, 255, 0, 255, %d  @ 27' % REL[FB],
        '@ 30': '\tvoice_keysplit voicegroup_heatran_power_keysplit, keysplit_heatran  @ 30',
        '@ 31': '\tvoice_keysplit voicegroup_heatran_lead_keysplit, keysplit_heatran_lead  @ 31',
        '@ 34': '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_synth_bass, 255, 0, 255, 160  @ 34',
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
        '@ Project Grounded: Battle! Heatran v6, powerchord (grondtoon+kwint+octaaf) per riffnoot (heatran_samples.py),\n'
        '@ tabel keysplit_heatran (sound/keysplit_tables.inc). Gegenereerd door tools/grounded/heatran_theme.py.\n'
        'voice_group heatran_power_keysplit\n' + body)
    body = ''.join('\tvoice_directsound %d, 0, DirectSoundWaveData_heatran_st_lead_%d, 255, 0, 255, %d\n'
                   % (k, k, REL[LEAD]) for k in (60, 67))
    open('sound/voicegroups/keysplits/heatran_lead.inc', 'w').write(
        '@ Project Grounded: Battle! Heatran v6, fuzzlead C4/G4 (heatran_samples.py), tabel keysplit_heatran_lead.\n'
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
        '@ Project Grounded: drumkit voor Battle! Heatran v6 (heatran_theme.py): de Gen 3-drums uit rs_drumset zonder\n'
        '@ PSG-noten: 36 kick, 37 snare (dof), 38 hihat, 39 open hihat (ongebruikt), 40 crash, 41-43 toms\n'
        '@ laag/midden/hoog, 44 trinity-crash (blikkerig).\n'
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
    ('gtrL', POWER, 100, 0, 34, 0),
    ('gtrR', POWER, 94, 1, 94, R_BEND),
    ('bass', BASS, 104, 2, 64, 0),
    ('lead', LEAD, 80, 3, 70, 0),
    ('fb', FB, 64, 4, 54, 0),
]
DRUM_VOL = 112
DRUM_PARTS = ('kick', 'snare', 'hat', 'cym', 'tom')


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
        if name == 'lead':                                      # bend/vibrato vóór het loopbegin terug
            fx += [(A * BAR, 'bend', 0), (A * BAR, 'mod', 0)]
        add_track(out, P.n[name], prog, vol, ch, pan, fx)
    add_track(out, sorted(sum((P.n[k] for k in DRUM_PARTS), [])), DRUMS, DRUM_VOL, 9, 64, P.fx['drums'])
    written = {k for k, *_ in LAYOUT} | set(DRUM_PARTS)
    assert not [k for k in P.n if P.n[k] and k not in written], 'partij niet weggeschreven'
    out.save(path)


def main():
    P = build()
    rep = stoner_checks(P)
    write_voicegroup()
    rel = releases(VG)
    progs = {'gtrL': POWER, 'gtrR': POWER, 'bass': BASS, 'lead': LEAD, 'fb': FB}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, FAST) + 2 for k, pr in progs.items()}   # snel tempo = meeste ticks
    for k in DRUM_PARTS:
        tail[k] = 0                                            # drums: de noot zelf = de echte lengte
    for k in ('lead', 'fb'):          # riffs níet losmaken: de fuzz klinkt door tot de volgende aanslag (legato)
        P.n[k] = detach(P.n[k], tail[k])
    # zelfde toonhoogte mag in één spoor niet overlappen (de note-off van de eerste zou de tweede afkappen)
    for k in P.n:
        ns = sorted(P.n[k])
        for i, x in enumerate(ns):
            nxt = next((y[0] for y in ns[i + 1:] if y[2] == x[2] and y[0] >= x[0]), None)
            if nxt is not None and nxt < x[1]:
                x[1] = max(x[0] + 6, nxt - 1)
        P.n[k] = ns
    order = ['bass', 'gtrL', 'kick', 'snare', 'lead', 'hat', 'gtrR', 'cym', 'tom', 'fb']
    kept = allocate({k: P.n[k] for k in order}, order, tail, max_voices=11)
    print('tail (ticks bij %d bpm):' % FAST, {k: v for k, v in tail.items() if v})
    for k in order:
        n = len(P.n[k])
        print('  %-6s %4d noten, %3d vallen weg (%.1f%%)' % (k, n, n - len(kept[k]), 100 * (n - len(kept[k])) / max(n, 1)))
        P.n[k] = kept[k]
    save(P, OUT)
    print(OUT, '%.1f s intro, %.1f s loop (totaal %.1f s)' % (secs(A * BAR), secs(END * BAR) - secs(A * BAR), secs(END * BAR)))
    for nm, a, b in SECTIONS:
        print('  %-9s maat %2d-%2d  %3d bpm  %6.1f - %6.1f s' % (nm, a, b - 1, bpm_at(a * BAR), secs(a * BAR), secs(b * BAR)))
    print('stoner_checks OK:')
    for k, v in rep.items():
        print('  %-28s %.2f' % (k, v))


if __name__ == '__main__':
    main()
