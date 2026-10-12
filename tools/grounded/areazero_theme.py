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
# v2 (Jordi: 'vocals veel te aanwezig, goofy, spookachtig; slaan de hele tijd over, moet 1 lange klank zijn; de seesaw-
# achtige vocal vanaf 7 s [= de aria, m24-25] slaat nergens op; de achtergrond is prima'): in 681 geen aria/zuchten meer,
# koor = 2 stemmen, één lange aangehouden noot per akkoord (sample loopt), zonder vibrato en zachter. 682 ongewijzigd.
MAIN_LEAD, MAIN_SIGHS, MAIN_CHOIR_MOD, MAIN_CHOIR_VOICES = False, False, 0, 2
# v3 (Jordi: 'vocalen nog steeds ver van het origineel; de achtergrond is goed'): de stem komt uit het origineel zelf
# (az_voice, areazero_samples.py) en speelt alleen wat de vocals-stem van het origineel heeft: de koorakkoorden m8-24
# (tot 3 stemmen, lange aangehouden tonen) en de aria m24-39. Geen koor meer in m25-64 (daar zwijgt de vocals-stem;
# de strijkers blijven). Geen vibrato/bends/detune: de vibrato zit in de sample zelf.
MAIN_LEAD, MAIN_CHOIR_VOICES, VOICE_UNTIL = True, 3, 24
VOICE, VOICE_LO, CHOIRKIT = 54, 55, 56   # az_voice (F5), az_voice_lo (Bb4), kit met de koorroepen (alleen 681)
VOICE_SPLIT = 73                          # aria-noten t/m C#5 op az_voice_lo, daarboven az_voice
from areazero_samples import CHOIR_EVENTS, ARIA_PHRASES, BELL_RIPS  # noqa: E402  (zelfde lijsten als de geknipte samples)
BELLKIT = 58
# v8 (Jordi: 'vanaf 8 s wordt van alles naar de achtergrond gedrongen'): alle knippen op één schaal (gain = piek /
# grootste piek, areazero_samples.py), velocity lineair -> stem, koor en begeleiding in de verhouding van het origineel
PAD_UNTIL = 40                            # m5-39: begeleiding uit de knippen, geen strijkers/PSG-bas
LVL_PAD, LVL_VOX = 1.0, 1.0
# v11 (Jordi over de 1.0: 'klinkt ingame zacht, als een platenspeler'): de begeleiding op twee sporen met dezelfde
# noten (coherent, +6 dB, +1 kanaal) en de stem (koor, aria, lead) dubbel zo luid via velocity/volume: zelfde
# verhoudingen, 6 dB meer niveau. Zie ook de lage plank en de piekbegrenzer in areazero_samples.py.
# Met de begrenzer bleef de piek op 72/127 (RMS 1708): de begeleiding op drie sporen (het derde op VOL3: samen x1,45)
# en de stem op twee sporen (koor, aria, lead) met LVL_VOX 1,45: samen x2,9.
LVL_VOX = 1.45
LEAD_VOL = 127                            # was 84 (met velocity 100 -> 127: +5,6 dB)
LEAD2_VOL = 65                            # tweede leadspoor: 127x127 + 65x127 = 2,9 x 84x100
VOL3 = 114                                # derde begeleidingsspoor


def vel(g, lvl):
    return max(1, min(127, int(round(127 * g * lvl))))


ARIAKIT = 57                              # v5: de aria in frasen uit het origineel (kit area_zero_aria)
# v5: wat niet in de vocals-stem zit (m36 Bb5, m39; Spleeter zette het in 'other') blijft op az_voice (gemeten in de mix)
LEAD_REST = [(36, 0, 18, 'Bb5'), (39, 0, 4, 'Ab5'), (39, 4, 4, 'Bb5'), (39, 8, 4, 'F#5'), (39, 12, 6, 'Ab5')]
CHOIR_MIN_GAIN = 0.10                     # roepen die in het origineel nauwelijks klinken (m8 opmaat, m18.04) weglaten
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
CELL = [(4, 'C#7'), (6, 'Eb7'), (8, 'Ab6'), (12, 'Eb7'), (14, 'C#7')]            # m8-9, m12-17 (onder het koor)
# pauzes: aanslagen per toon in de 'other'-stem (daar klinken alleen de belletjes), m10/m18 vanaf tel 2
PAUSE_BELLS = [(10, [(4, 'C#7'), (6, 'Eb7')]), (11, [(4, 'C#7'), (7, 'Eb7'), (11, 'C#7'), (12, 'Eb7')]),
               (18, [(4, 'C#7'), (6, 'Eb7'), (8, 'Ab6')]), (19, [(4, 'C#7'), (6, 'Eb7'), (8, 'Ab6'), (10, 'C#7'), (12, 'Eb7')])]
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
    (8, 6, 10, ['Eb3', 'G3'], ['F4']),                       # opmaat; v7: strijkers pas met de stem (m8 tel 2+, gemeten 15,0 s)
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


def legato(ev):
    """Noten van dezelfde toonhoogte die direct op elkaar aansluiten (of overlappen) samenvoegen tot één noot."""
    out = []
    for e in sorted(ev, key=lambda e: (e[2], e[0])):
        if out and out[-1][2] == e[2] and e[0] <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e[1])
        else:
            out.append(list(e))
    return sorted(out)


def build():
    P = {k: [] for k in ('lead', 'lead2', 'lead_lo', 'aria', 'aria2', 'choir', 'choir2', 'sigh', 'str', 'bell', 'bellecho', 'bellrip', 'bellrip2', 'bellrip3', 'echo', 'ost', 'bass', 'hat', 'drums')}
    bend_lead, bend_sigh = [], []

    # bellen
    # v4 (Jordi: 'de piepjes missen noten en vallen weg; de piano vanaf ±47 s speelt verkeerde noten; vanaf ±77 s speelt
    # een instrument een heel ander nummer'): kanaallog in de game = géén kanaalroof (max. 9 kanalen). Oorzaken: belletjes
    # van 0,25 s (het origineel laat ze ±0,8 s doorklinken), de PSG-echo 3 zestienden later (klinkt als losse foute
    # noten), de geraden arpeggio's ARP_AB/ARP_B in m24-39 en het geraden blokgolf-ostinato vanaf m40: weg.
    # v5 (Jordi: 'de piepjes lijken de helft te missen'): in het origineel klinkt elke belnoot ±1 maat door (een wolk
    # van tonen, zie de CQT van m1-2); ring = tot dezelfde toon opnieuw klinkt (max. 1 maat), kristalbel sterft in 1,3 s.
    def bells(bar, cell, vel, octave=0, ring=16):
        for pos, n in cell:
            t = T(bar, pos)
            P['bell'].append([t, t + ring * S, p(n) + 12 * octave, vel])
    # v7 (Jordi: 'vanaf 8 s gaan de piepjes hun eigen ding doen; vanaf 1:18 een deuntje dat niet in het nummer hoort'):
    # alleen nog belletjes die met een geïsoleerde A/B tegen de stem kloppen: het lage arpeggio m1-6 (+ echo 1/16 later)
    # en de pauzes m10-11/m18-19 (daar klinken in het origineel alleen de belletjes; aanslagen per toon gemeten).
    # Weg: het hoge arpeggio m4-7, de cel onder het koor (m8-23) en de groove-arpeggio's vanaf m40 (geraden).
    def lo(bar, vel, cell=INTRO, echo=True, ring=6):
        bells(bar, cell, vel, ring=ring)
        for pos, n in (cell if echo else ()):
            t = T(bar, pos)
            P['bellecho'].append([t + S, t + 3 * S, p(n), int(vel * 0.5)])
    for b in (1, 2, 3, 4):
        lo(b, 37)                                     # v8: in het origineel 8 dB onder de wolk (m5), wij 11 dB erboven -> -18 dB
    # m5-7 en de pauzes: de belletjeswolk zelf uit het origineel (kit area_zero_bells, A/B: pauze_*, piepjes_*)
    bg = [float(g) for g in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                              'areazero_bells_gain.txt')).read().split()]
    # v8: begeleiding m5-23 = drie aansluitende knippen uit 'other' + 'bass'; m16-23 herhaalt stuk 1 en 2
    # v10: de hele begeleiding m1-64 uit het origineel (stukken in areazero_samples.BELL_RIPS); (stuk, maat, eind-maat)
    PLAN = [(8, 1, 5), (0, 5, 8), (1, 8, 12), (2, 12, 16), (1, 16, 20), (2, 20, 24), (3, 24, 28), (4, 28, 32),
            (3, 32, 36), (4, 36, 40), (6, 54, 65)]
    LOUDER = {16: 10 ** (2.7 / 20)}                 # m16-19: in het origineel 2,7 dB luider dan m8-11
    # intro: in het origineel 8 dB onder de wolk (-42 dB), maar dat is op de GBA de ruisvloer van de 8-bit-uitgang
    # (gemeten: >2 kHz 34% ruis, origineel 0%); +6 dB = 1,5 dB onder de wolk, zoals de goedgekeurde v8/v9
    LOUDER[1] = 2.0
    # m40-53 per maat de beste geknipte maat (chroma per 8e in het origineel, zie areazero_samples.BELL_RIPS)
    BAR_SRC = {44: 5, 45: 7, 46: 9, 47: 10, 48: 11, 49: 12}
    GROOVE_MAP = {40: 44, 41: 45, 42: 46, 43: 47, 44: 44, 45: 45, 46: 46, 47: 47, 48: 48, 49: 49, 50: 48, 51: 47,
                  52: 44, 53: 49}
    PLAN += [(BAR_SRC[src], b, b + 1) for b, src in sorted(GROOVE_MAP.items())]
    for j, b0, b1 in PLAN:
        ln = BELL_RIPS[j][2]
        end = min(T(b0) + ln * S + 2, T(b1) - 1)    # afgebroken stuk (m52/m60) of exact aansluitend: 1 tick vóór
        P['bellrip'].append([T(b0), end, 36 + j, vel(bg[j], LVL_PAD * LOUDER.get(b0, 1))])
    P['bellrip2'] = [n[:] for n in P['bellrip']]     # v11: tweede en derde spoor, dezelfde noten
    P['bellrip3'] = [n[:] for n in P['bellrip']]

    # lead (aria): bend per noot (BENDR 2: 64 stappen = 2 halve tonen) + vibrato
    for bar, pos, ln, n in LEAD_REST:
        t = T(bar, pos)
        P['lead'].append([t, t + ln * S, p(n), 127])
    ag = [float(g) for g in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                              'areazero_aria_gain.txt')).read().split()]
    for j, (bar, pos, ln) in enumerate(ARIA_PHRASES):
        P['aria'].append([T(bar, pos), T(bar, pos) + ln * S, 36 + j, vel(ag[j], LVL_VOX)])

    # akkoorden
    def chord(t, ln, strings, choir, vs=80, vc=88):
        for n in strings:
            P['str'].append([t, t + ln, p(n), vs])
        if t >= T(VOICE_UNTIL + 1):                 # v3: na m24 geen koor (vocals-stem zwijgt, alleen de aria)
            choir = []
        if len(choir) > MAIN_CHOIR_VOICES:
            choir = [choir[0], choir[-1]][:MAIN_CHOIR_VOICES]
        for n in choir:
            P['choir'].append([t, t + ln, p(n), vc])
    for bar, pos, ln, strings, choir in CHORDS:
        if bar < PAD_UNTIL:                          # v8: m8-23 zit in de knippen (strijkers/PSG-bas vulden dat niet)
            continue
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
    for bar, pos, ln, notes in (SIGHS if MAIN_SIGHS else ()):
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
    # v8: m8-39 = de bas-stem in de knippen
    for b in range(40, 64):
        bass(b, BASS_G[PHRASE[b]], 92)
    bass(64, [(0, 8, 'C#3'), (8, 8, 'A2')], 80)

    # ostinato (groove)
    # v4: weg (geraden, niet uit het origineel)

    # drums (vanaf m24; gemeten in de 8-bit-cover en het origineel): 2-maatspatroon
    def hit(t, n, v, ln=S):
        P['drums'].append([t, t + ln, n, v])
    for b in range(PAD_UNTIL, 64):                 # v8: m24-39 zitten de drums (met Eb-bromtoon) in de knippen
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
        hats = ()                                   # v9: de hi-hats van het origineel zitten in de 16e-was (stuk 6)
        for h in hats:
            P['hat'].append([T(b, h), T(b, h) + S // 2, 72, 110 if h in (0, 8) else 84])

    # v3: koor = de echte roepen uit het origineel, één kitnoot per roep (eigen toonhoogte), velocity = luidheid daar
    P['choir'] = []
    gains = [float(g) for g in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                 'areazero_choir_gain.txt')).read().split()]
    for i, (bar, pos, ln) in enumerate(CHOIR_EVENTS):
        if gains[i] >= CHOIR_MIN_GAIN * max(gains):
            P['choir'].append([T(bar, pos), T(bar, pos) + ln * S, 36 + i, vel(gains[i], LVL_VOX)])
    P['lead_lo'] = [e for e in P['lead'] if e[2] <= VOICE_SPLIT]
    P['lead'] = [e for e in P['lead'] if e[2] > VOICE_SPLIT]
    for k in ('str', 'bass', 'drums', 'hat', 'bell', 'bellecho'):   # v10: zit allemaal in de knippen
        P[k] = []
    for k in P:
        P[k] = dedupe(P[k])

    write_voicegroup()
    rel = releases(VG)
    progs = {'lead': VOICE, 'lead_lo': VOICE_LO, 'sigh': SIGH, 'str': STR, 'bell': BELL}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) + 2 for k, pr in progs.items()}
    tail['choir'] = release_ticks(CHOIR_REL, TPB, BPM) + 2
    tail['drums'] = 0
    # v4: de aria niet loslaten vóór de volgende noot (detach gaf gaten = 'haperen'); belnoten van dezelfde toon afkappen
    P['bell'] = [[s0, min(e0, min([x[0] for x in P['bell'] if x[2] == n0 and x[0] > s0], default=e0)), n0, v0]
                 for s0, e0, n0, v0 in P['bell']]
    for k in ('str', 'sigh'):                       # v4: koorroepen sluiten aan (detach gaf 0,2 s stilte vóór elke roep)
        P[k] = detach(P[k], tail[k])
    tail['aria'] = release_ticks(CHOIR_REL, TPB, BPM) + 2
    tail['bellecho'] = tail['bell']
    P['bellecho'] = [[s0, min(e0, min([x[0] for x in P['bellecho'] if x[2] == n0 and x[0] > s0], default=e0)), n0, v0]
                     for s0, e0, n0, v0 in P['bellecho']]
    tail['bellrip'] = release_ticks(CHOIR_REL, TPB, BPM) + 2
    for k in ('lead', 'aria', 'choir'):             # v11: stem op twee sporen
        P[k + '2'] = [n[:] for n in P[k]]
        tail[k + '2'] = tail[k]
    tail['bellrip2'] = tail['bellrip3'] = tail['bellrip']
    order = ['aria', 'aria2', 'lead', 'lead2', 'lead_lo', 'choir', 'choir2', 'drums', 'bellrip', 'bellrip2', 'bellrip3',
             'bell', 'bellecho', 'sigh', 'str']
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
    ex_lead = [(0, mido.Message('control_change', control=1, value=0)), (0, mido.Message('pitchwheel', pitch=0))]
    ex_choir = [(0, mido.Message('control_change', control=1, value=0))]
    ex_sigh = [(0, mido.Message('control_change', control=20, value=1)),
               (0, mido.Message('control_change', control=21, value=LFOS + 6)),
               (0, mido.Message('control_change', control=1, value=SIGH_MOD))] + \
              [(t, mido.Message('pitchwheel', pitch=max(-8192, min(8191, v)))) for t, v in bend_sigh]
    TRACKS = [('lead', VOICE, LEAD_VOL, 64, ex_lead), ('lead2', VOICE, LEAD2_VOL, 64, ex_lead), ('lead_lo', VOICE_LO, LEAD_VOL, 64, ex_lead), ('choir', CHOIRKIT, 127, 64, ex_choir), ('choir2', CHOIRKIT, 127, 64, ex_choir), ('aria', ARIAKIT, 127, 64, ex_choir), ('aria2', ARIAKIT, 127, 64, ex_choir),
              ('sigh', SIGH, 66, 56, ex_sigh),
              ('str', STR, 62, 64, ()), ('bell', BELL, 17, 72, ()), ('bellecho', BELL, 17, 56, ()), ('bellrip', BELLKIT, 127, 64, ()), ('bellrip2', BELLKIT, 127, 64, ()), ('bellrip3', BELLKIT, VOL3, 64, ()), ('echo', ECHO, 30, 44, ()),
              ('ost', OST, 34, 80, ()), ('bass', BASS, 62, 64, ()), ('hat', HAT, 26, 70, ()),
              ('drums', DRUMS, 92, 64, ())]                   # m40+ zoals v7 (m24-39: drums-stem in de knip)
    free = [c for c in range(16) if c != 9]
    TRACKS = [tr for tr in TRACKS if P[tr[0]]]       # v11: lege sporen niet schrijven (mid2agb liet ze al weg)
    for k, prog, vol, pan, ex in TRACKS:
        ch = 9 if prog == DRUMS else free.pop(0)
        song.add(P[k], prog, vol, ch, pan, extra=ex)
    written = {k for k, *_ in TRACKS}
    assert not [k for k in P if P[k] and k not in written], 'partij niet weggeschreven'
    song.save(OUT, NBARS * BAR)
    print(OUT)


LEAD_P = LEAD_PROG = 82
CHOIR_REL = 200
KIT = [
    'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 200',          # 36
    'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 200',          # 37
    'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 200',         # 38
    'voice_directsound_no_resample 30, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 216',  # 39 (remix)
    'voice_directsound 50, 64, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 200',                       # 40 tom (remix)
]
CRASH, TOM = 39, 40


# ==== Battle! Area Zero (MUS_GROUNDED_VS_AREA_ZERO, 682) v2: naar de Area Zero wild battle (Scarlet/Violet) ========
# Bron (Jordi): <scratchpad>/az/src/areazero_wild_battle.mp3, Spleeter-stems in az/stems/areazero_wild_battle/.
# Gemeten: 148 bpm (drums), loop 111,1 s vanaf ±2 s; harmonie zoals Area Zero (Eb-orgelpunt <-> B/Cb maj7), bas Eb/B;
# de lead speelt de aria van Area Zero op battle-tempo (maat 5-8: F#5 Ab5 -> F6 met F#6-wisselnoot, 9-12 boven B:
# Ab4 C#5 Bb4, 13-16 F#5 Ab5 F5 -> F6, 17-20 C#6 Eb6 Bb5). Instrumenten = die van 681 (kristal, strijkers, PSG-bas,
# kit, de geknipte stem en twee koorroepen uit het origineel); geen nieuwe samples.
# Vorm (maten, 1-geteld): 1-4 intro | 5-8 A1 | 9-12 B1 | 13-16 A2 | 17-20 B2 | 21-24 brug (B -> Db, 2x) |
#   25-32 drive (groove-frase a b c d x2) | 33-34 pauze (alleen belletjes) -> loop naar 5.
OUT_VS = 'sound/songs/midi/mus_grounded_vs_area_zero.mid'
VS_BPM = 148
VS_LOOP0, VS_END = 5, 35
# lead: (maat, zestiende, lengte, noot) = gemeten bovenlijn van de 'other'-stem (per achtste)
VS_LEAD = [
    (4, 14, 2, 'F#5'),
    (5, 0, 4, 'F#5'), (5, 4, 4, 'Ab5'), (5, 8, 8, 'F6'), (6, 0, 4, 'F6'), (6, 4, 4, 'F#6'), (6, 8, 8, 'F6'),
    (7, 0, 4, 'F6'), (7, 4, 4, 'F#6'), (7, 8, 8, 'F6'), (8, 0, 6, 'F6'), (8, 6, 4, 'Eb6'), (8, 10, 2, 'Eb5'),
    (8, 12, 2, 'F5'),
    (9, 0, 4, 'Ab4'), (9, 4, 4, 'C#5'), (9, 8, 8, 'Bb4'), (10, 0, 16, 'Bb4'),
    (11, 0, 2, 'Bb4'), (11, 4, 4, 'C#5'), (11, 8, 8, 'Bb4'), (12, 0, 8, 'Bb4'), (12, 8, 4, 'Ab4'), (12, 12, 2, 'Bb4'),
    (12, 14, 2, 'F#5'),
    (13, 0, 2, 'F#5'), (13, 4, 4, 'Ab5'), (13, 8, 8, 'F5'), (14, 0, 4, 'F#5'), (14, 4, 2, 'Ab5'), (14, 6, 10, 'F5'),
    (15, 0, 2, 'F5'), (15, 4, 2, 'Bb5'), (15, 6, 10, 'F6'), (16, 0, 10, 'F6'), (16, 10, 4, 'F#6'), (16, 14, 4, 'C#6'),
    (17, 2, 2, 'Eb6'), (17, 6, 10, 'Bb5'), (18, 0, 4, 'Bb5'), (18, 12, 2, 'F#5'),
    (19, 0, 4, 'C#6'), (19, 4, 2, 'B5'), (19, 6, 10, 'Bb5'), (20, 0, 8, 'Bb5'), (20, 8, 2, 'Ab5'), (20, 12, 2, 'Bb5'),
]
VS_B = (9, 10, 11, 12, 17, 18, 19, 20)       # B (Cb); de rest van 5-20 is Eb


def build_remix():
    P = {k: [] for k in ('lead', 'lead_lo', 'choir', 'str', 'bell', 'bass', 'hat', 'drums')}

    def bells(bar, cell, vel, ring=3):
        for pos, n in cell:
            t = T(bar, pos)
            P['bell'].append([t, t + ring * S, p(n), vel])

    def chord(bar, pos, ln, strings, vs=76):
        for n in strings:
            P['str'].append([T(bar, pos), T(bar, pos) + ln * S, p(n), vs])

    def hit(t, n, v, ln=S):
        P['drums'].append([t, t + ln, n, v])

    def bass8(bar, root, alt=None, vel=100):
        for i in range(8):
            n = p(root) + (12 if i in (3, 6) else 0)
            if alt and i == 7:
                n = p(alt)
            P['bass'].append([T(bar, 2 * i), T(bar, 2 * i) + 2 * S - 6, n, vel if i in (0, 3, 6) else vel - 18])

    def hats(bar, step=1, vel=(100, 64)):
        for i in range(0, 16, step):
            P['hat'].append([T(bar, i), T(bar, i) + S // 2, 72, vel[0] if i % 4 == 2 else vel[1]])

    def four(bar, crash=False, fill=False):
        for q in (0, 4, 8, 12):
            hit(T(bar, q), KICK, 112 if q in (0, 8) else 100)
        hit(T(bar, 4), SNARE, 104); hit(T(bar, 12), SNARE, 110)
        if crash:
            hit(T(bar, 0), CRASH, 112, 4 * S)
        if fill:
            for i in (13, 14, 15):
                hit(T(bar, i), SNARE, 80 + 8 * (i - 13))

    # koorroepen uit het origineel (zelfde kit als 681): Eb-akkoord = roep 1 (m9), B-akkoord = roep 2 (m12)
    def roep(bar, i, ln=32, vel=96):
        P['choir'].append([T(bar), T(bar) + ln * S, 36 + i, vel])

    # intro 1-4: kristal-arpeggio + Eb-orgelpunt, kick op de tellen in maat 3-4
    for b in (1, 2, 3):
        bells(b, INTRO, 92, ring=6)
    bells(4, INTRO4, 92, ring=6)
    chord(1, 0, 64, ['Eb3', 'Bb3'], 66)
    for b in (3, 4):
        for q in (0, 4, 8, 12):
            hit(T(b, q), KICK, 90 + 4 * (b - 3))
        hats(b, 2, (80, 56))
    for i in range(8, 16):
        hit(T(4, i), SNARE, 60 + 6 * (i - 8))
    P['bass'] += [[T(b), T(b) + 16 * S - 6, p('Eb2'), 90] for b in (1, 2, 3, 4)]

    # A/B (5-20)
    for b in range(5, 21):
        isB = b in VS_B
        chord(b, 0, 16, ['B2', 'B3'] if isB else ['Eb3', 'Bb3'])
        bells(b, CELL_B if isB else G_A, 70)
        bass8(b, 'B2' if isB else 'Eb2', alt=('Bb2' if isB else 'D2') if b % 4 == 0 else None)
        four(b, crash=b in (5, 9), fill=b in (8, 12, 16, 20))   # geen bekken in 13/17: daar 12 kanalen (gemeten)
        hats(b)
        if (b - 5) % 2 == 0:
            roep(b, 2 if isB else 1, vel=88)
    # brug 21-24: B -> Db (bVI-bVII) vier keer, halve tijd
    for b in range(21, 25):
        for pos, ln, strings, choir in GROOVE['BD']:
            chord(b, pos, ln, strings, 80)
        bells(b, G_BD, 74)
        for i in range(8):
            n = 'B2' if i < 4 else 'C#3'
            P['bass'].append([T(b, 2 * i), T(b, 2 * i) + 2 * S - 6, p(n) + (12 if i in (3, 6) else 0), 100])
        hit(T(b, 0), KICK, 112); hit(T(b, 8), SNARE, 110); hit(T(b, 10), KICK, 92)
        hats(b, 2, (96, 66))
    for i in range(0, 16):
        hit(T(24, i), SNARE, 64 + 3 * i)
    # drive 25-32: groove-frase van 681 (a b c d) op battle-drums
    for k, b in enumerate(range(25, 33)):
        ph = 'abcd'[k % 4]
        for pos, ln, strings, choir in GROOVE[ph]:
            chord(b, pos, ln, strings, 74)
        bells(b, {'a': G_A, 'c': G_A, 'b': G_B, 'd': G_D}[ph], 74)
        bass8(b, 'Eb2', alt={'a': 'E2', 'c': 'D2', 'd': 'C#2'}.get(ph))
        four(b, crash=b in (25, 29), fill=b in (28, 32))
        hats(b)
        if k % 2 == 0:
            roep(b, 1, vel=84)
    # pauze 33-34: alleen belletjes (de adem van Area Zero), daarna terug naar A1
    bells(33, CELL, 84, ring=6)
    bells(34, CELL, 84, ring=6)
    for i in range(8, 16):
        hit(T(34, i), SNARE, 56 + 7 * (i - 8))

    for bar, pos, ln, n in VS_LEAD:
        P['lead_lo' if p(n) <= VOICE_SPLIT else 'lead'].append([T(bar, pos), T(bar, pos) + ln * S, p(n), 104])
    for k in P:
        P[k] = dedupe(P[k])
    P['bell'] = [[s0, min(e0, min([x[0] for x in P['bell'] if x[2] == n0 and x[0] > s0], default=e0)), n0, v0]
                 for s0, e0, n0, v0 in P['bell']]
    rel = releases(VG)
    progs = {'lead': VOICE, 'lead_lo': VOICE_LO, 'str': STR, 'bell': BELL}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, VS_BPM) + 2 for k, pr in progs.items()}
    tail['choir'] = release_ticks(CHOIR_REL, TPB, VS_BPM) + 2
    P['str'] = detach(legato(P['str']), tail['str'])      # één lange strijkersnoot per akkoord (minder uitklinkers)
    order = ['lead', 'lead_lo', 'choir', 'bell', 'str']
    dl = {KICK: 2 * S, SNARE: 2 * S, CRASH: 8 * S, TOM: 3 * S}
    busy = [(e[0], e[0] + dl.get(e[2], 2 * S)) for e in P['drums']]
    # stemverdeler op 10 (gemeten in de game: uitklinkers duren langer dan berekend; zo blijft het <= 11)
    kept = allocate({k: P[k] for k in order}, order, tail, max_voices=10, preset=busy)
    for k in order:
        n = len(P[k])
        if n:
            print('  %-7s %4d noten, %3d weg (%.0f%%)' % (k, n, n - len(kept[k]), 100 * (n - len(kept[k])) / n))
        P[k] = kept[k]

    song = Song(TPB, 500000)
    song.tempo(0, VS_BPM / 120)
    song.loop = (T(VS_LOOP0), T(VS_END))
    ex0 = [(0, mido.Message('control_change', control=1, value=0)), (0, mido.Message('pitchwheel', pitch=0))]
    TRACKS = [('lead', VOICE, 90, 64, ex0), ('lead_lo', VOICE_LO, 90, 64, ex0), ('choir', CHOIRKIT, 72, 64, ex0[:1]),
              ('str', STR, 60, 64, ()), ('bell', BELL, 64, 72, ()), ('bass', BASS, 66, 64, ()),
              ('hat', HAT, 28, 70, ()), ('drums', DRUMS, 100, 64, ())]
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
        VOICE: 'voice_directsound 60, 0, DirectSoundWaveData_az_voice, 40, 0, 255, 190',     # rustige aanzet
        VOICE_LO: 'voice_directsound 60, 0, DirectSoundWaveData_az_voice_lo, 40, 0, 255, 190',
        CHOIRKIT: 'voice_keysplit_all voicegroup_area_zero_choir',
        ARIAKIT: 'voice_keysplit_all voicegroup_area_zero_aria',
        BELLKIT: 'voice_keysplit_all voicegroup_area_zero_bells',
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
    for lab in ['az_crystal', 'az_voice', 'az_voice_lo'] + ['az_choir_%02d' % i for i in range(len(CHOIR_EVENTS))] + \
            ['az_aria_%d' % j for j in range(len(ARIA_PHRASES))] + ['az_bells_%d' % j for j in range(len(BELL_RIPS))]:
        if 'DirectSoundWaveData_%s::' % lab not in txt:
            txt = txt.rstrip('\n') + ('\n\n\t.align 2\nDirectSoundWaveData_%s::\n'
                                      '\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (lab, lab))
    open(dsd, 'w').write(txt)
    open('sound/voicegroups/drumsets/area_zero_choir.inc', 'w').write(
        '@ Project Grounded: de koorroepen van Area Zero, geknipt uit het origineel (areazero_samples.py); noot 36+i = roep i\n'
        '@ (CHOIR_EVENTS), op de eigen toonhoogte.\n'
        'voice_group area_zero_choir, 36\n' + ''.join(
            '\tvoice_directsound 60, 0, DirectSoundWaveData_az_choir_%02d, 255, 0, 255, %d\n' % (i, CHOIR_REL)
            for i in range(len(CHOIR_EVENTS))) + '\n')
    open('sound/voicegroups/drumsets/area_zero_aria.inc', 'w').write(
        '@ Project Grounded: de aria van Area Zero in frasen, geknipt uit het origineel (areazero_samples.py); noot 36+j =\n'
        '@ frase j (ARIA_PHRASES), op de eigen toonhoogte.\n'
        'voice_group area_zero_aria, 36\n' + ''.join(
            '\tvoice_directsound 60, 0, DirectSoundWaveData_az_aria_%d, 255, 0, 255, %d\n' % (j, CHOIR_REL)
            for j in range(len(ARIA_PHRASES))) + '\n')
    open('sound/voicegroups/drumsets/area_zero_bells.inc', 'w').write(
        '@ Project Grounded: de begeleiding van Area Zero m1-64 (belletjes, akkoordklank, bas; vanaf m24 met de\n'
        '@ drums-stem), geknipt uit het origineel in aansluitende stukken (areazero_samples.py BELL_RIPS).\n'
        'voice_group area_zero_bells, 36\n' + ''.join(
            '\tvoice_directsound 60, 0, DirectSoundWaveData_az_bells_%d, 255, 0, 255, %d\n' % (j, CHOIR_REL)
            for j in range(len(BELL_RIPS))) + '\n')
    vgi = 'sound/voice_groups.inc'
    txt = open(vgi).read()
    for inc in ('drumsets/area_zero.inc', 'drumsets/area_zero_choir.inc', 'drumsets/area_zero_aria.inc', 'drumsets/area_zero_bells.inc',
                'keysplits/area_zero_strings.inc', '%s.inc' % VG):
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
    # 682 (Battle! Area Zero) komt sinds okt 10 uit vs_areazero_theme.py (het origineel in knippen); build_remix() is
    # de oude nabouw (v2, geschrapt) en schrijft niet meer.
    if '--render' in sys.argv:
        d = sys.argv[sys.argv.index('--render') + 1]
        render_gm(d)
