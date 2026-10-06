#!/usr/bin/env python3
"""Project Grounded: "Battle! Ho-Oh" (song 658, MUS_GROUNDED_VS_HO_OH), eigen compositie, v2.

Jordi (brief): "Ho-Oh heeft een vurig theme, tegelijkertijd met Japanse instrumentatie, heel tof, lekker hoog tempo".
Jordi over v1: "te vrolijk, het mag epischer, vuriger, meer Japanse instrumenten; nu voeren trompetten/fluiten de
boventoon en die zijn schel. Nog niet Japans genoeg."
-> v2: 180 bpm, E-klein. Melodie in de hirajoshi-toonladder (E F# G B C: kleine terts + kleine sext = donker), harmonie
   i-bVI-bVII (Em C D), het vuur-deel in de in-toonladder (E F A B C, frygisch E-F), climax een hele toon hoger
   (F#m-D-E) en via F -> E (frygische cadens) terug. Geen trompet, geen whistle/shinobue, geen fonkel-arpeggio's
   (de yo-'regenboog' van v1 is weg). Leads = shakuhachi (midden-/laag register, met meri-buigingen, yuri-vibrato
   en kari-vallen aan het eind van een frase), koto (heterofonie met tremolo, glissandi) en tsugaru-shamisen
   (drijvende 16en-riffs, solo in het vuur-deel). Daaronder taiko-ensemble (odaiko, nagado, shime, ka, kiai-roepen),
   sho-clusters, laag koper (hoorn C3-B3), en zacht de rock-motor (distortion, bas, kick/snare).

Vorm (maat = 1,333 s):
  intro i1-i4 (5,3 s)  odaiko + kiai, sho zwelt aan, shakuhachi-muraiki met een grote buiging; koto-glissando omlaag,
                        nagado versnelt (cry ±2,3-3 s: geen drop daar); shime-roffel + shamisen-tremolo; i4 = unisono-
                        run van koto/shamisen/bas/gitaar + taiko-fill + kiai
  [loop]
  A    1-8   thema op de shakuhachi (Em C D Em | Em C Am B), shamisen-riff in 16en, koto gebroken akkoorden,
             taiko + kick/snare, distortion-chugs zacht eronder
  A'   9-16  koto speelt het thema mee (heterofonie, tremolo op lange noten), tweede helft klimt hoger; dubbele kick,
             shime in 16en
  B   17-24  episch: C D Em Em | C D B B (bVI-bVII-i), halftime; shakuhachi-roep met lange buigingen, laag koper,
             sho, koto-glissandi op elke akkoordwissel, biwa-achtige lage shamisenslagen, koor laag in 21-24
  C   25-32  heilig vuur: kumi-daiko (odaiko, nagado, shime-16en, ka, kiai) + tsugaru-shamisensolo in de in-toonladder
             (E-F frygisch); 29-32 opbouw (shakuhachi stijgt, koto-tremolo, gitaar terug), maat 32 D | E -> unisono-run
  D   33-40  climax: thema +2 (F#m D E F#m | F#m D Bm C#) op shakuhachi + koto, alles vol; maat 40 F -> E terug naar 1
  ]
Instrumenten: eigen samples (tools/grounded/hooh_samples.py, voorvoegsel hooh_*): 77 shakuhachi (keysplit hooh_shaku),
107 koto (hooh_koto), 106 shamisen (hooh_shami), 109 sho, drumkit drumsets/hooh.inc (odaiko, nagado, shime, ka, kiai);
stock: 30 distortion-gitaar laag, 33 fingered bass, 60 hoorn, 52 koor, kick/snare/crash/hyoshigi/kotsuzumi/ohtsuzumi/
toms in de kit, 120 PSG-ruis (hihat).
Noten staan hieronder op klinkende toonhoogte; OCT zet ze om naar de toets voor de GBA-sample.
Gebruik: python3 tools/grounded/hooh_theme.py [--render <map>]"""
import math, os, subprocess, sys
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

SHAKU, KOTO, SHAMI, SHO, GTR, BASS, HORN, CHOIR, NOISE, DRUMS = 77, 107, 106, 109, 30, 33, 60, 52, 120, 127
OCT = {GTR: 12}                              # distortion_guitar_low klinkt C3 op toets 60 (v1 gemeten)
(KICK, SNARE, ODAIKO, NAGADO, NAGADO_LO, SHIME, KA, KIAI, HYOU, KOTSU, OHTSU, CRASH, TOM_HI, TOM_LO,
 SNARE_R) = range(36, 51)

N = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8,
     'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def p(name):
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


def at(lb, q=0):
    """tick van 16e q in loopmaat lb (1 = loopbegin); lb <= 0 = intro (i1 = -3 ... i4 = 0)."""
    return (INTRO + lb - 1) * BAR + int(q * S16)


def seq(out, lb, s, vel=100, shift=0):
    """'q:len:NOOT[:vel] ...' in maat lb (q en len in 16en, mag fractioneel)."""
    for tok in s.split():
        f = tok.split(':')
        q, ln, nt = float(f[0]), float(f[1]), f[2]
        v = int(f[3]) if len(f) > 3 else vel
        st = at(lb, q)
        out.append([st, st + int(ln * S16), p(nt) + shift, v])


def run16(out, lb, notes, q0=0, step=1, vel=96, acc=(), accv=14, shift=0):
    """reeks noten (spaties) in stappen van `step` 16en vanaf q0; accenten op de 16en in acc."""
    for i, n in enumerate(notes.split()):
        if n == '.':
            continue
        q = q0 + i * step
        out.append([at(lb, q), at(lb, q) + int(step * S16), p(n) + shift, vel + (accv if (q % 16) in acc else 0)])


# ------------------------------------------------------------------------------- materiaal ------------------------
CH_A = ['Em', 'C', 'D', 'Em', 'Em', 'C', 'Am', 'B']
CH_B = ['C', 'D', 'Em', 'Em', 'C', 'D', 'B', 'B']
CH_D = ['F#m', 'D', 'E', 'F#m', 'F#m', 'D', 'Bm', 'C#']      # climax = A + 2
ROOT = {'Em': 'E', 'C': 'C', 'D': 'D', 'Am': 'A', 'B': 'B', 'F#m': 'F#', 'E': 'E', 'Bm': 'B', 'C#': 'C#', 'F': 'F'}

# hoofdthema (hirajoshi op E: E F# G B C, A/D als doorgang). Shakuhachi-register E4-G5 (geen schelle top).
THEME = [
    '0:6:E4 6:2:F#4 8:4:G4 12:4:B4',
    '0:10:C5 10:2:B4 12:2:G4 14:2:B4',
    '0:6:A4 6:2:B4 8:8:F#4',
    '0:12:E4 12:2:F#4 14:2:G4',
    '0:6:B4 6:2:C5 8:4:E5 12:2:F#5 14:2:G5',
    '0:8:G5 8:2:F#5 10:2:E5 12:4:C5',
    '0:6:E5 6:2:C5 8:4:B4 12:2:A4 14:2:C5',
    '0:12:B4 12:2:C5 14:2:A4',
]
THEME2_END = [   # A' maat 13-16: klimt hoger, eindigt open op B (koto-glissando + fill naar B)
    '0:6:B4 6:2:C5 8:4:E5 12:2:F#5 14:2:G5',
    '0:6:G5 6:2:A5 8:8:B5',
    '0:6:A5 6:2:G5 8:4:E5 12:4:C5',
    '0:10:B4',
]
CLIMAX_END = '0:4:F5 4:4:E5 8:2:C5 10:2:B4 12:2:A4 14:2:F4'       # maat 40 (in E): F -> E terug naar maat 1
# shakuhachi-expressie per (themamaat, 16e): meri = buiging omhoog naar de noot, kari = val aan het eind van de noot
MERI = {(1, 0), (2, 0), (4, 0), (6, 0), (8, 0)}
KARI = {(4, 0), (8, 0)}

# B: de roep (episch, lange noten)
CALL = [
    '0:4:G4 4:12:C5',
    '0:4:B4 4:4:A4 8:8:F#4',
    '0:12:G4 12:2:F#4 14:2:G4',
    '0:4:B4 4:12:E5',
    '0:4:E5 4:8:G5 12:2:F#5 14:2:E5',
    '0:8:F#5 8:4:A5 12:4:G5',
    '0:12:F#5 12:2:E5 14:2:C5',
    '0:14:B4',
]
CALL_MERI = {(17, 4), (20, 4), (21, 4), (23, 0), (24, 0)}
CALL_KARI = {(19, 0), (24, 0)}

# shamisen-riffcellen (16en; drijvend, accenten 3+3+2), op klinkende hoogte
SHAMI_CELL = {
    'Em': 'E3 E3 B3 E3 G3 E3 F#3 E3 B3 E3 C4 B3 G3 E3 F#3 G3',
    'C':  'C3 C3 G3 C3 E3 C3 G3 E3 C4 G3 B3 G3 E3 C3 E3 G3',
    'D':  'D3 D3 A3 D3 F#3 D3 A3 F#3 D4 A3 B3 A3 F#3 D3 E3 F#3',
    'Am': 'A3 A3 E4 A3 C4 A3 E4 C4 B3 A3 G3 A3 C4 A3 E4 C4',
    'B':  'B3 B3 F#4 B3 E4 B3 F#4 B3 C4 B3 A3 B3 F#3 G3 F#3 E3',
}
ACC = (0, 3, 6, 8, 11, 14)
# koto: gebroken akkoorden in achtsten (A), op klinkende hoogte
KOTO_BROKEN = {
    'Em': 'E4 B4 E5 B4 G4 B4 F#5 B4', 'C': 'C4 G4 C5 G4 E4 G4 B4 G4', 'D': 'D4 A4 D5 A4 F#4 A4 E5 A4',
    'Am': 'A3 E4 A4 E4 C4 E4 B4 E4', 'B': 'B3 F#4 B4 F#4 E4 F#4 C5 F#4',
}
GLISS_UP = {   # koto-glissando omhoog (32en) naar de akkoordtoon, per akkoord
    'C': 'C4 D4 E4 G4 B4 C5 E5 G5', 'D': 'D4 E4 F#4 A4 B4 D5 F#5 A5', 'Em': 'E4 F#4 G4 B4 C5 E5 F#5 G5',
    'B': 'B3 C4 E4 F#4 B4 C5 E5 F#5', 'Am': 'A3 B3 C4 E4 G4 A4 C5 E5',
}
# vuur-deel: tsugaru-shamisensolo in de in-toonladder (E F A B C)
SOLO = [
    'E4 E4 F4 E4 B3 E4 C4 B3 E4 E4 F4 E4 A4 F4 E4 C4',
    'B3 B3 C4 B3 A3 B3 F3 A3 B3 C4 E4 F4 A4 B4 C5 B4',
    'C5 B4 A4 F4 E4 F4 A4 B4 C5 E5 C5 B4 A4 F4 E4 C4',
    'B3 E4 B3 E4 F4 E4 C4 B3 A3 B3 C4 E4 F4 E4 B3 E3',
]
CH_C = ['Em', 'Em', 'F', 'Em', 'Em', 'F', 'Em', 'F']      # 25-32 (32 wordt D | E)
SHAMI_CELL['F'] = 'F3 F3 C4 F3 A3 F3 C4 A3 E4 C4 B3 A3 F3 E3 F3 A3'
SHAMI_CELL['E5'] = 'E3 E3 B3 E3 F3 E3 B3 E3 C4 B3 A3 B3 F3 E3 F3 B3'      # E in de in-toonladder (vuur)
SHO_ROOT = {'Em': 'E4', 'C': 'C4', 'D': 'D4', 'Am': 'A4', 'B': 'E4', 'F#m': 'F#4', 'E': 'E4', 'Bm': 'B3',
            'C#': 'F#4', 'F': 'F4', 'Ein': 'A4'}


def name_of(m):
    o, pc = m // 12 - 1, m % 12
    return ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][pc] + str(o)


def shift_str(s, k):
    return ' '.join(n if n == '.' else name_of(p(n) + k) for n in s.split())


CLIMAX_MAP = {'F#m': ('Em', 2), 'D': ('C', 2), 'E': ('D', 2), 'Bm': ('Am', 2), 'C#': ('B', 2)}


# ------------------------------------------------------------------------------- partijen -------------------------
def theme(out, first, shift=0, ends=None, vel=104):
    for i, s in enumerate(THEME):
        if ends and i >= 8 - len(ends):
            s = ends[i - (8 - len(ends))]
        seq(out, first + i, s, vel, shift)


SHAKU_EXPR = {'meri': set(), 'kari': set()}


def shakuhachi():
    out = []
    seq(out, -3, '2:14:E4:92')                            # intro: muraiki, grote buiging (zie bends)
    seq(out, -2, '0:6:F4:96 6:2:E4:90 8:8:B3:88')
    seq(out, -1, '0:16:B4:100')
    seq(out, 0, '0:8:E5:110 8:6:B4:104')
    theme(out, 1)
    # A': de shakuhachi speelt heterofoon mee in maat 9-12, tweede helft klimt
    theme(out, 9, 0, THEME2_END, 108)
    for i, s in enumerate(CALL):
        seq(out, 17 + i, s, 112)
    # C: 25-28 zwijgt (taiko + shamisensolo); 29-32 stijgende roep in de in-toonladder
    seq(out, 27, '8:8:B4:96')
    seq(out, 28, '0:12:C5:100 12:4:B4:96')
    seq(out, 29, '0:12:B4:100 12:4:C5:104')
    seq(out, 30, '0:12:E5:106 12:4:F5:108')
    seq(out, 31, '0:12:E5:110 12:2:F5:110 14:2:A5:112')
    seq(out, 32, '0:8:B5:116')
    theme(out, 33, 2, [CLIMAX_END], 116)
    # climax maat 40 staat in E (geen +2): corrigeer
    for e in out:
        if at(40) <= e[0] < at(41):
            e[2] -= 2
    for lb, q in MERI:
        SHAKU_EXPR['meri'] |= {at(lb, q), at(lb + 8, q) if lb < 5 else -1, at(lb + 32, q)}
    for lb, q in KARI:
        SHAKU_EXPR['kari'] |= {at(lb, q), at(lb + 32, q)}
    SHAKU_EXPR['meri'] |= {at(lb, q) for lb, q in CALL_MERI} | {at(-3, 2), at(-1, 0), at(29, 0), at(30, 0), at(31, 0)}
    SHAKU_EXPR['kari'] |= {at(lb, q) for lb, q in CALL_KARI} | {at(-2, 8), at(0, 8), at(32, 0)}
    return dedupe(out)


def shaku_bends(notes):
    """meri: begin een halve toon (intro: hele toon) te laag en buig in 1-2 16en omhoog; yuri: vibrato op lange noten
    (vanaf 40% van de noot, ±30 cent, ±5 Hz); kari: val van een hele toon in de laatste 16e. BENDR 2: 4096 = 1 halve
    toon. De buiging wordt bij de volgende aanslag teruggezet (niet bij de note-off)."""
    ev = [(0, mido.Message('control_change', control=20, value=2)), (0, mido.Message('pitchwheel', pitch=0))]
    notes = sorted(notes)
    for i, (s, e, n, v) in enumerate(notes):
        ln = e - s
        big = s == at(-3, 2)
        if s in SHAKU_EXPR['meri']:
            depth = 8191 if big else 4096
            steps = 8 if big else 5
            dur = 24 if big else 14
            for k in range(steps + 1):
                ev.append((s + k * dur // steps, mido.Message('pitchwheel', pitch=max(-8192, int(-depth * (1 - k / steps) ** 1.5)))))
        else:
            ev.append((s, mido.Message('pitchwheel', pitch=0)))
        if ln >= 7 * S16 // 1 and ln >= 72:
            t = s + max(int(ln * 0.4), 24)
            k = 0
            while t < e - (S16 if s in SHAKU_EXPR['kari'] else 3):
                depth = min(1, k / 8) * 1300
                ev.append((t, mido.Message('pitchwheel', pitch=int(depth * math.sin(2 * math.pi * k * 3 / 27)))))
                t += 3; k += 1
        if s in SHAKU_EXPR['kari']:
            for k in range(1, 5):
                ev.append((e - S16 + k * 3, mido.Message('pitchwheel', pitch=-2048 * k)))
    # elke tick maar één waarde: de laatste wint
    last = {}
    for t, m in ev:
        if m.type == 'pitchwheel':
            last[t] = m
    return [ev[0]] + sorted(last.items(), key=lambda x: x[0])


def koto():
    out, gl = [], []
    # intro i2: glissando omlaag door de in-toonladder (32en), dan tremolo op E4/B4
    down = 'E6 C6 B5 A5 F5 E5 C5 B4 A4 F4 E4 C4 B3 A3 F3 E3'.split()
    for i, n in enumerate(down):
        gl.append([at(-2, i * 0.5), at(-2, i * 0.5) + 6, p(n), 100 - i * 2])
    for q in range(8, 16):
        seq(out, -2, '%d:1:%s:%d' % (q, 'E4' if q % 2 == 0 else 'B4', 64 + q * 2))
    for q in range(16):
        seq(out, -1, '%d:1:%s:%d' % (q, 'E4' if q % 2 == 0 else 'B4', 70 + q * 2))
    run16(out, 0, 'E5 C5 B4 G4 F#4 E4 C4 B3', vel=108)
    seq(out, 0, '8:2:B3:116')
    # A: gebroken akkoorden in achtsten + glissando op maat 1 en 5
    for i, ch in enumerate(CH_A):
        run16(out, 1 + i, KOTO_BROKEN[ch], step=2, vel=74, acc=(0,), accv=12)
    # A' (9-16): heterofonie: het thema mee, met tremolo (herhaalde 16en) op noten van 4+ zestienden
    tmp = []
    theme(tmp, 9, 0, THEME2_END, 92)
    for s, e, n, v in tmp:
        if e - s >= 4 * S16:
            t = s
            k = 0
            while t < e:
                out.append([t, t + S16, n, v if k == 0 else 72 + (k % 2) * 6])
                t += S16; k += 1
        else:
            out.append([s, e, n, v])
    for i, n in enumerate('B3 C4 E4 F#4 B4 C5 E5 F#5 B5 C6 E6'.split()):     # maat 16: glissando omhoog
        gl.append([at(16, 10 + i * 0.5), at(16, 10 + i * 0.5) + 6, p(n), 84 + i * 3])
    # B: glissando omhoog op elke akkoordwissel, dan tremolo op de akkoordtoon
    for i, ch in enumerate(CH_B):
        g = GLISS_UP[ch].split()
        for j, n in enumerate(g):
            gl.append([at(17 + i, j * 0.5), at(17 + i, j * 0.5) + 6, p(n), 82 + j * 3])
        top = p(g[-1]) - 12
        for q in range(8, 16, 1):
            out.append([at(17 + i, q), at(17 + i, q) + S16, top if q % 2 == 0 else top - 5, 66 + (q % 4 == 0) * 8])
    # C: 25-28 stil (ruimte voor de shamisen), 29-32 tremolo stijgend door de in-toonladder
    for k, n in enumerate('E4 F4 A4 B4 C5 E5 F5 A5'.split()):
        lb, h = 29 + k // 2, (k % 2) * 8
        for q in range(8):
            out.append([at(lb, h + q), at(lb, h + q) + S16, p(n) if q % 2 == 0 else p(n) - 12 + 12 * (q % 4 == 1),
                        70 + k * 4 + (q == 0) * 10])
    run16(out, 32, 'D5 C#5 A4 G#4 E5 C#5 B4 G#4', q0=8, vel=110)
    # D: thema +2 heterofoon (tremolo), glissando omhoog op maat 33 en 37
    tmp = []
    theme(tmp, 33, 2, [CLIMAX_END], 100)
    for s, e, n, v in tmp:
        if at(40) <= s:
            n -= 2
        if e - s >= 4 * S16:
            t, k = s, 0
            while t < e:
                out.append([t, t + S16, n, v if k == 0 else 76 + (k % 2) * 6])
                t += S16; k += 1
        else:
            out.append([s, e, n, v])
    for lb, ch in ((33, 'Em'), (37, 'Em')):
        g = [p(x) + 2 for x in GLISS_UP[ch].split()]
        for j, n in enumerate(g[:6]):
            gl.append([at(lb - 1, 13 + j * 0.5), at(lb - 1, 13 + j * 0.5) + 6, n - 12, 80 + j * 4])
    return dedupe(out), dedupe(gl)


def shamisen():
    out = []
    # intro: tsugaru-tremolo op E3 (16en, crescendo) in i3, unisono-run in i4
    for q in range(16):
        seq(out, -1, '%d:1:E3:%d' % (q, 70 + q * 3))
    run16(out, 0, 'E4 C4 B3 G3 F#3 E3 C3 B2', vel=110)
    seq(out, 0, '8:2:B2:118')

    def cell(lb, ch, shift=0, vel=92):
        run16(out, lb, SHAMI_CELL[ch], vel=vel, acc=ACC, accv=16, shift=shift)
    for i, ch in enumerate(CH_A):
        cell(1 + i, ch)
    for i, ch in enumerate(CH_A[:7]):
        cell(9 + i, ch, vel=96)
    run16(out, 16, 'B3 B3 F#4 B3 E4 B3 F#4 B3 C4', vel=98, acc=ACC, accv=16)
    # B: biwa-achtige lage slagen (halftime): grondtoon + kwint op 0, 3, 6 en 8, kort tremolo op 12-15
    for i, ch in enumerate(CH_B):
        r = p(ROOT[ch] + '3')
        if r > p('D3'):
            r -= 12
        r = max(r, p('B2'))
        lb = 17 + i
        for q, n, v in ((0, r, 112), (3, r + 7, 96), (6, r, 100), (8, r + 7, 104), (12, r + 12, 90), (13, r + 12, 84),
                        (14, r + 12, 88), (15, r + 7, 92)):
            out.append([at(lb, q), at(lb, q) + S16, n, v])
    # C: tsugaru-solo 25-28, riff E/F (frygisch) 29-31, maat 32 D | E + unisono-run
    for i, s in enumerate(SOLO):
        run16(out, 25 + i, s, vel=100, acc=ACC, accv=18)
    for lb, ch in ((29, 'E5'), (30, 'F'), (31, 'E5')):
        cell(lb, ch, vel=98)
    run16(out, 32, 'D3 D3 A3 D3 E3 E3 B3 E3', vel=104, acc=(0, 4), accv=14)
    run16(out, 32, 'D4 C#4 A3 G#3 E4 C#4 B3 G#3', q0=8, vel=112)
    # D: riff +2
    for i, ch in enumerate(CH_D[:7]):
        src, k = CLIMAX_MAP.get(ch, (ch, 0))
        cell(33 + i, src if src in SHAMI_CELL else 'Em', shift=k, vel=100)
    cell(40, 'F', vel=102)
    out = [e for e in out if not (at(40, 8) <= e[0] < at(41))]
    run16(out, 40, 'E3 E3 B3 E3 C4 B3 F3 E3', q0=8, vel=104, acc=(8, 11, 14), accv=16)
    return dedupe(out)


def guitar():
    out = []

    def power(lb, root, pat, vel=100):
        for q, ln in pat:
            st = at(lb, q)
            out.append([st, st + ln * S16 - 2, p(root), vel if q % 4 == 0 else vel - 14])
    CHUG = [(0, 2), (3, 1), (4, 2), (6, 2), (8, 2), (11, 1), (12, 2), (14, 2)]
    GR = {'Em': 'E2', 'C': 'C3', 'D': 'D3', 'Am': 'A2', 'B': 'B2', 'F#m': 'F#2', 'E': 'E3', 'Bm': 'B2', 'C#': 'C#3',
          'F': 'F2'}
    out.append([at(-1), at(0) - 4, p('E2'), 80])                       # intro: aanzwellende E
    power(0, 'E2', [(8, 2)], 112)
    for i, ch in enumerate(CH_A[:7]):
        power(9 + i, GR[ch], CHUG, 100)
    power(16, 'B2', [(0, 2), (3, 1), (4, 2), (6, 2), (8, 2)], 100)
    for lb, ch in ((23, 'B'), (24, 'B')):                               # B: alleen de laatste twee maten (opbouw)
        power(lb, GR[ch], [(0, 6), (6, 2), (8, 8)], 92)
    power(32, 'D3', [(0, 7)], 104)
    power(32, 'E3', [(8, 7)], 110)
    for i, ch in enumerate(CH_D):
        power(33 + i, GR[ch], CHUG, 104)
    out[:] = [e for e in out if not (at(40) <= e[0] < at(41))]
    power(40, 'F2', [(0, 3), (3, 3), (6, 2)], 106)
    power(40, 'E2', [(8, 7)], 110)
    return dedupe(out)


def bass():
    out = []
    seq(out, -1, '0:16:E2:96')
    seq(out, 0, '0:2:E2:110 2:2:C2 4:2:B1 6:2:G1 8:2:B1:116')

    def eighths(lb, ch, vel=104, half=None):
        r = p(ROOT[ch] + '2')
        for q in range(0, 16, 2):
            n = r + 12 if q in (6, 14) else r
            out.append([at(lb, q), at(lb, q) + 2 * S16 - 3, n, vel])
    for i, ch in enumerate(CH_A):
        eighths(1 + i, ch)
    for i, ch in enumerate(CH_A[:7]):
        eighths(9 + i, ch)
    seq(out, 16, '0:2:B1 2:2:B1 4:2:B1 6:2:B2 8:2:B1')
    for i, ch in enumerate(CH_B):                      # B: lang, op de grondtoon
        r = p(ROOT[ch] + '2')
        lb = 17 + i
        out.append([at(lb), at(lb, 6) - 3, r, 110])
        out.append([at(lb, 6), at(lb, 8) - 3, r + 12, 96])
        out.append([at(lb, 8), at(lb, 16) - 3, r, 104])
    for lb in range(25, 29):                           # C: E1-pedaal op de odaiko-slagen
        seq(out, lb, '0:6:E1:110 10:4:E1:100')
    for lb, ch in ((29, 'Em'), (30, 'F'), (31, 'Em')):
        eighths(lb, ch)
    seq(out, 32, '0:2:D2 2:2:D2 4:2:D2 6:2:D2 8:2:E2 10:2:E2 12:2:E2 14:2:E2')
    for i, ch in enumerate(CH_D):
        eighths(33 + i, ch, 108)
    out[:] = [e for e in out if not (at(40) <= e[0] < at(41))]
    seq(out, 40, '0:2:F1 2:2:F1 4:2:F1 6:2:F2 8:2:E1 10:2:E1 12:2:E1 14:2:E2', 110)
    return dedupe(out)


def horn():
    """laag koper (hoorn C3-B3) als gewicht in B, de opbouw en de climax; in stukken van 2 tellen."""
    out = []

    def low(ch):
        r = p(ROOT[ch] + '3')
        return r if r <= p('B3') else r - 12
    for i, ch in enumerate(CH_B):
        n = low(ch)
        seq(out, 17 + i, '0:8:%s:%d 8:8:%s:%d' % (name_of(n), 96, name_of(n), 88))
    for k, n in enumerate(['E3', 'F3', 'E3', 'F3', 'E3', 'F3']):
        seq(out, 29 + k // 2, '%d:8:%s:%d' % ((k % 2) * 8, n, 84 + k * 4))
    seq(out, 32, '0:8:D3:108 8:8:E3:112')
    seq(out, 40, '0:8:F3:100 8:8:E3:104')
    return dedupe(out)


def sho():
    """sho-cluster (A4 B4 E5 A5 B5 -> grondtoon-secunde-kwint): lange zwellende akkoorden, 2 tellen per stuk."""
    out = []
    root = lambda ch: p(SHO_ROOT[ch])
    out.append([at(-3), at(-3, 8), root('Em'), 70])
    out.append([at(-3, 8), at(-2), root('Em'), 78])
    out.append([at(-2), at(-2, 8), root('Em'), 84])
    for i, ch in enumerate(CH_B):
        out.append([at(17 + i), at(17 + i, 8), root(ch), 80])
        out.append([at(17 + i, 8), at(18 + i), root(ch), 76])
    for i, ch in enumerate(CH_C):
        c = 'Ein' if ch == 'Em' else ch
        out.append([at(25 + i), at(25 + i, 8), root(c), 74])
        out.append([at(25 + i, 8), at(26 + i), root(c), 70])
    for i, ch in enumerate(CH_D):
        c = 'F' if i == 7 else ch
        out.append([at(33 + i), at(33 + i, 8), root(c), 76])
        out.append([at(33 + i, 8), at(34 + i), root('Em' if i == 7 else c), 72])
    return dedupe(out)


def choir():
    out = []
    for i, ch in enumerate(CH_B[4:]):                 # B tweede helft: lage 'aah' op de grondtoon
        n = p(ROOT[ch] + '3')
        n = n if n <= p('B3') else n - 12
        seq(out, 21 + i, '0:8:%s:76 8:8:%s:72' % (name_of(n + 12 if n < p('E3') else n), name_of(n + 12 if n < p('E3') else n)))
    for i, ch in enumerate(CH_D):
        n = p(ROOT[ch] + '3')
        n = n if n <= p('B3') else n - 12
        n = n + 12 if n < p('E3') else n
        seq(out, 33 + i, '0:8:%s:76 8:8:%s:72' % (name_of(n), name_of(n)))
    return dedupe(out)


def hats():
    """PSG-ruis: zachte hihat in achtsten (A, B-tweede helft), zestienden in A', de opbouw en de climax."""
    out = []
    for lb in range(1, 41):
        if 25 <= lb <= 28 or 17 <= lb <= 20:
            continue
        step = 1 if (9 <= lb <= 16 or lb >= 29) else 2
        for q in range(0, 16, step):
            v = 64 if q % 4 == 2 else (48 if q % 2 == 0 else 34)
            out.append([at(lb, q), at(lb, q) + 4, 80, v])
    return dedupe(out)


def drums():
    kit, oda, tai, pc = [], [], [], []

    def hit(lst, lb, q, note, vel, ln=2):
        lst.append([at(lb, q), at(lb, q) + int(ln * S16), note, vel])

    # ---- intro
    hit(oda, -3, 0, ODAIKO, 127)
    hit(pc, -3, 0, KIAI, 118)
    hit(kit, -3, 0, CRASH, 96, 8)
    for q in (0, 6, 10, 13, 15):
        hit(tai, -2, q, NAGADO if q % 2 == 0 else NAGADO_LO, 92 + q)
    hit(pc, -2, 0, HYOU, 100)
    hit(pc, -2, 8, HYOU, 104)
    hit(oda, -1, 10, ODAIKO, 118)                       # niet op i3-tel 1 (2,67 s): daar klinkt de cry
    for q in range(16):
        hit(pc, -1, q, SHIME, 64 + q * 3, 1)
    hit(pc, -1, 14, OHTSU, 116)
    hit(oda, 0, 0, ODAIKO, 124)
    hit(kit, 0, 0, CRASH, 110, 8)
    hit(kit, 0, 0, KICK, 124)
    hit(kit, 0, 8, KICK, 124)
    for q, n in ((10, NAGADO), (11, NAGADO), (12, NAGADO_LO), (13, NAGADO_LO), (14, NAGADO)):
        hit(tai, 0, q, n, 110 + (q - 10) * 3)
    hit(pc, 0, 12, KIAI, 120)
    hit(oda, 0, 15, ODAIKO, 112)

    def groove(lb, double=False):
        """A/D: taiko-groove (nagado don-don-doko) + zachte rockkit."""
        for q in ((0, 8) if not double else (0, 3, 6, 8, 10, 14)):
            hit(kit, lb, q, KICK, 112 if q % 8 == 0 else 98)
        for q in (4, 12):
            hit(kit, lb, q, SNARE, 104)
        for q, n, v in ((0, NAGADO, 116), (3, NAGADO_LO, 98), (6, NAGADO, 104), (8, NAGADO, 112), (11, NAGADO_LO, 98),
                        (13, NAGADO_LO, 94), (14, NAGADO, 104)):
            hit(tai, lb, q, n, v)
        for q in (4, 12):
            hit(pc, lb, q, KA, 84)

    for lb in range(1, 17):
        groove(lb, double=lb >= 9)
        if lb % 2 == 1:
            hit(oda, lb, 0, ODAIKO, 118)
        if lb >= 9:
            for q in (1, 2, 5, 7, 9, 10, 13, 15):
                hit(pc, lb, q, SHIME, 62 + (q % 2) * 6, 1)
    for lb in (1, 9):
        hit(kit, lb, 0, CRASH, 100, 8)
    hit(pc, 9, 0, KIAI, 116)
    for lb in (4, 12):                                  # einde frase: kotsuzumi 'pon' + ohtsuzumi 'ka'
        hit(pc, lb, 12, KOTSU, 100)
        hit(pc, lb, 14, OHTSU, 110)
    for q, n in ((8, NAGADO), (10, NAGADO), (12, NAGADO_LO), (13, NAGADO_LO), (14, NAGADO), (15, NAGADO)):
        hit(tai, 8, q, n, 112)
    for q in range(10, 16):                             # maat 16: roffel naar B
        hit(tai, 16, q, NAGADO if q % 2 == 0 else NAGADO_LO, 100 + q * 2)
    hit(pc, 16, 14, KIAI, 118)
    # ---- B: halftime, odaiko op elke maat
    for lb in range(17, 25):
        hit(oda, lb, 0, ODAIKO, 124)
        hit(kit, lb, 0, KICK, 116)
        hit(kit, lb, 8, SNARE, 112)
        hit(tai, lb, 6, NAGADO_LO, 96)
        hit(tai, lb, 10, NAGADO, 100)
        hit(tai, lb, 14, NAGADO_LO, 96)
        hit(pc, lb, 4, KA, 80)
        hit(pc, lb, 12, KA, 80)
        if lb % 2 == 0:
            hit(pc, lb, 14, KOTSU, 96)
    hit(kit, 17, 0, CRASH, 104, 8)
    for q, n in ((8, NAGADO), (10, NAGADO), (11, NAGADO), (12, NAGADO_LO), (13, NAGADO_LO), (14, NAGADO), (15, NAGADO)):
        hit(tai, 24, q, n, 108 + q)
    hit(oda, 24, 14, ODAIKO, 120)
    # ---- C: kumi-daiko
    KD = [   # (16e, noot, vel) per maat, 2-maats patroon (don-don doko don, ka op de rusten)
        [(0, ODAIKO, 124), (3, NAGADO, 104), (4, NAGADO, 110), (7, NAGADO_LO, 96), (8, NAGADO, 116),
         (10, ODAIKO, 118), (12, NAGADO, 108), (13, NAGADO_LO, 100), (14, NAGADO, 112)],
        [(0, ODAIKO, 124), (2, NAGADO, 106), (4, NAGADO, 112), (6, NAGADO_LO, 100), (8, ODAIKO, 120),
         (11, NAGADO, 104), (12, NAGADO, 112), (13, NAGADO, 104), (14, NAGADO_LO, 108), (15, NAGADO, 112)],
    ]
    for lb in range(25, 33):
        for q, n, v in KD[(lb - 25) % 2]:
            hit(oda if n == ODAIKO else tai, lb, q, n, v)
        for q in range(0, 16, 1 if lb < 29 else 2):     # shime-16en met accenten (opbouw: 8sten, 32: roffel op de kit)
            if lb == 32:
                break
            v = 92 if q % 4 == 0 else (76 if q % 2 == 0 else 62)
            hit(pc, lb, q, SHIME, v + (lb - 25) * 2, 1)
        for q in (5, 9):
            hit(pc, lb, q, KA, 82)
    for lb in (25, 27, 29):
        hit(pc, lb, 0, KIAI, 120)
    hit(kit, 25, 0, CRASH, 104, 8)
    for lb in range(29, 33):                            # opbouw: kick vier op de vloer, in 32 een snareroffel
        for q in (0, 4, 8, 12):
            hit(kit, lb, q, KICK, 112)
    for q in range(16):
        hit(kit, 32, q, SNARE_R, 80 + q * 2, 1)
    hit(pc, 32, 12, KIAI, 122)
    # ---- D: climax
    for lb in range(33, 41):
        groove(lb, double=True)
        hit(oda, lb, 0, ODAIKO, 122)
        if lb % 2 == 0:
            hit(oda, lb, 8, ODAIKO, 114)
    hit(kit, 33, 0, CRASH, 106, 8)
    hit(pc, 33, 0, KIAI, 120)
    hit(pc, 37, 0, KIAI, 118)
    for q, n in ((8, TOM_HI), (10, TOM_HI), (12, TOM_LO), (13, TOM_LO)):
        hit(kit, 40, q, n, 110)
    for q in (14, 15):
        hit(tai, 40, q, NAGADO, 116)
    return {'kit': dedupe(kit), 'oda': dedupe(oda), 'tai': dedupe(tai), 'perc': dedupe(pc)}


# ------------------------------------------------------------------------------- voicegroup -----------------------
KIT = [   # vanaf noot 36: (regel, uitklinktijd/release, lengte van de sample in s; None = geloopt)
    ('voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 150', 0.09),
    ('voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 180', 0.16),
    ('voice_directsound 60, 64, DirectSoundWaveData_hooh_odaiko, 255, 0, 255, 200', 1.05),
    ('voice_directsound 60, 58, DirectSoundWaveData_hooh_nagado, 255, 0, 255, 180', 0.60),
    ('voice_directsound 55, 70, DirectSoundWaveData_hooh_nagado, 255, 0, 255, 180', 0.80),
    ('voice_directsound 60, 76, DirectSoundWaveData_hooh_shime, 255, 0, 255, 90', 0.22),
    ('voice_directsound 60, 50, DirectSoundWaveData_hooh_ka, 255, 0, 255, 80', 0.12),
    ('voice_directsound 57, 64, DirectSoundWaveData_hooh_kiai, 255, 0, 255, 160', 0.42),
    ('voice_directsound 60, 40, DirectSoundWaveData_ethnic_flavours_hyoushigi, 255, 0, 255, 90', 0.36),
    ('voice_directsound 60, 48, DirectSoundWaveData_ethnic_flavours_kotsuzumi, 255, 0, 255, 110', 0.32),
    ('voice_directsound 60, 80, DirectSoundWaveData_ethnic_flavours_ohtsuzumi, 255, 0, 255, 110', 0.47),
    ('voice_directsound_no_resample 60, 54, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 170', None),
    ('voice_directsound 55, 44, DirectSoundWaveData_unused_sc55_tom, 255, 216, 77, 170', None),
    ('voice_directsound 46, 84, DirectSoundWaveData_unused_sc55_tom, 255, 216, 77, 170', None),
    ('voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 150', 0.16),
]
KEYSPLITS = {   # naam: (tabel, [(sample, release)])
    'hooh_shami': ['hooh_shami_%d' % k for k in (52, 59, 66, 73)],
    'hooh_koto': ['hooh_koto_%d' % k for k in (57, 64, 71, 78)],
    'hooh_shaku': ['hooh_shaku_%d' % k for k in (62, 69, 76)],
}
REL = {'hooh_shami': 100, 'hooh_koto': 100, 'hooh_shaku': 110}   # shaku 110: korte staart = legato na detach
VOICES = {
    SHAKU: 'voice_keysplit voicegroup_hooh_shaku_keysplit, keysplit_hooh_shaku',
    KOTO: 'voice_keysplit voicegroup_hooh_koto_keysplit, keysplit_hooh_koto',
    SHAMI: 'voice_keysplit voicegroup_hooh_shami_keysplit, keysplit_hooh_shami',
    SHO: 'voice_directsound 60, 0, DirectSoundWaveData_hooh_sho, 14, 0, 255, 200',
    GTR: 'voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_distortion_guitar_low, 255, 0, 255, 160',
    DRUMS: 'voice_keysplit_all voicegroup_hooh_drumset',
}
ATTACK = {'hooh_shaku': 40}      # shakuhachi: zachte aanzet (±6 frames)


def write_voicegroup():
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: grounded_gm voor Battle! Ho-Oh v2. Gegenereerd door tools/grounded/hooh_theme.py.'
    lines[1] = ('@ eigen samples (hooh_samples.py): 77 shakuhachi, 107 koto, 106 shamisen (keysplits hooh_*), 109 sho, '
                '127 = drumkit hooh; stock: 30 distortion-gitaar, 33 bas, 60 hoorn, 52 koor.')
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
        '@ Project Grounded: drumkit voor Battle! Ho-Oh v2 (hooh_theme.py): 36 kick, 37 snare, 38 odaiko, 39/40 nagado\n'
        '@ (hoog/laag), 41 shime-daiko, 42 ka (rand), 43 kiai, 44 hyoshigi, 45 kotsuzumi, 46 ohtsuzumi, 47 bekken,\n'
        '@ 48/49 toms, 50 orkestsnare (roffels). hooh_* = eigen samples (hooh_samples.py).\n'
        'voice_group hooh_drumset, 36\n' + ''.join('\t%s\n' % k for k, _ in KIT) + '\n')
    for name, samples in KEYSPLITS.items():
        att = ATTACK.get(name, 255)
        open('sound/voicegroups/keysplits/%s.inc' % name, 'w').write(
            '@ Project Grounded: Battle! Ho-Oh v2, %s (hooh_samples.py), tabel keysplit_%s.\n'
            '@ Gegenereerd door tools/grounded/hooh_theme.py.\nvoice_group %s_keysplit\n' % (name, name, name) +
            ''.join('\tvoice_directsound 60, 0, DirectSoundWaveData_%s, %d, 0, 255, %d\n' % (s, att, REL[name])
                    for s in samples))


# ------------------------------------------------------------------------------- bouwen ---------------------------
TRACKS = [   # (naam, programma, volume, pan)
    ('shaku', SHAKU, 124, 64), ('koto', KOTO, 104, 82), ('kotog', KOTO, 92, 76), ('shami', SHAMI, 124, 46),
    ('gtr', GTR, 54, 56), ('bass', BASS, 84, 64), ('horn', HORN, 68, 60), ('sho', SHO, 64, 70),
    ('kit', DRUMS, 88, 64), ('oda', DRUMS, 104, 64), ('tai', DRUMS, 100, 60),
    ('perc', DRUMS, 92, 72), ('hat', NOISE, 30, 64),
]
PSG = {'hat'}
ORDER = ['shaku', 'shami', 'koto', 'oda', 'tai', 'bass', 'kit', 'sho', 'horn', 'kotog', 'gtr', 'perc']
DRUMPARTS = ('kit', 'oda', 'tai', 'perc')
# hoe lang een slag mag doorklinken (16en) voordat de note-off komt; de volgende slag in dezelfde partij kapt eerder
RING = {ODAIKO: 9, NAGADO: 5, NAGADO_LO: 6, SHIME: 1, KA: 1, KIAI: 4, HYOU: 2, KOTSU: 2, OHTSU: 3, KICK: 1, SNARE: 2,
        SNARE_R: 1, CRASH: 4, TOM_HI: 2, TOM_LO: 2}


def tight(ev, tail):
    """tokkels (koto/shamisen): noot + uitklinktijd past precies tot de volgende aanslag (min. 3 ticks)."""
    ev = sorted(ev)
    starts = sorted(set(e[0] for e in ev))
    out = []
    for e in ev:
        nxt = next((t for t in starts if t > e[0]), None)
        end = e[1] if nxt is None else min(e[1], max(e[0] + 2, nxt - tail))
        out.append([e[0], end, e[2], e[3]])
    return out


def ring_gates(notes):
    """elke drumpartij = één speler: een slag klinkt door (RING) tot de volgende slag in dezelfde partij, en wordt
    zó vroeg losgelaten dat de release uitgeklonken is als de volgende slag komt (1 kanaal per partij).
    Bekken en kiai klinken los daarvan uit."""
    notes = sorted(notes)
    free = (CRASH, KIAI)
    starts = sorted({n[0] for n in notes if n[2] not in free})
    out = []
    for n in notes:
        ln = RING.get(n[2], 2) * S16
        if n[2] not in free:
            nxt = next((x for x in starts if x > n[0]), None)
            if nxt is not None:
                r = release_ticks(int(KIT[n[2] - 36][0].rsplit(',', 1)[1]), TPB, BPM) + 1
                ln = min(ln, max(3, nxt - n[0] - r))
        out.append([n[0], n[0] + ln, n[2], n[3]])
    return out


def no_overlap(ev):
    ev = sorted(ev)
    for i, e in enumerate(ev):
        nxt = next((x[0] for x in ev[i + 1:] if x[2] == e[2] and x[0] >= e[0] and x is not e), None)
        if nxt is not None and nxt < e[1]:
            e[1] = max(e[0] + 1, nxt)
    return ev


def build(render_dir=None):
    write_voicegroup()
    rel = releases(VG)
    kt, kg = koto()
    parts = {'shaku': shakuhachi(), 'koto': kt, 'kotog': kg, 'shami': shamisen(), 'gtr': guitar(), 'bass': bass(),
             'horn': horn(), 'sho': sho(), 'hat': hats()}
    parts.update(drums())
    progs = {k: pr for k, pr, _, _ in TRACKS}
    tail = {}
    for k, pr in progs.items():
        tail[k] = 0 if (k in PSG or pr == DRUMS) else release_ticks(rel.get(pr, 200), TPB, BPM) + 2
    for k in ('shaku', 'gtr', 'bass', 'horn', 'sho'):
        parts[k] = detach(parts[k], tail[k])
    for k in ('koto', 'kotog', 'shami'):
        parts[k] = tight(parts[k], tail[k])
    for k in DRUMPARTS:
        parts[k] = ring_gates(parts[k])
    for k in parts:
        parts[k] = no_overlap(parts[k])
    # drums: een kanaal is bezet tot de sample afgelopen is of de release na de note-off uitgeklonken is
    proxy = {}
    for k in DRUMPARTS:
        proxy[k] = []
        for i, (s0, e0, n, v) in enumerate(parts[k]):
            line, slen = KIT[n - 36]
            r = release_ticks(int(line.rsplit(',', 1)[1]), TPB, BPM) + 2
            occ = e0 - s0 + r
            if slen is not None:
                key = int(line.split()[1].rstrip(','))
                ticks = slen * 2 ** ((60 - key) / 12) * BPM / 60 * TPB if 'no_resample' not in line else slen * BPM / 60 * TPB
                occ = min(occ, int(ticks) + 1)
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
        if '-v' in sys.argv and gone:
            from collections import Counter
            print('     ', dict(Counter((e[0] // BAR) - INTRO + 1 for e in parts[k] if e not in kept[k])))
        print('  %-6s %4d noten, %3d vallen weg (%.1f%%)%s' % (k, n, n - len(kept[k]), 100 * (n - len(kept[k])) / max(n, 1),
                                                             ' (maten %s)' % gone[:16] if gone else ''))
        parts[k] = kept[k]
    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    song.tempo(at(1), BPM / 120)
    song.loop = (at(1), END * BAR)
    for ch, (k, prog, vol, pan) in enumerate(TRACKS):
        notes = [[s, e, n + OCT.get(prog, 0), v] for s, e, n, v in sorted(parts[k])]
        extra = shaku_bends(parts[k]) if k == 'shaku' else ()
        song.add(notes, prog, vol, ch, pan, extra=extra)
    song.save(OUT, END * BAR)
    print(OUT, 'intro %.2f s, loop %.1f s' % (INTRO * 4 * 60 / BPM, NLOOP * 4 * 60 / BPM))
    if render_dir:
        render_gm(render_dir)


# ---- offline-render (FluidR3 GM; andere klanken dan de GBA, wel noten/vorm/tempo) ------------------------------------
GM_PROG = {'shaku': 77, 'koto': 107, 'kotog': 107, 'shami': 106, 'gtr': 30, 'bass': 33, 'horn': 60, 'sho': 109,
           'choir': 52, 'hat': 0}
GM_DRUM = {KICK: 36, SNARE: 38, ODAIKO: 35, NAGADO: 41, NAGADO_LO: 43, SHIME: 40, KA: 37, KIAI: 39, HYOU: 75,
           KOTSU: 61, OHTSU: 60, CRASH: 49, TOM_HI: 48, TOM_LO: 45, SNARE_R: 40}


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
