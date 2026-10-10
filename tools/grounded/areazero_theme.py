#!/usr/bin/env python3
"""Project Grounded: Area Zero (Pokémon Scarlet/Violet), nagebouwd in GBA-stijl (MUS_GROUNDED_AREA_ZERO, 681).

Bron: het origineel (Spleeter-stems) + een 8-bit VRC6-cover; alles gemeten met de scripts in de scratchpad
(agent_areazero/: seg.py, ridge.py, onsets.py, peakroll.py, drums.py). 120 bpm, Eb-klein, 64 maten = 128 s, het hele
nummer loopt (ook de bijna stille opening). Maat 1 = 0,185 s in het origineel.
Vorm (maten, 1-geteld):
   1-7   kristal-arpeggio alleen (F6 F#6 C#6 Eb6 | Ab5 C#6 Eb6 Ab6 in achtsten), vanaf m5 de hoge 'cel' C#7-Eb7-Ab6
   8-10  koor + strijkers: Eb (sus2), opmaat F4
  10-11  PAUZE: alleen belletjes + een spookakkoord (Ab3 C#4 Eb4) heel zacht
  12-15  B (Cb) maj9: koor F#5 Bb5 C#6, bas B
  16-18  Eb: koor unisono F4 (glijdt in m17 naar F#4)
  18-19  PAUZE
  20-23  B
  24-39  aria (de 'stem'; hier een GBA-blokgolf, géén stem) boven Ab (Bbm7/Ab) en B; drums vanaf m24
  40-63  groove op een Eb-orgelpunt: 4-maats frase (a b c d), kristal-arpeggio met C/G (dorisch), koorzuchten die
         een halve toon omlaag glijden, blokgolf-ostinato Bb-C#-Bb-F; m55/m63 = B -> Db (bVI-bVII) naar Eb
  64     Db/Ab, uitsterven -> terug naar het begin
Uncanny (Jordi: 'trillingen, de pauzes tussendoor, wel met koren'):
  - de lead zingt in het origineel systematisch ±0,4 halve toon te hoog met een brede vibrato (gemeten, mediaan per
    noot, zie LEAD); dat zit erin als pitch bend per noot + MOD-vibrato. LEAD_DETUNE = 0 zet het uit.
  - koor met lichte MOD-tremolo; zuchten met een bend van een halve toon omlaag.
Laag: bas op de PSG-golf (driehoek, ProgrammableWaveData_2), nooit onder C2 (PSG klemt) en een octaaf boven het origineel
(Eb1/B1/Ab1 -> Eb2/B2/Ab2): geen 'overload' op Jordi's speakers.
Instrumenten (eigen voicegroup grounded_area_zero op basis van grounded_gm):
  lead   sc88pro_square_wave (DS)            koor  classical_choir_voice_ahhs (DS, MOD)
  strijk eigen keysplit (zachte aanzet)       bel   az_crystal (eigen sample, areazero_samples.py)
  ost    PSG-blokgolf 1 (25%)                 echo  PSG-blokgolf 2 (12,5%), belletjes 3 zestienden later
  bas    PSG-golf (driehoek)                  hats  PSG-ruis (eigen spoor, niet in de kit)
  kit    drumsets/area_zero.inc: kick (rnd_kick), snare (rnd_snare)
Gebruik: python3 tools/grounded/areazero_theme.py [--render <map>]"""
import os, subprocess, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

OUT = 'sound/songs/midi/mus_grounded_area_zero.mid'
VG = 'grounded_area_zero'
TPB, BPM = 96, 120
S = TPB // 4                 # zestiende
BAR = TPB * 4
NBARS = 64
MAXV = 10
LEAD_DETUNE = 1.0            # 1 = zoals gemeten (±0,4 halve toon te hoog), 0 = zuiver
LFOS = 24                    # vibratosnelheid: in de game gemeten 30 -> ±8 Hz, origineel ±6 Hz
LEAD_MOD, CHOIR_MOD, SIGH_MOD = 14, 6, 10   # in de game gemeten: MOD 6 gaf std 0,08 halve toon, origineel 0,33

# programma's (grounded_gm-nummering, eigen invulling)
BELL, STR, CHOIR, SIGH, OST, ECHO, LEAD, BASS, HAT, DRUMS = 9, 48, 52, 53, 80, 81, 82, 84, 121, 127
KICK, SNARE = 36, 38

N = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'Ab': 8, 'A': 9,
     'Bb': 10, 'B': 11}


def p(name):
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


def T(bar, pos=0):
    """tick van maat (1-geteld) + zestiende."""
    return (bar - 1) * BAR + pos * S


# ---- kristal-arpeggio (bellen), per maat: [(zestiende, noot)] -------------------------------------------------
INTRO = [(0, 'F6'), (2, 'F#6'), (4, 'C#6'), (6, 'Eb6'), (8, 'Ab5'), (10, 'C#6'), (12, 'Eb6'), (14, 'Ab6')]
INTRO4 = INTRO[:7] + [(13, 'Eb7'), (14, 'C#7')]
INTRO5 = [(0, 'F6'), (2, 'F#6'), (4, 'C#7'), (6, 'Eb7'), (8, 'Ab6'), (10, 'C#7'), (12, 'Eb7'), (14, 'C#7')]
CELL = [(4, 'C#7'), (6, 'Eb7'), (8, 'Ab6'), (12, 'Eb7'), (14, 'C#7')]            # m6-7, pauzes, m12-19
CELL_B = [(4, 'C#7'), (6, 'Eb7'), (8, 'Ab6'), (10, 'C#7'), (12, 'Eb7')]           # m20-23
ARP_AB = [(0, 'F6'), (3, 'F6'), (5, 'C#6'), (8, 'F6'), (10, 'C#6'), (12, 'Eb6')]  # aria boven Ab
ARP_B = [(0, 'F#5'), (2, 'C#6'), (5, 'Bb5'), (8, 'F#5'), (9, 'Bb6'), (10, 'C#6'), (12, 'Bb6')]   # aria boven B
G_A = [(0, 'F6'), (2, 'F#6'), (3, 'Bb5'), (4, 'C#6'), (6, 'Eb6'), (8, 'Ab5'), (9, 'C6'), (10, 'C#6'), (12, 'Eb6'),
       (14, 'C#7')]                                                               # groove, maat a/c (m40, 42, 44 ...)
G_B = [(0, 'Ab5'), (2, 'F6'), (3, 'Bb5'), (4, 'Eb6'), (9, 'C6'), (11, 'G5'), (12, 'Bb6')]             # maat b
G_D = [(2, 'C#7'), (3, 'Bb5'), (10, 'F#6'), (11, 'Ab6'), (13, 'G5'), (14, 'F#6')]                      # maat d
G_BD = [(0, 'F#5'), (2, 'C#6'), (4, 'Bb5'), (6, 'Eb6'), (8, 'F5'), (10, 'C#6'), (12, 'Bb5'), (14, 'Eb6')]  # B -> Db

# ---- de aria (lead), gemeten in de vocals-stem: (maat, zestiende, lengte, noot, afwijking in halve tonen) -------
LEAD = [
    (24, 11, 3, 'F#5', .39), (24, 14, 2, 'Ab5', .38),
    (25, 0, 12, 'F5', .31), (25, 12, 4, 'F#5', .41), (26, 0, 15, 'F5', .32),
    (27, 4, 2, 'F5', .55), (27, 13, 1, 'C#5', .32), (27, 14, 2, 'C5', .41),
    (28, 0, 11, 'B4', -.10),
    (29, 4, 4, 'Ab4', .51), (29, 8, 4, 'Bb4', .41), (29, 12, 4, 'C#5', .46),
    (30, 0, 11, 'Bb4', .33), (30, 11, 2, 'B4', -.20), (30, 14, 2, 'Bb4', .31),
    (31, 0, 4, 'Ab4', .49), (31, 4, 5, 'Bb4', .42), (31, 9, 3, 'F#4', .43), (31, 12, 5, 'Ab4', .35),
    (32, 2, 6, 'F#4', -.18), (32, 13, 3, 'Ab4', .26),
    (33, 0, 12, 'F5', .33), (33, 12, 4, 'F#5', .42), (34, 0, 15, 'F5', .56),
    (35, 0, 4, 'F5', .48), (35, 4, 4, 'F#5', .42), (35, 8, 6, 'C#6', .45),
    (37, 4, 5, 'F#5', .47), (37, 9, 3, 'C#6', .52),
    (38, 2, 9, 'Bb5', .39),
]

# ---- akkoorden: (maat, zestiende, lengte in 16en, strijkers, koor) ---------------------------------------------
EBS = (['Eb3', 'Bb3'], ['F4', 'Eb5', 'Bb5'])
BMAJ = (['B2', 'B3'], ['F#5', 'Bb5', 'C#6'])
CHORDS = [
    (8, 4, 12, ['Eb3', 'G3'], ['F4']),                       # opmaat: Eb-groot onder, koor F4 (gemeten G3 in 'other')
    (9, 0, 16) + EBS, (10, 0, 8) + EBS,
    (10, 10, 22, [], ['Ab3', 'C#4', 'Eb4']),                 # pauze: spookakkoord (chroma: Eb C# Ab)
    (12, 0, 32) + BMAJ, (14, 0, 16, ['B2', 'F#3'], ['B3', 'Bb4', 'C#5']),
    (15, 0, 12, ['B2', 'F#3'], ['Eb5', 'F#5', 'C#6']), (15, 12, 4, ['B2', 'F#3'], ['F#5', 'Bb5', 'F6']),
    (16, 0, 28, ['Eb3', 'Bb3'], ['F4', 'Bb4']), (17, 12, 4, ['Eb3', 'Bb3'], ['F#4', 'Bb4']),
    (18, 0, 4, ['Eb3', 'Bb3'], ['F#4', 'Eb5', 'F#5']), (18, 4, 4, ['Eb3', 'Bb3'], ['F4', 'F5']),
    (18, 10, 22, [], ['Ab3', 'C#4', 'Eb4']),                 # pauze
    (20, 0, 32, BMAJ[0], ['Bb4', 'F#5', 'Bb5']), (22, 0, 16, BMAJ[0], ['C#5', 'Bb5', 'C#6']),
    (23, 0, 8, BMAJ[0], ['Eb5', 'Bb5', 'Eb6']), (23, 8, 8, BMAJ[0], ['C#5', 'F#5', 'C#6']),
    (24, 0, 8, ['Eb3', 'Bb3'], ['F4', 'F5', 'C6']), (24, 8, 8, ['Ab2', 'Eb3'], ['F#4', 'Eb5']),
    (25, 0, 48, ['Eb3', 'Eb4'], ['Eb4', 'F#4']),       # Eb-orgelpunt: Eb is de sterkste toon, Bb hoor je niet (chroma)
    (28, 0, 64, BMAJ[0], ['Eb5', 'Ab5', 'B5']),            # B6 (chroma: B Eb Ab)
    (32, 0, 8, ['Ab2', 'Eb3'], ['Eb4', 'F4', 'Bb4']), (32, 8, 8, ['Ab2', 'Eb3'], ['F4', 'Bb4', 'C#5']),
    (33, 0, 48, ['Eb3', 'Eb4'], ['Eb4', 'F#4']),
    (36, 0, 64, BMAJ[0], ['Eb4', 'Ab4', 'B4']),
]
GROOVE = {'a': [(0, 8, ['Eb3', 'Bb3'], ['Eb4', 'F4', 'Bb4']), (8, 8, ['Ab2', 'Eb3'], ['B3', 'Eb4', 'F#4'])],
          'b': [(0, 16, ['Eb3', 'Eb4'], ['D4', 'F4', 'G4'])],      # Ebmaj9: D = trilpartner van Eb, G (chroma: Eb D F G)
          'd': [(0, 8, ['Eb3', 'Bb3'], ['Eb4', 'F4', 'Bb4']), (8, 8, ['Eb3'], ['C#4', 'Ab4'])],
          'BD': [(0, 8, ['B2', 'F#3'], ['Bb4', 'C#5', 'F#5']), (8, 8, ['C#3', 'C#4'], ['F4', 'Bb4', 'Eb5'])]}
GROOVE['c'] = GROOVE['a']
# frase per maat 40-63: a b c d a b c d ... ; m55/m63 = B -> Db
PHRASE = {}
for b in range(40, 64):
    PHRASE[b] = 'abcd'[(b - 40) % 4]
PHRASE[55] = PHRASE[63] = 'BD'

# ---- bas (PSG-golf): per maat [(zestiende, lengte, noot)] -------------------------------------------------------
BASS_G = {'a': [(0, 13, 'Eb3'), (13, 3, 'E3')], 'b': [(0, 16, 'Eb3')],
          'c': [(0, 6, 'Eb3'), (7, 5, 'Eb2'), (12, 1, 'D2'), (13, 3, 'E2')],
          'd': [(0, 8, 'Eb2'), (9, 4, 'C#2'), (13, 3, 'A2')],
          'BD': [(0, 8, 'B2'), (8, 8, 'C#3')]}
WOBBLE_B = [(0, 4, 'B2'), (4, 1, 'B2'), (5, 1, 'Bb2'), (6, 1, 'A2'), (7, 2, 'G2'), (9, 1, 'A2'), (10, 1, 'Bb2'),
            (11, 5, 'B2')]                                    # m31/37/39: chromatische dip (gemeten)
WOBBLE_EB = [(0, 10, 'Eb2'), (10, 1, 'D2'), (11, 5, 'Eb2')]  # m27/35 (Ab-G in de bas-stem = boventonen; 8-bit: Eb)
TO_AB = [(0, 2, 'Bb2'), (2, 2, 'Ab2'), (4, 2, 'G2'), (6, 10, 'Eb2')]     # m24/m32: Bb-Ab-G-Eb

# ---- ostinato (PSG-blokgolf 1), groove, achtsten -----------------------------------------------------------------
OST_A = ['Bb4', 'C#5', 'Bb4', 'F5', 'Bb4', 'C#5', 'B4', 'B4']
OST_B = ['Eb5', 'D5', 'Eb5', 'F5', 'Eb5', 'D5', 'Eb5', 'F5']    # trilfiguur Eb-D (chroma)
OST_BD = ['B4', 'C#5', 'F#5', 'C#5', 'Ab4', 'C#5', 'F5', 'C#5']

# zuchten (koor glijdt een halve toon omlaag): (maat, zestiende, lengte)
SIGHS = [(42, 10, 18, ('A4', 'D5')), (47, 14, 8, ('A4', 'D5')), (53, 14, 8, ('A4', 'D5')), (56, 10, 8, ('A4', 'D5')),
         (59, 6, 8, ('A4', 'D5')), (60, 5, 10, ('A4', 'D5')),
         (64, 8, 8, ('E4', 'A4', 'C#5'))]      # m64: A-groot glijdt naar Ab-groot -> het begin (Ab5 C#6 Eb6)


def build():
    P = {k: [] for k in ('lead', 'choir', 'sigh', 'str', 'bell', 'echo', 'ost', 'bass', 'hat', 'drums')}
    bend_lead, bend_sigh = [], []

    # bellen
    def bells(bar, cell, vel, octave=0):
        for pos, n in cell:
            t = T(bar, pos)
            P['bell'].append([t, t + 2 * S, p(n) + 12 * octave, vel])
            P['echo'].append([t + 3 * S, t + 5 * S, p(n) + 12 * octave, max(40, vel - 30)])
    for b in (1, 2, 3):
        bells(b, INTRO, 92)
    bells(4, INTRO4, 92)
    bells(5, INTRO5, 88)
    for b in (6, 7):
        bells(b, CELL, 84)
    for b in (10, 11, 18, 19):
        bells(b, CELL, 80)
    for b in (8, 9, 12, 13, 14, 15, 16, 17):
        bells(b, CELL, 64)
    for b in range(20, 24):
        bells(b, CELL_B, 66)
    for b in range(24, 40):
        bells(b, ARP_B if b in range(28, 32) or b in range(36, 40) else ARP_AB, 56)
    for b in range(40, 64):
        ph = PHRASE[b]
        bells(b, {'a': G_A, 'c': G_A, 'b': G_B, 'd': G_D, 'BD': G_BD}[ph], 70)
    bells(64, CELL[:3], 70)

    # lead (aria): bend per noot (BENDR 2: 64 stappen = 2 halve tonen) + vibrato
    for bar, pos, ln, n, dev in LEAD:
        t = T(bar, pos)
        P['lead'].append([t, t + ln * S, p(n), 100])
        bend_lead.append((t, int(round(dev * LEAD_DETUNE * 32)) * 128))

    # akkoorden
    def chord(t, ln, strings, choir, vs=80, vc=88):
        for n in strings:
            P['str'].append([t, t + ln, p(n), vs])
        for n in choir:
            P['choir'].append([t, t + ln, p(n), vc])
    for bar, pos, ln, strings, choir in CHORDS:
        quiet = bar in (10, 11, 18, 19) and pos >= 8
        # lange akkoorden in stukken van 2 tellen (koor-sample: geen eindeloze lus, heraanzet = 'adem')
        t, end = T(bar, pos), T(bar, pos) + ln * S
        while t < end:
            seg = min(end - t, 2 * TPB)
            chord(t, seg, strings, choir, 76, 60 if quiet else 88)
            t += seg
    for b in range(40, 64):
        for pos, ln, strings, choir in GROOVE[PHRASE[b]]:
            chord(T(b, pos), ln * S, strings, choir, 72, 80)
    chord(T(64), 8 * S, ['C#3'], ['C#4', 'F#4', 'Eb5'], 70, 74)

    # zuchten
    for bar, pos, ln, notes in SIGHS:
        t = T(bar, pos)
        for n in notes:
            P['sigh'].append([t, t + ln * S, p(n), 92])
        bend_sigh.append((t, 0))
        steps = 8
        for i in range(1, steps + 1):          # in de tweede helft van de noot een halve toon omlaag (BENDR 1)
            bend_sigh.append((t + ln * S // 2 + i * (ln * S // 2) // steps - 1, -int(8192 * i / steps)))
        bend_sigh.append((t + ln * S + 1, 0))

    # bas
    def bass(bar, figs, vel=100):
        for pos, ln, n in figs:
            t = T(bar, pos)
            P['bass'].append([t, t + ln * S - 4, p(n), vel])
    for b in (8, 9):
        bass(b, [(0 if b > 8 else 4, 16 if b > 8 else 12, 'Eb2')])
    bass(10, [(0, 8, 'Eb2')])
    for b in (12, 13, 14, 15, 20, 21, 22, 23, 28, 29, 30, 36, 38):
        bass(b, [(0, 16, 'B2')])
    for b in (31, 37, 39):
        bass(b, WOBBLE_B)
    for b in (16, 17):
        bass(b, [(0, 16, 'Eb2')])
    bass(18, [(0, 8, 'Eb2')])
    for b in (24, 32):
        bass(b, TO_AB)
    for b in (25, 26, 33, 34):
        bass(b, [(0, 16, 'Eb2')])
    for b in (27, 35):
        bass(b, WOBBLE_EB)
    for b in range(40, 64):
        bass(b, BASS_G[PHRASE[b]], 92)
    bass(64, [(0, 8, 'C#3'), (8, 8, 'A2')], 80)

    # ostinato (groove)
    for b in range(40, 64):
        pat = {'b': OST_B, 'BD': OST_BD}.get(PHRASE[b], OST_A)
        for i, n in enumerate(pat):
            t = T(b, 2 * i)
            P['ost'].append([t, t + 2 * S - 8, p(n), 84 if i % 4 == 0 else 70])

    # drums (vanaf m24; gemeten in de 8-bit-cover en het origineel): 2-maatspatroon
    def hit(t, n, v, ln=S):
        P['drums'].append([t, t + ln, n, v])
    for b in range(24, 64):
        even = (b % 2 == 0)
        full = b >= 40
        if b == 24:
            hit(T(b, 0), KICK, 110); hit(T(b, 8), SNARE, 96)
        elif even:
            hit(T(b, 0), KICK, 112); hit(T(b, 6), KICK, 92); hit(T(b, 8), SNARE, 100)
            if full:
                hit(T(b, 12), KICK, 80)
        else:
            hit(T(b, 2), KICK, 108); hit(T(b, 6), KICK, 92); hit(T(b, 7), KICK, 84); hit(T(b, 8), SNARE, 104)
        hats = (0, 4, 6, 8, 10, 12, 14) if even else (0, 2, 6, 7, 8, 11, 14)
        for h in hats:
            P['hat'].append([T(b, h), T(b, h) + S // 2, 72, 110 if h in (0, 8) else 84])

    for k in P:
        P[k] = dedupe(P[k])

    write_voicegroup()
    rel = releases(VG)
    progs = {'lead': LEAD_P, 'choir': CHOIR, 'sigh': SIGH, 'str': STR, 'bell': BELL}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) + 2 for k, pr in progs.items()}
    tail['drums'] = 0
    for k in ('lead', 'choir', 'str', 'sigh'):
        P[k] = detach(P[k], tail[k])
    order = ['lead', 'drums', 'bell', 'sigh', 'choir', 'str']
    ds = {k: P[k] for k in order}
    kept = allocate(ds, order, tail, drum_len=S * 2, drum_parts=('drums',), max_voices=MAXV)
    for k in order:
        n = len(ds[k])
        if n:
            print('  %-6s %4d noten, %3d weg (%.0f%%)' % (k, n, n - len(kept[k]), 100 * (n - len(kept[k])) / n))
        P[k] = kept[k]

    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.loop = (0, NBARS * BAR)
    ex_lead = [(0, mido.Message('control_change', control=20, value=2)),
               (0, mido.Message('control_change', control=21, value=LFOS)),
               (0, mido.Message('control_change', control=1, value=LEAD_MOD))] + \
              [(t, mido.Message('pitchwheel', pitch=v)) for t, v in bend_lead]
    ex_choir = [(0, mido.Message('control_change', control=21, value=LFOS)),
                (0, mido.Message('control_change', control=1, value=CHOIR_MOD))]
    ex_sigh = [(0, mido.Message('control_change', control=20, value=1)),
               (0, mido.Message('control_change', control=21, value=LFOS + 6)),
               (0, mido.Message('control_change', control=1, value=SIGH_MOD))] + \
              [(t, mido.Message('pitchwheel', pitch=max(-8192, min(8191, v)))) for t, v in bend_sigh]
    TRACKS = [('lead', LEAD_P, 92, 64, ex_lead), ('choir', CHOIR, 70, 64, ex_choir), ('sigh', SIGH, 66, 56, ex_sigh),
              ('str', STR, 62, 64, ()), ('bell', BELL, 66, 72, ()), ('echo', ECHO, 30, 44, ()),
              ('ost', OST, 34, 80, ()), ('bass', BASS, 62, 64, ()), ('hat', HAT, 26, 70, ()),
              ('drums', DRUMS, 92, 64, ())]
    free = [c for c in range(16) if c != 9]
    for k, prog, vol, pan, ex in TRACKS:
        ch = 9 if prog == DRUMS else free.pop(0)
        song.add(P[k], prog, vol, ch, pan, extra=ex)
    written = {k for k, *_ in TRACKS}
    assert not [k for k in P if P[k] and k not in written], 'partij niet weggeschreven'
    song.save(OUT, NBARS * BAR)
    print(OUT)


LEAD_P = LEAD_PROG = 82
KIT = [
    'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 200',          # 36
    'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 200',          # 37
    'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 200',         # 38
    'voice_directsound_no_resample 30, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 216',  # 39 (remix)
    'voice_directsound 50, 64, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 200',                       # 40 tom (remix)
]
CRASH, TOM = 39, 40


# ==== Battle! Area Zero (MUS_GROUNDED_VS_AREA_ZERO, 682): remix voor paradoxen, Koraidon/Miraidon, Terapagos =========
OUT_VS = 'sound/songs/midi/mus_grounded_vs_area_zero.mid'
VS_BPM = 150
# Vorm (remix-maten, 1-geteld), zelfde materiaal, zelfde voicegroup (geen nieuwe samples):
#   1-4   intro: het kristal-arpeggio (m1-4 van het origineel), maat 4 = roffel + koor zwelt (transitie)
#   5-12  A: de groove (frase a b c d) met dubbel zo drukke drums, ostinato in zestienden, bas in achtsten
#  12-27  B: de aria (origineel m24-39, opmaat in maat 12) op battle-drums
#  28-31  C: B (Cb) maj9, halve-tijd-drums, kristalcel
#  32-33  B -> Db (bVI-bVII) met roffel
#  34     PAUZE: alleen belletjes (Area Zero 'houdt zijn adem in')
#  35     inzet Eb + koorzucht -> terug naar A (loop 5-35)
VS_LOOP0, VS_END = 5, 36


def build_remix():
    P = {k: [] for k in ('lead', 'choir', 'sigh', 'str', 'bell', 'echo', 'ost', 'bass', 'hat', 'drums')}
    bend_lead, bend_sigh = [], []
    ORIG = lambda b: b + 12          # remix-maat -> origineel (aria-deel)

    def bells(bar, cell, vel):
        for pos, n in cell:
            t = T(bar, pos)
            P['bell'].append([t, t + 2 * S, p(n), vel])
            P['echo'].append([t + 3 * S, t + 5 * S, p(n), max(40, vel - 30)])

    def chord(t, ln, strings, choir, vs=78, vc=86):
        end = t + ln
        while t < end:
            seg = min(end - t, 2 * TPB)
            for n in strings:
                P['str'].append([t, t + seg, p(n), vs])
            for n in choir:
                P['choir'].append([t, t + seg, p(n), vc])
            t += seg

    def hit(t, n, v, ln=S):
        P['drums'].append([t, t + ln, n, v])

    def hats16(bar, accent=(0, 4, 8, 12), vel=(104, 70)):
        for i in range(16):
            P['hat'].append([T(bar, i), T(bar, i) + S // 2, 72, vel[0] if i in accent else vel[1]])

    def bass8(bar, root, alt=None, vel=100):
        """achtsten: grondtoon, octaafsprong op de 3+3+2-accenten (0, 3, 6 achtsten = 16e 0, 6, 12)."""
        for i in range(8):
            n = p(root) + (12 if i in (3, 6) else 0)
            if alt and i == 7:
                n = p(alt)
            P['bass'].append([T(bar, 2 * i), T(bar, 2 * i) + 2 * S - 6, n, vel if i in (0, 3, 6) else vel - 18])

    def groove_drums(bar, ph):
        hit(T(bar, 0), KICK, 116); hit(T(bar, 6), KICK, 100); hit(T(bar, 8), KICK, 104)
        hit(T(bar, 4), SNARE, 104); hit(T(bar, 12), SNARE, 110)
        if ph == 'd':
            hit(T(bar, 14), SNARE, 84); hit(T(bar, 15), SNARE, 92)
        hats16(bar)

    # intro (1-4): kristal-arpeggio, maat 3-4 dubbel zo snel; roffel en koorzwelling in maat 4
    bells(1, INTRO, 92); bells(2, INTRO, 92)
    for b in (3, 4):
        cell = INTRO if b == 3 else INTRO4
        for pos, n in cell:
            for d in (0, 1):
                t = T(b, pos + d)
                P['bell'].append([t, t + S, p(n) + (12 if d else 0), 88])
    chord(T(4), 16 * S, ['Eb3', 'Bb3'], ['Eb4', 'Bb4', 'Eb5'], 70, 80)
    for i in range(16):
        hit(T(4, i), SNARE, 50 + i * 4)
    hit(T(4, 0), TOM, 100); hit(T(4, 8), TOM, 108); hit(T(4, 12), TOM, 116)

    # A (5-12): groove
    for k, b in enumerate(range(5, 13)):
        ph = 'abcd'[k % 4]
        for pos, ln, strings, choir in GROOVE[ph]:
            chord(T(b, pos), ln * S, strings, choir)
        bells(b, {'a': G_A, 'c': G_A, 'b': G_B, 'd': G_D}[ph], 72)
        pat = {'b': OST_B}.get(ph, OST_A)
        for i in range(16):
            n = p(pat[i // 2]) + (12 if i % 2 else 0)          # elke achtste van het ostinato + zijn octaaf
            P['ost'].append([T(b, i), T(b, i) + S - 6, n, 84 if i % 4 == 0 else 64])
        bass8(b, 'Eb2', alt={'a': 'E2', 'c': 'D2', 'd': 'C#2'}.get(ph))
        groove_drums(b, ph)
        if b in (5, 9):
            hit(T(b, 0), CRASH, 112, 4 * S)
    for b, pos, ln, notes in ((7, 10, 8, ('A4', 'D5')), (11, 10, 8, ('A4', 'D5'))):
        t = T(b, pos)
        for n in notes:
            P['sigh'].append([t, t + ln * S, p(n), 96])
        bend_sigh.append((t, 0))
        for i in range(1, 9):
            bend_sigh.append((t + ln * S // 2 + i * (ln * S // 2) // 8 - 1, -int(8192 * i / 8)))
        bend_sigh.append((t + ln * S + 1, 0))

    # B (12-27): de aria van het origineel (m24-39) op battle-drums
    for bar, pos, ln, n, dev in LEAD:
        t = T(bar - 12, pos)
        P['lead'].append([t, t + ln * S, p(n), 110])
        bend_lead.append((t, int(round(dev * LEAD_DETUNE * 32)) * 128))
    for bar, pos, ln, strings, choir in CHORDS:
        if 25 <= bar <= 39:
            chord(T(bar - 12, pos), ln * S, strings, choir, 76, 80)
    for b in range(13, 28):
        o = ORIG(b)
        isB = o in range(28, 32) or o in range(36, 40)
        bells(b, ARP_B if isB else ARP_AB, 60)
        bass8(b, 'B2' if isB else 'Eb2', alt=('Bb2' if isB else 'D2') if b % 2 == 0 else None, vel=96)
        hit(T(b, 0), KICK, 112); hit(T(b, 6), KICK, 96); hit(T(b, 8), KICK, 100)
        hit(T(b, 4), SNARE, 100); hit(T(b, 12), SNARE, 108)
        if b in (13, 21):
            hit(T(b, 0), CRASH, 110, 4 * S)
        hats16(b, vel=(96, 60))
        chordtones = ['B3', 'F#4', 'Bb4', 'F#4'] if isB else ['Eb4', 'Bb4', 'F#4', 'Bb4']
        for i in range(16):
            if i % 4 != 3:
                P['ost'].append([T(b, i), T(b, i) + S - 6, p(chordtones[i % 4]), 70 if i % 4 else 82])

    # C (28-31): B maj9, halve tijd; 32-33 B -> Db met roffel; 34 pauze; 35 inzet
    for b in range(28, 32):
        chord(T(b), 16 * S, ['B2', 'B3'], ['F#5', 'Bb5', 'C#6'], 78, 86)
        bells(b, CELL_B, 72)
        bass8(b, 'B2', vel=92)
        hit(T(b, 0), KICK, 112); hit(T(b, 8), SNARE, 110); hit(T(b, 10), KICK, 90)
        if b == 28:
            hit(T(b, 0), CRASH, 112, 4 * S)
        for i in range(0, 16, 2):
            P['hat'].append([T(b, i), T(b, i) + S // 2, 72, 96 if i % 8 == 0 else 70])
    for b in (32, 33):
        for pos, ln, strings, choir in GROOVE['BD']:
            chord(T(b, pos), ln * S, strings, choir, 80, 90)
        bells(b, G_BD, 74)
        for i in range(8):
            n = 'B2' if i < 4 else 'C#3'
            P['bass'].append([T(b, 2 * i), T(b, 2 * i) + 2 * S - 6, p(n) + (12 if i in (3, 6) else 0), 100])
        hit(T(b, 0), KICK, 112); hit(T(b, 8), KICK, 108)
        for i in range(0, 16, 1 if b == 33 else 2):              # roffel: achtsten, dan zestienden, crescendo
            hit(T(b, i), SNARE, (76 if b == 33 else 56) + i * 3)
        hats16(b, vel=(100, 66))
    bells(34, CELL, 84)                                         # pauze
    chord(T(34, 10), 6 * S, [], ['Ab3', 'C#4', 'Eb4'], 60, 56)
    chord(T(35), 16 * S, ['Eb3', 'Bb3'], ['Eb4', 'F4', 'Bb4'], 80, 90)
    hit(T(35, 0), CRASH, 120, 4 * S); hit(T(35, 0), KICK, 120)
    for pos in (8, 10, 12, 14):
        hit(T(35, pos), TOM, 90 + pos * 2)
    hit(T(35, 15), SNARE, 100)
    bass8(35, 'Eb2', vel=100)
    bells(35, G_A, 74)
    t = T(35, 8)
    for n in ('A4', 'D5'):
        P['sigh'].append([t, t + 8 * S, p(n), 96])
    bend_sigh.append((t, 0))
    for i in range(1, 9):
        bend_sigh.append((t + 4 * S + i * 4 * S // 8 - 1, -int(8192 * i / 8)))
    bend_sigh.append((t + 8 * S + 1, 0))

    for k in P:
        P[k] = dedupe(P[k])
    rel = releases(VG)
    progs = {'lead': LEAD_P, 'choir': CHOIR, 'sigh': SIGH, 'str': STR, 'bell': BELL}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, VS_BPM) + 2 for k, pr in progs.items()}
    tail['drums'] = 0
    for k in ('lead', 'choir', 'str', 'sigh'):
        P[k] = detach(P[k], tail[k])
    order = ['lead', 'drums', 'bell', 'sigh', 'choir', 'str']
    ds = {k: P[k] for k in order}
    dl = {KICK: 2 * S, SNARE: 2 * S, CRASH: 8 * S, TOM: 3 * S}
    drum_len = max(dl.values())
    # drums: echte lengte per sample (kick/snare kort, bekken lang)
    busy = [(e[0], e[0] + dl.get(e[2], 2 * S)) for e in P['drums']]
    kept = allocate({k: ds[k] for k in order if k != 'drums'}, [k for k in order if k != 'drums'], tail,
                    max_voices=11, preset=busy)
    kept['drums'] = P['drums']
    for k in order:
        n = len(ds[k])
        if n:
            print('  %-6s %4d noten, %3d weg (%.0f%%)' % (k, n, n - len(kept[k]), 100 * (n - len(kept[k])) / n))
        P[k] = kept[k]

    song = Song(TPB, 500000)
    song.tempo(0, VS_BPM / 120)
    song.loop = (T(VS_LOOP0), T(VS_END))
    ex_lead = [(0, mido.Message('control_change', control=20, value=2)),
               (0, mido.Message('control_change', control=21, value=LFOS + 8)),
               (0, mido.Message('control_change', control=1, value=LEAD_MOD))] + \
              [(t, mido.Message('pitchwheel', pitch=v)) for t, v in bend_lead]
    ex_choir = [(0, mido.Message('control_change', control=21, value=LFOS + 8)),
                (0, mido.Message('control_change', control=1, value=CHOIR_MOD))]
    ex_sigh = [(0, mido.Message('control_change', control=20, value=1)),
               (0, mido.Message('control_change', control=21, value=LFOS + 14)),
               (0, mido.Message('control_change', control=1, value=SIGH_MOD))] + \
              [(t, mido.Message('pitchwheel', pitch=max(-8192, min(8191, v)))) for t, v in bend_sigh]
    TRACKS = [('lead', LEAD_P, 100, 64, ex_lead), ('choir', CHOIR, 66, 64, ex_choir), ('sigh', SIGH, 70, 56, ex_sigh),
              ('str', STR, 60, 64, ()), ('bell', BELL, 64, 72, ()), ('echo', ECHO, 28, 44, ()),
              ('ost', OST, 36, 80, ()), ('bass', BASS, 66, 64, ()), ('hat', HAT, 28, 70, ()),
              ('drums', DRUMS, 100, 64, ())]
    free = [c for c in range(16) if c != 9]
    for k, prog, vol, pan, ex in TRACKS:
        ch = 9 if prog == DRUMS else free.pop(0)
        song.add(P[k], prog, vol, ch, pan, extra=ex)
    assert not [k for k in P if P[k] and k not in {t[0] for t in TRACKS}], 'partij niet weggeschreven'
    song.save(OUT_VS, T(VS_END))
    print(OUT_VS)


def write_voicegroup():
    open('sound/voicegroups/keysplits/area_zero_strings.inc', 'w').write(
        '@ Project Grounded: zachte strijkers (trage aanzet) voor Area Zero (areazero_theme.py).\n'
        'voice_group area_zero_strings_keysplit\n' + ''.join(
            '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_string_ensemble_%d, 40, 0, 255, 180\n' % k
            for k in (60, 72, 84)) + '\n')
    open('sound/voicegroups/drumsets/area_zero.inc', 'w').write(
        '@ Project Grounded: drumkit voor Area Zero (areazero_theme.py): 36/37 kick, 38 snare. Hats op de PSG-ruis\n'
        '@ (eigen spoor). Alleen stock-samples, geen PSG in de kit.\n'
        'voice_group area_zero_drumset, 36\n' + ''.join('\t%s\n' % k for k in KIT) + '\n')
    over = {
        BELL: 'voice_directsound 60, 0, DirectSoundWaveData_az_crystal, 255, 0, 255, 150',
        STR: 'voice_keysplit voicegroup_area_zero_strings_keysplit, keysplit_strings',
        CHOIR: 'voice_directsound 60, 0, DirectSoundWaveData_classical_choir_voice_ahhs, 60, 0, 255, 175',
        SIGH: 'voice_directsound 60, 0, DirectSoundWaveData_classical_choir_voice_ahhs, 90, 0, 255, 165',
        LEAD_P: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_square_wave, 200, 0, 255, 170',
        OST: 'voice_square_1 60, 0, 0, 1, 0, 2, 6, 1',
        ECHO: 'voice_square_2 60, 0, 0, 0, 3, 0, 1',
        BASS: 'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_2, 0, 7, 15, 1',
        HAT: 'voice_noise_alt 60, 0, 0, 0, 1, 0, 0',
        DRUMS: 'voice_keysplit_all voicegroup_area_zero_drumset',
    }
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: voicegroup voor Area Zero (grounded_gm + kristalbel, koor, PSG-lagen, eigen kit).'
    lines[1] = '@ Gegenereerd door tools/grounded/areazero_theme.py.'
    lines[2] = 'voice_group %s' % VG
    out = []
    for l in lines:
        s = l.rstrip()
        if '@ ' in s and s.split('@ ')[-1].strip().isdigit() and int(s.split('@ ')[-1]) in over:
            n = int(s.split('@ ')[-1])
            out.append('\t%s  @ %d' % (over[n], n))
        else:
            out.append(l)
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    # sample-label en includes (idempotent)
    dsd = 'sound/direct_sound_data.inc'
    txt = open(dsd).read()
    if 'DirectSoundWaveData_az_crystal::' not in txt:
        txt = txt.rstrip('\n') + ('\n\n\t.align 2\nDirectSoundWaveData_az_crystal::\n'
                                  '\t.incbin "sound/direct_sound_samples/grounded/az_crystal.bin"\n')
        open(dsd, 'w').write(txt)
    vgi = 'sound/voice_groups.inc'
    txt = open(vgi).read()
    for inc in ('drumsets/area_zero.inc', 'keysplits/area_zero_strings.inc', '%s.inc' % VG):
        line = '.include "sound/voicegroups/%s"' % inc
        if line not in txt:
            txt = txt.rstrip('\n') + '\n' + line + '\n'
    open(vgi, 'w').write(txt)


# ---- offline-render (FluidR3 GM; benadering van noten/vorm/tempo, niet van de GBA-klank) -------------------
GM_PROG = {BELL: 8, STR: 49, CHOIR: 52, SIGH: 53, OST: 81, ECHO: 80, LEAD_P: 80, BASS: 38, HAT: 122}
GM_DRUM = {KICK: 36, 37: 36, SNARE: 38, 39: 49, 40: 45}


def render_gm(outdir, name='areazero', src_mid=OUT):
    m = mido.MidiFile(src_mid)
    gm = mido.MidiFile(type=1, ticks_per_beat=m.ticks_per_beat)
    gm.tracks.append(m.tracks[0])
    for src in m.tracks[1:]:
        t = mido.MidiTrack()
        drum = any(x.type == 'program_change' and x.channel == 9 for x in src)
        prog = None
        for x in src:
            if x.type == 'program_change':
                prog = x.program
                x = x.copy(program=0 if drum else GM_PROG.get(x.program, x.program))
            elif drum and x.type in ('note_on', 'note_off'):
                x = x.copy(note=GM_DRUM.get(x.note, x.note))
            elif x.type == 'control_change' and x.control == 20:      # BENDR -> RPN 0
                for c, v in ((101, 0), (100, 0), (6, x.value)):
                    t.append(mido.Message('control_change', channel=x.channel, control=c, value=v, time=0))
                x = x.copy(control=38, value=0)
            elif prog == HAT and x.type in ('note_on', 'note_off'):
                x = x.copy(note=min(127, x.note + 20))
            t.append(x)
        gm.tracks.append(t)
    os.makedirs(outdir, exist_ok=True)
    mid = os.path.join(outdir, name + '_gm.mid')
    gm.save(mid)
    wav = os.path.join(outdir, name + '_fluidr3.wav')
    subprocess.run(['fluidsynth', '-ni', '-g', '0.6', '-r', '22050', '-F', wav, '/usr/share/sounds/sf2/FluidR3_GM.sf2', mid],
                   check=True, capture_output=True)
    print('render:', wav)


if __name__ == '__main__':
    build()
    build_remix()
    if '--render' in sys.argv:
        d = sys.argv[sys.argv.index('--render') + 1]
        render_gm(d)
        render_gm(d, 'vs_areazero', OUT_VS)
