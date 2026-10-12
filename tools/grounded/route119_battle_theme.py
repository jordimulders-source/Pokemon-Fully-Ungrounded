#!/usr/bin/env python3
"""Project Grounded: Battle! Wild Pokémon (Route 119+), het wildthema op de landroutes vanaf Route 119.

Jordi (11 okt): "een nieuw gevechtsthema op alle land routes vanaf route 119. Deze moet grande klinken,
avontuurlijk. Gebruik de route 119 theme als inspiratie."
Jordi over v1 (11 okt): "klinkt een beetje gek, alsof het originele nummer slecht geremixed is, vallen allerlei klanken
weg lijkt wel, plus het is iets teveel een snellere versie van het origineel en net niet genoeg een battle theme."

MUS_GROUNDED_VS_WILD_ROUTE119 = 711. **v2: een eigen Hoenn-gevechtsthema**, geen remix meer. Route 119 levert alleen
het motief (C#5 . E4-E4-E4 C#5, de tonica die naar G6 en D/F# zakt, F-G-A) en de harmoniekleur (bVI-bVII-I); de vorm
komt van mus_vs_wild/mus_vs_trainer:
  - intro (4 maten): strijkers in een chromatische 16e-val vanaf E6 boven een paukenroffel, dan koperstoten in
    3+3+2: E-Eb-D omlaag, C-D-E omhoog, E7-klap + loopje E-F#-G#-A-A#-B naar het motief;
  - rechte, drijvende 8en in 180 bpm (geen triolengalop meer), Hoenn-gevechtsbas (8en met octaven en een
    chromatische opmaat naar het volgende akkoord), kick op 1/3 + de 'en' van 2, snare op 2/4, PSG-hihat in 8en;
  - A (8) motief op trompet, hoorns in tertsen/sexten alleen op lange noten, strijkers liggend eronder;
  - A' (8) zelfde begin, nieuw slot dat naar C stijgt;
  - B (8) heroïsche wending: F-G-C-Am-F-G-F/G-A, brede hoornmelodie met strijkers een octaaf hoger, pauken op de tel,
    trompetten pas in de laatste twee maten (bVI-bVII-I);
  - C (8) climax: het motief tutti (trompet + hoorns + strijkers een octaaf hoger), spiccato-8en, klokken;
  - D (4) opbouw: F-G-Bb (Napolitaans) -E7, koperstoten, paukenroffel, hetzelfde loopje terug naar het loopbegin.
Kanaalbudget (v1 liet noten wegvallen): de stemverdeler rekent nu met de ECHTE bezetting per noot (envelope van
de m4a-engine frame voor frame: aanslag/decay/sustain tot de note-off, dan release tot 0, of het einde van een
niet-lussende sample), niet met de 1/16-schatting van release_ticks(). In v1 hield een crash (decay 235) een kanaal
±1,1 s bezet terwijl de verdeler 0,5 s rekende, waardoor de engine echte noten afkapte. Doel: 0 weggevallen noten in
de hoofdpartijen; minder lagen (geen tegenstem, geen arpeggio's, geen dubbele strijkers terwijl de melodie loopt).
Alleen stock-Emerald-samples (trompet/hoorn/strijkers-keysplits, fingered bass, pauken, buisklok, kit).
  python3 tools/grounded/route119_battle_theme.py
Zie tools/grounded/MUZIEK.md ("Route 119+")."""
import math, os, sys, wave
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, Song

VG = 'grounded_route119_battle'
OUT = 'sound/songs/midi/mus_grounded_vs_wild_route119.mid'
MAXV = 10
BPM = 180
TPB = 96
E8 = TPB // 2          # 8e
S = TPB // 4           # 16e
BAR = TPB * 4
FPS = 59.7275
QUIET = 16             # envelope onder 1/16 = onhoorbaar in de mix
TICKS_PER_FRAME = TPB * BPM / 60 / FPS

CH = {'A': (9, (9, 1, 4)), 'G': (7, (7, 11, 2)), 'D/F#': (6, (2, 6, 9)), 'F': (5, (5, 9, 0)), 'E': (4, (4, 8, 11)),
      'E7': (4, (4, 8, 11, 2)), 'C': (0, (0, 4, 7)), 'Am': (9, (9, 0, 4)), 'Bb': (10, (10, 2, 5)),
      'Eb': (3, (3, 7, 10)), 'D': (2, (2, 6, 9))}

# programma's in voicegroup_grounded_route119_battle
BELL, FBASS, TROLL, TIMP, STR, SPICC, TPT, HORN, KIT = 14, 33, 45, 47, 48, 49, 56, 60, 127
SQ2, WAVE, NOISE = 81, 84, 121
# drumkit drumsets/route119_battle.inc (vanaf 36)
KICK, SNARE, CRASH, TOM_L, TOM_M, TOM_H, OCYM, TAIKO = range(36, 44)

# envelopes (a, d, s, r) + sample (naam, lus?) per programma/drumtoets: moet gelijk zijn aan voicegroup() hieronder
ENV = {
    TPT: (255, 0, 193, 127, None), HORN: (255, 0, 224, 165, None), STR: (255, 0, 255, 196, None),
    SPICC: (255, 0, 255, 100, None), FBASS: (255, 253, 0, 120, None), TIMP: (255, 0, 255, 192, None),
    TROLL: (255, 0, 255, 150, None), BELL: (255, 0, 255, 226, None),
}
KITDEF = [  # toets, (key, pan, sample, a, d, s, r)
    (KICK, (67, 64, 'drum_and_percussion_kick', 255, 0, 255, 180)),
    (SNARE, (60, 64, 'sc88pro_rnd_snare', 255, 0, 255, 180)),
    (CRASH, (60, 64, 'trinity_cymbal_crash', 255, 0, 255, 232)),
    (TOM_L, (45, 52, 'unused_sc55_tom', 255, 0, 255, 170)),
    (TOM_M, (51, 64, 'unused_sc55_tom', 255, 0, 255, 170)),
    (TOM_H, (57, 76, 'unused_sc55_tom', 255, 0, 255, 170)),
    (OCYM, (60, 64, 'sc88pro_orchestra_cymbal_crash', 255, 0, 255, 236)),
    (TAIKO, (57, 64, 'sc88pro_taiko', 255, 0, 255, 200)),
]


_SI = {}


def sample_info(name):
    if name in _SI:
        return _SI[name]
    """(duur in s op toets 60, lust?) uit de wav (smpl-chunk)."""
    import struct
    p = 'sound/direct_sound_samples/%s.wav' % name
    w = wave.open(p)
    dur = w.getnframes() / w.getframerate()
    d = open(p, 'rb').read()
    i, loop = 12, False
    while i < len(d) - 8:
        cid, sz = d[i:i + 4], struct.unpack('<I', d[i + 4:i + 8])[0]
        if cid == b'smpl' and struct.unpack('<I', d[i + 36:i + 40])[0]:
            loop = True
        i += 8 + sz + (sz & 1)
    _SI[name] = (dur, loop)
    return dur, loop


def channel_end(env, s, e, key=60, sample=None):
    """Tick waarop de m4a-engine het kanaal vrijgeeft: aanslag, decay tot sustain (sustain 0 = stop), note-off ->
    release per frame (env*r>>8) tot 0; een niet-lussende sample stopt aan zijn einde."""
    a, d, sus, r = env[:4]
    # een noot in de release-fase (SF_STOP) pakt de engine als eerste af als hij een kanaal nodig heeft
    # (ply_note in src/m4a_1.s); dat is onhoorbaar zodra de envelope onder 1/16 (-24 dB) is. Tot dan telt hij mee.
    off = (e - s) / TICKS_PER_FRAME
    lim = 1e9
    if sample:
        dur, loop = sample_info(sample)
        if not loop:
            lim = dur / (2 ** ((key - 60) / 12)) * FPS
    v, f, state = 0, 0, 'a'
    while f < lim and f < 2000:
        if state != 'r' and f >= off:
            state = 'r'
        if state == 'r':
            v = (v * r) >> 8
            if v < QUIET:
                break
        elif state == 'a':
            v = min(255, v + a)
            if v >= 255:
                state = 'd'
        elif state == 'd':
            v = (v * d) >> 8
            if v <= sus:
                v, state = sus, 's'
            if v < QUIET:
                break
        f += 1
    return s + int(math.ceil(min(f, lim) * TICKS_PER_FRAME))


def release_tail(r):
    """ticks van volle envelope tot onder QUIET na de note-off"""
    v, f = 255, 0
    while v >= QUIET:
        v = (v * r) >> 8
        f += 1
    return int(math.ceil(f * TICKS_PER_FRAME))


def timeline():
    tl = [('I', i, c) for i, c in enumerate(['E', 'E', 'E', 'E7'])]
    tl += [('A', i, c) for i, c in enumerate(['A', 'G', 'D/F#', ('F', 'G'), 'A', 'F', 'G', 'E'])]
    tl += [('A2', i, c) for i, c in enumerate(['A', 'G', 'D/F#', ('F', 'G'), 'A', 'F', 'G', 'C'])]
    tl += [('B', i, c) for i, c in enumerate(['F', 'G', 'C', 'Am', 'F', 'G', ('F', 'G'), 'A'])]
    tl += [('C', i, c) for i, c in enumerate(['A', 'G', 'D/F#', ('F', 'G'), 'A', 'F', 'G', 'E'])]
    tl += [('D', i, c) for i, c in enumerate(['F', 'G', 'Bb', 'E7'])]
    return tl


def halves(c):
    return c if isinstance(c, tuple) else (c, c)


def tones(ch, lo, hi):
    return [m for m in range(lo, hi + 1) if m % 12 in CH[ch][1]]


def near(pc, lo):
    return lo + ((pc - lo) % 12)


N = {n: i for i, n in enumerate('C C# D D# E F F# G G# A A# B'.split())}
N.update({'Db': 1, 'Eb': 3, 'Gb': 6, 'Ab': 8, 'Bb': 10})


def p(name):
    """'C#5' -> 73"""
    return N[name[:-1]] + 12 * (int(name[-1]) + 1)


# melodie per maat: (8e-plek, lengte in 8en, noot); '16' = 16en vanaf een 8e-plek
MOTIF = [(0, 3, 'C#5'), (3, 1, 'E4'), (4, 1, 'E4'), (5, 1, 'E4'), (6, 2, 'C#5')]
A_MEL = [MOTIF,
         [(0, 3, 'E5'), (3, 1, 'D5'), (4, 2, 'C#5'), (6, 2, 'B4')],
         [(0, 3, 'D5'), (3, 5, 'A4')],
         [(0, 1, 'F4'), (1, 1, 'G4'), (2, 2, 'A4'), (4, 1, 'G4'), (5, 1, 'A4'), (6, 2, 'B4')],
         MOTIF,
         [(0, 2, 'E5'), (2, 2, 'F5'), (4, 2, 'G5'), (6, 2, 'A5')],
         [(0, 3, 'B5'), (3, 1, 'A5'), (4, 2, 'G5'), (6, 2, 'D5')],
         [(0, 3, 'B4'), (3, 3, 'D5'), (6, 2, 'E5')]]
A2_MEL = A_MEL[:5] + [
         [(0, 2, 'F5'), (2, 2, 'E5'), (4, 2, 'F5'), (6, 2, 'A5')],
         [(0, 4, 'G5'), (4, 2, 'F5'), (6, 2, 'D5')],
         [(0, 6, 'E5'), (6, 1, 'F5'), (7, 1, 'G5')]]
B_MEL = [[(0, 3, 'C5'), (3, 1, 'A4'), (4, 4, 'F5')],
         [(0, 3, 'E5'), (3, 1, 'D5'), (4, 2, 'B4'), (6, 2, 'D5')],
         [(0, 6, 'E5'), (6, 1, 'D5'), (7, 1, 'E5')],
         [(0, 3, 'C5'), (3, 1, 'B4'), (4, 4, 'A4')],
         [(0, 3, 'C5'), (3, 1, 'A4'), (4, 4, 'F5')],
         [(0, 3, 'G5'), (3, 1, 'F5'), (4, 4, 'D5')],
         [(0, 3, 'F5'), (3, 1, 'E5'), (4, 3, 'G5'), (7, 1, 'G#5')],
         [(0, 8, 'A5')]]
C_MEL = A_MEL[:7] + [[(0, 8, 'E5')]]
D_MEL = [[(0, 2, 'A5'), (3, 2, 'A5'), (6, 2, 'C6')],
         [(0, 2, 'B5'), (3, 2, 'B5'), (6, 2, 'D6')],
         [(0, 8, 'D6')],
         [(0, 2, 'E5')]]
RUN = ['E4', 'F#4', 'G#4', 'A4', 'A#4', 'B4']            # 16en vanaf tel 3-en naar het motief


class Parts(dict):
    def __missing__(self, k):
        self[k] = []
        return self[k]


def mel_notes(bars, t0, vel):
    out = []
    for b, bar in enumerate(bars):
        for o, l, n in bar:
            s = t0 + b * BAR + o * E8
            out.append([s, s + l * E8, p(n), vel])
    return out


def run_notes(t0, vel):
    return [[t0 + 5 * E8 + k * S, t0 + 5 * E8 + (k + 1) * S, p(n), vel] for k, n in enumerate(RUN)]


def harmonize(notes, chord_at, lo, hi, gap=3, minlen=2 * E8, vel=100):
    """hoorns onder de melodie: hoogste akkoordtoon minstens `gap` halve tonen eronder, alleen op lange noten."""
    out = []
    for s, e, m, v in notes:
        if e - s < minlen:
            continue
        cand = [n for n in tones(chord_at(s), lo, hi) if n <= m - gap]
        if cand:
            out.append([s, e, cand[-1], vel])
    return out


def stab(P, part, t0, offs, ch, top, vel, length=E8, lo=55):
    """koperstoot: bovenstem `top` (trompet), hoorn een akkoordtoon eronder."""
    for o in offs:
        s = t0 + o * E8
        P['tpt'].append([s, s + length, top, vel])
        cand = [n for n in tones(ch, lo, top - 3)]
        if cand:
            P['horn'].append([s, s + length, cand[-1], vel - 6])


def drum(P, t0, offs, key, vel, length=S):
    for o in offs:
        P['drums'].append([t0 + o, t0 + o + length, key, vel])


def bass_bar(P, t0, chs, nxt, vel, mode='drive'):
    """Hoenn-gevechtsbas: rechte 8en, octaven, de laatste 8e chromatisch naar de volgende grondtoon."""
    split = chs[0] != chs[1]
    pat = {'drive': (0, 12, 0, 7, 0, 12, 10, 'a'), 'pump': (0, 0, 12, 0, 0, 0, 12, 'a'),
           'split': (0, 12, 0, 7, 0, 12, 7, 'a')}['split' if split and mode == 'drive' else mode]
    for k in range(8):
        r = near(CH[chs[k // 4]][0], 28)                   # E1..D#2
        iv = pat[k]
        if iv == 'a':
            nr = near(CH[nxt][0], 28) if nxt else r
            n = (nr - 1 if nr - 1 >= 28 else nr + 1) if nr != r else r + 12
        else:
            if mode == 'drive' and split and k == 3:
                iv = 7
            n = r + iv
        s = t0 + k * E8
        P['bass'].append([s, s + E8 - 6, n, vel + (8 if k in (0, 4) else 0)])


def timp_hits(P, t0, chs, offs, vel):
    for o in offs:
        ch = chs[0] if o < 4 else chs[1]
        hi = near(CH[ch][0], 41)                          # F2..E3
        n = hi if o % 4 == 0 else hi - 5 if hi - 5 >= 40 else hi + 7
        P['timp'].append([t0 + o * E8, t0 + o * E8 + S, n, vel + (8 if o % 4 == 0 else 0)])


def timp_roll(P, t0, ch, start, n, v0, dv, step=S):
    hi = near(CH[ch][0], 41)
    for k in range(n):
        P['troll'].append([t0 + start + k * step, t0 + start + k * step + 12, hi, min(127, v0 + dv * k)])


def pad(P, t0, chs, lo, hi, vel, part='pad', every=2):
    """liggende strijkers: één toon per halve maat (het sample is al een ensemble), dicht bij de vorige."""
    for h, ch in enumerate(chs):
        cand = tones(ch, lo, hi)
        prev = P[part][-1][2] if P[part] else cand[len(cand) // 2]
        n = min(cand, key=lambda m: (abs(m - prev), m))
        if P[part] and P[part][-1][2] == n and P[part][-1][1] == t0 + h * 2 * TPB:
            P[part][-1][1] += 2 * TPB                     # zelfde toon: doorhouden
        else:
            P[part].append([t0 + h * 2 * TPB, t0 + (h + 1) * 2 * TPB, n, vel])


def spicc_bar(P, t0, chs, vel):
    """spiccato-8en (climax): grondtoon-kwint-octaaf, korte release."""
    for k in range(8):
        ch = chs[k // 4]
        ts = tones(ch, 52, 64)
        n = ts[(0, 2, 1, 2)[k % 4] % len(ts)]
        P['spicc'].append([t0 + k * E8, t0 + k * E8 + E8 - 12, n, vel + (6 if k % 2 == 0 else 0)])


def compose():
    P = Parts()
    tl = timeline()
    halfs = []
    for _, _, c in tl:
        halfs += list(halves(c))

    def chord_at(t):
        return halfs[min(len(halfs) - 1, t // (2 * TPB))]

    start = {}
    for bi, (sec, i, c) in enumerate(tl):
        start.setdefault(sec, bi * BAR)
    tA, tA2, tB, tC, tD = start['A'], start['A2'], start['B'], start['C'], start['D']
    # ---------------- melodieën ----------------
    a = mel_notes(A_MEL, tA, 112)
    a2 = mel_notes(A2_MEL, tA2, 112)
    b = mel_notes(B_MEL, tB, 112)
    c = mel_notes(C_MEL, tC, 118)
    P['tpt'] += a + a2 + c
    P['horn'] += harmonize(a, chord_at, 55, 72) + harmonize(a2, chord_at, 55, 72)
    P['horn'] += harmonize(c, chord_at, 55, 74, vel=106)
    P['strings'] += [[s, e, n + 12, 100] for s, e, n, v in c if e - s >= E8 * 2]
    # B: hoornmelodie, strijkers een octaaf hoger; trompet pas op de laatste twee maten
    P['horn'] += [[s, e, n, 114] for s, e, n, v in b]
    P['strings'] += [[s, e, n + 12, 104] for s, e, n, v in b if e - s >= E8 * 2]
    P['tpt'] += [[s, e, n, 112] for s, e, n, v in b if s >= tB + 6 * BAR]
    P['_lead'] = a + a2 + c + [[s, e, n + 12, v] for s, e, n, v in b]
    # D: koperstoten
    for bi, ch in enumerate(('F', 'G', 'Bb')):
        for o, l, n in D_MEL[bi]:
            s = tD + bi * BAR + o * E8
            P['tpt'].append([s, s + l * E8 - (S if l < 8 else 0), p(n), 116])
            cand = tones(ch, 60, p(n) - 3)
            P['horn'].append([s, s + l * E8 - (S if l < 8 else 0), cand[-1], 108])
            P['strings'].append([s, s + l * E8, p(n) - 12, 104])
    P['_lead'] += [[e[0], e[1], e[2], e[3]] for e in P['tpt'] if e[0] >= tD]

    for bi, (sec, i, c) in enumerate(tl):
        t0 = bi * BAR
        chs = halves(c)
        nxt = halves(tl[bi + 1][2])[0] if bi + 1 < len(tl) else 'A'
        last = (bi + 1 == len(tl)) or tl[bi + 1][0] != sec
        # ================= intro =================
        if sec == 'I':
            if i in (0, 1):                     # chromatische 16e-val: x, x-2, x-1, x-3, elke groep 2 lager
                for g in range(4):
                    top = 88 - 2 * (g + 4 * i)
                    for k, dv in enumerate((0, -2, -1, -3)):
                        s = t0 + g * TPB + k * S
                        P['spicc'].append([s, s + S, top + dv, 104 + 2 * g])
            if i == 0:
                stab(P, 'tpt', t0, (0,), 'E', p('E5'), 118, length=TPB)
                drum(P, t0, (0,), CRASH, 116)
                drum(P, t0, (0,), TAIKO, 118)
                P['bass'].append([t0, t0 + TPB, 28, 116])
                timp_roll(P, t0, 'E', 2 * TPB, 8, 84, 4)
            if i == 1:                          # E - Eb - D omlaag
                for o, ch, top, br in ((0, 'E', 'E5', 40), (3, 'Eb', 'Eb5', 39), (6, 'D', 'D5', 38)):
                    stab(P, 'tpt', t0, (o,), ch, p(top), 114, length=E8 + S if o < 6 else 2 * E8)
                    P['bass'].append([t0 + o * E8, t0 + o * E8 + E8 + S, br, 112])
                    drum(P, t0, (o * E8,), KICK if o else TAIKO, 112)
                drum(P, t0, (0,), CRASH, 104)
            if i == 2:                          # C - D - E omhoog
                for o, ch, top, br in ((0, 'C', 'E5', 36), (3, 'D', 'F#5', 38), (6, 'E', 'G#5', 40)):
                    stab(P, 'tpt', t0, (o,), ch, p(top), 116, length=E8 + S if o < 6 else 2 * E8)
                    P['bass'].append([t0 + o * E8, t0 + o * E8 + E8 + S, br, 114])
                    drum(P, t0, (o * E8,), TAIKO, 114)
                    hi = near(CH[ch][0], 41)
                    P['timp'].append([t0 + o * E8, t0 + o * E8 + S, hi, 108])
                drum(P, t0, (0,), CRASH, 110)
                for k in range(4):              # snareroffel op tel 4 (16en, crescendo)
                    drum(P, t0, (3 * TPB + k * S,), SNARE, 92 + 6 * k)
            if i == 3:                          # E7-klap + loopje naar het motief
                stab(P, 'tpt', t0, (0,), 'E7', p('D5'), 120, length=TPB)
                P['tpt'] += run_notes(t0, 112)
                P['sqrun'] += run_notes(t0, 100)
                bass_bar(P, t0, chs, 'A', 108)
                drum(P, t0, (0,), CRASH, 112)
                drum(P, t0, (0, 4 * E8), KICK, 114)
                drum(P, t0, (2 * E8,), SNARE, 106)
                for k in range(4):
                    drum(P, t0, (6 * E8 + k * S,), SNARE, 96 + 6 * k)
                timp_roll(P, t0, 'E', TPB, 4, 92, 6, step=E8)
            if i >= 1:
                for k in range(8):
                    P['hat'].append([t0 + k * E8, t0 + k * E8 + 6, 84, 60 if k % 2 == 0 else 42])
            continue
        # ================= loop =================
        # strijkers liggend (A/A2), pad in B onder de hoorn, spiccato in C
        if sec in ('A', 'A2'):
            pad(P, t0, chs, 52, 64, 92)
        elif sec == 'B':
            pad(P, t0, chs, 50, 62, 92)
        # bas + golf-sub
        if sec == 'D' and i == 3:
            stab(P, 'tpt', t0, (0,), 'E7', p('D5'), 120, length=TPB)
            P['tpt'] += run_notes(t0, 112)
            P['sqrun'] += run_notes(t0, 100)
        if sec == 'D' and i < 3:
            for o in (0, 3, 6):
                ch = chs[0]
                P['bass'].append([t0 + o * E8, t0 + o * E8 + E8 + S, near(CH[ch][0], 28), 116])
                P['bass'].append([t0 + o * E8 + 2 * E8, t0 + o * E8 + 3 * E8 - 6, near(CH[ch][0], 28) + 12, 104]) \
                    if o < 6 else None
        else:
            bass_bar(P, t0, chs, nxt, 106, 'pump' if sec == 'B' else 'drive')
        for h, ch in enumerate(chs):
            P['wave'].append([t0 + h * 2 * TPB, t0 + (h + 1) * 2 * TPB - S, near(CH[ch][0], 36), 100])
        # pauken
        if sec == 'D' and i < 2:
            timp_hits(P, t0, chs, (0, 3, 6), 104)
        elif sec == 'D' and i == 2:
            timp_roll(P, t0, 'Bb', 0, 16, 84, 2, step=S)
        elif sec == 'D':
            timp_hits(P, t0, chs, (0,), 108)
            timp_roll(P, t0, 'E', TPB, 4, 92, 6, step=E8)
        elif sec == 'B':
            timp_hits(P, t0, chs, (0, 4), 100)
            if i == 7:
                timp_roll(P, t0, 'A', 2 * TPB, 8, 88, 4)
        elif sec == 'C':
            timp_hits(P, t0, chs, (0, 3, 4, 7), 104)
        elif last:
            timp_hits(P, t0, chs, (0, 3, 6), 104)
        else:
            timp_hits(P, t0, chs, (0, 3, 4), 98)
        # klokken
        if (sec == 'C' and i in (0, 4)) or (sec == 'B' and i == 7):
            P['bell'].append([t0, t0 + E8, near(CH[chs[0]][0], 64), 104])
        # drums
        first = i == 0
        if first or (sec in ('A', 'A2', 'C') and i == 4) or (sec == 'B' and i in (4, 7)) or sec == 'D':
            drum(P, t0, (0,), CRASH, 114)
        hat = range(8)
        if sec == 'D' and i < 3:
            for o in (0, 3, 6):
                drum(P, t0, (o * E8,), TAIKO if o == 0 else KICK, 116)
            if i == 2:
                for k in range(8):
                    drum(P, t0, (2 * TPB + k * S,), SNARE, 84 + 4 * k)
            hat = ()
        elif sec == 'D':
            drum(P, t0, (0, 4 * E8), KICK, 114)
            drum(P, t0, (2 * E8,), SNARE, 106)
            for k in range(4):
                drum(P, t0, (6 * E8 + k * S,), SNARE, 96 + 6 * k)
            hat = range(5)
        else:
            drum(P, t0, (0, 4 * E8), KICK, 114)
            drum(P, t0, (3 * E8,), KICK, 100)
            if last:                            # fill: snare op 2, tomroffel op 4
                drum(P, t0, (2 * E8, 4 * E8 + S * 2), SNARE, 104)
                if sec != 'B':                  # B eindigt op een paukenroffel
                    for k, key in enumerate((TOM_H, TOM_H, TOM_M, TOM_L)):
                        drum(P, t0, (6 * E8 + k * S,), key, 104 + 3 * k)
                hat = range(6)
            else:
                drum(P, t0, (2 * E8, 6 * E8), SNARE, 108)
                if i % 4 == 3:
                    drum(P, t0, (7 * E8 + S,), SNARE, 90)
        for k in hat:
            P['hat'].append([t0 + k * E8, t0 + k * E8 + 6, 84, 60 if k % 2 == 0 else 42])
    end = len(tl) * BAR
    return P, end, start


LAYOUT = [  # (partij, programma, volume, kanaal, pan)
    ('tpt', TPT, 108, 0, 64), ('horn', HORN, 98, 1, 52), ('strings', STR, 84, 2, 78), ('pad', STR, 72, 3, 44),
    ('spicc', SPICC, 80, 4, 84), ('bass', FBASS, 84, 5, 64), ('timp', TIMP, 100, 6, 64), ('troll', TROLL, 92, 12, 64),
    ('bell', BELL, 72, 7, 72),
    ('sqrun', SQ2, 40, 8, 88), ('wave', WAVE, 34, 10, 64), ('hat', NOISE, 56, 11, 64),
]
ORDER = ['tpt', 'horn', 'drums', 'bass', 'timp', 'strings', 'troll', 'bell', 'spicc', 'pad']
DRUMVOL = 96
PSG = {'sqrun', 'wave', 'hat'}


def voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm + overrides voor het Route 119+-wildthema (MUS_GROUNDED_VS_WILD_ROUTE119).'
    lines[1] = '@ Gegenereerd door tools/grounded/route119_battle_theme.py. Alleen Emerald-samples (Hoenn-koper/-strijkers/-pauken).'
    lines[2] = 'voice_group %s' % VG
    ds = lambda smp, e: 'voice_directsound 60, 0, DirectSoundWaveData_%s, %d, %d, %d, %d' % ((smp,) + e[:4])
    over = {
        BELL: ds('sc88pro_tubular_bell', ENV[BELL]),
        FBASS: ds('sc88pro_fingered_bass', ENV[FBASS]),
        TIMP: ds('sc88pro_timpani', ENV[TIMP]),
        TROLL: ds('sc88pro_timpani', ENV[TROLL]),
        STR: 'voice_keysplit voicegroup_strings_keysplit, keysplit_strings',
        SPICC: 'voice_keysplit voicegroup_route119_spicc_keysplit, keysplit_strings',
        TPT: 'voice_keysplit voicegroup_trumpet_keysplit, keysplit_trumpet',
        HORN: 'voice_keysplit voicegroup_french_horn_keysplit, keysplit_french_horn',
        SQ2: 'voice_square_2 60, 0, 2, 0, 1, 7, 1',
        WAVE: 'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_1, 0, 7, 15, 0',
        NOISE: 'voice_noise_alt 60, 0, 0, 0, 1, 0, 0',
        KIT: 'voice_keysplit_all voicegroup_route119_battle_drumset',
    }
    out = []
    for l in lines:
        for k, v in over.items():
            if l.rstrip().endswith('@ %d' % k):
                l = '\t%s  @ %d' % (v, k)
        out.append(l)
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    names = {KICK: 'kick', SNARE: 'snare', CRASH: 'crash', TOM_L: 'tom laag', TOM_M: 'tom midden', TOM_H: 'tom hoog',
             OCYM: 'orkestbekken', TAIKO: 'taiko'}
    open('sound/voicegroups/drumsets/route119_battle.inc', 'w').write(
        '@ Project Grounded: drumkit voor route119_battle_theme.py (Route 119+-wildthema). Alleen stock-samples, geen PSG.\n'
        '@ ' + ', '.join('%d %s' % (k, names[k]) for k, _ in KITDEF) + '.\n'
        '@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.\n'
        'voice_group route119_battle_drumset, 36\n' + ''.join(
            '\tvoice_directsound %d, %d, DirectSoundWaveData_%s, %d, %d, %d, %d\n' % v for _, v in KITDEF))
    open('sound/voicegroups/keysplits/route119_spicc.inc', 'w').write(
        '@ Project Grounded: spiccato-strijkers (korte release) voor route119_battle_theme.py.\n'
        'voice_group route119_spicc_keysplit\n' + ''.join(
            '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_string_ensemble_%d, 255, 0, 255, %d\n'
            % (k, ENV[SPICC][3]) for k in (60, 72, 84)))
    inc = 'sound/voice_groups.inc'
    txt = open(inc).read()
    line = '.include "sound/voicegroups/keysplits/route119_spicc.inc"\n'
    anchor = '.include "sound/voicegroups/drumsets/route119_battle.inc"\n'
    if line not in txt:
        txt = txt.replace(anchor, line + anchor)
        open(inc, 'w').write(txt)


def anti_kermis(P):
    """geen begeleiding (pad, spiccato, bas, PSG) boven de klinkende melodienoot."""
    lead = sorted(P.pop('_lead'))
    bad = 0
    for part in ('pad', 'spicc', 'bass', 'wave'):
        for s, e, n, v in P[part]:
            mel = [m for m in lead if m[0] <= s < m[1]]
            if mel and n > max(m[2] for m in mel):
                bad += 1
                print('  anti-kermis: %s noot %d op maat %.2f boven de melodie %d' % (part, n, s / BAR, max(m[2] for m in mel)))
    assert bad == 0, 'anti-kermis: %d begeleidingsnoten boven de melodie' % bad


def occupancy(part, prog, ev):
    """[start, kanaal-vrij] per noot volgens de echte m4a-envelope."""
    if part == 'drums':
        kit = dict(KITDEF)
        return [channel_end(kit[n][3:], s, e, kit[n][0], kit[n][2]) for s, e, n, v in ev]
    return [channel_end(ENV[prog], s, e) for s, e, n, v in ev]


def build():
    P, end, start = compose()
    for k in list(P):
        if k.startswith('_'):
            continue
        P[k] = sorted(dedupe([e for e in P[k] if e[0] < end]))
        for e in P[k]:
            e[1] = min(e[1], end)
    anti_kermis(P)
    progs = {k: pr for k, pr, *_ in LAYOUT}
    progs['drums'] = KIT
    # zelfde toonhoogte in één partij mag niet overlappen; een noot in dezelfde partij die nog uitklinkt kost een
    # extra kanaal: dat rekent de verdeler mee (geen detach nodig)
    for k in progs:
        if k in PSG or k == 'drums':
            continue
        low = [n for _, _, n, _ in P[k] if n < 28]
        assert not low, '%s: DirectSound-noten onder E1: %s' % (k, low[:5])
        if progs[k] in (TPT, HORN):
            bad = [n for _, _, n, _ in P[k] if n < 48]
            assert not bad, '%s: koper onder C3 %s' % (k, bad[:5])
        soft = [v for _, _, _, v in P[k] if v < 76]
        assert not soft, '%s: zachte DS-noten (8-bit-fuzz) %s' % (k, soft[:5])
    # legato: elke noot laat los zodra zijn release (tot -24 dB) precies op de volgende aanslag in dezelfde partij
    # eindigt, zodat een partij nooit twee kanalen bezet (v1: koper/strijkers dubbel op elke maatstreep)
    for k in ('tpt', 'horn', 'strings', 'pad', 'bass'):
        tail = release_tail(ENV[progs[k]][3])
        P[k] = detach(P[k], tail)
    # stemverdeler met echte bezetting: allocate() krijgt per noot een eigen staart (eind = kanaal vrij)
    busy, kept = [], {}
    for k in ORDER:
        occ = occupancy(k, progs[k], P[k])
        kk = []
        for e, fr in zip(P[k], occ):
            r = allocate({'p': [[e[0], fr, e[2], e[3]]]}, ['p'], 0, max_voices=MAXV, preset=[x[:2] for x in busy])['p']
            if r:
                kk.append(e)
                busy.append((e[0], fr, k))
            elif os.environ.get('R119_DEBUG'):
                from collections import Counter
                pts = [e[0]] + [x[0] for x in busy if e[0] < x[0] < fr]
                worst = max(pts, key=lambda t: sum(1 for x in busy if x[0] <= t < x[1]))
                print('    %s %d maat %.2f bezet op %.2f:' % (k, e[2], e[0] / BAR - 4, worst / BAR - 4),
                      dict(Counter(x[2] for x in busy if x[0] <= worst < x[1])))
        kept[k] = kk
        n = len(P[k])
        if n and len(kk) < n:
            kset = {tuple(x) for x in kk}
            print('  %s: %d van %d noten vallen weg (%.1f%%) op maat %s' % (
                k, n - len(kk), n, 100 * (n - len(kk)) / n,
                [round(x[0] / BAR - 4, 2) for x in P[k] if tuple(x) not in kset][:12]))
        P[k] = kk
    # piekbezetting
    pts = sorted({b[0] for b in busy})
    mx = max(sum(1 for b in busy if b[0] <= t < b[1]) for t in pts)
    print('  max. gelijktijdige DirectSound-kanalen (echte envelope): %d' % mx)
    lp = start['A']
    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.loop = (lp, end)
    for k, pr, vol, ch, pan in LAYOUT:
        song.add(P[k], pr, vol, ch, pan)
    song.add(sorted(P['drums']), KIT, DRUMVOL, 9)
    written = {k for k, *_ in LAYOUT} | {'drums'}
    assert not [k for k in P if P[k] and k not in written and not k.startswith('_')]
    song.save(OUT, end)
    print(OUT, '| intro %.1f s | loop %.1f s | totaal %.1f s' % (
        lp / TPB * 60 / BPM, (end - lp) / TPB * 60 / BPM, end / TPB * 60 / BPM))


if __name__ == '__main__':
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
    voicegroup()
    build()
