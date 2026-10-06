#!/usr/bin/env python3
"""Project Grounded: Battle! Lugia (MUS_GROUNDED_VS_LUGIA, 657), eigen compositie.

Idee (Jordi): de dualiteit van Lugia. Beschermer van de zee en 'moeder' van de legendarische vogels, maar ook
destructief: één vleugelslag kan een storm van 40 dagen veroorzaken; daarom slaapt hij diep in zee (Whirl Islands).
Jordi (correctie): géén wiegenlied/kinderliedje; de beschermende kant is heldhaftig en nobel.
Daarom één melodie (het 'Beschermersthema') in twee gedaanten:
  - Beschermer: D-groot, breed (halve tellen = een eenheid), hoorns + strijkers + koor, trompetfanfares.
  - Storm: dezelfde tonen in D-klein (F#->F, B->Bb, C# blijft als leidtoon), twee keer zo snel, scherper ritme
    (gepunt -> dubbel gepunt), jagende strijkers-achtsten, taiko/pauken.
144 bpm, 1 maat = 1,67 s.
  Intro (maat 0-3, 6,7 s): zinken naar de diepte (lage strijkers dalen, koor, belletjes van het water), een verre
    hoorn speelt de kop van het thema in mineur (Lugia slaapt); maat 3 = drie reusachtige vleugelslagen (3+3+2).
  A (8 maten) Storm: het thema in mineur.
  B (8 maten) De storm van 40 dagen: de kop van het thema in verkleining, vraag-antwoord hoorns/trompetten,
    vleugelslagen in 3+3+2, windvlagen; stijgt chromatisch (Dm-Ebm-Fm-Gm) naar de climax Bb-C-A; dan stilte + wind.
  C (8 maten) Het oog van de storm = de Beschermer: het thema in groot, breed en nobel; eerst strijkers/koor/hoorn,
    daarna vol met trompetten en pauken.
  D (8 maten) Ontwaken: het tweede deel van het thema in groot op storm-tempo (de beschermer vecht), dan kantelt
    groot naar klein (F# -> F, Bb-akkoord) en hamert de dominant terug naar de storm (loop naar A).
Alleen stock-Emerald-samples; eigen voicegroup grounded_lugia + kit drumsets/lugia.inc + twee keysplits.
Gebruik: python3 tools/grounded/lugia_theme.py [--render <map>]"""
import os, subprocess, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from musiclib import dedupe, detach, allocate, releases, release_ticks, Song

OUT = 'sound/songs/midi/mus_grounded_vs_lugia.mid'
VG = 'grounded_lugia'
TPB, BPM = 96, 144
FAST = 164                                  # v2: C en D (vanaf ±33 s)
E8, S16 = TPB // 2, TPB // 4
BAR = TPB * 4
MAXV = 11                                   # legendary: 11 DirectSound-noten (lint: MAX_PER_SONG)
# programma's (grounded_gm-nummering, eigen invulling in grounded_lugia)
HORN, TPT, SPICC, STR, TIMP, CHOIR, FLUTE, BELL, WIND, BUBBLE, PIZZ = 60, 56, 49, 48, 47, 52, 73, 9, 122, 123, 45
SUB, RAIN, DRUMS, TROLL = 84, 121, 127, 116            # PSG-golf (sub), PSG-ruis (regen/storm), drumkit
KICK, SNARE, TAIKO, TOML, TOMH, CRASH, THUNDER = 36, 37, 38, 39, 40, 41, 42
DLEN = {36: 24, 37: 48, 38: 96, 42: 96}   # echte samplelengte (kick 0,09 s, snare 0,16 s, taiko 0,42 s)
INTRO, A0, B0, C0, D0, END = 0, 4, 12, 20, 28, 36

N = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
     'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def p(name):
    return 12 * (int(name[-1]) + 1) + N[name[:-1]]


# ---- het Beschermersthema (D-groot); eenheid = 1 tel (storm/ontwaken) of 2 tellen (beschermer) ----------------
THEME = [
    [('D5', 1.5), ('A4', .5), ('D5', 1), ('E5', 1)], [('F#5', 2), ('E5', 1), ('D5', 1)],
    [('B4', 1.5), ('C#5', .5), ('D5', 1), ('B4', 1)], [('A4', 4)],
    [('G5', 1.5), ('F#5', .5), ('E5', 1), ('B4', 1)], [('C#5', 1.5), ('D5', .5), ('E5', 1), ('A5', 1)],
    [('F#5', 1.5), ('E5', .5), ('D5', 1), ('C#5', 1)], [('D5', 4)],
]
# akkoorden per halve maat (thema-maat)
MAJ = [('D', 'A'), ('Bm', 'G'), ('G', 'Em'), ('A', 'A'), ('Em', 'Em'), ('A', 'A'), ('D', 'A'), ('D', 'D')]
MIN = [('Dm', 'A'), ('Dm', 'Bb'), ('Gm', 'A'), ('A', 'A'), ('Gm', 'Gm'), ('A', 'A'), ('Dm', 'A'), ('Dm', 'Dm')]
CH = {'D': ('D', 'F#', 'A'), 'Dm': ('D', 'F', 'A'), 'A': ('A', 'C#', 'E'), 'Bm': ('B', 'D', 'F#'),
      'G': ('G', 'B', 'D'), 'Gm': ('G', 'Bb', 'D'), 'Em': ('E', 'G', 'B'), 'Bb': ('Bb', 'D', 'F'),
      'C': ('C', 'E', 'G'), 'Ebm': ('Eb', 'Gb', 'Bb'), 'Fm': ('F', 'Ab', 'C'), 'Eb': ('Eb', 'G', 'Bb')}
TO_MINOR = {'F#': 'F', 'B': 'Bb'}


def minor(name):
    return TO_MINOR.get(name[:-1], name[:-1]) + name[-1]


def bass_root(ch):
    """grondtoon van een akkoord in D2..C#3 (laag, maar >= E1)."""
    pc = N[CH[ch][0]]
    return 36 + pc if pc >= 2 else 48 + pc


def voicing(ch, lo=p('F#3')):
    """drieklank boven lo (voor koor/strijkers)."""
    out = []
    for name in CH[ch]:
        n = N[name]
        while n < lo:
            n += 12
        out.append(n)
    return sorted(out)


def melody(bars, t0, unit, vel, storm=False, shift=0, minor_mode=False):
    """thema-maten -> noten; storm = dubbel gepunt (1.5+.5 -> 1.75+.25)."""
    out, t = [], t0
    for bar in bars:
        prev_dot = False
        for name, d in bar:
            dd = d
            if storm and d == 1.5:
                dd = 1.75
            elif storm and d == .5 and prev_dot:
                dd = .25
            prev_dot = d == 1.5
            n = p(minor(name) if minor_mode else name) + shift
            ln = int(dd * unit)
            out.append([t, t + ln, n, vel])
            t += ln
    return out


def build():
    P = {k: [] for k in ('horn', 'tpt', 'spicc', 'str', 'timp', 'troll', 'choir', 'flute', 'bell', 'wind', 'bubble', 'pizz',
                         'drums', 'sub', 'rain')}
    W = {'wind': []}       # extra events (pitch bend) per partij
    bend = []              # (tick, pitchwheel) voor de wind

    def hit(t, notes, vel, ln):
        P['drums'].extend([[t, t + min(ln, DLEN.get(n, ln)), n, vel] for n in notes])

    def ostinato(bar, ch, vel, accents=(), major=False, pattern=(0, 0, 12, 0, 7, 0, 12, 7)):
        r = bass_root(ch)
        for i, iv in enumerate(pattern):
            t = bar * BAR + i * E8
            P['spicc'].append([t, t + E8 - 10, r + iv, min(127, vel + (22 if i in accents else 0))])

    def half_bar_chords(bar, chords):
        return [(bar * BAR, chords[0]), (bar * BAR + 2 * TPB, chords[1])]

    def wing(t0, vel=120, steps=(0, 3, 6)):
        """drie vleugelslagen (3+3+2 achtsten): taiko + kick + pauk + laag strijkersaccent."""
        for st in steps:
            t = t0 + st * E8
            hit(t, (TAIKO, KICK), vel, TPB)
            P['timp'].append([t, t + E8, p('D2') if st != 6 else p('A2'), vel])

    def gust(t0, length, peak=64):
        """windvlaag: windsample met pitch bend omhoog en weer omlaag."""
        P['wind'].append([t0, t0 + length, 60, peak])
        steps = length // 24
        for i in range(steps + 1):
            x = i / steps
            semis = -6 + 14 * x if x < .6 else 2.4 - 12 * (x - .6)
            bend.append((t0 + i * 24, max(-8192, min(8191, round(8192 * semis / 12)))))

    # ======================= INTRO: zinken (maat 0-3) =====================================================
    # dalende lage strijkers + koor; belletjes van het water
    for i, n in enumerate(('D3', 'C3', 'Bb2', 'A2')):
        t = (i * 2) * TPB
        P['str'].append([t, t + 2 * TPB - 6, p(n), 72 + i * 4])
    for i, n in enumerate(('A3', 'G3', 'F3', 'E3')):
        t = (i * 2) * TPB
        P['choir'].append([t, t + 2 * TPB - 6, p(n), 64 + i * 4])
    for i, n in enumerate((84, 79, 76, 72, 67, 64)):
        t = i * 52 + 20
        P['bubble'].append([t, t + 40, n, 70 - i * 5])
    P['sub'] += [[0, 2 * BAR - 8, p('D3'), 70]]
    # maat 2: diep in zee; een verre hoorn speelt de kop van het thema in mineur (Lugia slaapt)
    t2 = 2 * BAR
    P['str'] += [[t2, t2 + BAR - 6, p('D2'), 80], [t2, t2 + BAR - 6, p('A2'), 70]]
    P['horn'] += melody([THEME[0]], t2, TPB, 74, minor_mode=True, shift=-12)
    P['bubble'] += [[t2 + 3 * TPB + i * 30, t2 + 3 * TPB + i * 30 + 30, 60 + i * 5, 60] for i in range(3)]
    # maat 3: drie reusachtige vleugelslagen (3+3+2), wind, pauken-roffel, strijkers scheuren omhoog
    t3 = 3 * BAR
    wing(t3, 112)
    gust(t3, BAR, 76)
    P['troll'] += [[t3 + 7 * E8 + i * S16 // 2, t3 + 7 * E8 + (i + 1) * S16 // 2, p('A2'), 70 + i * 12] for i in range(4)]
    P['spicc'] += [[t3 + 6 * E8 + i * S16 // 2 * 1, t3 + 6 * E8 + (i + 1) * (S16 // 2) - 2, p('A2') + [0, 2, 3, 5, 7, 9, 10, 12][i], 70 + i * 6]
                   for i in range(8)]
    P['choir'] += [[t3, t3 + 3 * E8 - 6, p('A3'), 90], [t3, t3 + 3 * E8 - 6, p('D4'), 84],
                   [t3 + 3 * E8, t3 + 6 * E8 - 6, p('Bb3'), 96], [t3 + 3 * E8, t3 + 6 * E8 - 6, p('D4'), 90]]
    P['drums'] += [[t3 + 6 * E8 + i * S16, t3 + 6 * E8 + i * S16 + 12, SNARE, 70 + i * 12] for i in range(4)]

    # ======================= A: Storm (thema in mineur, 1 tel = eenheid) =================================
    P['horn'] += melody(THEME, A0 * BAR, TPB, 116, storm=True, minor_mode=True, shift=-12)
    P['tpt'] += melody(THEME[4:], (A0 + 4) * BAR, TPB, 104, storm=True, minor_mode=True)
    for k in range(8):
        b = A0 + k
        ch2 = MIN[k]
        if k == 3:                                      # hamerende dominant
            ostinato(b, 'A', 104, accents=(0, 3, 6), pattern=(0, 0, 0, 12, 0, 0, 12, 12))
        else:
            ostinato(b, ch2[0], 100, accents=(0, 4))
        for t, ch in half_bar_chords(b, ch2):
            P['choir'] += [[t, t + 2 * TPB - 8, n, 84] for n in voicing(ch, p('A3'))[-2:]]
            P['sub'].append([t, t + 2 * TPB - 8, bass_root(ch) + 12, 96])
        t0 = b * BAR
        hit(t0, (TAIKO, KICK), 118, TPB)
        hit(t0 + 2 * TPB, (TAIKO, KICK), 108, TPB)
        hit(t0 + TPB, (SNARE,), 96, E8)
        hit(t0 + 3 * TPB, (SNARE,), 100, E8)
        if k >= 4:
            P['drums'] += [[t0 + 3 * TPB + E8 + i * S16 // 1 * 0 + i * (E8 // 2), t0 + 3 * TPB + E8 + (i + 1) * (E8 // 2), SNARE, 70 + i * 14]
                           for i in range(2)]
        P['timp'] += [[t0, t0 + E8, bass_root(ch2[0]) + 12 if bass_root(ch2[0]) < p('F2') else bass_root(ch2[0]), 116],
                      [t0 + 2 * TPB, t0 + 2 * TPB + E8, bass_root(ch2[1]) if bass_root(ch2[1]) >= p('F2') else bass_root(ch2[1]) + 12, 104]]
        if k in (0, 4):
            hit(t0, (CRASH,), 112, 2 * TPB)
        P['rain'] += [[t0 + i * S16, t0 + i * S16 + 10, 70, 46 if i % 4 else 64] for i in range(16)]

    # ======================= B: de storm van 40 dagen ===================================================
    SEQ = ['Dm', 'Ebm', 'Fm', 'Gm']
    head = [('D5', 1.5), ('A4', .5), ('D5', 1), ('E5', 1)]       # in achtsten = verkleining
    for k, ch in enumerate(SEQ):
        b = B0 + k
        t0 = b * BAR
        sh = N[CH[ch][0]] - N['D']
        P['horn'] += melody([[(minor(n), d) for n, d in head]], t0, E8, 118, storm=True, shift=sh - 12)
        P['tpt'] += melody([[(minor(n), d) for n, d in head]], t0 + 2 * TPB, E8, 108, storm=True, shift=sh)
        ostinato(b, ch, 100, accents=(0, 3, 6))
        wing(t0, 116)
        P['choir'] += [[t0, t0 + 3 * E8 - 8, n, 92] for n in voicing(ch, p('A3'))[-2:]]
        P['choir'] += [[t0 + 3 * E8, t0 + BAR - 8, n, 96] for n in voicing(ch, p('A3'))[-2:]]
        P['sub'].append([t0, t0 + BAR - 8, bass_root(ch) + 12, 100])
        hit(t0 + TPB, (SNARE,), 100, E8)
        hit(t0 + 3 * TPB, (SNARE,), 104, E8)
        if k % 2 == 0:
            gust(t0, 2 * BAR, 80)
            hit(t0, (THUNDER,), 104, 2 * TPB)
        P['rain'] += [[t0 + i * S16, t0 + i * S16 + 14, 72, 56 if i % 4 else 74] for i in range(16)]
    # climax Bb - C - A - A(stop)
    CLIM = [('Bb', [('D5', 1.75), ('C5', .25), ('Bb4', 1), ('F5', 1)]),
            ('C', [('E5', 1.75), ('D5', .25), ('C5', 1), ('G5', 1)]),
            ('A', [('C#5', 1.5), ('D5', .5), ('E5', 1), ('A5', 1)])]
    for k, (ch, mel) in enumerate(CLIM):
        b = B0 + 4 + k
        t0 = b * BAR
        P['tpt'] += melody([mel], t0, TPB, 118)
        P['horn'] += melody([mel], t0, TPB, 118, shift=-12)
        ostinato(b, ch, 108, accents=(0, 2, 4, 6))
        P['choir'] += [[t0 + h * 2 * TPB, t0 + h * 2 * TPB + 2 * TPB - 8, n, 104] for h in (0, 1)
                       for n in voicing(ch, p('C4'))[-2:]]
        P['sub'] += [[t0, t0 + BAR - 8, bass_root(ch) + 12, 104]]
        hit(t0, (CRASH, TAIKO, KICK), 122, 2 * TPB)
        hit(t0 + 2 * TPB, (TAIKO, KICK), 114, TPB)
        hit(t0 + TPB, (SNARE,), 106, E8)
        hit(t0 + 3 * TPB, (SNARE,), 110, E8)
        P['timp'] += [[t0 + i * TPB, t0 + i * TPB + E8, bass_root(ch) + (12 if bass_root(ch) < p('F2') else 0), 118]
                      for i in range(4)]
        P['rain'] += [[t0 + i * S16, t0 + i * S16 + 14, 74, 60 if i % 4 else 80] for i in range(16)]
    gust((B0 + 4) * BAR, 3 * BAR, 88)
    t0 = (B0 + 6) * BAR + 3 * TPB                    # v2: tomfill aan het eind van de climax (start opbouw)
    for i, n in enumerate((TOMH, TOML, TOMH, TOML)):
        hit(t0 + i * S16, (n,), 100 + i * 5, S16)
    # maat 7 van B: tutti-slag op A, dan valt alles weg: wind + uitstervende paukenroffel (het oog van de storm)
    t0 = (B0 + 7) * BAR
    P['tpt'].append([t0, t0 + TPB, p('A5'), 120])
    P['horn'] += [[t0, t0 + TPB, p('A4'), 120], [t0, t0 + TPB, p('E4'), 110]]
    P['spicc'].append([t0, t0 + E8, p('A2'), 120])
    hit(t0, (CRASH, TAIKO, KICK), 124, 2 * TPB)
    # v2 (Jordi: 'tempo omhoog tussen 30 en 40 s, opbouwen met goed drumgebruik'): geen stilte meer maar een
    # drumopbouw die versnelt (achtsten taiko/toms -> 16en toms -> 32ste snareroffel) terwijl het tempo stijgt;
    # de pauk rolt aanzwellend i.p.v. uitstervend, de strijkers jagen omhoog naar de D van C.
    t1 = t0 + TPB
    hit(t1, (TAIKO, KICK), 96, TPB)
    hit(t1 + E8, (TOML,), 92, E8)
    t2 = t0 + 2 * TPB
    for i, n in enumerate((TOMH, TOMH, TOML, TOML)):
        hit(t2 + i * S16, (n,), 96 + i * 4, S16)
    hit(t2, (TAIKO, KICK), 104, TPB)
    hit(t2 + E8, (TAIKO,), 100, TPB)
    t3 = t0 + 3 * TPB
    P['drums'] += [[t3 + i * (S16 // 2), t3 + (i + 1) * (S16 // 2), SNARE, 84 + i * 5] for i in range(8)]
    hit(t3, (TAIKO, KICK), 112, E8)
    hit(t3 + E8, (TAIKO, KICK), 118, E8)
    P['troll'] += [[t1 + i * S16, t1 + (i + 1) * S16, p('A2'), min(124, 60 + i * 6)] for i in range(12)]
    P['spicc'] += [[t2 + i * S16, t2 + (i + 1) * S16 - 4, n, 84 + i * 4] for i, n in enumerate(
        (p('A2'), p('B2'), p('C#3'), p('D3'), p('E3'), p('F#3'), p('G3'), p('A3')))]
    gust(t0, BAR, 88)
    P['str'].append([t0 + TPB, t0 + BAR - 6, p('A3'), 80])

    # ======================= C: de Beschermer (thema in groot, breed: 2 tellen = eenheid) =================
    P['horn'] += melody(THEME[:4], C0 * BAR, 2 * TPB, 112, shift=-12)       # hoorns breed
    P['str'] += melody(THEME[:4], C0 * BAR, 2 * TPB, 92)                     # strijkers in octaven met de hoorn
    for k in range(8):
        b = C0 + k
        t0 = b * BAR
        ch = MAJ[k // 2][k % 2]
        full = k >= 4
        # koor: brede drieklank in stukken van 2 tellen
        P['choir'] += [[t0 + h * 2 * TPB, t0 + h * 2 * TPB + 2 * TPB - 8, n, 86 if not full else 100]
                       for h in (0, 1) for n in voicing(ch, p('A3'))[-2:]]
        # pizzicato-bas en zachte 'mars' (gezag, geen wiegje): grondtoon op 1 en 3, kwint op 2 en 4
        r = bass_root(ch)
        P['pizz'] += [[t0 + i * TPB, t0 + i * TPB + E8, r + (7 if i % 2 else 0), 104] for i in range(4)]
        P['sub'] += [[t0, t0 + 2 * TPB - 8, r + 12, 80], [t0 + 2 * TPB, t0 + BAR - 8, r + 12, 80]]
        hit(t0, (TAIKO,), 92 if not full else 108, TPB)
        if not full:                                 # v2: zachte puls, zodat het hogere tempo doorloopt
            hit(t0 + 2 * TPB, (KICK,), 84, TPB)
            hit(t0 + 3 * TPB, (SNARE,), 70, E8)
            if k == 3:
                for i, n in enumerate((TOMH, TOMH, TOML, TOML)):
                    hit(t0 + 3 * TPB + i * S16, (n,), 80 + i * 6, S16)
        P['timp'].append([t0, t0 + E8, r + (12 if r < p('F2') else 0), 90 if not full else 110])
        if full:
            hit(t0 + 2 * TPB, (TAIKO, KICK), 100, TPB)
            hit(t0 + TPB, (SNARE,), 80, E8)
            hit(t0 + 3 * TPB, (SNARE,), 84, E8)
            ostinato(b, ch, 84, pattern=(0, 12, 7, 12, 0, 12, 7, 12))
        # trompetfanfare in de rusten van de melodie (eind van frase: maat 1, 3, 5, 7 tweede helft)
        if k in (1, 5):
            tri = voicing(ch, p('D4'))
            P['tpt'] += [[t0 + 2 * TPB, t0 + 2 * TPB + E8 - 6, tri[0], 96], [t0 + 2 * TPB + E8, t0 + 3 * TPB - 6, tri[1], 100],
                         [t0 + 3 * TPB, t0 + BAR - 8, tri[2], 108]]
        if k in (0, 4):
            hit(t0, (CRASH,), 92 if not full else 116, 2 * TPB)
            # Silver Wing: zilveren glinstering
            P['bell'] += [[t0 + 2 * TPB + i * E8, t0 + 2 * TPB + i * E8 + E8, n, 70] for i, n in enumerate(
                (p('A6'), p('F#6'), p('D6'), p('A5')))]
    # opbouw naar D: snareroffel in de laatste maat
    t0 = (C0 + 7) * BAR
    P['drums'] += [[t0 + 2 * TPB + i * S16, t0 + 2 * TPB + i * S16 + 12, SNARE, 64 + i * 7] for i in range(8)]
    P['flute'] += [[t0 + 2 * TPB + i * S16, t0 + 2 * TPB + (i + 1) * S16 - 4, n, 84] for i, n in enumerate(
        (p('A4'), p('C#5'), p('E5'), p('G5'), p('A5'), p('C#6'), p('E6'), p('A6')))]

    # ======================= D: Ontwaken (deel 2 van het thema, storm-tempo, groot -> klein) ===============
    seq = [THEME[4], THEME[5], THEME[6], THEME[7], THEME[4], THEME[5]]
    P['horn'] += melody(seq, D0 * BAR, TPB, 116, shift=-12)
    P['tpt'] += melody(seq, D0 * BAR, TPB, 110)
    P['str'] += melody(seq, D0 * BAR, TPB, 80, shift=12)
    # de kanteling: F# wordt F (Bb-akkoord), daarna de dominant hameren
    flip = [[('F5', 1.5), ('E5', .5), ('D5', 1), ('C#5', 1)]]
    P['horn'] += melody(flip, (D0 + 6) * BAR, TPB, 120, shift=-12)
    P['tpt'] += melody(flip, (D0 + 6) * BAR, TPB, 116)
    DCH = [('Em', 'Em'), ('A', 'A'), ('D', 'A'), ('D', 'D'), ('Em', 'G'), ('A', 'A'), ('Bb', 'A'), ('A', 'A')]
    for k in range(8):
        b = D0 + k
        t0 = b * BAR
        chs = DCH[k]
        if k == 7:
            ostinato(b, 'A', 112, accents=(0, 2, 4, 6), pattern=(0, 0, 0, 0, 12, 12, 12, 12))
            P['horn'] += [[t0 + i * E8, t0 + i * E8 + E8 - 12, p('A3'), 100 + i * 3] for i in range(8)]
            P['tpt'] += [[t0 + i * E8, t0 + i * E8 + E8 - 12, p('E4') if i < 4 else p('A4'), 96 + i * 4] for i in range(8)]
            P['troll'] += [[t0 + i * S16, t0 + (i + 1) * S16, p('A2'), 70 + i * 3] for i in range(16)]
            P['choir'] += [[t0, t0 + BAR - 8, n, 104] for n in (p('C#4'), p('E4'))]
            P['sub'].append([t0, t0 + BAR - 8, p('A2'), 104])
            hit(t0, (CRASH, TAIKO, KICK), 120, 2 * TPB)
            wing(t0 + 2 * TPB, 118, steps=(0, 3))
            P['drums'] += [[t0 + 2 * TPB + i * S16, t0 + 2 * TPB + i * S16 + 12, SNARE, 80 + i * 5] for i in range(8)]
            gust(t0, BAR, 84)
            continue
        ostinato(b, chs[0], 96, accents=(0, 4), pattern=(0, 12, 7, 12, 0, 12, 7, 12) if k < 6 else (0, 0, 12, 0, 7, 0, 12, 7))
        for t, ch in half_bar_chords(b, chs):
            P['choir'] += [[t, t + 2 * TPB - 8, n, 96] for n in voicing(ch, p('A3'))[-2:]]
            P['sub'].append([t, t + 2 * TPB - 8, bass_root(ch) + 12, 96])
        hit(t0, (TAIKO, KICK), 116, TPB)
        hit(t0 + 2 * TPB, (TAIKO, KICK), 106, TPB)
        hit(t0 + TPB, (SNARE,), 94, E8)
        hit(t0 + 3 * TPB, (SNARE,), 98, E8)
        r = bass_root(chs[0])
        P['timp'] += [[t0, t0 + E8, r + (12 if r < p('F2') else 0), 112]]
        if k in (0, 4, 6):
            hit(t0, (CRASH,), 116, 2 * TPB)
        if k == 6:
            hit(t0, (THUNDER,), 110, 2 * TPB)
            gust(t0, BAR, 74)
            P['rain'] += [[t0 + i * S16, t0 + i * S16 + 14, 72, 56 if i % 4 else 72] for i in range(16)]
    t7 = (D0 + 7) * BAR
    P['rain'] += [[t7 + i * S16, t7 + i * S16 + 14, 74, 60 if i % 4 else 80] for i in range(16)]

    for k in P:
        P[k] = dedupe(P[k])

    write_voicegroup()
    rel = releases(VG)
    progs = {'horn': HORN, 'tpt': TPT, 'spicc': SPICC, 'str': STR, 'timp': TIMP, 'choir': CHOIR, 'flute': FLUTE,
             'bell': BELL, 'wind': WIND, 'bubble': BUBBLE, 'pizz': PIZZ, 'troll': TROLL}
    tail = {k: release_ticks(rel.get(pr, 200), TPB, BPM) + 2 for k, pr in progs.items()}   # C/D op 164 bpm: met FAST gerekend valt in C/D niets extra weg (v2)
    tail['drums'] = 0
    for k in ('horn', 'tpt', 'str', 'choir', 'flute'):
        P[k] = detach(P[k], tail[k])
    order = ['horn', 'tpt', 'drums', 'spicc', 'timp', 'troll', 'wind', 'flute', 'str', 'choir', 'pizz', 'bell', 'bubble']
    ds = {k: P[k] for k in order}
    kept = allocate(ds, order, tail, max_voices=MAXV)
    for k in order:
        n = len(ds[k])
        if n:
            print('  %-7s %4d noten, %3d weg (%.0f%%)' % (k, n, n - len(kept[k]), 100 * (n - len(kept[k])) / n))
            if os.environ.get('LUGIA_DEBUG'):
                kk = {tuple(e) for e in kept[k]}
                print('     weg op maat:', [round(e[0] / BAR, 2) for e in ds[k] if tuple(e) not in kk])
        P[k] = kept[k]

    song = Song(TPB, 500000)
    song.tempo(0, BPM / 120)
    # v2: accelerando 144 -> 164 bpm over de climax en de drumopbouw (maat 18-19 = 30-33 s); C en D op 164.
    for i, b in enumerate((146, 148, 150, 153, 156, 159, 162)):
        song.tempo((B0 + 6) * BAR + (i + 1) * TPB, b / 120)
    song.tempo(C0 * BAR, FAST / 120)
    song.tempo(A0 * BAR, BPM / 120)                 # terugsprong naar A: weer 144
    song.loop = (A0 * BAR, END * BAR)
    extra_wind = [(0, mido.Message('control_change', control=20, value=12))] + \
                 [(t, mido.Message('pitchwheel', pitch=v)) for t, v in bend]
    global TRACKS
    TRACKS = [('horn', HORN, 110, 64), ('tpt', TPT, 92, 70), ('spicc', SPICC, 96, 56), ('str', STR, 84, 64),
              ('timp', TIMP, 104, 64), ('troll', TROLL, 96, 64), ('choir', CHOIR, 80, 64), ('flute', FLUTE, 80, 72), ('bell', BELL, 60, 80),
              ('wind', WIND, 70, 64), ('bubble', BUBBLE, 70, 50), ('pizz', PIZZ, 100, 60),
              ('sub', SUB, 52, 64), ('rain', RAIN, 30, 64), ('drums', DRUMS, 108, 64)]
    free = [c for c in range(16) if c != 9]
    for k, prog, vol, pan in TRACKS:
        ch = 9 if prog == DRUMS else free.pop(0)
        song.add(P[k], prog, vol, ch, pan, extra=extra_wind if k == 'wind' else ())
    written = {k for k, *_ in TRACKS}
    assert not [k for k in P if P[k] and k not in written], 'partij niet weggeschreven'
    song.save(OUT, END * BAR)
    print(OUT)


KIT = [
    'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 200',          # 36
    'voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 200',   # 37
    'voice_directsound 54, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180',                          # 38 taiko laag
    'voice_directsound 45, 58, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 204',                       # 39 tom laag
    'voice_directsound 52, 70, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 204',                       # 40 tom hoog
    'voice_directsound_no_resample 30, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 216',  # 41
    'voice_directsound_no_resample 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165',      # 42 donder
]


def write_voicegroup():
    open('sound/voicegroups/keysplits/lugia_spicc.inc', 'w').write(
        '@ Project Grounded: jagende strijkers (harde aanzet, kort) voor Battle! Lugia (lugia_theme.py).\n'
        'voice_group lugia_spicc_keysplit\n' + ''.join(
            '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_string_ensemble_%d, 255, 200, 40, 120\n' % k
            for k in (60, 72, 84)) + '\n')
    open('sound/voicegroups/keysplits/lugia_strings.inc', 'w').write(
        '@ Project Grounded: brede strijkers (zachte aanzet) voor Battle! Lugia (lugia_theme.py).\n'
        'voice_group lugia_strings_keysplit\n' + ''.join(
            '\tvoice_directsound 60, 0, DirectSoundWaveData_sc88pro_string_ensemble_%d, 60, 0, 255, 170\n' % k
            for k in (60, 72, 84)) + '\n')
    open('sound/voicegroups/drumsets/lugia.inc', 'w').write(
        '@ Project Grounded: drumkit voor Battle! Lugia (lugia_theme.py): 36 kick, 37 orkestsnare, 38 taiko,\n'
        '@ 39/40 toms, 41 orkestbekken, 42 donder (trinity crash). Alleen stock-samples, geen PSG.\n'
        'voice_group lugia_drumset, 36\n' + ''.join('\t%s\n' % k for k in KIT) + '\n')
    over = {
        HORN: 'voice_keysplit voicegroup_french_horn_keysplit, keysplit_french_horn',
        TPT: 'voice_keysplit voicegroup_trumpet_keysplit, keysplit_trumpet',
        SPICC: 'voice_keysplit voicegroup_lugia_spicc_keysplit, keysplit_strings',
        STR: 'voice_keysplit voicegroup_lugia_strings_keysplit, keysplit_strings',
        TIMP: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 200',
        CHOIR: 'voice_directsound 60, 0, DirectSoundWaveData_classical_choir_voice_ahhs, 128, 0, 255, 165',
        FLUTE: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_flute, 255, 127, 231, 127',
        BELL: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_glockenspiel, 255, 165, 51, 190',
        WIND: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_wind, 14, 0, 255, 200',
        BUBBLE: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_bubbles, 255, 0, 255, 150',
        PIZZ: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_pizzicato_strings, 255, 216, 0, 140',
        SUB: 'voice_programmable_wave_alt 60, 0, ProgrammableWaveData_1, 0, 7, 15, 0',
        RAIN: 'voice_noise_alt 60, 0, 0, 0, 2, 0, 0',
        DRUMS: 'voice_keysplit_all voicegroup_lugia_drumset',
        TROLL: 'voice_directsound 60, 0, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 90',   # roffel: kort
    }
    lines = open('sound/voicegroups/grounded_gm.inc').read().split('\n')
    lines[0] = '@ Project Grounded: voicegroup voor Battle! Lugia (grounded_gm + eigen strijkers/kit/wind).'
    lines[1] = '@ Gegenereerd door tools/grounded/lugia_theme.py.'
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


# ---- offline-render (FluidR3 GM; benadering van noten/vorm/tempo, niet van de GBA-klank) -------------------
GM_PROG = {TROLL: 47, HORN: 60, TPT: 56, SPICC: 48, STR: 49, TIMP: 47, CHOIR: 52, FLUTE: 73, BELL: 9, WIND: 122, BUBBLE: 122,
           PIZZ: 45, SUB: 38, RAIN: 122}
GM_DRUM = {KICK: 36, SNARE: 38, TAIKO: 41, TOML: 43, TOMH: 48, CRASH: 49, THUNDER: 57}


def render_gm(outdir):
    m = mido.MidiFile(OUT)
    gm = mido.MidiFile(type=1, ticks_per_beat=m.ticks_per_beat)
    gm.tracks.append(m.tracks[0])
    for src in m.tracks[1:]:
        t = mido.MidiTrack()
        drum = any(x.type == 'program_change' and x.channel == 9 for x in src)
        for x in src:
            if x.type == 'program_change':
                x = x.copy(program=0 if drum else GM_PROG.get(x.program, x.program))
            elif drum and x.type in ('note_on', 'note_off'):
                x = x.copy(note=GM_DRUM.get(x.note, x.note))
            t.append(x)
        gm.tracks.append(t)
    os.makedirs(outdir, exist_ok=True)
    mid = os.path.join(outdir, 'lugia_gm.mid')
    gm.save(mid)
    wav = os.path.join(outdir, 'lugia_fluidr3.wav')
    subprocess.run(['fluidsynth', '-ni', '-g', '0.6', '-r', '44100', '-F', wav, '/usr/share/sounds/sf2/FluidR3_GM.sf2', mid],
                   check=True, capture_output=True)
    mp3 = os.path.join(outdir, 'lugia_fluidr3.mp3')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-b:a', '160k', mp3], check=True)
    os.remove(wav)
    print('render:', mp3)


if __name__ == '__main__':
    build()
    if '--render' in sys.argv:
        render_gm(sys.argv[sys.argv.index('--render') + 1])
