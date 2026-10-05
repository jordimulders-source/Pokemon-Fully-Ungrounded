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
A = [('A%d' % i, 7) for i in range(8)]
B = [('B%d' % i, m) for i, m in enumerate([9, 7, 9, 5, 9, 7, 9, 5])]
C = [('C%d' % i, 7) for i in range(7)]
D = [('D%d' % i, 7) for i in range(8)]
BARS, t = {}, 0
for name, n in INTRO + A + B + C + D:
    BARS[name] = (t, n)
    t += n * E8
LOOP_START, END = BARS['A0'][0], t
GROUPS = {9: (0, 2, 4, 6), 7: (0, 2, 4), 6: (0, 2, 4), 5: (0, 2)}
RIT = (BARS['C0'][0], BARS['C3'][0])           # ritardando: de speeldoos loopt af


def bt(name, eighth=0):
    return BARS[name][0] + int(eighth * E8)


def fit(bar, n):
    """Wiegeliedmaat (7 achtsten) passend maken op n achtsten: de laatste noot langer/korter."""
    bar = list(bar)
    nm, d = bar[-1]
    bar[-1] = (nm, max(1, d + n - 7))
    return bar


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
                         'drums', 'ghost', 'sub', 'breath')}
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
        if style == 'A':          # 7/8: K . S . K k S
            for pos, note, v in ((0, KICK, 124), (2, SNARE, 108), (4, KICK, 118), (5, KICK, 76), (6, SNARE, 116)):
                P['drums'].append([s + pos * E8, s + pos * E8 + E8, note, v + vel])
            P['drums'] += [[s + i * E8, s + i * E8 + E8 // 2, HAT, 92 if i in GROUPS[7] else 60] for i in range(7)]
        elif style == 'B':        # halftime: taiko op elke groep, toms in de laatste groep
            gs = GROUPS[n]
            for i, g in enumerate(gs):
                P['drums'].append([s + g * E8, s + g * E8 + Q, TAIKO if i == 0 else TOM, 120 if i == 0 else 92])
            last = gs[-1]
            P['drums'].append([s + last * E8, s + last * E8 + E8, SNARE, 112])
            P['drums'] += [[s + i * E8, s + i * E8 + E8 // 2, TICK, 70 if i % 2 == 0 else 44] for i in range(n)]

    lul_i = 0
    # A: het wiegelied op de ontstemde speeldoos
    for i in range(8):
        bar = 'A%d' % i
        s = bt(bar)
        mel = melody(LULLABY[i], s, 104)
        box_notes(mel, 0 if i < 4 else 0.6)
        P['ghost'] += [[a + 3 * E8 // 2, b + 3 * E8 // 2, n - 12, 70] for a, b, n, v in mel]   # spookecho
        ostinato(bar, ROOTS[i])
        kit(bar, 'A')
        P['sub'].append([s, s + 7 * E8 - 10, p(ROOTS[i]) + 12, 80])
        if i % 2 == 1:
            P['celesta'] += [[s + 4 * E8, s + 5 * E8, n, 72] for n in (p('E6'), p('F6'))]
        if i in (3, 7):           # de valse maat: koor + strijkers op het tritonusakkoord
            P['choir'] += [[s, s + 7 * E8 - 12, n, 84] for n in (p('A#3'), p('E4'))]
            P['strings'] += [[s, s + 7 * E8 - 12, n, 80] for n in (p('A#2'), p('F3'))]
        elif i in (0, 1, 4, 5):
            P['strings'] += [[s + E8, s + 7 * E8 - 12, n, 66] for n in (p('E3'), p('B3'))]
        if i in (0, 4):
            P['drums'].append([s, s + 2 * Q, CRASH, 104])
    P['rev'].append([bt('A7', 7) - 288, bt('A7', 7), 72, 96, REV_CLUSTER])   # zuigt naar B

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
        P['strings'] += [[s, s + n * E8 - 12, x, 62] for x in (p(pend[i]) + 24, p(pend[i]) + 25)]   # kleine secunde
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
    drone = ['E2', 'F2', 'D#2', 'E2']
    for i in range(4):
        s = bt('C%d' % (3 + i))
        P['strings'].append([s, s + 7 * E8 - 12, p(drone[i]), 64 + 6 * i])
        P['sub'].append([s + E8, s + 7 * E8 - 10, p(drone[i]) + 12, 50 + 8 * i])
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

    # D: climax
    for i in range(8):
        bar = 'D%d' % i
        s = bt(bar)
        lb = LULLABY[i]
        mel = melody(lb, s, 112)
        if i == 7:
            mel = [[a, min(b, s + 2 * E8 - 6), n, v] for a, b, n, v in mel if a < s + 2 * E8]   # breekt af na 1 tel
        box_notes([[a, b, n + 12, v] for a, b, n, v in mel], 0.7)
        P['choir'] += [[a, b - 4, n, 108] for a, b, n, v in mel]
        P['smel'] += [[a, b - 4, n - 12, 96] for a, b, n, v in mel]
        P['ghost'] += [[a + 3 * E8 // 2, b + 3 * E8 // 2, n, 76] for a, b, n, v in mel]
        if i < 7:
            ostinato(bar, ROOTS[i], 120)
            kit(bar, 'A', 6)
            P['sub'].append([s, s + 7 * E8 - 10, p(ROOTS[i]) + 12, 90])
            P['timp'].append([s, s + Q, p(ROOTS[i]) + 12 if p(ROOTS[i]) + 12 >= 40 else p(ROOTS[i]) + 24, 116])
            P['celesta'] += [[s + g * E8, s + g * E8 + E8, x, 76] for g in (2, 4) for x in (p('E6'), p('F6'))]
            if i % 2 == 0:
                P['drums'].append([s, s + 2 * Q, CRASH, 112])
        else:                     # afbreken na de eerste tel; het omgekeerde bekken (1 maat) zuigt terug naar A
            P['drums'] += [[s, s + E8, KICK, 124], [s, s + Q, TAIKO, 124], [s, s + 7 * E8, REVCYM, 112]]
            P['bass'] += [[s, s + 2 * E8 - 14, p('E1'), 120], [s, s + 2 * E8 - 14, p('E2'), 110]]
            P['timp'].append([s, s + Q, p('E2'), 116])

    # ---------------- voicegroup + drumkit ----------------
    write_voicegroup()
    rel = releases(VG)
    progs = {'box': BOX, 'celesta': CELESTA, 'strings': STRINGS, 'smel': STRINGS, 'choir': CHOIR, 'bass': PIANO_LO,
             'timp': TIMP}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) for k, pr in progs.items()}
    tail.update({k: release_ticks(rel[pr], TPB, BPM) for k, pr in (('rev', REV_CLUSTER), ('revlong', REV_LULLABY),
                                                                       ('cry', CRY_REV))})
    tail['drums'] = 0              # drumnoten: echte lengte (het omgekeerde bekken = 1 maat)
    for k in ('box', 'choir', 'smel'):
        P[k] = detach(P[k], tail[k])
    for k in P:
        if k not in ('rev', 'revlong', 'cry'):
            P[k] = dedupe(P[k])
    order = ['box', 'bass', 'drums', 'revlong', 'choir', 'cry', 'smel', 'rev', 'timp', 'strings', 'celesta']
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

    add('box', P['box'], BOX, 100, 0, 64, extra=pw(box_bend), ccs=[(0, 20, 2)])
    add('celesta', P['celesta'], CELESTA, 70, 1, 84)
    rv = rev_split(P['rev'])
    add('rev', sorted(rv.get(REV_CLUSTER, [])), REV_CLUSTER, 90, 2, 50)
    add('revlong', [x[:4] for x in P['revlong']], REV_LULLABY, 110, 3, 64)
    add('cry', [x[:4] for x in P['cry']], CRY_REV, 96, 4, 76)
    add('strings', P['strings'], STRINGS, 72, 5, 56, extra=pw(str_bend), ccs=[(0, 20, 2)])
    add('smel', P['smel'], STRINGS, 84, 6, 72)
    add('choir', P['choir'], CHOIR, 84, 7, 64)
    add('bass', P['bass'], PIANO_LO, 108, 8, 64)
    add('timp', P['timp'], TIMP, 92, 10, 64)
    add('ghost', P['ghost'], GHOST, 34, 11, 88, extra=[(0, mido.Message('pitchwheel', pitch=12 * 128))],
        ccs=[(0, 20, 1)])                                                     # +19 cent: vals
    add('sub', P['sub'], SUB, 60, 12, 64)
    add('breath', P['breath'], BREATH, 40, 13, 64)
    add('drums', P['drums'], DRUMS, 100, 9, 64)
    assert not [k for k in P if P[k] and k not in layout], 'partij niet weggeschreven'
    song.save(OUT, END)

    def sec(tick):
        s, t = 0.0, 0
        while t < tick:
            s += min(E8, tick - t) / TPB * 60 / tempo_at(t)
            t += E8
        return s
    print(OUT, '%d sporen, intro %.1f s, loop %.1f s' % (len(layout), sec(LOOP_START), sec(END) - sec(LOOP_START)))
    for nm in ('A0', 'B0', 'C0', 'C3', 'D0', 'D7'):
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
        '@ 47': '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 200  @ 47',
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
