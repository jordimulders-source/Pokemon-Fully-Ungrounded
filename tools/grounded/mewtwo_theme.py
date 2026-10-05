#!/usr/bin/env python3
"""Project Grounded: Battle! Mewtwo, een eigen compositie (Jordi): euforische trance, melancholisch én evil tegelijk;
Mewtwo is een kloon die zonder zijn wil op aarde is gezet, een 'imperfecte' kloon.

128 bpm, A-mineur. 1 maat = 1,875 s.
- Maat 0 (= de transitie, ±2 s): donkere drone + hartslag; tel 3 = de ogen lichten op (aanslag), tel 3,5-3,83 = drie
  barsten in de tank (glas), maat 1 tel 0 = de tank spat uiteen (crash, kick, bas, koor) = het gevecht begint.
- A (maat 1-8), hoog tempo: jagende 16e-bas, four-on-the-floor, kwaadaardig staccato-motief met frygische Bb.
- B (maat 9-16), trance-breakdown: geen kick, pads + koor, melancholische melodie; elke frase krijgt een zachte echo
  een halve toon ernaast (de imperfecte kloon); snareroffel naar de drop.
- C (maat 17-24), euforische drop: de hoofdhook vol, Am-F-C-G, de tweede keer eindigend op een dreigend E-groot.
- Loop terug naar A.
Gebruikt tools/grounded/musiclib.py; voicegroup_grounded_mewtwo = grounded_gm met een DirectSound-blokgolf als lead (82).
Zie tools/grounded/MUZIEK.md. Gebruik: python3 tools/grounded/mewtwo_theme.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

OUT = 'sound/songs/midi/mus_grounded_vs_mewtwo.mid'
VG = 'grounded_mewtwo'
TPB, BPM = 96, 128
S16 = TPB // 4                 # een 16e
BAR = TPB * 4
LEAD, PLUCK, PAD, CHOIR, BASS, TIMPANI, DRUMS, ORGAN = 82, 80, 48, 52, 38, 47, 127, 83
DELAY, SUB, SHAKER, RISER = 81, 84, 120, 121      # PSG-lagen (kosten geen DirectSound-kanalen)
EYES_BAR, BURST_BAR = 2, 3                        # transitie: ogen op maat 2, de tank barst op maat 3
BREATH = (3, 4)  # maat 3: ademmaat voor de cry van Mewtwo; maat 4: opbouw naar de beat
KICK, SNARE, CLAP, HH, OHH, CRASH, ORCH = 36, 38, 39, 42, 46, 57, 40
A_START, B_START, C_START, END = 5, 13, 21, 29

N = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'Ab': 8,
     'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def p(name):
    """'A4' -> midi-noot."""
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


# akkoorden (grondtoon, tonen voor de pad)
CH = {'Am': ('A', ['A3', 'C4', 'E4']), 'F': ('F', ['F3', 'A3', 'C4']), 'C': ('C', ['G3', 'C4', 'E4']),
      'G': ('G', ['G3', 'B3', 'D4']), 'E': ('E', ['G#3', 'B3', 'E4']), 'Bb': ('Bb', ['F3', 'Bb3', 'D4']),
      'Dm': ('D', ['F3', 'A3', 'D4'])}
PROG = {}
for b in range(A_START, B_START):
    PROG[b] = ['Am', 'Bb', 'Am', 'E'][(b - A_START) % 4]
for b in range(B_START, C_START):
    PROG[b] = ['Dm', 'Am', 'Bb', 'E'][(b - B_START) % 4]
for b in range(C_START, END):
    PROG[b] = ['Am', 'F', 'C', 'G', 'Am', 'F', 'C', 'E'][b - C_START]


def bars(pattern, bar, vel=110, shift=0):
    """pattern = [(16e-stap, lengte in 16en, 'A4'), ...] -> noten in maat `bar`."""
    return [[bar * BAR + st * S16, bar * BAR + (st + ln) * S16, p(n) + shift, vel] for st, ln, n in pattern]


# --- melodieën ---------------------------------------------------------------------------------------------------
EVIL = {   # A: staccato, frygisch
    'Am': [(0, 1, 'A4'), (2, 1, 'A4'), (3, 1, 'C5'), (5, 1, 'A4'), (6, 2, 'Bb4'), (8, 1, 'A4'), (10, 1, 'E5'),
           (11, 1, 'D5'), (12, 2, 'C5'), (14, 2, 'Bb4')],
    'Bb': [(0, 1, 'Bb4'), (2, 1, 'Bb4'), (3, 1, 'D5'), (5, 1, 'Bb4'), (6, 2, 'C5'), (8, 1, 'D5'), (10, 1, 'F5'),
           (11, 1, 'E5'), (12, 2, 'D5'), (14, 2, 'C5')],
    'E': [(0, 2, 'G#4'), (2, 2, 'B4'), (4, 2, 'D5'), (6, 2, 'F5'), (8, 8, 'E5')],
}
SAD = [   # B: melancholisch, lange noten (2 maten per frase)
    [(0, 8, 'F5'), (8, 8, 'E5')], [(0, 12, 'C5'), (12, 4, 'E5')],
    [(0, 8, 'D5'), (8, 6, 'F5'), (14, 2, 'E5')], [(0, 16, 'G#4')],
]
HOOK = {   # C: de euforische hook
    'Am': [(0, 3, 'E5'), (3, 3, 'A5'), (6, 2, 'C6'), (8, 3, 'B5'), (11, 3, 'A5'), (14, 2, 'E5')],
    'F': [(0, 3, 'F5'), (3, 3, 'A5'), (6, 2, 'C6'), (8, 3, 'A5'), (11, 3, 'G5'), (14, 2, 'F5')],
    'C': [(0, 3, 'E5'), (3, 3, 'G5'), (6, 2, 'C6'), (8, 3, 'D6'), (11, 3, 'C6'), (14, 2, 'G5')],
    'G': [(0, 6, 'B5'), (6, 2, 'A5'), (8, 4, 'G5'), (12, 4, 'D5')],
    'E': [(0, 6, 'G#5'), (6, 2, 'B5'), (8, 8, 'E6')],
}


def build():
    parts = {k: [] for k in ('lead', 'organ', 'echo', 'pluck', 'pad', 'gate', 'choir', 'bass', 'timp', 'drums', 'hats',
                             'delay', 'sub', 'shaker', 'riser')}

    # ---- filmische intro = de transitie (maat 0-2), tank barst op maat 3 ----
    for b in range(0, BURST_BAR):                                                 # drone + koor, steeds voller
        t0 = b * BAR
        parts['pad'] += [[t0, t0 + BAR - 8, p('A2'), 54 + b * 10], [t0, t0 + BAR - 8, p('E3'), 50 + b * 10]]
        parts['choir'] += [[t0, t0 + BAR - 8, p('A3') + (0, 0, 1)[b], 56 + b * 10]]
    for b in (0, 1):                                                              # langzame hartslag (lub-dub)
        for beat in (0, 2):
            t = b * BAR + beat * TPB
            parts['drums'] += [[t, t + S16, KICK, 64 + b * 16], [t + S16 + 8, t + 2 * S16 + 8, KICK, 50 + b * 16]]
    parts['organ'] += [[BAR, BAR + 2 * TPB - 8, n, 70] for n in (p('A3'), p('C4'), p('E4'))]       # de dagboekpagina's
    parts['organ'] += [[BAR + 2 * TPB, 2 * BAR - 8, n, 74] for n in (p('Bb3'), p('D4'), p('F4'))]
    parts['pluck'] += [[BAR + i * 2 * S16, BAR + i * 2 * S16 + 6, p('E6'), 30] for i in range(8)]  # tikkende pen
    eyes = EYES_BAR * BAR                                                         # de ogen lichten op
    parts['pad'] += [[eyes, eyes + 2 * TPB, n, 112] for n in (p('A#3'), p('E4'), p('A#4'))]       # tritonus-aanslag
    parts['timp'] += [[eyes, eyes + TPB, p('A2'), 124]]
    parts['drums'] += [[eyes + i * TPB, eyes + i * TPB + S16, KICK, 96] for i in range(2)]        # hart versnelt
    parts['drums'] += [[eyes, eyes + 2 * TPB, CRASH, 90]]
    for k, st in enumerate((2 * TPB, 2 * TPB + 64, 2 * TPB + 128)):              # drie barsten in het glas
        parts['drums'] += [[eyes + st, eyes + st + 8, ORCH, 96 + k * 12]]
        parts['pluck'] += [[eyes + st, eyes + st + 8, p('E6') + k * 3, 90]]
    burst = BURST_BAR * BAR                                                       # de tank barst
    parts['drums'] += [[burst, burst + 2 * TPB, CRASH, 127], [burst, burst + S16, KICK, 127]]
    parts['timp'] += [[burst, burst + TPB, p('A2'), 127]]
    # ademmaat (de cry van Mewtwo): alleen drone en koor
    t0 = BREATH[0] * BAR
    parts['pad'] += [[t0 + TPB, t0 + BAR - 8, p('A2'), 66], [t0 + TPB, t0 + BAR - 8, p('E3'), 60]]
    parts['choir'] += [[t0 + TPB, t0 + BAR - 8, p('E4'), 70]]
    # opbouw naar de beat: kick in kwarten, snareroffel 8en -> 16en, ruis-riser, stijgende strijkers
    t0 = BREATH[1] * BAR
    parts['drums'] += [[t0 + i * TPB, t0 + i * TPB + S16, KICK, 90 + i * 8] for i in range(4)]
    parts['drums'] += [[t0 + i * S16, t0 + i * S16 + 8, SNARE, 50 + i * 4] for i in list(range(0, 8, 2)) + list(range(8, 16))]
    parts['riser'] = [[t0 + i * 2 * S16, t0 + i * 2 * S16 + 2 * S16, 60 + i * 3, 60 + i * 8] for i in range(8)]
    parts['gate'] += [[t0 + i * 2 * S16, t0 + i * 2 * S16 + S16, p('E4') + i, 70 + i * 4] for i in range(8)]

    for b in range(A_START, END):
        ch = PROG[b]
        root, pad = CH[ch]
        t0 = b * BAR
        # bas: A en C jagend in 16en, B offbeat-trancebas
        r = 12 * 3 + N[root] if N[root] >= 4 else 12 * 4 + N[root]       # E2..D#3
        if b < B_START:
            parts['bass'] += [[t0 + i * S16, t0 + i * S16 + S16 - 4, r + (12 if i % 4 == 3 else 0), 112] for i in range(16)]
        elif b < C_START:
            parts['bass'] += [[t0, t0 + BAR - 12, r, 90]]
        else:
            parts['bass'] += [[t0 + i * TPB + 2 * S16, t0 + i * TPB + 4 * S16 - 4, r, 118] for i in range(4)]
            parts['bass'] += [[t0 + i * TPB, t0 + i * TPB + S16, r - 12 + 12, 100] for i in range(4)]
        # pad (strijkers) + koor
        vel_pad = 76 if b < B_START else 96 if b < C_START else 88
        if B_START <= b < C_START:          # aangehouden pad alleen in de breakdown; in A/C pompt de gate
            parts['pad'] += [[t0, t0 + BAR - 8, p(n), vel_pad] for n in pad]
        parts['choir'] += [[t0, t0 + BAR - 8, p(pad[-1]) + (0 if b < B_START else 12), 80 if b < B_START else 92 if b < C_START else 100]]
        if b < B_START or b >= C_START:      # pompende trance-strijkers in achtsten (gated pad)
            parts['gate'] += [[t0 + i * 2 * S16, t0 + i * 2 * S16 + S16, p(n) + 12, 84] for i in range(8) for n in pad[1:]]
        # drums
        if b < B_START or b >= C_START:
            parts['drums'] += [[t0 + i * TPB, t0 + i * TPB + S16, KICK, 124] for i in range(4)]
            parts['drums'] += [[t0 + i * TPB, t0 + i * TPB + 2 * S16, CLAP, 104] for i in (1, 3)]
            parts['hats'] += [[t0 + i * TPB + 2 * S16, t0 + i * TPB + 4 * S16, OHH, 90] for i in range(4)]
            if b < B_START:                                                  # hoog tempo: 16e-hihats
                parts['hats'] += [[t0 + i * S16, t0 + i * S16 + 8, HH, 70] for i in range(16) if i % 4 != 2]
            if (b - A_START) % 4 == 0 or b == C_START:
                parts['drums'] += [[t0, t0 + 2 * TPB, CRASH, 116]]
        if b in (C_START - 2, C_START - 1):                                    # snareroffel naar de drop
            steps = range(0, 16, 2) if b == C_START - 2 else range(16)
            parts['drums'] += [[t0 + i * S16, t0 + i * S16 + 8, SNARE, 60 + (i * 4 if b == C_START - 1 else i * 2)]
                               for i in steps]
        # melodie
        if b < B_START:
            parts['organ'] += bars(EVIL[ch], b, 110)
            parts['pluck'] += [[t0 + i * S16, t0 + i * S16 + 10, p(pad[i % 3]) + 24, 64] for i in range(16)]   # arpeggio
        elif b < C_START:
            k = b - B_START
            if k % 2 == 0:
                phrase = SAD[(k // 2) % 4]
                parts['organ'] += bars(phrase, b, 100)
                # de imperfecte kloon: dezelfde frase een maat later, zachter, een halve toon ernaast
                parts['echo'] += bars(phrase, b + 1, 64, shift=-1)
        else:
            parts['lead'] += bars(HOOK[ch], b, 104, shift=-12)
            parts['organ'] += bars(HOOK[ch], b, 118)
            parts['pluck'] += [[t0 + i * S16, t0 + i * S16 + 10, p(pad[i % 3]) + 24 + (12 if i % 8 >= 4 else 0), 72]
                               for i in range(16)]

    # ---- maximalistisch, op de PSG-kanalen (kost geen DirectSound-kanalen; het bestaande blijft gelijk) ----
    parts['delay'] = [[s + 3 * S16, e + 3 * S16, n, int(v * 0.6)] for s, e, n, v in parts['pluck'] if s >= A_START * BAR]
    for b in range(A_START, END):
        t0, root = b * BAR, CH[PROG[b]][0]
        if b < B_START or b >= C_START:
            parts['sub'] += [[t0 + h * 2 * TPB, t0 + h * 2 * TPB + 2 * TPB - 8, 12 * 3 + N[root], 100] for h in (0, 1)]
            parts['shaker'] += [[t0 + i * S16, t0 + i * S16 + 6, 84, 90 if i % 4 == 2 else 50] for i in range(16)]
        else:
            parts['sub'] += [[t0, t0 + BAR - 8, 12 * 3 + N[root], 70]]
    for b in (C_START - 2, C_START - 1):                                           # riser naar de drop
        t0 = b * BAR
        parts['riser'] += [[t0 + i * TPB, t0 + i * TPB + TPB, 56 + (b - C_START + 2) * 12 + i * 3, 50 + (b - C_START + 2) * 30 + i * 6]
                           for i in range(4)]

    for k in parts:
        parts[k] = dedupe(parts[k])

    # voicegroup: grounded_gm met een DirectSound-blokgolf als lead op 82
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm + DirectSound-blokgolf als lead (82) voor Battle! Mewtwo.'
    lines[1] = '@ Gegenereerd door tools/grounded/mewtwo_theme.py.'
    lines[2] = 'voice_group %s' % VG
    lines = [('\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_square_wave, 255, 0, 255, 165  @ 82'
              if l.rstrip().endswith('@ 82') else
              '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_church_organ3_low, 255, 76, 154, 188  @ 83'
              if l.rstrip().endswith('@ 83') else
              '\tvoice_programmable_wave_alt 60, 0, ProgrammableWaveData_1, 0, 7, 15, 0  @ 84'
              if l.rstrip().endswith('@ 84') else
              '\tvoice_noise_alt 60, 0, 0, 3, 0, 15, 2  @ 121'
              if l.rstrip().endswith('@ 121') else l) for l in lines]
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(lines))

    rel = releases(VG)
    progs = {'lead': LEAD, 'organ': ORGAN, 'echo': LEAD, 'pad': PAD, 'gate': PAD, 'choir': CHOIR, 'bass': BASS, 'timp': TIMPANI}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) for k, pr in progs.items()}
    for k in ('lead', 'organ', 'echo', 'choir'):
        parts[k] = detach(parts[k], tail[k])
    order = ['organ', 'lead', 'bass', 'drums', 'echo', 'timp', 'choir', 'gate', 'pad', 'hats']
    ds = {k: parts[k] for k in order}
    kept = allocate(ds, order, tail)
    for k in order:
        n = len(ds[k])
        if len(kept[k]) < n * 0.97:
            print('  %s: %d van %d noten vallen weg (te vol)' % (k, n - len(kept[k]), n))
        parts[k] = kept[k]

    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.loop = (A_START * BAR, END * BAR)          # intro en ademmaten niet herhalen
    layout = [('lead', LEAD, 76, 0, 64), ('organ', ORGAN, 104, 7, 64), ('gate', PAD, 70, 8, 64), ('echo', LEAD, 70, 1, 96), ('pluck', PLUCK, 38, 2, 40),
              ('pad', PAD, 78, 3, 64), ('choir', CHOIR, 76, 4, 64), ('bass', BASS, 112, 5, 64),
              ('timp', TIMPANI, 110, 6, 64)]
    for k, prog, vol, ch, pan in layout:
        song.add(parts[k], prog, vol, ch, pan)
    for k, prog, vol, ch, pan in (('delay', DELAY, 30, 10, 88), ('sub', SUB, 60, 11, 64), ('shaker', SHAKER, 34, 12, 70),
                                  ('riser', RISER, 44, 13, 64)):
        song.add(parts[k], prog, vol, ch, pan)
        layout.append((k, prog, vol, ch, pan))
    song.add(sorted(parts['drums'] + parts['hats']), DRUMS, 104, 9)
    written = {k for k, *_ in layout} | {'drums', 'hats'}
    assert not [k for k in parts if parts[k] and k not in written], 'partij niet weggeschreven'
    song.save(OUT, END * BAR)
    print(OUT)


if __name__ == '__main__':
    build()
