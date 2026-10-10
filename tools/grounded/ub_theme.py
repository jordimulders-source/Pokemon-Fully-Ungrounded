#!/usr/bin/env python3
"""Project Grounded: Battle! Ultra Beast (MUS_GROUNDED_VS_ULTRA_BEAST = 677), eigen compositie.

Jordi: "Ik wil een Ultra Beast theme maken, wat heel maf moet klinken, battle theme die wel veel regels van een battle
theme klinkt, moet echt klinken alsof het uit andere dimensies komt." (Rainbow Road was 'te euforisch'.)

Gevechtsregels: 168 bpm, intro van 8 maten, drijvende bas-ostinato, één duidelijke leadmelodie, loop vanaf A.
Andere dimensie:
  - octatonische toonladder (C Db Eb E F# G A Bb, half-heel): geen majeur/mineur, geen 'thuis'. Het thema komt terug
    een kleine terts lager (A2) en hoger (D): bij deze ladder zijn dat precies dezelfde tonen, dus het 'verschuift' zonder
    ooit ergens anders te komen. B is heeltoons (C D E F# G# Bb) in 7/8, C een Db-pedaal (frygisch, half-time).
  - de lead is een glazen FM-klank (ub_glass: niet-harmonische modulator x1,41, twee stemmen 13 cent uit elkaar) met
    pitch bends per noot: kwarttoon-scoops omhoog, duiken van een halve toon aan het eind van lange noten, en een
    kwarttoon-wiebel (geen gewoon vibrato, ongelijk);
  - de PSG-echo speelt de lead 3 zestienden later en 0,3 halve toon te hoog = een 'spiegelbeeld' dat net niet klopt;
  - twee koorstemmen buigen in tegengestelde richting een kwarttoon weg (microtonale cluster);
  - omgekeerde zwellingen (ub_swell, achterstevoren gespeelde FM-klok) naar elke sectie, de 'scheur';
  - glitches als muziek: glas-stotters in 32sten, PSG-'zaps' (blokgolf 1 met sweep), metallic ruis (korte periode);
  - verschoven accenten (bas 3+3+2 in 4/4), maten in 7/8 (B en de turnaround), grote sprongen (C4 -> Db6).
Vorm: I 8 | A 8 | A2 8 (thema -3) | B 8 x 7/8 | C 8 (glitch-dimensie) | D 8 (thema +3, climax) | T 7/8 + 4/4 -> A.
Eigen samples: ub_glass + ub_swell (ub_samples.py, 11 kHz, ±16 KB). Verder stock (synth bass, koor, detuned EP,
rnd-kit, 909-clap, trinity crash, ambient tom) en PSG.
Stemverdeler max. 11 DirectSound-noten (legendary).
  python3 tools/grounded/ub_theme.py [--ref <map>]
Zie tools/grounded/MUZIEK.md."""
import os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

VG = 'grounded_ub'
OUT = 'sound/songs/midi/mus_grounded_vs_ultra_beast.mid'
MAXV = 11
BPM = 168
TPB = 96
S = TPB // 4
T32 = S // 2

N = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
     'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def p(name):
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


# programma's in voicegroup_grounded_ub
EP, CHOIR, BASS, GLASS_S, GLASS, SWELL, KIT = 4, 52, 38, 87, 88, 89, 127
SQ1, SQ2, ZAP, WAVE, HAT, METAL = 80, 81, 82, 84, 120, 121
# drumkit drumsets/ub.inc (vanaf 36)
KICK, SNARE, SYN, CLAP, CRASH, TOM_L, TOM_H = range(36, 43)
DLEN = {KICK: 2 * S, SNARE: 3 * S, SYN: 2 * S, CLAP: 3 * S, CRASH: 2 * TPB, TOM_L: 4 * S, TOM_H: 4 * S}
BEND = 2                       # bend-range (halve tonen)


def pw(semis):
    return max(-8192, min(8191, int(round(8192 * semis / BEND))))


class Parts(dict):
    def __missing__(self, k):
        self[k] = []
        return self[k]


# ---------------------------------------------------------------------------------------------------------------------
# materiaal: (stap, lengte, noot[, effect]) per maat; effect: 'scoop' kwarttoon van onder, 'dive' zakt een halve toon,
# 'wob' kwarttoon-wiebel
# ---------------------------------------------------------------------------------------------------------------------
INTRO_LEAD = {
    1: [(0, 3, 'C5'), (3, 3, 'F#5'), (6, 2, 'C6'), (8, 8, 'Db5', 'dive')],
    3: [(0, 3, 'C6'), (3, 3, 'F#5'), (6, 2, 'C5'), (8, 8, 'B4', 'dive')],
    4: [(0, 2, 'C5'), (2, 2, 'Eb5'), (4, 2, 'F#5'), (6, 2, 'A5'), (8, 4, 'C6'), (12, 4, 'Bb5')],
    5: [(0, 6, 'G5', 'wob'), (6, 2, 'E5'), (8, 8, 'Db5', 'dive')],
    6: [(0, 2, 'Db5'), (2, 2, 'E5'), (4, 2, 'G5'), (6, 2, 'Bb5'), (8, 4, 'Db6'), (12, 4, 'C6')],
    7: [(0, 8, 'C6', 'wob'), (8, 2, 'F#4'), (10, 2, 'G4'), (12, 4, 'C5', 'scoop')],
}
INTRO_ROOTS = [0, 0, 0, 0, 0, 1, 0, 6]

THEME = [
    [(0, 4, 'C5'), (4, 2, 'G4'), (6, 2, 'Db5'), (8, 6, 'E5', 'scoop'), (14, 2, 'Eb5')],
    [(0, 8, 'F#5', 'dive'), (8, 2, 'A4'), (10, 2, 'Bb4'), (12, 4, 'C5')],
    [(0, 2, 'C6'), (3, 2, 'F#4'), (6, 2, 'C6'), (8, 4, 'Bb5'), (12, 4, 'G5')],
    [(0, 6, 'A5', 'wob'), (6, 2, 'G5'), (8, 8, 'E5', 'dive')],
    [(0, 4, 'C5'), (4, 2, 'G4'), (6, 2, 'Db5'), (8, 6, 'E5', 'scoop'), (14, 2, 'Eb5')],
    [(0, 8, 'F#5', 'scoop'), (8, 2, 'E5'), (10, 2, 'Eb5'), (12, 2, 'Db5'), (14, 2, 'C5')],
    [(0, 3, 'Eb5'), (3, 3, 'E5'), (6, 2, 'F#5'), (8, 3, 'G5'), (11, 3, 'A5'), (14, 2, 'Bb5')],
    [(0, 4, 'C6'), (4, 4, 'Db6'), (8, 8, 'G5', 'wob')],
]
A_ROOTS = [0, 0, 1, 0, 3, 3, 4, 6]

B_LEAD = [  # 7/8 = 14 zestienden, heeltoons
    [(0, 2, 'E5'), (2, 2, 'F#5'), (4, 4, 'G#5'), (8, 2, 'Bb5'), (10, 4, 'C6', 'dive')],
    [(0, 2, 'D5'), (2, 2, 'E5'), (4, 4, 'F#5'), (8, 2, 'G#5'), (10, 4, 'Bb5', 'dive')],
    [(0, 6, 'C6', 'wob'), (6, 2, 'Bb5'), (8, 2, 'G#5'), (10, 2, 'F#5'), (12, 2, 'E5')],
    [(0, 8, 'D5', 'scoop'), (8, 6, 'G#4', 'dive')],
    [(0, 2, 'E5'), (2, 2, 'F#4'), (4, 4, 'G#5'), (8, 2, 'Bb4'), (10, 4, 'C6')],
    [(0, 2, 'C6'), (2, 2, 'D5'), (4, 4, 'Bb5'), (8, 2, 'E5'), (10, 4, 'F#5', 'dive')],
    [(0, 4, 'G#5'), (4, 4, 'Bb5'), (8, 6, 'C6', 'wob')],
    [(8, 6, 'F#4', 'scoop')],
]
B_ROOTS = [0, 2, 4, 6, 0, 2, 6, 8]

C_LEAD = [
    [(0, 12, 'Db5', 'wob'), (12, 4, 'G5')],
    [(0, 4, 'C6'), (4, 12, 'G4', 'dive')],
    [(0, 12, 'C5', 'wob'), (12, 2, 'F#5'), (14, 2, 'G5')],
    [(0, 16, 'Db6', 'dive')],
    [(12, 4, 'C6', 'scoop')],
    [(0, 8, 'B5', 'scoop'), (8, 8, 'F5', 'dive')],
    [(0, 4, 'F#5'), (4, 4, 'C5'), (8, 4, 'F#4'), (12, 4, 'C6')],
    [(0, 8, 'G5', 'wob'), (8, 8, 'Db5', 'dive')],
]
C_ROOTS = [1, 1, 0, 0, 1, 1, 6, 7]
# glas-stotters: maat -> [(stap, aantal 32sten, noot)]
C_STUT = {4: [(0, 8, 'C5'), (8, 6, 'F#5')], 1: [(13, 6, 'C6')], 7: [(0, 4, 'G5')]}

T_LEAD = [[(0, 2, 'C6'), (4, 2, 'F#5'), (8, 6, 'C5', 'dive')],
          [(0, 8, 'Db5', 'wob')]]
T_ROOTS = [1, 7]

BASS4 = [(0, 2, 0), (3, 2, 0), (6, 2, 12), (8, 2, 0), (10, 1, 0), (11, 2, 13), (14, 2, 6)]
BASS7 = [(0, 3, 0), (4, 3, 0), (8, 2, 12), (10, 2, 0), (12, 2, 1)]
BASSC = [(0, 6, 0), (6, 2, 12), (8, 6, 0), (14, 2, 1)]


def near(pc, lo):
    return lo + ((pc - lo) % 12)


def compose():
    P, X = Parts(), Parts()        # X: extra events (pitchwheel) per partij, CC: programmawissels
    CC = Parts()
    tl = []
    tl += [('I', i, 16, r) for i, r in enumerate(INTRO_ROOTS)]
    tl += [('A', i, 16, r) for i, r in enumerate(A_ROOTS)]
    tl += [('A2', i, 16, (r - 3) % 12) for i, r in enumerate(A_ROOTS)]
    tl += [('B', i, 14, r) for i, r in enumerate(B_ROOTS)]
    tl += [('C', i, 16, r) for i, r in enumerate(C_ROOTS)]
    tl += [('D', i, 16, (r + 3) % 12) for i, r in enumerate(A_ROOTS)]
    tl += [('T', 0, 14, T_ROOTS[0]), ('T', 1, 16, T_ROOTS[1])]
    starts, t = [], 0
    for sec, i, ln, r in tl:
        starts.append(t)
        t += ln * S
    end = t
    loop = starts[8]

    def lead(t0, pat, tr=0, vel=112, part='lead', bendpart='lead'):
        for x in pat:
            st, ln, n = x[:3]
            fx = x[3] if len(x) > 3 else None
            s, e = t0 + st * S, t0 + (st + ln) * S
            P[part].append([s, e, p(n) + tr, vel])
            ev = X[bendpart]
            if fx == 'scoop':
                ev += [(s, pw(-0.5)), (s + 4, pw(-0.33)), (s + 8, pw(-0.16)), (s + 12, 0)]
            elif fx == 'dive':
                ev.append((s, 0))
                mid = s + (e - s) // 2
                k = 6
                for j in range(1, k + 1):
                    ev.append((mid + (e - mid) * j // (k + 1), pw(-1.0 * j / k)))
            elif fx == 'wob':
                ev.append((s, 0))
                q, j = s + 12, 0
                while q < e - 6:
                    ev.append((q, pw((0.25, -0.12, 0.3, -0.2)[j % 4])))
                    q, j = q + 12, j + 1
            else:
                ev.append((s, 0))

    def echo(t0, pat, tr=0, vel=70):
        for x in pat:
            st, ln, n = x[:3]
            s = t0 + (st + 3) * S
            P['echo'].append([s, s + min(ln, 2) * S, p(n) + tr, vel])

    def stut(t0, st, cnt, n, vel=104):
        for k in range(cnt):
            s = t0 + st * S + k * T32
            P['stut'].append([s, s + 6, p(n) + (12 if k == cnt - 1 and cnt > 4 else 0), vel - 2 * k])

    def drum(t0, steps, key, vel):
        for k in steps:
            P['drums'].append([t0 + int(k * S), t0 + int(k * S) + DLEN[key], key, vel])

    def hats(t0, n, every=1, acc=(96, 60, 76, 60), metal=()):
        for k in range(0, n, every):
            P['hat'].append([t0 + k * S, t0 + k * S + S // 2, 88 if k % 4 else 92, acc[k % 4]])
        for k in metal:
            P['metal'].append([t0 + k * S, t0 + k * S + S, 70, 90])

    def bass(t0, r, pat, vel=110):
        b = near(r, 36)
        for st, ln, iv in pat:
            P['bass'].append([t0 + st * S, t0 + (st + ln) * S, b + iv, vel + (8 if st == 0 else 0)])

    def wave(t0, r, n):
        b = near(r, 36)
        half = n // 2
        P['wave'] += [[t0, t0 + half * S, b, 100], [t0 + half * S, t0 + n * S, b, 100]]

    def ep(t0, r, steps, vel=92):
        lo = near(r + 4, 55)
        for st in steps:
            for iv in (0, 6):                       # tritonus-schelp (terts + kleine septiem van de grondtoon)
                P['ep'].append([t0 + st * S, t0 + (st + 2) * S, lo + iv, vel])

    def choir(t0, r, n, vel=96):
        a, b = near(r + 6, 60), near(r + 11, 64)    # tritonus + grote septiem: hangt, lost nooit op
        for h in range(0, n, 8):
            ln = min(8, n - h)
            s, e = t0 + h * S, t0 + (h + ln) * S
            P['choir1'].append([s, e, a, vel])
            P['choir2'].append([s, e, b, vel - 6])
            for j in range(4):
                X['choir1'].append((s + (e - s) * j // 4, pw(0.5 * j / 3)))
                X['choir2'].append((s + (e - s) * j // 4, pw(-0.5 * j / 3)))

    def swell(tdown, r, vel=104):
        L = 309 * TPB // 96 * 168 // BPM          # 1,15 s in ticks
        s = max(0, tdown - L)
        for n in (near(r, 60), near(r + 6, 60)):
            P['swell'].append([s, tdown, n, vel])

    def arp(t0, r, n, kind='oct', lo=72, vel=60):
        if kind == 'oct':
            seq = [0, 3, 6, 9, 12, 9, 6, 3]
        else:
            seq = [0, 2, 4, 6, 8, 10, 12, 14]
        b = near(r, lo)
        for k in range(n):
            P['sq'].append([t0 + k * S, t0 + k * S + S, b + seq[k % 8], vel])

    def zap(t0, st, n, vel=80):
        s = t0 + st * S
        CC['sq'].append((s, 'prog', ZAP))
        P['sq'].append([s, s + 3 * S, p(n), vel])
        CC['sq'].append((s + 3 * S, 'prog', SQ1))

    for bi, (sec, i, n, r) in enumerate(tl):
        t0 = starts[bi]
        nxt_t = starts[bi + 1] if bi + 1 < len(tl) else end
        nxt_r = tl[bi + 1][3] if bi + 1 < len(tl) else 0
        last = i == 7 or sec == 'T' and i == 1
        # ---------------- lead ----------------
        if sec == 'I':
            if i in INTRO_LEAD:
                lead(t0, INTRO_LEAD[i])
                if i >= 4:
                    echo(t0, INTRO_LEAD[i])
            if i == 2:
                stut(t0, 12, 8, 'C6')
            if i == 0:
                zap(t0, 4, 'C6'); zap(t0, 10, 'F#6'); zap(t0, 13, 'C7')
        elif sec in ('A', 'A2', 'D'):
            tr = {'A': 0, 'A2': -3, 'D': 3}[sec]
            lead(t0, THEME[i], tr, 116 if sec == 'D' else 112)
            echo(t0, THEME[i], tr + (12 if sec == 'A2' else 0))
            if sec == 'D' and i == 3:
                stut(t0, 14, 4, 'C6')
        elif sec == 'B':
            lead(t0, B_LEAD[i])
            echo(t0, B_LEAD[i])
            if i == 7:
                stut(t0, 0, 12, 'C6')
                zap(t0, 6, 'Bb6')
        elif sec == 'C':
            lead(t0, C_LEAD[i])
            for st, cnt, nn in C_STUT.get(i, []):
                stut(t0, st, cnt, nn)
            if i in (2, 6):
                zap(t0, 14, 'C7')
        elif sec == 'T':
            lead(t0, T_LEAD[i])
            if i == 1:
                stut(t0, 8, 8, 'Db6')
        # ---------------- bas, sub ----------------
        if sec == 'I':
            if i >= 2:
                bass(t0, r, BASS4, 104 if i < 4 else 110)
            wave(t0, r, n)
        elif sec == 'B' or (sec == 'T' and i == 0):
            bass(t0, r, BASS7)
            wave(t0, r, n)
        elif sec == 'C':
            bass(t0, r, BASSC, 108)
            wave(t0, r, n)
        else:
            bass(t0, r, BASS4)
            wave(t0, r, n)
        # ---------------- harmonie ----------------
        if sec in ('A', 'A2', 'D') or (sec == 'I' and i >= 4):
            ep(t0, r, (3, 10) if i % 2 == 0 else (3, 6, 10))
        if sec == 'T' and i == 0:
            ep(t0, r, (0, 4, 8), 100)
        if sec in ('B', 'C', 'D', 'A2'):
            choir(t0, r, n)
        if sec in ('A2', 'D'):
            arp(t0, r, n, 'oct', 76 if sec == 'D' else 72)
        if sec == 'C':
            arp(t0, r, n, 'whole', 72, 56)
        if sec == 'B' and i % 2 == 1:
            arp(t0 + 8 * S, r, 6, 'whole', 76, 52)
        # zwellingen naar de volgende sectie
        if last and bi + 1 < len(tl) or (sec == 'I' and i == 0):
            swell(nxt_t, nxt_r)
        if sec == 'T' and i == 1:
            swell(end, 0)                          # naar het loopbegin (A, grondtoon C)
        # ---------------- drums ----------------
        if sec == 'I':
            if i in (2, 3):
                hats(t0, 16, 2)
            if i >= 4:
                hats(t0, 16)
                if i == 4:
                    drum(t0, (0,), CRASH, 112)
                if i < 7:
                    drum(t0, (0, 3, 6, 10), KICK, 116)
                    drum(t0, (4, 12), SNARE, 110)
                    if i % 2:
                        drum(t0, (15,), SYN, 90)
                else:
                    drum(t0, (0, 3, 6), KICK, 116)
                    drum(t0, (4,), SNARE, 110)
                    drum(t0, (8, 10, 12, 13, 14, 15), SNARE, 96)
            if i == 1:
                drum(t0, (0,), CRASH, 104)
                drum(t0, (0,), KICK, 120)
        elif sec in ('A', 'A2', 'D'):
            hats(t0, 16, metal=(7,) if sec == 'D' and i % 2 else ())
            if i == 0 or (sec == 'D' and i == 4):
                drum(t0, (0,), CRASH, 116)
            if not last:
                drum(t0, (0, 3, 6, 10), KICK, 118)
                drum(t0, (4, 12), SNARE, 112)
                if sec == 'D':
                    drum(t0, (12,), CLAP, 100)
                if i % 2:
                    drum(t0, (7, 15), SYN, 88)
            else:
                drum(t0, (0, 3, 6), KICK, 118)
                drum(t0, (4,), SNARE, 112)
                drum(t0, (8, 10), TOM_H, 108)
                drum(t0, (12, 13), TOM_H, 104)
                drum(t0, (14, 15), TOM_L, 112)
        elif sec == 'B':
            hats(t0, 14, 2, metal=(13,) if i % 2 else ())
            if i == 0:
                drum(t0, (0,), CRASH, 112)
            drum(t0, (0, 8), KICK, 118)
            drum(t0, (4, 11), SNARE, 110)
            if i % 2:
                drum(t0, (11,), CLAP, 96)
                drum(t0, (6, 13), SYN, 86)
        elif sec == 'C':
            hats(t0, 16, 4, acc=(80, 60, 70, 60), metal=(5, 11) if i % 2 == 0 else (9,))
            if i == 0:
                drum(t0, (0,), CRASH, 112)
            drum(t0, (0, 10), KICK, 116)
            drum(t0, (8,), SNARE, 112)
            if i in (3, 7):
                for k in range(8):                 # glitch-roffel in 32sten
                    s = t0 + 12 * S + k * T32
                    P['drums'].append([s, s + T32, SYN, 84 + 4 * k])
        elif sec == 'T':
            if i == 0:
                drum(t0, (0,), CRASH, 116)
                drum(t0, (0, 4, 8), KICK, 120)
                drum(t0, (12,), SNARE, 112)
                hats(t0, 14, 2)
            else:
                hats(t0, 8)
                drum(t0, (0, 3, 6), KICK, 118)
                drum(t0, (4,), SNARE, 110)
                for k in range(8, 16):
                    P['drums'].append([t0 + k * S, t0 + k * S + DLEN[SNARE], SNARE, 88 + 4 * (k - 8)])
    return P, X, CC, end, loop


LAYOUT = [  # (partij, programma, volume, kanaal, pan, bend-partij)  (v2, Jordi: lead minder aanwezig: 110 -> 80, stotters 92 -> 80, echo 36 -> 28)
    ('lead', GLASS, 80, 0, 64, 'lead'), ('stut', GLASS_S, 80, 1, 76, None), ('bass', BASS, 104, 2, 64, None),
    ('ep', EP, 72, 3, 52, None), ('choir1', CHOIR, 70, 4, 40, 'choir1'), ('choir2', CHOIR, 66, 5, 88, 'choir2'),
    ('swell', SWELL, 84, 6, 64, None),
    ('sq', SQ1, 40, 8, 36, None), ('echo', SQ2, 28, 10, 92, 'echo'), ('wave', WAVE, 56, 11, 64, None),
    ('hat', HAT, 40, 12, 64, None), ('metal', METAL, 30, 13, 64, None),
]
ORDER = ['lead', 'drums', 'bass', 'stut', 'swell', 'choir1', 'ep', 'choir2']
DRUMVOL = 108
ECHO_DETUNE = 0.3                 # halve toon: de PSG-echo net naast de lead


def voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm + overrides voor Battle! Ultra Beast (MUS_GROUNDED_VS_ULTRA_BEAST).'
    lines[1] = '@ Gegenereerd door tools/grounded/ub_theme.py. Eigen samples: ub_glass, ub_swell (ub_samples.py).'
    lines[2] = 'voice_group %s' % VG
    over = {
        4: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_detuned_ep1_low, 255, 188, 128, 165',
        38: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_synth_bass, 255, 252, 0, 115',
        52: 'voice_directsound 60, 0, DirectSoundWaveData_classical_choir_voice_ahhs, 255, 0, 255, 150',
        80: 'voice_square_1 60, 0, 0, 0, 0, 1, 7, 1',
        81: 'voice_square_2 60, 0, 1, 0, 1, 6, 2',
        82: 'voice_square_1_alt 60, 0, 47, 2, 0, 2, 6, 0',
        84: 'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_1, 0, 7, 15, 0',
        87: 'voice_directsound 60, 0, DirectSoundWaveData_ub_glass, 255, 200, 160, 120',
        88: 'voice_directsound 60, 0, DirectSoundWaveData_ub_glass, 255, 220, 210, 190',
        89: 'voice_directsound 60, 0, DirectSoundWaveData_ub_swell, 255, 0, 255, 120',
        120: 'voice_noise_alt 60, 0, 0, 0, 1, 0, 0',
        121: 'voice_noise_alt 60, 0, 1, 0, 1, 0, 0',
        127: 'voice_keysplit_all voicegroup_ub_drumset',
    }
    out = []
    for l in lines:
        for k, v in over.items():
            if l.rstrip().endswith('@ %d' % k):
                l = '\t%s  @ %d' % (v, k)
        out.append(l)
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    kit = [
        ('36 kick', 'voice_directsound 62, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 160'),
        ('37 snare', 'voice_directsound 62, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 170'),
        ('38 synthsnare', 'voice_directsound 66, 64, DirectSoundWaveData_unknown_synth_snare, 255, 226, 0, 120'),
        ('39 clap', 'voice_directsound 60, 64, DirectSoundWaveData_sc88pro_tr909_hand_clap, 255, 0, 255, 170'),
        ('40 crash', 'voice_directsound 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165'),
        ('41 tom laag', 'voice_directsound 50, 52, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 150'),
        ('42 tom hoog', 'voice_directsound 58, 76, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 150'),
    ]
    open('sound/voicegroups/drumsets/ub.inc', 'w').write(
        '@ Project Grounded: drumkit voor ub_theme.py (Battle! Ultra Beast). Alleen stock-samples, geen PSG.\n'
        '@ ' + ', '.join(n for n, _ in kit) + '.\n'
        '@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.\n'
        'voice_group ub_drumset, 36\n' + ''.join('\t%s\n' % v for _, v in kit))


def build(refdir=None):
    P, X, CC, end, lp = compose()
    for k in list(P):
        P[k] = dedupe(P[k])
    progs = {k: pr for k, pr, *_ in LAYOUT}
    rel = releases(VG)
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) + 2 for k, pr in progs.items()}
    for k, pr in progs.items():
        if rel.get(pr) is not None and k not in ('swell', 'ep', 'lead'):
            P[k] = detach(P[k], tail[k])
    for k, pr in progs.items():
        if rel.get(pr) is not None:
            low = [n for _, _, n, _ in P[k] if n < 31]
            assert not low, '%s: DirectSound-noten onder G1: %s' % (k, low[:5])
            soft = [v for _, _, _, v in P[k] if v < 76]
            assert not soft, '%s: zachte DS-noten (8-bit-fuzz) %s' % (k, soft[:5])
    tail['drums'] = 0
    ds = {k: P[k] for k in ORDER}
    kept = allocate(ds, ORDER, tail, drum_len=None, max_voices=MAXV)
    # drums: echte lengte (DLEN) staat al in de noten; release van de kit telt erbij via tail 0 (korte releases)
    for k in ORDER:
        n = len(ds[k])
        if n and len(kept[k]) < n:
            print('  %s: %d van %d noten vallen weg (%.1f%%)' % (k, n - len(kept[k]), n, 100 * (n - len(kept[k])) / n))
            if os.environ.get('UB_DEBUG'):
                kk = {tuple(e) for e in kept[k]}
                print('     weg op tick:', [e[0] for e in ds[k] if tuple(e) not in kk][:24])
        P[k] = kept[k]
    for ref in (False, True):
        if ref and not refdir:
            continue
        song = Song(TPB, 500000)
        song.tempo(0, BPM / 120)
        song.loop = (lp, end)
        for k, pr, vol, ch, pan, bp in LAYOUT:
            extra = []
            if bp or k == 'echo':
                extra.append((0, mido.Message('control_change', control=20, value=BEND)))
            if k == 'echo':
                extra.append((0, mido.Message('pitchwheel', pitch=pw(ECHO_DETUNE))))
            elif bp:
                extra.append((0, mido.Message('pitchwheel', pitch=0)))
                extra += [(t, mido.Message('pitchwheel', pitch=v)) for t, v in sorted(X[bp]) if t > 0]
            prg = pr if not ref else {GLASS: 98, GLASS_S: 98, SWELL: 94, EP: 4, CHOIR: 52, BASS: 38}.get(pr, 80)
            ccs = [] if ref else list(CC.get(k, []))
            song.add(P[k], prg, vol, ch, pan, extra=extra, ccs=ccs)
        drums = sorted(P['drums'])
        if ref:
            gm = {KICK: 36, SNARE: 38, SYN: 40, CLAP: 39, CRASH: 49, TOM_L: 41, TOM_H: 48}
            drums = [[s, e, gm[n], v] for s, e, n, v in drums]
        song.add(drums, KIT if not ref else 0, DRUMVOL, 9)
        written = {k for k, *_ in LAYOUT} | {'drums'}
        assert not [k for k in P if P[k] and k not in written], [k for k in P if P[k] and k not in written]
        out = os.path.join(refdir, 'ub_ref.mid') if ref else OUT
        song.save(out, end)
        if not ref:
            sec = 60 / BPM / TPB
            print(out, '| intro %.1f s | loop %.1f s | totaal %.1f s' % (lp * sec, (end - lp) * sec, end * sec))


if __name__ == '__main__':
    ref = sys.argv[sys.argv.index('--ref') + 1] if '--ref' in sys.argv else None
    voicegroup()
    build(ref)
