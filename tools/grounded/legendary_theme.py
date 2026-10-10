#!/usr/bin/env python3
"""Project Grounded: Battle! Legendary Pokémon, het generieke legendary-thema voor alle legendaries zonder eigen thema.

Jordi: "Een generic legendary battle theme voor alle overige legendaries. Episch, maar perfect in theme met Hoenn
muziek, de beste instrumenten uit die soundfont moeten erin voor komen. De percussie zoals bij Weather Trio, de
trompetten uit de Elite Four theme, zulk soort dingen."

MUS_GROUNDED_VS_LEGENDARY = 670. Eigen compositie, E-klein, 176 bpm, alleen stock-Emerald-samples (0 KB samples).
Schrijfstijl naar mus_vs_kyogre_groudon / mus_vs_rayquaza / mus_vs_elite_four:
  - pauken-ostinato in achtsten (laag-hoog-laag-laag-hoog-laag-laag-hoog, grondtoon + kwint eronder), het hele
    nummer door, met roffels naar elke sectie: de Weather Trio-percussie; orkestbekken op de frasebegins;
  - koper zoals de Elite Four: trompetten (stock trumpet-keysplit) met de hoorns in tertsen/sexten eronder, in
    D5-C6; strijkers (stock string ensemble) liggend of in octaven met de melodie;
  - fingered bass in achtsten op de grondtoon met chromatische opmaat naar het volgende akkoord (Kyogre/Groudon);
  - PSG: blokgolf-arpeggio's in 16en en een zachte blokgolf-dubbeling van de melodie (de GBA-glans), golf-sub;
  - buisklokken op de climax, Hoenn-chromatiek: bII (F in E-klein), een fanfare die per twee maten een halve toon
    stijgt (E-F-F#), climax een hele toon hoger (F#-klein), terugweg C-D-B.
Vorm: intro 8 (pauken + klok, dan de koperroep) | A thema (trompet + hoorns) | A2 thema + strijkers + hoorn-
      tegenstem + arpeggio's | B strijkers zingen (C-D-Bm-Em-Am-D-G-B), half-time | C fanfare chromatisch omhoog |
      D climax: thema in F#-klein met klokken | T terugweg C-D-B-B -> loop naar A.
Eén voicegroup voicegroup_grounded_legendary (grounded_gm + overrides) en drumsets/legendary.inc.
Stemverdeler max. 11 DirectSound-noten (legendary).
  python3 tools/grounded/legendary_theme.py [--ref <map>]
Zie tools/grounded/MUZIEK.md."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

VG = 'grounded_legendary'
OUT = 'sound/songs/midi/mus_grounded_vs_legendary.mid'
MAXV = 11
BPM = 176
TPB = 96
S = TPB // 4
BAR = TPB * 4

N = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'Ab': 8,
     'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def p(name):
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


CH = {'Em': (4, (4, 7, 11)), 'C': (0, (0, 4, 7)), 'D': (2, (2, 6, 9)), 'F': (5, (5, 9, 0)), 'B': (11, (11, 3, 6)),
      'Bm': (11, (11, 2, 6)), 'Am': (9, (9, 0, 4)), 'G': (7, (7, 11, 2)), 'Fm': (5, (5, 8, 0)),
      'F#m': (6, (6, 9, 1)), 'E': (4, (4, 8, 11)), 'C#': (1, (1, 5, 8))}

# programma's in voicegroup_grounded_legendary
BELL, FBASS, TROLL, TIMP, STR, TPT, HORN, KIT = 14, 33, 45, 47, 48, 56, 60, 127
SQ1, SQ2, WAVE = 80, 81, 84
# drumkit drumsets/legendary.inc (vanaf 36)
TAIKO, OSN, TOM_L, TOM_M, TOM_H, CRASH, CRASH2 = range(36, 43)
DLEN = {TAIKO: TPB, OSN: 3 * S, TOM_L: 2 * S, TOM_M: 2 * S, TOM_H: 2 * S, CRASH: TPB, CRASH2: TPB}


def tones(ch, lo, hi):
    return [m for m in range(lo, hi + 1) if m % 12 in CH[ch][1]]


def near(pc, lo):
    return lo + ((pc - lo) % 12)


class Parts(dict):
    def __missing__(self, k):
        self[k] = []
        return self[k]


def mel(pat, t0, vel, tr=0):
    return [[t0 + st * S, t0 + (st + ln) * S, p(n) + tr, vel] for st, ln, n in pat]


def drum(P, t0, steps, key, vel):
    for k in steps:
        P['drums'].append([t0 + k * S, t0 + k * S + DLEN[key], key, vel])


def roll(P, t0, st, n, key, v0, dv):
    for k in range(n):
        P['drums'].append([t0 + (st + k) * S, t0 + (st + k + 1) * S, key, min(127, v0 + dv * k)])


# ---------------------------------------------------------------------------------------------------------------------
# materiaal
# ---------------------------------------------------------------------------------------------------------------------
INTRO = ['Em', 'Em', 'Em', 'Em', 'Em', 'C', 'D', 'B']
CALL = {4: [(0, 4, 'E5'), (4, 2, 'B4'), (6, 2, 'E5'), (8, 8, 'G5')],
        5: [(0, 3, 'G5'), (3, 3, 'A5'), (6, 2, 'G5'), (8, 8, 'E5')],
        6: [(0, 4, 'F#5'), (4, 2, 'D5'), (6, 2, 'F#5'), (8, 8, 'A5')],
        7: [(0, 2, 'B5'), (2, 2, 'A5'), (4, 2, 'G5'), (6, 2, 'F#5'), (8, 8, 'F#5')]}

A_PROG = ['Em', 'Em', 'C', 'D', 'Em', 'Em', 'F', 'B']
THEME = [
    [(0, 4, 'E5'), (4, 2, 'B4'), (6, 2, 'E5'), (8, 3, 'G5'), (11, 3, 'F#5'), (14, 2, 'E5')],
    [(0, 3, 'D5'), (3, 3, 'E5'), (6, 10, 'B4')],
    [(0, 4, 'E5'), (4, 2, 'B4'), (6, 2, 'E5'), (8, 3, 'G5'), (11, 3, 'A5'), (14, 2, 'B5')],
    [(0, 3, 'C6'), (3, 3, 'B5'), (6, 2, 'A5'), (8, 4, 'F#5'), (12, 4, 'D5')],
    [(0, 6, 'G5'), (6, 2, 'F#5'), (8, 4, 'E5'), (12, 2, 'D5'), (14, 2, 'E5')],
    [(0, 8, 'B4'), (8, 2, 'E5'), (10, 2, 'F#5'), (12, 2, 'G5'), (14, 2, 'A5')],
    [(0, 3, 'C6'), (3, 3, 'A5'), (6, 2, 'F5'), (8, 4, 'A5'), (12, 4, 'C6')],
    [(0, 6, 'B5'), (6, 2, 'A5'), (8, 4, 'F#5'), (12, 4, 'D#5')],
]
# A2: de tweede helft eindigt anders (chromatisch: E-F-F#-G in de melodie, Hoenn)
THEME2 = THEME[:4] + [
    [(0, 3, 'E5'), (3, 1, 'E5'), (4, 2, 'F5'), (6, 2, 'B4'), (8, 6, 'E5'), (14, 2, 'G5')],
    [(0, 4, 'F#5'), (4, 2, 'E5'), (6, 2, 'D5'), (8, 8, 'E5')],
    [(0, 3, 'F5'), (3, 3, 'A5'), (6, 2, 'C6'), (8, 4, 'B5'), (12, 4, 'A5')],
    [(0, 4, 'B5'), (4, 4, 'D#6'), (8, 8, 'F#5')],
]
B_PROG = ['C', 'D', 'Bm', 'Em', 'Am', 'D', 'G', 'B']
SONG_B = [
    [(0, 8, 'E5'), (8, 4, 'G5'), (12, 4, 'F#5')],
    [(0, 8, 'F#5'), (8, 4, 'A5'), (12, 2, 'G5'), (14, 2, 'F#5')],
    [(0, 12, 'D5'), (12, 4, 'F#5')],
    [(0, 12, 'E5'), (12, 2, 'B4'), (14, 2, 'D5')],
    [(0, 8, 'C6'), (8, 4, 'B5'), (12, 4, 'A5')],
    [(0, 8, 'A5'), (8, 4, 'F#5'), (12, 4, 'D5')],
    [(0, 6, 'G5'), (6, 2, 'A5'), (8, 8, 'B5')],
    [(0, 6, 'B5'), (6, 2, 'C6'), (8, 4, 'B5'), (12, 4, 'F#5')],
]
C_PROG = ['Em', 'Em', 'Fm', 'Fm', 'F#m', 'F#m', 'G', 'B']
FAN1 = [(0, 2, 0), (2, 1, 0), (3, 1, 0), (4, 4, 7), (8, 2, 3), (10, 2, 5), (12, 4, 7)]
FAN2 = [(0, 3, 8), (3, 3, 7), (6, 2, 3), (8, 8, 0)]
FAN_END = [[(0, 3, 'B5'), (3, 3, 'A5'), (6, 2, 'G5'), (8, 8, 'D5')],
           [(0, 4, 'D#5'), (4, 4, 'F#5'), (8, 8, 'B5')]]
D_PROG = ['F#m', 'F#m', 'D', 'E', 'F#m', 'F#m', 'G', 'C#']
T_PROG = ['C', 'D', 'B', 'B']
T_TPT = [[(0, 2, 'G5'), (3, 2, 'G5'), (6, 10, 'E5')],
         [(0, 2, 'A5'), (3, 2, 'A5'), (6, 10, 'F#5')],
         [(0, 2, 'B5'), (3, 2, 'B5'), (6, 2, 'B5'), (8, 8, 'D#5')],
         [(0, 4, 'F#5'), (4, 4, 'A5'), (8, 8, 'B5')]]


def harmonize(notes, chord_at, lo=55, hi=74, gap=3):
    """hoorns onder de trompet: hoogste akkoordtoon minstens `gap` halve tonen onder de melodienoot (tertsen/sexten)."""
    out = []
    for s, e, m, v in notes:
        ch = chord_at(s)
        cand = [n for n in tones(ch, lo, hi) if n <= m - gap]
        if not cand:
            continue
        out.append([s, e, cand[-1], v])
    return out


def voice_lead(bars, lo, hi, vel, unit=8):
    """tegenstem: per `unit` 16en een akkoordtoon, zo dicht mogelijk bij de vorige (niet 3x dezelfde)."""
    out, prev, same = [], None, 0
    for t0, ch in bars:
        for h in range(0, 16, unit):
            cand = tones(ch, lo, hi)
            if prev is None:
                n = cand[len(cand) // 2]
            else:
                cand.sort(key=lambda m: (abs(m - prev), m))
                n = cand[0]
                if n == prev:
                    same += 1
                    if same >= 2 and len(cand) > 1:
                        n, same = cand[1], 0
                else:
                    same = 0
            out.append([t0 + h * S, t0 + (h + unit) * S, n, vel])
            prev = n
    return out


def timp_pair(ch):
    t = near(CH[ch][0], 41)          # grondtoon F2..E3
    return t, t - 5                  # (hoog = grondtoon, laag = kwint eronder), zoals G2/C3 in Kyogre/Groudon


def timpani(P, t0, ch, vel, mode='ost'):
    hi, lo = timp_pair(ch)
    if mode == 'ost':                # laag-hoog-laag-laag-hoog-laag-laag-hoog in achtsten
        for k, n in enumerate((lo, hi, lo, lo, hi, lo, lo, hi)):
            P['timp'].append([t0 + 2 * k * S, t0 + 2 * k * S + 2 * S, n, vel + (14 if k in (0, 4) else 0)])
    elif mode == 'half':             # B: per tel
        for k, n in enumerate((hi, lo, hi, lo)):
            P['timp'].append([t0 + 4 * k * S, t0 + 4 * k * S + 4 * S, n, vel + (12 if k == 0 else 0)])
    elif mode == 'hit':
        P['timp'].append([t0, t0 + 4 * S, hi, vel])


def troll(P, t0, ch, st, n, v0, dv):
    """paukenroffel in 16en (korte release) op de grondtoon."""
    hi, _ = timp_pair(ch)
    for k in range(n):
        P['troll'].append([t0 + (st + k) * S, t0 + (st + k + 1) * S, hi, min(127, v0 + dv * k)])


def bass(P, t0, ch, nxt, vel, half=False):
    r = near(CH[ch][0], 36)
    if half:
        for k, off in enumerate((0, 0, 12, 0)):
            P['bass'].append([t0 + 4 * k * S, t0 + 4 * k * S + 3 * S, r + off, vel + (10 if k == 0 else 0)])
        return
    for k in range(8):
        n = r
        if k == 7 and nxt and nxt != ch:          # chromatische opmaat naar het volgende akkoord
            nr = near(CH[nxt][0], 36)
            n = nr - 1 if nr - 1 >= 36 and nr - 1 != r else nr + 1
        elif k in (3, 6):
            n = r + 12
        P['bass'].append([t0 + 2 * k * S, t0 + 2 * k * S + 2 * S, n, vel + (10 if k in (0, 4) else 0)])


def arp(P, t0, ch, lo, vel, part='sq'):
    ts = tones(ch, lo, lo + 19)[:5]
    pat = (0, 1, 2, 3, 2, 1, 2, 3)
    for k in range(16):
        n = ts[pat[k % 8] % len(ts)]
        P[part].append([t0 + k * S, t0 + k * S + S, n, vel])


def wave(P, t0, ch):
    r = near(CH[ch][0], 36)
    P['wave'].append([t0, t0 + 8 * S, r, 100])
    P['wave'].append([t0 + 8 * S, t0 + 16 * S, r, 100])


def strings_pad(P, t0, ch, lo, hi, vel, part='strings'):
    """liggende strijkerstoon (één stem: het sample is al een ensemble), in halve maten."""
    cand = tones(ch, lo, hi)
    n = cand[len(cand) // 2]
    P[part] += [[t0, t0 + 8 * S, n, vel], [t0 + 8 * S, t0 + 16 * S, n, vel]]


def compose():
    P, CC = Parts(), Parts()
    tl = []
    tl += [('I', i, c) for i, c in enumerate(INTRO)]
    tl += [('A', i, c) for i, c in enumerate(A_PROG)]
    tl += [('A2', i, c) for i, c in enumerate(A_PROG)]
    tl += [('B', i, c) for i, c in enumerate(B_PROG)]
    tl += [('C', i, c) for i, c in enumerate(C_PROG)]
    tl += [('D', i, c) for i, c in enumerate(D_PROG)]
    tl += [('T', i, c) for i, c in enumerate(T_PROG)]
    chords = [c for _, _, c in tl]

    def chord_at(t):
        return chords[t // BAR]

    for bi, (sec, i, ch) in enumerate(tl):
        t0 = bi * BAR
        nxt = chords[bi + 1] if bi + 1 < len(chords) else 'Em'
        last = (sec in 'ACD' or sec == 'A2' or sec == 'B') and i == 7 or (sec == 'T' and i == 3) or (sec == 'I' and i == 7)
        # ---------------- melodie en koper ----------------
        if sec == 'I':
            if i >= 4:
                m = mel(CALL[i], t0, 112)
                P['tpt'] += m
                P['horn'] += [[s, e, n - 12, v] for s, e, n, v in m]      # koperroep in octaven
                strings_pad(P, t0, ch, 52, 64, 96)
            else:
                P['strings'] += [[t0, t0 + 8 * S, p('E3') + (7 if i % 2 else 0), 84 + 4 * i],
                                 [t0 + 8 * S, t0 + 16 * S, p('E3') + (7 if i % 2 else 0), 84 + 4 * i]]
            if i in (0, 2):
                P['bell'].append([t0, t0 + 8 * S, p('E4'), 104])
            if i == 3:
                P['bell'].append([t0, t0 + 8 * S, p('B3'), 104])
        elif sec == 'A':
            m = mel(THEME[i], t0, 112)
            P['tpt'] += m
            P['horn'] += harmonize(m, chord_at)
            P['sqmel'] += [[s, e, n, 80] for s, e, n, v in m]
            strings_pad(P, t0, ch, 55, 67, 92)
        elif sec == 'A2':
            m = mel(THEME2[i], t0, 116)
            P['tpt'] += m
            P['strings'] += [[s, e, n - 12, 104] for s, e, n, v in m]   # strijkers in octaven met de trompet
        elif sec == 'B':
            m = mel(SONG_B[i], t0, 112)
            P['strings'] += m
            P['strings2'] += [[s, e, n - 12, 100] for s, e, n, v in m]
            if i in (6, 7):
                P['tpt'] += [[s, e, n, 100] for s, e, n, v in harmonize(m, chord_at, lo=62, hi=76)]
        elif sec == 'C':
            if i < 6:
                r = near(CH[ch][0], 76)
                pat = FAN1 if i % 2 == 0 else FAN2
                m = [[t0 + st * S, t0 + (st + ln) * S, r + iv, 116 if st == 0 else 108] for st, ln, iv in pat]
            else:
                m = mel(FAN_END[i - 6], t0, 116)
            P['tpt'] += m
            P['horn'] += [[s, e, n - 12, v] for s, e, n, v in m]
            strings_pad(P, t0, ch, 50, 62, 96)
        elif sec == 'D':
            m = mel(THEME[i], t0, 118, tr=2)
            P['tpt'] += m
            P['strings'] += [[s, e, n - 12, 108] for s, e, n, v in m]
            if i % 2 == 0:
                P['bell'].append([t0, t0 + 8 * S, near(CH[ch][0], 64), 110])
        elif sec == 'T':
            m = mel(T_TPT[i], t0, 118)
            P['tpt'] += m
            P['horn'] += [[s, e, n - 12, v] for s, e, n, v in m]
            strings_pad(P, t0, ch, 52, 64, 100)
        # ---------------- hoorn-tegenstem (A2, D) ----------------
        if sec in ('A2', 'D'):
            P['horn'] += voice_lead([(t0, ch)], 55, 67, 100) if sec == 'A2' else voice_lead([(t0, ch)], 57, 69, 104)
        # ---------------- bas, sub, PSG ----------------
        if sec == 'I':
            if i >= 4:
                bass(P, t0, ch, nxt, 104)
            wave(P, t0, ch)
        elif sec == 'B':
            bass(P, t0, ch, nxt, 104, half=True)
            wave(P, t0, ch)
        else:
            bass(P, t0, ch, nxt, 108)
            wave(P, t0, ch)
        if sec in ('A2', 'C', 'D'):
            arp(P, t0, ch, 64 if sec != 'D' else 66, 90)
        if sec == 'B':
            arp(P, t0, ch, 72, 70)
        # ---------------- pauken ----------------
        if sec == 'I':
            if i < 7:
                timpani(P, t0, ch, 80 + 4 * i)
            else:
                timpani(P, t0, ch, 104, 'hit')
                troll(P, t0, ch, 4, 12, 84, 3)
        elif sec == 'B':
            timpani(P, t0, ch, 100, 'half')
        elif last:
            timpani(P, t0, ch, 108, 'hit')
            P['timp'].append([t0 + 6 * S, t0 + 8 * S, timp_pair(ch)[1], 104])
            troll(P, t0, ch, 8, 8, 92, 4)
        else:
            timpani(P, t0, ch, 100)
        # ---------------- drums ----------------
        if i == 0 and sec != 'I' or (sec == 'I' and i == 4) or (sec in ('C', 'D') and i == 4):
            drum(P, t0, (0,), CRASH, 116)
        if sec == 'D' and i in (2, 6):
            drum(P, t0, (0,), CRASH2, 108)
        if sec in ('A', 'A2', 'D'):
            drum(P, t0, (0,), TAIKO, 112)
            if not last:
                drum(P, t0, (4, 12), OSN, 100)
                if i % 2 == 1:
                    drum(P, t0, (14, 15), OSN, 92)
        elif sec == 'C':
            drum(P, t0, (0, 10), TAIKO, 114)
            if i % 2 == 1 and i != 7:
                roll(P, t0, 12, 4, OSN, 90, 6)
            else:
                drum(P, t0, (4, 12), OSN, 100)
        elif sec == 'B':
            drum(P, t0, (0,), TAIKO, 104)
            drum(P, t0, (12,), OSN, 96)
        elif sec == 'T':
            drum(P, t0, (0, 3, 6), TAIKO, 116)
        if sec == 'I' and i == 7:
            roll(P, t0, 8, 8, OSN, 86, 5)
        if last and sec != 'I':
            if sec == 'C' or sec == 'T':
                roll(P, t0, 8, 8, OSN, 88, 5)
            else:
                drum(P, t0, (12, 13), TOM_H, 104)
                drum(P, t0, (14,), TOM_M, 108)
                drum(P, t0, (15,), TOM_L, 112)
    # dynamiek: B iets terug (CC7 per sectie op de begeleiding)
    end = len(tl) * BAR
    return P, CC, end


LAYOUT = [  # (partij, programma, volume, kanaal, pan)
    ('tpt', TPT, 104, 0, 64), ('horn', HORN, 96, 1, 52), ('strings', STR, 90, 2, 76), ('strings2', STR, 78, 3, 52),
    ('bass', FBASS, 100, 4, 64), ('timp', TIMP, 108, 5, 64), ('troll', TROLL, 100, 6, 64), ('bell', BELL, 80, 7, 70),
    ('sq', SQ1, 46, 8, 40), ('sqmel', SQ2, 40, 10, 88), ('wave', WAVE, 52, 11, 64),
]
ORDER = ['tpt', 'drums', 'timp', 'troll', 'horn', 'strings', 'bass', 'bell', 'strings2']
DRUMVOL = 112


def voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm + overrides voor Battle! Legendary Pokémon (MUS_GROUNDED_VS_LEGENDARY).'
    lines[1] = '@ Gegenereerd door tools/grounded/legendary_theme.py. Alleen Emerald-samples (Hoenn-koper/-strijkers/-pauken).'
    lines[2] = 'voice_group %s' % VG
    over = {
        14: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_tubular_bell, 255, 216, 90, 200',
        33: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_fingered_bass, 255, 253, 0, 149',
        45: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 90',
        47: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 170',
        48: 'voice_keysplit voicegroup_strings_keysplit, keysplit_strings',
        56: 'voice_keysplit voicegroup_trumpet_keysplit, keysplit_trumpet',
        60: 'voice_keysplit voicegroup_french_horn_keysplit, keysplit_french_horn',
        80: 'voice_square_1 60, 0, 0, 2, 0, 1, 7, 1',
        81: 'voice_square_2 60, 0, 2, 0, 1, 7, 1',
        84: 'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_1, 0, 7, 15, 0',
        127: 'voice_keysplit_all voicegroup_legendary_drumset',
    }
    out = []
    for l in lines:
        for k, v in over.items():
            if l.rstrip().endswith('@ %d' % k):
                l = '\t%s  @ %d' % (v, k)
        out.append(l)
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    kit = [
        ('36 taiko', 'voice_directsound 57, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180'),
        ('37 orkestsnare', 'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 200'),
        ('38 tom laag', 'voice_directsound 45, 52, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 204'),
        ('39 tom midden', 'voice_directsound 51, 64, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 204'),
        ('40 tom hoog', 'voice_directsound 57, 76, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 204'),
        ('41 orkestbekken', 'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 216'),
        ('42 crash', 'voice_directsound 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165'),
    ]
    open('sound/voicegroups/drumsets/legendary.inc', 'w').write(
        '@ Project Grounded: drumkit voor legendary_theme.py (Battle! Legendary Pokémon). Alleen stock-samples, geen PSG.\n'
        '@ ' + ', '.join(n for n, _ in kit) + '.\n'
        '@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.\n'
        'voice_group legendary_drumset, 36\n' + ''.join('\t%s\n' % v for _, v in kit))


def build(refdir=None):
    P, CC, end = compose()
    for k in list(P):
        P[k] = dedupe(P[k])
    cr = {e[0] for e in P['drums'] if e[2] in (CRASH, CRASH2)}
    P['drums'] = [e for e in P['drums'] if not (e[2] == OSN and e[0] in cr and e[3] < 95)]
    progs = {k: pr for k, pr, *_ in LAYOUT}
    rel = releases(VG)
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) + 2 for k, pr in progs.items()}
    for k, pr in progs.items():
        if rel.get(pr) is not None:
            P[k] = detach(P[k], tail[k])
    for k, pr in progs.items():
        if rel.get(pr) is not None:
            low = [n for _, _, n, _ in P[k] if n < 36]
            assert not low, '%s: DirectSound-noten onder C2: %s' % (k, low[:5])
            if pr in (TPT, HORN):
                bad = [n for _, _, n, _ in P[k] if n < 48]
                assert not bad, '%s: koper onder C3 %s' % (k, bad[:5])
            soft = [v for _, _, _, v in P[k] if v < 76]
            assert not soft, '%s: zachte DS-noten (8-bit-fuzz) %s' % (k, soft[:5])
        else:
            low = [n for _, _, n, _ in P[k] if n < 36]
            assert not low, '%s: PSG-noten onder C2' % k
    ds = {k: P[k] for k in ORDER}
    kept = allocate(ds, ORDER, tail, max_voices=MAXV)
    for k in ORDER:
        n = len(ds[k])
        if n and len(kept[k]) < n:
            print('  %s: %d van %d noten vallen weg (%.1f%%)' % (k, n - len(kept[k]), n, 100 * (n - len(kept[k])) / n))
            if os.environ.get('LG_DEBUG'):
                kk = {tuple(e) for e in kept[k]}
                print('     weg op maat:', [round(e[0] / BAR, 2) for e in ds[k] if tuple(e) not in kk][:24])
        P[k] = kept[k]
    lp = 8 * BAR
    for ref in (False, True):
        if ref and not refdir:
            continue
        song = Song(TPB, 500000)
        song.tempo(0, BPM / 120)
        song.loop = (lp, end)
        for k, pr, vol, ch, pan in LAYOUT:
            song.add(P[k], pr if not ref else (pr if pr < 80 else 80), vol, ch, pan, ccs=list(CC.get(k, [])))
        drums = sorted(P['drums'])
        if ref:
            gm = {TAIKO: 35, OSN: 38, TOM_L: 41, TOM_M: 45, TOM_H: 48, CRASH: 49, CRASH2: 57}
            drums = [[s, e, gm[n], v] for s, e, n, v in drums]
        song.add(drums, KIT if not ref else 0, DRUMVOL, 9)
        written = {k for k, *_ in LAYOUT} | {'drums'}
        assert not [k for k in P if P[k] and k not in written], [k for k in P if P[k] and k not in written]
        out = os.path.join(refdir, 'legendary_ref.mid') if ref else OUT
        song.save(out, end)
        if not ref:
            print(out, '| intro %.1f s | loop %.1f s | totaal %.1f s' % (
                lp / TPB * 60 / BPM, (end - lp) / TPB * 60 / BPM, end / TPB * 60 / BPM))


if __name__ == '__main__':
    ref = sys.argv[sys.argv.index('--ref') + 1] if '--ref' in sys.argv else None
    voicegroup()
    build(ref)
