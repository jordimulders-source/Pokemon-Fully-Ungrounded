#!/usr/bin/env python3
"""Project Grounded: Battle! Mew v3, de 'broer' van Battle! Mewtwo (mewtwo_theme.py): dezelfde kracht, een andere houding.

Geschiedenis (Jordi):
- v1 (132 bpm, A-lydisch, glockenspiel, hikjes): "tonen klinken raar, te hoog, niet in een goed tempo".
- v2 (156 bpm, legato, harp, fluit): "nog veel te lieflijk ... een soort van wolkentheme"; "Mew heeft alsnog hoge
  stats"; "Mewtwo's theme is super vet, dat mag iets minder dreigend, wat neutraler, maar hoeft niet naar oh my ik
  loop op de wolken niveau".
- v3 (dit script): Mewtwo's arrangement bijna 1-op-1 (128 bpm, four-on-the-floor, jagende 16e-bas, gated trance-
  strijkers, koor, pauken, blokgolf-lead, PSG-lagen, breakdown + euforische drop), alleen minder dreigend:
  * A: Mewtwo's frygische Bb en de verminderde E-maat eruit: Am-G-Am-Em (natuurlijk mineur), het motief zonder
    halve-toonstap (A A C A B A E D C B), de E-maat als Em9 (G B D F# E);
  * B: Dm-Am-Bb-E wordt D-Am-F-G (dorische IV in groot, dan bVI-bVII): de echo is zuiver (een octaaf lager, Mew is
    het origineel) i.p.v. een halve toon ernaast (de imperfecte kloon);
  * C: dezelfde hook Am-F-C-G, de tweede keer eindigend op G (bVII) die de loop in oplost naar Am i.p.v. het
    dreigende E-groot;
  * klank: het donkere kerkorgel weg; de melodie op de DirectSound-blokgolf + trompet (unisono), in v2's register
    (motief A4-E5, hook een octaaf lager dan Mewtwo's orgel: max. D5); geen tritonus-aanslag in de intro;
  * intro korter (Mew heeft de korte grid-transitie): drone + de vraag op de lead, Mew verschijnt (crash/pauk),
    ademmaat voor de cry, Mewtwo's opbouwmaat.
voicegroup_grounded_mew = grounded_mewtwo met een kortere harp-release (sinds v2, hier ongebruikt).
Gebruik: python3 tools/grounded/mew_theme.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

OUT = 'sound/songs/midi/mus_grounded_vs_mew.mid'
VG = 'grounded_mew'
TPB, BPM = 96, 128
S16 = TPB // 4
BAR = TPB * 4
LEAD, TRUMPET, PLUCK, PAD, CHOIR, BASS, TIMPANI, DRUMS = 82, 56, 80, 48, 52, 38, 47, 127
DELAY, SUB, SHAKER, RISER = 81, 84, 120, 121      # PSG-lagen
APPEAR, BREATH, BUILD = 1, 2, 3
KICK, SNARE, CLAP, HH, OHH, CRASH = 36, 38, 39, 42, 46, 57
A_START, B_START, C_START, END = 4, 12, 20, 28
MAX_DS = 11

N = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def p(name):
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


CH = {'Am': ('A', ['A3', 'C4', 'E4']), 'F': ('F', ['F3', 'A3', 'C4']), 'C': ('C', ['G3', 'C4', 'E4']),
      'G': ('G', ['G3', 'B3', 'D4']), 'Em': ('E', ['G3', 'B3', 'E4']), 'D': ('D', ['F#3', 'A3', 'D4'])}
PROG = {}
for b in range(A_START, B_START):
    PROG[b] = ['Am', 'G', 'Am', 'Em'][(b - A_START) % 4]         # Mewtwo: Am Bb Am E
for b in range(B_START, C_START):
    PROG[b] = ['D', 'Am', 'F', 'G'][(b - B_START) % 4]           # Mewtwo: Dm Am Bb E
for b in range(C_START, END):
    PROG[b] = ['Am', 'F', 'C', 'G', 'Am', 'F', 'C', 'G'][b - C_START]   # Mewtwo: ... C E


def bars(pattern, bar, vel=110, shift=0):
    return [[bar * BAR + st * S16, bar * BAR + (st + ln) * S16, p(n) + shift, vel] for st, ln, n in pattern]


MOTIF = {   # A: Mewtwo's staccato-motief zonder de frygische halve toon
    'Am': [(0, 1, 'A4'), (2, 1, 'A4'), (3, 1, 'C5'), (5, 1, 'A4'), (6, 2, 'B4'), (8, 1, 'A4'), (10, 1, 'E5'),
           (11, 1, 'D5'), (12, 2, 'C5'), (14, 2, 'B4')],
    'G': [(0, 1, 'G4'), (2, 1, 'G4'), (3, 1, 'B4'), (5, 1, 'G4'), (6, 2, 'A4'), (8, 1, 'B4'), (10, 1, 'D5'),
          (11, 1, 'C5'), (12, 2, 'B4'), (14, 2, 'A4')],
    'Em': [(0, 2, 'G4'), (2, 2, 'B4'), (4, 2, 'D5'), (6, 2, 'F#5'), (8, 8, 'E5')],
}
SAD = [   # B: Mewtwo's melancholische frase, over D-Am-F-G
    [(0, 8, 'F#5'), (8, 8, 'E5')], [(0, 12, 'C5'), (12, 4, 'E5')],
    [(0, 8, 'D5'), (8, 6, 'F5'), (14, 2, 'E5')], [(0, 16, 'D5')],
]
HOOK = {   # C: Mewtwo's hook (in build een octaaf lager gezet)
    'Am': [(0, 3, 'E5'), (3, 3, 'A5'), (6, 2, 'C6'), (8, 3, 'B5'), (11, 3, 'A5'), (14, 2, 'E5')],
    'F': [(0, 3, 'F5'), (3, 3, 'A5'), (6, 2, 'C6'), (8, 3, 'A5'), (11, 3, 'G5'), (14, 2, 'F5')],
    'C': [(0, 3, 'E5'), (3, 3, 'G5'), (6, 2, 'C6'), (8, 3, 'D6'), (11, 3, 'C6'), (14, 2, 'G5')],
    'G': [(0, 6, 'B5'), (6, 2, 'A5'), (8, 4, 'G5'), (12, 4, 'D5')],
    'G2': [(0, 6, 'D6'), (6, 2, 'C6'), (8, 4, 'B5'), (12, 2, 'C6'), (14, 2, 'D6')],   # bVII, lost op in de loop
}
QUESTION = [(0, 2, 'A4'), (2, 2, 'C5'), (4, 2, 'E5'), (6, 2, 'D5'), (8, 6, 'B4')]   # de intro: Mew kijkt je aan


def build():
    parts = {k: [] for k in ('lead', 'trumpet', 'echo', 'pluck', 'pad', 'gate', 'choir', 'bass', 'timp', 'drums', 'hats',
                             'delay', 'sub', 'shaker', 'riser')}

    # ---- intro: maat 0 = transitie, maat 1 = Mew verschijnt, maat 2 = adem (cry), maat 3 = opbouw ----
    for b in range(0, BREATH):
        t0 = b * BAR
        parts['pad'] += [[t0, t0 + BAR - 8, p('A2'), 60 + b * 12], [t0, t0 + BAR - 8, p('E3'), 56 + b * 12]]
        parts['choir'] += [[t0, t0 + BAR - 8, p('A3') if b == 0 else p('C4'), 60 + b * 12]]
    parts['lead'] += bars(QUESTION, 0, 92)
    for beat in (0, 2):
        parts['drums'] += [[beat * TPB, beat * TPB + S16, KICK, 70], [beat * TPB + S16 + 8, beat * TPB + 2 * S16 + 8, KICK, 56]]
    ap = APPEAR * BAR
    parts['drums'] += [[ap, ap + 2 * TPB, CRASH, 120], [ap, ap + S16, KICK, 124]]
    parts['timp'] += [[ap, ap + TPB, p('A2'), 124]]
    parts['trumpet'] += [[ap, ap + 2 * TPB - 8, n, 100] for n in (p('E4'), p('A4'))]        # open kwint: kracht
    parts['pluck'] += [[ap + i * 2 * S16, ap + i * 2 * S16 + 6, p('E5') + (0, 3, 7, 12)[i % 4], 50] for i in range(8)]
    t0 = BREATH * BAR
    parts['pad'] += [[t0 + TPB, t0 + BAR - 8, p('A2'), 66], [t0 + TPB, t0 + BAR - 8, p('E3'), 60]]
    parts['choir'] += [[t0 + TPB, t0 + BAR - 8, p('E4'), 70]]
    t0 = BUILD * BAR                                                              # Mewtwo's opbouwmaat
    parts['drums'] += [[t0 + i * TPB, t0 + i * TPB + S16, KICK, 90 + i * 8] for i in range(4)]
    parts['drums'] += [[t0 + i * S16, t0 + i * S16 + 8, SNARE, 50 + i * 4] for i in list(range(0, 8, 2)) + list(range(8, 16))]
    parts['riser'] = [[t0 + i * 2 * S16, t0 + i * 2 * S16 + 2 * S16, 60 + i * 3, 60 + i * 8] for i in range(8)]
    parts['gate'] += [[t0 + i * 2 * S16, t0 + i * 2 * S16 + S16, p('E4') + (0, 2, 3, 5, 7, 8, 10, 12)[i], 70 + i * 4]
                      for i in range(8)]

    for b in range(A_START, END):
        ch = PROG[b]
        root, pad = CH[ch]
        t0 = b * BAR
        r = 12 * 3 + N[root] if N[root] >= 4 else 12 * 4 + N[root]
        if b < B_START:
            parts['bass'] += [[t0 + i * S16, t0 + i * S16 + S16 - 4, r + (12 if i % 4 == 3 else 0), 112] for i in range(16)]
        elif b < C_START:
            parts['bass'] += [[t0, t0 + BAR - 12, r, 90]]
        else:
            parts['bass'] += [[t0 + i * TPB + 2 * S16, t0 + i * TPB + 4 * S16 - 4, r, 118] for i in range(4)]
            parts['bass'] += [[t0 + i * TPB, t0 + i * TPB + S16, r, 100] for i in range(4)]
        if B_START <= b < C_START:
            parts['pad'] += [[t0, t0 + BAR - 8, p(n), 92] for n in pad]
        parts['choir'] += [[t0, t0 + BAR - 8, p(pad[-1]) + (0 if b < B_START else 12), 80 if b < B_START else 92 if b < C_START else 100]]
        if b < B_START or b >= C_START:
            parts['gate'] += [[t0 + i * 2 * S16, t0 + i * 2 * S16 + S16, p(n) + 12, 84] for i in range(8) for n in pad[1:]]
            parts['drums'] += [[t0 + i * TPB, t0 + i * TPB + S16, KICK, 124] for i in range(4)]
            parts['drums'] += [[t0 + i * TPB, t0 + i * TPB + 2 * S16, CLAP, 104] for i in (1, 3)]
            parts['hats'] += [[t0 + i * TPB + 2 * S16, t0 + i * TPB + 4 * S16, OHH, 90] for i in range(4)]
            if b < B_START:
                parts['hats'] += [[t0 + i * S16, t0 + i * S16 + 8, HH, 70] for i in range(16) if i % 4 != 2]
            if (b - A_START) % 4 == 0 or b == C_START:
                parts['drums'] += [[t0, t0 + 2 * TPB, CRASH, 116]]
                parts['timp'] += [[t0, t0 + TPB, r - 12 if r - 12 >= 40 else r, 118]]
        if b in (C_START - 2, C_START - 1):
            steps = range(0, 16, 2) if b == C_START - 2 else range(16)
            parts['drums'] += [[t0 + i * S16, t0 + i * S16 + 8, SNARE, 60 + (i * 4 if b == C_START - 1 else i * 2)]
                               for i in steps]
        if b < B_START:
            parts['lead'] += bars(MOTIF[ch], b, 112)
            parts['pluck'] += [[t0 + i * S16, t0 + i * S16 + 10, p(pad[i % 3]) + 24, 64] for i in range(16)]
        elif b < C_START:
            k = b - B_START
            if k % 2 == 0:
                phrase = SAD[(k // 2) % 4]
                parts['lead'] += bars(phrase, b, 104)
                parts['echo'] += bars(phrase, b + 1, 70, shift=-12)       # zuivere echo: het origineel, geen kloon
        else:
            key = 'G2' if b == END - 1 else ch
            parts['lead'] += bars(HOOK[key], b, 114, shift=-12)
            parts['trumpet'] += bars(HOOK[key], b, 108, shift=-12)
            parts['pluck'] += [[t0 + i * S16, t0 + i * S16 + 10, p(pad[i % 3]) + 24 + (12 if i % 8 >= 4 else 0), 72]
                               for i in range(16)]

    # ---- PSG-lagen (zoals Mewtwo) ----
    parts['delay'] = [[s + 3 * S16, e + 3 * S16, n, int(v * 0.6)] for s, e, n, v in parts['pluck'] if s >= A_START * BAR]
    for b in range(A_START, END):
        t0, root = b * BAR, CH[PROG[b]][0]
        if b < B_START or b >= C_START:
            parts['sub'] += [[t0 + h * 2 * TPB, t0 + h * 2 * TPB + 2 * TPB - 8, 12 * 3 + N[root], 100] for h in (0, 1)]
            parts['shaker'] += [[t0 + i * S16, t0 + i * S16 + 6, 84, 90 if i % 4 == 2 else 50] for i in range(16)]
        else:
            parts['sub'] += [[t0, t0 + BAR - 8, 12 * 3 + N[root], 70]]
    for b in (C_START - 2, C_START - 1):
        t0 = b * BAR
        parts['riser'] += [[t0 + i * TPB, t0 + i * TPB + TPB, 56 + (b - C_START + 2) * 12 + i * 3, 50 + (b - C_START + 2) * 30 + i * 6]
                           for i in range(4)]

    for k in parts:
        parts[k] = dedupe(parts[k])

    # voicegroup (sinds v2): grounded_mewtwo met een kortere harp
    lines = open('sound/voicegroups/grounded_mewtwo.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_mewtwo met een kortere harp-release (46) voor Battle! Mew.'
    lines[1] = '@ Gegenereerd door tools/grounded/mew_theme.py.'
    lines[2] = 'voice_group %s' % VG
    lines = [('\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_harp, 255, 242, 51, 200  @ 46'
              if l.rstrip().endswith('@ 46') else l) for l in lines]
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(lines))

    rel = releases(VG)
    progs = {'lead': LEAD, 'trumpet': TRUMPET, 'echo': LEAD, 'pad': PAD, 'gate': PAD, 'choir': CHOIR, 'bass': BASS,
             'timp': TIMPANI}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) for k, pr in progs.items()}
    tail['drums'] = tail['hats'] = 0
    for k in ('lead', 'trumpet', 'echo', 'choir'):
        parts[k] = detach(parts[k], tail[k])
    order = ['lead', 'trumpet', 'bass', 'drums', 'echo', 'timp', 'choir', 'gate', 'pad', 'hats']
    ds = {k: parts[k] for k in order}
    kept = allocate(ds, order, tail, max_voices=MAX_DS)
    for k in order:
        n = len(ds[k])
        if len(kept[k]) < n:
            ks = set(map(tuple, kept[k]))
            print('  %s: %d van %d noten vallen weg (maten %s)' % (k, n - len(kept[k]), n,
                  sorted(set(e[0] // BAR for e in ds[k] if tuple(e) not in ks))))
        parts[k] = kept[k]

    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.loop = (A_START * BAR, END * BAR)
    layout = [('lead', LEAD, 92, 0, 64), ('trumpet', TRUMPET, 96, 7, 64), ('gate', PAD, 70, 8, 64),
              ('echo', LEAD, 66, 1, 96), ('pluck', PLUCK, 38, 2, 40), ('pad', PAD, 78, 3, 64),
              ('choir', CHOIR, 76, 4, 64), ('bass', BASS, 112, 5, 64), ('timp', TIMPANI, 110, 6, 64),
              ('delay', DELAY, 30, 10, 88), ('sub', SUB, 60, 11, 64), ('shaker', SHAKER, 34, 12, 70),
              ('riser', RISER, 44, 13, 64)]
    for k, prog, vol, chn, pan in layout:
        song.add(parts[k], prog, vol, chn, pan)
    song.add(sorted(parts['drums'] + parts['hats']), DRUMS, 104, 9)
    assert not [k for k in parts if parts[k] and k not in {x[0] for x in layout} | {'drums', 'hats'}]
    song.save(OUT, END * BAR)
    print(OUT)


if __name__ == '__main__':
    build()
