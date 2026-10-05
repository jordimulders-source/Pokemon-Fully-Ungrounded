#!/usr/bin/env python3
"""Project Grounded: "Battle! Shaymin", een eigen compositie. Shaymin vecht in het Gracidea-veld van Flower Paradise
(post-game, Bloom Ticket).

v1: "een hele relaxte, dwarrelende bloemenweide-achtig nummer" (6/8, gestippelde kwart 88).
v2 (Jordi: "qua thema uitstekend, maar lijkt meer een route-theme dan een battle-theme"): dezelfde melodieën,
instrumenten en bloemenweide, maar als gevechtsnummer: gestippelde kwart 112 (kwart 168, jig-drive), een lichte maar
doorlopende ritmesectie (zachte bassdrum, snare-roffels, toms, tamboerijn, bongo's), een bas-ostinato in achtsten
(contrabas), strijkers-spiccato onder de melodie, een intro-stoot en een B-deel met opbouw.

6/8, D-groot. 1 maat = 1,07 s.
  maat 0-3   intro-stoot: drie tutti-stoten D - C/D - Bb/D (fluit + klarinet in drieklanken, harp-glissando's, toms),
             dan A7sus-A7 met een snareroffel die aanzwelt (= de laatste loopmaat)
Loop (48 maten, ±51 s):
  A  4-19    de hook op de fluit (twee keer 8 maten); bas-ostinato, spiccato, harp-arpeggio's, bassdrum op 1 en snare
             op 4, bongo's; tweede keer met een klarinet-tegenstem en een crash
  B  20-31   Bm met spanning: half-time (bassdrum op 1, toms als hartslag), klarinet zingt, gitaar tokkelt, F#7;
             maat 28-31 opbouw: fluit neemt over, snare 8sten -> 16den, spiccato-tremolo, harp-glissando's
  C  32-43   'dwarrelen': dalende fluitfiguren, celesta-blaadjes, A/G en Gm6; lichter (geen snare), maar de bas en de
             bongo's lopen door; maat 42-43 roffel naar A'
  A' 44-51   de hook groter: crash, fluit + klarinet in decimes, celesta een octaaf hoger, volle drums -> maat 4

Voicegroup grounded_shaymin (gegenereerd) = grounded_gm met eigen samples uit FluidR3 (gm_samples.py en
shaymin_samples.py): 8 celesta, 24 nylon, 32 contrabas, 45 pizzicato, 46 harp, 48 zachte strijkers (pad),
49 spiccato-strijkers, 71 klarinet, 73 fluit, 121 shaker (PSG-ruis), 127 eigen kit (drumsets/shaymin.inc).
Max. 11 DirectSound-noten tegelijk (legendary; stemverdeler). Zie tools/grounded/MUZIEK.md.
Gebruik: python3 tools/grounded/shaymin_samples.py (eenmalig) en python3 tools/grounded/shaymin_theme.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

OUT = 'sound/songs/midi/mus_grounded_vs_shaymin.mid'
VG = 'grounded_shaymin'
TPB, BPM = 48, 168             # kwart = 168 -> gestippelde kwart = 112
E = TPB // 2                   # een achtste
S16 = TPB // 4
BAR = 6 * E                    # 6/8
MAX_VOICES = 11                # legendary
CELESTA, NYLON, UPRIGHT, PIZZ, HARP, PAD, SPICC, CLARINET, FLUTE, SHAKER, DRUMS = 8, 24, 32, 45, 46, 48, 49, 71, 73, 121, 127
# eigen kit (drumsets/shaymin.inc)
TRI, TRI_MUTE, BONGO_HI, BONGO_LO, KICK, SNARE, TAMB, CRASH, TOM_LO, TOM_HI = range(36, 46)
KIT_REL = {'tri': 200, 'bongo': 80, 'kick': 120, 'snare': 110, 'tamb': 100, 'crash': 165, 'toms': 120}

A0, B0, C0, R0, END = 4, 20, 32, 44, 52

N = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8,
     'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def p(name):
    """'A4' -> midi-noot (C4 = 60)."""
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


# akkoord: (bas, tonen); de eerste toon is de grondtoon
CH = {'Dmaj7': (2, [2, 6, 9, 1]), 'Gmaj7': (7, [7, 11, 2, 6]), 'D/F#': (6, [2, 6, 9, 1]), 'Bm7': (11, [11, 2, 6, 9]),
      'Em7': (4, [4, 7, 11, 2]), 'F#m7': (6, [6, 9, 1, 4]), 'A7sus': (9, [9, 2, 4, 7]), 'A7': (9, [9, 1, 4, 7]),
      'A': (9, [9, 1, 4]), 'F#7': (6, [6, 10, 1, 4]), 'A/G': (7, [9, 1, 4, 11]), 'Gm6': (7, [7, 10, 2, 4]),
      'D/A': (9, [2, 6, 9, 1]), 'D': (2, [2, 6, 9]), 'C/D': (2, [0, 4, 7]), 'Bb/D': (2, [10, 2, 5])}
A1 = ['Dmaj7', 'Gmaj7', 'D/F#', 'Gmaj7', 'Em7', 'F#m7', 'Gmaj7', ('A7sus', 'A7')]
A2 = ['Dmaj7', 'Gmaj7', 'D/F#', 'Gmaj7', 'Em7', 'A7', 'Dmaj7', ('Dmaj7', 'F#7')]
B = ['Bm7', 'Gmaj7', 'Dmaj7', 'F#7', 'Bm7', 'Gmaj7', 'Em7', 'A7', 'Gmaj7', 'F#m7', 'Em7', ('A7sus', 'A7')]
C = ['Gmaj7', 'A/G', 'F#m7', 'Bm7', 'Em7', 'A/G', 'Dmaj7', 'Dmaj7', 'Gmaj7', 'Gm6', 'D/A', ('A7sus', 'A7')]
PROG = ['D', 'C/D', 'Bb/D', ('A7sus', 'A7')] + A1 + A2 + B + C + A1
assert len(PROG) == END


def halves(b):
    """Akkoord per halve maat (gestippelde kwart)."""
    c = PROG[b]
    return (c, c) if isinstance(c, str) else c


def section(b):
    return 'intro' if b < A0 else 'A' if b < B0 else 'B' if b < C0 else 'C' if b < R0 else 'R'


SCALE = [2, 4, 6, 7, 9, 11, 1]          # D-groot


def third_below(n):
    """Diatonische terts onder n (D-groot)."""
    lo = next(n - d for d in range(1, 6) if (n - d) % 12 in SCALE)
    return next(lo - d for d in range(1, 6) if (lo - d) % 12 in SCALE)


def mel(pattern, bar, vel=112, shift=0, gap=4):
    """[(achtste, lengte in achtsten, 'A5'), ...] -> zingende noten (legato, met een klein ademgaatje)."""
    out = []
    for st, ln, nm in pattern:
        s = bar * BAR + st * E
        out.append([s, s + ln * E - gap, p(nm) + shift, vel + (6 if st in (0, 3) else 0)])
    return out


# ---- melodieën -----------------------------------------------------------------------------------------------------
INTRO_FLUTE = [   # de stoot: drieklanken omhoog op D, C/D, Bb/D; dan A7sus -> de hook
    [(0, 2, 'A5'), (2, 1, 'D6'), (3, 3, 'F#6')],
    [(0, 2, 'G5'), (2, 1, 'C6'), (3, 3, 'E6')],
    [(0, 2, 'F5'), (2, 1, 'Bb5'), (3, 3, 'D6')],
    [(0, 3, 'D6'), (3, 3, 'C#6')],
]
INTRO_CLAR = [
    [(0, 2, 'D5'), (2, 1, 'F#5'), (3, 3, 'A5')],
    [(0, 2, 'C5'), (2, 1, 'E5'), (3, 3, 'G5')],
    [(0, 2, 'Bb4'), (2, 1, 'D5'), (3, 3, 'F5')],
    [(0, 3, 'A4'), (3, 3, 'G4')],
]
HOOK = [   # A: 8 maten (fluit)
    [(0, 3, 'A5'), (3, 1, 'F#5'), (4, 1, 'E5'), (5, 1, 'F#5')],
    [(0, 3, 'D6'), (3, 2, 'B5'), (5, 1, 'A5')],
    [(0, 4, 'A5'), (4, 1, 'F#5'), (5, 1, 'A5')],
    [(0, 5, 'F#5')],                                                        # (celesta-blaadjes in het gat)
    [(0, 1, 'E5'), (1, 1, 'F#5'), (2, 1, 'G5'), (3, 3, 'B5')],
    [(0, 2, 'A5'), (2, 1, 'G5'), (3, 3, 'F#5')],
    [(0, 1, 'E5'), (1, 1, 'F#5'), (2, 1, 'G5'), (3, 2, 'D6'), (5, 1, 'C#6')],
    [(0, 2, 'B5'), (2, 1, 'A5'), (3, 3, 'E5')],                             # E5 -> A5 van maat 1
]
HOOK2_END = [   # tweede keer, maat 5-8: naar de tonica, dan de klarinet-opmaat naar B
    [(0, 1, 'E5'), (1, 1, 'F#5'), (2, 1, 'G5'), (3, 2, 'B5'), (5, 1, 'A5')],
    [(0, 2, 'G5'), (2, 1, 'F#5'), (3, 3, 'E5')],
    [(0, 3, 'F#5'), (3, 1, 'E5'), (4, 2, 'D5')],
    [],
]
B_CLAR = [   # B, maat 1-8: klarinet
    [(0, 3, 'F#4'), (3, 1, 'A4'), (4, 1, 'B4'), (5, 1, 'C#5')],
    [(0, 3, 'D5'), (3, 3, 'B4')],
    [(0, 2, 'A4'), (2, 1, 'F#4'), (3, 3, 'A4')],
    [(0, 5, 'E4')],
    [(0, 3, 'F#4'), (3, 1, 'A4'), (4, 1, 'B4'), (5, 1, 'D5')],
    [(0, 3, 'E5'), (3, 2, 'D5'), (5, 1, 'B4')],
    [(0, 3, 'G4'), (3, 2, 'B4'), (5, 1, 'A4')],
    [(0, 3, 'A4'), (3, 3, 'G4')],
]
B_FLUTE = [   # B, maat 9-12: de fluit neemt het over
    [(0, 3, 'B5'), (3, 1, 'A5'), (4, 1, 'G5'), (5, 1, 'F#5')],
    [(0, 3, 'A5'), (3, 1, 'G5'), (4, 1, 'F#5'), (5, 1, 'E5')],
    [(0, 3, 'G5'), (3, 3, 'B5')],
    [(0, 3, 'A5'), (3, 3, 'E5')],
]
B_ECHO = {3: [(3, 1, 'E6'), (4, 1, 'C#6'), (5, 1, 'A#5')],                 # fluit-echo (F#7: A#)
          7: [(3, 1, 'D6'), (4, 1, 'C#6'), (5, 1, 'A5')]}
C_FLUTE = [   # C: dalende 'dwarrel'-figuren
    [(0, 1, 'D6'), (1, 1, 'B5'), (2, 1, 'F#5'), (3, 3, 'A5')],
    [(0, 1, 'C#6'), (1, 1, 'A5'), (2, 1, 'E5'), (3, 2, 'B5'), (5, 1, 'A5')],
    [(0, 1, 'C#6'), (1, 1, 'A5'), (2, 1, 'F#5'), (3, 2, 'E5'), (5, 1, 'F#5')],
    [(0, 3, 'D5'), (3, 3, 'F#5')],
    [(0, 1, 'B5'), (1, 1, 'G5'), (2, 1, 'E5'), (3, 3, 'F#5')],
    [(0, 1, 'C#6'), (1, 1, 'B5'), (2, 1, 'A5'), (3, 3, 'E5')],
    [(0, 3, 'F#5'), (3, 3, 'A5')],
    [(0, 5, 'C#6')],
    [(0, 1, 'B5'), (1, 1, 'A5'), (2, 1, 'G5'), (3, 3, 'D6')],
    [(0, 3, 'Bb5'), (3, 2, 'G5'), (5, 1, 'E5')],
    [(0, 3, 'F#5'), (3, 3, 'A5')],
    [(0, 3, 'G5'), (3, 3, 'E5')],
]


def near(pc, lo, hi):
    n = pc
    while n < lo:
        n += 12
    return n if n <= hi else n - 12


def bass_note(pc):
    """Grondtoon tussen D2 (38) en C#3 (49)."""
    return near(pc, 38, 49)


def build():
    names = ('flute', 'clar', 'bass', 'pizz', 'spicc', 'harp', 'celesta', 'guitar', 'pad',
             'kick', 'snare', 'toms', 'crash', 'tamb', 'bongo', 'tri', 'shaker')
    parts = {k: [] for k in names}

    def hit(part, bar, e8, note, vel, ln=S16):
        s = bar * BAR + int(round(e8 * E))
        parts[part].append([s, s + ln, note, vel])

    def petals(bar, e8, chord, top=88, n=6, vel=78):
        """Celesta-blaadjes: dalende 16en over de akkoordtonen, vanaf ±E6-E7."""
        tones = sorted({near(pc, top - 11, top) for pc in CH[chord][1]}, reverse=True)
        seq = (tones + [t - 12 for t in tones])[:n]
        for k, nt in enumerate(seq):
            hit('celesta', bar, e8 + k * 0.5, nt, vel - k * 5, S16)

    def gliss(bar, e8, chord, lo, n, vel=64, step=0.5):
        """Harp-glissando omhoog over de akkoordtonen."""
        tones = sorted({near(pc, lo, lo + 11) + 12 * o for pc in CH[chord][1] for o in range(3)})
        for k, nt in enumerate(tones[:n]):
            hit('harp', bar, e8 + k * step, nt, vel + k * 3, E)

    def roll(bar, e0, e1, v0, v1, step=0.5):
        """Snareroffel van achtste e0 tot e1 (exclusief), velocity v0 -> v1."""
        k, n = 0, int((e1 - e0) / step)
        while k < n:
            hit('snare', bar, e0 + k * step, SNARE, v0 + (v1 - v0) * k // max(1, n - 1), S16)
            k += 1

    # ---- melodie -------------------------------------------------------------------------------------------------
    for i in range(4):
        parts['flute'] += mel(INTRO_FLUTE[i], i, 114)
        parts['clar'] += mel(INTRO_CLAR[i], i, 104)
    for i in range(8):
        parts['flute'] += mel(HOOK[i], A0 + i, 112)
        parts['flute'] += mel(HOOK[i] if i < 4 else HOOK2_END[i - 4], A0 + 8 + i, 112)
        parts['flute'] += mel(HOOK[i], R0 + i, 118)
        if i < 4:                                                       # A': klarinet een decime lager
            parts['clar'] += [[s, e, third_below(n) - 12, v - 14] for s, e, n, v in mel(HOOK[i], R0 + i, 114)]
            # en de celesta een octaaf hoger (glinstering op de grote terugkeer)
            parts['celesta'] += [[s, min(e, s + E), n + 12, v - 40] for s, e, n, v in mel(HOOK[i], R0 + i, 112)]
    parts['clar'] += mel([(4, 1, 'C#4'), (5, 1, 'E4')], A0 + 15, 100)  # opmaat naar B
    for i, pat in enumerate(B_CLAR):
        parts['clar'] += mel(pat, B0 + i, 110)
    for i, pat in B_ECHO.items():
        parts['flute'] += mel(pat, B0 + i, 92)
    for i, pat in enumerate(B_FLUTE):
        parts['flute'] += mel(pat, B0 + 8 + i, 112 + 3 * i)              # crescendo
        parts['clar'] += [[s, e, third_below(n) - 12, v - 14] for s, e, n, v in mel(pat, B0 + 8 + i, 112 + 3 * i)]
    for i, pat in enumerate(C_FLUTE):
        parts['flute'] += mel(pat, C0 + i, 110)

    # klarinet-tegenstem (gidstonen: terts/septiem, per halve maat) in A2, C en A' maat 5-8
    prev = 66
    for b in list(range(A0 + 8, A0 + 15)) + list(range(C0, R0)) + list(range(R0 + 4, END)):
        h = halves(b)
        for k, ch in enumerate(h if h[0] != h[1] else h[:1]):
            tones = CH[ch][1]
            cands = [near(tones[1], 58, 70), near(tones[-1], 58, 70)]
            nt = min(cands, key=lambda n: abs(n - prev))
            prev = nt
            ln = 6 if h[0] == h[1] else 3
            s = b * BAR + k * 3 * E
            parts['clar'].append([s, s + ln * E - 6, nt, 86])

    # ---- begeleiding ---------------------------------------------------------------------------------------------
    for b in range(END):
        h = halves(b)
        sec = section(b)
        build_up = B0 + 8 <= b < C0                                     # B maat 9-12: opbouw
        # -- bas-ostinato (contrabas) in achtsten: grondtoon - akkoordtoon - octaaf; in B donkerder (R R 5)
        stab = b < 2
        for half in range(2):
            bass, tones = CH[h[half]]
            r = bass_note(bass)
            up = [r + d for d in range(5, 10) if (r + d) % 12 in tones] or [r + 7]
            if stab:                                                    # intro-stoot: alleen op de stoten
                hit('bass', b, half * 3, r, 120, 2 * E)
                continue
            fig = [r, r, up[0]] if sec == 'B' and not build_up else [r, up[0], r + 12]
            for k, nt in enumerate(fig):
                hit('bass', b, half * 3 + k, nt, (118 if k == 0 else 92) + (6 if half == 0 and k == 0 else 0), E - 11)
        # -- spiccato-strijkers: achtsten op twee akkoordtonen (hoog-laag-hoog), in de opbouw tremolo in 16den
        if b >= 2:
            for half in range(2):
                tones = CH[h[half]][1]
                t = sorted({near(pc, 57, 68) for pc in tones[1:3]})
                if len(t) < 2:
                    t = [t[0] - 12 if t[0] > 62 else t[0], t[0] + (0 if t[0] > 62 else 12)]
                lo, hi = t[0], t[-1]
                base_v = {'intro': 72, 'A': 78, 'B': 74, 'C': 84, 'R': 86}[sec]
                spk = 'pizz' if sec == 'C' else 'spicc'      # C: lichter, getokkeld
                if (build_up and b >= C0 - 2) or b == A0 - 1 or b == R0 - 1:
                    for k in range(6):
                        hit(spk, b, half * 3 + k * 0.5, hi if k % 2 == 0 else lo,
                            base_v - 10 + 4 * (half * 6 + k) // 2, S16 - 2)
                else:
                    for k, nt in enumerate((hi, lo, hi)):
                        hit(spk, b, half * 3 + k, nt, base_v + (10 if k == 0 else 0), E - 10)
        # -- pizzicato: de stoten in de intro + accenten in C (octaaf boven de bas, op 1 en 4)
        if b < 3:
            for half in range(2):
                hit('pizz', b, half * 3, bass_note(CH[h[half]][0]) + 12, 104, E - 10)
        # -- harp: glissando's bij de stoten, arpeggio's in A/C/A', in B glissando's elke 4 maten / elke maat in de opbouw
        if b < 3:
            gliss(b, 0.5, h[0], 62, 5, 70, 0.5)
        elif sec == 'B':
            if (b - B0) % 4 == 0 or build_up:
                gliss(b, 0 if not build_up else 3, h[0] if not build_up else h[1], 62, 6, 64 + 2 * (b - B0 - 8) if build_up else 64)
        else:
            for half in range(2):
                bass, tones = CH[h[half]]
                base = near(tones[0], 50 if sec != 'C' else 57, 61 if sec != 'C' else 68)
                up = sorted({base + ((pc - base) % 12) for pc in tones} | {base + 12})
                fig = [up[0], up[1], up[2]] if half == 0 else [up[3], up[2], up[1]] if len(up) > 3 else [up[2], up[1], up[0]]
                if sec == 'C' and half == 1:
                    fig = [up[3] + 12 if len(up) > 3 else up[2] + 12, up[2] + 12 if len(up) > 3 else up[1] + 12, up[3] if len(up) > 3 else up[2]]
                for k, nt in enumerate(fig):
                    hit('harp', b, half * 3 + k, nt, (82 if k == 0 else 68) + (6 if sec == 'R' else 0), E - 8)
        # -- gitaar: tokkelen in B (achtsten)
        if sec == 'B' and not build_up:
            bass, tones = CH[h[0]]
            t = sorted({near(pc, 55, 66) for pc in tones})
            for k, idx in enumerate((0, 1, 2, 1, 2, 1) if len(t) < 4 else (0, 2, 3, 1, 3, 2)):
                hit('guitar', b, k, t[idx], 74 if k in (0, 3) else 62, E - 12)
        # -- strijkerspad: in B (spanning, zwelt aan in de opbouw) en C (per maat); intro maat 3 zwelt aan
        if sec in ('B', 'C') or b == A0 - 1:
            tones = CH[h[0]][1]
            counter = C0 <= b < R0
            for pc in ((tones[2],) if counter else (tones[1],)):
                for half in range(1 if sec == 'C' else 2):
                    v = 58 + (4 * (b - B0 - 8) + 2 * half if build_up else 0) + (8 if b == A0 - 1 else 0)
                    hit('pad', b, half * 3, near(pc, 57, 68), v, 3 * E - 14)

    # ---- celesta-blaadjes ------------------------------------------------------------------------------------------
    petals(0, 3, 'D', 93, 4, 70)
    petals(1, 3, 'C/D', 91, 4, 70)
    petals(3, 2, 'A7', 93, 8, 80)                                       # de grote val naar de hook
    for base in (A0, A0 + 8, R0):
        petals(base + 3, 3, 'Gmaj7', 91)
        petals(base + 7, 4, halves(base + 7)[1], 88, 4, 70)
    petals(A0 + 15, 3, 'Dmaj7', 93)
    for b in (B0 + 3, B0 + 7):
        petals(b, 0, halves(b)[0], 90, 4, 66)
    for i in range(12):                                                 # C: elke maat dwarrelt er een blaadje
        b = C0 + i
        ch = halves(b)[1]
        if i in (3, 7):
            petals(b, 3, ch, 93, 6, 80)
        elif i < 10:
            petals(b, 4, ch, 90 if i % 2 else 86, 3, 64)

    # ---- ritmesectie -----------------------------------------------------------------------------------------------
    for b in range(END):
        sec = section(b)
        build_up = B0 + 8 <= b < C0
        half_time = sec == 'B' and not build_up
        # crash op de grote inzetten
        if b in (0, A0, A0 + 8, C0, R0, R0 + 4):
            hit('crash', b, 0, CRASH, 100 if b in (0, A0, R0) else 84, 3 * E)
        # intro-stoten
        if b < 2:
            for e8 in (0, 3):
                hit('kick', b, e8, KICK, 120)
                hit('toms', b, e8, TOM_LO, 104)
            hit('toms', b, 4, TOM_HI, 86)
            hit('toms', b, 5, TOM_HI, 96)
            continue
        if b == 2:                                                      # derde stoot, dan roffel
            hit('kick', b, 0, KICK, 120)
            hit('toms', b, 0, TOM_LO, 104)
            hit('kick', b, 3, KICK, 110)
            roll(b, 3, 6, 62, 92, 1)
            continue
        if b == A0 - 1:                                                 # A7sus-A7: roffel zwelt aan (= maat 51)
            hit('kick', b, 0, KICK, 110)
            hit('kick', b, 3, KICK, 104)
            roll(b, 0, 6, 54, 104)
            continue
        # bassdrum
        hit('kick', b, 0, KICK, 116)
        if not half_time:
            if sec != 'C' or b % 2:
                hit('kick', b, 3, KICK, 96)
            if sec in ('A', 'R') and b % 2 == 1:
                hit('kick', b, 5, KICK, 80)
        # snare op 4 (A, A'), in B half-time toms als hartslag
        if sec in ('A', 'R') and b not in (A0 + 7, A0 + 15, END - 1):
            hit('snare', b, 3, SNARE, 84 if sec == 'R' else 74)
            if sec == 'R':
                hit('snare', b, 5, SNARE, 46)                            # ghostnoot
        if half_time:
            hit('toms', b, 3, TOM_LO, 72)
            hit('toms', b, 4, TOM_LO, 60)
            if (b - B0) % 4 == 3:
                for k, nt in enumerate((TOM_HI, TOM_HI, TOM_LO, TOM_LO)):
                    hit('toms', b, 4 + k * 0.5, nt, 70 + 6 * k)
        # fills op de frasegrenzen
        if b in (A0 + 7, R0 + 3):
            roll(b, 3, 6, 60, 88)
        if b == A0 + 15:                                                # naar B: toms
            for k, nt in enumerate((TOM_HI, TOM_HI, TOM_LO, TOM_LO, TOM_LO, TOM_LO)):
                hit('toms', b, 3 + k * 0.5, nt, 76 + 5 * k)
        if build_up:                                                    # opbouw: 8sten -> 16den
            i = b - (B0 + 8)
            if i == 0:
                roll(b, 3, 6, 50, 64, 1)
            elif i == 1:
                roll(b, 0, 6, 54, 72, 1)
            elif i == 2:
                roll(b, 0, 3, 60, 72, 1)
                roll(b, 3, 6, 72, 88)
            else:
                roll(b, 0, 6, 76, 112)
                hit('toms', b, 5, TOM_LO, 100)
        if b == R0 - 2:
            roll(b, 3, 6, 50, 66, 1)
        if b == R0 - 1:
            roll(b, 0, 6, 60, 106)
        if b == END - 1:                                                # = maat 3: roffel terug naar de hook
            roll(b, 0, 6, 54, 104)
        # tamboerijn: op 4 in A, op de achtsten 2 en 5 in A', op 4 in C
        if sec in ('A', 'C'):
            hit('tamb', b, 3, TAMB, 70)
        elif sec == 'R':
            hit('tamb', b, 2, TAMB, 66)
            hit('tamb', b, 5, TAMB, 74)
        # bongo's lopen door (tussen bassdrum en snare)
        for e8, nt, v in ((1, BONGO_HI, 64), (2, BONGO_HI, 56), (4, BONGO_LO, 70), (5, BONGO_HI, 58)):
            if sec == 'C' or half_time or e8 != 5 or b % 2 == 0:
                hit('bongo', b, e8, nt, v + (6 if sec == 'R' else 0))
        if sec == 'C':
            hit('bongo', b, 5.5, BONGO_HI, 50)
        # triangel op de frasegrenzen
        if (b in (A0, A0 + 8, B0, C0, R0) or (sec == "C" and b % 2 == 0)) and b not in (A0, A0 + 8, C0, R0, R0 + 4):
            hit('tri', b, 0, TRI, 70, E)
    for b in range(2, END):                                             # shaker (PSG-ruis) in achtsten
        for e8 in range(6):
            v = 72 if e8 in (0, 3) else 46
            hit('shaker', b, e8, 84, v, 8)
            if section(b) in ('C', 'R') and e8 in (2, 5):
                hit('shaker', b, e8 + 0.5, 84, 34, 6)

    for k in parts:                                                     # niets over de loopgrens
        parts[k] = dedupe([[s, min(e, END * BAR), n, v] for s, e, n, v in parts[k] if s < END * BAR])

    write_voicegroup()
    rel = releases(VG)
    progs = {'flute': FLUTE, 'clar': CLARINET, 'bass': UPRIGHT, 'pizz': PIZZ, 'spicc': SPICC, 'harp': HARP,
             'celesta': CELESTA, 'guitar': NYLON, 'pad': PAD}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) for k, pr in progs.items()}
    for k in ('kick', 'snare', 'toms', 'crash', 'tamb', 'bongo', 'tri'):
        tail[k] = release_ticks(KIT_REL['bongo' if k == 'bongo' else k], TPB, BPM)
    for k in ('flute', 'clar', 'pad'):
        parts[k] = detach(parts[k], tail[k])
    # harp wijkt vooraf voor de celesta-blaadjes (anders vallen er willekeurig blaadjes of arpeggionoten weg)
    cel = [(s0 - S16, e0 + S16) for s0, e0, _, _ in parts['celesta']]
    parts['harp'] = [g for g in parts['harp'] if not any(a <= g[0] < z for a, z in cel)]
    order = ['flute', 'kick', 'bass', 'snare', 'clar', 'crash', 'celesta', 'spicc', 'pizz', 'harp', 'bongo', 'toms',
             'tamb', 'pad', 'guitar', 'tri']
    ds = {k: parts[k] for k in order}
    kept = allocate(ds, order, tail, max_voices=MAX_VOICES)
    print('tail (ticks):', tail)
    for k in order:
        n = len(ds[k])
        lost = sorted({e[0] // BAR for e in ds[k] if e not in kept[k]})
        print('  %-8s %4d noten, %3d vallen weg (%.1f%%)' % (k, n, n - len(kept[k]), 100 * (n - len(kept[k])) / max(n, 1)),
              ('maten ' + ' '.join(map(str, lost))) if lost else '')
        parts[k] = kept[k]

    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.loop = (A0 * BAR, END * BAR)
    parts['kit'] = sorted(parts['kick'] + parts['snare'] + parts['toms'] + parts['crash'] + parts['tamb'])
    parts['perc'] = sorted(parts['bongo'] + parts['tri'])
    layout = [('flute', FLUTE, 118, 0, 70), ('clar', CLARINET, 100, 1, 50), ('harp', HARP, 90, 2, 82),
              ('celesta', CELESTA, 82, 3, 94), ('guitar', NYLON, 80, 4, 44), ('bass', UPRIGHT, 116, 5, 64),
              ('spicc', SPICC, 80, 6, 42), ('pad', PAD, 70, 8, 86), ('pizz', PIZZ, 92, 10, 60),
              ('kit', DRUMS, 104, 9, 64), ('perc', DRUMS, 84, 11, 78), ('shaker', SHAKER, 30, 7, 84)]
    for k, prog, vol, ch, pan in layout:
        song.add(parts[k], prog, vol, ch, pan)
    written = {k for k, *_ in layout} | {'kick', 'snare', 'toms', 'crash', 'tamb', 'bongo', 'tri'}
    assert not [k for k in parts if parts[k] and k not in written], 'partij niet weggeschreven'
    song.save(OUT, END * BAR)
    print(OUT, '%.1f s intro, %.1f s loop' % (A0 * BAR / TPB * 60 / BPM, (END - A0) * BAR / TPB * 60 / BPM))


def write_voicegroup():
    """grounded_gm + eigen samples, pizzicato, contrabas, zachte en spiccato-strijkers, shaker, kit."""
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Battle! Shaymin. Gegenereerd door tools/grounded/shaymin_theme.py.'
    lines[1] = ('@ 8 celesta, 24 nylon, 32 contrabas, 45 pizzicato, 46 harp, 48 zachte strijkers, 49 spiccato, '
                '71 klarinet, 73 fluit, 121 shaker, 127 kit.')
    lines[2] = 'voice_group %s' % VG
    repl = {
        '@ 8': '\tvoice_directsound 60, 0, DirectSoundWaveData_shaymin_celesta, 255, 0, 255, 180  @ 8',
        '@ 24': '\tvoice_directsound 60, 0, DirectSoundWaveData_shaymin_nylon, 255, 0, 255, 160  @ 24',
        '@ 32': '\tvoice_directsound 60, 0, DirectSoundWaveData_shaymin_upright, 255, 0, 255, 130  @ 32',
        '@ 45': '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_pizzicato_strings, 255, 226, 0, 150  @ 45',
        '@ 46': '\tvoice_directsound 60, 0, DirectSoundWaveData_shaymin_harp, 255, 0, 255, 180  @ 46',
        '@ 48': '\tvoice_keysplit voicegroup_shaymin_strings_keysplit, keysplit_strings  @ 48',
        '@ 49': '\tvoice_keysplit voicegroup_shaymin_spicc_keysplit, keysplit_strings  @ 49',
        '@ 71': '\tvoice_directsound 60, 0, DirectSoundWaveData_shaymin_clarinet, 255, 0, 255, 170  @ 71',
        '@ 73': '\tvoice_directsound 60, 0, DirectSoundWaveData_shaymin_flute, 255, 0, 255, 175  @ 73',
        '@ 121': '\tvoice_noise_alt 60, 0, 0, 0, 1, 0, 0  @ 121',
        '@ 127': '\tvoice_keysplit_all voicegroup_shaymin_drumset  @ 127',
    }
    out = []
    for l in lines:
        tag = '@' + l.rsplit('@', 1)[1] if '@' in l and l.startswith('\t') else None
        out.append(repl.get(tag.strip() if tag else None, l))
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    open('sound/voicegroups/keysplits/shaymin_strings.inc', 'w').write(
        '@ Project Grounded: strijkers met een zachte aanzet (pad) voor Battle! Shaymin (shaymin_theme.py).\n'
        'voice_group shaymin_strings_keysplit\n'
        + ''.join('\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_string_ensemble_%d, 24, 0, 255, 200\n' % k
                  for k in (60, 72, 84)) + '\n')
    open('sound/voicegroups/keysplits/shaymin_spicc.inc', 'w').write(
        '@ Project Grounded: spiccato-strijkers (harde aanzet, kort) voor Battle! Shaymin (shaymin_theme.py).\n'
        'voice_group shaymin_spicc_keysplit\n'
        + ''.join('\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_string_ensemble_%d, 255, 210, 0, 130\n' % k
                  for k in (60, 72, 84)) + '\n')
    r = KIT_REL
    kit = [   # vanaf noot 36; alles DirectSound (geen PSG-piepjes)
        'voice_directsound_no_resample 60, 80, DirectSoundWaveData_sd90_open_triangle, 255, 0, 255, %d' % r['tri'],  # 36 triangel
        'voice_directsound_no_resample 60, 80, DirectSoundWaveData_sd90_open_triangle, 255, 0, 255, 60',      # 37 triangel kort
        'voice_directsound 60, 44, DirectSoundWaveData_kc_bongo_hi, 255, 0, 255, %d' % r['bongo'],            # 38 bongo hoog
        'voice_directsound 60, 52, DirectSoundWaveData_kc_bongo_lo, 255, 0, 255, %d' % r['bongo'],            # 39 bongo laag
        'voice_directsound 60, 64, DirectSoundWaveData_shaymin_kick, 255, 0, 255, %d' % r['kick'],            # 40 bassdrum
        'voice_directsound_no_resample 60, 70, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, %d' % r['snare'],  # 41 snare
        'voice_directsound_no_resample 64, 86, DirectSoundWaveData_sc88pro_tambourine, 255, 127, 77, %d' % r['tamb'],       # 42 tamboerijn
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 235, 0, %d' % r['crash'],  # 43 crash
        'voice_directsound 60, 56, DirectSoundWaveData_shaymin_tom_lo, 255, 0, 255, %d' % r['toms'],          # 44 tom laag
        'voice_directsound 60, 72, DirectSoundWaveData_shaymin_tom_hi, 255, 0, 255, %d' % r['toms'],          # 45 tom hoog
    ]
    open('sound/voicegroups/drumsets/shaymin.inc', 'w').write(
        '@ Project Grounded: kit voor Battle! Shaymin (shaymin_theme.py): 36 triangel, 37 triangel kort,\n'
        '@ 38/39 bongo hoog/laag, 40 bassdrum, 41 snare, 42 tamboerijn, 43 crash, 44/45 tom laag/hoog.\n'
        'voice_group shaymin_drumset, 36\n' + ''.join('\t%s\n' % k for k in kit) + '\n')


if __name__ == '__main__':
    build()
