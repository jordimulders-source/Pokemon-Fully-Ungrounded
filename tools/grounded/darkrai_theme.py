#!/usr/bin/env python3
"""Project Grounded: Battle! Darkrai, een eigen compositie. Jordi: 'mag echt fucked up klinken, dissonant, dat het
klinkt alsof er iets mis is, uncommon time signature.' Idee: een verstoord wiegelied, achterstevoren klanken.

Een speeldoos-wiegelied (E-klein) dat ontspoort: de speeldoos is ontstemd (+22 cent gebakken in de sample, plus per
noot een pitch bend van 10-40 cent), het wiegelied heeft een tritonus op de plek waar je de leidtoon verwacht, en het
gevecht loopt in 7/8 (2+2+3), in B wisselend 9/8-7/8-9/8-5/8.
150 bpm (kwart), een achtste = 0,2 s, een maat 7/8 = 1,4 s.

Intro = de transitie (Darkrai-transitie start ±25 frames na de muziek; zie MUZIEK.md, Jirachi):
  tel 0-2  het wiegelied begint lief op de speeldoos; daaronder zuigt een omgekeerd cluster aan
  tel 3    het blauwe oog gaat open (t = 46 + 25 frames = 1,19 s): clusterstoot E-F-Bb, de speeldoos zakt weg
  tel 4    het oog valt aan (t = 70 + 25 = 1,59 s): dreun (taiko, lage piano, pauk)
  tel 5    het scherm wordt zwart (t = 94 + 25 = 1,99 s): een volle tel niets
  2 ademmaten 7/8 (de cry van Darkrai, ±4-5 s): alleen een lage, bewegende drone en adem (ruis)
  1 opbouwmaat: hartslag + omgekeerd bekken -> de loop
Loop:
  A (8 x 7/8)  het wiegelied op de ontstemde speeldoos boven een chromatische 7/8-ostinato (piano-octaven: grondtoon,
               b2, tritonus); spookecho van de melodie op de PSG (een halve tel later, vals)
  B (9-7-9-5 x2) bitonale canon: het koor zingt het wiegelied een tritonus lager (Bb), de speeldoos antwoordt in E
               twee achtsten later; tritonus-slinger in de bas, taiko/toms, omgekeerde clusters vóór elke frase
  C (7 x 7/8)  de speeldoos loopt af (ritardando 150 -> 92 bpm, toonhoogte zakt twee halve tonen), dan plots stilte;
               het wiegelied achterstevoren (één sample) boven een kruipende drone, de cry van Darkrai achterstevoren,
               een versnellende hartslag; omgekeerd bekken -> D
  D (8 x 7/8)  climax: wiegelied in koor + strijkers + speeldoos (octaven), volle drums; de laatste maat breekt af
               na de eerste tel, alleen het omgekeerde bekken zuigt terug naar A.
v2 (Jordi: "80%", duisterder/Giratina-achtig): wisselende maten (A 7-7-6-7-5-9-7-8, B 9-7-10-5-9-6-11-5,
D 7-6-8-5-7-10-5-7), rauwe koperstoten (verminderd / tritonus-cluster, één sample per akkoord) en een orgeldrone
E-Bb onder het wiegelied; C ongewijzigd.
v3 (Jordi: 'sfeer goed, maar kabbelt op één niveau; mist een epische climax'): nieuwe volgorde A-B-R-D-C. R (4 x 7/8)
= opbouw vanuit het wiegelied (hartslag -> pauken/taiko -> koperstoten -> snareroffel in 16en, stijgende
tritonusstoten E-F-F#-G-G#-A-Bb, omgekeerd bekken); D = de climax halverwege de loop: denderende lage koperstoten
(darkrai_brass_low, E2-Bb2-E3-F3) + taiko op elke groep, schurend clusterakkoord (darkrai_scream, E-F-Bb-B) per maat;
C (ritardando, achterstevoren) is nu de nasleep vóór de terugsprong. CC7 per sectie (DYN): A rustig, R crescendo,
D het luidst. rev/revlong/cry delen één spoor (programma + CC7 per noot).
Gebruikt tools/grounded/musiclib.py; samples uit tools/grounded/darkrai_samples.py.
Gebruik: python3 tools/grounded/darkrai_theme.py"""
import os, sys, random
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

OUT = 'sound/songs/midi/mus_grounded_vs_darkrai.mid'
VG = 'grounded_darkrai'
TPB, BPM = 96, 150
E8 = TPB // 2                       # een achtste
Q = TPB
MAX_VOICES = 11                     # legendary
# programma's
PIANO_LO, CELESTA, BOX, REV_BOX, REV_CLUSTER, REV_LULLABY, CRY_REV = 1, 8, 10, 11, 12, 13, 14
TIMP, STRINGS, CHOIR, GHOST, SUB, BREATH, DRUMS = 47, 48, 52, 81, 84, 121, 127
BRASS_DIM, BRASS_TT, DRONE = 61, 62, 19         # v2: rauwe koperstoten (verminderd / tritonus-cluster), orgeldrone
LOWBRASS, SCREAM = 58, 49                       # v3: lage koperstoot (E2-Bb2-E3-F3), schurend clusterakkoord (E-F-Bb-B)
# drumkit (sound/voicegroups/drumsets/darkrai.inc)
KICK, SNARE, HAT, CRASH, REVCYM, TAIKO, TOM, HEART, TICK = 36, 37, 38, 39, 40, 41, 42, 43, 44

N = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'Ab': 8,
     'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def p(name):
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


# het wiegelied: 8 maten 7/8 (2+2+3), (noot, achtsten); maat 4 eindigt met de tritonus Bb-E i.p.v. B-E
LULLABY = [
    [('B4', 2), ('G4', 2), ('B4', 1), ('E5', 2)],
    [('D#5', 2), ('C5', 2), ('B4', 3)],
    [('A4', 2), ('C5', 2), ('B4', 1), ('G4', 2)],
    [('F#4', 2), ('Bb4', 2), ('E4', 3)],
    [('B4', 2), ('G4', 2), ('B4', 1), ('E5', 2)],
    [('F5', 2), ('E5', 2), ('D#5', 3)],
    [('C5', 2), ('B4', 2), ('A4', 1), ('F#4', 2)],
    [('G4', 2), ('F#4', 2), ('E4', 3)],
]
# bas per wiegeliedmaat (grondtoon, laagste octaaf >= E1)
ROOTS = ['E1', 'C2', 'A1', 'A#1', 'E1', 'F1', 'D#2', 'E1']

# ---- tijdlijn: (naam, achtsten per maat) ----
INTRO = [('I0', 6), ('I1', 6), ('BR1', 7), ('BR2', 7), ('BUILD', 7)]
# v2: de maten wisselen constant (Jordi: 'ontregelend'): 7/8, 3/4, 5/8, 4/4, 9/8, 5/4, 11/8
A_METER = [7, 7, 6, 7, 5, 9, 7, 8]
B_METER = [9, 7, 10, 5, 9, 6, 11, 5]
D_METER = [7, 6, 8, 5, 7, 10, 5, 7]
R_METER = [7, 7, 7, 7]              # v3: de opbouw (crescendo) van het wiegelied naar de climax
A = [('A%d' % i, m) for i, m in enumerate(A_METER)]
B = [('B%d' % i, m) for i, m in enumerate(B_METER)]
C = [('C%d' % i, 7) for i in range(7)]
D = [('D%d' % i, m) for i, m in enumerate(D_METER)]
R = [('R%d' % i, m) for i, m in enumerate(R_METER)]
BARS, t = {}, 0
for name, n in INTRO + A + B + R + D + C:          # v3: climax halverwege (A-B-R-D), daarna C als nasleep -> A
    BARS[name] = (t, n)
    t += n * E8
LOOP_START, END = BARS['A0'][0], t
# v3: dynamiek per sectie (CC7 op drums, bas, koper, drone): A rustig, B midden, R crescendo, D het luidst, C nasleep
DYN = {'A': {'drums': 76, 'bass': 80, 'brass': 76, 'drone': 62},
       'B': {'drums': 90, 'bass': 100, 'brass': 88, 'drone': 76},
       'R0': {'drums': 84, 'bass': 92, 'brass': 84, 'drone': 76},
       'R1': {'drums': 96, 'bass': 100, 'brass': 92, 'drone': 84},
       'R2': {'drums': 108, 'bass': 108, 'brass': 100, 'drone': 92},
       'R3': {'drums': 118, 'bass': 116, 'brass': 108, 'drone': 100},
       'D': {'drums': 124, 'bass': 120, 'brass': 112, 'drone': 104},
       'C': {'drums': 100, 'bass': 108, 'brass': 92, 'drone': 84}}
GROUPS = {11: (0, 2, 4, 7, 9), 10: (0, 3, 6, 8), 9: (0, 2, 4, 6), 8: (0, 3, 6), 7: (0, 2, 4), 6: (0, 2, 4),
          5: (0, 2)}
# v2: koperstoot per wiegeliedmaat: (grondtoon C3-B3, sample) -> E-dim, C-tt, A-dim, Bb-tt, E-dim, F-tt, D#-dim, E-tt
BRASS = [('E3', BRASS_DIM), ('C3', BRASS_TT), ('A3', BRASS_DIM), ('A#3', BRASS_TT), ('E3', BRASS_DIM),
         ('F3', BRASS_TT), ('D#3', BRASS_DIM), ('E3', BRASS_TT)]
RIT = (BARS['C0'][0], BARS['C3'][0])           # ritardando: de speeldoos loopt af


def bt(name, eighth=0):
    return BARS[name][0] + int(eighth * E8)


def fit(bar, n):
    """Wiegeliedmaat (7 achtsten) passend maken op n achtsten: de laatste noot langer, of (v2) van achteren inkorten."""
    out, pos = [], 0
    for nm, d in bar:
        if pos >= n:
            break
        out.append((nm, min(d, n - pos)))
        pos += out[-1][1]
    if pos < n:
        out[-1] = (out[-1][0], out[-1][1] + n - pos)
    return out


def melody(bar, start, vel, shift=0, gap=6):
    out, pos = [], start
    for nm, d in bar:
        out.append([pos, pos + d * E8 - gap, p(nm) + shift, vel])
        pos += d * E8
    return out


def BAR_OF(tick):
    return max((b for b in BARS.items() if b[1][0] <= tick), key=lambda b: b[1][0])[0]


def tempo_at(tick):
    if RIT[0] <= tick < RIT[1]:
        f = (tick - RIT[0]) / (RIT[1] - RIT[0])
        return 150 - (150 - 92) * f ** 1.4
    return 150


def build():
    rnd = random.Random(491)       # vaste seed: de ontstemming is elke keer gelijk
    P = {k: [] for k in ('box', 'celesta', 'rev', 'revlong', 'cry', 'strings', 'smel', 'choir', 'bass', 'timp',
                         'drums', 'ghost', 'sub', 'breath', 'brass', 'drone', 'lowbrass', 'scream')}
    box_bend = []                  # (tick, msb) voor de speeldoos
    str_bend = []
    ghost_bend = []

    def bend(lst, tick, msb):
        lst.append((int(tick), max(-64, min(63, int(msb)))))

    def box_notes(notes, wild):
        """speeldoosnoten met per noot een valse bend (wild: 0 = licht, 1 = sterk) en zakkende lange noten."""
        for s, e, n, v in notes:
            P['box'].append([s, e, n, v])
            c = rnd.choice((-1, 1)) * rnd.uniform(8, 18 + 22 * wild)          # cent
            bend(box_bend, s, c / 200 * 64)                                   # BENDR 2: 64 = 2 halve tonen
            if e - s >= 2 * E8:                                               # lange noot zakt weg (kromme band)
                for k in range(1, (e - s) // 12):
                    bend(box_bend, s + 12 * k, (c - k * (4 + 6 * wild)) / 200 * 64)

    # ---------------- intro: de transitie ----------------
    t0 = bt('I0')
    box_notes([[t0, t0 + Q - 6, p('B4'), 92], [t0 + Q, t0 + 2 * Q - 6, p('G4'), 96],
               [t0 + 2 * Q, t0 + 3 * Q - 6, p('B4'), 100]], 0)
    P['rev'].append([t0, t0 + 3 * Q, 72, 92])                    # omgekeerd cluster (1,2 s) zuigt naar het oog
    P['rev'][-1].append(REV_CLUSTER)
    eye = bt('I1')
    P['celesta'] += [[eye, eye + Q, n, 110] for n in (p('E5'), p('F5'), p('A#5'))]
    box_notes([[eye, eye + 2 * Q - 6, p('E5'), 112]], 1)
    for k in range(1, 15):                                             # het wiegelied glijdt weg (- 1,5 halve toon)
        bend(box_bend, eye + 12 * k, -k * 3.4)
    P['strings'] += [[eye, eye + 2 * Q - 8, n, 84] for n in (p('E3'), p('A#3'))]
    P['timp'].append([eye, eye + Q, p('E2'), 90])
    lunge = eye + Q
    P['drums'] += [[lunge, lunge + Q, TAIKO, 127], [lunge, lunge + 2 * Q, CRASH, 96]]
    P['bass'] += [[lunge, lunge + Q - 12, p('E1'), 120], [lunge, lunge + Q - 12, p('E2'), 110]]
    P['timp'].append([lunge, lunge + Q, p('E2'), 124])
    # tel 5 (zwart): niets.  Ademmaten: drone + adem, ruimte voor de cry
    for i, bar in enumerate(('BR1', 'BR2')):
        s = bt(bar)
        P['strings'] += [[s, s + 7 * E8 - 10, p('E2'), 60 + 8 * i], [s, s + 7 * E8 - 10, p('B2') - i, 54 + 8 * i]]
        P['sub'].append([s, s + 7 * E8 - 10, p('E2') + i, 70])
        P['breath'].append([s + 2 * E8, s + 6 * E8, 50, 80])
        P['drums'] += [[s + g * E8, s + g * E8 + E8, HEART, 70 + 10 * i] for g in (0, 4)]
    bend(str_bend, bt('BR1'), 0)
    for k in range(14):                                                # de drone zakt langzaam (kromme band)
        bend(str_bend, bt('BR1') + k * E8, -k * 0.8)
    s = bt('BR2', 4)                                                   # twee breekbare speeldoosnoten
    box_notes([[s, s + E8 - 4, p('B5'), 54], [s + E8, s + 2 * E8, p('A#5'), 50]], 1)
    s = bt('BUILD')
    P['drums'] += [[s + g * E8, s + g * E8 + E8, HEART, 90 + 6 * g] for g in (0, 2, 4, 5, 6)]
    P['drums'].append([s, s + 7 * E8, REVCYM, 100])
    P['bass'] += [[s + g * E8, s + g * E8 + E8 - 12, p('E1'), 100 + 6 * g] for g in (0, 2, 4)]
    P['sub'].append([s, s + 7 * E8 - 10, p('E2'), 80])
    P['strings'] += [[s, s + 7 * E8 - 10, p('E3'), 70], [s, s + 7 * E8 - 10, p('A#3'), 70]]
    for k in range(7):
        bend(str_bend, s + k * E8, 0)

    # ---------------- de loop ----------------
    def ostinato(bar, root, vel=112, full=True):
        """7/8-ostinato (2+2+3): grondtoon-octaaf, grondtoon, b2, grondtoon, tritonus (kort)."""
        s, n = BARS[bar]
        r = p(root)
        pat = [(0, 0, 2), (2, 0, 2), (4, 1, 1), (5, 0, 1), (6, 6, 1)] if n == 7 else \
            [(g, 0 if i % 2 == 0 else 6, 2 if g + 2 <= n else 1) for i, g in enumerate(GROUPS[n])]
        for pos, iv, ln in pat:
            st = s + pos * E8
            P['bass'].append([st, st + ln * E8 - 14, r + iv, vel])
            if full and iv == 0 and pos == 0:
                P['bass'].append([st, st + ln * E8 - 14, r + iv + 12, vel - 10])

    def kit(bar, style, vel=0):
        s, n = BARS[bar]
        if style == 'A':          # 7/8: K . S . K k S; andere maten: K op de groepen, S op groep 2 en de laatste achtste
            if n == 7:
                pat = ((0, KICK, 124), (2, SNARE, 108), (4, KICK, 118), (5, KICK, 76), (6, SNARE, 116))
            else:
                gs = GROUPS[n]
                pat = [(0, KICK, 124), (gs[1], SNARE, 108)] + [(g, KICK, 118) for g in gs[2:] if g != n - 1]
                pat += [(n - 2, KICK, 76)] if n - 2 not in (gs[1],) + gs[2:] and n - 2 > gs[1] else []
                pat += [(n - 1, SNARE, 116)] if n - 1 != gs[1] else []
            for pos, note, v in pat:
                P['drums'].append([s + pos * E8, s + pos * E8 + E8, note, v + vel])
            P['drums'] += [[s + i * E8, s + i * E8 + E8 // 2, HAT, 92 if i in GROUPS[n] else 60] for i in range(n)]
        elif style == 'B':        # halftime: taiko op elke groep, toms in de laatste groep
            gs = GROUPS[n]
            for i, g in enumerate(gs):
                P['drums'].append([s + g * E8, s + g * E8 + Q, TAIKO if i == 0 else TOM, 120 if i == 0 else 92])
            last = gs[-1]
            P['drums'].append([s + last * E8, s + last * E8 + E8, SNARE, 112])
            P['drums'] += [[s + i * E8, s + i * E8 + E8 // 2, TICK, 70 if i % 2 == 0 else 44] for i in range(n)]

    def drone(bar, vel=88):
        """v2: lage orgeldrone E1-Bb1-E2 (tritonus, één sample = één kanaal), per maat opnieuw."""
        s, n = BARS[bar]
        P['drone'].append([s, s + n * E8 - 10, 40, vel])

    def stab(bar, i, at, vel=112, dur=E8 - 8):
        """v2: rauwe GBA-brass-stoot (verminderd of tritonus-cluster, één sample per akkoord)."""
        s, n = BARS[bar]
        root, prog = BRASS[i % 8]
        for g in at:
            P['brass'].append([s + g * E8, s + g * E8 + dur, p(root), vel, prog])

    lul_i = 0
    # A: het wiegelied op de ontstemde speeldoos
    for i in range(8):
        bar = 'A%d' % i
        s, n = BARS[bar]
        mel = melody(fit(LULLABY[i], n), s, 96)        # v3: 104 -> 96, het wiegelied rustiger (contrast met de climax)
        box_notes(mel, 0 if i < 4 else 0.6)
        P['ghost'] += [[a + 3 * E8 // 2, b + 3 * E8 // 2, n - 12, 70] for a, b, n, v in mel]   # spookecho
        ostinato(bar, ROOTS[i])
        kit(bar, 'A')
        P['sub'].append([s, s + n * E8 - 10, p(ROOTS[i]) + 12, 80])
        if i % 2 == 1:
            P['celesta'] += [[s + 4 * E8, s + 5 * E8, x, 72] for x in (p('E6'), p('F6'))]
        if i in (3, 7):           # de valse maat: koor + strijkers op het tritonusakkoord
            P['choir'] += [[s, s + n * E8 - 12, x, 84] for x in (p('A#3'), p('E4'))]
            # v2: geen strijkers meer: de orgeldrone (E-Bb) + de tritonus-koperstoten dragen de valse maat
        elif i in (0, 1, 4, 5):
            P['strings'] += [[s + E8, s + n * E8 - 12, x, 66] for x in (p('E3'), p('B3'))]
        drone(bar, 84 if i < 4 else 96)
        # v2: rauwe koperstoot op de laatste groep (de valse maten 3/7: op elke groep)
        stab(bar, i, GROUPS[n] if i in (3, 7) else GROUPS[n][-1:], 108 if i < 4 else 116)
        if i in (0, 4):
            P['drums'].append([s, s + 2 * Q, CRASH, 104])
    P['rev'].append([bt('B0') - 288, bt('B0'), 72, 96, REV_CLUSTER])   # zuigt naar B

    # B: bitonale canon, koor in Bb (tritonus lager), speeldoos in E twee achtsten later
    pend = ['E1', 'A#1', 'E1', 'A#1', 'F1', 'B1', 'E1', 'A#1']
    for i in range(8):
        bar = 'B%d' % i
        s, n = BARS[bar]
        lb = fit(LULLABY[i], n)
        P['choir'] += melody(lb, s, 100, shift=-6, gap=10)
        mel = melody(lb, s + 2 * E8, 88, gap=6)
        mel = [x for x in mel if x[0] < s + n * E8]
        for x in mel:
            x[1] = min(x[1], s + n * E8 + 2 * E8 - 6)
        box_notes(mel, 0.8)
        ostinato(bar, pend[i], 104, full=False)
        kit(bar, 'B')
        P['timp'].append([s, s + Q, p(pend[i]) + 12, 110])
        P['sub'].append([s, s + n * E8 - 10, p(pend[i]) + 12, 70])
        # v2: de strijkerssecunde is vervangen door de orgeldrone (de kanalen gaan naar de koperstoten)
        drone(bar, 80)
        stab(bar, 3 if pend[i] in ('A#1', 'B1') else 7, (0,), 112, Q - 8)   # tritonus-cluster op de slinger
        if i % 4 == 3:            # omgekeerd cluster naar de volgende frase
            P['rev'].append([s + n * E8 - 288, s + n * E8, 72 + (0 if i == 3 else -1), 92, REV_CLUSTER])
        if i % 2 == 0:
            P['celesta'] += [[s + g * E8, s + g * E8 + E8, x, 66] for g in GROUPS[n][1:] for x in (p('A#5'), p('B5'))]
    P['drums'].append([bt('B0'), bt('B0') + 2 * Q, CRASH, 110])
    P['drums'].append([bt('B4'), bt('B4') + 2 * Q, CRASH, 104])

    # C: de speeldoos loopt af, stilte, achterstevoren
    for i in range(2):
        s = bt('C%d' % i)
        box_notes(melody(LULLABY[i], s, 98 - 10 * i, gap=4), 0.3)
        P['strings'] += [[s, s + 7 * E8 - 12, p('E3'), 50], [s, s + 7 * E8 - 12, p('B3'), 44]]
        P['drums'] += [[s + g * E8, s + g * E8 + E8 // 2, TICK, 60 - 10 * i] for g in range(7)]   # het mechaniekje
    for k in range(28):                                                 # toonhoogte zakt 2 halve tonen
        bend(box_bend, bt('C0') + k * 24, -64 * (k / 27) ** 1.6)
    s = bt('C3')
    P['revlong'].append([s, s + 28 * E8, 60, 110, REV_LULLABY])        # het wiegelied achterstevoren (4 maten)
    bend(box_bend, s, 0)
    cdrone = ['E2', 'F2', 'D#2', 'E2']
    for i in range(4):
        s = bt('C%d' % (3 + i))
        P['strings'].append([s, s + 7 * E8 - 12, p(cdrone[i]), 64 + 6 * i])
        P['sub'].append([s + E8, s + 7 * E8 - 10, p(cdrone[i]) + 12, 50 + 8 * i])
        P['breath'].append([s + E8, s + 5 * E8, 46 + i, 70 + 10 * i])
        beats = [(0, 4), (0, 3, 5), (0, 2, 4, 6), (0, 1, 2, 3, 4, 5, 6)][i]
        P['drums'] += [[s + g * E8, s + g * E8 + E8, HEART, 70 + 8 * i] for g in beats]
    s = bt('C5')
    P['cry'].append([s, s + 8 * E8, 60, 110, CRY_REV])                 # de cry van Darkrai achterstevoren
    P['cry'].append([bt('C6', 1), bt('C6', 1) + 9 * E8, 55, 96, CRY_REV])
    for k in range(28):                                                  # drone kruipt
        bend(str_bend, bt('C3') + k * E8, (k % 7) * -1.5)
    bend(str_bend, bt('C6'), 0)
    s = bt('C6')                                                        # omgekeerd bekken -> D (stilte vlak ervoor)
    P['drums'].append([s, s + 7 * E8, REVCYM, 112])
    P['bass'] += [[s + g * E8, s + g * E8 + E8 - 12, p('E1'), 90 + 6 * g] for g in (0, 2, 4, 5, 6)]

    def reg(pc, lo):
        return lo + (pc - lo) % 12

    def scream(bar, root, vel, start=0, end=None):
        """v3: schurend clusterakkoord (E-F-Bb-B, één sample) op de grondtoon, binnen een tritonus van E4."""
        s, n = BARS[bar]
        sh = (p(root) % 12 - 4 + 6) % 12 - 6
        P['scream'].append([s + start * E8, s + (end or n) * E8 - 12, 64 + sh, vel])

    def low(bar, root, at, vel=124, dur=2 * E8 - 10):
        """v3: denderende lage koperstoot (E2-Bb2-E3-F3 als één sample) op de grondtoon (C2-B2)."""
        s, n = BARS[bar]
        for g in at:
            P['lowbrass'].append([s + g * E8, s + g * E8 + dur, reg(p(root) % 12, 36), vel])

    # R (v3): de opbouw. Het wiegelied keert terug op de speeldoos, rustig, en wordt maat voor maat een nachtmerrie:
    # hartslag -> pauken -> koperstoten -> snareroffel + stijgende tritonusstoten + omgekeerd bekken -> de climax.
    for i in range(4):
        bar = 'R%d' % i
        s, n = BARS[bar]
        mel = melody(fit(LULLABY[i], n), s, 88 + 8 * i)
        box_notes(mel, 0.2 + 0.25 * i)
        if i >= 2:
            P['ghost'] += [[a + 3 * E8 // 2, b + 3 * E8 // 2, k - 12, 64 + 6 * i] for a, b, k, v in mel]
        if i < 3:
            drone(bar, 72 + 10 * i)
        P['sub'].append([s, s + n * E8 - 10, p(ROOTS[i]) + 12, 60 + 8 * i])
        if i == 0:
            P['drums'] += [[s + g * E8, s + g * E8 + E8, HEART, 80] for g in (0, 4)]
        elif i == 1:
            P['drums'] += [[s + g * E8, s + g * E8 + E8, HEART, 92] for g in (0, 2, 4)]
            P['drums'].append([s, s + Q, TAIKO, 104])
            P['bass'] += [[s + g * E8, s + g * E8 + 2 * E8 - 14, p(ROOTS[i]), 96] for g in (0, 2, 4)]
            P['timp'] += [[s + g * E8, s + g * E8 + Q, p(ROOTS[i]) + 12, 88 + 4 * g] for g in (0, 4)]
            scream(bar, ROOTS[i], 64, 2)
        elif i == 2:
            ostinato(bar, ROOTS[i], 104, full=False)
            P['drums'] += [[s + g * E8, s + g * E8 + E8, KICK, 112] for g in (0, 2, 4)]
            P['drums'] += [[s, s + Q, TAIKO, 116], [s + 6 * E8, s + 7 * E8, SNARE, 108]]
            P['drums'] += [[s + g * E8, s + g * E8 + Q, TOM, 84 + 6 * g] for g in (2, 4)]
            P['timp'] += [[s + g * E8, s + g * E8 + Q, p(ROOTS[i]) + 12, 100 + 3 * g] for g in (0, 2, 4)]
            stab(bar, i, GROUPS[n], 104)
            scream(bar, ROOTS[i], 84)
        else:                       # de laatste maat: alles stijgt, en dan breekt de nachtmerrie los
            ostinato(bar, ROOTS[i], 116, full=True)
            for k in range(14):     # snareroffel in 16en, crescendo
                P['drums'].append([s + k * E8 // 2, s + k * E8 // 2 + E8 // 2, SNARE, 72 + 4 * k])
            P['drums'] += [[s + g * E8, s + g * E8 + E8, KICK, 100 + 3 * g] for g in range(7)]
            P['drums'].append([s, s + 7 * E8, REVCYM, 116])
            for g, root in enumerate(('E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3')):   # stijgende tritonusstoten
                P['brass'].append([s + g * E8, s + g * E8 + E8 - 8, p(root), 100 + 4 * g, BRASS_TT])
            scream(bar, ROOTS[i], 104)

    # D: climax (v3: halverwege de loop, na de opbouw; denderende lage koperstoten, schurende clusterakkoorden,
    # taiko + pauk op elke groep)
    for i in range(8):
        bar = 'D%d' % i
        s, n = BARS[bar]
        lb = fit(LULLABY[i], n) if i < 7 else LULLABY[i]
        mel = melody(lb, s, 112)
        if i == 7:
            mel = [[a, min(b, s + 2 * E8 - 6), n, v] for a, b, n, v in mel if a < s + 2 * E8]   # breekt af na 1 tel
        box_notes([[a, b, n + 12, v] for a, b, n, v in mel], 0.7)
        P['choir'] += [[a, b - 4, n, 120] for a, b, n, v in mel]       # v3: 108 -> 120
        P['ghost'] += [[a + 3 * E8 // 2, b + 3 * E8 // 2, n, 76] for a, b, n, v in mel]
        if i < 7:
            # v3: de climax draagt nu het schurende clusterakkoord (i.p.v. orgeldrone, strijkersmelodie en celesta)
            # en denderende lage koperstoten + taiko op elke groep; geen hihats (de kanalen gaan naar het koper)
            ostinato(bar, ROOTS[i], 120, full=False)
            gs = GROUPS[n]
            P['drums'] += [[s + g * E8, s + g * E8 + E8, KICK, 126] for g in gs if g != gs[1]]
            P['drums'] += [[s + gs[1] * E8, s + gs[1] * E8 + E8, SNARE, 116], [s + (n - 1) * E8, s + n * E8, SNARE, 120]]
            P['drums'] += [[s + g * E8, s + g * E8 + Q, TAIKO, 124 if g == 0 else 110] for g in gs]
            P['sub'].append([s, s + n * E8 - 10, p(ROOTS[i]) + 12, 90])
            stab(bar, i, gs, 122)                           # v2: koperstoot op elke groep: het wiegelied als nachtmerrie
            if i % 2 == 0:
                P['drums'].append([s, s + 2 * Q, CRASH, 116])
            low(bar, ROOTS[i], gs, 124 if i == 0 else 118)
            scream(bar, ROOTS[i], 112 if i else 120)
        else:                     # afbreken na de eerste tel; het omgekeerde bekken (1 maat) zuigt terug naar A
            P['drums'] += [[s, s + E8, KICK, 124], [s, s + Q, TAIKO, 124], [s, s + 7 * E8, REVCYM, 112]]
            P['bass'] += [[s, s + 2 * E8 - 14, p('E1'), 120], [s, s + 2 * E8 - 14, p('E2'), 110]]
            P['timp'].append([s, s + Q, p('E2'), 116])
            stab(bar, 7, (0,), 124, Q - 8)
            low(bar, 'E1', (0,), 127, Q - 10)

    # ---------------- voicegroup + drumkit ----------------
    write_voicegroup()
    rel = releases(VG)
    progs = {'box': BOX, 'celesta': CELESTA, 'strings': STRINGS, 'smel': STRINGS, 'choir': CHOIR, 'bass': PIANO_LO,
             'timp': TIMP}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) for k, pr in progs.items()}
    tail.update({k: release_ticks(rel[pr], TPB, BPM) for k, pr in (('rev', REV_CLUSTER), ('revlong', REV_LULLABY),
                                                                       ('cry', CRY_REV))})
    tail['drums'] = 0              # drumnoten: echte lengte (het omgekeerde bekken = 1 maat)
    tail['brass'] = release_ticks(rel[BRASS_DIM], TPB, BPM)
    tail['drone'] = release_ticks(rel[DRONE], TPB, BPM)
    tail['lowbrass'] = release_ticks(rel[LOWBRASS], TPB, BPM)
    tail['scream'] = release_ticks(rel[SCREAM], TPB, BPM)
    for k in ('box', 'choir', 'smel'):
        P[k] = detach(P[k], tail[k])
    for k in P:
        if k not in ('rev', 'revlong', 'cry', 'brass', 'lowbrass'):
            P[k] = dedupe(P[k])
    order = ['box', 'bass', 'drums', 'revlong', 'choir', 'cry', 'lowbrass', 'scream', 'brass', 'drone', 'smel', 'rev',
             'timp', 'strings', 'celesta']
    ds = {k: [x[:4] for x in P[k]] for k in order}
    kept = allocate(ds, order, tail, max_voices=MAX_VOICES)
    for k in order:
        n = len(ds[k])
        lost = n - len(kept[k])
        print('  %-8s %3d noten, %2d weggevallen (%.0f%%)' % (k, n, lost, 100 * lost / max(n, 1)))
        keep = set(map(tuple, kept[k]))
        if lost and os.environ.get('DK_DROPS'):
            print('     ', sorted(set(BAR_OF(x[0]) for x in ds[k] if tuple(x) not in keep)))
        P[k] = [x for x in P[k] if tuple(x[:4]) in keep]

    # ---------------- wegschrijven ----------------
    song = Song(TPB, 500000)
    t = 0
    last = None
    while t < END:                                     # tempokaart per achtste (ritardando in C)
        b = int(round(tempo_at(t) / 2)) * 2           # mid2agb: even bpm
        if b != last:
            song.tempo(t, b / 120)
            last = b
        t += E8
    song.loop = (LOOP_START, END)

    def pw(lst):
        return [(tk, mido.Message('pitchwheel', pitch=max(-8192, min(8191, v * 128)))) for tk, v in sorted(lst)]

    def rev_split(lst):
        out = {}
        for s, e, n, v, prog in lst:
            out.setdefault(prog, []).append([s, e, n, v])
        return out

    layout = []

    def add(name, notes, prog, vol, ch, pan=64, extra=(), ccs=()):
        song.add(sorted(notes), prog, vol, ch, pan, extra=extra, ccs=ccs)
        layout.append(name)

    def dyn(part):
        """v3: CC7 per sectie (zie DYN), ook op het loopbegin (terugsprong)."""
        out = []
        for name, (st, n) in sorted(BARS.items(), key=lambda b: b[1][0]):
            key = name if name in DYN else name[0]
            if key in DYN and (name == key or name.endswith('0')):
                out.append((st, 7, DYN[key][part]))
        return out

    add('box', P['box'], BOX, 100, 0, 64, extra=pw(box_bend), ccs=[(0, 20, 2)])
    add('celesta', P['celesta'], CELESTA, 70, 1, 84)
    # v3: omgekeerde clusters, het omgekeerde wiegelied en de omgekeerde cry delen één spoor (programma + volume per
    # noot), zodat er twee sporen vrijkomen voor de climax
    fxvol = {REV_CLUSTER: 90, REV_LULLABY: 110, CRY_REV: 96}
    fx = sorted(P['rev'] + P['revlong'] + P['cry'])
    add('fx', [x[:4] for x in fx], REV_CLUSTER, 90, 2, 64,
        ccs=[c for x in fx for c in ((x[0], 'prog', x[4]), (x[0], 7, fxvol[x[4]]))])
    add('lowbrass', P['lowbrass'], LOWBRASS, 112, 3, 64)
    add('scream', P['scream'], SCREAM, 92, 4, 68)
    add('strings', P['strings'], STRINGS, 72, 5, 56, extra=pw(str_bend), ccs=[(0, 20, 2)])
    add('choir', P['choir'], CHOIR, 84, 7, 64)
    add('bass', P['bass'], PIANO_LO, 108, 8, 64, ccs=dyn('bass'))
    add('timp', P['timp'], TIMP, 92, 10, 64)
    add('ghost', P['ghost'], GHOST, 34, 11, 88, extra=[(0, mido.Message('pitchwheel', pitch=12 * 128))],
        ccs=[(0, 20, 1)])                                                     # +19 cent: vals
    add('sub', P['sub'], SUB, 60, 12, 64)
    add('breath', P['breath'], BREATH, 40, 13, 64)
    add('drums', P['drums'], DRUMS, 100, 9, 64, ccs=dyn('drums'))
    br = sorted(P['brass'])
    add('brass', [x[:4] for x in br], BRASS_DIM, 92, 14, 60, ccs=[(x[0], 'prog', x[4]) for x in br] + dyn('brass'))
    add('drone', P['drone'], DRONE, 84, 15, 64, ccs=dyn('drone'))
    assert not [k for k in P if P[k] and k not in layout + ['rev', 'revlong', 'cry']], 'partij niet weggeschreven'
    song.save(OUT, END)

    def sec(tick):
        s, t = 0.0, 0
        while t < tick:
            s += min(E8, tick - t) / TPB * 60 / tempo_at(t)
            t += E8
        return s
    print(OUT, '%d sporen, intro %.1f s, loop %.1f s' % (len(layout), sec(LOOP_START), sec(END) - sec(LOOP_START)))
    for nm in ('A0', 'B0', 'R0', 'D0', 'D7', 'C0', 'C3'):
        print('  %-3s %5.1f s' % (nm, sec(BARS[nm][0])))


def write_voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm + ontstemde speeldoos, omgekeerde samples en een eigen drumkit voor Battle! Darkrai.'
    lines[1] = '@ Gegenereerd door tools/grounded/darkrai_theme.py.'
    lines[2] = 'voice_group %s' % VG
    rep = {
        '@ 1': '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_piano1_48, 255, 252, 0, 180  @ 1',
        '@ 8': '\tvoice_directsound 60, 0, DirectSoundWaveData_darkrai_celesta, 255, 246, 0, 180  @ 8',
        '@ 10': '\tvoice_directsound 60, 0, DirectSoundWaveData_darkrai_music_box, 255, 249, 0, 196  @ 10',
        '@ 11': '\tvoice_directsound 60, 0, DirectSoundWaveData_darkrai_rev_box, 255, 0, 255, 120  @ 11',
        '@ 12': '\tvoice_directsound 60, 0, DirectSoundWaveData_darkrai_rev_cluster, 255, 0, 255, 120  @ 12',
        '@ 13': '\tvoice_directsound 60, 0, DirectSoundWaveData_darkrai_lullaby_rev, 255, 0, 255, 140  @ 13',
        '@ 14': '\tvoice_directsound 60, 0, DirectSoundWaveData_darkrai_cry_rev, 255, 0, 255, 140  @ 14',
        '@ 19': '\tvoice_directsound 60, 0, DirectSoundWaveData_darkrai_drone, 255, 0, 255, 150  @ 19',
        '@ 47': '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 200  @ 47',
        '@ 61': '\tvoice_directsound 60, 0, DirectSoundWaveData_darkrai_brass_dim, 255, 0, 255, 140  @ 61',
        '@ 62': '\tvoice_directsound 60, 0, DirectSoundWaveData_darkrai_brass_tt, 255, 0, 255, 140  @ 62',
        '@ 58': '\tvoice_directsound 60, 0, DirectSoundWaveData_darkrai_brass_low, 255, 0, 255, 150  @ 58',
        '@ 49': '\tvoice_directsound 60, 0, DirectSoundWaveData_darkrai_scream, 255, 0, 255, 150  @ 49',
        '@ 52': '\tvoice_directsound 60, 0, DirectSoundWaveData_classical_choir_voice_ahhs, 255, 0, 255, 160  @ 52',
        '@ 81': '\tvoice_square_2 60, 0, 2, 0, 2, 9, 2  @ 81',
        '@ 84': '\tvoice_programmable_wave_alt 60, 0, ProgrammableWaveData_1, 0, 7, 15, 2  @ 84',
        '@ 121': '\tvoice_noise 60, 0, 0, 7, 0, 15, 7  @ 121',
        '@ 127': '\tvoice_keysplit_all voicegroup_darkrai_drumset  @ 127',
    }
    out = []
    for l in lines:
        tag = l.rstrip().rsplit('  ', 1)[-1] if '@' in l else None
        out.append(rep.get(tag, l))
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    kit = [
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 0',           # 36 kick
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 160',         # 37 snare
        'voice_directsound_no_resample 60, 74, DirectSoundWaveData_unknown_close_hihat, 255, 127, 0, 120',       # 38 hihat
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165',      # 39 crash
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_darkrai_revcym, 255, 0, 255, 120',           # 40 omgekeerd bekken
        'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 0',                          # 41 taiko
        'voice_directsound 55, 52, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 120',                    # 42 lage tom
        'voice_directsound 50, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 0',                      # 43 hartslag
        'voice_directsound 84, 76, DirectSoundWaveData_ethnic_flavours_hyoushigi, 255, 0, 255, 60',            # 44 tikje
    ]
    open('sound/voicegroups/drumsets/darkrai.inc', 'w').write(
        '@ Project Grounded: drumkit voor Battle! Darkrai (darkrai_theme.py), alles DirectSound: 36 kick, 37 snare,\n'
        '@ 38 hihat, 39 crash, 40 omgekeerd bekken (darkrai_revcym, 1,4 s), 41 taiko, 42 lage tom, 43 hartslag\n'
        '@ (kick 10 halve tonen lager), 44 tikje (het mechaniek van de speeldoos).\n'
        'voice_group darkrai_drumset, 36\n' + ''.join('\t%s\n' % k for k in kit) + '\n')


if __name__ == '__main__':
    build()
