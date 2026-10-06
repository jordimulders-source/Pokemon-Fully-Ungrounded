#!/usr/bin/env python3
"""Project Grounded: "Battle! Ho-Oh" (song 658, MUS_GROUNDED_VS_HO_OH), eigen compositie.

Jordi: "Ho-Oh heeft een vurig theme, tegelijkertijd met Japanse instrumentatie, heel tof, lekker hoog tempo".
-> 180 bpm, 4/4, E-frygisch rockfundament (powerchords E-A-F-E / A-C-F-E) onder een melodie in de Japanse
   in-toonladder (miyako-bushi: E F A B C). De regenboog-sectie staat in de yo-toonladder op G (G A C D E), de climax
   is het hoofdthema een hele toon hoger (F# in: F# G B C# D) en valt via F5 -> E (frygische cadens) terug naar de loop.
Lore: heilig vuur (Burned Tower / Tin Tower), de regenboogveer, de drie beesten die uit de as herrezen.

Vorm (maat = 1,333 s):
  intro  i1-i4  (5,3 s)  taiko-slag + aanzwellende shakuhachi, taiko-roffel + koto-glissando (cry ±2,3-3 s: geen
                          drop daar), i4 = unisono-run van de hele band in de in-toonladder + tomfill
  [loop]
  A     1-8   hoofdthema op de shakuhachi (met meri-buiginkjes), distortion-chugs, taiko + rockkit, koto in achtsten
  A'    9-16  thema op de trompet + shinobue (whistle) een octaaf hoger, koto in zestienden, strijkers-achtsten
  B    17-24  'regenboog': yo-toonladder op G, hoorn + strijkers zingen, koor, koto-arpeggio's, PSG-fonkeling,
              shinobue-antwoorden in de rusten
  C    25-32  heilig vuur: kumi-daiko (taiko, grote trom, hyoshigi, tsuzumi), shamisen-riff (lage koto) met
              shakuhachi-antwoord; 29-32 opbouw (kick, snareroffel, stijgende strijkers, koperstoten)
  D    33-40  climax: thema een hele toon hoger op trompet + shinobue, alles vol; maat 40 F5 -> E terug naar 1
  ]
Instrumenten (alleen stock-Emerald-samples; voicegroup grounded_hooh, gegenereerd op basis van grounded_gm):
  77 shakuhachi (sd90_classical_shakuhachi, klinkt C5 op toets 60), 78 shinobue (sd90_classical_whistle, C6 op 60),
  107 koto (unknown_koto_high, C5 op 60), 106 'shamisen' (unknown_koto_low, C4 op 60, kort), 30 distortion-gitaar
  (sd90_classical_distortion_guitar_low, C3 op 60), 33 fingered bass, 56 trompet, 60 hoorn, 48 strijkers, 52 koor,
  81 PSG-vierkant (fonkeling), 120 PSG-ruis (hihat), 127 = drumkit drumsets/hooh.inc (kick, snare, taiko hoog/laag,
  grote trom, 3 toms, hyoshigi, atarigane, kotsuzumi, ohtsuzumi, 2 bekkens, orkestsnare; geen PSG-drumnoten).
Noten staan hieronder op klinkende toonhoogte; OCT zet ze om naar de toets voor de GBA-sample.
Gebruik: python3 tools/grounded/hooh_theme.py [--render <map>]"""
import os, subprocess, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

OUT = 'sound/songs/midi/mus_grounded_vs_ho_oh.mid'
VG = 'grounded_hooh'
TPB = 48
S16 = TPB // 4
BAR = TPB * 4
BPM = 180
INTRO = 4
NLOOP = 40
END = INTRO + NLOOP
MAX_V = 11                                   # legendary: 11 DirectSound-noten

SHAKU, FUE, KOTO, SHAMI, GTR, BASS, TPT, HORN, STR, CHOIR, SQ, NOISE, DRUMS = 77, 78, 107, 106, 30, 33, 56, 60, 48, \
    52, 81, 120, 127
OCT = {SHAKU: -12, FUE: -24, KOTO: -12, SHAMI: 0, GTR: 12}      # klinkend -> toets (gemeten grondtoon van de sample)
KICK, SNARE, TAIKO, TAIKO_LO, ODAIKO, TOM_HI, TOM_MID, TOM_LO, HYOU, KANE, KOTSU, OHTSU, CRASH, CRASH2, OSNARE = \
    range(36, 51)

N = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8,
     'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def p(name):
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


def at(lb, q=0):
    """tick van 16e q in loopmaat lb (1 = loopbegin); lb <= 0 = intro (i1 = -3 ... i4 = 0)."""
    return (INTRO + lb - 1) * BAR + q * S16


def seq(out, lb, s, vel=100, shift=0):
    """'q:len:NOOT[:vel] ...' in maat lb."""
    for tok in s.split():
        f = tok.split(':')
        q, ln, nt = float(f[0]), float(f[1]), f[2]
        v = int(f[3]) if len(f) > 3 else vel
        st = at(lb) + int(q * S16)
        out.append([st, st + int(ln * S16), p(nt) + shift, v])


# ---------------------------------------------------------------- het hoofdthema (in-toonladder E F A B C) ------------
THEME = [
    '0:6:E5 6:2:F5 8:4:E5 12:2:C5 14:2:B4',
    '0:8:A4 8:2:B4 10:2:C5 12:2:B4 14:2:A4',
    '0:4:F4 4:2:A4 6:2:B4 8:4:C5 12:4:E5',
    '0:12:B4 12:2:A4 14:2:B4',
    '0:4:E5 4:2:F5 6:2:A5 8:4:B5 12:2:A5 14:2:F5',
    '0:6:E5 6:2:C5 8:4:B4 12:2:C5 14:2:E5',
    '0:4:F5 4:2:E5 6:2:C5 8:2:B4 10:2:A4 12:2:F4 14:2:A4',
    '0:12:E4 12:2:B4 14:2:C5',
]
THEME_END2 = ['0:4:F5 4:4:A5 8:4:B5 12:4:C6', '0:8:B5 8:2:A5 10:2:B5 12:4:D6']     # A': opgang naar de yo-sectie
CLIMAX_END = '0:4:F5 4:4:E5 8:2:C5 10:2:B4 12:2:B4 14:2:C5'                        # maat 40: terug naar E
BENDS = {(2, 0), (4, 0), (8, 0)}               # (maat in het thema, 16e): meri-buiging omhoog naar de noot

# akkoordgrondtonen per maat (klinkend, powerchord = grondtoon + kwint)
CH_A = ['E2', 'A2', 'F2', 'E2', 'A2', 'C3', 'F2', 'E2']
CH_A2 = ['E2', 'A2', 'F2', 'E2', 'A2', 'C3', 'F2', 'D2']
CH_B = ['C3', 'A2', 'E2', 'D2', 'C3', 'D2', 'E2', 'D2']
CH_D = ['F#2', 'B2', 'G2', 'F#2', 'B2', 'D3', 'G2', 'F2']
# yo-melodie (G A C D E)
YO = [
    '0:4:G4 4:4:A4 8:6:C5 14:2:D5',
    '0:8:E5 8:4:D5 12:2:C5 14:2:A4',
    '0:6:G4 6:2:A4 8:8:E4',
    '0:4:D4 4:2:E4 6:2:G4 8:8:A4',
    '0:4:C5 4:4:D5 8:6:E5 14:2:G5',
    '0:8:A5 8:4:G5 12:2:E5 14:2:D5',
    '0:12:E5 12:2:D5 14:2:C5',
    '0:8:D5 8:8:E5',
]
YO_FUE = {3: '12:1:G5 13:1:A5 14:1:C6 15:1:D6', 4: '12:1:E6 13:1:D6 14:1:C6 15:1:A5',
          7: '12:1:D6 13:1:E6 14:2:G6', 8: '0:2:A6:84 2:2:G6:84 4:2:E6:84 6:2:D6:84'}


def theme(out, first, shift=0, ends=None, vel=100, end_shift=None, top=None):
    """hoofdthema vanaf maat first; ends vervangt de laatste maten (met end_shift, standaard = shift);
    top = hoogste noot (hoger valt een octaaf terug, tegen schel)."""
    tmp = []
    for i, s in enumerate(THEME):
        lb, sh = first + i, shift
        if ends and i >= 8 - len(ends):
            s = ends[i - (8 - len(ends))]
            sh = shift if end_shift is None else end_shift
        seq(tmp, lb, s, vel, sh)
    for e in tmp:
        if top and e[2] > p(top):
            e[2] -= 12
    out += tmp


def shaku_bends(notes):
    """meri/kari: de noot begint een halve toon te laag en buigt in één 16e omhoog (BENDR 2: 4096 = 1 halve toon)."""
    ev = [(0, mido.Message('control_change', control=20, value=2)), (0, mido.Message('pitchwheel', pitch=0))]
    for bar, q in sorted(BENDS):                           # alleen in A (de shakuhachi-versie)
        st = at(bar, q)
        if not any(e[0] == st for e in notes):
            continue
        ev.append((st, mido.Message('pitchwheel', pitch=-4096)))
        for k in range(1, 5):
            ev.append((st + k * 3, mido.Message('pitchwheel', pitch=min(0, -4096 + k * 1024))))
    return ev


# ---------------------------------------------------------------- partijen ------------------------------------------
def shakuhachi():
    out = []
    seq(out, -3, '0:16:E5:70')                           # intro: aanzwellende lange noot
    seq(out, -2, '0:8:F5:84 8:8:E5:92')
    seq(out, -1, '0:12:B5:100 12:4:A5:96')
    theme(out, 1)
    # C: antwoorden op het shamisen-riff
    seq(out, 27, '0:6:B4 6:2:C5 8:2:B4 10:2:A4 12:4:F4')
    seq(out, 28, '0:8:E4 8:2:A4 10:2:B4 12:4:E5')
    seq(out, 31, '0:4:E5 4:2:F5 6:2:A5 8:4:B5 12:4:C6')
    seq(out, 32, '0:8:B5 8:2:C6:90 10:2:B5:90 12:4:E6:104')
    return dedupe(out)


def shinobue():
    out = []
    theme(out, 9, 12, THEME_END2, 88, top='A6')            # A': octaaf boven de trompet
    for k, s in YO_FUE.items():
        seq(out, 16 + k, s, 84)
    theme(out, 33, 14, [CLIMAX_END], 90, end_shift=12, top='A6')   # D: thema +2, octaaf hoger
    return dedupe(out)


def trumpet():
    out = []
    # intro i4: unisono-run van de hele band
    seq(out, 0, '0:2:E5:110 2:2:C5:104 4:2:B4:104 6:2:A4:104 8:2:F4:108 10:2:E4:110 12:2:F4:112 14:2:B4:116')
    # A: koperstoten aan het eind van elke 4 maten
    for lb in (4, 8):
        seq(out, lb, '10:1:B4:112 10:1:E5:112 12:2:B4:118 12:2:E5:118 14:1:C5:110 14:1:F5:110')
    theme(out, 9, 0, THEME_END2, 106)                      # A': melodie
    # B: stoten op de akkoordwissels (17-20), daarna zingt de trompet de hoge helft van de yo-melodie (21-24)
    for lb, b in zip(range(17, 21), ['G4', 'E4', 'E4', 'D4']):
        seq(out, lb, '0:2:%s:100' % b)
    for i, s in enumerate(YO[4:]):
        seq(out, 21 + i, s, 104)
    # C: koperstoten in de opbouw
    seq(out, 30, '12:1:E4:100 12:1:B4:100 14:1:E4:106 14:1:B4:106')
    seq(out, 32, '0:2:F4:112 0:2:C5:112 3:1:F4:108 3:1:C5:108 6:2:A4:114 6:2:E5:114 12:4:B4:120 12:4:F5:120')
    theme(out, 33, 2, [CLIMAX_END], 110, end_shift=0)      # D: climax
    return dedupe(out)


def horn():
    out = []
    for i, s in enumerate(YO[:4]):                         # B eerste helft (de trompet neemt de hoge helft over)
        seq(out, 17 + i, s, 100)
    # C: lange roep in 25-26 en 29-30
    seq(out, 25, '0:12:E4:92 12:4:F4:92')
    seq(out, 26, '0:16:E4:84')
    seq(out, 29, '0:12:B4:96 12:4:C5:96')
    seq(out, 30, '0:12:B4:92')
    return dedupe(out)


def horn2():
    """tegenstemmen (lage prioriteit, zelfde spoor als de hoorn)."""
    out = []
    for lb, n in zip(range(9, 17), ['B3', 'C4', 'C4', 'B3', 'C4', 'E4', 'C4', 'A3']):   # A': onder de trompet
        seq(out, lb, '0:16:%s:76' % n)
    return dedupe(out)


KOTO_CELL = {   # 8 zestienden per halve maat, tonen uit de in-toonladder (E F A B C) / yo (G A C D E)
    'E': 'E5 B4 C5 B4 E5 B4 F5 B4', 'A': 'A4 E5 F5 E5 C5 E5 A5 E5', 'F': 'F4 C5 E5 C5 A4 C5 F5 C5',
    'C': 'C5 B4 E5 B4 A4 B4 E5 B4', 'D': 'D5 A4 C5 A4 E5 A4 D5 A4',
    'F#': 'F#5 C#5 D5 C#5 F#5 C#5 G5 C#5', 'B': 'B4 F#5 G5 F#5 D5 F#5 B5 F#5', 'G': 'G4 D5 F#5 D5 B4 D5 G5 D5',
    'D3': 'D5 C#5 F#5 C#5 B4 C#5 F#5 C#5', 'Fn': 'F4 C5 E5 C5 A4 C5 F5 C5',
}
YO_ARP = {'C3': 'C5 D5 G5 D5 E5 G5 C6 G5', 'A2': 'A4 C5 E5 C5 D5 E5 A5 E5', 'E2': 'E5 G5 A5 G5 D5 G5 E6 G5',
          'D2': 'D5 E5 A5 E5 G5 A5 D6 A5'}


def koto():
    out = []
    # intro i2: glissando omhoog door de in-toonladder (E4 -> E6), i3: tremolo op E5/B5
    run = 'E4 F4 A4 B4 C5 E5 F5 A5 B5 C6 E6'.split()
    for i, n in enumerate(run):
        seq(out, -2, '%d:1:%s:%d' % (i + 5, n, 70 + i * 4))
    for q in range(16):
        seq(out, -1, '%d:1:%s:%d' % (q, 'E5' if q % 2 == 0 else 'B5', 70 + q * 2))

    def cell(lb, key, step):
        notes = KOTO_CELL[key].split()
        for h in range(2):
            for j in range(0, 8, step):
                seq(out, lb, '%d:%d:%s:%d' % (h * 8 + j, step, notes[j], 90 if j == 0 else 76))
    names = lambda ch: [c[:-1] for c in ch]
    for i, k in enumerate(names(CH_A)):
        cell(1 + i, k, 2)                                    # A: achtsten (thema voorop)
    for i, k in enumerate(names(CH_A2)):
        cell(9 + i, k, 1)                                    # A': zestienden
    for i, ch in enumerate(CH_B):
        notes = YO_ARP[ch].split()
        for h in range(2):
            for j in range(8):
                seq(out, 17 + i, '%d:1:%s:%d' % (h * 8 + j, notes[j], 82 if j == 0 else 68))
    for i, k in enumerate(['F#', 'B', 'G', 'F#', 'B', 'D3', 'G', 'Fn']):
        cell(33 + i, k, 1)                                   # D: zestienden
    # C 29-32: koto verdubbelt het riff een octaaf hoger
    riff(out, 25, 12, 70, 29)
    return dedupe(out)


RIFF = ['0:2:E3 3:1:E3 4:2:F3 6:2:E3 8:2:B3 10:2:A3 12:2:F3 14:2:E3',
        '0:2:E3 2:2:B3 4:3:C4 7:1:B3 8:4:A3 12:2:F3 14:2:A3']


def tight(ev, tail):
    """tokkels (koto/shamisen): noot + uitklinktijd past precies tot de volgende aanslag (min. 3 ticks)."""
    ev = sorted(ev)
    starts = sorted(set(e[0] for e in ev))
    out = []
    for e in ev:
        nxt = next((t for t in starts if t > e[0]), None)
        end = e[1] if nxt is None else min(e[1], max(e[0] + 3, nxt - tail))
        out.append([e[0], end, e[2], e[3]])
    return out


def no_overlap(ev):
    ev = sorted(ev)
    for i, e in enumerate(ev):
        nxt = next((x[0] for x in ev[i + 1:] if x[2] == e[2] and x[0] >= e[0]), None)
        if nxt is not None and nxt < e[1]:
            e[1] = max(e[0] + 1, nxt)
    return ev


def riff(out, lb, shift=0, vel=104, dest=None):
    for k in range(2):
        seq(out, (dest if dest else lb) + k, RIFF[k], vel, shift)


def shamisen():
    out = []
    seq(out, -3, '8:1:E3:90 10:1:E3:90 12:1:F3:96 14:1:E3:100')   # intro: shamisen-tikjes onder de taiko
    for lb in (25, 29):
        riff(out, lb)
    for lb in (27, 31):                                    # onder het shakuhachi-antwoord: kale grondtoon
        seq(out, lb, '0:1:E3:84 6:1:E3:84 8:1:E3:84 14:1:E3:84')
        seq(out, lb + 1, '0:1:E3:84 6:1:E3:84 8:1:E3:84 14:1:E3:84')
    # D: off-beat-stoten in de climax
    for i, r in enumerate(CH_D):
        n = p(r) + 12
        for q in (2, 6, 10, 14):
            out.append([at(33 + i, q), at(33 + i, q) + S16, n, 84])
    return dedupe(out)


def power(out, lb, root, pat, vel=108):
    """pat: lijst (16e, lengte) chugs op de grondtoon (gitaar speelt alleen de grondtoon; sample is vet genoeg)."""
    for q, ln in pat:
        st = at(lb) + q * S16
        out.append([st, st + ln * S16 - 2, p(root), vel if q % 4 == 0 else vel - 14])


CHUG = [(0, 2), (2, 1), (3, 1), (4, 2), (6, 2), (8, 2), (10, 1), (11, 1), (12, 2), (14, 2)]
CHUG_B = [(0, 3), (3, 3), (6, 2), (8, 3), (11, 3), (14, 2)]


def guitar():
    out = []
    power(out, 0, 'E2', [(0, 2), (2, 2), (4, 2), (6, 2), (8, 2), (10, 2), (12, 2), (14, 2)], 104)
    for i, r in enumerate(CH_A):
        power(out, 1 + i, r, CHUG)
    for i, r in enumerate(CH_A2):
        power(out, 9 + i, r, CHUG)
    for i, r in enumerate(CH_B):
        power(out, 17 + i, r, CHUG_B, 100)
    for lb in (29, 30):
        power(out, lb, 'E2', [(q, 2) for q in range(0, 16, 2)], 96)
    for lb in (31, 32):
        power(out, lb, 'E2' if lb == 31 else 'F2', [(q, 1) for q in range(16)], 92)
    for i, r in enumerate(CH_D):
        power(out, 33 + i, r, CHUG, 112)
    return dedupe(out)


def bass():
    out = []
    seq(out, -3, '0:16:E2:90')
    seq(out, -2, '0:16:E2:96')
    seq(out, -1, '0:16:E2:104')
    seq(out, 0, '0:2:E2 2:2:E2 4:2:E2 6:2:E2 8:2:F2 10:2:E2 12:2:F2 14:2:B1')

    def eighths(lb, root, vel=104):
        r = p(root) if p(root) <= p('C3') else p(root) - 12
        for q in range(0, 16, 2):
            n = r + 12 if q in (6, 14) else r
            out.append([at(lb, q), at(lb, q) + 2 * S16 - 3, n, vel])
    for i, r in enumerate(CH_A):
        eighths(1 + i, r)
    for i, r in enumerate(CH_A2):
        eighths(9 + i, r)
    for i, r in enumerate(CH_B):
        eighths(17 + i, r, 100)
    for lb in range(25, 29):
        seq(out, lb, '0:4:E1:104 6:2:E2:96 8:4:E1:100 12:2:B1:96 14:2:E2:96')
    for lb in range(29, 33):
        eighths(lb, 'E2' if lb < 32 else 'F2')
    for i, r in enumerate(CH_D):
        eighths(33 + i, r, 108)
    return dedupe(out)


def strings():
    out = []
    for q in range(16):                                    # intro i1: tremolo E4/B4 crescendo
        seq(out, -3, '%d:1:E4:%d %d:1:B4:%d' % (q, 40 + q * 3, q, 40 + q * 3))
    # A: lange noot op de bovenste akkoordtoon (in stukken van 2 tellen)
    for i, n in enumerate(['B4', 'A4', 'C5', 'B4', 'A4', 'C5', 'C5', 'B4']):
        seq(out, 1 + i, '0:8:%s:64 8:8:%s:60' % (n, n))
    # A': staccato-kwarten op de bovenste akkoordtoon
    for i, n in enumerate(['B4', 'A4', 'C5', 'B4', 'A4', 'C5', 'C5', 'A4']):
        for q in range(0, 16, 4):
            seq(out, 9 + i, '%d:1:%s:%d' % (q, n, 86 if q % 8 == 0 else 74))
    # C 29-32: stijgende lange noten door de in-toonladder (de zestienden-run staat op het PSG-vierkant)
    for k, n in enumerate('E4 F4 A4 B4 C5 E5 F5 A5'.split()):
        seq(out, 29 + k // 2, '%d:8:%s:%d' % ((k % 2) * 8, n, 70 + k * 4))
    # D: lange tweeklanken (F# in)
    for i, (a, b) in enumerate([('F#4', 'C#5'), ('F#4', 'B4'), ('G4', 'D5'), ('F#4', 'C#5'), ('F#4', 'B4'),
                                ('F#4', 'D5'), ('G4', 'D5'), ('F4', 'C5')]):
        seq(out, 33 + i, '0:8:%s:70 8:8:%s:66' % (b, b))
    return dedupe(out)


def choir():
    out = []
    for i, ch in enumerate(['G4', 'E4', 'E4', 'A4', 'G4', 'A4', 'E4', 'A4']):    # B: lange 'aah' (2 tellen per stuk)
        for h in range(2):
            seq(out, 17 + i, '%d:8:%s:%d' % (h * 8, ch, 74))
    for i, ch in enumerate(['F#4', 'B3', 'G4', 'F#4', 'B3', 'D4', 'G4', 'F4']):  # D: koor op de grondtoon
        for h in range(2):
            seq(out, 33 + i, '%d:8:%s:%d' % (h * 8, ch, 74))
    return dedupe(out)


def sparkle():
    """PSG-vierkant: fonkelende arpeggio's (regenboog) in B en de climax; kost geen DirectSound-kanaal."""
    out = []
    for i, ch in enumerate(CH_B):
        notes = YO_ARP[ch].split()
        for h in range(2):
            for j in range(8):
                st = at(17 + i, h * 8 + j)
                out.append([st, st + 8, p(notes[j]), 52])
    cells = ['F#', 'B', 'G', 'F#', 'B', 'D3', 'G', 'Fn']
    for i, k in enumerate(cells):
        notes = KOTO_CELL[k].split()
        for h in range(2):
            for j in range(8):
                st = at(33 + i, h * 8 + j) + 3 * S16                 # delay-echo van de koto, 3 zestienden later
                if st < at(41):
                    out.append([st, st + 8, p(notes[j]), 40])
    scale = [p(x) for x in 'E4 F4 A4 B4 C5 E5 F5 A5 B5 C6 E6 F6 A6 B6 C7 E7'.split()]
    for k in range(64):                                  # C 29-32: stijgende zestienden-run (vuur dat oplaait)
        lb, q = 29 + k // 16, k % 16
        out.append([at(lb, q), at(lb, q) + 8, scale[min(15, k // 4)] - 12, 36 + k // 3])
    return dedupe(out)


def hats():
    """PSG-ruis: hihat (gesloten in achtsten, accent op de tel; zestienden in A' en D)."""
    out = []
    for lb in range(1, 41):
        if 25 <= lb <= 28:
            continue
        step = 1 if (9 <= lb <= 16 or lb >= 33 or lb >= 31) else 2
        for q in range(0, 16, step):
            v = 70 if q % 4 == 0 else (54 if q % 2 == 0 else 40)
            out.append([at(lb, q), at(lb, q) + 5, 80, v])
    return dedupe(out)


def drums():
    kit, tk, pc = [], [], []

    def hit(lst, lb, q, note, vel, ln=2):
        st = at(lb) + int(q * S16)
        lst.append([st, st + int(ln * S16), note, vel])

    # ---- intro
    hit(tk, -3, 0, ODAIKO, 127, 4)
    hit(kit, -3, 0, CRASH, 110, 4)
    for q in (8, 11, 12, 14):
        hit(tk, -3, q, TAIKO_LO, 88 + q)
    for q in range(0, 16, 2):
        hit(tk, -2, q, TAIKO if q % 4 == 0 else TAIKO_LO, 84 + q * 2)
    hit(pc, -2, 0, HYOU, 100)
    hit(pc, -2, 8, HYOU, 100)
    for q in range(16):
        hit(tk, -1, q, TAIKO if q % 2 == 0 else TAIKO_LO, 90 + q * 2)
        hit(kit, -1, q, OSNARE, 60 + q * 3, 1)
    hit(pc, -1, 14, OHTSU, 116)
    hit(kit, 0, 0, CRASH, 120, 4)
    hit(kit, 0, 0, KICK, 124)
    hit(tk, 0, 0, ODAIKO, 124, 4)
    for q in range(2, 12, 2):
        hit(kit, 0, q, KICK, 112)
    for q, t in ((12, TOM_HI), (13, TOM_HI), (14, TOM_MID), (15, TOM_LO)):
        hit(kit, 0, q, t, 116)

    def rock(lb, double=False, taiko=True):
        for q in ((0, 6, 8, 10) if not double else range(0, 16, 2)):
            hit(kit, lb, q, KICK, 120 if q % 4 == 0 else 108)
        for q in (4, 12):
            hit(kit, lb, q, SNARE, 118)
        if taiko:
            hit(tk, lb, 0, TAIKO, 116)
            hit(tk, lb, 8, TAIKO, 110)
            hit(tk, lb, 14, TAIKO_LO, 104)

    for lb in range(1, 17):
        rock(lb, double=lb >= 13)
    for lb in (1, 9):
        hit(kit, lb, 0, CRASH, 116, 4)
    hit(kit, 5, 0, CRASH2, 104, 6)
    hit(kit, 13, 0, CRASH2, 108, 6)
    for lb in (4, 12):                                   # koperstoot-maten: snare-unisono met de stoten
        hit(kit, lb, 14, SNARE, 112)
    for q, t in ((12, TOM_HI), (13, TOM_MID), (14, TOM_LO), (15, TOM_LO)):
        hit(kit, 8, q, t, 112)
    for q in range(8, 16):                               # maat 16: snareroffel naar de yo-sectie
        hit(kit, 16, q, SNARE, 90 + q * 3, 1)
    # ---- B: halftime, atarigane op de achtsten
    for lb in range(17, 25):
        hit(kit, lb, 0, KICK, 120)
        hit(kit, lb, 10, KICK, 104)
        hit(kit, lb, 8, SNARE, 118)
        if lb % 2 == 1:
            hit(tk, lb, 0, ODAIKO, 116, 4)
        hit(tk, lb, 14, TAIKO_LO, 96)
        for q in range(2, 16, 4):
            hit(pc, lb, q, KANE, 66)
    hit(kit, 17, 0, CRASH, 116, 4)
    hit(kit, 21, 0, CRASH2, 108, 6)
    for q, t in ((8, TAIKO), (10, TAIKO), (12, TAIKO_LO), (13, TAIKO_LO), (14, ODAIKO)):
        hit(tk, 24, q, t, 112, 2)
    # ---- C: kumi-daiko
    KD = ['0:TAIKO:118 3:TAIKO_LO:96 4:TAIKO:110 8:TAIKO:118 10:TAIKO_LO:100 11:TAIKO_LO:96 12:TAIKO:112',
          '0:ODAIKO:122 4:TAIKO:108 6:TAIKO_LO:100 8:TAIKO:116 12:TAIKO:110 13:TAIKO_LO:100 14:TAIKO:112 15:TAIKO_LO:104']
    names = {'TAIKO': TAIKO, 'TAIKO_LO': TAIKO_LO, 'ODAIKO': ODAIKO}
    for lb in range(25, 33):
        for tok in KD[(lb - 25) % 2].split():
            q, n, v = tok.split(':')
            hit(tk, lb, int(q), names[n], int(v))
        for q in (4, 12):
            hit(pc, lb, q, HYOU, 92)
        hit(pc, lb, 14 if lb % 2 else 7, KOTSU, 96)
        if lb % 2 == 0:
            hit(pc, lb, 15, OHTSU, 104)
    hit(kit, 25, 0, CRASH, 112, 4)
    for lb in range(29, 33):                             # opbouw: kick vier op de vloer, snare 8sten -> 16en
        for q in (0, 4, 8, 12):
            hit(kit, lb, q, KICK, 116)
        step = 4 if lb == 29 else 2 if lb < 32 else 1
        for q in range(0, 16, step):
            hit(kit, lb, q, OSNARE if lb < 31 else SNARE, 70 + (lb - 29) * 12 + q, 1)
    hit(kit, 29, 0, CRASH2, 104, 6)
    # ---- D: climax
    for lb in range(33, 41):
        rock(lb, double=True)
        hit(tk, lb, 4, TAIKO, 108)
        hit(tk, lb, 12, TAIKO, 108)
    for lb in (33, 37):
        hit(kit, lb, 0, CRASH, 120, 4)
    hit(kit, 35, 0, CRASH2, 108, 6)
    hit(kit, 39, 0, CRASH2, 110, 6)
    for q, t in ((8, TOM_HI), (10, TOM_MID), (12, TOM_LO), (13, TOM_LO), (14, ODAIKO)):
        hit(kit if t != ODAIKO else tk, 40, q, t, 116)
    return {'kit': dedupe(kit), 'taiko': dedupe(tk), 'perc': dedupe(pc)}


# ---------------------------------------------------------------- sporen ----------------------------------------------
TRACKS = [   # (naam, programma, volume, pan)
    ('shaku', SHAKU, 110, 64), ('tpt', TPT, 100, 60), ('fue', FUE, 76, 70), ('horn', HORN, 96, 58),
    ('koto', KOTO, 84, 80), ('shami', SHAMI, 92, 46), ('gtr', GTR, 82, 54), ('bass', BASS, 96, 64),
    ('str', STR, 70, 72), ('choir', CHOIR, 70, 64), ('kit', DRUMS, 112, 64), ('taiko', DRUMS, 100, 64),
    ('perc', DRUMS, 84, 76), ('sq', SQ, 44, 84), ('hat', NOISE, 40, 64),
]
PSG = {'sq', 'hat'}
ORDER = ['shaku', 'tpt', 'horn', 'kit', 'taiko', 'bass', 'fue', 'gtr', 'koto', 'choir', 'shami', 'perc', 'horn2', 'str']
MERGE = {'horn': ['horn', 'horn2']}           # spoor -> partijen (de tegenstemmen hebben een lagere prioriteit)
# lengte van de drumsamples in ticks (bij 180 bpm, op de gespeelde toonhoogte; None = geloopt)
SAMPLE_TICKS = {KICK: 12, SNARE: 23, TAIKO: 60, TAIKO_LO: 90, ODAIKO: 90, TOM_HI: None, TOM_MID: None, TOM_LO: None,
                HYOU: 52, KANE: 59, KOTSU: 46, OHTSU: 68, CRASH: None, CRASH2: None, OSNARE: 23}

KIT = [   # vanaf noot 36; alles DirectSound (stock Emerald)
    ('voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 150', 150),
    ('voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 180', 180),
    ('voice_directsound 60, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 160', 160),
    ('voice_directsound 53, 58, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 160', 160),
    ('voice_directsound 60, 64, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 170', 170),
    ('voice_directsound 60, 44, DirectSoundWaveData_unused_sc55_tom, 255, 216, 77, 170', 170),
    ('voice_directsound 55, 64, DirectSoundWaveData_unused_sc55_tom, 255, 216, 77, 170', 170),
    ('voice_directsound 50, 84, DirectSoundWaveData_unused_sc55_tom, 255, 216, 77, 170', 170),
    ('voice_directsound 60, 40, DirectSoundWaveData_ethnic_flavours_hyoushigi, 255, 0, 255, 90', 90),
    ('voice_directsound 60, 88, DirectSoundWaveData_ethnic_flavours_atarigane, 255, 0, 255, 140', 140),
    ('voice_directsound 60, 48, DirectSoundWaveData_ethnic_flavours_kotsuzumi, 255, 0, 255, 110', 110),
    ('voice_directsound 60, 80, DirectSoundWaveData_ethnic_flavours_ohtsuzumi, 255, 0, 255, 110', 110),
    ('voice_directsound_no_resample 60, 54, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 200', 200),
    ('voice_directsound_no_resample 60, 76, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165', 165),
    ('voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 150', 150),
]
VOICES = {
    SHAKU: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_shakuhachi, 255, 0, 255, 165',
    FUE: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_whistle, 255, 0, 255, 150',
    KOTO: 'voice_directsound 60, 0, DirectSoundWaveData_unknown_koto_high, 255, 0, 206, 90',
    SHAMI: 'voice_directsound 60, 0, DirectSoundWaveData_unknown_koto_low, 255, 0, 206, 90',
    GTR: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_distortion_guitar_low, 255, 0, 255, 160',
    DRUMS: 'voice_keysplit_all voicegroup_hooh_drumset',
}


def write_voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Battle! Ho-Oh. Gegenereerd door tools/grounded/hooh_theme.py.'
    lines[1] = ('@ alleen stock-samples: 77 shakuhachi, 78 shinobue (whistle), 107 koto, 106 shamisen (koto laag), '
                '30 distortion-gitaar, 127 = drumkit hooh.')
    lines[2] = 'voice_group %s' % VG
    out = []
    for l in lines:
        if l.startswith('\t') and '@' in l:
            prog = int(l.rsplit('@', 1)[1])
            if prog in VOICES:
                l = '\t%s  @ %d' % (VOICES[prog], prog)
        out.append(l)
    open('sound/voicegroups/%s.inc' % VG, 'w').write('\n'.join(out))
    open('sound/voicegroups/drumsets/hooh.inc', 'w').write(
        '@ Project Grounded: drumkit voor Battle! Ho-Oh (hooh_theme.py), alleen stock-samples: 36 kick, 37 snare,\n'
        '@ 38/39 taiko (hoog/laag), 40 grote trom (odaiko), 41-43 toms, 44 hyoshigi, 45 atarigane, 46 kotsuzumi,\n'
        '@ 47 ohtsuzumi, 48/49 bekkens, 50 orkestsnare (roffels).\n'
        'voice_group hooh_drumset, 36\n' + ''.join('\t%s\n' % k for k, _ in KIT) + '\n')


def build(render_dir=None):
    write_voicegroup()
    rel = releases(VG)
    parts = {'shaku': shakuhachi(), 'tpt': trumpet(), 'fue': shinobue(), 'horn': horn(), 'horn2': horn2(), 'koto': koto(),
             'shami': shamisen(), 'gtr': guitar(), 'bass': bass(), 'str': strings(), 'choir': choir(),
             'sq': sparkle(), 'hat': hats()}
    parts.update(drums())
    progs = {k: pr for k, pr, _, _ in TRACKS}
    progs['horn2'] = HORN
    tail = {}
    for k, pr in progs.items():
        if k in PSG or pr == DRUMS:
            tail[k] = 0
            continue
        tail[k] = release_ticks(rel.get(pr, 200), TPB, BPM) + 2
    for k in ('shaku', 'tpt', 'fue', 'horn', 'horn2', 'gtr', 'bass', 'str', 'choir'):
        parts[k] = detach(parts[k], tail[k])
    for k in ('koto', 'shami'):
        parts[k] = tight(parts[k], tail[k])
    for k in parts:                                       # zelfde toonhoogte in één partij mag niet overlappen
        parts[k] = no_overlap(parts[k])
    # drums: een kanaal is bezet tot de sample afgelopen is of de release na de note-off uitgeklonken is
    proxy = {}
    for k in ('kit', 'taiko', 'perc'):
        proxy[k] = []
        for i, (s0, e0, n, v) in enumerate(parts[k]):
            r = release_ticks(KIT[n - 36][1], TPB, BPM) + 2
            occ = e0 - s0 + r if SAMPLE_TICKS[n] is None else min(SAMPLE_TICKS[n], e0 - s0 + r)
            proxy[k].append([s0, s0 + occ, n, v, i])
    alloc_in = {k: (proxy[k] if k in proxy else parts[k]) for k in ORDER}
    kept = allocate(alloc_in, ORDER, tail, max_voices=MAX_V)
    for k in proxy:
        idx = {e[4] for e in kept[k]}
        kept[k] = [e for i, e in enumerate(parts[k]) if i in idx]
    print('uitklinktijd (ticks):', tail)
    for k in ORDER:
        n = len(parts[k])
        gone = sorted({(e[0] // BAR) - INTRO + 1 for e in parts[k] if e not in kept[k]})
        print('  %-6s %4d noten, %3d vallen weg (%.1f%%)%s' % (k, n, n - len(kept[k]), 100 * (n - len(kept[k])) / max(n, 1),
                                                             ' (maten %s)' % gone[:14] if gone else ''))
        parts[k] = kept[k]
    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.tempo(at(1), BPM / 120)
    song.loop = (at(1), END * BAR)
    global SOUNDING
    SOUNDING = {k: [list(e) for e in v] for k, v in parts.items()}
    for ch, (k, prog, vol, pan) in enumerate(TRACKS):
        src = sorted(sum((parts[x] for x in MERGE.get(k, [k])), []))
        notes = [[s, e, n + OCT.get(prog, 0), v] for s, e, n, v in src]
        extra = shaku_bends(parts[k]) if k == 'shaku' else ()
        song.add(notes, prog, vol, ch, pan, extra=extra)
    song.save(OUT, END * BAR)
    print(OUT, 'intro %.2f s, loop %.1f s' % (INTRO * 4 * 60 / BPM, NLOOP * 4 * 60 / BPM))
    if render_dir:
        render_gm(render_dir)


# ---- offline-render (FluidR3 GM; andere klanken dan de GBA, wel noten/vorm/tempo) ------------------------------------
GM_PROG = {'shaku': 77, 'tpt': 56, 'fue': 72, 'horn': 60, 'koto': 107, 'shami': 106, 'gtr': 30, 'bass': 33,
           'str': 48, 'choir': 52, 'sq': 80, 'hat': 0}
GM_DRUM = {KICK: 36, SNARE: 38, TAIKO: 41, TAIKO_LO: 43, ODAIKO: 35, TOM_HI: 48, TOM_MID: 45, TOM_LO: 41,
           HYOU: 75, KANE: 80, KOTSU: 61, OHTSU: 60, CRASH: 49, CRASH2: 57, OSNARE: 40}


def gm_midi(path):
    m = mido.MidiFile(OUT)
    gm = mido.MidiFile(type=1, ticks_per_beat=m.ticks_per_beat)
    gm.tracks.append(m.tracks[0])
    free = [c for c in range(16) if c != 9]
    for i, (k, prog, vol, pan) in enumerate(TRACKS):
        drum = prog == DRUMS or k == 'hat'
        ch = 9 if drum else free.pop(0)
        off = OCT.get(prog, 0)
        t = mido.MidiTrack()
        for x in m.tracks[i + 1]:
            if x.type == 'program_change':
                x = x.copy(channel=ch, program=0 if drum else GM_PROG[k])
            elif x.type in ('note_on', 'note_off'):
                if k == 'hat':
                    x = x.copy(channel=ch, note=42)
                elif drum:
                    x = x.copy(channel=ch, note=GM_DRUM.get(x.note, 47))
                else:
                    x = x.copy(channel=ch, note=x.note - off)
            elif hasattr(x, 'channel'):
                x = x.copy(channel=ch)
            t.append(x)
        gm.tracks.append(t)
    gm.save(path)


def render_gm(outdir):
    os.makedirs(outdir, exist_ok=True)
    mid = os.path.join(outdir, 'hooh_gm.mid')
    gm_midi(mid)
    wav = os.path.join(outdir, 'hooh_fluidr3.wav')
    subprocess.run(['fluidsynth', '-ni', '-g', '0.5', '-r', '44100', '-F', wav, '/usr/share/sounds/sf2/FluidR3_GM.sf2',
                    mid], check=True, capture_output=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-t', '62', '-af',
                    'loudnorm=I=-16:TP=-1.5,afade=t=out:st=60:d=2', '-b:a', '160k', wav[:-4] + '.mp3'], check=True)
    os.remove(wav)
    print('render:', wav[:-4] + '.mp3')


if __name__ == '__main__':
    build(sys.argv[sys.argv.index('--render') + 1] if '--render' in sys.argv else None)
