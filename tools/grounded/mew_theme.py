#!/usr/bin/env python3
"""Project Grounded: Battle! Mew v2, remix van Battle! Mewtwo (mewtwo_theme.py) met het karakter omgedraaid (Jordi:
"minder evil, minder sinister, curious, geen kloon, originator gevoel").

v1 (132 bpm, A-lydisch, glockenspiel-antwoorden een octaaf hoger, hikje elke 4e maat) -> Jordi: "die tonen klinken
raar, te hoog, niet in een goed tempo, maak het meer fluïde". v2:
- Gewoon A-groot (geen lydische D#), Mewtwo's Bb-maat wordt B-mineur; geen glockenspiel meer.
- Lager register: motief A4-F#5, de hook een octaaf lager dan in Mewtwo (E4-E5), fluit + strijkers unisono.
- Vloeiend: Mewtwo's staccato-16en worden legato-8en (elke frase 2 maten), doorrollende harp-arpeggio's door het
  hele nummer (ook in de intro en de overgangen), golvende bas (grondtoon-kwint-octaaf), geen stops of hikjes.
- Twee gevoelens (FEEL): '44' = 156 bpm, rollende 4/4 zonder four-on-the-floor (kick 1, 2-en, 3);
  '128' = 12/8-wiegen op 120 bpm (8en geswingd tot triolen, triool-arpeggio's).
Vorm zoals Mewtwo: intro (2 maten motief + 2 adem-/aanloopmaten voor de cry), A (motief), B (breakdown, de
melancholische frase in groot met een gespiegelde tegenstem op de strijkers), C (de hook), loop naar A.
voicegroup_grounded_mew = grounded_mewtwo met een kortere harp-release (242 -> 200), anders vreten de arpeggio's kanalen.
Gebruik: python3 tools/grounded/mew_theme.py [44|128] [uit.mid]   (standaard: het gekozen gevoel naar mus_grounded_vs_mew.mid)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

FEEL = '44'                     # gekozen gevoel voor de game
OUT = 'sound/songs/midi/mus_grounded_vs_mew.mid'
VG = 'grounded_mew'
TPB = 96
BAR = TPB * 4
E8 = TPB // 2
FLUTE, STRINGS, HARP, CHOIR, BASS, DRUMS = 72, 48, 46, 52, 32, 127
SUB, SHAKER = 84, 120           # PSG
KICK, SNARE, HH, OHH, CRASH, TAMB = 36, 38, 42, 46, 57, 54
A_START, B_START, C_START, END = 4, 12, 20, 28
MAX_DS = 11

N = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}


def p(name):
    if isinstance(name, int):
        return name
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


CH = {'A': ('A', ['A3', 'C#4', 'E4']), 'Bm': ('B', ['B3', 'D4', 'F#4']), 'E': ('E', ['B3', 'E4', 'G#4']),
      'D': ('D', ['A3', 'D4', 'F#4']), 'F#m': ('F#', ['A3', 'C#4', 'F#4'])}
# elke akkoord duurt 2 maten (de frases zijn 2 maten lang)
PROG = {}
for b in range(A_START, B_START):
    PROG[b] = ['A', 'Bm', 'A', 'E'][(b - A_START) // 2]          # Mewtwo: Am Bb Am E
for b in range(B_START, C_START):
    PROG[b] = ['D', 'A', 'Bm', 'E'][(b - B_START) // 2]          # Mewtwo: Dm Am Bb E
for b in range(C_START, END):
    PROG[b] = ['A', 'F#m', 'D', 'E'][(b - C_START) // 2]         # Mewtwo: Am F C G (Am F C E)
PROG.update({0: 'A', 1: 'Bm', 2: 'A', 3: 'E'})


def phrase(pattern, bar, vel, shift=0):
    """pattern in 8en over 2 maten: [(stap, lengte, 'A4')]."""
    return [[bar * BAR + st * E8, bar * BAR + (st + ln) * E8, p(n) + shift, vel] for st, ln, n in pattern]


# --- melodieën: Mewtwo's contouren, in A-groot, legato in 8en -----------------------------------------------------
MOTIF = {
    'A': [(0, 2, 'A4'), (2, 1, 'A4'), (3, 2, 'C#5'), (5, 1, 'A4'), (6, 2, 'B4'), (8, 2, 'A4'), (10, 1, 'E5'),
          (11, 1, 'D5'), (12, 2, 'C#5'), (14, 2, 'B4')],
    'Bm': [(0, 2, 'B4'), (2, 1, 'B4'), (3, 2, 'D5'), (5, 1, 'B4'), (6, 2, 'C#5'), (8, 2, 'D5'), (10, 1, 'F#5'),
           (11, 1, 'E5'), (12, 2, 'D5'), (14, 2, 'C#5')],
    'E': [(0, 2, 'G#4'), (2, 2, 'B4'), (4, 2, 'E5'), (6, 2, 'F#5'), (8, 6, 'E5'), (14, 1, 'D5'), (15, 1, 'C#5')],
}
SAD = {   # B: Mewtwo's melancholische frases, in groot
    'D': [(0, 8, 'F#5'), (8, 8, 'E5')], 'A': [(0, 12, 'C#5'), (12, 4, 'E5')],
    'Bm': [(0, 8, 'D5'), (8, 6, 'F#5'), (14, 2, 'E5')], 'E': [(0, 12, 'E5'), (12, 2, 'D5'), (14, 2, 'B4')],
}
HOOK = {   # C: Mewtwo's hook, een octaaf lager (shift -12 in build), in 8en
    'A': [(0, 3, 'E5'), (3, 3, 'A5'), (6, 2, 'C#6'), (8, 3, 'B5'), (11, 3, 'A5'), (14, 2, 'E5')],
    'F#m': [(0, 3, 'F#5'), (3, 3, 'A5'), (6, 2, 'C#6'), (8, 3, 'A5'), (11, 3, 'G#5'), (14, 2, 'F#5')],
    'D': [(0, 3, 'F#5'), (3, 3, 'A5'), (6, 2, 'D6'), (8, 3, 'E6'), (11, 3, 'D6'), (14, 2, 'A5')],
    'E': [(0, 4, 'B5'), (4, 2, 'A5'), (6, 2, 'G#5'), (8, 4, 'E5'), (12, 2, 'G#5'), (14, 2, 'B5')],
}
INTRO = [(0, 2, 'A4'), (2, 2, 'C#5'), (4, 4, 'E5'), (8, 2, 'D5'), (10, 2, 'C#5'), (12, 4, 'B4')]   # het DNA: een vraag


def invert(pattern):
    """Gespiegeld rond de eerste noot, in A-groot (Mew probeert het andersom)."""
    scale = [n for n in range(128) if n % 12 in (9, 11, 1, 2, 4, 6, 8)]
    idx = lambda n: min(range(len(scale)), key=lambda i: abs(scale[i] - n))
    ax = idx(p(pattern[0][2]))
    return [(st, ln, scale[2 * ax - idx(p(nm))]) for st, ln, nm in pattern]


def warp(t, feel):
    """12/8: elke tel = 3 triolen; een 8e op de 'en' schuift naar de derde triool (lang-kort)."""
    b, r = divmod(t, TPB)
    if feel != '128' or r % 24:          # noten op het triool-raster (arpeggio's, hats) blijven staan
        return t
    return b * TPB + (r * 64 // 48 if r < 48 else 64 + (r - 48) * 32 // 48)


def build(feel=FEEL, out=OUT):
    bpm = 156 if feel == '44' else 120
    sub = 2 if feel == '44' else 3          # arpeggio-noten per tel
    step = TPB // sub
    parts = {k: [] for k in ('flute', 'str', 'harp', 'pad', 'choir', 'bass', 'drums', 'sub', 'shaker')}

    for b in range(0, END):
        t0 = b * BAR
        ch = PROG[b]
        root, chord = CH[ch]
        r = 12 * 3 + N[root] if N[root] >= 4 else 12 * 4 + N[root]      # E2..D#3
        intro = b < A_START
        # doorrollende harp: akkoord op en neer over 2 octaven (A3..A5), het lijmt alles aan elkaar
        tones = sorted(p(x) for x in chord) + sorted(p(x) + 12 for x in chord)
        wave = tones + tones[-2:0:-1]
        n = 4 * sub
        for i in range(n):
            s = t0 + i * step
            v = (44 + b * 6) if intro else 64 if b < B_START else 58 if b < C_START else 66
            parts['harp'] += [[s, s + step, wave[(i + (b % 2) * n) % len(wave)], min(v, 66)]]
        # strijkers/pad: zacht aangehouden (2 tonen), koor alleen in B en C
        held = BAR - E8 if intro else 2 * BAR - E8          # aangehouden over het hele akkoord (2 maten), los vóór het volgende
        if b >= 1 and (intro or b % 2 == 0):
            parts['pad'] += [[t0, t0 + held, p(x), 52 if intro else 62] for x in (chord[:2] if intro else chord[1:2])]
        if B_START <= b < C_START and b % 2 == 0:
            parts['choir'] += [[t0, t0 + held, p(chord[-1]) + 12, 70]]
        # bas: golvend grondtoon-kwint-octaaf-kwint in 8en (vanaf de aanloopmaat)
        if b >= 3:
            fig = [0, 7, 12, 7, 0, 7, 12, 14] if b % 2 == 0 else [0, 7, 12, 7, 0, 12, 7, 5]
            bv = 72 if b == 3 else 100 if b < B_START else 84 if b < C_START else 106
            if B_START <= b < C_START:
                fig = [0, None, 7, None, 12, None, 7, None]               # breakdown: luchtiger
            for i, iv in enumerate(fig):
                if iv is None:
                    continue
                ln = 2 * E8 if B_START <= b < C_START else E8
                parts['bass'] += [[t0 + i * E8, t0 + i * E8 + ln - 6, r + iv, bv]]
        # drums: rollend, geen four-on-the-floor
        if b >= A_START and not (B_START <= b < C_START - 1):
            v = 108 if b >= C_START else 100
            kicks = (0, 3, 4) if feel == '44' else (0, 4)                 # in 8en: 1, 2-en, 3
            parts['drums'] += [[t0 + k * E8, t0 + k * E8 + E8, KICK, v] for k in kicks]
            parts['drums'] += [[t0 + k * E8, t0 + k * E8 + E8, KICK, v - 20] for k in ((7,) if feel == '44' else (6, 7))]
            parts['drums'] += [[t0 + i * TPB, t0 + i * TPB + E8, SNARE, 70] for i in (1, 3)]
            if b >= C_START:
                parts['drums'] += [[t0 + i * TPB, t0 + i * TPB + E8, TAMB, 66] for i in (1, 3)]
            for i in range(4 * sub):
                if sub == 3 and i % 3 == 1:
                    continue                                              # 12/8: hats lang-kort (shuffle-ride)
                parts['drums'] += [[t0 + i * step, t0 + i * step + step // 2, HH, 58 if i % sub else 44]]
            if b in (A_START, C_START):
                parts['drums'] += [[t0, t0 + 2 * TPB, CRASH, 96]]
        if B_START <= b < C_START - 1 and b % 2 == 0:                     # breakdown: alleen een zachte kick per 2 maten
            parts['drums'] += [[t0, t0 + E8, KICK, 70]]
        if b == 3 or b == C_START - 1:                                    # zachte aanloop (snare in 8en, crescendo)
            parts['drums'] += [[t0 + i * step, t0 + i * step + step // 2, SNARE, 36 + i * 4] for i in range(4 * sub)]
        if b == A_START - 1:
            parts['drums'] += [[t0, t0 + E8, KICK, 80], [t0 + 2 * TPB, t0 + 2 * TPB + E8, KICK, 86]]
        # PSG: sub-bas en shaker
        if b >= A_START:
            parts['sub'] += [[t0, t0 + BAR - 6, 12 * 3 + N[root], 80 if not (B_START <= b < C_START) else 60]]
            if not (B_START <= b < C_START):
                parts['shaker'] += [[t0 + i * step, t0 + i * step + 6, 84, 70 if i % sub == sub - 1 else 40]
                                    for i in range(4 * sub)]

    # melodie
    parts['flute'] += phrase(INTRO, 0, 84)
    for b in range(A_START, END, 2):
        ch = PROG[b]
        if b < B_START:
            parts['flute'] += phrase(MOTIF[ch], b, 104)
        elif b < C_START:
            parts['flute'] += phrase(SAD[ch], b, 96)
            # de tegenstem: dezelfde frase gespiegeld, een octaaf lager op de strijkers, een maat later
            parts['str'] += [[s + BAR, min(e + BAR, (b + 2) * BAR + BAR // 2), n - 12, 70]
                             for s, e, n, v in phrase(invert(SAD[ch]), b, 70) if s + BAR < C_START * BAR]
        else:
            parts['flute'] += phrase(HOOK[ch], b, 112, shift=-12)
            parts['str'] += phrase(HOOK[ch], b, 80, shift=-12)             # unisono: warm, niet schel

    for k in parts:
        parts[k] = dedupe([[warp(s, feel), max(warp(s, feel) + 6, warp(e, feel)), n, v] for s, e, n, v in parts[k]])

    # voicegroup: grounded_mewtwo met een kortere harp
    lines = open('sound/voicegroups/grounded_mewtwo.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_mewtwo met een kortere harp-release (46) voor Battle! Mew.'
    lines[1] = '@ Gegenereerd door tools/grounded/mew_theme.py.'
    lines[2] = 'voice_group %s' % VG
    lines = [('\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_harp, 255, 242, 51, 200  @ 46'
              if l.rstrip().endswith('@ 46') else l) for l in lines]
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(lines))

    rel = releases(VG)
    progs = {'flute': FLUTE, 'str': STRINGS, 'harp': HARP, 'pad': STRINGS, 'choir': CHOIR, 'bass': BASS}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, bpm) for k, pr in progs.items()}
    tail['drums'] = 0
    for k in ('flute', 'str', 'choir'):
        parts[k] = detach(parts[k], tail[k])
    order = ['flute', 'bass', 'drums', 'str', 'pad', 'choir', 'harp']
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
    song.tempo(0, bpm / 120)
    song.loop = (A_START * BAR, END * BAR)
    layout = [('flute', FLUTE, 104, 0, 64), ('str', STRINGS, 70, 1, 76), ('harp', HARP, 78, 2, 48),
              ('pad', STRINGS, 60, 3, 64), ('choir', CHOIR, 56, 4, 64), ('bass', BASS, 108, 5, 64),
              ('sub', SUB, 38, 6, 64), ('shaker', SHAKER, 26, 7, 72)]
    for k, prog, vol, chn, pan in layout:
        song.add(parts[k], prog, vol, chn, pan)
    song.add(sorted(parts['drums']), DRUMS, 92, 9)
    assert not [k for k in parts if parts[k] and k not in {x[0] for x in layout} | {'drums'}]
    song.save(out, END * BAR)
    print(out, feel, bpm)


if __name__ == '__main__':
    f = sys.argv[1] if len(sys.argv) > 1 else FEEL
    build(f, sys.argv[2] if len(sys.argv) > 2 else OUT)
