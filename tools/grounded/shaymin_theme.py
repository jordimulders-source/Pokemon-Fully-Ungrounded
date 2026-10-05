#!/usr/bin/env python3
"""Project Grounded: "Battle! Shaymin", een eigen compositie. Jordi: "een hele relaxte, dwarrelende
bloemenweide-achtig nummer". Shaymin vecht in het Gracidea-veld van Flower Paradise (post-game, Bloom Ticket).

6/8, gestippelde kwart = 88 (kwart 132), D-groot met wat Lydisch/geleende kleur (A/G, Gm6). 1 maat = 1,36 s.
  maat 0-3   intro (±5,5 s, tijdens de bloemenwervel-transitie): harp-arpeggio's + celesta-blaadjes, strijkers
             zwellen aan, dan pizzicato-bas, gitaar en shaker; maat 3 = A7sus-A7 (= de laatste loopmaat)
Loop (48 maten, ±65 s):
  A  4-19    de hook op de fluit (twee keer 8 maten), harp-arpeggio's, nylon-gitaar op de 'en'-tellen, pizzicato-bas;
             tweede keer met een klarinet-tegenstem (gidstonen)
  B  20-31   Bm: de klarinet zingt, de gitaar tokkelt, pizzicato op de achtsten; bongo's erbij; laatste 4 maten
             neemt de fluit het over met de klarinet een decime lager
  C  32-43   'dwarrelen': dalende fluitfiguren, celesta-blaadjes elke maat, harp hoger, A/G en Gm6 (lente-weemoed)
  A' 44-51   de hook nog eens, fluit + klarinet in decimes -> naadloos terug naar maat 4
Lichte groove: pizzicato-bas op 1 en 4, gitaar op de 'en', shaker (PSG-ruis, kost geen kanaal) in achtsten,
triangel op de frasegrenzen, zachte bongo's in B/C/A'. Geen drumstel.

Voicegroup grounded_shaymin (gegenereerd) = grounded_gm met eigen samples uit FluidR3 (gm_samples.py):
8 = celesta, 24 = nylon-gitaar, 46 = harp, 71 = klarinet, 73 = fluit (beide met een exacte loop), 45 = pizzicato,
48 = strijkers met zachte aanzet (pad), 121 = shaker (ruis), 127 = eigen kit (drumsets/shaymin.inc: triangel, bongo's).
Max. 10 DirectSound-noten tegelijk (stemverdeler). Zie tools/grounded/MUZIEK.md.
Gebruik: python3 tools/grounded/shaymin_theme.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

OUT = 'sound/songs/midi/mus_grounded_vs_shaymin.mid'
VG = 'grounded_shaymin'
TPB, BPM = 48, 132             # kwart = 132 -> gestippelde kwart = 88
E = TPB // 2                   # een achtste
S16 = TPB // 4
BAR = 6 * E                    # 6/8
CELESTA, NYLON, PIZZ, HARP, PAD, CLARINET, FLUTE, SHAKER, DRUMS = 8, 24, 45, 46, 48, 71, 73, 121, 127
TRI, TRI_MUTE, BONGO_HI, BONGO_LO = 36, 37, 38, 39      # eigen kit (drumsets/shaymin.inc)

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
      'D/A': (9, [2, 6, 9, 1])}
A1 = ['Dmaj7', 'Gmaj7', 'D/F#', 'Gmaj7', 'Em7', 'F#m7', 'Gmaj7', ('A7sus', 'A7')]
A2 = ['Dmaj7', 'Gmaj7', 'D/F#', 'Gmaj7', 'Em7', 'A7', 'Dmaj7', ('Dmaj7', 'F#7')]
B = ['Bm7', 'Gmaj7', 'Dmaj7', 'A', 'Bm7', 'Gmaj7', 'Em7', 'A7', 'Gmaj7', 'F#m7', 'Em7', ('A7sus', 'A7')]
C = ['Gmaj7', 'A/G', 'F#m7', 'Bm7', 'Em7', 'A/G', 'Dmaj7', 'Dmaj7', 'Gmaj7', 'Gm6', 'D/A', ('A7sus', 'A7')]
PROG = ['Dmaj7', 'Gmaj7', 'Dmaj7', ('A7sus', 'A7')] + A1 + A2 + B + C + A1
assert len(PROG) == END


def halves(b):
    """Akkoord per halve maat (gestippelde kwart)."""
    c = PROG[b]
    return (c, c) if isinstance(c, str) else c


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
B_ECHO = {3: [(3, 1, 'E6'), (4, 1, 'C#6'), (5, 1, 'A5')],                  # fluit-echo in de lange klarinetnoten
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
    parts = {k: [] for k in ('flute', 'clar', 'bass', 'harp', 'celesta', 'guitar', 'pad', 'tri', 'perc', 'shaker')}

    def hit(part, bar, e8, note, vel, ln=S16):
        s = bar * BAR + int(e8 * E)
        parts[part].append([s, s + ln, note, vel])

    def petals(bar, e8, chord, top=88, n=6, vel=78):
        """Celesta-blaadjes: dalende 16en over de akkoordtonen, vanaf ±E6-E7."""
        tones = sorted({near(pc, top - 11, top) for pc in CH[chord][1]}, reverse=True)
        seq = (tones + [t - 12 for t in tones])[:n]
        for k, nt in enumerate(seq):
            hit('celesta', bar, e8 + k * 0.5, nt, vel - k * 5, S16)

    # ---- melodie -------------------------------------------------------------------------------------------------
    for i in range(8):
        parts['flute'] += mel(HOOK[i], A0 + i, 112)
        parts['flute'] += mel(HOOK[i] if i < 4 else HOOK2_END[i - 4], A0 + 8 + i, 112)
        parts['flute'] += mel(HOOK[i], R0 + i, 116)
        if i < 4:                                                       # A': klarinet een decime lager
            parts['clar'] += [[s, e, third_below(n) - 12, v - 14] for s, e, n, v in mel(HOOK[i], R0 + i, 112)]
    parts['clar'] += mel([(4, 1, 'C#4'), (5, 1, 'E4')], A0 + 15, 100)  # opmaat naar B
    for i, pat in enumerate(B_CLAR):
        parts['clar'] += mel(pat, B0 + i, 108)
    for i, pat in B_ECHO.items():
        parts['flute'] += mel(pat, B0 + i, 92)
    for i, pat in enumerate(B_FLUTE):
        parts['flute'] += mel(pat, B0 + 8 + i, 112)
        parts['clar'] += [[s, e, third_below(n) - 12, v - 14] for s, e, n, v in mel(pat, B0 + 8 + i, 112)]
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
            parts['clar'].append([s, s + ln * E - 6, nt, 84])

    # ---- harp, gitaar, bas, pad ----------------------------------------------------------------------------------
    for b in range(END):
        h = halves(b)
        sec = 'intro' if b < A0 else 'A' if b < B0 else 'B' if b < C0 else 'C' if b < R0 else 'R'
        # harp: arpeggio op en neer (intro, A, C, A'); in B alleen een glissando aan het begin van elke 4 maten
        if sec != 'B':
            for half in range(2):
                bass, tones = CH[h[half]]
                base = near(tones[0], 50 if sec != 'C' else 57, 61 if sec != 'C' else 68)
                up = sorted({base + ((pc - base) % 12) for pc in tones} | {base + 12})
                fig = [up[0], up[1], up[2]] if half == 0 else [up[3], up[2], up[1]] if len(up) > 3 else [up[2], up[1], up[0]]
                if sec == 'C' and half == 1:
                    fig = [up[3] + 12 if len(up) > 3 else up[2] + 12, up[2] + 12 if len(up) > 3 else up[1] + 12, up[3] if len(up) > 3 else up[2]]
                for k, nt in enumerate(fig):
                    hit('harp', b, half * 3 + k, nt, (84 if k == 0 else 72) - (10 if sec == 'intro' and b == 0 else 0), E + 4)
        elif (b - B0) % 4 == 0:
            tones = CH[h[0]][1]
            gl = sorted({near(pc, 62, 73) for pc in tones} | {near(pc, 74, 85) for pc in tones})[:6]
            for k, nt in enumerate(gl):
                hit('harp', b, k * 0.5, nt, 64 + k * 4, E)
        # gitaar: zachte 'en'-tellen (achtste 2-3 en 5-6, twee akkoordtonen na elkaar); in B tokkelen (achtsten)
        if b >= 2 and sec != 'C':                                       # C: harp + celesta dragen het
            if sec == 'B':
                bass, tones = CH[h[0]]
                t = sorted({near(pc, 55, 66) for pc in tones})
                for k, idx in enumerate((0, 1, 2, 1, 2, 1) if len(t) < 4 else (0, 2, 3, 1, 3, 2)):
                    hit('guitar', b, k, t[idx], 74 if k in (0, 3) else 62, E - 6)
            else:
                for half in range(2):
                    tones = CH[h[half]][1]
                    t = sorted({near(pc, 57, 68) for pc in tones[1:]})[:2]
                    for e8, nt in zip((1, 2), (t[-1], t[0])):
                        hit('guitar', b, half * 3 + e8, nt, 68 if e8 == 1 else 60, E - 4)
        # pizzicato-bas op 1 en 4 (vanaf maat 2); in B ook pizzicato in de middenligging op de achtsten 1, 2, 4, 5
        if b >= 2:
            for half in range(2):
                bass = CH[h[half]][0]
                nt = bass_note(bass)
                if half == 1 and h[0] == h[1]:
                    nt = near(bass + 7, 38, 49) if sec != 'C' or b not in (C0 + 6, C0 + 7) else bass_note(bass)
                hit('bass', b, half * 3, nt, 112 if half == 0 else 100, 2 * E)
            if sec == 'B':
                for half in range(2):
                    tones = CH[h[half]][1]
                    for e8, idx in ((2, 2),):
                        hit('bass', b, half * 3 + e8, near(tones[idx], 62, 73), 70, S16)
        # strijkerspad: terts + septiem, per maat (stopt een uitklinktijd vóór de volgende); speelt de klarinet de
        # gidstonen al, dan alleen de kwint/none
        if b >= 1 and not (A0 <= b < A0 + 4):
            tones = CH[h[0]][1]
            counter = A0 + 8 <= b < A0 + 15 or C0 <= b < R0 or b >= R0 + 4
            for pc in ((tones[2],) if counter else (tones[1], tones[-1])):
                for half in range(1 if sec == 'C' else 2):              # per halve maat: wiegt mee (C: 1e helft)
                    hit('pad', b, half * 3, near(pc, 57, 68), (60 if b > 1 else 46) - 6 * half, 3 * E - 14)

    # ---- celesta-blaadjes ------------------------------------------------------------------------------------------
    petals(0, 0, 'Dmaj7', 93, 6, 74)
    petals(0, 3, 'Dmaj7', 88, 6, 70)
    petals(1, 3, 'Gmaj7', 91, 6, 72)
    petals(2, 3, 'Dmaj7', 93, 6, 74)
    petals(3, 2, 'A7', 93, 8, 80)                                       # de grote val naar de hook
    for base in (A0, A0 + 8, R0):
        petals(base + 3, 3, 'Gmaj7', 91)
        petals(base + 7, 4, h_last(base + 7), 88, 4, 70)
    petals(A0 + 15, 3, 'Dmaj7', 93)
    for b in (B0 + 3, B0 + 7):
        petals(b, 0, halves(b)[0], 90, 4, 66)
    for i in range(12):                                                 # C: elke maat dwarrelt er een blaadje
        b = C0 + i
        ch = halves(b)[1]
        if i in (3, 7):
            petals(b, 3, ch, 93, 6, 80)
        else:
            petals(b, 4, ch, 90 if i % 2 else 86, 3, 64)

    # ---- percussie -----------------------------------------------------------------------------------------------
    for b in range(END):
        sec = 'intro' if b < A0 else 'A' if b < B0 else 'B' if b < C0 else 'C' if b < R0 else 'R'
        if b in (0, A0, B0, C0, R0) or (sec in ('A', 'R') and (b - A0) % 2 == 0) or sec == 'C':
            hit('tri', b, 0, TRI, 76 if b in (A0, B0, C0, R0) else 58, E)
        if sec == 'C':
            hit('tri', b, 3, TRI_MUTE, 46, S16)
        if sec in ('B', 'C', 'R'):                                      # zachte bongo's
            for e8, nt, v in ((2, BONGO_HI, 58), (3, BONGO_LO, 66), (5, BONGO_HI, 52)):
                hit('perc', b, e8, nt, v, S16)
            if b + 1 in (C0, R0, END) or (b - B0) % 4 == 3:
                hit('perc', b, 5.5, BONGO_HI, 60, S16)
        if b >= 2 and b != END:                                         # shaker (PSG-ruis) in achtsten
            for e8 in range(6):
                v = 72 if e8 in (0, 3) else 44
                hit('shaker', b, e8, 84, v - (16 if b < A0 else 0), 8)
                if sec == 'C' and e8 in (2, 5):
                    hit('shaker', b, e8 + 0.5, 84, 34, 6)

    # gitaar wijkt voor de celesta-blaadjes (anders vallen er willekeurig gitaarnoten weg in de stemverdeler)
    cel = [(s0 - E, e0 + E) for s0, e0, _, _ in parts['celesta']]
    parts['guitar'] = [g for g in parts['guitar'] if not any(a <= g[0] < z for a, z in cel)]
    for k in parts:                                                     # niets over de loopgrens
        parts[k] = dedupe([[s, min(e, END * BAR), n, v] for s, e, n, v in parts[k] if s < END * BAR])

    write_voicegroup()
    rel = releases(VG)
    progs = {'flute': FLUTE, 'clar': CLARINET, 'bass': PIZZ, 'harp': HARP, 'celesta': CELESTA, 'guitar': NYLON,
             'pad': PAD}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) for k, pr in progs.items()}
    tail['perc'] = 2                                                    # bongo's: korte sample (0,1 s) = nootlengte
    tail['tri'] = 0
    for k in ('flute', 'clar', 'pad'):
        parts[k] = detach(parts[k], tail[k])
    order = ['flute', 'bass', 'clar', 'harp', 'tri', 'perc', 'celesta', 'pad', 'guitar']
    ds = {k: parts[k] for k in order}
    kept = allocate(ds, order, tail, drum_len=TPB, drum_parts=('tri',))
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
    layout = [('flute', FLUTE, 118, 0, 70), ('clar', CLARINET, 100, 1, 50), ('harp', HARP, 96, 2, 80),
              ('celesta', CELESTA, 84, 3, 92), ('guitar', NYLON, 84, 4, 44), ('bass', PIZZ, 112, 5, 64),
              ('pad', PAD, 72, 6, 64), ('perc', DRUMS, 92, 9, 64), ('shaker', SHAKER, 30, 7, 84)]
    parts['perc'] = sorted(parts['perc'] + parts['tri'])
    for k, prog, vol, ch, pan in layout:
        song.add(parts[k], prog, vol, ch, pan)
    written = {k for k, *_ in layout} | {'tri'}
    assert not [k for k in parts if parts[k] and k not in written], 'partij niet weggeschreven'
    song.save(OUT, END * BAR)
    print(OUT, '%.1f s intro, %.1f s loop' % (A0 * BAR / TPB * 60 / BPM, (END - A0) * BAR / TPB * 60 / BPM))


def h_last(b):
    return halves(b)[1]


def write_voicegroup():
    """grounded_gm + eigen samples (celesta, nylon, harp, klarinet, fluit), pizzicato, zachte strijkers, shaker, kit."""
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Battle! Shaymin. Gegenereerd door tools/grounded/shaymin_theme.py.'
    lines[1] = '@ 8 celesta, 24 nylon, 45 pizzicato, 46 harp, 48 zachte strijkers, 71 klarinet, 73 fluit, 121 shaker, 127 kit.'
    lines[2] = 'voice_group %s' % VG
    repl = {
        '@ 8': '\tvoice_directsound 60, 0, DirectSoundWaveData_shaymin_celesta, 255, 0, 255, 200  @ 8',
        '@ 24': '\tvoice_directsound 60, 0, DirectSoundWaveData_shaymin_nylon, 255, 0, 255, 190  @ 24',
        '@ 45': '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_pizzicato_strings, 255, 226, 0, 150  @ 45',
        '@ 46': '\tvoice_directsound 60, 0, DirectSoundWaveData_shaymin_harp, 255, 0, 255, 205  @ 46',
        '@ 48': '\tvoice_keysplit voicegroup_shaymin_strings_keysplit, keysplit_strings  @ 48',
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
    kit = [   # vanaf noot 36; alles DirectSound (geen PSG-piepjes)
        'voice_directsound_no_resample 60, 80, DirectSoundWaveData_sd90_open_triangle, 255, 0, 255, 200',     # 36 triangel
        'voice_directsound_no_resample 60, 80, DirectSoundWaveData_sd90_open_triangle, 255, 0, 255, 60',      # 37 triangel kort
        'voice_directsound 74, 40, DirectSoundWaveData_sc88pro_mute_high_conga, 255, 0, 255, 60',             # 38 bongo hoog
        'voice_directsound 68, 54, DirectSoundWaveData_sc88pro_mute_high_conga, 255, 0, 255, 60',             # 39 bongo laag
    ]
    open('sound/voicegroups/drumsets/shaymin.inc', 'w').write(
        '@ Project Grounded: kit voor Battle! Shaymin (shaymin_theme.py): 36 triangel, 37 triangel kort,\n'
        '@ 38 bongo hoog, 39 bongo laag.\n'
        'voice_group shaymin_drumset, 36\n' + ''.join('\t%s\n' % k for k in kit) + '\n')


if __name__ == '__main__':
    build()
