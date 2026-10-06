#!/usr/bin/env python3
"""Project Grounded: Battle! Forces of Nature (Tornadus, Thundurus, Landorus), drie eigen composities op één thema.

Jordi: "voor Landorus, Tornadus en Thundurus ook wat bedenken ... die drie een vergelijkbaar theme geven met ander
tempo en instrumentatie". Eén gedeeld 'Forces'-motief (zelfde melodie en akkoordskelet), drie arrangementen.

Het motief (geschreven in D-klein, 8 maten): kop = gestippelde kwart D, dan E-F-A omhoog (een windstoot die opstijgt);
antwoord zakt stapsgewijs terug. Akkoorden A: Dm-Bb-C-A | Dm-Bb-Gm/A-Dm (i-bVI-bVII-V).
Brug B: dezelfde kop als sequens omhoog op Bb, C en D (de storm klimt), daarna Gm-A-Bb-A (dominant).
C (alleen Landorus): het motief in D-GROOT (D-Bb-C-D | G-A-Bb/C-D), triomfantelijk: Landorus bedaart de andere twee
en brengt de oogst (Abundant Shrine): trompetten, koor en buisklokken.

  Tornadus  (wind)      176 bpm, E-klein (+2). Fluit-lead, spiccato-strijkersloopjes en -arpeggio's, PSG-arpeggio's
                        en -echo, licht slagwerk (hihat, conga), windstoten = PSG-ruis met volume-zwelling en wervelende
                        pitch bend. Intro 4 maten, loop A-A2-B-S(werveling, 4 maten)-A3.
  Thundurus (bliksem)   152 bpm, C-klein (-2). Distortion-gitaarlead (+ PSG-unisono), gesyncopeerd motief (aanslagen een
                        16e vóór tel 3), trompetstoten off-beat, galopperende gitaarriff 3+3+2, synth-bas + PSG-sub,
                        snare met PSG-ruiscrack op elke backbeat, roffels, bliksem = crash + ruis die omlaag buigt.
                        Intro 4 maten, loop A-A2-B-K(stormbreak, 4 maten).
  Landorus  (aarde)     112 bpm, D-klein. Hoorns met het motief, trompetten erbij in A2/C, tuba, zware bas + PSG-sub,
                        pauken, taiko, galopperend strijkersostinato, koor; C = triomf in D-groot met buisklokken.
                        Intro 4 maten (aardrommel, hoornroep), loop A-A2-B-C.

Alleen Emerald-samples (geen eigen samples). Voicegroup voicegroup_grounded_forces (grounded_gm + overrides) en keysplit
keysplits/forces_spicc.inc (spiccato-strijkers, korte release). Stemverdeler max. 10 DirectSound-noten.
Schrijft ook FluidR3-referentie-MIDI's (met de octaafcorrecties van de GBA-samples) naar een map naar keuze:
  python3 tools/grounded/forces_theme.py [--ref <map>]
Zie tools/grounded/MUZIEK.md."""
import math, os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

VG = 'grounded_forces'
TPB = 96
S = TPB // 4                  # een 16e
BAR = TPB * 4

N = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'Ab': 8,
     'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def p(name):
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


# ---- het gedeelde materiaal (geschreven in D-klein) ----------------------------------------------------------------
CH = {'Dm': (2, (2, 5, 9)), 'Bb': (10, (10, 2, 5)), 'C': (0, (0, 4, 7)), 'A': (9, (9, 1, 4)), 'Gm': (7, (7, 10, 2)),
      'D': (2, (2, 6, 9)), 'G': (7, (7, 11, 2))}
PROG = {
    'A': [[(0, 'Dm')], [(0, 'Bb')], [(0, 'C')], [(0, 'A')], [(0, 'Dm')], [(0, 'Bb')], [(0, 'Gm'), (8, 'A')], [(0, 'Dm')]],
    'B': [[(0, 'Bb')], [(0, 'C')], [(0, 'Dm')], [(0, 'Dm')], [(0, 'Gm')], [(0, 'A')], [(0, 'Bb')], [(0, 'A')]],
    'C': [[(0, 'D')], [(0, 'Bb')], [(0, 'C')], [(0, 'D')], [(0, 'G')], [(0, 'A')], [(0, 'Bb'), (8, 'C')], [(0, 'D')]],
    'I': [[(0, 'Dm')], [(0, 'Dm')], [(0, 'Dm')], [(0, 'A')]],
}
PROG['S'] = PROG['K'] = PROG['A'][:4]
MEL = {   # (16e-stap, lengte in 16en, noot)
    'A': [[(0, 6, 'D5'), (6, 2, 'E5'), (8, 4, 'F5'), (12, 4, 'A5')],
          [(0, 8, 'G5'), (8, 2, 'F5'), (10, 2, 'E5'), (12, 4, 'D5')],
          [(0, 6, 'E5'), (6, 2, 'F5'), (8, 4, 'G5'), (12, 4, 'C6')],
          [(0, 8, 'A5'), (8, 4, 'E5'), (12, 4, 'C#5')],
          [(0, 6, 'D5'), (6, 2, 'E5'), (8, 4, 'F5'), (12, 4, 'A5')],
          [(0, 8, 'D6'), (8, 2, 'C6'), (10, 2, 'Bb5'), (12, 4, 'A5')],
          [(0, 4, 'G5'), (4, 4, 'Bb5'), (8, 4, 'A5'), (12, 2, 'G5'), (14, 2, 'E5')],
          [(0, 12, 'D5')]],
    'B': [[(0, 6, 'Bb4'), (6, 2, 'C5'), (8, 4, 'D5'), (12, 4, 'F5')],
          [(0, 6, 'C5'), (6, 2, 'D5'), (8, 4, 'E5'), (12, 4, 'G5')],
          [(0, 6, 'D5'), (6, 2, 'E5'), (8, 4, 'F5'), (12, 4, 'A5')],
          [(0, 12, 'D6'), (12, 2, 'C6'), (14, 2, 'A5')],
          [(0, 8, 'Bb5'), (8, 4, 'A5'), (12, 4, 'G5')],
          [(0, 8, 'E5'), (8, 4, 'C#5'), (12, 4, 'A4')],
          [(0, 6, 'D5'), (6, 2, 'E5'), (8, 4, 'F5'), (12, 4, 'G5')],
          [(0, 16, 'A5')]],
    'C': [[(0, 6, 'D5'), (6, 2, 'E5'), (8, 4, 'F#5'), (12, 4, 'A5')],
          [(0, 8, 'Bb5'), (8, 2, 'A5'), (10, 2, 'G5'), (12, 4, 'F5')],
          [(0, 6, 'E5'), (6, 2, 'F5'), (8, 4, 'G5'), (12, 4, 'C6')],
          [(0, 16, 'D6')],
          [(0, 6, 'B5'), (6, 2, 'A5'), (8, 4, 'G5'), (12, 4, 'D6')],
          [(0, 8, 'C#6'), (8, 4, 'B5'), (12, 4, 'A5')],
          [(0, 4, 'F5'), (4, 4, 'Bb5'), (8, 4, 'G5'), (12, 4, 'C6')],
          [(0, 16, 'D6')]],
}
SCALE = (2, 4, 5, 7, 9, 10, 0)      # D-eolisch
KICK, SNARE, OSNARE, TOM_L, HH, TOM_M, TOM_H, TOM_X, TAMB, CRASH, CONGA_H, CONGA_L = \
    36, 38, 40, 41, 42, 45, 47, 48, 54, 57, 62, 64

# programma's in voicegroup_grounded_forces
BELL, ORGAN, FBASS, SBASS, DIST_LO, DIST_HI, STR, TIMP, SPICC, CHOIR, TPT, TUBA, HORN, FLUTE, TAIKO, KIT = \
    14, 19, 33, 38, 29, 30, 48, 47, 49, 52, 56, 58, 60, 73, 116, 127
SQ_ARP, SQ_LEAD, SQ_ECHO, WAVE, GUST, CRACK = 80, 81, 82, 84, 121, 122
TAIKO_KEY = 57      # sc88pro_taiko klinkt 88 Hz op toets 60 (gemeten); 57 = 74 Hz = D2, de grondtoon (C3 gaf 44 Hz-dreun)
OCT_DOWN = {DIST_LO: 12, ORGAN: 12}   # GBA-sample klinkt een octaaf lager dan geschreven (gemeten): geschreven +12


def near(pc, lo):
    return lo + ((pc - lo) % 12)


def segs(sec, i):
    s = PROG[sec][i]
    return [(st, s[k + 1][0] if k + 1 < len(s) else 16, name) for k, (st, name) in enumerate(s)]


def chord_at(sec, i, step):
    return [n for st, n in PROG[sec][i] if st <= step][-1]


def tones(name, lo, hi):
    return [m for m in range(lo, hi + 1) if m % 12 in CH[name][1]]


def scale(lo, hi, harmonic=False):
    pcs = set(SCALE) - ({0} if harmonic else set()) | ({1} if harmonic else set())
    return [m for m in range(lo, hi + 1) if m % 12 in pcs]


def mel(sec, i, t0, vel, shift=0, pat=None):
    return [[t0 + st * S, t0 + (st + ln) * S, p(n) + shift, vel] for st, ln, n in (pat or MEL[sec][i])]


def push(pat):
    """Thundurus: de aanslag op tel 3 een 16e naar voren (gesyncopeerd), de vorige noot korter."""
    out = [list(x) for x in pat]
    for k in range(1, len(out)):
        if out[k][0] == 8 and out[k - 1][0] < 7:
            out[k][0], out[k][1] = 7, out[k][1] + 1
            out[k - 1][1] = 7 - out[k - 1][0]
    return out


def harmony_below(notes, sec_of):
    """Tweede stem: de hoogste akkoordtoon minstens een kleine terts onder elke melodienoot."""
    out = []
    for s, e, n, v in notes:
        sec, i, t0 = sec_of(s)
        ch = chord_at(sec, i, (s - t0) // S)
        cand = [m for m in tones(ch, n - 9, n - 3)]
        if cand:
            out.append([s, e, max(cand), v])
    return out


class Parts(dict):
    def __missing__(self, k):
        self[k] = []
        return self[k]


def gust(P, CC, EX, name, t0, length, key, vmax, wobble=5, seed=0, down=False):
    """Windstoot/donder op een PSG-ruisspoor: één noot, CC7 zwelt aan en af, pitch bend wervelt (BENDR 12)."""
    P[name].append([t0, t0 + length, key, 110])
    steps = max(2, length // S)
    for k in range(steps + 1):
        x = k / steps
        CC[name].append((t0 + k * S, 7, int(8 + vmax * math.sin(math.pi * min(1.0, x)) ** 1.5)))
        semis = (-12 * x) if down else wobble * math.sin(2 * math.pi * (x * 1.5 + seed * 0.37))
        EX[name].append((t0 + k * S, mido.Message('pitchwheel', pitch=max(-8192, min(8191, int(semis / 12 * 8191))))))


def timeline(plan):
    tl = []
    for sec, n, var in plan:
        for i in range(n):
            tl.append((len(tl), sec, i, var))
    return tl


# ---- Tornadus: wind -------------------------------------------------------------------------------------------------
def tornadus():
    P, CC, EX = Parts(), Parts(), Parts()
    tl = timeline([('I', 4, ''), ('A', 8, 'a1'), ('A', 8, 'a2'), ('B', 8, ''), ('S', 4, ''), ('A', 8, 'a3')])
    for b, sec, i, var in tl:
        t0 = b * BAR
        sg = segs(sec, i)
        # PSG-arpeggio's: wervelend over twee octaven, op en neer
        if sec == 'I' or var in ('a1', 'a3') or sec in ('B', 'S'):
            for st, en, ch in sg:
                ts = tones(ch, 57, 81)
                cyc = ts + ts[-2:0:-1]
                for k in range(st, en):
                    vel = 50 + 6 * b if sec == 'I' else 72
                    P['arp'].append([t0 + k * S, t0 + k * S + S - 4, cyc[(k * (2 if sec == 'S' else 1)) % len(cyc)],
                                     min(vel, 84)])
        root = CH[chord_at(sec, i, 0)][0]
        if sec == 'I':
            if b == 0:
                gust(P, CC, EX, 'gust', t0, 2 * BAR - S, 64, 100, seed=1)
            if b >= 1:
                for st, en, ch in sg:
                    for n in tones(ch, 57, 69)[1:3]:
                        P['pad'] += [[t0 + h * 8 * S, t0 + h * 8 * S + 8 * S - 8, n, 46 + 6 * b] for h in (0, 1)]
            if b == 2:      # strijkersloop omhoog, twee octaven
                run = scale(p('D4'), p('E6'))
                P['runs'] += [[t0 + k * S, t0 + k * S + S, run[k], 60 + k * 3] for k in range(16)]
                P['drums'] += [[t0 + k * TPB, t0 + k * TPB + 2 * S, KICK, 80 + 6 * k] for k in range(4)]
                P['wave'] += [[t0, t0 + BAR - 8, near(root, 38), 70]]
            if b == 3:      # op de dominant: fluit zwelt, strijkers-arpeggio, snare-opbouw
                P['lead'] += [[t0, t0 + 6 * S, p('A5'), 96], [t0 + 6 * S, t0 + 8 * S, p('G5'), 100],
                              [t0 + 8 * S, t0 + 12 * S, p('F5'), 104], [t0 + 12 * S, t0 + 16 * S, p('E5'), 108]]
                arp = tones('A', 57, 81)
                P['runs'] += [[t0 + k * S, t0 + k * S + S, arp[k % len(arp)], 78] for k in range(16)]
                P['drums'] += [[t0 + k * 2 * S, t0 + k * 2 * S + S, SNARE, 50 + 5 * k] for k in range(4)]
                P['drums'] += [[t0 + 8 * S + k * S, t0 + 9 * S + k * S, SNARE, 70 + 6 * k] for k in range(8)]
                P['drums'] += [[t0 + k * TPB, t0 + k * TPB + 2 * S, KICK, 100] for k in range(4)]
                P['bass'] += [[t0 + k * 2 * S, t0 + k * 2 * S + S, near(9, 38), 96] for k in range(8)]
                gust(P, CC, EX, 'gust', t0 + 8 * S, 8 * S, 70, 110, seed=2)
            continue
        # ---- loop ----
        if sec == 'A':
            vel = {'a1': 106, 'a2': 110, 'a3': 116}[var]
            P['lead'] += mel('A', i, t0, vel)
        elif sec == 'B':
            P['lead'] += mel('B', i, t0, 110)
        # strijkers
        if sec == 'A' and var == 'a1':
            if i in (3, 7):        # loopje in de lange melodienoot naar de volgende frase
                run = scale(p('A4') if i == 3 else p('D4'), p('D6'), harmonic=(i == 3))
                P['runs'] += [[t0 + (8 + k) * S, t0 + (9 + k) * S, run[k], 70 + k * 4] for k in range(8)]
        elif sec == 'A':
            for st, en, ch in sg:       # spiccato-ostinato in 16en onder de melodie
                ts = tones(ch, 50, 64)[:4]
                cyc = ts + ts[-2:0:-1]
                P['runs'] += [[t0 + k * S, t0 + k * S + S, cyc[k % len(cyc)], 74 if k % 4 == 0 else 60] for k in range(st, en)]
        elif sec == 'B':
            if i % 2 == 1 and i != 7:
                ch = chord_at('B', i, 8)
                run = scale(near(CH[ch][0], 62), p('D6'), harmonic=(ch == 'A'))
                P['runs'] += [[t0 + (8 + k) * S, t0 + (9 + k) * S, run[k], 66 + k * 4] for k in range(8)]
            if i == 7:
                run = scale(p('A3'), p('Bb5'), harmonic=True)
                P['runs'] += [[t0 + k * S, t0 + (k + 1) * S, run[k], 60 + k * 3] for k in range(16)]
        elif sec == 'S':               # werveling: tutti-loopjes op en neer
            lo = {0: p('D4'), 1: p('D6'), 2: p('C4'), 3: p('A3')}[i]
            if i == 3:
                arp = tones('A', 57, 81)
                seq = arp + arp[::-1]
            else:
                sc = scale(min(lo, p('D4') - 2), p('D6') + 2)
                seq = [m for m in sc if m >= lo][:16] if i != 1 else [m for m in sc if m <= lo][::-1][:16]
            P['runs'] += [[t0 + k * S, t0 + (k + 1) * S, seq[k % len(seq)], 76 + (k % 4 == 0) * 10] for k in range(16)]
            if i < 3:   # fluit antwoordt met de kop van het motief, een octaaf hoger gewerveld
                P['lead'] += mel('A', 0, t0, 100, pat=[(0, 3, 'A5'), (3, 1, 'G5'), (4, 2, 'F5'), (6, 2, 'E5')]) \
                    if i == 0 else mel('A', 0, t0, 100, pat=[(0, 6, 'D5'), (6, 2, 'E5'), (8, 4, 'F5'), (12, 4, 'A5')]) \
                    if i == 2 else []
        # bas
        for st, en, ch in sg:
            r = near(CH[ch][0], 38)
            if sec == 'B':
                P['bass'] += [[t0 + st * S, t0 + (st + 6) * S, r, 98]] + ([[t0 + (st + 8) * S, t0 + (st + 14) * S, r, 92]] if en - st > 8 else [])
            else:
                for k in (0, 3, 6, 8, 11, 14):
                    if st <= k < en:
                        P['bass'].append([t0 + k * S, t0 + k * S + 2 * S - 6, r + (12 if (sec == 'S' and k == 14) else 0), 104 if k in (0, 8) else 92])
            P['wave'] += [[t0 + st * S, t0 + en * S - 8, near(CH[ch][0], 38), 64]]
        # koor-pad (luchtig), niet in de werveling
        if sec != 'S':
            for st, en, ch in sg:
                for n in tones(ch, 57, 69)[1:3]:
                    for h in range(st, en, 8):
                        P['pad'].append([t0 + h * S, t0 + min(en, h + 8) * S - 8, n, 54 if sec == 'A' else 62])
        # drums (licht): kick 1 + 3, snare 2 + 4, hihat in achtsten, conga's in B/S/A3
        P['drums'] += [[t0 + k * S, t0 + k * S + 2 * S, KICK, 108] for k in ((0, 8) if sec != 'S' else (0, 4, 8, 12))]
        if var in ('a2', 'a3'):
            P['drums'].append([t0 + 10 * S, t0 + 12 * S, KICK, 92])
        P['drums'] += [[t0 + k * S, t0 + k * S + 3 * S, SNARE, 84 if sec != 'B' else 76] for k in (4, 12)]
        P['hats'] += [[t0 + k * S, t0 + k * S + S, HH, 66 if k % 4 == 0 else 52] for k in range(0, 16, 2)]
        if sec in ('B', 'S') or var == 'a3':
            P['hats'] += [[t0 + k * S, t0 + k * S + 2 * S, CONGA_H if k in (3, 11) else CONGA_L, 70] for k in (3, 7, 11, 14)]
        if i == 0:
            P['drums'].append([t0, t0 + 2 * TPB, CRASH, 100])
        if (sec == 'A' and i == 7) or (sec == 'B' and i == 7) or (sec == 'S' and i == 3):
            P['drums'] += [[t0 + k * S, t0 + (k + 1) * S, SNARE, 60 + 4 * k] for k in range(8, 16)]
        # PSG-echo van de fluit
        # windstoten
        if i == 7 or (sec == 'B' and i % 2 == 1) or sec == 'S':
            ln = 8 * S if sec != 'S' else BAR - S
            gust(P, CC, EX, 'gust', t0 + (BAR - ln - S if sec != 'S' else 0), ln, 60 + 4 * (i % 3), 96, seed=b)
    for s, e, n, v in P['lead']:
        if s >= 12 * BAR and not (20 * BAR <= s < 32 * BAR):
            P['echo'].append([s + 3 * S, e + 3 * S, n, int(v * 0.55)])
    return dict(parts=P, cc=CC, ex=EX, end=len(tl) * BAR, loop=4, bpm=176, shift=2,
                order=['lead', 'bass', 'drums', 'hats', 'runs', 'pad'],
                detach=('lead', 'pad'),
                layout=[('lead', FLUTE, 112, 0, 64), ('runs', SPICC, 84, 1, 44), ('pad', CHOIR, 58, 2, 84),
                        ('bass', FBASS, 104, 3, 64), ('arp', SQ_ARP, 40, 4, 40), ('echo', SQ_ECHO, 34, 5, 96),
                        ('wave', WAVE, 50, 6, 64), ('gust', GUST, 60, 7, 64)],
                drums=('drums', 'hats'))


# ---- Thundurus: bliksem ---------------------------------------------------------------------------------------------
RIFF = [(0, 3), (3, 3), (6, 2), (8, 3), (11, 3), (14, 2)]          # 3+3+2 | 3+3+2


def thundurus():
    P, CC, EX = Parts(), Parts(), Parts()
    tl = timeline([('I', 4, ''), ('A', 8, 'a1'), ('A', 8, 'a2'), ('B', 8, ''), ('K', 4, '')])
    for b, sec, i, var in tl:
        t0 = b * BAR
        sg = segs(sec, i)
        if sec == 'I':
            if b == 0:      # donder: tomroffel + lage ruis
                P['drums'] += [[t0 + k * S, t0 + (k + 1) * S, (TOM_L, TOM_L, TOM_M, TOM_L)[k % 4], 50 + 4 * k] for k in range(16)]
                gust(P, CC, EX, 'crack', t0, BAR, 40, 90, wobble=3)
                P['wave'] += [[t0, t0 + BAR - 8, p('D2'), 80]]
                P['bass'] += [[t0 + 8 * S, t0 + 16 * S - 8, p('D2'), 90]]
            if b == 1:      # BLIKSEM op tel 1, daarna stil (cry)
                P['drums'] += [[t0, t0 + 2 * TPB, CRASH, 124], [t0, t0 + 2 * S, KICK, 124]]
                P['stabs'] += [[t0, t0 + 2 * S, n, 120] for n in (p('F4'), p('A4'))]
                gust(P, CC, EX, 'crack', t0, TPB, 76, 120, down=True)
                P['zap'] += [[t0 + k * 12, t0 + k * 12 + 12, n, 90] for k, n in enumerate(tones('Dm', 62, 98)[::-1][:12])]
                P['bass'] += [[t0, t0 + 6 * S, p('D2'), 110]]
                P['wave'] += [[t0, t0 + BAR - 8, p('D2'), 80]]
                P['riff'] += [[t0 + k * S, t0 + k * S + S, p('D2') + 12, 60 + 3 * k] for k in (8, 10, 12, 14)]
            if b >= 2:      # riff valt in, opbouw
                ch = chord_at('I', b, 0)
                r = near(CH[ch][0], 38)
                P['riff'] += [[t0 + st * S, t0 + (st + ln) * S - 10, r + 12, 104] for st, ln in RIFF]
                P['bass'] += [[t0 + st * S, t0 + (st + ln) * S - 10, r, 108] for st, ln in RIFF]
                P['wave'] += [[t0, t0 + BAR - 8, r, 80]]
                P['drums'] += [[t0 + st * S, t0 + st * S + 2 * S, KICK, 110] for st, _ in RIFF]
                if b == 2:
                    P['hats'] += [[t0 + k * S, t0 + k * S + S, HH, 70] for k in range(0, 16, 2)]
                    P['stabs'] += [[t0 + k * S, t0 + k * S + S, n, 110] for k in (3, 6, 11, 14) for n in (p('F4'), p('A4'))]
                else:
                    P['drums'] += [[t0 + k * S, t0 + (k + 1) * S, SNARE, 70 + 3 * k] for k in range(16)]
                    P['cracks'] += [[t0 + k * S, t0 + k * S + S, 72, 60 + 3 * k] for k in range(0, 16, 2)]
                    P['stabs'] += [[t0 + k * S, t0 + k * S + S, n, 116] for k in (0, 3, 6) for n in (p('E4'), p('A4'))]
                    P['zap'] += [[t0 + 8 * S + k * 12, t0 + 8 * S + k * 12 + 12, n, 80] for k, n in enumerate(tones('A', 57, 93)[:16])]
            continue
        if sec == 'A':
            P['lead'] += mel('A', i, t0, 112, pat=push(MEL['A'][i]))
            if var == 'a2':
                P['lead2'] += mel('A', i, t0, 96, pat=push(MEL['A'][i]))
        elif sec == 'B':
            P['lead'] += mel('B', i, t0, 112, pat=push(MEL['B'][i]))
            P['lead2'] += mel('B', i, t0, 90, pat=push(MEL['B'][i]))
        # riff + bas + sub
        for st, en, ch in sg:
            r = near(CH[ch][0], 38)
            if sec == 'B' and i < 6:     # half-time
                pat = [(0, 6), (8, 6)]
            else:
                pat = RIFF
            for k, ln in pat:
                if st <= k < en:
                    P['riff'].append([t0 + k * S, t0 + (k + ln) * S - 10, r + 12, 108 if k in (0, 8) else 96])
                    P['bass'].append([t0 + k * S, t0 + (k + ln) * S - 10, r, 112 if k in (0, 8) else 100])
            P['wave'].append([t0 + st * S, t0 + en * S - 8, r, 80])
        # koperstoten (off-beat, gesyncopeerd)
        if var == 'a2' or sec in ('B', 'K'):
            hits = (2, 5, 10, 13) if sec != 'K' else (0, 3, 6, 8, 11, 14)
            if sec == 'B' and i % 2 == 0:
                hits = (6, 14)
            for k in hits:
                ch = chord_at(sec, i, k)
                for n in tones(ch, 62, 72)[:2]:
                    P['stabs'].append([t0 + k * S, t0 + k * S + S, n, 118 if sec == 'K' else 108])
        # orgelpad in de brug
        if sec == 'B':
            for st, en, ch in sg:
                for n in tones(ch, 50, 62)[1:2]:
                    for h in range(st, en, 8):
                        P['pad'].append([t0 + h * S, t0 + min(en, h + 8) * S - 8, n + 12, 70])
        # elektrische arpeggio's (PSG)
        if sec in ('B', 'K') or var == 'a2':
            for st, en, ch in sg:
                ts = tones(ch, 62, 86)
                for k in range(st, en):
                    P['zap'].append([t0 + k * S, t0 + k * S + S - 6, ts[(k * 3) % len(ts)], 70])
        # drums: snare-zwaar
        half = sec == 'B' and i < 6
        if half:
            kicks, snares = (0, 3, 10), (8,)
        else:
            kicks, snares = (0, 3, 6, 10), (4, 12)
        P['drums'] += [[t0 + k * S, t0 + k * S + 2 * S, KICK, 116] for k in kicks]
        P['drums'] += [[t0 + k * S, t0 + k * S + 3 * S, SNARE, 120] for k in snares]
        P['cracks'] += [[t0 + k * S, t0 + k * S + S, 74, 110] for k in snares]
        P['hats'] += [[t0 + k * S, t0 + k * S + S, HH, 74 if k % 4 == 0 else 58] for k in range(0, 16, 2)]
        if i % 4 == 0:
            P['drums'].append([t0, t0 + 2 * TPB, CRASH, 112])
            gust(P, CC, EX, 'crack', t0, TPB, 76, 100, down=True)
        if (sec == 'A' and i == 7) or (sec == 'B' and i in (6, 7)) or (sec == 'K' and i == 3):
            if sec == 'K' or (sec == 'B' and i == 7):
                fill = [(k, (TOM_X, TOM_H, TOM_M, TOM_L)[(k - 8) // 2]) for k in range(8, 16)]
                P['drums'] += [[t0 + k * S, t0 + (k + 1) * S, n, 100 + k] for k, n in fill]
            else:
                P['drums'] += [[t0 + k * S, t0 + (k + 1) * S, SNARE, 72 + 4 * (k - 8)] for k in range(8, 16)]
                P['cracks'] += [[t0 + k * S, t0 + k * S + S, 72, 70 + 4 * (k - 8)] for k in range(8, 16, 2)]
        if sec == 'K':    # stormbreak: bliksem op tel 1 van maat 1 en 3
            if i in (0, 2):
                P['drums'].append([t0, t0 + 2 * TPB, CRASH, 124])
            P['zap'] += [[t0 + 12 * S + k * 12, t0 + 12 * S + k * 12 + 12, n, 84]
                         for k, n in enumerate(tones(chord_at('K', i, 12), 62, 98)[::-1][:8])]
            if i == 3:     # de lead schreeuwt omhoog naar de loop
                P['lead'] += [[t0, t0 + 8 * S, p('E5'), 112], [t0 + 8 * S, t0 + 16 * S - 8, p('A5'), 116]]
    return dict(parts=P, cc=CC, ex=EX, end=len(tl) * BAR, loop=4, bpm=152, shift=-2,
                order=['lead', 'drums', 'bass', 'riff', 'stabs', 'hats', 'pad'],
                detach=('lead', 'pad'),
                layout=[('lead', DIST_HI, 100, 0, 64), ('riff', DIST_LO, 84, 1, 50), ('stabs', TPT, 92, 2, 78),
                        ('bass', SBASS, 110, 3, 64), ('pad', ORGAN, 60, 4, 64), ('lead2', SQ_LEAD, 34, 5, 64),
                        ('zap', SQ_ARP, 36, 6, 90), ('wave', WAVE, 56, 7, 64), ('crack', GUST, 70, 8, 64),
                        ('cracks', CRACK, 64, 10, 64)],
                drums=('drums', 'hats'))


# ---- Landorus: aarde ------------------------------------------------------------------------------------------------
def landorus():
    P, CC, EX = Parts(), Parts(), Parts()
    tl = timeline([('I', 4, ''), ('A', 8, 'a1'), ('A', 8, 'a2'), ('B', 8, ''), ('C', 8, '')])
    for b, sec, i, var in tl:
        t0 = b * BAR
        sg = segs(sec, i)
        if sec == 'I':
            if b == 0:      # aardrommel: paukenroffel, taiko, lage ruis, bas-pedaal
                P['timp'] += [[t0 + k * S, t0 + (k + 1) * S, p('D2'), 44 + 4 * k] for k in range(16)]
                P['taiko'].append([t0, t0 + TPB, TAIKO_KEY, 110])
                gust(P, CC, EX, 'rumble', t0, 2 * BAR - S, 36, 80, wobble=2)
            if b in (0, 1):
                P['bass'].append([t0, t0 + BAR - 8, p('D2'), 96])
                P['wave'].append([t0, t0 + BAR - 8, p('D2'), 80])
            if b == 1:      # ostinato begint zacht (cry)
                P['taiko'] += [[t0 + k * S, t0 + k * S + TPB, TAIKO_KEY, 100] for k in (0, 8)]
                P['strings'] += [[t0 + k * S, t0 + k * S + S, p('D3'), 50 + 2 * k] for k in range(16) if k % 4 != 3]
            if b == 2:      # de hoornroep: de kop van het motief
                P['horn'] += mel('A', 0, t0, 112, shift=-12)
                P['tuba'] += [[t0, t0 + 8 * S - 8, p('D3'), 100], [t0 + 8 * S, t0 + 16 * S - 8, p('A3'), 100]]
                P['timp'] += [[t0, t0 + 2 * S, p('D2'), 120], [t0 + 8 * S, t0 + 10 * S, p('A2') - 12, 110]]
                P['taiko'] += [[t0 + k * S, t0 + k * S + TPB, TAIKO_KEY, 110] for k in (0, 6, 8)]
                P['strings'] += [[t0 + k * S, t0 + k * S + S, p('D3'), 70] for k in range(16) if k % 4 != 3]
                P['bass'] += [[t0, t0 + 6 * S - 8, p('D2'), 108], [t0 + 8 * S, t0 + 16 * S - 8, p('D2'), 104]]
                P['wave'].append([t0, t0 + BAR - 8, p('D2'), 80])
            if b == 3:      # dominant: hoorn houdt A, roffel, crash op de loop
                P['horn'] += [[t0, t0 + 12 * S, p('A4'), 116], [t0 + 12 * S, t0 + 14 * S, p('G4'), 108],
                              [t0 + 14 * S, t0 + 16 * S, p('E4'), 110]]
                P['tuba'] += [[t0, t0 + 16 * S - 8, p('A3'), 104]]
                P['timp'] += [[t0 + k * S, t0 + (k + 1) * S, p('A1') + 12, 60 + 4 * k] for k in range(16)]
                P['drums'] += [[t0 + k * S, t0 + (k + 1) * S, OSNARE, 60 + 4 * k] for k in range(16)]
                P['strings'] += [[t0 + k * S, t0 + k * S + S, p('A3'), 80] for k in range(16) if k % 4 != 3]
                P['bass'].append([t0, t0 + BAR - 8, p('A1') + 12, 104])
                P['wave'].append([t0, t0 + BAR - 8, p('A2'), 80])
                gust(P, CC, EX, 'rumble', t0 + 8 * S, 8 * S, 40, 100, wobble=2)
            continue
        if sec == 'A':
            P['horn'] += mel('A', i, t0, 112 if var == 'a1' else 116, shift=-12)
            if var == 'a2' and i >= 4:
                P['tpt'] += mel('A', i, t0, 104)
        elif sec == 'B':
            P['horn'] += mel('B', i, t0, 114, shift=-12)
        elif sec == 'C':
            P['tpt'] += mel('C', i, t0, 118)
            P['horn'] += mel('C', i, t0, 108, shift=-12)
        for st, en, ch in sg:
            r = CH[ch][0]
            # bas: zwaar, gestippeld
            P['bass'] += [[t0 + (st + k) * S, t0 + (st + k + ln) * S - 8, near(r, 38), v]
                          for k, ln, v in ((0, 6, 112), (6, 2, 100), (8, 8, 108)) if st + k < en]
            P['wave'].append([t0 + st * S, t0 + en * S - 8, near(r, 38), 80])
            # tuba: lage koperharmonie (niet onder C3)
            if sec != 'C':
                P['tuba'] += [[t0 + h * S, t0 + min(en, h + 8) * S - 8, near(r, 48), 96] for h in range(st, en, 8)]
            # pauken: grondtoon en kwint
            P['timp'] += [[t0 + st * S, t0 + st * S + 2 * S, near(r, 38), 116]]
            if en - st > 8 and sec != 'C':
                P['timp'].append([t0 + (st + 8) * S, t0 + (st + 10) * S, near((r + 7) % 12, 38), 104])
            # galopperend strijkersostinato (da-da-DUM)
            if sec != 'B' or i >= 4:
                for k in range(st, en):
                    if k % 4 != 3:
                        P['strings'].append([t0 + k * S, t0 + k * S + (2 * S if k % 4 == 2 else S), near(r, 50),
                                             84 if k % 4 == 0 else 66])
            # koor
            if sec in ('C', 'B') or var == 'a2':
                for n in tones(ch, 57, 70)[-2:] if sec == 'C' else tones(ch, 57, 67)[:1]:
                    for h in range(st, en, 8):
                        P['choir'].append([t0 + h * S, t0 + min(en, h + 8) * S - 8, n, 84 if sec == 'C' else 70])
            # strijkerspad in de brug (eerste helft, legato)
            if sec == 'B' and i < 4:
                for n in tones(ch, 55, 67)[:2]:
                    P['pad'] += [[t0 + h * S, t0 + min(en, h + 8) * S - 8, n, 76] for h in range(st, en, 8)]
            # buisklokken: de oogst
            if sec == 'C' and st == 0:
                P['bell'].append([t0, t0 + 6 * S, near(r, 74), 92])
        # taiko + kick
        tk = {'A': (0, 6, 8) if var == 'a1' else (0, 6, 8, 12), 'B': (0, 8), 'C': (0, 3, 6, 8, 12)}[sec]
        if sec == 'B' and i >= 4:
            tk = tuple(range(0, 16, 2)) if i >= 6 else (0, 4, 8, 12)
        P['taiko'] += [[t0 + k * S, t0 + k * S + TPB, TAIKO_KEY, 116 if k in (0, 8) else 96] for k in tk]
        if i % 4 == 0 or (sec == 'C' and i % 2 == 0):
            P['drums'].append([t0, t0 + 2 * TPB, CRASH, 112 if sec == 'C' else 100])
        if (sec == 'A' and i == 7) or (sec == 'B' and i == 7) or (sec == 'C' and i == 7):
            P['drums'] += [[t0 + k * S, t0 + (k + 1) * S, OSNARE, 60 + 5 * (k - 8)] for k in range(8, 16)]
        if sec == 'B' and i == 7:
            gust(P, CC, EX, 'rumble', t0, BAR - S, 38, 110, wobble=2)
    sec_of = lambda t: next(((sec, i, b * BAR) for b, sec, i, var in tl if b * BAR <= t < (b + 1) * BAR))
    P['harm'] = [x for x in harmony_below([[s, e, n + 12, int(v * 0.8)] for s, e, n, v in P['horn']
                                           if 12 * BAR <= s < 20 * BAR or s >= 28 * BAR], sec_of)]
    return dict(parts=P, cc=CC, ex=EX, end=len(tl) * BAR, loop=4, bpm=112, shift=0,
                order=['horn', 'tpt', 'drums', 'bass', 'timp', 'taiko', 'choir', 'bell', 'tuba', 'strings', 'pad'],
                detach=('horn', 'tpt', 'tuba', 'choir', 'pad'),
                layout=[('horn', HORN, 112, 0, 64), ('tpt', TPT, 96, 1, 70), ('tuba', TUBA, 88, 2, 56),
                        ('bass', FBASS, 108, 3, 64), ('timp', TIMP, 104, 4, 64), ('taiko', TAIKO, 104, 5, 64),
                        ('strings', SPICC, 80, 6, 44), ('choir', CHOIR, 74, 7, 84), ('pad', STR, 70, 8, 64),
                        ('bell', BELL, 66, 10, 80), ('harm', SQ_LEAD, 26, 11, 64), ('wave', WAVE, 56, 12, 64),
                        ('rumble', GUST, 60, 13, 64)],
                drums=('drums',))


THEMES = {'tornadus': tornadus, 'thundurus': thundurus, 'landorus': landorus}
NOSHIFT = {'drums', 'hats', 'gust', 'crack', 'cracks', 'rumble', 'taiko'}


def voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm + overrides voor Battle! Tornadus/Thundurus/Landorus (Forces of Nature).'
    lines[1] = '@ Gegenereerd door tools/grounded/forces_theme.py. Alleen Emerald-samples.'
    lines[2] = 'voice_group %s' % VG
    over = {
        14: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_tubular_bell, 255, 165, 51, 200',
        29: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_distortion_guitar_low, 255, 0, 255, 120',
        30: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_distortion_guitar_high, 255, 0, 255, 165',
        47: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 200',
        49: 'voice_keysplit voicegroup_forces_spicc_keysplit, keysplit_strings',
        80: 'voice_square_1 60, 0, 0, 1, 0, 2, 6, 1',
        81: 'voice_square_2 60, 0, 1, 0, 0, 15, 1',
        82: 'voice_square_2 60, 0, 0, 0, 2, 8, 1',
        84: 'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_1, 0, 7, 15, 0',
        121: 'voice_noise_alt 60, 0, 0, 0, 0, 15, 2',
        122: 'voice_noise_alt 60, 0, 0, 0, 1, 0, 0',
    }
    out = []
    for l in lines:
        for k, v in over.items():
            if l.rstrip().endswith('@ %d' % k):
                l = '\t%s  @ %d' % (v, k)
        out.append(l)
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    open('sound/voicegroups/keysplits/forces_spicc.inc', 'w').write(
        '@ Project Grounded: spiccato-strijkers (harde aanzet, kort) voor Battle! Forces of Nature (forces_theme.py).\n'
        'voice_group forces_spicc_keysplit\n' +
        ''.join('\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_string_ensemble_%d, 255, 210, 0, 130\n' % k
                for k in (60, 72, 84)))


def build(name, refdir=None):
    th = THEMES[name]()
    P, bpm = th['parts'], th['bpm']
    for k in list(P):
        if k not in NOSHIFT:
            P[k] = [[s, e, n + th['shift'], v] for s, e, n, v in P[k]]
        P[k] = dedupe(P[k])
    progs = {k: pr for k, pr, *_ in th['layout']}
    rel = releases(VG)
    tail = {k: release_ticks(rel.get(pr, 200), TPB, bpm) + 2 for k, pr in progs.items()}
    for k, pr in progs.items():           # elke DS-partij: noot + uitklinktijd eindigt vóór de volgende aanslag
        if rel.get(pr) is not None:
            P[k] = detach(P[k], tail[k])
    for k, pr in progs.items():            # octaafcorrectie voor samples die lager klinken dan geschreven
        if pr in OCT_DOWN:
            P[k] = [[s, e, n + OCT_DOWN[pr], v] for s, e, n, v in P[k]]
    for k, pr in progs.items():
        if rel.get(pr) is not None:
            low = [n for _, _, n, _ in P[k] if n < 28]
            assert not low, '%s %s: noten onder E1' % (name, k)
            if pr in (TPT, HORN, TUBA):
                assert all(n >= 48 for _, _, n, _ in P[k]), '%s %s: koper onder C3' % (name, k)
    order = th['order']
    ds = {k: P[k] for k in order}
    kept = allocate(ds, order, tail)
    for k in order:
        n = len(ds[k])
        if n and len(kept[k]) < n:
            print('  %s %s: %d van %d noten vallen weg (%.1f%%)' % (name, k, n - len(kept[k]), n, 100 * (n - len(kept[k])) / n))
        P[k] = kept[k]
    lp = th['loop'] * BAR
    for ref in (False, True):
        if ref and not refdir:
            continue
        song = Song(TPB, 500000)
        song.tempo(0, bpm / 120)
        song.loop = (lp, th['end'])
        for k, pr, vol, ch, pan in th['layout']:
            notes = P[k]
            if ref and pr in OCT_DOWN:
                notes = [[s, e, n - OCT_DOWN[pr], v] for s, e, n, v in notes]
            ccs = list(th['cc'].get(k, []))
            ex = list(th['ex'].get(k, []))
            if ex:
                ccs = [(0, 20, 12)] + ccs
            song.add(notes, pr if not ref else min(pr, 126), vol, ch, pan, extra=ex, ccs=ccs)
        song.add(sorted(sum((P[k] for k in th['drums']), [])), KIT, 108, 9)
        written = {k for k, *_ in th['layout']} | set(th['drums'])
        assert not [k for k in P if P[k] and k not in written], '%s: partij niet weggeschreven %s' % (
            name, [k for k in P if P[k] and k not in written])
        out = os.path.join(refdir, 'forces_%s_ref.mid' % name) if ref else \
            'sound/songs/midi/mus_grounded_vs_%s.mid' % name
        song.save(out, th['end'])
        print(out, '| loop %.1f s' % ((th['end'] - lp) / TPB * 60 / bpm), '| totaal %.1f s' % (th['end'] / TPB * 60 / bpm))


if __name__ == '__main__':
    ref = sys.argv[sys.argv.index('--ref') + 1] if '--ref' in sys.argv else None
    voicegroup()
    for n in THEMES:
        build(n, ref)
