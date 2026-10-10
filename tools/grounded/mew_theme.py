#!/usr/bin/env python3
"""Project Grounded: Battle! Mew, remix van Battle! Mewtwo (mewtwo_theme.py) met het karakter omgedraaid (Jordi:
"minder evil, minder sinister, curious, geen kloon, originator gevoel").

Mewtwo was de vervormde kopie; dit is de bron waar het DNA vandaan komt. Zelfde motieven, contouren en vorm
(A hoog tempo / B breakdown / C drop, loop naar A), maar:
- 132 bpm, A-lydisch/A-groot i.p.v. A-mineur/frygisch: Mewtwo's Bb (frygische b2) wordt B-groot (lydische II),
  de verminderde E-maat wordt een open vraag (E met een hangende F#).
- A: het staccato-motief als vraag-en-antwoord: de fluit vraagt (eerste helft van de maat), de glockenspiel antwoordt
  een octaaf hoger; elke 4e maat een ritmisch 'hikje' (drums en bas houden een 8e in, Mew giechelt op de glock).
- B: de melancholische frase in groot op de fluit; Mewtwo's echo een halve toon ernaast (de imperfecte kloon) wordt
  hier een nieuwsgierige variatie: dezelfde frase omgekeerd (gespiegeld in de toonladder) op de glockenspiel, harp-
  arpeggio's i.p.v. dreigende pads.
- C: de euforische hook in groot (A-F#m-D-E, A-F#m-B-E) op fluit + glockenspiel, hoog koor, tamboerijn.
- Intro: Mew's transitie is kort (vanilla grid squares): twee maten 'DNA-motief' (glock vraagt, fluit antwoordt,
  A -> B lydisch zoals Mewtwo's dagboekakkoorden Am -> Bb), een ademmaat voor de cry, een opbouwmaat.
Gebruikt voicegroup_grounded_mewtwo (alleen stock-samples: fluit 72, glockenspiel 9, harp 46, fingered bass 32,
strijkers 48, koor 52, PSG); kost dus geen nieuwe samples. Gebruik: python3 tools/grounded/mew_theme.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

OUT = 'sound/songs/midi/mus_grounded_vs_mew.mid'
VG = 'grounded_mewtwo'          # hergebruik: alles wat Mew nodig heeft zit er al in
TPB, BPM = 96, 132
S16 = TPB // 4
BAR = TPB * 4
FLUTE, GLOCK, HARP, PAD, CHOIR, BASS, DRUMS = 72, 9, 46, 48, 52, 32, 127
ARP, DELAY, SUB, SHAKER, RISER = 80, 81, 84, 120, 121      # PSG-lagen (kosten geen DirectSound-kanalen)
KICK, SNARE, CLAP, HH, OHH, CRASH, TAMB = 36, 38, 39, 42, 46, 57, 54
BREATH, BUILD = 2, 3
A_START, B_START, C_START, END = 4, 12, 20, 28
MAX_DS = 11                     # legendary-budget

N = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'Ab': 8,
     'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
LYDIAN = [9, 11, 1, 3, 4, 6, 8]     # A B C# D# E F# G#


def p(name):
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


CH = {'A': ('A', ['A3', 'C#4', 'E4']), 'B': ('B', ['F#3', 'B3', 'D#4']), 'E': ('E', ['G#3', 'B3', 'E4']),
      'D': ('D', ['F#3', 'A3', 'D4']), 'F#m': ('F#', ['F#3', 'A3', 'C#4'])}
PROG = {}
for b in range(A_START, B_START):
    PROG[b] = ['A', 'B', 'A', 'E'][(b - A_START) % 4]            # Mewtwo: Am Bb Am E
for b in range(B_START, C_START):
    PROG[b] = ['D', 'A', 'B', 'E'][(b - B_START) % 4]            # Mewtwo: Dm Am Bb E
for b in range(C_START, END):
    PROG[b] = ['A', 'F#m', 'D', 'E', 'A', 'F#m', 'B', 'E'][b - C_START]   # Mewtwo: Am F C G Am F C E


def bars(pattern, bar, vel=110, shift=0):
    return [[bar * BAR + st * S16, bar * BAR + (st + ln) * S16, p(n) + shift, vel] for st, ln, n in pattern]


# --- melodieën: dezelfde contouren als Mewtwo, in A-lydisch -------------------------------------------------------
MOTIF = {   # A: Mewtwo's staccato-motief; stap < 8 = vraag (fluit), stap >= 8 = antwoord (glock)
    'A': [(0, 1, 'A4'), (2, 1, 'A4'), (3, 1, 'C#5'), (5, 1, 'A4'), (6, 2, 'B4'), (8, 1, 'A4'), (10, 1, 'E5'),
          (11, 1, 'D#5'), (12, 2, 'C#5'), (14, 2, 'B4')],
    'B': [(0, 1, 'B4'), (2, 1, 'B4'), (3, 1, 'D#5'), (5, 1, 'B4'), (6, 2, 'C#5'), (8, 1, 'D#5'), (10, 1, 'F#5'),
          (11, 1, 'E5'), (12, 2, 'D#5'), (14, 2, 'C#5')],
    'E': [(0, 2, 'G#4'), (2, 2, 'B4'), (4, 2, 'D#5'), (6, 2, 'F#5'), (8, 4, 'E5'), (12, 1, 'F#5')],  # open vraag
}
SAD = [   # B: Mewtwo's melancholische frase, in groot
    [(0, 8, 'F#5'), (8, 8, 'E5')], [(0, 12, 'C#5'), (12, 4, 'E5')],
    [(0, 8, 'D#5'), (8, 6, 'F#5'), (14, 2, 'E5')], [(0, 16, 'G#4')],
]
HOOK = {   # C: de hook
    'A': [(0, 3, 'E5'), (3, 3, 'A5'), (6, 2, 'C#6'), (8, 3, 'B5'), (11, 3, 'A5'), (14, 2, 'E5')],
    'F#m': [(0, 3, 'F#5'), (3, 3, 'A5'), (6, 2, 'C#6'), (8, 3, 'A5'), (11, 3, 'G#5'), (14, 2, 'F#5')],
    'D': [(0, 3, 'F#5'), (3, 3, 'A5'), (6, 2, 'D6'), (8, 3, 'E6'), (11, 3, 'D6'), (14, 2, 'A5')],
    'B': [(0, 3, 'F#5'), (3, 3, 'B5'), (6, 2, 'D#6'), (8, 3, 'E6'), (11, 3, 'D#6'), (14, 2, 'B5')],
    'E': [(0, 6, 'B5'), (6, 2, 'A5'), (8, 4, 'G#5'), (12, 4, 'E5')],
    'E2': [(0, 6, 'G#5'), (6, 2, 'B5'), (8, 8, 'E6')],
}


SCALE = [n for n in range(128) if n % 12 in LYDIAN]      # alle noten van A-lydisch, oplopend


def from_deg(octv, d):
    """trap d (0 = A) in octaaf octv (A4 = octaaf 5, zoals p('A4') = 69 = 12*5+9)."""
    return 12 * (octv + d // 7) + LYDIAN[d % 7] + (12 if LYDIAN[d % 7] < 9 else 0)


def invert(pattern, axis_name):
    """Spiegel de frase rond de eerste noot, in de toonladder (Mew probeert het andersom)."""
    idx = lambda n: min(range(len(SCALE)), key=lambda i: abs(SCALE[i] - n))
    ax = idx(p(axis_name))
    return [(st, ln, SCALE[2 * ax - idx(p(nm))]) for st, ln, nm in pattern]


def build():
    parts = {k: [] for k in ('flute', 'glock', 'harp', 'pad', 'gate', 'choir', 'bass', 'drums', 'hats',
                             'arp', 'delay', 'sub', 'shaker', 'riser')}

    # ---- intro (transitie, maat 0-1): het DNA-motief, glock vraagt, fluit antwoordt ----
    for b in (0, 1):
        t0 = b * BAR
        chord = ['A3', 'C#4', 'E4'] if b == 0 else ['B3', 'D#4', 'F#4']       # Mewtwo: Am -> Bb, hier A -> B
        parts['pad'] += [[t0, t0 + BAR - 8, p(n), 62 + b * 10] for n in chord]
        parts['choir'] += [[t0, t0 + BAR - 8, p('E5') if b == 0 else p('F#5'), 52 + b * 10]]
    q = [(0, 2, 'A5'), (2, 2, 'C#6'), (4, 2, 'E6'), (6, 6, 'D#6')]              # vraag: A C# E ... D#?
    parts['glock'] += bars(q, 0, 92)
    a = [(0, 1, 'E5'), (1, 1, 'D#5'), (2, 2, 'B4'), (4, 2, 'F#5'), (6, 6, 'E5')]
    parts['flute'] += bars(a, 1, 96)
    parts['harp'] += [[BAR + 12 * S16 + i * 8, BAR + 12 * S16 + i * 8 + 24, n, 60 + i * 6]   # glinster omhoog
                      for i, n in enumerate([p(x) for x in ('B4', 'D#5', 'F#5', 'A5', 'B5', 'D#6', 'F#6', 'A6')])]
    for b in (0, 1):                                                             # wiegende hartslag, licht
        for beat in (0, 2):
            t = b * BAR + beat * TPB
            parts['drums'] += [[t, t + S16, KICK, 52 + b * 14]]
    # ademmaat (cry): alleen pad + koor
    t0 = BREATH * BAR
    parts['pad'] += [[t0, t0 + BAR - 8, p(n), 66] for n in ('A3', 'E4')]
    parts['choir'] += [[t0 + TPB, t0 + BAR - 8, p('C#5'), 64]]
    # opbouw: kick in kwarten, snareroffel, riser, stijgende pomp
    t0 = BUILD * BAR
    parts['drums'] += [[t0 + i * TPB, t0 + i * TPB + S16, KICK, 88 + i * 8] for i in range(4)]
    parts['drums'] += [[t0 + i * S16, t0 + i * S16 + 8, SNARE, 44 + i * 4] for i in list(range(0, 8, 2)) + list(range(8, 16))]
    parts['riser'] = [[t0 + i * 2 * S16, t0 + i * 2 * S16 + 2 * S16, 60 + i * 3, 56 + i * 8] for i in range(8)]
    parts['gate'] += [[t0 + i * 2 * S16, t0 + i * 2 * S16 + S16, from_deg(5, 4 + i), 64 + i * 4] for i in range(8)]
    parts['glock'] += [[t0 + 12 * S16 + i * S16, t0 + 12 * S16 + i * S16 + S16, from_deg(6, i), 80 + i * 6]
                       for i in range(4)]                                        # A B C# D#: nieuwsgierig opstapje

    for b in range(A_START, END):
        ch = PROG[b]
        root, pad = CH[ch]
        t0 = b * BAR
        hiccup = b < B_START and (b - A_START) % 4 == 3        # A: 4e maat = het hikje op stap 12-13
        r = 12 * 3 + N[root] if N[root] >= 4 else 12 * 4 + N[root]
        # bas: A huppelende 8en grondtoon/octaaf, B lang, C offbeat-trancebas
        if b < B_START:
            for i in range(8):
                if hiccup and i == 6:
                    continue
                parts['bass'] += [[t0 + i * 2 * S16, t0 + i * 2 * S16 + S16 + 4, r + (12 if i % 2 else 0), 108]]
            if not hiccup:
                parts['bass'] += [[t0 + 15 * S16, t0 + 16 * S16 - 4, r + 7, 84]]     # 16e-opmaat (kwint)
        elif b < C_START:
            parts['bass'] += [[t0, t0 + BAR - 12, r, 88]]
        else:
            parts['bass'] += [[t0 + i * TPB + 2 * S16, t0 + i * TPB + 4 * S16 - 4, r, 114] for i in range(4)]
            parts['bass'] += [[t0 + i * TPB, t0 + i * TPB + S16, r, 92] for i in range(4)]
        # strijkers/koor: alleen in B aangehouden; in A/C pompen ze
        if B_START <= b < C_START:
            parts['pad'] += [[t0, t0 + BAR - 8, p(n), 88] for n in pad[:2]]
            parts['choir'] += [[t0, t0 + BAR - 8, p(pad[-1]) + 12, 84]]
        elif b >= C_START:
            parts['choir'] += [[t0, t0 + BAR - 8, p(pad[-1]) + 12, 92]]                 # hoog, luchtig
        if b < B_START or b >= C_START:
            parts['gate'] += [[t0 + i * 2 * S16, t0 + i * 2 * S16 + S16, p(n) + 12, 80]
                              for i in range(8) for n in pad[2:] if not (hiccup and i == 6)]
        # drums
        if b < B_START or b >= C_START:
            for i in range(4):
                parts['drums'] += [[t0 + i * TPB, t0 + i * TPB + S16, KICK, 118]]
            if hiccup:
                parts['drums'] += [[t0 + 13 * S16, t0 + 14 * S16, KICK, 96]]            # verlaat, ná het hikje
            parts['drums'] += [[t0 + i * TPB, t0 + i * TPB + 2 * S16, CLAP, 96] for i in (1, 3) if not (hiccup and i == 3)]
            parts['hats'] += [[t0 + i * TPB + 2 * S16, t0 + i * TPB + 4 * S16, OHH, 80] for i in range(4)
                              if not (hiccup and i == 3)]
            if b < B_START:
                parts['hats'] += [[t0 + i * S16, t0 + i * S16 + 8, HH, 62] for i in range(16)
                                  if i % 4 != 2 and not (hiccup and 12 <= i < 14)]
            else:
                parts['drums'] += [[t0 + i * TPB, t0 + i * TPB + S16, TAMB, 72] for i in (1, 3)]
            if b in (A_START, C_START):
                parts['drums'] += [[t0, t0 + 2 * TPB, CRASH, 108]]
        if b in (C_START - 2, C_START - 1):
            steps = range(0, 16, 2) if b == C_START - 2 else range(16)
            parts['drums'] += [[t0 + i * S16, t0 + i * S16 + 8, SNARE, 56 + (i * 4 if b == C_START - 1 else i * 2)]
                               for i in steps]
        # melodie
        if b < B_START:
            mot = MOTIF[ch]
            parts['flute'] += bars([x for x in mot if x[0] < 8], b, 108)
            parts['glock'] += bars([x for x in mot if x[0] >= 8], b, 96, shift=12)          # het antwoord
            if hiccup:                                                  # Mew giechelt in het gat
                parts['glock'] += [[t0 + 12 * S16 + k * 8, t0 + 12 * S16 + k * 8 + 8, n, 88]
                                   for k, n in enumerate((p('E6'), p('G#6'), p('B6')))]
            parts['arp'] += [[t0 + i * S16, t0 + i * S16 + 10, p(pad[i % 3]) + 24, 60] for i in range(16)]
        elif b < C_START:
            k = b - B_START
            if k % 2 == 0:
                phrase = SAD[(k // 2) % 4]
                parts['flute'] += bars(phrase, b, 100)
                inv = invert(phrase, phrase[0][2])
                # nieuwsgierige variatie: gespiegeld, een octaaf hoger, in huppelende 8en i.p.v. lange noten
                for st, ln, n in inv:
                    for j in range(0, ln, 4):
                        s = (b + 1) * BAR + (st + j) * S16
                        parts['glock'] += [[s, s + 2 * S16, n + 12, 70 - j * 2]]
            parts['harp'] += [[t0 + (4 * i + 2) * S16, t0 + (4 * i + 4) * S16, p(pad[i % 3]) + 12 + (12 if i == 3 else 0), 64]
                              for i in range(4)]                       # harp op de 'en': huppelend, luchtig
        else:
            key = 'E2' if b == END - 1 else ch
            parts['flute'] += bars(HOOK[key], b, 114)
            parts['glock'] += [e for e in bars(HOOK[key], b, 84, shift=12) if e[1] - e[0] >= 3 * S16]
            parts['arp'] += [[t0 + i * S16, t0 + i * S16 + 10, p(pad[i % 3]) + 24 + (12 if i % 8 >= 4 else 0), 66]
                             for i in range(16)]
            if b == END - 1:                                            # giechelloopje terug naar A
                parts['glock'] += [[t0 + (12 + i) * S16, t0 + (13 + i) * S16, from_deg(6, i), 80 + i * 6] for i in range(4)]

    # ---- PSG-lagen ----
    parts['delay'] = [[s + 3 * S16, e + 3 * S16, n, int(v * 0.6)] for s, e, n, v in parts['arp']]
    for b in range(A_START, END):
        t0, root = b * BAR, CH[PROG[b]][0]
        if b < B_START or b >= C_START:
            parts['sub'] += [[t0 + h * 2 * TPB, t0 + h * 2 * TPB + 2 * TPB - 8, 12 * 3 + N[root], 92] for h in (0, 1)]
            parts['shaker'] += [[t0 + i * S16, t0 + i * S16 + 6, 84, 86 if i % 4 == 2 else 46] for i in range(16)]
        else:
            parts['sub'] += [[t0, t0 + BAR - 8, 12 * 3 + N[root], 66]]
    for b in (C_START - 2, C_START - 1):
        t0 = b * BAR
        parts['riser'] += [[t0 + i * TPB, t0 + i * TPB + TPB, 56 + (b - C_START + 2) * 12 + i * 3, 50 + (b - C_START + 2) * 30 + i * 6]
                           for i in range(4)]

    for k in parts:
        parts[k] = dedupe(parts[k])

    rel = releases(VG)
    progs = {'flute': FLUTE, 'glock': GLOCK, 'harp': HARP, 'pad': PAD, 'gate': PAD, 'choir': CHOIR, 'bass': BASS}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) for k, pr in progs.items()}
    tail['drums'] = tail['hats'] = 0
    for k in ('flute', 'choir'):
        parts[k] = detach(parts[k], tail[k])
    order = ['flute', 'glock', 'bass', 'drums', 'hats', 'choir', 'pad', 'gate', 'harp']
    ds = {k: parts[k] for k in order}
    kept = allocate(ds, order, tail, max_voices=MAX_DS)
    for k in order:
        n = len(ds[k])
        if len(kept[k]) < n:
            ks = set(map(tuple, kept[k]))
            lost = sorted(set(e[0] // BAR for e in ds[k] if tuple(e) not in ks))
            print('  %s: %d van %d noten vallen weg (maten %s)' % (k, n - len(kept[k]), n, lost))
        parts[k] = kept[k]

    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.loop = (A_START * BAR, END * BAR)
    layout = [('flute', FLUTE, 108, 0, 64), ('glock', GLOCK, 66, 1, 80), ('harp', HARP, 70, 2, 44),
              ('gate', PAD, 64, 3, 64), ('pad', PAD, 72, 4, 64), ('choir', CHOIR, 66, 5, 64),
              ('bass', BASS, 112, 6, 64),
              ('arp', ARP, 30, 7, 40), ('delay', DELAY, 26, 8, 88), ('sub', SUB, 56, 10, 64),
              ('shaker', SHAKER, 30, 11, 70), ('riser', RISER, 40, 12, 64)]
    for k, prog, vol, ch, pan in layout:
        song.add(parts[k], prog, vol, ch, pan)
    song.add(sorted(parts['drums'] + parts['hats']), DRUMS, 98, 9)
    written = {k for k, *_ in layout} | {'drums', 'hats'}
    assert not [k for k in parts if parts[k] and k not in written], 'partij niet weggeschreven'
    song.save(OUT, END * BAR)
    print(OUT)


if __name__ == '__main__':
    build()
