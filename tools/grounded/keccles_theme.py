#!/usr/bin/env python3
"""Project Grounded: "Battle! Keccles", een eigen compositie in salsa dura-stijl (Fania, Willie Colón, Héctor Lavoe).
Keccles is een Kecleon met een PhD en existentiële angst; hij vecht op een harde New York-salsa.

190 bpm (4/4, in 'cut time' gedacht), A-mineur, clave 2-3 (even maten = 2-kant, oneven = 3-kant).
  maat 0-1   intro: piano-montuno + clave + güiro, conga's komen erbij
  maat 2     bloque: koperstoten op de clave (E7)
  maat 3     koperloop omhoog + timbale-abanico            (= maat 51, zodat de loop naadloos is)
Loop (48 maten, ±60 s):
  A  4-19    de hook: trompet + trombone in octaven (arpeggio omhoog, G#-draaitje); 2e helft met een tweede trompet
  B  20-31   'coro': trombone-melodie over Dm7-G7-Cmaj7-Fmaj7-Bm7b5-E7-Am, trompetstoten op de clave
  M  32-47   mambo: trombone-moña, campana, trompetten eerst op de clave, dan een eigen tegenmelodie
  break 48-51 bloque-stoten, timbalesolo, koperloop -> terug naar A
Bas = tumbao (2+ en 4, anticipeert de volgende maat), conga = tumbao (slap op 2, open tonen op 4 en 4+),
timbales = cascara op de zijkant (A/B), fills naar elke nieuwe sectie. Güiro op het PSG-ruiskanaal (kost geen
DirectSound-kanaal).

Voicegroup grounded_keccles (gegenereerd) = grounded_gm met: 0 = piano met korte release (montuno-stoten),
57 = trompet-keysplit (trombone-ligging, nooit onder C3), 121 = güiro (ruis), 127 = eigen salsa-drumkit
(drumsets/keccles.inc, alles DirectSound, geen PSG-piepjes).
Zie tools/grounded/MUZIEK.md. Gebruik: python3 tools/grounded/keccles_theme.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

OUT = 'sound/songs/midi/mus_grounded_vs_keccles.mid'
VG = 'grounded_keccles'
TPB, BPM = 48, 190
E = TPB // 2                   # een achtste
S16 = TPB // 4
BAR = TPB * 4
PIANO, TRUMPET, TROMBONE, BASS, GUIRO, DRUMS = 0, 56, 57, 33, 121, 127
# eigen drumkit (drumsets/keccles.inc, vanaf noot 36)
KICK, CLAVE, CASCARA, HEMBRA, MACHO, CAMPANA, SLAP, TUMBA, CONGA_HI, CRASH, RIM = range(36, 47)

A0, B0, M0, K0, END = 4, 20, 32, 48, 52      # secties (maat); de loop = maat 4-52

N = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def p(name):
    """'A4' -> midi-noot (C4 = 60)."""
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


CH = {'Am': [9, 0, 4], 'Dm': [2, 5, 9], 'E7': [4, 8, 11, 2], 'Dm7': [2, 5, 9, 0], 'G7': [7, 11, 2, 5],
      'Cmaj7': [0, 4, 7, 11], 'Fmaj7': [5, 9, 0, 4], 'Bm7b5': [11, 2, 5, 9]}
PROG = (['Am', 'Dm', 'E7', 'E7']
        + ['Am', 'Am', 'Dm', 'E7'] * 4
        + ['Dm7', 'G7', 'Cmaj7', 'Fmaj7', 'Bm7b5', 'E7', 'Am', 'Am', 'Dm', 'E7', 'Am', 'E7']
        + ['Am', 'Dm', 'E7', 'Am'] * 4
        + ['Dm', 'E7', 'E7', 'E7'])
assert len(PROG) == END

SCALE = [9, 11, 0, 2, 4, 5, 8]          # A harmonisch mineur


def third_below(n):
    """Diatonische terts onder n (A harmonisch mineur): de tweede trompet."""
    for d in range(1, 6):
        if (n - d) % 12 in SCALE:
            lo = n - d
            break
    for d in range(1, 6):
        if (lo - d) % 12 in SCALE:
            return lo - d
    return n - 3


def mel(pattern, bar, vel=116, shift=0):
    """[(achtste, lengte in achtsten, 'A4'), ...] -> punchy koper: korte noten staccato."""
    out = []
    for st, ln, nm in pattern:
        s = bar * BAR + st * E
        dur = int(E * 0.7) if ln == 1 else ln * E - 6
        out.append([s, s + dur, p(nm) + shift, vel + (6 if st in (0, 3) else 0)])
    return out


# ---- melodieën -----------------------------------------------------------------------------------------------------
HOOK = [   # A: de hook (4 maten: Am Am Dm E7); de vierde maat verschilt per herhaling
    [(0, 1, 'A4'), (1, 1, 'C5'), (2, 1, 'E5'), (3, 2, 'A5'), (5, 1, 'G#5'), (6, 1, 'A5'), (7, 1, 'C6')],
    [(1, 1, 'B5'), (2, 1, 'A5'), (3, 1, 'E5'), (4, 2, 'F5'), (6, 1, 'E5')],
    [(0, 1, 'D5'), (1, 1, 'F5'), (2, 1, 'A5'), (3, 2, 'D6'), (5, 1, 'C6'), (6, 1, 'B5'), (7, 1, 'A5')],
]
HOOK_END = [[(1, 1, 'G#5'), (2, 1, 'B5'), (3, 1, 'D6'), (4, 3, 'E6')],                       # open (vraag)
            [(1, 1, 'G#5'), (2, 1, 'B5'), (3, 1, 'D6'), (4, 1, 'C6'), (5, 1, 'B5'), (6, 2, 'G#5')]]  # naar de herhaling
CORO = [   # B: trombone-melodie (een octaaf onder de trompetligging), lang en zangerig
    [(0, 3, 'F5'), (3, 3, 'A5'), (6, 2, 'C6')],
    [(0, 4, 'B5'), (4, 2, 'D6'), (6, 2, 'F5')],
    [(0, 6, 'E5'), (6, 2, 'D5')],
    [(0, 4, 'C5'), (4, 2, 'A4'), (6, 2, 'C5')],
    [(0, 3, 'D5'), (3, 3, 'F5'), (6, 2, 'A5')],
    [(0, 4, 'G#5'), (4, 2, 'F5'), (6, 2, 'D5')],
    [(0, 7, 'C5')],
    [(0, 2, 'E5'), (3, 1, 'C5'), (4, 1, 'E5'), (5, 1, 'A5'), (6, 2, 'G#5')],
    [(0, 1, 'A5'), (1, 1, 'F5'), (2, 1, 'D5'), (3, 2, 'F5'), (5, 1, 'E5'), (6, 2, 'D5')],
    [(0, 1, 'B4'), (1, 1, 'D5'), (2, 1, 'E5'), (3, 2, 'G#5'), (5, 1, 'B5'), (6, 2, 'D6')],
    [(0, 3, 'C6'), (3, 1, 'B5'), (4, 1, 'A5'), (5, 1, 'E5'), (6, 2, 'C5')],
    [(0, 1, 'B4'), (1, 1, 'D5'), (2, 1, 'E5'), (3, 1, 'G#5'), (4, 1, 'B5'), (5, 1, 'D6'), (6, 1, 'E6')],
]
MONA = {   # mambo: trombone-moña (ostinato)
    'Am': [(1, 1, 'E4'), (2, 1, 'E4'), (3, 1, 'A4'), (5, 1, 'E4'), (6, 2, 'G4')],
    'Dm': [(0, 1, 'F4'), (1, 1, 'A4'), (3, 1, 'F4'), (4, 1, 'D4'), (6, 2, 'F4')],
    'E7': [(1, 1, 'G#4'), (2, 1, 'G#4'), (3, 1, 'B4'), (5, 1, 'G#4'), (6, 2, 'D4')],
    'Am2': [(0, 2, 'C4'), (3, 1, 'E4'), (4, 1, 'A3'), (6, 1, 'A3'), (7, 1, 'C4')],
}
MAMBO_TPT = {   # mambo, tweede helft: tegenmelodie van de trompetten in de gaten van de moña
    'Am': [(0, 2, 'C6'), (3, 1, 'B5'), (4, 1, 'A5'), (6, 2, 'E5')],
    'Dm': [(0, 2, 'D6'), (3, 1, 'C6'), (4, 1, 'A5'), (6, 2, 'F5')],
    'E7': [(0, 1, 'E6'), (1, 1, 'D6'), (2, 1, 'B5'), (3, 1, 'G#5'), (4, 1, 'E5'), (5, 1, 'F5'), (6, 2, 'G#5')],
    'Am2': [(0, 3, 'A5'), (4, 1, 'C6'), (5, 1, 'B5'), (6, 1, 'A5'), (7, 1, 'E5')],
}
RUN = [(i, 1, nm) for i, nm in enumerate(['E4', 'G#4', 'B4', 'D5', 'E5', 'F5', 'G#5', 'B5'])]   # koperloop omhoog
BLOQUE = {'Dm': ('A5', 'F5', 'D4'), 'E7': ('B5', 'G#5', 'E4')}


def clave_pos(bar):
    return (2, 4) if bar % 2 == 0 else (0, 3, 6)     # 2-3: even maat = 2-kant


def build():
    parts = {k: [] for k in ('tpt', 'tpt2', 'trb', 'piano', 'bass', 'clave', 'conga', 'bell', 'timb', 'crash', 'guiro')}

    def hit(part, bar, e8, note, vel, ln=S16):
        s = bar * BAR + int(e8 * E)
        parts[part].append([s, s + ln, note, vel])

    def bloque(bar, chord, positions, vel=120):
        lead, second, low = BLOQUE[chord]
        for e8 in positions:
            hit('tpt', bar, e8, p(lead), vel, int(E * 0.7))
            hit('tpt2', bar, e8, p(second), vel - 8, int(E * 0.7))
            hit('trb', bar, e8, p(low), vel - 4, int(E * 0.7))
            hit('bass', bar, e8, bass_root(CH[chord][0]), 120, int(E * 0.8))
            for o in (0, 12):
                hit('piano', bar, e8, p(lead) - 12 + o, 100, int(E * 0.5))
            hit('timb', bar, e8, RIM, 110)

    def run(bar):        # maat 3 = maat 51: koperloop + abanico, eindigt precies op de maatgrens
        parts['tpt'] += mel(RUN, bar, 112)
        parts['trb'] += mel(RUN, bar, 108, shift=-12)
        hit('bass', bar, 0, bass_root(4), 118, int(E * 0.8))
        hit('bass', bar, 4, bass_root(4) + 12, 110, int(E * 0.8))
        for k in range(4):                                             # abanico: rimshot-roffel naar de crash
            hit('timb', bar, 6 + k * 0.5, RIM if k % 2 else MACHO, 90 + k * 10)

    # ---- intro + break -------------------------------------------------------------------------------------------
    bloque(2, 'E7', (0, 3, 6))
    bloque(K0, 'Dm', (0, 3, 6))
    bloque(K0 + 1, 'E7', (2, 4, 6, 7))
    hit('crash', K0, 0, CRASH, 110, E)
    for k in range(16):                                                 # timbalesolo (maat 50)
        nt = [MACHO, MACHO, HEMBRA, RIM][k % 4] if k < 12 else [HEMBRA, HEMBRA, MACHO, RIM][k - 12]
        hit('timb', K0 + 2, k * 0.5, nt, 70 + k * 3 + (14 if k % 4 == 0 else 0))
    run(3)
    run(END - 1)

    # ---- bas (tumbao), piano (montuno) ----------------------------------------------------------------------------
    for b in range(END):
        ch, nxt = PROG[b], PROG[(b + 1) if b + 1 < END else A0]
        root, nroot = CH[ch][0], CH[nxt][0]
        rhythm = (A0 <= b < K0) or b == 1
        if rhythm:
            if b in (1, A0, B0, M0):
                hit('bass', b, 0, bass_root(root), 116, 3 * E - 6)
            hit('bass', b, 3, fifth(root), 108, 3 * E - 6)
            # 4: de grondtoon van de volgende maat, doorgehouden over de maatgrens (anticipatie)
            ln = 2 * E - 6 if b + 1 in (K0, 2) else 5 * E - 6
            hit('bass', b, 6, bass_root(nroot), 120, ln)
        if b < 2 or (A0 <= b < K0):
            montuno(parts, b, ch, nxt, 92 if b < 2 else 86)

    # ---- koper ---------------------------------------------------------------------------------------------------
    for i in range(16):                                                 # A: hook, 4 keer
        b = A0 + i
        k = i % 4
        pat = HOOK[k] if k < 3 else HOOK_END[0] if i in (3, 11) else HOOK_END[1]   # vraag, antwoord
        parts['tpt'] += mel(pat, b, 114)
        parts['trb'] += mel(pat, b, 108, shift=-12)
        if i >= 8:                                                      # tweede helft: tweede trompet (tertsen)
            parts['tpt2'] += [[s, e, third_below(n), v - 16] for s, e, n, v in mel(pat, b, 114)]
    for i, pat in enumerate(CORO):                                      # B: trombone zingt, trompetten steken
        b = B0 + i
        parts['trb'] += mel(pat, b, 112, shift=-12)
        if i >= 8:                                                      # opbouw naar de mambo: trompet erbij
            parts['tpt'] += mel(pat, b, 108)
        else:
            tones = CH[PROG[b]]
            for e8 in clave_pos(b):
                for part, idx, v in (('tpt', 1, 104), ('tpt2', 3 if len(tones) > 3 else 2, 96)):
                    hit(part, b, e8, top(tones[idx], 74, 86), v, int(E * 0.6))
    for i in range(16):                                                 # mambo
        b = M0 + i
        key = PROG[b] if i % 4 != 3 else 'Am2'
        parts['trb'] += mel(MONA[key], b, 116)
        if 4 <= i < 8:                                                  # trompetten op de clave
            for e8 in clave_pos(b):
                tones = CH[PROG[b]]
                hit('tpt', b, e8, top(tones[1], 76, 88), 112, int(E * 0.6))
                hit('tpt2', b, e8, top(tones[2], 72, 84), 100, int(E * 0.6))
        elif i >= 8:                                                    # tegenmelodie, in tertsen
            parts['tpt'] += mel(MAMBO_TPT[key], b, 116)
            parts['tpt2'] += [[s, e, third_below(n), v - 14] for s, e, n, v in mel(MAMBO_TPT[key], b, 116)]

    # ---- percussie -----------------------------------------------------------------------------------------------
    for b in range(END):
        for e8 in clave_pos(b):
            hit('clave', b, e8, CLAVE, 104)
        if b >= 1 and b != K0 + 2:                                      # conga-tumbao (niet in de timbalesolo)
            soft = 0 if b >= A0 else -20
            for e8, nt, v in ((0, SLAP, 46), (2, SLAP, 112), (4, SLAP, 46), (6, TUMBA, 104),
                              (7, CONGA_HI if b % 2 else TUMBA, 100)):
                if b in (2, 3, K0, K0 + 1) and e8 != 2:
                    continue                                            # bloque/loop: alleen de slap
                hit('conga', b, e8, nt, v + soft, S16 + 4)
            if M0 <= b < K0:
                hit('conga', b, 5, CONGA_HI, 84, S16 + 4)
        if (A0 <= b < M0) or b in (0, 1):                               # cascara op de zijkant van de timbales
            for e8 in ((0, 2, 4, 5, 7) if b % 2 == 0 else (0, 2, 3, 5, 7)):
                hit('bell', b, e8, CASCARA, 92 if e8 in clave_pos(b) else 64, S16)
        if M0 <= b < K0:                                                # campana in de mambo
            for e8, v in ((0, 112), (2, 86), (3, 70), (4, 106), (6, 86), (7, 70)):
                hit('bell', b, e8, CAMPANA, v, E - 4)
        rel = b - A0
        if A0 <= b < K0 and rel % 4 == 3 and b + 1 not in (B0, M0, K0):  # kleine fill elke 4 maten
            for k, nt in enumerate((MACHO, MACHO, HEMBRA, HEMBRA)):
                hit('timb', b, 6 + k * 0.5, nt, 84 + k * 6)
        if b + 1 in (B0, M0, K0):                                       # grote fill naar een nieuwe sectie
            for k in range(8):
                hit('timb', b, 4 + k * 0.5, [MACHO, HEMBRA][k // 4] if k < 7 else RIM, 80 + k * 6)
        if b in (A0, B0, M0):
            hit('crash', b, 0, CRASH, 112, E)
            hit('timb', b, 0, RIM, 112)
        # güiro (PSG-ruis): lang-kort-kort per tel
        if b < K0 or b == END - 1 or b in (2, 3):
            for beat in range(4):
                s = b * BAR + beat * TPB
                parts['guiro'] += [[s, s + 18, 76, 70], [s + E, s + E + 8, 79, 46], [s + E + S16, s + E + S16 + 8, 79, 46]]

    for k in parts:
        parts[k] = dedupe(parts[k])

    write_voicegroup()
    rel = releases(VG)
    progs = {'tpt': TRUMPET, 'tpt2': TRUMPET, 'trb': TROMBONE, 'piano': PIANO, 'bass': BASS}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) for k, pr in progs.items()}
    for k in ('clave', 'conga', 'bell', 'timb', 'crash'):
        tail[k] = 2
    for k in ('tpt', 'tpt2', 'trb', 'bass'):
        parts[k] = detach(parts[k], tail[k])
    order = ['tpt', 'trb', 'clave', 'bass', 'crash', 'timb', 'piano', 'conga', 'tpt2', 'bell']
    ds = {k: parts[k] for k in order}
    kept = allocate(ds, order, tail)
    print('tail (ticks):', tail)
    for k in order:
        n = len(ds[k])
        print('  %-6s %4d noten, %3d vallen weg (%.1f%%)' % (k, n, n - len(kept[k]), 100 * (n - len(kept[k])) / max(n, 1)))
        parts[k] = kept[k]

    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.loop = (A0 * BAR, END * BAR)
    layout = [('tpt', TRUMPET, 112, 0, 76), ('trb', TROMBONE, 104, 1, 52), ('tpt2', TRUMPET, 90, 2, 88),
              ('piano', PIANO, 92, 3, 40), ('bass', BASS, 118, 4, 64), ('guiro', GUIRO, 38, 5, 84)]
    for k, prog, vol, ch, pan in layout:
        song.add(parts[k], prog, vol, ch, pan)
    drums = ('clave', 'conga', 'bell', 'timb', 'crash')
    song.add(sorted(sum((parts[k] for k in drums), [])), DRUMS, 108, 9)
    written = {k for k, *_ in layout} | set(drums)
    assert not [k for k in parts if parts[k] and k not in written], 'partij niet weggeschreven'
    song.save(OUT, END * BAR)
    print(OUT, '%.1f s intro, %.1f s loop' % (A0 * 4 * 60 / BPM, (END - A0) * 4 * 60 / BPM))


def bass_root(pc):
    """Grondtoon tussen G1 (31) en F#2 (42)."""
    n = 24 + pc
    while n < 31:
        n += 12
    return n


def fifth(pc):
    r = bass_root(pc)
    return r + 7 if r + 7 <= 43 else r - 5


def top(pc, lo, hi):
    n = pc
    while n < lo:
        n += 12
    return n if n < hi else n - 12


def montuno(parts, b, ch, nxt, vel):
    """Piano-montuno in octaven: 2-maats-cel, gesyncopeerd, de laatste achtste anticipeert de volgende akkoord."""
    tones = sorted(top(pc, 64, 76) for pc in CH[ch][:3])
    ntones = sorted(top(pc, 64, 76) for pc in CH[nxt][:3])
    if b % 2 == 0:
        cell = [(0, tones[1]), (2, tones[0]), (3, tones[2]), (5, tones[1])]
    else:
        cell = [(1, tones[2]), (2, tones[1]), (4, tones[0]), (5, tones[1])]
    last = cell[-1][1]
    cell.append((7, min(ntones, key=lambda n: abs(n - last))))
    for e8, nt in cell:
        s = b * BAR + e8 * E
        for o in (0, 12):
            parts['piano'].append([s, s + 11, nt + o, vel + (8 if e8 in (2, 7) else 0)])


def write_voicegroup():
    """grounded_gm + piano met korte release (0), trompet als trombone (57), güiro (121), salsa-drumkit (127)."""
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Battle! Keccles (salsa dura). Gegenereerd door tools/grounded/keccles_theme.py.'
    lines[1] = '@ 0 = piano met korte release (montuno), 57 = trompet (trombone-ligging), 121 = güiro (ruis), 127 = salsa-drumkit.'
    lines[2] = 'voice_group %s' % VG
    repl = {
        '@ 0': '\tvoice_keysplit voicegroup_keccles_piano_keysplit, keysplit_piano  @ 0',
        '@ 57': '\tvoice_keysplit voicegroup_trumpet_keysplit, keysplit_trumpet  @ 57',
        '@ 121': '\tvoice_noise_alt 60, 0, 0, 0, 2, 6, 0  @ 121',
        '@ 127': '\tvoice_keysplit_all voicegroup_keccles_drumset  @ 127',
    }
    out = []
    for l in lines:
        tag = '@' + l.rsplit('@', 1)[1] if '@' in l and l.startswith('\t') else None
        out.append(repl.get(tag.strip() if tag else None, l))
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    open('sound/voicegroups/keysplits/keccles_piano.inc', 'w').write(
        '@ Project Grounded: piano met korte release voor de montuno van Battle! Keccles (keccles_theme.py).\n'
        'voice_group keccles_piano_keysplit\n'
        + ''.join('\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_piano1_%d, 255, 250, 0, 150\n' % k
                  for k in (48, 60, 72, 84)) + '\n')
    kit = [   # vanaf noot 36; alles DirectSound (geen PSG-piepjes)
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 0',          # 36 kick
        'voice_directsound 66, 64, DirectSoundWaveData_ethnic_flavours_hyoushigi, 255, 0, 255, 100',            # 37 clave
        'voice_directsound 79, 88, DirectSoundWaveData_ethnic_flavours_hyoushigi, 255, 0, 255, 80',             # 38 cascara
        'voice_directsound 70, 50, DirectSoundWaveData_unused_sc55_tom, 255, 220, 60, 140',                     # 39 timbal hembra
        'voice_directsound 77, 78, DirectSoundWaveData_unused_sc55_tom, 255, 220, 60, 140',                     # 40 timbal macho
        'voice_directsound_no_resample 64, 72, DirectSoundWaveData_sd90_cowbell, 255, 0, 255, 120',             # 41 campana
        'voice_directsound_no_resample 64, 54, DirectSoundWaveData_sc88pro_mute_high_conga, 255, 0, 255, 60',   # 42 conga slap
        'voice_directsound 60, 46, DirectSoundWaveData_sc88pro_open_low_conga, 255, 0, 255, 60',                # 43 tumbadora open
        'voice_directsound 66, 58, DirectSoundWaveData_sc88pro_open_low_conga, 255, 0, 255, 60',                # 44 conga open
        'voice_directsound_no_resample 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165',     # 45 crash
        'voice_directsound 72, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 100',              # 46 rimshot
    ]
    open('sound/voicegroups/drumsets/keccles.inc', 'w').write(
        '@ Project Grounded: salsa-drumkit voor Battle! Keccles (keccles_theme.py): 36 kick, 37 clave, 38 cascara,\n'
        '@ 39/40 timbales (hembra/macho), 41 campana, 42 conga slap, 43 tumbadora, 44 conga open, 45 crash, 46 rimshot.\n'
        'voice_group keccles_drumset, 36\n' + ''.join('\t%s\n' % k for k in kit) + '\n')


if __name__ == '__main__':
    build()
